"""Doctrine engine: turns the analysis into Halee/Ramone scores + warnings.

Every score is 0-100 and carries evidence. The engine never invents numbers it
cannot justify; when there is not enough information (e.g. fewer than two
sections) it says so rather than guessing.
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS
from .producer_profile import ProducerProfile, load_profile

FORWARD = {"intimate", "foreground"}

# The producer-specific judgment constants (component weights, per-scorer
# baselines, penalty coefficients, thresholds and bonuses) are SOURCED from the
# reference producer profile — the JSON is now their single source of truth
# (P-025 captured them; P-028 sources them). The PHYSICS/measurement code
# (forward-layer occupancy, band analysis, section spread via pstdev, distinct
# depth counting) stays IN the functions below; only the aesthetic numbers move
# to the profile, so the formula shape and evaluation order are byte-identical.
#
# Read-only in the consumers: every scorer does dict ``[...]`` reads off these
# shared structures, never an in-place mutation (the no-aliasing proof in
# ``tests/test_doctrine_profile_sourced.py`` is binding).
_DEFAULT_PROFILE = load_profile("halee_ramone")
_DOCTRINE = _DEFAULT_PROFILE.doctrine
_WEIGHTS = _DOCTRINE["weights"]
_BASELINES = _DOCTRINE["baselines"]
_PENALTY_COEFFS = _DOCTRINE["penalty_coeffs"]
# Per-function aesthetic constants for the five remaining scorers (P-028
# Finding A widened the profile to cover them): baseline, bonuses, penalties,
# coefficients and thresholds, each captured verbatim.
_SCORERS = _DOCTRINE["scorers"]


def _clamp(x: float) -> float:
    return round(max(0.0, min(100.0, x)), 1)


def score_doctrine(
    records: List[Dict],
    sections_analysis: List[Dict],
    masking_report: Dict,
    mix_metrics: Optional[Dict],
    intent: Optional[Dict] = None,
    profile: Optional[ProducerProfile] = None,
    groove: Optional[Dict] = None,
) -> Dict:
    # P-029: per-call producer selection. When ``profile is None`` the reference
    # ``_DEFAULT_PROFILE`` is used, so every existing caller (and the no-arg
    # pipeline path) stays byte-identical; when a profile IS passed, EVERY scorer
    # reads ITS doctrine constants, so ``analyze(producer=…)`` is a live lever.
    doctrine = (profile or _DEFAULT_PROFILE).doctrine
    events = masking_report.get("events", [])
    lead = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)
    warnings: List[Dict] = []

    halee, halee_ev = _halee(records, events, doctrine)
    ramone, ramone_ev = _ramone(records, lead, events, warnings, doctrine)
    vocal, vocal_ev = _vocal_centrality(lead, events, doctrine)
    depth, depth_ev = _depth_hierarchy(records, doctrine)
    contrast, contrast_ev = _section_contrast(sections_analysis, warnings, doctrine)
    static, static_ev = _static_mix(records, lead, events, mix_metrics, doctrine)
    dynamic, dynamic_ev = _dynamic_mix(sections_analysis, doctrine)
    # P-032e: the new producer-agnostic beat_identity axis. Appended LAST below so
    # the pre-existing 7-term summation order is preserved and ``overall`` stays
    # bit-identical for halee_ramone (its beat_identity weight is 0).
    beat, beat_ev = _beat_identity(records, events, doctrine)
    # P-032a: the second producer-agnostic axis — absolute arrangement room /
    # sparsity. Appended LAST (after beat_identity) so the pre-existing 8-term
    # summation order is preserved and ``overall`` stays bit-identical for
    # halee_ramone (its negative_space weight is 0).
    ns, ns_ev = _negative_space(records, sections_analysis, mix_metrics, doctrine)
    # P-032b: the third producer-agnostic axis — groove regularity/consistency as
    # a proxy for coherence. This is the FIRST live-wired axis: ``groove`` is
    # computed by ``analyze_groove`` BEFORE this call in the pipeline and threaded
    # in (default ``None`` keeps every existing caller byte-identical, via the
    # scorer's neutral fallback). Appended LAST (after negative_space) so the
    # pre-existing 9-term summation order is preserved and ``overall`` stays
    # bit-identical for halee_ramone (its groove_coherence weight is 0).
    gc, gc_ev = _groove_coherence(groove, doctrine)
    # P-032d: the fourth producer-agnostic axis — rhythmic surprise in its WEAK,
    # section-aggregate form (cross-section transient-density variation). ONE
    # input (``sections_analysis``), zero new plumbing. Appended LAST (after
    # groove_coherence) so the pre-existing 10-term summation order is preserved
    # and ``overall`` stays bit-identical for halee_ramone (its
    # rhythmic_surprise weight is 0).
    rs, rs_ev = _rhythmic_surprise(sections_analysis, doctrine)
    # P-032c: the fifth producer-agnostic axis — the low-end POCKET (kick/sub
    # relationship + room around the bass). Presence is a GATE only; the score
    # rewards the relationship and the room, never sheer bass level. Pure
    # additive: every input below is already in this function's arguments (zero
    # new plumbing). Appended LAST (after rhythmic_surprise) so the pre-existing
    # 11-term summation order is preserved and ``overall`` stays bit-identical
    # for halee_ramone (its low_end_motion weight is 0).
    lem, lem_ev = _low_end_motion(records, sections_analysis, masking_report, mix_metrics, doctrine)
    # P-032g: the sixth producer-agnostic axis — loop context (static vs
    # iconic). THE HINGE / the doctrine-pin exemplar: the engine DETECTS the
    # loop's context OBSERVATIONALLY (dominant + no sectional evolution =
    # static; dominant + groove-carrying function = iconic); the PROFILE
    # decides what to do about the reading (deconstruct vs protect — that
    # decision lives in profile JSON, never here). Appended LAST (after
    # low_end_motion) so the pre-existing 12-term summation order is preserved
    # and ``overall`` stays bit-identical for halee_ramone (its loop_context
    # weight is 0).
    lc, lc_ev = _loop_context(records, sections_analysis, masking_report, doctrine)
    # P-032f: the seventh producer-agnostic axis — vocal-role FIT. The engine
    # DETECTS vocal function on the record (``vocal_type`` /
    # ``vocal_type_confidence``, classified once in the pipeline); this axis
    # reads those types against the masking events OBSERVATIONALLY. The
    # masking PHILOSOPHY (whether a chop/stack blending into the bed is
    # acceptable) is profile-authored, never engine-coded. Appended LAST
    # (after loop_context) so the pre-existing 13-term summation order is
    # preserved and ``overall`` stays bit-identical for halee_ramone (its
    # vocal_role_fit weight is 0).
    vrf, vrf_ev = _vocal_role_fit(records, events, doctrine)

    component_scores = {
        "halee_score": halee,
        "ramone_score": ramone,
        "vocal_centrality_score": vocal,
        "depth_hierarchy_score": depth,
        "section_contrast_score": contrast,
        "static_mix_score": static,
        "dynamic_mix_score": dynamic,
        "beat_identity_score": beat,
        "negative_space_score": ns,
        "groove_coherence_score": gc,
        "rhythmic_surprise_score": rs,
        "low_end_motion_score": lem,
        "loop_context_score": lc,
        "vocal_role_fit_score": vrf,
    }
    weights = doctrine["weights"]
    present = {k: v for k, v in component_scores.items() if v is not None}
    overall = (
        _clamp(sum(present[k] * weights[k] for k in present) / sum(weights[k] for k in present))
        if present
        else None
    )

    return {
        **component_scores,
        "overall_mix_readiness_score": overall,
        "evidence": {
            "halee": halee_ev,
            "ramone": ramone_ev,
            "vocal_centrality": vocal_ev,
            "depth_hierarchy": depth_ev,
            "section_contrast": contrast_ev,
            "static_mix": static_ev,
            "dynamic_mix": dynamic_ev,
            "beat_identity": beat_ev,
            "negative_space": ns_ev,
            "groove_coherence": gc_ev,
            "rhythmic_surprise": rs_ev,
            "low_end_motion": lem_ev,
            "loop_context": lc_ev,
            "vocal_role_fit": vrf_ev,
        },
        "warnings": warnings,
    }


# --------------------------------------------------------------------------- #
def _halee(records: List[Dict], events: List[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["penalty_coeffs"]["halee"]
    score = doctrine["baselines"]["halee"]
    ev: List[str] = []
    n = len(records) or 1

    fg_frac = sum(1 for r in records if r["depth_default"] in FORWARD) / n
    if fg_frac > c["forward_threshold"]:
        penalty = (fg_frac - c["forward_threshold"]) * c["forward_occupancy"]
        score -= penalty
        ev.append(f"{fg_frac:.0%} of elements sit in forward layers; depth is collapsing.")
    else:
        ev.append(f"Forward-layer occupancy is healthy ({fg_frac:.0%}).")

    felt_fg = [r for r in records if r["perceptual_role"] == "felt" and r["depth_default"] in FORWARD]
    if felt_fg:
        score -= c["felt_forward"] * len(felt_fg)
        ev.append(f"{len(felt_fg)} felt element(s) sit too far forward: " + ", ".join(r["name"] for r in felt_fg) + ".")

    width_events = [e for e in events if e["classification"] == "width_crowding"]
    if width_events:
        score -= c["width_crowding"] * len(width_events)
        ev.append(f"{len(width_events)} section(s) show stereo-width crowding (artificial width).")

    loop_fg = [
        r for r in records
        if r["source_kind"] in LOOP_SAMPLE_KINDS
        and r["depth_default"] in FORWARD
        and r.get("stereo_width", 0) > 0.6
    ]
    if loop_fg:
        score -= c["loop_foregrounded"] * len(loop_fg)
        ev.append("Full-width loop(s) foregrounded: " + ", ".join(r["name"] for r in loop_fg) + ".")

    return _clamp(score), ev


def _ramone(records: List[Dict], lead: Optional[Dict], events: List[Dict],
            warnings: List[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["penalty_coeffs"]["ramone"]
    score = doctrine["baselines"]["ramone"]
    ev: List[str] = []
    if lead is None:
        score -= c["no_lead"]
        ev.append("No identified lead vocal — the emotional centre is undefined.")
        warnings.append({
            "warning": "No lead vocal identified. Confirm the emotional centre before mixing.",
            "doctrine": ["phil_ramone_vocal_centrality"],
        })
    else:
        bad_vocal = [e for e in events if lead["name"] in e["elements"] and e["classification"] == "bad_masking"]
        if bad_vocal:
            score -= c["vocal_masked"] * len(bad_vocal)
            ev.append(f"Vocal masked by {len(bad_vocal)} forward element(s).")
        else:
            ev.append("Vocal is not critically masked by forward elements.")

    n = len(records) or 1
    decorative = [r for r in records if r["sacredness"] in {"decorative", "expendable"}]
    if len(decorative) / n > c["decorative_threshold"]:
        score -= c["decorative_penalty"]
        ev.append(f"{len(decorative)} decorative/expendable element(s); risk of overmixing.")
        warnings.append({
            "warning": "Many decorative elements relative to core. Consider subtraction before processing.",
            "doctrine": ["phil_ramone_restraint", "sacred_vs_expendable"],
        })
    return _clamp(score), ev


def _vocal_centrality(lead: Optional[Dict], events: List[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["scorers"]["vocal_centrality"]
    if lead is None:
        return c["no_lead_score"], ["No lead vocal present."]
    score = c["baseline"]
    ev = [f"Lead vocal '{lead['name']}' identified."]
    if lead["sacredness"] == "sacred":
        score += c["sacred_bonus"]
        ev.append("Vocal correctly marked sacred.")
    if lead["depth_default"] in FORWARD:
        score += c["forward_bonus"]
        ev.append(f"Vocal sits in the {lead['depth_default']} layer.")
    bad = [e for e in events if lead["name"] in e["elements"] and e["classification"] == "bad_masking"]
    if bad:
        score -= c["masked_coeff"] * len(bad)
        ev.append(f"Vocal challenged by {len(bad)} masking conflict(s).")
    return _clamp(score), ev


def _depth_hierarchy(records: List[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["scorers"]["depth_hierarchy"]
    depths = [r["depth_default"] for r in records]
    distinct = len(set(depths))
    n = len(records) or 1
    score = c["baseline"] + distinct * c["per_distinct"]
    fg_frac = sum(1 for d in depths if d in FORWARD) / n
    if fg_frac > c["forward_threshold"]:
        score -= (fg_frac - c["forward_threshold"]) * c["forward_occupancy"]
    ev = [f"{distinct} of 4 depth layers used; {fg_frac:.0%} forward."]
    if distinct <= 1:
        ev.append("Everything occupies one layer — no hierarchy.")
    return _clamp(score), ev


def _section_contrast(sections: List[Dict], warnings: List[Dict], doctrine: Dict = _DOCTRINE):
    coeffs = doctrine["scorers"]["section_contrast"]
    if len(sections) < 2:
        return None, ["Fewer than two sections analysed; contrast cannot be scored."]
    lift_fail = 0
    for s in sections:
        c = s.get("contrast_vs_previous", {})
        if "warning" in c:
            lift_fail += 1
            warnings.append({"warning": c["warning"], "doctrine": ["section_contrast"]})
    score = coeffs["baseline"] - coeffs["lift_fail_penalty"] * lift_fail
    ev = [f"{lift_fail} section(s) fail to lift relative to the previous section."]
    return _clamp(score), ev


def _static_mix(records: List[Dict], lead: Optional[Dict], events: List[Dict],
                mix_metrics: Optional[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["scorers"]["static_mix"]
    score = c["baseline"]
    ev: List[str] = []
    if mix_metrics:
        if mix_metrics.get("peak_dbfs", -1) > c["peak_ceiling"]:
            score -= c["peak_penalty"]
            ev.append("Mixdown is at/over full scale — clipping risk.")
        bands = mix_metrics.get("band_energy", {})
        if bands:
            dominant = max(bands, key=bands.get)
            if bands[dominant] > c["dominant_band_threshold"]:
                score -= c["dominant_band_penalty"]
                ev.append(f"Tonal balance skewed: '{dominant}' band holds {bands[dominant]:.0%} of energy.")
            else:
                ev.append("Broad tonal balance is reasonable.")
    crit_low = [e for e in events if e["classification"] == "low_end_conflict" and e["severity"] == "critical"]
    if crit_low:
        score -= c["crit_low_coeff"] * len(crit_low)
        ev.append(f"{len(crit_low)} critical low-end (kick/bass) conflict(s).")
    if lead is None:
        score -= c["no_lead_penalty"]
        ev.append("No lead vocal to anchor intelligibility.")
    return _clamp(score), ev


def _dynamic_mix(sections: List[Dict], doctrine: Dict = _DOCTRINE):
    c = doctrine["scorers"]["dynamic_mix"]
    if len(sections) < 2:
        return c["insufficient_sections_score"], ["Fewer than two sections; dynamic movement cannot be assessed."]
    rms = [s["metrics"]["rms_dbfs"] for s in sections]
    width = [s["metrics"]["width"] for s in sections]
    bright = [s["metrics"]["brightness"] for s in sections]
    rms_std = statistics.pstdev(rms) if len(rms) > 1 else 0.0
    width_std = statistics.pstdev(width) if len(width) > 1 else 0.0
    bright_std = statistics.pstdev(bright) if len(bright) > 1 else 0.0
    score = c["baseline"] + rms_std * c["rms_coeff"] + width_std * c["width_coeff"] + bright_std * c["bright_coeff"]
    lift_fail = sum(1 for s in sections if "warning" in s.get("contrast_vs_previous", {}))
    score -= c["lift_fail_penalty"] * lift_fail
    ev = [
        f"Section RMS spread {rms_std:.1f} dB, width spread {width_std:.2f}, "
        f"brightness spread {bright_std:.2f}."
    ]
    if score < 55:
        ev.append("Sections are too similar — the mix is balanced but emotionally static.")
    return _clamp(score), ev


def _beat_identity(records: List[Dict], events: List[Dict], doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for the STRENGTH of a central rhythmic fingerprint.

    This is the "first second producer" epic's hardest axis (P-032e), front-loaded
    to prove the signal is HONESTLY MEASURABLE on exported stems. It answers ONE
    question — *is there a central, undeniable rhythmic element* — from transient
    physics alone. Candidacy is by ``transient_density`` (a stem PUNCHES), NEVER by
    instrument label, so the axis is producer-agnostic: a mouth-beat, a tabla, a
    synth knock and a chopped loop are all just "high-transient stems" here.

    HONEST BOUNDARIES — three things are explicitly OUT OF SCOPE and NOT faked:
      1. Fingerprint TYPING (mouth-sound vs tabla vs synth-knock vs beatbox) — NOT
         measurable on exported stems. We never name WHAT the beat is, only that a
         strong one exists.
      2. Onset REGULARITY / IOI — a real signal, but it is NOT visible at
         ``score_doctrine`` time (it lives in the post-doctrine groove analyzer;
         wiring it in is P-032b). We do NOT use it here.
      3. "More undeniable after a move" — needs a before/after render; out of scope
         in plan-only v1.

    Strength is composed from:
      * Presence — at least one stem clears the ``transient_floor`` (else ``no_beat``).
      * Distinctness/dominance — the top candidate's ``transient_density`` above the
        track-median transient_density (a beat that stands out from the bed is more
        undeniable), scaled by ``dominance_coeff``.
      * Definition — the dominant stem's ``crest_factor_db`` above threshold (punchy,
        defined hits vs smeared) → ``definition_bonus``.
      * Foreground/unmasked — the dominant stem sits in a forward/heard layer and is
        NOT ``bad_masking`` → ``foreground_bonus``; buried (felt/background) → a
        ``buried_penalty``; masked → a ``masked_penalty`` (the fingerprint exists but
        is not *undeniable*).
    """
    c = doctrine["scorers"]["beat_identity"]
    ev: List[str] = []

    def _td(r: Dict) -> float:
        return float(r.get("metrics", {}).get("transient_density", 0.0) or 0.0)

    def _crest(r: Dict) -> float:
        return float(r.get("metrics", {}).get("crest_factor_db", 0.0) or 0.0)

    densities = [_td(r) for r in records]
    # Agnostic candidacy: a rhythmic candidate is any stem whose transient physics
    # clear the floor — decided by transient_density, not by instrument identity.
    candidates = [r for r in records if _td(r) >= c["transient_floor"]]
    if not candidates:
        ev.append("No stem clears the transient floor — no defined rhythmic element present.")
        return _clamp(c["no_beat"]), ev

    dominant = max(candidates, key=_td)
    dom_td = _td(dominant)
    median_td = statistics.median(densities) if densities else 0.0

    score = c["baseline"]
    ev.append(f"Rhythmic fingerprint present: '{dominant['name']}' punches hardest (transient_density {dom_td:.2f}).")

    # Distinctness/dominance: how far the top candidate stands above the bed.
    lift = max(0.0, dom_td - median_td)
    if lift > 0:
        score += lift * c["dominance_coeff"]
        ev.append(f"It stands out from the bed (+{lift:.2f} over the track median).")
    else:
        ev.append("It does not stand out above the track median — the beat blends into the bed.")

    # Definition: punchy, defined hits vs a smeared transient.
    dom_crest = _crest(dominant)
    if dom_crest >= c["definition_crest_db"]:
        score += c["definition_bonus"]
        ev.append(f"Hits are well-defined (crest {dom_crest:.1f} dB).")

    # Foreground/unmasked: an undeniable fingerprint is heard, forward and clear.
    masked = any(
        dominant["name"] in e.get("elements", []) and e.get("classification") == "bad_masking"
        for e in events
    )
    forward = dominant["depth_default"] in FORWARD and dominant["perceptual_role"] in {"heard", "structural"}
    if forward and not masked:
        score += c["foreground_bonus"]
        ev.append("The fingerprint is foregrounded and unmasked — undeniable.")
    else:
        if not forward:
            score -= c["buried_penalty"]
            ev.append("The fingerprint is buried (felt/background) — present but not undeniable.")
        if masked:
            score -= c["masked_penalty"]
            ev.append("The fingerprint is masked by a forward element — its identity is challenged.")

    return _clamp(score), ev


