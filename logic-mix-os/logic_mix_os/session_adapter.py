"""SessionAdapter contract + FakeSessionAdapter (Hardening Packet 10, Layer 1).

The future execution seam. Packet 9 baked the fake-session mechanics into the
sandbox orchestration; this module extracts a stable ``SessionAdapter`` contract
that the orchestration depends on instead. ``FakeSessionAdapter`` is today's only
implementation; a future ``RealLogicSessionAdapter`` can satisfy the SAME contract
without rewriting manifest validation, diffing, rollback proof, or audit.

    ApplyOrchestrator (apply_sandbox.simulate_apply)
      → SessionAdapter contract
        → FakeSessionAdapter today
        → RealLogicSessionAdapter later

``FakeSessionAdapter`` preserves every Packet-9 guarantee: pure in-memory data,
deterministic target ids, eligible-only mutation, excluded/blocked untouched,
exact rollback — and writes NO ``.logicx``/DAW/session file, calls NO bridge or
AppleScript, runs NO subprocess, and connects to NO real macOS/Logic process.
"""

from __future__ import annotations

import abc
import copy
import hashlib
from typing import Dict, List, Optional

# Documented future adapter type — NOT implemented here (see RealLogicSessionAdapter).
REAL_LOGIC_ADAPTER_TYPE = "real_logic_session"

# --- shared data-structure shapes (documented; plain JSON-able dicts) -------
# session_snapshot : Dict  (adapter-specific; for fake = buckets of inert targets)
# target_id        : str   (stable, derived deterministically from a step)
# simulated_change : {"step_id", "target_id", "before", "after", "planned_action"}
# diff_entry       : {"step_id", "target_id", "planned_action", "before", "after", "rollback"}
# rollback_result  : {"rolled_back_session": session_snapshot}
# capabilities     : Dict  (see FakeSessionAdapter.capabilities)


def _h(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]


class SessionAdapter(abc.ABC):
    """The contract every apply surface (fake today, real Logic later) must satisfy."""

    @abc.abstractmethod
    def adapter_name(self) -> str: ...

    @abc.abstractmethod
    def capabilities(self) -> Dict: ...

    @abc.abstractmethod
    def build_initial_session(self, manifest: Dict) -> Dict: ...

    @abc.abstractmethod
    def resolve_target(self, step: Dict, manifest: Optional[Dict] = None) -> str: ...

    @abc.abstractmethod
    def apply_step(self, session: Dict, step: Dict) -> Dict: ...

    @abc.abstractmethod
    def diff(self, before: Dict, after: Dict) -> List[Dict]: ...

    @abc.abstractmethod
    def rollback(self, after: Dict, diff: List[Dict]) -> Dict: ...

    @abc.abstractmethod
    def verify_rollback(self, before: Dict, rolled_back: Dict) -> bool: ...

    @abc.abstractmethod
    def verify_untouched(self, changed_targets: List[str], excluded_target_ids: List[str],
                         blocked_target_ids: List[str]) -> bool: ...


# --- free-text change -> fake target kind (moved from apply_sandbox) --------
_KIND_BUCKET = [
    (("aux send", "send", "plate", "reverb", "delay", "room", "chamber", "hall"),
     "fake_send", "fake_sends"),
    (("plugin", "channel eq", " eq", "compress", "limiter", "stereo-width", "width", "imager"),
     "fake_plugin_slot", "fake_plugin_slots"),
    (("automation", "ride", "fader", "throw", "automate"),
     "fake_automation_lane", "fake_automation_lanes"),
    (("arrangement", "region", "mute", "chop", "one-shot", "accent"),
     "fake_region_edit", "fake_region_edits"),
]
_BUCKETS = ("fake_sends", "fake_plugin_slots", "fake_automation_lanes",
            "fake_region_edits", "fake_parameters")


def _kind_and_bucket(action: str):
    low = (action or "").lower()
    for needles, kind, bucket in _KIND_BUCKET:
        if any(n in low for n in needles):
            return kind, bucket
    return "fake_parameter", "fake_parameters"


