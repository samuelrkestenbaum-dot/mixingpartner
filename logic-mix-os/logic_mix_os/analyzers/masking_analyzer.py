"""Masking analyzer — masking as hierarchy, not as a blanket fault.

Doctrine (build packet 17): only flag masking as *critical* when competing
elements occupy the same depth layer **and** perceptual role. Allow controlled
overlap when one element is midground/background or classified as felt.

P-034 — the NON-LEAD vocal-band capacity: the analyzer also reads each
non-lead VOCAL stem (identity ``backing_vocal`` or a non-None ``vocal_type``
record field, the lead excluded on identity AND type) against the SAME
forward harmonic/melodic instrument set the lead pathway uses, and emits
``vocal_band_masking`` events — a classification of its own, consumed ONLY
by the vocal-role surface (``_vocal_role_fit`` + the profile blend gate).
The LEAD is NEVER in these events; lead-inclusive vocal masking stays the
``bad_masking`` pathway, untouched. The design decisions, made honest and
explicit:

* **Forward-only** — the vocal stem must sit in a forward depth for any
  event (the exact mirror of the lead gate). A buried chop/stack emits
  nothing in this packet; what overlap over a deliberately-buried vocal
  means is a profile question deferred to the fixture that makes it real.
* **Vocal-vs-vocal pairs do not fire** — two non-lead vocal stems sharing
  the presence band is the normal construction of a stack (intentional
  layering, an arrangement fact), and emitting both [A,B] and [B,A] would
  double-count one physical overlap. The lead is likewise never a masker
  here: the lead owning the presence band is the doctrine, not a conflict.
* **Severity capped at ``moderate``** — the lead pathway's 0.16 critical
  tier is deliberately not mirrored; what a non-lead vocal-band conflict is
  WORTH is a profile decision, and ``critical_count`` is never inflated.
  The sub-conflict tier (other element not forward/heard) is the ``info``
  reading, same classification.
* **No ``per_track_masking_risk`` contribution** — risk feeds
  ``track_analysis`` metrics consumed broadly; the new classification stays
  out of it in this packet (fixture-inert by construction).
* **Summary counted honestly, conditionally** — ``vocal_band_masking_count``
  appears ONLY when >= 1 such event exists, so a project without non-lead
  vocal stems keeps a byte-identical summary.
* **Wording is observational and philosophy-NEUTRAL** — the event reports
  the overlap; it prescribes nothing (the profile decides what masking of
  this class means).
"""

from __future__ import annotations

from typing import Dict, List, Optional

FORWARD_DEPTHS = {"intimate", "foreground"}
HEARD_ROLES = {"heard", "structural"}

# The forward harmonic/melodic identities checked against a forward vocal in
# the presence band — ONE set, shared by the lead pathway (``_vocal_conflict``,
# behavior unchanged) and the P-034 non-lead pathway (``_vocal_band_conflict``),
# so the two readings can never fork their detection basis.
VOCAL_MASKER_IDENTITIES = {
    "piano", "electric_piano", "organ", "acoustic_guitar",
    "electric_guitar", "synth", "backing_vocal", "strings",
}

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
    non_lead_vocals = [r for r in records if _is_non_lead_vocal_stem(r, lead)]

    for sid in section_ids:
        # --- lead vocal vs forward harmonic/melodic elements --------------
        if lead is not None and _depth(lead, sid) in FORWARD_DEPTHS:
            for r in records:
                if r is lead:
                    continue
                if r["instrument_identity"] not in VOCAL_MASKER_IDENTITIES:
                    continue
                ev = _vocal_conflict(lead, r, sid)
                if ev:
                    events.append(ev)
                    if ev["classification"] == "bad_masking":
                        risk[r["track_id"]] = max(risk[r["track_id"]], ev["overlap"])

        # --- P-034: non-lead vocal stems vs the same forward set ----------
        # Forward-only (the mirror of the lead gate); the lead and every
        # other vocal stem are excluded as maskers (see the module doc); the
        # events contribute NOTHING to per_track_masking_risk in this packet.
        for stem in non_lead_vocals:
            if _depth(stem, sid) not in FORWARD_DEPTHS:
                continue
            for r in records:
                if r is stem or r is lead or _is_non_lead_vocal_stem(r, lead):
                    continue
                if r["instrument_identity"] not in VOCAL_MASKER_IDENTITIES:
                    continue
                ev = _vocal_band_conflict(stem, r, sid)
                if ev:
                    events.append(ev)

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
    # P-034: the non-lead vocal-band count, present ONLY when >= 1 such event
    # exists (the evidence-key discipline) — a project without non-lead vocal
    # stems keeps a byte-identical summary. Moderate-tier events are already
    # counted in moderate_count above (they ARE moderate); critical_count
    # never moves for this classification (severity is capped).
    vband_count = sum(1 for e in events if e["classification"] == "vocal_band_masking")
    if vband_count:
        summary["vocal_band_masking_count"] = vband_count
    return {
        "doctrine_rule": DOCTRINE_RULE,
        "events": events,
        "per_track_masking_risk": {k: round(v, 3) for k, v in risk.items()},
        "summary": summary,
    }


