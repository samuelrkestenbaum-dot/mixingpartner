"""Deterministic synthetic fixtures for Logic Mix OS.

Generates four small test projects (stems + manifest) so the test-suite and the
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


def _vocal_chop(dur, base, rng, bpm=96, gain=0.6) -> np.ndarray:
    """Chopped vocal one-shots on a syncopated 16th grid (P-035): a vocal-ish
    partial ladder reaching the presence band, gated by short percussive
    envelopes — transient-dense with defined, non-smeared hits."""
    t = _t(dur)
    vib = 1 + 0.01 * np.sin(2 * np.pi * 5.2 * t)
    sig = np.zeros(t.size)
    for h, a in [(1, 1.0), (2, 0.7), (4, 0.55), (6, 0.5), (8, 0.4), (10, 0.3)]:
        sig += a * np.sin(2 * np.pi * base * h * t * vib)
    step = 60.0 / bpm / 4.0
    env = np.zeros(t.size)
    n_env = int(0.09 * SR)
    shape = np.exp(-np.arange(n_env) / (0.02 * SR))
    k = -1
    for start in np.arange(0.0, dur, step):
        k += 1
        if k % 4 == 3:  # drop every 4th 16th -> syncopation
            continue
        i = int(start * SR)
        end = min(i + n_env, t.size)
        env[i:end] = np.maximum(env[i:end], shape[: end - i])
    return _norm(sig * env, gain)


def _vocal_stack(dur, freqs, rng, gain=0.6) -> np.ndarray:
    """Wide, sustained backing-vocal stack (P-035): one decaying multi-voice
    chord (no onset grid — stacks sing, they do not punch) whose upper
    partials reach the vocal presence band, stereoized wide."""
    t = _t(dur)
    sig = np.zeros(t.size)
    for f in freqs:
        for h, a in [(1, 1.0), (2, 0.6), (4, 0.4), (6, 0.38), (8, 0.3)]:
            sig += a * np.sin(2 * np.pi * f * h * t)
    sig = (sig / len(freqs)) * np.exp(-2.0 * t)
    return _stereoize(_norm(sig, gain), rng, 0.9)


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


def build_vocal_chop_groove(rng: np.random.Generator) -> Dict:
    """The 4th fixture (P-035): the vocal chain end to end on real audio.

    A groove built from voices — a lead, a chopped vocal one-shot print
    (``BGV Chop``: backing-vocal identity by name, ``one_shot_sample`` by
    manifest hint, transient-dense/high-crest by synthesis → the classifier's
    ``vocal_percussive`` at 0.95), a wide sustained stack
    (``vocal_stack`` at 0.95), a kick/snare beat, and the P-034 reviewer
    advisory's mandatory masker-set instrument: a bright electric guitar
    whose chord partials sit in the vocal presence band (1.5-4 kHz) with
    overlap >= 0.1 against both non-lead vocal stems. The guitar sits
    forward/heard in the verse (where the depth planner tucks the chop and
    stack behind it) — the placement that makes the ``vocal_band_masking``
    moderate tier, and the profile blend differential behind it, live on
    real pipeline data."""
    g_part = [(1, 1.0), (2, 0.8), (3, 0.7), (4, 0.6), (5, 0.5), (6, 0.4)]
    stems = {
        "Lead Vocal": _concat([_vocal(DUR, 220, rng, 0.55), _vocal(DUR, 330, rng, 0.7)]),
        "BGV Chop": _concat([_vocal_chop(DUR, 392, rng, 96, 0.6), _vocal_chop(DUR, 392, rng, 96, 0.68)]),
        "Backing Vocals Stack": _concat([
            _vocal_stack(DUR, [262, 330, 392], rng, 0.5),
            _vocal_stack(DUR, [294, 370, 440], rng, 0.62),
        ]),
        "Electric Guitar": _stereoize(_chord([330, 415, 494], 2 * DUR, g_part, 1.2, 0.6), rng, 0.5),
        "Kick": _kick(2 * DUR, 96, 0.85),
        "Snare": _snare(2 * DUR, 96, rng, 0.7),
    }
    manifest = {
        "project": {"song_title": "Vocal Chop Groove", "tempo": 96, "key": "A minor", "sample_rate": SR, "bit_depth": 16},
        "intent": {
            "singular_emotional_truth": "A groove built from voices: the lead sings while chopped and stacked vocals lock into the beat.",
            "references": [],
            "negative_constraints": ["Do not bury the lead vocal.", "Do not let the chopped vocals lose their rhythmic identity."],
        },
        "sections": _two_sections(),
        "tracks": [
            {"file": "Lead Vocal.wav", "name": "Lead Vocal", "source_kind": "comped_audio_track"},
            {"file": "BGV Chop.wav", "name": "BGV Chop", "source_kind": "one_shot_sample"},
            {"file": "Backing Vocals Stack.wav", "name": "Backing Vocals Stack", "source_kind": "comped_audio_track"},
            {"file": "Electric Guitar.wav", "name": "Electric Guitar"},
            {"file": "Kick.wav", "name": "Kick"},
            {"file": "Snare.wav", "name": "Snare"},
        ],
    }
    return {"name": "vocal_chop_groove", "stems": stems, "manifest": manifest}


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
    # Seeds are per-builder (1000 + index), so APPENDING a builder can never
    # shift the earlier fixtures' bytes (P-035 byte-identity discipline).
    builders = [build_simple_vocal_piano, build_dense_chorus_with_loops,
                build_splice_loop_problem, build_vocal_chop_groove]
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
        "vocal_chop_groove": ["Lead Vocal.wav", "BGV Chop.wav",
                              "Backing Vocals Stack.wav", "Electric Guitar.wav",
                              "Kick.wav", "Snare.wav"],
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
