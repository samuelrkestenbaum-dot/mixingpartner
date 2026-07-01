# Receipt — P-032b — `groove_coherence` live-wire (third producer-agnostic doctrine axis)

**Date:** 2026-07-01
**Packet:** P-032b — `groove_coherence` live-wire: relocate `analyze_groove` to
BEFORE `score_doctrine` in `pipeline.py`, thread `groove=groove` into
`score_doctrine(..., groove: Optional[Dict] = None)`, REUSE the same groove
object in `result.expanded["groove"]` (computed exactly ONCE), and add
`_groove_coherence(groove, doctrine)` as the 10th doctrine component —
byte-identical for halee_ramone (weight 0). This is the packet where
onset-regularity/IOI (deferred from P-032e AND P-032a) finally reached doctrine.
The **RISKIEST packet of the sub-arc so far** (moved code, not just added).
**Status:** CLOSED — qa **GREEN**, reviewer **PASS**, plus an additional
**adversarial verification pass (3 independent skeptics) — ALL claims HELD.**

---

## Scope

**In:**
- **The live-wire (the P-016 lesson made structural):** `pipeline.py` relocates
  `analyze_groove` to BEFORE `score_doctrine` (pipeline.py:180, before
  `score_doctrine` at :183) and REUSES the exact same computed groove object in
  `result.expanded["groove"]` (:208) — exactly ONE `analyze_groove(` call site,
  never re-run. The relocation is behavior-preserving: `expanded["groove"]`
  byte-unchanged.
- **Threading:** `score_doctrine(..., groove: Optional[Dict] = None)` — keyword,
  default None, so EVERY existing caller (tests included) stays byte-identical.
- **New agnostic scorer** `_groove_coherence(groove, doctrine)` in
  `doctrine/doctrine_engine.py` → the 10th doctrine component. Maps
  `overall_regularity` (0..1) to `baseline + regularity * regularity_scale`;
  None/absent groove → documented neutral fallback float (never None, never a
  crash). Constants read (read-only) from
  `doctrine["scorers"]["groove_coherence"]`.
- **Wiring (byte-identical — identical pattern to P-032e/P-032a):**
  `groove_coherence_score` appended LAST to `component_scores` (9-term summation
  order preserved → overall bit-identical); `evidence["groove_coherence"]`;
  `halee_ramone.json` `doctrine.weights["groove_coherence_score"] = 0` + a
  `doctrine.scorers.groove_coherence` constants block; `producer_profile.py`
  `_validate` requires the `groove_coherence` scorer group;
  `schemas/doctrine_score.schema.json` gains the optional
  `groove_coherence_score` property.
- New `tests/test_groove_coherence.py` (453 lines): byte-identical (incl. the
  `expanded["groove"]` relocation guard), the P-016 no-re-run guard (spy-counted
  exactly-once), real-groove-threading proof, value-discrimination, liveness +
  sabotage, no-aliasing, honest-naming guard.
- Three pre-existing pins updated for the added axis
  (`test_producer_profile.py` scorers set, `test_doctrine_profile_sourced.py`
  `_WEIGHTS` pin, `test_negative_space.py` — negative_space now index 8, with
  the `keys[:8]` anchor intact).

**Explicitly OUT:**
- No new physics/analyzer code — `analyze_groove` itself is UNCHANGED, only
  relocated and threaded.
- No weight change for halee_ramone (weight 0 → byte-identical output).
- No claim of full "identity coherence" — see Honest naming below.

**Honest naming (test-guarded):** `overall_regularity` measures rhythmic
tightness/CONSISTENCY; the scorer's evidence scores regularity/consistency as a
**PROXY for coherence** and never asserts "tighter is better" — the agnostic
layer stays neutral; the *producer* decides the weighting.

**groove_coherence constants:** `neutral 45.0` (absence neither rewarded nor
punished), `baseline 15.0`, `regularity_scale 85.0` (linear map: regularity
0 → 15, 1.0 → 100; dense fixture 0.989 → 99.1).

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base:** set-active `bd98777` (`build-os: set P-032b (groove_coherence
  live-wire) active`), atop `3e991a5` (P-032a close) → `3edcd9c` (P-032a
  Commit 1).
- **`e9f793f`** — P-032b: groove_coherence live-wire — relocate analyze_groove
  before doctrine [single product commit]. 9 files, **582 insertions / 13
  deletions**: `doctrine_engine.py` (+84), `producer_profile.py`,
  `halee_ramone.json`, `pipeline.py` (+29/−…), `doctrine_score.schema.json`,
  `test_groove_coherence.py` (new, 453), + 3 pin updates
  (`test_doctrine_profile_sourced.py`, `test_negative_space.py`,
  `test_producer_profile.py`). **One logically-atomic commit; HEAD IS Commit-1 →
  green in isolation by construction.**

Parent chain: `e9f793f` → `bd98777` (active-packet confirmation) → `3e991a5`
(P-032a close) → `3edcd9c`.

