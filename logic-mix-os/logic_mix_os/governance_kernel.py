"""Gravito Creative Governance Kernel (Hardening Packet 3, Layer 1).

The gate that must exist before any real Logic execution. Every proposed
action / variant / render decision is classified onto a music-specific authority
ladder (Class 0-5), receipt-backed, given a rollback plan, and gated by approval.
Nothing above Class 2 can be marked *applied* without an approval receipt, and in
this environment real Logic mutation (Class 3+) is dry-run/spec only — never
executed. Class 5 is always blocked.

Pure, deterministic, local. No DAW, no network, no execution.
"""

from __future__ import annotations

import hashlib
from typing import Callable, Dict, List, Optional

from .governance_ledger import GovernanceLedger

# --- Authority ladder (music-specific) -------------------------------------
AUTHORITY_CLASSES = {
    0: {"name": "observe_only",
        "description": "Analyse stems, inspect renders, compare reports, classify. No writes except reports.",
        "examples": ["analyze", "inspect", "compare", "classify"]},
    1: {"name": "local_artifact_only",
        "description": "Write reports / JSON receipts / action plans / dry-run bridge artifacts. No source mutation.",
        "examples": ["write_report", "write_receipt", "write_plan", "dry_run_bridge", "ingest_external_render"]},
    2: {"name": "reversible_local_audio_artifact",
        "description": "Render offline variants to generated folders, write taste-memory entries, generate rollback plans. No Logic mutation.",
        "examples": ["offline_render", "write_taste", "write_rollback"]},
    3: {"name": "controlled_daw_mutation",
        "description": "Write Logic automation, insert plugins, change sends/routing, apply session edits. Explicit approval; dry-run/spec only here.",
        "examples": ["insert_plugin", "set_send", "automation", "routing", "session_edit", "arrangement"]},
    4: {"name": "high_risk_external_or_prod",
        "description": "Overwrite project, export final master, upload/share externally, replace source assets. Hard approval; must not execute here.",
        "examples": ["export_master", "upload", "share", "replace_source_asset"]},
    5: {"name": "forbidden_destructive",
        "description": "Mutate source stems in place, delete source audio, hidden/unlogged DAW mutation, unapproved Class 3/4 apply. Always blocked.",
        "examples": ["overwrite_source", "delete_source", "hidden_execution", "unlogged_mutation"]},
}

_KIND_CLASS = {}
for _cls, _meta in AUTHORITY_CLASSES.items():
    for _ex in _meta["examples"]:
        _KIND_CLASS[_ex] = _cls

_DESTRUCTIVE_MARKERS = ["overwrite source", "delete source", "in place", "in-place",
                        "hidden", "unlogged", "mutate source", "destroy"]
_EXTERNAL_MARKERS = ["export master", "final master", "upload", "share externally", "replace source"]
_DAW_MARKERS = ["insert plugin", "logic automation", "write automation", "send level",
                "routing", "session edit", "plugin parameter"]

_RISK_LEVEL = {0: "none", 1: "low", 2: "low", 3: "elevated", 4: "high", 5: "forbidden"}


def _h(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]


# Fail-safe-high: an unknown / ambiguous / unrecognised action must NOT default
# to Class 0 (observe). It is escalated to review-required at this class so a
# human gates it. (Pre-apply hardening, Packet 4.)
REVIEW_DEFAULT_CLASS = 3

_MARKER_SETS = [
    (_DESTRUCTIVE_MARKERS, 5, "destructive"),
    (_EXTERNAL_MARKERS, 4, "external_prod"),
    (_DAW_MARKERS, 3, "daw_session"),
]


def classify_action_detailed(action: Dict) -> Dict:
    """Classify an action onto the authority ladder, fail-safe-high.

    Known-safe kinds keep their low class; unknown kinds and benign kinds carrying
    risky markers are escalated to the HIGHER class (never the lower). Returns the
    class plus the reasoning so receipts can show *why* it escalated.
    """
    kind = (action.get("kind") or action.get("type") or "").strip()
    text = " ".join(str(action.get(k, "")) for k in ("kind", "type", "setting", "reason", "op", "intent")).lower()

    kind_class = _KIND_CLASS.get(kind)  # None if unrecognised
    unknown_kind = kind_class is None

    matched: Dict[str, List[str]] = {}
    marker_class = None
    for markers, mcls, label in _MARKER_SETS:
        hits = [m for m in markers if m in text]
        if hits:
            matched[label] = hits
            marker_class = mcls if marker_class is None else max(marker_class, mcls)

    candidates = [c for c in (kind_class, marker_class) if c is not None]
    final = max(candidates) if candidates else REVIEW_DEFAULT_CLASS
    base = kind_class if kind_class is not None else 0

    escalated_by_marker = marker_class is not None and marker_class > base
    ambiguous = bool(unknown_kind or escalated_by_marker or len(matched) > 1)

    if unknown_kind and marker_class is None:
        reason = f"Unknown action kind '{kind or '?'}' with no recognised markers — fail-safe-high review (Class {final})."
    elif unknown_kind:
        reason = f"Unknown action kind '{kind or '?'}'; markers {matched} — escalated to Class {final} (fail-safe-high)."
    elif escalated_by_marker:
        reason = f"Known kind '{kind}' (Class {base}) escalated to Class {final} by markers {matched}."
    elif len(matched) > 1:
        reason = f"Known kind '{kind}'; multiple marker categories {list(matched)} — highest wins (Class {final})."
    else:
        reason = f"Known kind '{kind}' — Class {final}."

    return {
        "authority_class": final,
        "ambiguous": ambiguous,
        "unknown_kind": unknown_kind,
        "matched_markers": matched,
        "classification_reason": reason,
        "escalated_from": base,
        "escalated_to": final,
    }


