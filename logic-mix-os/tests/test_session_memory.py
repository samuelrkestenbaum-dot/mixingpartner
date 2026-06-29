"""Layer C: session intelligence, memory, ledger, taste, album coherence."""

from __future__ import annotations

import pytest

from logic_mix_os.album import analyze_album
from logic_mix_os.analyzers.render_graph import stale_after
from logic_mix_os.memory import ProjectMemory


def test_provenance_tracks_loops(analyzed):
    prov = analyzed["splice_loop_problem"].provenance
    assert prov["summary"]["loops_tracked"] >= 1
    assert any(i["sample_origin"] == "Splice" for i in prov["items"])


def test_render_graph_staleness(analyzed):
    g = analyzed["simple_vocal_piano_song"].render_graph
    assert g["nodes"] and g["edges"]
    # changing a stem invalidates the bounce and downstream reports
    stem = next(n["id"] for n in g["nodes"] if n["type"] == "stem")
    stale = stale_after(g, stem)
    assert "bounce:mixdown" in stale
    assert any(s.startswith("report:") for s in stale)


def test_plugin_scan_all_stock_available(analyzed):
    scan = analyzed["dense_chorus_with_loops"].plugin_scan
    assert scan["plugins_used"]
    assert scan["all_available"] is True  # only Logic stock recommended


def test_plugin_scan_reports_missing_when_inventory_limited(analyzed):
    from logic_mix_os.analyzers.plugin_scanner import scan_plugins
    plan = analyzed["dense_chorus_with_loops"].mix_plan
    scan = scan_plugins(plan, available=["Channel EQ"])  # only EQ present
    assert not scan["all_available"]
    assert any(m["plugin"] == "Compressor" for m in scan["missing"])


def test_memory_records_passes_and_deltas(analyzed, tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    r = analyzed["dense_chorus_with_loops"]
    p1 = mem.record_pass("mix_pass_01", r)
    p2 = mem.record_pass("mix_pass_02", r)
    assert p1["pass_name"] == "mix_pass_01"
    # identical result -> no improvement/regression on second pass
    assert p2["improved"] == [] and p2["got_worse"] == []
    assert len(mem.history()) == 2


def test_decision_ledger_autopopulates(analyzed, tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    mem.record_plan_decisions(analyzed["dense_chorus_with_loops"])
    ledger = mem.ledger()
    assert ledger
    assert all("validation" in d and "reason" in d for d in ledger)


def test_add_decision_event_type_accept_reject_and_optional(tmp_path):
    mem = ProjectMemory(tmp_path / "mem")

    # accept: a valid event_type is stored on the entry
    entry = mem.add_decision({"decision": "x", "reason": "y"}, event_type="mix_decision")
    assert entry["event_type"] == "mix_decision"
    ledger = mem.ledger()
    assert ledger[-1]["event_type"] == "mix_decision"

    # reject: an unknown event_type raises ValueError
    with pytest.raises(ValueError):
        mem.add_decision({"decision": "x", "reason": "y"}, event_type="not_a_real_type")

    # backward-compat: omitting event_type succeeds and stores no event_type key
    plain = mem.add_decision({"decision": "x", "reason": "y"})
    assert "event_type" not in plain
    assert "event_type" not in mem.ledger()[-1]


def test_taste_calibration_forms_profile(tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    mem.add_feedback("too wide")
    taste = mem.add_feedback("too wide")  # twice -> stable preference
    assert any("narrower" in s for s in taste["profile"])


def test_album_coherence(analyzed):
    results = [analyzed["simple_vocal_piano_song"], analyzed["dense_chorus_with_loops"],
               analyzed["splice_loop_problem"]]
    report = analyze_album(results, ["a", "b", "c"])
    assert 0 <= report["coherence_score"] <= 100
    assert len(report["songs"]) == 3
    assert "verdict" in report
