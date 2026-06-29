# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** none active

## Last closed

- **P-001** — Resolve variant `tracks_affected` against real records.
  Closed 2026-06-29, reviewer verdict pass. Receipt:
  `build-os/receipts/P-001-resolve-variant-track-attribution.md`.

## Next (staged, awaiting user's call)

- **Candidate P-002:** net-new `EVENT_TYPES` decision-ledger vocabulary.
- **Candidate P-003:** readiness-vs-refusal ledger-status UI clarity.

Pick one via the build-orchestrator before the builder touches product code.

---
_Cleared by the archivist on P-001 close. No packet is in flight until the
orchestrator confirms the next one on the user's go._
