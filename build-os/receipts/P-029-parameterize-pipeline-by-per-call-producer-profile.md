# P-029 — Parameterize the pipeline by a per-call producer profile — `analyze(producer=…)` (THE PIVOT)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. **THE PIVOT of the producer-agnostic
epic.** P-025 extracted the reference profile; P-026/P-027/P-028 sourced
creative/governance/doctrine from it (the EXTRACTION PHASE, byte-identical);
**P-029 threads a PER-CALL profile through the pipeline so `analyze(producer=…)`
SELECTS which profile drives the judgment — the profile stops being a mirror of
today's hardcoded values and becomes a LIVE, selectable lever.**
**Type:** Build / feature — in authority, byte-identical default. No judgment
VALUE changed (guarded by the byte-identical default proof + the 68/68
regression); the new decision is the SELECTION mechanism, proven load-bearing.

---

## Title / what it does (the mechanism)

`pipeline.analyze(..., producer="halee_ramone")` gains an opt-in `producer`
param that accepts EITHER a name OR a ready `ProducerProfile` object (via
`isinstance` dispatch — name → `load_profile`, object → used directly), loads the
profile ONCE per call, and threads `profile=` to the three judgment entry points,
which thread it to EVERY leaf scorer:

- **doctrine:** `score_doctrine(..., profile=)` → all 7 scorers (`_halee` /
  `_ramone` / `_vocal_centrality` / `_depth_hierarchy` / `_section_contrast` /
  `_static_mix` / `_dynamic_mix`) + the component weights read their constants
  from the PASSED profile.
- **creative:** `run_creative_engine(..., profile=)` → `score_variant` /
  `_apply_nudges` / `_apply_promotions` read kind_scores / nudge_table /
  promotion_table / caps / risk_penalty / search_modes / philosophy from it.
- **governance:** `run_governance(..., profile=)` → `govern_branches` /
  `govern_variant` / `taste_triangle` / `_apply_taste` read truth_alignment /
  taste_kind_bias / taste_max_delta / taste_triangle / veto_thresholds from it.

Every entry point + leaf takes `profile: Optional[ProducerProfile] = None` and
defaults to the module `_DEFAULT_PROFILE` when `profile is None`, so existing
direct callers and the no-arg path stay byte-identical.

**KILL_SWITCHES recomposed per call** = the 5 hardcoded producer-AGNOSTIC SAFETY
switches + the passed profile's aesthetic switches, in the same order — **a
swapped producer can NEVER drop a safety guarantee**, and the default composed
list is byte-identical (no safety string appears in the JSON).

**No judgment VALUE changed; the physics/analyzers are untouched.** The safety
kill-switch path is unchanged.

---

## Scope (in / explicitly out)

**In (exactly 5 files — 4 product + 1 new test):**
- `pipeline.py`: `analyze(..., producer: str | ProducerProfile = "halee_ramone")`
  — load once (name or object), pass `profile=` to `score_doctrine` /
  `run_creative_engine` / `run_governance`.
- `doctrine_engine.py`: `score_doctrine` + the 7 scorers thread + read `profile`
  (default `_DEFAULT_PROFILE`).
- `creative.py`: `run_creative_engine` threads `profile` to
  `score_variant` / `_apply_nudges` / `_apply_promotions`.
- `governance.py`: `run_governance` threads `profile` through `govern_branches` /
  `govern_variant` / `taste_triangle` / `_apply_taste`; KILL_SWITCHES recomposed
  per call (5 hardcoded SAFETY + profile aesthetic).
- New `tests/test_producer_selection.py`: byte-identical default +
  selection-liveness (all 3 layers, load-bearing both ways) + determinism.

**Explicitly out:**
- No judgment VALUE change; no physics/analyzers/bridge/planners change.
- Existing tests UNEDITED.
- The module-level `_DEFAULT_PROFILE` singleton STAYS in all 3 consumer modules
  as the `None`-default fallback (removing it is not this packet).
- No second live producer profile authored (that is P-032, user-gated).

---

## Commits (≤2) and branch base

Branch base (merge-base): **`e79426a`** (Merge PR #16: Cowork-usable end-to-end;
current default-branch tip). Dev branch: `claude/logic-mix-os-hardening-12-7hbeh1`.

- **`42d6ebd`** — Thread a per-call producer profile through doctrine + creative +
  analyze (P-029 Commit 1). `creative.py` (+72/…) + `doctrine_engine.py` +
  `pipeline.py` wiring + new `tests/test_producer_selection.py` — byte-identical
  default + doctrine/creative selection-liveness. **Green in isolation = 383.**
- **`ea1aaa9`** (HEAD) — Thread the per-call producer profile through governance +
  the governance liveness proof (P-029 Commit 2). `governance.py` (+82/…),
  `pipeline.py` (final `run_governance` threading), `tests/test_producer_selection.py`
  (+47) — governance selection-liveness (truth_alignment is a live lever).

Parent chain: `ea1aaa9` → `42d6ebd` → `d05105d` (active-packet confirmation) →
`4fdae41` (P-028 close) → … → `e79426a` (base). **P-029 is local-only** (both
commits on the dev branch on top of the `e79426a` base), NOT pushed/merged/deployed.

---

## QA proof (exact, verified by qa + reviewer)

- **Full suite: 370 → 384 passed (+14)** — 0 failed / 0 skipped / 0 warnings,
  green under `-W error`. Existing tests pass **UNEDITED**.
