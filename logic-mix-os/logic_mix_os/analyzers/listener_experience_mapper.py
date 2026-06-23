"""Listener experience mapper (build packet section 29).

The non-engineer "what would a fan hear?" pass. Derives a plain-language journey
from section contrast, density, and vocal presence — where a first-time listener
leans in, zones out, or starts to fatigue, and whether the chorus feels earned.
"""

from __future__ import annotations

from typing import Dict, List, Optional


def map_experience(sections: List[Dict], lead_present: bool) -> Dict:
    if not sections:
        return {"journey": [], "fatigue_points": [], "summary": "No sections to map."}

    journey: List[Dict] = []
    fatigue_points: List[str] = []

    for i, s in enumerate(sections):
        m = s["metrics"]
        c = s.get("contrast_vs_previous", {})
        density = m.get("density", 0.0)
        vocal_db = m.get("vocal_presence_db")
        goal = (s.get("emotional_goal") or "").lower()

        feel = []
        engagement = "neutral"

        if i == 0:
            feel.append("sets the scene")
        if "warning" in c:
            feel.append("expected to lift but feels similar to the previous section")
            engagement = "may zone out"
        elif c.get("rms_delta_db", 0) >= 2.5 or c.get("width_delta", 0) >= 0.05:
            feel.append("opens up / pulls the listener in")
            engagement = "leans in"

        if density > 0.7:
            feel.append("dense — lots happening at once")
            if engagement != "leans in":
                fatigue_points.append(f"{s['name']}: density is high without a clear focal point.")
        if vocal_db is not None and vocal_db < -14 and lead_present:
            feel.append("vocal/lyric may be hard to follow")
            fatigue_points.append(f"{s['name']}: the lyric sits low in the balance.")

        if not feel:
            feel.append("steady")

        journey.append({
            "section_id": s["section_id"],
            "name": s["name"],
            "emotional_goal": s.get("emotional_goal"),
            "what_a_fan_hears": "; ".join(feel),
            "engagement": engagement,
        })

    chorus_earned = not any(
        "warning" in s.get("contrast_vs_previous", {})
        and ("chorus" in s["name"].lower() or (s.get("emotional_goal") or "") in {"release", "lift"})
        for s in sections
    )
    summary = (
        "The chorus feels earned." if chorus_earned
        else "The chorus does not yet feel earned — contrast into it is weak."
    )
    return {
        "journey": journey,
        "fatigue_points": fatigue_points,
        "chorus_feels_earned": chorus_earned,
        "summary": summary,
    }
