# P-028 — Source `doctrine_engine.py`'s producer constants from the reference profile (byte-identical, WIDENED — the last & largest extraction)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. **FOURTH and FINAL extraction step**
of the **producer-agnostic epic** — it COMPLETES the extraction phase. P-025
extracted the reference profile; P-026 sourced `creative.py`; P-027 sourced
`governance.py` (widened); **P-028 sources `doctrine_engine.py` (widened, the last
& largest) — so the entire producer-specific judgment layer is now profile-driven.**
**Type:** Build / feature — in authority, byte-identical. No new decision (the
byte-identical relocation + widening is guarded by P-025's round-trip + the 68/68
regression + the existing doctrine tests passing UNEDITED). No honesty-decision
needed — this is a VERBATIM relocation of today's values, not authoring a new
profile.

---

## Title / what it does (the mechanism)

`doctrine_engine.py` now SOURCES its producer-specific aesthetic constants FROM the
reference profile (`doctrine/producers/halee_ramone.json`) instead of hardcoded
literals, AND the profile is WIDENED to hold the 5 remaining doctrine scoring
functions' constants that were inline literals — making the JSON their **single
source of truth.** **Byte-identical by construction** (the reference profile == the
old literals, per P-025's round-trip + the byte-identical proof below). The
producer-AGNOSTIC physics/measurement code STAYS in the functions — only the
aesthetic numbers moved.

### Part A — source doctrine's ALREADY-captured (P-025) values from the profile
- **`_DEFAULT_PROFILE = load_profile("halee_ramone")`** — added once at module level.
- `score_doctrine`'s component **weights** (halee 1.0 / ramone 1.2 /
  vocal_centrality 1.2 / depth 1.0 / contrast 1.0 / static 1.0 / dynamic 0.8) now
  read from `_DEFAULT_PROFILE.doctrine.*`.
- `_halee` / `_ramone` **baselines (86.0)** + their **penalty coefficients** read
  from the profile instead of inline literals.
- These are the values P-025 already captured and round-trip-guarded; Part A moves
  the SOURCE behind `_DEFAULT_PROFILE` — the physics/measurement code stays in the
  functions, so the formula shape and evaluation order are byte-identical.

### Part B — WIDEN the profile with the 5 remaining scorers' constants (Finding A)
Extended `ProducerProfile` + `halee_ramone.json` (new `doctrine.scorers` group, 5
function groups) + the loader validation (requires `doctrine.scorers` and its five
function groups) + the round-trip test, capturing each constant VERBATIM, then
SOURCED each scorer from `_DEFAULT_PROFILE.doctrine["scorers"]`:
- **`_vocal_centrality`:** no_lead `35.0`, baseline `70.0`, sacred_bonus `10`,
  forward_bonus `10`, masked_coeff `6`.
- **`_depth_hierarchy`:** baseline `40`, per_distinct `12`, forward_threshold
  `0.6`, forward_occupancy `60`.
- **`_section_contrast`:** baseline `100`, lift_fail_penalty `18`.
- **`_static_mix`:** baseline `80.0`, peak_ceiling `-0.1`, peak_penalty `10`,
  dominant_band_threshold `0.55`, dominant_band_penalty `10`, crit_low_coeff `8`,
  no_lead_penalty `8`.
- **`_dynamic_mix`:** insufficient_sections_score `40.0`, baseline `30`, rms_coeff
  `8`, width_coeff `140`, bright_coeff `140`, lift_fail_penalty `10`.

### The physics / aesthetic boundary (load-bearing — what did NOT move)
Only the aesthetic CONSTANTS moved to the profile. The PHYSICS/measurement code
stays IN the functions — `fg_frac` computation, band max, `pstdev` spread, distinct
depth-band counting, section detection, and the measurement/presentation thresholds
(`stereo_width > 0.6`, `distinct <= 1`, the `score < 55` evidence gate). The formula
SHAPE and float order are preserved; int/float types match the originals. Clean
literal→`c["…"]` substitution — the formula's numeric result is unchanged.

