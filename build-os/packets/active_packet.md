# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed, handed to builder
- **Packet id:** P-032a
- **Title:** `negative_space` — second new producer-agnostic doctrine axis
  (absolute arrangement room/sparsity); byte-identical for halee_ramone.

## Why this packet

Second axis of the Timbaland sub-arc, after the P-032e crux proved the
add-an-agnostic-axis-byte-identically pattern. Lowest-risk of the remaining
axes: all inputs are already visible to `score_doctrine`. "Silence is
arrangement" (user framing) → measure the arrangement leaving room.

## Distinctness (the design guard — do NOT duplicate dynamic_mix)

`dynamic_mix` already measures section-to-section MOVEMENT (pstdev of
rms/width/brightness + lift-fail). **negative_space measures ABSOLUTE ROOM** — a
different thing: low spectral occupancy + a genuinely pulled-back/sparse section
+ transient breathing room. A wall-to-wall-dense mix that still varies
section-to-section scores HIGH on dynamic_mix but LOW on negative_space. The
scorer must be conceptually distinct, not a re-derivation of dynamic_mix.

## The honesty gate

negative_space works at the **section-aggregate** level (mean/min section
`density`, `transient_density`, `rms_dbfs`). **Deferred / NOT faked** (document
in the docstring): true sample-level **inter-onset silence gaps** (space between
individual hits) need onset timing, which lives in the post-doctrine groove
analyzer and is NOT visible at `score_doctrine` time (that's P-032b). Do not
claim sample-level gap detection.

## Signal surface (verified available to `score_doctrine`)

Per-section `section_analysis[i]["metrics"]`: `density` (spectral occupancy),
`transient_density`, `rms_dbfs`, `width`, `brightness`, `low_mid_energy`; plus
`contrast_vs_previous` deltas. Per-track `records[i]["metrics"]["density"]` as a
fallback/corroboration. `mix_metrics` (density) as a whole-mix fallback. Build
ONLY from these — no onset timing, no post-doctrine analyzers.

## Spec (build exactly this)

**New agnostic scorer** `_negative_space(records, sections_analysis, mix_metrics,
doctrine)` in `doctrine/doctrine_engine.py` → `(score_0_100, evidence_list)`,
constants from `doctrine["scorers"]["negative_space"]` (read-only, no mutation).
Compose ABSOLUTE ROOM as a STRENGTH:

- **Absolute room** — reward low mean section (or mix) spectral `density`
  (occupancy): more room = higher score. (`room = ceiling - mean_density`,
  bonus-coeff'd, clamped.)
- **Sparse-section presence** — reward a genuine dropout: `min_section_density`
  (or min RMS) meaningfully below the max → a section that pulls back → bonus.
  "Silence as arrangement." (Needs ≥2 sections; skip gracefully otherwise.)
- **Transient breathing room** — reward low mean section `transient_density`
  (space between hits); penalize wall-to-wall transients.
- Returns a clamped float ALWAYS (never None) — a documented neutral fallback
  when there is no section/mix data — so the axis is always present (mirror
  `_beat_identity`'s always-float discipline).

**Wiring (byte-identical mechanism — identical to P-032e):**
- Add `"negative_space_score": ns` to `component_scores` **LAST** (after
  `beat_identity_score`) — preserves summation order → overall bit-identical.
- Add `"negative_space": ns_ev` to the `evidence` dict.
- `halee_ramone.json`: `doctrine.weights["negative_space_score"] = 0` (byte-
  identical anchor) + a `doctrine.scorers.negative_space` constants block.
- `producer_profile.py` `_validate`: add `"negative_space"` to the required-
  scorers tuple (currently includes `beat_identity` from P-032e).
- `schemas/doctrine_score.schema.json`: add optional `negative_space_score`
  property (documentation; schema has no `additionalProperties:false`).

**Tests (test-first — new `tests/test_negative_space.py`):**
1. **Byte-identical** — all 3 fixtures: every pre-existing component score
   (now 8, incl. beat_identity_score) + `overall_mix_readiness_score` UNCHANGED
   vs base; `regression` 68/68 holds.
2. **Value-discrimination (unit)** — synthetic sections: a sparse, dynamic
   arrangement (low density + a dropout section) → HIGH negative_space; a
   wall-to-wall-dense arrangement → LOW. AND a case that scores high on
   dynamic-movement but LOW on negative_space (proves distinctness from
   dynamic_mix).
3. **Liveness (load-bearing)** — a profile weighting `negative_space_score`
   non-zero changes `analyze()` overall on a fixture; sabotage (hardcode/drop)
   FAILS liveness while byte-identical stays green (P-016/P-029 lesson).
4. **No-aliasing** — scorer only reads `doctrine[...]`; never mutates.

## Rigor bar (non-negotiable — same as P-032e)

- **RUN `python fixtures/generate_fixtures.py` FIRST** (stems gitignored).
- **≤2 commits**, **Commit-1 green in isolation**.
- Full `pytest` green; `regression` = 68/68.
- **Agnostic-first**: physics/measurement hardcoded & agnostic; only *weights*
  live in the profile. halee_ramone output byte-identical.
- Commit trailers exactly `Co-Authored-By: Claude Opus 4.8 …` +
  `Claude-Session: …`; no model identifier in body/subject/comments.
- No external mutation beyond the standing push-go to the dev branch (NO merge).

## Last-closed

- **P-032e — `beat_identity` (THE CRUX, front-loaded). ✓ CLOSED** — qa GREEN,
  reviewer PASS. First new producer-agnostic doctrine axis; strength-form;
  byte-identical for halee_ramone (0/24 mismatches; 68/68); liveness load-bearing;
  honest deferrals documented. Commits `8239f42`+`9d6764e`; suite 384→396; build-os
  close `8a2892b`. **Local-only on dev branch, NOT merged** (merge base still
  `e79426a` = PR #16). Receipt: `build-os/receipts/P-032e-beat-identity.md`.

## Epic arc (Timbaland sub-arc P-032.x)

**P-032e ✓ (beat_identity — CRUX) → P-032a (negative_space — ACTIVE) →** P-032b
(groove_coherence live-wire — where onset-regularity/IOI, deferred from P-032e,
gets plumbed in) → P-032c (low_end_motion/pocket) → P-032d (rhythmic_surprise,
weak-form) → P-032f (vocal-role refinement) → P-032g (loop static-vs-iconic
context) → **[fold P-031 confidence here]** → P-032h (author `timbaland.json`,
first non-byte-identical output) → P-032i (Timbaland-vs-Halee/Ramone differential
proof). P-030 (rename dims) orthogonal/last.

---
_Set active by the orchestrator-in-chief on P-032a confirm (2026-07-01). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
