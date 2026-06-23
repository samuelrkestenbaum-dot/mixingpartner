"""Layer 2 — taste memory + bounded scoring feedback (Hardening Packet 2)."""

from __future__ import annotations

from logic_mix_os.creative import TASTE_CAP, score_variant
from logic_mix_os.memory import ProjectMemory


def _ctx(**over):
    base = dict(contrast_deficit=0.5, overcrowding=0.5, masking_pressure=0.2, vocal_risk=0.2,
                loop_pressure=0.3, width_room=0.5, static_dynamic_gap=0.5, intimate=0.0, lean="neutral")
    base.update(over)
    return base


def _var(kind, problem="chorus_lift"):
    return {"kind": kind, "problem": problem, "name": kind}


def test_choice_creates_durable_memory(tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    chosen = {"kind": "subtractive_drop", "variant_id": "x", "scores": {"evidence": [{"signal": "overcrowding", "value": 0.6}]}}
    rejected = [{"kind": "width_bloom"}, {"kind": "drum_room_bloom"}]
    mem.add_variant_choice(chosen, rejected, reason="cleaner chorus")
    # reload from disk
    reloaded = ProjectMemory(tmp_path / "mem")
    store = reloaded.taste_profile()
    assert store["variant_choices"], "choice must persist"
    assert store["variant_choices"][0]["reason"] == "cleaner chorus"
    assert reloaded.taste_weights()["subtractive_drop"] > 0


def test_weights_are_capped(tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    chosen = {"kind": "vocal_ride", "variant_id": "v", "scores": {}}
    rejected = [{"kind": "width_bloom"}]
    for _ in range(10):  # many wins -> would exceed cap without clamping
        mem.add_variant_choice(chosen, rejected)
    w = mem.taste_weights()
    assert w["vocal_ride"] == TASTE_CAP
    assert w["width_bloom"] == -TASTE_CAP


def test_score_shifts_with_taste_but_is_bounded():
    ctx = _ctx()
    base = score_variant(_var("width_bloom"), ctx)
    boosted = score_variant(_var("width_bloom"), ctx, taste={"width_bloom": 8})
    assert boosted["overall_score"] > base["overall_score"]
    assert boosted["taste_adjustment"] == 8.0
    # over-cap requests are clamped
    capped = score_variant(_var("width_bloom"), ctx, taste={"width_bloom": 50})
    assert capped["taste_adjustment"] == TASTE_CAP


def test_empty_taste_is_a_noop():
    ctx = _ctx()
    none = score_variant(_var("vocal_ride"), ctx)
    empty = score_variant(_var("vocal_ride"), ctx, taste={})
    assert none["overall_score"] == empty["overall_score"]
    assert none["taste_adjustment"] == 0.0


def test_pipeline_applies_learned_taste(analyzed, tmp_path):
    # Record a preference for vocal_ride, then re-analyse with that memory.
    from logic_mix_os.pipeline import analyze
    import json
    base = analyzed["dense_chorus_with_loops"]
    by_id = {v["variant_id"]: v for b in base.creative["branches"] for v in b["variants"]}
    chosen = by_id["chorus_lift_C"]  # vocal_ride
    rejected = [by_id["chorus_lift_A"], by_id["chorus_lift_B"]]
    mem = ProjectMemory(tmp_path / "mem")
    mem.add_variant_choice(chosen, rejected)

    proj_dir = base.project.stems_dir
    manifest = json.loads((proj_dir.parent / "project_manifest.json").read_text())
    learned = analyze(str(proj_dir), manifest, memory_dir=str(tmp_path / "mem"))
    lb = {v["variant_id"]: v for b in learned.creative["branches"] for v in b["variants"]}
    # vocal_ride got a positive learned bump; width_bloom a negative one
    assert lb["chorus_lift_C"]["scores"]["taste_adjustment"] > 0
    assert lb["chorus_lift_A"]["scores"]["taste_adjustment"] < 0
    assert lb["chorus_lift_C"]["scores"]["overall_score"] > by_id["chorus_lift_C"]["scores"]["overall_score"]


def test_no_memory_dir_leaves_scoring_unchanged(analyzed):
    # The session fixture was analysed without a memory dir; taste adj must be 0.
    for b in analyzed["dense_chorus_with_loops"].creative["branches"]:
        for v in b["variants"]:
            assert v["scores"]["taste_adjustment"] == 0.0
