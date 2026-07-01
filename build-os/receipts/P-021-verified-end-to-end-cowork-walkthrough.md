# P-021 — Verified end-to-end agent walkthrough through the cowork surface (TESTS-ONLY) — the MILESTONE

**Date:** 2026-07-01
**Status:** CLOSED — **MILESTONE PROVEN.** Tests-only (no product/runtime change); qa GREEN, reviewer pass. Third step of the arc P-019→P-023 to a Claude-Cowork-usable end-to-end state — and the step that PROVES it.
**Type:** Build / test-additive — in authority. No new product decision; no product code touched.

---

## Title

Proves, EXECUTABLY, that an agent using ONLY the cowork command surface
(`build_context` + `run_command`) can drive a COMPLETE mixing session
start-to-finish — in `describe_session`'s canonical phase order — AND close the
learning loop, entirely within the surface (never bypassing to `analyze()` /
`record_pass` by hand). After P-021, "Cowork-usable end-to-end" is a pinned
fact, not a claim. No honesty-clause gap surfaced: every phase's essential
command was reachable and the loop closed across the full session.

## What it proves (the mechanism)

- **The driven spine — 8 phases, via `run_command` (NOT bypassing to
  `analyze()` / `record_pass`):** intake → `intake_project`, classify →
  `classify_tracks`, diagnose → `detect_masking`, plan → `generate_mix_plan`,
  checklist → `render_logic_checklist`, validate → `validate_mix_pass`,
  record-outcome → `record_mix_pass` (LIVE), next-pass → `suggest_next_pass`.
  The agent first calls `describe_session` to get the canonical order, then
  drives the essential happy-path command of each phase in that order. Each
  output is JSON-serializable and shape-asserted; the chain never drops out of
  the cowork surface.
- **The loop CLOSES (the milestone assertion — load-bearing + non-tautological):**
  `record_mix_pass(..., reverted=True)` on the LIVE channel → a FRESH
  `build_context(memory_dir=...)` → `suggest_next_pass` surfaces the confirmed
  "Revert last pass" (evidence contains "confirm"), with NO hand re-run of
  `record_pass` / the planner.
  - **Load-bearing:** proven independently by BOTH qa and reviewer — dropping
    `reverted` / routing off the live channel makes the assertion FAIL; restored
    → PASSES (reading an un-threaded store surfaces no revert).
  - **Non-tautological:** the IDENTICAL score-IMPROVED sequence with
    `reverted=False` surfaces NO revert — so the confirmed item is the confirmed
    revert overriding the score inference, not an echo of it.
- **Live-vs-dead pinned as an EXECUTABLE fact (resolves the carried P-020 clarity
  nudge):** `write_mix_decision` (the DEAD ledger — writes only
  `decision_ledger.json`, runtime-verified) does NOT change `suggest_next_pass`;
  `record_mix_pass` (the LIVE history channel) DOES. Only `record_mix_pass`
  closes the loop — so a future agent/reader cannot mistake the ledger write for
  loop-closing.
- **Determinism / honesty:** real seeded fixtures + the real `analyze()` path
  (fake adapters only — no DAW / Logic / AppleScript / subprocess / network /
  `.logicx`). Two fresh contexts → byte-identical plan / next-pass.

## Honest skips (recorded — none is an essential linear phase)

- `compare_to_reference` — needs a reference bounce; without one returns
  `{"note": "no reference supplied"}`. Off the happy-path spine.
- `override_track_identity` — param-heavy / mutating; not a linear phase.
- `build_missing_tool`, `run_creative_engine`, `describe_session` — auxiliary /
  off-axis (the same 3 auxiliaries P-020 identified, plus the two above).

None is a linear essential phase, so none is skipped dishonestly; the walkthrough
drives the core end-to-end path and records the skips explicitly.

## PRECISION NOTE — describe the P-021 coverage guard ACCURATELY (do NOT overstate)

The coverage-honesty test (`test_walkthrough_covers_the_registry_honestly`)
guards **PHASE-COMPLETENESS** (every `describe_session` phase has a driven
essential command belonging to that phase) **+ test-1's exact 8-phase order
pin**. It does **NOT** assert a full `driven ∪ skipped == 34` registry partition
— it references **13 of the 34** commands. The full 34-command exact-cover
partition is guarded **separately** by P-020's
`tests/test_cowork_session_flow.py` (**31 phases + 3 auxiliary = 34**). Together
the two files tell the truth about registry coverage:
- **P-021** — phase-completeness + canonical order of the DRIVEN spine.
- **P-020** — the full 34-command exact-cover invariant.

## Scope

**In:**
- New `tests/test_cowork_session_walkthrough.py` — 8 tests (+372): the driven
  spine in canonical order, the loop-close milestone (load-bearing +
  non-tautological), the live-vs-dead pin, determinism, and the coverage-honesty
  (phase-completeness + order) test.

**Explicitly out (verified UNTOUCHED):**
- **All product/runtime code** — `cowork.py`, `pipeline.py`, `memory.py`,
  `cli.py`, `creative.py`, `governance.py`, the ledger, `_apply_history` — NONE
  changed (tests-only; drives the already-built surface).
