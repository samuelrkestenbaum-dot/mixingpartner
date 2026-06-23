"""Audio metric correctness on synthesised signals + real fixtures."""

from __future__ import annotations

import math

import numpy as np

from logic_mix_os import dsp
from logic_mix_os.analyzers.audio_metrics import compute_metrics


SR = 32000


def _sine(freq, dur=1.0, amp=0.5):
    t = np.arange(int(dur * SR)) / SR
    return amp * np.sin(2 * np.pi * freq * t)


def test_level_metrics_make_sense():
    x = _sine(1000, amp=0.5)
    m = compute_metrics(x, SR)
    # peak of a 0.5 sine is ~-6 dBFS
    assert -7.0 < m["peak_dbfs"] < -5.0
    # RMS of a sine is peak/sqrt(2): ~-9 dBFS
    assert m["rms_dbfs"] < m["peak_dbfs"]
    assert m["crest_factor_db"] > 0
    assert m["sample_rate"] == SR
    assert m["channels"] == 1


def test_spectral_centroid_tracks_frequency():
    low = compute_metrics(_sine(300), SR)["spectral_centroid"]
    high = compute_metrics(_sine(4000), SR)["spectral_centroid"]
    assert abs(low - 300) < 200
    assert abs(high - 4000) < 400
    assert high > low


def test_band_energy_sums_to_one():
    m = compute_metrics(_sine(150) + _sine(3000), SR)
    total = sum(m["band_energy"].values())
    assert abs(total - 1.0) < 0.05
    for v in m["band_energy"].values():
        assert 0.0 <= v <= 1.0


def test_stereo_width_and_phase():
    mono = _sine(440)
    identical = np.column_stack([mono, mono])
    assert dsp.stereo_width(identical) < 0.05
    assert dsp.phase_correlation(identical) > 0.95

    rng = np.random.default_rng(0)
    wide = np.column_stack([mono + 0.5 * rng.standard_normal(mono.size),
                            mono - 0.5 * rng.standard_normal(mono.size)])
    assert dsp.stereo_width(wide) > 0.2

    antiphase = np.column_stack([mono, -mono])
    assert dsp.mono_collapse_loss_db(antiphase) < -20  # cancels in mono


def test_loudness_is_finite_and_ordered():
    quiet = compute_metrics(_sine(1000, amp=0.1), SR)["estimated_lufs"]
    loud = compute_metrics(_sine(1000, amp=0.8), SR)["estimated_lufs"]
    assert math.isfinite(quiet) and math.isfinite(loud)
    assert loud > quiet


def test_brightness_bounds_and_indicators():
    m = compute_metrics(_sine(8000), SR)
    assert 0.0 <= m["brightness"] <= 1.0
    assert m["brightness"] > 0.7  # 8 kHz is bright
    for k in ("mud_indicator", "harshness_indicator", "sibilance_indicator", "density", "transient_density"):
        assert 0.0 <= m[k] <= 1.0


def test_real_vocal_stem_metrics(analyzed):
    res = analyzed["simple_vocal_piano_song"]
    vocal = next(t for t in res.track_analysis if t["name"] == "Lead Vocal")["metrics"]
    assert vocal["peak_dbfs"] <= 0.0
    assert vocal["channels"] == 1
    assert vocal["stereo_width"] < 0.05  # mono vocal
