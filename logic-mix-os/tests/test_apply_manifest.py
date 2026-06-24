"""Packet 7, Layer 1 — pre-apply Logic change manifest builder."""

from __future__ import annotations

import copy
import json

import pytest

from logic_mix_os.apply_manifest import (
    MANIFEST_BANNER,
    ManifestError,
    build_change_manifest,
    manifest_hash,
    validate_manifest,
)
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus by blooming supporting elements.",
    "expected_strength": "emotional openness", "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB at chorus entry",   # review (set_send)
        "High-pass supporting bus ~250 Hz",                          # review (insert_plugin)
        "Ride lead vocal +1 dB into the chorus",                     # review (automation)
        "Mute decorative texture in the final pre-chorus bar",       # review (arrangement)
        "Delete source audio in place to bake the loop chop",        # blocked (Class 5)
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-03-01T00:00:{n['i']:02d}+00:00"

    return clock


def _scenario():
    """approve s0, reject s1, defer s2, leave s3 pending; s4 is blocked."""
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    blocked = next(s["step_id"] for s in packet["steps"] if s["decision"] == "blocked")
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "reject", actor="alice", reason="too washed")
    wf.decide(review[2], "request_revision", actor="bob", reason="try -2 dB")
    # review[3] left pending
    return packet, wf.state(), review, blocked


def test_manifest_builds_from_packet_and_decisions():
    packet, state, _, _ = _scenario()
    m = build_change_manifest(packet, state)
    assert m["banner"] == MANIFEST_BANNER
    assert m["plan_id"] == packet["plan_id"]
    assert m["manifest_hash"] and m["manifest_id"].startswith("man_")
    assert m["no_apply_guarantee"]["can_execute"] is False
    assert m["no_apply_guarantee"]["nothing_applied"] is True


def test_partition_eligible_excluded_blocked():
    packet, state, review, blocked = _scenario()
    m = build_change_manifest(packet, state)
    elig = {s["step_id"] for s in m["eligible_for_future_apply"]}
    exc = {s["step_id"]: s for s in m["excluded"]}
    blk = {s["step_id"] for s in m["blocked"]}
    assert elig == {review[0]}                                  # only the approved step
    assert exc[review[1]]["status"] == "rejected"
    assert exc[review[2]]["status"] == "revision_requested"
    assert exc[review[3]]["status"] == "pending"                # no decision
    assert blocked in blk and blocked not in elig               # blocked never eligible


def test_eligible_step_carries_required_fields():
    packet, state, review, _ = _scenario()
    m = build_change_manifest(packet, state)
    s = m["eligible_for_future_apply"][0]
    for f in ("step_id", "planned_logic_action", "authority_class", "receipt_id", "decision_id",
              "rollback_plan", "evidence", "approver", "timestamp"):
        assert s.get(f), f"missing {f}"
    assert s["must_not_execute_here"] is True and s["applied"] is False


def test_blocked_step_marked_not_eligible():
    packet, state, _, blocked = _scenario()
    m = build_change_manifest(packet, state)
    b = next(s for s in m["blocked"] if s["step_id"] == blocked)
    assert b["eligible"] is False and b["authority_class"] == 5


def test_mismatched_plan_id_refuses():
    packet, state, _, _ = _scenario()
    state2 = copy.deepcopy(state)
    state2["plan_id"] = "plan_other"
    with pytest.raises(ManifestError, match="plan_id mismatch"):
        build_change_manifest(packet, state2)


def test_mismatched_receipt_refuses():
    packet, state, review, _ = _scenario()
    state2 = copy.deepcopy(state)
    for d in state2["decisions"]:
        if d["step_id"] == review[0]:
            d["receipt_id"] = "rcpt_tampered"
    with pytest.raises(ManifestError, match="receipt_id mismatch"):
        build_change_manifest(packet, state2)


def test_unknown_step_in_approval_refuses():
    packet, state, _, _ = _scenario()
    state2 = copy.deepcopy(state)
    state2["decisions"].append({"step_id": "ghost", "decision": "approve", "actor": "x",
                                "receipt_id": "rcpt_x", "decision_id": "dec_x"})
    with pytest.raises(ManifestError, match="unknown step_id"):
        build_change_manifest(packet, state2)


def test_applied_eligible_step_refuses():
    packet, state, review, _ = _scenario()
    packet2 = copy.deepcopy(packet)
    for s in packet2["steps"]:
        if s["step_id"] == review[0]:
            s["applied"] = True
    with pytest.raises(ManifestError, match="applied:true"):
        build_change_manifest(packet2, state)


