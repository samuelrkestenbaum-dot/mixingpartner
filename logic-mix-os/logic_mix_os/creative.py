"""Creative experimentation engine (build packet sections 55-67).

Turns the diagnostic output into *testable creative hypotheses*: a static
baseline to protect, a static-vs-dynamic read, A/B/C/D variants per problem area,
deterministic variant scoring, search modes, and a winning-variant merge plan.

No audio is rendered (that needs a real session); variants are reversible,
scored *plans*. Determinism is preserved: same inputs -> same variants/scores.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .analyzers.vocal_type_classifier import lead_vocal_names
from .constants import (
    CREATIVE_EXTENDED_KINDS,
    LOOP_SAMPLE_KINDS,
    TRANSLATION_RISK_LEVELS,
)
from .doctrine.doctrine_engine import read_loop_context
from .doctrine.producer_profile import ProducerProfile, load_profile

# --- Producer-specific judgment: sourced from the reference ProducerProfile --
# (P-026, first wiring step of the producer-agnostic epic). The producer-specific
# values below are no longer hardcoded literals here — they are SOURCED from the
# reference profile's JSON (``doctrine/producers/halee_ramone.json``), which is now
# their single source of truth. The loader returns fresh, JSON-parsed collections
# on every load (nudge/promotion ``kinds`` rehydrated to sets), so these globals
# keep the exact names/shapes/types the old literals had and downstream code is
# untouched. Per-call producer selection is NOT threaded here (that is P-029).
_DEFAULT_PROFILE = load_profile("halee_ramone")

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
# Sourced from the reference profile (was a hardcoded literal; the JSON is now home).
SEARCH_MODES = _DEFAULT_PROFILE.search_modes

# Sourced from the reference profile (was a hardcoded literal; the JSON is now home).
PHILOSOPHY = _DEFAULT_PROFILE.philosophy

# Per-variant-kind scoring profile (build packet section 59). Numeric dims are
# 0-100; risk fields are categorical. Sourced from the reference profile (was a
# hardcoded literal; the JSON is now home). ``score_variant`` copies each row
# (``dict(_KIND_SCORES.get(...))``) before mutating, so this dict is never mutated
# in place — the fresh JSON-parsed collection stays pristine.
_KIND_SCORES = _DEFAULT_PROFILE.kind_scores

# Sourced from the reference profile (was a hardcoded literal; the JSON is now home).
_RISK_PENALTY = _DEFAULT_PROFILE.risk_penalty

# --- P-012: creative-scoring evidence-nudge layer (option B, PENALTY-ONLY) ---
# Context nudges that lower a variant's score when the diagnostic evidence makes
# the move risky. Penalty-only (a nudge can only LOWER a score, never promote a
# variant), bounded (the summed overall effect is clamped to ±CREATIVE_NUDGE_CAP
# on the overall axis governance ranks on), transparent (each fired nudge emits a
# verbatim evidence line into ``score_nudges``), and deterministic (fixed table
# order; pure helper). The curated ``_KIND_SCORES`` base is untouched.
# Sourced from the reference profile (was a hardcoded literal; the JSON is now home).
CREATIVE_NUDGE_CAP = _DEFAULT_PROFILE.creative_nudge_cap  # max summed overall-score movement, in overall points

# Sourced from the reference profile (was a hardcoded literal; the JSON is now
# home). Each row: kinds it applies to (a SET — the loader rehydrates the JSON
# list back to a set, so ``_apply_nudges``'s ``kind in row['kinds']`` is unchanged),
# the exact predicate over result.masking_report events, the dim it moves, the
# (negative) delta, and the verbatim evidence line.
#
# P-015 doctrine preserved in the JSON: intimacy_pass is EXEMPT — an intimacy pass
# is the CORRECT response to a masked lead vocal (it brings the vocal into focused
# proximity rather than shoving it forward), so it is not penalized as a risky
# vocal-forward move. Only width_bloom / vocal_ride are penalized. The -14 delta
# moves the single vocal_belief dim -14/7 = -2.0 overall = exactly CREATIVE_NUDGE_CAP.
_NUDGE_TABLE = _DEFAULT_PROFILE.nudge_table


def _lead_masked(result) -> bool:
    """The masked-LEAD evidence predicate (P-012 row-0 / the P-032g Ramone
    gate): any masking event classified ``bad_masking`` whose elements include
    the LEAD VOCAL — matched by the IDENTITY-derived lead name(s)
    (``instrument_identity == "lead_vocal"`` on ``result.records``).

    P-034 fix: the original predicate matched any element containing the
    SUBSTRING "vocal". With the analyzer now emitting non-lead vocal-band
    events (their own ``vocal_band_masking`` classification, lead never
    present) — and lead-free vocal-NAMED elements possible in principle —
    the match is identity-derived, so a non-lead vocal event can never
    falsely trigger the masked-lead gate. On the lead-inclusive
    ``bad_masking`` events the analyzer actually emits, the two predicates
    agree: byte-identical on every fixture. (P-037 consolidated the
    derivation onto the shared ``lead_vocal_names`` basis — the identical
    set comprehension, one home.)"""
    lead_names = lead_vocal_names(result.records)
    if not lead_names:
        return False
    return any(
        e["classification"] == "bad_masking" and any(el in lead_names for el in e["elements"])
        for e in result.masking_report.get("events", [])
    )


def _width_crowded(result) -> bool:
    return any(
        e["classification"] == "width_crowding"
        for e in result.masking_report.get("events", [])
    )


_NUDGE_EVIDENCE = {"lead_masked": _lead_masked, "width_crowding": _width_crowded}


def _apply_nudges(kind: str, result, profile: Optional[ProducerProfile] = None) -> List[tuple]:
    """Pure: the ordered ``(dim, delta, reason)`` for each FIRED nudge.

    A row fires when ``kind`` is in its ``kinds`` set AND its evidence predicate
    is true on ``result``. Rows are evaluated in table order, so the emitted
    evidence lines are deterministic. The nudge table is read from the PASSED
    ``profile`` (default = the reference), so per-call producer selection reaches
    the penalty layer.
    """
    nudge_table = (profile or _DEFAULT_PROFILE).nudge_table
    fired: List[tuple] = []
    for row in nudge_table:
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
# Sourced from the reference profile (was a hardcoded literal; the JSON is now home).
CREATIVE_PROMOTION_CAP = _DEFAULT_PROFILE.creative_promotion_cap  # max summed overall-score PROMOTION, in overall points

# Sourced from the reference profile (was a hardcoded literal; the JSON is now
# home). Each row: kinds it applies to (a SET — rehydrated by the loader), the
# evidence predicate key, the dim it moves, the (positive) delta, and the verbatim
# evidence line. The +35 delta on the (low) excitement dim is +35/7 = +5.0 raw
# overall, which the cap clamps down to exactly +CREATIVE_PROMOTION_CAP (+4.0) — so
# the cap genuinely BINDS, mirroring the way the -14 penalty binds the -2.0 cap.
_PROMOTION_TABLE = _DEFAULT_PROFILE.promotion_table


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


def _protected_iconic_loop(result, prof: ProducerProfile) -> bool:
    """P-032g — the first profile-DECIDED creative gate (pure, read-only).

    THE DOCTRINE PIN made operational: the engine DETECTS agnostically (the
    ``loop_context`` doctrine axis reads static-vs-iconic, observationally);
    the PROFILE decides. This predicate is True — and the ``loop_deconstruct``
    promotion is withheld — ONLY when ALL of:

      * the profile OPTS IN: ``protect_iconic_loops`` is True. The reference
        ``halee_ramone`` sets it False, so the default path short-circuits
        here and current behavior is byte-identical (Halee/Ramone still
        deconstructs a dominating loop).
      * the lead vocal is NOT bad-masked (the RAMONE GATE): iconic must not
        override a masked lead. Even a protecting profile lets the
        deconstruct pressure through when the loop context includes a buried
        vocal — checked FIRST, so protection can never shadow the vocal.
      * the loop READS iconic on the SAME shared detection basis as the
        doctrine axis (``read_loop_context`` with the profile's own
        ``loop_context`` constants — one basis, never forked): dominant +
        groove-carrying function while the mix evolves around it. A STATIC
        or ambiguous reading earns no protection.
    """
    if not prof.protect_iconic_loops:
        return False
    if _lead_masked(result):
        return False
    c = prof.doctrine["scorers"]["loop_context"]
    status, _ = read_loop_context(
        result.records, result.section_analysis,
        result.masking_report.get("events", []), c,
    )
    return status == "iconic"


def _apply_promotions(kind: str, result, profile: Optional[ProducerProfile] = None) -> List[tuple]:
    """Pure: the ordered ``(dim, delta, reason)`` for each FIRED promotion.

    A row fires when ``kind`` is in its ``kinds`` set AND its evidence predicate
    is true on ``result``. Rows are evaluated in table order, so the emitted
    evidence lines are deterministic. Mirrors ``_apply_nudges`` exactly, reading
    the promotion table from the PASSED ``profile`` (default = the reference).

    P-032g: the ``loop_deconstruct`` promotion additionally passes the
    profile-decided ``protect_iconic_loops`` gate — a profile that protects
    iconic-functioning loops withholds the promotion (unless the lead vocal is
    masked). With the reference default (False) the gate is inert and the
    firing behavior is byte-identical to the pre-gate engine.
    """
    prof = profile or _DEFAULT_PROFILE
    promotion_table = prof.promotion_table
    fired: List[tuple] = []
    for row in promotion_table:
        if kind in row["kinds"] and _PROMOTION_EVIDENCE[row["evidence"]](result):
            if kind == "loop_deconstruct" and _protected_iconic_loop(result, prof):
                continue  # the profile protects the iconic-functioning loop
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


def _curated_variants(problem: Dict, result) -> List[Dict]:
    """The engine's NEUTRAL curated candidate emission for one problem — the
    frozen ``_variant`` pool, exactly as it emitted before P-042 (set AND
    order). This is the shared move vocabulary every profile forks FROM; no
    profile data reaches it."""
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
                     "Drums may overpower the vocal.", ["physical room lift", "vocal still on top"], "physical lift"),
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


def _extended_variants(problem: Dict, result) -> List[Dict]:
    """The engine's EXTENDED curated emission for one problem (P-043): the
    two reach-gated move families, ``arrangement_lift`` (section-level lift
    built in the arrangement — parts withheld and entering across section
    boundaries, sectional builds) and ``ensemble_rebalance`` (ensemble-aware
    RELATIVE rebalancing that reveals arrangement roles — never mute-only
    aggression). Curated exactly like the neutral pool above — plan-only,
    non-destructive, real track targets via the same resolution helpers —
    but NEVER part of the neutral emission: these variants enter a candidate
    set ONLY when the active mode's authored ``reach_kinds`` admit them
    (``_fork_candidates``). No profile data reaches this builder."""
    records = result.records
    supporting = _supporting_elements(records)
    loops = [r["name"] for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    pid = problem["id"]
    variants: List[Dict] = []

    # The ensemble target: the supporting layers first, then the same
    # degrade-to-real-records chain the neutral pool uses (never phantom,
    # never empty while the project has records).
    ensemble_target = _resolve(supporting, loops, [r["name"] for r in records][:1])

    if pid == "chorus_lift":
        variants.append(
            _variant("chorus_lift_E", pid, "arrangement_lift", "Sectional Arrangement Lift",
                     "The chorus lifts hardest when parts are withheld before it and enter on its downbeat — build the lift in the arrangement, not the processing.",
                     ["Duplicate 1-2 supporting tracks and region-mute their final pre-chorus bars",
                      "Bring the withheld parts back in on the chorus downbeat",
                      "Reserve one texture for the final chorus only"],
                     ensemble_target, "A sparser pre-chorus may briefly read as lost energy before the payoff registers.",
                     ["chorus entry feels larger with no new processing", "pre-chorus tension increases"],
                     "sectional lift"))
    elif pid == "density":
        variants += [
            _variant("density_C", pid, "arrangement_lift", "Staggered Entrances",
                     "A crowded arrangement usually means everything plays everywhere — stagger entrances so each section carries fewer simultaneous parts.",
                     ["Map which supporting parts actually play in each section",
                      "Delay 1-2 entrances to the next section boundary (duplicate the track, region-mute the early bars)",
                      "Let one part exit at the bridge so its return reads as an event"],
                     ensemble_target, "Sections may feel emptier until the entrances start reading as events.",
                     ["each section has its own arrangement identity", "the chorus reads bigger by contrast"],
                     "arrangement clarity"),
            _variant("density_D", pid, "ensemble_rebalance", "Ensemble Role Rebalance",
                     "Reveal the hierarchy by rebalancing the ensemble into roles — one carrier forward, the rest tucked relative — instead of removing parts.",
                     ["Pick ONE supporting element as the section's carrier and hold its level",
                      "Tuck the remaining supporting elements -2 to -4 dB relative to the carrier (VCA or region gain)",
                      "Rotate the carrier role per section so every part keeps a purpose"],
                     ensemble_target, "Relative moves may read subtle on first listen.",
                     ["hierarchy reads without muting anything", "every part keeps an audible role"],
                     "ensemble hierarchy"),
        ]
    elif pid == "vocal_belief":
        variants.append(
            _variant("vocal_C", pid, "ensemble_rebalance", "Lead-in-Ensemble Rebalance",
                     "Make the lead read more present by rebalancing the ensemble around it — tuck the competing midrange under the phrases instead of pushing the vocal fader.",
                     ["Tuck midrange supporting elements -1.5 to -3 dB under lead phrases (VCA or region gain)",
                      "Restore the ensemble between phrases so the track keeps its size",
                      "Leave the lead fader untouched — the ensemble moves, not the vocal"],
                     ensemble_target, "Over-tucking can hollow the choruses — A/B against the static baseline.",
                     ["lead reads present at the same fader", "ensemble keeps its size between phrases"],
                     "lead prominence"))
    return variants


# --- P-042: profile-authored mode forking ------------------------------------
# The ownership split, verbatim from the packet: the ENGINE owns the shared
# move vocabulary (the frozen curated pool above), the PROFILE owns each
# mode's reach (the authored ``favor_kinds`` / ``suppress_kinds`` declarations
# on its ``search_modes`` entries), and GOVERNANCE owns the safety cap (the
# mode's existing ``allowed_risk`` posture, which an authored reach can never
# exceed). No producer name appears anywhere in this fork path — the fork is
# pure data threading.

# Severity rank of each translation-risk level (shared engine scale).
_RISK_RANK = {level: i for i, level in enumerate(TRANSLATION_RISK_LEVELS)}


def _mode_declarations(prof: ProducerProfile, mode: Optional[str]) -> Optional[Dict]:
    """The resolved mode's authored forking declarations, or ``None`` when the
    mode is NEUTRAL. Pure read of the passed profile's ``search_modes``.

    Neutral — meaning the engine's un-forked emission, byte-identical to the
    pre-P-042 behavior — covers: no mode requested; a mode the profile does
    not carry; a mode entry without the declaration fields (third-party
    profiles stay valid untouched); and a mode entry that authors ALL the
    declaration fields explicitly EMPTY (the shipped profiles' neutral modes
    — authored neutrality, equivalent to absence by construction).

    P-043: ``reach_kinds`` (the authored EXTENDED-vocabulary reach) is a
    third declaration field — a mode that authors ONLY a reach is declaring,
    exactly like one that only favors or only suppresses.
    """
    if mode is None:
        return None
    entry = prof.search_modes.get(mode)
    if not isinstance(entry, dict):
        return None
    favor = list(entry.get("favor_kinds") or [])
    suppress = list(entry.get("suppress_kinds") or [])
    reach = list(entry.get("reach_kinds") or [])
    if not favor and not suppress and not reach:
        return None
    allowed = entry.get("allowed_risk")
    if allowed not in _RISK_RANK:
        # Fail CLOSED: loader-validated profiles always carry a real level on
        # a declaring mode; a loader-bypassing profile without one is capped
        # at the most restrictive posture, never the most permissive.
        allowed = TRANSLATION_RISK_LEVELS[0]
    return {"favor_kinds": favor, "suppress_kinds": suppress,
            "reach_kinds": reach, "allowed_risk": allowed}


def _fork_candidates(variants: List[Dict], decl: Dict,
                     prof: ProducerProfile, extended: List[Dict] = ()) -> tuple:
    """Apply one mode's authored declarations to the neutral curated list.

    Pure and deterministic. Returns ``(candidates, fork)`` where ``fork`` is
    the honest per-emission report: ``{"suppressed", "favored",
    "risk_capped", "suppression_fallback"}`` plus — ONLY when the mode
    authors a reach (the evidence-key discipline) — ``{"reached",
    "reach_capped"}``. The authored semantics:

    * ``reach_kinds`` (P-043) ADMIT the engine's curated EXTENDED variants
      (``extended``, the ``_extended_variants`` pool for this problem) into
      emission — appended after the neutral pool in authored reach order
      (curated order within a kind). Reach is the ONLY admission path for
      extended kinds; the neutral pool never carries them. A reached kind
      whose curated translation risk (the profile's own ``kind_scores`` row,
      ``depth_cleanup`` fallback row for unknown kinds — the
      ``score_variant`` rule) ranks beyond the mode's ``allowed_risk`` is
      REFUSED fail-closed, surfaced in ``fork["reach_capped"]`` (the loader
      already rejects such authoring loudly; this guards loader-bypassing
      profiles). ``fork["reached"]`` lists the kinds actually present in
      THIS emission through reach (authored order) — [] where the extended
      pool holds nothing for the problem, where the cap refused, or where
      suppression removed them again.
    * ``suppress_kinds`` REMOVE their variants from emission — the
      candidate-SET fork, applied to the COMBINED (neutral + reached) pool,
      so suppression beats reach. ``fork["suppressed"]`` lists the kinds
      actually removed from THIS emission (authored order).
    * ``favor_kinds`` move their variants to the FRONT of emission (authored
      favor order; curated order within a kind) — order shaping only, never
      set growth: favoring can never add a kind the emission does not
      already hold (admission is ``reach_kinds``' job alone, so P-042's
      guarantee for the original seven is intact). ``fork["favored"]`` lists
      the kinds actually moved for THIS emission.
    * THE GOVERNANCE CAP: a favored kind beyond the mode's ``allowed_risk``
      is REFUSED, never elevated — surfaced in ``fork["risk_capped"]``
      (unchanged from P-042; the reach refusal above mirrors it).
    * NON-EMPTY GUARANTEE: suppression can never empty a candidate set. If
      it would, the FULL neutral curated set is emitted instead — the
      documented, profile-agnostic fallback (the engine's own pool, no
      profile data involved) — with ``fork["suppression_fallback"] = True``
      and ``fork["suppressed"] = []`` (nothing was actually removed). The
      fallback is NEUTRAL-POOL-ONLY: it never (re-)admits extended kinds,
      so ``fork["reached"]`` is [] on a fallback emission. Reached variants
      that SURVIVE suppression count as a non-empty set — a mode may
      legitimately emit extended variants alone.
    """
    kind_scores = prof.kind_scores
    cap = _RISK_RANK[decl["allowed_risk"]]

    # --- P-043: authored EXTENDED-vocabulary reach (admission) --------------
    reach = list(decl.get("reach_kinds") or [])
    reach_capped: List[str] = []
    admitted: List[Dict] = []
    if reach:
        by_kind: Dict[str, List[Dict]] = {}
        for v in extended:
            by_kind.setdefault(v["kind"], []).append(v)
        for k in reach:
            row = kind_scores.get(k, kind_scores.get("depth_cleanup", {}))
            risk = row.get("translation") if isinstance(row, dict) else None
            rank = _RISK_RANK.get(risk, len(TRANSLATION_RISK_LEVELS) - 1)
            if rank > cap:
                reach_capped.append(k)  # the cap wins — fail-closed refusal
            else:
                admitted.extend(by_kind.get(k, []))
    pool = list(variants) + admitted
    pool_kinds = {v["kind"] for v in pool}

    suppress = set(decl["suppress_kinds"])
    kept = [v for v in pool if v["kind"] not in suppress]
    fallback = bool(pool) and not kept
    if fallback:
        kept = list(variants)  # NEUTRAL pool only — a fallback never admits extended kinds
    suppressed = ([] if fallback
                  else [k for k in decl["suppress_kinds"] if k in pool_kinds])

    risk_capped: List[str] = []
    favored: List[str] = []
    kept_kinds = {v["kind"] for v in kept}
    for k in decl["favor_kinds"]:
        row = kind_scores.get(k, kind_scores.get("depth_cleanup", {}))
        risk = row.get("translation") if isinstance(row, dict) else None
        rank = _RISK_RANK.get(risk, len(TRANSLATION_RISK_LEVELS) - 1)
        if rank > cap:
            risk_capped.append(k)  # the cap wins — mode-level refusal, every branch
        elif k in kept_kinds:
            favored.append(k)
    if favored:
        front = [v for k in favored for v in kept if v["kind"] == k]
        kept = front + [v for v in kept if v["kind"] not in set(favored)]

    fork = {
        "suppressed": suppressed,
        "favored": favored,
        "risk_capped": risk_capped,
        "suppression_fallback": fallback,
    }
    if reach:  # evidence-key discipline: present ONLY when reach is authored
        fork["reached"] = [k for k in reach
                           if k not in reach_capped and k in kept_kinds]
        fork["reach_capped"] = reach_capped
    return kept, fork


def generate_variants(problem: Dict, result, mode: Optional[str] = None,
                      profile: Optional[ProducerProfile] = None) -> List[Dict]:
    """Candidate variants for one problem — MODE-FORKED per profile (P-042).

    The neutral curated pool (``_curated_variants``) is the engine's shared
    move vocabulary; the active ``mode``'s authored declarations, read from
    the PASSED ``profile`` (the additive P-029 parameter — default resolves
    to the reference), fork the CANDIDATE SET (suppression) and its emission
    order (favoring, capped by the mode's ``allowed_risk``). ``mode=None``,
    an unknown mode, or a mode without authored declarations emits the
    neutral pool byte-identically — pre-P-042 callers are unchanged.
    """
    variants = _curated_variants(problem, result)
    prof = profile or _DEFAULT_PROFILE
    decl = _mode_declarations(prof, mode)
    if decl is not None:
        # P-043: the engine's extended curated pool rides along so an
        # authored ``reach_kinds`` declaration can admit it; without a
        # declaring mode the extended pool is never even built — the
        # neutral path stays byte-identical.
        variants, _ = _fork_candidates(
            variants, decl, prof, _extended_variants(problem, result))
    return variants


def score_variant(variant: Dict, result, profile: Optional[ProducerProfile] = None) -> Dict:
    # P-029: per-call producer selection. The curated kind-score table, the risk
    # penalty, and the two caps are read from the PASSED ``profile`` (default = the
    # reference), and the same profile is threaded to the nudge/promotion layers —
    # so ``analyze(producer=…)`` steers variant scoring end to end.
    prof = profile or _DEFAULT_PROFILE
    kind_scores = prof.kind_scores
    risk_penalty = prof.risk_penalty
    nudge_cap = prof.creative_nudge_cap
    promotion_cap = prof.creative_promotion_cap

    base = dict(kind_scores.get(variant["kind"], kind_scores["depth_cleanup"]))
    numeric = ["technical", "physical_space", "emotional_hierarchy", "contrast", "vocal_belief", "excitement", "taste"]

    # Base overall on the curated dims, before any context nudge — this is the
    # axis governance ranks on, and the axis the cap binds.
    base_overall = sum(base[k] for k in numeric) / len(numeric) - risk_penalty[base["translation"]]

    # --- P-012: evidence-nudge layer (penalty-only, bounded, transparent) ----
    # Each fired nudge lowers a curated dim and emits an evidence line. The dims
    # carry the honest move; the *overall* effect is clamped to ±CREATIVE_NUDGE_CAP.
    fired = _apply_nudges(variant["kind"], result, prof)
    nudges: List[str] = []
    for dim, delta, reason in fired:
        base[dim] += delta
        nudges.append(reason)

    nudged_overall = sum(base[k] for k in numeric) / len(numeric) - risk_penalty[base["translation"]]
    # Clamp the SUMMED overall delta to ±CREATIVE_NUDGE_CAP. Worst case is
    # width_bloom under BOTH rows = -20 raw = -2.86 overall, clamped to -2.0;
    # vocal_ride under row-0 alone = -14 raw = -2.0 overall = exactly the cap.
    overall_delta = nudged_overall - base_overall
    if overall_delta < -nudge_cap:
        overall_delta = -nudge_cap
    elif overall_delta > nudge_cap:
        overall_delta = nudge_cap

    # --- P-016: evidence-PROMOTION layer (reward-only, bounded, transparent) --
    # Independent of the penalty path: each fired promotion raises a curated dim
    # and emits an evidence line. The SUMMED promotion overall-delta is clamped to
    # +CREATIVE_PROMOTION_CAP, exactly as the penalty path clamps to
    # -CREATIVE_NUDGE_CAP. Measured from the SAME curated base_overall so the two
    # bounded effects are additive and each independently bounded.
    promoted = _apply_promotions(variant["kind"], result, prof)
    for dim, delta, reason in promoted:
        base[dim] += delta
        nudges.append(reason)
    if promoted:
        promoted_overall = sum(base[k] for k in numeric) / len(numeric) - risk_penalty[base["translation"]]
        promotion_delta = (promoted_overall - base_overall) - overall_delta
        if promotion_delta > promotion_cap:
            promotion_delta = promotion_cap
        overall_delta += promotion_delta

    overall = base_overall + overall_delta
    overall = round(max(0.0, min(100.0, overall)), 1)

    verdict = "promising" if overall >= 80 else ("worth testing" if overall >= 70 else "marginal")
    if base["vocal_belief"] < 75:
        verdict += " — check vocal wash"

    scores = {
        "technical_score": base["technical"],
        "physical_space_score": base["physical_space"],
        "emotional_hierarchy_score": base["emotional_hierarchy"],
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


def _profile_default_mode(prof: ProducerProfile) -> str:
    """The profile's own deterministic default search mode (P-033).

    Resolution, in order — every candidate comes from the profile's OWN
    authored tables, so no reference mode name is hardcoded here:

    1. the profile's declared ``default_creative_mode["default_mode"]``, when
       that name exists in its ``search_modes`` — the mode the profile itself
       authors as its non-intimate default;
    2. otherwise the FIRST mode in the profile's ``search_modes`` (JSON
       authoring order, preserved by the loader) — a mode the profile is
       guaranteed to actually carry.
    """
    declared = prof.default_creative_mode.get("default_mode")
    if declared in prof.search_modes:
        return declared
    return next(iter(prof.search_modes))


def run_creative_engine(result, mode: Optional[str] = None,
                        profile: Optional[ProducerProfile] = None) -> Dict:
    # P-029: per-call producer selection. Search modes, the per-variant scoring
    # profile, and the philosophy line are read from the PASSED ``profile``
    # (default = the reference), so ``analyze(producer=…)`` drives the creative
    # engine. Passing ``profile is None`` reproduces the reference byte-for-byte.
    prof = profile or _DEFAULT_PROFILE
    search_modes = prof.search_modes
    # P-033: mode resolution is profile-owned. ``mode=None`` resolves to the
    # profile's own default (for the reference that is ``dramatic_contrast`` —
    # the same name this signature used to default to, so no-mode callers are
    # byte-identical). A REQUESTED mode absent from the profile's
    # ``search_modes`` resolves to the same profile-owned default and the
    # substitution is surfaced in ``search_mode_fallback`` below (present ONLY
    # when it happened — the ``score_nudges`` evidence-key discipline). The
    # old hardcoded ``"dramatic_contrast"`` substitute dereferenced a mode a
    # profile may not carry (a KeyError for any profile without that name).
    requested = mode
    if mode is None or mode not in search_modes:
        mode = _profile_default_mode(prof)
    problems = detect_creative_problems(result)
    # P-042: the resolved mode's authored declarations — non-None ONLY when
    # the mode forks (neutral/default modes leave every artifact byte
    # untouched, the ``score_nudges`` evidence-key discipline).
    decl = _mode_declarations(prof, mode)
    branches: List[Dict] = []
    for problem in problems:
        # P-042: the profile reaches the fork seam through the REAL call
        # chain — the resolved mode's authored declarations (this profile's,
        # not the reference's) fork candidate generation.
        variants = generate_variants(problem, result, mode, prof)
        for v in variants:
            v["scores"] = score_variant(v, result, prof)
        branch = {
            "problem": problem["problem"],
            "problem_id": problem["id"],
            "variants": variants,
            "winning": winning_variant(variants),
        }
        if decl is not None:
            # Requirement-10 honesty: the per-branch fork report is derived
            # by the SAME pure helpers, on the same inputs, that produced
            # the emission above — what was ACTUALLY suppressed/favored for
            # this branch, any allowed-risk refusal, and whether the
            # non-empty fallback fired. Identical pure functions, identical
            # inputs: the report cannot drift from the emission.
            _, branch["mode_fork"] = _fork_candidates(
                _curated_variants(problem, result), decl, prof,
                _extended_variants(problem, result))
        branches.append(branch)
    out = {
        "search_mode": mode,
        "search_mode_bias": search_modes[mode]["bias"],
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
        "philosophy": prof.philosophy,
    }
    # P-042 (requirement 10): echo the resolved mode's AUTHORED declarations
    # so a reader can explain WHY this run's candidate sets differ — present
    # ONLY when the mode actually forks (neutral/default runs, the committed
    # sample trees included, carry zero new bytes).
    if decl is not None:
        out["search_mode_declarations"] = {
            "allowed_risk": decl["allowed_risk"],
            "favor_kinds": list(decl["favor_kinds"]),
            "suppress_kinds": list(decl["suppress_kinds"]),
        }
        # P-043: the authored reach echoes ONLY when it exists (the same
        # evidence-key discipline) — a forking-but-not-reaching mode's
        # artifact stays byte-identical to its P-042 form.
        if decl["reach_kinds"]:
            out["search_mode_declarations"]["reach_kinds"] = list(decl["reach_kinds"])
    # P-033: observational fallback evidence — present ONLY when a requested
    # mode was substituted (never on the ``mode=None`` default resolution, and
    # never when the requested mode exists in the profile's table).
    # P-038: the reason states WHICH resolution branch fired — the profile's
    # declared default, or (when that is absent from ``search_modes`` too)
    # the first authored mode. The old wording said "the profile's own
    # default" on both branches, inaccurately on the second.
    if requested is not None and requested != mode:
        if mode == prof.default_creative_mode.get("default_mode"):
            resolved_how = f"resolved to the profile's declared default {mode!r}"
        else:
            resolved_how = (
                f"resolved to the first mode in the profile's own "
                f"search_modes, {mode!r} (its declared default is not "
                f"authored there either)"
            )
        out["search_mode_fallback"] = {
            "requested_mode": requested,
            "resolved_mode": mode,
            "reason": (
                f"requested mode {requested!r} is not one of this profile's "
                f"search_modes; {resolved_how}"
            ),
        }
    return out
