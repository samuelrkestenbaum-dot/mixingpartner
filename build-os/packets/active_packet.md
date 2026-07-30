# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE.
- **Last closed:** **P-062 — Multi-Lens Execution Brief** (2026-07-30, BOTH
  formal gates GREEN; final proof at `3a7144f`: suite 1470/0/0, regression
  93/93). Receipt: `build-os/receipts/P-062-multi-lens-execution-brief.md`.
  Branch `claude/logic-mix-os-p061-detector-0dvr2t`, HEAD `3a7144f` at close;
  merge-base with default `9cfe990` verified.

## Next candidates (NOT staged — each needs the user's word / orchestrator scoping)

- **★ THE OPEN USER GATE: the merges.** P-060 (PR #38 candidate), P-061, and
  P-062 all STACK on `claude/logic-mix-os-p061-detector-0dvr2t` awaiting the
  user's explicit merge word. Default remains `9cfe990`.
- **HAPPY MAN RE-RUN #2** — the real-world confirmation for both halves of the
  Happy Man fix, now with the execution brief available: analyze, then
  `execution-brief --dir <out>`.
- **Contract-fingerprint guard** (hash the cowork contract surface) — mildly
  more urgent now that `API_VERSION` has been hand-bumped twice (1.0 → 1.1 at
  P-062).
- **PR #12** — close-or-rebase decision (recommendation recorded at `86a3242`).
- Deferred advisories from P-062: host-prompt hardening against invented
  parameters; renderer dead-branch cleanup; re-audit `"wider"` in
  `_WIDTH_KEYWORDS` if `_iter_plan_texts` coverage ever expands.

---
_Cleared by the archivist on P-062 close (2026-07-30). One packet at a time:
builder → qa → reviewer → archivist → receipt._
