# Receipt — P-051: Cowork Registry MCP Adapter — Read/Plan Surface First

- **Packet:** P-051 — Cowork Registry MCP Adapter: Read/Plan Surface First. THE
  FIRST packet that reaches past the plan-only boundary into an **external
  transport** — an MCP server wrapping the cowork registry — and it HELD THE
  LINE: **MCP can ask the system what it recommends; MCP cannot make Logic do
  it.** Also the FIRST CODE-BEARING integration packet since the producer arc
  (real Python under `logic_mix_os/`, not profile-only). The product moves from
  "powerful local engine" to "**callable AI mixing service surface**" WITHOUT
  crossing the DAW-execution boundary — because there is no execution surface
  anywhere in the package to cross (structurally absent, and the safety scan
  bites when one is injected).
- **User authority (verbatim go, 2026-07-04):** "Make the next packet: Cowork
  Registry MCP Adapter — Read/Plan Surface First… That is exactly the right next
  layer." The SAFETY DOCTRINE is the user's, verbatim and invariant: *MCP can ask
  the system what it recommends. MCP cannot make Logic do it. Logic actions remain
  checklist / plan artifacts. Execution stays human/Cowork-in-the-loop.*
- **Date:** 2026-07-04
- **Status:** CLOSED — qa **GREEN (13/13)** + reviewer **PASS (no must-fix; the
  no-execution boundary verified STRUCTURALLY ABSENT)**. Single-model review —
  **Codex unavailable.**

## Scope

**In (the confirmed packet spec — a transport/adaptation packet, NOT a new mixing
engine and NOT a Logic execution backend):**

1. **The pure-Python ADAPTER** — `logic_mix_os/cowork_mcp/adapter.py` (NEW) +
   `logic_mix_os/cowork_mcp/__init__.py` (NEW): `tool_definitions()` derives one
   MCP tool per cowork command (35) from `describe_contract()` — name /
   description / inputSchema built from the registry's params (which cowork
   derives from real `inspect.signature` signatures), NO hand-written per-command
   schema. `dispatch(tool_name, arguments)` GATES in order (unknown tool →
   missing stems → side-effecting-without-`memory_dir` → unknown producer →
   unknown mode) BEFORE any analyze/disk touch, threads producer + mode via
   `analyze(creative_mode=mode, producer=…)` → `build_context(result=…)` (so
   cowork.py stays byte-unchanged, no double-analyze), routes ONLY via
   `run_command` into the registry, returns `{result, artifacts}` with
   memory-store paths surfaced.
2. **The minimal stdio JSON-RPC 2.0 MCP SERVER shell** —
   `logic_mix_os/cowork_mcp/server.py` (NEW) + `logic_mix_os/cowork_mcp/__main__.py`
   (NEW, so `python -m logic_mix_os.cowork_mcp` serves): `initialize`
   (protocolVersion `2025-06-18` + tools capability + serverInfo) /
   `notifications/initialized` / `tools/list` / `tools/call` (text content +
   `isError`) / JSON-RPC error codes. `handle_message` is a PURE function so the
   handshake is unit-testable via StringIO.
3. **The full proof suite** — `tests/test_cowork_mcp.py` (NEW, the 18 proofs + 9
   attacks: schema-from-contract, drift guard, dispatch gating, producer/mode
   threading, the `memory_dir` gate, the no-execution AST/behavioral guards) +
   `tests/test_cowork_mcp_server.py` (NEW, the handshake / tools-list / tools-call
   tests + the parametrized no-exec scan grown to the new module files).
