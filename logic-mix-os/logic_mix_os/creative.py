"""Creative experimentation engine (build packet sections 55-67).

Turns the diagnostic output into *testable creative hypotheses*: a static
baseline to protect, a static-vs-dynamic read, A/B/C/D variants per problem area,
deterministic variant scoring, search modes, and a winning-variant merge plan.

No audio is rendered (that needs a real session); variants are reversible,
scored *plans*. Determinism is preserved: same inputs -> same variants/scores.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .constants import LOOP_SAMPLE_KINDS

# --- Section 58: creative adjustment library --------------------------------
ADJUSTMENT_LIBRARY = {
    "space": ["short chamber intimacy", "plate bloom", "hall tail reveal", "room send lift",
              "pre-delay expansion", "dry-to-wet transition", "delay throw", "slapback intimacy",
              "reverb ducking", "shared-room glue"],
    "width": ["narrow verse / wide chorus", "mono texture in verse / stereo in chorus",
              "side-channel filtering", "background widening", "foreground narrowing",
              "support-stack widening", "stereo loop collapse", "mid-side contrast"],
    "tonal": ["dark verse / bright chorus", "filter opening", "low-pass background textures",
              "air lift only on emotional phrases", "low-mid warmth automation", "telephone bridge",
              "thin-to-full transition"],
    "dynamics": ["vocal phrase rides", "parallel compression bloom", "drum room lift",
                 "bass sustain increase", "chorus bus glue", "bridge compression pressure",
                 "final chorus release from compression"],
    "arrangement": ["mute decorative layer", "dropout before chorus", "introduce texture only at transition",
                    "deconstruct full loop into gestures", "remove duplicate midrange element",
                    "bring harmony forward for one line", "save strongest layer for final chorus"],
    "source_design": ["shorten synth release", "open synth filter by section", "change oscillator brightness",
                      "reduce MIDI velocity", "humanize MIDI timing", "alter sampler envelope",
                      "chop Splice loop", "reverse sample tail", "pitch sample down an octave",
                      "formant shift vocal texture", "turn full loop into one-shot accents",
                      "print alternate synth tone"],
}

# --- Section 60: creative search modes --------------------------------------
SEARCH_MODES = {
    "conservative": {"allowed_risk": "low", "bias": "preserve identity, subtle improvements, vocal belief"},
    "halee_depth": {"allowed_risk": "medium", "bias": "physical room/chamber/plate depth, space as storytelling"},
    "ramone_vocal_truth": {"allowed_risk": "low", "bias": "vocal rides, phrase emotion, clarity, restraint"},
    "dramatic_contrast": {"allowed_risk": "medium", "bias": "push verse/chorus/bridge contrast harder"},
    "deconstructive": {"allowed_risk": "medium", "bias": "remove, mute, chop, filter, simplify"},
    "experimental": {"allowed_risk": "high", "bias": "unusual transforms, reverses, extreme depth shifts"},
}

PHILOSOPHY = (
    "A mix is not finished when it is balanced. It is finished when the static balance "
    "supports the song and the dynamic movement makes the song feel inevitable. The best "
    "mix is the version where the song feels most inevitable, not the most processed."
)

# Per-variant-kind scoring profile (build packet section 59). Numeric dims are
# 0-100; risk fields are categorical.
_KIND_SCORES = {
    "width_bloom":      dict(technical=82, halee=78, ramone=79, contrast=91, vocal_belief=74, excitement=88, taste=80, translation="medium", mono="medium"),
    "subtractive_drop": dict(technical=85, halee=88, ramone=86, contrast=88, vocal_belief=86, excitement=78, taste=86, translation="low", mono="low"),
    "vocal_ride":       dict(technical=84, halee=84, ramone=92, contrast=70, vocal_belief=92, excitement=70, taste=88, translation="low", mono="low"),
    "drum_room_bloom":  dict(technical=80, halee=89, ramone=78, contrast=82, vocal_belief=76, excitement=83, taste=82, translation="low", mono="low"),
    "loop_deconstruct": dict(technical=83, halee=87, ramone=84, contrast=78, vocal_belief=85, excitement=72, taste=84, translation="low", mono="low"),
    "depth_cleanup":    dict(technical=84, halee=90, ramone=85, contrast=72, vocal_belief=86, excitement=66, taste=85, translation="low", mono="low"),
    "intimacy_pass":    dict(technical=82, halee=85, ramone=88, contrast=72, vocal_belief=90, excitement=64, taste=87, translation="low", mono="low"),
}

_RISK_PENALTY = {"low": 0, "medium": 6, "high": 14}

# --- P-012: creative-scoring evidence-nudge layer (option B, PENALTY-ONLY) ---
# Context nudges that lower a variant's score when the diagnostic evidence makes
# the move risky. Penalty-only (a nudge can only LOWER a score, never promote a
# variant), bounded (the summed overall effect is clamped to ±CREATIVE_NUDGE_CAP
# on the overall axis governance ranks on), transparent (each fired nudge emits a
# verbatim evidence line into ``score_nudges``), and deterministic (fixed table
# order; pure helper). The curated ``_KIND_SCORES`` base is untouched.
CREATIVE_NUDGE_CAP = 2.0  # max summed overall-score movement, in overall points

# Each row: kinds it applies to, the exact predicate over result.masking_report
# events, the dim it moves, the (negative) delta, and the verbatim evidence line.
_NUDGE_TABLE = [
    {
        # P-015: intimacy_pass is EXEMPT here. An intimacy pass is the CORRECT
        # response to a masked lead vocal — it brings the vocal into focused
        # proximity (lower verse sends, keep it close) rather than shoving it
        # forward by brute level/width — so it must NOT be penalized as a risky
        # vocal-forward move. Only the genuinely vocal-forward moves
        # (width_bloom, vocal_ride) are penalized. The delta is -14 so the
        # single vocal_belief dim moves -14/7 = -2.0 overall = exactly
        # CREATIVE_NUDGE_CAP (the cap is unchanged; it now also binds vocal_ride).
        "kinds": {"width_bloom", "vocal_ride"},
        "evidence": "lead_masked",
        "dim": "vocal_belief",
        "delta": -14,
        "reason": ("vocal_belief -14: lead vocal is masked (bad_masking) — "
                   "pushing the vocal forward by level/width is risky here; "
                   "bring it into intimate focus instead"),
    },
    {
        "kinds": {"width_bloom"},
        "evidence": "width_crowding",
        "dim": "vocal_belief",
        "delta": -6,
        "reason": "vocal_belief -6: stereo image is already width-crowded",
    },
]


def _lead_masked(result) -> bool:
    """Verbatim predicate from the original context adjustment (creative.py:252-255):
    any masking event classified ``bad_masking`` whose elements include the vocal."""
    return any(
        e["classification"] == "bad_masking" and any("vocal" in el.lower() for el in e["elements"])
        for e in result.masking_report.get("events", [])
    )


def _width_crowded(result) -> bool:
    return any(
        e["classification"] == "width_crowding"
        for e in result.masking_report.get("events", [])
    )


_NUDGE_EVIDENCE = {"lead_masked": _lead_masked, "width_crowding": _width_crowded}


def _apply_nudges(kind: str, result) -> List[tuple]:
    """Pure: the ordered ``(dim, delta, reason)`` for each FIRED nudge.

    A row fires when ``kind`` is in its ``kinds`` set AND its evidence predicate
    is true on ``result``. Rows are evaluated in table order, so the emitted
    evidence lines are deterministic.
    """
    fired: List[tuple] = []
    for row in _NUDGE_TABLE:
        if kind in row["kinds"] and _NUDGE_EVIDENCE[row["evidence"]](result):
            fired.append((row["dim"], row["delta"], row["reason"]))
    return fired


# --- P-016: creative-scoring evidence-PROMOTION layer (the FIRST reward nudge) --
# P-012/P-015 held a penalty-only line (a nudge could only LOWER a score). P-016
# crosses it deliberately, on the user's delegation: a bounded, evidence-gated
# PROMOTION that can RAISE a variant's score, layered on the SAME untouched
# ``_KIND_SCORES`` base and mirroring the penalty machinery exactly — pure,
# deterministic (fixed table order), transparent (each fired promotion emits a
# verbatim evidence line into ``score_nudges``), and bounded. The summed
# promotion overall-delta is clamped to ``+CREATIVE_PROMOTION_CAP`` on the same
# overall axis governance ranks on, EXACTLY as the penalty path clamps to
# ``-CREATIVE_NUDGE_CAP``. Promotion and penalty are INDEPENDENT and both bounded;
# the penalty cap and table above are untouched.
#
# Doctrine anchor (the system's OWN principle, not taste): ``governance``'s
# anti_template warns when the same move-kind wins >=3 problems. When a loop is
# GENUINELY foregrounded, promoting the loop-specific ``loop_deconstruct`` so it
# wins the ``loop`` problem honors ``loops_not_foregrounded`` and "never let a
# stock loop dominate the song identity."
CREATIVE_PROMOTION_CAP = 4.0  # max summed overall-score PROMOTION, in overall points

# Each row: kinds it applies to, the evidence predicate key, the dim it moves,
# the (positive) delta, and the verbatim evidence line. The delta is +35 on the
# (low) excitement dim: +35/7 = +5.0 raw overall, which the cap clamps down to
# exactly +CREATIVE_PROMOTION_CAP (+4.0) — so the cap genuinely BINDS, mirroring
# the way the -14 penalty binds the -2.0 penalty cap.
_PROMOTION_TABLE = [
    {
        "kinds": {"loop_deconstruct"},
        "evidence": "foregrounded_loop",
        "dim": "excitement",
        "delta": 35,
        "reason": ("loop_promotion +4.0: a foregrounded/dominating loop — "
                   "deconstruct it (source material respected), don't just accent it"),
    },
]


def _foregrounded_loop(result) -> bool:
    """Pure predicate over the REAL evidence wire (mirrors ``_lead_masked`` /
    ``_width_crowded``): fire only when the source auditors have flagged a
    ``"foregrounded loop"`` red_flag (source_auditors.py) AND the provenance
    analyzer corroborates it with ``high_risk`` (provenance.py). Both must hold —
    the auditors read the record's foregrounding, provenance reads recognizable +
    foregrounded, so requiring both keeps the promotion evidence-gated."""
    source_audits = getattr(result, "source_audits", None) or {}
    provenance = getattr(result, "provenance", None) or {}
    flagged = any(
        "foregrounded loop" in a.get("red_flags", [])
        for a in source_audits.get("audits", [])
    )
    high_risk = provenance.get("summary", {}).get("high_risk", 0)
    return flagged and bool(high_risk)


_PROMOTION_EVIDENCE = {"foregrounded_loop": _foregrounded_loop}


def _apply_promotions(kind: str, result) -> List[tuple]:
    """Pure: the ordered ``(dim, delta, reason)`` for each FIRED promotion.

    A row fires when ``kind`` is in its ``kinds`` set AND its evidence predicate
    is true on ``result``. Rows are evaluated in table order, so the emitted
    evidence lines are deterministic. Mirrors ``_apply_nudges`` exactly.
    """
    fired: List[tuple] = []
    for row in _PROMOTION_TABLE:
        if kind in row["kinds"] and _PROMOTION_EVIDENCE[row["evidence"]](result):
            fired.append((row["dim"], row["delta"], row["reason"]))
    return fired


# --------------------------------------------------------------------------- #
def static_baseline(result) -> Dict:
    return {
        "mix_state": "static_baseline",
        "status": "locked",
        "purpose": "Stable technical and musical balance before creative variants.",
        "locked_elements": [
            "lead vocal intelligibility",
            "kick/bass relationship",
            "basic tonal balance",
            "core depth hierarchy",
            "essential lyric audibility",
        ],
    }


def static_vs_dynamic(result) -> Dict:
    ds = result.doctrine_score
    static = ds.get("static_mix_score")
    dynamic = ds.get("dynamic_mix_score")
    rec = []
    if static is not None and dynamic is not None and dynamic + 12 < static:
        rec.append("Stop EQ-ing the static mix. Build dynamic movement: pre-chorus narrowing, "
                   "chorus bloom, final-chorus width release, vocal phrase rides.")
    elif dynamic is not None and dynamic < 55:
        rec.append("The mix is balanced but emotionally inactive — invest in section movement.")
    else:
        rec.append("Static and dynamic layers are reasonably matched; refine details.")
    return {
        "static_mix_score": static,
        "dynamic_mix_score": dynamic,
        "diagnosis": "balanced but static" if (dynamic or 100) < 55 else "moving",
        "recommendation": " ".join(rec),
    }


def _supporting_elements(records) -> List[str]:
    return [r["name"] for r in records
            if r["instrument_identity"] in {"acoustic_guitar", "electric_guitar", "backing_vocal", "piano", "electric_piano", "strings"}]


# Identity families/identities that count as "the drums" for room/overhead moves.
_DRUM_IDENTITIES = {"kick", "snare", "hat", "hi_hat", "tom", "drum_overhead", "drum_room", "cymbal", "percussion"}
_DRUM_FAMILIES = {"drums", "percussion"}


def _lead_vocal_tracks(records) -> List[str]:
    """Real lead-vocal track names, in project order."""
    return [r["name"] for r in records if r["instrument_identity"] == "lead_vocal"]


def _drum_tracks(records) -> List[str]:
    """Real drum/percussion track names, in project order."""
    return [r["name"] for r in records
            if r["instrument_identity"] in _DRUM_IDENTITIES or r["identity_family"] in _DRUM_FAMILIES]


def _resolve(*candidate_lists: List[str]) -> List[str]:
    """First non-empty candidate list (each already a real-record subset)."""
    for names in candidate_lists:
        if names:
            return names
    return []


def detect_creative_problems(result) -> List[Dict]:
    problems: List[Dict] = []
    sections = result.section_analysis
    records = result.records
    if any("warning" in s.get("contrast_vs_previous", {}) for s in sections):
        problems.append({"id": "chorus_lift", "problem": "Chorus does not lift enough emotionally."})
    if result.expanded.get("arrangement_density", {}).get("crowded_sections"):
        problems.append({"id": "density", "problem": "Arrangement is crowded; hierarchy is unclear."})
    if any(r["source_kind"] in LOOP_SAMPLE_KINDS for r in records):
        problems.append({"id": "loop", "problem": "An imported loop behaves like a finished record inside the record."})
    n = len(records) or 1
    if sum(1 for r in records if r["depth_default"] in {"intimate", "foreground"}) / n > 0.6 and n >= 5:
        problems.append({"id": "depth", "problem": "Too many elements occupy the foreground."})
    if any(r["instrument_identity"] == "lead_vocal" for r in records):
        problems.append({"id": "vocal_belief", "problem": "Vocal could feel more believable and present."})
    return problems


def _variant(vid, problem, kind, name, hypothesis, changes, tracks, risk, validation, expected) -> Dict:
    return {
        "variant_id": vid,
        "problem": problem,
        "kind": kind,
        "name": name,
        "creative_hypothesis": hypothesis,
        "changes": changes,
        "tracks_affected": tracks,
        "risk": risk,
        "reversibility": "non_destructive_duplicate_track",
        "validation": validation,
        "expected_strength": expected,
    }


def generate_variants(problem: Dict, result, mode: str = "dramatic_contrast") -> List[Dict]:
    records = result.records
    supporting = _supporting_elements(records)
    loops = [r["name"] for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    lead_vocal = _lead_vocal_tracks(records)
    drums = _drum_tracks(records)
    pid = problem["id"]
    variants: List[Dict] = []

    # Fallbacks so no variant ever emits a phantom or empty track list: the
    # lead-vocal/drum moves resolve against real records, then degrade to the
    # next musically-sensible real layer present in the project.
    lead_target = _resolve(lead_vocal, supporting, loops, [r["name"] for r in records][:1])
    drum_target = _resolve(drums, supporting, loops, lead_vocal, [r["name"] for r in records][:1])

    if pid == "chorus_lift":
        variants += [
            _variant("chorus_lift_A", pid, "width_bloom", "Width Bloom",
                     "The chorus opens if supporting elements bloom outward while the lead stays centered.",
                     ["Increase backing-vocal/guitar plate send +3 to +6 dB at chorus entry", "Widen supporting bus 60%->75%"],
                     supporting, "May feel too modern/washed.", ["chorus feels wider", "vocal remains centered"], "emotional openness"),
            _variant("chorus_lift_B", pid, "subtractive_drop", "Subtractive Drop",
                     "Withhold a decorative layer before the chorus so it feels larger by contrast.",
                     ["Mute decorative texture in the final pre-chorus bar"], _resolve(loops, supporting[-1:], [r["name"] for r in records][:1]),
                     "Chorus may still feel small.", ["chorus entrance feels more dramatic"], "impact through contrast"),
            _variant("chorus_lift_C", pid, "vocal_ride", "Vocal-Ride Lift",
                     "Ride the lead vocal into the chorus with a delay throw on the last pre-chorus phrase.",
                     ["Ride lead vocal +1 dB into chorus", "Delay throw on last pre-chorus phrase"],
                     lead_target, "May not create enough scale.", ["emotional belief increases"], "emotional belief"),
            _variant("chorus_lift_D", pid, "drum_room_bloom", "Drum Room Bloom",
                     "Use physical room/overheads rather than plugin hype to lift the chorus.",
                     ["Increase drum room/overhead energy at chorus entry"], drum_target,
                     "Drums may overpower the vocal.", ["Halee-style physical lift", "vocal still on top"], "physical lift"),
        ]
    elif pid == "density":
        variants += [
            _variant("density_A", pid, "depth_cleanup", "Depth Cleanup",
                     "Move supporting elements to the midground so the foreground breathes.",
                     ["Push 2-3 supporting elements to midground", "Reserve widest placement for one element"],
                     supporting, "Mix may feel less 'big' at first.", ["foreground clears", "vocal more present"], "hierarchy"),
            _variant("density_B", pid, "subtractive_drop", "Subtractive Simplify",
                     "Remove a duplicate midrange element entirely.",
                     ["Mute/duplicate-then-remove a redundant midrange layer"], supporting,
                     "Lose a part you liked.", ["clarity improves without loss of energy"], "clarity"),
        ]
    elif pid == "loop":
        target = loops[0] if loops else (([r["name"] for r in records][:1] or ["the loop"])[0])
        variants += [
            _variant("loop_A", pid, "loop_deconstruct", "Loop Deconstruct",
                     f"Re-contextualise {target} as movement (felt), not a stock loop (heard).",
                     [f"Chop {target} into transition gestures", "High-pass ~250 Hz", "Narrow to ~35%", "Push to background except bridge"],
                     loops, "May reduce perceived chorus energy.", ["chorus less crowded", "vocal more foregrounded"], "hierarchy"),
            _variant("loop_B", pid, "subtractive_drop", "Loop as Accent",
                     f"Replace the continuous {target} bed with one-shot accents at transitions.",
                     [f"Turn {target} into one-shot accents", "Use only at section transitions"],
                     loops, "Less continuous texture.", ["song identity stops being the loop"], "identity protection"),
        ]
    elif pid == "depth":
        variants.append(
            _variant("depth_A", pid, "depth_cleanup", "Depth Cleanup",
                     "Spread elements across the depth field instead of stacking them forward.",
                     ["Move felt/decorative elements to midground/background", "Keep vocal + hook forward"],
                     supporting, "Initial loss of size.", ["depth pyramid forms", "vocal owns the front"], "depth realism"))
    elif pid == "vocal_belief":
        variants += [
            _variant("vocal_A", pid, "vocal_ride", "Phrase Rides",
                     "Ride phrase endings before any compression so the words land.",
                     ["Clip gain + fader rides on phrase ends +0.5 to +1.5 dB"], lead_target,
                     "Time-consuming.", ["every word believable"], "vocal belief"),
            _variant("vocal_B", pid, "intimacy_pass", "Verse Intimacy",
                     "Pull verse reverb sends down and keep the vocal close; bloom only at the chorus.",
                     ["Lower verse vocal sends", "Bloom sends at chorus"], lead_target,
                     "Verses may feel dry — A/B vs baseline.", ["verse intimacy vs chorus openness"], "intimacy"),
        ]
    return variants


def score_variant(variant: Dict, result) -> Dict:
    base = dict(_KIND_SCORES.get(variant["kind"], _KIND_SCORES["depth_cleanup"]))
    numeric = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]

    # Base overall on the curated dims, before any context nudge — this is the
    # axis governance ranks on, and the axis the cap binds.
    base_overall = sum(base[k] for k in numeric) / len(numeric) - _RISK_PENALTY[base["translation"]]

    # --- P-012: evidence-nudge layer (penalty-only, bounded, transparent) ----
    # Each fired nudge lowers a curated dim and emits an evidence line. The dims
    # carry the honest move; the *overall* effect is clamped to ±CREATIVE_NUDGE_CAP.
    fired = _apply_nudges(variant["kind"], result)
    nudges: List[str] = []
    for dim, delta, reason in fired:
        base[dim] += delta
        nudges.append(reason)

    nudged_overall = sum(base[k] for k in numeric) / len(numeric) - _RISK_PENALTY[base["translation"]]
    # Clamp the SUMMED overall delta to ±CREATIVE_NUDGE_CAP. Worst case is
    # width_bloom under BOTH rows = -20 raw = -2.86 overall, clamped to -2.0;
    # vocal_ride under row-0 alone = -14 raw = -2.0 overall = exactly the cap.
    overall_delta = nudged_overall - base_overall
    if overall_delta < -CREATIVE_NUDGE_CAP:
        overall_delta = -CREATIVE_NUDGE_CAP
    elif overall_delta > CREATIVE_NUDGE_CAP:
        overall_delta = CREATIVE_NUDGE_CAP

    # --- P-016: evidence-PROMOTION layer (reward-only, bounded, transparent) --
    # Independent of the penalty path: each fired promotion raises a curated dim
    # and emits an evidence line. The SUMMED promotion overall-delta is clamped to
    # +CREATIVE_PROMOTION_CAP, exactly as the penalty path clamps to
    # -CREATIVE_NUDGE_CAP. Measured from the SAME curated base_overall so the two
    # bounded effects are additive and each independently bounded.
    promoted = _apply_promotions(variant["kind"], result)
    for dim, delta, reason in promoted:
        base[dim] += delta
        nudges.append(reason)
    if promoted:
        promoted_overall = sum(base[k] for k in numeric) / len(numeric) - _RISK_PENALTY[base["translation"]]
        promotion_delta = (promoted_overall - base_overall) - overall_delta
        if promotion_delta > CREATIVE_PROMOTION_CAP:
            promotion_delta = CREATIVE_PROMOTION_CAP
        overall_delta += promotion_delta

    overall = base_overall + overall_delta
    overall = round(max(0.0, min(100.0, overall)), 1)

    verdict = "promising" if overall >= 80 else ("worth testing" if overall >= 70 else "marginal")
    if base["vocal_belief"] < 75:
        verdict += " — check vocal wash"

    scores = {
        "technical_score": base["technical"],
        "halee_score": base["halee"],
        "ramone_score": base["ramone"],
        "section_contrast_score": base["contrast"],
        "vocal_belief_score": base["vocal_belief"],
        "listener_excitement_score": base["excitement"],
        "taste_alignment_score": base["taste"],
        "translation_risk": base["translation"],
        "mono_compatibility": base["mono"],
        "reversibility": "non_destructive",
        "overall_score": overall,
        "overall_verdict": verdict,
    }
    if nudges:  # evidence-key discipline: present ONLY when ≥1 nudge fired.
        scores["score_nudges"] = nudges
    return scores


def winning_variant(scored_variants: List[Dict]) -> Optional[Dict]:
    if not scored_variants:
        return None
    best = max(scored_variants, key=lambda v: v["scores"]["overall_score"])
    rejected = [v for v in scored_variants if v["variant_id"] != best["variant_id"]]
    return {
        "winning_variant": best["variant_id"],
        "keep_moves": best["changes"],
        "reject_moves": [c for v in rejected for c in v["changes"]],
        "reason": f"'{best['name']}' scored {best['scores']['overall_score']} "
                  f"({best['scores']['overall_verdict']}); strongest on its intended axis without breaking vocal belief.",
    }


def run_creative_engine(result, mode: str = "dramatic_contrast") -> Dict:
    if mode not in SEARCH_MODES:
        mode = "dramatic_contrast"
    problems = detect_creative_problems(result)
    branches: List[Dict] = []
    for problem in problems:
        variants = generate_variants(problem, result, mode)
        for v in variants:
            v["scores"] = score_variant(v, result)
        branches.append({
            "problem": problem["problem"],
            "problem_id": problem["id"],
            "variants": variants,
            "winning": winning_variant(variants),
        })
    return {
        "search_mode": mode,
        "search_mode_bias": SEARCH_MODES[mode]["bias"],
        "static_baseline": static_baseline(result),
        "static_vs_dynamic": static_vs_dynamic(result),
        "adjustment_library": ADJUSTMENT_LIBRARY,
        "branches": branches,
        "guardrails": [
            "Always preserve a static baseline.",
            "Never destructively alter source tracks.",
            "Never judge creative variants only by loudness.",
            "Never let novelty override vocal belief.",
            "Always compare creative variants to the song's emotional truth.",
        ],
        "philosophy": PHILOSOPHY,
    }
