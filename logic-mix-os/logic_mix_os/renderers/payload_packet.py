"""Typed payload negotiation report renderer (Hardening Packet 11, Layer 2).

Renders a negotiation result (from
:func:`logic_mix_os.logic_action_payload.negotiate_payloads`) into JSON + a
human-readable Markdown report under a
``TYPED LOGIC ACTION PAYLOAD NEGOTIATION — NO REAL DAW`` banner.

Rendering only — it never executes Logic, writes a ``.logicx``/DAW/session file,
calls the bridge/AppleScript, runs a subprocess, or touches audio. The payloads
it renders are inert intent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

PAYLOAD_BANNER = "TYPED LOGIC ACTION PAYLOAD NEGOTIATION — NO REAL DAW"


def _fmt_value(value: Dict) -> str:
    if not value:
        return "—"
    amount, unit, direction = value.get("amount"), value.get("unit"), value.get("direction")
    parts: List[str] = []
    if direction:
        parts.append(str(direction))
    if amount is not None:
        parts.append(f"{amount}{(' ' + unit) if unit else ''}")
    elif unit:
        parts.append(str(unit))
    return " ".join(parts) if parts else "—"


def _tick(flag) -> str:
    if flag is True:
        return "✅"
    if flag is False:
        return "❌"
    return "—"


def _payload_table(payloads: List[Dict]) -> List[str]:
    rows = ["| Step | Action type | Parameter | Value | Authority | Negotiated | Reversible |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for p in payloads:
        neg = p.get("negotiation", {})
        op = p.get("operation", {})
        rows.append(
            f"| `{p.get('step_id')}` | `{p.get('action_type')}` | `{p.get('parameter')}` | "
            f"{_fmt_value(p.get('value', {}))} | `{p.get('authority_class')}` | "
            f"{_tick(neg.get('accepted'))} | {_tick(op.get('reversible_through_adapter'))} |")
    return rows


def _adapter_section(result: Dict) -> List[str]:
    a = result.get("adapter") or {}
    caps = a.get("capabilities") or {}
    return [
        "## 🔌 Session Adapter Boundary", "",
        f"- **active adapter:** `{a.get('name', 'FakeSessionAdapter')}`",
        f"- adapter type: `{caps.get('adapter_type')}`",
        f"- real DAW support: `{caps.get('real_daw')}`",
        f"- real apply support: `{caps.get('supports_real_apply')}`",
        f"- simulated apply support: `{caps.get('supports_simulated_apply')}`",
        f"- rollback support: `{caps.get('supports_rollback')}`",
        f"- allowed execution authority: `{caps.get('allowed_authority_classes')}`",
        f"- supported action types: `{caps.get('supported_action_types', 'unrestricted')}`",
        "",
        "_Capability negotiation runs each typed payload against this exact interface. "
        "A future `RealLogicSessionAdapter` would advertise different capabilities and "
        "the SAME negotiation would admit or refuse the SAME payloads — unchanged._",
        "",
    ]


def _boundary_note() -> List[str]:
    return [
        "- Typed payloads are **inert intent** — never applied.",
        "- Operations are driven only through the **fake in-memory** adapter.",
        "- No `.logicx` writes. · No real DAW. · No AppleScript. · No subprocess. · No source mutation.",
    ]


def render_payload_markdown(result: Dict) -> str:
    audit = result.get("audit", {})
    ev = (f"`{audit.get('ledger_event_id')}` (entry `{audit.get('ledger_entry_hash')}`)"
          if audit.get("ledger_event_id") else "_none (not persisted)_")
    status = "recorded (negotiated)" if result.get("ok") else "refused"
    counts = result.get("counts", {})

    lines: List[str] = [
        f"# Logic Action Payload Negotiation — `{result.get('manifest_id')}`",
        "",
        f"> 🧪 **{PAYLOAD_BANNER}**",
        "",
        f"**Plan:** `{result.get('plan_id')}`  ",
        f"**Manifest id:** `{result.get('manifest_id')}`  ",
        f"**Manifest hash:** `{result.get('manifest_hash')}`  ",
        f"**Negotiation status:** `{status}`  ",
        f"**Ledger status:** {audit.get('ledger_status')}  ",
        f"**Audit event:** {ev}",
        "",
        "## 🚫 No-real-DAW guarantee", "",
        f"- real_applied: `{result.get('real_applied')}`",
        f"- real_executed: `{result.get('real_executed')}`",
        f"- touched_real_logic: `{result.get('touched_real_logic')}`",
        f"- no_real_daw: `{result.get('no_real_daw')}`",
        f"- environment: `{result.get('environment')}`",
        "",
    ]
    lines += _adapter_section(result)

    if not result.get("ok"):
        lines += ["## ⛔ Refused", "", f"- reason: {result.get('reason')}", "",
                  "## 📋 Boundary note", ""]
        lines += _boundary_note()
        lines += ["", "---", f"_{result.get('reason')}_", ""]
        return "\n".join(lines)

    lines += [
        f"## 🤝 Capability negotiation — {counts.get('payloads', 0)} payload(s)", "",
        f"- accepted: **{counts.get('accepted', 0)}**  ·  refused: **{counts.get('refused', 0)}**  ·  "
        f"reversible: **{counts.get('reversible', 0)}**",
        f"- operations driven: `{result.get('operations_driven')}`  ·  "
        f"all accepted reversible: `{result.get('all_accepted_reversible')}`",
        "",
    ]
    lines += _payload_table(result.get("payloads", []))
    refused = [p for p in result.get("payloads", []) if not p.get("negotiation", {}).get("accepted")]
    if refused:
        lines += ["", "### ⛔ Refused payloads", ""]
        for p in refused:
            reasons = "; ".join(p.get("negotiation", {}).get("reasons", [])) or "—"
            lines.append(f"- `{p.get('step_id')}` (`{p.get('action_type')}`): {reasons}")
    lines += ["", "## 📋 Boundary note", ""]
    lines += _boundary_note()
    lines += ["", "---", f"_{result.get('reason')}_", ""]
    return "\n".join(lines)


def write_payload_packet(result: Dict, out_dir: str) -> Dict:
    """Write payload_negotiation_report.json + .md; return their paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "payload_negotiation_report.json"
    md_path = out / "payload_negotiation_report.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_payload_markdown(result) + "\n", encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path)}
