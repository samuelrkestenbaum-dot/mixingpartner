"""Doctrine engine: turns the analysis into Halee/Ramone scores + warnings.

Every score is 0-100 and carries evidence. The engine never invents numbers it
cannot justify; when there is not enough information (e.g. fewer than two
sections) it says so rather than guessing.
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS
from .producer_profile import load_profile

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


def _clamp(x: float) -> float:
    return round(max(0.0, min(100.0, x)), 1)


def score_doctrine(
    records: List[Dict],
    sections_analysis: List[Dict],
    masking_report: Dict,
    mix_metrics: Optional[Dict],
    intent: Optional[Dict] = None,
) -> Dict:
    events = masking_report.get("events", [])
    lead = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)
    warnings: List[Dict] = []

    halee, halee_ev = _halee(records, events)
    ramone, ramone_ev = _ramone(records, lead, events, warnings)
    vocal, vocal_ev = _vocal_centrality(lead, events)
    depth, depth_ev = _depth_hierarchy(records)
    contrast, contrast_ev = _section_contrast(sections_analysis, warnings)
    static, static_ev = _static_mix(records, lead, events, mix_metrics)
    dynamic, dynamic_ev = _dynamic_mix(sections_analysis)

    component_scores = {
        "halee_score": halee,
        "ramone_score": ramone,
        "vocal_centrality_score": vocal,
        "depth_hierarchy_score": depth,
        "section_contrast_score": contrast,
        "static_mix_score": static,
        "dynamic_mix_score": dynamic,
    }
    weights = _WEIGHTS
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
        },
        "warnings": warnings,
    }


# --------------------------------------------------------------------------- #
def _halee(records: List[Dict], events: List[Dict]):
    c = _PENALTY_COEFFS["halee"]
    score = _BASELINES["halee"]
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


def _ramone(records: List[Dict], lead: Optional[Dict], events: List[Dict], warnings: List[Dict]):
    c = _PENALTY_COEFFS["ramone"]
    score = _BASELINES["ramone"]
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


def _vocal_centrality(lead: Optional[Dict], events: List[Dict]):
    if lead is None:
        return 35.0, ["No lead vocal present."]
    score = 70.0
    ev = [f"Lead vocal '{lead['name']}' identified."]
    if lead["sacredness"] == "sacred":
        score += 10
        ev.append("Vocal correctly marked sacred.")
    if lead["depth_default"] in FORWARD:
        score += 10
        ev.append(f"Vocal sits in the {lead['depth_default']} layer.")
    bad = [e for e in events if lead["name"] in e["elements"] and e["classification"] == "bad_masking"]
    if bad:
        score -= 6 * len(bad)
        ev.append(f"Vocal challenged by {len(bad)} masking conflict(s).")
    return _clamp(score), ev


def _depth_hierarchy(records: List[Dict]):
    depths = [r["depth_default"] for r in records]
    distinct = len(set(depths))
    n = len(records) or 1
    score = 40 + distinct * 12
    fg_frac = sum(1 for d in depths if d in FORWARD) / n
    if fg_frac > 0.6:
        score -= (fg_frac - 0.6) * 60
    ev = [f"{distinct} of 4 depth layers used; {fg_frac:.0%} forward."]
    if distinct <= 1:
        ev.append("Everything occupies one layer — no hierarchy.")
    return _clamp(score), ev


def _section_contrast(sections: List[Dict], warnings: List[Dict]):
    if len(sections) < 2:
        return None, ["Fewer than two sections analysed; contrast cannot be scored."]
    lift_fail = 0
    for s in sections:
        c = s.get("contrast_vs_previous", {})
        if "warning" in c:
            lift_fail += 1
            warnings.append({"warning": c["warning"], "doctrine": ["section_contrast"]})
    score = 100 - 18 * lift_fail
    ev = [f"{lift_fail} section(s) fail to lift relative to the previous section."]
    return _clamp(score), ev


def _static_mix(records: List[Dict], lead: Optional[Dict], events: List[Dict], mix_metrics: Optional[Dict]):
    score = 80.0
    ev: List[str] = []
    if mix_metrics:
        if mix_metrics.get("peak_dbfs", -1) > -0.1:
            score -= 10
            ev.append("Mixdown is at/over full scale — clipping risk.")
        bands = mix_metrics.get("band_energy", {})
        if bands:
            dominant = max(bands, key=bands.get)
            if bands[dominant] > 0.55:
                score -= 10
                ev.append(f"Tonal balance skewed: '{dominant}' band holds {bands[dominant]:.0%} of energy.")
            else:
                ev.append("Broad tonal balance is reasonable.")
    crit_low = [e for e in events if e["classification"] == "low_end_conflict" and e["severity"] == "critical"]
    if crit_low:
        score -= 8 * len(crit_low)
        ev.append(f"{len(crit_low)} critical low-end (kick/bass) conflict(s).")
    if lead is None:
        score -= 8
        ev.append("No lead vocal to anchor intelligibility.")
    return _clamp(score), ev


def _dynamic_mix(sections: List[Dict]):
    if len(sections) < 2:
        return 40.0, ["Fewer than two sections; dynamic movement cannot be assessed."]
    rms = [s["metrics"]["rms_dbfs"] for s in sections]
    width = [s["metrics"]["width"] for s in sections]
    bright = [s["metrics"]["brightness"] for s in sections]
    rms_std = statistics.pstdev(rms) if len(rms) > 1 else 0.0
    width_std = statistics.pstdev(width) if len(width) > 1 else 0.0
    bright_std = statistics.pstdev(bright) if len(bright) > 1 else 0.0
    score = 30 + rms_std * 8 + width_std * 140 + bright_std * 140
    lift_fail = sum(1 for s in sections if "warning" in s.get("contrast_vs_previous", {}))
    score -= 10 * lift_fail
    ev = [
        f"Section RMS spread {rms_std:.1f} dB, width spread {width_std:.2f}, "
        f"brightness spread {bright_std:.2f}."
    ]
    if score < 55:
        ev.append("Sections are too similar — the mix is balanced but emotionally static.")
    return _clamp(score), ev
