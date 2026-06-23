"""Audio loading with a hard dependency only on numpy.

Uses ``soundfile`` when available (broad format support). Falls back to the
stdlib :mod:`wave` module for PCM WAV (8/16/24/32-bit), which is enough for
exported Logic stems. Returns float64 samples normalised to roughly [-1, 1].
"""

from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

try:
    import soundfile as _sf  # type: ignore

    _HAVE_SF = True
except Exception:  # pragma: no cover - exercised only without soundfile
    _sf = None
    _HAVE_SF = False


@dataclass
class LoadedAudio:
    """A decoded stem. ``samples`` is (n,) mono or (n, channels)."""

    samples: np.ndarray
    sample_rate: int
    path: Optional[str] = None

    @property
    def channels(self) -> int:
        return 1 if self.samples.ndim == 1 else int(self.samples.shape[1])

    @property
    def num_frames(self) -> int:
        return int(self.samples.shape[0])

    @property
    def duration(self) -> float:
        return self.num_frames / float(self.sample_rate) if self.sample_rate else 0.0

    def slice_seconds(self, start: float, end: Optional[float] = None) -> np.ndarray:
        """Return the samples between ``start`` and ``end`` (seconds)."""
        a = max(0, int(round(start * self.sample_rate)))
        b = self.num_frames if end is None else min(self.num_frames, int(round(end * self.sample_rate)))
        if b <= a:
            b = min(self.num_frames, a + 1)
        return self.samples[a:b]


def load_audio(path: str | Path) -> LoadedAudio:
    """Load any supported audio file into a :class:`LoadedAudio`."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    if _HAVE_SF:
        data, sr = _sf.read(str(path), dtype="float64", always_2d=False)
        samples = np.asarray(data, dtype=np.float64)
        return LoadedAudio(samples=samples, sample_rate=int(sr), path=str(path))

    return _load_wav_stdlib(path)


def _load_wav_stdlib(path: Path) -> LoadedAudio:
    with wave.open(str(path), "rb") as wf:
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        sr = wf.getframerate()
        n = wf.getnframes()
        raw = wf.readframes(n)

    samples = _pcm_bytes_to_float(raw, sampwidth)
    if channels > 1:
        samples = samples.reshape(-1, channels)
    return LoadedAudio(samples=samples, sample_rate=int(sr), path=str(path))


def _pcm_bytes_to_float(raw: bytes, sampwidth: int) -> np.ndarray:
    """Decode interleaved PCM bytes into float64 in [-1, 1]."""
    if sampwidth == 1:  # unsigned 8-bit
        arr = np.frombuffer(raw, dtype=np.uint8).astype(np.float64)
        return (arr - 128.0) / 128.0
    if sampwidth == 2:  # signed 16-bit
        arr = np.frombuffer(raw, dtype="<i2").astype(np.float64)
        return arr / 32768.0
    if sampwidth == 3:  # signed 24-bit little-endian
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        val = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
        val = np.where(val >= (1 << 23), val - (1 << 24), val)
        return val.astype(np.float64) / float(1 << 23)
    if sampwidth == 4:  # signed 32-bit
        arr = np.frombuffer(raw, dtype="<i4").astype(np.float64)
        return arr / float(1 << 31)
    raise ValueError(f"Unsupported PCM sample width: {sampwidth} bytes")