4. **`docs/COWORK_MCP.md`** (NEW) — invocation, the tool surface, and the full
   safety doctrine VERBATIM (incl. "MCP can ask the system what it recommends.
   MCP cannot make Logic do it.").
5. **`pyproject.toml`** — ONE additive line listing `"logic_mix_os.cowork_mcp"`
   in packages. A PACKAGING line only, **ZERO new dependency** — dependencies stay
   `["numpy>=1.21"]`.

**Explicitly out (the user's strict non-scope, verbatim — every line binding):**

- Do NOT control Logic. Do NOT call `osascript`. Do NOT invoke subprocess against
  Logic. Do NOT write `.logicx`. Do NOT mutate DAW/project/session files. Do NOT
  implement an execution backend / true apply-to-DAW. Do NOT turn
  `logic_actions.applescript` into executable behavior. Do NOT weaken review/gate
  semantics or bypass existing dry-run / plan-only boundaries. Do NOT make
  side-effecting memory commands available without explicit `memory_dir`.
- `cli.py` + `cowork.py` — **BYTE-UNCHANGED** (blob hashes identical to their
  `c3726f5` blobs); the five producers + four sample trees + nine mode demos
  untouched.
- No new hard dependency (the `mcp` SDK is absent; pyproject stays numpy-only).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `5d8dfe7` — "P-051 Commit-1: Cowork MCP adapter (schema-from-contract, gated
    dispatch) + full proof suite" — 3 files, +762 (NEW `cowork_mcp/__init__.py`
    +42, NEW `cowork_mcp/adapter.py` +292, NEW `tests/test_cowork_mcp.py` +428).
    **Commit-1 GREEN IN ISOLATION at 1264** — the ADAPTER + its suite only, the
    SERVER CONTENT ABSENT (verified). All 18 proofs + 9 attacks live here — no MCP
    SDK, no server process, no network required to test.
  - `5a04ae1` — "P-051 Commit-2: minimal stdio JSON-RPC MCP server shell +
    entrypoint + docs" — 5 files, +420 (NEW `cowork_mcp/server.py` +132, NEW
    `cowork_mcp/__main__.py` +18, NEW `tests/test_cowork_mcp_server.py` +176, NEW
    `docs/COWORK_MCP.md` +93, `pyproject.toml` +1 packaging line).
  - Combined: **8 files.** `cli.py` + `cowork.py` byte-unchanged; the pyproject
    delta is exactly one packages line; ZERO third-party import in
    `cowork_mcp/*.py` (stdlib + numpy only).
