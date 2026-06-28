"""Typed LogicActionPayload contract + adapter capability negotiation (Hardening Packet 11, Layer 1).

Packet 10 extracted the :class:`SessionAdapter` seam; its fake session still
modelled targets only as ``{"configured": bool}`` and never *negotiated* the
adapter's declared ``capabilities()`` per step. This packet inserts the missing
typed layer between a governed manifest step and a session operation:

    governed manifest step
      → typed LogicActionPayload            (parse the free-text action into a
                                             structured, reversible parameter
                                             transition)
        → adapter capability negotiation    (does THIS adapter declare it can
                                             carry THIS payload? required caps +
                                             execution-authority allow-list)
          → reversible adapter operation    (drive ONLY capability-accepted
                                             payloads through the SAME adapter
                                             contract; prove rollback restores)
            → audit                          (record the negotiation to the
                                             hash-chained governance ledger)

It is the negotiation seam a future ``RealLogicSessionAdapter`` slots into
unchanged: it would declare different capabilities, and the SAME ``negotiate``
gate would admit or refuse the SAME typed payloads — without rewriting the
parse, the reversibility proof, or the audit.

Still no real Logic. This module derives typed data and drives only the inert
``FakeSessionAdapter``; it writes NO ``.logicx``/DAW/session file, runs NO
subprocess, calls NO bridge or AppleScript, connects to NO macOS/Logic process,
and — defensively — refuses to drive operations against any adapter that
declares ``real_daw``/``supports_real_apply`` in this environment.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

from .apply_harness import validate_manifest_for_harness
from .governance_ledger import GovernanceLedger
from .session_adapter import FakeSessionAdapter, SessionAdapter, _kind_and_bucket

EVENT_RECORDED = "payload_negotiation_recorded"
EVENT_REFUSED = "payload_negotiation_refused"

# A typed payload requires the adapter to be able to apply-and-reverse it.
REQUIRED_CAPABILITIES = ("supports_simulated_apply", "supports_rollback")
# In this environment every payload requires only simulated execution authority.
REQUIRED_EXECUTION_AUTHORITY = "simulated_only"

# Free-text fake-target kind → a clean, Logic-native action type. Aligned with
# the bridge logic_action schema enum (insert_plugin/set_send/automation/
# arrangement) plus set_parameter for the catch-all kind.
ACTION_TYPE_BY_KIND = {
    "fake_send": "set_send",
    "fake_plugin_slot": "insert_plugin",
    "fake_automation_lane": "automation",
    "fake_region_edit": "arrangement",
    "fake_parameter": "set_parameter",
}

# Inert no-real-world flags carried on every negotiation result (mirrors
# apply_sandbox._SAFE_FLAGS; the environment label marks this layer).
_PLAN_SAFE_FLAGS = {"real_applied": False, "real_executed": False, "touched_real_logic": False,
                    "no_real_daw": True, "environment": "typed_payload_negotiation"}

_AMOUNT_RE = re.compile(r"([+-]?\d+(?:\.\d+)?)\s*(dB|kHz|Hz|%|ms|semitones?|cents?|s)?", re.IGNORECASE)
_UNIT_CANON = {"db": "dB", "khz": "kHz", "hz": "Hz", "%": "%", "ms": "ms",
               "s": "s", "semitone": "semitones", "semitones": "semitones",
               "cent": "cents", "cents": "cents"}
_INCREASE = ("increase", "boost", "raise", "lift", "open", "widen", "add", "+", "up")
_DECREASE = ("decrease", "cut", "reduce", "lower", "narrow", "tighten", "duck", "-", "down")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _h12(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def _adapter_meta(adapter: SessionAdapter) -> Dict:
    caps = adapter.capabilities()
    return {"name": adapter.adapter_name(), "type": caps.get("adapter_type"), "capabilities": caps}


# --- typed parse ------------------------------------------------------------
def _parse_amount_unit(text: str):
    """Pull the first signed numeric amount (+ optional unit) out of free text."""
    m = _AMOUNT_RE.search(text or "")
    if not m or m.group(1) is None:
        return None, None
    try:
        amount = float(m.group(1))
    except (TypeError, ValueError):
        return None, None
    if amount.is_integer():
        amount = int(amount)
    raw_unit = (m.group(2) or "").lower()
    unit = _UNIT_CANON.get(raw_unit) if raw_unit else None
    return amount, unit


def _has_token(low: str, words) -> bool:
    """Word-boundary keyword match so 'up' does not hit inside 'supporting' and
    '-' does not hit inside 'high-pass'."""
    return any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low) for w in words)


def _parse_direction(text: str) -> Optional[str]:
    low = (text or "").lower()
    inc = _has_token(low, _INCREASE)
    dec = _has_token(low, _DECREASE)
    if inc and not dec:
        return "increase"
    if dec and not inc:
        return "decrease"
    return None


def _parameter_slug(action_type: str, text: str) -> str:
    low = (text or "").lower()
    if action_type == "set_send":
        return "send_level"
    if action_type == "insert_plugin":
        if "pass" in low or "hz" in low or " eq" in low or "eq " in low:
            return "eq_frequency"
        if "comp" in low or "limit" in low:
            return "dynamics_threshold"
        return "plugin_setting"
    if action_type == "automation":
        return "fader_ride"
    if action_type == "arrangement":
        return "region_edit"
    return "parameter_value"


def _state_after_op(state: Dict, op: Dict) -> Dict:
    """Apply a typed transition: if the current state matches ``op['before']``
    set it to ``op['after']``; otherwise leave it (idempotent, order-free)."""
    return dict(op["after"]) if state == op["before"] else dict(state)


def _typed_reversibility(transition: Dict) -> Dict:
    """Prove (computationally, not by assertion) that the transition is invertible:
    forward then inverse must return to the before-state."""
    before, after = transition["before"], transition["after"]
    inverse = {"before": after, "after": before}
    forwarded = _state_after_op(before, transition)
    restored = _state_after_op(forwarded, inverse)
    return {"reversible": restored == before, "inverse": inverse,
            "restores_to": before, "method": "typed_inverse"}


def build_payload(step: Dict) -> Dict:
    """Turn ONE governed manifest eligible step into a typed LogicActionPayload.

    Adapter-agnostic: derives the action type, parameter, and a reversible typed
    value transition from the step's free-text ``planned_logic_action``. The
    concrete adapter target id is resolved later (per adapter) during
    negotiation, so the payload is not bound to any one session surface.
    """
    step_id = step.get("step_id")
    action_text = step.get("planned_logic_action") or ""
    kind, _bucket = _kind_and_bucket(action_text)
    action_type = ACTION_TYPE_BY_KIND.get(kind, "set_parameter")
    amount, unit = _parse_amount_unit(action_text)
    direction = _parse_direction(action_text)
    parameter = _parameter_slug(action_type, action_text)

    before_value = {"set": False, "amount": None, "unit": None, "direction": None}
    after_value = {"set": True, "amount": amount, "unit": unit, "direction": direction}
    transition = {"before": before_value, "after": after_value}
    rev = _typed_reversibility(transition)

    return {
        "payload_id": "pld_" + _h12(str(step_id)),
        "step_id": step_id,
        "action_type": action_type,
        "parameter": parameter,
        "target": {"label": action_text, "kind": kind},
        "value": {"amount": amount, "unit": unit, "direction": direction},
        "transition": transition,
        "inverse": rev["inverse"],
        "reversible": rev["reversible"],
        "reversibility_proof": rev,
        "required_capabilities": list(REQUIRED_CAPABILITIES),
        "required_execution_authority": REQUIRED_EXECUTION_AUTHORITY,
        "required_action_support": action_type,
        "authority_class": step.get("authority_class"),
        "planned_logic_action": action_text,
        "rollback_plan": step.get("rollback_plan"),
        "receipt_id": step.get("receipt_id"),
        "decision_id": step.get("decision_id"),
        # payload is intent only — never an applied/real artifact
        "intent_only": True,
        "applied": False,
        "touches_real_logic": False,
    }


def build_payloads(manifest: Dict) -> List[Dict]:
    """Build a typed payload for every eligible step, ordered by step_id."""
    eligible = manifest.get("eligible_for_future_apply", [])
    payloads = [build_payload(s) for s in eligible]
    payloads.sort(key=lambda p: str(p["step_id"]))
    return payloads


# --- capability negotiation -------------------------------------------------
def negotiate(payload: Dict, capabilities: Dict) -> Dict:
    """Negotiate ONE typed payload against an adapter's declared capabilities.

    Accept iff the adapter declares every required capability AND allows the
    payload's required execution authority. Pure computation over the
    capabilities dict — no side effects, no operation driven.
    """
    caps = capabilities or {}
    required = payload.get("required_capabilities", [])
    missing = [c for c in required if not caps.get(c)]
    allowed = list(caps.get("allowed_authority_classes", []) or [])
    need_auth = payload.get("required_execution_authority")
    authority_ok = need_auth in allowed

    # Action-kind negotiation. An adapter that does not declare
    # ``supported_action_types`` is treated as supporting every kind (keeps the
    # Packet-10 FakeSessionAdapter — which declares none — backward compatible);
    # a future/real adapter can narrow what Logic operations it accepts.
    supported_types = caps.get("supported_action_types")        # None => unrestricted
    need_action = payload.get("required_action_support")
    action_supported = supported_types is None or need_action in supported_types

    accepted = (not missing) and authority_ok and action_supported

    reasons: List[str] = []
    if missing:
        reasons.append("adapter is missing required capabilities: " + ", ".join(missing))
    if not authority_ok:
        reasons.append(f"adapter does not allow execution authority '{need_auth}' (allows {allowed})")
    if not action_supported:
        reasons.append(f"adapter does not support action type '{need_action}' (supports {supported_types})")
    if accepted:
        reasons.append(f"adapter satisfies {list(required)}, allows '{need_auth}', and supports '{need_action}'")

    return {
        "payload_id": payload.get("payload_id"),
        "step_id": payload.get("step_id"),
        "accepted": accepted,
        "required_capabilities": list(required),
        "missing_capabilities": missing,
        "required_execution_authority": need_auth,
        "adapter_allowed_authority": allowed,
        "authority_ok": authority_ok,
        "required_action_support": need_action,
        "adapter_supported_action_types": supported_types,
        "action_supported": action_supported,
        "reasons": reasons,
    }


# --- reversible adapter operation (reuses the SessionAdapter contract) -------
def _drive_reversible_operations(adapter: SessionAdapter, manifest: Dict,
                                 accepted_steps: List[Dict]) -> Dict:
    """Drive ONLY the capability-accepted steps through the adapter and prove the
    operation is reversible. Adds NO new session mechanics — every mutation,
    diff, and rollback goes through the existing adapter methods.
    """
    mini = {"manifest_id": manifest.get("manifest_id"),
            "manifest_hash": manifest.get("manifest_hash"),
            "eligible_for_future_apply": accepted_steps}
    before = adapter.build_initial_session(mini)
    after = adapter.build_initial_session(mini)
    for s in accepted_steps:
        adapter.apply_step(after, s)
    diff = adapter.diff(before, after)
    rollback = adapter.rollback(after, diff)
    overall_reversible = adapter.verify_rollback(before, rollback)
    by_target = {}
    for d in diff:
        by_target[d["target_id"]] = {
            "driven": True, "target_id": d["target_id"],
            "before": d["before"], "after": d["after"], "rollback": d["rollback"],
            "reversible_through_adapter": overall_reversible,
        }
    return {"by_target": by_target, "overall_reversible": overall_reversible,
            "changed": len(diff)}


def _audit(manifest: Dict, event_type: str, status: str, reason: str, actor: Optional[str],
           *, ledger_path: Optional[str], clock: Callable[[], str]) -> Dict:
    if not ledger_path:
        return {"ledger_status": "not_persisted", "ledger_event_id": None,
                "ledger_entry_hash": None, "ledger_verification": None}
    ledger = GovernanceLedger(ledger_path)
    event = ledger.append(event_type, action_id=manifest.get("manifest_id"),
                          receipt_id=manifest.get("manifest_hash"), authority_class=None,
                          decision=event_type, approval_required=False, status=status,
                          actor=actor or "payload_negotiator", reason=reason, timestamp=clock())
    ver = ledger.verify()
    return {"ledger_status": "persisted" if ver["ok"] else "persisted_unverified",
            "ledger_event_id": event["event_id"], "ledger_entry_hash": event["entry_hash"],
            "ledger_verification": ver}


def _refusal(manifest: Dict, reason: str, adapter: SessionAdapter, caps: Dict,
             *, ledger_path, actor, clock) -> Dict:
    return {
        "ok": False,
        "negotiated": False,
        **_PLAN_SAFE_FLAGS,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "plan_id": manifest.get("plan_id"),
        "reason": reason,
        "adapter": _adapter_meta(adapter),
        "capabilities": caps,
        "payloads": [],
        "accepted": [],
        "refused": [],
        "counts": {"payloads": 0, "accepted": 0, "refused": 0, "reversible": 0},
        "operations_driven": False,
        "all_accepted_reversible": None,
        "audit": _audit(manifest, EVENT_REFUSED, "refused", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }


def negotiate_payloads(manifest: Dict, adapter: Optional[SessionAdapter] = None, *,
                       ledger_path: Optional[str] = None, actor: Optional[str] = None,
                       clock: Optional[Callable[[], str]] = None) -> Dict:
    """Full Packet-11 vertical slice: governed manifest → typed payloads →
    capability negotiation → reversible adapter operation → audit.

    Invalid manifests are refused before any payload is built. Only
    capability-accepted payloads are driven, and only against a non-real adapter;
    nothing real is ever applied or executed. Defaults to ``FakeSessionAdapter``.
    """
    clock = clock or _utc_now
    adapter = adapter or FakeSessionAdapter()
    caps = adapter.capabilities()

    v = validate_manifest_for_harness(manifest)
    if not v["ok"]:
        return _refusal(manifest, f"Payload negotiation refused: invalid manifest contract — {v['errors']}",
                        adapter, caps, ledger_path=ledger_path, actor=actor, clock=clock)

    eligible = manifest.get("eligible_for_future_apply", [])
    step_by_id = {s.get("step_id"): s for s in eligible}
    payloads = build_payloads(manifest)

    # Defensive: in THIS environment we never drive an operation against an
    # adapter that declares any real surface, even if negotiation would admit it.
    real_capable = bool(caps.get("real_daw") or caps.get("supports_real_apply"))

    for p in payloads:
        step = step_by_id.get(p["step_id"], {})
        p["resolved_target_id"] = adapter.resolve_target(step, manifest)
        p["negotiation"] = negotiate(p, caps)

    accepted = [p for p in payloads if p["negotiation"]["accepted"]]
    refused = [p for p in payloads if not p["negotiation"]["accepted"]]

    operations_driven = (not real_capable) and bool(accepted)
    if real_capable:
        for p in accepted:
            p["operation"] = {"driven": False, "reversible_through_adapter": None,
                              "reason": "real-capable adapter — operations are not driven in this environment"}
        all_reversible = None
    else:
        accepted_steps = [step_by_id[p["step_id"]] for p in accepted if p["step_id"] in step_by_id]
        ops = _drive_reversible_operations(adapter, manifest, accepted_steps) if accepted_steps \
            else {"by_target": {}, "overall_reversible": True, "changed": 0}
        for p in accepted:
            p["operation"] = ops["by_target"].get(
                p["resolved_target_id"],
                {"driven": False, "reversible_through_adapter": None,
                 "reason": "accepted but produced no diff"})
        all_reversible = all(p["operation"].get("reversible_through_adapter") is True for p in accepted) \
            if accepted else True

    for p in refused:
        p["operation"] = {"driven": False, "reversible_through_adapter": None,
                          "reason": "refused by capability negotiation — not driven"}

    counts = {"payloads": len(payloads), "accepted": len(accepted),
              "refused": len(refused),
              "reversible": sum(1 for p in accepted
                                if p["operation"].get("reversible_through_adapter") is True)}
    reason = (f"Negotiated {len(payloads)} typed Logic action payload(s) against "
              f"{adapter.adapter_name()}: {len(accepted)} accepted, {len(refused)} refused; "
              + ("reversible operations driven in a fake in-memory session"
                 if operations_driven else "no operations driven")
              + "; no real DAW was touched.")
    return {
        "ok": True,
        "negotiated": True,
        **_PLAN_SAFE_FLAGS,
        "manifest_id": manifest.get("manifest_id"),
        "manifest_hash": manifest.get("manifest_hash"),
        "plan_id": manifest.get("plan_id"),
        "adapter": _adapter_meta(adapter),
        "capabilities": caps,
        "payloads": payloads,
        "accepted": [p["payload_id"] for p in accepted],
        "refused": [p["payload_id"] for p in refused],
        "counts": counts,
        "operations_driven": operations_driven,
        "all_accepted_reversible": all_reversible,
        "reason": reason,
        "audit": _audit(manifest, EVENT_RECORDED, "recorded", reason, actor,
                        ledger_path=ledger_path, clock=clock),
    }


def assert_inert(result: Dict) -> bool:
    """True iff a negotiation result carries the no-real-world guarantee intact."""
    return (result.get("no_real_daw") is True
            and result.get("real_applied") is False
            and result.get("real_executed") is False
            and result.get("touched_real_logic") is False
            and result.get("environment") == "typed_payload_negotiation")
