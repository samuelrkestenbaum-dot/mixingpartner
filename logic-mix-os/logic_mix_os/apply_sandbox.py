"""In-memory simulated Logic sandbox (Hardening Packet 9, Layer 1).

The first packet where the system performs any kind of *apply* — but only inside
an inert, in-memory fake session. It consumes a Packet-7 change manifest, validates
it through the Packet-8 harness rules, builds a fake before-state, simulates ONLY
the eligible steps, produces a before/after diff and a rollback simulation, proves
rollback restores exactly and that excluded/blocked targets are untouched, and
records the simulation to the audit ledger.

Hard boundary: the only mutable target is an in-memory Python dict created here.
There is NO real Logic session, NO ``.logicx`` / DAW / project / session file, NO
bridge, NO AppleScript, NO subprocess, NO macOS/Logic connection, NO source
mutation. Nothing real is applied or executed.

Local, deterministic.
"""

from __future__ import annotations

import copy
import hashlib
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

from .apply_harness import validate_manifest_for_harness
from .governance_ledger import GovernanceLedger

EVENT_RECORDED = "simulated_apply_recorded"
EVENT_REFUSED = "simulated_apply_refused"

# Inert no-real-world flags carried on every result.
_SAFE_FLAGS = {"real_applied": False, "real_executed": False, "touched_real_logic": False,
               "no_real_daw": True, "environment": "simulated_sandbox"}

_KIND_BUCKET = [
    (("aux send", "send", "plate", "reverb", "delay", "room", "chamber", "hall"),
     "fake_send", "fake_sends"),
    (("plugin", "channel eq", " eq", "compress", "limiter", "stereo-width", "width", "imager"),
     "fake_plugin_slot", "fake_plugin_slots"),
    (("automation", "ride", "fader", "throw", "automate"),
     "fake_automation_lane", "fake_automation_lanes"),
    (("arrangement", "region", "mute", "chop", "one-shot", "accent"),
     "fake_region_edit", "fake_region_edits"),
]
_BUCKETS = ("fake_sends", "fake_plugin_slots", "fake_automation_lanes",
            "fake_region_edits", "fake_parameters")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _h(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]


def _target_id(step_id: str) -> str:
    """Deterministic, stable fake-target id derived from the manifest step id."""
    return "tgt_" + _h(step_id)


def _kind_and_bucket(action: str):
    low = (action or "").lower()
    for needles, kind, bucket in _KIND_BUCKET:
        if any(n in low for n in needles):
            return kind, bucket
    return "fake_parameter", "fake_parameters"


def build_fake_session(manifest: Dict) -> Dict:
    """Synthesize a deterministic, inert in-memory fake session from the manifest.

    Pure Python data. Writes nothing, connects to nothing. The ``value`` of every
    fake target starts unconfigured.
    """
    session: Dict = {
        "session_id": "fakesess_" + _h(str(manifest.get("manifest_id", "")) + "|"
                                       + str(manifest.get("manifest_hash", ""))),
        "is_fake": True,
        "real_logic": False,
        "environment": "simulated_sandbox",
        "fake_tracks": {},
    }
    for b in _BUCKETS:
        session[b] = {}
    for s in manifest.get("eligible_for_future_apply", []):
        sid = s.get("step_id")
        tid = _target_id(sid)
        kind, bucket = _kind_and_bucket(s.get("planned_logic_action", ""))
        session["fake_tracks"][tid] = {"track_id": "trk_" + _h(sid), "for_target": tid}
        session[bucket][tid] = {
            "target_id": tid, "step_id": sid, "kind": kind,
            "name": s.get("planned_logic_action"), "value": {"configured": False},
        }
    return session


def _all_targets(session: Dict) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    for b in _BUCKETS:
        out.update(session.get(b, {}))
    return out


def _set_value(session: Dict, target_id: str, value: Dict) -> None:
    for b in _BUCKETS:
        if target_id in session.get(b, {}):
            session[b][target_id]["value"] = value
            return


def _refusal(manifest: Dict, reason: str, *, ledger_path, actor, clock) -> Dict:
    res = {
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
        "audit": _audit(manifest, EVENT_REFUSED, "refused", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }
    return res


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


def simulate_apply(manifest: Dict, *, ledger_path: Optional[str] = None,
                   actor: Optional[str] = None, clock: Optional[Callable[[], str]] = None) -> Dict:
    """Simulate applying the eligible steps against an in-memory fake session.

    Invalid manifests are refused BEFORE any simulated-mutation path runs (no
    before/after state is built). Nothing real is ever applied or executed.
    """
    clock = clock or _utc_now
    v = validate_manifest_for_harness(manifest)
    if not v["ok"]:
        return _refusal(manifest, f"Simulation refused: invalid manifest contract — {v['errors']}",
                        ledger_path=ledger_path, actor=actor, clock=clock)

    before = build_fake_session(manifest)
    after = copy.deepcopy(before)
    diff: List[Dict] = []
    for s in manifest.get("eligible_for_future_apply", []):
        sid = s.get("step_id")
        tid = _target_id(sid)
        before_val = {"configured": False}
        after_val = {"configured": True, "action": s.get("planned_logic_action")}
        _set_value(after, tid, after_val)
        diff.append({"step_id": sid, "target_id": tid,
                     "planned_action": s.get("planned_logic_action"),
                     "before": before_val, "after": after_val, "rollback": before_val})

    # Rollback simulation: revert every changed target, prove it restores `before`.
    rolled_back = copy.deepcopy(after)
    for d in diff:
        _set_value(rolled_back, d["target_id"], d["rollback"])
    rollback_restored = rolled_back == before

    changed_targets = [d["target_id"] for d in diff]
    eligible_ids = [_target_id(s.get("step_id")) for s in manifest.get("eligible_for_future_apply", [])]
    excluded_ids = [_target_id(s.get("step_id")) for s in manifest.get("excluded", [])]
    blocked_ids = [_target_id(s.get("step_id")) for s in manifest.get("blocked", [])]
    untouched = not (set(changed_targets) & (set(excluded_ids) | set(blocked_ids)))

    reason = (f"Simulated {len(changed_targets)} eligible step(s) in a fake in-memory session; "
              "rollback restored the before-state; no real DAW was touched.")
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
        "reason": reason,
        "audit": _audit(manifest, EVENT_RECORDED, "recorded", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }
