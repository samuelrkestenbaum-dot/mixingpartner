"""Simulated apply orchestration (Hardening Packet 9; adapter-driven in Packet 10).

The orchestration layer. It consumes a Packet-7 change manifest, validates it
through the Packet-8 harness rules, and drives a :class:`SessionAdapter` to
build a before-state, simulate ONLY the eligible steps, diff before/after,
simulate rollback, prove rollback restores exactly and excluded/blocked targets
are untouched, and record the simulation to the audit ledger.

The orchestration no longer owns fake-session internals — those live behind
``FakeSessionAdapter`` (``session_adapter.py``). A future
``RealLogicSessionAdapter`` can satisfy the same contract without changing this
file. Today the only adapter is fake: nothing real is applied or executed, and
this module performs no file I/O of its own.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Dict, Optional

from .apply_harness import validate_manifest_for_harness
from .governance_ledger import GovernanceLedger
from .session_adapter import FakeSessionAdapter, SessionAdapter

EVENT_RECORDED = "simulated_apply_recorded"
EVENT_REFUSED = "simulated_apply_refused"

# Inert no-real-world flags carried on every result.
_SAFE_FLAGS = {"real_applied": False, "real_executed": False, "touched_real_logic": False,
               "no_real_daw": True, "environment": "simulated_sandbox"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _adapter_meta(adapter: SessionAdapter) -> Dict:
    caps = adapter.capabilities()
    return {"name": adapter.adapter_name(), "type": caps.get("adapter_type"), "capabilities": caps}


def build_fake_session(manifest: Dict, adapter: Optional[SessionAdapter] = None) -> Dict:
    """Back-compat helper: build a fake session via the (fake) session adapter."""
    return (adapter or FakeSessionAdapter()).build_initial_session(manifest)


def _audit(manifest, event_type, status, reason, actor, *, ledger_path, clock) -> Dict:
    if not ledger_path:
        return {"ledger_status": "not_persisted", "ledger_event_id": None,
                "ledger_entry_hash": None, "ledger_verification": None}
    ledger = GovernanceLedger(ledger_path)
    event = ledger.append(event_type, action_id=manifest.get("manifest_id"),
                          receipt_id=manifest.get("manifest_hash"), authority_class=None,
                          decision=event_type, approval_required=False, status=status,
                          actor=actor or "apply_sandbox", reason=reason, timestamp=clock())
    ver = ledger.verify()
    return {"ledger_status": "persisted" if ver["ok"] else "persisted_unverified",
            "ledger_event_id": event["event_id"], "ledger_entry_hash": event["entry_hash"],
            "ledger_verification": ver}


def _refusal(manifest: Dict, reason: str, adapter: SessionAdapter, *, ledger_path, actor, clock) -> Dict:
    return {
        "ok": False,
        "simulated": False,
        **_SAFE_FLAGS,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "reason": reason,
        "before": None,                 # no before/after for an invalid manifest
        "after": None,
        "diff": [],
        "rollback": None,
        "changed_targets": [],
        "excluded_blocked_untouched": True,
        "adapter": _adapter_meta(adapter),
        "audit": _audit(manifest, EVENT_REFUSED, "refused", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }


def simulate_apply(manifest: Dict, *, ledger_path: Optional[str] = None,
                   actor: Optional[str] = None, clock: Optional[Callable[[], str]] = None,
                   adapter: Optional[SessionAdapter] = None) -> Dict:
    """Simulate applying the eligible steps through a :class:`SessionAdapter`.

    Invalid manifests are refused BEFORE any session is built (no before/after
    state). Nothing real is ever applied or executed. Defaults to the
    in-memory ``FakeSessionAdapter``.
    """
    clock = clock or _utc_now
    adapter = adapter or FakeSessionAdapter()

    v = validate_manifest_for_harness(manifest)
    if not v["ok"]:
        return _refusal(manifest, f"Simulation refused: invalid manifest contract — {v['errors']}",
                        adapter, ledger_path=ledger_path, actor=actor, clock=clock)

    eligible = manifest.get("eligible_for_future_apply", [])
    before = adapter.build_initial_session(manifest)
    after = adapter.build_initial_session(manifest)
    for step in eligible:
        adapter.apply_step(after, step)          # mutate only eligible fake targets

    diff = adapter.diff(before, after)
    rollback = adapter.rollback(after, diff)
    rolled_back = rollback.get("rolled_back_session")
    rollback_restored = adapter.verify_rollback(before, rollback)

    changed_targets = [d["target_id"] for d in diff]
    eligible_ids = [adapter.resolve_target(s, manifest) for s in eligible]
    excluded_ids = [adapter.resolve_target(s, manifest) for s in manifest.get("excluded", [])]
    blocked_ids = [adapter.resolve_target(s, manifest) for s in manifest.get("blocked", [])]
    untouched = adapter.verify_untouched(changed_targets, excluded_ids, blocked_ids)

    reason = (f"Simulated {len(changed_targets)} eligible step(s) via {adapter.adapter_name()} in a "
              "fake in-memory session; rollback restored the before-state; no real DAW was touched.")
    return {
        "ok": True,
        "simulated": True,
        **_SAFE_FLAGS,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "plan_id": manifest.get("plan_id"),
        "before": before,
        "after": after,
        "diff": diff,
        "rollback": {"restored": rollback_restored, "rolled_back_session": rolled_back},
        "changed_targets": changed_targets,
        "eligible_target_ids": eligible_ids,
        "excluded_target_ids": excluded_ids,
        "blocked_target_ids": blocked_ids,
        "excluded_blocked_untouched": untouched,
        "counts": {"eligible": len(eligible_ids), "excluded": len(excluded_ids),
                   "blocked": len(blocked_ids), "changed": len(changed_targets)},
        "rollback_restored": rollback_restored,
        "adapter": _adapter_meta(adapter),
        "reason": reason,
        "audit": _audit(manifest, EVENT_RECORDED, "recorded", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }
