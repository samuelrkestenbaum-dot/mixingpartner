"""Deterministic synthetic fixtures for Logic Mix OS.

Generates three small test projects (stems + manifest) so the test-suite and the
README examples work without shipping large binary audio. Everything is seeded,
so the output is byte-stable across runs.

Run directly to (re)generate:  ``python fixtures/generate_fixtures.py``
The test ``conftest.py`` calls :func:`ensure_fixtures` automatically.
"""

from __future__ import annotations

import json
import wave
from pathlib import Path
from typing import Dict, List

import numpy as np

SR = 32000
DUR = 3.0  # seconds per section
HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------------- #
# Low-level synthesis helpers
# --------------------------------------------------------------------------- #
def _t(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def _norm(x: np.ndarray, gain: float = 1.0) -> np.ndarray:
    peak = float(np.max(np.abs(x))) or 1.0
    return gain * x / peak


def _silence(dur: float, stereo: bool = False) -> np.ndarray:
    n = int(dur * SR)
    return np.zeros((n, 2)) if stereo else np.zeros(n)


def _chord(freqs, dur, partials, decay, gain=0.7) -> np.ndarray:
    t = _t(dur)
    sig = np.zeros(t.size)
    for f in freqs:
        for h, a in partials:
            sig += a * np.sin(2 * np.pi * f * h * t)
    sig *= np.exp(-decay * t) if decay > 0 else (0.3 + 0.7 * np.minimum(1.0, t / 0.4))
    return _norm(sig, gain)


def _stereoize(mono: np.ndarray, rng: np.random.Generator, width: float) -> np.ndarray:
    """Make a stereo pair with controllable decorrelation (0=mono, 1=very wide)."""
    n = mono.size
    side = rng.standard_normal(n) * width * 0.6
    side = np.convolve(side, np.ones(64) / 64, mode="same")  # smooth the side
    left = mono + side
    right = mono - side
    return np.column_stack([left, right])


def _vocal(dur, base, rng, gain=0.6) -> np.ndarray:
    t = _t(dur)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5 * t)
    sig = np.zeros(t.size)
    for h, a in [(1, 1.0), (2, 0.6), (3, 0.3), (4, 0.12)]:
        sig += a * np.sin(2 * np.pi * base * h * t * vib)
    breath = 0.03 * rng.standard_normal(t.size)
    env = 0.45 + 0.55 * np.sin(2 * np.pi * 0.6 * t) ** 2
    return _norm((sig + breath) * env, gain)


def _bass(dur, freqs, gain=0.7) -> np.ndarray:
    t = _t(dur)
    sig = np.zeros(t.size)
    seg = t.size // max(1, len(freqs))
    for i, f in enumerate(freqs):
        s, e = i * seg, (i + 1) * seg
        tt = t[s:e] - t[s]
        note = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)
        sig[s:e] = note * np.exp(-2.0 * tt)
    return _norm(sig, gain)


def _kick(dur, bpm=92, gain=0.85) -> np.ndarray:
    t = _t(dur)
    sig = np.zeros(t.size)
    beat = 60.0 / bpm
    for start in np.arange(0, dur, beat):
        i = int(start * SR)
        tt = _t(0.25)
        body = np.sin(2 * np.pi * (110 * np.exp(-tt * 30) + 45) * tt) * np.exp(-tt * 18)
        end = min(i + tt.size, sig.size)
        sig[i:end] += body[: end - i]
    return _norm(sig, gain)


def _snare(dur, bpm=92, rng=None, gain=0.7) -> np.ndarray:
    rng = rng or np.random.default_rng(0)
    sig = np.zeros(int(dur * SR))
    beat = 60.0 / bpm
    for start in np.arange(beat, dur, 2 * beat):  # backbeat
        i = int(start * SR)
        tt = _t(0.2)
        noise = rng.standard_normal(tt.size) * np.exp(-tt * 22)
        tone = 0.4 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 22)
        end = min(i + tt.size, sig.size)
        sig[i:end] += (noise + tone)[: end - i]
    return _norm(sig, gain)


