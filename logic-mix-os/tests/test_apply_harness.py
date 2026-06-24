"""Packet 8, Layer 1 — manifest consumer contract + apply-harness stub."""

from __future__ import annotations

import copy
import json

from logic_mix_os.apply_harness import (
    NOT_READY_BLOCKED_ONLY,
    NOT_READY_INVALID,
    NOT_READY_NO_ELIGIBLE,
    READY,
    REFUSED_ENV,
    build_apply_readiness_report,
    load_change_manifest,
    refuse_apply,
    validate_manifest_for_harness,
)
from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",   # review -> approve -> eligible
        "High-pass supporting bus ~250 Hz",          # review -> reject -> excluded
        "Delete source audio in place to bake the loop chop",  # blocked
    ],
}
BLOCKED_ONLY = {
    "variant_id": "destructive_only", "kind": "subtractive_drop",
    "tracks_affected": ["Loop"], "changes": ["Delete source audio in place"],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-04-01T00:00:{n['i']:02d}+00:00"

    return clock


def _valid_manifest(ledger_path=None):
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "reject", actor="alice", reason="too washed")
    return build_change_manifest(packet, wf.state(), ledger_path=ledger_path)


def test_valid_manifest_loads(tmp_path):
    m = _valid_manifest()
    p = tmp_path / "change_manifest.json"
    p.write_text(json.dumps(m))
    loaded = load_change_manifest(str(p))
    assert loaded["manifest_hash"] == m["manifest_hash"]


def test_valid_manifest_validates_for_harness():
    assert validate_manifest_for_harness(_valid_manifest())["ok"] is True


def test_readiness_report_is_produced():
    r = build_apply_readiness_report(_valid_manifest())
    assert r["readiness_status"] == READY
    for k in ("manifest_id", "manifest_hash", "plan_id", "eligible_count", "excluded_count",
              "blocked_count", "ledger_status", "validation_status", "no_apply_guarantee_status"):
        assert k in r
    assert r["eligible_count"] == 1 and r["blocked_count"] == 1
    assert r["apply_permitted_here"] is False


def test_ready_manifest_still_refuses_apply():
    m = _valid_manifest()
    assert build_apply_readiness_report(m)["readiness_status"] == READY
    rec = refuse_apply(m, clock=_counter_clock())
    assert rec["ok"] is False and rec["applied"] is False and rec["executed"] is False
    assert rec["authority_boundary"] == "no_real_logic_surface"
    assert rec["readiness_status"] == REFUSED_ENV


def test_refusal_appends_ledger_event(tmp_path):
    m = _valid_manifest()
    path = str(tmp_path / "governance_ledger.jsonl")
    rec = refuse_apply(m, actor="alice", ledger_path=path, clock=_counter_clock())
    lines = [json.loads(l) for l in open(path)]
    assert lines[-1]["event_type"] == "apply_harness_refused"
    assert rec["ledger_status"] == "persisted" and rec["ledger_event_id"]
    assert rec["ledger_verification"]["ok"] is True


def test_no_ledger_refusal_reports_not_persisted():
    rec = refuse_apply(_valid_manifest(), clock=_counter_clock())
    assert rec["ledger_status"] == "not_persisted"
    assert rec["ledger_event_id"] is None and rec["ledger_verification"] is None


def test_refusal_chains_onto_manifest_ledger(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    m = _valid_manifest(ledger_path=path)            # appends manifest_emitted
    refuse_apply(m, ledger_path=path, clock=_counter_clock())
    types = [json.loads(l)["event_type"] for l in open(path)]
    assert types == ["manifest_emitted", "apply_harness_refused"]


def test_invalid_hash_refuses():
    m = _valid_manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    v = validate_manifest_for_harness(m)
    assert v["ok"] is False
    assert build_apply_readiness_report(m)["readiness_status"] == NOT_READY_INVALID


def test_missing_no_apply_guarantee_refuses():
    m = _valid_manifest()
    del m["no_apply_guarantee"]
    assert validate_manifest_for_harness(m)["ok"] is False
    assert build_apply_readiness_report(m)["readiness_status"] == NOT_READY_INVALID


def test_contains_apply_payload_true_refuses():
    m = _valid_manifest()
    m["no_apply_guarantee"]["contains_apply_payload"] = True
    v = validate_manifest_for_harness(m)
    assert v["ok"] is False
    assert any("contains_apply_payload" in e for e in v["errors"])


def test_can_execute_true_refuses():
    m = _valid_manifest()
    m["no_apply_guarantee"]["can_execute"] = True
    v = validate_manifest_for_harness(m)
    assert v["ok"] is False
    assert any("can_execute" in e for e in v["errors"])


def test_eligible_applied_true_refuses():
    m = _valid_manifest()
    m["eligible_for_future_apply"][0]["applied"] = True
    assert validate_manifest_for_harness(m)["ok"] is False


def test_eligible_missing_must_not_execute_refuses():
    m = _valid_manifest()
    m["eligible_for_future_apply"][0]["must_not_execute_here"] = False
    assert validate_manifest_for_harness(m)["ok"] is False


def test_blocked_step_in_eligible_refuses():
    m = _valid_manifest()
    m["eligible_for_future_apply"].append(dict(m["blocked"][0]))
    v = validate_manifest_for_harness(m)
    assert v["ok"] is False
    assert any("appears as eligible" in e or "eligible" in e for e in v["errors"])


def test_no_eligible_steps_returns_not_ready():
    # reject every review step -> nothing eligible, but excluded > 0
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    for sid in review:
        wf.decide(sid, "reject", actor="a", reason="no")
    m = build_change_manifest(packet, wf.state())
    assert build_apply_readiness_report(m)["readiness_status"] == NOT_READY_NO_ELIGIBLE


def test_blocked_only_manifest_is_not_ready():
    packet = build_review_packet(plan_logic_actions(BLOCKED_ONLY))
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    m = build_change_manifest(packet, wf.state())
    r = build_apply_readiness_report(m)
    assert r["eligible_count"] == 0 and r["blocked_count"] >= 1
    assert r["readiness_status"] == NOT_READY_BLOCKED_ONLY


def test_malformed_manifest_refuses():
    assert validate_manifest_for_harness({})["ok"] is False
    assert build_apply_readiness_report({})["readiness_status"] == NOT_READY_INVALID
    # refuse_apply still returns a refusal even for a malformed manifest
    rec = refuse_apply({}, clock=_counter_clock())
    assert rec["ok"] is False and rec["applied"] is False
