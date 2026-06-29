# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-002
- **Title:** Net-new `EVENT_TYPES` decision-ledger vocabulary + optional validated `event_type` on `add_decision`
- **Authority:** build

## Goal / "done" criteria

- `add_decision` accepts an **optional** `event_type`: omitted → behavior unchanged
  (entry stored as today, no `event_type` key); supplied **and in** `EVENT_TYPES`
  → stored on the entry; supplied **and not in** `EVENT_TYPES` → raises
  `ValueError` (mirroring `validation/confidence.py::tag_claim`). Full suite stays
  green (≥ 101 passed incl. new test) and `regression` stays 68/68.

## In scope (exact changes)

1. `logic_mix_os/constants.py` — add a module-level `EVENT_TYPES: list[str]` with a
   section-comment header, alongside `EVIDENCE_TYPES` (after ~line 155), matching
   that flat list-of-strings style (NOT the `RISK_CLASSES` dict style).
2. `logic_mix_os/memory.py` — `add_decision(self, decision, event_type=None)`:
   when `event_type is not None`, validate against `EVENT_TYPES` (mirror
   `tag_claim`'s raise), then store it on the entry **only when provided** (key
   absent for free-form callers, preserving today's shape). `from .constants import EVENT_TYPES`.
3. `tests/test_session_memory.py` — add the new test(s).

## Out of scope (explicit — do NOT touch)

- Ledger signing/hashing/integrity; tail-truncation/rotation/size bounds.
- Any ledger UI / dashboard rendering; new CLI flags/surface for event types.
- Governance / doctrine wiring.
- Making `event_type` required; back-filling beyond the optional Commit-2 tag.
- The two unresolved `creative.py` literals (separate cleanup packet).
- `RealLogicSessionAdapter`; real DAW / Logic / AppleScript / subprocess / `.logicx` / network.

## Backward-compat gate (4 callers, all must stay green)

- `memory.py:112` `record_plan_decisions` → `add_decision({...})` (no event_type)
- `cowork.py:93` `_write_mix_decision` → `mem.add_decision(decision or {})` (can be `{}`)
- `cli.py:291` `mem.record_plan_decisions(result)`
- `tests/test_session_memory.py:53` asserts only `validation`/`reason` keys present
- All stay green because `event_type` defaults to `None` and validation fires only
  when a value is supplied; the stored key is additive.

## Proposed `EVENT_TYPES` membership (builder may trim/rename, keep a flat closed list)

```python
EVENT_TYPES = [
    "mix_decision",     # a recommendation acted on / logged (default category)
    "mute_candidate",   # muting/chopping an element (record_plan_decisions)
    "revert",           # rolling back a prior pass/change
    "taste_feedback",   # user taste signal logged as a decision
    "validation_check", # a validation/QA gate result
    "manual_note",      # free-form analyst note
]
```

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1`, merge-base `694d19d` on default
  `claude/dreamy-turing-z0oxll` (verified). Do not rebase.

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** `EVENT_TYPES` in `constants.py` + optional
   validated `event_type` in `add_decision` + new test in `test_session_memory.py`
   asserting **all three**: accept (stored), reject (`ValueError`), and
   backward-compat (no `event_type` → succeeds, no key). Passes its own file
   (`pytest tests/test_session_memory.py`) standalone.
2. **Commit 2 (optional):** tag the internal auto-logger — `record_plan_decisions`
   passes `event_type="mute_candidate"`; suite + regression stay green.

## Guardrails

- Deterministic; no network/subprocess/AppleScript/`.logicx`; no
  `RealLogicSessionAdapter`; in-scope files only. No external mutation — STOP for
  explicit go before any push/merge/deploy.

---
_Confirmed P-002 on the user's "go". Builder implements exactly this; archivist
clears on close._