---

## Scope (in / explicitly out)

**In:**
- `doctrine_engine.py`: `_DEFAULT_PROFILE` load + all 8 scorers read their aesthetic
  constants from `_DEFAULT_PROFILE.doctrine.*` (Part A) and
  `_DEFAULT_PROFILE.doctrine["scorers"]` (Part B).
- `producer_profile.py`: `ProducerProfile` + loader widened for `doctrine.scorers`
  (5 function groups) + validation.
- `halee_ramone.json`: the `doctrine.scorers` group captured VERBATIM.
- New `tests/test_doctrine_profile_sourced.py` (sourcing pins, value pins, behavior
  pins, no-aliasing proof, determinism).
- `tests/test_producer_profile.py`: extended with the `doctrine.scorers` round-trips
  (exact value pins + drive-the-function indirect round-trip).

**Explicitly out:**
- `creative.py` (done, P-026), `governance.py` (done, P-027), `pipeline.py`
  (P-029) — **byte-unchanged.**
- No per-call producer threading (that is P-029). No signature/mechanism change.
- The physics/measurement code and the safety/presentation thresholds stay
  hardcoded (producer-agnostic).

---

## Commits (≤2) and branch base

Branch base (merge-base): **`e79426a`** (Merge PR #16: Cowork-usable end-to-end;
current default-branch tip). Dev branch: `claude/logic-mix-os-hardening-12-7hbeh1`.

- **`29b9dfe`** — Source doctrine_engine's already-captured weights/halee/ramone
  from the profile (P-028 Part A, byte-identical). `doctrine_engine.py` (+32/−20)
  + new `tests/test_doctrine_profile_sourced.py` (+240). **Green in isolation = 364.**
- **`72e98a7`** (HEAD) — Widen the profile with the 5 remaining doctrine scorers'
  constants and source them (P-028 Part B, byte-identical). `producer_profile.py` +
  `halee_ramone.json` + `doctrine_engine.py` (the 5 scorers) + extended
  `tests/test_producer_profile.py` round-trips.

Parent chain: `72e98a7` → `29b9dfe` → `d5260a6` (active-packet confirmation) →
`23850f7` (P-027 close) → … → `e79426a` (base). **P-028 is local-only** (both
commits on the dev branch on top of the `e79426a` base), NOT pushed/merged/deployed.

---

## QA proof (exact, verified by qa + reviewer)

- **Full suite: 351 → 370 passed (+19)** — 0 failed / 0 skipped / 0 warnings, green
  under `-W error`. Existing doctrine tests pass **UNEDITED**.
- **Commit-1 green in isolation = 364** (`29b9dfe` alone: Part A source +
  no-aliasing test).
- **Regression: 68/68, 0 critical, 0 warnings — UNCHANGED** — the corpus-level
  byte-identical proof (doctrine feeds `doctrine_score`, which the golden pins).
  Reviewer INDEPENDENTLY confirmed the live `doctrine_score` byte-matches the golden
  on all 3 fixtures, INCLUDING `overall_mix_readiness_score`.
- **Round-trip NON-VACUOUS:** an `18 → 17` flip of a captured constant fails the
  round-trip test AND shifts `_section_contrast` `64 → 66` — proving the sourced
  constant is load-bearing, not decorative.
- **No-aliasing PROVEN (the per-module safety invariant — DISCHARGED for doctrine):**
  grep confirmed no in-place mutation of the sourced structures; the no-aliasing
  test runs `score_doctrine` on a fixture (+ crafted multi-penalty inputs) and
  asserts the shared `_DEFAULT_PROFILE` structures are byte-unchanged afterward.
  Determinism holds.
- **Physics NOT moved:** the formula shapes are intact; the measurement/presentation
  thresholds (`stereo_width > 0.6`, `distinct <= 1`, `score < 55`) stay in the
  functions.
- **Scope clean:** `creative.py` / `governance.py` / `pipeline.py` untouched.
- **Safety grep:** CLEAN. **UI smoke:** N/A (no UI surface).

