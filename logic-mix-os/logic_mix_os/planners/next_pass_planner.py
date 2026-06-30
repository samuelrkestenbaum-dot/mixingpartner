"""Next-pass planner.

Distills everything into at most five prioritised moves, ordered by the house
bias: vocal belief, then contrast, then loop/width control, then depth cleanup,
then targeted fixes. Also provides the creative-hypothesis stub (build packet 8).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from ..constants import LOOP_SAMPLE_KINDS

FORWARD = {"intimate", "foreground"}

# P-008 — the OUTCOME side of the learning loop. The planner can be made
# history-aware, opt-in and bounded: a move recorded as having made things worse
# (and that we recommended last pass) is *demoted* (never deleted), and revert
# candidates surface as a single conservative move. The recorded history speaks
# two vocabularies — ``got_worse`` / ``revert_candidates`` are score-delta strings
# keyed by ``memory.SCORE_KEYS`` (e.g. ``"section_contrast_score 70->62"``) while
# ``next_recommended`` is a list of prior move *titles*. ``_MOVE_TARGET`` is the
# one piece of glue that bridges the two: it maps a move title to the score key it
# is meant to improve. Titles with no unambiguous target map to nothing and are
# left untouched (conservative). Pairings are pinned against ``memory.SCORE_KEYS``.
_MOVE_TARGET: Dict[str, str] = {
    "Vocal belief": "vocal_centrality_score",
    "Section contrast": "section_contrast_score",
    "Stereo loop / width control": "depth_hierarchy_score",
    "Depth cleanup": "depth_hierarchy_score",
    # "Low-end definition" and the "Establish the emotional centre" fallback have
    # no unambiguous SCORE_KEYS target → deliberately absent (never demoted).
}

# Fixed, bounded priority penalty for a recommended-and-regressed move. Floored so
# a demoted priority never goes negative; strictly a reorder, never a deletion.
HISTORY_DEMOTE = 40

# Fixed priority for the single surfaced "Revert last pass" move. Set above the
# normal candidate band (90 = top vocal move) so a recorded regression worth
# reverting is shown prominently rather than buried below the take-5 cut. It is
# still only a reorder/annotation — a revert is non-destructive (undo your own
# last change), never a manufactured destructive or doctrine-vetoed action.
HISTORY_REVERT_PRIORITY = 95

# P-010 — the CROSS-SONG coherence axis. An opt-in ``album_context`` (per-song
# deltas vs the album means) lets an album-outlier song earn ONE bounded,
# non-destructive, evidence-tagged next-pass item. The thresholds mirror
# ``album.py``'s outlier test verbatim (brightness delta > 0.15 at album.py:61,
# lufs delta > 3 at album.py:63) but are pinned as local constants so the planner
# never depends on ``album.py`` (the delta is derived in the consumer). The fixed
# priority 45 sits below every truth-driven move (Vocal 90, Section 80, Width 70,
# Depth 60, Low-end 50) so the album hint can NEVER outrank a song-truth move.
ALBUM_BRIGHTNESS_OUTLIER = 0.15
ALBUM_LUFS_OUTLIER = 3
ALBUM_OUTLIER_PRIORITY = 45


def _album_outlier_item(album_context: Dict) -> Optional[Tuple[int, Dict]]:
    """Pure, deterministic album-coherence hint from a per-song delta dict.

    ``album_context`` shape: ``{"brightness_delta": float|None, "lufs_delta":
    float|None}``. A ``None`` axis is skipped. Returns ONE bounded, advisory,
    reversible ``(ALBUM_OUTLIER_PRIORITY, item)`` tuple when an axis exceeds its
    threshold, else ``None``. If BOTH axes trip, the deterministic tie-break is
    brightness before loudness. No time / I/O / randomness; a pure function of the
    supplied deltas and the two fixed thresholds.
    """
    if not album_context:
        return None

    bd = album_context.get("brightness_delta")
    ld = album_context.get("lufs_delta")

    bright_trips = bd is not None and abs(bd) > ALBUM_BRIGHTNESS_OUTLIER
    loud_trips = ld is not None and abs(ld) > ALBUM_LUFS_OUTLIER

    if bright_trips:
        field = "brightness_delta"
        value = bd
        threshold = ALBUM_BRIGHTNESS_OUTLIER
        direction = "brighter" if bd > 0 else "darker"
        detail = (
            f"This song sits {value:+} {direction} than the album average "
            f"({field}={value:+}). Consider matching the record's tonal centre — "
            f"a gentle high-shelf / match-EQ toward the album, reversibly, before "
            f"committing."
        )
    elif loud_trips:
        field = "lufs_delta"
        value = ld
        threshold = ALBUM_LUFS_OUTLIER
        direction = "louder" if ld > 0 else "quieter"
        detail = (
            f"This song sits {value:+} LU {direction} than the album average "
            f"({field}={value:+}). Consider matching the record's loudness centre — "
            f"adjust the bus/output level toward the album, reversibly, before "
            f"committing."
        )
    else:
        return None

    item = {
        "title": "Album coherence",
        "detail": detail,
        "evidence": (
            f"album outlier: {field}={value:+} vs album mean "
            f"(threshold {threshold})"
        ),
    }
    return (ALBUM_OUTLIER_PRIORITY, item)


def _score_key(delta: str) -> str:
    """Extract the SCORE_KEYS member from a score-delta string.

    ``"section_contrast_score 70->62"`` → ``"section_contrast_score"`` (split on
    the first space). Strings without a space pass through unchanged.
    """
    return delta.split(" ", 1)[0]


def _apply_history(
    candidates: List[Tuple[int, Dict]], last: Dict
) -> List[Tuple[int, Dict]]:
    """Pure, deterministic reprioritizer driven by the most recent pass.

    Demotes (does not delete) any candidate whose ``_MOVE_TARGET`` target is in
    ``last.got_worse`` AND whose title is in ``last.next_recommended``; attaches an
    ``evidence`` line ONLY to candidates it actually moves. Surfaces exactly one
    ``"Revert last pass"`` move when ``last.revert_candidates`` is non-empty. No
    time / I/O / randomness; output order is a deterministic function of the input.
    """
    regressed = {_score_key(d) for d in last.get("got_worse", [])}
    recommended = set(last.get("next_recommended", []))

    out: List[Tuple[int, Dict]] = []
    for priority, item in candidates:
        title = item["title"]
        target = _MOVE_TARGET.get(title)
        if target is not None and target in regressed and title in recommended:
            new_priority = max(0, priority - HISTORY_DEMOTE)
            new_item = dict(item)
            new_item["evidence"] = (
                f"demoted: prior pass recorded {target} getting worse after this move"
            )
            out.append((new_priority, new_item))
        else:
            out.append((priority, item))

    revert = sorted(_score_key(d) for d in last.get("revert_candidates", []))
    if revert:
        out.append((HISTORY_REVERT_PRIORITY, {
            "title": "Revert last pass",
            "detail": ("The previous pass regressed " + ", ".join(revert)
                       + ". Revert it and re-approach the targeted change more conservatively."),
            "evidence": "surfaced because the last pass recorded revert candidate(s): "
                        + ", ".join(revert),
        }))
    return out


def plan_next_pass(
    records: List[Dict],
    doctrine_score: Dict,
    masking_report: Dict,
    sections_analysis: List[Dict],
    history: Optional[List[Dict]] = None,
    album_context: Optional[Dict] = None,
) -> List[Dict]:
    events = masking_report.get("events", [])
    candidates: List[Dict] = []

    lead = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)
    vocal_masks = [e for e in events if lead and lead["name"] in e["elements"] and e["classification"] == "bad_masking"]

    # 1) Vocal belief
    if lead is None:
        candidates.append((100, {
            "title": "Establish the emotional centre",
            "detail": "No lead vocal was identified. Confirm which track is the vocal so it can be protected and ridden.",
        }))
    else:
        detail = "Ride the lead vocal phrase-by-phrase before adding compression."
        if vocal_masks:
            detail += f" It is currently masked by {len(vocal_masks)} forward element(s); carve a presence pocket for it."
        candidates.append((90, {"title": "Vocal belief", "detail": detail}))

    # 2) Section / chorus contrast
    lift_fail = [s for s in sections_analysis if "warning" in s.get("contrast_vs_previous", {})]
    if lift_fail:
        names = ", ".join(s["name"] for s in lift_fail)
        candidates.append((80, {
            "title": "Section contrast",
            "detail": f"{names} do not lift enough. Create lift through supporting elements and automation "
                      f"(bloom on entry, intimacy in verses), not master level.",
        }))

    # 3) Stereo loop / width control
    loops_fg = [r for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS and r.get("stereo_width", 0) > 0.55]
    width_events = [e for e in events if e["classification"] == "width_crowding"]
    if loops_fg or width_events:
        targets = ", ".join(r["name"] for r in loops_fg) or "wide foreground elements"
        candidates.append((70, {
            "title": "Stereo loop / width control",
            "detail": f"{targets} appear full-width/foregrounded. Narrow to ~35-50%, filter, or push to the background "
                      f"so they are felt, not heard.",
        }))

    # 4) Depth cleanup
    n = len(records) or 1
    fg = [r for r in records if r["depth_default"] in FORWARD]
    if len(fg) / n > 0.6:
        candidates.append((60, {
            "title": "Depth cleanup",
            "detail": "Too many elements occupy the foreground. Move supporting guitars/keys/pads to the midground "
                      "instead of EQ-ing everything.",
        }))

    # 5) Targeted low-end / tonal fix
    low_conf = [e for e in events if e["classification"] == "low_end_conflict"]
    if low_conf:
        candidates.append((50, {
            "title": "Low-end definition",
            "detail": "Kick and bass share sub energy. Carve complementary space or sidechain the bass subtly to the kick.",
        }))

    # P-010 opt-in: when (and only when) an album_context trips a threshold,
    # append ONE bounded album-coherence hint BEFORE the history reprioritization
    # and the sort/take-5. It only ever appends; it never modifies an existing
    # candidate. Falsy / under-threshold context => no append => byte-identical.
    album_item = _album_outlier_item(album_context)
    if album_item is not None:
        candidates.append(album_item)

    # P-008 opt-in: when (and only when) history is supplied, reprioritize the
    # candidates against the most recent pass BEFORE the sort/take-5. Falsy history
    # (``None`` / ``[]``) leaves the default path byte-identical.
    if history:
        candidates = _apply_history(candidates, history[-1])

    candidates.sort(key=lambda c: c[0], reverse=True)
    out = []
    for i, (_, item) in enumerate(candidates[:5], start=1):
        out.append({"priority": i, **item})
    return out


def generate_creative_hypotheses(mix_plan: Dict, records: List[Dict]) -> List[Dict]:
    """Non-rendered creative hypotheses (static-vs-dynamic / creative-test stub)."""
    hyps: List[Dict] = []
    fails_lift = any(
        a.get("contrast_warning") for a in mix_plan.get("per_section_actions", [])
    )
    if fails_lift:
        hyps.append({
            "hypothesis_id": "chorus_bloom_01",
            "problem": "Chorus does not lift enough.",
            "variant": "Increase plate/chamber sends on backing vocals and acoustic guitars while keeping the lead vocal centered.",
            "risk": "May wash out the vocal.",
            "validation": "Check vocal intelligibility and section contrast.",
        })
        hyps.append({
            "hypothesis_id": "subtractive_drop_01",
            "problem": "Chorus feels dense but not impactful.",
            "variant": "Mute decorative texture in the final pre-chorus bar to create contrast before the chorus.",
            "risk": "May reduce momentum.",
            "validation": "Check whether the chorus entrance feels more dramatic.",
        })
    loops = [r for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    if loops:
        hyps.append({
            "hypothesis_id": "loop_deconstruct_01",
            "problem": f"Imported loop ({loops[0]['name']}) behaves like a finished record inside the record.",
            "variant": "Chop into transition gestures, high-pass ~250 Hz, narrow to ~35%, push to background except in the bridge.",
            "risk": "May reduce perceived chorus energy.",
            "validation": "Check the chorus feels less crowded and the vocal more foregrounded.",
        })
    if not hyps:
        hyps.append({
            "hypothesis_id": "intimacy_pass_01",
            "problem": "Mix is balanced but could feel more human.",
            "variant": "Pull verse reverb sends down and ride the vocal for intimacy; bloom only at the chorus.",
            "risk": "Verses may feel too dry — A/B against the static baseline.",
            "validation": "Check verse intimacy vs chorus openness.",
        })
    return hyps
