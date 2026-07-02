# Receipt — P-032f — vocal-role refinement + `vocal_blend_policy`

**Date:** 2026-07-02
**Packet:** P-032f — vocal-role refinement (`vocal_type`) + `vocal_blend_policy`:
the **LAST of the seven Timbaland weight-up axes** (`vocal_role_fit`, the 14th
doctrine component) **plus the SECOND profile-decided gate** (reusing the
P-032g pattern). **★ USER-GATED and CLEARED:** Decision 1 = **B** (acceptable
blend, profile-gated via a REQUIRED field) + Decision 2 = **conservative
default + explicit confidence threshold**. The engine DETECTS vocal function
agnostically; the profile DECIDES the masking philosophy;
safety/governance/non-destructive guarantees invariant.
**Status:** CLOSED — qa **GREEN**, reviewer **PASS (no must-fix)** — dual-green
with **ALL SIX user-mandated adversarial attacks defeated by BOTH gates
independently**.

---

## The user's approved rule table (implemented VERBATIM, binding)

```
lead or uncertain            → protect clarity (full lead-grade protection)
hook_candidate               → protect impact/clarity unless profile explicitly
                               says otherwise later (NOT in this packet)
chop/stutter/adlib or stack
  + profile opt-in
  + confidence threshold met → acceptable blend MAY apply
```

**Misclassification fails CLOSED toward vocal protection.**

---

## Scope

**In:**
- **Commit-1 (pure additive, byte-identical):** NEW
  `analyzers/vocal_type_classifier.py` — pure / deterministic / agnostic;
  **lead identity wins at 0.95**; **fail-closed** at `MIN_STRENGTH 0.6` +
  top-two tie → `vocal_uncertain`; the strongest hook claim CAPPED at
  `vocal_hook_candidate` (no recurrence/provenance signal at doctrine time —
  honesty policy); confidence capped at 0.95; **non-vocal stems → None
  contract**. Additive record fields (`vocal_type` + its confidence) wired in
  `pipeline.py`. New `_vocal_role_fit` weight-0 doctrine axis — the 14th
  component, appended LAST (established idiom); `halee_ramone.json` constants +
  weight 0; `producer_profile._validate` + `doctrine_score.schema.json` + the
  usual pin updates; new `tests/test_vocal_type.py` (**38 tests**).
- **Commit-2 (the profile-gated blend rule):** `vocal_blend_policy` =
  `{acceptable_blend: false, confidence_floor: 0.75}` for `halee_ramone` — a
  **REQUIRED top-level profile field with structural validation**. The gate
  `accepted_blend_under_policy` checks, in order: **flag FIRST →
  lead-by-IDENTITY → categorical type membership (frozenset
  `BLEND_ELIGIBLE_TYPES`) → confidence ≥ floor** — unreachable under
  halee_ramone defaults; new `tests/test_vocal_blend_policy.py` (**22 tests**,
  including the six attack defenses).
- Shared detection basis: the gate reuses the classifier's output — no fork.
- `role_classifier.py` untouched in place (new module instead — user-mandated).
- The 3 interacting live scorers (`_ramone` / `_vocal_centrality` /
  `_static_mix`) read, never rewired — byte-identical for halee_ramone.

**Explicitly OUT:**
- `hook_candidate` blend authority — protect unless explicitly profile-authored
  **LATER** (not in this packet).
- Proven hook status (needs a recurrence/provenance signal that does not exist
  at doctrine time — capped at `vocal_hook_candidate` instead).
- Real-data liveness of the blend gate — see the **reviewer corollary** below
  (an honest boundary; a future analyzer-extension packet, not this one).
- Any Timbaland taste in engine code — the profile authors only the flag + the
  floor.

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base (parent):** `89e792e` (`build-os: set P-032f (vocal-role)
  active — user gate CLEARED: B + stricter`), atop `001f36d` (P-032g close).
- **`3561845`** — P-032f: vocal_type detection + vocal_role_fit — seventh
  producer-agnostic axis [Commit-1]. **10 files, 1066 insertions / 6
  deletions**: `analyzers/vocal_type_classifier.py` (new, 177),
  `doctrine_engine.py` (+128), `pipeline.py`, `producer_profile.py`,
  `halee_ramone.json`, `doctrine_score.schema.json`, `test_vocal_type.py`
  (new, 725), + pin updates (`test_doctrine_profile_sourced.py`,
  `test_producer_profile.py`, `test_loop_context.py`). **GREEN IN ISOLATION:
  550 passed + 68/68 regression — verified in REAL WORKTREES by builder, qa,
  AND reviewer.**
- **`37f25ac`** — P-032f: vocal_blend_policy — the profile-gated
  acceptable-blend rule [Commit-2]. **5 files, 640 insertions / 13 deletions**:
  `vocal_type_classifier.py` (+76), `doctrine_engine.py` (+63 net),
  `producer_profile.py` (+31), `halee_ramone.json`,
  `test_vocal_blend_policy.py` (new, 476).

Parent chain: `37f25ac` → `3561845` → `89e792e` (active-packet confirmation) →
`001f36d` (P-032g close) → `e9e804d`.

**The commits are local AND PUSHED to the dev branch** (branch in sync with
origin). **NOT merged — merge base to default is still `e79426a` = PR #16**
(verified: `git merge-base HEAD e79426a` = `e79426a`); nothing since P-025 has
been merged.

---

## QA proof (GREEN)

- **Full suite:** 512 → **572 passed** / 0 failed / 0 skipped (+60 = 38 + 22).
- **Regression:** **68/68**, 0 critical / 0 warnings.
- **Commit-1 green in isolation:** `3561845` = **550 passed + 68/68** —
  verified in real worktrees by builder, qa, AND reviewer independently.
