# Receipt — P-042: Profile-Authored Mode Forking (Shape B)

- **Packet:** P-042 — Profile-Authored Mode Forking (Shape B). The packet
  that makes the mode lever LOAD-BEARING: `generate_variants` now READS the
  active mode and forks candidate generation via profile-authored
  `search_modes` declarations — `suppress_kinds` = candidate-SET fork,
  `favor_kinds` = order-only reach, absent = byte-identical neutral. Same
  problem + same producer + different mode → different candidate set; same
  mode name + different producer → differences attributable to
  profile-authored data. ★ RESOLVES the P-033 "thin lever" calibration
  note. The standing doctrine extends to creative reach: **engine owns move
  vocabulary / profile owns mode reach / governance owns safety cap.**
- **User authority (verbatim go, 2026-07-03):** "My call: B —
  Profile-authored mode forking. That is the right next skate." A (mode as
  gate/ranking) explicitly rejected as the final shape; C (new
  mode-specific move families) explicitly rejected FOR THIS PACKET — C
  stays STAGED for after B proves the seam. Full spec (ten required proofs,
  eight adversarial attacks — any success = must-fix — acceptance bar,
  doctrine line) transcribed in the active packet.
- **Date:** 2026-07-03
- **Status:** CLOSED — qa GREEN + reviewer **PASS (no must-fix; all eight
  user-mandated adversarial attacks defeated).**

## Scope

**In (the confirmed packet spec):**

1. **`logic_mix_os/constants.py`** — the frozen `CREATIVE_VARIANT_KINDS`
   vocabulary + the `TRANSLATION_RISK_LEVELS` scale ONLY (the engine owns
   the shared move vocabulary; no new move families).
2. **`logic_mix_os/creative.py`** — THE SEAM: additive `profile` parameter
   (the P-029 `score_variant` pattern); `suppress_kinds` = candidate-SET
   fork; `favor_kinds` = order-only reach; absent declarations =
   byte-identical neutral; suppression can never empty a set — non-empty
   fallback = the full neutral pool, surfaced honestly as
   `suppression_fallback`; runtime fail-closed risk cap; evidence-key
   artifact discipline (fork keys appear ONLY when the fork is live).
3. **`logic_mix_os/doctrine/producer_profile.py`** — load-time validation:
   vocabulary membership, duplicate rejection, favor∩suppress = ∅,
   `allowed_risk` required, over-cap favor "cannot be out-authored" →
   ValueError.
4. **The three producer JSONs** (`halee_ramone.json` / `timbaland.json` /
   `quincy_jones.json`) — EVERY mode explicitly authored (no silent
   inheritance for load-bearing choices); all three DEFAULT/intimate modes
   authored-neutral → defaults byte-identical.
5. **`logic_mix_os/renderers/creative_renderer.py`** — the requirement-10
   surface: "Mode reach" + "_Mode fork:_" lines (non-default renders only).
6. **Tests:** `tests/test_mode_forking.py` (NEW — 21 tests at Commit-1 →
   34 at HEAD; one C1 test consciously subsumed into the 3-producer
   generalization) + `tests/test_creative_profile_sourced.py` (conscious
   pin update — strictly additive, nothing unpinned).

