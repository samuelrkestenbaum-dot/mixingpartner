# P-019 — `record_mix_pass` closes the learning loop INSIDE the cowork surface

**Date:** 2026-07-01
**Status:** CLOSED — product change shipped (additive, opt-in, byte-identical by default); qa GREEN, reviewer pass.
**Type:** PRODUCT-code feature. **FIRST packet of the arc P-019→P-023** to the canonical target: Logic Mix OS as a tool Claude Cowork can drive END-TO-END in a Logic Pro mixing session (plan-only v1; the agent/human executes). Orchestrator-routed; in-authority (reuses the already-live `record_pass`/`_apply_history` channel — no new product decision).

---

## Title

Adds a `record_mix_pass` command to the cowork `COMMANDS` registry (count
**32 → 33**). Its handler records a pass OUTCOME on the LIVE history channel —
`ctx["memory"].record_pass(name, ctx["result"], reverted=...)` →
`mix_pass_history.json` — passing through the P-018 `reverted` ground-truth flag
(opt-in, default False), and returns the record JSON. So an agent driving through
the cowork surface can now RECORD an outcome and see `suggest_next_pass` change
WITHOUT leaving the surface: the read/write cowork surface is now **symmetric**
(the READ side was already live via P-009). Routes to the LIVE channel, NOT the
dead decision ledger.

## What it does (the mechanism)

