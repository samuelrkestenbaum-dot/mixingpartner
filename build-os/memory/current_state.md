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
  active dev branch `claude/logic-mix-os-hardening-12-7hbeh1` (`git merge-base`
  with default = `694d19d`). **PR #13 (P-001…P-012 + the canonical-alignment
  audit) is MERGED to default** — merge commit `0f4e7e9`. The post-merge dev
  branch carries P-013 (`172cfd0`, tests-only), **P-015 (`1756f61`, product)**,
  and **P-016 (`b15b957` + `a9f4e26`, product)** on top of `0f4e7e9`; all are
  local-only at this close (P-014 added no product commit).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-07-01):** suite **228 passed** (0 failed /
  skipped / warnings; green even under `-W error`); regression **68/68** (0
  critical / 0 warnings).

## Where we are

- **THE PENALTY-ONLY LINE IS CROSSED — P-016 SHIPS THE FIRST REWARD/PROMOTION
  NUDGE (loop branch), EVIDENCE-GATED AND NOW LIVE IN PRODUCTION.** User-delegated
  (direction A "open the base-scoring decision space" + fork (i) "evidence-gated"
  + "keep skating"; the build-orchestrator routed it). When the analyzers flag a
  genuinely foregrounded / dominating loop — the REAL `source_auditors`
  `"foregrounded loop"` red_flag corroborated by `provenance` `high_risk` — a
  bounded promotion (`CREATIVE_PROMOTION_CAP = 4.0`, a SEPARATE constant from the
  ±2.0 penalty `CREATIVE_NUDGE_CAP`) lifts `loop_deconstruct` past
  `subtractive_drop` to win the `loop` branch: `loop_deconstruct` 81.9 → **85.9**
  (raw +5.0 clamped to exactly +4.0 = the cap binds) > `subtractive_drop` 85.3 →
  loop winner flips `loop_B` → `loop_A` by 0.6 (governed winner also flips, no
  veto). **No such evidence → `subtractive_drop` stays the default.** Grounded in
  the system's OWN `anti_template` doctrine ("vary the move per problem") +
  `loops_not_foregrounded` + `source_material_respected` + the kill-switch "never
  allow a stock loop to dominate the song identity." Bounded, transparent (emits a
  `loop_promotion` `score_nudges` line), pure/deterministic, layered on an
  UNTOUCHED `_KIND_SCORES` and an UNTOUCHED penalty path. **`subtractive_drop` now
  wins 2 branches (`chorus_lift`, `density`), not 3 — anti_template pressure
  relieved; the loop branch goes to `loop_deconstruct` WHEN a loop is genuinely
  foregrounded.**
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
  pass unchanged after P-015 and P-016.

- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED (option B, P-012), MERGED
  (PR #13), MADE DECISIVE (P-015), AND NOW EXTENDED TO REWARD (P-016).** The
  bounded, transparent, capped evidence-nudge layer ON TOP of the curated
  `_KIND_SCORES` (values UNCHANGED) is live on default via PR #13; P-015 tunes
  row-0 to be decisive on the masked-vocal near-tie; **P-016 crosses into REWARD
  with the first promotion row (loop branch).** The reward-nudges family is now
  OPENED — future reward rows are in-doctrine follow-ups, each user-gated + bar'd.

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
- **Last closed packet:** **P-016** — Evidence-gated problem-native promotion
  (`loop` branch, the FIRST reward/promotion nudge) + a production live-wire.
  User-delegated (direction A + fork (i), "keep skating"; the build-orchestrator
  routed). **Two commits (≤2):** `b15b957` Commit-1 — promotion mechanism
  (`CREATIVE_PROMOTION_CAP = 4.0`, `_PROMOTION_TABLE`, `_foregrounded_loop`
  predicate reading the real `source_audits`/`provenance`, applied in
  `score_variant`) + binding tests, **green in isolation (226 passed)**; `a9f4e26`
  Commit-2 — the LIVE-WIRE (pure relocation of `analyze_provenance` + `audit_all`
  to just before `run_creative_engine`) + two production-liveness tests. Suite
  **217 → 228 passed** (+11; 0 failed/skipped/warnings, green under `-W error`);
  regression **68/68, 0 critical, 0 warnings** (`loops_not_foregrounded` held).
  Reorder byte-identical across all 3 fixtures (12-artifact diff). qa verdict
  **GREEN**. Reviewer **pass** with a non-vacuity mutation check (emptying the
  promotion row → 5 promotion-dependent + 2 liveness tests RED, negative control
  GREEN; reverting ONLY the reorder → the 2 liveness tests RED) and a
  **reward-creep watch-item**. **Codex NOT available — single-reviewer verdict.**
  **P-016 is local-only** (commits `b15b957`, `a9f4e26` on the dev branch on top of
  `0f4e7e9`), not pushed/merged at close. Receipt:
  `build-os/receipts/P-016-evidence-gated-loop-promotion.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — the creative-scoring decision is resolved (penalty + first reward both
  shipped). Remaining moves are small in-authority additives + user-gated
  follow-ups.** Candidates:
  - **More reward nudges (now IN-DOCTRINE, precedent set by P-016)** — future
    reward rows on other branches (`density → depth_cleanup`,
    `chorus_lift → drum_room_bloom`). **User-gated per-row;** each needs its own
    evidence gate + the same non-vacuity + collateral-safety bar + a **live-wire
    check** (evidence before `run_creative_engine`, asserted no-re-run). Do not batch.
  - **Deeper `_KIND_SCORES` re-curation** — the bigger lever, untouched by P-012 /
    P-015 / P-016 by design (all layered on the untouched base). User-gated.
  - **Taste-flip-via-product-change** — user-gated, separate packet (the reachable
    taste claim is already covered by `test_live_wire.py::test_taste_axis_changes_governance`).
  - **Wider `--memory-dir` CLI surface** (from P-009 — partly a product question);
    net-new **event-logging** producers (behind a product decision). Deferred.

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **★ An evidence-gated creative nudge is only LIVE if its evidence is computed
  BEFORE `run_creative_engine` (P-016 live-wire lesson).** Masking is pre-creative,
  so P-015 was ALWAYS live; `provenance` / `source_audits` were POST-creative until
  P-016's reorder moved them just before creative. **A green test that RE-RUNS the
  engine on the finished result can MASK production inertness** (the P-009 failure
  mode) — always add a no-re-run liveness assertion on the real
  `result.creative` / `result.governance`.
- **Variant-scoring path is golden-unguarded:** `regression.py` reads
  `doctrine_score`, never `score_variant`, so the 68/68 golden cannot catch a
  creative-scoring change. **Unit + visibility + liveness tests are the binding
  guard for any `creative.py`/`score_variant` change** (P-012's
  `tests/test_creative_nudges.py`, P-013's `tests/test_creative_nudge_visibility.py`,
  P-015's `tests/test_decisive_nudge.py`, and P-016's `tests/test_loop_promotion.py`
  including the two production-liveness tests).
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
  the FIRST reward nudge):** the `_PROMOTION_TABLE` row lifts `loop_deconstruct`
  (81.9 → 85.9, raw +5.0 clamped to exactly +4.0) past `subtractive_drop` (85.3);
  gated on the REAL `source_auditors` `"foregrounded loop"` red_flag corroborated
  by `provenance` `high_risk`; NOW LIVE via the pipeline reorder. `CREATIVE_PROMOTION_CAP
  = 4.0` is a SEPARATE constant from the ±2.0 penalty `CREATIVE_NUDGE_CAP`; the
  penalty table/path is byte-untouched. Bounded — cannot overturn a gap ≥ 4.0, and
  `loop_deconstruct` competes only in the `loop` branch. Binding guard:
  `tests/test_loop_promotion.py`.
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-016 close (2026-07-01)._
