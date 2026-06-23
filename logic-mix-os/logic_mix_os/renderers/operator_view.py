"""Operator status surface — the CLI 'mix control room' (build packet section 50).

A single text surface showing project state, scores, the section map, depth
crowding, masking, and the next recommended action. This is the CLI-first
realisation of the section-50 screen map; the graphical dashboard is deferred to
a later milestone per the staged roadmap (section 52).
"""

from __future__ import annotations

from typing import Dict

from ..pipeline import ProjectAnalysis


def _score_line(label: str, v) -> str:
    if v is None:
        return f"  {label:<26} n/a"
    width = 16
    filled = int(round((v / 100.0) * width))
    bar = "█" * filled + "░" * (width - filled)
    return f"  {label:<26} {v:>5.1f}  {bar}"


def render_status(result: ProjectAnalysis) -> str:
    proj = result.project
    ds = result.doctrine_score
    out = []
    out.append("=" * 66)
    out.append(f" LOGIC MIX OS — {proj.song_title}")
    out.append("=" * 66)
    out.append(f" Tempo: {proj.tempo or '—'}   Key: {proj.key or '—'}   "
               f"Tracks: {len(result.track_analysis)}   Sections: {len(result.section_analysis)}")
    truth = proj.intent.get("singular_emotional_truth")
    if truth:
        out.append(f" Emotional truth: {truth}")
    out.append("")

    out.append(" SCORES")
    for label, key in [
        ("Overall mix readiness", "overall_mix_readiness_score"),
        ("Roy Halee (space)", "halee_score"),
        ("Phil Ramone (vocal)", "ramone_score"),
        ("Depth hierarchy", "depth_hierarchy_score"),
        ("Section contrast", "section_contrast_score"),
        ("Dynamic movement", "dynamic_mix_score"),
    ]:
        out.append(_score_line(label, ds.get(key)))
    out.append("")

    # Section map with per-section forward-element crowding.
    if result.section_analysis:
        out.append(" SECTION MAP")
        out.append(f"   {'Section':<14}{'Goal':<13}{'RMS':>7}{'Width':>7}{'Fwd':>5}  Note")
        for s in result.section_analysis:
            sid = s["section_id"]
            fwd = sum(
                1 for r in result.records
                if r["depth_by_section"].get(sid, r["depth_default"]) in {"intimate", "foreground"}
            )
            note = "⚠ no lift" if "warning" in s.get("contrast_vs_previous", {}) else ""
            crowd = "  CROWDED" if fwd >= 6 else ""
            out.append(
                f"   {s['name'][:13]:<14}{str(s.get('emotional_goal'))[:12]:<13}"
                f"{s['metrics']['rms_dbfs']:>7.1f}{s['metrics']['width']:>7.2f}{fwd:>5}  {note}{crowd}"
            )
        out.append("")

    # Masking summary.
    summary = result.masking_report.get("summary", {})
    if summary:
        out.append(" MASKING")
        out.append(f"   critical: {summary.get('critical_count', 0)}   "
                   f"moderate: {summary.get('moderate_count', 0)}   "
                   f"blends: {summary.get('blend_count', 0)}   "
                   f"total: {summary.get('total_events', 0)}")
        out.append("")

    # Next recommended action.
    nxt = result.mix_plan.get("next_pass", [])
    out.append(" NEXT RECOMMENDED ACTION")
    if nxt:
        out.append(f"   → {nxt[0]['title']}: {nxt[0]['detail']}")
    else:
        out.append("   → Foundation solid; validate the bounce and move to mastering-readiness checks.")
    out.append("=" * 66)
    return "\n".join(out)