class FakeSessionAdapter(SessionAdapter):
    """In-memory, inert implementation of the SessionAdapter contract.

    Owns ALL fake-session mechanics that Packet 9 had inline: session
    construction, target-id derivation, step mutation, diff, rollback, and the
    untouched-target proof. Pure data; touches nothing real.
    """

    NAME = "FakeSessionAdapter"

    def adapter_name(self) -> str:
        return self.NAME

    def capabilities(self) -> Dict:
        return {
            "adapter_type": "fake_session",
            "real_daw": False,
            "writes_project_files": False,
            "supports_real_apply": False,
            "supports_simulated_apply": True,
            "supports_rollback": True,
            "requires_macos": False,
            "requires_logic": False,
            "allowed_authority_classes": ["simulated_only"],
        }

    # -- target identity ----------------------------------------------------
    def resolve_target(self, step: Dict, manifest: Optional[Dict] = None) -> str:
        """Deterministic, stable fake-target id derived from the manifest step id."""
        return "tgt_" + _h(str(step.get("step_id")))

    # -- session construction ----------------------------------------------
    def build_initial_session(self, manifest: Dict) -> Dict:
        session: Dict = {
            "session_id": "fakesess_" + _h(str(manifest.get("manifest_id", "")) + "|"
                                           + str(manifest.get("manifest_hash", ""))),
            "is_fake": True,
            "real_logic": False,
            "environment": "simulated_sandbox",
            "adapter": self.NAME,
            "fake_tracks": {},
        }
        for b in _BUCKETS:
            session[b] = {}
        for s in manifest.get("eligible_for_future_apply", []):
            sid = s.get("step_id")
            tid = self.resolve_target(s, manifest)
            kind, bucket = _kind_and_bucket(s.get("planned_logic_action", ""))
            session["fake_tracks"][tid] = {"track_id": "trk_" + _h(str(sid)), "for_target": tid}
            session[bucket][tid] = {
                "target_id": tid, "step_id": sid, "kind": kind,
                "name": s.get("planned_logic_action"), "value": {"configured": False},
            }
        return session

    # -- mutation -----------------------------------------------------------
    def _all_targets(self, session: Dict) -> Dict[str, Dict]:
        out: Dict[str, Dict] = {}
        for b in _BUCKETS:
            out.update(session.get(b, {}))
        return out

    def _set_value(self, session: Dict, target_id: str, value: Dict) -> None:
        for b in _BUCKETS:
            if target_id in session.get(b, {}):
                session[b][target_id]["value"] = value
                return

    def apply_step(self, session: Dict, step: Dict) -> Dict:
        tid = self.resolve_target(step)
        before_val = {"configured": False}
        after_val = {"configured": True, "action": step.get("planned_logic_action")}
        self._set_value(session, tid, after_val)
        return {"step_id": step.get("step_id"), "target_id": tid,
                "planned_action": step.get("planned_logic_action"),
                "before": before_val, "after": after_val}

    # -- diff / rollback / proofs ------------------------------------------
    def diff(self, before: Dict, after: Dict) -> List[Dict]:
        bt, at = self._all_targets(before), self._all_targets(after)
        out: List[Dict] = []
        for tid, a in at.items():
            b = bt.get(tid, {})
            if a.get("value") != b.get("value"):
                out.append({
                    "step_id": a.get("step_id"), "target_id": tid,
                    "planned_action": (a.get("value") or {}).get("action") or a.get("name"),
                    "before": b.get("value"), "after": a.get("value"), "rollback": b.get("value"),
                })
        out.sort(key=lambda d: d["target_id"])     # deterministic order
        return out

    def rollback(self, after: Dict, diff: List[Dict]) -> Dict:
        rolled = copy.deepcopy(after)
        for d in diff:
            self._set_value(rolled, d["target_id"], d["rollback"])
        return {"rolled_back_session": rolled}

    def verify_rollback(self, before: Dict, rolled_back: Dict) -> bool:
        rb = rolled_back.get("rolled_back_session", rolled_back) if isinstance(rolled_back, dict) else rolled_back
        return rb == before

    def verify_untouched(self, changed_targets: List[str], excluded_target_ids: List[str],
                         blocked_target_ids: List[str]) -> bool:
        return not (set(changed_targets) & (set(excluded_target_ids) | set(blocked_target_ids)))


class RealLogicSessionAdapter(SessionAdapter):
    """Documented future seam — NOT implemented in this environment.

    A real macOS/Logic adapter will implement the SAME SessionAdapter contract.
    It is intentionally non-functional here: constructing it raises, so no real
    Logic pathway can be reached. This class exists only to name the seam.
    """

    NAME = "RealLogicSessionAdapter"

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "RealLogicSessionAdapter is a documented future seam and is not implemented "
            "in this environment. No real macOS/Logic surface exists yet.")

    def adapter_name(self) -> str:  # pragma: no cover - unreachable (init raises)
        return self.NAME

    def capabilities(self) -> Dict:  # pragma: no cover
        return {"adapter_type": REAL_LOGIC_ADAPTER_TYPE, "real_daw": True}

    def build_initial_session(self, manifest):  # pragma: no cover
        raise NotImplementedError

    def resolve_target(self, step, manifest=None):  # pragma: no cover
        raise NotImplementedError

    def apply_step(self, session, step):  # pragma: no cover
        raise NotImplementedError

    def diff(self, before, after):  # pragma: no cover
        raise NotImplementedError

    def rollback(self, after, diff):  # pragma: no cover
        raise NotImplementedError

    def verify_rollback(self, before, rolled_back):  # pragma: no cover
        raise NotImplementedError

    def verify_untouched(self, changed_targets, excluded_target_ids, blocked_target_ids):  # pragma: no cover
        raise NotImplementedError