def _negative_space(records: List[Dict], sections: List[Dict],
                    mix_metrics: Optional[Dict], doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for ABSOLUTE arrangement room / sparsity.

    This is the SECOND new agnostic axis (P-032a), after the P-032e
    ``beat_identity`` crux proved the add-an-axis-byte-identically pattern. It
    answers a DIFFERENT question from ``dynamic_mix``: not *does the arrangement
    MOVE section-to-section* (that is ``dynamic_mix``: pstdev of rms/width/
    brightness + lift-fail), but *does the arrangement leave ROOM at all* —
    "silence is arrangement" (the user's framing). A wall-to-wall-dense mix that
    still varies section-to-section scores HIGH on ``dynamic_mix`` but LOW here,
    because it is packed: the two axes are conceptually distinct, not a
    re-derivation of one another.

    Room, as a STRENGTH, is composed from section-aggregate physics only:
      * Absolute room — reward low mean spectral ``density`` (occupancy):
        ``room = (density_ceiling - mean_density) * room_coeff``. More empty
        spectrum = more room = higher score. Falls back to whole-mix
        ``mix_metrics["density"]`` when there are no sections.
      * Sparse-section presence ("silence as arrangement") — reward a genuine
        dropout: the spread ``max_section_density - min_section_density`` above a
        small ``dropout_floor`` (so a section that pulls right back is rewarded).
        Needs >=2 sections; skipped gracefully otherwise.
      * Transient breathing room — reward low mean section ``transient_density``
        (space between hits): ``(transient_ceiling - mean_transient) *
        breathing_coeff``; a wall-to-wall-transient section earns none of it.

    Always returns a clamped float (never None) — a documented NEUTRAL fallback
    when there is neither section nor mix data — so the axis is always present
    (mirrors ``_beat_identity``'s always-float discipline).

    HONEST BOUNDARY — DEFERRED, NOT FAKED: this works at the SECTION-AGGREGATE
    level. True sample-level **inter-onset silence gaps** — the actual space
    BETWEEN individual hits — require onset timing, which is NOT visible at
    ``score_doctrine`` time (it lives in the post-doctrine groove analyzer;
    plumbing it in is P-032b). We do NOT claim sample-level gap detection here;
    we measure occupancy and pull-back at the section grain only.
    """
    c = doctrine["scorers"]["negative_space"]
    ev: List[str] = []

    def _dens(s: Dict) -> Optional[float]:
        v = s.get("metrics", {}).get("density")
        return float(v) if v is not None else None

    def _trans(s: Dict) -> Optional[float]:
        v = s.get("metrics", {}).get("transient_density")
        return float(v) if v is not None else None

    densities = [d for d in (_dens(s) for s in sections) if d is not None]
    transients = [t for t in (_trans(s) for s in sections) if t is not None]

    # No section signal: fall back to the whole-mix density if present, else the
    # documented neutral (the axis is always a float).
    if not densities:
        mix_density = None
        if mix_metrics is not None and mix_metrics.get("density") is not None:
            mix_density = float(mix_metrics["density"])
        if mix_density is None:
            ev.append("No section or mix density available — neutral room fallback.")
            return _clamp(c["neutral"]), ev
        score = c["baseline"] + max(0.0, c["density_ceiling"] - mix_density) * c["room_coeff"]
        ev.append(f"No sections analysed; whole-mix occupancy {mix_density:.2f} gives room from the mix fallback.")
        return _clamp(score), ev

    mean_density = statistics.mean(densities)
    score = c["baseline"]

    # Absolute room: low occupancy => more empty spectrum => more room.
    room = max(0.0, c["density_ceiling"] - mean_density) * c["room_coeff"]
    score += room
    ev.append(f"Mean section occupancy {mean_density:.2f} → absolute room {room:.1f}.")

    # Transient breathing room: space between hits at the section grain.
    if transients:
        mean_trans = statistics.mean(transients)
        breathing = max(0.0, c["transient_ceiling"] - mean_trans) * c["breathing_coeff"]
        score += breathing
        if mean_trans >= c["transient_ceiling"]:
            ev.append("Wall-to-wall transients — no breathing room between hits.")
        else:
            ev.append(f"Transient breathing room (mean transient density {mean_trans:.2f}) → +{breathing:.1f}.")

    # Sparse-section presence ("silence as arrangement"): reward a genuine
    # dropout — a section that pulls right back below the busiest one.
    if len(densities) >= 2:
        spread = max(densities) - min(densities)
        dropout = max(0.0, spread - c["dropout_floor"]) * c["dropout_coeff"]
        if dropout > 0:
            score += dropout
            ev.append(f"A section pulls back (density spread {spread:.2f}) — silence used as arrangement.")
        else:
            ev.append("No section genuinely drops out — the arrangement stays uniformly filled.")
    else:
        ev.append("Only one section — a dropout cannot be assessed.")

    return _clamp(score), ev


def _groove_coherence(groove: Optional[Dict], doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for groove REGULARITY / CONSISTENCY.

    This is the THIRD new agnostic axis (P-032b) and the FIRST *live-wired* one:
    it reads a signal — ``analyze_groove``'s ``overall_regularity`` (mean per-track
    ``1 − CoV(IOIs)``, i.e. rhythmic tightness) — that used to be computed AFTER
    ``score_doctrine`` in the pipeline. To feed it to doctrine the pipeline now
    computes ``groove`` ONCE, BEFORE this call, and threads it in here; the same
    object is reused for ``result.expanded["groove"]`` (behavior-preserving).

    HONEST NAMING — this does NOT overclaim. ``overall_regularity`` measures
    rhythmic tightness/consistency, NOT "identity coherence" in the full sense. We
    therefore score groove regularity/consistency as a *proxy* for coherence, and
    say so in the evidence. And we do NOT bake in a "tighter = better" bias — the
    groove analyzer's own doctrine is "the doctrine does not assume tighter is
    better — it reports the feel." A machine-tight groove and a loose/human one are
    both valid; the AGNOSTIC layer stays neutral and only reports how consistent
    the groove is. A *producer* chooses whether (and how) to weight this axis (for
    ``halee_ramone`` the weight is 0, so it is inert). The evidence never asserts
    that any regularity is objectively "better".

    Mapping (all constants sourced read-only from
    ``doctrine["scorers"]["groove_coherence"]``):
      * ``overall_regularity`` present (0..1) → ``baseline + regularity *
        regularity_scale``, clamped 0..100. A coherent, consistent groove
        (regularity near 1) scores high; an incoherent/loose one (regularity near
        0) scores low. This is a report of consistency, not a value judgement.
      * ``groove is None`` (no rhythm-track signal available at all — e.g. the
        backward-compat default when doctrine is called without threading) OR
        ``overall_regularity is None`` (rhythm stems present but too few onsets to
        judge, or no rhythm stems) → a documented NEUTRAL fallback float. Never
        None, never a crash. The neutral sits deliberately BETWEEN a coherent and
        an incoherent groove: absence is neither rewarded as coherence nor punished
        as maximal incoherence.

    Optionally reads per-track regularities for evidence colour only; the score is
    driven by ``overall_regularity`` (the analyzer's aggregate).
    """
    c = doctrine["scorers"]["groove_coherence"]
    ev: List[str] = []

    overall = None if groove is None else groove.get("overall_regularity")

    if overall is None:
        if groove is None:
            ev.append("No groove signal available — neutral groove-coherence fallback.")
        else:
            ev.append("No rhythm-track regularity to judge — neutral groove-coherence fallback.")
        return _clamp(c["neutral"]), ev

    overall = float(overall)
    score = c["baseline"] + overall * c["regularity_scale"]

    # Evidence names REGULARITY/CONSISTENCY as a PROXY for coherence — never
    # "tighter is better". We report the feel; the producer decides how to weight.
    graded = [
        t for t in (groove.get("per_track") or [])
        if t.get("regularity") is not None
    ]
    if graded:
        ev.append(
            f"Groove regularity/consistency {overall:.3f} across {len(graded)} "
            f"rhythm track(s) — scored as a proxy for coherence (not 'tighter is good')."
        )
    else:
        ev.append(
            f"Groove regularity/consistency {overall:.3f} — scored as a proxy for "
            f"coherence (not 'tighter is good')."
        )

    return _clamp(score), ev


def _rhythmic_surprise(sections: List[Dict], doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for rhythmic surprise/variation — WEAK FORM ONLY.

    This is the FOURTH new agnostic axis (P-032d): the smallest lift of the
    P-032.x sub-arc — ONE input (section ``transient_density``), pure additive,
    zero new plumbing. It rewards the arrangement CHANGING its rhythmic
    intensity across sections: "the beat drops out / the fill hits", measured in
    aggregate form.

    HONEST SCOPE — this is the WEAK, SECTION-AGGREGATE form and says so in its
    evidence. It measures exactly two things over per-section
    ``metrics.transient_density``:
      * Spread — ``statistics.pstdev`` of the per-section values, scaled by
        ``spread_coeff`` (the ``_dynamic_mix`` idiom applied to the one signal
        that scorer never reads).
      * Largest swing — the max ``|Δ transient_density|`` between ADJACENT
        sections, scaled by ``swing_coeff`` — a beat dropping out (or slamming
        in) between neighbouring sections, at the section grain.

    DEFERRED, NOT FAKED — the STRONG form of rhythmic surprise needs onset
    timing/sequence, which is groove territory and NOT visible here:
      1. Fill detection (a burst of extra hits before a boundary).
      2. Unexpected-hit detection (a hit off the established grid).
      3. Per-onset IOI deviation (moment-to-moment surprise within a section).
    None of these are claimed or approximated. And this scorer must NOT read
    the groove signal (``overall_regularity``) — that is ``_groove_coherence``'s
    input; re-reading it here would duplicate that axis.

    DISTINCTNESS — this is the ONLY axis keyed on the *VARIATION* of section
    transient_density: ``_negative_space`` reads its MEAN (central tendency —
    the opposite statistic); ``_dynamic_mix`` reads pstdev of
    rms/width/brightness (never transient_density); ``_beat_identity`` reads
    per-STEM transient dominance; ``_section_contrast`` counts lift-fail
    warnings. A high-mean but ZERO-VARIANCE transient bed scores LOW here even
    though the mean-reading and stem-reading axes may score it high.

    Fewer than two sections with the metric → the documented
    ``insufficient_sections_score`` fallback (mirrors ``_dynamic_mix``'s
    idiom). Always returns a clamped float, never None.
    """
    c = doctrine["scorers"]["rhythmic_surprise"]
    ev: List[str] = []

    transients = [
        float(v)
        for v in (s.get("metrics", {}).get("transient_density") for s in sections)
        if v is not None
    ]

    if len(transients) < 2:
        ev.append(
            "Fewer than two sections with transient data; rhythmic surprise "
            "(weak, section-aggregate form) cannot be assessed."
        )
        return _clamp(c["insufficient_sections_score"]), ev

    spread = statistics.pstdev(transients)
    swing = max(abs(b - a) for a, b in zip(transients, transients[1:]))
    score = c["baseline"] + spread * c["spread_coeff"] + swing * c["swing_coeff"]

    ev.append(
        f"Cross-section transient-density spread {spread:.3f}, largest adjacent-"
        f"section swing {swing:.3f} — the weak, section-aggregate form of "
        f"rhythmic surprise (fill/unexpected-hit/per-onset detection deferred)."
    )
    if spread == 0.0:
        ev.append(
            "Transient density is constant across sections — no rhythmic "
            "surprise at the section grain."
        )
    return _clamp(score), ev


def _low_end_motion(records: List[Dict], sections_analysis: List[Dict],
                    masking_report: Dict, mix_metrics: Optional[Dict],
                    doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for the low-end POCKET — the kick/sub
    relationship plus ROOM around the bass.

    This is the FIFTH new agnostic axis (P-032c) and a PRODUCER-PROFILE
    PRIMITIVE, not any single producer's hack: it measures a neutral,
    relational property of the low end that different profiles weight and
    interpret differently (a pocket/impact/sub-kick producer, a natural-
    foundation balance producer, a translation/controlled-sub-density pop
    profile, a sub-identity/808-space trap profile). The scorer itself stays
    relational; the producer decides what it is worth (for ``halee_ramone``
    the weight is 0, so it is inert).

    THE CORE DESIGN RULE — "more bass" must NOT win: a clean low-end
    RELATIONSHIP beats high low-end QUANTITY, always. Low-end PRESENCE is a
    GATE only: ``band_energy["low"]`` (the 20-120Hz sub fraction) is only ever
    COMPARED against the ``low_floor`` / ``stack_floor`` thresholds, never
    multiplied into the score. The SCORE comes from the RELATIONSHIP and the
    ROOM:
      * Presence GATE — at least one stem clears ``low_floor`` on its sub
        fraction (falling back to ``mix_metrics["band_energy"]["low"]`` when
        no stem does); else the documented ``no_low_end`` neutral-low float
        (the ``_beat_identity`` ``no_beat`` idiom). No records AND no mix
        band data at all → the documented ``neutral`` fallback instead
        (absence of signal is not evidence of an absent low end). Always a
        clamped float, never None.
      * Reserved sub / room — QUALIFIED, never sufficient on its own. FEW
        stems carrying the sub band (1..``reserved_max`` clearing
        ``stack_floor``) read as reserved room ONLY when the carriers also
        BEHAVE like a pocket: no critical collision (clean) AND a defined,
        non-smeared envelope somewhere in the low end (the punchiest carrier
        clears ``defined_crest_db``). Then ``reserved_bonus`` fires. One
        giant smeared or colliding blob swallowing the whole floor is
        technically "fewest carriers" but is the OPPOSITE of room — it takes
        ``blob_penalty`` instead. A pile-up over the ceiling is penalized per
        extra stem (``stack_penalty``); gate passed via the mix fallback only
        (a diffuse low end no stem distinctly carries) earns nothing.
      * Relationship, weak form — existing ``low_end_conflict`` masking
        events break the pocket, scaled by severity
        (``critical_conflict_penalty`` / ``moderate_conflict_penalty``; a
        critical collision ALSO disqualifies the reserved reading above); and
        complementary punch-vs-sustain among the carriers is rewarded: the
        punchiest carrier's ``crest_factor_db`` minus the most sustained
        carrier's, capped at ``complement_cap_db`` and scaled by
        ``complement_coeff``. A single smeared carrier with no punch partner
        earns no complementarity — a blob, not a defined pocket.

    PHYSICS PRIMARY — ``instrument_identity`` / ``identity_family`` labels are
    a corroborating tie-break ONLY, never the gate: they break exact
    crest-factor ties when picking the punchiest/most-sustained carrier, and
    colour the evidence when they agree with the physics. A mislabeled 808
    still gates presence, still counts as a carrier, still forms the pocket.

    DISTINCTNESS vs ``_static_mix`` — static_mix applies a hygiene PENALTY for
    critical ``low_end_conflict`` events (pass/fail fault-checking); this axis
    scores the POSITIVE relationship (reserved sub, punch-vs-sustain, room).
    A mix with NO conflicts but NO defined pocket leaves static_mix healthy
    and scores low here — a strength axis, not a sign-flipped duplicate.

    DEFERRED, NOT FAKED — three real signals are NOT visible at doctrine time
    and are never claimed in the evidence:
      1. Kick/sub TEMPORAL interlock (sidechain-pocket alternation) — bass
         onset times are never computed (bass is excluded from
         ``RHYTHM_IDENTITIES``; onset timing lives in the groove analyzer for
         drum stems only).
      2. Low-end MOTIF detection (a recurring bass figure) — needs a
         pitch/onset sequence.
      3. Per-section true-sub (20-120Hz) movement — sections expose
         ``low_mid_energy`` (120-500Hz) ONLY, which is also why
         ``sections_analysis`` is accepted for the axis's declared surface
         but read by nothing in this v1.
    """
    c = doctrine["scorers"]["low_end_motion"]
    ev: List[str] = []
    events = masking_report.get("events", []) if masking_report else []

    def _low(r: Dict) -> float:
        return float((r.get("metrics", {}).get("band_energy") or {}).get("low", 0.0) or 0.0)

    def _crest(r: Dict) -> float:
        return float(r.get("metrics", {}).get("crest_factor_db", 0.0) or 0.0)

    mix_low = None
    if mix_metrics and mix_metrics.get("band_energy"):
        mix_low = float(mix_metrics["band_energy"].get("low", 0.0) or 0.0)

    # No signal at all: neither per-stem records nor a mix band read exists.
    if not records and mix_low is None:
        ev.append("No stem or mix low-band signal available — neutral low-end fallback.")
        return _clamp(c["neutral"]), ev

    # Presence GATE (gate ONLY — the level is never multiplied into the score).
    carriers = [r for r in records if _low(r) >= c["low_floor"]]
    if not carriers and (mix_low is None or mix_low < c["low_floor"]):
        ev.append(
            "No stem (or mix) carries sub weight above the low floor — "
            "no low-end foundation to pocket."
        )
        return _clamp(c["no_low_end"]), ev

    score = c["baseline"]

    crit = [e for e in events
            if e.get("classification") == "low_end_conflict" and e.get("severity") == "critical"]
    mod = [e for e in events
           if e.get("classification") == "low_end_conflict" and e.get("severity") == "moderate"]

    # Reserved sub / room: the sub band carried by FEW stems is room around
    # the bass — but ONLY when those carriers behave like a pocket. Few-ness
    # is never sufficient on its own: the reserve is QUALIFIED by a clean
    # (no critical collision) and defined (non-smeared envelope) low end,
    # so one giant muddy blob swallowing the floor cannot masquerade as a
    # reserved pocket. A pile-up is the opposite of room.
    stack = [r for r in records if _low(r) >= c["stack_floor"]]
    n_stack = len(stack)
    if 1 <= n_stack <= c["reserved_max"]:
        best_crest = max(_crest(r) for r in stack)
        defined = best_crest >= c["defined_crest_db"]
        clean = not crit
        if defined and clean:
            score += c["reserved_bonus"]
            names = ", ".join(r["name"] for r in stack)
            ev.append(
                f"Sub band reserved: {n_stack} stem(s) carry it ({names}), clean and "
                f"with envelope definition (best crest {best_crest:.1f} dB) — "
                f"the arrangement makes room for the low end."
            )
        else:
            score -= c["blob_penalty"]
            reasons = []
            if not clean:
                reasons.append("it collides (critical low-end conflict)")
            if not defined:
                reasons.append(f"its envelope is smeared (best crest {best_crest:.1f} dB)")
            ev.append(
                f"Few low carriers but not a pocket: {' and '.join(reasons)} — "
                f"a low-end blob occupying the floor, not reserved room."
            )
    elif n_stack > c["reserved_max"]:
        extra = n_stack - c["reserved_max"]
        score -= extra * c["stack_penalty"]
        ev.append(
            f"Low-end pile-up: {n_stack} stems stack the sub band "
            f"({extra} over the reserved ceiling) — no room around the bass."
        )
    else:
        ev.append(
            "Low end present in the mix but no stem distinctly carries it — "
            "a diffuse, undefined pocket earns no reserved-sub reward."
        )

    # Relationship (weak form): existing kick/bass collisions break the pocket.
    if crit or mod:
        score -= len(crit) * c["critical_conflict_penalty"] + len(mod) * c["moderate_conflict_penalty"]
        ev.append(
            f"Kick/bass collision: {len(crit)} critical and {len(mod)} moderate "
            f"low-end conflict(s) break the pocket."
        )
    elif n_stack >= 1:
        ev.append("No kick/bass collision — the pocket is clean.")

    # Complementarity: punch vs sustain among the carriers. Physics (crest)
    # picks the roles; identity labels only break exact ties and corroborate.
    if len(carriers) >= 2:
        punchy = max(
            carriers,
            key=lambda r: (_crest(r), 1 if r.get("identity_family") == "drums" else 0),
        )
        sustained = min(
            carriers,
            key=lambda r: (_crest(r), 0 if r.get("identity_family") == "bass" else 1),
        )
        gap = _crest(punchy) - _crest(sustained)
        if gap > 0:
            score += min(gap, c["complement_cap_db"]) * c["complement_coeff"]
            ev.append(
                f"Complementary pocket: '{punchy['name']}' punches (crest "
                f"{_crest(punchy):.1f} dB) against '{sustained['name']}' sustaining "
                f"(crest {_crest(sustained):.1f} dB)."
            )
            if punchy.get("identity_family") == "drums" and sustained.get("identity_family") == "bass":
                ev.append(
                    "Identity labels corroborate the physics (drum punch vs bass "
                    "sustain) — corroboration only, never the gate."
                )
        else:
            ev.append(
                "Low carriers show no punch-vs-sustain differentiation — "
                "an undifferentiated low end."
            )
    elif len(carriers) == 1:
        ev.append(
            f"A single reserved low carrier ('{carriers[0]['name']}') — "
            f"punch-vs-sustain complementarity is not applicable."
        )

    return _clamp(score), ev


def read_loop_context(records: List[Dict], sections: List[Dict],
                      events: List[Dict], c: Dict):
    """The SHARED observational loop-context read (P-032g).

    Returns ``(status, facts)`` where ``status`` is one of:

      * ``"no_loop"``             — no imported loop/sample stem present.
      * ``"not_dominant"``        — loop material present, but it sits in the
                                    bed (no dominance signal fires).
      * ``"dominant_unassessed"`` — a dominant loop, but fewer than two
                                    sections carry metrics, so evolution
                                    around it cannot be assessed.
      * ``"static"``              — a dominant loop with NO sectional
                                    evolution around it.
      * ``"iconic"``              — a dominant loop with groove-carrying
                                    FUNCTION (transient character + envelope
                                    definition + heard/unmasked) while the mix
                                    evolves around it.
      * ``"dominant_evolving"``   — dominant, the mix evolves, but the loop
                                    does not read as the groove carrier — an
                                    ambiguous context.

    and ``facts`` carries the measured detail the caller needs for evidence.

    This helper is the SINGLE detection basis used by BOTH the doctrine scorer
    ``_loop_context`` and (P-032g Commit-2) the creative engine's
    profile-decided ``protect_iconic_loops`` gate — the two consumers can
    never fork the physics. Every read is observational; every constant comes
    from the passed ``c`` (``doctrine["scorers"]["loop_context"]``,
    read-only).

    Detection, all from in-argument fields:
      * Loop presence — ``source_kind`` in ``LOOP_SAMPLE_KINDS``.
      * Dominance (any single signal suffices — three honest ways a loop can
        dominate): foregrounded (``depth_default`` in the forward layers),
        wide (``stereo_width`` above ``width_floor``, the stereo field), or
        transient lift (``metrics.transient_density`` at least
        ``transient_lift_floor`` above the whole-track median — the loop
        punches above the bed). Among dominant loops the most transient-
        forward one is read.
      * Evolution — whether the mix around the loop MOVES at the section
        grain: pstdev of section ``rms_dbfs`` / ``width`` / ``brightness``
        compared against the ``evolution_*`` floors (threshold comparisons
        ONLY — the spreads are never multiplied into any score, so this is
        not a re-derivation of ``_dynamic_mix``). ``contrast_vs_previous``
        warnings are counted as corroborating colour.
      * Groove/fingerprint function (the ICONIC read — an acoustic proxy):
        the dominant loop's ``transient_density`` clears
        ``groove_transient_floor`` (it carries rhythm), its
        ``crest_factor_db`` clears ``definition_crest_db`` (defined, not
        smeared hits), its ``perceptual_role`` is heard/structural, and no
        ``bad_masking`` event buries it.
    """
    facts: Dict = {}
    loops = [r for r in records if r.get("source_kind") in LOOP_SAMPLE_KINDS]
    if not loops:
        return "no_loop", facts

    def _td(r: Dict) -> float:
        return float(r.get("metrics", {}).get("transient_density", 0.0) or 0.0)

    def _crest(r: Dict) -> float:
        return float(r.get("metrics", {}).get("crest_factor_db", 0.0) or 0.0)

    densities = [_td(r) for r in records]
    median_td = statistics.median(densities) if densities else 0.0
    facts["loops"] = [r["name"] for r in loops]

    def _signals(r: Dict) -> List[str]:
        s: List[str] = []
        if r.get("depth_default") in FORWARD:
            s.append("foregrounded")
        if float(r.get("stereo_width", 0) or 0) > c["width_floor"]:
            s.append("wide")
        if _td(r) - median_td >= c["transient_lift_floor"]:
            s.append("transient lift above the bed")
        return s

    dominant_loops = [(r, _signals(r)) for r in loops]
    dominant_loops = [(r, s) for r, s in dominant_loops if s]
    if not dominant_loops:
        return "not_dominant", facts

    dom, signals = max(dominant_loops, key=lambda pair: _td(pair[0]))
    facts["dominant"] = dom["name"]
    facts["signals"] = signals

    def _vals(key: str) -> List[float]:
        return [
            float(v)
            for v in (s.get("metrics", {}).get(key) for s in sections)
            if v is not None
        ]

    rms, width, bright = _vals("rms_dbfs"), _vals("width"), _vals("brightness")
    if len(rms) < 2 and len(width) < 2 and len(bright) < 2:
        return "dominant_unassessed", facts

    rms_std = statistics.pstdev(rms) if len(rms) > 1 else 0.0
    width_std = statistics.pstdev(width) if len(width) > 1 else 0.0
    bright_std = statistics.pstdev(bright) if len(bright) > 1 else 0.0
    lift_fails = sum(1 for s in sections if "warning" in s.get("contrast_vs_previous", {}))
    facts.update(rms_std=rms_std, width_std=width_std, bright_std=bright_std,
                 lift_fails=lift_fails)

    evolving = (
        rms_std >= c["evolution_rms_floor_db"]
        or width_std >= c["evolution_width_floor"]
        or bright_std >= c["evolution_brightness_floor"]
    )
    if not evolving:
        return "static", facts

    # The ICONIC read — groove-carrying FUNCTION, an acoustic proxy only.
    groove_char = _td(dom) >= c["groove_transient_floor"]
    defined = _crest(dom) >= c["definition_crest_db"]
    heard = dom.get("perceptual_role") in {"heard", "structural"}
    masked = any(
        dom["name"] in e.get("elements", []) and e.get("classification") == "bad_masking"
        for e in events
    )
    facts.update(transient_density=_td(dom), crest_db=_crest(dom),
                 groove_char=groove_char, defined=defined, heard=heard,
                 masked=masked, role=dom.get("perceptual_role"))
    if groove_char and defined and heard and not masked:
        return "iconic", facts
    return "dominant_evolving", facts


def _loop_context(records: List[Dict], sections_analysis: List[Dict],
                  masking_report: Dict, doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for LOOP CONTEXT — static vs iconic. THE HINGE.

    This is the SIXTH new agnostic axis (P-032g) and the exemplar of the
    pinned architecture doctrine: **the engine DETECTS agnostically; the
    profile DECIDES.** A dominating loop is not, by itself, a fault or a
    virtue — one profile may deconstruct it, another may treat it as the very
    identity of the record and protect it. That reversal lives in profile
    JSON (weights here; the ``protect_iconic_loops`` creative gate in
    Commit-2), never in this function. The language is therefore strictly
    OBSERVATIONAL (USER-MANDATED): the evidence reports what IS — dominant,
    static, iconic-functioning, ambiguous — and never rules on it.

    The reading (all detection shared with the creative gate via
    ``read_loop_context`` — one basis, never forked):

      * **No loop** — no stem with a loop/sample ``source_kind`` → the
        documented ``no_loop`` NEUTRAL float. Sectional evolution alone can
        never move this axis (with no loop the movement axes own that signal
        — see DISTINCTNESS below).
      * **Loop present, not dominant** — no dominance signal (not
        foregrounded, not wide, no transient lift above the bed's median
        transient density) → the ``not_dominant`` neutral: a loop sitting in
        the bed is neither static-dominating nor iconic-functioning.
      * **Dominant + evolution unassessable** (fewer than two sections with
        metrics) → the ``dominant_unassessed`` fallback, a documented
        ambiguous reading, never a guess.
      * **Dominant + no sectional evolution = STATIC** → the LOW ``static``
        float. The mix does not move around the loop at the section grain
        (RMS/width/brightness spreads all under the evolution floors).
      * **Dominant + evolution + groove/fingerprint FUNCTION = ICONIC** → the
        HIGH ``iconic`` float: the loop carries the rhythm (transient density
        over ``groove_transient_floor``), with defined hits
        (``crest_factor_db`` over ``definition_crest_db``), heard and
        unmasked, while the mix evolves around it.
      * **Dominant + evolution, but no groove-function read** → the
        ``dominant_evolving`` mid float — an ambiguous context.

    The score is a CONTEXT reading, not a verdict: high = iconic-functioning
    dominant loop, mid = no loop / ambiguous, low = static-dominating loop.
    Always a clamped float, never None. Constants are read-only from
    ``doctrine["scorers"]["loop_context"]``.

    WHAT "ICONIC" HONESTLY MEANS HERE — an ACOUSTIC PROXY, nothing more: the
    measurable groove-carrying FUNCTION of the dominant loop on the exported
    stems. It does NOT and cannot mean CULTURAL recognizability ("everyone
    knows this break") — that is provenance/manifest territory (sample
    identification, clearance metadata), not audio measurement, and it is
    DEFERRED, not faked. The evidence names the proxy explicitly.

    DISTINCTNESS — evolution is a context INPUT here, never the score:
    ``_dynamic_mix`` scores the section spreads themselves,
    ``_rhythmic_surprise`` scores transient-density variation,
    ``_section_contrast`` scores lift failures. This axis only COMPARES the
    spreads against floors to interpret the LOOP; with no loop present the
    sectional movement has zero effect on this axis.

    DEFERRED, NOT FAKED (docstring, never claimed in evidence):
      1. Cultural/recognizability iconic-ness — provenance/manifest, not
         audio (above).
      2. Per-loop bar-level variation (does the LOOP itself vary bar to bar,
         or repeat verbatim) — needs an onset/bar sequence, post-doctrine
         groove territory.
      3. Anything else needing the onset sequence (chop-pattern detection,
         loop-vs-arrangement phase) — same territory.
    """
    c = doctrine["scorers"]["loop_context"]
    events = masking_report.get("events", []) if masking_report else []
    status, facts = read_loop_context(records, sections_analysis, events, c)
    ev: List[str] = []

    if status == "no_loop":
        ev.append("No imported loop/sample material present — loop context is neutral.")
        return _clamp(c[status]), ev

    if status == "not_dominant":
        names = ", ".join(facts["loops"])
        ev.append(
            f"Imported loop material present ({names}) without dominance "
            f"signals — it sits in the bed (not foregrounded, not wide, no "
            f"transient lift above the bed)."
        )
        return _clamp(c[status]), ev

    dom = facts["dominant"]
    signals = " + ".join(facts["signals"])

    if status == "dominant_unassessed":
        ev.append(
            f"Dominant loop '{dom}' ({signals}); fewer than two sections with "
            f"metrics, so evolution around it cannot be assessed — an "
            f"ambiguous loop context."
        )
        return _clamp(c[status]), ev

    spreads = (
        f"RMS spread {facts['rms_std']:.2f} dB, width spread "
        f"{facts['width_std']:.3f}, brightness spread {facts['bright_std']:.3f}"
    )

    if status == "static":
        lift_txt = (
            f"; {facts['lift_fails']} section(s) do not lift vs the previous"
            if facts["lift_fails"] else ""
        )
        ev.append(
            f"Dominant loop '{dom}' ({signals}) with no sectional evolution "
            f"around it ({spreads}{lift_txt}) — the loop reads STATIC: "
            f"dominant while the mix around it does not move."
        )
        return _clamp(c[status]), ev

    if status == "iconic":
        ev.append(
            f"Dominant loop '{dom}' ({signals}) reads ICONIC-functioning — an "
            f"acoustic proxy for groove-carrying function: transient density "
            f"{facts['transient_density']:.2f} with defined hits (crest "
            f"{facts['crest_db']:.1f} dB), heard and unmasked, while the mix "
            f"evolves around it ({spreads})."
        )
        return _clamp(c[status]), ev

    # dominant_evolving — the ambiguous mid reading; report WHY it does not
    # read as the groove carrier, observationally.
    reasons: List[str] = []
    if not facts["groove_char"]:
        reasons.append(
            f"transient density {facts['transient_density']:.2f} under the groove floor"
        )
    if not facts["defined"]:
        reasons.append(f"crest {facts['crest_db']:.1f} dB under the definition floor")
    if not facts["heard"]:
        reasons.append(f"perceptual role '{facts['role']}', not heard")
    if facts["masked"]:
        reasons.append("masked by a forward element")
    detail = "; ".join(reasons) if reasons else "no groove-function read"
    ev.append(
        f"Dominant loop '{dom}' ({signals}); the mix evolves around it "
        f"({spreads}), and the loop does not read as the groove carrier "
        f"({detail}) — an ambiguous loop context."
    )
    return _clamp(c[status]), ev


def _vocal_role_fit(records: List[Dict], events: List[Dict],
                    doctrine: Dict = _DOCTRINE):
    """Producer-AGNOSTIC scorer for vocal-role FIT — the LAST of the seven
    P-032.x axes (P-032f) and the vocal half of the doctrine pin: **the
    engine DETECTS vocal function; the profile decides masking philosophy.**

    DETECTION IS UPSTREAM AND SHARED: the ``vocal_type`` /
    ``vocal_type_confidence`` record fields are classified ONCE in the
    pipeline by ``analyzers.vocal_type_classifier`` (lead / hook_candidate /
    percussive / stack / uncertain — see its module doc for the honesty caps
    and deferrals: hook recurrence, lyric meaning, per-onset stutter rate are
    NOT measurable at doctrine time and are never claimed). This scorer never
    re-classifies — it reads the record fields, so every consumer shares one
    detection basis.

    THE READING (strictly observational — the evidence reports what IS and
    never rules on it):

      * **No vocal stems** → the documented ``no_vocals`` NEUTRAL float.
        Always a clamped float, never None.
      * **Census** — every classified vocal stem's type + confidence is
        reported as evidence colour.
      * **The lead** (``vocal_lead``): forward and clear of vocal-band
        masking conflicts → ``lead_forward_bonus`` (high fit — the lead owns
        the presence band). Challenged by forward elements (vocal-band
        masking events that include the lead) → ``masked_penalty`` per event
        (low fit). Not forward → reported, no bonus.
      * **Non-lead vocal stems** (hook_candidate / percussive / stack /
        uncertain): their OWN vocal-band masking involvements — events that
        do NOT include a lead stem — read as reduced role fit
        (``masked_penalty`` per event): the default philosophy protects
        every vocal's clarity at lead grade, uncertain included
        (misclassification fails CLOSED toward vocal protection).

    THE MASKED-LEAD PATHWAY IS STRUCTURALLY SEPARATE: an event that includes
    a lead stem belongs to the LEAD reading above — it is counted there,
    once, and is never re-read (or re-interpreted) through any non-lead
    stem in the same event. Profile-authored blend policy (P-032f Commit-2)
    can therefore never reach the masked-lead pathway by construction.

    DISTINCTNESS vs the live vocal scorers — this axis READS, it never
    rewires: ``_ramone`` / ``_vocal_centrality`` keep sole ownership of the
    reference producer's lead-masking PENALTIES (and their behavior for
    halee_ramone is untouched; this axis is weight-0 there). This axis adds
    the role-TYPE dimension those scorers do not have: they see "a lead" and
    "events"; this axis sees WHAT KIND of vocal every stem is and reads fit
    per role. ``_static_mix``'s no-lead hygiene penalty is likewise
    untouched.

    Constants are read-only from ``doctrine["scorers"]["vocal_role_fit"]``.
    """
    c = doctrine["scorers"]["vocal_role_fit"]
    ev: List[str] = []

    vocal_stems = [r for r in records if r.get("vocal_type")]
    if not vocal_stems:
        ev.append("No vocal stems present — vocal-role fit is neutral.")
        return _clamp(c["no_vocals"]), ev

    def _conf(r: Dict) -> float:
        return float(r.get("vocal_type_confidence") or 0.0)

    census = ", ".join(
        f"'{r['name']}' reads {r['vocal_type']} (confidence {_conf(r):.2f})"
        for r in vocal_stems
    )
    ev.append(f"Vocal roles read: {census}.")

    lead_names = {r["name"] for r in vocal_stems if r["vocal_type"] == "vocal_lead"}

    def _vocal_masking(name: str) -> List[Dict]:
        return [
            e for e in events
            if name in e.get("elements", []) and e.get("classification") == "bad_masking"
        ]

    score = c["baseline"]
    for r in vocal_stems:
        name = r["name"]
        involved = _vocal_masking(name)
        if r["vocal_type"] == "vocal_lead":
            if involved:
                score -= c["masked_penalty"] * len(involved)
                ev.append(
                    f"Lead vocal '{name}' is challenged by {len(involved)} "
                    f"forward element(s) in the presence band — reduced role fit."
                )
            elif r.get("depth_default") in FORWARD:
                score += c["lead_forward_bonus"]
                ev.append(
                    f"Lead vocal '{name}' sits forward and clear of masking "
                    f"conflicts — the lead owns the presence band."
                )
            else:
                ev.append(
                    f"Lead vocal '{name}' sits {r.get('depth_default')}, "
                    f"clear of masking conflicts."
                )
        else:
            # The masked-LEAD pathway (events including a lead stem) belongs
            # to the lead reading above — never re-read through this stem.
            own = [
                e for e in involved
                if not (set(e.get("elements", [])) & lead_names)
            ]
            if own:
                score -= c["masked_penalty"] * len(own)
                ev.append(
                    f"'{name}' ({r['vocal_type']}, confidence {_conf(r):.2f}) "
                    f"overlaps {len(own)} forward element(s) in the vocal band "
                    f"— read under full clarity protection: reduced role fit."
                )

    return _clamp(score), ev
