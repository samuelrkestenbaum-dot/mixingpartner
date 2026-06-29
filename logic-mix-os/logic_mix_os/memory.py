"""Session memory, decision ledger, and taste calibration (spec 32, 37, 38, 39).

Local, file-backed persistence so the system can remember mix passes, log
bounded decisions (evidence + reason + validation + recovery), and learn taste
over time. Everything is plain JSON under a memory directory — no database, no
network. Nothing here is destructive.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional

from .constants import EVENT_TYPES

SCORE_KEYS = [
    "overall_mix_readiness_score", "halee_score", "ramone_score", "static_mix_score",
    "dynamic_mix_score", "section_contrast_score", "depth_hierarchy_score",
    "vocal_centrality_score", "translation_score", "mono_compatibility_score",
]

# feedback label -> taste statement when it recurs
_TASTE_MAP = {
    "too wide": "tends to prefer narrower stereo images",
    "too narrow": "prefers wider images",
    "too modern": "prefers a less modern/hyped sound",
    "too vintage": "prefers a less vintage/dull sound",
    "too dry": "prefers more space / wetness",
    "too wet": "prefers a drier, closer sound",
    "too polished": "prefers a rawer, more human sound",
    "too raw": "prefers a touch more polish",
}


def _scores_from_result(result) -> Dict:
    out = {}
    for k in SCORE_KEYS:
        out[k] = result.doctrine_score.get(k, result.mix_plan.get(k))
    return out


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class ProjectMemory:
    def __init__(self, memory_dir: str | Path):
        self.dir = Path(memory_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.passes_path = self.dir / "mix_pass_history.json"
        self.ledger_path = self.dir / "decision_ledger.json"
        self.taste_path = self.dir / "taste_profile.json"
        self.refs_path = self.dir / "reference_profiles.json"

    # -- low-level io -------------------------------------------------------
    def _load(self, path: Path, default):
        if path.exists():
            return json.loads(path.read_text())
        return default

    def _save(self, path: Path, data) -> None:
        path.write_text(json.dumps(data, indent=2) + "\n")

    # -- mix pass history ---------------------------------------------------
    def record_pass(self, name: str, result, changes: Optional[List[str]] = None,
                    input_bounce: Optional[str] = None) -> Dict:
        history = self._load(self.passes_path, [])
        scores = _scores_from_result(result)
        prev = history[-1]["scores"] if history else None

        improved, worse = [], []
        if prev:
            for k, v in scores.items():
                pv = prev.get(k)
                if v is None or pv is None:
                    continue
                if v - pv > 1.0:
                    improved.append(f"{k} {pv}->{v}")
                elif pv - v > 1.0:
                    worse.append(f"{k} {pv}->{v}")

        record = {
            "pass_name": name,
            "date": _now(),
            "input_bounce": input_bounce,
            "scores": scores,
            "changes_made": changes or [],
            "improved": improved,
            "got_worse": worse,
            "revert_candidates": worse,
            "next_recommended": [i["title"] for i in result.mix_plan.get("next_pass", [])][:3],
        }
        history.append(record)
        self._save(self.passes_path, history)
        return record

    def history(self) -> List[Dict]:
        return self._load(self.passes_path, [])

    # -- decision ledger ----------------------------------------------------
    def add_decision(self, decision: Dict, event_type: Optional[str] = None) -> Dict:
        if event_type is not None and event_type not in EVENT_TYPES:
            raise ValueError(f"Unknown event type: {event_type}. Allowed: {EVENT_TYPES}")
        ledger = self._load(self.ledger_path, [])
        decision = {"date": _now(), **decision}
        if event_type is not None:
            decision["event_type"] = event_type
        ledger.append(decision)
        self._save(self.ledger_path, ledger)
        return decision

    def record_plan_decisions(self, result) -> List[Dict]:
        """Auto-log the headline decisions from a mix plan."""
        added = []
        for m in result.mix_plan.get("mute_candidates", [])[:5]:
            added.append(self.add_decision({
                "decision": f"Consider muting/chopping {m['element']}",
                "reason": m["reason"],
                "doctrine": ["sacred_vs_expendable", "felt_vs_heard"],
                "risk": f"Class {m.get('risk_class', 3)}",
                "validation": "Check chorus width and emotional lift after render.",
            }))
        return added

    def ledger(self) -> List[Dict]:
        return self._load(self.ledger_path, [])

    # -- taste calibration --------------------------------------------------
    def add_feedback(self, label: str, context: Optional[str] = None) -> Dict:
        taste = self._load(self.taste_path, {"feedback": [], "profile": []})
        taste["feedback"].append({"label": label.lower().strip(), "context": context, "date": _now()})
        taste["profile"] = self._derive_taste(taste["feedback"])
        self._save(self.taste_path, taste)
        return taste

    def _derive_taste(self, feedback: List[Dict]) -> List[str]:
        counts: Dict[str, int] = {}
        for f in feedback:
            counts[f["label"]] = counts.get(f["label"], 0) + 1
        statements = []
        for label, statement in _TASTE_MAP.items():
            if counts.get(label, 0) >= 2:
                statements.append(statement)
        return statements

    def taste_profile(self) -> Dict:
        return self._load(self.taste_path, {"feedback": [], "profile": []})

    # -- reference profiles -------------------------------------------------
    def save_reference_profile(self, name: str, metrics: Dict) -> None:
        refs = self._load(self.refs_path, {})
        refs[name] = metrics
        self._save(self.refs_path, refs)

    def reference_profiles(self) -> Dict:
        return self._load(self.refs_path, {})
