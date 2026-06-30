# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

No product packet in flight. The orchestrator stages the next one here.

## Last closed

- **P-015 — Make the masked-vocal nudge DECISIVE (user-signed-off aesthetic
  change).** Closed 2026-06-30. The deliberate, user-gated successor to P-012 and
  the resolution of the P-014 user-gated decision: it changes the default creative
  winner on a masked-lead-vocal near-tie. The user chose "Option 1 — Proceed,
  corrected" after the orchestrator transparently corrected an arithmetic error
  (the old `−8` penalty only moves overall `−1.14`, insufficient to flip; the
  corrected mechanism strengthens to `−14`). **Single product commit `1756f61`**
  (product change + updated/new tests together so Commit-1 is green in isolation):
  `creative.py` `_NUDGE_TABLE` row-0 ONLY — exempt `intimacy_pass`, strengthen
  `−8`→`−14` (`= −2.0` overall = the cap, unchanged), honest reason + doctrine
  comment + corrected stale clamp comment. Net effect in the `vocal_belief` branch
  under a masked lead vocal: `vocal_ride` (vocal_A) 82.9 → 80.9 (cap binds);
  `intimacy_pass` (vocal_B) 81.1 unchanged (exempt) → **winner FLIPS vocal_ride →
  intimacy_pass** by 0.2. Bounded — `subtractive_drop` (85.3) still wins every
  clear-ranking branch; only `vocal_belief` flips. Suite **207 → 217 passed**;
  regression **68/68, 0 critical, 0 warnings** held; Commit-1 green in isolation;
  safety grep clean; UI N/A. qa **GREEN**; reviewer **pass** (independently
  reproduced the arithmetic + a mutation test confirming non-vacuity — reverting
  both edits turned 5 binding tests RED, the negative control stayed GREEN);
  **Codex NOT available — single-reviewer verdict.** **Local-only** (product commit
  `1756f61` on the dev branch on top of `0f4e7e9`), not pushed/merged at close (the
  orchestrator pushes the dev branch after). Receipt:
  `build-os/receipts/P-015-decisive-masked-vocal-nudge.md`.

---
_Cleared by the archivist on P-015 close (2026-06-30). One packet at a time._
</content>
