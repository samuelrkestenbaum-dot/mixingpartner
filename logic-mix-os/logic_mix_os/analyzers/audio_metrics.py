"""Per-stem and per-range audio metrics.

Produces the deterministic ``track_analysis`` numbers consumed by every later
stage (identity, depth, masking, doctrine). All values are JSON-serialisable.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from .. import dsp
from ..constants import HARSH_BAND, MUD_BAND, SIBILANCE_BAND, VOCAL_PRESENCE_BAND
from .audio_loader import LoadedAudio


def compute_metrics(samples: np.ndarray, sr: int) -> Dict:
    """Full metric dict for a raw samples array (mono or stereo)."""
    samples = np.asarray(samples, dtype=np.float64)
    mono = dsp.to_mono(samples)
    freqs, power = dsp.average_power(mono, sr)

    bands = dsp.band_energy_fractions(freqs, power)
    centroid = dsp.spectral_centroid(freqs, power)
    onsets = dsp.onset_density_per_sec(mono, sr)

    mud = dsp.band_fraction(freqs, power, *MUD_BAND)
    harsh = dsp.band_fraction(freqs, power, *HARSH_BAND)
    sib = dsp.band_fraction(freqs, power, *SIBILANCE_BAND)

    channels = 1 if samples.ndim == 1 else int(samples.shape[1])

    return {
        "duration": round(mono.size / float(sr), 3),
        "sample_rate": int(sr),
        "channels": channels,
        "peak_dbfs": round(dsp.peak_dbfs(mono), 2),
        "rms_dbfs": round(dsp.rms_dbfs(mono), 2),
        "estimated_lufs": dsp.integrated_loudness(samples, sr),
        "crest_factor_db": dsp.crest_factor_db(mono),
        "spectral_centroid": centroid,
        "spectral_rolloff": dsp.spectral_rolloff(freqs, power),
        "spectral_flatness": dsp.spectral_flatness(power),
        "brightness": dsp.brightness_from_centroid(centroid),
        "band_energy": bands,
        "stereo_width": dsp.stereo_width(samples),
        "phase_correlation": dsp.phase_correlation(samples),
        "mono_collapse_loss_db": dsp.mono_collapse_loss_db(samples),
        "transient_density_per_sec": onsets,
        "transient_density": dsp.normalize(onsets, 0.0, 6.0),
        "density": dsp.spectral_occupancy(freqs, power),
        # Heuristic problem indicators, 0..1. Tagged "inferred" downstream.
        "mud_indicator": dsp.normalize(mud, 0.18, 0.45),
        "harshness_indicator": dsp.normalize(harsh, 0.10, 0.30),
        "sibilance_indicator": dsp.normalize(sib, 0.04, 0.18),
        "vocal_presence_energy": round(
            dsp.band_fraction(freqs, power, *VOCAL_PRESENCE_BAND), 4
        ),
        # Filled in later by the masking analyzer (cross-track).
        "masking_risk": None,
    }


def analyze_audio(loaded: LoadedAudio) -> Dict:
    """Full metrics for a loaded stem, including its file path."""
    metrics = compute_metrics(loaded.samples, loaded.sample_rate)
    metrics["path"] = loaded.path
    return metrics


def analyze_range(loaded: LoadedAudio, start: float, end: Optional[float]) -> Dict:
    """Section-level metrics for a time slice of a stem (or mixdown)."""
    seg = loaded.slice_seconds(start, end)
    return compute_metrics(seg, loaded.sample_rate)
