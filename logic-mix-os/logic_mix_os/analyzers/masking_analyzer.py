"""Masking analyzer — masking as hierarchy, not as a blanket fault.

Doctrine (build packet 17): only flag masking as *critical* when competing
elements occupy the same depth layer **and** perceptual role. Allow controlled
overlap when one element is midground/background or classified as felt.
"""

from __future__ import annotations

from typing import Dict, List, Optional

FORWARD_DEPTHS = {"intimate", "foreground"}
HEARD_ROLES = {"heard", "structural"}

DOCTRINE_RULE = (
    "Only flag masking as critical when competing elements occupy the same depth "
    "layer and perceptual role. Allow controlled overlap when one element is "
    "midground/background or classified as felt."
)


def analyze_masking(records: List[Dict], sections: List[Dict]) -> Dict:
    """``records`` is a list of per-track dicts assembled by the pipeline.

    Required keys: track_id, name, instrument_identity, identity_family,
    perceptual_role, depth_default, depth_by_section, band_energy,
    vocal_presence_energy, stereo_width.
    """
    section_ids = [s["section_id"] for s in sections] if sections else ["full"]
    events: List[Dict] = []
    risk: Dict[str, float] = {r["track_id"]: 0.0 for r in records}

    lead = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)

    for sid in section_ids:
        # --- vocal vs forward harmonic/melodic elements -------------------
        if lead is not None and _depth(lead, sid) in FORWARD_DEPTHS:
            for r in records:
                if r is lead:
                    continue
                if r["instrument_identity"] not in {
                    "piano", "electric_piano", "organ", "acoustic_guitar",
                    "electric_guitar", "synth", "backing_vocal", "strings",
                }:
                    continue
                ev = _vocal_conflict(lead, r, sid)
                if ev:
                    events.append(ev)
                    if ev["classification"] == "bad_masking":
                        risk[r["track_id"]] = max(risk[r["track_id"]], ev["overlap"])

        # --- kick vs bass low-end conflict --------------------------------
        kick = next((r for r in records if r["instrument_identity"] == "kick"), None)
        bass = next(
            (r for r in records if r["instrument_identity"] in {"bass_guitar", "synth_bass"}),
            None,
        )
        if kick and bass:
            ev = _low_end_conflict(kick, bass, sid)
            if ev:
                events.append(ev)
                risk[bass["track_id"]] = max(risk[bass["track_id"]], ev["overlap"])

        # --- stereo width crowding in this section ------------------------
        wide = [
            r for r in records
            if _depth(r, sid) in FORWARD_DEPTHS
            and r.get("stereo_width", 0) > 0.5
            and r["perceptual_role"] in HEARD_ROLES
        ]
        if len(wide) >= 3:
            events.append(_width_crowding(wide, sid))

    summary = {
        "critical_count": sum(1 for e in events if e["severity"] == "critical"),
        "moderate_count": sum(1 for e in events if e["severity"] == "moderate"),
        "blend_count": sum(1 for e in events if e["classification"] == "acceptable_blend"),
        "total_events": len(events),
    }
    return {
        "doctrine_rule": DOCTRINE_RULE,
        "events": events,
        "per_track_masking_risk": {k: round(v, 3) for k, v in risk.items()},
        "summary": summary,
    }


def _depth(record: Dict, section_id: str) -> str:
    return record.get("depth_by_section", {}).get(section_id, record.get("depth_default", "midground"))


def _vocal_conflict(lead: Dict, other: Dict, sid: str) -> Optional[Dict]:
    overlap = round(min(lead.get("vocal_presence_energy", 0.0), other.get("vocal_presence_energy", 0.0)), 4)
    if overlap < 0.05:
        return None
    other_depth = _depth(other, sid)
    both_forward = other_depth in FORWARD_DEPTHS
    other_heard = other["perceptual_role"] in HEARD_ROLES

    if both_forward and other_heard and overlap >= 0.1:
        return {
            "elements": [lead["name"], other["name"]],
            "frequency_range": "1.5kHz-4kHz",
            "section": sid,
            "depth_layers": [_depth(lead, sid), other_depth],
            "perceptual_roles": [lead["perceptual_role"], other["perceptual_role"]],
            "classification": "bad_masking",
            "severity": "critical" if overlap >= 0.16 else "moderate",
            "overlap": overlap,
            "reason": (
                f"Both elements are forward/heard and overlap in the vocal "
                f"presence range (overlap {overlap:.2f})."
            ),
            "recommendation": (
                f"Move {other['name']} to the midground with more chamber send, or "
                f"dip ~2.5 kHz by 1.5-2 dB so the vocal keeps the presence band."
            ),
        }
    return {
        "elements": [lead["name"], other["name"]],
        "frequency_range": "1.5kHz-4kHz",
        "section": sid,
        "depth_layers": [_depth(lead, sid), other_depth],
        "perceptual_roles": [lead["perceptual_role"], other["perceptual_role"]],
        "classification": "acceptable_blend",
        "severity": "info",
        "overlap": overlap,
        "reason": (
            f"{other['name']} overlaps the vocal but sits {other_depth}/"
            f"{other['perceptual_role']}; controlled blend is fine."
        ),
        "recommendation": "No action required; this is good masking (shared fabric).",
    }


def _low_end_conflict(kick: Dict, bass: Dict, sid: str) -> Optional[Dict]:
    overlap = round(min(kick["band_energy"].get("low", 0.0), bass["band_energy"].get("low", 0.0)), 4)
    if overlap < 0.2:
        return None
    return {
        "elements": [kick["name"], bass["name"]],
        "frequency_range": "40Hz-150Hz",
        "section": sid,
        "depth_layers": [_depth(kick, sid), _depth(bass, sid)],
        "perceptual_roles": [kick["perceptual_role"], bass["perceptual_role"]],
        "classification": "low_end_conflict",
        "severity": "moderate" if overlap < 0.32 else "critical",
        "overlap": overlap,
        "reason": f"Kick and bass share substantial sub energy (overlap {overlap:.2f}).",
        "recommendation": (
            "Carve complementary space (e.g. bass dipped where kick thumps), or "
            "sidechain the bass subtly to the kick. Avoid stacking both at the same Hz."
        ),
    }


def _width_crowding(wide: List[Dict], sid: str) -> Dict:
    return {
        "elements": [r["name"] for r in wide],
        "frequency_range": "full-band (stereo image)",
        "section": sid,
        "depth_layers": ["foreground"] * len(wide),
        "perceptual_roles": [r["perceptual_role"] for r in wide],
        "classification": "width_crowding",
        "severity": "moderate",
        "overlap": round(sum(r.get("stereo_width", 0) for r in wide) / len(wide), 3),
        "reason": (
            f"{len(wide)} wide, forward elements share the stereo image in "
            f"section '{sid}'. The mix may feel crowded even if levels balance."
        ),
        "recommendation": (
            "Narrow or push some of these to the midground/background, or reserve "
            "the widest placement for the single most important element."
        ),
    }
