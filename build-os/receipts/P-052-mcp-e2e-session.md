# Receipt — P-052: Real End-to-End MCP Client Session

- **Packet:** P-052 — Real End-to-End MCP Client Session. THE PROOF packet that
  answers the "does this actually work?" moment. P-051 proved the server in
  controlled tests (in-memory `handle_message` + one smoke subprocess); **P-052
  proves the ACTUAL PRODUCT PATH** — a real client PROCESS spawns
  `python -m logic_mix_os.cowork_mcp` as a subprocess and drives a full
  producer/mode Cowork session over the child's REAL stdio pipes, boundary
  intact, with **ZERO product-runtime change**. The standing safety line now
  holds across the REAL path, not just controlled tests: **MCP can ask what the
  system recommends; MCP cannot make Logic do it.**
- **User authority (verbatim go, 2026-07-04):** "Merge P-050 + P-051 together
  now. Then do the real end-to-end MCP client test… The next skate is: P-052 —
  Real End-to-End MCP Client Session." The P-050+P-051 bundle merged FIRST as
  **PR #29** (merge commit `f6cc9b7`, the current default tip and this packet's
  merge base), then this packet was opened.
- **Date:** 2026-07-04
- **Status:** CLOSED — qa **GREEN (15/15)** + reviewer **PASS (no must-fix; the
  over-the-wire proof genuine, the no-DAW boundary held across the real path)**.
  Single-model review — **Codex unavailable.**

## Scope

**In (a TEST + DOCS packet — NOT a new mixing engine, NOT a Logic execution
backend, NOT any product-runtime change):**

1. **The real MCP client harness** — `tests/_mcp_client.py` (NEW, stdlib-only):
   spawns `python -m logic_mix_os.cowork_mcp` via
   `subprocess.Popen([sys.executable, "-m", …], stdin/stdout/stderr=PIPE,
   text=True)` and speaks JSON-RPC 2.0 over the child's REAL pipes. Two daemon
   pump threads drain stdout (bounded queue) + stderr so a full OS pipe buffer
   can't deadlock; every read has a 30s bounded timeout (a hung server →
   terminate + raise); a context manager guarantees child teardown (no orphans).
2. **The over-the-wire session test** — `tests/test_mcp_e2e_session.py` (NEW, 12
   tests): drives a REAL nine-command Cowork session against
   `fixtures/dense_chorus_with_loops` — intake_project → detect_track_identities
   → classify_tracks → detect_masking → generate_mix_plan → score_mix →
   render_logic_checklist → validate_mix_pass → suggest_next_pass, each
   `isError:false` with a real, JSON-deserialized result. Determinism, no-DAW,
   stems-immutability, and the memory gate get first-class assertions.
3. **`docs/COWORK_MCP.md`** (+38) — a "Connecting a real MCP client" section:
   the `{command, args}` `mcpServers` server-config JSON an external host uses to
   launch the server, a note that reads/plans are free while the four
   side-effecting commands need an explicit `memory_dir`, the safety line
   VERBATIM, and an explicit no-apply-to-Logic disclaimer. Docs only, zero
   collection change.

**Explicitly out (binding non-scope):**

- No MCP SDK / SDK transport swap. No apply-to-Logic. No DAW execution backend.
  No `osascript`. No `.logicx`. No subprocess-to-Logic (spawning the SERVER — a
  Python process — is the product path and is explicitly fine; the non-scope
  forbids subprocess-to-LOGIC, not running the server).
- **ZERO product-runtime change:** `cowork_mcp/`, `cli.py`, `cowork.py`, the
  whole engine — byte-unchanged. `git diff f6cc9b7..172150a --
  logic-mix-os/logic_mix_os/` is EMPTY. `pyproject.toml` untouched (deps stay
  `["numpy>=1.21"]`). The five producers + four sample trees + nine mode demos
  byte-unchanged. No new hard dependency (the harness is stdlib-only).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets. If a
  real bug in the surface had surfaced, the rule was STOP-and-report (its own
  packet), never a silent fix — none was needed.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `987ab18` — "P-052 Commit-1: real end-to-end MCP client harness +
    over-the-wire session test" — 2 NEW files (`tests/_mcp_client.py` +236,
    `tests/test_mcp_e2e_session.py` +343). **Commit-1 GREEN IN ISOLATION at
    1291** — the harness + its 12-test session suite; all 10 contract proofs +
    the 7 attacks it can cover live here. The harness collects 0 tests.
  - `172150a` — "P-052 Commit-2: docs — connecting a real MCP client
    (server-config + safety line)" — 1 file (`docs/COWORK_MCP.md` +38). Docs
    only; ZERO collection change (C1 == HEAD node-ids).
  - Combined: exactly **3 files** touched under `logic-mix-os/`. ZERO
    product-runtime change.
