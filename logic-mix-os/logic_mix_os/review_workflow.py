"""Operator review → decision workflow (Hardening Packet 6, Layer 1).

Packet 5 produces a governed, dry-run Logic *review packet*. This module lets a
human operator record structured per-step decisions against that packet —
``approve`` / ``reject`` / ``request_revision`` / ``defer`` — plus plan-level
helpers, while preserving the no-apply boundary.

Every decision:
  * is validated (plan/step/receipt/actor; reason required to reject or revise),
  * appends a tamper-evident event to the persisted governance audit ledger,
  * creates a NEW decision receipt without mutating the original review packet,
  * never applies anything. Approving a Class-3 step means
    ``approved_for_future_apply_when_a_real_logic_surface_exists`` — not applied.
    ``must_not_execute_here`` and ``nothing_applied`` stay true throughout.

This module records decisions; it never executes Logic, mutates a session,
invokes AppleScript, or changes bridge behaviour. Local, deterministic.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .governance_ledger import GovernanceLedger

DECISIONS = ("approve", "reject", "request_revision", "defer")
_REASON_REQUIRED = ("reject", "request_revision")
# Decision verbs that would mean execution — always refused in this environment.
_APPLY_WORDS = ("apply", "applied", "mark_applied", "execute", "run")

_RESULTING_STATE = {
    "reject": "rejected",
    "request_revision": "revision_requested",
    "defer": "deferred",
}
APPROVED_FUTURE = "approved_for_future_apply_when_a_real_logic_surface_exists"

DECISIONS_BANNER = "DECISIONS RECORDED — NOTHING APPLIED"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _h(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]


def load_review_packet(path: str) -> Dict:
    """Load a Packet-5 operator review packet (read-only)."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_decisions(path: str) -> Dict:
    """Load a previously-written operator decision state artifact."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


class ReviewWorkflow:
    """Records operator decisions against a review packet, append-only + audited."""

    def __init__(self, packet: Dict, *, decisions: Optional[List[Dict]] = None,
                 ledger_path: Optional[str] = None, ledger: Optional[GovernanceLedger] = None,
                 clock: Optional[Callable[[], str]] = None):
        if "plan_id" not in packet or "steps" not in packet:
            raise ValueError("not a review packet: missing plan_id/steps")
        self.packet = packet
        self.plan_id = packet["plan_id"]
        self._steps = {s["step_id"]: s for s in packet["steps"]}
        self._decisions: List[Dict] = list(decisions or [])
        self._clock = clock or _utc_now
        self.ledger_path = ledger_path
        self._ledger = ledger or GovernanceLedger(ledger_path, clock)

    # -- single-step decision ----------------------------------------------
    def decide(self, step_id: str, decision: str, *, actor: str,
               reason: Optional[str] = None) -> Dict:
        if decision in _APPLY_WORDS:
            raise ValueError("applying is not permitted — this is a dry-run/spec-only "
                             "workflow; decisions never execute Logic.")
        if decision not in DECISIONS:
            raise ValueError(f"unknown decision '{decision}'; expected one of {DECISIONS}")
        if not actor:
            raise ValueError("an operator/actor id is required to record a decision")
        step = self._steps.get(step_id)
        if step is None:
            raise ValueError(f"unknown step_id '{step_id}' for plan {self.plan_id}")
        if decision in _REASON_REQUIRED and not (reason and reason.strip()):
            raise ValueError(f"a reason is required to {decision} step {step_id}")
        if decision == "approve" and step.get("decision") == "blocked":
            raise ValueError(f"step {step_id} is blocked (Class {step.get('authority_class')}) "
                             "and cannot be approved")

        cls = step.get("authority_class")
        if decision == "approve":
            resulting_state = APPROVED_FUTURE if (cls or 0) >= 3 else "approved"
        else:
            resulting_state = _RESULTING_STATE[decision]

        ts = self._clock()
        event = self._ledger.append(
            f"operator_{decision}", action_id=step_id, receipt_id=step.get("receipt_id"),
            authority_class=cls, decision=decision, approval_required=(cls or 0) >= 3,
            status=resulting_state, actor=actor, reason=reason or "", timestamp=ts,
        )
        decision_receipt = {
            "decision_id": "dec_" + _h(f"{self.plan_id}|{step_id}|{decision}|{actor}|{len(self._decisions)}"),
            "plan_id": self.plan_id,
            "step_id": step_id,
            "receipt_id": step.get("receipt_id"),       # original planner receipt, preserved
            "planned_logic_action": step.get("planned_logic_action") or step.get("logic_action"),
            "authority_class": cls,
            "decision": decision,
            "resulting_state": resulting_state,
            "actor": actor,
            "reason": reason or None,
            "timestamp": ts,
            "must_not_execute_here": bool(step.get("must_not_execute_here", (cls or 0) >= 3)),
            "applied": False,
            "audit_event_id": event["event_id"],
            "audit_entry_hash": event["entry_hash"],
        }
        self._decisions.append(decision_receipt)
        return decision_receipt

    # -- plan-level helpers -------------------------------------------------
    def _approvable(self) -> List[str]:
        return [sid for sid, s in self._steps.items() if s.get("decision") != "blocked"]

    def approve_all_allowed(self, *, actor: str) -> List[Dict]:
        """Approve every non-blocked step (blocked steps are skipped, never approved)."""
        return [self.decide(sid, "approve", actor=actor) for sid in self._approvable()]

    def reject_all(self, *, actor: str, reason: str) -> List[Dict]:
        return [self.decide(sid, "reject", actor=actor, reason=reason) for sid in self._steps]

    def defer_all(self, *, actor: str, reason: Optional[str] = None) -> List[Dict]:
        return [self.decide(sid, "defer", actor=actor, reason=reason) for sid in self._steps]

    # -- state / summary ----------------------------------------------------
    def summarize_decisions(self) -> Dict:
        latest: Dict[str, str] = {}
        for d in self._decisions:               # last decision per step wins
            latest[d["step_id"]] = d["decision"]
        counts = {"approved": 0, "rejected": 0, "revision_requested": 0, "deferred": 0}
        keymap = {"approve": "approved", "reject": "rejected",
                  "request_revision": "revision_requested", "defer": "deferred"}
        for dec in latest.values():
            counts[keymap[dec]] += 1
        decided = set(latest)
        blocked = [sid for sid, s in self._steps.items() if s.get("decision") == "blocked"]
        return {
            "total_steps": len(self._steps),
            "decisions_recorded": len(self._decisions),
            **counts,
            "pending": len([sid for sid in self._steps if sid not in decided]),
            "blocked": len(blocked),
        }

    def state(self) -> Dict:
        return {
            "banner": DECISIONS_BANNER,
            "plan_id": self.plan_id,
            "source_type": self.packet.get("source_type"),
            "source_id": self.packet.get("source_id"),
            "decisions": list(self._decisions),
            "summary": self.summarize_decisions(),
            "ledger_path": self.ledger_path,
            "ledger_verification": self._ledger.verify() if self.ledger_path else None,
            "environment": "dry_run_spec_only",
            "must_not_execute_here": True,
            "nothing_applied": True,
        }

    def decisions(self) -> List[Dict]:
        return list(self._decisions)

    def verify_ledger(self) -> Dict:
        return self._ledger.verify()

    def save_json(self, out_dir: str) -> str:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = out / "operator_decisions.json"
        path.write_text(json.dumps(self.state(), indent=2) + "\n", encoding="utf-8")
        return str(path)


def workflow_from_artifacts(packet_path: str, *, decisions_path: Optional[str] = None,
                            ledger_path: Optional[str] = None,
                            clock: Optional[Callable[[], str]] = None) -> ReviewWorkflow:
    """Reconstruct a workflow: load the packet and (optionally) prior decision state."""
    packet = load_review_packet(packet_path)
    prior = load_decisions(decisions_path)["decisions"] if decisions_path else None
    return ReviewWorkflow(packet, decisions=prior, ledger_path=ledger_path, clock=clock)
