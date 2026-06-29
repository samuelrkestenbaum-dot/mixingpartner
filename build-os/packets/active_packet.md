# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-003
- **Title:** Readiness-vs-refusal clarity in the status / dashboard surface
- **Authority:** design-UI — FRONTEND / RENDERER FILES ONLY

## ⚠️ AUTHORITY GATE (read first)

RENDER-ONLY packet. The builder **consumes** `result.governance["stop_conditions"]`
exactly as `governance.py` already produces it, and MUST NOT edit `governance.py`,
`pipeline.py`, `cowork.py`, `cli.py`, `bridge/`, `planners/`, `doctrine/`, or any
backend/runtime logic. No new stop-condition computation, fields, or thresholds.
If a new governance field seems "needed" → STOP (that's a separate data packet).

## Goal / "done" criteria (single, testable)

- The status TEXT surface (`render_status`) AND the HTML dashboard
  (`render_dashboard`) EACH render a distinct, labelled **ready-to-stop vs
  not-yet/refusal-reasons** block sourced solely from
  `result.governance["stop_conditions"]`:
  - `should_stop is True` → a labelled "READY" block showing the met state and the
    `warning` (overworking-risk) line.
  - `should_stop is False` → a labelled "NOT YET" block listing each `reasons`
    entry (the "not yet: <label>" refusal reasons).
- A renderer test asserts BOTH states appear with the correct labels in BOTH
  renderers, driven by a hand-built `stop_conditions` dict (render-only).

## Data consumed (verified, read-only)

- `governance.py::stop_conditions` (`governance.py:228-248`), surfaced at
  `result.governance["stop_conditions"]` (`governance.py:299`). Shape:
  `should_stop: bool`, `reasons: List[str]` (always non-empty), `warning: str|None`
  (set only when `should_stop` True). Same dict `cowork::_validate_mix_pass`
  consumes (single source of truth — OUT OF SCOPE to touch). Shape locked by
  `test_governance.py::test_stop_conditions_shape`.

## Current gap (verified)

- `operator_view.py::render_status` (25-87): does NOT reference governance/
  stop_conditions at all today — readiness signal is net-new.
- `html_dashboard.py::render_dashboard` (184-185): renders only `should_stop` as a
  bare boolean; drops `reasons` and `warning`.

## In scope (confirmed)

- `logic_mix_os/renderers/operator_view.py` — add readiness block to `render_status`
  (near the "NEXT RECOMMENDED ACTION" block, ~80-86).
- `logic_mix_os/renderers/html_dashboard.py` — expand the governance-card readiness
  rendering (184-185) into a labelled ready/not-yet block with `reasons` + `warning`,
  inside the existing `id="governance"` card.
- `tests/test_dashboard.py` — extend with the both-states assertions.

## Out of scope (do NOT touch)

- `governance.py`, `pipeline.py`, `cowork.py`, `cli.py`, `bridge/`, `planners/`,
  `doctrine/` — all backend/runtime. No new computation/thresholds/fields. The CLI
  already calls the renderers correctly — mirror its PATTERN, do not edit it.

## Testing note (fixtures can't produce READY)

- All 3 fixtures currently yield `should_stop=False` (non-empty "not yet:" reasons,
  `warning=None`). None hits READY; forcing it needs backend changes (out of scope).
  So test BOTH states at the renderer UNIT level by passing a constructed
  `stop_conditions` dict:
  - NOT-YET: a real analyzed fixture (already False) or a hand-built dict.
  - READY: hand-built `{"should_stop": True, "reasons": ["all stop conditions met …"],
    "warning": "<overworking note>"}` wrapped in a minimal stand-in result whose
    `.governance` carries it. Keep it render-only and deterministic.

## Determinism + guardrails

- Same `stop_conditions` in → same block out. No time/randomness/I/O.
- Dashboard stays **self-contained**: inline CSS only, NO `<script>`, NO `http(s)://`,
  NO external assets — keep `test_dashboard_is_self_contained_html` and
  `test_dashboard_includes_core_screens` green.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1`, base `claude/dreamy-turing-z0oxll` @
  `694d19d` (verified correct base).

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** add renderer tests to
   `tests/test_dashboard.py` asserting BOTH renderers emit a labelled READY block
   (hand-built `should_stop=True` + `warning`) and a labelled NOT-YET block listing
   `reasons` (`should_stop=False`) — these FAIL on today's output. Then the minimal
   render change in `operator_view.py` + `html_dashboard.py` to pass. Commit-1
   passes its own tests standalone.
2. **Commit 2 (optional polish):** wording/label refinement + self-contained-HTML
   assertion tightening. No scope expansion.

---
_Confirmed P-003 on the user's "go". Builder implements exactly this; archivist
clears on close._
