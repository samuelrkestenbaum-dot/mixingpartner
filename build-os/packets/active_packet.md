# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed, handed to builder
- **Packet id:** P-032d
- **Title:** `rhythmic_surprise` (weak-form) — fourth new producer-agnostic
  doctrine axis (cross-section transient-density variation); byte-identical for
  halee_ramone.

## Why this packet, and why now

Fourth axis of the Timbaland sub-arc, first of the RESEQUENCED remaining order
(d → c → g → f): the smallest, safest lift. ONE input (section
`transient_density`), pure additive, ZERO new plumbing — `score_doctrine`
already receives `sections_analysis`. User design: reward rhythmic
surprise/variation. The scoping sweep confirmed the STRONG form (fills,
unexpected hits, per-onset deviation) is NOT measurable at doctrine time; the
defensible WEAK form is cross-section transient-density variation.

## The honesty gate (weak-form, clearly labeled)

The scorer measures the **WEAK, section-aggregate form**: cross-section
`transient_density` variance + the largest single section-to-section swing.
Evidence strings must say so explicitly. **Deferred / NOT faked** (docstring):
(1) fill detection, (2) unexpected-hit detection, (3) per-onset IOI deviation —
all need onset timing/sequence, which is groove territory. And it must NOT read
`groove.overall_regularity` — that is `_groove_coherence`'s input; re-reading it
here would duplicate that axis.

## Distinctness (the design guard)

This is the ONLY axis keyed on the *variation of section transient_density*:
- `_dynamic_mix` = pstdev of section rms/width/brightness (never transient_density).
- `_negative_space` = **mean** section transient_density (central tendency — the
  opposite statistic; a mix can have high mean AND high variance).
- `_beat_identity` = per-STEM transient dominance (one point in time, not the arc).
- `_section_contrast` = lift-fail count from contrast warnings.
- `_groove_coherence` = onset IOI regularity (groove input, untouched here).
A wall-to-wall CONSTANT transient bed (high mean, zero variance) must score LOW
on rhythmic_surprise even though beat_identity/dynamic_mix may score it high.

## Signal surface (verified — zero new plumbing)

`section_analysis[i]["metrics"]["transient_density"]` (+ optionally
`contrast_vs_previous` density deltas). Needs ≥2 sections; fewer → documented
neutral/insufficient fallback float (mirror `_dynamic_mix`'s
`insufficient_sections_score` idiom; never None).

## Spec (build exactly this)

**New agnostic scorer** `_rhythmic_surprise(sections_analysis, doctrine)` in
`doctrine/doctrine_engine.py` → `(score_0_100, evidence_list)`, constants from
`doctrine["scorers"]["rhythmic_surprise"]` (read-only). Compose:
- **Spread** — pstdev of section transient_density (the `_dynamic_mix` idiom
  applied to the one signal it never reads), scaled by a profile coefficient.
- **Largest swing** — max |Δ transient_density| between adjacent sections,
  bonus-coeff'd ("the beat drops out / the fill hits" in aggregate form).
- **Insufficient data** — <2 sections → documented fallback float.
- Always returns a clamped float (never None).

**Wiring (byte-identical — the established pattern):**
- `"rhythmic_surprise_score": rs` appended **LAST** to `component_scores` (after
  `groove_coherence_score`; preserves the 10-term summation order).
- `"rhythmic_surprise": rs_ev` in `evidence`.
- `halee_ramone.json`: `doctrine.weights["rhythmic_surprise_score"] = 0` + a
  `doctrine.scorers.rhythmic_surprise` constants block.
- `producer_profile.py` `_validate`: add `"rhythmic_surprise"` to required-scorers.
- `schemas/doctrine_score.schema.json`: optional `rhythmic_surprise_score`.

**Tests (test-first — new `tests/test_rhythmic_surprise.py`):**
1. **Byte-identical** — all 3 fixtures: every pre-existing component score (now
   10) + overall UNCHANGED; regression 68/68.
2. **Value-discrimination** — varied/fill-like sections (big transient swings) →
   HIGH; flat/constant transient bed → LOW; <2 sections → the fallback.
   AND the distinctness case: high MEAN but ZERO VARIANCE transient bed → LOW
   rhythmic_surprise (while negative_space would read its mean and beat_identity
   its per-stem dominance — different statistics).
3. **Liveness (load-bearing)** — non-zero weight changes `analyze()` overall on
   a fixture; drop/hardcode sabotage fails while byte-identical stays green.
4. **No-aliasing** — reads only; never mutates `doctrine`/sections.

## Rigor bar (non-negotiable)

- **RUN `python fixtures/generate_fixtures.py` FIRST.**
- **≤2 commits**, **Commit-1 green in isolation**. Full `pytest` green;
  `regression` = 68/68.
- **Agnostic-first**; halee_ramone byte-identical (weight 0).
- Commit trailers exactly `Co-Authored-By: Claude Opus 4.8 …` +
  `Claude-Session: …`; no model identifier in body/subject/comments.
- No external mutation beyond the standing push-go to the dev branch (NO merge).

## Last-closed

- **P-032b — `groove_coherence` live-wire. ✓ CLOSED** — qa GREEN, reviewer PASS,
  3-skeptic adversarial pass all HELD (triple-verified). 10 component axes; the
  onset/IOI signal is LIVE at doctrine time. Single commit `e9f793f`; suite
  413→433; build-os close `2fdf77d`. Local-only, NOT merged (merge base
  `e79426a` = PR #16). Receipt:
  `build-os/receipts/P-032b-groove-coherence-livewire.md`.

## Epic arc (Timbaland sub-arc P-032.x — RESEQUENCED)

**P-032e ✓ → P-032a ✓ → P-032b ✓ → P-032d (rhythmic_surprise — ACTIVE) →**
P-032c (low_end_motion) → P-032g (loop static-vs-iconic) → P-032f (vocal-role —
★ USER-GATED) → **[fold P-031 confidence here]** → P-032h (author
`timbaland.json`) → P-032i (differential proof). P-030 (rename dims)
orthogonal/last.

---
_Set active by the orchestrator-in-chief on P-032d confirm (2026-07-01). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
