"""Packet 7, Layer 2 — manifest renderer + build-manifest CLI."""

from __future__ import annotations

import copy
import json

from logic_mix_os.apply_manifest import MANIFEST_BANNER, build_change_manifest
from logic_mix_os.cli import build_parser
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.manifest_packet import render_manifest_markdown, write_manifest_packet
from logic_mix_os.renderers.review_packet import build_review_packet
from logic_mix_os.review_workflow import ReviewWorkflow

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus.", "expected_strength": "openness",
    "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB",
        "High-pass supporting bus ~250 Hz",
        "Delete source audio in place to bake the loop chop",   # blocked
    ],
}


def _counter_clock():
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-03-01T00:00:{n['i']:02d}+00:00"

    return clock


def _packet_and_state():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    review = [s["step_id"] for s in packet["steps"] if s["decision"] == "review_required"]
    wf = ReviewWorkflow(packet, clock=_counter_clock())
    wf.decide(review[0], "approve", actor="alice")
    wf.decide(review[1], "reject", actor="alice", reason="too washed")
    return packet, wf.state()


# --- renderer -------------------------------------------------------------
def test_json_and_markdown_artifacts_created(tmp_path):
    packet, state = _packet_and_state()
    m = build_change_manifest(packet, state)
    paths = write_manifest_packet(m, str(tmp_path / "man"))
    assert paths["json_path"].endswith("change_manifest.json")
    assert paths["md_path"].endswith("change_manifest.md")
    assert json.loads(open(paths["json_path"]).read())["manifest_hash"] == m["manifest_hash"]


def test_markdown_has_banner_and_sections(tmp_path):
    packet, state = _packet_and_state()
    md = render_manifest_markdown(build_change_manifest(packet, state))
    assert MANIFEST_BANNER in md
    assert "Eligible for future apply" in md
    assert "Excluded" in md
    assert "Blocked" in md
    assert "No-apply guarantee" in md
    assert "Future apply contract" in md
    assert "manifest_hash" not in md or "Manifest hash:" in md  # hash is surfaced


# --- CLI ------------------------------------------------------------------
def _write_inputs(tmp_path, mismatch_plan=False):
    packet, state = _packet_and_state()
    if mismatch_plan:
        state = copy.deepcopy(state)
        state["plan_id"] = "plan_other"
    pp = tmp_path / "operator_review_packet.json"
    dp = tmp_path / "operator_decisions.json"
    pp.write_text(json.dumps(packet))
    dp.write_text(json.dumps(state))
    return str(pp), str(dp)


def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_builds_manifest(tmp_path, capsys):
    pp, dp = _write_inputs(tmp_path)
    out = tmp_path / "man"
    rc = _run_cli(["build-manifest", "--packet", pp, "--decisions", dp, "--out", str(out)])
    assert rc == 0
    assert (out / "change_manifest.json").exists()
    assert (out / "change_manifest.md").exists()
    captured = capsys.readouterr().out
    assert MANIFEST_BANNER in captured
    assert "manifest_hash:" in captured            # CLI prints the hash


def test_cli_rejects_missing_packet(tmp_path, capsys):
    _, dp = _write_inputs(tmp_path)
    rc = _run_cli(["build-manifest", "--decisions", dp, "--out", str(tmp_path / "m")])
    assert rc == 1 and "missing --packet" in capsys.readouterr().out.lower()


def test_cli_rejects_missing_decisions(tmp_path, capsys):
    pp, _ = _write_inputs(tmp_path)
    rc = _run_cli(["build-manifest", "--packet", pp, "--out", str(tmp_path / "m")])
    assert rc == 1 and "missing --decisions" in capsys.readouterr().out.lower()


def test_cli_rejects_mismatched_plan(tmp_path, capsys):
    pp, dp = _write_inputs(tmp_path, mismatch_plan=True)
    rc = _run_cli(["build-manifest", "--packet", pp, "--decisions", dp, "--out", str(tmp_path / "m")])
    assert rc == 1 and "plan_id mismatch" in capsys.readouterr().out.lower()


def test_cli_appends_manifest_emitted_with_ledger(tmp_path):
    pp, dp = _write_inputs(tmp_path)
    ledger = tmp_path / "governance_ledger.jsonl"
    out = tmp_path / "man"
    _run_cli(["build-manifest", "--packet", pp, "--decisions", dp,
              "--ledger", str(ledger), "--out", str(out)])
    lines = [json.loads(l) for l in open(ledger)]
    assert lines[-1]["event_type"] == "manifest_emitted"
    m = json.loads((out / "change_manifest.json").read_text())
    assert m["ledger_status"] == "persisted" and m["manifest_emitted_event_id"]


def test_cli_reports_not_persisted_without_ledger(tmp_path, capsys):
    pp, dp = _write_inputs(tmp_path)
    out = tmp_path / "man"
    _run_cli(["build-manifest", "--packet", pp, "--decisions", dp, "--out", str(out)])
    m = json.loads((out / "change_manifest.json").read_text())
    assert m["ledger_status"] == "not_persisted"
    assert "not_persisted" in capsys.readouterr().out


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0 and report["tests_run"] == 68
