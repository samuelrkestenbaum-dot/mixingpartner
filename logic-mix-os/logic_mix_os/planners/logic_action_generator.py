"""Logic-native action generator.

Maps each track's identity, role, depth, and measured problems to specific,
reversible, Logic-stock actions. Follows the preferred order: automation,
level/pan, depth, subtractive EQ, compression, then additive moves.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS

DEPTH_SEND = {
    "intimate": "Short room or slapback only, very low send (~-24 dB). Keep it close.",
    "foreground": "Short chamber, low send (~-18 dB).",
    "midground": "Shared plate/chamber, moderate send (~-14 dB).",
    "background": "Hall or long plate, higher send (~-10 dB), filtered and diffuse.",
}


def _action(plugin: str, setting: str, reason: str, risk_class: int = 2) -> Dict:
    return {"plugin": plugin, "setting": setting, "reason": reason, "risk_class": risk_class}


def generate_track_actions(record: Dict, masking_events: List[Dict]) -> Dict:
    ident = record["instrument_identity"]
    metrics = record.get("metrics", {})
    depth = record["depth_default"]
    actions: List[Dict] = []
    automation: List[Dict] = []
    warnings: List[str] = []

    masks_vocal = [
        e for e in masking_events
        if record["name"] in e["elements"]
        and e["classification"] in {"bad_masking"}
        and any("vocal" in el.lower() for el in e["elements"])
    ]

    if ident == "lead_vocal":
        _vocal_actions(actions, automation, metrics)
    elif ident in {"bass_guitar", "synth_bass"}:
        _bass_actions(actions, metrics, masking_events)
    elif ident == "kick":
        _kick_actions(actions, metrics)
    elif ident in {"snare", "hi_hat", "cymbal", "overhead", "drum_room", "percussion"}:
        _drum_actions(actions, ident, metrics)
    elif ident in {"piano", "electric_piano", "organ", "acoustic_guitar", "electric_guitar", "backing_vocal", "strings"}:
        _harmonic_actions(actions, ident, metrics, masks_vocal)
    elif ident in {"pad", "synth", "texture", "loop", "fx"} or record["source_kind"] in LOOP_SAMPLE_KINDS:
        _felt_actions(actions, automation, record, metrics, warnings)
    else:
        actions.append(_action("Channel EQ", "Gentle clean-up; high-pass below useful range.", "Default placement.", 2))

    # Shared: depth-appropriate reverb send.
    send_reverb = DEPTH_SEND.get(depth, DEPTH_SEND["midground"])

    diagnosis = _diagnosis(record, metrics, masks_vocal)
    risk_class = max([a["risk_class"] for a in actions], default=2)

    return {
        "track": record["name"],
        "track_id": record["track_id"],
        "instrument_identity": ident,
        "perceptual_role": record["perceptual_role"],
        "depth_layer": depth,
        "diagnosis": diagnosis,
        "actions": actions,
        "automation": automation,
        "send_reverb": send_reverb,
        "pan_depth": f"{depth} layer — {record['perceptual_role']}",
        "risk_class": risk_class,
        "warnings": warnings,
    }


def generate_logic_actions(records: List[Dict], masking_report: Dict) -> List[Dict]:
    events = masking_report.get("events", [])
    return [generate_track_actions(r, events) for r in records]


# --------------------------------------------------------------------------- #
def _vocal_actions(actions, automation, metrics):
    automation.append({
        "parameter": "gain (clip gain + fader)",
        "move": "Ride phrase endings +0.5 to +1 dB where the lyric drops, before adding compression.",
        "reason": "Ramone-style vocal belief: performance rides before brute-force compression.",
        "risk_class": 2,
    })
    eq = "High-pass ~80 Hz."
    if metrics.get("mud_indicator", 0) > 0.4:
        eq += " Cut ~250 Hz by 1-2 dB (mud)."
    eq += " Avoid large 12 kHz+ air boosts (keeps the vocal human, not glossy)."
    actions.append(_action("Channel EQ", eq, "Clean low-end build-up and keep believable presence without hype.", 2))
    if metrics.get("sibilance_indicator", 0) > 0.45:
        actions.append(_action("DeEsser 2", "Target 5-8 kHz, gentle, only on the harsh syllables.", "Sibilance detected; de-ess surgically.", 2))
    actions.append(_action("Compressor", "Vintage Opto, target 2-3 dB gain reduction, slow-ish attack.", "Stabilise the vocal while preserving the performance (invisible compression).", 2))


def _bass_actions(actions, metrics, masking_events):
    actions.append(_action("Channel EQ", "High-pass ~30 Hz; control 200-350 Hz if boxy.", "Tighten the low end without thinning the body.", 2))
    actions.append(_action("Compressor", "Vintage Opto, gentle 2-4 dB GR for consistent sustain.", "Even out the low-end foundation.", 2))
    low_conflict = any(e["classification"] == "low_end_conflict" for e in masking_events)
    if low_conflict:
        actions.append(_action("Channel EQ", "Carve a small dip where the kick thumps (complementary to kick).", "Resolve kick/bass low-end conflict by carving, not stacking.", 2))


def _kick_actions(actions, metrics):
    actions.append(_action("Channel EQ", "Shape sub (~50-70 Hz) vs beater (~3-5 kHz); leave room for bass.", "Define the kick without masking the bass.", 2))


def _drum_actions(actions, ident, metrics):
    if ident in {"overhead", "drum_room", "cymbal", "hi_hat"} and metrics.get("harshness_indicator", 0) > 0.45:
        actions.append(_action("Channel EQ", "Tame 2-4 kHz harshness gently; high-shelf control if brittle.", "Smooth cymbal/room harshness.", 2))
    else:
        actions.append(_action("Channel EQ", "Light tonal shaping only; preserve transient detail and room realism.", "Halee naturalism: keep the kit believable.", 2))


def _harmonic_actions(actions, ident, metrics, masks_vocal):
    if masks_vocal:
        actions.append(_action(
            "Channel EQ",
            "Dip ~2.5 kHz by 1.5-2 dB (carve a pocket for the vocal presence band).",
            "Resolve vocal masking via subtraction, not by pushing the vocal harder.",
            2,
        ))
    if metrics.get("mud_indicator", 0) > 0.45:
        actions.append(_action("Channel EQ", "Cut 250-400 Hz by 1-2 dB.", "Reduce low-mid mud build-up.", 2))
    if not masks_vocal and metrics.get("mud_indicator", 0) <= 0.45:
        actions.append(_action("Channel EQ", "Light shaping; high-pass below the instrument's body.", "Make room without thinning.", 2))


def _felt_actions(actions, automation, record, metrics, warnings):
    is_loop = record["source_kind"] in LOOP_SAMPLE_KINDS
    if record.get("stereo_width", 0) > 0.55:
        actions.append(_action(
            "Direction Mixer",
            "Narrow stereo width to ~35-50%.",
            "Felt/atmospheric element should not occupy the same width as heard elements.",
            3,
        ))
    actions.append(_action("Channel EQ", "High-pass ~250 Hz; low-pass the top if it is purely atmospheric.", "Filter felt elements so they support without crowding.", 2))
    automation.append({
        "parameter": "filter cutoff / send",
        "move": "Open the filter and lift the reverb send only in chorus sections; pull back in verses.",
        "reason": "Use the element as movement (felt), not a constant heard layer.",
        "risk_class": 2,
    })
    if is_loop:
        actions.append(_action(
            "(arrangement)",
            "Consider chopping into transition gestures and muting the continuous bed; reserve for pre-chorus/bridge.",
            "Re-contextualise the imported loop instead of running it as a finished record inside the record.",
            4,
        ))
        warnings.append("Imported loop: do not let it dominate the song identity. Non-destructive duplicate before chopping.")


def _diagnosis(record, metrics, masks_vocal) -> str:
    bits = [f"{record['perceptual_role']} element in the {record['depth_default']} layer."]
    if masks_vocal:
        bits.append("Currently competing with the vocal in the presence band.")
    if metrics.get("mud_indicator", 0) > 0.45:
        bits.append("Low-mid mud is elevated.")
    if record.get("stereo_width", 0) > 0.6 and record["perceptual_role"] == "felt":
        bits.append("Wider than a felt element should be.")
    return " ".join(bits)
