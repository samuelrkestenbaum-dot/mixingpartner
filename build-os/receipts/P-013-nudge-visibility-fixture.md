# Receipt — P-013: Nudge-visibility fixture — P-012 nudge fires through `analyze()` (option a)

- **Date:** 2026-06-30
- **Authority:** build (router row 1: `builder → qa → reviewer → archivist`).
  Tests-only; no design-UI / marketing / swarm / infra gate tripped.
- **Branch base (merge-base):** dev branch `claude/logic-mix-os-hardening-12-7hbeh1`;
  default `claude/dreamy-turing-z0oxll` (`git merge-base` = `694d19d`). **PR #13
  (P-001…P-012 + the canonical-alignment audit) is now MERGED to default** — merge
  commit `0f4e7e9` is verified in P-013's ancestry, so P-013 is the **first
  post-merge packet** on the freshly-restarted dev branch.

## What it does

Lifts the already-shipped **P-012 creative evidence-nudge** claim from the
**unit level** (hand-built `SimpleNamespace` in `tests/test_creative_nudges.py`)
to **REAL DATA through the live `pipeline.analyze()` production path** — closing
the gap left by the golden-unguarded variant-scoring path (the 68/68 golden reads
`doctrine_score`, never `score_variant`, so only tests can guard this behavior).

On the `dense_chorus_with_loops` fixture, the live masking analyzer emits a real
`width_crowding` event, so the **row-2 nudge** (`vocal_belief −6`: stereo image
already width-crowded) fires on the `chorus_lift` `width_bloom` variant **with no
contrivance**. The nudge lowers that variant's `overall_score` (the value
governance ranks on) from the curated base **75.7 → 74.9** — a real,
evidence-backed movement of **−0.857**, well inside the `±2.0` cap — yet the
governed/creative winner stays `chorus_lift_B` (`subtractive_drop`, 85.3) because
the base gap (~9.6) exceeds **2× the cap**.

This is the builder's chosen **option (a): the cap binds and the winner does NOT
flip** — the documented latent-but-armed posture, now proven end-to-end on
realistic data rather than only at the unit level.

## Scope

- **In:**
  - `logic-mix-os/tests/test_creative_nudge_visibility.py` — **new, tests-only**
    (+154 lines, **5 tests**). Fake adapters only (seeded synthetic stems +
    manifest; local I/O).
- **Out (explicit):**
  - **All product / runtime code** — `creative.py`, `governance.py`, `pipeline.py`,
    `memory.py`, `album.py`, `next_pass_planner.py`, `cli.py` — **untouched**. This
    is a pure tests-only proof of already-shipped P-012 behavior.
  - **Fixture #2 (taste-driven governed-winner flip through `analyze()`) — NOT
    BUILT.** Re-scoped at builder handback; structurally unreachable test-only on
    curated data. Recorded below as an **alignment finding** (a positive
    confirmation), not a TODO. Making a flip reachable would require a product-code
    aesthetic change → **user-gated, a separate packet.**

## Commits

- `172cfd0` P-013: nudge-visibility fixture — P-012 nudge fires through `analyze()`
  (option a) — **single tests-only commit** (new
  `tests/test_creative_nudge_visibility.py`, +154 lines, 5 tests; no product tree
  change).
- `3874175` Confirm P-013 (option-B-visibility fixtures, tests-only) as active
  packet — **non-product** (memory-only: `build-os/packets/active_packet.md`).

The 5 tests:
- `test_width_crowding_nudge_fires_through_analyze`
- `test_nudge_movement_on_governed_axis_within_bound` (overall_score 75.7 base →
  74.9 nudged, movement −0.857 within ±2.0 cap)
- `test_armed_nudge_does_not_flip_creative_winner` (winner stays `chorus_lift_B`)
- `test_armed_nudge_does_not_flip_governed_winner` (governed_winner stays
  `chorus_lift_B`)
- `test_base_gap_exceeds_twice_the_cap_so_no_flip_is_possible`
  (`subtractive_drop` 85.3 − `width_bloom` 75.7 = 9.6 > 2×2.0)