- **Every existing test** — no existing assertion edited (a signal to flag, not
  silently edit; none was needed).
- Any push / merge / deploy / secret action.

## Commits (branch base + hash)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-021:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion" — the default-branch tip; confirmed an ancestor of
  HEAD. (`bb3d521` was the P-021 active-packet confirmation; `d40e8a2` was the
  P-020 close.)
- **`dce156b`** — SINGLE packet commit (tests-only): adds exactly ONE file
  `tests/test_cowork_session_walkthrough.py` (8 tests, +372). No product/runtime
  file changed; no existing test edited. **Single commit = the tip; Commit-1
  green in isolation = 277 passed.**

One commit (within ≤2). No product-code change.

## QA proof (exact)

- **Suite: 269 → 277 passed** (+8; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 277 passed** (single commit = tip).
- **Regression: 68/68, 0 critical, 0 warnings** held (tests-only → goldens
  untouched).
- **Milestone loop-close proven load-bearing:** dropping `reverted` / routing off
  the live channel → the assertion FAILS; restored → PASSES (qa AND reviewer
  independently verified, reviewer via monkeypatch). **Non-tautological:** the
  identical score-IMPROVED sequence with `reverted=False` surfaces NO revert.
- **Live-vs-dead pinned:** `write_mix_decision` (dead ledger) does NOT change
  next-pass; `record_mix_pass` (live history) DOES. Runtime-verified the dead
  write touches only `decision_ledger.json`.
- **Determinism confirmed:** two fresh `build_context` calls → byte-identical
  plan / next-pass.
- **Genuine drive, not a bypass:** the spine goes through `run_command`, never
  hand-calling `analyze()` / `record_pass`.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN.**

## Reviewer verdict

**Pass.** Reviewer empirically re-verified the loop-close is load-bearing (via
monkeypatch), confirmed the walkthrough is a genuine drive through the cowork
surface (not a bypass), and confirmed the honest skips are honest. Reviewer
flagged the coverage-honesty test's scope for accurate description (phase-
completeness + order, NOT a 34-registry partition) — captured in the PRECISION
NOTE above.

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## ★ THE MILESTONE SYNTHESIS (the strategic headline)

**The canonical target — "a tool Claude Cowork can use in Logic Pro," plan-only
v1 — is now essentially MET AT THE DECISION-SYSTEM LEVEL.** An agent using ONLY
the cowork command surface can drive the COMPLETE plan-only mixing session
(intake → … → next-pass) AND learn from outcomes (record → the loop closes),
entirely within the surface, proven executably (load-bearing + non-tautological).

What remains is genuinely only **transport packaging**:
- **P-023** — MCP server vs a documented raw-CLI contract as the agent transport.
  A **USER-GATED** architecture decision; do NOT open blind; sequenced LAST.
- **P-022 (session-efficiency / override-propagation) stays OPTIONAL / UNNEEDED**
  — the honesty clause surfaced NO real gap requiring it.

## Residue

- **The arc is now down to ONE remaining step — P-023 (transport), USER-GATED.**
  P-019 ✓ (loop closeable inside cowork), P-020 ✓ (self-describing session flow),
  **P-021 ✓ (MILESTONE — end-to-end drive + loop-close proven).** **P-022 is
  OPTIONAL / UNNEEDED** (no gap surfaced). **P-023 — MCP server vs documented
  raw-CLI contract — is the ONLY remaining arc step; USER-GATED, do NOT open
  blind.**
- **Routing guard now EXECUTABLY pinned (was a standing P-018 note):** outcome
  producers go on a LIVE channel (`record_mix_pass` → `mix_pass_history.json` →
  `_apply_history`, or taste → governance), NEVER the display-only decision
  ledger (`write_mix_decision` → `decision_ledger.json`, zero analyze-path
  consumers). P-021 pins this as an executable fact, not just a note.
- **Standing threads (unchanged, carried):** the judgment layer is at a
  doctrine-honest equilibrium (flip program complete); the symmetric
  `subtractive_drop` over-valuation re-judgment (user-gated, NOT staged); the
  outcome-enum generalization (`reverted`/`kept`/`refined`, widens without
  breaking the default; user-gated for the semantics); wider `--memory-dir` CLI
  surface (small in-authority, partly product).

## Open boundaries (awaiting explicit go)

- **P-021 is local-only at this close** — commit `dce156b` on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15)
  merge base. **Not pushed / merged.** Any push of this commit — and any
  subsequent PR / merge into the protected default — needs the user's explicit
  go. **No push / merge / deploy / secret action taken in this close.** (The
  build-os-only close commit is separate from the tests-only product-repo commit
  above.)

---
_Archivist close, 2026-07-01. THE MILESTONE of the arc (P-019→P-023): an agent driving ONLY the cowork surface can complete a full plan-only mixing session AND close the learning loop, proven executably (load-bearing + non-tautological). Canonical target essentially MET at the decision-system level; only P-023 transport packaging (USER-GATED) remains; P-022 optional/unneeded. Live-vs-dead routing now executably pinned. Single tests-only commit `dce156b` (+372, 8 tests). Suite 269 → 277; regression 68/68. Single-reviewer verdict (Codex unavailable)._
