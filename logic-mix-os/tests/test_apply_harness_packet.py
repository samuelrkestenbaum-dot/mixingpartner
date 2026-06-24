"""Packet 8, Layer 2 — apply-harness readiness renderer + CLI."""

from __future__ import annotations

import json

from logic_mix_os.apply_harness import build_apply_readiness_report, refuse_apply
from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.cli import build_parser
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.apply_harness_packet import HARNESS_BANNER, render_readiness_markdown
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",
        "High-pass supporting bus ~250 Hz",
        "Delete source audio in place to bake the loop chop",
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-04-01T00:00:{n['i']:02d}+00:00"

    return clock


def _valid_manifest():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "reject", actor="alice", reason="too washed")
    return build_change_manifest(packet, wf.state())


# --- renderer -------------------------------------------------------------
def test_markdown_has_banner_and_sections():
    m = _valid_manifest()
    md = render_readiness_markdown(build_apply_readiness_report(m), refuse_apply(m, clock=_counter_clock()))
    assert HARNESS_BANNER in md
    assert "Apply decision" in md
    assert "No-apply guarantee" in md
    assert "Future apply boundary" in md
    assert "applied:** `False`" in md and "executed:** `False`" in md


# --- CLI ------------------------------------------------------------------
def _write_manifest(tmp_path, mutate=None):
    m = _valid_manifest()
    if mutate:
        mutate(m)
    p = tmp_path / "change_manifest.json"
    p.write_text(json.dumps(m))
    return str(p)


def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_validates_and_refuses(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    out = tmp_path / "ah"
    rc = _run_cli(["apply-harness", "--manifest", mp, "--actor", "alice", "--out", str(out)])
    assert rc == 0
    captured = capsys.readouterr().out
    assert HARNESS_BANNER in captured
    assert "readiness: ready_for_future_apply_surface" in captured
    assert "applied=False executed=False" in captured


def test_cli_writes_json_md_and_refusal(tmp_path):
    mp = _write_manifest(tmp_path)
    out = tmp_path / "ah"
    _run_cli(["apply-harness", "--manifest", mp, "--out", str(out)])
    assert (out / "apply_readiness_report.json").exists()
    assert (out / "apply_readiness_report.md").exists()
    refusal = json.loads((out / "apply_refusal_receipt.json").read_text())
    assert refusal["ok"] is False and refusal["applied"] is False and refusal["executed"] is False


def test_cli_appends_ledger_event(tmp_path):
    mp = _write_manifest(tmp_path)
    ledger = tmp_path / "governance_ledger.jsonl"
    _run_cli(["apply-harness", "--manifest", mp, "--ledger", str(ledger), "--out", str(tmp_path / "ah")])
    lines = [json.loads(l) for l in open(ledger)]
    assert lines[-1]["event_type"] == "apply_harness_refused"


def test_cli_reports_not_persisted_without_ledger(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    _run_cli(["apply-harness", "--manifest", mp, "--out", str(tmp_path / "ah")])
    assert "not_persisted" in capsys.readouterr().out


def test_cli_rejects_missing_manifest(capsys):
    rc = _run_cli(["apply-harness", "--out", "/tmp/none"])
    assert rc == 1 and "missing --manifest" in capsys.readouterr().out.lower()


def test_cli_rejects_invalid_hash(tmp_path, capsys):
    def bad(m):
        m["manifest_hash"] = "deadbeefdeadbeef"
    mp = _write_manifest(tmp_path, mutate=bad)
    rc = _run_cli(["apply-harness", "--manifest", mp, "--out", str(tmp_path / "ah")])
    assert rc == 1 and "invalid manifest" in capsys.readouterr().out.lower()


def test_cli_rejects_executable_payload_flags(tmp_path, capsys):
    def bad(m):
        m["no_apply_guarantee"]["can_execute"] = True
        m["no_apply_guarantee"]["contains_apply_payload"] = True
    mp = _write_manifest(tmp_path, mutate=bad)
    rc = _run_cli(["apply-harness", "--manifest", mp, "--out", str(tmp_path / "ah")])
    assert rc == 1 and "invalid manifest" in capsys.readouterr().out.lower()


def test_cli_prints_readiness_status(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    _run_cli(["apply-harness", "--manifest", mp, "--out", str(tmp_path / "ah")])
    assert "readiness:" in capsys.readouterr().out


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0 and report["tests_run"] == 68
