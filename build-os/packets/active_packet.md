# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-04 ("Make the next
  packet: Cowork Registry MCP Adapter — Read/Plan Surface First… That is
  exactly the right next layer.").
- **ID / Title:** **P-051 — Cowork Registry MCP Adapter: Read/Plan Surface
  First**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `2b0ad1a` (= PR #28; the unmerged P-050 [`ec16ae6`+`74feeab`+`0e1009a`+
  `931a257`] sits on the branch ahead of it — this packet builds ON TOP of
  P-050 on the same dev branch; verify the base chain with
  `git merge-base` + `git log`).
- **Baseline to protect:** suite **1235** / regression **93/93** / the
  five producers + four sample trees + nine mode demos byte-stable / the
  plan-only, non-destructive boundary INVARIANT.

## Intent (the user's, verbatim)

Expose the existing `logic_mix_os/cowork.py` registry through an MCP
server. **This is a transport/adaptation packet, not a new mixing engine
and not a Logic execution backend.** The system is usable today as a
local-first mix-decision engine (stems + manifest → producer/mode analysis
→ mix plan → doctrine score → verdict → Logic action checklist → dashboard
→ next-pass recommendations); this packet makes that surface callable
through MCP.

## THE SAFETY DOCTRINE (the user's, verbatim — the invariant line)

> MCP can ask the system what it recommends.
> MCP cannot make Logic do it.

> Logic actions remain checklist / plan artifacts.
> Execution stays human/Cowork-in-the-loop.

## Architecture (the user's preferred shape + the orchestrator's binding
## environment decision)

The user's shape: MCP server → imports `logic_mix_os.cowork` in-process →
calls `describe_contract()` → auto-generates MCP tool schemas →
`build_context(...)` → `run_command(name, ctx, **params)` → returns JSON.
The contract stays drift-proof: cowork.py signatures → `describe_contract()`
→ MCP tool definitions. "Do not hand-write duplicated tool schemas if
`describe_contract()` can supply them."

