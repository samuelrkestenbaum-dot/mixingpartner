"""Operator decision packet renderer (Hardening Packet 6, Layer 2).

Renders the operator decision state (from
:class:`logic_mix_os.review_workflow.ReviewWorkflow`) into a human-readable
Markdown artifact alongside the JSON state, under a
``DECISIONS RECORDED — NOTHING APPLIED`` banner.

Rendering only — it never executes Logic, mutates a session, or touches audio.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from ..review_workflow import DECISIONS_BANNER

_STATEMENT = ("These are recorded operator decisions on a dry-run / spec-only plan. "
              "No Logic session, plug-in, send, automation, or source file was or will be "
              "modified. Approval means approved-for-future-apply, not applied.")

_LABEL = {"approve": "✅ approve", "reject": "⛔ reject",
          "request_revision": "✏️ request revision", "defer": "⏸️ defer"}


def _table(decisions: List[Dict]) -> List[str]:
    rows = ["| Step | Decision | Resulting state | Class | Actor | Receipt | Reason |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for d in decisions:
        rows.append(
            f"| `{d['step_id']}` | {_LABEL.get(d['decision'], d['decision'])} | "
            f"`{d['resulting_state']}` | C{d['authority_class']} | {d['actor']} | "
            f"`{d['receipt_id']}` | {d.get('reason') or '—'} |")
    return rows


def render_decisions_markdown(state: Dict) -> str:
    decisions = state.get("decisions", [])
    summ = state.get("summary", {})
    led = state.get("ledger_path")
    ledv = state.get("ledger_verification") or {}
    led_line = (f"`{led}` (integrity: **{'ok' if ledv.get('ok') else 'broken'}**, "
                f"{ledv.get('entries', 0)} entries)" if led else "_not persisted (in-memory only)_")
    last_ts = decisions[-1]["timestamp"] if decisions else "—"

    lines: List[str] = [
        f"# Operator Decisions — `{state.get('plan_id')}`",
        "",
        f"> ✅ **{DECISIONS_BANNER}** — {state.get('environment', 'dry_run_spec_only')}.",
        f"> {_STATEMENT}",
        "",
        f"**Plan:** `{state.get('plan_id')}` ({state.get('source_type')} `{state.get('source_id')}`)  ",
        f"**Decisions recorded:** {summ.get('decisions_recorded', 0)} of {summ.get('total_steps', 0)} steps "
        f"(last recorded: {last_ts})  ",
        f"**Tally:** {summ.get('approved', 0)} approved · {summ.get('rejected', 0)} rejected · "
        f"{summ.get('revision_requested', 0)} revision-requested · {summ.get('deferred', 0)} deferred · "
        f"{summ.get('pending', 0)} pending · {summ.get('blocked', 0)} blocked  ",
        f"**Audit ledger:** {led_line}",
        "",
        "## Decisions",
        "",
    ]
    lines += _table(decisions) if decisions else ["_No decisions recorded yet._"]
    lines.append("")

    approvals = [d for d in decisions if d["decision"] == "approve"]
    lines += ["## ✅ Approval receipts (approved for future apply — NOT applied)", ""]
    lines += ([f"- `{d['step_id']}` — {d['planned_logic_action']} — by **{d['actor']}** "
               f"(receipt `{d['receipt_id']}`, audit `{d['audit_event_id']}`); state: `{d['resulting_state']}`, "
               f"applied: `{d['applied']}`" for d in approvals] or ["_None._"])
    lines.append("")

    reasoned = [d for d in decisions if d["decision"] in ("reject", "request_revision")]
    lines += ["## ⛔/✏️ Rejections & revision requests (with reasons)", ""]
    lines += ([f"- `{d['step_id']}` — **{d['decision']}** by {d['actor']}: {d.get('reason') or '—'}"
               for d in reasoned] or ["_None._"])
    lines.append("")

    deferred = [d for d in decisions if d["decision"] == "defer"]
    lines += ["## ⏸️ Deferred steps", ""]
    lines += ([f"- `{d['step_id']}` — deferred by {d['actor']}" for d in deferred] or ["_None._"])
    lines += ["", "---", f"_{_STATEMENT}_", ""]
    return "\n".join(lines)


def write_decision_packet(state: Dict, out_dir: str) -> Dict:
    """Write both operator_decisions.json and operator_decisions.md; return paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "operator_decisions.json"
    md_path = out / "operator_decisions.md"
    json_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_decisions_markdown(state) + "\n", encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path)}
