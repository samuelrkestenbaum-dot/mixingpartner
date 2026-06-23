"""Mix planner — assembles the final ``mix_plan`` from every analysis stage.

Produces per-track actions, per-section actions, an automation narrative, mute
candidates, source-material warnings, and production-vs-mix boundary calls.
Bias (build packet section 14): automation over compression, depth over EQ,
subtraction over addition, vocal belief over polish, contrast over static balance.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS

# Standard automation gestures (build packet section 22).
AUTOMATION_GESTURES = {
    "verse_intimacy": [
        "Pull reverb sends down",
        "Narrow stereo image",
        "Ride vocal +0.5 to +1.5 dB",
        "Reduce background texture level",
        "Keep the emotional centre close",
    ],
    "pre_chorus_build": [
        "Gradually increase reverb sends",
        "Open filters on background elements",
        "Slightly increase drum room / overhead presence",
        "Push transition elements forward",
    ],
    "chorus_bloom": [
        "Increase selected reverb sends +3 to +6 dB at chorus entry",
        "Slightly widen supporting elements",
        "Move some midground elements forward",
        "Let the vocal sit in more room without losing intelligibility",
    ],
    "bridge_pressure": [
        "Narrow selected elements",
        "Reduce reverb temporarily",
        "Increase perceived density / constriction",
        "Create emotional pressure before the final release",
    ],
    "final_chorus_release": [
        "Widest point of the song",
        "Most open depth field",
        "Longest emotional reverb tails",
        "Largest vocal support stack",
        "Avoid over-limiting the release",
    ],
}

LIFT_GOALS = {"release", "lift", "catharsis", "climax", "bloom", "open"}
PRESSURE_GOALS = {"pressure", "collapse", "anger", "constriction"}
LOW_GOALS = {"intimacy", "vulnerability", "restraint", "grief", "warmth"}


def build_plan(
    song_title: str,
    intent: Dict,
    records: List[Dict],
    sections_analysis: List[Dict],
    masking_report: Dict,
    doctrine_score: Dict,
    logic_actions: List[Dict],
    mix_metrics: Optional[Dict],
    reference_delta: Optional[Dict] = None,
) -> Dict:
    events = masking_report.get("events", [])
    mute_candidates = _mute_candidates(records, events)
    source_warnings = _source_warnings(records)
    boundaries = _boundaries(events, sections_analysis, records)
    automation_plan = _automation_plan(sections_analysis, records)
    per_section = _per_section_actions(sections_analysis)
    risks, opportunities = _risks_and_opportunities(doctrine_score, records, events, sections_analysis)

    return {
        "song_title": song_title,
        "singular_emotional_truth": intent.get("singular_emotional_truth", ""),
        "negative_constraints": intent.get("negative_constraints", []),
        "overall_diagnosis": _overall_diagnosis(doctrine_score, mute_candidates, sections_analysis),
        "halee_score": doctrine_score.get("halee_score"),
        "ramone_score": doctrine_score.get("ramone_score"),
        "section_contrast_score": doctrine_score.get("section_contrast_score"),
        "depth_hierarchy_score": doctrine_score.get("depth_hierarchy_score"),
        "vocal_centrality_score": doctrine_score.get("vocal_centrality_score"),
        "static_mix_score": doctrine_score.get("static_mix_score"),
        "dynamic_mix_score": doctrine_score.get("dynamic_mix_score"),
        "overall_mix_readiness_score": doctrine_score.get("overall_mix_readiness_score"),
        "biggest_risks": risks,
        "best_opportunities": opportunities,
        "per_track_actions": logic_actions,
        "per_section_actions": per_section,
        "automation_plan": automation_plan,
        "mute_candidates": mute_candidates,
        "reference_deltas": reference_delta or {},
        "source_material_warnings": source_warnings,
        "production_vs_mix_boundaries": boundaries,
        "warnings": [w["warning"] for w in doctrine_score.get("warnings", [])],
        "next_pass": [],  # filled by next_pass_planner
    }


# --------------------------------------------------------------------------- #
def _mute_candidates(records: List[Dict], events: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    for r in records:
        if r["perceptual_role"] == "candidate_for_mute" or r["sacredness"] == "expendable":
            out.append({
                "element": r["name"],
                "track_id": r["track_id"],
                "sacredness": r["sacredness"],
                "reason": "Expendable / low-value element; mute or chop if it crowds the vocal or chorus.",
                "risk_class": 4 if r["source_kind"] in LOOP_SAMPLE_KINDS else 3,
            })
    # Width crowding suggests muting/pushing one of the wide forward elements.
    for e in events:
        if e["classification"] == "width_crowding":
            out.append({
                "element": e["elements"][-1],
                "section": e["section"],
                "reason": f"Width crowding in '{e['section']}': reserve the widest placement for one element; "
                          f"push or mute the rest.",
                "risk_class": 3,
            })
    return out


def _source_warnings(records: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    for r in records:
        for w in r.get("source_warnings", []):
            out.append({"track": r["name"], "warning": w})
    return out


def _boundaries(events: List[Dict], sections: List[Dict], records: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    for e in events:
        if e["classification"] == "width_crowding":
            out.append({
                "issue": f"'{e['section']}' feels crowded",
                "boundary_classification": "arrangement_problem",
                "reason": e["reason"],
                "mix_fix_possible": True,
                "best_fix": "Mute or push decorative/wide elements to the background rather than EQ-ing all of them.",
            })
    for s in sections:
        c = s.get("contrast_vs_previous", {})
        if "warning" in c and s["metrics"].get("density", 0) > 0.6:
            out.append({
                "issue": f"{s['name']} does not lift but is already dense",
                "boundary_classification": "arrangement_problem",
                "reason": "Density increases without an increase in space/width; adding more will not create lift.",
                "mix_fix_possible": True,
                "best_fix": "Create contrast by subtraction before the section, then bloom space at entry.",
            })
    return out


def _section_gesture(s: Dict, is_final_lift: bool) -> str:
    goal = (s.get("emotional_goal") or "").lower()
    name = s["name"].lower()
    if "pre" in name and "chorus" in name:
        return "pre_chorus_build"
    if goal in LIFT_GOALS or "chorus" in name or "drop" in name:
        return "final_chorus_release" if is_final_lift else "chorus_bloom"
    if goal in PRESSURE_GOALS or "bridge" in name:
        return "bridge_pressure"
    if goal in LOW_GOALS or "verse" in name or "intro" in name:
        return "verse_intimacy"
    return "verse_intimacy"


def _automation_plan(sections: List[Dict], records: List[Dict]) -> List[Dict]:
    lift_idxs = [
        i for i, s in enumerate(sections)
        if (s.get("emotional_goal") or "").lower() in LIFT_GOALS or "chorus" in s["name"].lower()
    ]
    final_lift = lift_idxs[-1] if lift_idxs else -1

    plan: List[Dict] = []
    for i, s in enumerate(sections):
        gesture = _section_gesture(s, is_final_lift=(i == final_lift))
        entry = {
            "section": s["section_id"],
            "name": s["name"],
            "emotional_goal": s.get("emotional_goal"),
            "gesture": gesture,
            "moves": AUTOMATION_GESTURES[gesture],
        }
        c = s.get("contrast_vs_previous", {})
        if "warning" in c:
            entry["contrast_warning"] = c["warning"]
        plan.append(entry)

    # Per-track automation gathered from felt/vocal elements.
    track_moves = []
    for r in records:
        if r["instrument_identity"] == "lead_vocal":
            track_moves.append({
                "track": r["name"],
                "parameter": "gain",
                "move": "Phrase-level rides +0.5 to +1.5 dB before compression.",
            })
        elif r["perceptual_role"] == "felt":
            track_moves.append({
                "track": r["name"],
                "parameter": "filter cutoff / reverb send",
                "move": "Open and lift only in choruses; pull back in verses.",
            })
    if track_moves:
        plan.append({"section": "*", "name": "Per-track rides", "gesture": "track_rides", "moves": track_moves})
    return plan


def _per_section_actions(sections: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    for s in sections:
        c = s.get("contrast_vs_previous", {})
        out.append({
            "section": s["section_id"],
            "name": s["name"],
            "emotional_goal": s.get("emotional_goal"),
            "rms_dbfs": s["metrics"]["rms_dbfs"],
            "width": s["metrics"]["width"],
            "contrast_warning": c.get("warning"),
        })
    return out


def _risks_and_opportunities(doctrine_score, records, events, sections):
    risks: List[str] = []
    opportunities: List[str] = []

    for w in doctrine_score.get("warnings", []):
        risks.append(w["warning"])

    scores = {
        "Halee physical-space realism": doctrine_score.get("halee_score"),
        "Ramone vocal centrality": doctrine_score.get("ramone_score"),
        "Section contrast": doctrine_score.get("section_contrast_score"),
        "Depth hierarchy": doctrine_score.get("depth_hierarchy_score"),
        "Dynamic movement": doctrine_score.get("dynamic_mix_score"),
    }
    for label, val in scores.items():
        if val is not None and val < 60:
            risks.append(f"{label} is weak ({val}/100).")

    crit = [e for e in events if e.get("severity") == "critical"]
    if crit:
        opportunities.append(f"Resolve {len(crit)} critical masking conflict(s) by depth placement and subtraction.")
    if any("warning" in s.get("contrast_vs_previous", {}) for s in sections):
        opportunities.append("Create real section contrast with automation (bloom/intimacy) instead of master level.")
    felt_fg = [r for r in records if r["perceptual_role"] == "felt" and r["depth_default"] in {"intimate", "foreground"}]
    if felt_fg:
        opportunities.append("Push felt elements back so the heard elements (vocal, hooks) own the foreground.")
    if not opportunities:
        opportunities.append("Foundation is solid; focus the next pass on emotional movement and vocal rides.")
    return risks[:8], opportunities[:6]


def _overall_diagnosis(doctrine_score, mute_candidates, sections) -> str:
    static = doctrine_score.get("static_mix_score")
    dynamic = doctrine_score.get("dynamic_mix_score")
    overall = doctrine_score.get("overall_mix_readiness_score")
    bits = []
    if overall is not None:
        bits.append(f"Overall mix readiness {overall}/100.")
    if static is not None and dynamic is not None:
        bits.append(f"Static balance {static}/100; dynamic movement {dynamic}/100.")
        if dynamic + 12 < static:
            bits.append("The mix is more balanced than it is alive — invest in section contrast and rides, not more EQ.")
    if mute_candidates:
        bits.append(f"{len(mute_candidates)} mute/chop candidate(s) flagged; subtraction may help more than addition.")
    return " ".join(bits) if bits else "Analysis complete."
