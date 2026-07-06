# Receipt — P-056: Textural Coherence Analyzer

- **Packet:** P-056 — Textural Coherence Analyzer. A 15th producer-agnostic
  doctrine axis, `textural_coherence_score` (0–100), measuring bed-similarity
  DISPERSION (Option A, the user's D1=A). The FIRST engine-deepening packet since
  the producer arc: it produces a real per-record number wired into
  `score_doctrine`, weighted non-zero ONLY by Eno (so his overall genuinely
  MOVES), measured-but-weight-0 for the other four (their overall + decisions
  byte-stable). It flips Eno's own confidence_map deferral ("textural coherence
  as its own measurement" — deferred → high). **Zero new DSP, zero new
  dependency** (`statistics` stdlib; deps stay numpy>=1.21).
- **User authority:** opened on the user's "go" (2026-07-06) after the P-055
  merge (PR #33 → default `b03f388`), with **D1 = A confirmed** (textural
  coherence = bed-similarity dispersion). The other Eno-deferral analyzers
  (ambient patience, generative process), the non-Eno weighting taste call, and a
  sixth producer stayed USER-GATED and were NOT touched — this packet is textural
  coherence ONLY.
- **Date:** 2026-07-06
- **Status:** CLOSED — qa GREEN **(suite 1347 / 0; regression 93/93; Commit-1 iso
  1331)** + reviewer **PASS (no must-fix)**. Both gates independently re-ran the
  suite.

## Scope

**In (the confirmed packet spec, D1=A / D2 / D3 defaults accepted):**

1. **The axis** — `textural_coherence_score` (0–100) = 100 − dispersion of the
   texture beds across three equally-weighted sub-terms: **tonal** (`band_energy`
   5-band L1 spread + `brightness` stdev), **spatial** (`stereo_width` stdev),
   **dynamic** (`crest_factor_db` stdev). A PURE cross-bed dispersion statistic —
   it never reads room / occupancy-mean / depth-count / foreground salience /
   rhythm, so distinctness from `negative_space` / `physical_space` /
   `depth_hierarchy` / `groove_coherence` is PROVEN by disjoint-input tests, not
   asserted.
2. **The scorer** — `_textural_coherence` + `_textural_bed_set` +
   `_coherence_from_dispersion` (the mutation-testable sign seam), wired **LAST**
   into `doctrine_engine.score_doctrine` to preserve summation order
   (component_scores + evidence). Bed set replicates the engine-owned
   `_dropout_texture_beds` surface (D3, pinned equal). `<2` beds → **neutral 55.0
   float** (never None / crash; mirrors the negative_space 40 / groove 45
   fallbacks — a single/absent bed cannot be "incoherent").
3. **Profile wiring** — `producer_profile._validate` scorer-list + all five
   profile JSONs gain the identical additive `doctrine.scorers.textural_coherence`
   constants block (sub-weights/scale tunable per-profile, code-change-free);
   Eno weight **1.2** (his high tier = static_mix 1.2, above depth_hierarchy 1.1,
   below physical_space 1.3 / negative_space 1.4), the other four weight **0**;
   Eno's confidence_map entry flipped deferred → high (reason stamped, contains
   "dispersion"). The `doctrine_score.schema.json` gained the labeled key.
4. **Real-CLI-faithful regeneration** — the five sample trees regenerated (the
   P-053 pattern); pin updates (`test_sample_refresh` / `test_mode_demo_refresh`,
   Eno's re-pinned overall, README's pinned Eno cell). NEW
   `tests/test_textural_coherence.py` (Commit-1); the differential + sabotage
   proof `tests/test_five_way_differential.py` + `tests/test_eno_profile.py`
   (Commit-2).

**Explicitly out (binding non-scope, held):**

- **No sixth producer.** No apply-to-Logic / DAW execution. No widened dropout
  reach (`_dropout_protected_names` byte-untouched). No new creative move-kind /
  mode / `score_variant` dim change (this is a DOCTRINE axis). **No weighting of
  the axis for the four non-Eno producers** (Quincy / CLA staged measured-but-0).
- **No governance / kill-switch / veto change; no new dependency.** `governance.py`
  and `creative.py` are ABSENT from the diff; the five JSONs' aesthetic + loudness
  kill-switches, `veto_thresholds`, `protect_iconic_loops` byte-unchanged.
