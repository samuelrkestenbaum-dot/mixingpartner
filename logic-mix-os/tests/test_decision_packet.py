"""Packet 6, Layer 2 — decision packet renderer + review-decision CLI."""

from __future__ import annotations

import json

import pytest

from logic_mix_os.cli import build_parser
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.decision_packet import render_decisions_markdown
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus by blooming supporting elements.",
    "expected_strength": "emotional openness", "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB at chorus entry",
        "High-pass supporting bus ~250 Hz",
        "Delete source audio in place to bake the loop chop",  # Class 5 blocked
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-02-01T00:00:{n['i']:02d}+00:00"

    return clock


def _write_packet(tmp_path):
    packet = build_review_packet(plan_logic_actions(VARIANT))
    p = tmp_path / "operator_review_packet.json"
    p.write_text(json.dumps(packet))
    review = next(s["step_id"] for s in packet["steps"] if s["decision"] == "review_required")
    blocked = next(s["step_id"] for s in packet["steps"] if s["decision"] == "blocked")
    return str(p), review, blocked, packet


# --- renderer -------------------------------------------------------------
def test_markdown_has_banner_table_receipts_reasons_and_ledger(tmp_path):
    _, review, blocked, packet = _write_packet(tmp_path)
    wf = ReviewWorkflow(packet, ledger_path=str(tmp_path / "governance_ledger.jsonl"),
                        clock=_counter_clock())
    wf.decide(review, "approve", actor="alice")
    wf.decide(blocked, "reject", actor="alice", reason="destructive — never")
    md = render_decisions_markdown(wf.state())
    assert "DECISIONS RECORDED — NOTHING APPLIED" in md
    assert "## Decisions" in md and "| Step | Decision |" in md
    assert "Approval receipts" in md and "approved_for_future_apply_when_a_real_logic_surface_exists" in md
    assert "destructive — never" in md           # rejection reason surfaced
    assert "integrity:" in md                     # ledger integrity shown


# --- CLI ------------------------------------------------------------------
def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_approves_review_step_without_applying(tmp_path, capsys):
    ppath, review, _, _ = _write_packet(tmp_path)
    out = tmp_path / "dec"
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", review,
                   "--decision", "approve", "--actor", "alice", "--out", str(out)])
    assert rc == 0
    state = json.loads((out / "operator_decisions.json").read_text())
    assert state["nothing_applied"] is True
    d = state["decisions"][0]
    assert d["resulting_state"] == "approved_for_future_apply_when_a_real_logic_surface_exists"
    assert d["applied"] is False
    assert "NOTHING APPLIED" in capsys.readouterr().out


def test_cli_writes_json_and_markdown(tmp_path):
    ppath, review, _, _ = _write_packet(tmp_path)
    out = tmp_path / "dec"
    _run_cli(["review-decision", "--packet", ppath, "--step-id", review,
              "--decision", "defer", "--actor", "bob", "--out", str(out)])
    assert (out / "operator_decisions.json").exists()
    assert (out / "operator_decisions.md").exists()


def test_cli_rejects_blocked_step_approval(tmp_path, capsys):
    ppath, _, blocked, _ = _write_packet(tmp_path)
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", blocked,
                   "--decision", "approve", "--actor", "alice", "--out", str(tmp_path / "d")])
    assert rc == 1
    assert "blocked" in capsys.readouterr().out.lower()


def test_cli_requires_reason_for_reject(tmp_path, capsys):
    ppath, review, _, _ = _write_packet(tmp_path)
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", review,
                   "--decision", "reject", "--actor", "alice", "--out", str(tmp_path / "d")])
    assert rc == 1
    assert "reason" in capsys.readouterr().out.lower()


def test_cli_appends_ledger_events(tmp_path):
    ppath, review, _, _ = _write_packet(tmp_path)
    ledger = tmp_path / "governance_ledger.jsonl"
    _run_cli(["review-decision", "--packet", ppath, "--step-id", review, "--decision", "approve",
              "--actor", "alice", "--ledger", str(ledger), "--out", str(tmp_path / "d")])
    lines = [json.loads(l) for l in open(ledger)]
    assert lines and lines[0]["event_type"] == "operator_approve"


def test_cli_reloads_and_appends(tmp_path, capsys):
    ppath, review, blocked, _ = _write_packet(tmp_path)
    out = tmp_path / "dec"
    ledger = tmp_path / "governance_ledger.jsonl"
    _run_cli(["review-decision", "--packet", ppath, "--step-id", review, "--decision", "approve",
              "--actor", "alice", "--ledger", str(ledger), "--out", str(out)])
    # Second run on the same --out reloads and appends a second decision.
    _run_cli(["review-decision", "--packet", ppath, "--step-id", blocked, "--decision", "defer",
              "--actor", "bob", "--ledger", str(ledger), "--out", str(out)])
    state = json.loads((out / "operator_decisions.json").read_text())
    assert state["summary"]["decisions_recorded"] == 2
    assert state["ledger_verification"]["ok"] is True


def test_cli_rejects_missing_actor(tmp_path, capsys):
    ppath, review, _, _ = _write_packet(tmp_path)
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", review,
                   "--decision", "approve", "--out", str(tmp_path / "d")])
    assert rc == 1
    assert "actor" in capsys.readouterr().out.lower()


def test_cli_rejects_unknown_step(tmp_path, capsys):
    ppath, _, _, _ = _write_packet(tmp_path)
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", "nope",
                   "--decision", "approve", "--actor", "alice", "--out", str(tmp_path / "d")])
    assert rc == 1
    assert "unknown step" in capsys.readouterr().out.lower()


def test_cli_cannot_mark_applied(tmp_path):
    ppath, review, _, _ = _write_packet(tmp_path)
    # argparse restricts --decision to the four; "apply" is not selectable.
    with pytest.raises(SystemExit):
        build_parser().parse_args(["review-decision", "--packet", ppath, "--step-id", review,
                                   "--decision", "apply", "--actor", "alice"])


def test_cli_rejects_conflicting_actions(tmp_path, capsys):
    ppath, review, _, _ = _write_packet(tmp_path)
    rc = _run_cli(["review-decision", "--packet", ppath, "--step-id", review, "--decision", "approve",
                   "--approve-all-allowed", "--actor", "alice", "--out", str(tmp_path / "d")])
    assert rc == 1
    assert "exactly one action" in capsys.readouterr().out.lower()


def test_cli_approve_all_allowed_skips_blocked(tmp_path):
    ppath, _, _, packet = _write_packet(tmp_path)
    out = tmp_path / "dec"
    _run_cli(["review-decision", "--packet", ppath, "--approve-all-allowed",
              "--actor", "alice", "--out", str(out)])
    state = json.loads((out / "operator_decisions.json").read_text())
    n_blocked = sum(1 for s in packet["steps"] if s["decision"] == "blocked")
    assert state["summary"]["approved"] == len(packet["steps"]) - n_blocked
