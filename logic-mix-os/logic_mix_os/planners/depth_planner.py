"""Depth planner.

Assigns every track to a depth layer (intimate / foreground / midground /
background), per section where sections exist. This is how dense arrangements
become clear without making everything smaller (Roy Halee depth doctrine).
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..project import Section

LIFT_GOALS = {"release", "lift", "catharsis", "climax", "bloom", "open"}
LOW_GOALS = {"intimacy", "vulnerability", "restraint", "grief", "warmth", "tension"}
PRESSURE_GOALS = {"pressure", "collapse", "anger", "constriction"}


def plan_depth(
    identity: Dict, roles: Dict, source_material: Dict, sections: List[Section]
) -> Dict:
    ident = identity.get("instrument_identity", "unknown")
    perceptual = roles.get("perceptual_role", "felt")
    sacredness = roles.get("sacredness", "useful")
    base = _base_depth(ident, perceptual, sacredness)

    depth_by_section: Dict[str, str] = {}
    for sec in sections:
        depth_by_section[sec.section_id] = _section_depth(ident, perceptual, base, sec)

    return {
        "track_id": identity.get("track_id"),
        "name": identity.get("name"),
        "instrument_identity": ident,
        "default_depth": base,
        "depth_by_section": depth_by_section,
        "reason": _reason(ident, perceptual, base),
    }


def _base_depth(ident: str, perceptual: str, sacredness: str) -> str:
    if ident == "lead_vocal":
        return "intimate"
    if ident in {"kick", "snare", "bass_guitar", "synth_bass"}:
        return "foreground"
    if ident == "backing_vocal":
        return "midground"
    if ident in {"piano", "acoustic_guitar", "electric_guitar", "electric_piano"}:
        return "foreground" if perceptual == "heard" else "midground"
    if ident in {"hi_hat", "cymbal", "overhead", "drum_room", "percussion", "organ"}:
        return "midground"
    if ident in {"pad", "strings", "texture", "loop"}:
        return "background" if sacredness in {"decorative", "expendable"} else "midground"
    if ident in {"synth"}:
        return "midground"
    if ident in {"fx"}:
        return "background"
    return "midground"


def _section_energy(sec: Section) -> str:
    goal = (sec.emotional_goal or "").lower()
    name = sec.name.lower()
    if goal in LIFT_GOALS or "chorus" in name or "drop" in name:
        return "high"
    if goal in PRESSURE_GOALS or "bridge" in name:
        return "bridge"
    if goal in LOW_GOALS or "verse" in name or "intro" in name or "outro" in name:
        return "low"
    return "mid"


def _section_depth(ident: str, perceptual: str, base: str, sec: Section) -> str:
    energy = _section_energy(sec)

    if ident == "lead_vocal":
        return "foreground" if energy == "high" else "intimate"

    if ident == "backing_vocal":
        return {"high": "foreground", "low": "background"}.get(energy, "midground")

    if ident in {"piano", "acoustic_guitar", "electric_guitar", "electric_piano"} and perceptual == "heard":
        # Support the exposed vocal in low sections; step back in big choruses.
        return {"low": "foreground", "high": "midground", "bridge": "background"}.get(energy, base)

    if ident in {"pad", "strings", "texture", "loop"} or perceptual == "felt":
        return {"high": "midground", "low": "background"}.get(energy, "background")

    # Structural rhythm section stays put.
    return base


def _reason(ident: str, perceptual: str, base: str) -> str:
    if ident == "lead_vocal":
        return "Emotional centre: intimate in verses, foreground in choruses; never buried."
    if perceptual == "felt":
        return "Felt element: lives behind the heard elements, deeper and more filtered."
    if base == "foreground":
        return "Heard element supporting the emotional centre; clear but not competing with the vocal."
    return f"Placed in the {base} layer based on identity and role."
