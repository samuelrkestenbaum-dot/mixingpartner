"""Expanded analysis suite (translation, mono, density, narrative, etc.)."""

from __future__ import annotations

import pytest

FIXTURES = ["simple_vocal_piano_song", "dense_chorus_with_loops", "splice_loop_problem"]


@pytest.mark.parametrize("fixture", FIXTURES)
def test_expanded_present(analyzed, fixture):
    e = analyzed[fixture].expanded
    for key in ["translation", "mono_compatibility", "arrangement_density",
                "listener_experience", "transitions", "groove", "harmonic",
                "vocal_performance", "lyrics"]:
        assert key in e


def test_translation_scores_and_profiles(analyzed):
    tr = analyzed["dense_chorus_with_loops"].expanded["translation"]
    assert 0 <= tr["translation_score"] <= 100
    assert len(tr["profiles"]) == 8
    assert any(p["profile"] == "mono_bluetooth_speaker" for p in tr["profiles"])


def test_mono_compatibility_flags_wide_loops(analyzed):
    mono = analyzed["dense_chorus_with_loops"].expanded["mono_compatibility"]
    assert 0 <= mono["mono_score"] <= 100
    # the wide texture loop should appear as a mono-collapse risk
    flagged = {e["track"] for e in mono["events"]}
    assert any("Loop" in t or "Pad" in t for t in flagged)


def test_arrangement_density_flags_crowded_verse(analyzed):
    dens = analyzed["dense_chorus_with_loops"].expanded["arrangement_density"]
    assert dens["crowded_sections"], "dense fixture should crowd at least one section"


def test_listener_experience_reports_unearned_chorus(analyzed):
    le = analyzed["dense_chorus_with_loops"].expanded["listener_experience"]
    assert le["chorus_feels_earned"] is False
    assert le["journey"]


def test_groove_regularity_on_rhythm_stems(analyzed):
    groove = analyzed["dense_chorus_with_loops"].expanded["groove"]
    assert groove["per_track"], "kick/snare should be analysed for groove"
    assert groove["overall_regularity"] is not None


def test_harmonic_relative_key_is_consistent(analyzed):
    # Fixture manifest says E minor; detector tends to find G major (relative).
    harm = analyzed["dense_chorus_with_loops"].expanded["harmonic"]
    assert harm["available"]
    assert harm["matches_manifest"] is True


def test_vocal_performance_available(analyzed):
    vp = analyzed["simple_vocal_piano_song"].expanded["vocal_performance"]
    assert vp["available"]
    assert vp["dynamic_range_db"] >= 0
    assert vp["recommendations"]


def test_mix_plan_carries_translation_and_mono_scores(analyzed):
    plan = analyzed["dense_chorus_with_loops"].mix_plan
    assert plan["translation_score"] is not None
    assert plan["mono_compatibility_score"] is not None
