# Receipt — P-059: Audio-Driven Section Detection

- **Packet:** P-059 — Audio-Driven Section Detection. The engine now **DETECTS**
  section structure from per-stem arrangement activity when a manifest supplies
  none — the pivot from "the engine only *analyzes* the sections it is *given*"
  to "a song with no section map gets a real, contrasting structure inferred
  from the audio." A NEW deterministic detector (`analyzers/section_detector.py`)
  + a guarded `pipeline.analyze` auto-detect wire + a strictly-opt-in scaffolder
  flag. **The whole scoring corpus is provably byte-untouched** — the detector
  only fires when `len(project.sections) <= 1`.
- **User authority + decision:** surfaced by a REAL first-audio session — the
  user ran P-058's on-ramp on a real 49-track song ("Happy Man") and the engine
  analyzed the WHOLE song as ONE block (it only *analyzed* the sections it was
  *given* and never *detected* them), yielding a FALSE "no dynamics / not alive"
  verdict (`Section contrast: n/a`, `Dynamic mix: 40`). The user's directive:
  **infer the sections from the audio — "based on what's added at various
  points."** Opened on the user's "go" (2026-07-06: honest structural+energy
  labels; P-058 merged first via PR #36 → default `32d7f47`).
- **Date:** 2026-07-06
- **Status:** CLOSED — qa GREEN **(suite 1390 → 1405 / 0 failed / 0 warnings;
  +15 = 10 detector + 5 onramp; regression 93/93 with 0 warnings; Commit-1 iso
  1400)** + reviewer **PASS (no must-fix)**. Both gates independently re-ran the
  suite.

## Scope

**In (the confirmed packet spec — the detector + guarded wire + opt-in UX):**

1. **The detector.** NEW `logic_mix_os/analyzers/section_detector.py` (+288) —
   deterministic, **numpy + first-party `dsp` only, ZERO new dependency**.
   Algorithm: per-stem active-region on a common frame grid (`H=0.25s`), a
   two-part silence gate `max(ABS_FLOOR_DB=-50, peak−REL_RANGE_DB=40)`,
   debounce/hysteresis → a boolean activity matrix → **arrangement novelty =
   Hamming distance of the active-set bitmask** (entrances AND exits) →
   boundaries where `novelty ≥ 1`, clustered (~1.0s) → `Section` objects.
   Guardrails: `MIN_SECTION_SEC=4.0` (merge sub-min segments), `MAX_SECTIONS=12`
   (keep top-novelty). Mixdown energy/density novelty is a **tie-breaker ONLY**
   (2nd sort key within an already arrangement-driven cluster — it can never
   create or cap a boundary; the guard against re-creating the false-dynamics
   artifact). Always-on tracks (a full-mix bus / an eternal pad) toggle never →
   contribute ZERO boundaries by construction. Deterministic (fixed grid +
   constants, sorted stem order, no RNG, times rounded to 3 decimals).
2. **Honest labeling.** Structural `section_1..N` + a relative `energy_tag` ∈
   {high, med, low} + `inferred=True`, `emotional_goal=None`. **NO semantic
   verse/chorus/bridge naming** — function is not honestly inferable from audio.
   Two optional, default-OFF `Section` fields (`energy_tag`, `inferred`) added to
   `project.py` (+5) — stamped only on the detector branch.
3. **The guarded integration (the byte-stability boundary).** `pipeline.analyze`
   (+20/−1) branches on `len(project.sections)`: **`>= 2`** runs the UNCHANGED
   `analyze_sections(project.sections, ...)` (the detector is NEVER entered);
   **`<= 1`** runs `detect_sections(loaded_by_id, mixdown, duration)` fed into
   the SAME `analyze_sections`, with `inferred`/`energy_tag` stamped on THAT
   branch only. This is the fix for real sessions like "Happy Man".
