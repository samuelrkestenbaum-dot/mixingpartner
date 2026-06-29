# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **Candidate cleanup packet:** two pre-existing literals in `creative.py` still
  not record-resolved — `chorus_lift_B`'s `loops or supporting[-1:]` (~line 194)
  and the `loop` branch's `loops[0] if loops else "the loop"` (~line 217).
  Latent on today's 3 fixtures (the `"the loop"` string never leaks — that
  branch only fires when `loops` is non-empty), but worth a follow-up packet.
- **Candidate event-tagging follow-up (from P-002):** only
  `record_plan_decisions` tags its events today (`mute_candidate`). Tag the other
  live ledger callers — `cowork.py::_write_mix_decision` → `mix_decision`, and
  wire `taste_feedback` / `validation_check` where those signals are produced.
  Out of scope for P-002; a natural future packet building on the new
  `EVENT_TYPES` seam.
- **Candidate `creative_renderer` readiness follow-up (NEW, from P-003):**
  `creative_renderer.py:104` also consumes `stop_conditions` but does NOT yet
  show the labelled READY/NOT-YET treatment that P-003 added to
  `operator_view.py` and `html_dashboard.py`. A future design-UI (render-only)
  packet for full surface consistency. Flagged by the reviewer; out of scope for
  P-003.

## Genuinely real carried follow-ups (verified)

- **Real macOS/Logic test surface** — out of current authority (needs real DAW;
  blocked by the no-real-DAW guardrail).
- **Controlled Class-3 apply path** — guardrail-gated; do not open without an
  explicit apply-safety packet.

## Done (resolved)

- **Richer variant→track attribution** — **DONE via P-001**
  (`build-os/receipts/P-001-resolve-variant-track-attribution.md`).
- **Net-new `EVENT_TYPES` decision-ledger vocabulary** — **DONE via P-002**
  (`build-os/receipts/P-002-event-types-vocabulary.md`). `EVENT_TYPES` in
  `constants.py`, optional validated `event_type` on `add_decision`,
  `record_plan_decisions` tags `mute_candidate`, new test added.
- **Readiness-vs-refusal ledger-status UI clarity** — **DONE via P-003**
  (`build-os/receipts/P-003-readiness-vs-refusal-clarity.md`). Labelled
  `READY TO STOP` / `NOT YET — keep iterating` blocks in
  `operator_view.py::render_status` and the `html_dashboard.py` governance card,
  sourced from `result.governance["stop_conditions"]`; 5 new render-only tests.
  Render-only; no backend reach-in. (Full surface consistency for
  `creative_renderer.py` deferred — see Deferred above.)

## Stale / not-real (verified by orchestrator — do NOT act on as written)

- The following inherited follow-ups reference architecture that has **ZERO
  matches in this repo** and should be treated as stale: `LogicActionPayload`
  (multi-parameter), a real adapter narrowing `supported_action_types`,
  `RealLogicSessionAdapter`, dead `_RISK_HINTS` cleanup, adding to an existing
  `EVENT_TYPES` enum, full `Gravito` adapter, standalone `compare-variants`
  alias. That architecture does not exist here — verified by grep (0 matches).
  NOTE: P-002 delivered `EVENT_TYPES` as **net-new** flat vocabulary (not "added
  to an existing enum"); the stale "existing enum" framing remains wrong.
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
- **Commits on this branch are unsigned.** The configured SSH signing key
  (`/home/claude/.ssh/commit_signing_key.pub`) is an empty 0-byte file and the
  container runs as `root`, so signing is impossible. Author + committer are
  correctly `noreply@anthropic.com`; GitHub will show these commits as
  "Unverified" (missing signature only, not a misattribution). This is an
  environment limitation, not a fix-it item.

## Open boundaries (awaiting explicit go)

- **P-002 commits are now pushed** (PR #13 updated). The earlier "P-002 push
  paused for go" boundary is retired.
- The **NEW unpushed commits** are P-003's `0cd4243`, the memory commit
  `b179ca3`, plus the archivist's P-003 close commit. The user has granted
  **STANDING push-go**, so these will be pushed immediately after this close —
  pushing updates the already-open **PR #13** (base
  `claude/dreamy-turing-z0oxll`) to also include P-003 alongside P-001, P-002,
  and the Build OS install.
- NOTE: P-000's install commits are **already pushed** to
  `origin/claude/logic-mix-os-hardening-12-7hbeh1`. The earlier "P-000 push
  paused for go" boundary is retired.

---
_Append-only working notes._
