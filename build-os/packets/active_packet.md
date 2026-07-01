# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

No product packet is in flight. The orchestrator picks the next one from the arc
below (or re-surveys `build-os/memory/residue.md`).

## Last closed

- **P-020 — `describe_session` session-flow discoverability** (CLOSED 2026-07-01,
  qa GREEN, reviewer pass; **Codex NOT available — single-reviewer verdict**).
  SECOND step of the arc P-019→P-023 to the Cowork-usable end-to-end state. Adds a
  pure `_SESSION_FLOW` structure + a read-only `describe_session` command to the
  cowork registry (count **33 → 34**) that returns the SAME registry as an ORDERED,
  phase-grouped session flow `{"phases": [...], "auxiliary": [...]}` in the canonical
  order **intake → classify → diagnose → plan → checklist → validate → record-outcome
  → next-pass** (31 commands across 8 phases + 3 honest `auxiliary` off-axis:
  `run_creative_engine`, `build_missing_tool`, `describe_session`). Completeness
  INVARIANT load-bearing (every `COMMANDS` key covered EXACTLY ONCE; qa verified
  31+3=34). Additive / read-only (every existing handler byte-unchanged; output
  deterministic + deep-copied). Single commit **`942a68a`** (green in isolation =
  tip). Suite **259 → 269 passed** (+10, green under `-W error`); regression
  **68/68, 0 critical, 0 warnings**; safety grep clean; UI N/A. **Local-only** on
  the dev branch (base `6c40e2b`, PR #15) — not pushed/merged. Receipt:
  `build-os/receipts/P-020-describe-session-flow-discoverability.md`.
  **Carry-forward → P-021:** surface the live-vs-dead-ledger distinction
  (`record_mix_pass` live history vs `write_mix_decision` dead ledger, both under
  `record-outcome`) in the walkthrough/session view.

## Next (staged — the arc to the Cowork-usable end-to-end state, P-021 → P-023)

Steps 1 (P-019) and 2 (P-020) are DONE. Remaining, in sequence:

- **P-021 — verified end-to-end agent walkthrough (TESTS-ONLY).** Drive a full
  Logic-Pro mixing session through the cowork surface start-to-finish; prove the
  whole chain works as one session. **Also the home for the carried
  live-vs-dead-ledger clarity nudge** (make it clear an agent should not treat the
  `write_mix_decision` dead-ledger write as loop-closing — only `record_mix_pass`
  on the LIVE history channel closes the loop).
- **P-022 — OPTIONAL session-efficiency / override-propagation.** Sequence only if
  P-021 surfaces a real need.
- **P-023 — USER-GATED transport decision: MCP server vs a documented raw-CLI
  contract as the agent transport.** **Do NOT open blind; sequenced LAST** — a
  product/architecture fork that needs an explicit user ask.

---
_Cleared by the archivist on P-020 close (2026-07-01). One packet at a time; the
orchestrator-in-chief confirms the next active packet._
