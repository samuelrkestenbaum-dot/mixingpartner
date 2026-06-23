"""Translation analyzer (build packet section 30).

Simulates how the mix is likely to behave across playback systems, from the
deterministic mixdown metrics and per-track stereo behaviour. No real device
modelling — heuristic risk flags grounded in measured band balance, width,
mono-collapse, harshness and sub energy.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..constants import LOOP_SAMPLE_KINDS

# Each profile: (display name, what it stresses)
PROFILES = [
    "headphones",
    "airpods_earbuds",
    "car",
    "phone_speaker",
    "laptop_speakers",
    "studio_monitors",
    "mono_bluetooth_speaker",
    "club_pa",
]


def analyze_translation(mix_metrics: Optional[Dict], records: List[Dict]) -> Dict:
    if not mix_metrics:
        return {"profiles": [], "checks": {}, "translation_score": None, "warnings": ["No mixdown to assess translation."]}

    bands = mix_metrics.get("band_energy", {})
    sub = bands.get("low", 0.0)
    low_mid = bands.get("low_mid", 0.0)
    presence = bands.get("presence", 0.0)
    high = bands.get("high", 0.0)
    width = mix_metrics.get("stereo_width", 0.0)
    mono_loss = mix_metrics.get("mono_collapse_loss_db", 0.0)
    harsh = mix_metrics.get("harshness_indicator", 0.0)
    sib = mix_metrics.get("sibilance_indicator", 0.0)

    wide_loops = [r for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS and r.get("stereo_width", 0) > 0.55]
    sub_tracks = [r for r in records if r["band_energy"].get("low", 0) > 0.45]

    profiles: List[Dict] = []

    def add(name, risks):
        sev = "high" if any(r[1] == "high" for r in risks) else ("moderate" if risks else "low")
        profiles.append({"profile": name, "risks": [r[0] for r in risks], "severity": sev})

    # headphones — width illusions, reverb washout
    hp = []
    if width > 0.55:
        hp.append(("Wide image may sound impressive on headphones but collapse on speakers.", "moderate"))
    add("headphones", hp)

    # earbuds — sub disappears
    eb = []
    if sub > 0.35:
        eb.append(("Heavy sub may be inaudible on earbuds; check kick/bass definition in the low-mids.", "moderate"))
    add("airpods_earbuds", eb)

    # car — harshness, low-mid buildup
    car = []
    if harsh > 0.45 or high > 0.28:
        car.append(("Upper-mid/high energy may turn harsh in a car.", "high" if harsh > 0.6 else "moderate"))
    if low_mid > 0.4:
        car.append(("Low-mid buildup can boom in a car.", "moderate"))
    add("car", car)

    # phone speaker — vocal/lyric loss, no lows
    phone = []
    if presence < 0.12:
        phone.append(("Thin presence band: the vocal/lyric may get lost on a phone speaker.", "high"))
    add("phone_speaker", phone)

    # laptop — low-mid mud, no sub
    lap = []
    if low_mid > 0.42:
        lap.append(("Low-mid heavy mixes sound congested on laptop speakers.", "moderate"))
    add("laptop_speakers", lap)

    add("studio_monitors", [])

    # mono bluetooth — stereo collapse
    mono = []
    if mono_loss < -3 or wide_loops:
        names = ", ".join(r["name"] for r in wide_loops) or "wide content"
        mono.append((f"Stereo collapse risk in mono ({names}); ~{mono_loss:.1f} dB level change.",
                     "high" if mono_loss < -6 else "moderate"))
    add("mono_bluetooth_speaker", mono)

    # club PA — sub + harshness both matter
    club = []
    if sub < 0.2:
        club.append(("Light low end may feel small on a club PA.", "moderate"))
    if sib > 0.5:
        club.append(("Sibilance can become piercing on a large PA.", "moderate"))
    add("club_pa", club)

    high_count = sum(1 for p in profiles if p["severity"] == "high")
    mod_count = sum(1 for p in profiles if p["severity"] == "moderate")
    score = max(0.0, 100.0 - high_count * 18 - mod_count * 7)

    warnings = []
    for p in profiles:
        for r in p["risks"]:
            if p["severity"] == "high":
                warnings.append(f"[{p['profile']}] {r}")

    return {
        "profiles": profiles,
        "checks": {
            "stereo_width": width,
            "mono_collapse_loss_db": mono_loss,
            "sub_energy": sub,
            "low_mid_energy": low_mid,
            "harshness": harsh,
            "sibilance": sib,
        },
        "translation_score": round(score, 1),
        "warnings": warnings,
    }
