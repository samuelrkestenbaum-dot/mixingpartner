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

    component_scores = {
        "halee_score": halee,
        "ramone_score": ramone,
        "vocal_centrality_score": vocal,
        "depth_hierarchy_score": depth,
        "section_contrast_score": contrast,
        "static_mix_score": static,
        "dynamic_mix_score": dynamic,
        "beat_identity_score": beat,
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
