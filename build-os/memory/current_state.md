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
- **Green baseline (verified 2026-06-29):** suite **138 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **Last closed packet:** **P-008** — History-aware next pass (the OUTCOME side
  of the learning loop). `plan_next_pass` now consumes recorded mix-pass history
  — **opt-in, bounded, evidence-tagged**. An optional trailing `history` arg
  (default `None` → byte-identical); a `_MOVE_TARGET` map (move title →
  `SCORE_KEYS` member) bridges history's score-keyed `got_worse` to the planner's
  titled candidates; a move whose target regressed AND was recommended last pass
  is **demoted** (`HISTORY_DEMOTE = 40`, floored ≥ 0, survives — not deleted); a
  single non-destructive `"Revert last pass"` move surfaces at priority 95 when
  `revert_candidates` is non-empty; each history-touched candidate carries an
  `evidence` line (absent otherwise). Uses only `history[-1]`. Deterministic.
  Commit-1 `d98a194` (planner +88/−1 + new `tests/test_next_pass_history.py`,
  12 tests), Commit-2 `dbf94c3` (folded `drum_room_bloom` narrower-taste test in
  `test_governance_taste.py`). Suite 125→**138**; regression 68/68 held; **default
  path BYTE-IDENTICAL three ways** (arg-omitted == `history=None` == `history=[]`,
  no `evidence` key); Commit-1 green in isolation. Reviewer: **pass** (revert at
  95>90 ruled acceptable — bounded, non-destructive, cannot manufacture a move;
  Codex not available). Receipt:
  `build-os/receipts/P-008-history-aware-next-pass.md`.
  - **MILESTONE — THE LEARNING LOOP IS NOW FULLY CLOSED:** with **P-007** (taste →
    governance, the *consumer* side) AND **P-008** (outcome → next-pass, the
    *outcome* side), **BOTH halves of the learning loop are closed.** The system
    both **personalizes to recorded taste** (governance biased by recorded
    operator taste — opt-in, bounded `±15`, doctrine-inviolable) and **stops
    re-recommending moves that regressed** (next-pass demotes recorded `got_worse`
    moves and surfaces revert — opt-in, bounded, non-destructive). Memory is no
    longer write-only on either axis: real consumers of recorded signals exist on
    both the taste and outcome axes. What remains to make the loop **real in
    production** is the live wiring (P-008b / P-007b), not new core behavior.
- **Now:** **none active.** No product packet in flight.
- **Next:** the trajectory follow-ons that make the now-closed loop **real in
  production** — **user's call** which to open:
  - **P-008b — Live history wire:** thread `memory.history()` into
    `pipeline.analyze()` / the planner call so a real recorded history reaches
    `plan_next_pass` in production (kept opt-in/explicit so byte-identical-by-
    default survives — symmetric to P-007b).
  - **P-007b — Live taste surface:** wire a real per-operator `taste_profile`
    from `memory_dir` into a pipeline/cowork run (explicit per-operator).
  - Also available (still behind the product decision, now with two consumers
    existing): the net-new **event-logging** producers (`taste_feedback` /
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
_Updated by the archivist on close. Last advanced on P-008 close (2026-06-29)._
