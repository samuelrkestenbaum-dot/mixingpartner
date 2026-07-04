# Cowork MCP

`logic_mix_os.cowork_mcp` exposes the existing Cowork command registry
(`logic_mix_os/cowork.py`) through the **Model Context Protocol (MCP)** as a
callable AI mixing-decision surface.

> **MCP can ask the system what it recommends.**
> **MCP cannot make Logic do it.**
>
> **Logic actions remain checklist / plan artifacts.**
> **Execution stays human/Cowork-in-the-loop.**

This is a **transport/adaptation** layer, not a new mixing engine and not a
Logic execution backend. It never drives a DAW, never writes a Logic session or
an audio file, and carries no execution backend. The only files any tool can
touch are the memory/history store under an **explicit `memory_dir`**, and only
for the four commands the registry declares as side-effecting.

## Invocation

Zero new dependency (stdlib + numpy only). Serve over newline-delimited stdio
(JSON-RPC 2.0):

```
python -m logic_mix_os.cowork_mcp
```

The server speaks the stable core of MCP:

| Method | Result |
| --- | --- |
| `initialize` | `{protocolVersion, capabilities: {tools: {}}, serverInfo: {name: "logic-mix-os-cowork", version}}` |
| `notifications/initialized` | (notification — no response) |
| `tools/list` | `{tools: [...]}` — the tool definitions |
| `tools/call` | `{content: [{type: "text", text: <json>}], isError}` |

Errors follow JSON-RPC 2.0: unknown method `-32601`, parse error `-32700`,
invalid params `-32602`. A **handled** adapter error (e.g. a missing `stems`
path, or a side-effecting tool without a `memory_dir`) is returned as
`isError: true` with the message in the text content — never a transport crash.

## The tool surface (derived from the registry)

Tool definitions are **generated from `cowork.describe_contract()`**, whose
per-command `params` are themselves derived from the real handler signatures via
`inspect.signature`. Nothing is hand-written per command, so the MCP schema can
never silently diverge from the Cowork surface — a drift guard test reconstructs
the schema from the contract and asserts they match exactly.

Each tool is `{name, description, inputSchema}`:

- **`name`** — the Cowork command name (one tool per registry command).
- **`description`** — the command's purpose plus an honest side-effect label:
  read/plan commands are marked `[read-only]`; the four side-effecting commands
  carry their exact `side_effect` classification and the memory-only boundary.
- **`inputSchema`** — a JSON-Schema object combining the command's own params
  with the shared context inputs:
  - `stems` (**required**) — path to the folder of exported stems;
  - `manifest` — path to `project_manifest.json` (optional);
  - `memory_dir` — path to the project memory store (**required** for the four
    side-effecting commands, optional/history-aware for reads);
  - `producer` — producer profile name (default `halee_ramone`);
  - `mode` — a creative search mode from that producer's `search_modes`.

Read/planning commands (identity, sections, masking, depth, mix plan, doctrine
scores, next-pass, creative, governance, checklist, the self-describing
`describe_contract` / `describe_session`, …) run against a `stems` path and
return JSON. The four **side-effecting** commands write **only** to the explicit
`memory_dir` store:

| Command | `side_effect` | Writes |
| --- | --- | --- |
| `record_mix_pass` | `writes:history(live)` | `mix_pass_history.json` |
| `update_taste_calibration` | `writes:taste(live)` | `taste_profile.json` |
| `write_mix_decision` | `writes:ledger(dead)` | `decision_ledger.json` |
| `override_track_identity` | `mutates:session` | (in-session only, no file) |

Calling any of these without an explicit `memory_dir` is refused with a clean
error, and nothing is analysed or written.

## Safety boundary

- No `osascript`, no shelling out, no `.logicx` writes, no DAW/session/audio
  mutation, no execution backend — anywhere in this module (guarded by a
  source-scan test).
- Dispatch routes **only** into the Cowork `COMMANDS` registry; an unknown tool
  name is a clean error.
- Source stems are byte-unchanged after any run.
- Same inputs produce the same JSON out (deterministic).

An SDK-based MCP transport is a trivial future swap; the adapter
(`logic_mix_os/cowork_mcp/adapter.py`) is the stable, dependency-free heart and
the server shell (`server.py`) is intentionally thin.
