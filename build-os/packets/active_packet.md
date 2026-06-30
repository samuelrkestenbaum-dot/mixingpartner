# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —
- **Authority:** —

## Last closed

- **P-008 — History-aware next pass (the OUTCOME side of the learning loop)** —
  closed 2026-06-29. Receipt:
  `build-os/receipts/P-008-history-aware-next-pass.md`. `plan_next_pass` now
  consumes recorded mix-pass history (opt-in, bounded, evidence-tagged); default
  path byte-identical. Commits `d98a194` (planner + tests) and `dbf94c3`
  (drum_room_bloom test). Suite 138 passed; regression 68/68.
  **MILESTONE — the learning loop is now FULLY CLOSED** (P-007 consumer side +
  P-008 outcome side).

## Staged next (candidates — user's call)

- **P-008b — Live history wire:** thread `memory.history()` into
  `pipeline.analyze()` / the planner call so a real recorded history reaches
  `plan_next_pass` in production — kept opt-in / explicit so byte-identical-by-
  default survives (symmetric to P-007b). The natural next trajectory packet.
- **P-007b — Live taste surface:** wire a real per-operator `taste_profile` from
  `memory_dir` into a pipeline/cowork run (explicit per-operator).

Both make the now-closed learning loop **real in production**. No packet is
active until the orchestrator confirms the next one.

---
_Cleared by the archivist on P-008 close (2026-06-29)._
