"""Role classification: musical role, felt-vs-heard, and sacred-vs-expendable.

Identity answers *what is this sound*; this module answers *what is it doing*
and *how much does it matter* — the inputs the depth planner and doctrine
engine need so dense arrangements get hierarchy instead of more EQ.
"""

from __future__ import annotations

from typing import Dict, Optional

from ..constants import LOOP_SAMPLE_KINDS

# identity -> (musical_role, perceptual_role, sacredness)
_DEFAULTS = {
    "lead_vocal": ("emotional_center", "heard", "sacred"),
    "backing_vocal": ("harmonic_support", "heard", "important"),
    "kick": ("transient_anchor", "structural", "important"),
    "snare": ("transient_anchor", "structural", "important"),
    "hi_hat": ("rhythmic_drive", "structural", "useful"),
    "cymbal": ("rhythmic_drive", "structural", "useful"),
    "overhead": ("glue", "felt", "useful"),
    "drum_room": ("glue", "felt", "useful"),
    "percussion": ("groove_support", "felt", "useful"),
    "bass_guitar": ("low_end_foundation", "structural", "important"),
    "synth_bass": ("low_end_foundation", "structural", "important"),
    "acoustic_guitar": ("harmonic_support", "heard", "important"),
    "electric_guitar": ("harmonic_support", "heard", "important"),
    "piano": ("harmonic_support", "heard", "important"),
    "electric_piano": ("harmonic_support", "heard", "useful"),
    "organ": ("harmonic_support", "felt", "useful"),
    "strings": ("atmosphere", "felt", "useful"),
    "pad": ("atmosphere", "felt", "decorative"),
    "synth": ("texture", "heard", "useful"),
    "loop": ("texture", "felt", "decorative"),
    "texture": ("texture", "felt", "decorative"),
    "fx": ("transition", "transitional", "useful"),
    "unknown": ("glue", "felt", "useful"),
}


def classify_roles(
    identity: Dict, source_material: Dict, metrics: Optional[Dict]
) -> Dict:
    ident = identity.get("instrument_identity", "unknown")
    source_kind = source_material.get("source_kind", "unknown")
    musical_role, perceptual_role, sacredness = _DEFAULTS.get(
        ident, _DEFAULTS["unknown"]
    )
    reasons = []

    # Imported loops/samples are decorative and mute-able unless promoted.
    if source_kind in LOOP_SAMPLE_KINDS:
        sacredness = "decorative"
        if metrics and identity.get("confidence", 1.0) < 0.6:
            perceptual_role = "candidate_for_mute"
            musical_role = "candidate_for_mute"
            sacredness = "expendable"
            reasons.append("Low-confidence imported loop; candidate for mute/chop.")
        else:
            reasons.append("Imported loop/sample treated as felt, re-contextualisable texture.")

    # A keys/guitar element that is wide + sustained leans felt, not heard.
    if ident in {"piano", "electric_piano", "acoustic_guitar", "electric_guitar", "organ"} and metrics:
        if metrics.get("transient_density", 1.0) < 0.2 and metrics.get("stereo_width", 0.0) > 0.55:
            perceptual_role = "felt"
            reasons.append("Sustained and wide; supports the fabric rather than leading it.")

    # Live recordings carry human feel worth protecting.
    if source_kind in {"live_audio_recording", "comped_audio_track"} and sacredness == "useful":
        reasons.append("Live performance; preserve human feel before processing.")

    if not reasons:
        reasons.append(f"Default classification for identity '{ident}'.")

    return {
        "track_id": identity.get("track_id"),
        "name": identity.get("name"),
        "instrument_identity": ident,
        "musical_role": musical_role,
        "perceptual_role": perceptual_role,
        "sacredness": sacredness,
        "reason": " ".join(reasons),
    }
