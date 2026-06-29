# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** Logic Mix OS — a local-first, deterministic mix-decision
  system that turns exported Logic Pro stems + a `project_manifest.json` into a
  section-aware, Logic-native **mix plan** (Roy Halee / Phil Ramone judgment
  layer). Not an auto-mixer, preset generator, or mastering tool. All product
  code lives under `logic-mix-os/`.
- **Primary branch / base:** default branch `claude/dreamy-turing-z0oxll` @
  `694d19d`; active dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **110 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 warnings).

## Where we are

- **Last closed packet:** **P-005** — Extend the readiness-vs-refusal treatment
  to `creative_renderer.py::render_governance`. The `## Stop Conditions` section
  now renders P-003's labelled `READY TO STOP` / `NOT YET — keep iterating`
  block in **markdown** (full `reasons` list, warning-when-ready), replacing the
  flat boolean dump at `creative_renderer.py:104`. Single product commit
  `107b6e5` (renderer +19/-5, `tests/test_creative.py` +58; 2 new tests).
  Suite 108→110. Render-only; no backend reach-in; markdown-clean (no HTML).
  **Milestone:** the readiness-vs-refusal treatment is now CONSISTENT across all
  THREE governance surfaces — `operator_view.py` (text, P-003),
  `html_dashboard.py` (HTML, P-003), and `creative_renderer.py` (markdown,
  P-005). The P-003 surface-consistency thread is fully closed. Reviewer: pass
  (single-eyes). Receipt:
  `build-os/receipts/P-005-creative-renderer-readiness.md`.
- **Now:** **none active.** No product packet in flight.
- **Next (user has directed working through the next bunch):**
  **P-006 — `creative.py` literal cleanup** (`chorus_lift_B` ~line 194, loop
  branch ~line 217), then the **deferred net-new event-logging packets**
  (`taste_feedback` / `validation_check` / `revert` / `manual_note` — each
  net-new, no producer wired today).

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-005 close (2026-06-29)._
