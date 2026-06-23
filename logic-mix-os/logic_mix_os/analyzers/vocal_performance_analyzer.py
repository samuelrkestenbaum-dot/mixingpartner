"""Vocal performance analyzer (build packet section 25.4).

Reads the lead-vocal stem for phrase-energy variation, dynamic range, sibilance,
and where the singer pushes vs pulls back — the inputs to phrase-level rides
(Ramone) rather than heavier compression.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from .. import dsp
from .audio_loader import LoadedAudio


def analyze_vocal(vocal: Optional[LoadedAudio], metrics: Optional[Dict]) -> Dict:
    if vocal is None:
        return {"available": False, "summary": "No identified lead vocal."}

    times, env_db = dsp.rms_envelope(vocal.samples, vocal.sample_rate, win=0.08)
    # Ignore silence/very-low frames when describing dynamics.
    active = env_db[env_db > (np.max(env_db) - 30)]
    if active.size < 2:
        active = env_db
    p95 = float(np.percentile(active, 95))
    p5 = float(np.percentile(active, 5))
    dynamic_range = round(p95 - p5, 2)
    variation = round(float(np.std(active)), 2)

    # Push / pull moments: loudest and quietest active windows.
    loud_idx = int(np.argmax(env_db))
    quiet_active = np.where(env_db > (np.max(env_db) - 30), env_db, np.inf)
    quiet_idx = int(np.argmin(quiet_active))

    sib = (metrics or {}).get("sibilance_indicator", 0.0)

    recommendations = []
    if dynamic_range > 18:
        recommendations.append("Wide phrase-to-phrase dynamics: use clip gain + rides before compression to even it out.")
    elif dynamic_range < 6:
        recommendations.append("Very even delivery: may already be compressed/performed flat; avoid over-compressing further.")
    if sib > 0.45:
        recommendations.append("Sibilance is elevated: de-ess surgically (DeEsser 2), don't dull the whole top.")
    if not recommendations:
        recommendations.append("Balanced delivery: light stabilisation and phrase rides should be enough.")

    return {
        "available": True,
        "dynamic_range_db": dynamic_range,
        "phrase_energy_variation_db": variation,
        "push_moment_sec": round(float(times[loud_idx]), 2),
        "pull_back_moment_sec": round(float(times[quiet_idx]), 2),
        "sibilance_indicator": round(sib, 3),
        "recommendations": recommendations,
        "summary": f"Vocal dynamic range ~{dynamic_range} dB; "
                   f"{'wide, ride it' if dynamic_range > 18 else 'controlled'}.",
    }
