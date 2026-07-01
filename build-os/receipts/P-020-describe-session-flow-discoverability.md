# P-020 — `describe_session` session-flow discoverability

**Date:** 2026-07-01
**Status:** CLOSED — product change shipped (additive, read-only, byte-identical to every existing command); qa GREEN, reviewer pass.
**Type:** PRODUCT-code feature. **SECOND packet of the arc P-019→P-023** to the canonical target: Logic Mix OS as a tool Claude Cowork can drive END-TO-END in a Logic Pro mixing session (plan-only v1; the agent/human executes). Orchestrator-routed; in-authority, additive, no new product decision.

---

## Title

Adds a pure `_SESSION_FLOW` structure + a read-only `describe_session` command to
the cowork `COMMANDS` registry (count **33 → 34**). `list_commands` is a flat,
alphabetized catalog; an agent cannot read the canonical end-to-end mixing-session
SEQUENCE from it. `describe_session` returns the SAME registry as an ORDERED,
phase-grouped session flow — `{"phases": [...ordered...], "auxiliary": [...]}` —
so an agent can navigate: **intake → classify → diagnose → plan → checklist →
validate → record-outcome → next-pass**. Changes no existing command's behavior
or output; `list_commands` stays the flat catalog.

## What it does (the mechanism)

- **`cowork.py::_SESSION_FLOW` (new, pure data)** — an ORDERED list of the 8
  canonical session phases, each `{phase, purpose, commands: [...]}`, mapping the
  REAL `COMMANDS` keys into the canonical session order. Phase order is grounded in
  the README pipeline (source → identity → metrics → role → sections → depth →
  masking → doctrine → plan → checklist → next-pass) plus the P-018/P-019
  record/validate steps. **31 of the 34 commands** map onto the 8 linear phases.
- **The `auxiliary` bucket (honesty clause honored)** — **3 commands** are
  honestly OFF the linear session axis and go in an explicit `auxiliary` bucket
  rather than being forced into a phase they don't belong to:
  `run_creative_engine` (parallel creative exploration), `build_missing_tool`
  (meta tooling-gap helper), and `describe_session` itself (self-describing). No
  fabricated flow: `suggest_next_pass` is placed ONCE (in `next-pass`), not
  double-listed.
- **`cowork.py::_describe_session` (new handler)** — returns
  `{"phases": [...], "auxiliary": [...]}`, pure/deterministic/JSON, DEEP-COPIED so
  a caller cannot mutate the module-level `_SESSION_FLOW`.
- **`cowork.py::COMMANDS` (registry)** — registers `describe_session`. Command
  count goes **33 → 34**.
- **Result:** an agent can now discover the correct end-to-end order and phase
  grouping directly from the surface — the discoverability step the P-021
  end-to-end walkthrough sits on.

## The completeness INVARIANT (the load-bearing guard)

The binding guard is an **exact-cover invariant**: every key in `COMMANDS` appears
**EXACTLY ONCE** across all phases + the `auxiliary` bucket — no command orphaned
from the flow, none double-listed. This keeps the flow view honest and complete AS
COMMANDS ARE ADDED: a new command with no phase, or a duplicate, fails the test.
**Proven load-bearing** (orphan → test fails; duplicate → test fails), and
independently verified by qa: **31 (phases) + 3 (auxiliary) = 34 = len(COMMANDS)**.

## Scope

**In:**
- `logic_mix_os/cowork.py` (purely additive): the `_SESSION_FLOW` data structure,
  the `_describe_session` handler (deep-copied output), and one `COMMANDS` registry
  line. `list_commands` / `run_command` / every existing handler are BYTE-UNCHANGED.
- `tests/test_cowork.py`: the one registry-count assertion updated **33 → 34** (an
  intended, not silent, change).
- New `tests/test_cowork_session_flow.py`: 10 tests (completeness invariant +
  canonical order + real-key checks + determinism + count 34).

**Explicitly out (verified UNTOUCHED):**
- Every existing command's behavior/output; `list_commands` stays the flat catalog.
- `record_pass` / `_apply_history` / the P-008/P-009/P-018/P-019 channel.
- `_KIND_SCORES` / creative / governance; the dead ledger; `pipeline.analyze()`'s
  memory wiring; `cli.py` plumbing beyond registering the new command.
