"""Pre-apply Logic change manifest (Hardening Packet 7, Layer 1).

Consolidates a Packet-5 operator review packet, a Packet-6 operator decision
state, and the governance audit ledger into ONE governed, spec-only change
manifest — the single handoff artifact a future apply harness would consume.

The manifest partitions every step by its latest operator decision into
``eligible_for_future_apply`` / ``excluded`` / ``blocked``, carries a
deterministic ``manifest_hash`` over the full handoff contract, and an explicit
no-apply guarantee. It is non-executing and non-applying: approval here means
*approved for future apply when a real Logic surface exists*, never applied.

When a ledger path is given, emitting a manifest appends one ``manifest_emitted``
event to the hash-chained audit ledger (the handoff is audited); with no ledger
path the manifest is a pure local artifact marked ``ledger_status:not_persisted``.

This module derives an artifact; it never runs Logic, mutates a session, invokes
AppleScript, or changes bridge behaviour. Local, deterministic.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

from .governance_ledger import GovernanceLedger

MANIFEST_BANNER = "APPROVED CHANGE MANIFEST — SPEC ONLY, NOTHING WILL BE APPLIED"
APPROVED_FUTURE = "approved_for_future_apply_when_a_real_logic_surface_exists"
FUTURE_APPLY_CONTRACT = (
    "This manifest is the input a future apply harness would consume. It does not "
    "authorize execution and cannot be applied in this environment.")
_NO_APPLY = {"nothing_applied": True, "must_not_execute_here": True,
             "environment": "dry_run_spec_only", "contains_apply_payload": False,
             "can_execute": False}
_EXCLUSION_STATUS = {"reject": "rejected", "request_revision": "revision_requested",
                     "defer": "deferred"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha(payload: Dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


class ManifestError(ValueError):
    """Raised when a bundle is inconsistent — never produce a partial manifest."""


def _canonical_contract(plan_id, source, eligible, excluded, blocked, guarantee, ledger_status) -> Dict:
    """The exact content the manifest_hash covers — the full handoff contract."""
    def el(s):
        return {"step_id": s["step_id"], "receipt_id": s["receipt_id"],
                "decision_id": s.get("decision_id"), "authority_class": s["authority_class"],
                "planned_logic_action": s["planned_logic_action"],
                "rollback_plan": s.get("rollback_plan"), "operator_decision": s.get("operator_decision")}

    def ex(s):
        return {"step_id": s["step_id"], "status": s["status"], "decision_id": s.get("decision_id"),
                "receipt_id": s["receipt_id"], "authority_class": s["authority_class"],
                "planned_logic_action": s["planned_logic_action"], "reason": s.get("reason")}

    def bl(s):
        return {"step_id": s["step_id"], "receipt_id": s["receipt_id"],
                "authority_class": s["authority_class"], "planned_logic_action": s["planned_logic_action"]}

    return {
        "plan_id": plan_id,
        "source": source,
        "eligible_for_future_apply": [el(s) for s in sorted(eligible, key=lambda r: r["step_id"])],
        "excluded": [ex(s) for s in sorted(excluded, key=lambda r: r["step_id"])],
        "blocked": [bl(s) for s in sorted(blocked, key=lambda r: r["step_id"])],
        "no_apply_guarantee": guarantee,
        "ledger_status": ledger_status,
    }


def build_change_manifest(review_packet: Dict, decision_state: Dict, *,
                          ledger_path: Optional[str] = None,
                          clock: Optional[Callable[[], str]] = None) -> Dict:
    """Build the governed pre-apply change manifest. Spec-only; never applies."""
    clock = clock or _utc_now
    if not isinstance(review_packet, dict) or "plan_id" not in review_packet or "steps" not in review_packet:
        raise ManifestError("malformed review packet: missing plan_id/steps")
    if not isinstance(decision_state, dict) or "decisions" not in decision_state \
            or not isinstance(decision_state["decisions"], list):
        raise ManifestError("malformed decision state: missing decisions[]")
    plan_id = review_packet["plan_id"]
    if decision_state.get("plan_id") != plan_id:
        raise ManifestError(f"plan_id mismatch: decisions {decision_state.get('plan_id')!r} "
                            f"vs review packet {plan_id!r}")

    steps = {s["step_id"]: s for s in review_packet["steps"]}
    latest: Dict[str, Dict] = {}
    for d in decision_state["decisions"]:        # last decision per step wins
        latest[d["step_id"]] = d

    # Approved decisions referencing unknown steps / wrong receipts must error.
    for sid, d in latest.items():
        if d["decision"] == "approve":
            if sid not in steps:
                raise ManifestError(f"approved decision references unknown step_id {sid!r}")
            if d.get("receipt_id") != steps[sid].get("receipt_id"):
                raise ManifestError(f"approved step {sid} receipt_id mismatch: decision "
                                    f"{d.get('receipt_id')!r} vs packet {steps[sid].get('receipt_id')!r}")
            if not d.get("actor"):
                raise ManifestError(f"approval of step {sid} is missing an actor/operator id")

    eligible: List[Dict] = []
    excluded: List[Dict] = []
    blocked: List[Dict] = []
    for sid, step in steps.items():
        d = latest.get(sid)
        common = {"step_id": sid, "receipt_id": step.get("receipt_id"),
                  "authority_class": step.get("authority_class"),
                  "planned_logic_action": step.get("planned_logic_action")}
        if step.get("decision") == "blocked":
            blocked.append({**common, "eligible": False,
                            "reason": step.get("cannot_apply_reason", "Class 5 — forbidden, never applied"),
                            "decision_state": (d["decision"] if d else "no_decision")})
            continue
        if d and d["decision"] == "approve":
            # belt-and-suspenders invariants for anything we mark eligible
            if step.get("applied") is True:
                raise ManifestError(f"eligible step {sid} has applied:true — refused")
            if step.get("must_not_execute_here") is not True:
                raise ManifestError(f"eligible step {sid} lacks must_not_execute_here:true — refused")
            eligible.append({
                **common,
                "decision_id": d.get("decision_id"),
                "operator_decision": "approve",
                "resulting_state": d.get("resulting_state", APPROVED_FUTURE),
                "rollback_plan": step.get("rollback_summary"),
                "evidence": step.get("evidence_summary"),
                "approver": d.get("actor"),
                "timestamp": d.get("timestamp"),
                "must_not_execute_here": True,
                "applied": False,
            })
        else:
            status = _EXCLUSION_STATUS.get(d["decision"], "pending") if d else "pending"
            excluded.append({
                **common, "status": status,
                "decision_id": (d or {}).get("decision_id"),
                "reason": (d or {}).get("reason"),
            })

    source = {"source_type": review_packet.get("source_type"), "source_id": review_packet.get("source_id"),
              "variant_id": review_packet.get("variant_id"), "mix_plan_id": review_packet.get("mix_plan_id")}

    # Ledger status (pre-emission) participates in the hash; live counts do not.
    ledger = GovernanceLedger(ledger_path) if ledger_path else None
    if ledger is None:
        ledger_status = "not_persisted"
    else:
        ledger_status = "persisted" if ledger.verify()["ok"] else "persisted_unverified"

    contract = _canonical_contract(plan_id, source, eligible, excluded, blocked, _NO_APPLY, ledger_status)
    manifest_hash = _sha(contract)
    manifest_id = "man_" + manifest_hash[:12]

    emitted_event_id = emitted_entry_hash = None
    ledger_verification = None
    if ledger is not None:
        event = ledger.append("manifest_emitted", action_id=manifest_id, receipt_id=manifest_hash,
                              authority_class=None, decision="emit_manifest", approval_required=False,
                              status="manifest_emitted", actor="manifest_builder",
                              reason=f"Emitted change manifest {manifest_id}: {len(eligible)} eligible, "
                                     f"{len(excluded)} excluded, {len(blocked)} blocked.")
        emitted_event_id, emitted_entry_hash = event["event_id"], event["entry_hash"]
        ledger_verification = ledger.verify()           # re-verify after appending

    return {
        "banner": MANIFEST_BANNER,
        "manifest_id": manifest_id,
        "manifest_hash": manifest_hash,
        "plan_id": plan_id,
        **source,
        "created": clock(),
        "summary": {"total_steps": len(steps), "eligible": len(eligible),
                    "excluded": len(excluded), "blocked": len(blocked)},
        "eligible_for_future_apply": eligible,
        "excluded": excluded,
        "blocked": blocked,
        "no_apply_guarantee": dict(_NO_APPLY),
        "ledger_path": ledger_path,
        "ledger_status": ledger_status,
        "ledger_verification": ledger_verification,
        "manifest_emitted_event_id": emitted_event_id,
        "manifest_emitted_entry_hash": emitted_entry_hash,
        "future_apply_contract": FUTURE_APPLY_CONTRACT,
    }


def manifest_hash(manifest: Dict) -> str:
    """Recompute the canonical manifest hash from a manifest's contract content."""
    source = {k: manifest.get(k) for k in ("source_type", "source_id", "variant_id", "mix_plan_id")}
    contract = _canonical_contract(
        manifest.get("plan_id"), source, manifest.get("eligible_for_future_apply", []),
        manifest.get("excluded", []), manifest.get("blocked", []),
        manifest.get("no_apply_guarantee", {}), manifest.get("ledger_status"))
    return _sha(contract)


