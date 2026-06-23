"""Layer 2 — ground-truth render ingest + calibration (Hardening Packet 3)."""

from __future__ import annotations

import hashlib

import numpy as np

from logic_mix_os.analyzers.audio_loader import load_audio, write_wav
from logic_mix_os.render_ingest import ingest_render
from logic_mix_os.variant_renderer import run_variant_trial


def _renders(analyzed, tmp_path):
    """Produce a real base.wav + variant.wav to act as base + offline + 'external'."""
    res = analyzed["dense_chorus_with_loops"]
    out = run_variant_trial(res, "chorus_lift_B", out_dir=str(tmp_path))
    return out["base_render"], out["variant_render"]


def test_valid_ingest_succeeds(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    rec = ingest_render(var, base_wav=base, offline_wav=var)
    assert rec["render_id"].startswith("rnd_")
    assert rec["metadata"]["sample_rate"] > 0 and rec["metadata"]["duration"] > 0


def test_incompatible_render_is_surfaced(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    # write a short, wrong-sample-rate WAV
    bad = tmp_path / "bad.wav"
    write_wav(bad, np.zeros(11025), 22050)
    rec = ingest_render(str(bad), base_wav=base)
    assert rec["compatibility"]["compatible"] is False
    assert any("sample-rate" in i or "duration" in i for i in rec["compatibility"]["issues"])


def test_ingest_does_not_mutate_source(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    before = hashlib.md5(open(var, "rb").read()).hexdigest()
    ingest_render(var, base_wav=base, offline_wav=var)
    after = hashlib.md5(open(var, "rb").read()).hexdigest()
    assert before == after


def test_durable_metadata_record(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    rec = ingest_render(var, base_wav=base, store_dir=str(tmp_path / "renders"))
    assert "metadata_path" in rec
    import json
    reloaded = json.loads(open(rec["metadata_path"]).read())
    assert reloaded["render_id"] == rec["render_id"]


def test_external_vs_offline_comparison_produces_deltas(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    rec = ingest_render(var, base_wav=base, offline_wav=var)
    comp = rec["comparison"]
    assert "external_vs_base" in comp and "offline_vs_base" in comp
    assert "loudness_matched_external_vs_base" in comp


def test_calibration_perfect_when_external_equals_offline(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    # external IS the offline render -> directions must align perfectly
    rec = ingest_render(var, base_wav=base, offline_wav=var)
    cal = rec["calibration"]
    assert cal["predicted_direction_correct"] is True
    assert cal["divergent_metrics"] == []


def test_calibration_flags_divergence(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    # external == base (no change), but offline == variant (changed) -> divergence
    rec = ingest_render(base, base_wav=base, offline_wav=var)
    cal = rec["calibration"]
    assert cal["divergent_metrics"], "differing external vs offline directions must be flagged"


def test_ingest_links_to_governance_receipt(analyzed, tmp_path):
    base, var = _renders(analyzed, tmp_path)
    rec = ingest_render(var, base_wav=base, link="chorus_lift_B")
    gov = rec["governance"]
    assert gov["receipt_id"].startswith("rcpt_") and gov["action_id"].startswith("act_")
    assert gov["authority_class"] == 1  # ingest is a local-artifact action
    assert rec["link"] == "chorus_lift_B"
