"""Dry-run executor (build packet sections 41, 76, 77, 78).

Simulates applying an action list under a review mode, honouring kill-switches
and risk classes. It NEVER touches Logic or any audio file — it returns a log of
what *would* happen. This is the safety spine of the bridge: propose, preview,
log, validate.
"""

from __future__ import annotations

from typing import Dict, List

from ..governance import REVIEW_MODES, validate_action_safety

EXECUTION_MODES = {
    "A_file_processing": "Direct file/audio analysis and preview renders (safe).",
    "B_checklist": "Generate a Logic checklist for human/Cowork execution.",
    "C_ui_automation": "AppleScript/Shortcuts/accessibility scaffolding (review required).",
    "D_helper_au": "Custom Audio Unit helper plugin for metering Logic can't expose.",
}


def dry_run(actions: List[Dict], review_mode: str = "approve_before_apply") -> Dict:
    if review_mode not in REVIEW_MODES:
        review_mode = "approve_before_apply"

    log = {"review_mode": review_mode, "executed": [], "would_apply": [],
           "pending_approval": [], "blocked": [], "observed": []}

    for a in actions:
        safety = validate_action_safety({"risk_class": a.get("risk_class", 2),
                                         "plugin": a.get("plugin", ""),
                                         "setting": a.get("settings", "")})
        if safety["blocked"]:
            log["blocked"].append({"id": a["id"], "track": a["track"], "reason": safety["reason"]})
            continue

        rc = a.get("risk_class", 2)
        if review_mode == "observe_only":
            log["observed"].append(a["id"])
        elif review_mode in {"recommend_only", "checklist_only", "manual_only"}:
            log["pending_approval"].append(a["id"])
        elif review_mode == "approve_before_apply":
            log["pending_approval"].append(a["id"])
        elif review_mode == "safe_auto_apply":
            (log["would_apply"] if rc <= 2 else log["pending_approval"]).append(a["id"])

    # NOTE: nothing is ever actually executed here; "executed" stays empty by design.
    log["summary"] = {
        "total": len(actions),
        "blocked": len(log["blocked"]),
        "would_apply": len(log["would_apply"]),
        "pending_approval": len(log["pending_approval"]),
        "note": "Dry run only — no Logic session or audio was modified.",
    }
    return log
