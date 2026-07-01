# P-017 — Minimal doctrine-honest `_KIND_SCORES` re-curation (density → depth_cleanup): VERIFIED NEGATIVE FINDING

**Date:** 2026-07-01
**Status:** CLOSED — verified negative finding (no honest flip), a committed load-bearing characterization guard.
**Type:** PRODUCT-code aesthetic change to the curated judgment itself (attempted) — the FIRST attempt to change a base `_KIND_SCORES` value. User-signed-off ("A"). Resolved to a FINDING: NO product change; `_KIND_SCORES` left UNTOUCHED.

---

## Title

Minimal doctrine-honest `_KIND_SCORES` re-curation — the depth/hierarchy move
(`depth_cleanup`) should win the `density` problem over `subtractive_drop`. The
FIRST base-value change attempt (crossing the line P-012/P-015/P-016 held: they
layered bounded evidence nudges on an UNTOUCHED base).

## Outcome (the headline)

**FINDING — an honest re-curation CANNOT flip the `density` branch.** It is
**arithmetically forced by the DOCTRINE** (which dims are honestly movable), not
a search failure — verified adversarially by qa and confirmed by the reviewer.
`_KIND_SCORES` is **LEFT UNTOUCHED** — **NO product change**. The builder
committed ONLY a 12-test characterization guard (the honesty clause held, P-014
discipline: honesty beats the flip).

## Scope

**In:**
- Attempt a minimal, doctrine-honest re-curation of `_KIND_SCORES["depth_cleanup"]`
  ONLY, to let the depth/hierarchy move win the `density` branch.
- Honesty constraint (load-bearing): every changed dim must be a defensible
  re-judgment of `depth_cleanup`'s character; never inflate to cross the threshold.
  `excitement` OFF-LIMITS to inflate (subtle depth work is honestly un-flashy).
- Report the before/after overalls and the full 5-branch winner table either way.
- If honest values cannot flip → STOP and report a FINDING (P-014 discipline).

**Explicitly out:**
- Touching `subtractive_drop` or any other kind's base dims (fixed untouched).
- Touching the penalty layer (`_NUDGE_TABLE`, `CREATIVE_NUDGE_CAP`), the promotion
  layer (`_PROMOTION_TABLE`, `CREATIVE_PROMOTION_CAP`), or either cap.
- Any product-code change at all (the finding forced this — none was made).
- Inflating `excitement` or re-labeling a depth pass as a vocal-forward move
  (both dishonest — the only paths that would flip density).
- The symmetric question "is `subtractive_drop` over-valued?" — a different,
  un-signed-off packet. NOT opened, NOT staged (recorded as the one open thread).

## The verified arithmetic (the honest-ceiling proof — recorded exactly)

Scoring model: `overall = mean(7 dims) − risk_penalty`.

- `depth_cleanup` base overall **81.14** (dim sum 568); `subtractive_drop`
  **85.29** (dim sum 597, low risk) → **gap 4.14**.
- The only doctrine-defensible under-valuation is **`contrast`** (dc 72 vs sd 88):
  depth creates foreground/midground/background separation = perceptual contrast
  (`masking_is_hierarchy` + `section_contrast_considered`). Reconsidering it:
  - `contrast → 88` = **83.43** (short **1.86**).
  - `contrast → 100` (the impossible ceiling) = **85.14** — **STILL below 85.29.**
