# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-005
- **Title:** Extend readiness-vs-refusal treatment to `creative_renderer.py::render_governance`
- **Authority:** design-UI — FRONTEND / RENDERER FILES ONLY

## ⚠️ AUTHORITY GATE (read first)

RENDER-ONLY. CONSUME `governance["stop_conditions"]` as-is. MUST NOT edit
`governance.py`, `pipeline.py`, `cowork.py`, `cli.py`, `bridge/`, `planners/`,
`doctrine/`, or any backend/runtime logic. No new stop-condition computation,
fields, or thresholds. **Output is MARKDOWN** — the new block must be
markdown-clean (NO HTML tags); mirror P-003's labels/logic, not its HTML.

## Goal / "done" criteria (single, testable)

- In `creative_renderer.py::render_governance`, the `## Stop Conditions` section
  renders P-003's labelled treatment in markdown:
  - `should_stop` falsy → label `NOT YET — keep iterating`, lists every `reasons`
    entry, no READY label, no `None` warning.
  - `should_stop` truthy → label `READY TO STOP`, lists every `reasons` entry,
    renders `warning` only when present.
- One test asserts BOTH states: NOT-YET from a real fixture
  (`dense_chorus_with_loops`); READY from a hand-built `stop_conditions` dict
  merged into a copy of the governance dict (render-only stand-in). Both assert
  the block introduces NO HTML.

## Data consumed (verified, read-only)

- `render_governance(governance: Dict)` reads `governance.get("stop_conditions", {})`
  at `creative_renderer.py:104` and renders `should_stop`/`reasons`/`warning`
  (currently a flat boolean dump, lines ~105-112). Same `stop_conditions` dict
  P-003's renderers consume (single source of truth, `governance.py:228`/`:299`).
- Output is markdown — `pipeline.py:289-291` writes `render_governance(...)` to
  `governance_report.md` (verified: zero HTML tags).

## In scope (exactly two)

- `logic_mix_os/renderers/creative_renderer.py` — modify the `## Stop Conditions`
  block (~104-112) in `render_governance` ONLY. Keep the section header +
  surrounding markdown structure.
- `tests/test_creative.py` — add the render-only test(s). (`render_governance`
  lives in `creative_renderer.py`; its tests belong here, not `test_dashboard.py`.)

## Out of scope (explicit)

- `governance.py`/`pipeline.py`/any backend — untouched.
- `operator_view.py` and `html_dashboard.py` — done in P-003, do NOT re-touch.
- `render_creative` (same file, no `stop_conditions`) — out of scope.
- No new computation/fields/thresholds.

## Labels (reuse P-003 verbatim)

- `READY TO STOP` / `NOT YET — keep iterating`.

## Testing technique (governance-dict-level stand-in — the key nuance)

- `render_governance` takes the dict, NOT a `ProjectAnalysis`. Do NOT reuse
  `test_dashboard.py::_with_stop_conditions` (it clones a `ProjectAnalysis`).
  - NOT-YET: `render_governance(analyzed["dense_chorus_with_loops"].governance)`
    → assert `NOT YET — keep iterating` present, `READY TO STOP` absent, each real
    reason present.
  - READY: `ready = {"should_stop": True, "reasons": [...], "warning": "..."}`;
    `gov = dict(analyzed[...].governance); gov["stop_conditions"] = ready;`
    `render_governance(gov)` → assert `READY TO STOP` present, `NOT YET` absent,
    warning present.

## Determinism + format guard

- Same governance dict → same markdown; `reasons` preserve source order; no
  time/random.
- Markdown-clean guard: assert the readiness block introduces NO HTML (no `<li`,
  `<div`, `<span`, `<p>`, `<script`, `http(s)://`).

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `f9549fe` (clean, up to date
  with origin). Default `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** add the readiness block to
   `render_governance` AND the new test in `test_creative.py`, in one commit
   (test REDs without the impl). Passes its own tests standalone.
2. **Commit 2 (optional):** none expected for product.

## Guardrails

- Deterministic; markdown-clean (no HTML); render only existing `stop_conditions`;
  no backend reach-in; no network/subprocess/AppleScript/`.logicx`.

---
_Confirmed P-005 on the user's "keep going". Builder implements exactly this;
archivist clears on close._
