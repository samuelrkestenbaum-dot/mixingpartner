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
  and **P-017 (`1b03ad3`, tests-only guard — verified finding, no product change)**;
  the local-only-at-close commits (P-013, P-015, P-017's guard) are not pushed.
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-07-01):** suite **240 passed** (0 failed /
  skipped / warnings; green even under `-W error`); regression **68/68** (0
  critical / 0 warnings).

## Where we are

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
- **Last closed packet:** **P-017** — Minimal doctrine-honest `_KIND_SCORES`
  re-curation (density → depth_cleanup), the FIRST base-value change attempt.
  User-signed-off ("A"). **Resolved to a VERIFIED NEGATIVE FINDING: an honest
  re-curation CANNOT flip the `density` branch — arithmetically forced by the
  doctrine, verified adversarially. `_KIND_SCORES` LEFT UNTOUCHED — NO product
  change.** The builder committed ONLY the 12-test characterization guard
  (`tests/test_density_recuration.py`, +183, commit **`1b03ad3`** — the sole packet
  commit, green in isolation = 12 passed). Suite **228 → 240 passed** (+12; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held; safety grep clean; UI N/A; P-012/P-013/P-015/P-016 test files
  NOT edited and pass (69). The guard is load-bearing (an injected inflated
  `depth_cleanup` makes it FAIL — density → density_A). qa **GREEN — FINDING
  CONFIRMED**; reviewer **pass**. **Codex NOT available — single-reviewer verdict.**
  **P-017's guard commit `1b03ad3` is local-only** (dev branch on top of the
  `6c40e2b` PR #15 merge), not pushed/merged at close. Receipt:
  `build-os/receipts/P-017-doctrine-honest-kind-scores-recuration.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — the judgment layer is at a DOCTRINE-HONEST EQUILIBRIUM; the flip program
  is essentially complete.** The penalty, reward, and base-value re-curation levers
  have all converged: subtractive_drop's dominance is legitimate and no honest
  further flip exists in the current dimension set. Remaining threads:
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
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-017 close (2026-07-01)._
