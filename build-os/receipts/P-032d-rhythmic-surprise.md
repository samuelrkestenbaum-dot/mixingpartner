# Receipt — P-032d — `rhythmic_surprise` (weak form) — fourth producer-agnostic doctrine axis

**Date:** 2026-07-01
**Packet:** P-032d — `rhythmic_surprise` (weak form): the FOURTH new
producer-agnostic doctrine axis — cross-section transient-density variation
(pstdev spread + the largest adjacent section-to-section swing). First packet of
the RESEQUENCED remaining order (d → c → g → f) — the smallest/safest lift (one
input, zero new plumbing), confirmed in practice. Byte-identical for
halee_ramone (weight 0). **The 11th doctrine component.**
**Status:** CLOSED — qa **GREEN**, reviewer **PASS (no must-fix)**.

---

## Scope

**In:**
- **New agnostic scorer** `_rhythmic_surprise(sections_analysis, doctrine)` in
  `doctrine/doctrine_engine.py` (+82) composing, from section-aggregate physics
  only:
  - **Spread** — pstdev of section `transient_density` (the `_dynamic_mix`
    idiom applied to the ONE signal it never reads), scaled by `spread_coeff`.
  - **Largest swing** — max |Δ transient_density| between adjacent sections
    ("the beat drops out / the fill hits" in aggregate form), scaled by
    `swing_coeff`.
  - **Insufficient data** — <2 sections → documented fallback float. Always
    returns a clamped float (never None).
- **Wiring (byte-identical — the established P-032e/a/b pattern):**
  `rhythmic_surprise_score` appended **LAST** to `component_scores` (after
  `groove_coherence_score`; the 10-term summation order preserved → overall
  bit-identical); `evidence["rhythmic_surprise"]`; `halee_ramone.json`
  `doctrine.weights["rhythmic_surprise_score"] = 0` + a
  `doctrine.scorers.rhythmic_surprise` constants block; `producer_profile.py`
  `_validate` requires the `rhythmic_surprise` scorer group;
  `schemas/doctrine_score.schema.json` gains the optional
  `rhythmic_surprise_score` property.
- New `tests/test_rhythmic_surprise.py` (430 lines, +18 tests): byte-identical
  (independent capture), value-discrimination + the FOUR distinctness guards,
  liveness + sabotage, no-aliasing, honest-scope.
- Three pre-existing pins updated for the added axis (`test_producer_profile.py`
  scorers set, `test_doctrine_profile_sourced.py` `_WEIGHTS` pin,
  `test_groove_coherence.py` — groove_coherence now index 9).

**Explicitly OUT (the honesty gate — weak form, deliberately NOT faked):**
- **Deferred in the docstring:** (1) fill detection, (2) unexpected-hit
  detection, (3) per-onset IOI deviation — all need onset timing/sequence
  (groove territory), not visible at `score_doctrine` time.
- **Must NOT read `overall_regularity`** — that is `_groove_coherence`'s input;
  re-reading it here would duplicate that axis. ENFORCED (AST/grep-verified:
  the scorer reads sections + doctrine only).
- No weight change for halee_ramone (weight 0 → byte-identical output).
- No new plumbing — `score_doctrine` already receives `sections_analysis`.

**Distinctness (the design guard):** this is the ONLY axis keyed on the
*variation* of section `transient_density` — `_negative_space` reads its MEAN
(the opposite statistic), `_dynamic_mix` reads pstdev of rms/width/brightness
(never transient_density), `_beat_identity` reads per-STEM transient dominance,
`_groove_coherence` reads onset IOI regularity. A wall-to-wall CONSTANT
transient bed (high mean, zero variance) must score LOW here — proven (below).

**rhythmic_surprise constants:** `insufficient_sections_score 40.0`,
`baseline 20.0`, `spread_coeff 160`, `swing_coeff 60`. Live fixture scores
(weight-0, informational): **51.1** (simple — some sectional variation) /
**20.0** (dense — the real-world high-mean/ZERO-variance constant bed) /
**27.8** (splice).

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base:** set-active `8c03f14` (`build-os: set P-032d
  (rhythmic_surprise) active`), atop `2fdf77d` (P-032b close) → `e9f793f`
  (P-032b product commit).
- **`8a81516`** — P-032d: rhythmic_surprise (weak form) — fourth
  producer-agnostic doctrine axis [single product commit]. 8 files, **535
  insertions / 6 deletions**: `doctrine_engine.py` (+82),
  `producer_profile.py`, `halee_ramone.json`, `doctrine_score.schema.json`,
  `test_rhythmic_surprise.py` (new, 430), + 3 pin updates
  (`test_doctrine_profile_sourced.py`, `test_groove_coherence.py`,
  `test_producer_profile.py`). **One logically-atomic commit; HEAD IS Commit-1
  → green in isolation by construction.**

Parent chain: `8a81516` → `8c03f14` (active-packet confirmation) → `2fdf77d`
(P-032b close) → `e9f793f`.

