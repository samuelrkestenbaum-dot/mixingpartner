"""Deterministic DSP primitives.

Everything here is numpy-only by default. More accurate / faster paths are used
when ``scipy`` or ``pyloudnorm`` are installed, but the module always works with
just numpy so the tool stays local-first and dependency-light.

All functions are pure: same input -> same output, no global state, no I/O.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np

from .constants import BANDS

try:  # optional, only used to make loudness measurement exact
    import scipy.signal as _scipy_signal  # type: ignore

    _HAVE_SCIPY = True
except Exception:  # pragma: no cover - exercised only without scipy
    _scipy_signal = None
    _HAVE_SCIPY = False

try:  # optional, best-in-class loudness across all sample rates
    import pyloudnorm as _pyln  # type: ignore

    _HAVE_PYLN = True
except Exception:  # pragma: no cover - exercised only without pyloudnorm
    _pyln = None
    _HAVE_PYLN = False

EPS = 1e-12


# --------------------------------------------------------------------------- #
# Basic level helpers
# --------------------------------------------------------------------------- #
def to_mono(samples: np.ndarray) -> np.ndarray:
    """Collapse to a mono float array. Accepts (n,) or (n, channels)."""
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim == 1:
        return x
    return x.mean(axis=1)


def db_from_amplitude(amp: float) -> float:
    """Amplitude (0..1 full scale) -> dBFS, floored at -120 dB."""
    return 20.0 * math.log10(max(float(amp), 10 ** (-120 / 20)))


def rms(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(x)) + EPS))


def peak(x: np.ndarray) -> float:
    x = np.asarray(x)
    if x.size == 0:
        return 0.0
    return float(np.max(np.abs(x)))


def rms_dbfs(x: np.ndarray) -> float:
    return db_from_amplitude(rms(x))


def peak_dbfs(x: np.ndarray) -> float:
    return db_from_amplitude(peak(x))


def crest_factor_db(x: np.ndarray) -> float:
    """Peak-to-RMS ratio in dB. Higher = more dynamic / transient."""
    return round(peak_dbfs(x) - rms_dbfs(x), 3)


# --------------------------------------------------------------------------- #
# Framing + spectra
# --------------------------------------------------------------------------- #
def _hann(n: int) -> np.ndarray:
    return np.hanning(n) if n > 1 else np.ones(n)


def frame_signal(x: np.ndarray, frame: int, hop: int) -> np.ndarray:
    """Return a (num_frames, frame) matrix of overlapping windows."""
    x = np.asarray(x, dtype=np.float64)
    if x.size < frame:
        pad = np.zeros(frame, dtype=np.float64)
        pad[: x.size] = x
        return pad[None, :]
    num = 1 + (x.size - frame) // hop
    idx = np.arange(frame)[None, :] + hop * np.arange(num)[:, None]
    return x[idx]


def power_spectrogram(
    x: np.ndarray, sr: int, frame: int = 2048, hop: int = 1024
) -> Tuple[np.ndarray, np.ndarray]:
    """Return (freqs, power[num_frames, bins]) with a Hann window."""
    x = to_mono(x)
    frame = min(frame, max(8, 1 << int(math.log2(max(x.size, 8)))))
    hop = max(1, min(hop, frame))
    win = _hann(frame)
    frames = frame_signal(x, frame, hop) * win
    spec = np.fft.rfft(frames, axis=1)
    power = (np.abs(spec) ** 2) / (np.sum(win ** 2) + EPS)
    freqs = np.fft.rfftfreq(frame, d=1.0 / sr)
    return freqs, power


def average_power(x: np.ndarray, sr: int) -> Tuple[np.ndarray, np.ndarray]:
    """Mean power spectrum across frames -> (freqs, power[bins])."""
    freqs, power = power_spectrogram(x, sr)
    return freqs, power.mean(axis=0)


# --------------------------------------------------------------------------- #
# Spectral descriptors
# --------------------------------------------------------------------------- #
def band_energy_fractions(freqs: np.ndarray, power: np.ndarray) -> Dict[str, float]:
    """Fraction of total spectral energy in each named band (sums ~1.0)."""
    total = float(np.sum(power)) + EPS
    out: Dict[str, float] = {}
    for name, (lo, hi) in BANDS.items():
        mask = (freqs >= lo) & (freqs < hi)
        out[name] = round(float(np.sum(power[mask])) / total, 4)
    return out


def band_fraction(freqs: np.ndarray, power: np.ndarray, lo: float, hi: float) -> float:
    total = float(np.sum(power)) + EPS
    mask = (freqs >= lo) & (freqs < hi)
    return float(np.sum(power[mask])) / total


def spectral_centroid(freqs: np.ndarray, power: np.ndarray) -> float:
    """Energy-weighted mean frequency (Hz). Uses magnitude weighting."""
    mag = np.sqrt(np.maximum(power, 0.0))
    denom = float(np.sum(mag)) + EPS
    return round(float(np.sum(freqs * mag) / denom), 2)


def spectral_rolloff(freqs: np.ndarray, power: np.ndarray, pct: float = 0.85) -> float:
    """Frequency below which ``pct`` of the energy lies (Hz)."""
    cumulative = np.cumsum(power)
    total = cumulative[-1] + EPS
    threshold = pct * total
    idx = int(np.searchsorted(cumulative, threshold))
    idx = min(idx, len(freqs) - 1)
    return round(float(freqs[idx]), 2)


def spectral_flatness(power: np.ndarray) -> float:
    """Geometric mean / arithmetic mean of power. 0 = tonal, 1 = noise-like."""
    p = np.maximum(power, EPS)
    geo = np.exp(np.mean(np.log(p)))
    arith = np.mean(p) + EPS
    return round(float(geo / arith), 4)


def spectral_occupancy(freqs: np.ndarray, power: np.ndarray, floor_db: float = -45.0) -> float:
    """Fraction of frequency bins carrying meaningful energy. Density proxy."""
    if power.ndim == 1:
        peak_p = float(np.max(power)) + EPS
        active = power >= peak_p * (10 ** (floor_db / 10))
        return round(float(np.mean(active)), 4)
    # spectrogram: average occupancy per frame
    peak_p = np.max(power, axis=1, keepdims=True) + EPS
    active = power >= peak_p * (10 ** (floor_db / 10))
    return round(float(np.mean(active)), 4)


def _flux_novelty(x: np.ndarray, sr: int, hop: int = 512):
    freqs, power = power_spectrogram(x, sr, frame=1024, hop=hop)
    mag = np.sqrt(np.maximum(power, 0.0))
    flux = np.sqrt(np.sum(np.maximum(np.diff(mag, axis=0), 0.0) ** 2, axis=1))
    return flux


def onset_density_per_sec(x: np.ndarray, sr: int) -> float:
    """Crude onset rate via spectral-flux novelty peak picking (onsets/sec)."""
    flux = _flux_novelty(x, sr)
    if flux.size < 3:
        return 0.0
    flux = flux / (np.max(flux) + EPS)
    thresh = float(np.mean(flux) + np.std(flux))
    peaks = (flux[1:-1] > flux[:-2]) & (flux[1:-1] >= flux[2:]) & (flux[1:-1] > thresh)
    count = int(np.sum(peaks))
    duration = max(x.size / float(sr), EPS)
    return round(count / duration, 3)


def onset_times_sec(x: np.ndarray, sr: int, hop: int = 512) -> list:
    """Onset times in seconds via spectral-flux peak picking."""
    flux = _flux_novelty(x, sr, hop=hop)
    if flux.size < 3:
        return []
    norm = flux / (np.max(flux) + EPS)
    thresh = float(np.mean(norm) + 0.8 * np.std(norm))
    idx = np.where(
        (norm[1:-1] > norm[:-2]) & (norm[1:-1] >= norm[2:]) & (norm[1:-1] > thresh)
    )[0] + 1
    return [round(float((i * hop) / sr), 4) for i in idx]


def rms_envelope(x: np.ndarray, sr: int, win: float = 0.05):
    """Return (times_sec, rms_dbfs[]) over short windows."""
    x = to_mono(x)
    n = max(1, int(win * sr))
    if x.size < n:
        return np.array([0.0]), np.array([rms_dbfs(x)])
    num = x.size // n
    trimmed = x[: num * n].reshape(num, n)
    rms_vals = np.sqrt(np.mean(trimmed ** 2, axis=1) + EPS)
    db = 20.0 * np.log10(np.maximum(rms_vals, 10 ** (-120 / 20)))
    times = (np.arange(num) * n + n / 2) / sr
    return times, db


# 12 pitch-class names starting at C.
_PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
# Krumhansl-Kessler major/minor key profiles.
_KK_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_KK_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def chroma_vector(x: np.ndarray, sr: int) -> np.ndarray:
    """Normalised 12-bin pitch-class energy from the average spectrum."""
    freqs, power = average_power(x, sr)
    chroma = np.zeros(12)
    valid = freqs > 20
    pcs = np.round(12 * np.log2((freqs[valid] + EPS) / 440.0) + 9).astype(int) % 12
    np.add.at(chroma, pcs, power[valid])
    total = float(np.sum(chroma)) + EPS
    return chroma / total


def estimate_key(x: np.ndarray, sr: int):
    """Return (key_name, mode, confidence) via Krumhansl key-profile correlation."""
    chroma = chroma_vector(x, sr)
    best = (None, None, -2.0)
    for shift in range(12):
        rolled = np.roll(chroma, -shift)
        for mode, profile in (("major", _KK_MAJOR), ("minor", _KK_MINOR)):
            corr = float(np.corrcoef(rolled, profile)[0, 1])
            if corr > best[2]:
                best = (_PITCH_CLASSES[shift], mode, corr)
    return best[0], best[1], round(best[2], 3)


# --------------------------------------------------------------------------- #
# Stereo descriptors
# --------------------------------------------------------------------------- #
def stereo_width(samples: np.ndarray) -> float:
    """0.0 (mono / fully correlated) .. ~1.0 (very wide). Side/Mid energy."""
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim == 1 or x.shape[1] < 2:
        return 0.0
    left, right = x[:, 0], x[:, 1]
    mid = (left + right) * 0.5
    side = (left - right) * 0.5
    width = rms(side) / (rms(mid) + EPS)
    return round(float(min(width, 1.5)) / 1.5, 4)


def phase_correlation(samples: np.ndarray) -> float:
    """Pearson correlation of L/R, range -1..1. Mono returns 1.0."""
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim == 1 or x.shape[1] < 2:
        return 1.0
    left, right = x[:, 0], x[:, 1]
    if np.std(left) < EPS or np.std(right) < EPS:
        return 1.0
    corr = float(np.corrcoef(left, right)[0, 1])
    if math.isnan(corr):
        return 1.0
    return round(corr, 4)


def mono_collapse_loss_db(samples: np.ndarray) -> float:
    """Level drop when summed to mono (dB). Large negative = mono risk.

    Compares the mono sum ``(L+R)/2`` against the per-channel level. Fully
    correlated content loses nothing (~0 dB); anti-correlated content cancels
    and drops sharply.
    """
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim == 1 or x.shape[1] < 2:
        return 0.0
    left, right = x[:, 0], x[:, 1]
    channel_level = 0.5 * (rms(left) + rms(right))
    mono = (left + right) * 0.5
    drop = rms_dbfs(mono) - db_from_amplitude(channel_level)
    return round(float(drop), 3)


# --------------------------------------------------------------------------- #
# Loudness (BS.1770-ish)
# --------------------------------------------------------------------------- #
# 48 kHz K-weighting biquad coefficients (ITU-R BS.1770). Used by the scipy and
# FFT fallbacks; pyloudnorm recomputes correct coefficients per sample-rate.
_K_STAGE1_B = np.array([1.53512485958697, -2.69169618940638, 1.19839281085285])
_K_STAGE1_A = np.array([1.0, -1.69065929318241, 0.73248077421585])
_K_STAGE2_B = np.array([1.0, -2.0, 1.0])
_K_STAGE2_A = np.array([1.0, -1.99004745483398, 0.99007225036621])


def _biquad_freq_response(b: np.ndarray, a: np.ndarray, freqs: np.ndarray, sr: int) -> np.ndarray:
    # Evaluate against the 48k design grid so weighting tracks real Hz.
    w = np.exp(-1j * 2.0 * np.pi * freqs / 48000.0)
    num = b[0] + b[1] * w + b[2] * w ** 2
    den = a[0] + a[1] * w + a[2] * w ** 2
    return np.abs(num / den)


def integrated_loudness(samples: np.ndarray, sr: int) -> float:
    """Integrated loudness in LUFS.

    Prefers pyloudnorm, then a scipy BS.1770 implementation, then an FFT-domain
    K-weighted estimate. The estimate is labelled as such in reports.
    """
    x = np.asarray(samples, dtype=np.float64)
    if x.size == 0:
        return -120.0

    if _HAVE_PYLN:  # pragma: no cover - depends on optional dep
        try:
            meter = _pyln.Meter(sr)
            data = x if x.ndim == 2 else x[:, None]
            return round(float(meter.integrated_loudness(data)), 2)
        except Exception:
            pass

    if _HAVE_SCIPY:  # pragma: no cover - depends on optional dep
        try:
            return round(_loudness_scipy(x, sr), 2)
        except Exception:
            pass

    return round(_loudness_fft(x, sr), 2)


def _loudness_scipy(x: np.ndarray, sr: int) -> float:
    chans = x if x.ndim == 2 else x[:, None]
    weighted = np.zeros_like(chans)
    for c in range(chans.shape[1]):
        y = _scipy_signal.lfilter(_K_STAGE1_B, _K_STAGE1_A, chans[:, c])
        y = _scipy_signal.lfilter(_K_STAGE2_B, _K_STAGE2_A, y)
        weighted[:, c] = y
    return _gated_loudness(weighted, sr)


def _gated_loudness(weighted: np.ndarray, sr: int) -> float:
    block = max(int(0.4 * sr), 1)
    step = max(int(0.1 * sr), 1)
    n = weighted.shape[0]
    if n < block:
        ms = float(np.mean(np.sum(weighted ** 2, axis=1)))
        return -0.691 + 10.0 * math.log10(ms + EPS)
    loud = []
    powers = []
    for start in range(0, n - block + 1, step):
        seg = weighted[start : start + block]
        ms = float(np.mean(np.sum(seg ** 2, axis=1)))
        l = -0.691 + 10.0 * math.log10(ms + EPS)
        loud.append(l)
        powers.append(ms)
    loud = np.array(loud)
    powers = np.array(powers)
    abs_mask = loud > -70.0
    if not np.any(abs_mask):
        return float(np.max(loud))
    gated_mean_power = float(np.mean(powers[abs_mask]))
    rel_thresh = -0.691 + 10.0 * math.log10(gated_mean_power + EPS) - 10.0
    rel_mask = abs_mask & (loud > rel_thresh)
    if not np.any(rel_mask):
        rel_mask = abs_mask
    final_power = float(np.mean(powers[rel_mask]))
    return -0.691 + 10.0 * math.log10(final_power + EPS)


def _loudness_fft(x: np.ndarray, sr: int) -> float:
    mono = to_mono(x)
    freqs, power = average_power(mono, sr)
    gain = _biquad_freq_response(_K_STAGE1_B, _K_STAGE1_A, freqs, sr)
    gain *= _biquad_freq_response(_K_STAGE2_B, _K_STAGE2_A, freqs, sr)
    weighted_ms = float(np.sum(power * gain ** 2)) / (power.size + EPS)
    return -0.691 + 10.0 * math.log10(weighted_ms + EPS)


# --------------------------------------------------------------------------- #
# Mapping helpers (raw measurement -> 0..1 perceptual scales)
# --------------------------------------------------------------------------- #
def normalize(value: float, lo: float, hi: float) -> float:
    """Clamp+scale a value from [lo, hi] into [0, 1]."""
    if hi <= lo:
        return 0.0
    return round(float(max(0.0, min(1.0, (value - lo) / (hi - lo)))), 4)


def brightness_from_centroid(centroid_hz: float) -> float:
    """Map spectral centroid to a 0..1 brightness scale (log-ish)."""
    # ~200 Hz reads dark, ~6 kHz reads very bright.
    c = max(centroid_hz, 1.0)
    return normalize(math.log10(c), math.log10(200.0), math.log10(6000.0))
