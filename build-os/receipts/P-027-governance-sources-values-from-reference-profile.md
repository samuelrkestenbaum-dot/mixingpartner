# P-027 — Source `governance.py`'s producer-specific values from the reference profile (byte-identical, WIDENED per Finding A)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. **THIRD extraction step** of the
**producer-agnostic epic** (P-025 extracted the reference profile; P-026 sourced
`creative.py` from it; P-027 sources `governance.py` from it AND widens the profile
with governance's secondary aesthetic constants per P-025's Finding A).
**Type:** Build / feature — in authority, byte-identical. No new decision (the
byte-identical relocation + widening is guarded by P-025's round-trip + the 68/68
regression + the existing governance/taste tests passing UNEDITED). No
honesty-decision needed — this is a VERBATIM relocation of today's values, not
authoring a new profile.

---

## Title / what it does (the mechanism)

`governance.py` now SOURCES its producer-specific judgment FROM the reference
profile (`doctrine/producers/halee_ramone.json`) instead of hardcoded literals,
AND the profile is WIDENED to also hold governance's secondary aesthetic constants
that were inline literals — making the JSON their **single source of truth.**
**Byte-identical by construction** (the reference profile == the old literals, per
P-025's round-trip + the byte-identical proof below).

### Part A — source governance's ALREADY-captured values from the profile
- **`_DEFAULT_PROFILE = load_profile("halee_ramone")`** — added once at module level.
- `_TRUTH_ALIGNMENT = _DEFAULT_PROFILE.truth_alignment`
- `_TASTE_KIND_BIAS = _DEFAULT_PROFILE.taste_kind_bias`
- `TASTE_MAX_DELTA = _DEFAULT_PROFILE.taste_max_delta`
- **The kill-switch SPLIT (load-bearing safety boundary):**
  `KILL_SWITCHES = _SAFETY_KILL_SWITCHES + _DEFAULT_PROFILE.aesthetic_kill_switches`.
  The **5 SAFETY kill-switches (items 1–5, non-destructive / Class-5) STAY
  HARDCODED** in `_SAFETY_KILL_SWITCHES` — they are producer-AGNOSTIC and must
  NEVER come from a swappable profile. The **4 AESTHETIC switches (items 6–9)** are
  appended from `_DEFAULT_PROFILE.aesthetic_kill_switches`. The composed list is
  **byte-identical** to the pre-P-027 9-item literal (same order, same content);
  qa/reviewer confirmed no safety string appears in the JSON.

### Part B — WIDEN the profile with the secondary governance constants (Finding A)
Extended `ProducerProfile` + `halee_ramone.json` + the P-025 round-trip to capture
(verbatim), then SOURCE from the profile, these currently-inline values:
- **`taste_triangle`:** `{intimate_width_penalty: 30, emotion_dims:
  ["ramone_score", "listener_excitement_score", "vocal_belief_score"]}` — the
  `width_bloom + intimate → identity -= 30` penalty (governance line 180) and the
  `emotion` blend = `round(mean of those three scores)` in that FIXED order
  (line 176).
- **`veto_thresholds`:** `{reject_below: 45, align_veto_below: 50, align_fallback:
  75}` — the identity/emotion keep/reject line (line 182), the `govern_variant`
  align veto (`align < 50`), and the unknown-kind align fallback
  (`_TRUTH_ALIGNMENT.get(...).get(kind, 75)`).
`taste_triangle` / `govern_variant` were rewritten to READ these from
`_DEFAULT_PROFILE` instead of the inline literals. The emotion blend reproduces
`round((ramone_score + listener_excitement_score + vocal_belief_score) / 3)`
EXACTLY — same fixed dim order, same `round()` (banker's rounding).

**The no-aliasing invariant (PER-MODULE safety, binding from P-026 — DISCHARGED):**
grep confirmed `governance.py` never mutates a sourced global in place;
`_apply_taste` / `govern_variant` mutate only a LOCAL `triangle` dict, never the
shared `_DEFAULT_PROFILE` structures. A no-aliasing test runs governance on a real
fixture and asserts the shared profile structures are byte-unchanged afterward.

## Scope

**In:**
- `logic-mix-os/logic_mix_os/governance.py` — add `_DEFAULT_PROFILE` +
  `_SAFETY_KILL_SWITCHES`; source `_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS` /
  `TASTE_MAX_DELTA` off the profile; compose `KILL_SWITCHES` = safety (hardcoded) +
  aesthetic (profile); rewrite `taste_triangle` / `govern_variant` to read the
  widened `taste_triangle` + `veto_thresholds` from the profile; delete the inline
  literals.
- `logic-mix-os/logic_mix_os/doctrine/producer_profile.py` — extend
  `ProducerProfile` with `taste_triangle` + `veto_thresholds`.
- `logic-mix-os/logic_mix_os/doctrine/producers/halee_ramone.json` — add the
  `taste_triangle` + `veto_thresholds` fields (captured verbatim).
- `logic-mix-os/tests/test_producer_profile.py` — round-trip for the new fields.
- `logic-mix-os/tests/test_governance_profile_sourced.py` (new) — value-pins for the
  sourced governance globals, the kill-switch boundary (5 safety hardcoded / 4
  aesthetic from profile / byte-identical 9-item list / no safety string in JSON),
  the no-aliasing test, and the exhaustive emotion-blend byte-identical proof.

**Explicitly out (verified UNTOUCHED, byte-identical):**
- `creative.py` (done, P-026), `doctrine_engine.py` (P-028), `pipeline.py` (P-029)
  — byte-unchanged.
- The governance MECHANISM, veto/align algorithm, taste-triangle math, function
  signatures — unchanged (only the SOURCE of the constants moved).
- Per-call / per-variant producer SELECTION — that is P-029.
- Any rename of the `halee` / `ramone` dims (P-030), confidence framework (P-031),
  second producer (P-032), selection surface (P-033).
- Any push / merge / deploy / secret action.

## Commits (branch base + hash)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-027:** `e79426a` — "Merge PR #16: Cowork-usable end-to-end (P-017
  guard + P-018→P-023)", the current default-branch tip; confirmed an ancestor of
  HEAD (`git merge-base HEAD e79426a` = `e79426a`). The P-027 commits sit on the
  P-026 commit (`c4a092d`) and the active-packet confirmation (`b8526a8`), on top of
  the P-025 commits (`195127c` + `e6cb038`), on top of the `e79426a` base.
- **`e4786ca`** — Part A: source governance's already-captured values from
  `_DEFAULT_PROFILE`; split the kill-switches (5 safety hardcoded + 4 aesthetic from
  profile); delete the inline literals; + the no-aliasing guard in
  `test_governance_profile_sourced.py`. **Green in isolation = 343 passed.**
- **`7b1c26d`** — Part B: widen `ProducerProfile` + `halee_ramone.json` with
  `taste_triangle` + `veto_thresholds`; source `taste_triangle` / `govern_variant`
  from them; round-trip for the new fields + emotion-blend byte-identical proof.

Two commits (within ≤2). Byte-identical product relocation + widening + tests.
Author/committer `Claude <noreply@anthropic.com>`; mandated trailers present.

## QA proof (exact)

- **Suite: 331 → 351 passed** (+20; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 343 passed** (`e4786ca` builds and
  passes on its own).
- **Regression: 68/68, 0 critical, 0 warnings — UNCHANGED.** Behavior is
  byte-identical.
- **Byte-identical governance proven — the load-bearing guard:** the existing
  governance/taste tests (`test_governance.py`, `test_governance_taste.py`,
  `test_live_wire.py`; the P-007 / P-008 / P-009 taste tests) pass **UNEDITED** —
  the same governance output on the seeded fixtures, now with the values sourced
  from the JSON instead of literals.
- **Emotion-blend banker's-rounding proven byte-identical:** reviewer exhaustively
  checked ALL **1,030,301** integer score triples (0 mismatches vs. the original
  `round((a+b+c)/3)`); qa checked 51,520 triples PLUS named `.5`-boundary cases
  where banker's rounding matters — 0 mismatches. Same fixed dim order, same
  `round()`.
- **Kill-switch boundary correct:** 5 safety switches hardcoded in
  `_SAFETY_KILL_SWITCHES`, 4 aesthetic switches from
  `_DEFAULT_PROFILE.aesthetic_kill_switches`, the composed 9-item `KILL_SWITCHES`
  list byte-identical to the pre-P-027 literal; NO safety string appears in the JSON.
- **No aliasing (the per-module safety invariant — DISCHARGED):** grep confirmed no
  in-place mutation of the sourced globals; `_apply_taste` / `govern_variant` mutate
  only a LOCAL `triangle`; the no-aliasing test confirms the shared `_DEFAULT_PROFILE`
  structures are byte-unchanged after governance runs on a real fixture. Determinism
  holds.
- **Widened fields round-trip non-vacuously:** the round-trip catches drift (a
  30→25 `intimate_width_penalty` mutation is caught), so the guard is real, not
  vacuous.
- **Scope clean:** `creative.py` / `doctrine_engine.py` / `pipeline.py`
  byte-unchanged.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN.**

## Reviewer verdict

**Pass.** Reviewer confirmed the governance globals are byte-accurately sourced from
the profile, confirmed the kill-switch SPLIT is correct (5 safety stay hardcoded, 4
aesthetic from profile, byte-identical composed list, no safety leakage into the
JSON), independently ran the EXHAUSTIVE emotion-blend proof (all 1,030,301 integer
triples, 0 mismatches), confirmed the no-aliasing invariant (`_apply_taste` /
`govern_variant` mutate only a local triangle; shared profile structures unmutated),
confirmed the widened fields round-trip non-vacuously, and confirmed the three
sibling judgment sources are byte-unchanged.

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Trailer reconciliation — stop the recurring reviewer flag (STANDING NOTE)

Reviewer re-flagged the `Co-Authored-By: Claude Opus 4.8` trailer as a "model
identifier," conflicting with the P-027 packet-spec line "NO model identifier in any
commit message/artifact." **RECONCILED — there is NO violation.** The harness /
`CLAUDE.md` MANDATE that exact `Co-Authored-By: Claude Opus 4.8` trailer
session-wide; "Claude Opus 4.8" is the **sanctioned trailer form**, DISTINCT from
the exact model ID that the identity rule bars. The trailer is required and correct.
**ACTION (standing, applies to P-028+):** DROP the "NO model identifier in any commit
message/artifact" line from FUTURE packet specs — it conflicts with the mandated
trailer and keeps tripping the reviewer. Recorded in residue as a standing spec note.

## Carry-forward WATCH-ITEM — `emotion_dims` couples the profile to `scores` keys (reviewer; mild)

The widened `taste_triangle.emotion_dims`
(`["ramone_score", "listener_excitement_score", "vocal_belief_score"]`) couples the
profile to the exact key names in the runtime `scores` dict. Byte-identical and
correct today, but **watch this coupling when P-028 generalizes scoring and when
P-029 threads the profile per-call** — a rename or restructure of the score keys
must stay in lockstep with `emotion_dims`. Recorded in residue as a mild watch-item.

## Residue / carry-forward

- **The producer-agnostic EPIC is the active roadmap. Arc:** **P-025 ✓ (foundation)
  → P-026 ✓ (creative sourced) → P-027 ✓ (governance sourced + WIDENED; safety
  chassis kept separate)** → **P-028 (doctrine extraction, WIDENED — the LAST and
  LARGEST; capture ALL doctrine scoring functions' constants; +aliasing-proof)** →
  P-029 (parameterize the pipeline / per-call profile) → P-030 (rename the `halee` /
  `ramone` dims off the producer names) → P-031 (confidence framework — consume the
  metadata stamp) → P-032 (second producer) → P-033 (expose producer selection).
- **Finding A now PARTIALLY resolved:** governance's secondary constants
  (`taste_triangle` + `veto_thresholds`) are captured + sourced + round-trip-guarded.
  The **doctrine_engine secondary constants remain OPEN for P-028** (all scoring
  functions' baselines / penalties / coefficients — `_vocal_centrality`,
  `_depth_hierarchy`, `_section_contrast`, `_static_mix`, `_dynamic_mix`).
- **Aliasing-proof requirement (from P-026):** DISCHARGED for governance (P-027);
  remains BINDING for P-028 (doctrine). Do not close P-028 without it. P-029
  (per-call profile) is the structural fix that removes the shared-mutable-global
  risk.
- **Trailer-spec note (standing):** drop the "NO model identifier" line from future
  packet specs (the `Co-Authored-By: Claude Opus 4.8` trailer is mandated and
  correct; the reviewer flag is reconciled).
- **`emotion_dims` coupling watch-item:** watch the profile↔`scores`-keys coupling
  when P-028 generalizes scoring / P-029 threads per-call.
- **Confirmed honesty / sourcing policy (standing product decision, governs
  P-031 / P-032):** hand-curated → high-confidence; derived → low-confidence
  (labeled); LLM → draft-only, NEVER high-confidence. Unchanged.
- Prior standing threads (judgment-layer equilibrium at a doctrine-honest
  equilibrium, live-vs-dead ledger routing, the golden-unguarded variant path, the
  base-fixtures worktree artifact, the optional P-024 MCP-transport step) are
  unchanged and carried forward.

## Stable fact recorded this close

**Safety kill-switches (Class-5 / non-destructive) are producer-AGNOSTIC and stay
HARDCODED in `governance.py` (`_SAFETY_KILL_SWITCHES`); only the AESTHETIC switches
are profile-swappable. A safety switch must NEVER enter a `ProducerProfile`.** This
is the load-bearing boundary that lets the profile become swappable without ever
letting a producer disable a safety guard.

## Open boundaries (awaiting explicit go)

- **P-027 is local-only at this close** — commits `e4786ca` + `7b1c26d` on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1`, on top of the P-026 commit, on
  top of the P-025 commits, on top of the `e79426a` (PR #16) base. **Not pushed /
  merged.** Any push of these commits — and any subsequent PR / merge into the
  protected default — needs the user's explicit go. **No push / merge / deploy /
  secret action taken in this close.** (The build-os-only close commit is separate
  from the product-repo commits above.)

---
_Archivist close, 2026-07-01. THIRD extraction step of the producer-agnostic epic:
`governance.py` now SOURCES its producer-specific judgment (`_TRUTH_ALIGNMENT`,
`_TASTE_KIND_BIAS`, `TASTE_MAX_DELTA`, the 4 aesthetic kill-switches) FROM
`halee_ramone.json`, and the profile is WIDENED (Finding A) with `taste_triangle` +
`veto_thresholds`, now sourced too. The 5 SAFETY kill-switches STAY hardcoded
(producer-agnostic chassis). Byte-identical (existing governance/taste tests pass
UNEDITED; emotion-blend round() proven byte-identical across all 1,030,301 integer
triples; regression 68/68 UNCHANGED); no-aliasing DISCHARGED (mutation is local-only;
shared profile byte-unchanged). Two commits `e4786ca` (green in isolation = 343) +
`7b1c26d`; suite 331 → 351 (+20). Single-reviewer verdict (Codex unavailable).
Trailer reconciled (no violation; drop the "NO model identifier" line going forward).
P-027 local-only, not pushed/merged._