- Any push / merge / deploy.

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-020:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion" — the default-branch tip. Confirmed `6c40e2b` IS an
  ancestor of HEAD. (`159cb66` was the P-020 active-packet confirmation; `6e66d86`
  was the P-019 close.)
- **`942a68a`** — SINGLE packet commit (test-first, additive): `_SESSION_FLOW` +
  `_describe_session` + the one `COMMANDS` registry line. `cowork.py` (+100),
  `tests/test_cowork.py` (registry count 33→34, +2/−2), new
  `tests/test_cowork_session_flow.py` (NEW, +156, 10 tests). **Single commit = the
  tip; Commit-1 green in isolation = 269 passed.**

One commit (within ≤2). No product-code change outside `cowork.py`.

## QA proof (exact)

- **Suite: 259 → 269 passed** (+10; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 269 passed** (single commit = tip).
- **Regression: 68/68, 0 critical, 0 warnings** held (additive read-only command →
  goldens untouched).
- **Completeness invariant proven load-bearing:** every `COMMANDS` key covered
  EXACTLY ONCE across phases + auxiliary (exact cover); orphan → test fails,
  duplicate → test fails. Independently verified partition **31 + 3 = 34 =
  len(COMMANDS)**.
- **`describe_session` deterministic:** byte-identical across calls; output
  DEEP-COPIED so callers cannot mutate the module-level `_SESSION_FLOW`. Returns the
  canonical phase order (intake → classify → diagnose → plan → checklist → validate
  → record-outcome → next-pass); every listed command is a real registry key.
- **Registry: 34, no stale 33 anywhere.**
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN** — independent exact-partition verification (31+3=34).

## Reviewer verdict

**Pass.** Reviewer verified EVERY command placement against its real handler; the
flow is truthful (two defensible judgment calls recorded: `score_mix` and
`compare_to_reference` placed in `plan`); the 3 auxiliaries are genuinely off the
linear axis; the completeness invariant is load-bearing.

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

**One non-blocking reviewer flag → carried to P-021 (below).**

## Residue

- **Carry-forward to P-021 (reviewer flag, non-blocking):** `write_mix_decision`
  writes the display-only DEAD ledger, while `record_mix_pass` writes the LIVE
  history channel; both sit under `record-outcome`. This is honest (both ARE
  outcome-recording, and the per-command `desc` strings telegraph the difference),
  but the dead/live distinction is NOT surfaced in `describe_session`'s output.
  **P-021 (the end-to-end walkthrough) is the natural place to add a one-line
  clarity nudge** so an agent doesn't treat the dead-ledger write as loop-closing.
  Carry as a P-021 consideration.
- **The arc remains the active roadmap (P-021→P-023):**
  - **P-021** — a verified end-to-end agent walkthrough (TESTS-ONLY): drive a full
    Logic-Pro-mixing session through the cowork surface start-to-finish. (Also the
    home for the live-vs-dead-ledger clarity nudge above.)
  - **P-022** — OPTIONAL session-efficiency / override-propagation. Sequence only
    if P-021 surfaces a real need.
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
- **Standing routing guard (P-018, reaffirmed):** outcome/event PRODUCERS go on a
  LIVE channel (history `mix_pass_history.json` → `_apply_history`, or taste
  `taste_profile.json` → governance), NEVER the display-only decision ledger
  (`add_decision` → `decision_ledger.json` has ZERO analyze-path consumers).

## Open boundaries (awaiting explicit go)

- **P-020 is local-only at this close** — commit `942a68a` on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge
  base. **Not pushed / merged.** Any push of this commit — and any subsequent PR /
  merge into the protected default — needs the user's explicit go. **No push /
  merge / deploy / secret action taken in this close.** (The build-os-only close
  commit is separate from the product commit above.)

---
_Archivist close, 2026-07-01. SECOND packet of the arc (P-019→P-023) to a Cowork-usable end-to-end state; the cowork surface is now self-describing as an ordered, phase-grouped session flow (34 commands: 31 across 8 phases + 3 honest auxiliaries); completeness invariant proven load-bearing (exact cover 31+3=34); byte-identical to every existing command. Live-vs-dead-ledger clarity nudge carried to P-021. Single-reviewer verdict (Codex unavailable)._
