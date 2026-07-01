# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

No product packet in flight. The orchestrator stages the next packet on the
user's go.

## Last closed

- **P-018** — Confirmed-revert outcome feeds the live next-pass loop (the FIRST
  confirmed-outcome signal in the learning loop). A PIVOT off the complete
  judgment-tuning path onto the learning-loop / feedback frontier (user said
  "Yes"); orchestrator-routed. An opt-in `memory-record --reverted` records a
  confirmed operator revert (`record_pass(..., reverted=True)` →
  `mix_pass_history.json`); the live `_apply_history` consumer then DEMOTES the
  reverted move and surfaces exactly ONE confirmed "Revert last pass" item at
  priority 95 **regardless of the score-delta `got_worse` inference (OVERRIDE)**
  — measurably changing real `analyze(--memory-dir)` `next_pass`; opt-in /
  byte-identical by default. **OVERRIDE semantics chosen by the
  orchestrator-in-chief (user may redirect at the merge gate).** **Why THIS seam:**
  the decision LEDGER (`add_decision`/`decision_ledger`) is display-only
  (`cli.py:315`, ZERO analyze-path consumers), so a ledger producer would be inert;
  the ONLY LIVE seam was the history axis. Two commits: `736fa8b` Commit-1
  (`record_pass` field + `_apply_history` override + 9 unit tests; green in
  isolation = 249) + `6134d27` Commit-2 (`--reverted` CLI wire + 4 no-re-run
  liveness/CLI tests). Suite **240 → 253 passed** (+13; 0 failed/skipped/warnings,
  green under `-W error`); regression **68/68, 0 critical, 0 warnings** held;
  byte-identical default; liveness proven load-bearing (FAILS pre-P-018, PASSES at
  tip); override non-vacuous; safety grep clean; UI N/A; P-008/P-009 test files
  unedited and green (17). qa **GREEN**; reviewer **pass**. **Codex NOT available
  — single-reviewer verdict.** **P-018 is local-only** (commits `736fa8b`,
  `6134d27` on the dev branch on top of the `6c40e2b` PR #15 merge). Receipt:
  `build-os/receipts/P-018-confirmed-revert-feeds-next-pass-loop.md`.

## Next (candidate — NOT staged)

- **The OUTCOME→learning axis is now OPEN** (P-018 landed the first
  confirmed-outcome signal). The reachable next move is the **outcome-enum
  generalization** — widen the `reverted: bool` field to a small outcome enum
  (`reverted`/`kept`/`refined`) to round out the loop (widens WITHOUT breaking the
  byte-identical default). **User-gated for the semantics — do NOT open without an
  explicit ask.** Route any further outcome/event producer onto a LIVE channel
  (history or taste), NEVER the display-only ledger.
- The judgment-layer flip program remains at a DOCTRINE-HONEST EQUILIBRIUM. The one
  remaining honest thread there is the SYMMETRIC re-judgment (is `subtractive_drop`
  at 85.29 itself slightly OVER-valued?) — user-gated, un-signed-off, NOT staged.

---
_Cleared by the archivist on P-018 close (2026-07-01). One packet at a time._
