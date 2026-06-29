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
- **Green baseline (verified 2026-06-29):** suite **112 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 warnings).

## Where we are

- **Last closed packet:** **P-006** — `creative.py` literal cleanup. Two
  pre-existing un-resolved literals in `generate_variants` are now record-backed:
  Site 1 (`creative.py:194`, `chorus_lift_B`) `loops or supporting[-1:]` →
  `_resolve(loops, supporting[-1:], [r["name"] for r in records][:1])` (closes the
  empty-`tracks_affected` path, restores P-001's non-empty + real-record-subset
  invariant, reuses the `_resolve` seam); Site 2 (`creative.py:217`, `loop`
  branch) replaces the `"the loop"` literal with a real-record-name fallback so
  loop prose names an actual track whenever records exist. Single product commit
  `6e98a3b` (`creative.py` +4/-2, `tests/test_creative_attribution.py` +62; 2 new
  tests). Suite 110→112. Pure list logic; no renderer/backend reach-in; helper
  reuse only (no signature change). **Milestone:** every `tracks_affected` site in
  `generate_variants` is now record-backed and non-empty, and loop-branch prose
  can no longer name a non-existent track (except under a degenerate record-free
  input — tracked as a low-priority Known-risk note). Reviewer: pass
  (single-eyes; Codex not available). Receipt:
  `build-os/receipts/P-006-creative-literal-cleanup.md`.
- **Now:** **none active.** No product packet in flight.
- **Next:** the **net-new event-logging packets** (`taste_feedback` /
  `validation_check` / `revert` / `manual_note` — each net-new, no producer wired
  today). These are **blocked on a PRODUCT DECISION from the user**: should
  validation / taste / revert / note signals actually be written to the decision
  ledger? They are net-new features, not mechanical follow-ups — the user is being
  asked this next.

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
_Updated by the archivist on close. Last advanced on P-006 close (2026-06-29)._
