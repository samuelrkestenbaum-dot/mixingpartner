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
- **Green baseline (verified 2026-06-29):** suite **102 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 warnings).

## Where we are

- **Last closed packet:** **P-002** — Net-new `EVENT_TYPES` decision-ledger
  vocabulary + optional validated `event_type` on `add_decision`. New vocabulary
  in `constants.py`; optional validated `event_type` on `memory.py::add_decision`;
  `record_plan_decisions` tags `mute_candidate`; new test in
  `tests/test_session_memory.py`. Reviewer: pass. Receipt:
  `build-os/receipts/P-002-event-types-vocabulary.md`.
- **Now:** **none active.** No product packet in flight.
- **Next:** user's call — **P-003** (readiness-vs-refusal UI clarity), the
  **`creative.py` literal cleanup**, or the **new event-tagging follow-up** (tag
  `cowork.py::_write_mix_decision` → `mix_decision`, wire `taste_feedback` /
  `validation_check`).

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
_Updated by the archivist on close. Last advanced on P-002 close (2026-06-29)._