**Merge base for decisions is still `e79426a` = PR #16** (`git merge-base HEAD
e79426a` = `e79426a` — confirmed; nothing since P-025 has been merged). P-032d
is **local-only**, not pushed/merged.

---

## QA proof (GREEN)

- **Full suite:** 433 → **451 passed** / 0 failed / 0 skipped — base
  independently verified at `8c03f14` in a throwaway worktree (= 433).
- **Regression:** **68/68**, 0 warnings.
- **Commit-1 green in isolation:** HEAD **IS** Commit-1 (single-commit packet),
  so the tip is the isolation point = 451.
- **Byte-identical — INDEPENDENT capture (qa's own, not builder pins):**
  **33/33 pre-existing values × 3 fixtures unchanged** (overalls
  **73.8 / 70.7 / 74.3**).
- **New axis values at weight 0:** `rhythmic_surprise_score` = **51.1 / 20.0 /
  27.8** (informational — zero effect on halee_ramone overall).
- **All 4 distinctness guards pass AND independently recomputed:**
  1. high-mean/zero-variance constant bed → **20.0** (LOW — the design crux);
  2. mean-invisibility — a mean shift alone leaves rs **20.0 == 20.0**;
  3. negative_space-OPPOSITE — ns **78.0** vs rs **20.0** (mean vs variance);
  4. dynamic_mix-DISTINCT — dyn **100.0** vs rs **20.0** (rms/width/brightness
     vs transient_density).
- **Liveness load-bearing:** drop-axis monkeypatch sabotage → liveness **2
  FAILED** / byte-identical **5 passed** — the axis is genuinely wired;
  byte-identical alone would not catch an accepted-but-ignored axis.
- **Safety grep:** **NONE FOUND** (535 insertions / 6 deletions across the 8
  in-packet files).
- **Honest-scope verified:** AST/grep — the scorer reads sections + doctrine
  ONLY; evidence strings say "weak, section-aggregate form";
  fills / unexpected hits / per-onset IOI deferred in the docstring.
- **UI smoke:** N/A (doctrine-engine change, no UI surface).

---

## Reviewer verdict — PASS (no must-fix)

- **Ran THREE own sabotages — ALL caught:**
  - **(A)** hardcode the scorer to a constant → **7**
    discrimination/fallback/evidence tests fail;
  - **(B)** drop the axis from `component_scores` → **3** fail, incl. BOTH
    liveness tests;
  - **(C)** flip the halee weight 0→2 → **8** fail across three guard files.
- **Constants sanity:** smooth mid-range discrimination (swing 0.1 → 34,
  0.3 → 62, 0.5 → 90), clamps at 100 for swings ≳0.57 — consistent with the
  sibling-scorer idiom, not degenerate.
- **Codex NOT available — single-model review.**

---

## Residue (deferred / follow-ups / risks)

1. **NEW (reviewer — cosmetic): liveness-docstring overclaim, now a FOUR-file
   family.** `test_liveness_direction_tracks_the_rhythmic_surprise_score`'s
   docstring overclaims — a hardcoded constant still moves the mean
   directionally; the *discrimination* tests are what catch hardcoding. SAME
   family as the standing note covering `test_beat_identity.py` /
   `test_negative_space.py` (and CHECK `test_groove_coherence.py`). Fold ONE
   docstring sweep across ALL FOUR files into a future doctrine-touching
   packet.
2. **NEW (reviewer — cosmetic): non-adjacent swing under a missing middle
   metric.** In `_rhythmic_surprise`, None-filtering happens BEFORE the
   adjacency zip, so a missing middle `transient_density` would compute a swing
   across NON-adjacent sections. Defensive-only (the pipeline always emits the
   metric) — same future-packet ride-along.
3. **Retained:** the shared-mutable-groove-dict note (`expanded["groove"]` IS
   the doctrine arg — P-032b), the P-032e `spectral_flatness` docstring-drift
   note, and the `_DEFAULT_PROFILE` no-aliasing carry-forward (do NOT mutate a
   loaded profile's structures in place when P-032h loads a second profile).
4. **Retained — scoping-workflow findings for the remaining axes:** P-032c
   needs ZERO new plumbing (P-032d confirmed the same claim in practice);
   P-032c cautions — distinctness-vs-static_mix (POSITIVE relationship vs
   hygiene penalty), presence is a GATE only ("more bass" must not win),
   kick/sub interlock + low-end motif + per-section true-sub movement DEFERRED,
   physics primary / identity labels only a corroborating tie-break; P-032g's
   `creative.py` gate must default to current behavior + needs the
   creative-scores byte-identity surface; P-032f must NOT edit
   `role_classifier.py` in place, caps at `hook_candidate`, defaults to
   protect-as-lead when uncertain.
5. **Resequenced remaining order (recorded in memory):** P-032d ✓ → **P-032c
   (low_end_motion — NEXT)** → P-032g (loop static-vs-iconic) → P-032f
   (vocal-role — HIGH risk, LAST, ★ USER-GATED) → [fold P-031 confidence] →
   P-032h (author `timbaland.json`) → P-032i (differential proof). P-030
   orthogonal/last.

---

## Open boundaries (pending explicit go)

- **No merge / no push handled here.** P-032d's commit `8a81516` is local on
  the dev branch; the orchestrator owns the build-os close commit + push.
  **Merge base to default is still `e79426a` = PR #16 — NOT merged.** No
  deploy, no secrets touched. P-032f remains ★ USER-GATED (needs explicit go on
  the "masked chop/stack = acceptable-blend" aesthetic rule + the conservative
  protect-as-lead-when-uncertain default).

---

## ★ Milestone

**The engine now carries 11 component axes** (7 original + `beat_identity` +
`negative_space` + `groove_coherence` + `rhythmic_surprise`). **4 of the 7
Timbaland "weight up" axes have now landed**, all
append-last / weight-0 / profile-sourced — zero plumbing debt.