---

## Reviewer verdict

**PASS.** Reviewer independently confirmed the live `doctrine_score` (incl.
`overall_mix_readiness_score`) byte-matches the golden on all 3 fixtures, judged the
literal→`c["…"]` substitution clean (formula shape/order preserved, int/float types
match), and verified the physics/aesthetic boundary is honest (only aesthetic
constants moved; the `stereo_width > 0.6` / `distinct <= 1` / `score < 55`
thresholds are correctly left hardcoded as physics/presentation, not producer
taste). No-aliasing discharged. **Codex second-eyes: NOT available — single-reviewer
verdict** (consistent with P-025→P-027).

---

## MILESTONE recorded — the EXTRACTION PHASE is COMPLETE

**The entire producer-specific judgment layer — creative (P-026), governance
(P-027, widened), doctrine (P-028, widened) — is now sourced from the reference
`ProducerProfile`, BYTE-IDENTICAL, with the producer-AGNOSTIC physics chassis +
safety kill-switches cleanly separated and left hardcoded.** The reference profile
now FULLY DRIVES the judgment layer.

- **Finding A is now FULLY RESOLVED** — governance's secondary constants (P-027) and
  doctrine's 5-scorer constants (P-028) are all captured. No further deferred
  producer-aesthetic capture remains.
- **The aliasing-proof requirement is DISCHARGED for all three consumer modules**
  (creative P-026, governance P-027, doctrine P-028) — each independently proved its
  consumers never mutate a sourced global in place.
- **The producer-agnostic physics chassis stays hardcoded** — analyzers, the 5
  SAFETY kill-switches (governance `_SAFETY_KILL_SWITCHES`), the bounded-nudge
  mechanism, the determinism/evidence contract, and the doctrine
  measurement/presentation thresholds are all left as producer-AGNOSTIC universals.

---

## Residue — deferred / follow-ups / risks

- **NEXT — P-029 (the pivot): parameterize the pipeline by a per-call producer.**
  Thread a per-call `producer` through the pipeline so `analyze(producer=...)`
  SELECTS a profile — the profile stops being a mirror of today's hardcoded values
  and becomes a LIVE lever. Default = the `halee_ramone` reference, byte-identical
  (guarded by the P-025 round-trip + 68/68 regression). P-029 is ALSO the structural
  fix that ends the shared-module-singleton aliasing risk (the per-call profile
  removes the shared-mutable-global).
- **Epic arc after P-029:** P-030 (rename the `halee`/`ramone` dims off the producer
  names) → P-031 (confidence framework — consume the metadata stamp per the honesty
  policy) → P-032 (second producer — first real test of producer-agnosticism,
  governed by the honesty policy) → P-033 (expose producer selection).
- **Reviewer observation (carry into P-029):** a few measurement-vs-aesthetic
  thresholds (`stereo_width > 0.6`, `distinct <= 1`, `score < 55`) are correctly
  left hardcoded as physics/presentation, NOT producer taste — keep them out of the
  profile when P-029 threads the profile per-call.
- **Standing honesty/sourcing policy (governs P-031/P-032):** hand-curated → high
  confidence; derived → low (labeled); LLM → draft-only, NEVER high. No LLM-authored
  profile may claim `high` confidence.
- **Trailer-spec standing note:** OMIT the "NO model identifier" constraint line from
  future packet specs — it conflicts with the mandated `Co-Authored-By: Claude Opus
  4.8` trailer and keeps tripping the reviewer.

---

## Open boundaries (pending explicit go)

- **Merge to default: PENDING explicit go.** P-028 (`29b9dfe`, `72e98a7`) is
  local-only on the dev branch; NOT pushed/merged/deployed. The accumulated
  producer-agnostic epic (P-025 → P-028) plus the earlier local-only arc remain
  un-landed on default, awaiting a user-gated merge decision.
- No push, merge, deploy, publish, or secret access performed in this close.
