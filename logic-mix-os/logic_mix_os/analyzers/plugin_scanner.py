"""Plugin availability scanner (build packet section 36).

Cross-references the plugins the mix plan recommends against an available
inventory (from the manifest, or assumed Logic stock) and proposes alternatives
for anything missing.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from ..doctrine import load_doctrine

# Fallback alternatives if a recommended stock plugin is somehow unavailable.
_ALTERNATIVES = {
    "Channel EQ": ["Linear Phase EQ", "any parametric EQ"],
    "Compressor": ["Vintage Opto-style optical comp", "any transparent comp"],
    "DeEsser 2": ["any de-esser", "dynamic EQ on 5-8 kHz"],
    "Space Designer": ["ChromaVerb", "any convolution/algorithmic reverb"],
    "ChromaVerb": ["Space Designer", "any plate/hall reverb"],
    "Direction Mixer": ["any mid-side / width utility"],
    "Tape Delay": ["any analog-style delay"],
}


def _normalize(name: str) -> str:
    return re.sub(r"\s*\(.*?\)", "", name).strip()


def scan_plugins(mix_plan: Dict, available: Optional[List[str]] = None) -> Dict:
    stock = load_doctrine("plugin_mapping.logic")["allowed_plugins_mvp"]
    stock_norm = {_normalize(p) for p in stock}
    available_norm = {_normalize(p) for p in available} if available else stock_norm

    used: Dict[str, int] = {}
    for track in mix_plan.get("per_track_actions", []):
        for action in track.get("actions", []):
            name = _normalize(action.get("plugin", ""))
            if name and name != "(arrangement)":
                used[name] = used.get(name, 0) + 1

    missing = []
    for name in used:
        if name not in available_norm:
            missing.append({"plugin": name, "alternatives": _ALTERNATIVES.get(name, ["any equivalent"])})

    return {
        "inventory_source": "manifest" if available else "assumed Logic stock",
        "plugins_used": used,
        "available_count": len(available_norm),
        "missing": missing,
        "all_available": not missing,
    }