- **Parent:** `5921e24` (set-active — "set P-052 … active — user go") on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base:** `f6cc9b7` (= the PR #29 merge — the P-050+P-051 bundle).
  Verified at close: `git merge-base HEAD f6cc9b7` = `f6cc9b7`.
- **Push state:** PUSHED to the dev branch under the orchestrator's standing go
  **BEFORE qa/reviewer ran** (both gates validated the final SHAs). **NOT
  merged** — the P-052 merge is a user gate.

## The architecture (the harness — production-grade)

- **Genuinely over-the-wire, no in-process shortcut** — `tests/_mcp_client.py`
  imports ONLY stdlib (`subprocess`, `json`, `threading`, `queue`, `sys`); it
  never imports `logic_mix_os` / the adapter / the server / `handle_message`.
  The ONLY path from a request to a result is the child process's real pipes.
- **Deadlock-proof** — two daemon pump threads drain the child's stdout (into a
  bounded queue) and stderr, so a full OS pipe buffer can never deadlock the
  test.
- **Fail-fast** — every read carries a 30s bounded timeout; a hung server →
  terminate the child + raise (never hangs the suite).
- **Guaranteed teardown** — a context manager tears the child down on every exit
  path, so a failing test never leaks a process (ps clean after the suite).
- **Reusable, minimal** — `request()` / `notify()` / `call_tool()` over the
  pipes; mirrors the project's existing subprocess discipline
  (`tests/test_producer_cli.py`, the P-051 smoke).

## QA proof (GREEN — 15/15)

- **Suite:** 1279 → **1291 passed, 0 failed** (+12, all
  `tests/test_mcp_e2e_session.py`; the harness `tests/_mcp_client.py` collects
  0); regression **93/93**; **Commit-1 iso 1291** (the whole packet's test
  content is Commit-1; Commit-2 is docs-only so HEAD == C1 collection).
- **Scope integrity:** `git diff f6cc9b7..172150a --
  logic-mix-os/logic_mix_os/` EMPTY — the whole engine + `cowork_mcp/` +
  `cli.py` + `cowork.py` byte-identical; `pyproject.toml` untouched (deps stay
  `["numpy>=1.21"]`); the five producers + four sample trees + nine mode demos
  byte-unchanged. ZERO new dependency (harness stdlib-only).

### The crux — genuinely over-the-wire (attack 5)

- The harness imports ONLY stdlib; the only request→result path is the child's
  pipes — no in-process shortcut. **Non-vacuous:** a bogus module → no handshake
  (EOF); killing the child mid-session → the next request RAISES
  (`BrokenPipeError` / `MCPClientError`) — impossible for a disguised in-process
  call. `child pid != os.getpid()`.

### Producer + mode over the wire

- **Producer (proof 4):** `score_mix` on identical dense stems →
  `chris_lord_alge` **59.6** / `timbaland` **52.6** / `halee_ramone` **70.7** —
  three distinct values, each `result.producer.name` correctly attributed (qa
  independently reproduced the exact numbers). The tests pin inequality +
  attribution — robust to future re-tuning, still red if threading breaks.
- **Mode (proof 5):** `run_creative_engine` `chris_lord_alge` default
  `search_mode=commit_and_slam`; `mode=front_and_center` →
  `search_mode=front_and_center`, result differs (a deliberately non-default
  mode, so the difference is load-bearing).

### The memory gate over the wire (attack 4 / proof 7)

- A side-effecting command WITHOUT `memory_dir` → `isError:true`, `"memory_dir"`
  in the message, nothing written; from a fresh empty cwd the refused write
  leaves cwd EMPTY (`iterdir() == []`). WITH `memory_dir` → writes only
  `mix_pass_history.json` UNDER that store (a `.json`, surfaced in artifacts) —
  a memory dir, never a DAW/session file.

### No-DAW + stems immutable (attacks 1,2,3 / proof 8)

- sha256 of the fixture stem tree identical before/after a full session
  including a memory write; only `.json` under the memory store produced; the
  ONLY subprocess anywhere is the server itself; the server exits **rc 0 with
  empty stderr** on stdin close. No orphaned processes after the suite (ps
  clean).

### Determinism + no new dependency (proof 9 / proof 10)

- A plan command run twice over the wire → identical JSON. Harness stdlib-only —
  ZERO new dependency. Docs carry the `{command, args}` server-config JSON + the
  safety line VERBATIM + an explicit no-apply-to-Logic disclaimer.

## ★ The user's acceptance bar — all met

