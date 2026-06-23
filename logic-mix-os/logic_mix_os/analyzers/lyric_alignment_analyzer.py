"""Lyric alignment / treatment analyzer (build packet section 25.4).

Optional. If the manifest supplies lyrics (per section or whole-song), align them
to sections and flag where intelligibility is at risk because the vocal sits low
in the balance. Without lyrics it reports availability=False and stays quiet.
"""

from __future__ import annotations

from typing import Dict, List, Optional


def analyze_lyrics(manifest: Dict, sections_analysis: List[Dict], lead_present: bool) -> Dict:
    intent = manifest.get("intent", {})
    lyrics = intent.get("lyrics") or manifest.get("lyrics")
    # Per-section lyrics may also live on the section entries.
    section_lyrics = {
        s.get("section_id"): s.get("lyrics")
        for s in manifest.get("sections", [])
        if s.get("lyrics")
    }

    if not lyrics and not section_lyrics:
        return {"available": False, "summary": "No lyrics provided in the manifest."}

    rows: List[Dict] = []
    at_risk: List[str] = []
    for s in sections_analysis:
        text = section_lyrics.get(s["section_id"])
        vocal_db = s["metrics"].get("vocal_presence_db")
        risk = None
        if lead_present and vocal_db is not None and vocal_db < -14:
            risk = "Vocal sits low here — the lyric may be hard to follow."
            at_risk.append(s["section_id"])
        rows.append({
            "section_id": s["section_id"],
            "name": s["name"],
            "lyric": text,
            "vocal_presence_db": vocal_db,
            "intelligibility_risk": risk,
        })

    return {
        "available": True,
        "rows": rows,
        "at_risk_sections": at_risk,
        "summary": f"{len(at_risk)} section(s) with lyric-intelligibility risk." if at_risk
                   else "Lyric intelligibility looks acceptable across sections.",
    }
