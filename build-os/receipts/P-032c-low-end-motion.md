# Receipt — P-032c — `low_end_motion` (the low-end POCKET) — fifth producer-agnostic doctrine axis

**Date:** 2026-07-01
**Packet:** P-032c — `low_end_motion`: the FIFTH new producer-agnostic doctrine
axis — the low-end POCKET (kick/sub relationship + room around the bass). **A
producer-profile PRIMITIVE under the pinned architecture doctrine** (axes =
shared measurable substrate; taste = weighting layer; safety invariant).
Different profiles will interpret it differently — Timbaland:
pocket/impact/negative-space/sub-kick; Halee/Ramone: balance/natural
foundation; modern pop: translation/controlled sub density; trap: sub
identity/808 envelope/space around transient — **this interpretation table is
in the scorer docstring.** Byte-identical for halee_ramone (weight 0). **The
12th doctrine component.**
**Status:** CLOSED — qa **GREEN**, reviewer **PASS** — dual-green against the
USER'S explicit acceptance invariant.

---

## Scope

**In:**
- **New agnostic scorer** `_low_end_motion` in `doctrine/doctrine_engine.py`
  (+211) composing: a **presence GATE** (band_energy.low, the 20–120 Hz sub
  fraction, is ONLY ever compared against `low_floor`/`stack_floor` — never
  multiplied into the score; no carrier and no mix fallback above the floor →
  documented `no_low_end` 25; no signal at all → documented `neutral` 40); a
  **QUALIFIED reserved-sub/room term** (few carriers read as reserved room ONLY
  when clean of critical collision AND with a defined, non-smeared envelope —
  crest ≥ `defined_crest_db` 10.0; one giant muddy blob takes `blob_penalty`
  instead; a pile-up over `reserved_max` is penalized per stem); and the **weak
  relationship form** (low_end_conflict events penalized by severity +
  complementary punch-vs-sustain crest gap among carriers, capped). Always a
  clamped float.
- **Wiring (byte-identical — the established P-032e/a/b/d pattern):**
  `low_end_motion_score` appended LAST to `component_scores` (12-term summation
  order preserved); `halee_ramone.json` weight 0 + a
  `doctrine.scorers.low_end_motion` constants block; `producer_profile.py`
  `_validate` required-scorers; `doctrine_score.schema.json` optional property.
- New `tests/test_low_end_motion.py` (598 lines, +22 tests): byte-identical
  (independent capture), the acceptance-invariant suite (mud-loses,
  blob-loophole, presence-leakage, static_mix distinctness), liveness/sabotage,
  no-aliasing, honest-scope.
- Pin updates: `test_producer_profile.py` scorers set,
  `test_doctrine_profile_sourced.py` `_WEIGHTS` pin,
  `test_rhythmic_surprise.py` (index shift).

**Explicitly OUT (honest deferrals — in the docstring, NOT faked):**
- Kick/sub temporal interlock (bass excluded from `RHYTHM_IDENTITIES` — no
  bass onsets available).
- Low-end motif detection.
- Per-section true-sub movement (sections expose `low_mid` only).
- No weight change for halee_ramone (weight 0 → byte-identical output). No new
  plumbing.

**Physics primary:** `identity_family` is a corroborating tie-break only;
`instrument_identity` is never read; `sections_analysis` accepted per the
established signature, 0 reads, documented.

**USER'S ACCEPTANCE INVARIANT (all proven):** a clean low-end relationship
BEATS high low-end quantity —
1. **Mud loses despite MORE bass:** total low 4.40 vs 1.22, 6 carriers, 2
   criticals → **0.0** vs clean pocket **80.0**.
2. **Blob loophole CLOSED (fewer-carriers direction):** a single smeared blob
   (1 carrier, per-stem low 0.95) → **28.0**, colliding → **14.0**, both < the
   SAME solo carrier clean+defined → **60.0** — the reservation is QUALIFIED by
   pocket behavior (crest ≥ 10 dB AND no critical collision), never carrier
   count.
