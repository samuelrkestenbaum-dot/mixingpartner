"""Source material detector — *what kind of Logic object is this?*

Answers the question that must come before "what instrument is this": a live
piano, a MIDI piano bounce, and an imported piano loop are all "piano" but the
editable domains differ. Uses manifest hints first, then filename clues, then
audio features.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS, SOURCE_KINDS
from ..project import Track

# Ordered keyword -> source_kind table. First match wins, so put the most
# specific phrases first.
_KEYWORD_RULES: List[tuple] = [
    (("splice",), "splice_sample"),
    (("apple loop", "apple_loop", "apploop"), "apple_loop"),
    (("one shot", "one-shot", "oneshot", "1shot"), "one_shot_sample"),
    (("texture", "atmos", "ambience", "ambient", "drone"), "texture_loop"),
    (("riser", "uplifter", "sweep up", "rise fx", "whoosh"), "fx_riser"),
    (("impact", "boom", "downlifter", "hit fx"), "impact"),
    (("loop",), "imported_sample_loop"),
    (("reamp", "amp ", "amp_", "cab "), "amp_recording"),
    (("di ", "di_", "_di", "direct in"), "di_audio_track"),
    (("synth", "saw", "pluck", "arp", "lead synth"), "synth_bounce"),
    (("midi", "vst", "instrument", "soft synth"), "software_instrument_bounce"),
    (("bus", "submix", "sub mix", "group"), "bus"),
    (("aux", "return", "verb return", "fx return"), "aux_return"),
    (("comp", "vox comp", "vocal comp"), "comped_audio_track"),
    (("stem", "print", "bounce"), "bounced_stem"),
]

# Editable domains keyed by source kind.
_AUDIO_BASE = ["gain", "eq", "dynamics", "reverb_send", "automation", "region_editing", "fade"]
_SAMPLE_EXTRA = ["stereo_width", "pitch_shift", "time_stretch", "chop", "reverse"]


def detect_source_material(track: Track, metrics: Optional[Dict]) -> Dict:
    source_kind, confidence, evidence = _infer_kind(track)

    editable = list(_AUDIO_BASE)
    not_editable: List[str] = []
    if source_kind in LOOP_SAMPLE_KINDS:
        editable += _SAMPLE_EXTRA
    if source_kind in {"software_instrument_bounce", "synth_bounce"}:
        editable += ["stereo_width"]
        not_editable += ["midi_notes", "velocity", "synth_patch_parameters"]
    if source_kind in {"bus", "aux_return"}:
        not_editable += ["individual_constituent_tracks"]

    warnings = _warnings(source_kind, metrics)

    return {
        "track_id": track.track_id,
        "name": track.name,
        "file": track.file,
        "source_kind": source_kind,
        "confidence": round(confidence, 2),
        "editable_domains": editable,
        "not_editable_directly": not_editable,
        "requires_render_for_analysis": False,
        "evidence": evidence,
        "warnings": warnings,
    }


def _infer_kind(track: Track):
    # 1) Manifest hint wins if it is a known kind.
    hint = (track.source_kind_hint or "").strip()
    if hint in SOURCE_KINDS:
        return hint, 0.95, {"manifest_hint": hint}

    # Match on the track name + file *basename* only. The full path is excluded
    # so a parent folder name (e.g. ".../with_loops/") can't pollute keywords.
    basename = Path(track.file).name if track.file else ""
    name = f"{track.name} {basename}".lower()
    for keywords, kind in _KEYWORD_RULES:
        for kw in keywords:
            if kw in name:
                return kind, 0.82, {"filename_clue": kw}

    # 2) Fall back to identity-style defaults from the track name.
    if any(k in name for k in ("vox", "vocal", "lead", "bgv", "harm")):
        return "comped_audio_track", 0.6, {"filename_clue": "vocal-like name"}
    if any(k in name for k in ("kick", "snare", "drum", "tom", "hat", "perc", "gtr", "guitar", "bass", "piano", "keys")):
        return "live_audio_recording", 0.55, {"filename_clue": "live-instrument name"}

    return "unknown", 0.4, {"note": "no manifest hint or recognised keyword"}


def _warnings(source_kind: str, metrics: Optional[Dict]) -> List[str]:
    warnings: List[str] = []
    if source_kind in LOOP_SAMPLE_KINDS:
        warnings.append(
            "Imported loop/sample: verify it is not accepted at full width in the "
            "foreground by default. Re-contextualise into the song's depth and tone."
        )
        if metrics:
            if metrics.get("stereo_width", 0) >= 0.6:
                warnings.append(
                    "Stereo image is wide; consider narrowing and placing it in "
                    "the midground/background rather than full-width foreground."
                )
            if metrics.get("crest_factor_db", 99) < 8:
                warnings.append(
                    "Low crest factor suggests the loop is pre-compressed/mastered; "
                    "it may make live tracks feel small next to it."
                )
    if source_kind in {"software_instrument_bounce", "synth_bounce"}:
        warnings.append(
            "Printed instrument bounce: note/patch/envelope changes require "
            "re-rendering from the original MIDI, not audio editing."
        )
    return warnings
