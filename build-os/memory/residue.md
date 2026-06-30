# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## Deferred (follow-up packets)

- **P-008 — History-aware next pass (THE OUTCOME SIDE OF THE LEARNING LOOP):**
  `plan_next_pass` should consume `mix_pass_history` (improved / got_worse /
  revert_candidates) so the system does **not** re-recommend a move that
  regressed. With P-007 closing the *consumer* (taste → governance) half of the
  loop, this is the natural **next high-leverage trajectory packet** — the
  *outcome* (history → next-pass) half. **Fold in the test gap below.**
- **P-007b — Live opt-in surface (from P-007):** wire a real per-operator
  `taste_profile` from `memory_dir` into a pipeline/cowork run. Must stay
  **explicit per-operator** so P-007's byte-identical-by-default guarantee
  survives into the pipeline (the default `taste_profile=None` path must remain
  byte-identical end-to-end). Deferred deliberately out of P-007's two-file scope.
- **Test gap (low priority, from P-007):** the `drum_room_bloom` narrower-taste
  path in `_TASTE_KIND_BIAS` is **data-symmetric with `width_bloom`** but
  currently untested. Add a test — **fold into P-008.**
- **Net-new event-logging packets (from P-002/P-004) — REFRAMED, still BLOCKED ON
  A PRODUCT DECISION:** `taste_feedback`, `validation_check`, `revert`,
  `manual_note` remain valid `EVENT_TYPES` members with **NO producer wired into
  the decision ledger today** (taste → `taste_calibration.json`; validation only
  returns; revert is a pass-record field; no `manual_note` writer exists).
  **Reframe:** now that P-007 delivers a real CONSUMER of recorded signals
  (recorded taste → governance), wiring `validation_check` / `taste_feedback`
  producers is **more justified** — the recorded-signal loop now has a downstream
  use. BUT this is still **net-new FEATURE work** behind the same unanswered
  product decision: **should validation / taste / revert / note signals actually
  be written to the decision ledger?** Keep deferred; do NOT start as packets
  until that product decision lands.

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
  Render-only; no backend reach-in.
- **Event-tagging follow-up (from P-002) — in-scope part** — **DONE via P-004**
  (`build-os/receipts/P-004-event-tagging-mix-decision.md`). The one existing
  untagged ledger write (`cowork.py::_write_mix_decision`) now passes
  `event_type="mix_decision"`. **EVENT_TYPES is now applied to every EXISTING
  ledger write:** `mute_candidate` (via P-002's `record_plan_decisions`) and
  `mix_decision` (via P-004's `_write_mix_decision`). The other vocabulary
  members (`taste_feedback` / `validation_check` / `revert` / `manual_note`) have
  no existing producer and are tracked as net-new packets under Deferred above —
  NOT part of this DONE item.
- **`creative_renderer` readiness follow-up (from P-003)** — **DONE via P-005**
  (`build-os/receipts/P-005-creative-renderer-readiness.md`).
  `creative_renderer.py::render_governance`'s `## Stop Conditions` section now
  renders P-003's labelled `READY TO STOP` / `NOT YET — keep iterating` block in
  **markdown** (full `reasons` list, warning-when-ready), replacing the flat
  boolean dump at `creative_renderer.py:104`. Render-only; markdown-clean (no
  HTML); 2 new render-only tests; suite 108→110.
  **MILESTONE — surface consistency closed:** the readiness-vs-refusal treatment
  is now CONSISTENT across all THREE governance surfaces — `operator_view.py`
  (text, P-003), `html_dashboard.py` (HTML, P-003), and `creative_renderer.py`
  (markdown, P-005). The P-003 surface-consistency thread is **fully closed**.
- **`creative.py` literal cleanup** — **DONE via P-006**
  (`build-os/receipts/P-006-creative-literal-cleanup.md`). The two pre-existing
  un-resolved literals in `generate_variants` are now record-backed: Site 1
  (`creative.py:194`, `chorus_lift_B`) `loops or supporting[-1:]` →
  `_resolve(loops, supporting[-1:], [r["name"] for r in records][:1])` (closes the
  empty-`tracks_affected` path, restores P-001's non-empty + real-record-subset
  invariant, reuses the `_resolve` seam); Site 2 (`creative.py:217`, `loop`
  branch) replaces the `"the loop"` literal with a real-record-name fallback.
  Single product commit `6e98a3b`; suite 110→112; 2 new tests.
  **Every `tracks_affected` site in `generate_variants` is now record-backed and
  non-empty**, and loop-branch prose can no longer name a non-existent track
  (except under a degenerate record-free input — see Known risks below).
- **Taste profile feeds governance** — **DONE via P-007**
  (`build-os/receipts/P-007-taste-feeds-governance.md`). The recorded operator
  taste profile (`memory._derive_taste` statements) now **biases variant
  governance** — opt-in, bounded, evidence-tagged. An optional `taste_profile`
  arg (default `None`) on `govern_variant` / `govern_branches` / `run_governance`;
  a pure `_apply_taste` helper + `_TASTE_KIND_BIAS` map (verbatim `_TASTE_MAP`
  statements); `TASTE_MAX_DELTA = 15` (`< 30`, the truth nudge); a
  `taste_adjustments` evidence field present **only** when an adjustment applies.
  Two operators with different taste now get different governed winners from the
  same song (proven: narrower taste flips `chorus_lift_A` → `chorus_lift_C`).
  Single product commit `bd08f28` (`governance.py` +75/−6,
  `tests/test_governance_taste.py` new, 13 tests); suite 112→125; regression
  68/68 held; default path byte-identical (the HARD backward-compat gate).
  **MILESTONE — FIRST CLOSURE OF THE LEARNING LOOP:** recorded taste now
  influences recommendations (opt-in, bounded `±15`, evidence-tagged,
  doctrine-inviolable — a doctrine-vetoed `width_bloom` at `align=45<50` stays
  rejected even with maxed wider taste pushing identity to 84). **Memory is no
  longer purely write-only on the governance axis** — a real consumer of recorded
  signals exists. The *consumer* half of the loop is closed; the *outcome* half is
  P-008.

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

- **Degenerate empty-`records` input (low priority — NOT a packet yet):** under a
  truly **empty** `records` list (an unconstructible / degenerate input on the
  engine path), P-006's Site 1 still returns `[]` and Site 2 still yields
  `"the loop"`. Acknowledged by the reviewer as out-of-scope — a possible future
  guard, not a defect. Raise as a packet only if a record-free engine path
  becomes constructible.
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

- **P-007's product commit `bd08f28` is local-only as of this close** (this
  archivist close did not push). Earlier packets' push history: P-000 install
  commits are pushed to `origin/claude/logic-mix-os-hardening-12-7hbeh1`; P-004
  is pushed (PR #13). Any push of `bd08f28` (and the P-005/P-006 commits, if not
  yet pushed) updates the already-open **PR #13** (base
  `claude/dreamy-turing-z0oxll`) — do so only under the user's standing/explicit
  push-go.

---
_Append-only working notes._
