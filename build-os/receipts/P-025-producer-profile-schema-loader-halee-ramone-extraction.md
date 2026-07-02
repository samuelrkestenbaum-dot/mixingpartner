# P-025 — `ProducerProfile` schema + `load_profile()` + extracted `halee_ramone.json` reference (data + loader ONLY, no wiring)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. **FOUNDATION step** of the new
**producer-agnostic epic** (make the engine select any producer's judgment as a
swappable `ProducerProfile`; the physics stays fixed).
**Type:** Build / feature — in authority, additive. Data + loader + tests only;
nothing consumes the profile, so behavior is trivially byte-identical. No
honesty-decision needed for this extraction (the confirmed sourcing policy binds
authoring a SECOND profile, P-031+, not this VERBATIM extraction of today's
values).

---

## Title / what it does (the mechanism)

Creates the schema + loader + reference data that make today's 100%-hardcoded
Roy-Halee/Phil-Ramone judgment a swappable, honestly-stamped artifact — WITHOUT
wiring anything to consume it. Three new files:

- **`logic_mix_os/doctrine/producer_profile.py`** — a **frozen `ProducerProfile`
  dataclass** (immutable view over every producer-specific value the pipeline
  hardcodes) plus a pure **`load_profile(name="halee_ramone")`** that reads the
  JSON, validates it against the schema, rejects an unknown producer, and returns
  the frozen profile. Deterministic, local file read only — no network / DAW /
  subprocess.
- **`logic_mix_os/doctrine/producers/halee_ramone.json`** — the **reference
  profile** holding today's producer-specific values **VERBATIM, extracted FROM
  CODE.** This is the load-bearing honesty correction: the pre-existing
  `roy_halee.json` / `phil_ramone.json` are **prose the scorer never reads**; the
  real judgment lives in Python constants and inline-computed coefficients. The
  reference profile captures the *actual* values, not the prose.
- **`tests/test_producer_profile.py`** — the binding guard (round-trip identity,
  extraction-completeness, schema/metadata, determinism, immutability).

**The extraction mechanism (extract, don't change):** the profile is populated
from the live module constants; the round-trip test then asserts the loaded
profile reconstructs each live structure. Two capture classes:

- **Exact-equal (clean module constants):** `kind_scores` (= `creative._KIND_SCORES`),
  `nudge_table` / `promotion_table`, the caps (`CREATIVE_NUDGE_CAP = 2.0` /
  `CREATIVE_PROMOTION_CAP = 4.0`), `_RISK_PENALTY`, `SEARCH_MODES`, `PHILOSOPHY`,
  `_TRUTH_ALIGNMENT`, `_TASTE_KIND_BIAS`, `TASTE_MAX_DELTA`, and the **aesthetic**
  kill-switches `KILL_SWITCHES[5:9]` (items 6–9 only). The **safety** kill-switches
  (items 1–5, non-destructive / Class-5) are **correctly EXCLUDED** — they are
  producer-AGNOSTIC and stay universal; qa/reviewer verified the slice.
- **Indirect (values computed INLINE, not stored as constants):** `doctrine.weights`,
  the `86.0` baselines, `penalty_coeffs`, and `default_creative_mode` are not
  module constants — they are computed inside `_halee` / `_ramone` /
  `_default_creative_mode`. Their round-trip is asserted **by driving the real
  functions one condition at a time** and matching the captured coefficients. This
  was proven **non-vacuous:** qa mutated `ramone.vocal_masked` 6 → 7 and the test
  FAILED, confirming the assertion actually binds the extracted value to the code.

**Metadata / honesty stamp (scaffolding for the confirmed sourcing policy):** the
profile carries `{name: "halee_ramone", display_name: "Roy Halee / Phil Ramone",
provenance: "hand-curated-documented", confidence: "high", risk_class: 0}`. The
tests assert `confidence == "high"`, `provenance == "hand-curated-documented"`,
`risk_class == 0` (a judgment profile is observe-only, not a destructive action).
Nothing enforces/propagates this stamp yet — it is consumed in P-031.

**The no-wiring guarantee (load-bearing):** `creative.py`, `governance.py`,
`doctrine_engine.py`, `pipeline.py` are **byte-for-byte unchanged** (verified:
none appears in the `e79426a..HEAD` diff). No runtime module imports
`load_profile` (verified: the only references are the module itself + its
pycache). The regression is UNCHANGED because nothing consumes the profile.

## Scope

**In:**
- `logic-mix-os/logic_mix_os/doctrine/producer_profile.py` (new, +160) — frozen
  `ProducerProfile` dataclass + pure `load_profile()`.
- `logic-mix-os/logic_mix_os/doctrine/producers/halee_ramone.json` (new, +119) —
  the extracted reference profile (VERBATIM from code) + honesty metadata stamp.
- `logic-mix-os/tests/test_producer_profile.py` (new, +344 across the two commits)
  — round-trip identity (exact + indirect), extraction-completeness,
  schema/metadata, determinism, immutability / non-aliasing.

**Explicitly out (verified UNTOUCHED, byte-identical):**
- `creative.py`, `governance.py`, `doctrine_engine.py`, `pipeline.py` — the four
  judgment source files; they still use their hardcoded dicts / inline
  computations. **Nothing in the runtime imports or consumes `load_profile`.**
- The pre-existing prose `roy_halee.json` / `phil_ramone.json` — left in place;
  they were never read by the scorer and are not the reference profile.
- Any wiring, parameterization, rename, confidence-framework, second-producer, or
  selection surface — those are P-026 → P-033, deferred by design.
- Any push / merge / deploy / secret action.

## Commits (branch base + hash)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-025:** `e79426a` — "Merge PR #16: Cowork-usable end-to-end (P-017
  guard + P-018→P-023)", the current default-branch tip; confirmed an ancestor of
  HEAD (`git merge-base HEAD e79426a` = `e79426a`). (`4e9eaa2` was the P-025
  active-packet confirmation.)
