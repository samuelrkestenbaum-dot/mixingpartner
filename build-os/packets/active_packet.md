# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

## Last closed

- **P-023 — Versioned, self-describing raw-CLI contract (option C, step 1).**
  CLOSED 2026-07-01, qa GREEN + reviewer pass (Codex unavailable —
  single-reviewer verdict). Added `API_VERSION = "1.0"` + a `describe_contract`
  command (registry 34 → 35) returning `{api_version, invocation, commands:{name:
  {purpose, phase, params, side_effect}}}` — `params` inspect-derived (cannot
  drift from code), `side_effect` an honest classification making live-vs-dead a
  first-class contract fact (4 writers, 31 `none`) — plus a concise
  `COWORK_CONTRACT.md`. Two commits `60b3b92` + `dcc4c5b` on the dev branch
  (base `6c40e2b`); **local-only, not pushed/merged.** Suite 277 → 293 (+16);
  regression 68/68. Receipt:
  `build-os/receipts/P-023-versioned-self-describing-cli-contract.md`.

## Next (staged — NOT yet confirmed active)

- **P-024 — thin MCP server wrapping the same cowork registry (option C, step 2 —
  the FINAL arc step).** The follow-on the user sequenced: expose the
  already-proven, now-versioned cowork surface as an MCP server so Claude Cowork
  calls it as native tools. **Reuse `describe_contract`'s per-command `params` /
  `side_effect` metadata directly as the MCP tool schemas** (do NOT re-derive).
  **Carry-forward guard to fold in:** add a **version-fingerprint test** — pin a
  hash of the contract surface so any change to `params` / `side_effect` forces a
  conscious `API_VERSION` decision (closes the P-023 reviewer watch-item that the
  hand-maintained version can silently lag a surface change).
  - After P-024 the arc to the Cowork-usable final state is COMPLETE; landing the
    accumulated P-017-guard → P-024 work on default is the natural close
    (USER-GATED).
  - Architecture/transport fork — confirm as active via the orchestrator before
    building; do NOT open blind.

---
_Cleared by the archivist on P-023 close (2026-07-01). Next = P-024 (MCP server,
the final step of option C / the arc). One packet at a time._
