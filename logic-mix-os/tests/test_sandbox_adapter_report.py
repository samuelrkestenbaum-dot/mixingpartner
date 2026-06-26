"""Packet 10, Layer 2 — adapter metadata in sandbox report + CLI --adapter."""

from __future__ import annotations

import json

from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.apply_sandbox import simulate_apply
from logic_mix_os.cli import build_parser
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.renderers.sandbox_packet import render_sandbox_markdown
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
        return f"2026-06-01T00:00:{n['i']:02d}+00:00"

    return clock


def _manifest():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "approve", actor="alice")
    return build_change_manifest(packet, wf.state())


# --- report ---------------------------------------------------------------
def test_json_report_includes_adapter_metadata():
    res = simulate_apply(_manifest(), clock=_counter_clock())
    assert res["adapter"]["name"] == "FakeSessionAdapter"
    assert res["adapter"]["type"] == "fake_session"
    assert res["adapter"]["capabilities"]["real_daw"] is False


def test_markdown_has_session_adapter_boundary():
    md = render_sandbox_markdown(simulate_apply(_manifest(), clock=_counter_clock()))
    assert "Session Adapter Boundary" in md
    assert "active adapter:** `FakeSessionAdapter`" in md
    assert "real DAW support: `False`" in md
    assert "real apply support: `False`" in md
    assert "simulated apply support: `True`" in md
    assert "rollback support: `True`" in md
    assert "RealLogicSessionAdapter" in md          # names the future seam


# --- CLI ------------------------------------------------------------------
def _write_manifest(tmp_path):
    m = _manifest()
    p = tmp_path / "change_manifest.json"
    p.write_text(json.dumps(m))
    return str(p)


def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_still_simulates_with_fake_adapter(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    out = tmp_path / "sb"
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--out", str(out)])
    assert rc == 0
    captured = capsys.readouterr().out
    assert "adapter: FakeSessionAdapter" in captured
    assert "no_real_daw: True" in captured
    res = json.loads((out / "sandbox_simulation_report.json").read_text())
    assert res["adapter"]["name"] == "FakeSessionAdapter"


def test_cli_accepts_explicit_fake_adapter(tmp_path):
    mp = _write_manifest(tmp_path)
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--adapter", "fake", "--out", str(tmp_path / "sb")])
    assert rc == 0


def test_cli_rejects_non_fake_adapter(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    rc = _run_cli(["simulate-apply", "--manifest", mp, "--adapter", "real", "--out", str(tmp_path / "sb")])
    assert rc == 1
    assert "unknown session adapter" in capsys.readouterr().out.lower()


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0 and report["tests_run"] == 68