3. **Presence leakage FENCED:** boosted-low variants EXACT-equal
   (80.0 == 80.0, 60.0 == 60.0).
4. **static_mix distinctness:** 4-pad pile-up with no conflicts → static
   **80.0** (healthy hygiene) vs lem **16.0** (no pocket) — orthogonal axes,
   not a re-derivation.
5. **Byte-identity:** overalls **73.8 / 70.7 / 74.3** untouched.

**Constants (`doctrine.scorers.low_end_motion`):** `low_floor`/`stack_floor`
0.2, `baseline` 40, `reserved_bonus` 20 (`reserved_max` 2), `defined_crest_db`
10.0, `blob_penalty` 12, `stack_penalty` 12, `critical`/`moderate`
conflict penalties 14/6, `complement_coeff` 2.0 (cap 12 dB), `no_low_end` 25,
`neutral` 40. **Score landscape:** clean pocket 80 > defined solo 60 >
pile-with-spread 52 > neutral 40 > any-critical ≤ 38 > blob 28 > no_low_end 25
> worst mud 0. **Design note: the theoretical ceiling is 84 (40+20+24), never
100** — fine, but relevant when authoring `timbaland.json` weights (P-032h).

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base:** set-active `fe5f6b4` (`build-os: set P-032c (low_end_motion)
  active`); parent of the product commit is `b7e116a` (`build-os: pin the
  user-issued architecture doctrine into memory` — build-os-only, so the code
  base is effectively `fe5f6b4`), atop `89e7106` (P-032d close).
- **`ab14ac7`** — P-032c: low_end_motion (pocket) — fifth producer-agnostic
  doctrine axis [single product commit]. 8 files, **837 insertions / 4
  deletions**: `doctrine_engine.py` (+211), `producer_profile.py`,
  `halee_ramone.json`, `doctrine_score.schema.json`, `test_low_end_motion.py`
  (new, 598), + pin updates (`test_doctrine_profile_sourced.py`,
  `test_producer_profile.py`, `test_rhythmic_surprise.py`). **One
  logically-atomic commit; HEAD IS Commit-1 → green in isolation (473).**

Parent chain: `ab14ac7` → `b7e116a` (doctrine pin, build-os only) → `fe5f6b4`
(active-packet confirmation) → `89e7106` (P-032d close).

