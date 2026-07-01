# Receipt — P-032a — `negative_space` (second producer-agnostic doctrine axis)

**Date:** 2026-07-01
**Packet:** P-032a — `negative_space`: the SECOND new producer-agnostic doctrine
axis of the Timbaland sub-arc (after the P-032e `beat_identity` crux). Measures
**absolute arrangement room/sparsity** ("silence is arrangement"), deliberately
DISTINCT from `_dynamic_mix` (which measures section-to-section movement).
**Status:** CLOSED — qa **GREEN**, reviewer **PASS**.

---

## Scope

**In:**
- New agnostic scorer `_negative_space(records, sections, mix_metrics, doctrine)`
  in `doctrine/doctrine_engine.py` → `(score_0_100, evidence_list)`, composing
  ABSOLUTE ROOM as a STRENGTH from section-aggregate physics: low mean section
  spectral `density` (room), a genuine dropout section (`min_section_density` /
  min RMS meaningfully below max — "silence as arrangement"), and transient
  breathing room (low mean section `transient_density`). Always returns a clamped
  float (documented neutral fallback when no section/mix data) — mirrors
  `_beat_identity`'s always-float discipline.
- Wired into `score_doctrine` as `negative_space_score` appended **LAST** to
  `component_scores` (after `beat_identity_score`) → summation order preserved →
  overall bit-identical; matching `evidence["negative_space"]`.
- `halee_ramone.json`: `doctrine.weights["negative_space_score"] = 0`
  (byte-identical anchor) + a `doctrine.scorers.negative_space` constants block.
- `producer_profile._validate`: `negative_space` added to the required-scorers
  tuple (structurally bound; already includes `beat_identity` from P-032e).
- `schemas/doctrine_score.schema.json`: optional `negative_space_score` property
  (documentation; schema has no `additionalProperties: false`).
- New `tests/test_negative_space.py` (17 tests): byte-identical,
  value-discrimination (incl. the distinctness-from-dynamic_mix guard), liveness
  (load-bearing), no-aliasing.
- Three doctrine-key-pin updates for the new axis: `test_producer_profile.py`
  (scorers set), `test_doctrine_profile_sourced.py` (`_WEIGHTS` value-pin),
  `test_beat_identity.py` (`beat_identity_score` now index 7, no longer the tail).

**Explicitly OUT (honest deferral, documented in the scorer docstring — NOT
faked):**
- Sample-level **inter-onset silence gaps** (space between individual hits) need
  onset timing, which is not visible at `score_doctrine` time (it lives in the
  post-doctrine groove analyzer). Deferred to **P-032b**'s groove live-wire.
  `negative_space` works at the **section-aggregate grain only** — no instrument
  labels, no onset timing, no post-doctrine analyzers.

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base:** `6d34c30` (P-029 close), atop set-active `836bd22`
  (`build-os: set P-032a (negative_space) active`).
- **`3edcd9c`** — Add `negative_space` — the second producer-agnostic doctrine
  axis (absolute arrangement room/sparsity, byte-identical for halee_ramone)
  [P-032a Commit 1]. Scorer + `doctrine.scorers.negative_space` constants +
  `weights.negative_space_score=0` + `_validate` requires `negative_space` +
  `tests/test_negative_space.py` (17 tests) + 3 doctrine-key-pin updates.
  **One logically-atomic commit; no Commit-2 needed.**

Parent chain: `3edcd9c` → `836bd22` (active-packet confirmation) → `8a2892b`
(P-032e close) → `9d6764e` (P-032e Commit 2).

