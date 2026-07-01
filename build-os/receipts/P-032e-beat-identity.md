# Receipt — P-032e: `beat_identity` (the first new producer-agnostic doctrine axis)

- **Packet id:** P-032e
- **Title:** `beat_identity` — the FIRST new producer-agnostic doctrine axis and
  the front-loaded CRUX of the Timbaland sub-arc (P-032.x). Measures the
  central-rhythmic-fingerprint **STRENGTH** only.
- **Date closed:** 2026-07-01
- **Status:** CLOSED — qa GREEN, reviewer PASS (single-model; Codex not available).

## Why first (front-loaded)

The Timbaland sub-arc (P-032.x) instantiates the epic's user-gated "first second
producer." The user **front-loaded the hardest/riskiest axis** — beat_identity —
to de-risk the whole sub-arc early: prove the central-rhythmic-fingerprint signal
is *honestly measurable on exported stems* before investing in the easier axes.
Sequencing (user-confirmed): Timbaland axes first; fold the confidence framework
(P-031) in at authoring (P-032h); the rename (P-030) is orthogonal/last.

## Scope

**In:**
- New agnostic scorer `_beat_identity(records, events, doctrine)` in
  `doctrine/doctrine_engine.py`, idiom-matching the existing scorers; constants
  read (read-only, no mutation) from `doctrine["scorers"]["beat_identity"]`.
  Measures fingerprint STRENGTH: agnostic rhythmic-candidate identification by
  transient physics (not by instrument label), presence vs a `no_beat` floor,
  distinctness/dominance above the track median, definition via `crest_factor_db`,
  and a foreground/unmasked bonus (buried/masked → penalty).
- Wiring (byte-identical mechanism): `beat_identity_score` appended **LAST** to
  `component_scores` (preserves the 7-term summation order → overall bit-identical);
  `beat_identity` added to the `evidence` dict.
- `halee_ramone.json`: `doctrine.weights["beat_identity_score"] = 0` (the
  byte-identical anchor — `beat·0` numerator, `+0` denominator → weighted mean
  unchanged) + a `doctrine.scorers.beat_identity` constants block.
- `producer_profile._validate`: required-scorers set now includes `beat_identity`
  so the new axis is structurally bound.
- `doctrine_score.schema.json`: optional `beat_identity_score` property documented
  (schema has no `additionalProperties: false`, so this is documentation only).

**Explicitly OUT (documented in the scorer docstring as P-014-style honest
boundaries — deliberately NOT faked):**
1. **Fingerprint TYPING** (mouth-sound / tabla / synth-knock / beatbox) — not
   measurable on exported stems; do not name what the beat *is*.
2. **Onset REGULARITY / IOI** — a real signal, but it lives in the groove analyzer
   which runs post-doctrine (`pipeline.py:187-197`) and is not visible at
   `score_doctrine` time. Deferred to **P-032b**'s groove live-wire.
3. **"More undeniable after a move"** — needs a before/after render; out of scope
   in plan-only v1.

## Commits (local, branch `claude/logic-mix-os-hardening-12-7hbeh1`)

Branch base `6d34c30` (P-029 close). The two packet commits build atop the
orchestrator's active-packet confirmation `2491f42`:

- **`8239f42`** — Commit-1: `_beat_identity` scorer + `doctrine.scorers.beat_identity`
  constants + `weights.beat_identity_score = 0` in `halee_ramone.json` +
  `producer_profile._validate` required-scorers now includes `beat_identity` + new
  `tests/test_beat_identity.py` (12 tests) + 2 guard updates
  (`test_producer_profile.py` scorer-set, `test_doctrine_profile_sourced.py`
  `_WEIGHTS` value-pin). 6 files, +409/−3.
- **`9d6764e`** — Commit-2: `doctrine_score.schema.json` adds the optional
  `beat_identity_score` property (documentation). 1 file, +1.