**Merge base for decisions is still `e79426a` = PR #16** (`git merge-base HEAD
e79426a` = `e79426a` — confirmed; nothing since P-025 has been merged). P-032c
is **local-only**, not pushed/merged.

**Trailer note:** the commit carries `Co-Authored-By: Claude Fable 5` — the
harness-sanctioned attribution for the current session model (the mandate
changed mid-session); accepted by the orchestrator; parallel to the earlier
Opus-4.8 reconciliation. Future packets use the current harness trailer; do
not re-flag.

---

## QA proof (GREEN)

- **Full suite:** 451 → **473 passed** / 0 failed / 0 skipped (+22; base
  independently verified at `fe5f6b4`).
- **Regression:** **68/68**, 0 warnings.
- **Commit-1 green in isolation:** HEAD **IS** Commit-1 (single-commit packet),
  so the tip is the isolation point = 473.
- **Byte-identical — INDEPENDENT capture (qa's own, not builder pins):**
  **36/36 pre-existing values repr-identical × 3 fixtures** (overalls
  **73.8 / 70.7 / 74.3** untouched).
- **New axis values at weight 0:** `low_end_motion_score` = **60.0 / 21.1 /
  25.0** (simple: single reserved clean carrier / dense: critical kick-bass
  collisions break the pocket / splice: no_low_end gate) — informational, zero
  effect on halee_ramone overall.
- **Sabotage — both directions load-bearing:** DROP the axis → **2 liveness
  FAIL** / anchors PASS; HARDCODE the scorer → **4 discrimination FAIL** /
  anchors PASS.
- **Acceptance invariant:** all five clauses of the user's invariant proven
  (exact values above in Scope).
- **Safety grep:** **NONE FOUND** (837 insertions / 4 deletions across the 8
  in-packet files).
- **Honest-scope verified:** `identity_family` = tie-break only;
  `instrument_identity` never read; `sections_analysis` accepted per the
  signature, 0 reads, documented; deferrals in the docstring.
- **UI smoke:** N/A (doctrine-engine change, no UI surface).

---

## Reviewer verdict — PASS (adversarial proof — the strongest close of the arc)

- **AST analysis:** the low-band level appears in **ZERO arithmetic nodes**,
  only **2 threshold comparisons** — level structurally CANNOT leak into the
  score.
- **20,000-configuration adversarial search:** max score with ANY critical
  collision = **38.0** (below the 40.0 baseline); maxed-out mud = **0.0** vs
  **80.0**.
- **Structural bound:** only the QUALIFIED reserve can push past 64, so no
  quantity-beats-relationship path exists.
- **Ran THREE own sabotages — ALL caught:** hardcode / drop / weight-flip.
- **Codex NOT available — single-model review.**

---

## Residue (deferred / follow-ups / risks)

1. **Liveness-docstring-overclaim family now spans FIVE test files:** add
   `tests/test_low_end_motion.py:518-526` to the standing note covering
   `test_beat_identity.py`, `test_negative_space.py`,
   `test_rhythmic_surprise.py` (+ CHECK `test_groove_coherence.py`). Fold ONE
   docstring sweep into a future doctrine-touching packet.
2. **NEW ride-alongs:** lem's 84-point theoretical ceiling (relevant to
   `timbaland.json` weight authoring) + the defensive `r.get("metrics",{})`
   None edge — same future-doctrine-packet ride-along bucket.
3. **Retained:** the shared-mutable-groove-dict note (P-032b), the P-032e
   `spectral_flatness` docstring drift, the `_DEFAULT_PROFILE` no-aliasing
   carry-forward (P-032h loads a second profile), the P-032d non-adjacent-swing
   defensive note, and the scoping findings for P-032g/f.
4. **P-032g staging notes (USER-MANDATED, binding):** the SECOND byte-identity
   surface is **NOT optional** — qa must prove BOTH (a) doctrine overall
   byte-identical AND (b) **creative variant scores + `loop_deconstruct`
   promotion firing behavior byte-identical under Halee/Ramone defaults** (the
   risk is the recommendation engine subtly changing behavior before
   `timbaland.json` turns the interpretation on). Engine language must be
   OBSERVATIONAL (dominant+no-evolution = static;
   dominant+groove/fingerprint-function = iconic) with zero judgment words; the
   profile decides deconstruct-vs-protect via a flag defaulting to CURRENT
   behavior.
5. **Resequenced remaining order (recorded in memory):** P-032c ✓ → **P-032g
   (loop static-vs-iconic — THE HINGE, NEXT)** → P-032f (vocal-role — HIGH
   risk, LAST, ★ USER-GATED) → [fold P-031 confidence] → P-032h (author
   `timbaland.json`) → P-032i (differential proof). P-030 orthogonal/last.

---

## Open boundaries (pending explicit go)

- **No merge / no push handled here.** P-032c's commit `ab14ac7` is local on
  the dev branch; the orchestrator owns the build-os close commit + push.
  **Merge base to default is still `e79426a` = PR #16 — NOT merged.** No
  deploy, no secrets touched. P-032f remains ★ USER-GATED (needs explicit go on
  the "masked chop/stack = acceptable-blend" aesthetic rule + the conservative
  protect-as-lead-when-uncertain default).

---

## ★ Milestone

**The engine now carries 12 component axes** (7 original + `beat_identity` +
`negative_space` + `groove_coherence` + `rhythmic_surprise` +
`low_end_motion`). **5 of the 7 Timbaland "weight up" axes have now landed**,
all append-last / weight-0 / profile-sourced — zero plumbing debt. This packet
also closed dual-green against a USER-STATED acceptance invariant, with the
reviewer's AST + 20k-configuration adversarial proof as the strongest close of
the arc.
