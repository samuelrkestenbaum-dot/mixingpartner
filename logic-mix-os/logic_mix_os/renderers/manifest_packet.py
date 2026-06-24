"""Pre-apply change manifest renderer (Hardening Packet 7, Layer 2).

Renders a change manifest (from :func:`logic_mix_os.apply_manifest.build_change_manifest`)
into JSON + human-readable Markdown under an
``APPROVED CHANGE MANIFEST — SPEC ONLY, NOTHING WILL BE APPLIED`` banner.

Rendering only — it never executes Logic, mutates a session, or touches audio.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from ..apply_manifest import MANIFEST_BANNER


def _eligible_table(rows: List[Dict]) -> List[str]:
    out = ["| Step | Planned Logic action | Class | Receipt | Decision | Approver | Rollback |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    for s in rows:
        out.append(f"| `{s['step_id']}` | {s['planned_logic_action']} | C{s['authority_class']} | "
                   f"`{s['receipt_id']}` | `{s['decision_id']}` | {s.get('approver')} | "
                   f"{s.get('rollback_plan') or '—'} |")
    return out


def render_manifest_markdown(manifest: Dict) -> str:
    summ = manifest.get("summary", {})
    ledv = manifest.get("ledger_verification") or {}
    led_line = (f"`{manifest['ledger_path']}` (status: **{manifest['ledger_status']}**"
                + (f", integrity: {'ok' if ledv.get('ok') else 'broken'}, {ledv.get('entries', 0)} entries"
                   if ledv else "") + ")") if manifest.get("ledger_path") else \
               f"_status: **{manifest['ledger_status']}**_"
    emitted = (f"`{manifest['manifest_emitted_event_id']}` (entry `{manifest['manifest_emitted_entry_hash']}`)"
               if manifest.get("manifest_emitted_event_id") else "_none (not persisted)_")
    g = manifest.get("no_apply_guarantee", {})

    lines: List[str] = [
        f"# Approved Change Manifest — `{manifest.get('manifest_id')}`",
        "",
        f"> 🔒 **{MANIFEST_BANNER}**",
        "",
        f"**Plan:** `{manifest.get('plan_id')}` "
        f"(source: {manifest.get('source_type')} `{manifest.get('source_id')}`)  ",
        f"**Manifest id:** `{manifest.get('manifest_id')}`  ",
        f"**Manifest hash:** `{manifest.get('manifest_hash')}`  ",
        f"**Created:** {manifest.get('created')}  ",
        f"**Summary:** {summ.get('total_steps', 0)} steps — "
        f"{summ.get('eligible', 0)} eligible · {summ.get('excluded', 0)} excluded · "
        f"{summ.get('blocked', 0)} blocked  ",
        f"**Audit ledger:** {led_line}  ",
        f"**manifest_emitted event:** {emitted}",
        "",
        "## ✅ Eligible for future apply (approved — NOT applied here)",
        "",
    ]
    lines += _eligible_table(manifest.get("eligible_for_future_apply", [])) \
        if manifest.get("eligible_for_future_apply") else ["_None._"]
    lines.append("")

    lines += ["## ⏸️ Excluded (rejected / revision-requested / deferred / pending)", ""]
    excluded = manifest.get("excluded", [])
    lines += ([f"- `{s['step_id']}` — **{s['status']}** — {s['planned_logic_action']}"
               + (f" — reason: {s['reason']}" if s.get("reason") else "") for s in excluded]
              or ["_None._"])
    lines.append("")

    lines += ["## ⛔ Blocked (Class 5 — forbidden, never eligible)", ""]
    blocked = manifest.get("blocked", [])
    lines += ([f"- `{s['step_id']}` — {s['planned_logic_action']} — {s.get('reason', '')}"
               for s in blocked] or ["_None._"])
    lines.append("")

    lines += [
        "## 🚫 No-apply guarantee", "",
        f"- nothing_applied: `{g.get('nothing_applied')}`",
        f"- must_not_execute_here: `{g.get('must_not_execute_here')}`",
        f"- environment: `{g.get('environment')}`",
        f"- contains_apply_payload: `{g.get('contains_apply_payload')}`",
        f"- can_execute: `{g.get('can_execute')}`",
        "",
        "## 📋 Future apply contract", "",
        "- This is the input a future apply harness would consume.",
        "- It does **not** itself authorize execution.",
        "- It **cannot** be applied in this environment.",
        "",
        "---",
        f"_{manifest.get('future_apply_contract')}_",
        "",
    ]
    return "\n".join(lines)


def write_manifest_packet(manifest: Dict, out_dir: str) -> Dict:
    """Write change_manifest.json + change_manifest.md; return their paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "change_manifest.json"
    md_path = out / "change_manifest.md"
    json_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_manifest_markdown(manifest) + "\n", encoding="utf-8")
    return {"json_path": str(json_path), "md_path": str(md_path)}
