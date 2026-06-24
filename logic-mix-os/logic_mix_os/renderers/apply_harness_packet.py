"""Apply-harness readiness renderer (Hardening Packet 8, Layer 2).

Renders the apply-readiness report + refusal receipt (from
:mod:`logic_mix_os.apply_harness`) into JSON + human-readable Markdown under an
``APPLY HARNESS STUB — VALIDATED AND REFUSED, NOTHING APPLIED`` banner.

Rendering only — it never executes Logic, mutates a session, touches audio, or
connects to a real macOS/Logic process.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

HARNESS_BANNER = "APPLY HARNESS STUB — VALIDATED AND REFUSED, NOTHING APPLIED"


def render_readiness_markdown(report: Dict, refusal: Optional[Dict] = None) -> str:
    refusal = refusal or {}
    ev = (f"`{refusal.get('ledger_event_id')}` (entry `{refusal.get('ledger_entry_hash')}`)"
          if refusal.get("ledger_event_id") else "_none (not persisted)_")
    errs = report.get("validation_errors", [])
    g = report.get("no_apply_guarantee") or {}

    lines: List[str] = [
        f"# Apply-Harness Readiness — `{report.get('manifest_id')}`",
        "",
        f"> ⛔ **{HARNESS_BANNER}**",
        "",
        f"**Plan:** `{report.get('plan_id')}`  ",
        f"**Manifest id:** `{report.get('manifest_id')}`  ",
        f"**Manifest hash:** `{report.get('manifest_hash')}`  ",
        f"**Eligibility:** {report.get('eligible_count', 0)} eligible · "
        f"{report.get('excluded_count', 0)} excluded · {report.get('blocked_count', 0)} blocked  ",
        f"**Validation:** {report.get('validation_status')}"
        + (f" ({len(errs)} error(s))" if errs else "") + "  ",
        f"**No-apply guarantee:** {report.get('no_apply_guarantee_status')}  ",
        f"**Ledger status:** {report.get('ledger_status')}  ",
        f"**Readiness:** `{report.get('readiness_status')}`  ",
        f"**Apply permitted here:** `{report.get('apply_permitted_here')}`",
        "",
        "## ⛔ Apply decision",
        "",
        f"- **ok:** `{refusal.get('ok')}`",
        f"- **applied:** `{refusal.get('applied')}`",
        f"- **executed:** `{refusal.get('executed')}`",
        f"- **authority boundary:** `{refusal.get('authority_boundary')}`",
        f"- **reason:** {refusal.get('reason', '—')}",
        f"- **audit event:** {ev}",
        "",
        "## 🚫 No-apply guarantee (from manifest)",
        "",
        f"- nothing_applied: `{g.get('nothing_applied')}`",
        f"- must_not_execute_here: `{g.get('must_not_execute_here')}`",
        f"- environment: `{g.get('environment')}`",
        f"- contains_apply_payload: `{g.get('contains_apply_payload')}`",
        f"- can_execute: `{g.get('can_execute')}`",
        "",
    ]
    if errs:
        lines += ["## ❗ Validation errors", ""] + [f"- {e}" for e in errs] + [""]
    lines += [
        "## 📋 Future apply boundary", "",
        "- This validates the manifest contract.",
        "- This does **not** touch Logic.",
        "- This is **not** a real apply path.",
        "- A future macOS/Logic test surface must consume this contract separately.",
        "",
        "---",
        f"_{refusal.get('reason', HARNESS_BANNER)}_",
        "",
    ]
    return "\n".join(lines)


def write_harness_packet(report: Dict, refusal: Dict, out_dir: str) -> Dict:
    """Write apply_readiness_report.json/.md + apply_refusal_receipt.json."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rj = out / "apply_readiness_report.json"
    rm = out / "apply_readiness_report.md"
    rr = out / "apply_refusal_receipt.json"
    rj.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    rm.write_text(render_readiness_markdown(report, refusal) + "\n", encoding="utf-8")
    rr.write_text(json.dumps(refusal, indent=2) + "\n", encoding="utf-8")
    return {"json_path": str(rj), "md_path": str(rm), "refusal_path": str(rr)}
