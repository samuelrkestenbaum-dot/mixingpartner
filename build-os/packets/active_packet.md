# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active
- **Packet id:** —
- **Title:** —

## Last closed

- **P-010 — Album context into per-song planning** (opt-in, bounded,
  evidence-tagged). Closed 2026-06-29. Receipt:
  `build-os/receipts/P-010-album-context-into-planning.md`. Product commits
  `dc61f20` + `9ebd4ee` (local-only). Suite **155 passed**; regression **68/68**.
  **MILESTONE:** the cross-song coherence axis is now OPEN — a song's plan (via the
  `album` command) reflects its album siblings.

## Next (staged — awaiting orchestrator re-survey)

User is driving via "skate to where the puck." Re-ranked strategic candidates
(see `build-os/memory/residue.md` for detail):

1. **Deeper creative scoring (LEADING)** — `creative.py::_KIND_SCORES` is hardcoded
   (verified NOT golden-blocked); richer evidence-driven kind-scoring.
2. **`album.py` delta consolidation (P-011 candidate)** — retire the duplicate mean
   computation between `album.py:55-58` and `cli.py:367-370` by having `album.py`
   emit per-song deltas.
3. **Loop polish** — borderline taste fixture (flip the governed winner through
   `analyze()`), wider `--memory-dir` CLI surface, CLI advisory float rounding
   (cosmetic, from P-010 reviewer).

Net-new event-logging producers remain behind the product decision.

---
_Cleared by the archivist on P-010 close. The orchestrator stages the next packet
on its re-survey._
