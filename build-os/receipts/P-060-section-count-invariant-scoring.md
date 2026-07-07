# Receipt — P-060: Section-Count-Invariant Doctrine Scoring

- **Packet:** P-060 — Section-Count-Invariant Doctrine Scoring. **The FIRST packet
  to intentionally MOVE the committed scoring corpus.** A real 49-track session
  ("Happy Man", 12 detected sections) exposed a correctness bug: `analyze_masking`
  emits each masking conflict **once per section**, and six doctrine scorers
  counted the raw per-section total, so a conflict duplicated across N sections was
  penalized N× ("masked by 48" = 4×12 at 12 sections → emotional_hierarchy /
  vocal_centrality → 0, physical_space → 2). The fix dedups DISTINCT masking
  relationships scorer-side (filter-THEN-dedup) so every masking-driven component
  is section-count-INVARIANT. Penalty coefficients are unchanged — only the COUNT
  they multiply is deduped.
- **User authority + decision:** opened on the user's "ok go" (2026-07-06): dedup
  distinct conflicts (FORK A); accept the authorized surgical `dense` corpus move;
  P-061 (detector calibration) is the next packet. Base = dev HEAD `9cfe990`
  (= PR #37 / P-059 merged to default).
- **Date:** 2026-07-07
- **Status:** CLOSED — qa GREEN **(suite 1405 → 1414 / 0 failed / 0 warnings;
  +9 invariance tests; regression 93/93, critical_failures == [], 0 warnings;
  full suite green at HEAD = the isolation proof)** + reviewer **PASS (no
  must-fix)**. Both gates independently re-ran the suite.

## Scope

**In (the confirmed packet spec — the section-count-invariance fix + its guard +
the one authorized corpus move):**

1. **The fix (FORK A — dedup distinct element-pairs, scorer-side,
   filter-THEN-dedup).** A shared helper in `doctrine/doctrine_engine.py`,
   `_distinct_conflict_count(filtered) = len({frozenset(e["elements"]) for e in
   filtered})`, applied AFTER each scorer's EXISTING classification/severity
   predicate, in six scorers:
   - `_physical_space` (width_crowding),
   - `_emotional_hierarchy` (bad_masking incl. lead),
   - `_vocal_centrality` (bad_masking incl. lead),
   - `_static_mix` (critical low_end_conflict),
   - `_low_end_motion` (crit + mod — the boolean `crit or mod` PRESENCE reads stay
     on the raw lists; only the multiplied COUNTS dedup),
   - `_vocal_role_fit` (`_lead_band_masking` / `_own_band_masking`).
   Penalty COEFFICIENTS unchanged. `_beat_identity` +
   `read_loop_context`/`_loop_context` LEFT UNTOUCHED (already boolean `any(...)` —
   the correct pattern the fix emulates). `masking_analyzer.py` UNTOUCHED — events
   stay per-section (the plan's per-section recommendations are a feature). The
   `vocal_chop_groove` moderate/info ordering guardrail holds (severity filter runs
   FIRST, then dedup).
2. **The invariance regression** (`tests/test_section_count_invariance.py`, 9
   tests): the SAME records scored at **1 vs 6 vs 12** sections → every
   masking-driven component (emotional_hierarchy, vocal_centrality, static_mix,
   low_end_motion, physical_space, vocal_role_fit) IDENTICAL across all three; a
   sanity test that `analyze_masking` really emits N duplicate events yet
   distinct-count == 1; the "masked by N" evidence uses distinct maskers (not
   maskers×sections); an over-correction guard (a masker forward in only 1 of 12
   sections still registers ONCE — `specific < baseline` AND `specific ==
   single-section`).
3. **The one authorized corpus move — ALL ONE correction.** `dense_chorus_with_loops`'s
   `(Kick, Bass)` critical low-end conflict is emitted identically in both sections
   → distinct-count 2×→1× → `static_mix +8.0` (crit_low coeff 8) + `low_end_motion
   +14.0` (critical_conflict_penalty 14), both propagating into the weighted-mean
   overall. Every re-pinned number traces to this single 2×→1× dedup.

**Explicitly out (binding non-scope, held):**

- **No coefficient / weight / policy change.** ZERO change to producer-profile
  JSON, governance, kill-switches, the dropout filter, doctrine weights. Only the
  COUNT the existing coefficients multiply is deduped.
- **No event-emission change.** `masking_analyzer.py` UNTOUCHED — `masking_report.events`
  STAYS per-section (plan detail preserved).
- **No new dependency** — numpy + first-party only.
- **BUG 2 (detector over-segmentation calibration) is NOT in this packet** — it is
  **P-061** (the next packet). P-060 fixes the crater; the fake-100 contrast/dynamics
  persist until P-061.
- Merge — a user gate (see Open boundaries). No push beyond the standing dev-branch
  pre-gate go; no deploy/publish/secrets.

## Commits and base

- **SINGLE ATOMIC commit** (≤2-commit rule honored; the fix + all re-pins are
  INSEPARABLE — split across commits and either half is red, so one commit by
  necessity):
  - `ae0b9fc` — "P-060: section-count-invariant doctrine scoring (dedup distinct
    conflicts)" — **39 files changed, +327/−78**: 1 source
    (`logic_mix_os/doctrine/doctrine_engine.py`, +66-ish net — the shared helper +
    the six scorers using it) + 1 new test
    (`tests/test_section_count_invariance.py`, +197, **9 tests**) + 1 golden
    (`fixtures/dense_chorus_with_loops/golden/snapshot.json`) + 22 mode-demo files
    (`examples/mode_demos/*/creative.{json,md}`) + 14 re-pinned test files. **HEAD
    is the isolation proof** — the full suite is green at HEAD (fix and re-pin are
    one commit).
- **Commit-1 green in isolation:** HEAD = `ae0b9fc` runs the full suite green
  (1414 passed) — the atomic commit IS the isolation.
- **Parent / base chain:** `ae0b9fc` → `8034289` (set-active, metadata-only —
  "build-os: set P-060 (Section-Count-Invariant Doctrine Scoring) active — user
  go") → merge base `9cfe990` (= PR #37 merge — P-059 already merged to default).
- **Merge base with default:** verified at close — `git merge-base HEAD 9cfe990`
  = `9cfe990`; the dev branch is fast-forwarded onto default, so a P-060 PR carries
  only `ae0b9fc` + the close commit — a clean single-packet PR.
- **Push state:** PUSHED to the dev branch under the standing go (the pre-gate
  push). **NOT merged** — the merge of P-060 is a user gate.

## QA proof (GREEN — both gates independently re-ran the suite)

- **Suite:** 1405 → **1414 passed, 0 failed, 0 warnings** (+9 invariance tests).
- **Regression:** `run_regression_suite` **93/93, critical_failures == [], 0
  warnings** after re-pin. The structural `doctrine_invariants` do NOT shift (dedup
  changes no classification/structure). `static_mix +8.0` exceeds `SCORE_WARN=3.0`
  (under `SCORE_FAIL=9.0`), so the golden MUST be re-pinned to the corrected values
  → 0 warnings preserved.
- **Commit-1 isolation:** the single atomic commit `ae0b9fc` runs the full suite
  green at HEAD (1414) — the fix + all re-pins land self-green (they are
  inseparable).
- **Per-file collect:** `test_section_count_invariance.py` = **9** (new).
- **Invariance test is NON-VACUOUS (proven by the reviewer):** the reviewer
  monkeypatched `_distinct_conflict_count` back to `len()` and reproduced the exact
  crater — all six masking-driven components crater with section count. The test
  genuinely catches the bug.
- **The authorized corpus move (each number = the SAME Kick/Bass 2×→1× dedup):**
  - **dense golden** (`fixtures/dense_chorus_with_loops/golden/snapshot.json`):
    static_mix 64.0→72.0, overall 70.7→71.8. UNCHANGED: physical_space 67.6 /
    emotional 86.0 / vocal_centrality 90.0 / vocal_role_fit 85.0 / lowest_components
    / search_mode → no other relationship deduped, no decision/winner shift.
  - **low_end_motion 21.1→35.1** (not a golden key; 5 differential/context test
    pins).
  - **11 mode-demo pairs** (`examples/mode_demos/*/creative.{json,md}`, 22 files):
    the ONLY changed line is `static_mix_score 64→72` — ZERO change to overall,
    dynamic, winners, candidates, declarations, reach, nudges, diagnosis,
    recommendation.
  - **Differential dense-column overalls (all 5 producers):** halee_ramone
    70.7→71.8, timbaland 52.6→54.2, quincy 60.4→61.6, eno 54.2→55.5, cla 59.6→61.5
    (+ eno/quincy pre-axis 14-term baselines). No `simple`/`splice`/`vocal_chop`
    line moved.
  - **BYTE-IDENTICAL (proven):** all 5 sample trees (`examples/sample_output*`,
    vocal_chop-derived — `test_sample_refresh` regen 0 mismatches across 30×5), and
    the other 3 fixtures (simple / splice / vocal_chop — absent from the diff;
    regression recomputes + compares).
- **`test_producer_profile.py` fixup (honest):** four coefficient round-trips built
  DEGENERATE synthetic events (duplicate `elements`, or width events with NO
  `elements` key — which would now KeyError); replaced with realistic distinct
  element pairs so distinct-count == 2; every `coeff × 2` assertion RHS UNCHANGED
  (real analyzer events always carry `elements`). No behavior change concealed.
- **Safety grep = 0 reach:** NO producer-profile JSON change, NO governance /
  kill-switch / dropout / doctrine-weight change, NO new dependency;
  `masking_analyzer.py` untouched; `masking_report.events` STILL per-section. No
  push/merge/deploy/secret beyond the standing pre-gate dev push.
- **UI smoke:** N/A — this is a scoring/engine packet; no UI surface is touched
  (recorded as such, not skipped silently).
- **39 files changed:** 1 source + 1 new test + 1 golden + 22 mode-demo files + 14
  re-pinned test files.

## ★ DEVIATION RECORDED HONESTLY (reviewer's note)

The packet's written "Baseline to protect" said **"mode demos UNCHANGED"** — but
the 11 mode demos are DENSE-DERIVED, so they CORRECTLY moved (`static_mix_score`
only, zero decision/structural change). This is the RIGHT behavior (leaving them
stale at 64 would make committed examples inconsistent with the corrected
pipeline), but it is a DEVIATION from the packet's stated baseline and is recorded
here so the corpus scope is honestly documented. The scope's "only dense moves / 5
sample trees don't move" was correct for the SAMPLE TREES + the other 3 fixtures;
it simply UNDER-COUNTED the dense-DERIVED artifacts (the 11 mode demos + the
differential dense-columns), which move by the SAME one correction (Kick/Bass
2×→1×). No decision, winner, or structural output changed anywhere.

## Reviewer verdict — PASS (no must-fix)

- The fix is minimal and correct: a single shared helper applied AFTER each
  scorer's existing predicate (filter-THEN-dedup), so the `vocal_chop_groove`
  moderate/info ordering guardrail holds and section-specific conflicts still
  register once. Coefficients are untouched; only the multiplied COUNT is deduped.
  The `_low_end_motion` boolean presence reads correctly stay on the raw lists —
  only the counts dedup.
- **Non-vacuity proven:** the reviewer monkeypatched `_distinct_conflict_count`
  back to `len()` and reproduced the exact crater (all six components crater with
  section count) — the invariance test genuinely catches the bug that a real 49-track
  session exposed.
- The one authorized corpus move is fully attributed to a single 2×→1× dedup and
  changes NO decision/winner/structure anywhere; the honest deviation (dense-derived
  mode demos + differential columns move too) is recorded above.
- **Latent semantic note (non-blocking, NOT a defect):** the score no longer
  distinguishes a conflict spanning the WHOLE song from one local to a single
  section. NOT lossy at the data level — per-section `masking_report.events` are
  preserved — so a future packet could add breadth/severity weighting from the
  still-available events without re-plumbing. Low priority (residue #3).
- **Codex second-eyes:** not separately reported for P-060; consistent with the
  recent single-model posture. No second-model verdict is claimed — recorded as
  such.

## Residue (carried to `build-os/memory/residue.md` — accepted standing notes)

1. **★ THE HAPPY MAN RE-RUN #2 (after P-060) — the crater is FIXED, but
   over-segmentation REMAINS until P-061.** With P-060 the vocal/emotional/space
   axes NO LONGER scale with section count (the "masked by 48" → "masked by 4"
   correction). The user should pull P-060 + re-run to confirm the crater is gone.
   BUT `section_contrast` / `dynamic_mix` will STILL read a ceiling-pinned 100/100
   because the detector still over-segments to 12 sections — that is BUG 2, fixed by
   **P-061**. Expectation-set: **P-060 fixes the crater; P-061 fixes the fake-100s.**
2. **P-061 — detector over-segmentation calibration is the immediate next packet**
   (already scoped by the orchestrator: raise `MIN_SECTION_SEC` ~8-10s, raise
   `MIN_RUN` ~1.5s, widen `CLUSTER` ~2s, lower `MAX_SECTIONS` ~8; adaptive novelty
   floor only if needed; byte-stable for the whole scoring corpus, re-pins only the
   ~10 detector tests).
3. **Latent semantic note (reviewer, non-blocking, NOT a defect):** the score no
   longer distinguishes a conflict spanning the WHOLE song from one local to a single
   section. NOT lossy at the data level (per-section `masking_report.events` are
   preserved) — a future packet could add breadth/severity weighting from the
   still-available events without re-plumbing. Low priority.
4. **Prior standing notes + named lessons retained:** the P-059
   detector-fails-safe note is now SUPERSEDED by the real-audio finding that it
   OVER-segments (→ P-061); the Eno/Quincy `<2 beds` neutral-fallback calibration
   knob; the two remaining Eno-deferral analyzers (ambient patience #2, generative
   process #3); CLA-deferred textural (Halee/Timbaland/CLA textural weighting still
   needs grounding); the real Cowork host connection (manual); the safety line.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-060** — `ae0b9fc` (+ this close commit)
  atop `9cfe990` (= PR #37) — a clean single-packet PR (the branch is fast-forwarded
  onto default). Awaits the user's explicit word. The commit is pushed to the dev
  branch (standing go, pre-gates); NOT merged; no deploy/publish/secrets touched.
- **STAGED next: P-061 — detector over-segmentation calibration** (the other half
  of the Happy Man fix; already scoped) is the highest-value item, alongside the
  **HAPPY MAN RE-RUN #2** (pull P-060 → confirm the crater is gone; note contrast/
  dynamics still fake-100 until P-061). Then the remaining user-gated directions:
  ambient patience (Eno-deferral #2) · generative process (Eno-deferral #3) ·
  CLA/Halee/Timbaland textural weighting · the `<2 beds` fallback calibration · the
  real Cowork host connection (manual) · apply-to-Logic (FUTURE, re-gated — never
  auto; the safety line stands) · a sixth producer (roster frozen at five) ·
  anything else the user calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-07). qa GREEN (suite 1405 → **1414 passed, 0
failed, 0 warnings**; +9 invariance tests; regression **93/93, critical_failures ==
[], 0 warnings**; full suite green at HEAD = the isolation proof for the single
atomic commit) + reviewer PASS (no must-fix; single-model; non-vacuity proven by
monkeypatching the helper back to `len()` → the exact crater reproduces). P-060 is
the FIRST intentional corpus move: `analyze_masking` emits each conflict once
per-section and six doctrine scorers counted the raw per-section total, so a
conflict duplicated across N sections was penalized N× — real many-section songs
cratered. The fix dedups DISTINCT masking relationships scorer-side (filter-THEN-dedup)
so every masking-driven component is section-count-INVARIANT; coefficients unchanged,
only the count they multiply is deduped; `masking_analyzer.py` untouched (events stay
per-section). One authorized surgical corpus move — dense's Kick/Bass critical
low-end 2×→1× — propagated consistently to all dense-DERIVED artifacts (golden
static_mix 64→72 / overall 70.7→71.8, low_end_motion 21.1→35.1, the 11 mode demos
static_mix-only, the differential dense-columns for all 5 producers); the 5 sample
trees + the other 3 fixtures proven BYTE-IDENTICAL. HONEST DEVIATION recorded: the
packet said "mode demos UNCHANGED" but they are dense-derived and correctly moved
(static_mix only, zero decision change). Single atomic commit `ae0b9fc` (39 files,
+327/−78) atop set-active `8034289` atop merge base `9cfe990` (= PR #37); verified
`git merge-base HEAD 9cfe990` = `9cfe990`; PUSHED to the dev branch, NOT merged. The
merge is the OPEN USER GATE. P-061 (detector over-segmentation calibration) is the
immediate next packet — the Happy Man re-run #2 confirms the crater-fix, but the
fake-100 contrast/dynamics persist until P-061._
