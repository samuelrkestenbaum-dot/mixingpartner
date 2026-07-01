# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-020
- **Title:** Session-flow discoverability — a `describe_session` command (phase-grouped, ordered)

## Why (the arc to the canonical target)

Arc P-019→P-023 to "Claude Cowork drives a full mixing session end-to-end."
P-019 made the loop closeable inside cowork (read/write symmetric, 33 commands).
But the 33 commands are exposed only as a flat/alphabetized catalog
(`list_commands`) — an agent can't tell the correct END-TO-END SEQUENCE from it.
P-020 adds a canonical, ordered, phase-grouped view so an agent can navigate:
intake → classify → diagnose → plan → checklist → validate → record → next-pass.
This is the discoverability step the end-to-end walkthrough (P-021) sits on.

## Authority

**Build / feature — in authority, additive, no new product decision.** A new
read-only command that returns a grouping over the EXISTING registry. Changes no
existing command's behavior. **Merge to default stays gated on the user's
explicit go; dev-branch commits covered by standing push-go.**

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/cowork.py` (additive)
1. Add a pure data structure `_SESSION_FLOW` (or similar): an ORDERED list of
   session phases, each `{phase, purpose, commands: [...]}`, mapping the REAL
   commands in `COMMANDS` into the canonical session order. Ground the phase order
   in the actual pipeline/session flow (README pipeline: source→identity→metrics→
   role→sections→depth→masking→doctrine→plan→checklist→next-pass; plus the P-019
   record + validate steps). Phases to cover (refine names to fit the real
   commands): **intake → classify → diagnose → plan → checklist/export →
   validate/govern → record-outcome → next-pass.**
2. Commands that are NOT part of the linear session flow (e.g. album coherence,
   memory-show, status/dashboard, list_commands itself, diagnostics) go in an
   explicit **`auxiliary`** bucket — do NOT force them into a phase they don't
   belong to. Honesty: the flow must reflect what the commands actually do.
3. Add a **`describe_session`** command whose handler returns
   `{"phases": [...ordered...], "auxiliary": [...]}` (pure, deterministic, JSON).
   Register in `COMMANDS` (count 33→34; update the count assertion — intended).
4. Do NOT change any existing command's behavior or output; do NOT touch
   `record_pass`/`_apply_history`/creative/governance/the ledger/`cli.py` plumbing
   beyond registering the new command. `list_commands` stays as the flat catalog.

### Tests — the binding guard. Test-first. (extend `tests/test_cowork.py` or new `tests/test_cowork_session_flow.py`)
- **Completeness INVARIANT (the load-bearing guard):** assert that EVERY key in
  `COMMANDS` appears **exactly once** across all phases + the `auxiliary` bucket
  (no command orphaned from the flow, none double-listed). This keeps the flow
  view honest and complete as commands are added — a new command with no phase
  fails this test. Also assert `describe_session` itself is accounted for.
- `describe_session` returns the phases in the declared canonical ORDER (assert the
  phase sequence), each phase non-empty (or auxiliary), each listed command is a
  real registry key.
- Determinism: two calls return identical output.
- Registry count 33→34 reflected (no stale 33).
- Existing cowork tests + P-008/P-009/P-018/P-019 tests pass UNCHANGED (only the
  registry-count assertion changes 33→34).

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network. Pure in-memory data + JSON.

## Constraints

- **≤2 commits.** Commit-1 (test-first, green in isolation): `_SESSION_FLOW` +
  `describe_session` + the completeness-invariant test + order/determinism tests.
  Commit-2 reserved only if a clean split emerges.
- **No external mutation** — no push / merge / deploy / secret. (Standing push-go
  covers dev-branch commits only.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **259 → 259+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held (additive read-only command →
  goldens untouched).
- Commit-1 green in isolation.
- **Completeness invariant proven load-bearing:** every `COMMANDS` key is covered
  exactly once in the flow/auxiliary partition; removing a command from the flow
  (or adding an uncovered one) fails the invariant test.
- `describe_session` returns the canonical ordered phases; deterministic; registry
  34, no stale 33. Safety grep clean; UI N/A; existing cowork + P-008/9/18/19
  tests green.

---
_Confirmed as active by the orchestrator-in-chief (P-020), second step of the arc
to the Claude-Cowork-usable final state. One packet at a time._
