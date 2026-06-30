"""Album-level coherence engine (build packet section 40).

Given several analysed songs, asks the core question: does this sound like one
album, or N separate productions? Reports consistency of loudness, brightness,
width, vocal placement, and the emotional/energy arc, and flags outliers.
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional


def _song_profile(name: str, result) -> Dict:
    mm = result.mix_metrics or {}
    ds = result.doctrine_score
    harm = result.expanded.get("harmonic", {})
    return {
        "name": name,
        "lufs": mm.get("estimated_lufs"),
        "brightness": mm.get("brightness"),
        "stereo_width": mm.get("stereo_width"),
        "low_energy": (mm.get("band_energy") or {}).get("low"),
        "vocal_centrality": ds.get("vocal_centrality_score"),
        "dynamic_movement": ds.get("dynamic_mix_score"),
        "detected_key": harm.get("detected_key"),
    }


def _spread(values: List[float]) -> Optional[float]:
    vals = [v for v in values if v is not None]
    return round(statistics.pstdev(vals), 4) if len(vals) > 1 else None


def analyze_album(results: List, names: Optional[List[str]] = None) -> Dict:
    names = names or [f"track_{i+1}" for i in range(len(results))]
    songs = [_song_profile(n, r) for n, r in zip(names, results)]

    lufs_spread = _spread([s["lufs"] for s in songs])
    bright_spread = _spread([s["brightness"] for s in songs])
    width_spread = _spread([s["stereo_width"] for s in songs])

    # Coherence: large spreads reduce the score.
    score = 100.0
    if lufs_spread is not None:
        score -= min(30, lufs_spread * 6)
    if bright_spread is not None:
        score -= min(30, bright_spread * 120)
    if width_spread is not None:
        score -= min(20, width_spread * 120)
    score = round(max(0.0, score), 1)

    # Outliers vs album means.
    outliers = []
    bvals = [s["brightness"] for s in songs if s["brightness"] is not None]
    lvals = [s["lufs"] for s in songs if s["lufs"] is not None]
    b_mean = statistics.mean(bvals) if bvals else None
    l_mean = statistics.mean(lvals) if lvals else None
    for s in songs:
        # Single-source the cross-song deltas: emit each song's signed delta vs the
        # album means alongside the outlier check that already uses them. ``None``
        # when the metric or its mean is unavailable (mirrors the outlier guards
        # below). Additive keys — existing output stays a strict superset, so the
        # consumer (cli.py) no longer has to recompute ``statistics.mean``.
        s["brightness_delta"] = (
            (s["brightness"] - b_mean)
            if (b_mean is not None and s["brightness"] is not None)
            else None
        )
        s["lufs_delta"] = (
            (s["lufs"] - l_mean)
            if (l_mean is not None and s["lufs"] is not None)
            else None
        )

        reasons = []
        if b_mean is not None and s["brightness"] is not None and abs(s["brightness"] - b_mean) > 0.15:
            reasons.append("brightness" if s["brightness"] > b_mean else "darkness")
        if l_mean is not None and s["lufs"] is not None and abs(s["lufs"] - l_mean) > 3:
            reasons.append("loudness")
        if reasons:
            outliers.append({"name": s["name"], "stands_out_on": reasons})

    verdict = ("Sounds like one album." if score >= 75
               else "Reads more like separate productions — tighten tonal/loudness consistency.")

    return {
        "songs": songs,
        "consistency": {
            "loudness_spread_lu": lufs_spread,
            "brightness_spread": bright_spread,
            "width_spread": width_spread,
        },
        "coherence_score": score,
        "outliers": outliers,
        "emotional_arc": [{"name": s["name"], "dynamic_movement": s["dynamic_movement"]} for s in songs],
        "verdict": verdict,
    }