## QA proof (exact)

- **Suite:** `python -m pytest` → **202 → 207 passed** (0 failed / 0 skipped /
  0 warnings; +5 new).
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68**, 0 critical,
  0 warnings (held). Standing fact: the variant-scoring path is **golden-unguarded**
  — these fixtures are the binding visibility guard, not the golden.
- **Commit-1 green in isolation:** verified. The single commit is the tip
  (`172cfd0`); the new test file alone = **5 passed**; the product tree at that
  commit is unmodified (the `0f4e7e9` merge is in ancestry, no product diff).
- **Safety grep:** clean — the only hit is a docstring asserting the **no-DAW**
  posture. No real DAW / Logic / AppleScript / subprocess / `.logicx` write /
  network.
- **UI smoke:** N/A (tests-only; no surface touched).

## Review

- **Verdict: pass.** The reviewer ran an **independent negative control** —
  disarmed `_apply_nudges` and observed **3 of 5 tests fail**, proving the
  assertions are load-bearing (not tautological). The reviewer **independently
  recomputed the option-(a) numbers** (75.7 base → 74.9 nudged; −0.857 movement;
  9.6 base gap > 4.0) and confirmed the **Fixture #2 re-scope is sound** by
  reading the source.
- **Codex second-eyes: NOT available** — **single-reviewer verdict** (recorded
  caveat).
- **Product Trajectory Check:** converts P-012's unit-level nudge proof into a
  real-data `analyze()` proof, hardening the golden-unguarded variant-scoring path
  with the binding guard. No product behavior changed.

## Residue

- **Fixture #2 alignment finding (POSITIVE — taste structurally cannot flip a
  governed winner on curated data):** the builder brute-forced **all 3 fixtures ×
  4 intents** with a narrower-taste `ProjectMemory` and found **no governed-winner
  flip anywhere**. Reviewer-verified in source: `_apply_taste` (governance.py)
  moves **only** the `taste_triangle` **identity** axis, clamped to
  `±TASTE_MAX_DELTA (15)`, and maps **only** to `width_bloom` / `drum_room_bloom`
  (`_TASTE_KIND_BIAS`); the governed winner is ranked on `overall_score` behind an
  **align-veto** — so **taste structurally cannot reorder a truth-ranked winner.**
  This is the doctrine **"taste can never outrank a truth move," working as
  intended** — a positive alignment confirmation, not a defect. The unit "flip"
  in `test_governance_taste.py` only works because it hand-injects branch values
  curated scoring never produces. The reachable end-to-end taste claim (taste
  reaches governance + down-weights identity with bounded evidence) is **ALREADY
  proven on real data** by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`.
- **Deferred / follow-up:**
  - **"Near-tie-creative-flip" fixture (NEW, reachable, deferred):** a fixture
    where the creative nudge actually FLIPS the winner through `analyze()` (a true
    near-tie, distinct from P-013's no-flip option-(a) case). Reachable test-only,
    the natural future increment. Small additive test.
  - **Taste-flip-via-product-change (user-gated):** making a taste-driven
    governed-winner flip reachable through `analyze()` requires a product-code
    aesthetic change — a separate, user-gated packet. Distinct from the reachable
    near-tie-creative fixture above.
  - (carried) **Reward nudges (orchestrator rows 3+4)** — user-gated; P-012 is
    penalty-only by design. **Wider `--memory-dir` CLI surface** — partly a product
    question. **Net-new event-logging producers** — behind a product decision.
- **Known risks:** the variant-scoring path remains golden-unguarded by design —
  unit/visibility tests are the binding guard. Commits on this branch are unsigned
  (environment limitation; correct author/committer, GitHub shows "Unverified").

## Open boundaries (awaiting explicit go)

- **The product commit `172cfd0` is local-only as of this close** (this archivist
  close did not push). It lands on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` **after** the PR #13 merge to default.
  Any push of it (and a subsequent PR / merge into the protected default) needs the
  user's explicit go. No merge / deploy / push / secret action taken in this close.
