# Receipt — P-016: Evidence-gated problem-native promotion — `loop` branch (the FIRST reward/promotion nudge) + a production live-wire

- **Date:** 2026-07-01
- **Authority:** build (router row 1: `builder → qa → reviewer → archivist`).
  **PRODUCT-CODE aesthetic change to a default recommendation — user-delegated.**
  The user chose direction **(A)** "open the base-scoring decision space",
  recommended fork **(i)** "evidence-gated", and delegated the decision to the
  orchestrator ("you figure out what to do using ClaudeOrchestrator" / "keep
  skating"). The build-orchestrator routed and recommended this exact packet.
  **This crosses the penalty-only line P-012 deliberately held — it is the FIRST
  reward/promotion nudge** — the load-bearing design shift, on record as
  user-delegated. The variant-scoring path is **golden-unguarded** (regression
  reads `doctrine_score`, never `score_variant`), so the **unit + liveness tests
  are the binding guard**. Merge to default stays gated on explicit go;
  dev-branch commits are covered by standing push-go. No design-UI / marketing /
  swarm / infra gate tripped.
- **Branch base (merge-base):** dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`; default `claude/dreamy-turing-z0oxll`
  (`git merge-base` = `694d19d`). PR #13 (P-001…P-012 + the canonical-alignment
  audit) is MERGED to default (merge commit `0f4e7e9`, in ancestry). P-015's
  product commit `1756f61` and P-016's two commits sit on the dev branch on top of
  that merge and are **local-only** at close.

## What it does (the mechanism)

When the analyzers flag a genuinely foregrounded / dominating loop — the REAL
existing `source_auditors` `"foregrounded loop"` red_flag (source_auditors.py:191)
corroborated by `provenance` `high_risk` — a bounded **promotion** lifts
`loop_deconstruct` past `subtractive_drop` to win the `loop` branch. With no such
evidence, `subtractive_drop` stays the default winner. Bounded, evidence-gated,
transparent (emits a `loop_promotion` `score_nudges` line), pure/deterministic,
layered on an UNTOUCHED `_KIND_SCORES` and an UNTOUCHED penalty path.

- **`CREATIVE_PROMOTION_CAP = 4.0`** — a SEPARATE constant from the ±2.0 penalty
  `CREATIVE_NUDGE_CAP`. The summed promotion overall-delta is clamped to
  `+CREATIVE_PROMOTION_CAP` exactly as the penalty path clamps to
  `−CREATIVE_NUDGE_CAP`. The penalty table, cap, and predicates are byte-untouched.
- **`_PROMOTION_TABLE` row:** kind `loop_deconstruct`, evidence `foregrounded_loop`,
  `+35` on excitement (`= +5.0` raw overall) clamped to exactly
  `+CREATIVE_PROMOTION_CAP`, with a verbatim `score_nudges` reason line.
- **`_foregrounded_loop` predicate** reads the REAL evidence wire off the real
  `result` (mirrors `_lead_masked` / `_width_crowded`; getattr-defensive so P-012
  unit results without those attrs still evaluate `False`) — a `"foregrounded
  loop"` red_flag from `source_auditors` corroborated by `provenance` `high_risk`.
  No monkeypatch of the nudge, no fabricated field.
- **Applied in `score_variant`** alongside the penalty path: fired promotions raise
  the curated dims / overall, the summed promotion overall-delta clamped to
  `+4.0`; the fired reason appended to `score_nudges` (present only when ≥1 nudge
  fired). Promotion and penalty are independent and both bounded.

## Doctrine anchor (the system's OWN principle — not subjective taste)

`governance.py::anti_template` warns when the same move-kind wins ≥3 problems:
"vary the move per problem." `subtractive_drop` was winning `chorus_lift` +
`density` + `loop` = 3 branches — exactly that pattern. Letting the loop-specific
move win the loop problem WHEN a loop is genuinely foregrounded drops
`subtractive_drop` to 2 branches (below the threshold), and is backed by
`loops_not_foregrounded`, `source_material_respected`, and the kill-switch "never
allow a stock loop to dominate the song identity."

## ★ THE IMPORTANT LESSON — Commit-1's mechanism was INERT in production; the orchestrator-in-chief caught it before close (a P-009-style catch)

**Commit-1 shipped a mechanism that never fired in the real `analyze()` output.**
In `pipeline.analyze()`, `run_creative_engine` (was line 221) ran BEFORE
`provenance` (was 225) and `source_audits` (was 228) were populated — so the
`_foregrounded_loop` promotion predicate always read empty evidence and the
promotion **never fired in the real `analyze()` output**. Commit-1's tests passed
only because they re-ran `run_creative_engine` on the finished `result` (which by
then HAD the evidence). **This is exactly the P-009 "inert learning loop" failure
mode.** The builder disclosed the ordering but mislabeled it "by design / mirrors
P-015" — but **P-015 is genuinely live** because its evidence (`masking_report`)
is computed BEFORE creative (line 187/193).

**Commit-2 fixed it with a minimal live-wire:** relocated `analyze_provenance` +
`audit_all` to just BEFORE `run_creative_engine`. Their inputs
(`source_material` / `depth_map` / `records`) are all populated ~90 lines earlier
(the per-track loop fills `source_material` / `depth_map`; `records` is assigned
before section/masking analysis), so it is a **pure relocation** —
`render_graph` / `plugin_scan` / `run_governance` stay in place. Added TWO
**production-liveness tests** that assert on the real `analyze()`
`result.creative` / `result.governance` WITHOUT any re-run of the engine — they
**FAIL on the pre-reorder pipeline** (winner `loop_B`, inert) and **PASS after**
(winner `loop_A`), so they genuinely guard the live-wire.

**STANDING LESSON (carry forward):** an evidence-gated creative nudge is only
*real* if its evidence is computed BEFORE `run_creative_engine`. A green test that
re-runs the engine on the finished result can MASK production inertness. Any
future creative reward/penalty nudge needs a live-wire check (assert on the real
`result.creative` / `result.governance`, no re-run) — not just a unit test.

## Scope

- **In (the exact edits):**
  1. `logic_mix_os/creative.py` (Commit-1, +88): `CREATIVE_PROMOTION_CAP = 4.0`,
     `_PROMOTION_TABLE`, `_foregrounded_loop` predicate, and promotion application
     in `score_variant` (summed promotion overall-delta clamped to `+4.0`;
     `loop_promotion` reason appended to `score_nudges` on fire).
  2. `logic_mix_os/pipeline.py` (Commit-2, +17/−3): **relocated `analyze_provenance`
     + `audit_all` to just BEFORE `run_creative_engine`** (pure relocation — inputs
     already populated ~90 lines earlier). This is the LIVE-WIRE.
  3. `tests/test_loop_promotion.py` (NEW; Commit-1 +233, Commit-2 +70): the binding
     guard — flip, load-bearing negative control, cap-binds, collateral safety, and
     the two production-liveness tests.
- **Out (explicit) — verified UNTOUCHED:** `_KIND_SCORES` (values unchanged),
  `CREATIVE_NUDGE_CAP` (still 2.0), the entire penalty table / path (byte-untouched),
  both existing predicates (`_lead_masked` / `_width_crowded`), the clamp logic.
  `governance.py` has ZERO references to `provenance` / `source_audits`. The P-012 /
  P-013 / P-015 test files were NOT edited (and pass). `render_graph` / `plugin_scan`
  / `run_governance` positions unchanged.
- **Out (explicit):** no push / merge into the protected default / deploy / secret —
  out of authority for this close.

## Behavior (verified by qa + reviewer)

In the `loop` branch under a genuinely foregrounded loop:

- `loop_deconstruct` (loop_A): 81.9 → **85.9** — raw `+5.0` **clamped to exactly
  `+4.0`** (the cap binds), carries the `loop_promotion` `score_nudges` line.
- `subtractive_drop` (loop_B): **85.3** unchanged (in no promotion row).
- **Loop winner FLIPS `loop_B` → `loop_A` by 0.6**; the **governed winner also
  flips** (no veto).
- **Negative control (load-bearing):** with NO foregrounded-loop evidence,
  `subtractive_drop` (loop_B) wins — the flip is caused by the EVIDENCE, not a
  base re-rank.

**Reorder SAFE BY CONSTRUCTION:** `governance.py` has ZERO references to
`provenance` / `source_audits`; `creative.py`'s ONLY reads of those attrs are
inside the new `_foregrounded_loop` predicate → nothing but the promotion consumes
them in the reordered region → the default output cannot change. Backed by a
**12-artifact byte-identical diff** across all 3 seeded fixtures (none foreground a
loop): `provenance` / `source_audits` / `creative` / `governance` byte-identical
before/after the reorder.

**Collateral (bounded — no clear-ranking overturn):** only the `loop` branch flips.
`chorus_lift` / `density` still `subtractive_drop`; `vocal_belief` per P-015; depth
unchanged. `subtractive_drop` now wins **2** branches (`chorus_lift`, `density`),
not 3 — anti_template pressure relieved.

## Commits

- `b15b957` **P-016: evidence-gated loop-deconstruct promotion (first reward
  nudge).** Commit-1 — the promotion mechanism + binding tests together (green in
  isolation, required because it alters default-winner behavior).
  `creative.py` +88, `tests/test_loop_promotion.py` +233 (2 files, 321 insertions).
  **Green in isolation: 226 passed.** Author/committer `Claude <noreply@anthropic.com>`.
- `a9f4e26` **P-016: live-wire the loop-promotion evidence in analyze().** Commit-2 —
  the LIVE-WIRE (pure relocation of `analyze_provenance` + `audit_all` to just
  before `run_creative_engine`) + two production-liveness tests.
  `pipeline.py` +17/−3, `tests/test_loop_promotion.py` +70 (2 files, 84 insertions /
  3 deletions). Author/committer `Claude <noreply@anthropic.com>`.
- `13528bf` Confirm P-016 as active packet — **non-product** (memory-only:
  `build-os/packets/active_packet.md`).
- This archivist close adds **one build-os-only commit** (receipt + memory advance),
  following the prior-close pattern (`1cfe93b`, `678b9bf`, `0573e9c`, `f591f89`, …).

## QA proof (exact)

- **Suite:** `python -m pytest` → **217 → 228 passed** (+11; 0 failed / 0 skipped /
  0 warnings — green even under `-W error`). **Commit-1 in isolation: 226 passed.**
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68, 0 critical, 0
  warnings** held (doctrine golden — `loops_not_foregrounded` held; the default
  depth planner never foregrounds a loop). Standing fact: the variant-scoring path
  is golden-unguarded (`regression.py` reads `doctrine_score`, never
  `score_variant`); the **unit + liveness tests are the binding guard**.
- **Commit-1 in isolation:** **GREEN — 226 passed** (the mechanism + tests are
  bundled in `b15b957`; the promotion tests passed by re-running the engine — see
  the INERT-in-production catch above; Commit-2 makes it live).
- **Behavior:** loop_deconstruct 81.9 → 85.9 (raw +5.0 clamped to exactly +4.0 =
  the cap binds) > subtractive_drop 85.3 → loop winner flips `loop_B` → `loop_A` by
  0.6; governed winner also flips (no veto). Negative control (no evidence) →
  subtractive_drop wins.
- **Reorder safe by construction:** `governance.py` has ZERO
  `provenance`/`source_audits` refs; `creative.py`'s only reads are in the new
  predicate → 12-artifact byte-identical diff across all 3 seeded fixtures.
- **Collateral:** only the loop branch flips (chorus_lift / density still
  subtractive_drop; vocal_belief per P-015; depth unchanged). P-012/P-013/P-015 test
  files NOT edited and pass (58 passed).
- **Safety grep:** **clean** — no real DAW / Logic / AppleScript / subprocess /
  `.logicx` write / network introduced; fake adapters only.
- **UI smoke:** **N/A** — no surface touched.
- **qa verdict: GREEN.**

## Review

- **Verdict: pass**, with a **non-vacuity mutation check**: emptying the promotion
  row → the 5 promotion-dependent + 2 liveness tests go RED, the negative control
  stays GREEN; reverting ONLY the reorder (keeping the mechanism) → the 2 liveness
  tests go RED (proving the reorder is what makes the promotion live) while the
  re-run tests stay green (which is exactly the inertness the liveness tests exist
  to catch). → the tests are **load-bearing, not always-green**.
- The `plan_depth` monkeypatch in the liveness test is a **legitimate seam**: it
  models a real foregrounded-loop song; the REAL `audit_all` / `analyze_provenance`
  / `run_creative_engine` produce AND consume the evidence — nothing is faked.
- **Codex second-eyes: NOT available** — **single-reviewer verdict** (recorded
  caveat), consistent with P-012 / P-013 / P-014 / P-015.
- **Reviewer watch-item (non-blocking) — reward-creep trajectory:** this is the
  FIRST reward nudge; the penalty-only line is now crossed and precedent is set.
  Any FUTURE reward row must clear the same bar: its own evidence gate + a
  non-vacuity mutation check + a collateral-safety proof + **a live-wire check**
  (evidence computed before `run_creative_engine`; assert on the real
  `result.creative`/`result.governance`, no re-run). Carry into every future
  `creative.py` / `_PROMOTION_TABLE` touch.
- **Non-blocking standing config tension (flagged, not a P-016 regression):** the
  mandated `Co-Authored-By: Claude Opus 4.8` commit trailer is technically a model
  identifier, but it is required by the harness commit instructions and is
  consistent across all packets — a standing environment constraint.

## Residue

- **Reward nudges family — OPENED.** The penalty-only line is crossed and precedent
  is set. Future reward rows on other branches
  (`density → depth_cleanup`, `chorus_lift → drum_room_bloom`) are now **in-doctrine
  follow-ups**, but each needs its own evidence gate + the same non-vacuity +
  collateral-safety bar + a **live-wire check**. **User-gated per-row** — do not
  batch.
- **Standing lesson (new):** an evidence-gated creative nudge is only LIVE if its
  evidence is computed BEFORE `run_creative_engine`. Masking is pre-creative, so
  P-015 was always live; `provenance` / `source_audits` were POST-creative until
  P-016's reorder moved them. A green test that re-runs the engine can mask
  production inertness — always add a no-re-run liveness assertion.
- **Bigger lever still untouched by design:** the deeper `_KIND_SCORES`
  re-curation remains the larger creative-scoring move; P-016 (like P-012/P-015)
  layered on the UNTOUCHED base rather than re-curating it.
- **(carried) Deferred candidates, unchanged:** wider `--memory-dir` CLI surface
  (partly a product question); net-new event-logging producers (behind a product
  decision); taste-flip-via-product-change (user-gated, separate packet — the
  reachable taste claim is already covered by
  `test_live_wire.py::test_taste_axis_changes_governance`).
- **Known risks:** commits on this branch are unsigned (environment limitation;
  correct author/committer `noreply@anthropic.com`, GitHub shows "Unverified").

## Open boundaries (awaiting explicit go)

- **P-016 is local-only on the dev branch** as of this close. The two product
  commits `b15b957` and `a9f4e26` sit on `claude/logic-mix-os-hardening-12-7hbeh1`
  on top of the `0f4e7e9` merge. The orchestrator pushes the dev branch separately
  (standing push-go). Any subsequent PR / **merge into the protected default**
  needs the user's explicit go. **No push / merge / deploy / secret action taken in
  this close.**