- a real client process drives a real server subprocess over stdio ✓
- a realistic multi-command session returns real producer/mode plans +
  artifacts ✓
- producer/mode work over the wire ✓
- the memory gate holds over the wire ✓
- no DAW execution anywhere on the real path ✓
- source stems immutable ✓
- zero new dependency ✓
- zero product-runtime drift ✓
- the safety doctrine preserved verbatim in docs ✓

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- **The harness judged PRODUCTION-GRADE** — deadlock-avoidance via the pump
  threads, fail-fast bounded timeouts, guaranteed teardown.
- **The inequality-not-float assertions judged the RIGHT call** — they pin the
  attributable difference + attribution without pinning brittle exact floats, so
  they stay green under future re-tuning yet go red if producer/mode threading
  breaks.
- **The over-the-wire proof judged genuine** and the no-DAW boundary judged held
  across the real path; the docs judged honest, no overclaim.

## Residue (carried to `build-os/memory/residue.md`) — non-blocking

1. **`test_proof07`'s `assert not (tmp_path/"should_not_exist").exists()` is
   cosmetic** — a never-created path is trivially absent; the REAL "nothing
   written" proof is `test_attack4` (fresh cwd, `iterdir() == []`). Harmless.
2. **proof09 determinism is within one server process**, not across two
   independently spawned servers (cross-process is implicitly covered by every
   test getting a fresh server). Acceptable.
3. **Docs use `"command": "python"` while the harness uses `sys.executable`** —
   `python` is the conventional MCP-config example form, honest/usable; optional
   future nicety.
4. **The killed-child exception surface** appeared as `BrokenPipeError` in qa's
   probe vs the builder's `MCPClientError` — same guarantee, environment-
   dependent surface; non-blocking.
- All prior standing notes RETAINED (the ★★ groove-carrier trajectory
  watch-item, the P-049 sample-pin micro-hardening, the CLA
  sha256-self-pin-on-sixth-producer note, the CLA product-surface refresh
  candidate, the README 32→35 cleanup) and the three named lessons.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-052.** The dev branch carries P-052
  (`5921e24` + `987ab18` + `172150a` + this close commit) atop `f6cc9b7` (= PR
  #29). The commits are pushed to the dev branch (standing go, pre-gates); NOT
  merged; no deploy/publish/secrets touched.
- **THE SAFETY LINE HOLDS ACROSS THE REAL PATH NOW** — not just controlled
  tests: "MCP can ask what the system recommends; MCP cannot make Logic do it."
  The apply-to-Logic backend stays a FUTURE, EXPLICITLY re-gated packet — never
  auto.
- **A real external host (Claude Desktop / Cowork) launching the server via the
  documented config is a MANUAL product step** — documented here, but not
  machine-exercised in this packet (the harness IS a real external process, but
  it is not the branded host app).
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open directions (ALL
  user-gated): the merge · a real external host launching the server via the
  documented config (manual) · a real MCP-SDK transport swap (optional polish) ·
  the apply-to-Logic backend (FUTURE, explicitly re-gated) · a CLA
  product-surface refresh · the future-analyzer candidates from Eno's deferrals ·
  quincy/halee authored dropout reach · a sixth producer · the README 32→35 +
  sample-pin micro-hardening cleanups · anything else the user calls. Do NOT open
  anything blind.

---
_Closed by the archivist (2026-07-04). qa GREEN (1291 / 93/93 / Commit-1 iso
1291 / +12 all test_mcp_e2e_session.py, harness collects 0 / a real client
process spawns `python -m logic_mix_os.cowork_mcp` and drives a nine-command
Cowork session over the child's REAL stdio pipes / attack-5 non-vacuous: bogus
module → EOF, killed child → next request raises, child pid != os.getpid() /
producer over the wire 59.6/52.6/70.7 correctly attributed / mode
front_and_center reflected / memory gate refuses without memory_dir [fresh cwd
iterdir()==[]], writes only .json under the store with it / stems sha256-stable
before==after a full session incl. a memory write / the only subprocess is the
server itself, rc 0 empty stderr, ps clean / determinism identical JSON / zero
new dependency / `git diff f6cc9b7..172150a -- logic-mix-os/logic_mix_os/` EMPTY)
+ reviewer PASS (no must-fix; single-model — Codex unavailable; the harness
production-grade, the inequality-not-float assertions the right call, the
over-the-wire proof genuine, the no-DAW boundary held across the real path). THE
PRODUCT PATH IS PROVEN END-TO-END: a real external process spawns the MCP server
and drives a full producer/mode Cowork session over real stdio, the boundary
intact, the product byte-unchanged — the "does it actually work?" moment answered
YES._