Parent chain: `9d6764e` → `8239f42` → `2491f42` (active-packet confirm) →
`6d34c30` (P-029 close, base). `git merge-base HEAD 6d34c30 = 6d34c30` (confirmed).

## beat_identity constants (chosen)

`no_beat 20.0, transient_floor 0.35, baseline 50.0, dominance_coeff 40,
definition_crest_db 12.0, definition_bonus 12, foreground_bonus 18,
buried_penalty 14, masked_penalty 12`.

Live fixture scores (weight-0, informational): **89.1 / 52.7 / 46.0** across the 3
fixtures — a sensible discriminating spread. **Zero effect on the halee_ramone
overall** (weight 0).

## QA proof (GREEN)

- **Full suite:** 384 → **396 passed** / 0 failed / 0 skipped (0 warnings).
- **Regression:** **68/68**, 0 warnings, 0 critical.
- **Commit-1 green in isolation:** verified in a throwaway worktree @ `8239f42` —
  **396 / 68-68** — the shared HEAD never moved.
- **Byte-identical:** **0/24 mismatches** vs clean base `6d34c30` (overalls
  73.8 / 70.7 / 74.3 unchanged across the 3 fixtures).
- **Liveness load-bearing:** a non-zero `beat_identity_score` weight moves the
  `analyze()` overall and its direction tracks the beat score; sabotage
  (hardcode beat / drop the threading) FAILS the liveness tests while byte-identical
  stays green — verified in isolation (the P-016/P-029 lesson).
- **Safety grep:** clean — no secrets / destructive / network / auto-apply.
- **Honest-scope:** confirmed — candidacy by transient physics only (no instrument
  labels, no onset regularity/IOI, no before/after render).
- **UI smoke:** N/A (no UI surface in this packet).

## Reviewer verdict — PASS

All 7 scrutiny points pass:
1. Byte-identical mechanism proven numerically (over 100k trials).
2. Honesty gate genuine (the three deferrals are real boundaries, not faked signal).
3. Liveness verified load-bearing — an in-memory sabotage failed the liveness tests
   while byte-identical stayed green (byte-identical alone would NOT catch an
   accepted-but-ignored axis).
4. Agnostic-first (physics/measurement hardcoded & agnostic; only *weights* live
   in the profile).
5. No-aliasing (scorer only reads `doctrine[...]`; never mutates the profile).
6. Guard updates are legitimate tightening, not loosening (the weight-dict pin and
   the scorer-set assertion both widen to include the new axis).
7. Product Trajectory Check — pass.

**No must-fix items.** **Single-model review — Codex NOT available (not on PATH).**

## ★ MILESTONE

The engine now has its FIRST new producer-agnostic measurement axis beyond the
original Halee/Ramone set — the capacity to *hear* a Timbaland-relevant dimension
— added byte-identically for the reference producer. **The producer-agnostic
architecture (P-029) is now proven EXTENSIBLE, not just parameterizable.**

## Residue / follow-ups

- **Docstring drift (non-blocking):** `_beat_identity`'s docstring says candidacy
  is "optionally corroborated by crest/spectral_flatness" but the body reads only
  `crest_factor_db`, never `spectral_flatness`. The spec made flatness optional, so
  this is harmless — **fold a one-line docstring fix into a future doctrine-touching
  packet** rather than spending a commit now.
- **`_DEFAULT_PROFILE` singleton no-aliasing carry-forward** still applies whenever
  a second live profile is loaded per call (do not mutate a loaded profile's
  structures in place) — now reinforced by beat_identity's two no-aliasing tests.
- **Next in the sub-arc:** **P-032a (negative_space)** — lowest-risk, all inputs
  already visible to doctrine.

## Open boundaries (pending explicit go)

- **P-032e is local-only** on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1`
  (commits `8239f42` + `9d6764e`). **NOT merged.** The base for merge decisions is
  still **`e79426a` = PR #16**. No push/merge/deploy performed by the archivist; the
  orchestrator handles push under the standing push-go to the dev branch. No merge
  without explicit go.
