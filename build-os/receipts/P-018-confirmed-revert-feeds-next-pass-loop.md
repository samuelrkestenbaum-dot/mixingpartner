# P-018 — Confirmed-revert outcome feeds the live next-pass loop (the FIRST confirmed-outcome signal in the learning loop)

**Date:** 2026-07-01
**Status:** CLOSED — product change shipped (additive, opt-in, byte-identical by default); qa GREEN, reviewer pass.
**Type:** PRODUCT-code feature. A PIVOT off the (complete) judgment-tuning path onto the learning-loop / feedback frontier (user said "Yes"). Orchestrator-routed; override semantics chosen by the orchestrator-in-chief (user may redirect at the merge gate).

---

## Title

An opt-in `memory-record --reverted` records a CONFIRMED operator revert on a
pass; the live `_apply_history` consumer then, on a confirmed revert, DEMOTES the
recommended-then-reverted moves and surfaces exactly ONE confirmed
"Revert last pass" item at priority 95 — **regardless of the score-delta
`got_worse` inference (OVERRIDE)** — measurably changing real
`analyze(--memory-dir)` `next_pass` output. The FIRST confirmed-outcome signal in
the learning loop (all prior loop signals were score-INFERRED).

## What it does (the mechanism)

- **`memory.py::record_pass`** — adds an opt-in `reverted: bool = False` field
  recorded on the pass in `mix_pass_history.json`. Default `False` → the `reverted`
  key is NOT written and the stored history is byte-identical to today when the
  flag is unused (opt-in discipline).
- **`planners/next_pass_planner.py::_apply_history`** — consumes the confirmed
  `reverted` flag with **OVERRIDE** semantics: when the most-recent pass carries
  `reverted=True`, it treats the revert as GROUND TRUTH — demotes exactly that
  pass's recommended moves and surfaces exactly ONE confirmed "Revert last pass"
  item at **priority 95**, **regardless of the score-delta `got_worse`
  inference**, with an **early return** that prevents double-up with the
  score-inferred revert candidate. The surfaced item carries a DISTINCT, honest
  evidence line — "surfaced because the operator confirmed reverting the last
  pass" (contains "confirm") — as opposed to the score-inferred wording
  ("recorded revert candidate(s): …"). When `reverted` is absent/False, behavior
  is UNCHANGED (the existing score-inferred path).
- **`cli.py`** — wires an opt-in `--reverted` flag on the `memory-record` command
  that sets `record_pass(..., reverted=True)`. No other CLI surface change.

## Override semantics + rationale (chosen by the orchestrator-in-chief)

**OVERRIDE (Option A), not additive.** A confirmed operator revert is GROUND TRUTH
and takes precedence over the score-inferred guess when they disagree — the
doctrine-honest, operator-serving Halee/Ramone choice: if the engineer says they
reverted, the system defers to that, it does not argue with the metrics. Additive
was the alternative; override is the evidence-weighted choice (a confirmed action
outranks a heuristic proxy). **The user may redirect this at the merge gate.**

## Why THIS seam — the dead-ledger finding (recorded so no future session routes an inert producer)

The decision **LEDGER** (`add_decision` → `decision_ledger.json`) has **ZERO
decision-making consumers**: `mem.ledger()` is called only at `cli.py:315`
(display-only). So a producer for ANY reserved ledger event
(`manual_note` / `taste_feedback` / `mix_decision` / `validation_check`) would be
**INERT** — a dead event nobody reads on the `analyze()` path (the hollow-packet /
P-016-inertness trap). The ONLY reachable LIVE seam was the history axis
(`record_pass` → `mix_pass_history.json` → P-009 threads `history()` →
`plan_next_pass` → `_apply_history`, which already runs live through
`analyze(--memory-dir)`), which is why the confirmed revert lands there.

## Scope

**In:**
- `memory.py::record_pass` opt-in `reverted: bool = False` field.
- `planners/next_pass_planner.py::_apply_history` confirmed-revert OVERRIDE
  consumer (demote reverted move + one priority-95 confirmed "Revert last pass"
  item, distinct evidence line, early-return anti-double-up).
- `cli.py` opt-in `--reverted` flag on `memory-record`.
- Unit + no-re-run liveness/CLI tests (test-first).

**Explicitly out (verified UNTOUCHED):**
- The ledger / `add_decision` / any reserved ledger event.
- The taste axis.
- `_KIND_SCORES` / creative scoring / governance.
- `pipeline.analyze()`'s existing memory wiring beyond what `_apply_history`
  already reads.
