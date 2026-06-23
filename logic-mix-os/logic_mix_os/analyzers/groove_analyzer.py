"""Groove analyzer (build packet section 25.2).

Estimates rhythmic tightness of the rhythm-section stems from inter-onset
interval regularity. High regularity = machine-tight; lower = human feel. The
doctrine does not assume tighter is better — it reports the feel.
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from .. import dsp
from .audio_loader import LoadedAudio

RHYTHM_IDENTITIES = {"kick", "snare", "hi_hat", "percussion", "drum_room", "overhead"}


def analyze_groove(rhythm_tracks: List[Dict]) -> Dict:
    """``rhythm_tracks`` = list of {name, identity, loaded: LoadedAudio}."""
    per_track: List[Dict] = []
    regularities: List[float] = []

    for t in rhythm_tracks:
        loaded: LoadedAudio = t["loaded"]
        onsets = dsp.onset_times_sec(loaded.samples, loaded.sample_rate)
        if len(onsets) < 3:
            per_track.append({"track": t["name"], "onsets": len(onsets), "regularity": None,
                              "feel": "too few onsets to judge"})
            continue
        iois = np.diff(onsets)
        mean_ioi = float(np.mean(iois)) or 1e-9
        cv = float(np.std(iois) / mean_ioi)  # coefficient of variation
        regularity = round(max(0.0, 1.0 - cv), 3)
        regularities.append(regularity)
        feel = "machine-tight" if regularity > 0.85 else ("steady with feel" if regularity > 0.6 else "loose / human")
        per_track.append({"track": t["name"], "onsets": len(onsets), "regularity": regularity, "feel": feel})

    overall = round(float(np.mean(regularities)), 3) if regularities else None
    return {
        "per_track": per_track,
        "overall_regularity": overall,
        "summary": (
            "No rhythm stems detected." if not rhythm_tracks
            else f"Overall groove regularity {overall} ({'tight' if (overall or 0) > 0.8 else 'human'})."
        ),
    }