def _texture_loop(dur, rng, gain=0.8) -> np.ndarray:
    """Bright, full-width, pre-mastered-feeling shimmer (low crest factor).

    Left and right are synthesised independently (different partial phases and
    noise), giving a genuinely decorrelated, very wide image — exactly the kind
    of stock-loop stereo field the doctrine warns about.
    """
    t = _t(dur)

    def one_side() -> np.ndarray:
        s = np.zeros(t.size)
        for f in [3200, 4800, 6400, 8200, 9600]:
            s += np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28))
        nz = rng.standard_normal(t.size)
        nz = nz - np.convolve(nz, np.ones(8) / 8, mode="same")  # crude high-pass
        return np.tanh(_norm(s + 0.5 * nz, 1.0) * 3.0)  # soft-clip -> mastered

    stereo = np.column_stack([one_side(), one_side()])
    return _norm(stereo, gain)


# --------------------------------------------------------------------------- #
# WAV writer (stdlib, 16-bit PCM)
# --------------------------------------------------------------------------- #
def write_wav(path: Path, samples: np.ndarray) -> None:
    samples = np.clip(np.asarray(samples, dtype=np.float64), -1.0, 1.0)
    int16 = (samples * 32767.0).astype("<i2")
    nch = 1 if int16.ndim == 1 else int16.shape[1]
    data = int16.tobytes()  # (n,2) C-order flatten = interleaved L,R
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(nch)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(data)


def _concat(segments: List[np.ndarray]) -> np.ndarray:
    # ensure consistent channel count
    stereo = any(s.ndim == 2 for s in segments)
    fixed = []
    for s in segments:
        if stereo and s.ndim == 1:
            s = np.column_stack([s, s])
        fixed.append(s)
    return np.concatenate(fixed, axis=0)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
def _two_sections() -> List[Dict]:
    return [
        {"section_id": "verse_1", "name": "Verse 1", "start_time": "0:00", "end_time": "0:03", "emotional_goal": "intimacy"},
        {"section_id": "chorus_1", "name": "Chorus 1", "start_time": "0:03", "end_time": "0:06", "emotional_goal": "release"},
    ]


def build_simple_vocal_piano(rng: np.random.Generator) -> Dict:
    stems = {
        "Lead Vocal": _concat([_vocal(DUR, 220, rng, 0.55), _vocal(DUR, 330, rng, 0.7)]),
        "Piano": _concat([
            _stereoize(_chord([261, 329, 392], DUR, [(1, 1), (2, 0.5), (4, 0.2)], 2.5, 0.6), rng, 0.3),
            _stereoize(_chord([293, 369, 440], DUR, [(1, 1), (2, 0.5), (4, 0.2)], 2.5, 0.7), rng, 0.3),
        ]),
        "Bass": _concat([_silence(DUR), _bass(DUR, [73, 82, 98, 110], 0.7)]),
    }
    manifest = {
        "project": {"song_title": "Simple Vocal Piano", "tempo": 92, "key": "E major", "sample_rate": SR, "bit_depth": 16},
        "intent": {
            "singular_emotional_truth": "Intimate in the verse, opening up in the chorus.",
            "references": [],
            "negative_constraints": ["Do not make the vocal glossy."],
        },
        "sections": _two_sections(),
        "tracks": [
            {"file": "Lead Vocal.wav", "name": "Lead Vocal", "source_kind": "comped_audio_track"},
            {"file": "Piano.wav", "name": "Piano"},
            {"file": "Bass.wav", "name": "Bass"},
        ],
    }
    return {"name": "simple_vocal_piano_song", "stems": stems, "manifest": manifest}