def _depth(record: Dict, section_id: str) -> str:
    return record.get("depth_by_section", {}).get(section_id, record.get("depth_default", "midground"))


def _is_non_lead_vocal_stem(record: Dict, lead: Optional[Dict]) -> bool:
    """A NON-LEAD vocal stem for the P-034 vocal-band pathway: vocal material
    by identity (``backing_vocal``) or by the pipeline's ``vocal_type`` read,
    with the lead excluded on identity AND type — the lead can never appear
    in a ``vocal_band_masking`` event, as subject or masker."""
    if record is lead or record.get("instrument_identity") == "lead_vocal":
        return False
    if record.get("vocal_type") == "vocal_lead":
        return False
    return (
        record.get("instrument_identity") == "backing_vocal"
        or record.get("vocal_type") is not None
    )


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


def _vocal_band_conflict(stem: Dict, other: Dict, sid: str) -> Optional[Dict]:
    """P-034 — the NON-LEAD vocal-band reading: an honest mirror of
    ``_vocal_conflict``'s floors (0.05 / 0.1) with the PHILOSOPHY removed.
    One classification (``vocal_band_masking``) for both tiers; severity
    carries the tier (``moderate`` when the other element is forward/heard
    at or above the conflict floor — capped there, never critical in this
    packet — ``info`` otherwise). The wording reports the overlap and
    prescribes nothing: what masking of this class means is the profile's
    decision, not the analyzer's."""
    overlap = round(min(stem.get("vocal_presence_energy", 0.0),
                        other.get("vocal_presence_energy", 0.0)), 4)
    if overlap < 0.05:
        return None
    other_depth = _depth(other, sid)
    both_forward = other_depth in FORWARD_DEPTHS
    other_heard = other["perceptual_role"] in HEARD_ROLES
    neutral = (
        "Observational reading: what vocal-band overlap means for a non-lead "
        "vocal is a producer-profile decision; no action is prescribed by "
        "this event."
    )
    if both_forward and other_heard and overlap >= 0.1:
        return {
            "elements": [stem["name"], other["name"]],
            "frequency_range": "1.5kHz-4kHz",
            "section": sid,
            "depth_layers": [_depth(stem, sid), other_depth],
            "perceptual_roles": [stem["perceptual_role"], other["perceptual_role"]],
            "classification": "vocal_band_masking",
            "severity": "moderate",
            "overlap": overlap,
            "reason": (
                f"Non-lead vocal '{stem['name']}' and '{other['name']}' sit "
                f"forward/heard together in the vocal presence range "
                f"(overlap {overlap:.2f})."
            ),
            "recommendation": neutral,
        }
    return {
        "elements": [stem["name"], other["name"]],
        "frequency_range": "1.5kHz-4kHz",
        "section": sid,
        "depth_layers": [_depth(stem, sid), other_depth],
        "perceptual_roles": [stem["perceptual_role"], other["perceptual_role"]],
        "classification": "vocal_band_masking",
        "severity": "info",
        "overlap": overlap,
        "reason": (
            f"'{other['name']}' overlaps non-lead vocal '{stem['name']}' in "
            f"the presence range from {other_depth}/{other['perceptual_role']} "
            f"(overlap {overlap:.2f})."
        ),
        "recommendation": neutral,
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