- Any push / merge / deploy.

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-018:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion (first reward nudge, live-wired)" — the default-branch
  tip (P-016 MERGED via PR #15). Confirmed `6c40e2b` IS an ancestor of HEAD.
  (`fe832d9` was the P-018 active-packet confirmation; `cfbb4b8` was the P-017
  close.)
- **`736fa8b`** — Commit-1 (test-first, green in isolation): `record_pass`
  `reverted` field + `_apply_history` OVERRIDE consumer + 9 unit tests.
  `memory.py` (+9/−?), `planners/next_pass_planner.py` (+65 region),
  `tests/test_confirmed_revert.py` (NEW, +244). **Green in isolation = 249 passed.**
- **`6134d27`** — Commit-2 (same packet): the `--reverted` CLI wire + 4 no-re-run
  liveness/CLI tests. `cli.py` (+7/−1), `tests/test_confirmed_revert_live.py`
  (NEW, +168).

Two commits (within ≤2). No product-code change outside the three named files.

## QA proof (exact)

- **Suite: 240 → 253 passed** (+13; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 in isolation: 249 passed.**
- **Regression: 68/68, 0 critical, 0 warnings** held (regression calls `analyze()`
  with no `memory_dir` → falsy no-op → goldens untouched).
- **LIVENESS proven load-bearing (the P-016 lesson honored):** the no-re-run
  liveness test asserts on real `analyze(memory_dir=...)` `next_pass` and **FAILS**
  with the pre-P-018 `_apply_history` (a confirmed revert doesn't reach analyze
  output = would be inert) and **PASSES** at tip. The confirmed revert genuinely
  changes real `analyze(--memory-dir)` output — NOT inert.
- **OVERRIDE non-vacuous:** with an IMPROVED score delta (`got_worse` empty) but
  `reverted=True`, the confirmed "Revert last pass" still surfaces at rank 0 and
  the reverted move is demoted — proving override, not an echo of the score signal.
- **Byte-identical default:** no `--reverted` → `next_pass` identical to today; the
  stored history has no `reverted` key when unused.
- **Scope clean:** ledger / `add_decision` / reserved ledger events, taste axis,
  `_KIND_SCORES` / creative / governance all UNTOUCHED. P-008
  `tests/test_next_pass_history.py` + P-009 `tests/test_live_wire.py` unedited and
  green (17 passed).
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN** — independently mutation-verified liveness + non-vacuous
  override.

### qa harness note (a qa-harness quirk, NOT a product defect)

qa self-flagged a transient stale-state artifact in one of its OWN scratch scripts
(it showed 0 items once) and confirmed the isolated / traced re-runs are
authoritative and consistent. This is a qa-harness quirk, not a product defect.

## Reviewer verdict

**Pass.** The override is bounded and deterministic; the early return skips only
the score-inferred revert (no double-up); it demotes exactly the reverted pass's
recommended moves (no over-reach); and it is mutation-verified load-bearing.

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Reviewer trajectory note (non-blocking — recorded as a candidate, NOT staged)

Capturing only `revert` leaves the outcome vocabulary lopsided. A future
generalization to a small outcome enum (`reverted` / `kept` / `refined`) would
round out the outcome→learning loop — and the `reverted: bool` field can widen to
that later **WITHOUT breaking the byte-identical default**. Record as a candidate,
not staged (the semantics are user-gated).

## Residue

- **Outcome-enum generalization (the reviewer's trajectory note)** — widen
  `reverted: bool` to a small outcome enum (`reverted` / `kept` / `refined`).
  Reachable (widens without breaking the byte-identical default), NOT staged,
  user-gated for the semantics.
- **The ledger-is-dead finding** — the decision LEDGER (`add_decision` /
  `decision_ledger`) has NO analyze-path consumer (display-only, `cli.py:315`). A
  future confirmed-outcome producer is only real if it lands on a LIVE channel
  (history `mix_pass_history.json` → `_apply_history`, or taste `taste_profile.json`
  → governance), NOT the ledger. `validation_check` / `manual_note` producers now
  need a NEW consumer — not just a ledger write.
- Carried unchanged: wider `--memory-dir` CLI surface (from P-009, partly a product
  question); the symmetric `subtractive_drop` re-judgment (user-gated,
  un-signed-off, NOT staged).

## Open boundaries (awaiting explicit go)

- **P-018 is local-only at this close** — commits `736fa8b`, `6134d27` on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b`
  (PR #15) merge base. **Not pushed / merged.** Any push of these commits — and any
  subsequent PR / merge into the protected default — needs the user's explicit go.
  The override semantics are the merge-gate redirect point. **No push / merge /
  deploy / secret action taken in this close.**

---
_Archivist close, 2026-07-01. First confirmed-outcome signal in the learning loop; OVERRIDE semantics, liveness proven load-bearing, non-vacuous override, byte-identical default. Single-reviewer verdict (Codex unavailable)._
