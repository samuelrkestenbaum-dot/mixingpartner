"""Governance / taste-protection tests (build packet 68-84)."""

from __future__ import annotations

from logic_mix_os.governance import (
    KILL_SWITCHES,
    REVIEW_MODES,
    validate_action_safety,
)


def test_governance_present(analyzed):
    g = analyzed["dense_chorus_with_loops"].governance
    for key in ["emotional_truth_lock", "reference_sanity", "negative_constraints",
                "governed_branches", "listener_panel", "stop_conditions",
                "kill_switches", "review_modes", "mixer_feedback"]:
        assert key in g


def test_emotional_truth_lock_locks_when_present(analyzed):
    truth = analyzed["dense_chorus_with_loops"].governance["emotional_truth_lock"]
    assert truth["locked"] is True
    assert truth["lean"] in {"intimate", "big", "neutral"}


def test_negative_constraints_have_severity(analyzed):
    nc = analyzed["dense_chorus_with_loops"].governance["negative_constraints"]
    assert nc, "dense fixture manifest declares negative constraints"
    for c in nc:
        assert c["severity"] in {"high", "medium"}


def test_governed_winner_selected_per_branch(analyzed):
    g = analyzed["dense_chorus_with_loops"].governance
    for b in g["governed_branches"]:
        assert b["governed_winner"] is not None
        assert b["governance"]["taste_triangle"]["verdict"] in {"keep", "reject"}


def test_intimate_song_vetoes_or_downranks_width_bloom(analyzed):
    # Build an intimate-truth project and confirm a width bloom is not the
    # governed winner for chorus lift (it should be vetoed on emotional truth).
    from logic_mix_os.pipeline import analyze
    import pathlib, json
    base = pathlib.Path(__file__).resolve().parent.parent / "fixtures" / "dense_chorus_with_loops"
    m = json.loads((base / "project_manifest.json").read_text())
    m["intent"]["singular_emotional_truth"] = "Intimate and conflicted, quietly falling apart."
    res = analyze(str(base / "stems"), m)
    chorus = next((b for b in res.governance["governed_branches"] if b["problem_id"] == "chorus_lift"), None)
    if chorus:
        assert chorus["governed_winner"] != "chorus_lift_A"  # width bloom vetoed for intimate truth


def test_kill_switch_blocks_destructive_action():
    assert validate_action_safety({"risk_class": 5, "plugin": "x", "setting": "y"})["blocked"]
    assert validate_action_safety({"risk_class": 2, "plugin": "EQ", "setting": "overwrite file"})["blocked"]
    assert not validate_action_safety({"risk_class": 2, "plugin": "Channel EQ", "setting": "cut 250 Hz"})["blocked"]
    assert len(KILL_SWITCHES) >= 5 and len(REVIEW_MODES) == 6


def test_stop_conditions_shape(analyzed):
    stop = analyzed["simple_vocal_piano_song"].governance["stop_conditions"]
    assert isinstance(stop["should_stop"], bool)
    assert stop["reasons"]


def test_mixer_feedback_tones(analyzed):
    fb = analyzed["dense_chorus_with_loops"].governance["mixer_feedback"]
    for tone in ["collaborative", "producer", "direct", "technical", "do_not"]:
        assert fb[tone]
