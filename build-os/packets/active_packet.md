# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-004
- **Title:** Event-tagging: tag the one existing untagged ledger write (`cowork.py::_write_mix_decision` → `mix_decision`)
- **Authority:** build (feature follow-up to P-002)

## Census result (why this packet is one line + one test)

The decision ledger (`decision_ledger.json`) is appended ONLY via
`ProjectMemory.add_decision`. Its callers: `record_plan_decisions` (already tags
`mute_candidate`, P-002) and `cowork.py::_write_mix_decision` (UNTAGGED — this
packet). `taste_feedback`, `validation_check`, `revert`, `manual_note` have **no
existing ledger producer** (taste → `taste_calibration.json`; validation only
returns; revert is a pass-record field) → DEFERRED as net-new feature packets, not
tagged here.

## Goal / "done" criteria (single, testable)

- `cowork.py::_write_mix_decision` passes `event_type="mix_decision"` into
  `add_decision`, so EVERY existing ledger write now carries a valid `EVENT_TYPES`
  tag. A new test drives the `write_mix_decision` cowork command through
  `run_command` with a memory-backed ctx and asserts the resulting ledger entry
  has `event_type == "mix_decision"`. Suite 107→108 passed; regression 68/68.

## In scope (exact)

- `logic_mix_os/cowork.py:93` — `return mem.add_decision(decision or {})` →
  `return mem.add_decision(decision or {}, event_type="mix_decision")`. No
  signature/command-surface change.
- `tests/test_cowork.py` (or `tests/test_session_memory.py`) — one new test using
  the ctx-build pattern from `test_cowork.py:36-47` (fresh ctx with
  `ProjectMemory(tmp_path)` under the `"memory"` key) asserting the tag.

## Out of scope (explicit — DEFER as separate net-new packets)

- Inventing `taste_feedback` ledger logging (routing `add_feedback` into the ledger).
- Inventing `validation_check` ledger logging (routing `_validate_mix_pass`/
  `validate_output` into the ledger).
- Inventing `revert` ledger logging.
- Any `manual_note` writer.
- UI/renderers, governance, CLI argument/surface changes.

## Backward-compat (verified)

- `test_session_memory.py:53` asserts only `validation`/`reason` (subset) — additive
  `event_type` is fine. `test_cowork.py:30-31` SKIPS `write_mix_decision` (no
  positive-path shape assertion today). No test asserts an exact key-set.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ current HEAD (clean, up to date with
  origin). Default `claude/dreamy-turing-z0oxll` @ `694d19d`. No `main` exists.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** add the new test asserting
   `write_mix_decision` → `event_type == "mix_decision"`, AND the one-line
   `cowork.py:93` edit in the same commit (the test REDs without the edit, so they
   ship together to keep Commit-1 green in isolation).
2. **Commit 2 (optional):** none expected.

## Guardrails

- No network/subprocess/AppleScript/`.logicx`/`RealLogicSessionAdapter`;
  deterministic; tag the one existing write only — add no new ledger-logging feature.

---
_Confirmed P-004 on the user's "go". Builder implements exactly this; archivist
clears on close._
