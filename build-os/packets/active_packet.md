# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed, handed to builder
- **Packet id:** P-032e
- **Title:** `beat_identity` — first new producer-agnostic doctrine axis (THE CRUX),
  strength-form only; byte-identical for halee_ramone.

## Why this packet, why first

The Timbaland sub-arc (P-032.x) instantiates the epic's user-gated "first second
producer." The user front-loaded **beat_identity** — the hardest, riskiest axis —
to **de-risk the whole sub-arc early**: prove the central-rhythmic-fingerprint
signal is *honestly measurable on exported stems* before investing in the easier
axes. Sequencing decision (user-confirmed): **Timbaland axes first**, fold the
confidence framework (P-031) in at authoring (P-032h); rename (P-030) is
orthogonal/last.

## The honesty gate (the crux of this packet)

beat_identity measures **STRENGTH ONLY** — "is there a central, undeniable
rhythmic element" — from transient physics. Three things are **explicitly
deferred / NOT attempted** (documented as P-014-style honest boundaries, not
faked):

1. **Fingerprint TYPING** (mouth-sound vs tabla vs synth-knock vs beatbox) — NOT
   measurable on exported stems. Do not attempt to name what the beat *is*.
2. **Onset REGULARITY / IOI** — a real signal, but it lives in the groove
   analyzer which runs *post-doctrine* (pipeline.py:187-197). It is NOT visible
   at `score_doctrine` time. This packet does NOT use it; wiring it in is
   **P-032b**'s plumbing move.
3. **"More undeniable after a move"** — needs a before/after render; out of scope
   in plan-only v1.

## Signal surface (verified — available to `score_doctrine`)

Per-track `records` carry (via `metrics` + record fields): `transient_density`
(0..1), `crest_factor_db`, `spectral_flatness`, `band_energy` (fractions),
`density`, plus `perceptual_role`, `depth_default`, `source_kind`, `sacredness`,
`instrument_identity`. Plus `masking_report["events"]`. **beat_identity builds
ONLY from these** — no onset regularity, no post-doctrine analyzers.

## Spec (build exactly this)

**New agnostic scorer** `_beat_identity(records, events, doctrine)` in
`doctrine/doctrine_engine.py`, returning `(score_0_100, evidence_list)`, idiom-
matching the existing scorers (constants read from `doctrine["scorers"]
["beat_identity"]`, read-only, no mutation). Measures **fingerprint strength**:

- **Agnostic rhythmic-candidate identification** — a stem is a rhythmic candidate
  by *transient physics* (high `transient_density`, optionally corroborated by
  `crest_factor_db` / `spectral_flatness`), NOT by instrument label. Keeps it
  producer-agnostic.
- **Presence** — is there a defined rhythmic element at all (baseline vs a
  `no_beat` floor when none clears the transient floor).
- **Distinctness/dominance** — top candidate's transient_density above the track
  median (a beat that stands out from the bed is more undeniable).
- **Definition** — dominant rhythmic stem's `crest_factor_db` above threshold
  (punchy, defined hits vs smeared).
- **Foreground/unmasked** — dominant rhythmic stem is `heard` / forward layer and
  NOT `bad_masking` → bonus; buried/felt/background or masked → penalty (the
  fingerprint exists but isn't *undeniable*).

**Wiring (byte-identical mechanism):**
- Add `"beat_identity_score": beat` to `component_scores` **LAST** (preserves the
  existing 7-term summation order → overall bit-identical).
- Add `"beat_identity": beat_ev` to the `evidence` dict.
- `halee_ramone.json`: add `doctrine.weights["beat_identity_score"] = 0` (the
  byte-identical anchor: `beat·0` numerator, `+0` denominator → weighted mean
  unchanged) and a `doctrine.scorers.beat_identity` constants block.
- `producer_profile.py`: extend the `_validate` required-scorers set to include
  `beat_identity` so the new axis is structurally bound.
- Check `schemas/` for a `doctrine_score` schema with `additionalProperties:
  false` — if present, add `beat_identity_score` + `evidence.beat_identity`.

**Tests (test-first; the binding guards):**
1. **Byte-identical** — all 3 fixtures: `analyze()` (default halee_ramone) →
   every existing component score + `overall_mix_readiness_score` UNCHANGED vs a
   captured baseline; `regression` 68/68 holds.
2. **Value-discrimination (unit)** — synthetic records: a punchy, foregrounded,
   distinct rhythmic stem → HIGH beat_identity; no rhythmic element → baseline/low.
   Proves the scorer measures what it claims.
3. **Liveness (load-bearing)** — a synthetic profile weighting
   `beat_identity_score` non-zero changes `analyze()` overall on the
   dense_chorus_with_loops fixture; **sabotage** (hardcode beat / drop the
   threading) FAILS liveness while byte-identical stays green (the P-016/P-029
   lesson).
4. **No-aliasing** — scorer only reads `doctrine[...]`; consistent with
   `tests/test_doctrine_profile_sourced.py` discipline.

## Rigor bar (non-negotiable)

- **≤2 commits**, **Commit-1 green in isolation** (scorer + profile constants +
  weight=0 + byte-identical/discrimination tests).
- **68/68 golden regression holds** (run `fixtures/generate_fixtures.py` first in
  a fresh tree — stems are gitignored/generated).
- Full suite green; qa reports exact counts, Commit-1 isolation, safety grep.
- **Agnostic-first**: physics/measurement stays hardcoded & agnostic; only
  *weights* live in the profile. halee_ramone output byte-identical.
- No external mutation beyond the standing push-go to the dev branch (NO merge).

## Last-closed

- **P-029 — Parameterize the pipeline by a per-call producer profile —
  `analyze(producer=…)` (THE PIVOT). ✓ CLOSED** — qa GREEN, reviewer pass.
  Producer-agnostic architecture COMPLETE and VALIDATED; profile is a live,
  selectable lever end-to-end. Two commits `42d6ebd` + `ea1aaa9`; suite 384.
  Local-only on dev branch (base `e79426a`), not merged. Receipt:
  `build-os/receipts/P-029-parameterize-pipeline-by-per-call-producer-profile.md`.

## Epic arc (Timbaland sub-arc P-032.x)

**P-032e (beat_identity — THE CRUX, front-loaded) →** P-032a (negative_space) →
P-032b (groove_coherence live-wire) → P-032c (low_end_motion/pocket) → P-032d
(rhythmic_surprise, weak-form) → P-032f (vocal-role refinement) → P-032g (loop
static-vs-iconic context) → **[fold P-031 confidence here]** → P-032h (author
`timbaland.json`, first non-byte-identical output) → P-032i (Timbaland-vs-
Halee/Ramone differential proof). P-030 (rename dims) orthogonal/last.

---
_Set active by the orchestrator-in-chief on P-032e confirm (2026-07-01). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
