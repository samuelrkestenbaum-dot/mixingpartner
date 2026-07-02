# Receipt — P-035: the `vocal_chop_groove` fixture + the real-data vocal-blend differential (the arc's payoff)

- **Packet:** P-035 — the 4th fixture (`vocal_chop_groove`) + the real-data
  vocal-blend differential; **packet 2 of 2 of the user-approved
  analyzer-extension plan (P-034 capacity → P-035 live)**. This is the P-032f
  corollary's FULL resolution: **policy (P-032f, dormant) → capacity (P-034,
  inert) → LIVE, MEASURED, ATTRIBUTABLE (P-035).**
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer PASS (no must-fix).
- **★ THE ANALYZER-EXTENSION ARC (P-034 + P-035) IS COMPLETE.** The last
  promise of the original Timbaland design conversation is now a measured
  product claim: *"Timbaland can treat vocal chops/stacks rhythmically without
  the engine becoming anti-vocal — same stems, two philosophies, 76.3 vs 60.9,
  every point attributable."*

## Scope

**In:**

- **Commit-1 — the buried-vocal analyzer decision:** `masking_analyzer.py`
  reads the vocal-band pair when EITHER side is forward (vocal stem forward OR
  a heard masker-set element in a forward depth in front of it);
  both-sides-buried stays silent (depth-separated arrangement fabric — no
  clarity question). Strictly additive: every P-034 emission preserved
  string-identical. Severity tiering, floors, classification, lead exclusion,
  vocal-vs-vocal exclusion, risk non-contribution, and observational wording
  all unchanged.
- **Commit-2 — the fixture:** `vocal_chop_groove` (6 stems, seed 1003,
  appended after the original three so their bytes can never shift): lead +
  chopped vocal one-shot print ("BGV Chop") + wide sustained stack +
  kick/snare beat + the BINDING P-034 advisory's masker (a bright electric
  guitar with vocal-presence-band partials, overlap ≥ 0.1 against both
  non-lead vocal stems). Generator builders `_vocal_chop` / `_vocal_stack`,
  the manifest, the targeted-script golden, the 13-test
  `tests/test_vocal_chop_groove.py`, the conscious pin flips, README.
- **The conscious pin flips:** the P-032i no-vocal-blend-delta pin flipped
  exactly as its docstring pre-registered (no-delta STILL pinned on the
  original three; the 65-vs-85 delta pinned on the 4th); the regression count
  moved 68/68 → 93/93 consciously; the ten 68/68 count pins updated;
  EXPECTED_SNAPSHOT and every pinned-value suite stay pin-to-3 by conscious
  decision (the 4th fixture's snapshot, component picture and divergence audit
  live in `tests/test_vocal_chop_groove.py`).
- **The three P-034 deferrals revisited and decided** (see "Deferral
  decisions" below).

**Explicitly out:**

- The original 3 fixtures' goldens/manifests/stems — byte-identical discipline
  held (git diff EMPTY; all pins live-verified under both producers).
- The stale `confidence_map` entries surfaced by this packet (→ the NEXT
  packet, per the reviewer's recommendation — see Residue).
- The standing residue-sweep items (producer-named-VALUE surfaces,
  `logic_action_generator.py:38`, validation tightening, etc.).

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `0b940c7` — "P-035: read the vocal-band pair when either side is forward —
    the buried-vocal decision" — 2 files, 90+/34− (`masking_analyzer.py`,
    `tests/test_vocal_band_masking.py`). **Commit-1 GREEN IN ISOLATION: 741 +
    68/68 (real worktree check); fixture-inert at that tree.**
  - `e5a12dc` — "P-035: the vocal_chop_groove fixture — the real-data
    vocal-blend differential goes live" — 17 files, 908+/82− (generator +
    manifest + golden + conftest + the NEW 532-line 13-test
    `tests/test_vocal_chop_groove.py` + the ten count-pin updates +
    `test_differential_proof.py` conscious flip + README).
- **Parent:** `916e577` (active-packet confirmation), atop `4ea1717` (P-034
  close), on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `58d21dd` (= the PR #17 merge, the
  default-branch tip) — verified live at close (`git merge-base HEAD 58d21dd`
  = `58d21dd`).
- **PUSHED to the dev branch (orchestrator-handled), NOT merged.**

## ★ The central finding (Commit-1)

**The moderate event was STRUCTURALLY UNREACHABLE on any real fixture under
P-034's stem-forward-only gate.** A non-lead vocal is necessarily
`backing_vocal`, which the depth planner places forward ONLY at high energy —
exactly where it steps every masker-set instrument to the midground. Disjoint
by construction: no possible fixture could produce a forward non-lead vocal
under a forward/heard masker. The reviewer traced the logic independently and
confirmed it "literally correct." This was the P-034 buried-vocal deferral
resolved in the packet that owned it: either-side-forward, both-sides-buried
stays silent, strictly additive (every P-034 emission preserved
string-identical).

## ★ The measured payoff (Commit-2)

