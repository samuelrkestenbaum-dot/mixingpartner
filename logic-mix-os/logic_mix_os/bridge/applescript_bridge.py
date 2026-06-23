"""AppleScript / Shortcuts code generation (build packet section 41.1, mode C).

Generates *scaffolding only*. Logic Pro's direct AppleScript dictionary is
limited, so real automation goes through System Events / accessibility or a
control surface; these generators emit commented, human-reviewable steps and a
Shortcuts-style action list. Nothing here runs — it returns strings/dicts.
"""

from __future__ import annotations

from typing import Dict, List

_HEADER = """-- Logic Mix OS — generated AppleScript SCAFFOLDING (does not run automatically).
-- Logic Pro exposes limited AppleScript; UI steps go via System Events / a
-- control surface. Review every step. No source audio is modified.
tell application "Logic Pro" to activate
"""


def generate_applescript(actions: List[Dict]) -> str:
    lines = [_HEADER]
    current = None
    for a in actions:
        if a["track"] != current:
            current = a["track"]
            lines.append(f'\n-- ===== Track: {current} =====')
            lines.append(f'-- TODO(System Events): select track "{current}"')
        if a["type"] == "insert_plugin":
            lines.append(f'-- Insert "{a["plugin"]}" on "{a["track"]}"')
            lines.append(f'--   settings: {a["settings"]}')
            lines.append(f'--   reason:   {a["reason"]}  (risk class {a["risk_class"]})')
        elif a["type"] == "set_send":
            lines.append(f'-- Set send for "{a["track"]}": {a["settings"]}')
        elif a["type"] == "automation":
            lines.append(f'-- Automate {a["plugin"]} on "{a["track"]}": {a["settings"]}')
        elif a["type"] == "arrangement":
            lines.append(f'-- Arrangement (manual): {a["settings"]}')
    lines.append('\n-- End of scaffolding. Apply manually or via the Cowork UI bridge.')
    return "\n".join(lines)


def generate_shortcuts(actions: List[Dict]) -> List[Dict]:
    """A macOS Shortcuts-style action list (data only)."""
    out: List[Dict] = []
    current = None
    for a in actions:
        if a["track"] != current:
            current = a["track"]
            out.append({"action": "SelectTrack", "track": current})
        out.append({
            "action": {"insert_plugin": "InsertPlugin", "set_send": "SetSend",
                       "automation": "WriteAutomation", "arrangement": "ManualNote"}.get(a["type"], "Note"),
            "track": a["track"],
            "plugin": a["plugin"],
            "settings": a["settings"],
            "risk_class": a["risk_class"],
        })
    return out
