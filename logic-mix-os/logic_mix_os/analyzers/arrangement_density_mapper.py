"""Arrangement density mapper (build packet sections 25.2 / 50.5).

Counts how many elements occupy each depth layer per section, surfacing the
classic dense-arrangement failure: everything technically audible, nothing with
hierarchy.
"""

from __future__ import annotations

from typing import Dict, List

FORWARD = {"intimate", "foreground"}


def map_density(records: List[Dict], sections: List[Dict]) -> Dict:
    section_ids = [s["section_id"] for s in sections] if sections else ["full"]
    per_section: List[Dict] = []

    for sid in section_ids:
        counts = {"intimate": 0, "foreground": 0, "midground": 0, "background": 0}
        for r in records:
            layer = r.get("depth_by_section", {}).get(sid, r.get("depth_default", "midground"))
            counts[layer] = counts.get(layer, 0) + 1
        forward = counts["intimate"] + counts["foreground"]
        density_metric = next(
            (s["metrics"]["density"] for s in sections if s["section_id"] == sid), None
        )
        warning = None
        if forward >= 6:
            warning = (
                f"{forward} elements occupy forward layers in '{sid}'. Consider moving "
                f"decorative synths/loops to midground/background for hierarchy."
            )
        per_section.append({
            "section_id": sid,
            "layer_counts": counts,
            "forward_count": forward,
            "density_metric": density_metric,
            "warning": warning,
        })

    crowded = [p["section_id"] for p in per_section if p["warning"]]
    return {
        "per_section": per_section,
        "crowded_sections": crowded,
        "summary": {"total_sections": len(per_section), "crowded": len(crowded)},
    }