**BINDING environment decision (orchestrator recon — the `mcp` SDK is NOT
installed; pyproject states "numpy is the only hard dependency, everything
else optional"). ZERO new hard dependency. TWO layers:**

1. **The pure-Python ADAPTER** (e.g. `logic_mix_os/cowork_mcp/adapter.py`
   or a single module — builder's call): the numpy-only, dependency-free
   heart. Generates MCP tool definitions from `describe_contract()`
   (name / description / inputSchema derived from the registry's
   `params` + `side_effect`); a `dispatch(tool_name, arguments)` that
   validates inputs, builds context (`build_context(stems, manifest,
   memory_dir, producer=…)`), runs the command (threading `mode` where the
   command analyzes), returns the JSON-serializable result + any produced
   artifact paths; the memory_dir GATE (below); the drift guard. **ALL 18
   proofs + 9 attacks live here, fully covered by the existing pytest
   suite** — no MCP SDK, no server process, no network required to test.
2. **The stdio SERVER shell** (e.g. `logic_mix_os/cowork_mcp/server.py`
   + `__main__.py` so `python -m logic_mix_os.cowork_mcp` serves): a
   MINIMAL self-contained JSON-RPC 2.0 over newline-delimited stdio MCP
   server (initialize handshake with protocolVersion + tools capability +
   serverInfo; tools/list; tools/call returning text content). Zero new
   deps. Unit-testable by driving it with request dicts (feed an
   `initialize` then `tools/list` then `tools/call`, assert the responses)
   — this is how "the MCP server starts" (proof 1) is proven
   deterministically without a live client. Confirm the MCP stdio
   framing/handshake shape against the current spec (the claude-code-guide
   agent is available for MCP protocol questions; do NOT depend on network
   for the build). An SDK-based transport is a trivial future swap — OUT
   OF SCOPE here.

## Scope (the user's)

A small MCP server/adapter exposing the existing Cowork commands.
Read/planning commands first-class. Side-effecting memory commands exposed
ONLY with an explicit `memory_dir`. The four side-effecting commands
(`record_mix_pass`, `update_taste_calibration`, `write_mix_decision`,
`override_track_identity`) MUST be clearly marked (side_effect label from
the registry) and gated — allowed ONLY as memory/history writes, NEVER DAW
writes.

Required behavior: list available Cowork commands; expose names / purposes
/ params / side-effect labels; run planning/analysis commands against a
`stems` path + optional `project_manifest.json` + optional `memory_dir` +
`producer` + `mode`; return JSON-serializable outputs; surface generated
artifact paths when commands produce them; preserve deterministic
behavior.

## Strict non-scope (the user's, verbatim — every line binding)

Do NOT control Logic. Do NOT call `osascript`. Do NOT invoke subprocess
against Logic. Do NOT write `.logicx`. Do NOT mutate DAW/project/session
files. Do NOT implement an execution backend. Do NOT add true
apply-to-DAW. Do NOT turn `logic_actions.applescript` into executable
behavior. Do NOT weaken review/gate semantics. Do NOT bypass existing
dry-run / plan-only boundaries. Do NOT make side-effecting memory commands
available without explicit `memory_dir`. Plus the Build OS standing lines:
no new hard dependency; existing CLI/cowork behavior byte-unchanged; no
tuning of producers/analyzers/scoring/governance; no merge without go.

## Required proof (the user's 18 — every one)

1. MCP server starts. 2. MCP tool list generated from
`describe_contract()`. 3. Tool params match Cowork function signatures.
4. Read/planning command works through MCP. 5. Producer selection works
through MCP. 6. Mode selection works through MCP. 7. Generated artifacts
reachable/reported. 8. Side-effecting commands marked clearly.
9. Side-effecting commands require explicit `memory_dir`. 10. No DAW/Logic
execution path exists. 11. No `osascript`. 12. No `.logicx` writes. 13. No
subprocess-to-Logic behavior. 14. No mutation of source stems. 15. Full
suite passes. 16. Regression passes. 17. Existing CLI/Cowork behavior
unchanged. 18. Contract-drift guard exists so the MCP schema cannot
silently diverge from the Cowork registry.

## Required adversarial reviewer attacks (any success = MUST-FIX)

1. run a tool without required stems path; 2. run a memory-writing tool
without `memory_dir`; 3. make MCP expose stale params not matching Cowork
signatures; 4. make MCP call a non-registry command; 5. find any DAW
execution surface; 6. find `osascript` or `.logicx` writes; 7. mutate
source audio; 8. bypass producer/mode validation; 9. get a side-effecting
command mislabeled as read-only.

## Acceptance bar (the user's, verbatim)

MCP wraps the Cowork registry · schemas are generated from the registry ·
planner commands work · producer/mode work · side effects are memory-only
and explicit · Logic execution remains impossible · existing behavior does
not drift.

## Orchestrator recon (binding on the builder)

- This is PRODUCT CODE (not profile-only) — the builder writes real Python
  under `logic_mix_os/`. That is expected and in-scope for this packet.
- Keep `cli.py` and `cowork.py` BYTE-UNCHANGED if possible (proof 17 +
  drift-minimization): prefer a NEW module/subpackage + a `python -m …`
  entrypoint over editing `cli.py`. If a thin additive `mcp-serve`
  subcommand is genuinely cleaner, it must be purely additive and the
  existing subcommands byte-unchanged — enumerate the delta.
- The drift guard (proof 18 / attack 3): a test that reconstructs the tool
  schemas from `describe_contract()` at test time and asserts the adapter
  exposes exactly those — so a cowork.py signature change either flows
  through automatically or fails loudly. The registry already derives
  params from real signatures via `inspect.signature`, so lean on that.
- The no-execution guards (proofs 10–14 / attacks 5–7): extend the
  house AST/safety-grep pattern (like `test_no_producer_names_in_the_fork_
  path_code`) to the new mcp module — assert it contains no `osascript`,
  no `subprocess`/`Popen`/`os.system`, no `.logicx`/audio-write path, and
  that dispatch reaches ONLY the cowork registry (attack 4). A behavioral
  test: a memory-write tool called without `memory_dir` returns a clean
  error, writes nothing (attack 2 / proof 9); source stems are
  byte-unchanged after any run (attack 7 / proof 14).
- Determinism: same inputs → same JSON out (proof, mirroring the CLI==
  library pin discipline).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the pure-Python adapter + its full test suite (schema gen
  from describe_contract, dispatch, producer/mode threading, the
  memory_dir gate, the drift guard, the no-execution AST/behavioral
  guards) — full suite green in isolation, zero new dependency, existing
  CLI/cowork byte-unchanged.
- **Commit-2:** the minimal stdio JSON-RPC server shell + `__main__`
  entrypoint + its handshake/tools-list/tools-call tests + a short
  docs/README "Cowork MCP" usage section (invocation, the tool surface,
  the safety line verbatim: "MCP can ask the system what it recommends.
  MCP cannot make Logic do it.") — full suite green.

## Why this is the right skate (the user's framing)

Moves the product from "powerful local engine" to "callable AI mixing
service surface" WITHOUT crossing the DAW-execution boundary prematurely.

---
_Set active by the orchestrator on the user's explicit go (2026-07-04).
One packet at a time: builder → qa + reviewer → archivist → receipt._
