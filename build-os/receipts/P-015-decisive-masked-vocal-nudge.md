# Receipt — P-015: Make the masked-vocal nudge DECISIVE (user-signed-off aesthetic change)

- **Date:** 2026-06-30
- **Authority:** build (router row 1: `builder → qa → reviewer → archivist`).
  **PRODUCT-CODE aesthetic change to default recommendations — explicitly
  user-gated, and the user gave explicit go** ("Option 1 — Proceed, corrected",
  2026-06-30). The deliberate, signed-off successor to P-012. No design-UI /
  marketing / swarm / infra gate tripped.
- **Branch base (merge-base):** dev branch `claude/logic-mix-os-hardening-12-7hbeh1`;
  default `claude/dreamy-turing-z0oxll` (`git merge-base` = `694d19d`). PR #13
  (P-001…P-012 + the canonical-alignment audit) is MERGED to default (merge commit
  `0f4e7e9`, in ancestry). The single product commit `1756f61` sits on the dev
  branch on top of that merge and is **local-only** at close.

## The story (P-014 finding → user decision → corrected preview → Option 1 → this change)

P-014 closed as a **verified negative finding**: under the then-current curation
the P-012 nudge was structurally **transparency-only** — it moved the displayed
`overall_score` and emitted `score_nudges` but could **never reorder any
branch**. Two structural reasons: the universal branch leader `subtractive_drop`
(85.29) is in NO nudge row (penalty-immune), and the one sub-cap near-tie branch
`vocal_belief` (`vocal_ride` 82.86 vs `intimacy_pass` 81.14, gap 1.71) had BOTH
its leader and runner-up hit by the **identical** row-0 `lead_masked −8`,
preserving the gap. P-014 surfaced — as a user-gated DECISION, not a TODO — the
"make-the-nudge-decisive (curation change)" packet, with two concrete routes
(split row-0's `kinds`, or re-curate `_KIND_SCORES`).

The user asked to make the nudge decisive. The orchestrator's **original
preview contained an arithmetic error**: it implied the existing `−8` penalty
could flip the near-tie, but `−8/7 = −1.14` overall moves vocal_ride only to
~81.7 — **insufficient** to cross `intimacy_pass` at 81.14 (it would still lead
by ~0.6). The orchestrator **transparently corrected the arithmetic** and
re-presented the mechanism: to flip within the cap you must BOTH (1) exempt
`intimacy_pass` so the runner-up no longer drops in lock-step, AND (2) strengthen
the penalty to `−14` (= `−14/7 = −2.0` overall = exactly the existing
`CREATIVE_NUDGE_CAP = 2.0`, unchanged) so vocal_ride lands at the cap. The user
chose **"Option 1 — Proceed, corrected"** on 2026-06-30. P-015 implements
exactly that corrected mechanism.

## Scope

- **In (the exact edits — `_NUDGE_TABLE` row-0 only, the `lead_masked` row):**
  1. **Exempt `intimacy_pass`:** `kinds` `{width_bloom, vocal_ride,
     intimacy_pass}` → `{width_bloom, vocal_ride}`. Doctrine: an intimacy pass is
     the CORRECT response to a masked lead vocal — it brings the vocal into
     focused proximity rather than shoving it forward by brute level/width — so it
     must NOT be penalized as a risky vocal-forward move. (Captured in a code
     comment.)
  2. **Strengthen the penalty:** `delta` `−8` → `−14` (= `−14/7 = −2.0` overall =
     EXACTLY `CREATIVE_NUDGE_CAP = 2.0`, which is UNCHANGED and now binds for
     vocal_ride too).
  3. **Honest `−14` reason string** + a doctrine comment.
  4. **Corrected the now-stale clamp comment** to the new numbers (width_bloom
     under both rows is `−20` raw, still clamped to `−2.0` overall; vocal_ride
     under row-0 alone is now `−14` raw `= −2.0` overall).
- **Out (explicit) — verified UNTOUCHED by diff:** `_KIND_SCORES` (values
  unchanged), `CREATIVE_NUDGE_CAP` (still 2.0), row-1 (`width_crowding` /
  `vocal_belief −6`), the clamp logic, both predicates, every other kind. No
  `governance.py` / `pipeline.py` change. The P-013 visibility tests
  (`tests/test_creative_nudge_visibility.py`) were verified-not-edited.
- **Out (explicit):** no push / merge into the protected default / deploy /
  secret — out of authority for this close.

## Behavior (verified by qa independently)

In the `vocal_belief` branch under a masked lead vocal:

- `vocal_ride` (vocal_A): 82.9 → **80.9** — the cap binds, `overall_delta` is
  EXACTLY `−2.0`, and the variant carries the `−14` `score_nudges` evidence line.
- `intimacy_pass` (vocal_B): 81.1 → **81.1 unchanged** (now exempt).
- **Winner FLIPS from `vocal_ride` (vocal_A) to `intimacy_pass` (vocal_B)** by 0.2.

**Negative control (load-bearing):** WITHOUT `lead_masked`, `vocal_ride`
(vocal_A) wins — proving the flip is caused by the masking EVIDENCE, not a base
re-rank.

**Bounded — no clear-ranking overturn (P-012's bound preserved):**
`subtractive_drop` (85.3, penalty-immune) still wins `chorus_lift` / `density` /
`loop` under `lead_masked` (gaps 3.4–4.2 ≫ 2×cap); ONLY the `vocal_belief`
branch flips. This is the doctrine "breaks a genuine near-tie, never overturns a
clear ranking."

## Tests (the BINDING guard — variant-scoring path is golden-unguarded)

- **Updated** `tests/test_creative_nudges.py` — the ~existing P-012 cases moved to
  the new behavior (delta `−8`→`−14`; `intimacy_pass` now asserted EXEMPT under
  `lead_masked`; new reason string; width_bloom worst case now `−20` raw clamped
  to `−2.0`), and ADDED `test_intimacy_pass_exempt_from_lead_masked_nudge` +
  `test_vocal_ride_clamps_to_cap_under_lead_masked`. **No coverage deleted to turn
  red green.**
- **Added** `tests/test_decisive_nudge.py` (NEW, 8 tests) — the decisive-flip
  proof through the real `run_creative_engine`/`score_variant` path: the flip
  (layer ON → `intimacy_pass` wins), the load-bearing negative control (no
  `lead_masked` → `vocal_ride` wins), the cap binding exactly, a clear-ranking
  branch that does NOT flip (`test_subtractive_drop_branch_does_not_flip_under_lead_masked`),
  and a collateral-safety check that ONLY the `vocal_belief` branch flips
  (`test_only_vocal_belief_branch_flips_under_lead_masked`).

## Commits

- `1756f61` **P-015: make the masked-vocal nudge DECISIVE — exempt intimacy_pass,
  strengthen to the cap.** The single product commit (product change + updated/new
  tests TOGETHER so Commit-1 is green in isolation, as required because the change
  intentionally breaks old-behavior tests). `creative.py` +22, `test_creative_nudges.py`
  +59, `test_decisive_nudge.py` +195 (3 files, 260 insertions / 16 deletions).
  Author/committer `Claude <noreply@anthropic.com>`.
- `09dec28` Confirm P-015 as active packet — **non-product** (memory-only:
  `build-os/packets/active_packet.md`).
- This archivist close adds **one build-os-only commit** (receipt + memory
  advance), following the prior-close pattern (`678b9bf`, `0573e9c`, `f591f89`, …).

## QA proof (exact)

- **Suite:** `python -m pytest` → **207 → 217 passed** (0 failed / 0 skipped / 0
  warnings). The two changed test files alone = **53 passed**
  (`test_creative_nudges.py` 45, `test_decisive_nudge.py` 8).
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68, 0 critical, 0
  warnings** (doctrine golden HELD — the aesthetic change did NOT break any
  doctrine invariant). Standing fact: the variant-scoring path is
  golden-unguarded (`regression.py` reads `doctrine_score`, never
  `score_variant`); the **unit tests are the binding guard** for this change.
- **Commit-1 in isolation:** **GREEN** — the single product commit `1756f61` is
  the tip and includes the product change + updated/new tests together; tree
  clean.
- **Safety grep:** **clean** — only hit a no-DAW docstring line (no real DAW /
  Logic / AppleScript / subprocess / `.logicx` write / network introduced; fake
  adapters only).
- **UI smoke:** **N/A** — no surface touched.
- **qa verdict: GREEN.**

## Review

- **Verdict: pass.** The reviewer independently REPRODUCED the arithmetic
  (vocal_ride `−14/7 = −2.0` to the cap → 80.9; `intimacy_pass` exempt → 81.1; flip
  margin 0.2) and ran a **mutation test confirming non-vacuity**: reverting BOTH
  product edits turned **5 binding tests RED**, while the negative control
  correctly stayed GREEN → the tests are **load-bearing, not always-green**. The
  reviewer confirmed scope discipline (row-0 only; `_KIND_SCORES` / cap / row-1 /
  clamp / predicates untouched), the no-overturn bound (clear-ranking branches do
  not flip), evidence-line honesty (the `−14` reason matches the mechanism), and
  that coverage was not weakened to pass.
- **Codex second-eyes: NOT available** — **single-reviewer verdict** (recorded
  caveat), consistent with P-012 / P-013 / P-014.
- **Non-blocking standing config tension (flagged, not a P-015 regression):** the
  mandated `Co-Authored-By: Claude Opus 4.8` commit trailer is technically a model
  identifier, but it is required by the harness commit instructions and is
  consistent across all packets — a standing environment constraint, not
  introduced by P-015.

## Residue

- **"Make-the-nudge-decisive (curation change)" → RESOLVED by P-015.** The
  user-gated P-014 decision is actioned: the nudge is now decisive on the
  masked-vocal near-tie (`vocal_belief`: `vocal_ride` → `intimacy_pass`), bounded
  so it still cannot overturn a clear ranking.
- **Reviewer trajectory flag (non-blocking):** the **0.2 flip margin is thin** but
  is **fully pinned by binding tests** — a future re-curation would surface as a
  RED test, not a silent re-rank. The variant-scoring path stays golden-unguarded
  by design; the unit/flip tests are the guard.
- **(carried) Deferred candidates, unchanged:**
  - **Reward nudges (orchestrator rows 3+4)** — user-gated; P-012 is penalty-only
    by design.
  - **Wider `--memory-dir` CLI surface** — partly a product question.
  - **Net-new event-logging producers** — behind a product decision.
  - **Taste-flip-via-product-change** — user-gated, separate packet (the reachable
    taste claim is already covered by
    `test_live_wire.py::test_taste_axis_changes_governance`).
- **Known risks:** Commits on this branch are unsigned (environment limitation;
  correct author/committer `noreply@anthropic.com`, GitHub shows "Unverified").

## Open boundaries (awaiting explicit go)

- **P-015's product commit `1756f61` is local-only as of this close.** It sits on
  the dev branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9`
  merge. The orchestrator pushes the dev branch separately. Any push — and any
  subsequent PR / merge into the protected default — needs the user's explicit go.
  **No push / merge / deploy / secret action taken in this close.**
</content>
</invoke>
