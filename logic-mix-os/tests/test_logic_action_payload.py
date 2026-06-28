"""Packet 11, Layer 1 — typed LogicActionPayload + adapter capability negotiation."""

from __future__ import annotations

import json

from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.governance_ledger import GovernanceLedger
from logic_mix_os.logic_action_payload import (
    REQUIRED_CAPABILITIES,
    REQUIRED_EXECUTION_AUTHORITY,
    assert_inert,
    build_payload,
    build_payloads,
    negotiate,
    negotiate_payloads,
)
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.session_adapter import FakeSessionAdapter
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",
        "High-pass supporting bus ~250 Hz",
        "Ride lead vocal +1 dB into the chorus",               # reject -> excluded
        "Delete source audio in place to bake the loop chop",  # blocked
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-06-01T00:00:{n['i']:02d}+00:00"

    return clock


def _manifest():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "approve", actor="alice")
    wf.decide(review[2], "reject", actor="alice", reason="not now")
    return build_change_manifest(packet, wf.state())


# --- typed parse ----------------------------------------------------------
def test_payload_is_typed_and_reversible():
    p = build_payloads(_manifest())[0]
    assert p["payload_id"].startswith("pld_")
    assert p["action_type"] in {"set_send", "insert_plugin", "automation", "arrangement", "set_parameter"}
    assert p["parameter"]
    assert p["transition"]["before"]["set"] is False
    assert p["transition"]["after"]["set"] is True
    assert p["reversible"] is True
    assert p["intent_only"] is True and p["applied"] is False and p["touches_real_logic"] is False


def test_send_payload_parsed():
    # "Set/adjust aux send: Increase backing-vocal plate send +3 dB"
    p = [p for p in build_payloads(_manifest()) if p["action_type"] == "set_send"][0]
    assert p["parameter"] == "send_level"
    assert p["value"] == {"amount": 3, "unit": "dB", "direction": "increase"}


def test_eq_payload_parsed():
    # "Insert/adjust Channel EQ: High-pass supporting bus ~250 Hz"
    p = [p for p in build_payloads(_manifest()) if p["action_type"] == "insert_plugin"][0]
    assert p["parameter"] == "eq_frequency"
    assert p["value"]["amount"] == 250 and p["value"]["unit"] == "Hz"
    # 'high-pass' / 'supporting' must NOT be misread as a direction
    assert p["value"]["direction"] is None


def test_payloads_deterministic_and_sorted():
    m = _manifest()
    a, b = build_payloads(m), build_payloads(m)
    assert a == b
    assert [p["step_id"] for p in a] == sorted(p["step_id"] for p in a)


def test_typed_reversibility_is_computed():
    for p in build_payloads(_manifest()):
        proof = p["reversibility_proof"]
        assert proof["method"] == "typed_inverse"
        assert proof["reversible"] is True
        assert proof["restores_to"] == p["transition"]["before"]
        # the declared inverse swaps before/after
        assert p["inverse"]["after"] == p["transition"]["before"]


# --- capability negotiation (unit) ----------------------------------------
def test_negotiate_accepts_fake_capabilities():
    p = build_payloads(_manifest())[0]
    neg = negotiate(p, FakeSessionAdapter().capabilities())
    assert neg["accepted"] is True
    assert neg["missing_capabilities"] == []
    assert neg["authority_ok"] is True
    assert neg["required_capabilities"] == list(REQUIRED_CAPABILITIES)
    assert neg["required_execution_authority"] == REQUIRED_EXECUTION_AUTHORITY


def test_negotiate_refuses_missing_capability():
    p = build_payloads(_manifest())[0]
    caps = dict(FakeSessionAdapter().capabilities())
    caps["supports_rollback"] = False
    neg = negotiate(p, caps)
    assert neg["accepted"] is False
    assert "supports_rollback" in neg["missing_capabilities"]


def test_negotiate_refuses_disallowed_authority():
    p = build_payloads(_manifest())[0]
    caps = dict(FakeSessionAdapter().capabilities())
    caps["allowed_authority_classes"] = ["real_apply"]   # does not allow simulated_only
    neg = negotiate(p, caps)
    assert neg["authority_ok"] is False and neg["accepted"] is False


def test_negotiate_gates_on_action_type():
    payloads = build_payloads(_manifest())
    send = [p for p in payloads if p["action_type"] == "set_send"][0]
    eq = [p for p in payloads if p["action_type"] == "insert_plugin"][0]
    caps = dict(FakeSessionAdapter().capabilities())
    caps["supported_action_types"] = ["set_send"]        # narrows what the adapter accepts
    assert negotiate(send, caps)["accepted"] is True
    eq_neg = negotiate(eq, caps)
    assert eq_neg["accepted"] is False and eq_neg["action_supported"] is False


def test_absent_supported_action_types_means_unrestricted():
    # FakeSessionAdapter declares no supported_action_types — every kind is allowed.
    for p in build_payloads(_manifest()):
        neg = negotiate(p, FakeSessionAdapter().capabilities())
        assert neg["adapter_supported_action_types"] is None
        assert neg["action_supported"] is True


# --- full negotiation slice ------------------------------------------------
def test_negotiate_payloads_accepts_and_drives_reversible_ops():
    res = negotiate_payloads(_manifest(), FakeSessionAdapter(), clock=_counter_clock())
    assert res["ok"] is True and res["negotiated"] is True
    assert res["counts"]["payloads"] == 2 and res["counts"]["accepted"] == 2
    assert res["counts"]["refused"] == 0 and res["counts"]["reversible"] == 2
    assert res["operations_driven"] is True
    assert res["all_accepted_reversible"] is True
    for p in res["payloads"]:
        assert p["negotiation"]["accepted"] is True
        assert p["operation"]["driven"] is True
        assert p["operation"]["reversible_through_adapter"] is True