def build_dense_chorus_with_loops(rng: np.random.Generator) -> Dict:
    g_part = [(1, 1), (2, 0.6), (3, 0.4), (5, 0.2)]
    stems = {
        "Lead Vocal": _concat([_vocal(DUR, 246, rng, 0.55), _vocal(DUR, 370, rng, 0.7)]),
        "Acoustic Guitar": _stereoize(_chord([196, 246, 392], 2 * DUR, g_part, 2.0, 0.6), rng, 0.7),
        "Electric Guitar 1": _stereoize(_chord([164, 246, 330], 2 * DUR, g_part, 1.6, 0.6), rng, 0.8),
        "Electric Guitar 2": _stereoize(_chord([220, 277, 415], 2 * DUR, g_part, 1.6, 0.6), rng, 0.85),
        "Synth Pad": _stereoize(_chord([130, 196, 246, 330], 2 * DUR, [(1, 1), (2, 0.7), (3, 0.5)], 0.0, 0.5), rng, 1.1),
        "Splice Texture Loop": _texture_loop(2 * DUR, rng, 0.8),
        "Bass": _bass(2 * DUR, [82, 98, 110, 123, 82, 98, 110, 123], 0.7),
        "Kick": _concat([_silence(DUR), _kick(DUR, 92, 0.85)]),
        "Snare": _concat([_silence(DUR), _snare(DUR, 92, rng, 0.7)]),
    }
    manifest = {
        "project": {"song_title": "Dense Chorus With Loops", "tempo": 92, "key": "E minor", "sample_rate": SR, "bit_depth": 16},
        "intent": {
            "singular_emotional_truth": "A big chorus that must not bury the vocal.",
            "references": [],
            "negative_constraints": ["Do not let the chorus become a wall of sound.", "Do not let stock loops dominate the song identity."],
        },
        "sections": _two_sections(),
        "tracks": [
            {"file": "Lead Vocal.wav", "name": "Lead Vocal", "source_kind": "comped_audio_track"},
            {"file": "Acoustic Guitar.wav", "name": "Acoustic Guitar"},
            {"file": "Electric Guitar 1.wav", "name": "Electric Guitar 1"},
            {"file": "Electric Guitar 2.wav", "name": "Electric Guitar 2"},
            {"file": "Synth Pad.wav", "name": "Synth Pad"},
            {"file": "Splice Texture Loop.wav", "name": "Splice Texture Loop"},
            {"file": "Bass.wav", "name": "Bass"},
            {"file": "Kick.wav", "name": "Kick"},
            {"file": "Snare.wav", "name": "Snare"},
        ],
    }
    return {"name": "dense_chorus_with_loops", "stems": stems, "manifest": manifest}


def build_splice_loop_problem(rng: np.random.Generator) -> Dict:
    stems = {
        "Lead Vocal": _concat([_vocal(DUR, 196, rng, 0.5), _vocal(DUR, 261, rng, 0.6)]),
        "Splice Loop": _texture_loop(2 * DUR, rng, 0.92),  # loud, bright, wide, foregrounded
        "Acoustic Guitar": _stereoize(_chord([196, 246, 294], 2 * DUR, [(1, 1), (2, 0.5)], 2.2, 0.45), rng, 0.4),
    }
    manifest = {
        "project": {"song_title": "Splice Loop Problem", "tempo": 100, "key": "G major", "sample_rate": SR, "bit_depth": 16},
        "intent": {
            "singular_emotional_truth": "A personal song the loop is currently steamrolling.",
            "references": [],
            "negative_constraints": ["Do not let the loop dominate the song identity."],
        },
        "sections": _two_sections(),
        "tracks": [
            {"file": "Lead Vocal.wav", "name": "Lead Vocal", "source_kind": "comped_audio_track"},
            {"file": "Splice Loop.wav", "name": "Splice Loop"},
            {"file": "Acoustic Guitar.wav", "name": "Acoustic Guitar"},
        ],
    }
    return {"name": "splice_loop_problem", "stems": stems, "manifest": manifest}


def _write_fixture(base: Path, fixture: Dict) -> None:
    fx_dir = base / fixture["name"]
    stems_dir = fx_dir / "stems"
    stems_dir.mkdir(parents=True, exist_ok=True)
    for name, samples in fixture["stems"].items():
        write_wav(stems_dir / f"{name}.wav", samples)
    with open(fx_dir / "project_manifest.json", "w", encoding="utf-8") as fh:
        json.dump(fixture["manifest"], fh, indent=2)
        fh.write("\n")


def generate_all(base: Path = HERE) -> List[str]:
    builders = [build_simple_vocal_piano, build_dense_chorus_with_loops, build_splice_loop_problem]
    written = []
    for i, builder in enumerate(builders):
        rng = np.random.default_rng(1000 + i)
        fixture = builder(rng)
        _write_fixture(base, fixture)
        written.append(fixture["name"])
    return written


def ensure_fixtures(base: Path = HERE) -> None:
    """Generate fixtures only if their stems are missing."""
    builders = {
        "simple_vocal_piano_song": ["Lead Vocal.wav", "Piano.wav", "Bass.wav"],
        "dense_chorus_with_loops": ["Lead Vocal.wav", "Splice Texture Loop.wav"],
        "splice_loop_problem": ["Lead Vocal.wav", "Splice Loop.wav"],
    }
    missing = False
    for name, files in builders.items():
        for f in files:
            if not (base / name / "stems" / f).exists():
                missing = True
    if missing:
        generate_all(base)


if __name__ == "__main__":
    names = generate_all()
    print("Generated fixtures:", ", ".join(names))
