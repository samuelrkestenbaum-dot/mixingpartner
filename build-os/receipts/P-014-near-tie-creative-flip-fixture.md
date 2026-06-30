# Receipt — P-014: Near-tie-creative-FLIP fixture — VERIFIED NEGATIVE FINDING (the P-012 nudge cannot reorder ANY branch under current curation)

- **Date:** 2026-06-30
- **Authority:** build (router row 1: `builder → qa → reviewer → archivist`).
  Tests-only intent; no design-UI / marketing / swarm / infra gate tripped.
  **Outcome: VERIFIED NEGATIVE FINDING — no product code, no product/test commit.**
- **Branch base (merge-base):** dev branch `claude/logic-mix-os-hardening-12-7hbeh1`;
  default `claude/dreamy-turing-z0oxll` (`git merge-base` = `694d19d`). PR #13
  (P-001…P-012 + the canonical-alignment audit) is MERGED to default (merge commit
  `0f4e7e9`, in ancestry). HEAD `596174d` is the P-014 active-packet confirmation
  commit only — **no product change.**

## Intent vs outcome

P-014 was the **complement to P-013**. P-013 proved the P-012 nudge fires on real
data through `analyze()` but the cap binds and the winner does NOT flip (option a,
on a *clear* ranking). P-014's goal was to prove the OTHER half: a genuine
**near-tie** creative case where the bounded nudge, firing through the live
`analyze()` path, is **decisive** — i.e. it flips the creative/governed winner to
the runner-up within the `CREATIVE_NUDGE_CAP = ±2.0` bound.

**Outcome: UNREACHABLE (verified).** A near-tie creative FLIP via the P-012 nudge
is **structurally unreachable test-only under the current `_KIND_SCORES` /
`_NUDGE_TABLE` curation.** The builder wrote **ZERO code** — the honesty clause in
the packet was honored: no product-code change, no contrived fixture, no commit.
qa then **adversarially tried to REFUTE the finding** with THREE independent
harnesses and re-derived the arithmetic from source; **all produced 0 flips.**
The finding stands.

## The verified structural reason (qa source-read facts)

- `overall` is **derived, not stored**: `overall = mean(7 numeric dims) −
  risk_penalty{low: 0, medium: 6, high: 14}`, recomputed exactly as
  `score_variant` derives it.
- **Base `overall_score` per kind:** `subtractive_drop` **85.29**, `vocal_ride`
  82.86, `loop_deconstruct` 81.86, `drum_room_bloom` 81.4,
  `depth_cleanup` / `intimacy_pass` 81.14, `width_bloom` 75.71.
- **`_NUDGE_TABLE` (exact):**
  - **row-0** `{width_bloom, vocal_ride, intimacy_pass}` ← condition `lead_masked`,
    `vocal_belief −8`.
  - **row-1** `{width_bloom}` ← condition `width_crowding`, `vocal_belief −6`.
  - `CREATIVE_NUDGE_CAP = 2.0`, clamped on the **summed overall delta**
    (`nudged_overall − base_overall` clamped to ±2.0, then re-added to base).
- **Penalizable kinds (only):** `width_bloom` (rows 0+1), `vocal_ride` (row 0),
  `intimacy_pass` (row 0). The **universal branch leader `subtractive_drop` is in
  NO nudge row → penalty-immune.**
- **Per-branch leaders** (competing kinds are LITERALS in `generate_variants` keyed
  on `problem['id']`, proven **fixture-invariant** across 4 record sets — a fixture
  cannot inject a kind or a third differentiating condition):
  - `chorus_lift` `[width_bloom, subtractive_drop, vocal_ride, drum_room_bloom]`:
    leader `subtractive_drop` 85.29 (**immune**) → no flip.
  - `density` `[depth_cleanup, subtractive_drop]`: leader `subtractive_drop` 85.29
    (**immune**), gap 4.14 > cap → no flip.
  - `loop` `[loop_deconstruct, subtractive_drop]`: leader `subtractive_drop` 85.29
    (**immune**) → no flip.
  - `depth` `[depth_cleanup]`: single kind → nothing to reorder.
  - `vocal_belief` `[vocal_ride 82.86, intimacy_pass 81.14]`, gap **1.71 (< 4.0)**:
    leader `vocal_ride` IS penalizable, BUT the only row that hits it (row-0
    `lead_masked −8`) hits the runner-up `intimacy_pass` by the **identical −8** →
    both drop −1.14 overall, gap preserved → **no flip.**
- Predicates take only `result` (not `kind`), so for a fixed fixture each predicate
  is uniformly true/false across **all** kinds; the only per-kind discriminator is
  row-membership, and **no membership pattern lets a bounded penalty reorder any
  branch.**

## Three-harness adversarial confirmation (qa)

qa tried to REFUTE the finding (not confirm it), with three independent paths:

1. **Builder's inline-math harness** — re-derives base/nudged `overall` from the
   tables directly. **0 flips.**
2. **qa's real-`score_variant` driver** — drives the actual product
   `score_variant` rather than recomputed math. **0 flips.**
3. **Saturated worst-case `masking_report`** — every classification the analyzer
   emits set true at once (maximal penalty pressure on every penalizable kind).
   **0 flips.**

All three agree, and the arithmetic was re-derived from source. The harnesses live
in **scratchpad (NOT committed)** — they are negative-finding instruments, not
product tests.

## The reframing this finding establishes (headline)

