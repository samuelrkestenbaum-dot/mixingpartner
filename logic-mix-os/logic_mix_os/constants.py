"""Controlled vocabularies shared across the whole system.

Keeping every enum in one place means the detectors, planners, renderers, and
JSON schemas can never drift out of sync. These mirror the taxonomy in the
Logic Mix OS build packet (sections 7.1 - 7.9).
"""

from __future__ import annotations

# --- Source material (what kind of Logic object is this?) -------------------
SOURCE_KINDS = [
    "live_audio_recording",
    "comped_audio_track",
    "di_audio_track",
    "amp_recording",
    "software_instrument_bounce",
    "synth_bounce",
    "imported_sample_loop",
    "splice_sample",
    "apple_loop",
    "one_shot_sample",
    "texture_loop",
    "fx_riser",
    "impact",
    "bounced_stem",
    "bus",
    "aux_return",
    "unknown",
]

# Source kinds that are imported/borrowed material and therefore need to be
# re-contextualised rather than accepted as finished mix elements.
LOOP_SAMPLE_KINDS = {
    "imported_sample_loop",
    "splice_sample",
    "apple_loop",
    "one_shot_sample",
    "texture_loop",
}

# --- Instrument identity (what is this sound?) ------------------------------
INSTRUMENT_IDENTITIES = [
    "lead_vocal",
    "backing_vocal",
    "kick",
    "snare",
    "hi_hat",
    "cymbal",
    "overhead",
    "drum_room",
    "bass_guitar",
    "synth_bass",
    "acoustic_guitar",
    "electric_guitar",
    "piano",
    "electric_piano",
    "organ",
    "synth",
    "pad",
    "strings",
    "percussion",
    "loop",
    "texture",
    "fx",
    "unknown",
]

# Map an instrument identity to a coarse family used by the doctrine engine.
IDENTITY_FAMILY = {
    "lead_vocal": "vocal",
    "backing_vocal": "vocal",
    "kick": "drums",
    "snare": "drums",
    "hi_hat": "drums",
    "cymbal": "drums",
    "overhead": "drums",
    "drum_room": "drums",
    "percussion": "percussion",
    "bass_guitar": "bass",
    "synth_bass": "bass",
    "acoustic_guitar": "guitars",
    "electric_guitar": "guitars",
    "piano": "keys",
    "electric_piano": "keys",
    "organ": "keys",
    "synth": "synth",
    "pad": "synth",
    "strings": "strings",
    "loop": "loop",
    "texture": "texture",
    "fx": "fx",
    "unknown": "unknown",
}

# --- Musical role (what is this sound doing?) -------------------------------
MUSICAL_ROLES = [
    "emotional_center",
    "lead_hook",
    "countermelody",
    "harmonic_support",
    "rhythmic_drive",
    "groove_support",
    "low_end_foundation",
    "transient_anchor",
    "texture",
    "atmosphere",
    "transition",
    "impact",
    "glue",
    "decorative",
    "candidate_for_mute",
]

# --- Perceptual role (felt vs heard) ----------------------------------------
PERCEPTUAL_ROLES = [
    "heard",
    "felt",
    "structural",
    "transitional",
    "decorative",
    "candidate_for_mute",
]

# --- Sacredness (artistic importance) ---------------------------------------
SACREDNESS_VALUES = [
    "sacred",
    "important",
    "useful",
    "decorative",
    "expendable",
    "harmful",
]

# --- Depth layers (where does it live?) -------------------------------------
DEPTH_LAYERS = ["intimate", "foreground", "midground", "background"]

# --- Risk classes for mix actions (build packet section 77) -----------------
RISK_CLASSES = {
    0: "observe / analyze only",
    1: "report / checklist only",
    2: "reversible mix recommendation",
    3: "reversible Logic action requiring approval",
    4: "source-level creative change requiring explicit approval",
    5: "destructive or identity-changing action; never auto-apply",
}

# --- Evidence types for confidence tagging (build packet section 37) --------
EVIDENCE_TYPES = [
    "measured",
    "inferred",
    "subjective",
    "comparative",
    "doctrine",
    "user_intent",
]

# Frequency band edges (Hz) used everywhere for tonal-balance reasoning.
BANDS = {
    "low": (20.0, 120.0),
    "low_mid": (120.0, 500.0),
    "mid": (500.0, 2000.0),
    "presence": (2000.0, 6000.0),
    "high": (6000.0, 20000.0),
}

# Problem-specific bands used by the indicator detectors.
MUD_BAND = (180.0, 500.0)
HARSH_BAND = (2000.0, 4500.0)
SIBILANCE_BAND = (5000.0, 9000.0)
VOCAL_PRESENCE_BAND = (1500.0, 4000.0)
