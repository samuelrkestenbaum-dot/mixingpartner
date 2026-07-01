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
  **NOW MERGED to default via PR #13 (merge commit `0f4e7e9`)** — the user's
  reviewed aesthetic change is live. **P-013 (tests-only) then proved the nudge
  fires on REAL DATA through the live `analyze()` path** (`dense_chorus_with_loops`
  emits a real `width_crowding` event → row-2 nudge fires; overall_score
  75.7→74.9; winner unchanged — option (a)), closing the golden-unguarded gap.
  Receipts: `build-os/receipts/P-012-creative-scoring-nudge-layer.md`,
  `build-os/receipts/P-013-nudge-visibility-fixture.md`. (Options (a) leave
  as-is and (c) fuller song-derived rescoring were NOT chosen.)

- **THE BASE-VALUE RE-CURATION LEVER IS PROBED AND THE JUDGMENT LAYER IS AT A
  DOCTRINE-HONEST EQUILIBRIUM (P-017).** The user chose "A" -- attempt the FIRST
  change to a base `_KIND_SCORES` value (re-curate `depth_cleanup` so the
  depth/hierarchy move wins the `density` branch). **FINDING: an honest re-curation
  CANNOT flip `density` -- arithmetically forced by the doctrine, verified
  adversarially. `_KIND_SCORES` LEFT UNTOUCHED (no product change).** THREE
  independent levers have now converged on the same place: penalty (P-012/P-015),
  reward/promotion (P-016), and base-value re-curation (P-017) all confirm that
  `subtractive_drop`'s default dominance is legitimate, the masked-vocal near-tie
  (P-015) and foregrounded-loop promotion (P-016) are the ONLY doctrinally-warranted
  flips, and **there is NO honest further flip move inside the current dimension
  set.** The evidence/re-curation program to make judgment decisive is essentially
  COMPLETE. The one remaining honest thread is a SYMMETRIC re-judgment (is
  `subtractive_drop` itself slightly over-valued?) -- user-gated, un-signed-off, NOT
  staged. Receipt: `build-os/receipts/P-017-doctrine-honest-kind-scores-recuration.md`.

## Deferred (follow-up packets)

- **★ THE ACTIVE ROADMAP — THE ARC TO A COWORK-USABLE END-TO-END STATE
  (P-020 → P-023).** Canonical target: Logic Mix OS as a tool Claude Cowork can
  drive END-TO-END in a Logic Pro mixing session (plan-only v1). **P-019 closed the
  FIRST step** — the learning loop is now closeable INSIDE the cowork surface
  (`record_mix_pass`, read/write symmetric). The rest of the arc, in sequence:
  - **P-020 — session-flow discoverability:** phase-grouped commands so an agent
    can navigate the 33-command surface (intake → classify → diagnose → plan →
    checklist → validate → record → next-pass). In-authority, additive.
  - **P-021 — verified end-to-end agent walkthrough (TESTS-ONLY):** drive a full
    Logic-Pro mixing session through the cowork surface start-to-finish; prove the
    whole chain works as one session.
  - **P-022 — OPTIONAL session-efficiency / override-propagation.** Sequence only
    if P-020/P-021 surface a real need.
  - **P-023 — USER-GATED transport decision: MCP server vs a documented raw-CLI
    contract.** **Do NOT open blind; sequenced LAST** — it is a product/architecture
    fork that needs an explicit user ask.

- **Reward-nudges family — NOW CLOSED as SATURATED / EQUILIBRIUM (P-017).**
  P-016 shipped the FIRST reward/promotion nudge (the `loop` branch:
  `loop_deconstruct` promoted +4.0 past `subtractive_drop` when a loop is
  genuinely foregrounded), evidence-gated and LIVE in production, and it MERGED via
  PR #15. **But the further-reward-rows thread is now CLOSED:** the reward layer is
  saturated at cap 4.0 — only `loop` (gap 3.43) was cleanly reachable; `density`
  (gap 4.14) is unreachable + circular-gated; `drum_room_bloom` is hollow (no
  evidence signal). And P-017 confirmed the base-value re-curation lever cannot
  honestly flip `density` either. The three levers (penalty, reward, base-value)
  have all converged on a DOCTRINE-HONEST EQUILIBRIUM: **there is no honest further
  flip move inside the current dimension set.** Should the user ever ask for a NEW
  reward row anyway, it would still be user-gated per-row and must clear the SAME
  bar as P-016 (its own evidence gate + a non-vacuity mutation check + a
  collateral-safety proof + a live-wire check: evidence computed BEFORE
  `run_creative_engine`; asserted on the real `result.creative`/`result.governance`
  with NO re-run) — but this is no longer an in-flight candidate.
- **Near-tie-creative-FLIP fixture — RESOLVED-as-UNREACHABLE (P-014 verified
  negative finding).** This was the reachable-deferred complement to P-013's
  no-flip case; **P-014 proved a flip is structurally UNREACHABLE test-only**
  under the current `_KIND_SCORES` / `_NUDGE_TABLE`. The builder wrote ZERO code
  (honesty clause); qa adversarially CONFIRMED with THREE independent harnesses
  (inline-math, real-`score_variant`, saturated worst-case `masking_report`) —
  **all 0 flips** — plus a source re-derivation. Two structural reasons: the
  universal branch leader `subtractive_drop` (85.29) is in NO nudge row →
  penalty-immune; the one sub-cap near-tie branch (`vocal_belief`, gap 1.71)
  penalizes leader (`vocal_ride`) and runner-up (`intimacy_pass`) equally
  (identical row-0 `lead_masked −8`). **No longer a reachable candidate** — it is
  replaced by the user-gated curation packet directly below. Receipt:
  `build-os/receipts/P-014-near-tie-creative-flip-fixture.md`. (The P-014
  harnesses live in scratchpad — not committed.)