- **Commit-1 green in isolation = 383** (`42d6ebd` alone: doctrine + creative +
  pipeline wiring + byte-identical + doctrine/creative liveness).
- **Regression: 68/68, 0 critical, 0 warnings — UNCHANGED** — the default-path
  byte-identical guard.
- **Byte-identical default PROVEN** — reviewer INDEPENDENTLY byte-diffed the
  default `analyze()` doctrine + creative + governance artifacts pre-P-029 vs HEAD
  across all 3 fixtures → IDENTICAL. no-arg == `producer="halee_ramone"` == the
  reference `ProducerProfile` object.
- **Selection is GENUINELY LIVE across all 3 layers** — through the REAL
  `analyze()` path with synthetic one-value-mutated profiles (NO monkeypatch):
  - **doctrine:** `baselines.halee` −20 → `halee_score` delta exactly 20.
  - **creative:** boosted `vocal_ride` kind_score → that variant's real
    `overall_score` → 100.
  - **governance:** `truth_alignment["intimate"]["vocal_ride"]` 88 → 60 → governed
    `emotional_truth_alignment` 60 (stays above the align veto line so the winner
    is stable and the changed value is the direct observable).
- **LOAD-BEARING proven BOTH ways (the P-016 lesson):** sabotaging each layer's
  threading fails ITS liveness test while the byte-identical / determinism tests
  stay green — proving byte-identical-by-default alone would NOT catch an
  accepted-but-ignored profile. **Reviewer grep: ZERO module-global
  producer-value reads inside any scorer body on the hot path — no leaf missed.**
- **Safety kill-switches intact:** 5 hardcoded SAFETY switches, the composed list
  byte-identical, no safety string in JSON.
- **Scope clean:** exactly 5 files (4 product + 1 new test); existing tests
  UNEDITED; physics / analyzers / bridge / planners untouched.
- **Safety grep:** CLEAN. **UI smoke:** N/A (no UI surface).

---

## Reviewer verdict

**PASS.** Reviewer independently byte-diffed the default `analyze()` output
(doctrine + creative + governance) pre-P-029 vs HEAD across all 3 fixtures
(IDENTICAL), independently verified each layer's liveness delta, confirmed the
threading is load-bearing both ways (sabotage → the layer's liveness test fails
while byte-identical/determinism stay green), and grepped for leftover
module-global producer reads on the hot path (ZERO — no leaf scorer missed). The
per-call KILL_SWITCHES composition was verified to keep the 5 SAFETY switches
hardcoded and byte-identical. **Codex second-eyes: NOT available — single-reviewer
verdict** (consistent with P-025 → P-028).

---

## MILESTONE recorded — THE PIVOT: the profile is now a LIVE, SELECTABLE LEVER

**`analyze(producer=…)` genuinely drives a DIFFERENT plan for a DIFFERENT
profile, proven across doctrine + creative + governance and proven load-bearing.**
The producer-agnostic ARCHITECTURE is now complete and validated:
reference-profile-driven judgment + a producer-AGNOSTIC physics/safety chassis +
per-call producer selection. The profile has stopped being a mirror of today's
hardcoded values and has become a real lever.

What remains: **P-030** (rename the `halee` / `ramone` dimension names off the
producer names) → **P-031** (confidence / honesty framework — consume the
metadata stamp per the honesty policy) → **P-032** (the FIRST SECOND PRODUCER —
the payoff, and the USER-GATED decision point: WHICH producer + grounding per the
confirmed honesty/sourcing policy) → **P-033** (expose producer selection).

---

## Residue — deferred / follow-ups / risks

- **NEXT — P-030 (rename dims off producer names):** rename the `halee` / `ramone`
  dimension names so they describe the aesthetic, not the producer, before a
  second producer lands. Then P-031 (confidence framework), then P-032.
- **★ P-032 is the USER-GATED decision point approaching** — the first SECOND
  producer requires the user's decision: WHICH producer + the grounding per the
  confirmed honesty/sourcing policy (hand-curated → high / derived → low-labeled /
  LLM → draft-only, NEVER high). Flag it before building.
- **★ ALIASING CARRY-FORWARD (reviewer, non-blocking) — for P-032:** the
  module-level `_DEFAULT_PROFILE` singleton STILL exists in all 3 consumer modules
  as the `None`-default fallback, so the per-module copy-before-mutate no-aliasing
  discipline still carries on the DEFAULT path. When P-032 loads a SECOND live
  profile per call, KEEP the aliasing discipline in mind — do NOT mutate a loaded
  profile's structures in place.
- **Standing honesty/sourcing policy (governs P-031/P-032):** hand-curated → high
  confidence; derived → low (labeled); LLM → draft-only, NEVER high. No
  LLM-authored profile may claim `high` confidence.
- **Watch-item (from P-028, still valid):** the measurement-vs-aesthetic
  thresholds (`stereo_width > 0.6`, `distinct <= 1`, `score < 55`) are correctly
  left HARDCODED as physics/presentation, NOT producer taste — keep them out of
  the profile.

---

## Open boundaries (pending explicit go)

- **Merge to default: PENDING explicit go.** P-029 (`42d6ebd`, `ea1aaa9`) is
  local-only on the dev branch on top of the `e79426a` base; NOT
  pushed/merged/deployed. The accumulated producer-agnostic epic (P-025 → P-029)
  plus the earlier local-only arc remain un-landed on default, awaiting a
  user-gated merge decision.
- No push, merge, deploy, publish, or secret access performed in this close.
