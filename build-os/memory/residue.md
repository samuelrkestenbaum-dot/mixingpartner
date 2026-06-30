# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## ★ RESOLVED USER DECISION (was: "read this first")

- **Deeper creative scoring (`creative.py::_KIND_SCORES`) — RESOLVED via P-012
  (option B, penalty-only).** The user chose **option B**: a bounded, transparent,
  capped, **penalty-only** evidence-nudge layer ON TOP of the curated table (the
  `_KIND_SCORES` VALUES are UNCHANGED). Shipped — `score_variant` applies two
  evidence-gated `vocal_belief` penalties (`−8` masked vocal across
  `width_bloom`/`vocal_ride`/`intimacy_pass`; `−6` `width_crowding` for
  `width_bloom`), the summed overall delta clamped to `±2.0`, `score_nudges`
  emitted only on fire. It DELIBERATELY changes default scoring when a nudge fires
  but provably cannot overturn a clear base ranking (cap 2.0 < 2.4–4.2 base gaps).
  **NOTE: this is on the UNMERGED PR #13, awaiting the user's sign-off before merge
  — it's the user's reviewed aesthetic change.** Receipt:
  `build-os/receipts/P-012-creative-scoring-nudge-layer.md`. (Options (a) leave
  as-is and (c) fuller song-derived rescoring were NOT chosen.)

## Deferred (follow-up packets)

- **Reward nudges (orchestrator rows 3+4) — NEW, user-gated:**
  `depth_cleanup +6 halee` / `subtractive_drop +4 taste` when `crowded_sections`
  is non-empty — a possible later ADDITIVE packet IF the user wants reward
  (promotion) nudges. **Deferred** — P-012 is penalty-only by the user's
  recommended reading. Do NOT open without the user asking for reward nudges.
- **Borderline near-tie fixture (from P-012 — NEW, informational, in authority):**
  a fixture that demonstrates an INTENDED near-tie flip through `analyze()` would
  make the option-B behavior visible on real data (today the layer fires but
  overturns nothing on the 3 fixtures — row 2 fires on the LOSING variant; row 1
  never fires). Small additive test, future packet.
- **Borderline-song taste fixture (from P-009 reviewer — non-blocking, in
  authority):** add a fixture where the bounded taste nudge actually **flips the
  governed winner through `analyze()`** end-to-end. Today the decision-level taste
  flip is proven only at the P-007 unit level
  (`test_narrower_taste_changes_governed_winner`); on the real fixtures driven
  through `analyze()` the dominant-variant margin exceeds the bounded ±15 nudge, so
  no winner flip is observed end-to-end. A borderline fixture would make the taste
  axis's production impact visible at the decision level through the live path. Not
  its own large packet — a small additive test. (Pairs naturally with the P-012
  near-tie fixture above.)
- **Wider `--memory-dir` CLI surface (from P-009 reviewer — non-blocking; partly a
  product question):** consider whether more analyze-class CLI commands (beyond
  `cowork`) should accept `--memory-dir`. P-009 wired exactly one prod surface
  (`cowork.py:28`); the other 13 `analyze()` CLI call sites stay memoryless by
  design. Evaluate which, if any, warrant the live wire.
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

## Re-ranked strategic candidates (creative-scoring decision now resolved)

