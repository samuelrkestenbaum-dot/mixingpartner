# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

## Last closed

- **P-012 — Creative-scoring evidence-nudge layer (option B, penalty-only)** —
  CLOSED 2026-06-29. Receipt:
  `build-os/receipts/P-012-creative-scoring-nudge-layer.md`. Single product
  commit `0df436c` (local-only). A bounded, transparent, capped, penalty-only
  evidence-nudge layer ON TOP of the curated `_KIND_SCORES` (values unchanged):
  `vocal_belief −8` on masked vocal / `vocal_belief −6` on `width_crowding`,
  summed overall delta clamped to `±2.0`, `score_nudges` emitted only on fire.
  Suite 159→**202**; regression **68/68** held; reviewer **pass** (adversarially
  proven). **Deliberately NOT byte-identical when a nudge fires — awaiting the
  user's sign-off at the PR #13 merge.**

## Next (staged — not yet active)

- No product packet in flight. The creative-scoring aesthetic decision is
  resolved (option B shipped). Candidate next moves (see `residue.md`):
  - **Reward nudges (orchestrator rows 3+4)** — additive promotion nudges on
    `crowded_sections`; **user-gated** (P-012 is penalty-only by choice).
  - **Option-B-visibility fixtures** — a near-tie creative fixture (P-012) and the
    borderline taste fixture (P-009) through `analyze()`; small in-authority tests.
  - **Wider `--memory-dir` CLI surface** (partly product); net-new
    **event-logging** producers (behind a product decision) — both deferred.
- Route any next packet via the build-orchestrator before starting.

---
_Cleared by the archivist on P-012 close (2026-06-29). One packet at a time._
