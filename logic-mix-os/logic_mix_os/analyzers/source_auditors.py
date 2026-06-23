"""Source-aware auditors (build packet sections 19, 20, 21).

Different Logic objects afford different fixes. A live vocal is a performance
(clip gain + rides before compression); a synth bounce is an arrangement actor
(filter/width/release, re-render from MIDI for notes); a Splice loop is borrowed
material that must be re-contextualised. Each auditor returns source-specific,
non-destructive recommendations grounded in the measured metrics.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS
from ..doctrine import load_doctrine

LIVE_KINDS = {"live_audio_recording", "comped_audio_track", "di_audio_track", "amp_recording"}
SYNTH_KINDS = {"software_instrument_bounce", "synth_bounce"}


def audit_all(records: List[Dict]) -> Dict:
    lead_brightness = next(
        (r["brightness"] for r in records if r["instrument_identity"] == "lead_vocal"), 0.5
    )
    audits: List[Dict] = []
    for r in records:
        sk = r["source_kind"]
        if sk in LIVE_KINDS:
            audits.append(_audit_live(r))
        elif sk in SYNTH_KINDS or r["instrument_identity"] in {"synth", "pad"}:
            audits.append(_audit_synth(r))
        elif sk in LOOP_SAMPLE_KINDS:
            audits.append(_audit_loop(r, lead_brightness))
        else:
            audits.append(_audit_generic(r))

    by_type: Dict[str, int] = {}
    for a in audits:
        by_type[a["auditor_type"]] = by_type.get(a["auditor_type"], 0) + 1
    red_flag_total = sum(len(a["red_flags"]) for a in audits)
    return {"audits": audits, "summary": {"by_type": by_type, "red_flags": red_flag_total}}


# --------------------------------------------------------------------------- #
def _base(record: Dict, auditor_type: str) -> Dict:
    m = record.get("metrics", {})
    return {
        "track": record["name"],
        "track_id": record["track_id"],
        "source_kind": record["source_kind"],
        "instrument_identity": record["instrument_identity"],
        "auditor_type": auditor_type,
        "checks": {
            "crest_factor_db": m.get("crest_factor_db"),
            "stereo_width": record.get("stereo_width"),
            "brightness": record.get("brightness"),
            "transient_density": m.get("transient_density"),
            "mud_indicator": m.get("mud_indicator"),
            "sibilance_indicator": m.get("sibilance_indicator"),
            "low_energy": record["band_energy"].get("low"),
        },
        "recommendations": [],
        "preferred_moves": [],
        "red_flags": [],
    }


def _audit_live(record: Dict) -> Dict:
    a = _base(record, "live_track")
    a["preferred_moves"] = [
        "clip gain before compression", "phrase-level rides", "light tuning only where distraction occurs",
        "preserve transient character", "use room/depth to integrate the performance",
    ]
    m = record.get("metrics", {})
    if (m.get("crest_factor_db") or 0) > 14:
        a["recommendations"].append("Inconsistent phrase energy: use clip gain + phrase rides before compression "
                                    "(do not compress harder).")
    if (m.get("sibilance_indicator") or 0) > 0.45 and record["instrument_identity"] in {"lead_vocal", "backing_vocal"}:
        a["recommendations"].append("De-ess surgically (DeEsser 2) rather than dulling the whole top.")
    a["recommendations"].append("Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.")
    return a


def _audit_synth(record: Dict) -> Dict:
    a = _base(record, "synth_patch")
    a["preferred_moves"] = [
        "automate filter cutoff by section", "shorten release if it clouds transitions",
        "narrow width if it competes with guitars/vocals", "high-pass pads when they are felt elements",
        "move pads to background", "use modulation for motion instead of adding parts",
    ]
    if record.get("stereo_width", 0) > 0.55:
        a["recommendations"].append("Narrow stereo width to ~50%; it competes with heard elements.")
    if record["instrument_identity"] == "pad" and record["band_energy"].get("low_mid", 0) > 0.3:
        a["recommendations"].append("High-pass the pad (~150-250 Hz); it is a felt element and is clouding the low-mids.")
    if record.get("brightness", 0) > 0.6:
        a["recommendations"].append("Reduce filter cutoff 1-2 kHz in verses; open it only in choruses (automate).")
    if record["source_kind"] in SYNTH_KINDS:
        a["recommendations"].append("This is a software-instrument bounce: note/patch/envelope changes require "
                                    "re-rendering from the MIDI, then print to audio for validation.")
        a["red_flags"].append("printed bounce — MIDI-level changes need a re-render")
    return a


def _audit_loop(record: Dict, lead_brightness: float) -> Dict:
    a = _base(record, "sample_loop")
    a["preferred_moves"] = load_doctrine("stereo_source_handling")["sample_loop_doctrine"]["preferred_moves"]
    width = record.get("stereo_width", 0)
    crest = record.get("metrics", {}).get("crest_factor_db", 99)
    if width > 0.55:
        a["red_flags"].append("full-width loop")
        a["recommendations"].append("Narrow to ~35%, high-pass ~250 Hz, push to background except at transitions.")
    if record.get("brightness", 0) > lead_brightness + 0.1:
        a["red_flags"].append("loop is brighter than the vocal")
    if crest < 8:
        a["red_flags"].append("mastered/compressed loop tone")
    if record["depth_default"] in {"intimate", "foreground"}:
        a["red_flags"].append("foregrounded loop")
    a["recommendations"].append("This loop is acting like a finished record inside your record. Chop into "
                                "transition gestures and re-contextualise into the song's depth, tone, and groove.")
    return a


def _audit_generic(record: Dict) -> Dict:
    a = _base(record, "generic")
    a["recommendations"].append("Treat as printed audio: gain, EQ, dynamics, depth, and automation only.")
    return a
