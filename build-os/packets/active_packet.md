# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — no product packet in flight.
- **Packet id:** —
- **Title:** —

## Next candidates (orchestrator to route — none committed)

- **Near-tie-creative-FLIP fixture (NEW from P-013, reachable, in authority)** — a
  fixture where the creative nudge actually FLIPS the winner through `analyze()` (a
  true near-tie, distinct from P-013's option-(a) no-flip case). Small additive
  tests-only test. The natural next increment.
- **Reward nudges (orchestrator rows 3+4) — user-gated.** `depth_cleanup +6 halee` /
  `subtractive_drop +4 taste` on non-empty `crowded_sections`. A later ADDITIVE
  packet only IF the user asks for reward (promotion) nudges; P-012 is penalty-only
  by design.
- **Taste-flip-via-product-change — user-gated.** Making a taste-driven
  governed-winner flip reachable through `analyze()` needs a product-code aesthetic
  change (P-013 proved it is structurally unreachable test-only). Separate packet.
  The reachable taste claim is already covered by
  `test_live_wire.py::test_taste_axis_changes_governance`.
- **Wider `--memory-dir` CLI surface** (from P-009 — partly a product question);
  net-new **event-logging** producers (behind a product decision). Deferred.

## Last closed

- **P-013 — Nudge-visibility fixture — P-012 nudge fires through `analyze()`
  (option a)** — CLOSED 2026-06-30. Receipt:
  `build-os/receipts/P-013-nudge-visibility-fixture.md`. **Tests-only** — one new
  file `tests/test_creative_nudge_visibility.py` (+154 lines, 5 tests); NO product
  code touched. Drives the P-012 creative nudge through the live `analyze()` path on
  `dense_chorus_with_loops` (real `width_crowding` event → row-2 nudge fires);
  builder chose **option (a)** — the cap binds, the winner does NOT flip
  (overall_score 75.7→74.9, movement −0.857 within ±2.0; winner stays
  `chorus_lift_B`; base gap 9.6 > 2×2.0). Single tests-only commit `172cfd0`. Suite
  202→**207**; regression **68/68** held; Commit-1 green in isolation; safety grep
  clean (only hit a no-DAW docstring); UI N/A. Reviewer **pass** — independent
  negative control (disarmed `_apply_nudges` → 3 of 5 fail), recomputed the numbers,
  confirmed the Fixture #2 re-scope; **Codex not available — single-reviewer
  verdict.** Fixture #2 (taste-flip) re-scoped to a positive alignment finding
  (structurally unreachable test-only — user-gated to a product change). **P-013 is
  the first post-merge packet** — PR #13 (P-001…P-012 + canonical-alignment audit)
  is MERGED to default (merge commit `0f4e7e9`).

---
_Cleared by the archivist on P-013 close (2026-06-30). None active — one packet at
a time._