- **Make-the-nudge-decisive (curation change) — RESOLVED by P-015 (user-signed-off
  PRODUCT change).** The user chose "Option 1 — Proceed, corrected" (2026-06-30)
  and P-015 actioned route (a): `creative.py` `_NUDGE_TABLE` row-0 now **exempts
  `intimacy_pass`** and **strengthens the penalty `−8` → `−14`** (= −2.0 overall =
  the cap), so the `vocal_belief` 1.71-gap near-tie now FLIPS `vocal_ride` (vocal_A)
  → `intimacy_pass` (vocal_B) within the ±2.0 cap. The nudge is **no longer
  transparency-only** — it is decisive on exactly that near-tie, still bounded so it
  cannot overturn a clear ranking. Receipt:
  `build-os/receipts/P-015-decisive-masked-vocal-nudge.md`. **No remaining work
  here.**
- **Reviewer trajectory flag (from P-015 — non-blocking, watch-item):** the P-015
  flip margin is **thin (0.2)**, but it is **fully pinned by binding tests**
  (`tests/test_decisive_nudge.py`: flip + load-bearing negative control + collateral
  safety; updated `tests/test_creative_nudges.py`). A future re-curation of the
  creative scoring would surface as a **RED test, not a silent re-rank** — the
  golden-unguarded variant-scoring path is covered by these unit/flip tests. Carry
  this awareness into any future `creative.py` / `_NUDGE_TABLE` / `_KIND_SCORES`
  touch.
- **Reviewer watch-item (from P-016 — non-blocking, standing) — REWARD-CREEP:**
  P-016 crossed the penalty-only line with the FIRST reward nudge. Any FUTURE
  reward row must clear the same bar P-016 did: its own evidence gate + a
  non-vacuity mutation check + a collateral-safety proof + a **live-wire check**.
  Watch the trajectory — reward nudges are additive pressure on the default
  recommendation; keep each one bounded (a separate `CREATIVE_PROMOTION_CAP`),
  evidence-gated, and user-gated per-row.
- **★ STANDING LESSON (from P-016 — the P-009-style catch):** an evidence-gated
  creative nudge is only LIVE if its evidence is computed BEFORE
  `run_creative_engine`. In P-016, Commit-1's promotion was INERT in production —
  `run_creative_engine` ran before `provenance`/`source_audits` were populated, so
  the predicate always read empty evidence; the tests passed only because they
  RE-RAN the engine on the finished result (masking the inertness). Commit-2's
  live-wire (relocate `analyze_provenance` + `audit_all` just before
  `run_creative_engine`, a pure relocation) fixed it, guarded by two
  production-liveness tests that assert on the real `analyze()`
  `result.creative`/`result.governance` with NO re-run (FAIL pre-reorder, PASS
  after). Masking is pre-creative so P-015 was always live; provenance/source_audits
  were post-creative until P-016. **Rule:** for any future creative nudge, add a
  no-re-run liveness assertion — a green re-run test can mask production inertness.