def validate_manifest(manifest: Dict) -> Dict:
    """Structural + integrity validation of a built manifest."""
    errors: List[str] = []
    if manifest.get("manifest_hash") != manifest_hash(manifest):
        errors.append("manifest_hash does not match canonical contract content")
    g = manifest.get("no_apply_guarantee", {})
    if g.get("nothing_applied") is not True:
        errors.append("no_apply_guarantee.nothing_applied must be true")
    if g.get("can_execute") is not False:
        errors.append("no_apply_guarantee.can_execute must be false")
    if not manifest.get("ledger_status"):
        errors.append("ledger_status must be explicit")

    eligible = manifest.get("eligible_for_future_apply", [])
    elig_ids = {s["step_id"] for s in eligible}
    for s in eligible:
        if s.get("applied") is not False:
            errors.append(f"eligible step {s.get('step_id')} is marked applied — forbidden")
        if s.get("operator_decision") != "approve":
            errors.append(f"eligible step {s.get('step_id')} is not an approve decision")
        if not s.get("receipt_id"):
            errors.append(f"eligible step {s.get('step_id')} missing receipt_id")
        if not s.get("decision_id"):
            errors.append(f"eligible step {s.get('step_id')} missing decision_id")
        if s.get("must_not_execute_here") is not True:
            errors.append(f"eligible step {s.get('step_id')} missing must_not_execute_here")
    for s in manifest.get("blocked", []):
        if s["step_id"] in elig_ids:
            errors.append(f"blocked step {s['step_id']} also appears as eligible")
    for s in manifest.get("excluded", []):
        if s["step_id"] in elig_ids:
            errors.append(f"excluded step {s['step_id']} also appears as eligible")
        if s.get("status") != "pending" and not s.get("decision_id"):
            errors.append(f"decided excluded step {s['step_id']} missing decision_id")
    return {"ok": not errors, "errors": errors}
