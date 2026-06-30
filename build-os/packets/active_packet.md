# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —
- **Authority:** —

## Last closed

- **P-007 — Taste profile feeds governance (first closure of the learning loop)**
  — closed 2026-06-29. Recorded operator taste now biases variant governance
  (opt-in, bounded `±15`, evidence-tagged, doctrine-inviolable). Single product
  commit `bd08f28`; suite 112→125; regression 68/68 held; default path
  byte-identical. **MILESTONE: first closure of the learning loop** — memory is no
  longer purely write-only on the governance axis. Receipt:
  `build-os/receipts/P-007-taste-feeds-governance.md`.

## Staged next (user's call — not yet active)

- **P-008 — History-aware next pass** (the OUTCOME side of the loop):
  `plan_next_pass` consumes `mix_pass_history` (improved / got_worse /
  revert_candidates) so a regressed move is not re-recommended. The next
  high-leverage trajectory packet; fold in the `drum_room_bloom` taste test gap.
- **P-007b — Live opt-in surface:** wire a real per-operator `taste_profile` from
  `memory_dir` into a pipeline/cowork run, kept explicit per-operator so the
  byte-identical-by-default guarantee survives into the pipeline.
- **Event-logging producers** (`taste_feedback` / `validation_check`) — more
  justified now a consumer exists, still net-new feature work behind the same
  product decision.

See `build-os/memory/current_state.md` and `build-os/memory/residue.md` for full
context.

---
_Cleared by the archivist on P-007 close (2026-06-29). One packet at a time._
