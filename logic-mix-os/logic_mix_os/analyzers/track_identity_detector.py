"""Track identity detector — *what is this sound?*

Separate from musical role (*what is it doing?*). Combines filename/track-name
clues with spectral, transient, and stereo evidence. Names dominate when
present; audio features confirm the choice and set the confidence.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..constants import IDENTITY_FAMILY, INSTRUMENT_IDENTITIES
from ..project import Track

# Ordered (keywords -> identity). Most specific phrases first.
_NAME_RULES: List[Tuple[Tuple[str, ...], str]] = [
    (("overhead", " oh", "oh ", "_oh", "oh_", "drum oh"), "overhead"),
    (("crash", "ride", "cymbal", " cym", "cym "), "cymbal"),
    (("hi-hat", "hihat", "hi hat", " hat", "hat ", "_hh", "hh_"), "hi_hat"),
    (("drum room", "room mic", " room", "drm room"), "drum_room"),
    (("snare", " snr", "snr ", " sd ", "sidestick"), "snare"),
    (("kick", " bd ", "bassdrum", "bass drum"), "kick"),
    (("shaker", "tambourine", " tamb", "conga", "bongo", "clap", " perc", "perc "), "percussion"),
    (("808", " sub ", "sub_", "sub bass", "subbass"), "synth_bass"),
    (("synth bass", "synthbass"), "synth_bass"),
    (("bass",), "bass_guitar"),
    (("backing vocal", "bgv", " bv ", "bv_", "harmony", " harm", "vocal double", "vox double"), "backing_vocal"),
    (("lead vocal", "lead vox", " lv ", "lv_", "_lv", "vocal", " vox", "vox "), "lead_vocal"),
    (("rhodes", "wurli", "wurlitzer", "electric piano", "e.piano", "epiano", " ep ", "ep_"), "electric_piano"),
    (("piano", " pno", "pno ", "upright", "grand"), "piano"),
    (("organ", "hammond", " b3", "b3 "), "organ"),
    (("acoustic guitar", "acoustic gtr", "ac gtr", "ac.gtr", "aco gtr", "acgtr", "nylon", "steel string"), "acoustic_guitar"),
    (("electric guitar", "el gtr", "elec gtr", "egtr", " gtr", "gtr ", "guitar"), "electric_guitar"),
    (("strings", "violin", "cello", "viola", " strs", "string section"), "strings"),
    (("pad",), "pad"),
    (("texture", "atmos", "ambience", "ambient", "drone"), "texture"),
    (("riser", "impact", " fx", "fx ", "sweep", "whoosh", "uplifter"), "fx"),
    (("synth", "saw", "pluck", "arp", "lead synth", "poly"), "synth"),
    (("loop",), "loop"),
]


def detect_track_identity(track: Track, metrics: Optional[Dict]) -> Dict:
    # 1) Manifest hint wins.
    hint = (track.identity_hint or "").strip()
    if hint in INSTRUMENT_IDENTITIES:
        return _result(track, hint, 0.95, {"manifest_hint": hint}, [])

    # Match on track name + file basename only (avoid parent-folder pollution).
    basename = Path(track.file).name if track.file else ""
    name = f"{track.name} {basename}".lower()
    name_id, name_clue = _name_match(name)

    audio_scores = _audio_scores(metrics) if metrics else {}
    scores: Dict[str, float] = defaultdict(float)
    for ident, s in audio_scores.items():
        scores[ident] += s
    if name_id:
        scores[name_id] += 1.3

    if not scores:
        return _result(track, "unknown", 0.3, {"note": "no clues"}, [])

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    best_id, best_score = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    confidence = _confidence(best_score, second, bool(name_id))

    evidence: Dict = {}
    if name_clue:
        evidence["filename_clues"] = [name_clue]
    if metrics:
        evidence["spectral_profile"] = _describe_spectrum(metrics)
        evidence["transient_profile"] = _describe_transient(metrics)
        evidence["stereo_profile"] = _describe_stereo(metrics)

    total = sum(s for _, s in ranked[:3]) or 1.0
    alternates = [
        {"instrument_identity": ident, "confidence": round(s / total, 2)}
        for ident, s in ranked[1:3]
        if s > 0
    ]
    return _result(track, best_id, confidence, evidence, alternates)


def _result(track, identity, confidence, evidence, alternates) -> Dict:
    return {
        "track_id": track.track_id,
        "name": track.name,
        "instrument_identity": identity,
        "identity_family": IDENTITY_FAMILY.get(identity, "unknown"),
        "confidence": round(float(confidence), 2),
        "evidence": evidence,
        "alternate_candidates": alternates,
        "manual_override": None,
    }


def _name_match(name: str) -> Tuple[Optional[str], Optional[str]]:
    for keywords, ident in _NAME_RULES:
        for kw in keywords:
            if kw in name:
                return ident, kw.strip()
    return None, None


def _audio_scores(m: Dict) -> Dict[str, float]:
    """Heuristic feature memberships. Confirm name matches and break ties."""
    bands = m.get("band_energy", {})
    low = bands.get("low", 0.0)
    low_mid = bands.get("low_mid", 0.0)
    mid = bands.get("mid", 0.0)
    pres = bands.get("presence", 0.0)
    high = bands.get("high", 0.0)
    b = m.get("brightness", 0.5)
    trans = m.get("transient_density", 0.0)
    width = m.get("stereo_width", 0.0)
    flat = m.get("spectral_flatness", 0.2)
    tonal = max(0.0, 1.0 - flat)

    def c(v: float) -> float:
        return max(0.0, min(1.0, v))

    return {
        "kick": c(0.55 * low + 0.25 * trans + 0.2 * (1 - b) + 0.1 * (1 - width) - 0.5 * high),
        "snare": c(0.3 * mid + 0.3 * pres + 0.3 * trans + 0.1 * (1 - width) - 0.4 * low),
        "hi_hat": c(0.45 * high + 0.25 * b + 0.2 * trans - 0.5 * low),
        "cymbal": c(0.5 * high + 0.3 * b + 0.2 * flat - 0.4 * low),
        "overhead": c(0.4 * high + 0.2 * b + 0.3 * width + 0.1 * trans - 0.4 * low),
        "bass_guitar": c(0.4 * low + 0.3 * low_mid + 0.2 * (1 - trans) + 0.15 * (1 - b) - 0.5 * high),
        "piano": c(0.3 * mid + 0.2 * low_mid + 0.2 * pres + 0.15 * tonal + 0.1 * trans),
        "electric_piano": c(0.3 * mid + 0.2 * low_mid + 0.15 * pres + 0.15 * tonal + 0.05 * (1 - trans)),
        "organ": c(0.3 * mid + 0.2 * low_mid + 0.25 * (1 - trans) + 0.15 * tonal),
        "lead_vocal": c(0.35 * mid + 0.3 * pres + 0.2 * tonal + 0.15 * (1 - width) - 0.3 * low),
        "backing_vocal": c(0.3 * mid + 0.3 * pres + 0.2 * tonal + 0.2 * width - 0.3 * low),
        "acoustic_guitar": c(0.3 * mid + 0.25 * pres + 0.2 * trans + 0.15 * tonal - 0.2 * low),
        "electric_guitar": c(0.32 * mid + 0.22 * pres + 0.15 * tonal + 0.1 * trans - 0.2 * low),
        "strings": c(0.3 * mid + 0.2 * pres + 0.25 * (1 - trans) + 0.2 * width + 0.1 * tonal),
        "pad": c(0.25 * (1 - trans) + 0.25 * width + 0.2 * tonal + 0.2 * mid + 0.15 * low_mid),
        "synth": c(0.25 * pres + 0.2 * b + 0.2 * tonal + 0.15 * width + 0.1 * mid),
        "texture": c(0.3 * flat + 0.3 * width + 0.2 * high + 0.1 * (1 - trans)),
        "percussion": c(0.3 * trans + 0.2 * mid + 0.2 * high + 0.1 * flat - 0.3 * low),
    }


def _confidence(best: float, second: float, named: bool) -> float:
    margin = best / (best + second + 1e-9)
    base = 0.35 + 0.6 * (margin - 0.5) * 2  # margin 0.5->0.35, 1.0->0.95
    base = max(0.3, min(0.95, base))
    if named:
        base = max(base, 0.7)
    return min(0.95, base)


def _describe_spectrum(m: Dict) -> str:
    bands = m.get("band_energy", {})
    dominant = max(bands, key=bands.get) if bands else "unknown"
    return f"centroid {m.get('spectral_centroid', 0):.0f} Hz; dominant band: {dominant}"


def _describe_transient(m: Dict) -> str:
    t = m.get("transient_density", 0.0)
    if t > 0.6:
        return "sharp, percussive transients"
    if t > 0.3:
        return "moderate transient articulation"
    return "slow attack / sustained, low transient density"


def _describe_stereo(m: Dict) -> str:
    w = m.get("stereo_width", 0.0)
    if w >= 0.6:
        return "wide stereo image"
    if w >= 0.25:
        return "moderate stereo width"
    return "centred / near-mono"