4. **The scaffolder opt-in.** `--detect-sections` (default OFF) writes the same
   detected sections into the draft so the user sees + adjusts them; default OFF
   = the byte-identical header-only stub (reads no audio). Shares the ONE
   detector (no second copy — the P-058 `guess_source_kind` shared-helper
   discipline) + a `docs/REAL_SESSION.md` note.

**Explicitly out (binding non-scope, held):**

- **No scoring-math change.** ZERO change to `doctrine_engine.py`,
  `governance.py`, `creative.py`, the 15 axes, kill-switches, the dropout filter,
  the 5 producer profiles, or `analyzers/section_analyzer.py` — the detector is a
  NEW file that produces BOUNDARY DATA feeding the EXISTING `analyze_sections`.
- **Never overrides a manifest's supplied sections** (≥2 → the detector is not
  entered; the supplied-path output shape is untouched).
- **No semantic section naming** (no verse/chorus/bridge — function is not
  honestly inferable from audio).
- **No new dependency** — numpy + first-party `dsp` only (`pyproject.toml`
  blob-identical, absent from the diff). No audio-write, no DAW, no Logic session
  (plan/data only).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2-commit rule honored; local + PUSHED to the dev branch under
  the standing go — NOT merged):**
  - `c44f11c` — "P-059: audio-driven section detection (detector + guarded
    auto-detect wire)" — **4 files, +526/−1**: NEW
    `logic_mix_os/analyzers/section_detector.py` (+288 — the deterministic
    detector); the guarded `pipeline.analyze` auto-detect wire (+20/−1); two
    optional default-off `Section` fields on `project.py` (+5, `energy_tag`,
    `inferred`); NEW `tests/test_section_detector.py` (+214, **10 tests**).
    **GREEN IN ISOLATION at 1400** (the load-bearing commit).
  - `9d1a6a2` — "P-059: scaffolder --detect-sections opt-in (same shared
    detector) + docs" — **4 files, +206/−18**: the scaffolder `--detect-sections`
    opt-in (default OFF, sharing the ONE detector — `onramp.py` +90/−…,
    `cli.py` +14); `tests/test_onramp_scaffold.py` (+90, **+5 tests** → 29) + a
    `docs/REAL_SESSION.md` note (+30). Additive UX — no scoring change.