def test_missing_must_not_execute_refuses():
    packet, state, review, _ = _scenario()
    packet2 = copy.deepcopy(packet)
    for s in packet2["steps"]:
        if s["step_id"] == review[0]:
            s["must_not_execute_here"] = False
    with pytest.raises(ManifestError, match="must_not_execute_here"):
        build_change_manifest(packet2, state)


def test_missing_actor_on_approval_refuses():
    packet, state, review, _ = _scenario()
    state2 = copy.deepcopy(state)
    for d in state2["decisions"]:
        if d["step_id"] == review[0]:
            d["actor"] = ""
    with pytest.raises(ManifestError, match="missing an actor"):
        build_change_manifest(packet, state2)


def test_malformed_decision_state_refuses():
    packet, _, _, _ = _scenario()
    with pytest.raises(ManifestError, match="malformed decision state"):
        build_change_manifest(packet, {"plan_id": packet["plan_id"]})


def test_hash_is_deterministic():
    packet, state, _, _ = _scenario()
    h1 = build_change_manifest(packet, state)["manifest_hash"]
    h2 = build_change_manifest(packet, state)["manifest_hash"]
    assert h1 == h2


def test_hash_changes_when_eligible_set_changes():
    packet, state, review, _ = _scenario()
    base = build_change_manifest(packet, state)["manifest_hash"]
    # additionally approve the pending step -> eligible set grows
    wf = ReviewWorkflow(packet, decisions=copy.deepcopy(state["decisions"]), clock=_counter_clock())
    wf.decide(review[3], "approve", actor="alice")
    changed = build_change_manifest(packet, wf.state())["manifest_hash"]
    assert base != changed


def test_hash_changes_when_excluded_set_changes():
    packet, state, review, _ = _scenario()
    base = build_change_manifest(packet, state)["manifest_hash"]
    state2 = copy.deepcopy(state)
    for d in state2["decisions"]:
        if d["step_id"] == review[1]:
            d["reason"] = "completely different reason"
    assert build_change_manifest(packet, state2)["manifest_hash"] != base


def test_hash_changes_when_rollback_content_changes():
    packet, state, review, _ = _scenario()
    base = build_change_manifest(packet, state)["manifest_hash"]
    packet2 = copy.deepcopy(packet)
    for s in packet2["steps"]:
        if s["step_id"] == review[0]:
            s["rollback_summary"] = "a totally different rollback plan"
    assert build_change_manifest(packet2, state)["manifest_hash"] != base


def test_validation_passes_on_clean_manifest():
    packet, state, _, _ = _scenario()
    m = build_change_manifest(packet, state)
    assert validate_manifest(m)["ok"] is True


def test_validation_fails_on_tampered_manifest():
    packet, state, _, _ = _scenario()
    m = build_change_manifest(packet, state)
    m["eligible_for_future_apply"][0]["rollback_plan"] = "tampered"   # hash now stale
    res = validate_manifest(m)
    assert res["ok"] is False and any("manifest_hash" in e for e in res["errors"])
    m2 = build_change_manifest(packet, state)
    m2["eligible_for_future_apply"][0]["applied"] = True
    assert validate_manifest(m2)["ok"] is False


def test_manifest_emitted_event_appends_when_ledger_given(tmp_path):
    packet, state, _, _ = _scenario()
    path = str(tmp_path / "governance_ledger.jsonl")
    m = build_change_manifest(packet, state, ledger_path=path)
    assert m["ledger_status"] == "persisted"
    lines = [json.loads(l) for l in open(path)]
    assert lines[-1]["event_type"] == "manifest_emitted"
    assert m["manifest_emitted_event_id"] == lines[-1]["event_id"]
    assert m["ledger_verification"]["ok"] is True


def test_no_ledger_mode_reports_not_persisted():
    packet, state, _, _ = _scenario()
    m = build_change_manifest(packet, state)
    assert m["ledger_status"] == "not_persisted"
    assert m["ledger_verification"] is None
    assert m["manifest_emitted_event_id"] is None


def test_manifest_emitted_chains_onto_existing_ledger(tmp_path):
    """Emitting onto a ledger that already has decision events keeps it verifying."""
    packet, _, review, _ = _scenario()
    path = str(tmp_path / "governance_ledger.jsonl")
    wf = ReviewWorkflow(packet, ledger_path=path, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    m = build_change_manifest(packet, wf.state(), ledger_path=path)
    assert m["ledger_verification"]["ok"] is True
    types = [json.loads(l)["event_type"] for l in open(path)]
    assert types == ["operator_approve", "manifest_emitted"]