- **Taste-flip through `analyze()` — STRUCTURALLY UNREACHABLE test-only
  (P-013 finding); a flip is USER-GATED to a product change.** P-013 tried to build
  a taste-driven governed-winner flip fixture and could NOT: the builder brute-forced
  all 3 fixtures × 4 intents with a narrower-taste `ProjectMemory` and found NO
  governed-winner flip anywhere. **This is a POSITIVE alignment confirmation, not a
  gap** — reviewer-verified in source: `_apply_taste` (governance.py) moves only the
  `taste_triangle` **identity** axis (clamped ±`TASTE_MAX_DELTA 15`), maps only to
  `width_bloom`/`drum_room_bloom` (`_TASTE_KIND_BIAS`), and the governed winner is
  ranked on `overall_score` behind an **align-veto**, so **taste structurally cannot
  reorder a truth-ranked winner** (doctrine: "taste can never outrank a truth move,"
  working as intended). The unit "flip" in `test_governance_taste.py` only works
  because it hand-injects branch values curated scoring never produces. **The
  reachable end-to-end taste claim (taste reaches governance + down-weights identity
  with bounded evidence) is ALREADY proven on real data** by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`. Making a real
  governed-winner flip reachable would need a product-code aesthetic change →
  **user-gated, a separate packet** (distinct from the reachable near-tie-creative
  FLIP fixture above).
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
  **★ CORRECTION (P-018 finding — read before routing any such producer):** the
  decision LEDGER (`add_decision` → `decision_ledger.json`) has **ZERO analyze-path
  consumers** — `mem.ledger()` is display-only (`cli.py:315`). So a producer that
  merely WRITES to the ledger is **INERT** (the hollow trap). `validation_check` /
  `manual_note` producers now **need a NEW consumer — not just a ledger write.**
  The only LIVE learning channels are HISTORY (`mix_pass_history.json` →
  `_apply_history`) and TASTE (`taste_profile.json` → governance); P-018's
  confirmed `revert` correctly landed on the history channel (not the ledger).
- **★ Outcome-enum generalization (reviewer's P-018 trajectory note — non-blocking;
  a candidate, NOT staged):** capturing only `revert` leaves the outcome vocabulary
  lopsided. A future generalization to a small outcome enum
  (`reverted` / `kept` / `refined`) would round out the outcome→learning loop, and
  the P-018 `reverted: bool` field can widen to that later **WITHOUT breaking the
  byte-identical default.** Reachable, user-gated for the semantics; do NOT open
  without an explicit ask.
- **★ THE LEDGER-IS-DEAD FINDING (P-018 — a standing routing guard):** the decision
  LEDGER (`add_decision`/`decision_ledger`) has NO decision-making consumer — it is
  display-only (`cli.py:315`). **Do NOT route an inert ledger producer.** A
  confirmed-outcome / event producer is only real if it lands on a LIVE channel
  (history `mix_pass_history.json` → `_apply_history`, or taste `taste_profile.json`
  → governance). This is why P-018's confirmed revert lands on the history axis.

## Genuinely real carried follow-ups (verified)

- **Real macOS/Logic test surface** — out of current authority (needs real DAW;
  blocked by the no-real-DAW guardrail).
- **Controlled Class-3 apply path** — guardrail-gated; do not open without an
  explicit apply-safety packet.

## Re-ranked strategic candidates (creative-scoring decision now resolved)

> The learning loop is real in production (P-007→P-008→P-009), the cross-song
> coherence axis is open (P-010), the album-means truth is single-sourced (P-011),
> the creative-scoring aesthetic decision is RESOLVED (P-012 option B, MERGED PR
> #13; P-015 decisive; P-016 reward, MERGED PR #15), and the judgment layer is now
> at a DOCTRINE-HONEST EQUILIBRIUM (P-017 — no honest further flip in the current
> dimension set), the OUTCOME→learning axis is OPEN (P-018 — the first
> confirmed-outcome signal is live), and the learning loop is now CLOSEABLE INSIDE
> the cowork surface (P-019 — read/write symmetric; FIRST step of the arc
> P-019→P-023 to a Cowork-usable end-to-end state). For orchestrator re-survey:

- **THE FLIP PROGRAM IS ESSENTIALLY COMPLETE — DOCTRINE-HONEST EQUILIBRIUM
  (P-017).** The three levers have converged: penalty (P-012/P-015), reward
  (P-016), and base-value re-curation (P-017) all confirm `subtractive_drop`'s
  dominance is legitimate; the masked-vocal and foregrounded-loop overrides are the
  only warranted flips; **NO honest further flip exists in the current dimension
  set.** The reward-family (further rows) and re-curation-for-flips threads are
  CLOSED as saturated. **The ONE remaining honest thread — user-gated, NOT staged:**
  a SYMMETRIC re-judgment — is `subtractive_drop` at 85.29 (high on every dim)
  itself slightly OVER-valued? Lowering it (rather than inflating a rival) would be
  a different, un-signed-off packet. Surface to the user; do NOT open without an
  explicit ask.
- **★ THE OUTCOME→LEARNING AXIS IS OPEN (P-018) AND NOW CLOSEABLE INSIDE COWORK
  (P-019).** P-018 landed the first confirmed-outcome signal (`memory-record
  --reverted` overrides the score-inference and measurably changes real
  `analyze(--memory-dir)` next_pass; opt-in / byte-identical default). **P-019
  brought the RECORD side onto the cowork surface** — a `record_mix_pass` command
  (registry 32→33) records a pass on the LIVE history channel, so an agent can close
  the loop (record → see `suggest_next_pass` change) without leaving the surface
  (read/write symmetric). The reachable outcome-side next move is the **outcome-enum
  generalization** (`reverted`/`kept`/`refined`, widening the `reverted: bool`
  without breaking the default) — **user-gated for the semantics; NOT staged.** The
  in-flight roadmap now is the cowork ARC (P-020→P-023, see the Deferred section).
  **Standing routing guard:** route any outcome/event producer onto a LIVE channel
  (history or taste), never the display-only ledger.
- **Option-B-visibility / decisiveness** — the CREATIVE half is fully closed:
  **P-013** proved the nudge fires on real data through `analyze()` (option-(a)
  no-flip on a clear ranking), **P-014** proved a near-tie FLIP was unreachable
  *under the then-current curation*, and **P-015** (user-signed-off product change)
  made it decisive on the masked-vocal near-tie (`vocal_belief`: vocal_ride →
  intimacy_pass, within the cap). Nothing reachable remains here. The TASTE-flip
  half is **user-gated** (needs a product change; the reachable taste claim is already
  covered by `test_live_wire.py::test_taste_axis_changes_governance`).
- Wider `--memory-dir` surface remains a small in-authority move (partly product).
- Net-new **event-logging** producers remain behind the product decision.

## Done (resolved)

- **`record_mix_pass` closes the learning loop INSIDE the cowork surface (FIRST
  step of the arc P-019→P-023 to a Cowork-usable end-to-end state) — DONE via
  P-019** (`build-os/receipts/P-019-record-mix-pass-closes-loop-in-cowork.md`).
  **PRODUCT-code feature; in-authority (reuses the already-live
  `record_pass`/`_apply_history` channel — no new product decision).** Adds a
  **`record_mix_pass`** command to the cowork `COMMANDS` registry (count **32 →
  33**). **The mechanism:** its handler (`cowork.py:97-106`) records a pass on the
  LIVE history channel — `ctx["memory"].record_pass(name, ctx["result"],
  reverted=...)` → `mix_pass_history.json` — passing through the P-018 `reverted`
  ground-truth flag (opt-in, default False), returning the record JSON; clean
  `{"error": "no memory_dir configured"}` when no memory dir (mirrors
  `_write_mix_decision`). So an agent driving through the cowork surface can now
  RECORD an outcome and see `suggest_next_pass` change WITHOUT leaving the surface —
  the read/write cowork surface is symmetric (the READ side was already live via
  P-009). Routes to the LIVE channel, NOT the dead decision ledger. **One surface
  finding, resolved minimally (NOT a wall):** the cowork `--params '{...}'` path
  unpacks user JSON into `run_command(name, ctx, **params)`, so a handler param
  named `name` collided with the dispatcher's positional `name`; fixed by making
  the dispatcher's `name`/`ctx` **positional-only** (`run_command(name, ctx, /,
  **params)`) — behavior-preserving (repo-wide grep found ZERO callers passing
  `name=`/`ctx=` by keyword; the sole product caller `cli.py:237` passes
  positionally). **Two commits (≤2):** `b7572b7` Commit-1 (handler + registry row +
  positional-only + unit tests; test-first, green in isolation = 257) + `de5679f`
  Commit-2 (no-re-run liveness guard). `cowork.py` is the only product file touched.
  **Proof:** suite **253 → 259 passed** (+6; 0 failed/skipped/warnings, green under
  `-W error`); regression **68/68, 0 critical, 0 warnings** held (opt-in memory path
  → goldens untouched; byte-identical default). **LIVENESS proven load-bearing (the
  P-016/P-018 lesson honored):** `test_loop_closes_through_cowork_no_rerun` records
  a confirmed revert via `run_command("record_mix_pass", ...)` on a score-IMPROVED
  override case, then a FRESH `build_context(memory_dir=...)` →
  `run_command("suggest_next_pass")` surfaces the confirmed "Revert last pass" — NO
  hand re-run. Both qa and reviewer INDEPENDENTLY broke the wiring (handler off the
  live channel) → FAILS; restored → PASSES. **Routes to the live channel (runtime
  probe):** only `mix_pass_history.json` created, never `decision_ledger.json`.
  **Byte-identical default:** date-neutralised canonical JSON equal to standalone
  `memory-record`. Registry 33, no stale 32. Scope: only 3 files (`cowork.py`
  additive, `test_cowork.py` count assertion 32→33, new `tests/test_cowork_record.py`);
  `memory.py`/`cli.py`/`pipeline.py`/ledger/creative/governance UNTOUCHED;
  P-008/P-009/P-018/existing-cowork tests green. Safety grep clean; UI N/A. qa
  **GREEN** (mutation-verified liveness + non-tautological override + live-channel
  routing probe). Reviewer **pass** (handler correct + routes live [verified by
  breaking it]; positional-only safe/minimal; loop closes through cowork;
  non-tautological override case). **Codex NOT available — single-reviewer
  verdict.** **P-019 is local-only** (commits `b7572b7`, `de5679f` on the dev branch
  on top of the `6c40e2b` PR #15 merge base), not pushed/merged at close.

- **Confirmed-revert outcome feeds the live next-pass loop (the FIRST
  confirmed-outcome signal in the learning loop) — DONE via P-018**
  (`build-os/receipts/P-018-confirmed-revert-feeds-next-pass-loop.md`).
  **PRODUCT-code feature; a PIVOT off the complete judgment-tuning path onto the
  learning-loop / feedback frontier** (user said "Yes"); orchestrator-routed;
  **OVERRIDE semantics chosen by the orchestrator-in-chief (user may redirect at
  the merge gate).** Until now every loop signal was score-INFERRED; P-018 adds a
  CONFIRMED one. **The mechanism:** an opt-in `memory-record --reverted` records a
  confirmed operator revert on a pass (`record_pass(..., reverted=True)` →
  `mix_pass_history.json`); the live `_apply_history` consumer (already threaded to
  real `analyze(--memory-dir)` via P-009) then, on a confirmed revert, DEMOTES the
  recommended-then-reverted moves and surfaces exactly ONE confirmed "Revert last
  pass" item at priority 95 — **regardless of the score-delta `got_worse`
  inference (OVERRIDE)**, with an early return that prevents double-up with the
  score-inferred revert candidate; distinct honest evidence line (contains
  "confirm", vs the score-inferred "recorded revert candidate(s): …").
  **OVERRIDE rationale:** a confirmed operator revert is GROUND TRUTH and outranks
  the heuristic proxy (Halee/Ramone operator-serving judgment). **Why THIS seam:**
  the decision LEDGER (`add_decision` → `decision_ledger.json`) has ZERO
  analyze-path consumers (display-only, `cli.py:315`), so any reserved-ledger-event
  producer would be INERT; the ONLY reachable LIVE seam was the history axis
  (`record_pass` → `_apply_history`) — hence the confirmed revert lands there.
  **Two commits (≤2):** `736fa8b` Commit-1 (`record_pass` `reverted` field +
  `_apply_history` override + 9 unit tests; test-first, green in isolation = 249) +
  `6134d27` Commit-2 (`--reverted` CLI wire + 4 no-re-run liveness/CLI tests).
  `memory.py`, `planners/next_pass_planner.py`, `cli.py` are the only product files
  touched. **Proof:** suite **240 → 253 passed** (+13; 0 failed/skipped/warnings,
  green under `-W error`); regression **68/68, 0 critical, 0 warnings** held (no
  `memory_dir` → falsy no-op → goldens untouched). **LIVENESS proven load-bearing
  (the P-016 lesson honored):** the no-re-run liveness test asserts on real
  `analyze(memory_dir=...)` `next_pass` and FAILS with the pre-P-018
  `_apply_history` (would be inert) and PASSES at tip — NOT inert. **OVERRIDE
  non-vacuous:** with an IMPROVED score delta (`got_worse` empty) but
  `reverted=True`, the confirmed "Revert last pass" still surfaces at rank 0 and
  the reverted move is demoted — override, not a score echo. **Byte-identical
  default:** no `--reverted` → next_pass identical to today; no `reverted` key when
  unused. **Scope clean:** ledger/`add_decision`/reserved ledger events, taste axis,
  `_KIND_SCORES`/creative/governance UNTOUCHED; P-008 `test_next_pass_history.py` +
  P-009 `test_live_wire.py` unedited and green (17). Safety grep clean; UI N/A. qa
  **GREEN** (independently mutation-verified liveness + non-vacuous override; qa
  self-flagged a transient stale-state artifact in one of its OWN scratch scripts —
  a qa-harness quirk, NOT a product defect — and confirmed the traced re-runs are
  authoritative). Reviewer **pass** (override bounded/deterministic; early-return
  skips only the score-inferred revert; demotes exactly the reverted pass's
  recommended moves; mutation-verified load-bearing). **Codex NOT available —
  single-reviewer verdict.** **Reviewer trajectory note (non-blocking, candidate,
  NOT staged):** a future outcome enum (`reverted`/`kept`/`refined`) would round
  out the loop — the `reverted: bool` field can widen to it WITHOUT breaking the
  byte-identical default. **P-018 is local-only** (commits `736fa8b`, `6134d27` on
  the dev branch on top of the `6c40e2b` PR #15 merge), not pushed/merged at close.

- **Base-value `_KIND_SCORES` re-curation (density → depth_cleanup) — RESOLVED as
  a VERIFIED NEGATIVE FINDING via P-017**
  (`build-os/receipts/P-017-doctrine-honest-kind-scores-recuration.md`).
  **User-signed-off ("A"); the FIRST attempt to change a base `_KIND_SCORES`
  value** (crossing the line P-012/P-015/P-016 held: they layered evidence nudges
  on an UNTOUCHED base). **FINDING: an honest re-curation of `depth_cleanup` CANNOT
  flip the `density` branch — arithmetically forced by the DOCTRINE (which dims are
  honestly movable), not a search failure. `_KIND_SCORES` LEFT UNTOUCHED — NO
  product change** (the honesty clause held; P-014 discipline). **The forced
  arithmetic:** `overall = mean(7 dims) − risk_penalty`; `depth_cleanup` 81.14
  (dim sum 568) vs `subtractive_drop` 85.29 (dim sum 597, low risk) → gap 4.14; the
  only doctrine-defensible under-valuation is `contrast` (dc 72 vs sd 88): →88 =
  83.43 (short 1.86), →100 (impossible ceiling) = 85.14 (STILL below); a FULL honest
  re-curation (contrast→88, technical→85, ramone→86, taste→86; halee stays 90=max,
  vocal_belief stays 86; **excitement LOCKED at 66**) reaches only 83.86 (short
  1.43); the entire residual deficit lives in `excitement` (66 vs 78), OFF-LIMITS to
  inflate (subtle depth work is honestly un-flashy) — the only flips require
  inflating excitement or re-labeling a depth pass as vocal-forward, both dishonest.
  **The committed guard (load-bearing, non-tautological):** the builder committed
  ONLY `tests/test_density_recuration.py` (NEW, 12 tests, +183, sole packet commit
  `1b03ad3`) pinning the 5-branch winner table UNCHANGED on the real `analyze()`
  path + the honest-ceiling arithmetic + `_KIND_SCORES` untouched; an injected
  inflated `depth_cleanup` (contrast=88+excitement=90, or all dims=100) makes it
  FAIL (density → density_A), so it genuinely catches an accidental/dishonest
  density flip. Committing executable arithmetic is defensible here (unlike P-014's
  no-commit finding) because the finding IS arithmetic and the variant-scoring path
  is golden-unguarded. **Before/after winner table (all 5 branches, real path)
  UNCHANGED:** chorus_lift→subtractive_drop 85.3; density→subtractive_drop 85.3;
  loop→subtractive_drop 85.3 (default); depth→depth_cleanup 81.1 (single-variant);
  vocal_belief→vocal_ride 82.9. **Proof:** suite **228 → 240 passed** (+12; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held; Commit-1 (the sole commit) green in isolation (new file alone
  12 passed); safety grep clean; UI N/A; P-012/P-013/P-015/P-016 test files NOT
  edited and pass (69). qa **GREEN — FINDING CONFIRMED**; reviewer **pass** (judged
  the finding doctrine-HONEST, not a masked search failure). **Codex NOT available
  — single-reviewer verdict.** **THE EQUILIBRIUM SYNTHESIS:** three levers converge
  — penalty (P-012/P-015, saturated: only vocal_belief gap 1.71<cap 2.0 flippable),
  reward (P-016, saturated at cap 4.0: only loop gap 3.43 reachable), base-value
  re-curation (P-017: density unflippable honestly) — **the judgment layer is at a
  DOCTRINE-HONEST EQUILIBRIUM; no honest further flip exists in the current
  dimension set.** The one open thread: is `subtractive_drop` itself over-valued? —
  a symmetric re-judgment, user-gated, un-signed-off, NOT staged. **P-017's guard
  commit `1b03ad3` is local-only** (dev branch on top of the `6c40e2b` PR #15
  merge), not pushed/merged at close.

- **Evidence-gated loop-deconstruct PROMOTION — the FIRST reward nudge — DONE via
  P-016** (`build-os/receipts/P-016-evidence-gated-loop-promotion.md`).
  **User-delegated PRODUCT-code change** (direction A "open the base-scoring
  decision space" + fork (i) "evidence-gated" + "keep skating"; the
  build-orchestrator routed). **This crosses the penalty-only line P-012/P-015
  held — the FIRST reward/promotion nudge.** **Two commits (≤2):**
  `b15b957` Commit-1 — `creative.py` (+88): `CREATIVE_PROMOTION_CAP = 4.0` (a
  SEPARATE constant from the ±2.0 penalty `CREATIVE_NUDGE_CAP`), a
  `_PROMOTION_TABLE` row (kind `loop_deconstruct`, evidence `foregrounded_loop`,
  `+35` excitement `= +5.0` raw clamped to exactly `+4.0`, verbatim reason), a
  `_foregrounded_loop` predicate reading the REAL wire (a `"foregrounded loop"`
  red_flag from `source_auditors` corroborated by `provenance` `high_risk`;
  getattr-defensive), and promotion application in `score_variant` (summed
  promotion overall-delta clamped to `+4.0`; `loop_promotion` reason appended to
  `score_nudges` on fire) + `tests/test_loop_promotion.py` (NEW, +233).
  **Green in isolation: 226 passed.** `a9f4e26` Commit-2 — the LIVE-WIRE:
  `pipeline.py` (+17/−3) relocates `analyze_provenance` + `audit_all` to just
  BEFORE `run_creative_engine` (a pure relocation — inputs already populated
  ~90 lines earlier) + two production-liveness tests (+70). **★ The P-009-style
  catch:** Commit-1's mechanism was INERT in production —
  `run_creative_engine` ran BEFORE `provenance`/`source_audits`, so the predicate
  always read empty evidence and the promotion NEVER fired in the real
  `analyze()` output; Commit-1's tests passed only because they RE-RAN the engine
  on the finished result. The orchestrator-in-chief caught it (the builder had
  mislabeled the ordering "by design"); Commit-2's live-wire fixed it, guarded by
  the two liveness tests that assert on the real `analyze()`
  `result.creative`/`result.governance` with NO re-run (FAIL pre-reorder, PASS
  after). **`_KIND_SCORES`, `CREATIVE_NUDGE_CAP`, the entire penalty table/path,
  and both existing predicates are byte-UNTOUCHED; `governance.py` has ZERO
  `provenance`/`source_audits` refs** → reorder SAFE BY CONSTRUCTION (backed
  by a 12-artifact byte-identical diff across all 3 seeded fixtures). **Behavior
  (qa-verified):** loop_deconstruct 81.9 → **85.9** (raw +5.0 clamped to
  exactly +4.0 = the cap binds, carries the `loop_promotion` line) >
  subtractive_drop 85.3 → **loop winner flips `loop_B` → `loop_A` by
  0.6** (governed winner also flips, no veto). **Load-bearing negative control:**
  no foregrounded-loop evidence → subtractive_drop wins (flip caused by the
  EVIDENCE). **Collateral:** ONLY the loop branch flips (chorus_lift/density still
  subtractive_drop — `subtractive_drop` now wins 2 branches, not 3, relieving
  anti_template; vocal_belief per P-015; depth unchanged); P-012/P-013/P-015 test
  files NOT edited and pass (58). **Proof:** suite **217 → 228 passed** (+11;
  0 failed/skipped/warnings, green under `-W error`); regression **68/68, 0
  critical, 0 warnings** (`loops_not_foregrounded` held); safety grep clean; UI
  N/A. **Reviewer pass** with a non-vacuity mutation check (emptying the promotion
  row → 5 promotion-dependent + 2 liveness tests RED, negative control GREEN;
  reverting ONLY the reorder → the 2 liveness tests RED) + a reward-creep
  watch-item; the `plan_depth` monkeypatch in the liveness test is a legitimate
  seam (real audit_all/analyze_provenance/run_creative_engine produce+consume the
  evidence, nothing faked). **Codex NOT available — single-reviewer
  verdict.** **P-016 is local-only** (commits `b15b957`, `a9f4e26` on the dev
  branch on top of `0f4e7e9`), not pushed/merged at close.

- **Make-the-nudge-decisive (masked-vocal near-tie) — DONE via P-015**
  (`build-os/receipts/P-015-decisive-masked-vocal-nudge.md`). **User-signed-off
  PRODUCT-code aesthetic change** (the user chose "Option 1 — Proceed, corrected",
  2026-06-30, after the orchestrator transparently corrected an arithmetic error —
  the old `−8` penalty only moves overall `−1.14`, insufficient to flip; the
  corrected mechanism strengthens to `−14`). The deliberate successor to P-012 and
  the resolution of the P-014 user-gated decision. **Single product commit
  `1756f61`** (product change + updated/new tests TOGETHER so Commit-1 is green in
  isolation, required because the change intentionally breaks old-behavior tests):
  `creative.py` `_NUDGE_TABLE` **row-0 only** — (1) exempt `intimacy_pass`
  (`kinds` `{width_bloom, vocal_ride, intimacy_pass}` → `{width_bloom,
  vocal_ride}` — an intimacy pass is the CORRECT response to a masked lead vocal,
  focused proximity not brute level/width), (2) strengthen `delta` `−8` → `−14`
  (`= −14/7 = −2.0` overall = EXACTLY `CREATIVE_NUDGE_CAP = 2.0`, unchanged, now
  binds `vocal_ride` too), plus an honest `−14` reason string, a doctrine comment,
  and a corrected stale clamp comment. `_KIND_SCORES`, the cap, row-1, the clamp,
  and both predicates are UNTOUCHED (verified by diff). **Behavior (qa-verified):**
  in the `vocal_belief` branch under a masked lead vocal, `vocal_ride` (vocal_A)
  82.9 → **80.9** (cap binds, overall_delta EXACTLY −2.0, carries the `−14`
  `score_nudges` line); `intimacy_pass` (vocal_B) 81.1 unchanged (exempt) →
  **winner FLIPS from vocal_ride to intimacy_pass** by 0.2. **Load-bearing negative
  control:** without `lead_masked`, vocal_ride wins (flip is caused by the masking
  evidence, not a base re-rank). **Bounded — no clear-ranking overturn:**
  `subtractive_drop` (85.3, penalty-immune) still wins `chorus_lift` / `density` /
  `loop` under `lead_masked` (gaps 3.4–4.2 ≫ 2×cap); ONLY the `vocal_belief`
  branch flips. **Tests (the binding guard — variant-scoring path golden-unguarded):**
  updated the ~existing P-012 cases in `tests/test_creative_nudges.py` (delta
  `−8`→`−14`, `intimacy_pass` now asserted EXEMPT, new reason, width_bloom worst
  case `−20` raw clamped to `−2.0`; added `test_intimacy_pass_exempt_from_lead_masked_nudge`
  + `test_vocal_ride_clamps_to_cap_under_lead_masked`) and ADDED
  `tests/test_decisive_nudge.py` (NEW, 8 tests: flip + load-bearing negative control
  + `test_only_vocal_belief_branch_flips_under_lead_masked` +
  `test_subtractive_drop_branch_does_not_flip_under_lead_masked`); no coverage
  deleted to turn red green. **Proof:** suite **207 → 217 passed** (0
  failed/skipped/warnings; changed files alone = 53 — `test_creative_nudges.py` 45,
  `test_decisive_nudge.py` 8); regression **68/68, 0 critical, 0 warnings** (doctrine
  golden held); Commit-1 green in isolation; safety grep clean (only a no-DAW
  docstring line); UI N/A. **Reviewer pass** — independently reproduced the
  arithmetic and ran a **mutation test confirming non-vacuity** (reverted both
  product edits → 5 binding tests went RED, the negative control correctly stayed
  GREEN → tests are load-bearing); confirmed scope discipline, no-overturn,
  evidence-line honesty, coverage not weakened. **Codex NOT available —
  single-reviewer verdict.** Non-blocking reviewer note: the mandated
  `Co-Authored-By: Claude Opus 4.8` trailer is a standing harness-required config
  tension, not a P-015 regression. **P-015 is local-only** (product commit `1756f61`
  on the dev branch on top of `0f4e7e9`), not pushed/merged at close.

- **Near-tie-creative-FLIP fixture — RESOLVED as a VERIFIED NEGATIVE FINDING via
  P-014** (`build-os/receipts/P-014-near-tie-creative-flip-fixture.md`). **No
  product code, no product/test commit.** The goal — prove the P-012 nudge is
  *decisive* and FLIPS the creative winner through `analyze()` on a genuine
  near-tie within the ±2.0 cap — is **structurally UNREACHABLE test-only** under
  the current `_KIND_SCORES` / `_NUDGE_TABLE`. The builder wrote ZERO code
  (honesty clause honored); qa adversarially tried to REFUTE it with THREE
  independent harnesses (builder inline-math + qa real-`score_variant` driver +
  a saturated worst-case `masking_report` with every classification the analyzer
  emits) — **all 0 flips** — and re-derived the arithmetic from source.
  Structural proof: `overall = mean(7 dims) − risk_penalty{low0/med6/high14}`,
  recomputed exactly as `score_variant`; base leaders are `generate_variants`
  literals keyed on `problem['id']` (fixture-invariant across 4 record sets);
  the **universal leader `subtractive_drop` (85.29) is penalty-immune** (in no
  `_NUDGE_TABLE` row), so `chorus_lift` / `density` / `loop` cannot reorder, and
  the **one sub-cap near-tie branch `vocal_belief`** (`vocal_ride` 82.86 vs
  `intimacy_pass` 81.14, gap 1.71) has BOTH hit by the identical row-0
  `lead_masked −8`, preserving the gap. **Headline reframing:** the P-012 nudge
  is a TRANSPARENCY/EVIDENCE layer — it moves the displayed governed
  `overall_score` and emits `score_nudges` but **can never reorder any branch**;
  P-013's option-(a) "cannot overturn a ranking" holds UNIVERSALLY (sharper than
  the P-012 "cannot overturn a *clear* ranking" framing). **Not a defect** — the
  nudge stays honest/bounded/penalty-only/evidence-tagged; decisive-when-close is
  latent until a user-gated curation change (see Deferred). **Suite 207 passed
  UNCHANGED; regression 68/68 held.** Commit-1-in-isolation N/A; `creative.py`
  unchanged since P-012 (`0df436c`); working tree clean; safety grep N/A.
  qa verdict **GREEN — FINDING CONFIRMED**; **Codex not available — single-reviewer
  verdict.** HEAD `596174d` (P-014 active-packet confirmation only; no product
  change). The P-014 harnesses live in scratchpad (not committed).

- **P-012 nudge proven on real data through `analyze()` (creative visibility
  fixture)** — **DONE via P-013**
  (`build-os/receipts/P-013-nudge-visibility-fixture.md`). **Tests-only** — one new
  file `tests/test_creative_nudge_visibility.py` (+154 lines, 5 tests); NO product
  code touched. Lifts the P-012 creative evidence-nudge from the unit level to the
  **live `pipeline.analyze()` production path**: on `dense_chorus_with_loops` the
  live masking analyzer emits a real `width_crowding` event, so the row-2 nudge
  (`vocal_belief −6`) fires on the `chorus_lift` `width_bloom` variant with no
  contrivance — overall_score (the governed-rank value) 75.7→**74.9** (movement
  −0.857, inside the ±2.0 cap), yet the winner stays `chorus_lift_B` (base gap ~9.6
  > 2× the cap). Builder chose **option (a)** — the cap binds, the winner does NOT
  flip — the documented latent-but-armed posture, now proven end-to-end. **Closes
  the golden-unguarded gap** on the variant-scoring path. Single tests-only commit
  `172cfd0`; suite 202→**207**; regression **68/68** held; Commit-1 green in
  isolation; safety grep clean (only hit a no-DAW docstring). Reviewer **pass** —
  independent negative control (disarmed `_apply_nudges` → 3 of 5 tests fail, so the
  assertions are load-bearing), independently recomputed the numbers, confirmed the
  Fixture #2 re-scope sound; **Codex not available — single-reviewer verdict.**
  Fixture #2 (taste-flip through `analyze()`) re-scoped to a POSITIVE alignment
  finding (taste structurally cannot flip a governed winner on curated data — see
  Deferred). P-013 is the **first post-merge packet** (PR #13 merged at `0f4e7e9`).
- **PR #13 (P-001…P-012 + canonical-alignment audit) MERGED to default** — merge
  commit `0f4e7e9` on `claude/dreamy-turing-z0oxll`. The whole P-001…P-012 line
  (including the option-B creative-scoring change) plus the AUDIT-2026-06-29
  canonical-alignment audit (verdict ALIGNED) is now on the default branch. The dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` was freshly restarted on top of
  the merge for post-merge work (P-013 onward).

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

