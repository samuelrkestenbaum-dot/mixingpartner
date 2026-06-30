# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **CLI advisory float rounding (from P-010 reviewer — cosmetic, non-blocking):**
  the `"Album coherence"` detail/evidence print a real CLI-derived delta with a long
  un-rounded float repr; apply `round(value, 2)` for display in a future packet.
  Display-only — the planner-level tests use clean literals, so this does not affect
  correctness, only the rendered text.
- **Mean-derivation consolidation (P-011 candidate — from P-010 reviewer):**
  `album.py:55-58` and `cli.py:367-370` now BOTH compute the album means (currently
  byte-identical, which P-010's QA proved by matching coherence/outliers/verdict).
  A future packet could have `album.py` optionally EMIT per-song deltas, retiring the
  consumer-side recompute in `cli.py` and removing the duplication.
- **Borderline-song taste fixture (from P-009 reviewer — non-blocking):** add a
  fixture where the bounded taste nudge actually **flips the governed winner
  through `analyze()`** end-to-end. Today the decision-level taste flip is proven
  only at the P-007 unit level (`test_narrower_taste_changes_governed_winner`); on
  the real fixtures driven through `analyze()` the dominant-variant margin exceeds
  the bounded ±15 nudge, so no winner flip is observed end-to-end. A borderline
  fixture would make the taste axis's production impact visible at the decision
  level through the live path. Not its own large packet — a small additive test.
- **Wider `--memory-dir` CLI surface (from P-009 reviewer — non-blocking):**
  consider whether more analyze-class CLI commands (beyond `cowork`) should accept
  `--memory-dir`. P-009 wired exactly one prod surface (`cowork.py:28`); the other
  13 `analyze()` CLI call sites stay memoryless by design. Evaluate which, if any,
  warrant the live wire.
- **Low-priority test cleanup (from P-008):** `test_evidence_only_on_moved_candidates`
  in `tests/test_next_pass_history.py` has a redundant always-true inner guard;
  tidy when convenient. **Not its own packet** — fold into any future touch of
  that file.
- **Net-new event-logging packets (from P-002/P-004) — REFRAMED, still BLOCKED ON
  A PRODUCT DECISION:** `taste_feedback`, `validation_check`, `revert`,
  `manual_note` remain valid `EVENT_TYPES` members with **NO producer wired into
  the decision ledger today** (taste → `taste_calibration.json`; validation only
  returns; revert is a pass-record field; no `manual_note` writer exists).
  **Reframe (strengthened by P-009):** the recorded-signal loop now has TWO real
  downstream consumers **that are live in production** (P-007 recorded taste →
  governance and P-008 recorded history → next-pass, both wired through
  `analyze()` by P-009), so wiring `validation_check` / `taste_feedback` producers
  is **more justified than ever**. BUT this is still **net-new FEATURE work**
  behind the same unanswered product decision: **should validation / taste / revert
  / note signals actually be written to the decision ledger?** Keep deferred; do
  NOT start as packets until that product decision lands.

## Genuinely real carried follow-ups (verified)

- **Real macOS/Logic test surface** — out of current authority (needs real DAW;
  blocked by the no-real-DAW guardrail).
- **Controlled Class-3 apply path** — guardrail-gated; do not open without an
  explicit apply-safety packet.

## Re-ranked strategic candidates (cross-song coherence axis now OPEN)

> The learning loop is real in production (P-007→P-008→P-009) AND the cross-song
> coherence axis is open (P-010). The leading trajectory candidate is now deeper
> creative scoring. For orchestrator re-survey:

- **Deeper creative scoring (LEADING candidate)** — `creative.py::_KIND_SCORES` is
  hardcoded (verified NOT golden-blocked). Richer, evidence-driven kind-scoring is
  the leading net-new strategic direction now that coherence is open.
- **`album.py` delta consolidation (P-011 candidate)** — retire the duplicate mean
  computation between `album.py:55-58` and `cli.py:367-370` by having `album.py`
  emit per-song deltas (see Deferred above).
- Loop-polish follow-ups (borderline taste fixture, wider `--memory-dir` surface)
  and the CLI float-rounding cosmetic (see Deferred above).
- Net-new **event-logging** producers remain behind the product decision.

## Done (resolved)

- **Album cross-song coherence** — **DONE via P-010**
  (`build-os/receipts/P-010-album-context-into-planning.md`).
  **MILESTONE — the cross-song coherence axis is now OPEN.** `analyze()` gained an
  opt-in `album_context: {brightness_delta, lufs_delta}`; an album-outlier song
  (thresholds 0.15 brightness / 3 LUFS, verbatim from `album.py:61,63`, not
  imported) receives ONE bounded, advisory, evidence-tagged `"Album coherence"`
  next-pass item at priority 45 (below every truth move — can never outrank Vocal),
  via a pure `_album_outlier_item`. The `album` CLI is now two-pass (pass 1 = album
  means via `analyze_album`; pass 2 = re-run each song with its derived delta) so
  the album report shows album-aware per-song guidance. **`album.py` is NOT
  modified** (delta derived in the consumer, `cli.py`). Default
  (`album_context=None`) is BYTE-IDENTICAL. **A song's plan now reflects its album
  siblings — the product is no longer strictly song-isolated.** Commits `dc61f20`
  (planner+pipeline+test, 10 tests) and `9ebd4ee` (CLI two-pass+test, 2 tests);
  suite 143→**155**; regression 68/68 held; Commit-1 green in isolation.
- **Richer variant→track attribution** — **DONE via P-001**
  (`build-os/receipts/P-001-resolve-variant-track-attribution.md`).
- **Net-new `EVENT_TYPES` decision-ledger vocabulary** — **DONE via P-002**
  (`build-os/receipts/P-002-event-types-vocabulary.md`). `EVENT_TYPES` in
  `constants.py`, optional validated `event_type` on `add_decision`,
  `record_plan_decisions` tags `mute_candidate`, new test added.
- **Readiness-vs-refusal ledger-status UI clarity** — **DONE via P-003**
  (`build-os/receipts/P-003-readiness-vs-refusal-clarity.md`). Labelled
  `READY TO STOP` / `NOT YET — keep iterating` blocks in
  `operator_view.py::render_status` and the `html_dashboard.py` governance card,
  sourced from `result.governance["stop_conditions"]`; 5 new render-only tests.
  Render-only; no backend reach-in.
- **Event-tagging follow-up (from P-002) — in-scope part** — **DONE via P-004**
  (`build-os/receipts/P-004-event-tagging-mix-decision.md`). The one existing
  untagged ledger write (`cowork.py::_write_mix_decision`) now passes
  `event_type="mix_decision"`. **EVENT_TYPES is now applied to every EXISTING
  ledger write:** `mute_candidate` (via P-002's `record_plan_decisions`) and
  `mix_decision` (via P-004's `_write_mix_decision`). The other vocabulary
  members (`taste_feedback` / `validation_check` / `revert` / `manual_note`) have
  no existing producer and are tracked as net-new packets under Deferred above —
  NOT part of this DONE item.
- **`creative_renderer` readiness follow-up (from P-003)** — **DONE via P-005**
  (`build-os/receipts/P-005-creative-renderer-readiness.md`).
  `creative_renderer.py::render_governance`'s `## Stop Conditions` section now
  renders P-003's labelled `READY TO STOP` / `NOT YET — keep iterating` block in
  **markdown** (full `reasons` list, warning-when-ready), replacing the flat
  boolean dump at `creative_renderer.py:104`. Render-only; markdown-clean (no
  HTML); 2 new render-only tests; suite 108→110.
  **MILESTONE — surface consistency closed:** the readiness-vs-refusal treatment
  is now CONSISTENT across all THREE governance surfaces — `operator_view.py`
  (text, P-003), `html_dashboard.py` (HTML, P-003), and `creative_renderer.py`
  (markdown, P-005). The P-003 surface-consistency thread is **fully closed**.
- **`creative.py` literal cleanup** — **DONE via P-006**
  (`build-os/receipts/P-006-creative-literal-cleanup.md`). The two pre-existing
  un-resolved literals in `generate_variants` are now record-backed: Site 1
  (`creative.py:194`, `chorus_lift_B`) `loops or supporting[-1:]` →
  `_resolve(loops, supporting[-1:], [r["name"] for r in records][:1])` (closes the
  empty-`tracks_affected` path, restores P-001's non-empty + real-record-subset
  invariant, reuses the `_resolve` seam); Site 2 (`creative.py:217`, `loop`
  branch) replaces the `"the loop"` literal with a real-record-name fallback.
  Single product commit `6e98a3b`; suite 110→112; 2 new tests.
  **Every `tracks_affected` site in `generate_variants` is now record-backed and
  non-empty**, and loop-branch prose can no longer name a non-existent track
  (except under a degenerate record-free input — see Known risks below).
- **Taste profile feeds governance** — **DONE via P-007**
  (`build-os/receipts/P-007-taste-feeds-governance.md`). The recorded operator
  taste profile (`memory._derive_taste` statements) now **biases variant
  governance** — opt-in, bounded, evidence-tagged. An optional `taste_profile`
  arg (default `None`) on `govern_variant` / `govern_branches` / `run_governance`;
  a pure `_apply_taste` helper + `_TASTE_KIND_BIAS` map (verbatim `_TASTE_MAP`
  statements); `TASTE_MAX_DELTA = 15` (`< 30`, the truth nudge); a
  `taste_adjustments` evidence field present **only** when an adjustment applies.
  Two operators with different taste now get different governed winners from the
  same song (proven: narrower taste flips `chorus_lift_A` → `chorus_lift_C`).
  Single product commit `bd08f28` (`governance.py` +75/−6,
  `tests/test_governance_taste.py` new, 13 tests); suite 112→125; regression
  68/68 held; default path byte-identical (the HARD backward-compat gate).
  **This was the FIRST closure of the learning loop (the *consumer* half).**
- **`drum_room_bloom` narrower-taste test gap (from P-007)** — **DONE via P-008
  (Commit-2 `dbf94c3`).** The `drum_room_bloom` path in
  `governance._TASTE_KIND_BIAS` was data-symmetric with `width_bloom` but
  untested; a mirror of `test_narrower_taste_lowers_width_bloom_identity_bounded`
  was folded into `tests/test_governance_taste.py` (additive). Closed.
- **History-aware next pass (THE OUTCOME SIDE OF THE LEARNING LOOP)** — **DONE via
  P-008** (`build-os/receipts/P-008-history-aware-next-pass.md`). `plan_next_pass`
  now consumes recorded mix-pass history — opt-in, bounded, evidence-tagged. An
  optional trailing `history` arg (default `None` → byte-identical); a
  `_MOVE_TARGET` map bridges history's score-keyed `got_worse` to titled
  candidates; a move whose target regressed AND was recommended last pass is
  **demoted** (`HISTORY_DEMOTE = 40`, floored ≥ 0, survives — not deleted); a
  single non-destructive `"Revert last pass"` move surfaces at priority 95 when
  `revert_candidates` is non-empty; each history-touched candidate carries an
  `evidence` line (absent otherwise). Uses only `history[-1]`. Deterministic.
  Commit-1 `d98a194` (planner + new `tests/test_next_pass_history.py`, 12 tests),
  Commit-2 `dbf94c3` (drum_room_bloom test); suite 125→138; regression 68/68 held;
  default path BYTE-IDENTICAL three ways; Commit-1 green in isolation. Reviewer:
  **pass** (revert at 95>90 ruled acceptable — bounded/non-destructive/cannot
  manufacture a move; Codex not available). **This was the SECOND closure (the
  *outcome* half).**
- **P-007b — Live opt-in taste surface** — **DONE via P-009** (subsumed). The real
  per-operator `taste_profile` from `memory_dir` is now wired into the production
  analysis path: `analyze(..., memory_dir=...)` threads
  `taste_profile()["profile"]` into `run_governance`, and `cowork.py:28` passes
  `memory_dir` so the live `cowork --memory-dir` CLI run personalizes governance.
  The byte-identical-by-default guarantee survives (default `memory_dir=None` →
  `_taste=None` → existing no-op). Receipt:
  `build-os/receipts/P-009-live-wire-memory-into-analyze.md`.
- **P-008b — Live history wire** — **DONE via P-009** (subsumed). `memory.history()`
  is now threaded into `pipeline.analyze()` → `plan_next_pass` so a real recorded
  history reaches the planner in production; the live `cowork --memory-dir` run
  history-demotes regressed moves / surfaces revert. The byte-identical-by-default
  guarantee survives (default `memory_dir=None` → `_history=None` → existing
  no-op). Receipt: `build-os/receipts/P-009-live-wire-memory-into-analyze.md`.
- **Live wire — real memory into the production analysis path (THE LOOP IS NOW
  REAL IN PRODUCTION)** — **DONE via P-009**
  (`build-os/receipts/P-009-live-wire-memory-into-analyze.md`). `analyze()` gained
  an opt-in trailing `memory_dir`; when set it builds `ProjectMemory` once and
  threads `history()` → `plan_next_pass` and `taste_profile()["profile"]` →
  `run_governance`; `cowork.py:28` passes `memory_dir` so the pre-existing CLI
  `cowork --memory-dir` chain is live. Single product commit `27bfebf`; suite
  138→**143**; regression 68/68 held; **default path BYTE-IDENTICAL** (full
  `ProjectAnalysis` exact string-equal three ways — the `"evidence"` keys are
  pre-existing baseline fields, not a leak); Commit-1 green in isolation; safety
  grep clean. Reviewer: **pass** (taste axis ruled genuinely live — flows e2e +
  lowers identity; no winner flip on this fixture is a data property, decision-level
  flip proven by P-007's unit test on the same `analyze()`-driven path; Codex not
  available).
  **MAJOR MILESTONE — THE LEARNING LOOP IS NOW REAL IN PRODUCTION.** A real
  `cowork --memory-dir` run both **learns** (records → history-aware next pass)
  and **personalizes** (taste → governance). P-009 subsumes and completes
  **P-007b + P-008b**. The full arc **P-007 (consumer) → P-008 (outcome) → P-009
  (live wire)** is closed end-to-end.

## Stale / not-real (verified by orchestrator — do NOT act on as written)

- The following inherited follow-ups reference architecture that has **ZERO
  matches in this repo** and should be treated as stale: `LogicActionPayload`
  (multi-parameter), a real adapter narrowing `supported_action_types`,
  `RealLogicSessionAdapter`, dead `_RISK_HINTS` cleanup, adding to an existing
  `EVENT_TYPES` enum, full `Gravito` adapter, standalone `compare-variants`
  alias. That architecture does not exist here — verified by grep (0 matches).
  NOTE: P-002 delivered `EVENT_TYPES` as **net-new** flat vocabulary (not "added
  to an existing enum"); the stale "existing enum" framing remains wrong.
- A prior chat handoff referenced git state (a `main` branch, PR #12, branch
  `claude/hardening-11-…`) that does NOT match this repo on disk — there is no
  `main`; default is `claude/dreamy-turing-z0oxll`. Treat any inherited
  SHA/PR/packet-number claims as unverified until checked against `git`.

## Known risks / debt

- **Degenerate empty-`records` input (low priority — NOT a packet yet):** under a
  truly **empty** `records` list (an unconstructible / degenerate input on the
  engine path), P-006's Site 1 still returns `[]` and Site 2 still yields
  `"the loop"`. Acknowledged by the reviewer as out-of-scope — a possible future
  guard, not a defect. Raise as a packet only if a record-free engine path
  becomes constructible.
- Test env: numpy + pytest are not preinstalled. The full suite requires
  `pip install -e ".[dev]"` from `logic-mix-os/` (a network install) before
  `python -m pytest`.
- **Commits on this branch are unsigned.** The configured SSH signing key
  (`/home/claude/.ssh/commit_signing_key.pub`) is an empty 0-byte file and the
  container runs as `root`, so signing is impossible. Author + committer are
  correctly `noreply@anthropic.com`; GitHub will show these commits as
  "Unverified" (missing signature only, not a misattribution). This is an
  environment limitation, not a fix-it item.

## Open boundaries (awaiting explicit go)

- **P-010's product commits `dc61f20` + `9ebd4ee` are local-only as of this close**
  (this archivist close did not push). **P-009's product commit `27bfebf` is also
  local-only.** Earlier packets' push history: P-000 install commits are pushed to
  `origin/claude/logic-mix-os-hardening-12-7hbeh1`; P-004 is pushed (PR #13). Any
  push of `dc61f20` / `9ebd4ee` / `27bfebf` (and the P-005/P-006/P-007/P-008
  commits, if not yet pushed) updates the already-open **PR #13** (base
  `claude/dreamy-turing-z0oxll`) — do so only under the user's standing/explicit
  push-go. No merge / deploy / secret action taken.

---
_Append-only working notes._