def classify_action(action: Dict) -> int:
    """Map a proposed action to an authority class (0-5)."""
    return classify_action_detailed(action)["authority_class"]


def _rollback_for(cls: int, action: Dict):
    target = action.get("target_artifacts") or action.get("target") or "the generated artifact"
    return {
        0: ("trivial", "No state changed; reports/analyses are read-only outputs."),
        1: ("reversible", f"Delete {target}."),
        2: ("reversible", "Delete the generated render/folder; taste-memory entries are append-only and "
                          "can be reverted by removing the last entry."),
        3: ("reversible_with_plan", "Duplicate the track and save a Logic project alternative BEFORE applying; "
                                    "undo via Logic history or restore the alternative. (Dry-run/spec only here.)"),
        4: ("not_permitted_here", "n/a — must not execute in this environment."),
        5: ("not_permitted", "n/a — blocked."),
    }[cls]


class GovernanceKernel:
    """Holds the action ledger + operator review state.

    The in-memory ``_ledger`` (a list of full receipts) is the live working
    state. The optional persisted ``GovernanceLedger`` is a separate, append-only,
    hash-chained audit trail (``governance_ledger.jsonl``). When a ledger path is
    given, a fresh kernel reconstructs its authority state from the persisted
    events so gating survives a process restart.
    """

    def __init__(self, ledger_path: Optional[str] = None, actor: str = "operator",
                 clock: Optional[Callable[[], str]] = None):
        self._ledger: List[Dict] = []
        self._counter = 0
        self._actor = actor
        self._events = GovernanceLedger(ledger_path, clock)
        if len(self._events):
            self._reconstruct_from_events()

    # -- reconstruction (process-restart durability) ------------------------
    def _reconstruct_from_events(self) -> None:
        """Replay persisted events into minimal-but-functional receipts."""
        for e in self._events.entries():
            etype, action_id = e["event_type"], e.get("action_id")
            if etype == "propose":
                self._ledger.append({
                    "action_id": action_id,
                    "receipt_id": e.get("receipt_id"),
                    "authority_class": e.get("authority_class"),
                    "approval_required": bool(e.get("approval_required")),
                    "decision": e.get("decision"),
                    "status": e.get("status"),
                    "approved": False,
                    "approval_receipt": None,
                    "reconstructed": True,
                })
                if action_id and action_id.startswith("act_"):
                    try:
                        self._counter = max(self._counter, int(action_id.split("_")[1]))
                    except (ValueError, IndexError):
                        pass
            elif etype == "approve":
                r = self._find(action_id)
                if r is not None:
                    r["approved"] = True
                    r["approval_receipt"] = {"approver": e.get("actor"), "note": e.get("reason"),
                                             "reconstructed": True}
            elif etype == "applied":
                r = self._find(action_id)
                if r is not None:
                    r["status"] = "applied"

    # -- proposal -----------------------------------------------------------
    def propose(self, action: Dict) -> Dict:
        detail = classify_action_detailed(action)
        cls = detail["authority_class"]
        source_immutable = bool(action.get("source_immutable", True))
        generated_only = bool(action.get("generated_output_only", True))

        if cls <= 1:
            decision, allowed_now, approval_required = "allow", True, False
        elif cls == 2:
            if source_immutable and generated_only:
                decision, allowed_now, approval_required = "allow", True, False
            else:
                decision, allowed_now, approval_required = "review_required", False, True
        elif cls == 3:
            decision, allowed_now, approval_required = "review_required", False, True
        elif cls == 4:
            decision, allowed_now, approval_required = "review_required", False, True
        else:  # cls == 5
            decision, allowed_now, approval_required = "blocked", False, False

        reversibility, rollback_plan = _rollback_for(cls, action)
        self._counter += 1
        action_id = f"act_{self._counter:03d}"
        receipt_id = "rcpt_" + _h(f"{action_id}|{action.get('kind') or action.get('type')}|{action.get('reason','')}")

        receipt = {
            "action_id": action_id,
            "receipt_id": receipt_id,
            "kind": action.get("kind") or action.get("type"),
            "authority_class": cls,
            "authority_name": AUTHORITY_CLASSES[cls]["name"],
            "risk_level": _RISK_LEVEL[cls],
            "ambiguous": detail["ambiguous"],
            "unknown_kind": detail["unknown_kind"],
            "matched_markers": detail["matched_markers"],
            "classification_reason": detail["classification_reason"],
            "escalated_from": detail["escalated_from"],
            "escalated_to": detail["escalated_to"],
            "allowed_now": allowed_now,
            "approval_required": approval_required,
            "must_not_execute_here": cls >= 3,
            "evidence": action.get("evidence", []),
            "reason": action.get("reason", AUTHORITY_CLASSES[cls]["description"]),
            "reversibility": reversibility,
            "rollback_plan": rollback_plan,
            "source_artifacts": action.get("source_artifacts", []),
            "target_artifacts": action.get("target_artifacts", []),
            "decision": decision,
            "status": {"allow": "allowed", "review_required": "pending_review", "blocked": "blocked"}[decision],
            "approved": False,
            "approval_receipt": None,
        }
        self._ledger.append(receipt)
        self._events.append(
            "propose", action_id=action_id, receipt_id=receipt_id, authority_class=cls,
            decision=decision, approval_required=approval_required, status=receipt["status"],
            actor=self._actor, reason=detail["classification_reason"],
        )
        return receipt

    # -- approval / apply ---------------------------------------------------
    def _find(self, action_id: str) -> Optional[Dict]:
        return next((r for r in self._ledger if r["action_id"] == action_id), None)

    def approve(self, action_id: str, approver: str = "operator", note: Optional[str] = None) -> Dict:
        r = self._find(action_id)
        if r is None:
            return {"ok": False, "reason": f"unknown action {action_id}"}
        if r["authority_class"] == 5:
            self._log_event("blocked_approval_attempt", r, approver,
                            "Class 5 is forbidden and cannot be approved.")
            return {"ok": False, "reason": "Class 5 is forbidden and cannot be approved."}
        r["approved"] = True
        r["approval_receipt"] = {
            "approver": approver, "note": note,
            "approval_id": "appr_" + _h(f"{action_id}|{approver}|{note}"),
        }
        self._log_event("approve", r, approver, note or "approved")
        return {"ok": True, "approval_receipt": r["approval_receipt"]}

    def mark_applied(self, action_id: str) -> Dict:
        r = self._find(action_id)
        if r is None:
            return {"ok": False, "reason": f"unknown action {action_id}"}
        cls = r["authority_class"]
        self._log_event("mark_applied_attempt", r, self._actor, "apply requested")
        if cls >= 5:
            reason = "Class 5 is blocked; never applied."
            self._log_event("mark_applied_refused", r, self._actor, reason)
            return {"ok": False, "reason": reason}
        if cls >= 3:
            reason = "Class 3+ is dry-run/spec only in this environment — not applied."
            self._log_event("mark_applied_refused", r, self._actor, reason)
            return {"ok": False, "reason": reason}
        if r["approval_required"] and not r["approved"]:
            reason = "Approval receipt required before this action can be applied."
            self._log_event("mark_applied_refused", r, self._actor, reason)
            return {"ok": False, "reason": reason}
        r["status"] = "applied"
        self._log_event("applied", r, self._actor, "applied")
        return {"ok": True, "status": "applied"}

    # -- audit-trail helpers -----------------------------------------------
    def _log_event(self, event_type: str, receipt: Dict, actor: str, reason: str) -> Dict:
        return self._events.append(
            event_type, action_id=receipt["action_id"], receipt_id=receipt.get("receipt_id"),
            authority_class=receipt["authority_class"], decision=receipt.get("decision"),
            approval_required=receipt.get("approval_required"), status=receipt.get("status"),
            actor=actor, reason=reason,
        )

    def ledger(self) -> List[Dict]:
        return self._ledger

    def events(self) -> List[Dict]:
        """The persisted (or in-memory) hash-chained audit events."""
        return self._events.entries()

    def verify_ledger(self) -> Dict:
        """Verify the tamper-evidence chain of the governance event ledger."""
        return self._events.verify()


