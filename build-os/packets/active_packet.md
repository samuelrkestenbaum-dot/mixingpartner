# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — routed to builder
- **Packet id:** P-013
- **Title:** Option-B-visibility fixtures — near-tie creative + borderline taste,
  driven through `analyze()`

## Scope (the builder implements EXACTLY this)

**Test-only.** Add fixtures that exercise the already-shipped P-012 nudge layer
and the P-007/P-009 taste axis through the live `analyze()` production path,
making the bounded-but-armed behavior visible on realistic data. **No product /
runtime code touched — `tests/` only.** This converts two claims that are today
proven only at the unit level into claims proven on real data through
`analyze()`:

1. **Near-tie creative fixture (P-012):** an `analyze()`-driven case where the
   creative nudge **fires through the production path** and the outcome is
   asserted explicitly — either (a) the cap binds and the winner does **not**
   flip, or (b) a constructed near-tie where it flips **within the ±2.0 bound**.
   The builder must state which, and the assertion must be on the value the
   governance ranks on (not just the raw nudge).
2. **Borderline-taste fixture (P-007/P-009):** an `analyze()`-driven case where a
   bounded taste profile **flips the governed winner end-to-end** through the
   live memory wire (today proven only at the P-007 unit level in
   `test_governance_taste.py`).

Fixtures must use **fake adapters only** — no real DAW / Logic / AppleScript /
subprocess / `.logicx` write / network.

## Authority + budget

- **Authority:** build (router row 1: `builder → qa → reviewer → archivist`).
  No design-UI, marketing, swarm, or infra authority touched. No gate tripped.
- **Tool Budget:** `[Read, Grep, Glob, Edit, Write, Bash] + builder → qa →
  reviewer → archivist` — add `analyze()`-driven visibility fixtures for the
  P-012 nudge layer and the taste axis; tests-only, prove on real data.
- **Commits:** ≤2 (likely 1 tests-only commit; Commit-2 reserved only if the two
  fixtures split cleanly). **Commit-1 green in isolation.**
- **Hard stop:** no push/merge/deploy in scope. Standing push-go covers commits
  to this dev branch; a merge into the protected default still needs explicit go.

## Expected proof (qa reports exact counts at close)

- Suite **202 → ~206–210 passed** (0 failed / skipped / warnings).
- Regression **68/68 held** (0 critical / 0 warnings). Standing fact: the
  variant-scoring path is **golden-unguarded**, so these fixtures are the binding
  visibility guard, not the golden.
- **Commit-1 green in isolation.**
- **Safety grep clean** (fake adapters only; no DAW/Logic/AppleScript/subprocess/
  `.logicx`/network).

## Last closed

- **P-012 — Creative-scoring evidence-nudge layer (option B, penalty-only)** —
  CLOSED 2026-06-29; **MERGED to default via PR #13 (merge commit `0f4e7e9`)**.
  Receipt: `build-os/receipts/P-012-creative-scoring-nudge-layer.md`. A bounded,
  transparent, capped, penalty-only evidence-nudge layer ON TOP of the curated
  `_KIND_SCORES` (values unchanged): `vocal_belief −8` on masked vocal /
  `vocal_belief −6` on `width_crowding`, summed overall delta clamped to `±2.0`,
  `score_nudges` emitted only on fire. Suite 159→202; regression 68/68 held;
  reviewer pass (adversarially proven). The whole P-001…P-012 line plus the
  canonical-alignment audit (verdict ALIGNED) is now on the default branch.

---
_Confirmed active on P-013 open (2026-06-30) by the orchestrator-in-chief.
One packet at a time._
