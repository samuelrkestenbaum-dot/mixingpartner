# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-019
- **Title:** Close the learning loop INSIDE the cowork surface — a `record_mix_pass` command

## Why (the arc to the canonical target)

Canonical target: Logic Mix OS as a tool Claude Cowork can drive **end-to-end**
in a Logic Pro mixing session (plan-only v1; the agent/human executes). The
orchestrator's gap survey: the 32-command `cowork` surface is coherent for the
FORWARD half (intake → classify → diagnose → plan → checklist → validate →
`suggest_next_pass`), and the READ side of the learning loop is live through
`cowork` (`build_context(memory_dir=...)` → `analyze(memory_dir=...)` threads
history→next-pass and taste→governance, P-009). **But the cowork registry has NO
command to RECORD a pass outcome** — `record_pass` / the P-018 `--reverted`
confirmed-outcome signal is reachable only via the SEPARATE `memory-record` CLI
verb. So an agent driving through `cowork` can read the next pass but cannot
close the loop (record outcome → see next pass change) without leaving the
surface. This packet is FIRST in the arc (P-019→P-023) because it makes the
product's whole learning loop **closeable by an agent**; everything downstream
(session-flow discoverability, end-to-end walkthrough, MCP transport) assumes it.

## Authority

**Build / feature — in authority, no new product decision.** Reuses the
already-live `record_pass`/`_apply_history` channel (P-008/P-009/P-018). Additive
to the cowork registry. The MCP-vs-raw-CLI fork is deliberately sequenced LAST
(P-023, user-gated) — NOT this packet. **Merge to default stays gated on the
user's explicit go; dev-branch commits covered by standing push-go.**

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/cowork.py` (additive)
1. Add a **`record_mix_pass`** command to the cowork `COMMANDS` registry. Its
   handler records a pass outcome on the LIVE history channel via the context's
   memory: `ctx["memory"].record_pass(name, result, reverted=...)` — passing
   through the P-018 `reverted` ground-truth flag (opt-in, default False) — and
   returns the record JSON. Mirror the existing `_write_mix_decision` handler's
   shape and its clean error when no `memory_dir` is configured (the loop
   requires a memory dir; error clearly, don't crash).
2. Register it in `COMMANDS`; the command count goes 32 → 33. Update any
   list-commands / registry-count assertions accordingly (find them; do not leave
   a stale 32).
3. Wire the params the cowork invocation path already uses (`--params '{...}'` →
   the handler kwargs), including `name` (the pass name) and `reverted: bool`.
   Do NOT change `cli.py`'s `_run_cowork` plumbing beyond what registering a new
   command requires; do NOT touch `memory-record` (it stays as the standalone
   verb too).

Do NOT touch: `record_pass`/`_apply_history` internals (reuse as-is); the
`_KIND_SCORES`/creative/governance; the dead ledger (`write_mix_decision` stays
as-is — do NOT route the loop through it); `analyze()`'s memory wiring; any
push/merge. The dry-run bridge and real-Logic execution stay OUT (env-bound).

### Tests — the binding guard (this axis isn't golden-covered). Test-first.
New `tests/test_cowork_record.py` (or extend an existing cowork test):
- **Unit:** `run_command("record_mix_pass", ctx, name=..., reverted=True)` records
  a pass (asserts the stored `mix_pass_history.json` gets the pass with the
  `reverted` flag); the no-`memory_dir` path errors cleanly (mirrors
  `_write_mix_decision`); default `reverted=False` omits the flag (byte-identical
  stored history vs the standalone `memory-record`).
- **Liveness (no re-run — the P-016/P-018 lesson):** drive the loop THROUGH the
  cowork surface — `run_command("record_mix_pass", ctx, reverted=True)`, then a
  FRESH `build_context(memory_dir=...)` → `run_command("suggest_next_pass")` — and
  assert the confirmed "Revert last pass" item surfaces in the next-pass output.
  Must FAIL if the record isn't actually persisted/threaded (e.g. if the handler
  doesn't hit the live channel) and PASS at tip — proving the loop closes
  *through the cowork surface*, not just in unit-land.
- Existing cowork tests + P-008 `test_next_pass_history.py` + P-009
  `test_live_wire.py` + P-018 `test_confirmed_revert*.py` pass UNCHANGED (do not
  edit them; only update a registry-count assertion 32→33 if one exists — that is
  an intended, not a silent, change).

Fake adapters only — no real DAW / Logic / AppleScript / subprocess / `.logicx`
write / network. Memory is local JSON only.

## Constraints

- **≤2 commits.** Commit-1 (test-first, green in isolation): the `record_mix_pass`
  handler + registry + unit tests. Commit-2 (same packet): the no-re-run liveness
  test proving the loop closes through cowork (fails without the wiring, passes at
  tip). If it all lands cleanly in one commit, that's fine — but Commit-1 must be
  green in isolation.
- **No external mutation** — no push / merge / deploy / secret. (Standing push-go
  covers dev-branch commits only.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **253 → 253+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held (opt-in memory path → goldens
  untouched; byte-identical default).
- Commit-1 green in isolation.
- **Liveness proven load-bearing:** the no-re-run test (record via cowork → fresh
  context → `suggest_next_pass` shows the confirmed revert) FAILS without the new
  command's live wiring and PASSES at tip. The loop is closeable ENTIRELY within
  the cowork surface.
- Registry count 32→33 reflected; no stale count. Safety grep clean; UI N/A;
  P-008/P-009/P-018/existing-cowork tests green.

---
_Confirmed as active by the orchestrator-in-chief (P-019), first packet of the
arc to the Claude-Cowork-usable final state. One packet at a time._
