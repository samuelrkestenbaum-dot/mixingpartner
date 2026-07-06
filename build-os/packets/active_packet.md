# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "go" (2026-07-06) after the P-055
  merge (PR #33 → default `b03f388`). The roster is FROZEN at five (no sixth
  producer). The callable MCP surface is proven end-to-end (P-052, PR #30); the
  only remaining MCP item is the literal Claude-app-as-client, a MANUAL user
  step, not a packet. This is the first ENGINE-DEEPENING packet since the
  producer arc: the highest-ranked Eno-deferral analyzer.
- **ID / Title:** **P-056 — Textural Coherence Analyzer** (a 15th doctrine axis)
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `b03f388` (= PR #33 merge — the branch was fast-forwarded to it, clean; verify
  with `git merge-base`).
- **Baseline to protect:** suite **1306** / regression **93/93** / the five
  producers' **overall-score + decision** byte-stability where they do NOT opt in
  / the aesthetic + loudness kill-switches, veto thresholds, `governance.py`, and
  the dropout structural-protection filter byte-untouched.

## The user's decision (D1 = A, confirmed)

**Textural coherence = bed-similarity DISPERSION** (Option A — the recommended,
provably-distinct definition). Coherence measures how much the record's texture
beds RESEMBLE each other across three feature families:

- **tonal** — `band_energy` (5-band) L1 spread + `brightness` stdev
- **spatial** — `stereo_width` stdev
- **dynamic** — `crest_factor_db` stdev

Low cross-bed dispersion → HIGH coherence (one woven surface); high dispersion →
LOW coherence (a pile of unrelated layers). It is a PURE dispersion statistic:
it never reads room, occupancy-mean, depth-count, foreground salience, or rhythm
— so distinctness from `negative_space` / `physical_space` / `depth_hierarchy` /
`groove_coherence` is PROVABLE, not asserted. This is the most literal reading of
Eno's documented practice ("the beds cohere as one woven surface") and flips his
own confidence_map deferral ("textural coherence as its own measurement" —
deferred → high/limited).

**D2 (defaults, accepted):** three EQUALLY-weighted sub-terms (tonal / spatial /
dynamic); relative sub-weights live in `doctrine.scorers.textural_coherence` so
they're per-profile tunable later without code change. Eno's AXIS weight lands in
his "high" tier (near `depth_hierarchy` 1.1 / `physical_space` 1.3 — exact value
a calibration knob the differential pins).

**D3 (defaults, accepted):** reuse the engine-owned `_dropout_texture_beds`
surface as-is (records with `perceptual_role == "felt"` and `depth_default ∈
{midground, background}`, plus `source_kind ∈ LOOP_SAMPLE_KINDS`) — already "the
beds," already profile-blind. Folding in "heard" support or foregrounded loops is
a deferred membership taste call.

## Measurement (named signals — all already extracted; zero new DSP, zero new dep)

Over the bed set B (`creative._dropout_texture_beds(records)`): the tonal term
from cross-bed dispersion of each stem's `band_energy` vector + `brightness`; the
spatial term from stdev of `stereo_width`; the dynamic term from stdev of
`crest_factor_db`. Combine into a 0–100 `textural_coherence_score` via constants
in `doctrine.scorers.textural_coherence`. Deterministic, local-first,
non-destructive, plan-only. **Always-float fallbacks** (mirror `_negative_space`
/ `_groove_coherence`): fewer than 2 beds → a neutral float (a single/absent bed
cannot be "incoherent"); never None, never a crash. NO new feature — if the
builder finds one genuinely required, that is a STOP-AND-FLAG, not a silent add.

## How it deepens the engine (scores, not just re-weights)

A real 15th axis producing a real per-record number wired into `score_doctrine`
(component_scores + evidence), appended LAST to preserve summation order. Eno
weights it non-zero → his `overall_mix_readiness_score` genuinely MOVES (a new
measured signal, not a re-weighting of old ones). The metric is a producer-
profile PRIMITIVE ("does this read as one produced record or a stack of parts") —
the most defensible secondary beneficiary is Quincy (ensemble cohesion), with a
natural future reading for CLA (does the wall cohere or merely pile up). Weighting
the axis for the other four is EXPLICITLY OUT (a separate future taste call) —
they ship at weight 0 to preserve their decision byte-stability. Even at weight 0
the axis emits an honest diagnostic evidence line in every producer's artifact.

## Profile-respecting + gated (precise — no overclaim)

Plugs in exactly like the six prior agnostic axes (beat_identity … loop_context):
a new `doctrine.weights.textural_coherence_score` (real for Eno, **0** for the
other four) + a `doctrine.scorers.textural_coherence` constants block. Because the
loader REQUIRES every scorer name in `doctrine.scorers` (`producer_profile._validate`),
all five JSONs necessarily gain the additive block + a weight, and Eno's
confidence_map entry flips `deferred → high` (or `limited`) with an honest reason.

**What "byte-stable" means here (be precise):** the four non-Eno producers keep
**overall-score and decision** byte-stability (a 0-weight term adds nothing to the
weighted-mean numerator or denominator — winners, governance, veto all unchanged);
they do NOT keep *file* byte-stability (every profile JSON gets the additive block;
every committed sample artifact gains the labeled `textural_coherence_score` key +
evidence, so the sample trees are regenerated real-CLI-faithful, the P-053 pattern).

**Untouched, diff-proven byte-identical:** the aesthetic kill-switches, the
loudness kill-switch, the veto thresholds, `governance.py`, and the profile-blind
dropout structural-protection filter (`_dropout_protected_names`).

## Required proof (qa, before close)

- Full suite green + exact before/after counts; regression **93/93**; Commit-1
  green in isolation; safety grep zero (no DAW/execution/subprocess/apply reach).
- **Five-way differential:** (a) Eno's `overall` CHANGES vs his pre-axis baseline
  on a bed-carrying fixture; (b) the four other producers' `overall` is
  BYTE-IDENTICAL to their committed pre-axis baseline (the weight-0 proof); (c) the
  `textural_coherence_score` key is present in ALL FIVE artifacts (measured for
  all; weighted only by Eno); (d) Eno's confidence-flip asserted.
- **Distinctness proof:** a dense-but-coherent bed set scores LOW negative_space /
  HIGH textural_coherence, and a sparse-but-incoherent set scores HIGH
  negative_space / LOW textural_coherence (independence from negative_space); a
  scattered-bed set with constant sections leaves groove/dynamic unmoved while
  textural_coherence drops (independence from the rhythm/section axes).
- **Sabotage/mutation (named lesson #2 — defense needs mutation tests):** delete
  or zero Eno's `textural_coherence_score` weight → his overall reverts to the
  four-way value (load-bearing, not decorative); flip the dispersion sign in the
  scorer → the HIGH/LOW synthetic cases swap (the metric truly reads dispersion).
- **Determinism:** same stems → same score. **Diff-proof** that `governance.py` +
  the dropout filter are byte-untouched.

## Non-scope (binding)

No sixth producer. No apply-to-Logic / DAW execution. No widened dropout reach
(the `_dropout_protected_names` filter byte-untouched). No new creative move-kind,
mode, or change to `score_variant`'s dims (this is a DOCTRINE axis, not a
creative-variant kind). No weighting of the axis for the four non-Eno producers.
No governance / kill-switch / veto change. No new dependency (numpy-only, existing
per-stem features). **No ambient-patience or generative-process work** — both stay
deferred; this packet is textural coherence ONLY, and it deliberately steers clear
of the negative-space overlap flagged for the sibling analyzers.

## Commit shape (≤2; Commit-1 green in isolation) — mirrors P-050

- **Commit-1:** the `_textural_coherence` scorer wired LAST into
  `doctrine_engine.score_doctrine`; `producer_profile._validate` scorer-list + all
  five profile JSONs (Eno weighted + confidence flip; four at weight 0);
  regenerated sample trees (real-CLI faithful); NEW `tests/test_textural_coherence.py`
  (scorer unit + distinctness) + `test_sample_refresh` / `test_mode_demo_refresh`
  pin updates + re-pin of Eno's moved overall wherever existing tests assert it —
  so the commit is green ON ITS OWN.
- **Commit-2:** the permanent FIVE-WAY differential + sabotage coverage —
  `test_five_way_differential.py` (+ `test_eno_profile.py`): Eno moves, the four
  byte-identical, the axis key present in all five, the confidence-flip asserted,
  the delete/zero-weight + sign-flip mutation bites.

---
_Set active by the orchestrator + confirmed on the user's "go" (2026-07-06, D1=A),
after the P-055 merge — the first engine-deepening packet since the producer arc.
One packet at a time: builder → qa + reviewer → archivist → receipt._