- **Variant-scoring path is golden-unguarded (reinforced by P-012, P-015):**
  `regression.py` reads `doctrine_score`, never `score_variant`, so the 68/68
  golden cannot catch a `creative.py`/`score_variant` change. **Unit + visibility
  + flip tests are the binding guard** for any creative-scoring touch (P-012's
  `tests/test_creative_nudges.py` safety-invariant suite, P-013's
  `tests/test_creative_nudge_visibility.py` driving the live `analyze()` path, and
  P-015's `tests/test_decisive_nudge.py` pinning the masked-vocal flip). Treat any
  future creative-scoring change as test-binding, not golden-binding. Watch-item:
  P-015's flip margin is thin (0.2) but fully pinned — a future re-curation would
  surface as a RED test, not a silent re-rank.
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

- **P-017 closed with NO product-code change (verified negative finding).** The
  ONLY committed change is the tests-only characterization guard
  (`tests/test_density_recuration.py`, commit `1b03ad3`) plus the `fecc4e5`
  active-packet confirmation and this build-os close. All sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge.
  **`1b03ad3` is local-only at this close.** Any push of it — and any subsequent
  PR / merge into the protected default — needs the user's explicit go. No push /
  merge / deploy / secret action taken in this close.
- **P-016 is now MERGED to default via PR #15** (merge commit `6c40e2b`, the current
  default-branch tip and the base for P-017). The earlier P-016 dev commits
  (`b15b957`, `a9f4e26`) are landed on default via that merge. That boundary is
  resolved. (Earlier stale note said "P-016 local-only on `0f4e7e9`" — superseded.)
