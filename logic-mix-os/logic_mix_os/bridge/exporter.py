"""Logic action exporter (build packet section 41, mode A/B).

Normalises the mix plan's per-track actions into a flat, machine-executable
action list that the AppleScript / Shortcuts generators and the dry-run executor
consume. Pure data transform — no side effects.
"""

from __future__ import annotations

from typing import Dict, List


def export_actions(mix_plan: Dict) -> List[Dict]:
    actions: List[Dict] = []
    for track in mix_plan.get("per_track_actions", []):
        tid = track.get("track_id", track["track"])
        track_name = track["track"]

        # Depth-appropriate send first (depth before EQ doctrine).
        if track.get("send_reverb"):
            actions.append({
                "id": f"{tid}:send",
                "track": track_name,
                "type": "set_send",
                "plugin": "Aux Send",
                "settings": track["send_reverb"],
                "risk_class": 2,
                "reason": f"Place '{track_name}' in the {track.get('depth_layer')} depth layer.",
                "validation": "Check depth/space after bounce.",
            })

        for i, a in enumerate(track.get("actions", [])):
            atype = "arrangement" if a["plugin"] == "(arrangement)" else "insert_plugin"
            actions.append({
                "id": f"{tid}:plugin:{i}",
                "track": track_name,
                "type": atype,
                "plugin": a["plugin"],
                "settings": a["setting"],
                "risk_class": a["risk_class"],
                "reason": a["reason"],
                "validation": "A/B against the static baseline.",
            })

        for j, au in enumerate(track.get("automation", [])):
            actions.append({
                "id": f"{tid}:automation:{j}",
                "track": track_name,
                "type": "automation",
                "plugin": au["parameter"],
                "settings": au["move"],
                "risk_class": au.get("risk_class", 2),
                "reason": au["reason"],
                "validation": "Check the gesture lands across the section boundary.",
            })
    return actions
