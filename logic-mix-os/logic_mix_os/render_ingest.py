"""Ground-truth render ingest (Hardening Packet 3, Layer 2).

Accepts an externally produced render (e.g. a real Logic bounce — a WAV produced
elsewhere; Logic is NOT required here), validates it, gives it a durable metadata
record, links it to a governance receipt, and compares it against the base and
the offline-approximation render to calibrate how trustworthy the offline
renderer's predictions are.

Read-only on inputs: it loads WAVs and writes only its own metadata/report.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

from . import dsp
from .analyzers.audio_loader import load_audio
from .analyzers.audio_metrics import compute_metrics
from .analyzers.translation_analyzer import analyze_translation
from .governance_kernel import GovernanceKernel
from .variant_renderer import loudness_match

_EPS = 1e-4
# metric -> +1 if "higher is better", -1 if "lower is better", 0 if neutral/contextual
_GOODNESS = {"translation": +1, "vocal_presence": +1, "mono_collapse_loss_db": +1,
             "lufs": 0, "stereo_width": 0, "brightness": 0, "density": 0}


def _metrics_view(m: Dict) -> Dict:
    return {
        "lufs": m["estimated_lufs"],
        "stereo_width": m["stereo_width"],
        "brightness": m["brightness"],
        "density": m["density"],
        "mono_collapse_loss_db": m["mono_collapse_loss_db"],
        "vocal_presence": m["vocal_presence_energy"],
        "translation": analyze_translation(m, [])["translation_score"],
    }


def _delta(a: Dict, b: Dict) -> Dict:
    return {k: round(b[k] - a[k], 4) for k in a}


def _sign(x: float) -> int:
    return 0 if abs(x) < _EPS else (1 if x > 0 else -1)


def ingest_render(wav: str, base_wav: Optional[str] = None, offline_wav: Optional[str] = None,
                  link: Optional[str] = None, store_dir: Optional[str] = None,
                  kernel: Optional[GovernanceKernel] = None) -> Dict:
    try:
        ext = load_audio(wav)
    except Exception as exc:
        return {"error": f"could not load render '{wav}': {exc}"}

    ext_m = compute_metrics(ext.samples, ext.sample_rate)
    render_id = "rnd_" + hashlib.md5(f"{wav}|{ext.sample_rate}|{ext.num_frames}".encode()).hexdigest()[:8]

    kernel = kernel or GovernanceKernel()
    receipt = kernel.propose({
        "kind": "ingest_external_render",
        "reason": "Ingest an externally produced render and write a comparison report.",
        "source_artifacts": [wav],
        "target_artifacts": [f"{render_id}.json"],
        "source_immutable": True, "generated_output_only": True,
    })

    record: Dict = {
        "render_id": render_id,
        "path": str(wav),
        "link": link,
        "governance": receipt,
        "metadata": {
            "sample_rate": ext.sample_rate,
            "channels": ext.channels,
            "duration": round(ext.duration, 3),
            "peak_dbfs": ext_m["peak_dbfs"],
            "rms_dbfs": ext_m["rms_dbfs"],
            "lufs": ext_m["estimated_lufs"],
        },
        "compatibility": {"compatible": True, "issues": []},
        "comparison": {},
        "calibration": None,
    }

    base = load_audio(base_wav) if base_wav else None
    if base is not None:
        issues: List[str] = []
        if base.sample_rate != ext.sample_rate:
            issues.append(f"sample-rate mismatch: external {ext.sample_rate} vs base {base.sample_rate}")
        if abs(base.duration - ext.duration) > 0.5:
            issues.append(f"duration mismatch: external {ext.duration:.2f}s vs base {base.duration:.2f}s")
        if base.channels != ext.channels:
            issues.append(f"channel-count mismatch: external {ext.channels} vs base {base.channels}")
        record["compatibility"] = {"compatible": not issues, "issues": issues}

        base_view = _metrics_view(compute_metrics(base.samples, base.sample_rate))
        ext_view = _metrics_view(ext_m)
        matched = compute_metrics(loudness_match(ext.samples, ext.sample_rate, base_view["lufs"]), ext.sample_rate)
        record["comparison"]["external_vs_base"] = _delta(base_view, ext_view)
        record["comparison"]["loudness_matched_external_vs_base"] = _delta(base_view, _metrics_view(matched))

        if offline_wav:
            off = load_audio(offline_wav)
            off_view = _metrics_view(compute_metrics(off.samples, off.sample_rate))
            off_delta = _delta(base_view, off_view)
            ext_delta = record["comparison"]["external_vs_base"]
            record["comparison"]["offline_vs_base"] = off_delta
            record["calibration"] = _calibrate(ext_delta, off_delta)

    if store_dir:
        sd = Path(store_dir)
        sd.mkdir(parents=True, exist_ok=True)
        path = sd / f"{render_id}.json"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        record["metadata_path"] = str(path)

    return record


def _calibrate(ext_delta: Dict, off_delta: Dict) -> Dict:
    aligned, divergent = [], []
    for metric in ext_delta:
        se, so = _sign(ext_delta[metric]), _sign(off_delta[metric])
        (aligned if se == so else divergent).append(metric)

    # Optimism: did the offline renderer predict MORE "goodness" improvement than reality?
    optimism_terms = []
    for metric, good in _GOODNESS.items():
        if good and metric in ext_delta:
            optimism_terms.append(good * (off_delta[metric] - ext_delta[metric]))
    optimism = round(sum(optimism_terms) / len(optimism_terms), 4) if optimism_terms else 0.0

    predicted_correct = len(aligned) >= len(divergent)
    if predicted_correct and len(divergent) <= 1:
        verdict = "Offline approximation is directionally trustworthy for this variant type."
    elif predicted_correct:
        verdict = "Offline approximation is partly trustworthy; some metrics diverge — treat as medium-confidence."
    else:
        verdict = "Offline approximation diverged from the real render — treat as low-confidence for this variant type; calibrate."

    notes = []
    if optimism > 0.5:
        notes.append("Offline renderer is over-optimistic (predicted more improvement than the real render).")
    elif optimism < -0.5:
        notes.append("Offline renderer is under-optimistic (real render improved more than predicted).")
    else:
        notes.append("Offline optimism is roughly calibrated on goodness-direction metrics.")

    return {
        "aligned_metrics": aligned,
        "divergent_metrics": divergent,
        "optimism": optimism,
        "predicted_direction_correct": predicted_correct,
        "trust_verdict": verdict,
        "notes": notes,
    }
