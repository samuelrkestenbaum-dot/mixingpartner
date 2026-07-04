# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-04 ("Merge P-050 +
  P-051 together now. Then do the real end-to-end MCP client test… The
  next skate is: P-052 — Real End-to-End MCP Client Session."). The
  P-050+P-051 bundle merged FIRST as PR #29 → default tip `f6cc9b7`.
- **ID / Title:** **P-052 — Real End-to-End MCP Client Session**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `f6cc9b7` (= PR #29 merge — the branch was fast-forwarded to it; verify
  with `git merge-base`).
- **Baseline to protect:** suite **1279** / regression **93/93** / the
  five producers + four sample trees + nine mode demos byte-stable / the
  MCP surface (`cowork_mcp/`), `cli.py`, `cowork.py` byte-stable — this is
  a PROOF packet: prove the real product path, do NOT change product
  runtime code.

## Intent (the user's, verbatim)

P-051 proved the server in controlled tests (in-memory `handle_message` +
one smoke subprocess). **P-052 proves the ACTUAL PRODUCT PATH:**

> Claude/Cowork MCP client
> → stdio MCP server
> → Cowork registry
> → stems + manifest
> → producer/mode plan
> → artifacts
> → no DAW execution

"That is the real 'does this actually work?' moment." SDK swap is optional
polish; apply-to-Logic is a future re-gated architecture. The
product-facing next step is: **drive a real session through the MCP
surface.**

## THE SAFETY DOCTRINE (standing, preserved — binding)

> MCP can ask what the system recommends; MCP cannot make Logic do it.
> The product is callable as a planning/recommendation surface, not a DAW
> execution surface.

## Scope

Build a **real MCP client harness** and a **committed end-to-end session
test** that drives the actual product path — a genuine client process
speaking JSON-RPC 2.0 over the REAL stdio pipes of a spawned
`python -m logic_mix_os.cowork_mcp` server subprocess (NOT the in-memory
`handle_message` shortcut P-051 already covers; NOT a mock). The client is
hand-rolled, **zero new dependency** (stdlib subprocess + json over the
child's stdin/stdout), matching the project's numpy-only discipline. Note:
spawning the MCP SERVER (a Python process) is the product path and is
explicitly fine — the non-scope forbids subprocess-to-LOGIC, not running
the server.

The end-to-end session drives a realistic multi-command flow over the wire
(the `describe_session` `_SESSION_FLOW`: intake → classify → diagnose →
plan → checklist → validate → record-outcome → next-pass, or a faithful
realistic subset) against a REAL fixture (`fixtures/dense_chorus_with_loops`
or another shipped fixture — stems + manifest), with a real producer
(showcase `chris_lord_alge` and at least one other for the attributable
difference) and a real mode.

Optionally (docs, recommended): a `docs/COWORK_MCP.md` addition (or a new
snippet) showing how an ACTUAL external MCP client (Claude Desktop /
Cowork) is configured to launch the server — the `{command, args}` MCP
server-config JSON — so the "real client" story is documented for product
use. No overclaim; the safety line verbatim.

## Required proof (the real product path)

1. A real hand-rolled MCP client spawns `python -m logic_mix_os.cowork_mcp`
   as a subprocess and completes the `initialize` handshake over the REAL
   stdio pipes (protocolVersion 2025-06-18, serverInfo, tools capability).
2. `tools/list` over the wire returns the 35 tools with their schemas.
3. A full realistic session sequence (several `tools/call` in order) runs
   over the wire against a real fixture and returns real,
   JSON-deserializable results (a real producer/mode plan + verdict +
   checklist + next-pass).
4. Producer selection works over the wire — `chris_lord_alge` vs another
   producer on identical stems → attributable difference in the returned
   plan.
5. Mode selection works over the wire — a creative command with a mode →
   reflected in the result.
6. Artifacts/plan/checklist are reachable and reported over the wire.
7. The memory-write path over the wire: a side-effecting command WITHOUT
   `memory_dir` → clean error over the wire (nothing written); WITH an
   explicit `memory_dir` → writes to the MEMORY STORE (JSON), and the
   store is a memory dir, never a DAW/session file.
8. Across the whole REAL path: no `osascript`, no `.logicx`, no DAW
   execution; the source stems are byte-unchanged (sha256 before/after the
   whole session); the server subprocess exits cleanly (exit 0, empty or
   benign stderr).
9. Deterministic: the same session twice → the same plan results.
10. Full suite passes; regression passes; ZERO new dependency; ZERO change
    to product runtime code (`cowork_mcp/`, `cli.py`, `cowork.py`, the
    engine — byte-unchanged); the five producers + trees + demos untouched.

## Required adversarial reviewer attacks (any success = MUST-FIX)

1. find any DAW/Logic execution reachable through the real client path;
2. find `osascript` / `.logicx` / subprocess-to-Logic anywhere the session
   touches; 3. mutate source audio across a real session; 4. get a
   side-effecting command to write without `memory_dir` over the wire;
5. make the end-to-end test pass without actually spawning the server
   subprocess (i.e. prove it's a REAL over-the-wire test, not a disguised
   in-process call); 6. find a hidden new dependency; 7. find product
   runtime drift (cowork_mcp/cli/cowork/engine changed).

## Acceptance bar

A real client process drives a real server subprocess over stdio · a
realistic multi-command session returns real producer/mode plans +
artifacts · producer/mode work over the wire · the memory gate holds over
the wire · no DAW execution anywhere on the real path · source stems
immutable · zero new dependency · zero product-runtime drift · the safety
doctrine preserved verbatim in any docs.

## Orchestrator recon (binding on the builder)

- This is a TEST + (optional) DOCS packet. Do NOT modify `cowork_mcp/`,
  `cli.py`, `cowork.py`, or any engine file (if a real bug in the surface
  is discovered → STOP and report; do not fix silently — that would be its
  own packet).
- The client MUST speak over the child process's real stdin/stdout pipes
  (`subprocess.Popen(..., stdin=PIPE, stdout=PIPE, text=True)`, write a
  JSON-RPC line + flush, read a response line) — NOT `handle_message`
  in-process (that's P-051's coverage). Attack 5 is the guard that this is
  genuinely over-the-wire.
- Robustness: bounded timeouts, clean teardown (terminate the child,
  drain pipes), deterministic — must not flake or hang the suite. Mirror
  the existing subprocess discipline (`tests/test_producer_cli.py`, the
  P-051 smoke).
- A small reusable client helper (e.g. `tests/_mcp_client.py` or a
  `tests/mcp_e2e/` helper) is fine; keep it minimal and stdlib-only.
- Determinism/no-DAW/stems-immutability get first-class assertions (the
  packet's whole point is the REAL path holding the boundary).

## Non-scope (binding)

No MCP SDK / SDK transport swap. No apply-to-Logic. No DAW execution
backend. No `osascript`. No `.logicx`. No product runtime changes
(`cowork_mcp`/`cli`/`cowork`/engine byte-unchanged). No new producers /
analyzers / move families. No new hard dependency. No safety/governance
changes. No merge until qa + reviewer dual-green.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the real MCP client harness + the end-to-end session test
  (all 10 proofs + the 7 attacks it can cover) — full suite green in
  isolation.
- **Commit-2 (optional):** the docs snippet (how a real Cowork/Claude MCP
  client launches the server; the safety line verbatim) — zero collection
  change. If no docs, one commit is fine.

---
_Set active by the orchestrator on the user's explicit go (2026-07-04),
after the PR #29 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