- **Parent:** `c3726f5` (set-active — "set P-051 … active — user go") on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1`, atop the UNMERGED P-050
  (`931a257` close → `0e1009a` → `74feeab` → `ec16ae6`).
- **Merge base for landing decisions:** `2b0ad1a` (= the PR #28 merge). Verified
  at close: `git merge-base HEAD 2b0ad1a` = `2b0ad1a`.
- **Push state:** PUSHED to the dev branch under the orchestrator's standing go
  **BEFORE qa/reviewer ran**. **NOT merged** — the P-051 merge is a user gate.
  **The dev branch now carries BOTH P-050 AND P-051 unmerged atop `2b0ad1a`.**

## The architecture (the key decisions)

- **Zero new hard dependency, two layers** — the orchestrator's binding decision
  after finding the `mcp` SDK absent and pyproject numpy-only. The adapter is the
  dependency-free heart (all 18 proofs + 9 attacks covered by pytest without a
  server process or network); the server is a self-contained stdio JSON-RPC 2.0
  shell. An SDK-based transport is a trivial FUTURE swap — out of scope here.
- **Schema from the contract, never hand-written** — `tool_definitions()`
  reconstructs the 35 tool schemas from `describe_contract()` at call time; the
  registry already derives params from real signatures via `inspect.signature`,
  so a cowork.py signature change either flows through automatically or fails the
  DRIFT GUARD loudly.
- **Gated dispatch, no dynamic callable** — `dispatch` validates in a fixed order
  and routes ONLY through `run_command` into the registry. No `getattr`/`eval`/
  `exec`/`__import__` reach; a non-registry name (`"__import__"`, `"os.system"`)
  is refused before any work (attack 4).
- **Producer + mode threaded correctly** — `analyze(creative_mode=mode,
  producer=…)` then `build_context(result=…)` (build_context skips re-analysis
  and ignores its own producer default — no double-analyze, no conflict), so
  cowork.py stays byte-unchanged.
- **The `memory_dir` GATE** — the four side-effecting commands (`record_mix_pass`,
  `update_taste_calibration`, `write_mix_decision`, `override_track_identity`) are
  marked from `cowork._SIDE_EFFECTS` (derived, not hand-listed) and allowed ONLY
  as memory/history writes with an explicit `memory_dir` — NEVER DAW writes.
- **Strict mode validation (the one genuine behavior choice)** — the adapter
  errors on an explicitly-wrong mode rather than falling through to the engine's
  silent `search_mode_fallback`; `mode=None` still flows to the engine default,
  so only an explicitly-bad mode is refused. Reviewer ACCEPTED (explicit > silent
  at a machine/agent transport boundary; consistent with unknown-producer
  handling; additive, engine byte-unchanged).

## ★★ THE NO-EXECUTION BOUNDARY — verified STRUCTURALLY ABSENT (the packet's reason for being)

- **Whole-package safety grep = ZERO hits** for `osascript` / `subprocess` /
  `Popen` / `os.system` / `os.exec` / `pty` / `.logicx` / `.applescript` / `.wav`
  / `.aif` / `eval` / `exec` / `__import__` / `getattr` / `open` / `socket` /
  `urllib` across `cowork_mcp/*.py`.
- **The scan is NON-VACUOUS:** the AST/token scan BITES an injected
  `subprocess.Popen(['osascript', …])` line (proven, not placement-faith); attack-4
  rejects `dispatch("__import__")` / `dispatch("os.system")`.
- **Reviewer's structural finding:** `write_artifacts` (the ONLY
  `.applescript`/artifact writer in the codebase) is a standalone CLI function no
  registry handler calls — so it is UNREACHABLE from any MCP tool call. The only
  tool-reachable disk writes are ProjectMemory JSON confined to the explicit
  `memory_dir`. Logic execution is not merely refused — it is absent.

## QA proof (GREEN — 13/13)

- **Suite:** 1235 → **1279 passed, 0 failed** (+29 at Commit-1 =
  `test_cowork_mcp.py`; +15 at Commit-2 = `test_cowork_mcp_server.py` 13 + the
  parametrized no-exec scan growing 2→4 module files); regression **93/93**;
  **Commit-1 iso 1264** (server content ABSENT verified). Arithmetic closes
  1235 + 31 + 13 = **1279**.
- **Scope:** `cli.py` + `cowork.py` blob-identical to `c3726f5`; the pyproject
  delta is exactly one packages line; ZERO third-party import in `cowork_mcp/*.py`
  (stdlib + numpy only).
- **The no-execution boundary (above):** whole-package grep ZERO hits; dispatch
  routes only via `run_command` (no dynamic callable); the AST/token scan bites an
  injected `subprocess.Popen(['osascript',…])`; attack-4 rejects
  `dispatch("__import__")` / `dispatch("os.system")`.
- **The gate:** a side-effecting tool without `memory_dir` → clean error, ZERO
  writes (fresh-cwd verified no store created); the marked side-effecting set ==
  `cowork._SIDE_EFFECTS` EXACTLY (no read command mislabeled — attack 9 defeated).
- **The drift guard (proof 18 / attack 3):** an injected synthetic registry
  command → `tool_definitions()` picks up EXACTLY its novel params (follows the
  registry, not a hardcode); CONTEXT_INPUTS subtracted before the equality check so
  they cannot mask cowork drift.
- **The server (proof 1):** in-memory handshake via StringIO + a REAL subprocess
  `python -m logic_mix_os.cowork_mcp` fed `initialize` + `tools/list` over stdin →
  exit 0, handshake + 35 tools, empty stderr.
- **Source integrity (proof 14 / attack 7):** source stems sha256-identical
  before/after a read + plan + memory-write run; existing cowork behavior
  byte-unchanged; safety grep 0.

## ★ The user's acceptance bar — all met (pinned evidence)

- **MCP wraps the Cowork registry ✓** — 35 tools, one per command, served over
  stdio.
- **schemas generated from the registry ✓** — from `describe_contract()`,
  drift-guarded (a synthetic command's novel params flow through).
- **planner commands work ✓** — read/planning first-class through dispatch.
- **producer / mode work ✓** — threaded via `analyze(creative_mode=…,
  producer=…)` → `build_context(result=…)`, no double-analyze.
- **side effects memory-only + explicit ✓** — `memory_dir`-gated, derived from
  `_SIDE_EFFECTS`; without it, a clean error and zero writes.
- **Logic execution remains impossible ✓** — structurally absent; the scan bites
  an injected execution line.
- **existing behavior does not drift ✓** — `cli.py`/`cowork.py` byte-unchanged;
  the existing suite green; regression 93/93.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- **No-execution boundary: PASS and STRUCTURALLY ABSENT** — `write_artifacts`
  (the only artifact writer) is a standalone CLI function no registry handler
  calls, unreachable from any MCP tool; the only tool-reachable disk writes are
  ProjectMemory JSON confined to the explicit `memory_dir`.
- **The one genuine behavior choice — strict mode validation vs the engine's
  silent `search_mode_fallback`: RECOMMEND ACCEPT** (explicit > silent at a
  machine/agent transport boundary; consistent with unknown-producer handling;
  `mode=None` still flows to the engine default — only an explicitly-bad mode is
  refused; additive, engine byte-unchanged). Optional polish only: the error could
  suggest "omit mode for the profile default."
- **`override_track_identity` gated behind `memory_dir`:** contract-mandated (one
  of the four named side-effecting commands), correct.
- **The drift guard is load-bearing; producer/mode threading correct**
  (`build_context(result=…)` skips re-analysis, ignores its own producer default —
  no conflict); zero new dependency; the docs carry the full safety doctrine
  verbatim without overclaim.

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, recorded not fixed (P-051, non-blocking):**
  1. **The thin server's deliberate protocol gaps** — it pins its own
     `protocolVersion` (no client negotiation), no `structuredContent`, no
     JSON-RPC batch. Acceptable for a shell explicitly framed as a future SDK swap.
  2. **The pre-existing stale README "32 commands"** (the registry is 35) —
     GENUINE residue, a later docs cleanup, OUT of this packet's scope.
  3. **The awareness note:** a read/plan tool called WITH a `memory_dir` will
     mkdir it via `ProjectMemory.__init__` though it writes no history —
     pre-existing engine behavior, confined to the explicit path, NOT a DAW write,
     NOT reported as an artifact.
  4. **The optional strict-mode error-message polish** — suggest omitting mode for
     the default.
- All prior standing notes RETAINED (the ★★ groove-carrier trajectory
  watch-item, the P-049 sample-pin micro-hardening, the CLA sha256-self-pin-
  on-sixth-producer note, the CLA product-surface refresh candidate) and the three
  named lessons.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge.** The dev branch carries BOTH
  P-050 (`ec16ae6` + `74feeab` + `0e1009a` + `931a257`) AND P-051 (`c3726f5` +
  `5d8dfe7` + `5a04ae1` + this close commit) atop `2b0ad1a` (= PR #28). A single
  merge PR would land BOTH — the fifth producer AND the MCP surface. The commits
  are pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **NEW STANDING SAFETY LINE (recorded):** "MCP can ask the system what it
  recommends; MCP cannot make Logic do it — Logic actions remain checklist/plan
  artifacts; execution stays human/Cowork-in-the-loop." The apply-to-Logic backend
  is a FUTURE, EXPLICITLY re-gated packet — never auto.
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open directions (ALL
  user-gated): the merge · a real MCP-SDK transport swap (optional-extra) · the
  apply-to-Logic backend (future, explicitly re-gated) · a CLA product-surface
  refresh · the future-analyzer candidates from Eno's deferrals · quincy/halee
  authored dropout reach · a sixth producer · the README 32→35 + sample-pin
  micro-hardening cleanups · anything else the user calls. Do NOT open anything
  blind.

---
_Closed by the archivist (2026-07-04). qa GREEN (1279 / 93/93 / Commit-1 iso 1264
[server content absent] / arithmetic 1235+31+13=1279 / the no-execution scan bites
an injected osascript-Popen / dispatch routes only via run_command / the memory_dir
gate zero-writes without it / the drift guard follows a synthetic command / a REAL
`python -m logic_mix_os.cowork_mcp` subprocess handshakes + serves 35 tools, empty
stderr / source stems sha256-stable / safety grep 0) + reviewer PASS (no must-fix;
single-model — Codex unavailable; the no-execution boundary verified STRUCTURALLY
ABSENT — write_artifacts unreachable from any tool). The plan-only → callable-surface
milestone is crossed WITHOUT crossing the DAW-execution boundary: the cowork registry
(35 commands) is reachable through a zero-dependency stdio MCP server, and Logic
execution is not merely refused but absent._
</content>
</invoke>
