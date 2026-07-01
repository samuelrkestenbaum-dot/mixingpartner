# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** Logic Mix OS — a local-first, deterministic mix-decision
  system that turns exported Logic Pro stems + a `project_manifest.json` into a
  section-aware, Logic-native **mix plan** (Roy Halee / Phil Ramone judgment
  layer). Not an auto-mixer, preset generator, or mastering tool. All product
  code lives under `logic-mix-os/`.
- **Primary branch / base:** default branch `claude/dreamy-turing-z0oxll`;
  active dev branch `claude/logic-mix-os-hardening-12-7hbeh1`. **P-016 is now
  MERGED to default via PR #15 — merge commit `6c40e2b`, which is the current
  default-branch tip and the base for P-017** (confirmed: `6c40e2b` is an ancestor
  of the dev HEAD, and is exactly the commit before P-017's active-packet
  confirmation). (Earlier, **PR #13** — P-001…P-012 + the canonical-alignment
  audit — merged at `0f4e7e9`; the whole-branch `git merge-base` with default is
  the older shared ancestor `694d19d`.) On top of the `6c40e2b` base the dev branch
  carries P-013 (`172cfd0`, tests-only), **P-015 (`1756f61`, product)**,
  **P-016 (`b15b957` + `a9f4e26`, product — now also landed on default via PR #15)**,
  **P-017 (`1b03ad3`, tests-only guard — verified finding, no product change)**,
  **P-018 (`736fa8b` + `6134d27`, product — the first confirmed-outcome
  learning signal, opt-in / byte-identical by default)**, and
  **P-019 (`b7572b7` + `de5679f`, product — `record_mix_pass` closes the learning
  loop INSIDE the cowork surface, additive / byte-identical by default)**, and
  **P-020 (`942a68a`, product — `describe_session` makes the cowork surface
  self-describing as an ordered, phase-grouped session flow; additive / read-only /
  byte-identical to every existing command)**, and
  **P-021 (`dce156b`, TESTS-ONLY — the MILESTONE: an executable proof that an
  agent driving ONLY the cowork surface completes a full plan-only mixing session
  AND closes the learning loop; no product change)**; the local-only-at-close
  commits (P-013, P-015, P-017's guard, P-018, P-019, P-020, P-021) are not pushed.
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-07-01):** suite **277 passed** (0 failed /
  skipped / warnings; green even under `-W error`); regression **68/68** (0
  critical / 0 warnings). (Prior baseline was 269; P-021 added +8 — tests-only.)

## Where we are

- **★★ MILESTONE — P-021 PROVES THE COWORK SURFACE IS AGENT-DRIVABLE END-TO-END
  (arc step 3 of 5; the step that PROVES it).** The canonical target — Logic Mix
  OS as a tool Claude Cowork can drive END-TO-END in a Logic Pro mixing session
  (plan-only v1) — is now essentially **MET AT THE DECISION-SYSTEM LEVEL.** P-021
  (TESTS-ONLY) drives a full mixing session THROUGH the cowork surface only
  (`build_context` + `run_command`), in `describe_session`'s canonical order, and
  the learning loop CLOSES within the surface. No product change; no honesty-clause
  gap found — every phase's essential command was reachable and the loop closed
  across the full session.
  - **The driven spine (8 phases, via `run_command`, NOT bypassing to
    `analyze()` / `record_pass`):** intake → `intake_project`, classify →
    `classify_tracks`, diagnose → `detect_masking`, plan → `generate_mix_plan`,
    checklist → `render_logic_checklist`, validate → `validate_mix_pass`,
    record-outcome → `record_mix_pass` (LIVE), next-pass → `suggest_next_pass`.
    Each output JSON-serializable + shape-asserted; the chain never drops out of
    the surface.
  - **The loop CLOSES (milestone assertion — load-bearing + non-tautological):**
    `record_mix_pass(..., reverted=True)` on the LIVE channel → a FRESH
    `build_context(memory_dir=...)` → `suggest_next_pass` surfaces the confirmed
    "Revert last pass" (evidence contains "confirm"), NO hand re-run. **Proven
    load-bearing** (qa AND reviewer independently — dropping `reverted` / routing
    off the live channel → the assertion FAILS; reviewer via monkeypatch) and
    **non-tautological** (the identical score-IMPROVED sequence with
    `reverted=False` surfaces NO revert).
  - **Live-vs-dead pinned as an EXECUTABLE fact (resolves the carried P-020 clarity
    nudge):** `write_mix_decision` (DEAD ledger — writes only `decision_ledger.json`,
    runtime-verified) does NOT change next-pass; `record_mix_pass` (LIVE history)
    does. Only `record_mix_pass` closes the loop.
  - **Honest skips (none an essential linear phase):** `compare_to_reference`
    (needs a reference bounce → `{"note": "no reference supplied"}`),
    `override_track_identity` (param-heavy / mutating), `build_missing_tool` /
    `run_creative_engine` / `describe_session` (auxiliary / off-axis).
  - **PRECISION (do NOT overstate):** the coverage-honesty test
    (`test_walkthrough_covers_the_registry_honestly`) guards PHASE-COMPLETENESS
    (every `describe_session` phase has a driven essential command belonging to it)
    + test-1's exact 8-phase order pin — it does NOT assert a full
    `driven ∪ skipped == 34` registry partition (it references 13 of 34). The full
    34-command exact-cover partition is guarded SEPARATELY by P-020's
    `test_cowork_session_flow.py` (31 phases + 3 auxiliary = 34). Together the two
    files tell the truth about registry coverage.
  - **Single commit `dce156b` (TESTS-ONLY):** adds exactly ONE file
    `tests/test_cowork_session_walkthrough.py` (8 tests, +372); no product/runtime
    file changed, no existing test edited. Suite **269 → 277 passed** (+8; 0
    failed/skipped/warnings, green under `-W error`); regression **68/68, 0
    critical, 0 warnings** held; Commit-1 green in isolation (277; single commit =
    tip); determinism confirmed (two contexts → byte-identical plan/next-pass);
    safety grep clean; UI N/A. qa **GREEN**; reviewer **pass** (empirically
    re-verified load-bearing via monkeypatch; genuine drive, not a bypass; honest
    skips). **Codex NOT available — single-reviewer verdict.** **P-021 local-only**
    (commit `dce156b` on the dev branch on top of the `6c40e2b` PR #15 base), not
    pushed/merged.
  - **★ SYNTHESIS (the strategic headline):** the canonical target is essentially
    MET at the decision-system level — an agent using ONLY the cowork surface can
    drive the complete plan-only session (intake → … → next-pass) AND learn from
    outcomes (record → loop closes), entirely within the surface, proven
    executably. What remains is genuinely only **transport packaging** — **P-023**
    (MCP server vs documented raw-CLI contract), a USER-GATED architecture
    decision. **P-022 stays OPTIONAL / UNNEEDED** — the honesty clause surfaced no
    real gap requiring it.

- **★ THE ARC ADVANCES — P-020 MAKES THE COWORK SURFACE SELF-DESCRIBING AS AN
  ORDERED, PHASE-GROUPED SESSION FLOW (arc step 2 of 5).** `list_commands` is a flat
  alphabetized catalog; an agent could not read the canonical end-to-end SEQUENCE
  from it. **P-020 adds a pure `_SESSION_FLOW` structure + a read-only
  `describe_session` command (registry 33 → 34)** that returns the SAME registry as
  `{"phases": [...ordered...], "auxiliary": [...]}` in the canonical order **intake
  → classify → diagnose → plan → checklist → validate → record-outcome →
  next-pass**. **31 commands** map onto the 8 linear phases; **3 are honestly
  `auxiliary`** (off the linear axis): `run_creative_engine` (parallel creative
  exploration), `build_missing_tool` (meta tooling-gap helper), `describe_session`
  (self-describing). Honesty clause honored — no fabricated flow; `suggest_next_pass`
  placed ONCE (in `next-pass`), not double-listed.
  - **Completeness INVARIANT (the load-bearing guard):** every `COMMANDS` key
    appears EXACTLY ONCE across phases + auxiliary (exact cover — no orphan, no
    duplicate), keeping the flow honest as commands are added. Proven load-bearing
    (orphan/duplicate → the test fails); qa independently verified the partition
    **31 + 3 = 34 = len(COMMANDS)**.
  - **Additive / read-only:** `list_commands` / `run_command` / every existing
    handler are BYTE-UNCHANGED; `describe_session` is deterministic (byte-identical
    across calls) and DEEP-COPIES its output so callers can't mutate the module
    structure. Single commit `942a68a` (purely additive `cowork.py` +100, new
    `tests/test_cowork_session_flow.py` 10 tests, the one intended `test_cowork.py`
    count assertion 33→34). Suite **259 → 269** (+10; green under `-W error`);
    regression **68/68, 0 critical**; Commit-1 green in isolation (269; single
    commit = tip). qa **GREEN**; reviewer **pass** (verified every command placement
    against its real handler; two defensible judgment calls — `score_mix` and
    `compare_to_reference` in `plan`). **Codex NOT available — single-reviewer
    verdict.** **Reviewer non-blocking flag carried to P-021:** `write_mix_decision`
    (dead ledger) and `record_mix_pass` (live history) both sit under
    `record-outcome` but the dead/live distinction is NOT surfaced in
    `describe_session`'s output — add a one-line clarity nudge in the P-021
    walkthrough. **P-020 local-only** (commit `942a68a` on the dev branch on top of
    the `6c40e2b` PR #15 base), not pushed/merged.

- **★ THE CANONICAL TARGET HAS AN ARC — P-019 LANDS ITS FIRST STEP: THE LEARNING
  LOOP IS NOW CLOSEABLE INSIDE THE COWORK SURFACE (read/write SYMMETRIC).** The
  canonical target is Logic Mix OS as a tool Claude Cowork can drive END-TO-END in
  a Logic Pro mixing session (plan-only v1; the agent/human executes). The
  orchestrator opened an arc to that state — **P-019 → P-023** — and **P-019 is the
  FIRST step, now DONE.** Until now the cowork surface was coherent for the FORWARD
  half (intake → classify → diagnose → plan → checklist → validate →
  `suggest_next_pass`) and the READ side of the learning loop was live through
  cowork (P-009), but the registry had **NO command to RECORD a pass outcome** —
  the P-018 confirmed-outcome signal was reachable only via the SEPARATE
  `memory-record` CLI verb. P-019 adds a **`record_mix_pass`** command (registry
  **32 → 33**) whose handler records a pass on the LIVE history channel
  (`ctx["memory"].record_pass(name, ctx["result"], reverted=...)` →
  `mix_pass_history.json`), passing through the P-018 `reverted` ground-truth flag
  (opt-in, default False), returning the record JSON — with a clean
  `{"error": "no memory_dir configured"}` when no memory dir (mirrors
  `_write_mix_decision`). **So an agent driving through cowork can now RECORD an
  outcome and see `suggest_next_pass` change WITHOUT leaving the surface** — the
  read/write cowork surface is symmetric. Routes to the LIVE channel, NOT the dead
  decision ledger.
  - **One surface finding, resolved minimally (NOT a wall):** the cowork
    `--params '{...}'` path unpacks user JSON into `run_command(name, ctx, **params)`,
    so a handler param named `name` collided with the dispatcher's positional
    `name`. Fixed by making the dispatcher's `name`/`ctx` **positional-only**
    (`run_command(name, ctx, /, **params)`) — behavior-preserving: a repo-wide grep
    found ZERO callers passing `name=`/`ctx=` by keyword (the sole product caller
    `cli.py:237` passes positionally). Param-naming, not a missing wire.
  - **LIVENESS proven load-bearing (the P-016/P-018 lesson honored):**
    `test_loop_closes_through_cowork_no_rerun` records a confirmed revert via
    `run_command("record_mix_pass", ...)` on a score-IMPROVED override case, then a
    FRESH `build_context(memory_dir=...)` → `run_command("suggest_next_pass")`
    surfaces the confirmed "Revert last pass" — **NO hand re-run.** Both qa and
    reviewer INDEPENDENTLY broke the wiring (handler off the live channel) → the
    test FAILS; restored → PASSES. The loop closes THROUGH the cowork surface.
  - **Routes to the live channel (runtime probe):** only `mix_pass_history.json`
    created, never `decision_ledger.json`. **Byte-identical default:**
    date-neutralised canonical JSON equal to the standalone `memory-record`.
  - Two commits (≤2): `b7572b7` Commit-1 (handler + registry row + positional-only
    + unit tests; green in isolation = 257) + `de5679f` Commit-2 (no-re-run
    liveness guard). Scope: only 3 files (`cowork.py` additive,
    `test_cowork.py` count assertion 32→33, new `tests/test_cowork_record.py`);
    `memory.py`/`cli.py`/`pipeline.py`/ledger/creative/governance UNTOUCHED. qa
    **GREEN**; reviewer **pass** (handler correct + routes live [verified by
    breaking it]; positional-only safe/minimal; loop closes through cowork;
    non-tautological override case). **Codex NOT available — single-reviewer
    verdict.**

- **★ THE OUTCOME→LEARNING AXIS IS NOW OPEN — P-018 SHIPS THE FIRST
  CONFIRMED-OUTCOME SIGNAL IN THE LEARNING LOOP (a PIVOT off the complete
  judgment-tuning path onto the feedback frontier; user said "Yes").** Until
  now every loop signal was score-INFERRED (`record_pass` guesses "that
  regressed, maybe revert" from score deltas). P-018 adds a CONFIRMED one. An
  opt-in `memory-record --reverted` records a confirmed operator revert on a
  pass (`record_pass(..., reverted=True)` → `mix_pass_history.json`); the live
  `_apply_history` consumer (already threaded to real `analyze(--memory-dir)`
  via P-009) then, on a confirmed revert, DEMOTES the recommended-then-reverted
  moves and surfaces exactly ONE confirmed "Revert last pass" item at priority
  95 — **regardless of the score-delta `got_worse` inference (OVERRIDE)**, with
  an early-return that prevents double-up with the score-inferred revert. Distinct
  honest evidence line ("…because the operator confirmed reverting the last
  pass" — contains "confirm", vs the score-inferred "recorded revert
  candidate(s): …").
  - **OVERRIDE semantics (chosen by the orchestrator-in-chief; user may redirect
    at the merge gate):** a confirmed operator revert is GROUND TRUTH and takes
    precedence over the score-inferred guess when they disagree — the
    doctrine-honest, operator-serving choice (a confirmed action outranks a
    heuristic proxy).
  - **Why THIS seam (the dead-ledger finding):** the decision LEDGER
    (`add_decision` → `decision_ledger.json`) has ZERO analyze-path consumers
    (`mem.ledger()` is display-only at `cli.py:315`), so a producer for any
    reserved ledger event would be INERT — the hollow trap. The ONLY reachable
    LIVE seam was the history axis (`record_pass` → `_apply_history`), which is
    why the confirmed revert lands there.
  - **Opt-in / byte-identical by default:** no `--reverted` → the `reverted` key
    is not written and `next_pass` is unchanged vs today.
  - **LIVENESS proven load-bearing (the P-016 lesson honored):** the no-re-run
    liveness test asserts on real `analyze(memory_dir=...)` `next_pass` and FAILS
    with the pre-P-018 `_apply_history` (confirmed revert doesn't reach analyze
    output = would be inert) and PASSES at tip — NOT inert. **Override
    non-vacuous:** with an IMPROVED score delta (`got_worse` empty) but
    `reverted=True`, the confirmed item still surfaces at rank 0 and the reverted
    move is demoted — proving override, not an echo of the score signal.
  - Two commits (≤2): `736fa8b` Commit-1 (`record_pass` field + `_apply_history`
    override + 9 unit tests; green in isolation = 249) + `6134d27` Commit-2
    (`--reverted` CLI wire + 4 no-re-run liveness/CLI tests). qa **GREEN**
    (mutation-verified liveness + non-vacuous override); reviewer **pass**
    (override bounded/deterministic; early-return skips only the score-inferred
    revert; demotes exactly the reverted pass's recommended moves). **Codex NOT
    available — single-reviewer verdict.**

- **★ THE JUDGMENT LAYER IS AT A DOCTRINE-HONEST EQUILIBRIUM — P-017 (the FIRST
  base-value re-curation attempt) CLOSED AS A VERIFIED NEGATIVE FINDING.** The user
  chose "A": try a minimal, doctrine-honest re-curation of
  `_KIND_SCORES["depth_cleanup"]` so the depth/hierarchy move wins the `density`
  branch over `subtractive_drop` — with a hard honesty constraint (never inflate a
  dim to force a win). **FINDING: an honest re-curation CANNOT flip `density` —
  arithmetically forced by the DOCTRINE, verified adversarially.** `_KIND_SCORES`
  is **LEFT UNTOUCHED (no product change)**; the honesty clause held (P-014
  discipline: honesty beats the flip). The builder committed ONLY a 12-test
  characterization guard.
  - **The forced arithmetic:** `overall = mean(7 dims) − risk_penalty`.
    `depth_cleanup` base overall **81.14** (dim sum 568) vs `subtractive_drop`
    **85.29** (dim sum 597, low risk) → gap **4.14**. The one doctrine-defensible
    under-valuation is `contrast` (dc 72 vs sd 88): `contrast → 88` = **83.43**
    (short 1.86); `contrast → 100` (impossible ceiling) = **85.14** — STILL below
    85.29. A FULL honest re-curation (contrast→88, technical→85, ramone→86,
    taste→86; halee stays 90=max, vocal_belief stays 86; **excitement LOCKED at
    66**) reaches only **83.86** (short 1.43). The entire residual deficit lives in
    `excitement` (66 vs 78), OFF-LIMITS to inflate (subtle depth work is honestly
    un-flashy). The only flips require inflating `excitement` or re-labeling a depth
    pass as vocal-forward — both dishonest.
  - **The committed guard (load-bearing, non-tautological):**
    `tests/test_density_recuration.py` (12 tests, +183, commit `1b03ad3`) pins the
    5-branch winner table UNCHANGED on the real `analyze()` path + the honest-ceiling
    arithmetic + `_KIND_SCORES` untouched. Proven load-bearing: injecting an inflated
    `depth_cleanup` (contrast=88+excitement=90, or all dims=100) makes the density
    guard FAIL (density flips to `density_A`) — it genuinely catches an
    accidental/dishonest density flip. Committing executable arithmetic is defensible
    (unlike P-014's no-commit finding) because the finding IS arithmetic and the
    variant-scoring path is golden-unguarded.
  - **THREE LEVERS CONVERGE (the equilibrium):** penalty (P-012/P-015) — saturated,
    only the `vocal_belief` near-tie (gap 1.71<cap 2.0) flippable, P-015 made it
    decisive; reward/promotion (P-016) — saturated at cap 4.0, only `loop` (gap 3.43)
    cleanly reachable, P-016 made it decisive (density gap 4.14 unreachable +
    circular gate; drum_room_bloom hollow); base-value re-curation (P-017) — honest
    re-curation cannot flip density either. **Conclusion: subtractive_drop's default
    dominance is legitimate; the masked-vocal and foregrounded-loop overrides are the
    only doctrinally-warranted flips; there is NO honest further flip move inside the
    current dimension set.** The one remaining honest thread is a SYMMETRIC
    re-judgment (is subtractive_drop itself slightly over-valued?) — user-gated,
    un-signed-off, NOT staged.

- **THE PENALTY-ONLY LINE IS CROSSED — P-016 SHIPS THE FIRST REWARD/PROMOTION
  NUDGE (loop branch), EVIDENCE-GATED AND NOW LIVE IN PRODUCTION (MERGED via PR
  #15, merge commit `6c40e2b`).** User-delegated (direction A "open the base-scoring
  decision space" + fork (i) "evidence-gated" + "keep skating"; the
  build-orchestrator routed it). When the analyzers flag a genuinely foregrounded /
  dominating loop — the REAL `source_auditors` `"foregrounded loop"` red_flag
  corroborated by `provenance` `high_risk` — a bounded promotion
  (`CREATIVE_PROMOTION_CAP = 4.0`, a SEPARATE constant from the ±2.0 penalty
  `CREATIVE_NUDGE_CAP`) lifts `loop_deconstruct` past `subtractive_drop` to win the
  `loop` branch: `loop_deconstruct` 81.9 → **85.9** (raw +5.0 clamped to exactly
  +4.0 = the cap binds) > `subtractive_drop` 85.3 → loop winner flips `loop_B` →
  `loop_A` by 0.6 (governed winner also flips, no veto). **No such evidence →
  `subtractive_drop` stays the default.** Grounded in the system's OWN
  `anti_template` doctrine ("vary the move per problem") + `loops_not_foregrounded`
  + `source_material_respected` + the kill-switch "never allow a stock loop to
  dominate the song identity." Bounded, transparent (emits a `loop_promotion`
  `score_nudges` line), pure/deterministic, layered on an UNTOUCHED `_KIND_SCORES`
  and an UNTOUCHED penalty path.
  - **★ THE P-009-STYLE CATCH (record prominently):** Commit-1's mechanism was
    **INERT in production** — the orchestrator-in-chief caught it before close. In
    `pipeline.analyze()`, `run_creative_engine` ran BEFORE `provenance` /
    `source_audits` were populated, so the promotion predicate always read empty
    evidence and NEVER fired in the real `analyze()` output; Commit-1's tests
    passed only because they RE-RAN `run_creative_engine` on the finished result.
    **Commit-2 fixed it** with a minimal live-wire: relocated `analyze_provenance`
    + `audit_all` to just BEFORE `run_creative_engine` (a pure relocation — their
    inputs are populated ~90 lines earlier), plus two production-liveness tests
    that assert on the real `analyze()` `result.creative` / `result.governance`
    WITHOUT any re-run (they FAIL pre-reorder, PASS after). The promotion is now
    genuinely live.
  - **Reorder SAFE BY CONSTRUCTION:** `governance.py` has ZERO references to
    `provenance` / `source_audits`; `creative.py`'s ONLY reads are inside the new
    `_foregrounded_loop` predicate → nothing but the promotion consumes those
    attrs in the reordered region → default output cannot change. Backed by a
    12-artifact byte-identical diff across all 3 seeded fixtures.

- **THE P-012 NUDGE IS NO LONGER TRANSPARENCY-ONLY — P-015 MAKES IT DECISIVE ON
  THE MASKED-VOCAL NEAR-TIE (USER-SIGNED-OFF AESTHETIC CHANGE).** P-014 proved a
  near-tie creative FLIP was structurally UNREACHABLE test-only **under the
  then-current curation**. The user chose **"Option 1 — Proceed, corrected"**
  (2026-06-30). **P-015** edits `creative.py` `_NUDGE_TABLE` row-0 (`lead_masked`)
  ONLY: **(1) exempt `intimacy_pass`** (an intimacy pass is the CORRECT response to
  a masked lead vocal) and **(2) strengthen the penalty `−8` → `−14`** (`= −2.0`
  overall = EXACTLY the existing `CREATIVE_NUDGE_CAP = 2.0`, UNCHANGED). Net: in
  the `vocal_belief` branch under a masked lead vocal, `vocal_ride` (vocal_A)
  82.9 → **80.9** (cap binds), `intimacy_pass` (vocal_B) 81.1 unchanged (exempt) →
  **winner FLIPS `vocal_ride` → `intimacy_pass`** by 0.2. **Bounded — cannot
  overturn a clear ranking** (`subtractive_drop` still wins its branches).

- **THE P-012 CREATIVE NUDGE IS PROVEN ON REAL DATA THROUGH `analyze()`.** With
  **P-013** (tests-only), the bounded penalty-only evidence-nudge layer is lifted
  from the unit level to the **live `pipeline.analyze()` production path** — on
  `dense_chorus_with_loops` the row-1 nudge (`vocal_belief −6`) fires on the
  `chorus_lift` `width_bloom` variant, lowering `overall_score` 75.7 → 74.9 (inside
  the ±2.0 cap), winner unchanged (option-(a)). The P-013 visibility tests still
  pass unchanged after P-015, P-016, and P-017.

- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED (option B, P-012), MERGED
  (PR #13), MADE DECISIVE (P-015), EXTENDED TO REWARD (P-016, MERGED PR #15), AND
  ITS BASE-VALUE LEVER PROBED (P-017 — no honest flip).** The bounded, transparent,
  capped evidence-nudge layer ON TOP of the curated `_KIND_SCORES` (values
  UNCHANGED) is live on default via PR #13; P-015 tunes row-0 to be decisive on the
  masked-vocal near-tie; **P-016 crosses into REWARD with the first promotion row
  (loop branch), now on default via PR #15;** **P-017 confirmed the base values
  themselves are doctrine-honest (no flip of density is honestly reachable).** The
  judgment layer is now at equilibrium.

- **THE ALBUM-MEANS TRUTH IS SINGLE-SOURCED.** Via **P-011**, the album means live
  in exactly ONE place: `album.py::analyze_album` additively emits per-song
  `brightness_delta` / `lufs_delta` and `cli.py::_run_album` consumes them; the
  duplicate `statistics.mean` recompute is gone. The `album` report stays
  value-identical.
- **MILESTONE (still standing) — THE CROSS-SONG COHERENCE AXIS IS OPEN.** Via
  **P-010**, a song's plan (through the `album` command) reflects its album
  siblings: album-aware per-song guidance, opt-in / bounded / evidence-tagged. **The
  product is no longer strictly song-isolated.**
- **MILESTONE (still standing) — THE LEARNING LOOP IS REAL IN PRODUCTION.** The
  full arc **P-007 (consumer) → P-008 (outcome) → P-009 (live wire)** is closed
  end-to-end: a real `cowork --memory-dir` run both **learns** and **personalizes**.
- **POSITIVE ALIGNMENT FINDING (from P-013) — taste cannot flip a governed winner
  on curated data, BY DESIGN.** `_apply_taste` moves only the `taste_triangle`
  identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and is
  align-vetoed before it can reorder a truth-ranked winner. The reachable taste
  claim is proven on real data by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`.
- **Last closed packet:** **P-021** — verified end-to-end agent walkthrough
  through the cowork surface (TESTS-ONLY) — **the MILESTONE** (THIRD step of the arc
  P-019→P-023; the step that PROVES the Cowork-usable end-to-end state). Drives a
  full plan-only mixing session THROUGH the cowork surface only (`build_context` +
  `run_command`), in `describe_session`'s canonical order, and closes the learning
  loop within the surface. **The driven spine (8 phases, via `run_command`, NOT
  bypassing to `analyze()`/`record_pass`):** intake→`intake_project`,
  classify→`classify_tracks`, diagnose→`detect_masking`, plan→`generate_mix_plan`,
  checklist→`render_logic_checklist`, validate→`validate_mix_pass`,
  record-outcome→`record_mix_pass` (LIVE), next-pass→`suggest_next_pass` (each
  JSON-serializable + shape-asserted). **The loop CLOSES (milestone assertion):**
  `record_mix_pass(..., reverted=True)` (LIVE) → FRESH `build_context(memory_dir=...)`
  → `suggest_next_pass` surfaces the confirmed "Revert last pass" (evidence contains
  "confirm"), NO hand re-run — **proven load-bearing** (qa AND reviewer independently;
  reviewer via monkeypatch) and **non-tautological** (identical score-IMPROVED
  sequence with `reverted=False` → NO revert). **Live-vs-dead pinned executably**
  (resolves the carried P-020 nudge): `write_mix_decision` (DEAD ledger) does NOT
  change next-pass; `record_mix_pass` (LIVE history) does. **Honest skips**
  (`compare_to_reference` needs a reference, `override_track_identity`,
  `build_missing_tool`/`run_creative_engine`/`describe_session`) — none an essential
  phase. **PRECISION:** the coverage-honesty test guards PHASE-COMPLETENESS + the
  8-phase order (references 13 of 34), NOT a full 34-registry partition — P-020's
  `test_cowork_session_flow.py` holds the 34-command exact cover (31+3=34); together
  they tell the truth about coverage. **Single commit `dce156b`** (TESTS-ONLY; one
  new file `tests/test_cowork_session_walkthrough.py`, 8 tests, +372; no
  product/runtime file changed, no existing test edited; single commit = tip, green
  in isolation = 277). Suite **269 → 277 passed** (+8; 0 failed/skipped/warnings,
  green under `-W error`); regression **68/68, 0 critical, 0 warnings** held;
  determinism confirmed; safety grep clean; UI N/A. qa **GREEN**; reviewer **pass**
  (empirically re-verified load-bearing via monkeypatch; genuine drive; honest skips).
  **Codex NOT available — single-reviewer verdict.** **★ SYNTHESIS:** the canonical
  target is essentially MET at the decision-system level; only P-023 transport
  packaging (USER-GATED) remains; **P-022 optional/unneeded (no gap surfaced).**
  **P-021 is local-only** (commit `dce156b` on the dev branch on top of the `6c40e2b`
  PR #15 base), not pushed/merged. Receipt:
  `build-os/receipts/P-021-verified-end-to-end-cowork-walkthrough.md`.
- **P-020 (prior close)** — `describe_session` session-flow
  discoverability (SECOND step of the arc P-019→P-023 to the Cowork-usable
  end-to-end state). Adds a pure `_SESSION_FLOW` structure + a read-only
  `describe_session` command to the cowork registry (count **33 → 34**) that returns
  the SAME registry as an ORDERED, phase-grouped session flow
  `{"phases": [...], "auxiliary": [...]}` in the canonical order **intake → classify
  → diagnose → plan → checklist → validate → record-outcome → next-pass**. **31
  commands** map onto the 8 linear phases; **3 are honestly `auxiliary`** (off the
  linear axis: `run_creative_engine`, `build_missing_tool`, `describe_session`).
  Honesty clause honored (no fabricated flow; `suggest_next_pass` placed ONCE).
  **Completeness INVARIANT (load-bearing):** every `COMMANDS` key covered EXACTLY
  ONCE across phases + auxiliary (exact cover; orphan/duplicate → test fails); qa
  independently verified **31 + 3 = 34 = len(COMMANDS)**. Additive / read-only:
  `list_commands` / `run_command` / every existing handler byte-unchanged;
  `describe_session` deterministic + deep-copies its output. Single commit
  **`942a68a`** (purely additive `cowork.py`; new `tests/test_cowork_session_flow.py`,
  10 tests; the one intended `test_cowork.py` count assertion 33→34; single commit =
  tip, green in isolation = 269). Suite **259 → 269 passed** (+10; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held (additive read-only → goldens untouched); registry 34, no stale
  33; safety grep clean; UI N/A; existing cowork + P-008/P-009/P-018/P-019 tests
  green. qa **GREEN**; reviewer **pass** (verified every command placement against
  its real handler; two defensible judgment calls — `score_mix` and
  `compare_to_reference` in `plan`). **Codex NOT available — single-reviewer
  verdict.** **Reviewer non-blocking flag carried to P-021:** the live-vs-dead-ledger
  distinction (`record_mix_pass` live history vs `write_mix_decision` dead ledger,
  both under `record-outcome`) is NOT surfaced in `describe_session`'s output — add a
  one-line clarity nudge in the P-021 walkthrough. **P-020 is local-only** (commit
  `942a68a` on the dev branch on top of the `6c40e2b` PR #15 merge base), not
  pushed/merged at close. Receipt:
  `build-os/receipts/P-020-describe-session-flow-discoverability.md`.
- **P-019 (prior close)** — `record_mix_pass` closes the learning loop INSIDE the
  cowork surface (FIRST step of the arc). Adds a `record_mix_pass` command (registry
  32→33) whose handler records a pass on the LIVE history channel
  (`record_pass(name, result, reverted=...)` → `mix_pass_history.json`), so an agent
  can close the loop (record → see `suggest_next_pass` change) without leaving the
  surface. Surface finding resolved minimally (dispatcher `name`/`ctx` positional-only;
  behavior-preserving, zero keyword callers). Two commits `b7572b7` (Commit-1: green
  in isolation = 257) + `de5679f` (Commit-2: no-re-run liveness guard). Suite **253 →
  259 passed** (+6); regression **68/68, 0 critical** held; byte-identical default;
  liveness proven load-bearing; routes to the live channel (only
  `mix_pass_history.json`, never `decision_ledger.json`). qa **GREEN**; reviewer
  **pass**. **Codex NOT available — single-reviewer verdict.** **P-019 local-only**
  (commits `b7572b7`, `de5679f` on the dev branch on top of the `6c40e2b` PR #15 base),
  not pushed/merged. Receipt:
  `build-os/receipts/P-019-record-mix-pass-closes-loop-in-cowork.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — THE ARC IS DOWN TO ITS LAST STEP: P-023 TRANSPORT (USER-GATED).**
  P-019 closed the learning loop inside the cowork surface (step 1); P-020 made the
  surface self-describing as an ordered, phase-grouped session flow (step 2);
  **P-021 PROVED the surface is agent-drivable end-to-end and the loop closes within
  it (step 3 — the MILESTONE).** The canonical target is now essentially MET at the
  decision-system level, so what remains is only transport packaging:
  - **P-022 — OPTIONAL / UNNEEDED.** The P-021 honesty clause surfaced NO real gap
    requiring session-efficiency / override-propagation work. Do NOT open unless a
    concrete gap emerges.
  - **P-023 — the ONLY remaining arc step: USER-GATED transport decision — MCP
    server vs a documented raw-CLI contract as the agent transport. Do NOT open
    blind; sequenced LAST; needs an explicit user ask.**
- **Also standing — the judgment layer is at a DOCTRINE-HONEST EQUILIBRIUM (flip
  program complete); the OUTCOME→learning axis is OPEN (P-018 + P-019).** The
  penalty, reward, and base-value re-curation levers have all converged:
  subtractive_drop's dominance is legitimate and no honest further flip exists in
  the current dimension set. Remaining threads:
  - **★ Outcome-enum generalization (reviewer's P-018 trajectory note — candidate,
    NOT staged):** widen the `reverted: bool` field to a small outcome enum
    (`reverted`/`kept`/`refined`) to round out the outcome→learning loop — widens
    WITHOUT breaking the byte-identical default; user-gated for the semantics.
  - **The ledger is DEAD (P-018 finding):** `add_decision`/`decision_ledger` has
    NO analyze-path consumer (display-only). A confirmed-outcome producer is only
    real if it lands on a LIVE channel (history or taste), not the ledger.
  - **★ The one open honest thread — SYMMETRIC re-judgment (user-gated, NOT
    staged):** is `subtractive_drop` at 85.29 (high on every dim) itself slightly
    OVER-valued? Lowering it (rather than inflating a rival) would be a different,
    un-signed-off packet. Surface to the user; do NOT open without an explicit ask.
  - **Reward-family (further reward rows) and re-curation-for-flips are now CLOSED
    as saturated / equilibrium** — not candidates unless the dimension set itself
    changes.
  - **Wider `--memory-dir` CLI surface** (from P-009 — partly a product question);
    net-new **event-logging** producers (behind a product decision);
    **taste-flip-via-product-change** (user-gated, separate packet). Off-path,
    deferred.

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **★ THE JUDGMENT LAYER IS AT A DOCTRINE-HONEST EQUILIBRIUM (P-017-verified):**
  the penalty (P-015), reward (P-016), and base-value re-curation (P-017) levers
  all converge on the same place. `subtractive_drop`'s default dominance is
  legitimate (subtraction IS the safe default and genuinely out-scores the
  alternatives on the ranked axis); the masked-vocal near-tie override (P-015
  penalty) and the foregrounded-loop promotion (P-016 reward) are the ONLY
  doctrinally-warranted flips; **there is NO honest further flip move inside the
  current dimension set.** The only remaining honest thread is a symmetric
  re-judgment (is subtractive_drop itself over-valued?) — user-gated, un-signed-off.
- **★ An evidence-gated creative nudge is only LIVE if its evidence is computed
  BEFORE `run_creative_engine` (P-016 live-wire lesson).** Masking is pre-creative,
  so P-015 was ALWAYS live; `provenance` / `source_audits` were POST-creative until
  P-016's reorder moved them just before creative. **A green test that RE-RUNS the
  engine on the finished result can MASK production inertness** (the P-009 failure
  mode) — always add a no-re-run liveness assertion on the real
  `result.creative` / `result.governance`.
- **Variant-scoring path is golden-unguarded:** `regression.py` reads
  `doctrine_score`, never `score_variant`, so the 68/68 golden cannot catch a
  creative-scoring change. **Unit + visibility + liveness + characterization tests
  are the binding guard for any `creative.py`/`score_variant`/`_KIND_SCORES`
  change** (P-012's `tests/test_creative_nudges.py`, P-013's
  `tests/test_creative_nudge_visibility.py`, P-015's `tests/test_decisive_nudge.py`,
  P-016's `tests/test_loop_promotion.py` including the two production-liveness
  tests, and **P-017's `tests/test_density_recuration.py`** which pins the 5-branch
  winner table + `_KIND_SCORES` untouched — an inflated `depth_cleanup` makes it
  FAIL).
- **Taste is structurally below truth (P-013-verified):** `_apply_taste` moves only
  the identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and
  is align-vetoed — so taste cannot reorder a truth-ranked governed winner on
  curated data. Working as intended.
- **The creative penalty nudge CAN reorder EXACTLY the `vocal_belief` branch under
  `lead_masked`, within the ±2.0 cap (P-015):** row-0 penalizes `vocal_ride` (`−14`
  raw = `−2.0` overall, the cap) but EXEMPTS `intimacy_pass`, so the 1.71-gap
  near-tie flips to `intimacy_pass` (vocal_B). Binding guard:
  `tests/test_decisive_nudge.py` + updated `tests/test_creative_nudges.py`.
- **The creative PROMOTION (reward) nudge CAN reorder EXACTLY the `loop` branch
  when a loop is genuinely foregrounded, within the +4.0 promotion cap (P-016 —
  the FIRST reward nudge, MERGED via PR #15):** the `_PROMOTION_TABLE` row lifts
  `loop_deconstruct` (81.9 → 85.9, raw +5.0 clamped to exactly +4.0) past
  `subtractive_drop` (85.3); gated on the REAL `source_auditors` `"foregrounded
  loop"` red_flag corroborated by `provenance` `high_risk`; NOW LIVE via the
  pipeline reorder. `CREATIVE_PROMOTION_CAP = 4.0` is a SEPARATE constant from the
  ±2.0 penalty `CREATIVE_NUDGE_CAP`; the penalty table/path is byte-untouched.
  Bounded — cannot overturn a gap ≥ 4.0, and `loop_deconstruct` competes only in
  the `loop` branch. Binding guard: `tests/test_loop_promotion.py`.
- **The `density` branch CANNOT be honestly flipped by base-value re-curation
  (P-017-verified):** `depth_cleanup` (81.14) trails `subtractive_drop` (85.29) by
  4.14; the only doctrine-defensible under-valuation is `contrast` (72→88 = 83.43;
  even →100 = 85.14, still below); the residual deficit lives entirely in
  `excitement` (66 vs 78), which is off-limits to inflate. `_KIND_SCORES` stays
  UNTOUCHED. Binding guard: `tests/test_density_recuration.py`.
- **★ THE DECISION LEDGER IS DISPLAY-ONLY — the LIVE learning channels are HISTORY
  and TASTE (P-018 finding):** `add_decision` → `decision_ledger.json` has NO
  analyze-path consumer; `mem.ledger()` is called only at `cli.py:315` (display).
  So a producer for any reserved ledger event (`manual_note`/`taste_feedback`/
  `mix_decision`/`validation_check`) would be INERT (the hollow-packet trap). The
  LIVE learning channels are HISTORY (`mix_pass_history.json` → `_apply_history`)
  and TASTE (`taste_profile.json` → governance). **A confirmed-outcome producer is
  only real if it lands on one of those, NOT the ledger.**
- **The confirmed-revert OVERRIDE CAN change real `analyze(--memory-dir)`
  `next_pass` (P-018 — the FIRST confirmed-outcome signal):** an opt-in
  `record_pass(reverted=True)` (via `memory-record --reverted`) makes
  `_apply_history` demote the reverted move + surface one confirmed "Revert last
  pass" item at priority 95 **regardless of the score-inferred `got_worse`**
  (early-return anti-double-up; distinct evidence line containing "confirm").
  Opt-in / byte-identical by default. Binding guard:
  `tests/test_confirmed_revert.py` (unit + override non-vacuity) +
  `tests/test_confirmed_revert_live.py` (no-re-run liveness — FAILS pre-P-018,
  PASSES at tip). The variant/golden path won't catch memory/next-pass changes, so
  these unit + liveness tests are the binding guard (mirrors the P-016 live-wire
  lesson: assert on real `analyze` output with NO re-run).
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-021 close (2026-07-01) — the MILESTONE step of the arc._
