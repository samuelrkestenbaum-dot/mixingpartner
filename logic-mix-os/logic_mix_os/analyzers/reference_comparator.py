"""Reference comparator.

Analyses a reference track the same way as the user's bounce and reports the
deltas, so the reference can be used for the *relevant* traits and ignored for
the irrelevant ones (build packet section 24 / 69).
"""

from __future__ import annotations

from typing import Dict

from .audio_loader import LoadedAudio
from .audio_metrics import compute_metrics


def compare_to_reference(bounce: LoadedAudio, reference: LoadedAudio) -> Dict:
    mine = compute_metrics(bounce.samples, bounce.sample_rate)
    ref = compute_metrics(reference.samples, reference.sample_rate)

    band_delta = {
        b: round(mine["band_energy"][b] - ref["band_energy"][b], 4)
        for b in mine["band_energy"]
    }
    notes = _notes(mine, ref, band_delta)

    return {
        "overall_lufs_delta": round(mine["estimated_lufs"] - ref["estimated_lufs"], 2),
        "my_lufs": mine["estimated_lufs"],
        "reference_lufs": ref["estimated_lufs"],
        "crest_factor_delta_db": round(mine["crest_factor_db"] - ref["crest_factor_db"], 2),
        "stereo_width_delta": round(mine["stereo_width"] - ref["stereo_width"], 4),
        "brightness_delta": round(mine["brightness"] - ref["brightness"], 4),
        "spectral_centroid_delta_hz": round(mine["spectral_centroid"] - ref["spectral_centroid"], 1),
        "band_balance_delta": band_delta,
        "mono_compatibility": {
            "my_mix_db": mine["mono_collapse_loss_db"],
            "reference_db": ref["mono_collapse_loss_db"],
        },
        "notes": notes,
    }


def _notes(mine: Dict, ref: Dict, band_delta: Dict) -> list:
    notes = []
    lufs_d = mine["estimated_lufs"] - ref["estimated_lufs"]
    if lufs_d < -2:
        notes.append(f"My mix is ~{abs(lufs_d):.1f} LU quieter than the reference (do not chase loudness at mix stage).")
    elif lufs_d > 2:
        notes.append(f"My mix is ~{lufs_d:.1f} LU louder than the reference.")

    if mine["brightness"] - ref["brightness"] < -0.1:
        notes.append("My mix is darker than the reference — but only brighten if it serves the song, not to match.")
    elif mine["brightness"] - ref["brightness"] > 0.1:
        notes.append("My mix is brighter than the reference; watch for harshness/modern glare.")

    if mine["stereo_width"] - ref["stereo_width"] < -0.1:
        notes.append("Reference is wider; consider arrangement/placement width rather than artificial widening.")

    if band_delta.get("low", 0) < -0.05:
        notes.append("Less low-end energy than the reference; check kick/bass foundation.")
    if not notes:
        notes.append("My mix is broadly in the reference's territory on the measured traits.")
    return notes