- The chop classifies `vocal_percussive` at **0.95** (transient density 0.805,
  crest 19.25 — **3-of-3 real physics**; the manifest hint alone = 1-of-3 =
  fail-closed 0.33). The stack classifies `vocal_stack` at **0.95** (width
  0.795).
- **4 lead-free `vocal_band_masking` events:** 2 moderate in the verse
  (overlaps 0.2191 / 0.1655), 2 info in the chorus (unconsumed).
- **The differential:** `vocal_role_fit` **65.0** (reference protects clarity)
  vs **85.0** (timbaland accepts blend); overalls **76.3 vs 60.9**; the blend
  gate worth **exactly +0.7** at timbaland's authored 0.4 weight; timbaland's
  overall reconstructs from the reference's measurements + exactly TWO
  authored substitutions (loop static polarity 15→10, blend acceptance 65→85).
- Groove axes read genuinely on the new fixture: `groove_coherence` 99.4,
  `beat_identity` 63.6.

## QA proof (GREEN)

- **Suite:** 741 → **754** passed (+13 = the new fixture's pins). 0
  failed/skipped.
- **Regression:** **68/68 → 93/93** (+25 = +16 golden +9 invariants; the 1
  inapplicable invariant correctly reasoned).
- **Commit-1 isolation:** real worktree check at `0b940c7` → **741 + 68/68**,
  fixture-inert at that tree.
- **Determinism:** 21 stems sha256-identical across double generation.
- **Original 3 fixtures:** git diff EMPTY (goldens/manifests/stems
  byte-untouched) + all pins live-verified under BOTH producers.
- **The either-side-forward gate probed with raw synthetics across 6 depth
  combinations.**
- **Safety grep:** none. **UI smoke:** n/a (no UI surface in this packet).

## Reviewer verdict — PASS (no must-fix)

- The deferral pre-authorization honored (Commit-1 is the P-034 deferral
  flipped in the packet that owned it).
- The synthesis judged honest: the audio delivers the physics; the manifest
  hint is a legitimate provenance idiom (never load-bearing alone —
  fail-closed 0.33 without the audio's 3-of-3).
- **The differential arithmetic verified independently:** 60.9 exact; the
  +0.7 counterfactual; the reference immovable at weight 0.
- **ALL pin flips honor their pre-registrations** — the P-032i flip RETAINS
  the no-delta guard on the original 3.
- **Pin-to-3 endorsed as the right call** (scope-explosion avoidance; nothing
  load-bearing runs only via shared parametrization).
- Golden accounting verified (+25 = 16 + 9).
- **Both sabotages caught:** gate-revert → 7 failures; floor-raise → 6
  failures.
- **Codex NOT available — single-model review.**

## Deferral decisions (the three P-034 deferrals, decided against real data)

- **(a) `per_track_masking_risk` exclusion KEPT** — 4 real events, all risks
  0.0.
- **(b) `severity != "info"` consumption filter KEPT** — the chorus infos are
  the lead-acceptable controlled-overlap shape; consuming them would protect
  non-lead vocals STRICTER than the lead. Consumption-invariance pinned.
- **(c) buried-vocal reading FLIPPED** — Commit-1, the packet that owned it.

## Residue (carried to `build-os/memory/residue.md`)

- **NEW, TOP — the stale `confidence_map` entries (jumps the residue queue
  per the reviewer's recommendation):** BOTH profiles' "limited" vocal-blend
  entries claim a dormancy that is now FALSE on both halves. Contained (no
  scorer consumes the map) but reputationally first for a product whose brand
  is honest labeling. Shape: rewrite the two entries' reasons to live status +
  re-judge levels; consciously flip the verbatim map pins for exactly those
  entries; byte-identical everywhere else.
- **NEW convention note:** FIXTURE_NAMES pinned-to-3 — every future fixture
  needs its own file or a conscious re-parametrization.
- **NEW cosmetic:** the mechanically-repeated "(P-035 moved the corpus count
  consciously…)" parenthetical ~15× across 10 files — a future tidy pass.
- The P-032f inert-blend corollary is **FULLY RESOLVED**
  (policy → capacity → live); the three P-034 deferrals are **DECIDED**
  (a/b kept with pinned justifications, c flipped).
- All standing carry-forwards retained (the residue-sweep list: three
  producer-named-VALUE surfaces, `logic_action_generator.py:38`, validation
  tightening, liveness docstrings, `cli.py` `--mode` text, etc.).

## Open boundaries

- **NOT merged.** The dev branch now carries **FIVE unmerged packets —
  P-033, P-030, P-034, P-035 + closes** — atop merge base `58d21dd` (PR #17).
  **The merge decision is an open USER GATE — no merge without explicit go.**
- Push was orchestrator-handled (`0b940c7` + `e5a12dc` pushed to the dev
  branch); no deploy/publish/secrets touched.
- The **stale-confidence-map fix packet** is STAGED, not active, until the
  orchestrator confirms on the user's go.
