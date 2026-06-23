"""Harmonic / melodic analyzer (build packet section 25.2).

Estimates the key from the mixdown chroma and compares it to the manifest key,
plus a coarse harmonic-stability read. This is advisory context, not a music
theory engine.
"""

from __future__ import annotations

import re
from typing import Dict, Optional

from .. import dsp
from .audio_loader import LoadedAudio

_KEY_RE = re.compile(r"([A-Ga-g][#b]?)\s*(maj(or)?|min(or)?|m)?", re.IGNORECASE)
_FLAT_TO_SHARP = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
_PC_INDEX = {n: i for i, n in enumerate(
    ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
)}


def _is_relative(expected_root, expected_mode, detected_root, detected_mode) -> bool:
    """E minor and G major are the same notes — treat as consistent."""
    if expected_root not in _PC_INDEX or detected_root not in _PC_INDEX:
        return False
    ei, di = _PC_INDEX[expected_root], _PC_INDEX[detected_root]
    if expected_mode == "minor" and detected_mode == "major":
        return di == (ei + 3) % 12
    if expected_mode == "major" and detected_mode == "minor":
        return di == (ei - 3) % 12
    return False


def _parse_manifest_key(key: Optional[str]):
    if not key:
        return None, None
    m = _KEY_RE.match(key.strip())
    if not m:
        return None, None
    raw = m.group(1)
    root = raw[0].upper() + raw[1:]  # e.g. "e" -> "E", "bb" -> "Bb"
    root = _FLAT_TO_SHARP.get(root, root)
    mode = "minor" if (m.group(2) or "").lower() in {"min", "minor", "m"} else "major"
    return root, mode


def analyze_harmony(mixdown: Optional[LoadedAudio], manifest_key: Optional[str]) -> Dict:
    if mixdown is None:
        return {"available": False, "summary": "No mixdown for harmonic analysis."}

    detected_root, detected_mode, confidence = dsp.estimate_key(mixdown.samples, mixdown.sample_rate)
    expected_root, expected_mode = _parse_manifest_key(manifest_key)

    match = None
    relative = False
    if expected_root:
        exact = (detected_root == expected_root and detected_mode == expected_mode)
        relative = _is_relative(expected_root, expected_mode, detected_root, detected_mode)
        match = exact or relative

    note = f"Detected key ~{detected_root} {detected_mode} (confidence {confidence})."
    if expected_root:
        note += f" Manifest says {expected_root} {expected_mode}."
        if relative:
            note += " Consistent (relative major/minor — same notes)."
        elif match:
            note += " Consistent."
        else:
            note += " Detected key differs from the manifest — verify tuning/voicing or the manifest."

    return {
        "available": True,
        "detected_key": f"{detected_root} {detected_mode}",
        "detected_confidence": confidence,
        "manifest_key": manifest_key,
        "matches_manifest": match,
        "summary": note,
    }
