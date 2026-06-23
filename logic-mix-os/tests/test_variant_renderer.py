"""Layer 1 — offline variant renderer + before/after compare (Hardening Packet 2)."""

from __future__ import annotations

import numpy as np

from logic_mix_os.analyzers.audio_loader import load_audio
from logic_mix_os.variant_renderer import plan_ops, run_variant_trial


def test_render_produces_real_wavs(analyzed, tmp_path):
    res = analyzed["dense_chorus_with_loops"]
    out = run_variant_trial(res, "chorus_lift_B", out_dir=str(tmp_path))  # subtractive drop (mutes loop)
    base = load_audio(out["base_render"])
    var = load_audio(out["variant_render"])
    assert base.num_frames > 0 and var.num_frames > 0
    assert base.sample_rate == var.sample_rate


def test_variant_is_measurably_different_from_base(analyzed, tmp_path):
    res = analyzed["dense_chorus_with_loops"]
    out = run_variant_trial(res, "chorus_lift_B", out_dir=str(tmp_path))
    base = load_audio(out["base_render"]).samples
    var = load_audio(out["variant_render"]).samples
    n = min(base.shape[0], var.shape[0])
    assert not np.allclose(base[:n], var[:n]), "muting the loop must change the bounce"


def test_compare_has_raw_and_loudness_matched_deltas(analyzed):
    out = run_variant_trial(analyzed["dense_chorus_with_loops"], "chorus_lift_A")
    c = out["compare"]
    assert "raw_delta" in c and "loudness_matched_delta" in c
    # loudness match neutralises level: matched lufs delta ~ 0
    assert abs(c["loudness_matched_delta"]["lufs"]) < 0.5


def test_loudness_match_neutralises_a_louder_variant(analyzed):
    # vocal_ride raises level; raw shows it, loudness-matched does not.
    out = run_variant_trial(analyzed["dense_chorus_with_loops"], "chorus_lift_C")
    c = out["compare"]
    assert abs(c["loudness_matched_delta"]["lufs"]) < 0.5


def test_unmapped_changes_are_surfaced(analyzed):
    # chorus_lift_C contains a "Delay throw …" change the renderer can't do.
    out = run_variant_trial(analyzed["dense_chorus_with_loops"], "chorus_lift_C")
    assert out["unmapped_changes"], "unsupported changes must be reported, not dropped"
    assert any("delay" in u.lower() for u in out["unmapped_changes"])


def test_plan_ops_maps_known_kinds(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    by_id = {v["variant_id"]: v for b in res.creative["branches"] for v in b["variants"]}
    ops, _ = plan_ops(by_id["chorus_lift_A"], res.records, res.project.sections)  # width_bloom
    assert ops and any(o["op"] == "width" for o in ops)
    ops2, _ = plan_ops(by_id["loop_A"], res.records, res.project.sections)  # loop_deconstruct
    assert any(o["op"] == "eq" for o in ops2) and any(o["op"] == "width" for o in ops2)


def test_compare_flags_translation_or_wash_risk(analyzed):
    # The width bloom widens the field; compare should produce a verdict + notes.
    out = run_variant_trial(analyzed["dense_chorus_with_loops"], "chorus_lift_A")
    c = out["compare"]
    assert isinstance(c["perceptual_improvement"], bool)
    assert c["notes"]


def test_renderer_does_not_modify_source_stems(analyzed, tmp_path):
    res = analyzed["dense_chorus_with_loops"]
    t = res.project.resolved_tracks()[0]
    before = load_audio(t.file).samples.copy()
    run_variant_trial(res, "chorus_lift_B", out_dir=str(tmp_path))
    after = load_audio(t.file).samples
    assert np.array_equal(before, after), "source stems must never be modified"
