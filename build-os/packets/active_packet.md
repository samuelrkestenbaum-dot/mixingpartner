# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — P-040 (the SAMPLE REFRESH — the two-producer
  demo output) CLOSED 2026-07-02: qa GREEN + reviewer PASS (no must-fix).
  Receipt: `build-os/receipts/P-040-sample-refresh.md`.
- **Last-closed:** P-040 — commits `33cf10d` (the two 30-artifact trees
  from `vocal_chop_groove` + test-9 over both + the FULL-strength
  staleness pin) + `9e58e9b` (README only) on parent `1783683`, atop
  merge base `2c09428`; PUSHED after close (orchestrator standing go),
  NOT merged. Suite **806** / regression **93/93**. The P-038
  stale-samples standing note ✓ CLEARED.

## STAGED (next per the USER'S SEQUENCE — NOT active until confirmed)

**THE THIRD PRODUCER — ★ USER-GATED: the orchestrator PRESENTS the
decision; do NOT open blind.**

Two decisions belong to the user before this packet opens:

1. **WHICH producer.**
2. **The grounding**, per the standing honesty policy:
   hand-curated-documented → `high`; derived → `low`, labeled;
   LLM-synthesized → draft-only, NEVER `high`.

**What the third producer costs now (the P-025 → P-039 substrate makes
this authoring, not engineering):** a JSON file
(`doctrine/producers/<name>.json`) + the three REQUIRED declarations
(`protect_iconic_loops`, `vocal_blend_policy`, `confidence_map`) + its
own verbatim map pin + a differential test + a sample tree/README column
if desired — **ZERO code changes** (the P-039 surfaces scan the
producers dir).

## The arc after (user-sequenced)

**P-040 ✓ (sample refresh) → the third producer (staged, user-gated) →
deeper mode-forking.**

---
_Cleared by the archivist at P-040 close (2026-07-02). One packet at a
time. The orchestrator confirms the next packet with the user before it
goes active._
