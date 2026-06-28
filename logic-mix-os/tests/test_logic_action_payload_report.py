"""Packet 11, Layer 2 — payload negotiation report renderer + CLI + schema."""

from __future__ import annotations

import json
import os

import logic_mix_os
from logic_mix_os.apply_manifest import build_change_manifest
from logic_mix_os.cli import build_parser
from logic_mix_os.logic_action_payload import build_payloads, negotiate_payloads
from logic_mix_os.logic_planner import plan_logic_actions
from logic_mix_os.renderers.payload_packet import render_payload_markdown
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
def test_markdown_has_banner_and_guarantee():
    md = render_payload_markdown(negotiate_payloads(_manifest(), clock=_counter_clock()))
    assert "TYPED LOGIC ACTION PAYLOAD NEGOTIATION — NO REAL DAW" in md
    assert "No-real-DAW guarantee" in md
    assert "no_real_daw: `True`" in md
    assert "environment: `typed_payload_negotiation`" in md


def test_markdown_has_adapter_boundary_and_table():
    md = render_payload_markdown(negotiate_payloads(_manifest(), clock=_counter_clock()))
    assert "Session Adapter Boundary" in md
    assert "active adapter:** `FakeSessionAdapter`" in md
    assert "RealLogicSessionAdapter" in md                       # names the future seam
    assert "| Step | Action type | Parameter | Value | Authority | Negotiated | Reversible |" in md
    assert "Capability negotiation" in md


def test_json_report_includes_payloads_and_adapter():
    res = negotiate_payloads(_manifest(), clock=_counter_clock())
    assert res["adapter"]["name"] == "FakeSessionAdapter"
    assert res["adapter"]["capabilities"]["real_daw"] is False
    assert len(res["payloads"]) == 2
    assert all("negotiation" in p and "operation" in p for p in res["payloads"])


def test_markdown_refusal_path():
    m = _manifest()
    m["manifest_hash"] = "deadbeefdeadbeef"
    md = render_payload_markdown(negotiate_payloads(m, clock=_counter_clock()))
    assert "⛔ Refused" in md
    assert "invalid manifest" in md


# --- CLI ------------------------------------------------------------------
def _write_manifest(tmp_path):
    p = tmp_path / "change_manifest.json"
    p.write_text(json.dumps(_manifest()))
    return str(p)


def _run_cli(argv):
    args = build_parser().parse_args(argv)
    return args.func(args)


def test_cli_negotiates_with_fake_adapter(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    out = tmp_path / "pn"
    rc = _run_cli(["negotiate-payloads", "--manifest", mp, "--out", str(out)])
    assert rc == 0
    captured = capsys.readouterr().out
    assert "adapter: FakeSessionAdapter" in captured
    assert "no_real_daw: True" in captured
    assert "accepted: 2" in captured
    res = json.loads((out / "payload_negotiation_report.json").read_text())
    assert res["counts"]["accepted"] == 2 and res["operations_driven"] is True


def test_cli_accepts_explicit_fake_adapter(tmp_path):
    mp = _write_manifest(tmp_path)
    rc = _run_cli(["negotiate-payloads", "--manifest", mp, "--adapter", "fake", "--out", str(tmp_path / "pn")])
    assert rc == 0


def test_cli_rejects_non_fake_adapter(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    rc = _run_cli(["negotiate-payloads", "--manifest", mp, "--adapter", "real", "--out", str(tmp_path / "pn")])
    assert rc == 1
    assert "unknown session adapter" in capsys.readouterr().out.lower()


def test_cli_audits_to_ledger(tmp_path, capsys):
    mp = _write_manifest(tmp_path)
    ledger = tmp_path / "gov.jsonl"
    rc = _run_cli(["negotiate-payloads", "--manifest", mp, "--ledger", str(ledger),
                   "--actor", "alice", "--out", str(tmp_path / "pn")])
    assert rc == 0
    assert "payload_negotiation_recorded" in capsys.readouterr().out
    from logic_mix_os.governance_ledger import GovernanceLedger
    assert GovernanceLedger(str(ledger)).verify()["ok"] is True


# --- schema ---------------------------------------------------------------
def test_payload_conforms_to_documented_schema():
    schema_path = os.path.join(os.path.dirname(logic_mix_os.__file__),
                               "schemas", "logic_action_payload.schema.json")
    schema = json.load(open(schema_path, encoding="utf-8"))
    assert set(schema["properties"]["action_type"]["enum"]) >= {"set_send", "insert_plugin"}
    for p in build_payloads(_manifest()):
        for key in schema["required"]:
            assert key in p, f"payload missing required schema field {key}"
        assert p["action_type"] in schema["properties"]["action_type"]["enum"]
        assert p["intent_only"] is True and p["applied"] is False


def test_no_golden_regression_changes_required(fixtures_dir):
    from logic_mix_os.regression import run_regression_suite
    report = run_regression_suite(str(fixtures_dir))
    assert report["failed"] == 0 and report["tests_run"] == 68
