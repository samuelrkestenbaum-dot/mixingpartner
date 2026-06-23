"""Transition quality analyzer (build packet section 25.2).

Looks at each section boundary in the mixdown: does the energy/space actually
change, is the change smooth or abrupt, and does a section that should lift get
a real transition gesture?
"""

from __future__ import annotations

from typing import Dict, List

from .. import dsp
from .audio_loader import LoadedAudio

LIFT_GOALS = {"release", "lift", "catharsis", "climax", "bloom", "open"}


def analyze_transitions(mixdown: LoadedAudio, sections: List) -> Dict:
    if mixdown is None or len(sections) < 2:
        return {"transitions": [], "summary": "Not enough sections for transition analysis."}

    sr = mixdown.sample_rate
    transitions: List[Dict] = []

    for i in range(len(sections) - 1):
        nxt = sections[i + 1]
        boundary = nxt.start
        before = dsp.to_mono(mixdown.slice_seconds(max(0.0, boundary - 0.4), boundary))
        after = dsp.to_mono(mixdown.slice_seconds(boundary, boundary + 0.4))
        rms_before = dsp.rms_dbfs(before)
        rms_after = dsp.rms_dbfs(after)
        jump = round(rms_after - rms_before, 2)

        is_lift = (nxt.emotional_goal or "").lower() in LIFT_GOALS or "chorus" in nxt.name.lower()

        if abs(jump) < 1.0:
            quality = "flat"
            note = "Little energy change across the boundary."
            if is_lift:
                note += " A section meant to lift needs a transition gesture (swell, drop, fill)."
        elif jump > 6:
            quality = "abrupt"
            note = "Large jump — ensure a clean crossfade/edit and that it feels intentional."
        else:
            quality = "smooth"
            note = "Energy changes naturally into the section."

        transitions.append({
            "from": sections[i].section_id,
            "to": nxt.section_id,
            "boundary_sec": round(boundary, 3),
            "rms_jump_db": jump,
            "is_lift_target": is_lift,
            "quality": quality,
            "note": note,
        })

    weak = [t for t in transitions if t["quality"] == "flat" and t["is_lift_target"]]
    return {
        "transitions": transitions,
        "weak_transitions": [t["to"] for t in weak],
        "summary": f"{len(weak)} lift transition(s) lack a real gesture." if weak else "Transitions read intentionally.",
    }
