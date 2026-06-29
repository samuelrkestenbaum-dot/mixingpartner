# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **Candidate P-002 (net-new):** add a decision-ledger event-type vocabulary
  (`EVENT_TYPES`) as **new** vocabulary — NOT "add to an existing enum" (no such
  enum exists in this repo; see stale note below).
- **Candidate P-003:** readiness-vs-refusal ledger-status UI clarity.
- **Candidate cleanup packet:** two pre-existing literals in `creative.py` still
  not record-resolved — `chorus_lift_B`'s `loops or supporting[-1:]` (~line 194)
  and the `loop` branch's `loops[0] if loops else "the loop"` (~line 217).
  Latent on today's 3 fixtures (the `"the loop"` string never leaks — that
  branch only fires when `loops` is non-empty), but worth a follow-up packet.

## Genuinely real carried follow-ups (verified)

- **Real macOS/Logic test surface** — out of current authority (needs real DAW;
  blocked by the no-real-DAW guardrail).
- **Controlled Class-3 apply path** — guardrail-gated; do not open without an
  explicit apply-safety packet.

## Done (resolved)

- **Richer variant→track attribution** — **DONE via P-001**
  (`build-os/receipts/P-001-resolve-variant-track-attribution.md`).

## Stale / not-real (verified by orchestrator — do NOT act on as written)

- The following inherited follow-ups reference architecture that has **ZERO
  matches in this repo** and should be treated as stale: `LogicActionPayload`
  (multi-parameter), a real adapter narrowing `supported_action_types`,
  `RealLogicSessionAdapter`, dead `_RISK_HINTS` cleanup, adding to an existing
  `EVENT_TYPES` enum, full `Gravito` adapter, standalone `compare-variants`
  alias. That architecture does not exist here — verified by grep (0 matches).
- A prior chat handoff referenced git state (a `main` branch, PR #12, branch
  `claude/hardening-11-…`) that does NOT match this repo on disk — there is no
  `main`; default is `claude/dreamy-turing-z0oxll`. Treat any inherited
  SHA/PR/packet-number claims as unverified until checked against `git`.

## Known risks / debt

- The two unresolved `creative.py` literals (above) remain a latent attribution
  gap until the cleanup packet lands.
- Test env: numpy + pytest are not preinstalled. The full suite requires
  `pip install -e ".[dev]"` from `logic-mix-os/` (a network install) before
  `python -m pytest`.

## Open boundaries (awaiting explicit go)

- Push of the P-001 commits (`2bc48cb`, `318042b`) plus the archivist memory
  commit to `origin/claude/logic-mix-os-hardening-12-7hbeh1` is paused for the
  user's explicit go. Pushing will update the already-open **PR #13**
  (base `claude/dreamy-turing-z0oxll`) to include P-001 alongside the Build OS
  install.
- NOTE: P-000's install commits are **already pushed** to
  `origin/claude/logic-mix-os-hardening-12-7hbeh1` (git confirms branch tracking
  is up to date for those). The earlier "P-000 push paused for go" boundary is
  retired.

---
_Append-only working notes._
