"""Creative experimentation engine tests (build packet 55-67)."""

from __future__ import annotations

import pytest

from logic_mix_os.creative import SEARCH_MODES, run_creative_engine


def test_creative_present_with_branches(analyzed):
    c = analyzed["dense_chorus_with_loops"].creative
    assert c["search_mode"] in SEARCH_MODES
    assert c["branches"], "dense fixture should surface creative problems"
    assert c["static_baseline"]["status"] == "locked"


def test_each_variant_scored(analyzed):
    for res in analyzed.values():
        for branch in res.creative["branches"]:
            assert branch["variants"]
            for v in branch["variants"]:
                s = v["scores"]
                assert 0 <= s["overall_score"] <= 100
                assert s["translation_risk"] in {"low", "medium", "high"}
                assert v["reversibility"] == "non_destructive_duplicate_track"


def test_chorus_lift_has_abcd_branching(analyzed):
    c = analyzed["dense_chorus_with_loops"].creative
    branch = next((b for b in c["branches"] if b["problem_id"] == "chorus_lift"), None)
    assert branch is not None
    kinds = {v["kind"] for v in branch["variants"]}
    # at least width bloom, subtractive, vocal ride options
    assert {"width_bloom", "subtractive_drop", "vocal_ride"} <= kinds


def test_winning_variant_has_merge_plan(analyzed):
    c = analyzed["dense_chorus_with_loops"].creative
    for branch in c["branches"]:
        win = branch["winning"]
        assert win["winning_variant"]
        assert win["keep_moves"]


def test_search_mode_resolves_from_intent(analyzed):
    # splice fixture truth mentions "personal/steamrolling" -> not intimate keyword,
    # simple fixture is neutral. Dense is neutral -> dramatic_contrast.
    assert analyzed["dense_chorus_with_loops"].creative["search_mode"] in SEARCH_MODES


def test_explicit_mode_override():
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest
    import pathlib
    base = pathlib.Path(__file__).resolve().parent.parent / "fixtures" / "simple_vocal_piano_song"
    m = load_manifest(base / "project_manifest.json")
    res = analyze(str(base / "stems"), m, creative_mode="deconstructive")
    assert res.creative["search_mode"] == "deconstructive"
