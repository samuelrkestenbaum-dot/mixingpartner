"""Section analyzer.

Computes per-section metrics from the mixdown (or supplied stereo bounce) and
the section-to-section contrast that drives the "does the chorus lift?" verdict.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .. import dsp
from ..analyzers.audio_loader import LoadedAudio
from ..analyzers.audio_metrics import compute_metrics
from ..project import Section

LIFT_GOALS = {"release", "lift", "catharsis", "climax", "bloom", "open"}

# A track counts as "active" in a section if its section RMS is loud enough in
# absolute terms AND within this many dB of its own loudest section. This is what
# stops a kick that is silent in the verse from being treated as present there.
ACTIVE_ABS_FLOOR_DBFS = -55.0
ACTIVE_REL_RANGE_DB = 25.0


def analyze_sections(
    sections: List[Section],
    mixdown: LoadedAudio,
    lead_vocal: Optional[LoadedAudio] = None,
) -> List[Dict]:
    if not sections:
        return []

    duration = mixdown.duration
    bounds = _resolve_bounds(sections, duration)

    results: List[Dict] = []
    prev_metrics: Optional[Dict] = None
    for sec, (start, end) in zip(sections, bounds):
        seg = mixdown.slice_seconds(start, end)
        m = compute_metrics(seg, mixdown.sample_rate)

        section_metrics = {
            "rms_dbfs": m["rms_dbfs"],
            "lufs": m["estimated_lufs"],
            "width": m["stereo_width"],
            "brightness": m["brightness"],
            "density": m["density"],
            "low_mid_energy": m["band_energy"]["low_mid"],
            "presence_energy": m["band_energy"]["presence"],
            "transient_density": m["transient_density"],
        }
        if lead_vocal is not None:
            section_metrics["vocal_presence_db"] = _vocal_presence(
                lead_vocal, mixdown, start, end
            )

        contrast = _contrast(section_metrics, prev_metrics, sec)
        results.append(
            {
                "section_id": sec.section_id,
                "name": sec.name,
                "start_time": round(start, 3),
                "end_time": round(end, 3),
                "emotional_goal": sec.emotional_goal,
                "metrics": section_metrics,
                "contrast_vs_previous": contrast,
            }
        )
        prev_metrics = section_metrics
    return results


def resolve_section_bounds(sections: List[Section], duration: float):
    bounds = []
    for i, sec in enumerate(sections):
        start = sec.start
        if sec.end is not None:
            end = sec.end
        elif i + 1 < len(sections):
            end = sections[i + 1].start
        else:
            end = duration
        end = max(end, start + 0.05)
        bounds.append((start, min(end, duration if duration else end)))
    return bounds


# Backwards-compatible alias.
_resolve_bounds = resolve_section_bounds


def compute_section_track_metrics(
    loaded_by_id: Dict[str, LoadedAudio], sections: List[Section], duration: float
) -> Dict[str, Dict[str, Dict]]:
    """Per-track, per-section metrics computed from the actual time slices.

    Returns ``{track_id: {section_id: {band_energy, vocal_presence_energy,
    stereo_width, rms_dbfs, mud/harshness/sibilance_indicator, active}}}``.
    The ``active`` flag is what lets masking analysis ignore a stem that is
    silent in a given section (e.g. a kick that only enters at the chorus).
    """
    if not sections or not loaded_by_id:
        return {}
    bounds = resolve_section_bounds(sections, duration)
    out: Dict[str, Dict[str, Dict]] = {}
    for tid, loaded in loaded_by_id.items():
        sec_metrics: Dict[str, Dict] = {}
        for sec, (start, end) in zip(sections, bounds):
            m = compute_metrics(loaded.slice_seconds(start, end), loaded.sample_rate)
            sec_metrics[sec.section_id] = m
        max_rms = max((m["rms_dbfs"] for m in sec_metrics.values()), default=-120.0)
        per_sec: Dict[str, Dict] = {}
        for sid, m in sec_metrics.items():
            active = m["rms_dbfs"] > ACTIVE_ABS_FLOOR_DBFS and m["rms_dbfs"] > (max_rms - ACTIVE_REL_RANGE_DB)
            per_sec[sid] = {
                "band_energy": m["band_energy"],
                "vocal_presence_energy": m["vocal_presence_energy"],
                "stereo_width": m["stereo_width"],
                "rms_dbfs": m["rms_dbfs"],
                "mud_indicator": m["mud_indicator"],
                "harshness_indicator": m["harshness_indicator"],
                "sibilance_indicator": m["sibilance_indicator"],
                "active": bool(active),
            }
        out[tid] = per_sec
    return out


def _vocal_presence(
    lead_vocal: LoadedAudio, mixdown: LoadedAudio, start: float, end: float
) -> float:
    v = dsp.to_mono(lead_vocal.slice_seconds(start, end))
    mix = dsp.to_mono(mixdown.slice_seconds(start, end))
    return round(dsp.rms_dbfs(v) - dsp.rms_dbfs(mix), 2)


def _contrast(cur: Dict, prev: Optional[Dict], sec: Section) -> Dict:
    if prev is None:
        return {"note": "first analysed section; no previous section to compare."}

    rms_delta = round(cur["rms_dbfs"] - prev["rms_dbfs"], 2)
    width_delta = round(cur["width"] - prev["width"], 4)
    brightness_delta = round(cur["brightness"] - prev["brightness"], 4)
    density_delta = round(cur["density"] - prev["density"], 4)

    out = {
        "rms_delta_db": rms_delta,
        "width_delta": width_delta,
        "brightness_delta": brightness_delta,
        "density_delta": density_delta,
    }

    goal = (sec.emotional_goal or "").lower()
    is_lift = goal in LIFT_GOALS or "chorus" in sec.name.lower()
    if is_lift and rms_delta < 2.5 and width_delta < 0.05:
        out["warning"] = (
            f"{sec.name} may not lift enough relative to the previous section "
            f"(only {rms_delta:+.1f} dB and {width_delta:+.2f} width). "
            f"Target roughly +3 to +5 dB and +0.05 to +0.10 width via supporting "
            f"elements and automation, not master level."
        )
    return out
