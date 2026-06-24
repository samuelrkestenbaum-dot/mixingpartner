"""Packet 9, Layer 2 — sandbox renderer + simulate-apply CLI."""

from __future__ import annotations

import copy
import json

from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.apply_sandbox import simulate_apply
from logic_mix_os.cli import build_parser
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.renderers.sandbox_packet import SANDBOX_BANNER, render_sandbox_markdown
from logic_mix_os.review_workflow import ReviewWorkflow

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


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-05-01T00:00:{n['i']:02d}+00:00"

    return clock


def _valid_manifest():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "approve", actor="alice")
    wf.decide(review[2], "reject", actor="alice", reason="not now")
    return build_change_manifest(packet, wf.state())


# --- renderer -------------------------------------------------------------
def test_markdown_has_banner_sections_diff_and_rollback():
    res = simulate_apply(_valid_manifest(), clock=_counter_clock())
    md = render_sandbox_markdown(res)
    assert SANDBOX_BANNER in md
    assert "Eligible simulated" in md
    assert "Excluded untouched" in md and "Blocked untouched" in md
    assert "Before / after diff" in md and "| Step | Target |" in md
    assert "rollback_restored" in md
    assert "No-real-DAW guarantee" in md and "Boundary note" in md


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


def test_cli_simulates_and_writes_artifacts(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    out = tmp_path / "sb"
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--actor", "alice", "--out", str(out)])
    assert rc == 0
    assert (out / "sandbox_simulation_report.json").exists()
    assert (out / "sandbox_simulation_report.md").exists()
    captured = capsys.readouterr().out
    assert SANDBOX_BANNER in captured
    assert "no_real_daw: True" in captured           # prints the no-real-DAW guarantee
    assert "simulation: recorded" in captured


def test_cli_appends_recorded_with_ledger(tmp_path):
    mp = _write_manifest(tmp_path)
    ledger = tmp_path / "governance_ledger.jsonl"
    _run_cli(["simulate-apply", "--manifest", mp, "--ledger", str(ledger), "--out", str(tmp_path / "sb")])
    lines = [json.loads(l) for l in open(ledger)]
    assert lines[-1]["event_type"] == "simulated_apply_recorded"
    res = json.loads((tmp_path / "sb" / "sandbox_simulation_report.json").read_text())
    assert res["after"] is not None and res["rollback_restored"] is True


def test_cli_reports_not_persisted_without_ledger(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    _run_cli(["simulate-apply", "--manifest", mp, "--out", str(tmp_path / "sb")])
    assert "not_persisted" in capsys.readouterr().out


def test_cli_rejects_missing_manifest(capsys):
    rc = _run_cli(["simulate-apply", "--out", "/tmp/none"])
    assert rc == 1 and "missing --manifest" in capsys.readouterr().out.lower()


def test_cli_rejects_invalid_hash(tmp_path, capsys):
    mp = _write_manifest(tmp_path, mutate=lambda m: m.__setitem__("manifest_hash", "deadbeefdeadbeef"))
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--out", str(tmp_path / "sb")])
    assert rc == 1 and "invalid manifest" in capsys.readouterr().out.lower()


def test_cli_rejects_executable_payload(tmp_path, capsys):
    def bad(m):
        m["no_apply_guarantee"]["can_execute"] = True
    mp = _write_manifest(tmp_path, mutate=bad)
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--out", str(tmp_path / "sb")])
    assert rc == 1 and "invalid manifest" in capsys.readouterr().out.lower()


def test_cli_prints_no_real_daw_guarantee(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    _run_cli(["simulate-apply", "--manifest", mp, "--out", str(tmp_path / "sb")])
    out = capsys.readouterr().out
    assert "no_real_daw: True" in out and "real_applied: False" in out


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0 and report["tests_run"] == 68