- **No ambient-patience or generative-process work** — both stay deferred; this
  packet deliberately steers clear of the negative-space overlap flagged for the
  sibling analyzers.
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2-commit rule honored; local + PUSHED to the dev branch under
  the standing go — NOT merged):**
  - `acd9a3e` — "P-056 Commit-1: textural_coherence — the 15th doctrine axis
    (bed-similarity dispersion)" — **28 files, +707/−59**: the
    `_textural_coherence` scorer + `_textural_bed_set` + `_coherence_from_dispersion`
    wired LAST into `doctrine_engine.py` (+125); `producer_profile.py` scorer-list
    (+2/−1); all five profile JSONs (identical additive block; Eno weight 1.2 +
    confidence flip, four at weight 0); `schemas/doctrine_score.schema.json` (+1);
    the five regenerated sample trees (only Eno's decision artifacts —
    `dashboard.html` / `doctrine_score.json` / `mix_plan.json` / `mix_verdict.md`
    — moved; the other four gained only the additive `doctrine_score.json` key +
    evidence line); NEW `tests/test_textural_coherence.py` (+383); README's pinned
    Eno cell + the existing-test re-pins (`test_sample_refresh`, `test_eno_profile`,
    `test_cla_profile`, `test_quincy_profile`, `test_timbaland_profile`,
    `test_four_way_differential`, `test_five_way_differential`,
    `test_doctrine_profile_sourced`, `test_producer_profile`, `test_vocal_type`).
    **GREEN IN ISOLATION at 1331** (verified by both qa and reviewer in a detached
    worktree, PYTHONPATH-pinned to that tree).
  - `d6f9b0b` — "P-056 Commit-2: the fifteenth-axis permanent proof (differential
    + sabotage)" — **exactly 2 files, +179**: `tests/test_five_way_differential.py`
    (+151) + `tests/test_eno_profile.py` (+28) — the five-way differential +
    sabotage/mutation coverage. Purely additive proof (+16 → 1347).
- **Commit-1 green in isolation:** 1331 (the axis + all in-tree re-pins land in
  one commit, so it is self-green — Commit-2 is additive proof only).
- **Parent / base chain:** `d6f9b0b` → `acd9a3e` → `81494c2` (set-active —
  "build-os: set P-056 (Textural Coherence Analyzer) active — user go (D1=A)") →
  merge base `b03f388` (= PR #33 merge — P-055 already merged to default).
- **Merge base with default:** verified at close — `git merge-base HEAD b03f388`
  = `b03f388`; the dev branch is fast-forwarded onto default, so a P-056 PR
  carries only `acd9a3e` + `d6f9b0b` + the close commit — a clean single-packet PR.
- **Push state:** PUSHED to the dev branch under the standing go **BEFORE
  qa/reviewer ran** (both gates validated the final SHAs). **NOT merged** — the
  merge of P-056 is a user gate.

## QA proof (GREEN — both gates independently re-ran the suite)

- **Suite:** 1306 → **1347 passed, 0 failed** (+41: +25 Commit-1 axis tests,
  +16 Commit-2 proof tests); regression **93/93** — the corpus is **4 fixtures**.
- **Commit-1 iso:** **1331** (detached worktree, PYTHONPATH-pinned).
- **Per-file collect:** `test_textural_coherence.py` = **25**,
  `test_five_way_differential.py` = **57**, `test_eno_profile.py` = **37**.
- **The axis is measured for all five, weighted only by Eno** (the numbers, all
  measured identically for every producer): per fixture
  `textural_coherence_score` = simple/splice/chop **55.0** (neutral, <2 beds),
  dense **27.0** (2 genuinely dissimilar beds).
- **Eno's committed sample-tree overall MOVED 65.5 → 64.3** (per-fixture: simple
  65.4→64.2, dense 57.8→54.2, splice 59.3→58.8, chop 65.5→64.3). His axis weight
  1.2 sits in his high tier.
- **Weight-0 four-way invariant (byte-proven):** aggregate is `sum(w·s)/sum(w)`,
  so a 0-weight term is arithmetically inert. The four non-Eno overalls are
  BYTE-IDENTICAL base↔HEAD (Halee 76.3, CLA 67.8, Quincy 68.8, Timbaland 60.9);
  their `mix_verdict.md` / `mix_plan.json` / `dashboard.html` byte-identical; only
  their `doctrine_score.json` gained the additive labeled key + evidence line.
  Only Eno's tree moved decision artifacts.
- **Distinctness proof (disjoint-input, both directions):** a dense-but-coherent
  bed set → LOW negative_space / HIGH textural_coherence; a sparse-but-incoherent
  set → the inverse; a constant-section scattered-bed set leaves rhythm/section
  axes fixed while textural_coherence drops — independence from
  negative_space / physical_space / depth_hierarchy / groove_coherence PROVEN.
- **Sabotage / mutation (all non-vacuous — fail loudly under the exact defect
  they name):** zeroing Eno's weight reverts his overall to the pre-axis
  (14-term) value; DELETING the weight raises KeyError (genuinely dereferenced,
  not decorative); flipping the `_coherence_from_dispersion` sign swaps the
  coherent/incoherent ordering (the metric truly reads dispersion). Eno's
  confidence-flip asserted (level high, reason contains the documented stamp +
  "dispersion", weight 1.2).
- **Determinism:** same stems → same score (identical JSON).
- **UI smoke:** Eno's `dashboard.html` regenerated real-CLI-faithful (in the
  moved-artifact set); the four non-Eno `dashboard.html` byte-identical
  base↔HEAD. No UI regression.
- **Diff-proven byte-identical:** `governance.py` and `creative.py` ABSENT from
  the diff; the five JSONs' aesthetic + loudness kill-switches, `veto_thresholds`,
  `protect_iconic_loops` byte-unchanged; no new dependency.
