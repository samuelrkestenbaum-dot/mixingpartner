"""Sample provenance / licensing tracker (build packet section 34).

For imported loops, Splice samples, Apple Loops and one-shots, tracks origin,
license status, whether the material is still recognizable, and whether it is
foregrounded — flagging creative/legal risk.
"""

from __future__ import annotations

from typing import Dict, List

from ..constants import LOOP_SAMPLE_KINDS

FORWARD = {"intimate", "foreground"}


def analyze_provenance(project, source_material: List[Dict], depth_map: List[Dict]) -> Dict:
    sm_by_id = {s["track_id"]: s for s in source_material}
    depth_by_id = {d["track_id"]: d for d in depth_map}
    items: List[Dict] = []

    for track in project.tracks:
        sm = sm_by_id.get(track.track_id)
        if not sm or sm["source_kind"] not in LOOP_SAMPLE_KINDS:
            continue
        extra = track.extra or {}
        origin = extra.get("sample_origin") or ("Splice" if sm["source_kind"] == "splice_sample" else "imported")
        altered = bool(extra.get("altered", False))
        recognizable = not altered
        depth = depth_by_id.get(track.track_id, {}).get("default_depth", "background")
        foregrounded = depth in FORWARD

        if recognizable and foregrounded:
            risk, reason = "high", "Recognizable loop is foregrounded and identifiable."
        elif recognizable:
            risk, reason = "medium", "Recognizable loop; re-contextualise so it reads as the song, not the loop."
        else:
            risk, reason = "low", "Altered enough that it no longer reads as a stock loop."

        items.append({
            "track": track.name,
            "track_id": track.track_id,
            "sample_origin": origin,
            "filename": track.file.split("/")[-1] if track.file else None,
            "license_status": extra.get("license", "unknown"),
            "bpm": extra.get("bpm"),
            "key": extra.get("key"),
            "altered": altered,
            "recognizable": recognizable,
            "foregrounded": foregrounded,
            "risk": risk,
            "reason": reason,
            "recommendation": ("Chop, filter, reverse, re-pitch, or move to background."
                               if risk != "low" else "No action needed."),
        })

    return {
        "items": items,
        "summary": {
            "loops_tracked": len(items),
            "high_risk": sum(1 for i in items if i["risk"] == "high"),
            "unknown_license": sum(1 for i in items if i["license_status"] == "unknown"),
        },
    }
