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

# Preferred moves for a live recording, by instrument family. Phrase rides /
# clip gain belong to performance-pitched sources (vocals, and lightly to
# guitars/keys/bass) — NOT to drums, which want transient/room/phase work.
_LIVE_MOVES = {
    "vocal": ["clip gain before compression", "phrase-level rides", "light tuning only where it distracts",
              "de-ess surgically", "integrate with shared room/depth"],
    "drums": ["transient shaping", "overhead/room balance", "phase & bleed checks", "tuning/ring control",
              "bus/parallel compression for punch", "preserve transient detail"],
    "percussion": ["balance level and panning", "control room/bleed", "preserve transients", "place with depth"],
    "bass": ["gentle optical leveling for consistent sustain", "complementary EQ vs the kick",
             "source-tone shaping", "preserve note definition"],
    "guitars": ["set source tone first", "control noise/handling", "light leveling (not heavy compression)",
                "preserve pick/strum transients", "place with depth"],
    "keys": ["harmonic support", "control low-mids", "preserve performance dynamics/pedal", "place with depth"],
    "strings": ["sustained support", "control low-mids", "shared room and depth"],
    "default": ["set source tone", "control noise", "light leveling before compression", "place with depth"],
}


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
        "identity_family": record.get("identity_family"),
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


def _drum_recs(ident: str, harsh: float) -> List[str]:
    """Drum-appropriate advice — never phrase rides / 'phrase energy'."""
    recs: List[str] = []
    if ident == "kick":
        recs.append("Define sub vs beater (~50-70 Hz vs 2-5 kHz); check kick/overhead phase; leave headroom for the bass.")
    elif ident == "snare":
        recs.append("Control ring/tuning and balance top vs bottom; check the snare's phase in the overheads.")
    elif ident in {"hi_hat", "cymbal"}:
        recs.append("High-pass spill and tame harshness gently; preserve transient sheen.")
    elif ident in {"overhead", "drum_room"}:
        recs.append("Set the kit's depth and width here and check phase against the close mics — this is where the Halee room lives.")
    else:
        recs.append("Shape transients and balance room/overheads; preserve punch.")
    if harsh > 0.45 and ident in {"hi_hat", "cymbal", "overhead", "drum_room"}:
        recs.append("Smooth 2-4 kHz harshness rather than dulling the whole top.")
    recs.append("Use bus/parallel compression for punch instead of squashing the transients.")
    return recs


def _audit_live(record: Dict) -> Dict:
    """Live-recording audit, branched by instrument family.

    A live recording is a performance, but the *right* performance fix depends on
    what it is: vocals want phrase rides + clip gain before compression; drums
    want transient/room/phase work (not rides); bass wants sustain consistency;
    guitars/keys want source tone + light leveling.
    """
    a = _base(record, "live_track")
    fam = record.get("identity_family", "unknown")
    ident = record["instrument_identity"]
    m = record.get("metrics", {})
    crest = m.get("crest_factor_db") or 0.0
    sib = m.get("sibilance_indicator") or 0.0
    mud = m.get("mud_indicator") or 0.0
    harsh = m.get("harshness_indicator") or 0.0

    a["preferred_moves"] = _LIVE_MOVES.get(fam, _LIVE_MOVES["default"])
    recs: List[str] = []

    if fam == "vocal":
        if crest > 14:
            recs.append("Inconsistent phrase energy: use clip gain + phrase rides before compression "
                        "(do not compress harder).")
        if sib > 0.45:
            recs.append("De-ess surgically (DeEsser 2) rather than dulling the whole top.")
        recs.append("Keep the vocal as the emotional centre — phrase rides before heavier compression.")
    elif fam in {"drums", "percussion"}:
        recs += _drum_recs(ident, harsh)
    elif fam == "bass":
        recs.append("Even out low-end sustain with gentle optical compression (consistency, not pumping).")
        recs.append("Carve complementary low-end space against the kick rather than stacking at the same frequency.")
        if mud > 0.45:
            recs.append("Trim 200-350 Hz if the low-mids are boxy.")
    elif fam == "guitars":
        if mud > 0.45:
            recs.append("Cut 250-400 Hz low-mid build-up.")
        recs.append("Set source tone and depth before processing; preserve pick/strum transients with light "
                    "leveling, not heavy compression.")
    elif fam == "keys":
        if mud > 0.45:
            recs.append("Control 250-500 Hz where it clouds the vocal.")
        recs.append("Support harmonically; preserve performance dynamics and pedal, and place it with depth.")
    elif fam == "strings":
        recs.append("Sustained support: control low-mids and place it with shared room and depth.")
    else:
        recs.append("Set source tone, control noise, and place it with depth; light leveling before compression.")

    a["recommendations"] = recs
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
