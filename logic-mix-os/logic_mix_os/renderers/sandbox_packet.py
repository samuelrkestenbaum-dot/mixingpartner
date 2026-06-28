"""Simulated sandbox report renderer (Hardening Packet 9, Layer 2).

Renders a sandbox simulation result (from
:func:`logic_mix_os.apply_sandbox.simulate_apply`) into JSON + human-readable
Markdown under a ``SIMULATED LOGIC SANDBOX — FAKE SESSION, NO REAL DAW`` banner.

Rendering only — the reports may persist, but the fake session itself is inert
in-memory data. It never executes Logic, writes a ``.logicx``/DAW/session file,
calls the bridge/AppleScript, or touches audio.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

SANDBOX_BANNER = "SIMULATED LOGIC SANDBOX — FAKE SESSION, NO REAL DAW"


def _diff_table(diff: List[Dict]) -> List[str]:
    rows = ["| Step | Target | Planned action | Before | After | Rollback |",
            "| --- | --- | --- | --- | --- | --- |"]
    for d in diff:
        rows.append(
            f"| `{d['step_id']}` | `{d['target_id']}` | {d.get('planned_action')} | "
            f"`{d['before'].get('configured')}` | `{d['after'].get('configured')}` | "
            f"`{d['rollback'].get('configured')}` |")
    return rows


def render_sandbox_markdown(result: Dict) -> str:
    audit = result.get("audit", {})
    ev = (f"`{audit.get('ledger_event_id')}` (entry `{audit.get('ledger_entry_hash')}`)"
          if audit.get("ledger_event_id") else "_none (not persisted)_")
    status = "recorded (simulated)" if result.get("ok") else "refused"

    lines: List[str] = [
        f"# Sandbox Simulation — `{result.get('manifest_id')}`",
        "",
        f"> 🧪 **{SANDBOX_BANNER}**",
        "",
        f"**Plan:** `{result.get('plan_id')}`  ",
        f"**Manifest id:** `{result.get('manifest_id')}`  ",
        f"**Manifest hash:** `{result.get('manifest_hash')}`  ",
        f"**Simulation status:** `{status}`  ",
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

    counts = result.get("counts", {})
    lines += [
        f"## ✅ Eligible simulated (fake world) — {counts.get('changed', 0)} target(s)", "",
        "Changed target ids: " + (", ".join(f"`{t}`" for t in result.get("changed_targets", [])) or "—"),
        "",
        "### Before / after diff", "",
    ]
    lines += _diff_table(result.get("diff", []))
    lines += [
        "",
        f"## ⏸️ Excluded untouched — {counts.get('excluded', 0)} target(s)",
        "",
        "Excluded target ids: " + (", ".join(f"`{t}`" for t in result.get("excluded_target_ids", [])) or "—"),
        "",
        f"## ⛔ Blocked untouched — {counts.get('blocked', 0)} target(s)",
        "",
        "Blocked target ids: " + (", ".join(f"`{t}`" for t in result.get("blocked_target_ids", [])) or "—"),
        "",
        f"- excluded_blocked_untouched: `{result.get('excluded_blocked_untouched')}`",
        "",
        "## ↩️ Rollback", "",
        f"- rollback_restored (after → before exact): `{result.get('rollback_restored')}`",
        "",
        "## 📋 Boundary note", "",
    ]
    lines += _boundary_note()
    lines += ["", "---", f"_{result.get('reason')}_", ""]
    return "\n".join(lines)


def _adapter_section(result: Dict) -> List[str]:
    a = result.get("adapter") or {}
    caps = a.get("capabilities") or {}
    return [
        "## 🔌 Session Adapter Boundary", "",
        f"- **active adapter:** `{a.get('name', 'FakeSessionAdapter')}`",
        f"- adapter type: `{caps.get('adapter_type')}`",
        f"- real DAW support: `{caps.get('real_daw')}`",
        f"- project file writes: `{caps.get('writes_project_files')}`",
        f"- real apply support: `{caps.get('supports_real_apply')}`",
        f"- simulated apply support: `{caps.get('supports_simulated_apply')}`",
        f"- rollback support: `{caps.get('supports_rollback')}`",
        f"- requires macOS: `{caps.get('requires_macos')}`  ·  requires Logic: `{caps.get('requires_logic')}`",
        "",
        "_This interface is the seam a future `RealLogicSessionAdapter` must satisfy. "
        "This packet does not implement real Logic; the orchestration is now adapter-driven._",
        "",
    ]


def _boundary_note() -> List[str]:
    return [
        "- Fake **in-memory** session only.",
        "- No `.logicx` writes.",
        "- No real DAW.",
        "- No AppleScript.",
        "- No bridge execution.",
        "- No source mutation.",
    ]


def write_sandbox_packet(result: Dict, out_dir: str) -> Dict:
    """Write sandbox_simulation_report.json + .md; return their paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "sandbox_simulation_report.json"
    md_path = out / "sandbox_simulation_report.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_sandbox_markdown(result) + "\n", encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path)}
