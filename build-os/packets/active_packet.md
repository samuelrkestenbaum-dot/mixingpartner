# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-018
- **Title:** Confirmed-revert outcome feeds the live next-pass loop (first CONFIRMED-outcome signal)

## Authority

**Build / feature — in authority.** A PIVOT off the (complete) judgment-tuning
path onto the learning-loop frontier (user said "Yes" to making the
outcome→learning feedback loop real). Additive, **opt-in, byte-identical by
default.** The variant/golden path won't catch it (this is the memory/next-pass
axis) → **unit + liveness tests are the binding guard.** **Merge to default stays
gated on the user's explicit go; dev-branch commits are covered by standing
push-go.**

## Semantics decision (made by the orchestrator-in-chief; user may redirect at the merge gate)

Today the loop only ever **infers** "that regressed, maybe revert" from score
deltas inside `record_pass`. It never captures a **confirmed** operator outcome.
This packet adds one. **Chosen semantics: OVERRIDE (Option A).** A confirmed
operator revert is GROUND TRUTH and takes precedence over the score-inferred
guess when they disagree — this is a Halee/Ramone operator-serving judgment layer;
if the engineer says they reverted, the system defers to that, it does not argue
with the metrics. (Additive was the alternative; override is the doctrine-honest,
evidence-weighted choice: a confirmed action outranks a heuristic proxy.)

## Why this seam (not the others)

The decision **ledger** (`add_decision` → `decision_ledger.json`) has **ZERO
decision-making consumers** — `mem.ledger()` is called only at `cli.py:315`
(display). So a producer for any reserved ledger event (`manual_note`,
`taste_feedback`, `mix_decision`, `validation_check`) would be **inert** — a dead
event nobody reads on the `analyze()` path (the hollow-packet / P-016-inertness
trap). The ONLY reachable LIVE seam is the history axis: `record_pass` →
`mix_pass_history.json` → P-009 threads `history()` → `plan_next_pass` →
`_apply_history` (`next_pass_planner.py:131`), which already runs live through
`analyze(--memory-dir)` and surfaces demotion / `"Revert last pass"`. A confirmed
revert lands on that EXISTING, PROVEN-LIVE consumer.

## Scope (the builder implements EXACTLY this)

### Product change (additive, opt-in)
1. **`memory.py::record_pass`** — add an opt-in `reverted: bool = False` field
   recorded on the pass in `mix_pass_history.json`. Default `False` → the stored
   history is byte-identical to today when the flag is not used.
2. **`planners/next_pass_planner.py::_apply_history`** — consume the confirmed
   `reverted` flag with OVERRIDE semantics: when the most-recent pass carries
   `reverted=True`, treat it as a **confirmed** regression — demote the reverted
   move / surface the revert-awareness in `next_pass` **regardless of the
   score-delta `got_worse` inference**, and make the surfaced item honestly
   reflect that it is operator-CONFIRMED (e.g. wording/evidence distinct from the
   score-inferred case). When `reverted` is absent/False, behavior is UNCHANGED
   (the existing score-inferred path). Keep it pure/deterministic; bounded;
   evidence-tagged (the next-pass item should carry that it came from a confirmed
   revert, not a score guess).
3. **`cli.py`** — wire an opt-in `--reverted` flag on the `memory-record` command
   that sets `record_pass(..., reverted=True)`. No other CLI surface changes.

Do NOT touch: the ledger / `add_decision` / any reserved ledger event; the taste
axis; `_KIND_SCORES` / creative scoring / governance; `pipeline.analyze()`'s
existing memory wiring beyond what `_apply_history` already reads; any push/merge.

### Liveness (the P-016 lesson — MANDATORY)
A confirmed revert MUST measurably change a real `analyze(--memory-dir)` run's
`next_pass` output — NOT be an inert stored field. Prove it with a **no-re-run**
liveness test: seed a memory dir with a pass recorded `reverted=True`, run the
REAL `analyze(memory_dir=...)`, and assert the produced `next_pass` reflects the
confirmed revert (demotion / confirmed-revert item) — WITHOUT re-running the
planner by hand. The test must FAIL before the `_apply_history` consumer change
and PASS after (load-bearing, like P-016's liveness tests).

### Tests — the binding guard. Test-first.
- **Unit:** `record_pass` stores `reverted`; `_apply_history` override behavior
  (confirmed revert surfaces/demotes even when the score delta says "improved" —
  the override case, which is what makes it non-tautological); default/no-flag
  path unchanged.
- **Liveness (no re-run):** as above, through real `analyze(memory_dir=...)`.
- **Byte-identical default:** a run with NO `reverted` flag / no `--reverted`
  produces the same `next_pass` as today (opt-in discipline).
- Existing P-008 `tests/test_next_pass_history.py` and P-009
  `tests/test_live_wire.py` pass UNCHANGED (do not edit them; if the new field
  changes a shared fixture, adapt the NEW tests, not the old assertions — flag if
  a real conflict arises).

Fake adapters only — no real DAW / Logic / AppleScript / subprocess / `.logicx`
write / network. Memory is local JSON only.

## Constraints

- **≤2 commits.** Commit-1 (test-first, green in isolation): `record_pass` field
  + `_apply_history` override consumer + failing-then-passing unit tests.
  Commit-2 (same packet): the `--reverted` CLI wire + the no-re-run liveness test
  (fails pre-wire, passes after — the anti-inertness guard).
- **No external mutation** — no push / merge / deploy / secret. (Standing push-go
  covers dev-branch commits only.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **240 → 240+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held (regression calls `analyze()`
  with no `memory_dir` → falsy no-op → goldens untouched — confirm).
- **Byte-identical default:** no `--reverted` → `next_pass` unchanged vs today.
- **Liveness proven load-bearing:** the no-re-run test FAILS before the
  `_apply_history` change and PASSES after; a confirmed revert genuinely changes
  real `analyze(--memory-dir)` output (NOT inert).
- **Override non-vacuous:** a test where the score delta says "improved" but
  `reverted=True` → the confirmed revert still surfaces (proves override, not just
  additive echo of the score signal).
- Commit-1 green in isolation; safety grep clean; P-008/P-009 tests green.

---
_Confirmed as active by the orchestrator-in-chief (P-018), on the user's "Yes"
+ the build-orchestrator's routing; override semantics chosen (user may redirect
at the merge gate). One packet at a time._
