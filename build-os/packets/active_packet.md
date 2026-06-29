# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-001
- **Title:** Resolve variant `tracks_affected` against real records

## Goal / "done" criteria

- For every fixture, every variant emitted by the creative engine
  (`run_creative_engine` / `generate_variants`) has a **non-empty**
  `tracks_affected` whose entries are **all real track names present in
  `result.records`** — no hard-coded literal that is absent from the project.
  Asserted by a new test that **fails on today's code** and passes after the fix.

## In scope

- `logic_mix_os/creative.py` — `generate_variants` and the `_variant(...)` call
  sites that hard-code track names (e.g. `["Lead Vocal"]`,
  `["Drum Overheads","Drum Room"]`); resolve them against `result.records` /
  existing supporting-element / loop-name helpers.
- New `tests/test_creative_attribution.py`.
- May **read** `governance.py` for the governed/winning paths — **must not edit it.**

## Out of scope (explicit)

- Scoring weights, governance verdicts, new variant kinds, any CLI change, any
  bridge/apply/executor work. Surface those as separate packets.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1`, cleanly based on the default
  `claude/dreamy-turing-z0oxll` @ `694d19d` (verified: 2 ahead / 0 behind, no
  product code changed by the P-000 install).

## Plan (≤2 commits)

1. **Commit 1 (green in isolation):** add `tests/test_creative_attribution.py`
   asserting every variant's `tracks_affected` ⊆ real record names across all 3
   fixtures, **and** the minimal `creative.py` change to make it pass (test-first;
   the commit builds and passes on its own).
2. **Commit 2 (optional, same packet):** tidy any remaining hard-coded literals /
   add a small resolver helper, keeping the full suite + regression green.

## Guardrails

- No real DAW / Logic / AppleScript / subprocess / `.logicx` write / network in
  tests; fake/fixture data only; do not introduce `RealLogicSessionAdapter` or a
  `compare-variants` alias. Deterministic outputs preserved.

---
_Confirmed P-001 on the user's "go". Builder implements exactly this; archivist
clears on close._