- **Commit-1 green in isolation:** 1400.
- **Parent / base chain:** `9d1a6a2` → `c44f11c` → `57ab73d` (set-active —
  "build-os: set P-059 (Audio-Driven Section Detection) active — user go") →
  merge base `32d7f47` (= PR #36 merge — P-058 already merged to default).
- **Merge base with default:** verified at close — `git merge-base HEAD 32d7f47`
  = `32d7f47`; the dev branch is fast-forwarded onto default, so a P-059 PR
  carries only `c44f11c` + `9d1a6a2` + the close commit — a clean single-packet
  PR.
- **Push state:** PUSHED to the dev branch under the standing go (the pre-gate
  push). **NOT merged** — the merge of P-059 is a user gate.

## QA proof (GREEN — both gates independently re-ran the suite)

- **Suite:** 1390 → **1405 passed, 0 failed, 0 warnings** (+15: 10 detector + 5
  onramp); regression **93/93** UNCHANGED with **0 warnings** (no score/
  confidence drift); the corpus is **4 fixtures**.
- **Commit-1 iso:** **1400** (detector + guarded wire + the 10 detector tests
  land self-green).
- **Per-file collect:** `test_section_detector.py` = **10**,
  `test_onramp_scaffold.py` = **29** (+5).
- **Byte-stability PROVEN 4 independent ways (the packet's core safety):**
  (a) `git diff 32d7f47..HEAD -- examples/ fixtures/` is **EMPTY**;
  (b) a detector-call SPY shows `detect_sections` invoked **0 times** across all
  4 fixtures + all 5 producer runs (every corpus reports `supplied_sections=2`,
  ≥2 → the unchanged path; zero `inferred`/`energy_tag` key-leak);
  (c) a fresh `write_artifacts` byte-diff = **150/150 sample-tree files (5×30)
  byte-identical**;
  (d) an in-test guard (`test_supplied_sections_do_not_enter_detector`) mocks
  `detect_sections` to raise and asserts `assert_not_called()`.
- **Regression invariant #7 holds:** supplied corpora keep ≥2 sections →
  `section_contrast_score` stays non-None → **93/93, 0 warnings**.
- **Synthetic detection test:** stems pad-throughout + drums in@8/out@32 + bass
  in@16 + vocal in@24 → boundaries at exactly **[0, 8, 16, 24, 32]**, no
  spurious points; the always-on pad → **1 section**; the `MIN_SECTION_SEC` merge
  + `MAX_SECTIONS ≤ 12` guardrails bite; deterministic (twice → identical
  `Section` list).
- **Boundary held (structural):** safety grep = **0 reach** (no push/deploy/
  secret, no audio-write, no new import beyond numpy + first-party); doctrine
  engine / the 5 profiles / governance / creative / kill-switches / dropout
  filter / `analyzers/section_analyzer.py` all UNTOUCHED (the detector is a new
  file feeding the existing `analyze_sections`); **no new dependency**
  (`pyproject.toml` blob-identical, absent from the diff).

## The user's required proof — every clause met

full suite GREEN ✓ (1390 → **1405 / 0 / 0 warnings**, +15 = 10 detector + 5
onramp) · regression **93/93 UNCHANGED** with 0 warnings ✓ · Commit-1 green in
isolation ✓ (1400) · safety grep = 0 reach ✓ (numpy + first-party only; no
push/deploy/secret; no audio-write; no new dependency) · **synthetic
multi-section detection** ✓ (boundaries at exactly [0,8,16,24,32]; always-on pad
→ 1 section; no spurious; guardrails bite) · **supplied-section fixtures (4) +
sample trees (5) byte-identical** ✓ (proven 4 ways: empty examples/fixtures diff;
0-invocation spy; 150/150 byte-identical write_artifacts; the mock-to-raise
in-test guard) · **determinism** ✓ (twice → identical `Section` list) ·
byte-stability (engine / governance / creative / 5 profiles / kill-switches /
dropout filter / `section_analyzer.py` untouched) ✓ · no new dependency ✓.

## Reviewer verdict — PASS (no must-fix)

- The one real risk is that the detector could re-create the very false-dynamics
  artifact that surfaced it — and it structurally cannot: mixdown energy/density
  novelty is a **tie-breaker ONLY** (a 2nd sort key inside an already
  arrangement-driven cluster; it never creates or caps a boundary), always-on
  tracks toggle never → contribute ZERO boundaries by construction, and the
  guarded `len(project.sections)` branch keeps the detector out of every
  supplied-section corpus (byte-stability proven 4 ways). The labeling is honest
  (structural + relative energy, `inferred=True`, no semantic naming). The
  scaffolder shares the ONE detector (no drift-prone second copy) and stays
  strictly opt-in (default path byte-identical).
- **Reviewer's key insight (carried to residue #2):** the constants (`H=0.25s`,
  `ABS_FLOOR_DB=-50`, `REL_RANGE_DB=40`) err toward **UNDER-detection** — bleed/
  noise above -50dB MERGES sections rather than hallucinating them, so the
  detector **FAILS SAFE**: the worst case degrades to today's single-block status
  quo, never a false boundary. They are validated on SYNTHETIC audio only and are
  the tuning knob (a code-change, not a redesign) for the Happy Man re-run.
- **Codex second-eyes:** not separately reported for P-059; consistent with the
  recent single-model posture. No second-model verdict is claimed — recorded as
  such.
- **Cosmetic nit (non-blocking):** an unused `rng = np.random.default_rng(0)` in
  the `test_onramp_scaffold.py` `_write_arrangement_stems` helper (each stem
  makes its own generator) — a dead line, drop in a future cleanup (see Residue
  3). Not a defect.

## Residue (carried to `build-os/memory/residue.md` — accepted standing notes)

1. **★ THE HAPPY MAN RE-RUN (round two) is the immediate next real step — the
   standing TOP open item.** P-059 unblocks it: a re-run of `analyze` on the
   user's real song now AUTO-DETECTS sections (the manifest's 1-section stub →
   `len <= 1` → the detector fires), so the false "Section contrast n/a /
   Dynamic mix 40 / not alive" verdict should collapse and the automation plan's
   blind "open in choruses" rides become song-specific. **This needs the user to
   update their local clone (pull P-059) and re-run** — the real validation of
   whether auto-detected sections sharpen the read.
