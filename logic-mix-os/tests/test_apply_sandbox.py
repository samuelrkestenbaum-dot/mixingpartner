"""Packet 9, Layer 1 — in-memory simulated Logic sandbox."""

from __future__ import annotations

import copy
import json

from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.apply_sandbox import (
    EVENT_RECORDED,
    EVENT_REFUSED,
    build_fake_session,
    simulate_apply,
)
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",   # approve -> eligible (send)
        "High-pass supporting bus ~250 Hz",          # approve -> eligible (plugin)
        "Ride lead vocal +1 dB into the chorus",     # reject -> excluded
        "Delete source audio in place to bake the loop chop",  # blocked
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-05-01T00:00:{n['i']:02d}+00:00"

    return clock


def _valid_manifest(ledger_path=None):
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "approve", actor="alice")
    wf.decide(review[2], "reject", actor="alice", reason="not now")
    return build_change_manifest(packet, wf.state(), ledger_path=ledger_path)


def test_fake_session_builds_from_manifest():
    s = build_fake_session(_valid_manifest())
    assert s["is_fake"] is True and s["real_logic"] is False
    assert s["environment"] == "simulated_sandbox"
    # one fake target per eligible step
    total = sum(len(s[b]) for b in ("fake_sends", "fake_plugin_slots", "fake_automation_lanes",
                                    "fake_region_edits", "fake_parameters"))
    assert total == 2


def test_fake_session_is_deterministic():
    m = _valid_manifest()
    assert build_fake_session(m) == build_fake_session(m)


def test_valid_manifest_simulates_eligible_only():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert res["ok"] is True and res["simulated"] is True
    assert res["counts"]["eligible"] == 2 and res["counts"]["changed"] == 2
    # every changed target maps back to an eligible step
    assert set(res["changed_targets"]) == set(res["eligible_target_ids"])


def test_excluded_and_blocked_not_simulated():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert res["excluded_blocked_untouched"] is True
    changed = set(res["changed_targets"])
    assert not (changed & set(res["excluded_target_ids"]))
    assert not (changed & set(res["blocked_target_ids"]))
    assert res["excluded_target_ids"] and res["blocked_target_ids"]  # they exist, just untouched


def test_before_after_diff_is_produced():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert len(res["diff"]) == 2
    for d in res["diff"]:
        assert d["before"] == {"configured": False}
        assert d["after"]["configured"] is True
        assert {"step_id", "target_id", "planned_action", "before", "after", "rollback"} <= set(d)


def test_changed_targets_are_deterministic():
    m = _valid_manifest()
    a = simulate_apply(m, clock=_counter_clock())
    b = simulate_apply(m, clock=_counter_clock())
    assert a["changed_targets"] == b["changed_targets"]
    assert [d["target_id"] for d in a["diff"]] == [d["target_id"] for d in b["diff"]]


def test_rollback_restores_exactly():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert res["rollback_restored"] is True
    assert res["rollback"]["rolled_back_session"] == res["before"]
    assert res["after"] != res["before"]   # something did change in the fake world


def test_successful_simulation_has_all_no_real_world_flags():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert res["real_applied"] is False and res["real_executed"] is False
    assert res["touched_real_logic"] is False and res["no_real_daw"] is True
    assert res["environment"] == "simulated_sandbox"


def test_successful_simulation_appends_recorded_with_ledger(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    res = simulate_apply(_valid_manifest(), ledger_path=path, clock=_counter_clock())
    lines = [json.loads(l) for l in open(path)]
    assert lines[-1]["event_type"] == EVENT_RECORDED
    assert res["audit"]["ledger_status"] == "persisted"
    assert res["audit"]["ledger_verification"]["ok"] is True


def test_no_ledger_reports_not_persisted():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    assert res["audit"]["ledger_status"] == "not_persisted"
    assert res["audit"]["ledger_event_id"] is None


def test_recorded_chains_onto_manifest_ledger(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    m = _valid_manifest(ledger_path=path)        # appends manifest_emitted
    simulate_apply(m, ledger_path=path, clock=_counter_clock())
    types = [json.loads(l)["event_type"] for l in open(path)]
    assert types == ["manifest_emitted", "simulated_apply_recorded"]


def test_invalid_manifest_returns_refused(tmp_path):
    m = _valid_manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    path = str(tmp_path / "governance_ledger.jsonl")
    res = simulate_apply(m, ledger_path=path, clock=_counter_clock())
    assert res["ok"] is False and res["simulated"] is False
    assert [json.loads(l) for l in open(path)][-1]["event_type"] == EVENT_REFUSED


def test_invalid_manifest_produces_no_after_state():
    m = _valid_manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    res = simulate_apply(m, clock=_counter_clock())
    assert res["before"] is None and res["after"] is None
    assert res["diff"] == [] and res["changed_targets"] == []
    # still carries the safe flags
    assert res["no_real_daw"] is True and res["touched_real_logic"] is False


def test_executable_payload_manifest_refuses():
    m = _valid_manifest()
    m["no_apply_guarantee"]["can_execute"] = True
    res = simulate_apply(m, clock=_counter_clock())
    assert res["ok"] is False and res["after"] is None


def test_eligible_applied_manifest_refuses():
    m = _valid_manifest()
    m["eligible_for_future_apply"][0]["applied"] = True
    res = simulate_apply(m, clock=_counter_clock())
    assert res["ok"] is False and res["after"] is None


def test_blocked_in_eligible_manifest_refuses():
    m = _valid_manifest()
    m["eligible_for_future_apply"].append(dict(m["blocked"][0]))
    res = simulate_apply(m, clock=_counter_clock())
    assert res["ok"] is False and res["after"] is None
