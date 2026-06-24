"""Packet 5, Layer 2 — operator review packet + plan-logic CLI."""

from __future__ import annotations

import json

from logic_mix_os.cli import build_parser
from logic_mix_os.creative import run_creative_engine
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.review_packet import (
    BANNER,
    build_review_packet,
    render_review_markdown,
    validate_review_packet,
    write_review_packet,
)

VARIANT = {
    "variant_id": "chorus_lift_X", "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus by blooming supporting elements.",
    "expected_strength": "emotional openness", "tracks_affected": ["Backing Vocals"],
    "changes": [
        "Increase backing-vocal plate send +3 dB at chorus entry",
        "Ride lead vocal +1 dB into the chorus",
        "Delete source audio in place to bake the loop chop",   # -> Class 5 blocked
        "Trust the performance and leave it alone",             # -> unmapped
    ],
}

MIX_PLAN = {
    "song_title": "Test Song",
    "per_track_actions": [{
        "track": "Lead Vocal", "track_id": "lead_vocal", "depth_layer": "intimate",
        "send_reverb": "Short room, very low send.",
        "actions": [{"plugin": "Channel EQ", "setting": "High-pass ~80 Hz.",
                     "reason": "Clean mud.", "risk_class": 2}],
        "automation": [],
    }],
}


def test_json_and_markdown_packets_are_created(tmp_path):
    plan = plan_logic_actions(VARIANT)
    res = write_review_packet(plan, str(tmp_path / "review"))
    assert res["json_path"].endswith("operator_review_packet.json")
    assert res["md_path"].endswith("operator_review_packet.md")
    assert json.loads(open(res["json_path"]).read())["plan_id"] == plan["plan_id"]
    assert open(res["md_path"]).read().strip()


def test_packet_has_nothing_will_be_applied_banner(tmp_path):
    plan = plan_logic_actions(VARIANT)
    packet = build_review_packet(plan)
    assert packet["banner"] == BANNER == "NOTHING WILL BE APPLIED"
    md = render_review_markdown(plan)
    assert "NOTHING WILL BE APPLIED" in md
    assert packet["nothing_applied"] is True


def test_packet_contains_per_step_receipts():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    assert packet["steps"]
    for s in packet["steps"]:
        assert s["receipt_id"].startswith("rcpt_")
        assert s["applied"] is False


def test_packet_contains_rollback_summaries():
    packet = build_review_packet(plan_logic_actions(MIX_PLAN))
    assert all(s["rollback_summary"] and s["rollback_summary"] != "—" for s in packet["steps"])


def test_packet_contains_ledger_integrity_status(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    packet = build_review_packet(plan_logic_actions(VARIANT, ledger_path=path))
    assert packet["ledger"]["integrity"] == "ok"
    assert packet["ledger"]["verification"]["ok"] is True
    # Without a ledger path the status is explicit, not a silent omission.
    packet2 = build_review_packet(plan_logic_actions(VARIANT))
    assert packet2["ledger"]["integrity"] == "not_persisted"


def test_packet_surfaces_blocked_and_unsupported(tmp_path):
    plan = plan_logic_actions(VARIANT)
    packet = build_review_packet(plan)
    assert packet["blocked"]            # the destructive change
    assert packet["unsupported"]        # the unmapped change
    md = render_review_markdown(plan)
    assert "Blocked steps" in md and "Unsupported / unmapped" in md
    # Human-mixer structure is present.
    assert "Here is what I would do in Logic" in md
    assert "Here is why it cannot apply here" in md


def test_packet_validation_passes_and_catches_applied():
    packet = build_review_packet(plan_logic_actions(VARIANT))
    assert validate_review_packet(packet)["ok"] is True
    packet["steps"][0]["applied"] = True
    bad = validate_review_packet(packet)
    assert bad["ok"] is False and any("applied" in e for e in bad["errors"])


def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_plan_logic_variant_input(tmp_path, analyzed, capsys):
    creative = run_creative_engine(analyzed["dense_chorus_with_loops"])
    cpath = tmp_path / "creative.json"
    cpath.write_text(json.dumps(creative))
    out = tmp_path / "rev_variant"
    rc = _run_cli(["plan-logic", "--variant", str(cpath), "--out", str(out)])
    assert rc == 0
    assert (out / "operator_review_packet.json").exists()
    assert (out / "operator_review_packet.md").exists()
    assert "NOTHING WILL BE APPLIED" in capsys.readouterr().out


def test_cli_plan_logic_mix_plan_input(tmp_path, capsys):
    ppath = tmp_path / "mix_plan.json"
    ppath.write_text(json.dumps(MIX_PLAN))
    out = tmp_path / "rev_plan"
    ledger = tmp_path / "governance_ledger.jsonl"
    rc = _run_cli(["plan-logic", "--plan", str(ppath), "--ledger", str(ledger), "--out", str(out)])
    assert rc == 0
    assert (out / "operator_review_packet.json").exists()
    assert ledger.exists()
    assert "audit ledger" in capsys.readouterr().out


def test_cli_rejects_missing_and_conflicting_inputs(tmp_path, capsys):
    assert _run_cli(["plan-logic"]) == 1                      # neither
    capsys.readouterr()
    ppath = tmp_path / "mix_plan.json"; ppath.write_text(json.dumps(MIX_PLAN))
    cpath = tmp_path / "creative.json"; cpath.write_text(json.dumps(VARIANT))
    assert _run_cli(["plan-logic", "--variant", str(cpath), "--plan", str(ppath)]) == 1  # both


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0
    assert report["tests_run"] == 68
