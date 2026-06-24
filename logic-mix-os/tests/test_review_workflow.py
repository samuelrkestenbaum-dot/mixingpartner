"""Packet 6, Layer 1 — operator review → decision workflow."""

from __future__ import annotations

import json

import pytest

from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import (
    APPROVED_FUTURE,
    DECISIONS_BANNER,
    ReviewWorkflow,
    load_review_packet,
    workflow_from_artifacts,
)

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus by blooming supporting elements.",
    "expected_strength": "emotional openness", "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB at chorus entry",   # Class 3 review
        "High-pass supporting bus ~250 Hz",                          # Class 3 review
        "Mute decorative texture in the final pre-chorus bar",       # Class 3 review
        "Delete source audio in place to bake the loop chop",        # Class 5 blocked
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-02-01T00:00:{n['i']:02d}+00:00"

    return clock


def _packet():
    return build_review_packet(plan_logic_actions(VARIANT))


def _review_step(packet):
    return next(s["step_id"] for s in packet["steps"] if s["decision"] == "review_required")


def _blocked_step(packet):
    return next(s["step_id"] for s in packet["steps"] if s["decision"] == "blocked")


def test_review_packet_loads_correctly(tmp_path):
    packet = _packet()
    p = tmp_path / "operator_review_packet.json"
    p.write_text(json.dumps(packet))
    loaded = load_review_packet(str(p))
    assert loaded["plan_id"] == packet["plan_id"]
    wf = ReviewWorkflow(loaded)
    assert wf.plan_id == packet["plan_id"]


def test_approve_creates_decision_receipt():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    d = wf.decide(_review_step(packet), "approve", actor="alice")
    assert d["decision_id"].startswith("dec_")
    assert d["decision"] == "approve" and d["actor"] == "alice"
    assert d["receipt_id"] and d["timestamp"]


def test_class3_approval_does_not_apply():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    d = wf.decide(_review_step(packet), "approve", actor="alice")
    assert d["resulting_state"] == APPROVED_FUTURE
    assert d["applied"] is False
    assert d["must_not_execute_here"] is True
    assert wf.state()["nothing_applied"] is True


def test_reject_requires_reason():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    with pytest.raises(ValueError, match="reason is required"):
        wf.decide(_review_step(packet), "reject", actor="alice")
    d = wf.decide(_review_step(packet), "reject", actor="alice", reason="too washed")
    assert d["resulting_state"] == "rejected" and d["reason"] == "too washed"


def test_request_revision_requires_reason():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    with pytest.raises(ValueError, match="reason is required"):
        wf.decide(_review_step(packet), "request_revision", actor="bob")
    d = wf.decide(_review_step(packet), "request_revision", actor="bob", reason="try -2 dB instead")
    assert d["resulting_state"] == "revision_requested"


def test_defer_records_deferred_state():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    d = wf.decide(_review_step(packet), "defer", actor="alice")
    assert d["resulting_state"] == "deferred" and d["applied"] is False


def test_blocked_steps_cannot_be_approved():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    with pytest.raises(ValueError, match="blocked"):
        wf.decide(_blocked_step(packet), "approve", actor="alice")
    # but a blocked step may still be rejected/deferred by the operator
    assert wf.decide(_blocked_step(packet), "reject", actor="alice", reason="agree, destructive")["resulting_state"] == "rejected"


def test_apply_attempts_are_refused():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    for word in ("apply", "applied", "mark_applied", "execute"):
        with pytest.raises(ValueError, match="applying is not permitted"):
            wf.decide(_review_step(packet), word, actor="alice")


def test_missing_actor_and_unknown_step_are_rejected():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    with pytest.raises(ValueError, match="actor"):
        wf.decide(_review_step(packet), "approve", actor="")
    with pytest.raises(ValueError, match="unknown step_id"):
        wf.decide("no_such_step", "approve", actor="alice")


def test_original_review_packet_not_mutated():
    packet = _packet()
    before = json.dumps(packet, sort_keys=True)
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(_review_step(packet), "approve", actor="alice")
    wf.decide(_blocked_step(packet), "reject", actor="alice", reason="destructive")
    assert json.dumps(packet, sort_keys=True) == before  # packet untouched


def test_decision_state_writes_as_separate_artifact(tmp_path):
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(_review_step(packet), "approve", actor="alice")
    path = wf.save_json(str(tmp_path / "dec"))
    assert path.endswith("operator_decisions.json")
    state = json.loads(open(path).read())
    assert state["banner"] == DECISIONS_BANNER
    assert state["plan_id"] == packet["plan_id"] and state["decisions"]


def test_every_decision_appends_to_audit_ledger(tmp_path):
    packet = _packet()
    path = str(tmp_path / "governance_ledger.jsonl")
    wf = ReviewWorkflow(packet, ledger_path=path, clock=_counter_clock())
    rs = _review_step(packet)
    wf.decide(rs, "approve", actor="alice")
    wf.decide(_blocked_step(packet), "reject", actor="alice", reason="destructive")
    lines = [json.loads(l) for l in open(path)]
    assert [e["event_type"] for e in lines] == ["operator_approve", "operator_reject"]
    assert wf.verify_ledger()["ok"] is True


def test_fresh_reload_reconstructs_decision_state(tmp_path):
    packet = _packet()
    ppath = tmp_path / "operator_review_packet.json"
    ppath.write_text(json.dumps(packet))
    ledger = str(tmp_path / "governance_ledger.jsonl")

    wf1 = ReviewWorkflow(packet, ledger_path=ledger, clock=_counter_clock())
    rs = _review_step(packet)
    wf1.decide(rs, "approve", actor="alice")
    dpath = wf1.save_json(str(tmp_path / "dec"))

    # Fresh workflow from artifacts continues where it left off.
    wf2 = workflow_from_artifacts(str(ppath), decisions_path=dpath,
                                  ledger_path=ledger, clock=_counter_clock())
    assert len(wf2.decisions()) == 1
    wf2.decide(_blocked_step(packet), "defer", actor="bob")
    assert wf2.summarize_decisions()["decisions_recorded"] == 2
    assert wf2.verify_ledger()["ok"] is True


def test_summary_counts_each_decision_kind():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    steps = [s["step_id"] for s in packet["steps"]]
    wf.decide(steps[0], "approve", actor="a")
    wf.decide(steps[1], "reject", actor="a", reason="no")
    wf.decide(steps[2], "request_revision", actor="a", reason="tweak")
    summ = wf.summarize_decisions()
    assert summ["approved"] == 1 and summ["rejected"] == 1 and summ["revision_requested"] == 1
    assert summ["pending"] == len(steps) - 3
    assert summ["blocked"] >= 1


def test_plan_level_approve_all_allowed_skips_blocked():
    packet = _packet()
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    decided = wf.approve_all_allowed(actor="alice")
    blocked_ids = {s["step_id"] for s in packet["steps"] if s["decision"] == "blocked"}
    approved_ids = {d["step_id"] for d in decided}
    assert approved_ids and not (approved_ids & blocked_ids)  # no blocked step approved
    assert all(d["applied"] is False for d in decided)