- A FULL doctrine-honest re-curation (`contrast → 88`, `technical → 85`,
  `ramone → 86`, `taste → 86`; `halee` stays 90 = table max; `vocal_belief` stays
  86 = sd's level; **`excitement` LOCKED at 66**) reaches only **83.86** — short
  by **1.43**.
- The entire residual deficit lives in **`excitement` (66 vs 78)**, which is
  OFF-LIMITS to inflate (subtle depth work is honestly un-flashy; `excitement → 79`
  to tie would pass sd's own 78). The only flips require inflating `excitement`
  or re-labeling a depth pass as a vocal-forward move — **both dishonest.**
- **The finding is forced by the DOCTRINE** (which dims are honestly movable),
  not by a failed search.

### Before/after winner table (all 5 branches, real `analyze()` path) — UNCHANGED

| Branch         | Winner            | Overall | Note                        |
|----------------|-------------------|---------|-----------------------------|
| chorus_lift    | subtractive_drop  | 85.3    | unchanged                   |
| density        | subtractive_drop  | 85.3    | **no honest flip** (finding)|
| loop (default) | subtractive_drop  | 85.3    | default, no foregrounded loop|
| depth          | depth_cleanup     | 81.1    | single-variant branch       |
| vocal_belief   | vocal_ride        | 82.9    | per prior curation          |

## The committed guard (load-bearing, non-tautological — recorded as valuable)

`logic-mix-os/tests/test_density_recuration.py` — **12 tests, +183 lines** (NEW).
Pins: the 5-branch winner table UNCHANGED on the real `analyze()` /
`run_creative_engine` path; the honest-ceiling arithmetic (proving the finding is
arithmetically forced); and `_KIND_SCORES` untouched.

**Why this is load-bearing, not busywork (proven by qa and reviewer):** injecting
an inflated `depth_cleanup` (contrast=88 + excitement=90, or all dims=100) makes
the density guard **FAIL** on the real `analyze()` path (density flips to
`density_A`) — so the guard genuinely catches an accidental/dishonest density
flip. Unlike P-014's no-commit finding, committing **executable arithmetic** here
is defensible because **the finding IS arithmetic** and the variant-scoring path
is **golden-unguarded** (`regression.py` reads `doctrine_score`, never
`score_variant`).

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-017:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion (first reward nudge, live-wired)". **This is the
  default-branch tip** — P-016 MERGED via PR #15; `6c40e2b` is now the base
  (confirmed: `6c40e2b` is an ancestor of HEAD, and is exactly the commit before
  the P-017 active-packet confirmation). (The whole-branch `git merge-base` with
  default is the older shared ancestor `694d19d`, but the effective P-017 base is
  `6c40e2b`.)
- `fecc4e5` — Confirm P-017 as active packet (build-os only, no product change).
- **`1b03ad3`** — "P-017: FINDING — honest depth_cleanup re-curation cannot flip
  density" — the SOLE packet commit. Adds `tests/test_density_recuration.py`
  (+183, 12 tests) only; **`_KIND_SCORES` and all product code byte-untouched.**

Single packet commit (well within ≤2). No product-code commit (the finding forced
it).

## QA proof (exact)

- **Suite: 228 → 240 passed** (+12; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`).
- **Regression: 68/68, 0 critical, 0 warnings** held.
- **Commit-1 (the sole commit) green in isolation:** the new file alone = **12
  passed**.
- **Safety grep: clean.**
- P-012/P-013/P-015/P-016 test files **NOT edited**, and pass (**69**).
- **UI smoke: N/A** (no UI surface touched — tests-only, and no product change).
- **Non-vacuity (adversarial):** injecting an inflated `depth_cleanup` (contrast=88
  + excitement=90, or all dims=100) makes the density guard FAIL on the real
  `analyze()` path (density → `density_A`) — the guard is load-bearing.
- **qa verdict: GREEN — FINDING CONFIRMED.**

## Reviewer verdict

**Pass.** Judged the finding doctrine-HONEST (not a masked search failure): the
residual deficit lives entirely in `excitement`, which is off-limits to inflate,
so no honest dim re-judgment flips density; committing executable arithmetic is
defensible here because the finding IS arithmetic and the variant-scoring path is
golden-unguarded.

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Equilibrium synthesis (the strategic headline — recorded prominently)

THREE independent levers have now all converged on the same place:
- **Penalty layer (P-012/P-015):** saturated — only the `vocal_belief` near-tie
  (gap 1.71 < cap 2.0) was flippable; P-015 made it decisive.
- **Reward/promotion layer (P-016):** saturated at cap 4.0 — only `loop` (gap 3.43)
  was cleanly reachable; P-016 made it decisive. `density` (gap 4.14) unreachable
  + circular gate; `drum_room_bloom` hollow (no evidence signal).
- **Base-value re-curation (P-017):** an honest re-curation cannot flip `density`
  either.

**Conclusion: the judgment layer is at a DOCTRINE-HONEST EQUILIBRIUM.**
`subtractive_drop`'s default dominance is legitimate (subtraction IS the safe
default and genuinely out-scores the alternatives on the ranked axis), and the two
context-overrides — the masked-vocal near-tie (P-015 penalty) and the
foregrounded-loop promotion (P-016 reward) — are the only doctrinally-warranted
flips. **The evidence/re-curation program to make judgment decisive is essentially
COMPLETE; there is no honest further flip move inside the current dimension set.**

## Residue

- **The one remaining honest thread (the single open user-gated question):** the
  only honest further move is a SYMMETRIC re-judgment — is `subtractive_drop` at
  85.29 (high on every dim) itself slightly OVER-valued? Lowering it (rather than
  inflating a rival) would be a different, un-signed-off packet. Out of P-017's
  scope (which fixed `subtractive_drop` untouched). **Recorded as the open
  question; NOT staged.**
- The reward-family (further reward rows) and re-curation-for-flips threads are now
  **CLOSED as saturated / equilibrium.**
- Off-path deferred items carried unchanged: wider `--memory-dir` CLI surface;
  net-new event-logging producers (behind a product decision);
  taste-flip-via-product-change (user-gated, separate packet).

## Open boundaries (awaiting explicit go)

- **P-017 closed with NO product/test-of-product change to runtime code** — the
  ONLY committed change is the tests-only characterization guard (`1b03ad3`) plus
  the `fecc4e5` active-packet confirmation and this build-os close. All sit on the
  dev branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b`
  (PR #15) merge. **`1b03ad3` is local-only at this close.** Any push of it — and
  any subsequent PR / merge into the protected default — needs the user's explicit
  go. **No push / merge / deploy / secret action taken in this close.**

---
_Archivist close, 2026-07-01. Verified negative finding; committed load-bearing guard `1b03ad3`; single-reviewer verdict (Codex unavailable)._