- **`195127c`** — Commit-1 (test-first): `ProducerProfile` schema + `load_profile()`
  + `halee_ramone.json` + the round-trip / determinism tests. **Green in isolation
  = 311 passed.** Touches the two new product files + `test_producer_profile.py`.
- **`e6cb038`** — Commit-2: extraction-completeness + schema/metadata tests
  (extends `test_producer_profile.py` only, +86). No source module changed.

Two commits (within ≤2). Additive product data + loader + tests.

## QA proof (exact)

- **Suite: 293 → 319 passed** (+26; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 311 passed.**
- **Regression: 68/68, 0 critical, 0 warnings — UNCHANGED** across both commits
  (nothing wired → goldens + judgment identical).
- **Byte-identical round-trip proven — the load-bearing guard:** the extracted
  `halee_ramone.json`, loaded via `load_profile`, reconstructs each live module
  structure exactly. **Exact-equal** for the clean constants (kind_scores,
  nudge/promotion tables, caps 2.0/4.0, `_RISK_PENALTY`, SEARCH_MODES, PHILOSOPHY,
  `_TRUTH_ALIGNMENT`, `_TASTE_KIND_BIAS`, TASTE_MAX_DELTA, `KILL_SWITCHES[5:9]`).
  **Indirect** for the inline-computed values (doctrine weights, 86.0 baselines,
  penalty_coeffs, default_creative_mode) — asserted by driving `_halee` /
  `_ramone` / `_default_creative_mode` one condition at a time. The round-trip is
  an **honest set-vs-set compare, not loosened.**
- **Round-trip proven NON-VACUOUS:** qa mutated `ramone.vocal_masked` 6 → 7 → the
  test FAILS. The indirect assertion genuinely binds the extracted coefficient to
  the code.
- **Extraction-completeness:** every producer-specific structure named in the
  packet has a profile home (no silent omission), plus the doctrine subfields
  present.
- **Schema validity + metadata:** `load_profile` validates the JSON and rejects an
  unknown producer; metadata fields present and typed; `confidence == "high"`,
  `provenance == "hand-curated-documented"`, `risk_class == 0`.
- **Immutability / non-aliasing:** the returned profile is frozen; loading does
  NOT mutate the live module dicts.
- **Scope clean:** only the 3 new files changed; the 4 judgment source files are
  byte-unchanged; nothing in the runtime imports `load_profile`.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN.**

## Reviewer verdict

**Pass.** Reviewer HAND-VERIFIED every extracted value byte-accurate against its
source (each constant compared to its live module definition; each inline
coefficient traced through `_halee` / `_ramone` / `_default_creative_mode`),
confirmed the aesthetic kill-switch slice `KILL_SWITCHES[5:9]` is correct and the
safety items 1–5 are correctly EXCLUDED, confirmed the metadata stamp matches the
confirmed honesty policy, and confirmed the no-wiring guarantee (the four judgment
sources byte-unchanged, nothing consumes the profile).

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Finding A — the COMPLETENESS carry-forward (reviewer; IMPORTANT for the epic arc)

P-025 captured what its scope declared, but there are ADDITIONAL
producer-aesthetic constants **not yet in the profile** that the arc MUST capture
before it can claim FULL producer-agnosticism (**deferred by design, not drift**).
Assigned explicitly to the two extraction packets:

- **WIDEN P-027 (governance extraction) to ALSO capture:** `governance.py`
  (~lines 179–182) — the `taste_triangle` inline rule `width_bloom + intimate →
  identity -= 30` (a sibling of `_TASTE_KIND_BIAS`); the `<45` reject / `<50`
  align-veto / `75` align-fallback thresholds; and the `emotion` blend definition
  (~line 176).
- **WIDEN P-028 (doctrine extraction) to capture ALL doctrine scoring functions'
  constants** (not just `_halee` / `_ramone`): `_vocal_centrality`,
  `_depth_hierarchy`, `_section_contrast`, `_static_mix`, `_dynamic_mix` — their
  baselines (80.0, 70.0, 40), penalties, and coefficients (e.g.
  `30 + rms_std*8 + width_std*140`).

The P-025 round-trip guard is the safety net these packets will rely on as they
widen the profile.

## Env note — recorded so it is NOT re-litigated (base-fixtures artifact)

qa observed the BASE commit `e79426a` (the PR #16 merge = current default tip)
reporting **"22 critical" regression failures in a detached worktree.** **This is
a WORKTREE ARTIFACT, not a real breakage — VERIFIED:** `fixtures/` content is
GENERATED (not committed), so a bare checkout that never ran
`fixtures/generate_fixtures.py` fails the golden regression. With fixtures
generated, `e79426a` passes **68/68** (the orchestrator-in-chief re-ran it
directly). **The default branch is HEALTHY.** Recorded as a Known-fact:
*regression requires generated fixtures — run `fixtures/generate_fixtures.py` (or
pytest via conftest) before `cli regression` in a fresh checkout; a bare worktree
shows false critical failures.*

## Residue / carry-forward

- **The producer-agnostic EPIC is the active roadmap** (this receipt opens it):
  **P-025 ✓ (foundation)** → P-026 (creative extraction) → P-027 (governance
  extraction, **WIDENED** per Finding A) → P-028 (doctrine extraction, **WIDENED**
  per Finding A) → P-029 (parameterize the pipeline to consume the profile) →
  P-030 (rename the `halee`/`ramone` dims off the producer names) → P-031
  (confidence framework — consume the metadata stamp) → P-032 (second producer) →
  P-033 (expose producer selection).
- **Finding A (secondary constants)** is the explicit carry-forward, assigned to
  **P-027 / P-028** (see above).
- **Confirmed honesty / sourcing policy (standing product decision, governs
  P-031 / P-032):** hand-curated → high-confidence; derived → low-confidence
  (labeled); LLM → draft-only, NEVER high-confidence. The `halee_ramone` reference
  is hand-curated-documented → high-confidence, consistent with this policy.
- Prior standing threads (judgment-layer equilibrium, live-vs-dead ledger routing,
  golden-unguarded variant path, the optional P-024 MCP-transport step) are
  unchanged and carried forward.

## Open boundaries (awaiting explicit go)

- **P-025 is local-only at this close** — commits `195127c` + `e6cb038` on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `e79426a` (PR #16)
  base. **Not pushed / merged.** Any push of these commits — and any subsequent
  PR / merge into the protected default — needs the user's explicit go. **No push /
  merge / deploy / secret action taken in this close.** (The build-os-only close
  commit is separate from the two product-repo commits above.)

---
_Archivist close, 2026-07-01. FOUNDATION of the producer-agnostic epic: today's
100%-hardcoded Halee/Ramone judgment is now a frozen `ProducerProfile` + a pure
`load_profile()` + a VERBATIM-extracted `halee_ramone.json` reference, guarded by
a byte-identical round-trip (exact + non-vacuous indirect), stamped with the
confirmed-honesty metadata (hand-curated-documented / high / risk_class 0), and
**completely unwired** (the four judgment sources byte-unchanged; regression 68/68
UNCHANGED). Two commits `195127c` + `e6cb038`; suite 293 → 319 (+26). Single-
reviewer verdict (Codex unavailable). Finding A (secondary governance/doctrine
constants) is carried forward to a WIDENED P-027 / P-028. Base-fixtures env note
recorded: the base is healthy; a bare worktree needs generated fixtures._
