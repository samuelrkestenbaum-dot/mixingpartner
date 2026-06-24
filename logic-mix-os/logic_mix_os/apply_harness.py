"""Manifest consumer contract + apply-harness stub (Hardening Packet 8, Layer 1).

Packet 7 produced a validated pre-apply change manifest. This module is the first
*consumer* of that contract: it loads a manifest, validates it for a future apply
surface, classifies readiness, produces an apply-readiness report — and then
explicitly REFUSES to apply, because this environment is still dry-run/spec-only.

It is the apply-boundary rehearsal, not a real apply path. It never executes
Logic, mutates a session, invokes AppleScript, changes bridge behaviour, or
connects to a real macOS/Logic process. The only side effect is appending an
``apply_harness_refused`` event to the governance ledger when a path is given.

Local, deterministic.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .apply_manifest import manifest_hash, validate_manifest
from .governance_ledger import GovernanceLedger

# Readiness statuses (explicit).
READY = "ready_for_future_apply_surface"
NOT_READY_INVALID = "not_ready_invalid_manifest"
NOT_READY_NO_ELIGIBLE = "not_ready_no_eligible_steps"
NOT_READY_BLOCKED_ONLY = "not_ready_blocked_only"
NOT_READY_LEDGER = "not_ready_ledger_invalid"
REFUSED_ENV = "refused_in_this_environment"

_REFUSAL_REASON = ("Apply refused: there is no real Logic surface in this environment. "
                   "This harness validates the manifest contract and stops at the boundary "
                   "(dry-run/spec-only); a future macOS/Logic surface must consume it separately.")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_change_manifest(path: str) -> Dict:
    """Load a Packet-7 change manifest (read-only)."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest_for_harness(manifest: Dict, *, ledger_path: Optional[str] = None) -> Dict:
    """Manifest-only contract validation a future apply surface would require.

    Does NOT touch the ledger file (ledger verification is a readiness concern).
    """
    errors: List[str] = []
    if not isinstance(manifest, dict):
        return {"ok": False, "errors": ["manifest is not an object"]}
    if not manifest.get("manifest_id"):
        errors.append("manifest missing manifest_id")
    if not manifest.get("manifest_hash"):
        errors.append("manifest missing manifest_hash")
    # Re-derive and re-check the full Packet-7 contract (covers hash, eligible
    # invariants, blocked/excluded-not-eligible, nothing_applied, can_execute, ...).
    errors += validate_manifest(manifest)["errors"]

    g = manifest.get("no_apply_guarantee")
    if not isinstance(g, dict):
        errors.append("manifest missing no_apply_guarantee")
    else:
        if g.get("nothing_applied") is not True:
            errors.append("no_apply_guarantee.nothing_applied must be true")
        if g.get("must_not_execute_here") is not True:
            errors.append("no_apply_guarantee.must_not_execute_here must be true")
        if g.get("environment") != "dry_run_spec_only":
            errors.append("no_apply_guarantee.environment must be 'dry_run_spec_only'")
        if g.get("contains_apply_payload") is not False:
            errors.append("no_apply_guarantee.contains_apply_payload must be false")
        if g.get("can_execute") is not False:
            errors.append("no_apply_guarantee.can_execute must be false")

    elig_ids = {s.get("step_id") for s in manifest.get("eligible_for_future_apply", [])}
    for s in manifest.get("eligible_for_future_apply", []):
        if s.get("applied") is not False:
            errors.append(f"eligible step {s.get('step_id')} has applied:true")
        if s.get("must_not_execute_here") is not True:
            errors.append(f"eligible step {s.get('step_id')} lacks must_not_execute_here:true")
    for s in manifest.get("blocked", []):
        if s.get("step_id") in elig_ids:
            errors.append(f"blocked step {s.get('step_id')} appears as eligible")
    if not manifest.get("ledger_status"):
        errors.append("manifest ledger_status must be explicit")
    return {"ok": not errors, "errors": errors}


def _counts(manifest: Dict):
    return (len(manifest.get("eligible_for_future_apply", [])),
            len(manifest.get("excluded", [])), len(manifest.get("blocked", [])))


def build_apply_readiness_report(manifest: Dict, *, ledger_path: Optional[str] = None) -> Dict:
    """Classify whether the manifest would be ready for a future apply surface.

    NOTE: ``ready_for_future_apply_surface`` is NOT permission to apply — apply is
    always refused in this environment (see :func:`refuse_apply`).
    """
    v = validate_manifest_for_harness(manifest)
    eligible, excluded, blocked = _counts(manifest)

    ledger_ok = True
    if ledger_path:
        ledger_ok = GovernanceLedger(ledger_path).verify()["ok"]

    if not v["ok"]:
        readiness = NOT_READY_INVALID
    elif ledger_path and not ledger_ok:
        readiness = NOT_READY_LEDGER
    elif eligible == 0 and blocked > 0 and excluded == 0:
        readiness = NOT_READY_BLOCKED_ONLY
    elif eligible == 0:
        readiness = NOT_READY_NO_ELIGIBLE
    else:
        readiness = READY

    return {
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "plan_id": manifest.get("plan_id"),
        "eligible_count": eligible,
        "excluded_count": excluded,
        "blocked_count": blocked,
        "ledger_status": manifest.get("ledger_status", "not_persisted"),
        "ledger_path": ledger_path,
        "validation_status": "valid" if v["ok"] else "invalid",
        "validation_errors": v["errors"],
        "no_apply_guarantee_status": "ok" if isinstance(manifest.get("no_apply_guarantee"), dict)
        and manifest["no_apply_guarantee"].get("can_execute") is False else "bad",
        "no_apply_guarantee": manifest.get("no_apply_guarantee"),
        "readiness_status": readiness,
        "apply_permitted_here": False,        # never, in this packet
    }


def refuse_apply(manifest: Dict, *, reason: Optional[str] = None, actor: Optional[str] = None,
                 ledger_path: Optional[str] = None, clock: Optional[Callable[[], str]] = None) -> Dict:
    """Refuse to apply a manifest. Always returns ok:false / applied:false / executed:false."""
    clock = clock or _utc_now
    eligible, _excluded, blocked = _counts(manifest)
    ts = clock()
    receipt = {
        "ok": False,
        "applied": False,
        "executed": False,
        "reason": reason or _REFUSAL_REASON,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "authority_boundary": "no_real_logic_surface",
        "environment": "dry_run_spec_only",
        "readiness_status": REFUSED_ENV,
        "eligible_steps_count": eligible,
        "blocked_steps_count": blocked,
        "actor": actor or "apply_harness",
        "timestamp": ts,
    }
    if ledger_path:
        ledger = GovernanceLedger(ledger_path)
        event = ledger.append("apply_harness_refused", action_id=manifest.get("manifest_id"),
                              receipt_id=manifest.get("manifest_hash"), authority_class=None,
                              decision="refuse_apply", approval_required=False,
                              status="refused_in_this_environment", actor=receipt["actor"],
                              reason=receipt["reason"], timestamp=ts)
        ver = ledger.verify()
        receipt.update({"ledger_status": "persisted" if ver["ok"] else "persisted_unverified",
                        "ledger_event_id": event["event_id"], "ledger_entry_hash": event["entry_hash"],
                        "ledger_verification": ver})
    else:
        receipt.update({"ledger_status": "not_persisted", "ledger_event_id": None,
                        "ledger_entry_hash": None, "ledger_verification": None})
    return receipt
