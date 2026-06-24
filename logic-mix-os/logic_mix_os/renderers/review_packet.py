"""Operator review packet (Hardening Packet 5, Layer 2).

Renders a dry-run Logic plan (from :func:`logic_mix_os.logic_planner.plan_logic_actions`)
into an operator-review packet in two forms:

* a structured JSON packet, and
* a human-readable Markdown packet built for a mixer/operator, answering for
  every planned step: *what* I would do in Logic, *why*, the *authority class*,
  the supporting *evidence*, the *rollback plan*, and *why it cannot apply here*.

It renders only — it never executes Logic, mutates a session, or touches audio.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

BANNER = "NOTHING WILL BE APPLIED"
_DRY_RUN_STATEMENT = ("This is a dry-run / spec-only plan. No Logic session, plug-in, send, "
                      "automation, or source file was or will be modified by this packet. "
                      "Class 3+ steps are review-required and cannot execute in this environment.")

_REQUIRED_KEYS = {"banner", "environment", "plan_id", "source_type", "summary",
                  "ledger", "steps", "review_required", "blocked", "unsupported", "statement"}


def _evidence_summary(step: Dict) -> str:
    return "; ".join(step.get("evidence", [])) or "—"


def _rollback_summary(step: Dict) -> str:
    return step.get("rollback_plan") or "—"


def _packet_step(step: Dict) -> Dict:
    return {
        "step_id": step["step_id"],
        "planned_logic_action": step["logic_action"],
        "track": step.get("track"),
        "target": step.get("target"),
        "setting": step.get("setting"),
        "why": step.get("reason"),
        "authority_class": step["authority_class"],
        "authority_name": step["authority_name"],
        "decision": step["decision"],
        "receipt_id": step["receipt_id"],
        "rollback_summary": _rollback_summary(step),
        "evidence_summary": _evidence_summary(step),
        "mapping_supported": step["mapping_supported"],
        "must_not_execute_here": step["must_not_execute_here"],
        "cannot_apply_reason": step["cannot_apply_reason"],
        "applied": step["applied"],
    }


def build_review_packet(plan: Dict) -> Dict:
    """Structured JSON review packet derived from a planner result."""
    steps = [_packet_step(s) for s in plan.get("steps", [])]
    ledger_v = plan.get("ledger_verification")
    return {
        "banner": BANNER,
        "environment": plan.get("environment", "dry_run_spec_only"),
        "plan_id": plan.get("plan_id"),
        "source_type": plan.get("source_type"),
        "source_id": plan.get("source_id"),
        "variant_id": plan.get("variant_id"),
        "mix_plan_id": plan.get("mix_plan_id"),
        "summary": plan.get("summary", {}),
        "ledger": {
            "path": plan.get("ledger_path"),
            "integrity": ("ok" if (ledger_v or {}).get("ok") else
                          ("broken" if ledger_v else "not_persisted")),
            "verification": ledger_v,
        },
        "steps": steps,
        "review_required": [s["step_id"] for s in steps if s["decision"] == "review_required"],
        "blocked": [s["step_id"] for s in steps if s["decision"] == "blocked"],
        "unsupported": plan.get("unsupported", []),
        "nothing_applied": plan.get("nothing_applied", True),
        "statement": _DRY_RUN_STATEMENT,
    }


def validate_review_packet(packet: Dict) -> Dict:
    """Lightweight structural validation (no external schema dependency)."""
    errors: List[str] = []
    missing = _REQUIRED_KEYS - set(packet)
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if packet.get("banner") != BANNER:
        errors.append("banner must be the NOTHING WILL BE APPLIED notice")
    if packet.get("nothing_applied") is not True:
        errors.append("nothing_applied must be true")
    for s in packet.get("steps", []):
        if s.get("applied") is not False:
            errors.append(f"step {s.get('step_id')} is marked applied — forbidden")
        if not s.get("receipt_id"):
            errors.append(f"step {s.get('step_id')} missing receipt_id")
    return {"ok": not errors, "errors": errors}


# --- Markdown -------------------------------------------------------------
def _class_phrase(cls: int, name: str) -> str:
    suffix = {3: "review required", 4: "review required (high-risk)", 5: "blocked (forbidden)"}.get(
        cls, "auto-allowed")
    return f"Class {cls} — {name} — {suffix}"


def _step_block(idx: int, s: Dict) -> str:
    flag = "" if s["mapping_supported"] else "  _(no direct Logic mapping — fail-safe review)_"
    return "\n".join([
        f"### Step {idx} — {s['planned_logic_action']}{flag}",
        f"- **Here is what I would do in Logic:** {s['planned_logic_action']}"
        + (f"  _(track: {s['track']})_" if s.get("track") else ""),
        f"- **Here is why:** {s['why'] or '—'}",
        f"- **Here is the authority class:** {_class_phrase(s['authority_class'], s['authority_name'])}"
        f"  (decision: `{s['decision']}`, receipt `{s['receipt_id']}`)",
        f"- **Here is what evidence supports it:** {s['evidence_summary']}",
        f"- **Here is the rollback plan:** {s['rollback_summary']}",
        f"- **Here is why it cannot apply here:** {s['cannot_apply_reason']}",
        "",
    ])


def render_review_markdown(plan: Dict) -> str:
    packet = build_review_packet(plan)
    steps = packet["steps"]
    summ = packet["summary"]
    src = (f"variant `{packet['variant_id']}`" if packet["source_type"] == "variant"
           else f"mix_plan `{packet['mix_plan_id']}`")
    led = packet["ledger"]
    led_line = (f"`{led['path']}` (integrity: **{led['integrity']}**, "
                f"{(led['verification'] or {}).get('entries', 0)} entries)"
                if led["path"] else "_not persisted (in-memory only)_")

    lines: List[str] = [
        f"# Operator Review Packet — `{packet['plan_id']}`",
        "",
        f"> 🚫 **{BANNER}** — {packet['environment']}.",
        f"> {packet['statement']}",
        "",
        f"**Source:** {src}  ",
        f"**Steps:** {summ.get('total', 0)} — "
        f"{summ.get('allowed', 0)} allowed · {summ.get('review_required', 0)} review-required · "
        f"{summ.get('blocked', 0)} blocked · {summ.get('unsupported', 0)} unsupported  ",
        f"**Audit ledger:** {led_line}",
        "",
        "## What I would do in Logic",
        "",
    ]
    if steps:
        lines += [_step_block(i, s) for i, s in enumerate(steps, 1)]
    else:
        lines.append("_No planned steps._\n")

    blocked = [s for s in steps if s["decision"] == "blocked"]
    lines += ["## ⛔ Blocked steps (Class 5 — forbidden, never applied)", ""]
    lines += ([f"- `{s['step_id']}` — {s['planned_logic_action']} — {s['cannot_apply_reason']}"
               for s in blocked] or ["_None._"])
    lines.append("")

    review = [s for s in steps if s["decision"] == "review_required"]
    lines += ["## 🔶 Review-required steps (Class 3+ — operator approval needed; dry-run only)", ""]
    lines += ([f"- `{s['step_id']}` — {s['planned_logic_action']}" for s in review] or ["_None._"])
    lines.append("")

    lines += ["## ❓ Unsupported / unmapped changes (surfaced, not dropped)", ""]
    lines += ([f"- `{u['step_id']}` — {u['change']} — {u['note']}"
               for u in packet["unsupported"]] or ["_None._"])
    lines += ["", "---", f"_{packet['statement']}_", ""]
    return "\n".join(lines)


def write_review_packet(plan: Dict, out_dir: str) -> Dict:
    """Write both the JSON and Markdown packets; return their paths + the packet."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    packet = build_review_packet(plan)
    json_path = out / "operator_review_packet.json"
    md_path = out / "operator_review_packet.md"
    json_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_review_markdown(plan) + "\n", encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path), "packet": packet}
