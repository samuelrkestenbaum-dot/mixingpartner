# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- Confirm the first product packet ("hardening-12" line) — scope it before the
  builder touches product code.
- Carried-forward follow-ups noted in prior sessions (verify against current code
  before acting — a prior handoff was stale): real macOS/Logic test surface;
  controlled Class-3 apply path; multi-parameter `LogicActionPayload`; a real
  adapter that narrows `supported_action_types`; richer variant→track attribution;
  dead `_RISK_HINTS` cleanup; signed/tail-truncation audit hardening; full Gravito
  adapter; standalone compare-variants alias; readiness-vs-refusal ledger-status
  UI clarity; adding new ledger event types to `EVENT_TYPES`.

## Known risks / debt

- A prior chat handoff referenced git state (a `main` branch, PR #12, branch
  `claude/hardening-11-…`) that does NOT match this repo on disk — there is no
  `main`; default is `claude/dreamy-turing-z0oxll`. Treat any inherited
  SHA/PR/packet-number claims as unverified until checked against `git`.
- Test env: numpy + pytest are not preinstalled. The full suite requires
  `pip install -e ".[dev]"` from `logic-mix-os/` (a network install) before
  `python -m pytest`.

## Open boundaries (awaiting explicit go)

- Push of the P-000 install commits to `origin/claude/logic-mix-os-hardening-12-7hbeh1`
  is paused for explicit go (per the no-external-mutation gate).

---
_Append-only working notes._
