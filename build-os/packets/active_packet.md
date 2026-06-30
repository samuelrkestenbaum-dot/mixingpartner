# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-009
- **Title:** Live wire — thread real memory into the production analysis path (subsumes P-007b + P-008b)
- **Authority:** build (trajectory-realizing)

## Why (trajectory)

P-007 (taste→governance) and P-008 (history→next-pass) are INERT in production:
`pipeline.analyze()` never receives memory, so every real run passes
`taste_profile=None` / `history=None`. P-009 wires it — one opt-in `memory_dir`
param + one prod-surface line — turning two dormant packets into behavior a real
operator experiences. The CLI `cowork --memory-dir` chain ALREADY exists
(`cli.py:235-236,:486` register/pass it); the only missing edge is `cowork.py:28`.

## ⚠️ HARD BACKWARD-COMPAT GATE

When no `memory_dir` is supplied, EVERYTHING is byte-identical to today — all 138
tests + 68 regression invariants stay green, unchanged. Memory threading applies
ONLY when an explicit `memory_dir` is passed. The regression harness
(`regression.py:255`) and all 13 other `analyze()` CLI call sites stay memoryless.

## Goal / "done" criteria (single, testable)

- With a `memory_dir` arg on `analyze()` threaded at `cowork.py:28`: (a) every
  existing test + 68 regression invariants green, default path byte-identical; AND
  (b) `tests/test_live_wire.py` proves END-TO-END through `analyze()` and through
  the cowork surface that a pre-seeded `memory_dir` (written via real
  `ProjectMemory`) measurably changes `mix_plan["next_pass"]` (history axis) and
  the governed winner (taste axis), while `memory_dir=None` == the no-arg call.

## In scope (exactly three files)

1. `logic_mix_os/pipeline.py` — add trailing `memory_dir: Optional[str|Path] = None`
   to `analyze()` (`:75-81`); add `from .memory import ProjectMemory`; construct-once
   block (build `ProjectMemory(memory_dir)` once under `if memory_dir is not None:`,
   bind `_history = mem.history()` and `_taste = (mem.taste_profile() or {}).get("profile")`,
   both default `None`); pass `history=_history` into `plan_next_pass` (`:196`) and
   `taste_profile=_taste` into `run_governance` (`:206`).
2. `logic_mix_os/cowork.py` — at `:28`, add `memory_dir=memory_dir` to the
   `analyze(...)` call (the ONE prod-surface change; `build_context` already takes
   `memory_dir` and builds `ProjectMemory` at `:29`).
3. `tests/test_live_wire.py` (new) — end-to-end, no DAW/network.

## Verified shape matches (no mismatch)

- `memory.history()` (`memory.py:99`) → `List[Dict]` with `got_worse`/`next_recommended`/
  `revert_candidates` — exactly what `plan_next_pass`'s `_apply_history` reads.
- `memory.taste_profile()` (`memory.py:148`) → `{"feedback","profile"}`; `["profile"]`
  is the `List[str]` `run_governance`'s `_apply_taste` consumes.
- Empty store degrades to no-op: absent JSON → `history()`=`[]`, `profile`=`[]` →
  falsy → same as `None`. Never crashes (`memory.py:49-61` non-destructive `_load`).

## Out of scope (explicit)

- The other 13 `analyze()` CLI call sites (no new flags); album coherence
  (`analyze_album`); creative `_KIND_SCORES`; the bridge apply / Class-3 path;
  net-new event-logging producers; `memory.py` changes (accessors already match);
  any push/merge to PR #13.

## End-to-end test plan (`tests/test_live_wire.py`)

Drive `analyze(str(base/"stems"), manifest)` on `dense_chorus_with_loops` (mirror
`test_governance.py:43-48`). Seed the store with REAL `ProjectMemory` writes.
- **(a) Byte-identical default:** `analyze(s,m)` == `analyze(s,m, memory_dir=None)`
  == `analyze(s,m, memory_dir=<empty fresh dir>)` — assert `mix_plan["next_pass"]`
  and `governance["governed_branches"]` identical, no `evidence`/`taste_adjustments`.
- **(b) History axis e2e:** seed via `ProjectMemory.record_pass(...)` so the latest
  record's `got_worse` implicates a `_MOVE_TARGET` score key AND its title is in
  `next_recommended` (record two passes — a better then a worse result — so
  `got_worse` is non-empty). Assert the implicated move is demoted / a
  `"Revert last pass"` surfaces in `analyze(..., memory_dir=seeded)["mix_plan"]["next_pass"]`
  vs the memoryless run.
- **(c) Taste axis e2e:** `ProjectMemory.add_feedback("too wide", ...)` ×2 (the ≥2
  recurrence threshold, `memory.py:144`) so `profile` contains
  `"tends to prefer narrower stereo images"`. Assert the governed winner shifts in
  `analyze(..., memory_dir=seeded).governance["governed_branches"]` vs memoryless.
- **(d) Prod surface reaches the wire:** `cowork.build_context(..., memory_dir=seeded)`
  then `run_command("suggest_next_pass"/"run_governance", ctx)` shows the same
  memory-driven change — proving `cowork.py:28` threads it (the real CLI
  `cowork --memory-dir` path is live).

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `45437d2` (clean, 28 ahead/0
  behind base). Default `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first + wire, green in isolation):** the `pipeline.py` param +
   construct-once threading + import, the one-arg `cowork.py:28` change, and the
   full `tests/test_live_wire.py`; passes its own new tests AND the existing 138
   standalone; regression 68/68.
2. **Commit 2 (optional):** docstring/comment polish on `analyze()`'s memory
   contract, or the low-priority `test_evidence_only_on_moved_candidates` cleanup.
   Skip if Commit-1 is clean.

## Regression-safety argument

- `regression.py:255` calls `analyze()` with no `memory_dir` → `_history=None`,
  `_taste=None` → both consumers hit their existing falsy-guard no-op → goldens
  unchanged → 68/68 holds. The new param is purely additive (default `None`); no
  existing test/CLI path passes memory. New behavior reachable ONLY via explicit
  non-empty `memory_dir`.

## Guardrails

- Build authority; the live wire is LOCAL file I/O of the app's own JSON store
  (same kind as `cli memory show` already does) — non-network, non-DAW, no
  subprocess, no `.logicx` write, no secrets. Deterministic. Truth-lock/kill-switch
  inviolability and the bounded taste/history effects from P-007/P-008 carry through.

---
_Confirmed P-009 on the user's "skate to where the puck" — the move that realizes
the P-007/P-008 learning-loop investment in production. Builder implements exactly
this; archivist clears on close._
