# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-057 — Non-Eno Textural Weighting** (set on the user's
  "ok go", 2026-07-06: **Quincy 0.6, CLA defer**). Profile-data packet; roster
  frozen at five; base `1ab5878` (= PR #34, the default tip — verify
  `git merge-base HEAD 1ab5878` = `1ab5878`).
- **Baseline to protect:** suite **1347** / regression **93/93** / the four
  non-opting producers' (Halee, Timbaland, CLA, Eno) **overall + decision**
  byte-stability / the aesthetic + loudness kill-switches, veto thresholds,
  `governance.py`, `creative.py`, and the dropout structural-protection filter
  byte-untouched.

## P-057 — Non-Eno Textural Weighting

Make the P-056 `textural_coherence_score` axis COUNT for Quincy Jones — the one
non-Eno producer whose documented aesthetic genuinely supports bed cohesion.
**Profile-data ONLY — ZERO `.py` under `logic_mix_os/`** (the axis, the
`_textural_coherence` scorer, the `_coherence_from_dispersion` sign seam,
`producer_profile._validate`, the schema, and the shared
`doctrine.scorers.textural_coherence` constants block all exist from P-056; this
is a weight change + confidence entry + regen + test re-pins). If any engine edit
is genuinely required → **STOP AND FLAG**.

### The taste decisions (user-confirmed: Quincy 0.6, CLA defer)

- **Quincy Jones: weight 0 → 0.6.** Grounding: his retained support/hygiene
  cluster (= `negative_space`/`beat_identity`/`groove_coherence` 0.6), explicitly
  BELOW his `depth_hierarchy` 1.4 center and `section_contrast` 1.3 — a
  support-tier "the ensemble texture coheres as one arranged surface" reading,
  never his center of gravity. It is DISJOINT from his distinct-layer center:
  `depth_hierarchy` reads placement/room; textural coherence reads timbral/spatial
  bed similarity and provably reads none of depth's inputs (a big-band arranger
  keeps every part in a distinct, readable PLACE and wants the ensemble's texture
  beds to share one coherent surface). Confidence_map: add a textural-coherence
  entry at level **`limited`** (documented big-band/ensemble arranging; secondary,
  support-tier; the "one woven surface" framing runs partly counter to his
  distinct-readable-layer center, so `limited`, NOT `high` — `high` would
  over-claim; Eno earns `high` because texture-as-composition is HIS center).
- **Chris Lord-Alge: DEFER — stay weight 0.** The measured axis reads the
  background/midground texture-bed layer, which is exactly the layer CLA
  de-emphasizes to his floor (`depth_hierarchy` 0.4, `negative_space` 0.2, his
  "anti-Eno" absolute floor). His real cohesion instinct is impact-glue /
  loudness translation — and loudness is a DEFERRED concern by design, not a
  doctrine axis. His profile already honestly defers "loudness maximization",
  "saturation as energy", and "whole-mix translation" rather than fake them with
  imperfect proxies; deferring textural coherence is the CONSISTENT, honest
  posture, and it keeps him byte-identical. **Touch nothing in CLA's profile.**
- **Brian Eno: UNTOUCHED** — weight 1.2, confidence, overall byte-identical.
- **Halee/Ramone, Timbaland: UNTOUCHED** — weight 0.

### Effect (honest, expected)

Opting Quincy in pulls his `overall` DOWN (the axis reads 55.0 neutral on the
`<2`-bed fixtures simple/splice/chop, 27.0 on the one ≥2-bed fixture
`dense_chorus_with_loops`) — same direction as Eno's 65.5→64.3. Quincy's
committed headline 68.8 moves; regenerate his sample tree real-CLI-faithful and
re-pin. The per-fixture axis VALUE is profile-blind and does NOT change (55/55/55/27);
only Quincy's weighted overall moves.

### Commit shape (≤2; Commit-1 green in isolation)

- **Commit-1:** Quincy's `weights.textural_coherence_score` `0 → 0.6` +
  `confidence_map` textural entry (`limited`); regenerate Quincy's sample tree
  real-CLI-faithful (P-053/P-056 pattern); re-pin EVERY moved/weight-0 assertion
  so C1 is green ALONE — `test_five_way_differential.py` (`_NON_ENO` set drops
  Quincy → {Halee, Timbaland, CLA}; the weight-0 byte-identical proof re-pinned to
  that shrunk set; `FIVE_WAY_OVERALLS` re-pins Quincy's moved overall),
  `test_four_way_differential.py` (Quincy's four-way overall), `test_quincy_profile.py`
  (weight pin `0→0.6`; the "sole weight-0 axis is textural_coherence" assertions
  flip — Quincy now has NO weight-0 axis; confidence-map pin gains the entry),
  `test_sample_refresh.py` (HEADLINES), `test_doctrine_profile_sourced.py`,
  `test_producer_profile.py`, and `README.md` (the five-producer table + prose
  cell for Quincy — the P-054 numbers guard + P-055 prose guard will FORCE this;
  a missed re-pin fails loudly). **`test_cla_profile.py` is UNTOUCHED** (CLA
  deferred). Green in isolation.
- **Commit-2 (purely additive proof):** the permanent P-057 differential —
  `test_five_way_differential.py` (+ `test_quincy_profile.py` if a dedicated home
  fits): Quincy's overall MOVED vs the pre-P-057 (post-P-056) committed baseline,
  per fixture (dense-largest); the shrunk weight-0 set {Halee, Timbaland, CLA}
  byte-identical; Eno unchanged; the axis key present in all five; a
  zero-weight sabotage bite (zeroing Quincy's textural weight reverts his overall
  to the pre-P-057 value; deleting the key → KeyError).

### Required proof (qa, before close)

Full suite counts (new total; +N from C2); regression **93/93**; Commit-1 iso
count; the MOVE differential (Quincy's overall moves, dense-largest); the
**four→three** byte-identical proof (Halee/Timbaland/CLA overall + `mix_verdict.md`
+ `mix_plan.json` + `dashboard.html` byte-identical to their committed P-057
baselines); Eno unchanged (weight 1.2 / confidence / overall byte-identical); the
axis key present + measured in all five; the sabotage bite; safety grep of the
source diff = 0 reach (diff is JSON + tests + regenerated Quincy tree + README);
diff-proof that `governance.py`, `creative.py`, the kill-switches, veto, and
`protect_iconic_loops` are byte-untouched. No new dependency.

### Non-scope (binding)

No new axis/scorer; **no engine `.py` change** (flag if forced); no
governance/kill-switch/veto/`protect_iconic_loops` change; no sixth producer; no
apply-to-Logic; no dropout-reach / ambient-patience / generative-process; Eno's
weight untouched; CLA's profile untouched (deferred). Textural-coherence
WEIGHTING only.

- **Receipt (on close):** `build-os/receipts/P-057-non-eno-textural-weighting.md`.

---
_Set active by the orchestrator + confirmed on the user's "ok go" (2026-07-06,
Quincy 0.6 / CLA defer), after the P-056 merge (PR #34 → `1ab5878`). One packet
at a time: builder → qa + reviewer → archivist → receipt._