- **`cowork.py::_record_mix_pass` (new handler, `cowork.py:97-106`)** — records a
  pass outcome on the LIVE history channel via the context's memory:
  `mem.record_pass(name, _r(ctx), reverted=reverted)` where `_r(ctx)` is the
  analysis result already on the cowork context. Passes through the P-018
  `reverted` ground-truth flag (opt-in, `reverted: bool = False`). Returns the
  record JSON. Mirrors the existing `_write_mix_decision` handler's shape and its
  clean `{"error": "no memory_dir configured"}` when no memory dir is configured
  (the loop requires a memory dir; error clearly, don't crash).
- **`cowork.py::COMMANDS` (registry)** — registers `record_mix_pass`
  (`cowork.py:155`, desc: "Record a pass outcome on the live history channel
  (params: name, reverted)"). Command count goes **32 → 33**.
- **Result:** an agent on the cowork surface can now close the loop entirely
  in-surface: `run_command("record_mix_pass", ctx, reverted=True)` → a fresh
  `build_context(memory_dir=...)` → `run_command("suggest_next_pass")` surfaces
  the confirmed "Revert last pass". Reuses P-008/P-009/P-018 as-is; nothing new on
  the memory or planner internals.

## The one surface finding, resolved minimally (recorded — NOT a wall)

The cowork `--params '{...}'` invocation path unpacks user JSON into
`run_command(name, ctx, **params)`, so a handler param named `name` (the pass
name for `record_mix_pass`) **collided** with the dispatcher's positional `name`.
Fixed by making the dispatcher's `name`/`ctx` **positional-only**:
`def run_command(name: str, ctx: Dict, /, **params)` (`cowork.py:165`).
**Behavior-preserving:** a repo-wide grep found ZERO callers passing
`name=`/`ctx=` by keyword — the sole product caller (`cli.py:237`) passes
positionally. This is a param-naming detail, NOT a missing wire or an
architectural wall.

## Scope

**In:**
- `logic_mix_os/cowork.py` (additive): the `_record_mix_pass` handler, its
  `COMMANDS` registry row, and the positional-only `/` on `run_command`.
- `tests/test_cowork.py`: registry-count assertion updated **32 → 33** (an
  intended, not silent, change).
- New `tests/test_cowork_record.py`: unit + no-re-run liveness guard.

**Explicitly out (verified UNTOUCHED):**
- `memory.py::record_pass` / `planners/next_pass_planner.py::_apply_history`
  internals (reused as-is — the P-008/P-009/P-018 channel).
- `cli.py`'s `_run_cowork` plumbing beyond what registering a command requires;
  the standalone `memory-record` verb (stays as-is too).
- The dead ledger (`write_mix_decision` / `decision_ledger.json` — the loop is
  NOT routed through it).
- `_KIND_SCORES` / creative / governance; `pipeline.analyze()`'s memory wiring.
- The dry-run bridge / real-Logic execution (env-bound, OUT of v1).
- Any push / merge / deploy.

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-019:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion" — the default-branch tip (P-016 MERGED via PR #15).
  Confirmed `6c40e2b` IS an ancestor of HEAD. (`242a4f0` was the P-019
  active-packet confirmation; `e63aa77` was the P-018 close.)
- **`b7572b7`** — Commit-1 (test-first, green in isolation): `_record_mix_pass`
  handler + `COMMANDS` registry row + positional-only `run_command` +
  unit tests. `cowork.py` (+19/−?), `tests/test_cowork.py` (registry count
  32→33), `tests/test_cowork_record.py` (NEW, +116). **Green in isolation = 257
  passed.**
- **`de5679f`** — Commit-2 (same packet): the no-re-run liveness guard.
  `tests/test_cowork_record.py` (+85).

Two commits (within ≤2). No product-code change outside `cowork.py`.

## QA proof (exact)

- **Suite: 253 → 259 passed** (+6; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 in isolation: 257 passed.**
- **Regression: 68/68, 0 critical, 0 warnings** held (opt-in memory path → goldens
  untouched; byte-identical default).
- **LIVENESS proven load-bearing (the P-016/P-018 lesson honored):**
  `test_loop_closes_through_cowork_no_rerun` records a confirmed revert via
  `run_command("record_mix_pass", ...)` on a score-IMPROVED override case, then a
  FRESH `build_context(memory_dir=...)` → `run_command("suggest_next_pass")`
  surfaces the confirmed "Revert last pass" — **NO hand re-run**. Both qa and
  reviewer INDEPENDENTLY broke the wiring (handler off the live channel) → the
  test FAILS; restored → PASSES. The loop closes THROUGH the cowork surface, not
  just in unit-land.
- **Routes to the LIVE channel (runtime probe):** only `mix_pass_history.json` is
  created, NEVER `decision_ledger.json`.
- **Byte-identical default:** date-neutralised canonical JSON equal to the
  standalone `memory-record`; default `reverted=False` omits the flag.
- **Registry: 33, no stale 32.** Scope: only 3 files (`cowork.py` additive,
  `test_cowork.py` count assertion 32→33, new `tests/test_cowork_record.py`).
  `memory.py` / `cli.py` / `pipeline.py` / ledger / creative / governance
  UNTOUCHED. P-008 / P-009 / P-018 / existing-cowork tests green.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN** — independently mutation-verified liveness + non-tautological
  override case + live-channel routing probe.

## Reviewer verdict

**Pass.** Handler correct + routes to the live channel (verified by breaking it);
positional-only `/` is safe and minimal (zero keyword callers — behavior-preserving);
the loop closes through cowork (mutation-verified); the override case is
non-tautological (score-IMPROVED, so the confirmed revert cannot be an echo of the
score signal).

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Residue

- **The arc is the active roadmap (P-020→P-023):**
  - **P-020** — session-flow discoverability: phase-grouped commands so an agent
    can find its way across the 33-command surface (intake → classify → diagnose →
    plan → checklist → validate → record → next-pass).
  - **P-021** — a verified end-to-end agent walkthrough (tests-only): drive a full
    Logic-Pro-mixing session through the cowork surface start-to-finish.
  - **P-022** — optional session-efficiency / override-propagation.
  - **P-023** — the **USER-GATED** decision: MCP server vs a documented raw-CLI
    contract as the agent transport. **Do NOT open blind; sequenced LAST.**
- **Outcome-enum generalization (carried from P-018, reviewer trajectory note)** —
  widen `reverted: bool` to a small outcome enum (`reverted`/`kept`/`refined`).
  Reachable (widens without breaking the byte-identical default), NOT staged,
  user-gated for the semantics.
- **Symmetric `subtractive_drop` re-judgment (carried)** — is `subtractive_drop`
  itself slightly over-valued? User-gated, un-signed-off, NOT staged.
- **Wider `--memory-dir` CLI surface (carried from P-009)** — small in-authority
  move, partly a product question.
- **Standing routing guard (P-018, reaffirmed by P-019):** outcome/event PRODUCERS
  go on a LIVE channel (history `mix_pass_history.json` → `_apply_history`, or
  taste `taste_profile.json` → governance), NEVER the display-only decision ledger
  (`add_decision` → `decision_ledger.json` has ZERO analyze-path consumers).

## Open boundaries (awaiting explicit go)

- **P-019 is local-only at this close** — commits `b7572b7`, `de5679f` on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b`
  (PR #15) merge base. **Not pushed / merged.** Any push of these commits — and any
  subsequent PR / merge into the protected default — needs the user's explicit go.
  **No push / merge / deploy / secret action taken in this close.** (The
  build-os-only close commit is separate from the two product commits above.)

---
_Archivist close, 2026-07-01. FIRST packet of the arc (P-019→P-023) to a Cowork-usable end-to-end state; the learning loop is now closeable inside the cowork surface (read/write symmetric); positional-only surface finding resolved minimally; liveness proven load-bearing; byte-identical default. Single-reviewer verdict (Codex unavailable)._