def test_negotiate_payloads_is_inert():
    res = negotiate_payloads(_manifest(), clock=_counter_clock())
    assert assert_inert(res) is True
    assert res["no_real_daw"] is True
    assert res["real_applied"] is False and res["real_executed"] is False
    assert res["touched_real_logic"] is False
    assert res["environment"] == "typed_payload_negotiation"


def test_reuses_adapter_target_resolution():
    m = _manifest()
    adapter = FakeSessionAdapter()
    res = negotiate_payloads(m, adapter, clock=_counter_clock())
    step_by_id = {s["step_id"]: s for s in m["eligible_for_future_apply"]}
    for p in res["payloads"]:
        assert p["resolved_target_id"] == adapter.resolve_target(step_by_id[p["step_id"]], m)


class _NoRollbackAdapter(FakeSessionAdapter):
    def capabilities(self):
        c = dict(super().capabilities())
        c["supports_rollback"] = False
        return c


def test_only_accepted_payloads_are_driven():
    # An adapter that cannot roll back fails negotiation for every reversible
    # payload, so NOTHING is driven.
    res = negotiate_payloads(_manifest(), _NoRollbackAdapter(), clock=_counter_clock())
    assert res["counts"]["accepted"] == 0 and res["counts"]["refused"] == 2
    assert res["operations_driven"] is False
    for p in res["payloads"]:
        assert p["negotiation"]["accepted"] is False
        assert p["operation"]["driven"] is False
        assert "refused by capability negotiation" in p["operation"]["reason"]


class _SendOnlyAdapter(FakeSessionAdapter):
    def capabilities(self):
        c = dict(super().capabilities())
        c["supported_action_types"] = ["set_send"]
        return c


def test_partial_support_drives_only_accepted_payloads():
    # The adapter supports only set_send, so the EQ payload is refused and never
    # driven, while the send payload is accepted and reversibly driven.
    res = negotiate_payloads(_manifest(), _SendOnlyAdapter(), clock=_counter_clock())
    assert res["counts"]["accepted"] == 1 and res["counts"]["refused"] == 1
    assert res["operations_driven"] is True
    accepted = [p for p in res["payloads"] if p["negotiation"]["accepted"]]
    refused = [p for p in res["payloads"] if not p["negotiation"]["accepted"]]
    assert accepted[0]["action_type"] == "set_send"
    assert accepted[0]["operation"]["driven"] is True
    assert accepted[0]["operation"]["reversible_through_adapter"] is True
    assert refused[0]["action_type"] == "insert_plugin"
    assert refused[0]["operation"]["driven"] is False
    assert res["all_accepted_reversible"] is True


class _RealishAdapter(FakeSessionAdapter):
    def capabilities(self):
        c = dict(super().capabilities())
        c["real_daw"] = True
        c["supports_real_apply"] = True
        c["allowed_authority_classes"] = ["simulated_only", "real_apply"]
        return c


def test_real_capable_adapter_never_drives_operations():
    # Even if negotiation would admit the payloads, a real-capable adapter must
    # never have an operation driven in this environment.
    res = negotiate_payloads(_manifest(), _RealishAdapter(), clock=_counter_clock())
    assert res["operations_driven"] is False
    assert res["all_accepted_reversible"] is None
    assert all(p["operation"]["driven"] is False for p in res["payloads"])
    assert any("real-capable adapter" in p["operation"]["reason"]
              for p in res["payloads"] if p["negotiation"]["accepted"])
    # the no-real-world guarantee still holds
    assert assert_inert(res) is True


def test_refuses_invalid_manifest():
    m = _manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"          # break the integrity hash
    res = negotiate_payloads(m, clock=_counter_clock())
    assert res["ok"] is False and res["negotiated"] is False
    assert res["payloads"] == [] and res["accepted"] == [] and res["refused"] == []
    assert res["operations_driven"] is False
    assert "invalid manifest" in res["reason"]


def test_audits_to_hash_chained_ledger(tmp_path):
    ledger_path = str(tmp_path / "governance_ledger.jsonl")
    res = negotiate_payloads(_manifest(), ledger_path=ledger_path,
                             actor="alice", clock=_counter_clock())
    audit = res["audit"]
    assert audit["ledger_status"] == "persisted"
    assert audit["ledger_event_id"]
    assert audit["ledger_verification"]["ok"] is True
    # the event is really on the hash-chained ledger and verifies independently
    reloaded = GovernanceLedger(ledger_path)
    assert reloaded.verify()["ok"] is True
    assert reloaded.entries()[-1]["event_type"] == "payload_negotiation_recorded"


def test_invalid_manifest_audits_a_refusal(tmp_path):
    ledger_path = str(tmp_path / "governance_ledger.jsonl")
    m = _manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    res = negotiate_payloads(m, ledger_path=ledger_path, clock=_counter_clock())
    assert res["audit"]["ledger_event_id"]
    assert GovernanceLedger(ledger_path).entries()[-1]["event_type"] == "payload_negotiation_refused"


def test_full_negotiation_is_deterministic():
    m = _manifest()
    a = negotiate_payloads(m, clock=_counter_clock())
    b = negotiate_payloads(m, clock=_counter_clock())
    # drop the audit block (timestamps differ only if persisted; here both not_persisted)
    a.pop("audit"), b.pop("audit")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