**Merge base for decisions is still `e79426a` = PR #16** (`git merge-base HEAD
e79426a` = `e79426a` — confirmed; nothing since P-025 has been merged). P-032b
is **local-only**, not pushed/merged.

---

## QA proof (GREEN)

- **Full suite:** 413 → **433 passed** / 0 failed / 0 skipped — verified at HEAD
  **AND independently at base `bd98777` in a throwaway worktree** (base = 413).
- **Regression:** **68/68**, 0 warnings, 0 critical.
- **Commit-1 green in isolation:** HEAD **IS** Commit-1 (single-commit packet),
  so the tip is the isolation point = 433.
- **Byte-identical — INDEPENDENT (qa's own capture, not builder pins):** all 9
  pre-existing component scores + overall + `expanded["groove"]`, all 3
  fixtures → **diff EMPTY** (overalls **73.8 / 70.7 / 74.3** unchanged).
- **Compute-once:** exactly ONE `analyze_groove(` call site (pipeline.py:180,
  before `score_doctrine` at :183, reuse at :208).
- **Liveness + sabotage:** gc(0.989) = **99.1**, neutral **45.0** — the liveness
  and sabotage tests pass (threading is genuinely load-bearing).
- **Safety grep:** **NONE FOUND** (582 insertions / 13 deletions across the 9
  in-packet files).
- **Honest-naming guard:** passes ("proxy for coherence", never "tighter is
  better").
- **UI smoke:** N/A (pipeline/doctrine-engine change, no UI surface).

---

## Reviewer verdict — PASS (no must-fix)

- **The relocation crux verified by INJECTED REGRESSIONS in an isolated
  worktree:** re-adding a second `analyze_groove` call turned
  `test_analyze_groove_called_exactly_once` **red** (2==1); threading
  `groove=None` turned `test_score_doctrine_receives_the_real_groove` **red**
  (45.0 ≠ 99.1) — **both guards genuinely load-bearing.**
- **Backward-compat:** keyword default None keeps every existing caller green
  and byte-identical.
- **None-handling:** no KeyError path; the `is None` guard means a real 0.0
  regularity maps to 15.0 — not swallowed into the neutral fallback.
- **Guard updates legitimate:** negative_space now index 8, with the `keys[:8]`
  anchor intact.
- **Codex NOT available — single-model review.**

---

## Adversarial verification (3 independent skeptics — ALL claims HELD)

1. **byte-identical / float-determinism:** 9-component recomputation
   bit-identical on all fixtures; `gc * 0 == 0.0` exactly; the `nan * 0`
   poisoning path is **UNREACHABLE** (`_clamp` neutralizes non-finites;
   `analyze_groove` can only emit None or float[0,1]); relocation side-effects —
   all 8 non-groove `expanded` keys byte-identical.
2. **compute-once / threading:** call-count 1 across ALL branches (ref-delta,
   creative, memory); `expanded["groove"]` IS the same object passed to doctrine
   (`is`-identity); nothing mutates it on the real path; the `groove=None`
   sabotage collapses 99.1 → 45.0 (guard load-bearing).
3. **None/edge robustness:** every None/empty/missing-key case → clamped neutral
   45.0; boundaries clamp to [0,100]; out-of-contract crash inputs
   (strings/lists) proven **UNREACHABLE** from the sole producer.

---

## Residue (deferred / follow-ups / risks)

1. **NEW (adversarial skeptic — cosmetic): shared mutable groove dict.**
   `result.expanded["groove"]` IS the same dict passed to `score_doctrine`
   (shared mutable state); nothing mutates it today (deepcopy-proven), but a
   FUTURE doctrine change mutating its `groove` arg would silently corrupt the
   expanded artifact. Consider a defensive copy or a read-only test pin in a
   future doctrine-touching packet.
2. **Retained:** the liveness-docstring-overclaim note (`test_beat_identity.py`
   + `test_negative_space.py` — and CHECK `test_groove_coherence.py` for the
   same pattern when folding the fix).
3. **Retained:** the P-032e `spectral_flatness` docstring-drift note (harmless;
   fold into a future doctrine touch).
4. **Retained:** the `_DEFAULT_PROFILE` no-aliasing carry-forward (the module
   singleton remains the `None`-default fallback; when a SECOND live profile is
   loaded per call — P-032h — do NOT mutate a loaded profile's structures in
   place).
5. **Scoping-workflow findings for the remaining axes (evidence-backed — the
   next orchestrator needn't re-derive):** P-032d and P-032c need ZERO new
   plumbing (`score_doctrine` already receives everything they read); P-032g's
   `creative.py` gate must default to current behavior (the halee_ramone
   promotion fires exactly as today) and needs the creative-scores byte-identity
   surface; P-032f must NOT edit `role_classifier.py` in place (new
   `vocal_type_classifier.py` + an additive record field), must cap at
   `hook_candidate` (no recurrence signal at doctrine time), and defaults to
   protect-as-lead when uncertain.
6. **Resequenced remaining order (recorded in memory):** P-032d
   (rhythmic_surprise — NEXT, smallest/safest) → P-032c (low_end_motion) →
   P-032g (loop static-vs-iconic) → P-032f (vocal-role — HIGH risk, LAST,
   ★ USER-GATED) → [P-031 confidence] → P-032h (author `timbaland.json`) →
   P-032i (differential proof). P-030 orthogonal/last.

---

## Open boundaries (pending explicit go)

- **No merge / no push handled here.** P-032b's commit `e9f793f` is local on the
  dev branch; the orchestrator owns the build-os close commit + push. **Merge
  base to default is still `e79426a` = PR #16 — NOT merged.** No deploy, no
  secrets touched. P-032f is ★ USER-GATED (needs explicit go on the "masked
  chop/stack = acceptable-blend" aesthetic rule + the conservative
  protect-as-lead-when-uncertain default).

---

## ★ Milestone

**The engine now carries 10 component axes** (7 original + `beat_identity` +
`negative_space` + `groove_coherence`), all three new ones weight-0
byte-identical for the reference producer. **The onset/IOI signal is now LIVE at
doctrine time — unblocking the axes that need rhythm timing.** Triple-verified
close: qa GREEN + reviewer PASS + 3-skeptic adversarial pass, all claims held.