**Merge base for decisions is still `e79426a` = PR #16** (`git merge-base HEAD
e79426a` = `e79426a` — confirmed; nothing since P-025 has been merged). P-032a is
**local-only**, not pushed/merged.

---

## QA proof (GREEN)

- **Full suite:** 396 → **413 passed** / 0 failed / 0 skipped (green under
  `-W error`; `test_negative_space.py` = 17 tests).
- **Regression:** **68/68**, 0 warnings, 0 critical.
- **Commit-1 green in isolation:** HEAD **IS** Commit-1 (single-commit packet),
  so the tip is the isolation point = 413.
- **Byte-identical:** **0 mismatches / 27 comparisons** vs base `836bd22`
  (overalls **73.8 / 70.7 / 74.3** unchanged across all 3 fixtures).
- **Distinctness PROVEN (non-tautological):** dense-but-moving case →
  `dynamic_mix = 100.0` vs `negative_space = 15.0` — an **85-pt gap**, genuinely
  orthogonal (a wall-to-wall-dense mix that varies section-to-section scores HIGH
  on dynamic_mix but LOW on negative_space).
- **Liveness load-bearing (both ways):** a profile weighting `negative_space_score`
  non-zero moves `analyze()` overall; **drop the threading → liveness FAIL
  (KeyError); hardcode the constant → 8 fail + 5 err; byte-identical stays green**
  — byte-identical alone would NOT catch an accepted-but-ignored axis (the
  P-016/P-029 lesson honored).
- **Live fixture scores (weight-0, informational):** **62.3** (roomy
  simple_vocal_piano) / **15.0** (dense_chorus) / **20.0** (splice) — sparse ≥ 75,
  wall-to-wall ≤ 35, neutral fallback 40. **Zero effect on halee_ramone overall**
  (weight 0).
- **Safety grep:** clean.
- **Honest-scope:** confirmed (section-aggregate; no instrument labels; no
  onset timing).
- **UI smoke:** N/A (doctrine-engine change, no UI surface).

**negative_space constants chosen:** `neutral 40.0, baseline 15.0,
density_ceiling 1.0, room_coeff 50, transient_ceiling 1.0, breathing_coeff 20,
dropout_coeff 25, dropout_floor 0.1`.

---

## Reviewer verdict — PASS

All **8** scrutiny points pass:
1. byte-identical empirically proven base→HEAD;
2. distinctness non-tautological (85-pt dynamic_mix vs negative_space gap);
3. honesty gate genuine (sample-level gaps deferred in-docstring, not faked);
4. liveness load-bearing at suite level;
5. agnostic-first — all 8 tunables live in the profile;
6. no-aliasing (scorer only reads `doctrine[...]`, never mutates);
7. guard updates are legitimate tightening (index shift + scorers set + weights
   pin);
8. Product Trajectory Check pass.

**No must-fix items.** **Single-reviewer — Codex NOT available.**

---

## Residue (deferred / follow-ups / risks)

1. **NEW non-blocking note (reviewer) — liveness docstring overclaim in TWO
   files:** the two `liveness` test docstrings in `tests/test_negative_space.py`
   (~lines 536-540, 553-557) OVERCLAIM — a general hardcoded-constant sabotage is
   actually caught by the *discrimination* tests, not the liveness tests
   themselves (the direction test reads the score from the same reference dict a
   constant poisons). The SAME imprecision exists in the already-closed
   `tests/test_beat_identity.py`. **Cosmetic only** (the guard SET as a whole is
   sound); fold a one-line docstring fix for BOTH files into a future
   doctrine-touching packet.
2. **Retained:** the P-032e docstring-drift note (`_beat_identity` docstring says
   candidacy is "optionally corroborated by crest/spectral_flatness" but the body
   reads only `crest_factor_db`, never `spectral_flatness` — harmless, flatness
   was optional; fold into a future doctrine touch).
3. **Retained:** the `_DEFAULT_PROFILE` no-aliasing carry-forward — the module
   singleton still exists as the `None`-default fallback in all 3 consumer
   modules; when a SECOND live profile is loaded per call (P-032h), do NOT mutate
   a loaded profile's structures in place.
4. **NEXT in the sub-arc — P-032b (`groove_coherence` live-wire), the RISKIER
   packet:** it relocates `analyze_groove` to BEFORE `score_doctrine` and threads
   it in (the P-016 live-wire lesson: an evidence-gated signal is only live if
   computed before its consumer; needs a no-re-run live-wire test asserting on
   real `analyze()` output), then adds the groove-coherence scorer. This is where
   onset-regularity/IOI (deferred from P-032e AND P-032a) finally reaches
   doctrine.

---

## Open boundaries (pending explicit go)

- **No merge / no push handled here.** P-032a's commit `3edcd9c` is local on the
  dev branch. The orchestrator owns push; **merge base to default is still
  `e79426a` = PR #16 — NOT merged.** No deploy, no secrets touched.

---

## ★ Milestone

The engine now carries **9 component axes** (7 original + `beat_identity` +
`negative_space`), the second added byte-identically for the reference producer.
The producer-agnostic architecture (P-029) continues to prove **extensible**, not
just parameterizable.
