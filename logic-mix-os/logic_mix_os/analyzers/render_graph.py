"""Render dependency graph (build packet section 35).

Models source -> stem -> mixdown -> analysis-report dependencies so Cowork knows
what becomes stale when a source changes (e.g. editing a synth MIDI invalidates
its stem, the mix bounce, and the reference-delta report).
"""

from __future__ import annotations

from typing import Dict, List

REPORTS = [
    "track_analysis", "section_analysis", "masking_report", "depth_map",
    "doctrine_score", "mix_plan", "reference_delta", "expanded_analysis",
]


def build_render_graph(project) -> Dict:
    nodes: List[Dict] = []
    edges: List[Dict] = []

    for track in project.tracks:
        src = f"source:{track.track_id}"
        stem = f"stem:{track.track_id}"
        nodes.append({"id": src, "type": "source", "name": track.name})
        nodes.append({"id": stem, "type": "stem", "name": track.name})
        edges.append({"from": src, "to": stem})
        edges.append({"from": stem, "to": "bounce:mixdown"})

    nodes.append({"id": "bounce:mixdown", "type": "bounce", "name": "Full Mix Bounce"})
    for r in REPORTS:
        nodes.append({"id": f"report:{r}", "type": "report", "name": r})
        edges.append({"from": "bounce:mixdown", "to": f"report:{r}"})

    return {"nodes": nodes, "edges": edges}


def stale_after(graph: Dict, changed_node: str) -> List[str]:
    """Return every downstream node invalidated by a change to ``changed_node``."""
    adj: Dict[str, List[str]] = {}
    for e in graph["edges"]:
        adj.setdefault(e["from"], []).append(e["to"])

    stale: List[str] = []
    stack = list(adj.get(changed_node, []))
    seen = set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stale.append(node)
        stack.extend(adj.get(node, []))
    return stale
