# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — P-039 CLOSED by the archivist (2026-07-02).
- **Last closed:** P-039 — Producer Selection CLI Exposure + Demo-Safe
  Invocation (the FIRST post-substrate PRODUCT packet). qa GREEN + reviewer
  fix-then-pass → PASS (one fix round, fully resolved). Commits `b111a18`
  (the feature) + review-fix `a56cb96` (TEST-ONLY) on parent `73a134e`, atop
  merge base `2c09428` (the post-backlog batch merge); pushed AFTER close
  (orchestrator standing go), NOT merged. Suite **801** / regression
  **93/93**. Receipt: `build-os/receipts/P-039-producer-cli-exposure.md`.

## Staged next (NOT active until the orchestrator confirms with the user)

- **THE SAMPLE REFRESH — next per the USER'S SEQUENCE** (P-039 ✓ → sample
  refresh → third producer → deeper mode-forking):
  - **Shape:** regenerate `examples/sample_output/` from a chosen fixture
    under BOTH producers — two trees, or one tree + a differential README
    section (**the orchestrator scopes the shape with the user**).
  - **Why now:** this CLEARS the accepted P-038 standing note (the samples
    ship stale pre-P-036/P-038 prose — producer-named action strings, stale
    verdict text), and the P-039 identity surface gives the samples
    SELF-DESCRIBING trees (each artifact names its producer).
  - **Conscious interaction check:** test-9 (OLD_KEYS) — verify the
    regenerated samples' interaction with the old-keys guard; any pin touch
    is a conscious, enumerated flip, never a weakening.
  - **After:** the THIRD producer, then deeper mode-forking.

---
_Cleared by the archivist at P-039 close (2026-07-02). One packet at a time.
The staged packet activates only on the orchestrator's confirmation with the
user._