- **P-014 closed with NO product/test commit (verified negative finding).** Only
  the build-os memory advance (this close) and the prior `596174d` active-packet
  confirmation sit on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1` on
  top of the `0f4e7e9` merge. Nothing product-side to push. Any push, and any
  subsequent PR / merge into the protected default, needs the user's explicit go.
  No push / merge / deploy / secret action taken in this close.
- **PR #13 is MERGED** (merge commit `0f4e7e9`) — the earlier local-only product
  commits (P-005…P-012: `0df436c`, `effccd0`, `ea9bebf`, `dc61f20`, `9ebd4ee`,
  `27bfebf`, etc.) are now landed on the default branch via that merge. That
  boundary is resolved.
- **P-013's tests-only product commit `172cfd0` is local-only as of this close**
  (this archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9` merge. Any push
  of it — and any subsequent PR / merge into the protected default — needs the
  user's explicit go. No push / merge / deploy / secret action taken in this close.
- **P-015's product commit `1756f61` is local-only as of this close** (this
  archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9` merge — the
  user-signed-off masked-vocal-nudge change. The orchestrator pushes the dev branch
  separately. Any push of it — and any subsequent PR / merge into the protected
  default — needs the user's explicit go. No push / merge / deploy / secret action
  taken in this close.

- **P-019's product commits `b7572b7`, `de5679f` are local-only as of this close**
  (this archivist close did not push). They sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge
  base — the additive `record_mix_pass` cowork command (byte-identical by default).
  The build-os-only close commit is separate. Any push of the product commits — and
  any subsequent PR / merge into the protected default — needs the user's explicit
  go. No push / merge / deploy / secret action taken in this close.

---
_Append-only working notes. Last advanced on P-019 close (2026-07-01)._