- **Safety grep clean:** 0 reach across the source diff
  (osascript / subprocess / `.logicx` / exec / apply / socket / urllib /
  requests) — no DAW / execution / apply reach.

## The user's required proof — every clause met

suite clean ✓ (1347/0) · regression clean ✓ (93/93) · Commit-1 green in isolation
✓ (1331) · five-way differential ✓ (Eno's overall CHANGES 65.5→64.3 vs his
pre-axis baseline; the four others' overall BYTE-IDENTICAL — the weight-0 proof;
the `textural_coherence_score` key present + measured in ALL FIVE artifacts;
Eno's confidence-flip asserted) · distinctness ✓ (dense-coherent → low
negative_space / high textural_coherence, and the inverse; constant-section
scattered beds leave the rhythm/section axes fixed) · sabotage/mutation ✓ (zero
weight reverts; delete weight → KeyError; sign-flip swaps HIGH/LOW) · determinism
✓ · `governance.py` + the dropout filter byte-untouched ✓ · zero new DSP / zero
new dependency ✓.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- The axis is load-bearing (Eno's overall genuinely moves; the sabotage bites
  prove it is dereferenced, not decorative) and PROVABLY distinct (disjoint
  inputs, not asserted). The weight-0 four-way byte-stability is honest
  (arithmetic inertness, not curation). The `<2 beds → 55.0` neutral fallback is
  the HONEST choice (dispersion is unmeasurable with <2 beds; claiming HIGH would
  be unearned) and mirrors the sibling fallbacks. Real-CLI-faithful regeneration,
  no overclaim. **Latent-trajectory note raised** (the neutral-fallback taste knob
  — see Residue note 1) — NOT a correctness bug, NOT a merge blocker.

## Residue (carried to `build-os/memory/residue.md` — accepted standing notes)

1. **The `<2 beds → 55.0` neutral fallback is a taste knob, not a bug**
   (reviewer's latent-trajectory note): bed-light / single-sustained-bed ambient
   material — the most literally "one woven surface" case — injects 55.0 into
   Eno's weighted mean at weight 1.2, so it reads as MEDIOCRE rather than high and
   nudges his overall down (the 1-bed sample: 65.5→64.3). This is the HONEST
   choice (dispersion is unmeasurable with <2 beds), mirrors the sibling fallbacks
   (negative_space 40 / groove 45), and the value is an explicitly-deferred,
   code-change-free calibration knob in the constants block. Flag for the NEXT
   Eno-calibration pass — NOT a correctness bug, NOT a merge blocker.
2. **The two non-Eno beneficiaries are staged, not wired:** Quincy (ensemble
   cohesion) and CLA (does the wall cohere or merely pile up) are MEASURED-but-
   weight-0 — a future taste call is a one-line weight change. Deferred.
3. **The two remaining Eno-deferral analyzers stay deferred:** ambient patience
   (user rank #2 — flagged for the negative-space overlap risk that must be
   carefully separated) and generative process (rank #3 — flagged as hand-wavy
   without arrangement-time/provenance signals; its confidence entry is
   untouched). This packet was textural coherence ONLY.
- All prior standing notes retained (incl. the P-055 content-dependent
  prose-count residues, the ★★ groove-carrier trajectory watch-item, the CLA
  sha256-self-pin-on-sixth-producer note, the safety line, and the named lessons).

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-056** — `acd9a3e` + `d6f9b0b` (+ this
  close commit) atop `b03f388` (= PR #33) — a clean single-packet PR (the branch
  is fast-forwarded onto default). Awaits the user's explicit word. The commits
  are pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING opened blind.** The orchestrator PRESENTS the user-gated
  directions: ambient patience (Eno-deferral #2, overlap-risk to separate) ·
  generative process (Eno-deferral #3, needs new signals) · the non-Eno textural
  weighting taste call (Quincy / CLA, one-line) · the Eno `<2 beds`
  neutral-fallback calibration · apply-to-Logic (future, re-gated — never auto) ·
  a real external host / MCP-SDK transport swap (manual) · a sixth producer ·
  anything else the user calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-06). qa GREEN (suite 1306 → **1347 passed, 0
failed**; regression 93/93; Commit-1 iso 1331; per-file collect
test_textural_coherence.py=25 / test_five_way_differential.py=57 /
test_eno_profile.py=37; distinctness + sabotage bites non-vacuous; safety grep
clean) + reviewer PASS (no must-fix; single-model — Codex unavailable). P-056 is
the 15th doctrine axis and the FIRST engine-deepening packet since the producer
arc: `textural_coherence_score` (bed-similarity dispersion, D1=A) is now MEASURED
for all five producers and WEIGHTED only by Eno — his overall genuinely moves
(65.5 → 64.3), the four others' overall + decisions byte-stable (weight-0). Eno's
own confidence deferral is flipped deferred → high. Zero new DSP, zero new
dependency; governance + creative + the dropout filter byte-untouched. The merge
is the open user gate._
