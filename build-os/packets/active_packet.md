# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed, handed to builder
- **Packet id:** P-032b
- **Title:** `groove_coherence` live-wire — relocate `analyze_groove` before
  `score_doctrine`, thread it in, add the groove-coherence axis; byte-identical
  for halee_ramone.

## Why this packet is the RISKIER one

Unlike P-032e/P-032a (pure additive scorers over signals already visible to
doctrine), P-032b is a **live-wire relocation**: the groove signal
(`overall_regularity` = per-track `1 − CoV(IOIs)`) is computed at pipeline.py:193,
which is **27 lines AFTER** `score_doctrine` at :166. To feed doctrine, groove
must be computed BEFORE doctrine and threaded in. This is the packet where
onset-regularity/IOI — deferred from BOTH P-032e and P-032a — finally reaches
doctrine. The **P-016 lesson governs**: an evidence-gated signal is only live if
computed BEFORE its consumer, and computed ONCE (not re-run).

## The live-wire (do exactly this)

In `pipeline.py`: build `rhythm_tracks` (currently :182-186, from
`result.track_identity` + `loaded_by_id` + `RHYTHM_IDENTITIES`) and compute
`groove = analyze_groove(rhythm_tracks)` **BEFORE** the `score_doctrine` call at
:166 (all its inputs — `result.track_identity`, `loaded_by_id` — are already
available by then). Pass `groove=groove` into `score_doctrine`. Then **REUSE the
exact same computed `groove`** in `result.expanded["groove"]` (:193) — do NOT call
`analyze_groove` a second time. The relocation must be **behavior-preserving**:
`result.expanded["groove"]` is byte-unchanged (same value, computed earlier and
reused).

## Honest naming (do NOT overclaim)

`overall_regularity` measures rhythmic **tightness/consistency**, NOT "identity
coherence" in the full sense. Name the scorer's evidence honestly: it scores
groove **regularity/consistency** as a *proxy* for coherence. And it must NOT
bake in a "tighter = better" bias — the doctrine's own stance is "tighter is not
better; it reports the feel." The agnostic layer stays neutral; a *producer*
chooses whether/how to weight groove_coherence. Document this in the docstring.

## Spec (build exactly this)

**New agnostic scorer** `_groove_coherence(groove, doctrine)` in
`doctrine/doctrine_engine.py` → `(score_0_100, evidence_list)`, constants from
`doctrine["scorers"]["groove_coherence"]` (read-only). Reads `groove`'s
`overall_regularity` (0..1) and/or per-track regularities:
- **None/absent groove** (no rhythm stems, or `overall_regularity is None`) →
  documented **neutral fallback** float (never None, never crash).
- **Present** → map `overall_regularity` to a 0..100 coherence score (a coherent,
  consistent groove scores high; an incoherent/absent one low/neutral). Sensible
  constants (baseline/scale) in the profile.

**score_doctrine signature:** add `groove: Optional[Dict] = None` (keyword,
default None) so EVERY existing caller (tests included) stays byte-identical.
When `groove is None`, `_groove_coherence` uses its neutral fallback.

**Wiring (byte-identical — identical pattern to P-032e/a):**
- Add `"groove_coherence_score": gc` to `component_scores` **LAST** (after
  `negative_space_score`) — preserves the 9-term summation order → overall
  bit-identical.
- Add `"groove_coherence": gc_ev` to `evidence`.
- `halee_ramone.json`: `doctrine.weights["groove_coherence_score"] = 0` + a
  `doctrine.scorers.groove_coherence` constants block.
- `producer_profile.py` `_validate`: add `"groove_coherence"` to required-scorers.
- `schemas/doctrine_score.schema.json`: add optional `groove_coherence_score`.

**Tests (test-first — new `tests/test_groove_coherence.py`):**
1. **Byte-identical** — all 3 fixtures: every pre-existing component score (now 9)
   + `overall_mix_readiness_score` UNCHANGED vs base; `regression` 68/68. **AND
   `result.expanded["groove"]` byte-unchanged** vs base (the relocation is
   behavior-preserving).
2. **No-re-run live-wire (THE P-016 GUARD)** — during a full `analyze()`,
   `analyze_groove` is called **exactly ONCE** (spy/patch a call counter) — proving
   it's computed before doctrine and REUSED, not re-run. AND `score_doctrine`
   actually receives the real groove: `groove_coherence` in the doctrine output
   reflects the real `overall_regularity` on `dense_chorus_with_loops` (NOT the
   None-fallback).
3. **Value-discrimination (unit)** — a coherent/regular groove dict → HIGH
   groove_coherence; `overall_regularity=None`/incoherent → neutral/low.
4. **Liveness (load-bearing)** — a profile weighting `groove_coherence_score`
   non-zero changes `analyze()` overall on `dense_chorus_with_loops`; **sabotage**
   (pass `groove=None` into `score_doctrine`, i.e. break the threading) makes the
   liveness + no-re-run assertions FAIL while byte-identical stays green.
5. **No-aliasing** — scorer only reads `doctrine[...]`/`groove[...]`; never mutates.

## Risk callouts (the builder must respect)

- **Behavior-preservation:** `result.expanded["groove"]` MUST be identical after
  the relocation — the whole expanded suite is order-independent EXCEPT that
  groove must be the same computed value. Guard it with a test.
- **Backward-compat:** `score_doctrine(..., groove=None)` default keeps all
  existing callers green.
- **None-handling:** `_groove_coherence` must handle `overall_regularity is None`
  gracefully (fixtures without rhythm stems).
- **Compute-once:** exactly ONE `analyze_groove` call per `analyze()` (the
  no-re-run guard). If you find yourself computing it twice, the live-wire is wrong.

## Rigor bar (non-negotiable)

- **RUN `python fixtures/generate_fixtures.py` FIRST** (stems gitignored).
- **≤2 commits**, **Commit-1 green in isolation**.
- Full `pytest` green; `regression` = 68/68.
- **Agnostic-first**; halee_ramone output byte-identical (weight 0).
- Commit trailers exactly `Co-Authored-By: Claude Opus 4.8 …` + `Claude-Session:
  …`; no model identifier in body/subject/comments.
- No external mutation beyond the standing push-go to the dev branch (NO merge).

## Last-closed

- **P-032a — `negative_space` (2nd new agnostic axis). ✓ CLOSED** — qa GREEN,
  reviewer PASS. Byte-identical (0/27; overalls 73.8/70.7/74.3; 68/68); distinct
  from dynamic_mix (85-pt gap); single commit `3edcd9c`; suite 396→413; build-os
  close `3e991a5`. Local-only on dev branch, NOT merged (base `e79426a` = PR #16).
  Receipt: `build-os/receipts/P-032a-negative-space.md`.

## Epic arc (Timbaland sub-arc P-032.x)

**P-032e ✓ (beat_identity — CRUX) → P-032a ✓ (negative_space) → P-032b
(groove_coherence live-wire — ACTIVE) →** P-032c (low_end_motion/pocket) → P-032d
(rhythmic_surprise, weak-form) → P-032f (vocal-role refinement) → P-032g (loop
static-vs-iconic context) → **[fold P-031 confidence here]** → P-032h (author
`timbaland.json`, first non-byte-identical output) → P-032i (Timbaland-vs-
Halee/Ramone differential proof). P-030 (rename dims) orthogonal/last.

---
_Set active by the orchestrator-in-chief on P-032b confirm (2026-07-01). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges +
an adversarial live-wire verification pass; archivist closes with a receipt._