- **★ DUAL byte-identity — BOTH surfaces, INDEPENDENT:**
  - **(a) Doctrine:** overalls **73.8 / 70.7 / 74.3** untouched; the new
    `vocal_role_fit` axis reads **85.0 × 3** at weight 0.
  - **(b) Creative:** **EMPTY diff**; **zero vocabulary leakage**.
- **★ ALL SIX user-mandated attacks independently defeated** (any success =
  must-fix; zero succeeded), including devious extras: a hand-corrupted lead
  `vocal_type` is STILL protected by IDENTITY; **8 malformed-profile variants
  all raise ValueError** (no silent default); a **288-record sweep** — the
  confidence cap holds.
- **Flag-lever liveness:** the A/B delta is **exactly `masked_penalty`**, with
  `_ramone` / `_vocal_centrality` **byte-identical across A/B** — the lever
  moves only what it claims to move.
- **Safety grep:** **NONE FOUND.**
- **UI smoke:** N/A (analyzer/doctrine/profile change, no UI surface).

---

## Reviewer verdict — PASS (no must-fix)

- **26 independent attack checks — 0 successes:** boundary ≥ pinned BOTH ways
  at the floor; lead+chop hybrid events are never offered to the gate; novel
  type strings refused; the `profile=None` path clean.
- **SIX own sabotages — each caught by named tests.**
- **★ The honest-location finding VERIFIED:** the masking analyzer emits
  vocal-band `bad_masking` ONLY via `_vocal_conflict`, whose elements are
  always `[lead, other]` — the new axis is the ONLY surface where non-lead
  vocal masking manifests, and the gate bites exactly there.
- **Module-constants-for-detection ENDORSED:** detection = shared substrate,
  engine-fixed; profile authors only the flag + the floor — profile-JSON
  thresholds would let profiles fork the physics.
- **Regression-safety explained structurally:** `build_snapshot` is categorical
  + the 7 original keys; the new record fields cannot reach the golden.
- **Codex NOT available — single-model review.**

---

## ★★ Reviewer corollary (BINDING on P-032h / P-032i expectations — an honest boundary, not a defect)

Because today's analyzer emits vocal-band faults **only against the LEAD**, the
blend gate is **INERT on real pipeline data** — exercised only via synthetic
events. **Flipping Timbaland's `acceptable_blend` will produce ZERO real-data
delta through this axis on current fixtures.** P-032i's differential proof
must **NOT** expect a vocal-blend delta; the Timbaland delta will come from
the OTHER axes until the analyzer emits non-lead vocal-band events (a future
analyzer-extension packet).

---

## Residue (deferred / follow-ups / risks)

1. **★ The reviewer corollary (above)** — carried to memory as a binding
   P-032h/P-032i expectation. When the future analyzer-extension packet opens
   (emitting non-lead vocal-band events), note that `creative.py:98`'s
   name-based "vocal" match is a **latent misfire risk** there.
2. **NEW ride-alongs (cosmetic/defensive):** (a) NaN-floor self-guard — add
   `0.0 <= floor <= 1.0` in the raw `accepted_blend_under_policy` gate (qa's
   `math.isfinite` note); (b) `lead_names` in `_vocal_role_fit` derives from
   `vocal_type` rather than `instrument_identity` — identity-derived would be
   sturdier; (c) `_validate` accepts EXTRA keys inside `vocal_blend_policy`;
   (d) the axis ceiling is **85, never 100** — joins lem's 84 as a
   `timbaland.json` weight-authoring consideration (P-032h).
3. **Retained:** all prior carry-forwards — the liveness-docstring six-file
   sweep (CHECK the two new test files `test_vocal_type.py` /
   `test_vocal_blend_policy.py` too when folding); the shared-mutable-groove
   dict (P-032b); the P-032e `spectral_flatness` docstring drift; the
   `loop_deconstruct` literal-kind gate (`creative.py:232`, P-032g); the
   `_DEFAULT_PROFILE` no-aliasing carry-forward (P-032h loads a second
   profile); the P-032d non-adjacent-swing note; lem's `r.get("metrics",{})`
   edge (P-032c).
4. **Staged next:** P-031 (confidence framework fold-in) → P-032h (author
   `timbaland.json` — must declare BOTH `protect_iconic_loops` AND
   `vocal_blend_policy` in writing, REQUIRED fields) → P-032i (differential
   proof — mind the corollary).

---

## Open boundaries (pending explicit go)

- **No merge / no deploy handled here.** P-032f's product commits `3561845` +
  `37f25ac` sit on the dev branch (local AND pushed); the orchestrator owns the
  build-os close commit. **Merge base to default is still `e79426a` = PR #16 —
  NOT merged**; merging to default remains USER-GATED. No secrets touched.

---

## ★★ Milestone

**ALL SEVEN TIMBALAND WEIGHT-UP AXES ARE NOW LANDED** (`beat_identity`,
`negative_space`, `groove_coherence`, `rhythmic_surprise`, `low_end_motion`,
`loop_context`, `vocal_role_fit`) — **14 doctrine components, every one
byte-identical for halee_ramone**. The measurement phase of the Timbaland
sub-arc is COMPLETE. What P-032f proved (the user's own criteria): vocal
function can be measured without changing reference taste; masking philosophy
can be profile-authored; **uncertainty protects the vocal**; Timbaland can
later treat vocal chops/stacks rhythmically **without making the engine
anti-vocal**. `timbaland.json` must declare BOTH `protect_iconic_loops` AND
`vocal_blend_policy` in writing (REQUIRED fields).