# --- convenience -----------------------------------------------------------
def govern_actions(actions: List[Dict], kernel: Optional[GovernanceKernel] = None) -> Dict:
    kernel = kernel or GovernanceKernel()
    receipts = [kernel.propose(a) for a in actions]
    summary: Dict[str, int] = {}
    for r in receipts:
        summary[r["decision"]] = summary.get(r["decision"], 0) + 1
    return {"receipts": receipts, "summary": summary, "ledger_size": len(kernel.ledger())}


def demo_actions() -> List[Dict]:
    """Representative actions spanning the full ladder (for examples/tests)."""
    return [
        {"kind": "analyze", "reason": "inspect stems"},
        {"kind": "write_report", "target_artifacts": ["reports/mix_plan.md"], "reason": "write the mix plan"},
        {"kind": "offline_render", "target_artifacts": ["renders/variant_A.wav"],
         "source_immutable": True, "generated_output_only": True, "reason": "render an offline variant"},
        {"kind": "offline_render", "source_immutable": False, "reason": "render that would touch a source stem"},
        {"kind": "insert_plugin", "setting": "Channel EQ on Lead Vocal", "reason": "write a Logic plugin insert"},
        {"kind": "export_master", "reason": "export the final master and upload externally"},
        {"kind": "overwrite_source", "reason": "overwrite source stem in place"},
    ]
