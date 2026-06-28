"""Packet 10, Layer 1 — SessionAdapter contract + FakeSessionAdapter."""

from __future__ import annotations

import pytest

from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.apply_sandbox import build_fake_session, simulate_apply
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow
from logic_mix_os.session_adapter import (
    FakeSessionAdapter,
    RealLogicSessionAdapter,
    SessionAdapter,
)

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",
        "High-pass supporting bus ~250 Hz",
        "Ride lead vocal +1 dB into the chorus",     # reject -> excluded
        "Delete source audio in place to bake the loop chop",  # blocked
    ],
}

CONTRACT = ("adapter_name", "capabilities", "build_initial_session", "resolve_target",
            "apply_step", "diff", "rollback", "verify_rollback", "verify_untouched")


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


def test_fake_adapter_implements_contract():
    fake = FakeSessionAdapter()
    assert isinstance(fake, SessionAdapter)
    for m in CONTRACT:
        assert callable(getattr(fake, m))
    assert fake.adapter_name() == "FakeSessionAdapter"


def test_capabilities_are_explicit_and_non_real():
    caps = FakeSessionAdapter().capabilities()
    assert caps["adapter_type"] == "fake_session"
    assert caps["real_daw"] is False
    assert caps["writes_project_files"] is False
    assert caps["supports_real_apply"] is False
    assert caps["supports_simulated_apply"] is True
    assert caps["supports_rollback"] is True
    assert caps["requires_macos"] is False and caps["requires_logic"] is False
    assert caps["allowed_authority_classes"] == ["simulated_only"]


def test_real_logic_adapter_is_a_non_instantiable_placeholder():
    assert issubclass(RealLogicSessionAdapter, SessionAdapter)
    with pytest.raises(NotImplementedError):
        RealLogicSessionAdapter()


def test_simulation_routes_through_adapter():
    # A spy adapter proves the orchestration calls the adapter rather than owning mechanics.
    calls = []

    class SpyAdapter(FakeSessionAdapter):
        def build_initial_session(self, manifest):
            calls.append("build_initial_session")
            return super().build_initial_session(manifest)

        def apply_step(self, session, step):
            calls.append("apply_step")
            return super().apply_step(session, step)

        def diff(self, before, after):
            calls.append("diff")
            return super().diff(before, after)

        def rollback(self, after, diff):
            calls.append("rollback")
            return super().rollback(after, diff)

        def verify_rollback(self, before, rolled_back):
            calls.append("verify_rollback")
            return super().verify_rollback(before, rolled_back)

        def verify_untouched(self, *a):
            calls.append("verify_untouched")
            return super().verify_untouched(*a)

    res = simulate_apply(_manifest(), adapter=SpyAdapter(), clock=_counter_clock())
    assert res["ok"] is True
    for expected in ("build_initial_session", "apply_step", "diff", "rollback",
                     "verify_rollback", "verify_untouched"):
        assert expected in calls, f"orchestration did not call adapter.{expected}"


def test_adapter_owns_target_id_derivation():
    fake = FakeSessionAdapter()
    m = _manifest()
    step = m["eligible_for_future_apply"][0]
    tid = fake.resolve_target(step, m)
    assert tid.startswith("tgt_")
    # deterministic + owned by the adapter
    assert fake.resolve_target(step, m) == tid


def test_adapter_owns_session_construction_and_diff_and_rollback():
    fake = FakeSessionAdapter()
    m = _manifest()
    before = fake.build_initial_session(m)
    after = fake.build_initial_session(m)
    assert before == after                          # deterministic build
    for s in m["eligible_for_future_apply"]:
        fake.apply_step(after, s)
    diff = fake.diff(before, after)
    assert diff and all(d["before"] == {"configured": False} for d in diff)
    rb = fake.rollback(after, diff)
    assert fake.verify_rollback(before, rb) is True


def test_packet9_behaviour_unchanged_through_adapter():
    res = simulate_apply(_manifest(), clock=_counter_clock())
    assert res["ok"] is True and res["simulated"] is True
    assert res["real_applied"] is False and res["real_executed"] is False
    assert res["touched_real_logic"] is False and res["no_real_daw"] is True
    assert res["environment"] == "simulated_sandbox"
    assert set(res["changed_targets"]) == set(res["eligible_target_ids"])
    assert res["excluded_blocked_untouched"] is True
    assert not (set(res["changed_targets"]) & set(res["excluded_target_ids"]))
    assert not (set(res["changed_targets"]) & set(res["blocked_target_ids"]))
    assert res["rollback_restored"] is True
    # adapter metadata now carried on the result
    assert res["adapter"]["name"] == "FakeSessionAdapter"
    assert res["adapter"]["capabilities"]["real_daw"] is False


def test_deterministic_through_adapter():
    m = _manifest()
    a = simulate_apply(m, clock=_counter_clock())
    b = simulate_apply(m, clock=_counter_clock())
    assert a["changed_targets"] == b["changed_targets"]
    assert [d["target_id"] for d in a["diff"]] == [d["target_id"] for d in b["diff"]]
    assert build_fake_session(m) == build_fake_session(m)


def test_refusal_still_carries_adapter_metadata():
    m = _manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    res = simulate_apply(m, clock=_counter_clock())
    assert res["ok"] is False and res["after"] is None
    assert res["adapter"]["name"] == "FakeSessionAdapter"