Under the current curation, the **P-012 nudge is effectively a TRANSPARENCY /
EVIDENCE layer**: it moves the displayed governed `overall_score` (and emits
`score_nudges`) but **can NEVER reorder a winner in any branch.** P-013's option-(a)
"cannot overturn a ranking" therefore holds **UNIVERSALLY**, not just on one
fixture. This is **sharper** than the P-012 sign-off framing ("cannot overturn a
*clear* ranking," which implied it could break a near-tie). The verified truth: it
cannot break ANY tie either, for the two structural reasons above (immune universal
leader; the one near-tie branch penalizes leader + runner-up equally).

**This is NOT a defect.** The nudge remains honest, bounded, penalty-only,
evidence-tagged — its "decisive-when-close" capability is currently **latent and
unrealizable** without a curation change.

## Scope

- **In:** nothing committed. A verified structural finding (source read +
  three-harness adversarial refutation attempt), reported with full evidence rigor
  — exactly the honesty-clause path the packet authorized.
- **Out (explicit):**
  - **All product / runtime code** — `creative.py` (`_KIND_SCORES`, `_NUDGE_TABLE`,
    `_apply_nudges`, `score_variant`, `generate_variants`), `governance.py`,
    `pipeline.py` — **untouched.** `creative.py` is unchanged since P-012
    (`0df436c`).
  - **No new test / fixture** — a flip-producing fixture cannot exist without a
    product-code aesthetic change; per the honesty clause, none was forced.
  - **The user-gated "make-the-nudge-decisive" curation change** — out of authority;
    surfaced as a decision in residue (see below), not actioned.

## Commits

- **No product / test commit** — negative finding.
- `596174d` Confirm P-014 (near-tie-creative-FLIP fixture, tests-only) as active
  packet — **non-product** (memory-only:
  `build-os/packets/active_packet.md`). The only P-014 commit; no product change.
- This archivist close adds **one build-os-only commit** (receipt + memory
  advance), following the prior-close pattern (`0573e9c`, `f591f89`, …).

## QA proof (exact)

- **Suite:** `python -m pytest` → **207 passed** (0 failed / 0 skipped / 0
  warnings) — **UNCHANGED** (no code added).
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68**, **0
  critical** (held). Standing fact: the variant-scoring path is golden-unguarded;
  unit/visibility tests are the binding guard — and this packet adds none, because
  no behavior exists to guard.
- **Commit-1 in isolation:** **N/A** — negative finding; no product/test commit
  exists. `creative.py` unchanged since P-012 (`0df436c`). Working tree clean.
- **Safety grep:** **N/A** — no new product/test code. (The scratchpad harnesses
  are negative-finding instruments, not committed.)
- **UI smoke:** N/A (no surface touched).
- **HEAD:** `596174d` (only the P-014 active-packet confirmation commit; no product
  change).
- **qa verdict: GREEN — FINDING CONFIRMED.**

## Review

- **Verdict: pass — FINDING CONFIRMED (verified negative).** qa adversarially set
  out to REFUTE the unreachability claim and could not: three independent harnesses
  (inline-math, real-`score_variant`, saturated worst-case `masking_report`) each
  returned **0 flips**, and the arithmetic was re-derived from source. The
  per-branch leader/penalizability table is the structural proof.
- **Codex second-eyes: NOT available** — **single-reviewer verdict** (recorded
  caveat), consistent with P-012/P-013.
- **Product Trajectory Check:** sharpens the P-012 sign-off from "cannot overturn a
  *clear* ranking" to "cannot reorder **any** branch under current curation." No
  product behavior changed; the nudge's role is documented as transparency-only.

## Residue

- **"Near-tie-creative-FLIP fixture" candidate → RESOLVED-as-unreachable.** What
  was a reachable-deferred candidate after P-013 is now a **verified negative
  finding**: no fixture can produce a flip without a product-code aesthetic change.
  It is replaced by the user-gated curation packet below.
- **USER-GATED DECISION (record as a decision, not a TODO) — "make-the-nudge-
  decisive (curation change)":** Making the nudge decisive-on-a-near-tie requires a
  **product-code aesthetic change → user-gated, separate packet.** Two concrete
  routes:
  - **Split row-0's `kinds` set** so `vocal_ride` is penalized but `intimacy_pass`
    is **NOT** — then the `vocal_belief` 1.71-gap near-tie WOULD flip within the
    cap (the runner-up no longer drops by the identical −8).
  - **Re-curate `_KIND_SCORES`** so a penalizable kind narrowly leads a
    non-equally-penalized rival in some branch.
  Until the user asks for that, the nudge stays **transparency-only**, and this
  finding documents the reality.
- **(carried) Deferred candidates, unchanged:**
  - **Reward nudges (orchestrator rows 3+4)** — user-gated; P-012 is penalty-only
    by design.
  - **Wider `--memory-dir` CLI surface** — partly a product question.
  - **Net-new event-logging producers** — behind a product decision.
- **Known risks:** the variant-scoring path remains golden-unguarded by design.
  Commits on this branch are unsigned (environment limitation; correct
  author/committer, GitHub shows "Unverified").

## Open boundaries (awaiting explicit go)

- **No product/test commit to push.** Only the build-os memory advance (this close)
  and the prior `596174d` active-packet confirmation sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9` merge. Any push,
  and any subsequent PR / merge into the protected default, needs the user's
  explicit go. **No push / merge / deploy / secret action taken in this close.**