2. **The detector's constants are validated on SYNTHETIC audio only** (the
   in-memory test + 32kHz fixtures); they have NOT been tuned on real 44.1/48k
   full-length material. They FAIL SAFE toward under-detection (see the reviewer
   insight above). A real-audio CALIBRATION candidate: when the Happy Man re-run
   comes back, check whether detection is granular enough; the constants
   (`H`, `ABS_FLOOR_DB`, `REL_RANGE_DB`) are the tuning knob. **First thing to
   check on that re-run.**
3. **Cosmetic nit (reviewer, non-blocking):** an unused
   `rng = np.random.default_rng(0)` in the `test_onramp_scaffold.py`
   `_write_arrangement_stems` helper — a dead line, drop in a future cleanup.
4. **Prior standing notes + named lessons retained:** the P-058 real-audio gap is
   now further advanced by auto-sections; the Eno/Quincy `<2 beds` neutral-
   fallback calibration knob; the two remaining Eno-deferral analyzers (ambient
   patience #2, generative process #3); CLA-deferred textural
   (Halee/Timbaland/CLA textural weighting still needs grounding); the safety
   line.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-059** — `c44f11c` + `9d1a6a2` (+ this
  close commit) atop `32d7f47` (= PR #36) — a clean single-packet PR (the branch
  is fast-forwarded onto default). Awaits the user's explicit word. The commits
  are pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING opened blind.** The orchestrator PRESENTS the user-gated
  directions, with the **HAPPY MAN RE-RUN (pull P-059, re-run `analyze` →
  auto-sections)** now the highest-value item, then the real-audio constant
  calibration (residue #2), alongside: ambient patience (Eno-deferral #2) ·
  generative process (Eno-deferral #3) · CLA/Halee/Timbaland textural weighting ·
  the `<2 beds` fallback calibration · the real Cowork host connection (manual) ·
  apply-to-Logic (FUTURE, re-gated — never auto; the safety line stands) · a sixth
  producer (roster frozen at five) · anything else the user calls. Do NOT open
  anything blind.

---
_Closed by the archivist (2026-07-06). qa GREEN (suite 1390 → **1405 passed, 0
failed, 0 warnings**; +15 = 10 detector + 5 onramp; regression 93/93 with 0
warnings; Commit-1 iso 1400; per-file collect test_section_detector.py=10 /
test_onramp_scaffold.py=29; byte-stability PROVEN 4 ways — empty examples/fixtures
diff, a 0-invocation detector spy across all 4 fixtures + 5 producer runs, 150/150
sample-tree files byte-identical, and a mock-to-raise in-test guard; the synthetic
detection test lands boundaries at exactly [0,8,16,24,32] with the always-on pad →
1 section and the guardrails biting; deterministic; safety grep 0 reach, no new
dependency) + reviewer PASS (no must-fix; single-model). P-059 makes the engine
DETECT section structure from per-stem arrangement activity when a manifest
supplies none — guarded by `len(project.sections) <= 1` so the WHOLE scoring
corpus is byte-stable, with honest structural + relative-energy labels and NO
semantic naming. The detector FAILS SAFE toward under-detection (bleed merges
rather than hallucinates). The HAPPY MAN RE-RUN (auto-sections, needs the user to
pull P-059 + re-run) is the immediate next validation step and the standing top
open item; the real-audio constant calibration is the first thing to check on that
re-run. The merge is the open user gate._
