"""Dry-run Logic action planner (Hardening Packet 5, Layer 1).

Turns a creative *recommendation* — either a chosen variant or a ``mix_plan`` —
into a governed, **dry-run/spec-only** Logic action plan. Every planned Logic
step is routed through the Packet-4 governance kernel (authority class, receipt,
rollback plan) and recorded to the persisted, hash-chained audit ledger when a
ledger path is given.

This module plans Logic work; it never performs it. It does NOT run Logic, does
NOT mutate a session, does NOT invoke AppleScript, and does NOT change the
behaviour of ``bridge/exporter``, ``bridge/executor`` or ``bridge/applescript_bridge``
(it only reuses the exporter read-only to normalise a mix_plan). Class 3+ steps
are review-required and ``must_not_execute_here``; nothing is ever applied.

Pure, deterministic, local. No DAW, no network, no execution.
"""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional

from .bridge.exporter import export_actions
from .governance_kernel import GovernanceKernel

# Free-text change -> (Logic action kind, verb) heuristics, ordered: first match
# wins. Kinds line up with the governance kernel's Class-3 vocabulary so a planned
# Logic move classifies as controlled_daw_mutation (dry-run/spec only here).
_CHANGE_MAP = [
    (("high-pass", "low-pass", "hi-pass", "highpass", "filter", " eq", "eq ", " hz", "khz",
      "cut ", "boost", "shelf", "mud"), "insert_plugin", "Insert/adjust Channel EQ"),
    (("compress", "compressor", "limiter", "gain reduction", "opto"), "insert_plugin",
     "Insert/adjust dynamics plugin"),
    (("widen", "wider", "width", "narrow", "stereo", "mono", "imager", "mid/side", "m/s"),
     "insert_plugin", "Insert/adjust stereo-width plugin"),
    (("send", "plate", "reverb", "delay throw", "room ", "chamber", "hall", "space"),
     "set_send", "Set/adjust aux send"),
    (("ride", "automate", "automation", "fader", "throw", "+1 db", "+0.5", "level into",
      "swell", "gesture"), "automation", "Write automation"),
    (("mute", "remove", "chop", "one-shot", "one shot", "accent", "deconstruct", "duplicate",
      "transition", "re-contextualise", "recontextualise", "drop ", "withhold", "simplify"),
     "arrangement", "Arrangement / region edit"),
    (("midground", "background", "foreground", "depth", "push to", "move to"), "set_send",
     "Depth placement via send"),
]

_RISK_HINTS = ("overwrite", "delete source", "in place", "in-place", "destroy", "hidden",
               "unlogged", "mutate source", "export master", "final master", "upload",
               "share externally", "replace source")


def _sid(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:6]


def _map_change(text: str) -> Optional[Dict]:
    """Map one free-text variant change to a Logic action kind, or None if unmapped."""
    low = text.lower()
    for needles, kind, verb in _CHANGE_MAP:
        if any(n in low for n in needles):
            return {"kind": kind, "verb": verb}
    return None


def _step(step_id: str, kind: str, logic_action: str, *, track: Optional[str], target: Optional[str],
          setting: Optional[str], reason: str, evidence: List[str], mapping_supported: bool) -> Dict:
    return {
        "step_id": step_id, "kind": kind, "logic_action": logic_action, "track": track,
        "target": target, "setting": setting, "reason": reason, "evidence": evidence,
        "mapping_supported": mapping_supported,
    }


# --- source normalisation (both inputs -> one flat step list) --------------
def _normalize_variant(variant: Dict) -> List[Dict]:
    vid = variant.get("variant_id", "variant")
    vkind = variant.get("kind", "")
    tracks = variant.get("tracks_affected") or []
    hypothesis = variant.get("creative_hypothesis", "")
    expected = variant.get("expected_strength", "")
    base_evidence = [e for e in (
        f"variant {vid} ({vkind})" if vkind else f"variant {vid}",
        f"hypothesis: {hypothesis}" if hypothesis else "",
        f"expected: {expected}" if expected else "",
    ) if e]

    steps: List[Dict] = []
    track = tracks[0] if tracks else None
    for i, change in enumerate(variant.get("changes", [])):
        change = str(change)
        mapping = _map_change(change)
        sid = f"{vid}:{i:02d}:{_sid(change)}"
        if mapping is None:
            # Never drop it: route as an unknown kind so the kernel fail-safe-high
            # gate reviews it (and escalates if it carries risk markers).
            steps.append(_step(
                sid, "unmapped_change",
                f"(No direct Logic mapping) proposed change: {change}",
                track=track, target=None, setting=change, reason=change,
                evidence=base_evidence, mapping_supported=False))
        else:
            steps.append(_step(
                sid, mapping["kind"], f"{mapping['verb']}: {change}",
                track=track, target=mapping["verb"], setting=change, reason=change,
                evidence=base_evidence, mapping_supported=True))
    return steps


def _normalize_mix_plan(mix_plan: Dict) -> List[Dict]:
    steps: List[Dict] = []
    for a in export_actions(mix_plan):  # read-only reuse of the legacy exporter
        evidence = [e for e in (a.get("reason", ""), a.get("validation", "")) if e]
        steps.append(_step(
            a["id"], a["type"],
            f"{a['type'].replace('_', ' ')} on '{a['track']}': {a.get('settings') or a.get('plugin')}",
            track=a.get("track"), target=a.get("plugin"), setting=a.get("settings"),
            reason=a.get("reason", ""), evidence=evidence, mapping_supported=True))
    return steps


