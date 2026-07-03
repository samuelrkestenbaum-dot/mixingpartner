# Receipt — P-043: Curated Move Vocabulary Expansion: Arrangement Lift + Ensemble Rebalance

- **Packet:** P-043 — Curated Move Vocabulary Expansion: Arrangement Lift +
  Ensemble Rebalance (the user's title, verbatim). Shape C, opened NARROWLY:
  the move vocabulary widens from 7 to **9 kinds — 7 neutral + 2 reach-gated
  EXTENDED** (`arrangement_lift` + `ensemble_rebalance`). An extended kind
  NEVER joins the neutral emission pool: it emits ONLY when the active mode's
  authored `reach_kinds` declaration reaches for it. The standing doctrine
  holds and deepens: **the engine curates the families / the profile authors
  reach / governance caps.** Quincy's mode behavior is now GENUINELY MUSICAL
  (the user's product intent for C) — his P-042 in-vocabulary approximation
  favor is consciously REPLACED by real authored reach.
- **User authority (verbatim go, 2026-07-03):** "Merge P-042 now. Then open
  Shape C, but narrowly: arrangement_lift + ensemble_rebalance only." —
  P-042 merged FIRST as PR #21 (default tip `17cc270`), then this packet.
  **Negative-space dropout EXPLICITLY EXCLUDED by the user:** "higher risk…
  smells more Timbaland-specific. It should come after C proves the widened
  vocabulary can stay governed."
- **Date:** 2026-07-03
- **Status:** CLOSED — qa GREEN + reviewer **PASS (no must-fix; all adapted
  adversarial attacks defeated).**

## Scope

**In (the confirmed packet spec):**

1. **`logic_mix_os/constants.py`** — `CREATIVE_VARIANT_KINDS` 7→9;
   `CREATIVE_EXTENDED_KINDS = (arrangement_lift, ensemble_rebalance)`; the
   dropout family's ABSENCE documented as the next user-gated decision.
2. **`logic_mix_os/creative.py`** — THE REACH SEAM: `reach_kinds` = the
   THIRD per-mode declaration (extended-vocabulary-only at load); reached
   variants append AFTER the neutral pool; `favor_kinds` stays order-only
   for the original seven; suppression beats reach; the fallback is
   neutral-pool-only (never admits extended kinds); the cap binds at TWO
   layers incl. the runtime `reach_capped` surface. Four new curated
   variants — `chorus_lift_E` / `density_C` / `density_D` / `vocal_C` — all
   `non_destructive_duplicate_track`, anti-mute by design; the loop and
   depth problems get NEITHER new family, by curation.
3. **`logic_mix_os/doctrine/producer_profile.py`** — load gates:
   extended-vocabulary membership for `reach_kinds`; reach∩suppress = ∅;
   over-cap reach "cannot be out-authored" → ValueError.
4. **`logic_mix_os/renderers/creative_renderer.py`** — the reach lines;
   evidence-key discipline (new keys only where the reach is live).
5. **The three producer JSONs** — `kind_scores` + `truth_alignment` rows
   for BOTH new kinds in ALL three profiles (no silent inheritance;
   timbaland's `ensemble_rebalance` honestly `medium` translation risk).
   **QUINCY ONLY authors reach:** his default `arrangement_lift` mode →
   [arrangement_lift]; `ensemble_balance` → [ensemble_rebalance];
   `experimental` → both — with the P-042 approximation favor consciously
   REPLACED. Halee/Timbaland author `reach_kinds []` everywhere. (Namespace
   care held: Quincy's MODE `arrangement_lift` vs the KIND
   `arrangement_lift` kept unambiguous.)
6. **Tests:** `tests/test_move_vocabulary_expansion.py` (NEW — 36 tests at
   HEAD) + conscious pin updates in `tests/test_mode_forking.py`,
   `tests/test_creative_profile_sourced.py`,
   `tests/test_governance_profile_sourced.py`.

**Explicitly out (the user's non-scope, verbatim where quoted):**

- **No negative-space dropout family** (the user's explicit exclusion — see
  authority above). No other new families beyond the two. No new analyzers.
  No doctrine/scoring changes (`doctrine_engine` untouched). No
  safety/governance/veto changes; the caps never weakened; **B's guarantees
  for the original seven kinds intact** (the requirement-8 test body is
  byte-identical; the attribution rule extends without loosening —
  reviewer-verified).
- No per-producer engine branches; no hardcoded producer behavior — held
  (AST guard 4/4; ZERO producer names added to engine code).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `ed94020` — "P-043 Commit-1: the widened move vocabulary —
    arrangement_lift + ensemble_rebalance, reach-gated, zero behavioral
    change" — 11 files, +911/−77 (the vocabulary + the reach seam + the
    load gates + the 4 curated variants + all three profiles' explicit
    rows + guards). **Commit-1 GREEN IN ISOLATION (944 passed); zero
    behavioral change verified: all 18 mode entries author reach_kinds [],
    zero extended emissions across 6 probe runs.**
  - `e382d86` — "P-043 Commit-2: Quincy's authored reach + the
    differential proof — the new families are quincy-reached,
    data-attributed" — 3 files, +277/−23.
  - Combined: **exactly 11 files, +1184/−96** (verified `git diff --stat
    3110126 e382d86` at close).
- **Parent:** `3110126` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `17cc270` (= the PR #21 merge —
  P-042 landed FIRST per the user's sequencing). Verified at close:
  `git merge-base HEAD 17cc270` = `17cc270`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the FINAL
  SHAs. **NOT merged** — the merge of P-043 is a user gate.

## QA proof (GREEN — the eleven items, exact counts)

- **Suite:** 907 → **950 passed, 0 failed**; regression **93/93**;
  **Commit-1 iso 944** — arithmetic verified: 907 + 29 new + 8 passive
  growth in the UNTOUCHED `tests/test_creative_nudges.py`; Commit-2 net
  +6 = +7 new-file / −1 mode_forking consolidation (**qa discrepancy #1**,
  count composition only — direction safe).
- **Sample trees:** the staleness pin 4/4 WITHOUT regeneration; both trees
  independently re-rendered via the verbatim README invocations →
  **30/30 + 30/30 byte-identical**; headlines 76.3/60.9 unchanged.
- **Default-flow byte-identity:** halee + timbaland identical over all 4
  fixtures pre/post (import-path-guarded worktree comparison). Quincy's
  CONSCIOUS delta exactly as enumerated (dense/splice chorus_lift +E,
  dense density +C, simple/intimate unchanged). **qa discrepancy #2:** the
  chop default flow ALSO gains chorus_lift_E — same authored mechanism,
  winner unchanged, doctrine unmoved, sample trees unaffected, but
  UNPINNED (the 4th fixture lives outside the FIXTURE_NAMES pin corpus) —
  accepted pin-coverage note.
- **ALL WINNERS UNCHANGED** on every fixture/branch; doctrine overalls
  unmoved (dense 70.7/52.6/62.1; chop 76.3/60.9/68.8).
- **The reach gate independently reproduced:** quincy experimental dense
  [E,A,B,C,D] / [C,D,A,B] / [C,A,B]; halee/timbaland ZERO extended ids
  over 48 runs; **attribution reconstruction over 234 cells (3 producers ×
  6 modes × 13 fixture-problems), 0 mismatches**; suppression beats reach;
  the fallback never admits extended kinds.
- **Cap + loader:** over-cap reach → ValueError (live proof = timbaland's
  medium row under a low posture); reach∩suppress → ValueError; reach
  naming a NEUTRAL kind → ValueError; loader-BYPASSING profiles →
  runtime fail-closed with `reach_capped` surfaced.
- **Sabotage 4/4 bites:** neutral-pool admission → **36 failed** (incl.
  the staleness pins — the gate IS what protects the trees); quincy reach
  deletion → 6 failed; fallback-admits-reach → 1 failed (the exact test);
  timbaland row deletion → 6 failed.
- **The real chain:** `vocal_C` WINS vocal_belief at exactly **83.1**
  through full `analyze()` incl. governance ("keep", zero violations) —
  the new families are LIVE, not inert.
- **Safety grep:** 0 across all categories on 1184 added lines; 0 producer
  names added to engine code; AST guard 4/4.
- **Requirement-10 surface (the UI smoke):** the quincy experimental
  artifact carries `search_mode_declarations.reach_kinds` + per-branch
  `mode_fork.reached` + the renderer lines; the halee DEFAULT render
  carries ZERO new-key bytes.

## ★ The user's acceptance bar — all nine clauses met (pinned evidence)

- **new move families exist ✓**
- **curated risk rows exist ✓** — all three profiles, both kinds,
  byte-pinned.
- **profiles author reach ✓** — loader-validated, explicit everywhere (no
  silent inheritance).
- **Quincy can reach them ✓** — three modes, live emissions, a governed
  WIN through full analyze().
- **Timbaland/Halee only if authored ✓** — zero reach → zero extended ids
  over 48 runs; the synthetic profile proves data-not-producer.
- **safety caps bind ✓** — two layers + the live medium-risk proof.
- **no producer-specific engine branches ✓** — AST guard + qa grep.
- **sample-tree drift is conscious ✓** — zero drift; quincy's default-flow
  delta enumerated.
- **differential proof attributes to vocabulary + reach ✓** — the 234-cell
  reconstruction from the JSONs on disk, 0 mismatches.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable;** independent worktree
  execution: **HEAD 950 + Commit-1 iso 944 REPRODUCED.**
- **Reach gate: NO LEAK** — extended pools built only inside
  declaring-mode branches; favor-of-extended silently order-only (no
  admission); the test helper does NOT share the engine's derivation
  (hand-pinned literals both sides — no shared-bug channel).
- **Cap authority:** correct data-authority semantics, not a hole —
  byte-identical to the P-042 favor precedent; the shipped rows
  byte-pinned.
- **Quincy's default-mode reach: JUSTIFIED, HONEST, COMPLETE** — all six
  authored overalls reconstructed from disk; the 85.6 vs 85.3 margin real
  (85.3 = second-highest in his table, and ensemble_rebalance outright
  WINS vocal_belief — not authored-to-be-inert); the pin delta
  append-only; the artifact-keys pin narrowing to (halee, timbaland)
  judged EXACTLY RIGHT (precisely the committed trees) with quincy's
  surface re-pinned STRONGER.
- **Content:** house style holds; density_D/vocal_C explicitly anti-mute;
  nothing smells like the excluded dropout family; the loop/depth
  exclusion defensible and pinned.
- **kind_scores/truth_alignment** read as each producer's lens; the
  truth_alignment extension = consistency not creep (prevents silent
  align_fallback inheritance).
- **Vocabulary discipline intact** (exact-tuple + length pins close the
  union-pin tolerance); AST clean; **P-042 guarantees intact** (the
  requirement-8 test body byte-identical; the attribution rule extends
  without loosening).
- **Non-blocking observations, accepted (no fix cycle → residue):**
  1. `fork["reached"]` on a loader-BYPASSING profile reaching a NEUTRAL
     kind would misreport it as reached (emission unaffected; the loader
     rejects the authoring) — future tightening: intersect with admitted
     kinds.
  2. The degenerate empty-neutral-pool + bypass edge — unreachable on all
     five shipped problem ids; pre-existing in shape.
- **Trajectory:** delivers "widen the vocabulary just enough to make
  Quincy's mode behavior genuinely musical"; dropout later = one tuple
  entry + authored reach, ZERO engine changes.

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, recorded not fixed:**
  1. qa discrepancy #1 — Commit-1 count composition (944 = 907 + 29 new +
     8 passive growth; C2 net +6 = +7/−1 consolidation) — direction safe.
  2. qa discrepancy #2 — quincy's chop-fixture default flow also gains
     chorus_lift_E, UNPINNED (pin-coverage note; candidate one-line pin
     extension in a future packet).
  3. Reviewer observation 1 — the `fork["reached"]` misreport on a
     loader-bypassing neutral reach (future tightening: intersect with
     admitted kinds).
  4. Reviewer observation 2 — the degenerate empty-neutral-pool + bypass
     edge (pre-existing in shape, unreachable shipped).
- **★ The P-042 residue note 3 (quincy-experimental as in-vocabulary
  approximation) is ✓ RESOLVED by this packet** — the approximation favor
  consciously replaced by real authored reach over the true families.
- The residue list otherwise stays **ZERO** — all prior standing notes and
  the three named lessons retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-043** — `3110126` + `ed94020` +
  `e382d86` (+ this close commit) atop `17cc270` (= PR #21) — awaits the
  user's explicit word. The commits are pushed to the dev branch (standing
  go, pre-gates); NOT merged; no deploy/publish/secrets touched.
- **NEXT — ★ USER-GATED: negative-space dropout as a move family (STAGED,
  not active):** the user's own sequencing — "after C proves the widened
  vocabulary can stay governed" — and C has now proven exactly that.
  Adding it = one `CREATIVE_EXTENDED_KINDS` entry + curated variants +
  authored reach, ZERO engine changes. The decision of whether/when is the
  USER'S — the orchestrator presents scope first; it does not open blind.

---
_Closed by the archivist (2026-07-03). qa GREEN (950 / 93/93 / Commit-1 iso
944 / 234-cell reach reconstruction 0 mismatches / all winners unchanged /
sabotage 4/4 / a governed 83.1 win through full analyze() / safety grep 0)
+ reviewer PASS (no must-fix; all adapted attacks defeated; single-model —
Codex unavailable; HEAD 950 + C1 944 independently reproduced)._
