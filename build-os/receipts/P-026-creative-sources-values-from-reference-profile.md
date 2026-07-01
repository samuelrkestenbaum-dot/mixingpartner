# P-026 — Source `creative.py`'s producer-specific values from the reference profile (byte-identical, single-source-of-truth)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. **FIRST WIRING step** of the
**producer-agnostic epic** (P-025 extracted the reference profile; P-026 makes the
first consumer SOURCE its values from it).
**Type:** Build / feature — in authority, byte-identical. No new decision (the
byte-identical relocation is guarded by P-025's round-trip + the 68/68 regression).
No honesty-decision needed — this is a VERBATIM relocation of today's values, not
authoring a new profile.

---

## Title / what it does (the mechanism)

`creative.py` now SOURCES its 8 producer-specific module globals FROM the reference
profile instead of hardcoded literals, making
`doctrine/producers/halee_ramone.json` their **single source of truth.** The
hardcoded literals are DELETED — the JSON is now their home. **Byte-identical by
construction** (the reference profile == the old literals, per P-025's round-trip).

- **`_DEFAULT_PROFILE = load_profile("halee_ramone")`** — added once at module
  level (imported from `doctrine.producer_profile`). Loads JSON at import: a local,
  deterministic, package-relative read. If the profile is missing/corrupt, import
  fails loudly — correct, since the JSON is now the source of truth.
- **The 8 globals sourced off `_DEFAULT_PROFILE`**, keeping the SAME names/shapes so
  every downstream consumer is untouched: `_KIND_SCORES`, `_NUDGE_TABLE`,
  `_PROMOTION_TABLE`, `CREATIVE_NUDGE_CAP`, `CREATIVE_PROMOTION_CAP`, `_RISK_PENALTY`,
  `SEARCH_MODES`, `PHILOSOPHY`. The nudge/promotion kinds stay SETS (the loader
  rehydrates them); the caps stay `2.0` / `4.0`.
- **No function SIGNATURE changed; no per-call producer threading** (that is P-029).
  The variant KINDS, the scoring MECHANISM, and every algorithm stay byte-identical.
  `governance.py` / `doctrine_engine.py` / `pipeline.py` are byte-unchanged
  (P-027/P-028/P-029 own those).

**The no-aliasing invariant (load-bearing safety):** `score_variant` copies each
`_KIND_SCORES` row via `dict(_KIND_SCORES.get(...))` BEFORE mutating, so the shared
`_DEFAULT_PROFILE.kind_scores` is never mutated in place. qa forced a nudge AND a
promotion to fire, then confirmed the profile's `kind_scores` is byte-unchanged and
determinism holds. **NOTE (carry-forward, below): this copy-before-mutate safety is
a PER-MODULE invariant, not a structural guarantee — each future extraction packet
(P-027 governance, P-028 doctrine) must independently prove its consumers never
mutate a sourced global in place.**

## Scope

**In:**
- `logic-mix-os/logic_mix_os/creative.py` (+47/−71 net; 118 lines changed) — add
  `_DEFAULT_PROFILE`; source the 8 globals off it; delete the hardcoded literals.
- `logic-mix-os/tests/test_creative_profile_sourced.py` (new, +222) — 12 tests:
  value-pins (now that the literals are gone), each global is the profile's object
  with exact type/shape, no-aliasing (nudge + promotion fire, profile unchanged),
  determinism.

**Explicitly out (verified UNTOUCHED, byte-identical):**
- `governance.py`, `doctrine_engine.py`, `pipeline.py` — the other three judgment
  sources; owned by P-027 / P-028 / P-029.
- The nudge/promotion MECHANISM, variant KINDS, function signatures, and every
  scoring algorithm — unchanged.
- Per-call / per-variant producer SELECTION — that is P-029 (this packet only
  relocates the SOURCE of the values, single `_DEFAULT_PROFILE`).
- Any rename of the `halee` / `ramone` dims (P-030), confidence framework (P-031),
  second producer (P-032), selection surface (P-033).
- Any push / merge / deploy / secret action.

## Commits (branch base + hash)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-026:** `e79426a` — "Merge PR #16: Cowork-usable end-to-end (P-017
  guard + P-018→P-023)", the current default-branch tip; confirmed an ancestor of
  HEAD (`git merge-base HEAD e79426a` = `e79426a`). The P-026 commit's direct parent
  is `84d208d` (the P-026 active-packet confirmation), which sits on the P-025
  commits (`195127c` + `e6cb038`) on top of the `e79426a` base.
- **`c4a092d`** — single commit: source the 8 creative globals from
  `_DEFAULT_PROFILE`, delete the hardcoded literals, + new
  `test_creative_profile_sourced.py` (12 tests). **Green in isolation = 331 passed.**
  Touches `creative.py` + the one new test. Author/committer
  `Claude <noreply@anthropic.com>`; trailers present; no model identifier in the
  message body.

One commit (within ≤2). Byte-identical product relocation + tests.

## QA proof (exact)

- **Suite: 319 → 331 passed** (+12; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 331 passed** (single commit == HEAD).
- **Regression: 68/68, 0 critical, 0 warnings — UNCHANGED** (parent `84d208d` is
  also 68/68 once fixtures are generated). Behavior is byte-identical.
- **Byte-identical scoring proven — the load-bearing guard:** the P-012 / P-013 /
  P-015 / P-016 creative tests pass **UNEDITED** (69 combined) — the same
  `analyze()` / `score_variant` output on the seeded fixtures, now with the values
  sourced from the JSON instead of literals. This is the golden-unguarded variant
  path exercised on REAL data.
- **Values spot-checked** against the JSON AND the pre-P-026 git literals — they
  match (the new value-pin tests assert the concrete values now that the literals
  are deleted, so a future JSON edit that changes them is caught).
- **No aliasing (the safety invariant):** qa forced a nudge AND a promotion to fire,
  then confirmed the shared `_DEFAULT_PROFILE.kind_scores` is byte-unchanged
  (`score_variant` copies via `dict(_KIND_SCORES.get(...))` before mutating).
  Determinism confirmed.
- **Scope clean:** only `creative.py` + the new test changed;
  `governance.py` / `doctrine_engine.py` / `pipeline.py` byte-unchanged.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN.**

## Reviewer verdict

**Pass.** Reviewer confirmed the 8 globals are byte-accurately sourced from the
profile (each spot-checked against the JSON and the pre-P-026 literals), confirmed
the copy-before-mutate no-aliasing invariant in `score_variant`, confirmed no
function signature or scoring mechanism changed, and confirmed the three sibling
judgment sources are byte-unchanged. Reviewer raised the **aliasing WATCH-ITEM** as
a binding requirement for P-027 / P-028 (recorded below and in residue).

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Carry-forward WATCH-ITEM — the aliasing invariant is PER-MODULE (reviewer; binding for P-027 / P-028)

The copy-before-mutate safety (copy a sourced global before touching it) is a
**PER-MODULE invariant, not a structural guarantee.** As this sourcing pattern
repeats for **governance (P-027)** and **doctrine (P-028)**, EACH extraction packet
MUST independently PROVE its consumers never mutate the sourced globals in place —
grep for in-place mutation of the sourced structures + a no-aliasing test like
P-026's (fire the relevant path, confirm the shared profile object is byte-
unchanged). **P-029 (per-call profile) reduces this risk** by making the profile
explicitly per-call rather than a shared module global. **Binding requirement for
P-027 / P-028** — recorded in residue.

## Env note — base-fixtures artifact (fully root-caused; reinforce the Stable fact)

The earlier "22 critical" regression scare is **fully explained and is a WORKTREE
ARTIFACT, not a breakage:** fixture STEMS (`fixtures/*/stems/`) are **gitignored**
and generated by `conftest.py`→`ensure_fixtures()` on the first pytest run; a bare
worktree checkout runs `analyze()` against missing audio → false criticals. **Run
pytest (or `fixtures/generate_fixtures.py`) before `cli regression` in a fresh
checkout.** The default and all branch commits (including the parent `84d208d` and
the P-026 commit `c4a092d`) are **68/68 with fixtures present.** Reinforces the
existing Stable fact from P-025.

## Residue / carry-forward

- **The producer-agnostic EPIC is the active roadmap. Arc:** **P-025 ✓ (foundation)
  → P-026 ✓ (creative sourced from the profile)** → P-027 (governance extraction,
  **WIDENED** per Finding A + **aliasing-proof required**) → P-028 (doctrine
  extraction, **WIDENED** per Finding A + **aliasing-proof required**) → P-029
  (parameterize the pipeline to consume the profile, per-call) → P-030 (rename the
  `halee` / `ramone` dims off the producer names) → P-031 (confidence framework —
  consume the metadata stamp) → P-032 (second producer) → P-033 (expose producer
  selection).
- **Aliasing-proof requirement (this packet's carry-forward)** is BINDING for
  **P-027 / P-028** (see the watch-item above).
- **Finding A (secondary governance/doctrine constants, from P-025)** remains the
  standing widening carry-forward, assigned to **P-027 / P-028** (unchanged).
- **Confirmed honesty / sourcing policy (standing product decision, governs
  P-031 / P-032):** hand-curated → high-confidence; derived → low-confidence
  (labeled); LLM → draft-only, NEVER high-confidence. Unchanged.
- Prior standing threads (judgment-layer equilibrium at a doctrine-honest
  equilibrium, live-vs-dead ledger routing, the golden-unguarded variant path, the
  optional P-024 MCP-transport step) are unchanged and carried forward.

## Open boundaries (awaiting explicit go)

- **P-026 is local-only at this close** — commit `c4a092d` on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`, on top of the P-025 commits, on top of
  the `e79426a` (PR #16) base. **Not pushed / merged.** Any push of this commit —
  and any subsequent PR / merge into the protected default — needs the user's
  explicit go. **No push / merge / deploy / secret action taken in this close.**
  (The build-os-only close commit is separate from the product-repo commit above.)

---
_Archivist close, 2026-07-01. FIRST WIRING step of the producer-agnostic epic:
`creative.py` now SOURCES its 8 producer-specific globals (`_KIND_SCORES`,
`_NUDGE_TABLE`, `_PROMOTION_TABLE`, `CREATIVE_NUDGE_CAP`, `CREATIVE_PROMOTION_CAP`,
`_RISK_PENALTY`, `SEARCH_MODES`, `PHILOSOPHY`) FROM `halee_ramone.json`, which is now
their single source of truth; the hardcoded literals are DELETED. Byte-identical by
construction (P-025 round-trip + the 68/68 regression); the P-012/13/15/16 creative
tests pass UNEDITED (69 combined). No-aliasing proven (copy-before-mutate; profile
byte-unchanged after a nudge + promotion fire). Single commit `c4a092d`; suite 319 →
331 (+12); regression 68/68 UNCHANGED. Single-reviewer verdict (Codex unavailable).
Carry-forward: the aliasing invariant is PER-MODULE — P-027 / P-028 must each prove
their consumers do not mutate sourced globals in place. P-026 local-only, not
pushed/merged._
