# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — awaiting orchestrator confirmation of the next packet.
- **Packet id:** —
- **Title:** —

## Last-closed

- **P-032a — `negative_space` (the SECOND new producer-agnostic doctrine axis;
  absolute arrangement room/sparsity). ✓ CLOSED** — qa GREEN, reviewer PASS.
  Byte-identical for halee_ramone (0 mismatches / 27 comparisons; overalls
  73.8 / 70.7 / 74.3 unchanged; regression 68/68). Distinct from `dynamic_mix`
  (dense-but-moving: dynamic_mix=100.0 vs negative_space=15.0 — 85-pt gap).
  Liveness load-bearing; sample-level inter-onset silence gaps honestly deferred
  to P-032b. Single commit `3edcd9c` (base `6d34c30`, atop set-active `836bd22`);
  suite 396 → 413; `test_negative_space.py` = 17 tests. **Single-reviewer — Codex
  NOT available.** **Local-only on dev branch, NOT merged** (merge base still
  `e79426a` = PR #16). Receipt: `build-os/receipts/P-032a-negative-space.md`.

## Staged next (recommended by the sub-arc)

- **P-032b — `groove_coherence` live-wire — the RISKIER packet.** It relocates
  `analyze_groove` to BEFORE `score_doctrine` and threads it in (the P-016
  live-wire lesson: an evidence-gated signal is only live if computed before its
  consumer — needs a no-re-run live-wire test asserting on real `analyze()`
  output), THEN adds the groove-coherence scorer. This is where
  onset-regularity/IOI (deferred from P-032e AND P-032a) finally reaches
  doctrine. Confirm active via the orchestrator; do NOT open blind.

## Epic arc (Timbaland sub-arc P-032.x)

**P-032e ✓ (beat_identity — CRUX) → P-032a ✓ (negative_space) → P-032b
(groove_coherence live-wire — where onset-regularity/IOI, deferred from P-032e
AND P-032a, gets plumbed in — NEXT) →** P-032c (low_end_motion/pocket) → P-032d
(rhythmic_surprise, weak-form) → P-032f (vocal-role refinement) → P-032g (loop
static-vs-iconic context) → **[fold P-031 confidence here]** → P-032h (author
`timbaland.json`, first non-byte-identical output) → P-032i
(Timbaland-vs-Halee/Ramone differential proof). P-030 (rename dims)
orthogonal/last.

---
_Cleared by the archivist on P-032a close (2026-07-01). One packet at a time.
Builder implements exactly this; qa proves; reviewer judges; archivist closes
with a receipt._