def _select_variant(source: Dict, variant_id: Optional[str]) -> Optional[Dict]:
    """Pull a single variant out of a creative-engine result (branches/variants)."""
    branches = source.get("branches", [])
    if variant_id is None:
        first = branches[0] if branches else {}
        win = (first.get("winning") or {}).get("winning_variant")
        variant_id = win
    for b in branches:
        for v in b.get("variants", []):
            if v.get("variant_id") == variant_id:
                return v
    return None


def _classify_source(source: Dict, variant_id: Optional[str]):
    """Return (source_type, source_id, variant_dict_or_None)."""
    if "per_track_actions" in source:
        return "mix_plan", source.get("song_title", "mix_plan"), None
    if "branches" in source:  # full creative-engine result
        v = _select_variant(source, variant_id)
        return "variant", (v or {}).get("variant_id", variant_id or "variant"), v
    if "changes" in source or "variant_id" in source:  # a single variant recommendation
        return "variant", source.get("variant_id", "variant"), source
    raise ValueError("Unrecognised planner source: expected a mix_plan, a creative result, "
                     "or a variant recommendation.")


# --- the planner -----------------------------------------------------------
def plan_logic_actions(source: Dict, *, variant_id: Optional[str] = None,
                       kernel: Optional[GovernanceKernel] = None,
                       ledger_path: Optional[str] = None,
                       plan_id: Optional[str] = None) -> Dict:
    """Plan governed, dry-run-only Logic steps from a variant or a mix_plan.

    Every step is classified through ``GovernanceKernel.propose`` and (when a
    ledger path is given) recorded to the persisted hash-chained audit ledger.
    Nothing is applied: Class 3+ steps are review-required and must_not_execute_here.
    """
    source_type, source_id, variant = _classify_source(source, variant_id)
    if source_type == "variant":
        if variant is None:
            raise ValueError(f"variant '{variant_id}' not found in source")
        raw_steps = _normalize_variant(variant)
    else:
        raw_steps = _normalize_mix_plan(source)

    kernel = kernel or GovernanceKernel(ledger_path=ledger_path)
    plan_id = plan_id or ("plan_" + _sid(f"{source_type}|{source_id}|{len(raw_steps)}"))

    steps: List[Dict] = []
    counts = {"allowed": 0, "review_required": 0, "blocked": 0}
    for s in raw_steps:
        receipt = kernel.propose({
            "kind": s["kind"],
            "setting": s["setting"],
            "reason": s["reason"],
            "intent": s["logic_action"],
            "source_artifacts": [s["track"]] if s["track"] else [],
            "target_artifacts": [f"{plan_id} (dry-run plan artifact)"],
            "source_immutable": True,
            "generated_output_only": True,
            "evidence": s["evidence"],
        })
        decision = receipt["decision"]
        counts[decision if decision in counts else "review_required"] = \
            counts.get(decision if decision in counts else "review_required", 0) + 1
        steps.append({
            **s,
            "authority_class": receipt["authority_class"],
            "authority_name": receipt["authority_name"],
            "decision": decision,
            "receipt_id": receipt["receipt_id"],
            "action_id": receipt["action_id"],
            "rollback_plan": receipt["rollback_plan"],
            "reversibility": receipt["reversibility"],
            "must_not_execute_here": receipt["must_not_execute_here"],
            "ambiguous": receipt["ambiguous"],
            "unknown_kind": receipt["unknown_kind"],
            "classification_reason": receipt["classification_reason"],
            "cannot_apply_reason": _cannot_apply_reason(receipt["authority_class"]),
            "applied": False,
            "receipt": receipt,
        })

    plan = {
        "plan_id": plan_id,
        "source_type": source_type,
        "source_id": source_id,
        "variant_id": source_id if source_type == "variant" else None,
        "mix_plan_id": source_id if source_type == "mix_plan" else None,
        "steps": steps,
        "unsupported": [
            {"step_id": s["step_id"], "change": s["reason"], "authority_class": s["authority_class"],
             "decision": s["decision"],
             "note": "No direct Logic action mapping — routed to fail-safe-high review."}
            for s in steps if not s["mapping_supported"]
        ],
        "summary": {
            "total": len(steps),
            "allowed": counts["allowed"],
            "review_required": counts["review_required"],
            "blocked": counts["blocked"],
            "unsupported": sum(1 for s in steps if not s["mapping_supported"]),
        },
        "ledger_path": ledger_path,
        "ledger_verification": kernel.verify_ledger() if ledger_path else None,
        "environment": "dry_run_spec_only",
        "nothing_applied": True,
    }
    return plan


def _cannot_apply_reason(cls: int) -> str:
    if cls >= 5:
        return "Class 5 is forbidden and is always blocked — never applied."
    if cls >= 3:
        return ("Class 3+ controlled DAW mutation is dry-run/spec only in this environment; "
                "mark_applied refuses it. No Logic session is touched.")
    return "Reversible local action; still not applied by the planner (plan/preview only)."
