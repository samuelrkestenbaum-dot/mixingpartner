"""Logic action checklist renderer — human-executable Markdown.

Specific enough that a human (or Claude Cowork) can open Logic Pro and know
exactly what to do, without any of it being destructive.
"""

from __future__ import annotations

from typing import Dict, List

from ..constants import RISK_CLASSES

PREFERRED_ORDER = [
    "automation",
    "level and panning",
    "depth placement",
    "subtractive EQ",
    "compression",
    "additive EQ",
    "saturation / excitement",
    "last-resort enhancement",
]


def render_logic_checklist(mix_plan: Dict) -> str:
    out = ["# Logic Action Checklist", ""]
    out.append("> **Non-destructive only.** Duplicate tracks / save presets before changes. "
               "No source audio is overwritten. Approve creative or source-level moves before applying.")
    out.append("")
    out.append("**Preferred order of operations:** " + " → ".join(PREFERRED_ORDER) + ".")
    out.append("")

    for track in mix_plan.get("per_track_actions", []):
        out.append(f"## {track['track']}")
        out.append("")
        out.append(f"*{track.get('diagnosis', '')}*")
        out.append("")
        out.append(f"- **Depth:** {track.get('depth_layer')} · **Role:** {track.get('perceptual_role')}")
        out.append(f"- **Reverb / send:** {track.get('send_reverb')}")
        out.append("")

        actions = track.get("actions", [])
        if actions:
            for i, a in enumerate(actions, start=1):
                out.append(f"{i}. **{a['plugin']}** — {a['setting']}")
                out.append(f"   - _Why:_ {a['reason']}")
                out.append(f"   - _Risk:_ Class {a['risk_class']} ({RISK_CLASSES.get(a['risk_class'], '')})")
        automation = track.get("automation", [])
        if automation:
            out.append(f"{len(actions) + 1}. **Automation**")
            for au in automation:
                out.append(f"   - {au['parameter']}: {au['move']}")
                out.append(f"     _Why:_ {au['reason']}")
        for w in track.get("warnings", []):
            out.append(f"- ⚠️ {w}")
        out.append("")

    mutes = mix_plan.get("mute_candidates", [])
    if mutes:
        out.append("## Mute / Chop Candidates")
        out.append("")
        out.append("_Subtraction often helps more than addition. Non-destructive (duplicate first)._")
        out.append("")
        for m in mutes:
            loc = f" (section `{m['section']}`)" if m.get("section") else ""
            out.append(f"- **{m['element']}**{loc} — {m['reason']} _Risk: Class {m.get('risk_class', 3)}._")
        out.append("")

    warnings = mix_plan.get("source_material_warnings", [])
    if warnings:
        out.append("## Source-Material Warnings")
        out.append("")
        for w in warnings:
            out.append(f"- **{w['track']}**: {w['warning']}")
        out.append("")

    return "\n".join(out)