**Explicitly out (the user's non-scope, verbatim):**

- No new mode-specific move families (= Shape C, STAGED). No
  dropout/mute-only negative-space families. No new analyzers. No changes
  to safety/governance/veto behavior. No weakening of allowed-risk caps.
- **No per-producer code branches; no hardcoded Timbaland or Quincy
  behavior in the engine** — held (AST guard + qa grep: zero producer
  names ADDED to engine code).
- No change to existing default behavior except where the profile-authored
  default mode explicitly requires it AND the proof captures it — held:
  defaults byte-identical, zero conscious default-mode fork needed.
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `9acecfd` — "P-042 Commit-1: the mode-forking seam — generate_variants
    reads the mode via profile-authored declarations" — 6 files, +792/−13
    (the seam + loader validation + the reference's explicit authored
    declarations + guards). **Commit-1 green in isolation (894 passed).**
  - `9d746e3` — "P-042 Commit-2: timbaland + quincy mode declarations, the
    three-way mode differential, and the requirement-10 artifact surface" —
    5 files, +290/−27.
  - Combined: **exactly 9 files, +1069/−27** (verified `git diff --stat
    ab4914a 9d746e3` at close).
- **Parent:** `ab4914a` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `dadda12` (= the PR #20 merge —
  P-041, the third producer, landed FIRST). Verified at close:
  `git merge-base HEAD dadda12` = `dadda12`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the FINAL
  SHAs. **NOT merged** — the merge of P-042 is a user gate.

## QA proof (GREEN — the user's ten required proofs, exact counts)

- **Suite:** 873 → **907 passed, 0 failed** (`907 passed in 63.05s`);
  arithmetic closes exactly: +21 at Commit-1, +13 net at Commit-2.
- **Regression:** **93/93** (tests_run 93 / passed 93 / failed 0).
- **Commit-1 GREEN IN ISOLATION:** throwaway worktree at `9acecfd` →
  **894 passed.**
- **Sample trees (requirement 8):** the staleness pin 4 passed WITHOUT
  regeneration; qa independently re-rendered BOTH trees via the verbatim
  README invocations → **byte-identical 30/30 + 30/30**; headlines
  76.3/60.9 unchanged; **zero fork bytes** in committed creative.json
  (grep 0).
- **Default no-drift at the ENGINE level:** 4 fixtures × 3 producers = 12
  default-flow runs at `ab4914a` vs HEAD → byte-identical ordered
  candidate-id JSON.
- **The fork independently reproduced (requirements 2/4):** halee dramatic
  {A,B,C,D} / conservative {B,C,D} / deconstructive {B,C}; the conservative
  three-way — halee {B,C,D} · timbaland {A,B,C,D} · quincy {B,C} —
  pairwise distinct.
- **Attribution (requirements 3/9):** reconstruction from the JSONs on
  disk over **90 producer×mode×problem cells, 0 mismatches**;
  suppress∩emitted = ∅ everywhere; favor = order-only (halee experimental
  [A,D,B,C], set unchanged).
- **Sabotage 4/4 bites:** gutted fork → **10 failed** (builder claimed 5 —
  the net is STRONGER than claimed; qa discrepancy #1, direction safe);
  suppress-field deletion → 2 failed; self-consistent JSON element
  deletion → 1 failed (the real-call-chain pin catches it); cap no-op →
  3 failed; fallback disabled → 3 failed. **qa discrepancy #2:** the
  brief's sabotage-(b) as worded was impossible (timbaland conservative
  authors suppress `[]` — its neutrality IS its differential pole); both
  adjacent probes bite, no gap.
- **Loader validation** (scratch profiles through the REAL load_profile):
  over-cap favor → ValueError; favor∩suppress → ValueError; unknown kind →
  raises at load. Loader-BYPASSING profiles: fail-closed to low; unknown
  kinds inert (tested).
- **Safety grep:** 0 real hits across all categories; **zero producer
  names ADDED to engine code** (every standing pre-packet hit enumerated,
  all pre-existing); the AST guard enforces fork-path code mentions ==
  "halee_ramone" only.
- **Requirement-10 surface (the UI smoke):** the non-default render
  carries `search_mode_declarations` + per-branch `mode_fork` + the
  renderer lines ("Mode reach" / "_Mode fork:_"); the DEFAULT render
  carries ZERO new keys/bytes.

## ★ The user's acceptance bar — every clause met

- **mode becomes load-bearing ✓** — read through every product path incl.
  cowork.
- **candidate sets can differ by mode ✓** — the three-mode fork
  independently reproduced.
- **differences are profile-authored ✓** — the 90-cell reconstruction from
  the JSONs on disk, 0 mismatches; synthetic re-authoring proves
  data-not-code causality.
- **safety caps still bind ✓** — both layers (loader + runtime
  fail-closed) + the reviewer's own probes.
- **no new move families ✓** — the vocabulary pinned = the frozen pool
  union.
- **no producer-specific engine code ✓** — AST guard + qa grep.
- **existing default behavior remains explainable ✓** — byte-identical
  defaults, evidence-key discipline, strictly additive pins.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable;** the reviewer ran its OWN
  executed probes.
- **All EIGHT user-mandated attacks attempted and FAILED:** (1) mode not
  cosmetic — load-bearing through every product path incl. cowork; (2) not
  ranking-only — set-level asserts defeat a ranking-only reimplementation;
  (3) profile data not ignored — attribution reconstructs from the disk
  JSONs; (4) zero hidden producer-specific branches; (5) experimental
  cannot exceed the allowed-risk cap — binds at BOTH layers incl. the
  reviewer's own favor-over-cap + suppress-the-rest probe; (6) suppressed
  kinds never appear; (7) default Halee/Ramone does not drift —
  byte-identical, and the reference pins are strictly additive; (8)
  same-mode/different-producer differences trace to profile data —
  synthetic re-authoring proves data-not-code causality.
- **Non-blocking findings, accepted (no fix cycle → residue):**
  1. **Cap-semantics stated decision:** `allowed_risk` caps authored
     ELEVATION (favor), not pool membership — a loader-legal low-posture
     mode can suppress everything except the one medium-risk kind and
     thereby concentrate emission on it; that kind was always in the
     neutral pool, scoring/governance unchanged. Documented semantics, not
     a hole.
  2. **Dedupe nit:** duplicate favor_kinds from a loader-BYPASSING profile
     duplicate variant dicts in emission (unreachable via load_profile —
     the loader rejects duplicates); one-line dedupe = future hardening
     candidate.
  3. **Quincy experimental** (subtractive_drop + width_bloom) is the
     closest IN-VOCABULARY approximation of the user's "arrangement-lift /
     ensemble-rebalance" example — the true families are STAGED C; named
     as C's motivation.
  4. **winning_variant tie-break:** max = first-wins; favor-reordering
     could flip an EXACT score tie; none exists today, and a favored kind
     winning a tie is arguably authored intent — accepted note.

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, recorded not fixed:**
  1. The cap-semantics stated decision (reviewer finding 1) — elevation
     cap, not pool-membership cap; documented semantics.
  2. The dedupe nit (reviewer finding 2) — loader-bypassing-only; one-line
     future hardening.
  3. Quincy-experimental as in-vocabulary approximation (reviewer finding
     3) — named as Shape C's motivation.
  4. The winning_variant tie-break note (reviewer finding 4).
  5. qa's builder-report discrepancy: gutted-fork sabotage 5 claimed vs
     **10 measured** — direction safe (the net is stronger than claimed).
- The residue list otherwise stays **ZERO** — all prior standing notes and
  the three named lessons retained. The P-033 "thin lever" calibration
  note is ✓ RESOLVED by this packet.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-042** — `ab4914a` + `9acecfd` +
  `9d746e3` (+ this close commit) atop `dadda12` (= PR #20) — awaits the
  user's explicit word. The commits are pushed to the dev branch (standing
  go, pre-gates); NOT merged; no deploy/publish/secrets touched.
- **NEXT per the USER = Shape C — new mode-specific move families (STAGED,
  not active):** extend `CREATIVE_VARIANT_KINDS` + the curated builders
  through a conscious packet; profiles then author reach with ZERO
  loader/fork changes. ★ USER-GATED: not built until the user opens it;
  the orchestrator presents scope first.

---
_Closed by the archivist (2026-07-03). qa GREEN (907 / 93/93 / Commit-1 iso
894 / 12 default-flow runs byte-identical / 90-cell reconstruction 0
mismatches / sabotage 4/4 / safety grep zero real hits) + reviewer PASS (no
must-fix; all eight attacks defeated; single-model — Codex unavailable)._