> The learning loop is real in production (P-007→P-008→P-009), the cross-song
> coherence axis is open (P-010), the album-means truth is single-sourced (P-011),
> and the creative-scoring aesthetic decision is RESOLVED via option B (P-012,
> penalty-only — awaiting PR #13 sign-off). For orchestrator re-survey:

- **Reward nudges (orchestrator rows 3+4)** — the natural ADDITIVE follow-on to
  P-012's penalty-only layer, but **user-gated** (the user chose penalty-only).
- **Option-B-visibility fixtures** — near-tie creative fixture (P-012) +
  borderline taste fixture (P-009) — small in-authority additive tests that make
  the bounded nudge axes visible on real data through `analyze()`.
- Wider `--memory-dir` surface remains a small in-authority move (partly product).
- Net-new **event-logging** producers remain behind the product decision.

## Done (resolved)

- **Deeper creative scoring (option B, penalty-only)** — **DONE via P-012**
  (`build-os/receipts/P-012-creative-scoring-nudge-layer.md`).
  **The standing OPEN USER DECISION is resolved.** A bounded, transparent, capped,
  penalty-only evidence-nudge layer sits ON TOP of the curated `_KIND_SCORES`
  (values UNCHANGED): pure `_apply_nudges`/`_NUDGE_TABLE`; `vocal_belief −8` on a
  masked lead vocal (`bad_masking`) across `width_bloom`/`vocal_ride`/`intimacy_pass`
  (generalizing the old `width_bloom`-only caution); `vocal_belief −6` on
  `width_crowding` for `width_bloom`; summed overall delta clamped to
  `±CREATIVE_NUDGE_CAP = 2.0`; `score_nudges: [reason]` emitted only on fire.
  Deliberately NOT byte-identical when a nudge fires, but cannot overturn a clear
  base ranking (cap 2.0 < 2.4–4.2 gaps). Single product commit `0df436c`;
  suite 159→**202** (43 new); regression **68/68** held (variant path
  golden-unguarded — unit tests are the binding guard); Commit-1 green in
  isolation; CAP BINDS EXACTLY (75.7→73.7); NO RECOMMENDATION FLIP on the 3
  fixtures. Reviewer **pass** (adversarially proven — forced −70 raw still clamps
  to base−2.0; layer-ON vs OFF confirms non-tautological no-flip; Codex not
  available). **Awaiting the user's sign-off at PR #13 merge.** Reward nudges
  (rows 3+4) deferred; near-tie visibility fixture deferred.
- **Album delta consolidation / mean-derivation consolidation (P-011 candidate)**
  — **DONE via P-011**
  (`build-os/receipts/P-011-album-delta-consolidation.md`).
  **The two-place album-means truth is killed — single-sourced in `album.py`.**
  `album.py::analyze_album` additively emits per-song `brightness_delta` /
  `lufs_delta` (from the means it already computes); `cli.py::_run_album` consumes
  them and the duplicate `statistics.mean` recompute block (and the now-unused
  `import statistics`) is removed. VALUE-IDENTITY proven exact (emitted deltas ==
  `song − statistics.mean(non-None)` for all 3 fixtures, 0 mismatches; the `album`
  report's `coherence_score` / `outliers` / `verdict` unchanged). Commit-1
  `effccd0`; suite 155→**159**; regression 68/68 held; Commit-1 green in isolation.
- **CLI advisory float rounding (cosmetic, from P-010 reviewer)** — **DONE via
  P-011 Commit-2** (`build-os/receipts/P-011-album-delta-consolidation.md`).
  `next_pass_planner.py::_album_outlier_item` now applies `round(value, 2)` to the
  `"Album coherence"` **DISPLAY** delta text. **Display-only** — the outlier
  threshold logic still uses full precision (`0.151` trips `0.15`). Commit-2
  `ea9bebf`; 4 float-round tests in `tests/test_album_context.py`.
- **Album cross-song coherence** — **DONE via P-010**
  (`build-os/receipts/P-010-album-context-into-planning.md`).
  **MILESTONE — the cross-song coherence axis is now OPEN.** `analyze()` gained an
  opt-in `album_context: {brightness_delta, lufs_delta}`; an album-outlier song
  (thresholds 0.15 brightness / 3 LUFS, verbatim from `album.py:61,63`, not
  imported) receives ONE bounded, advisory, evidence-tagged `"Album coherence"`
  next-pass item at priority 45 (below every truth move — can never outrank Vocal),
  via a pure `_album_outlier_item`. The `album` CLI is now two-pass (pass 1 = album
  means via `analyze_album`; pass 2 = re-run each song with its derived delta) so
  the album report shows album-aware per-song guidance. **A song's plan now
  reflects its album siblings — the product is no longer strictly song-isolated.**
  Commits `dc61f20` (planner+pipeline+test, 10 tests) and `9ebd4ee` (CLI two-pass+
  test, 2 tests); suite 143→**155**; regression 68/68 held; Commit-1 green in
  isolation. NOTE: P-010 left the album means in two places — **resolved by P-011**.
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

- **Variant-scoring path is golden-unguarded (reinforced by P-012):**
  `regression.py` reads `doctrine_score`, never `score_variant`, so the 68/68
  golden cannot catch a `creative.py`/`score_variant` change. **Unit tests are the
  binding guard** for any creative-scoring touch (P-012's
  `tests/test_creative_nudges.py` is the current safety-invariant suite). Treat
  any future creative-scoring change as test-binding, not golden-binding.
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

- **P-012's product commit `0df436c` is local-only as of this close** (this
  archivist close did not push). It carries the user's **reviewed aesthetic
  change** (option B, penalty-only) and is **awaiting the user's sign-off at the
  PR #13 merge** — this is the deliberate review gate for the not-byte-identical
  creative-scoring change. Earlier local-only product commits also remain:
  **`effccd0` + `ea9bebf`** (P-011), **`27bfebf`** (P-009),
  **`dc61f20` + `9ebd4ee`** (P-010). Earlier packets' push history: P-000 install
  commits are pushed to `origin/claude/logic-mix-os-hardening-12-7hbeh1`; P-004 is
  pushed (PR #13). Any push of `0df436c` / `effccd0` / `ea9bebf` / `dc61f20` /
  `9ebd4ee` / `27bfebf` (and the P-005/P-006/P-007/P-008 commits, if not yet
  pushed) updates the already-open **PR #13** (base `claude/dreamy-turing-z0oxll`)
  — do so only under the user's standing/explicit push-go. No merge / deploy /
  secret action taken.

---
_Append-only working notes._
