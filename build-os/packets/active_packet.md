# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-063 — Contract-Surface Fingerprint Guard** (staged
  2026-07-30 on the user's explicit go: "ok go" on the remaining board).

## P-063 — Contract-Surface Fingerprint Guard

Closes the P-023 reviewer watch-item ("a hash of the contract surface") that
P-024's retirement left open as its own item.

- **Branch:** `claude/logic-mix-os-p061-detector-0dvr2t`, restarted atop the
  NEW default `5d52253` (the PR #38 merge). HEAD at staging: `4386a18`
  (tree identical to `5d52253`; tree clean).
- **Route:** builder → qa → reviewer → archivist. Receipt on close:
  `build-os/receipts/P-063-contract-fingerprint-guard.md`.

### Why (from the recorded residue — 2026-07-26 bookkeeping pass, carried through P-062's close)

The cowork contract's only version guard is tautological. Quoting
`build-os/memory/residue.md`:

> What exists instead is `API_VERSION = "1.0"` … a **hand-maintained literal**.
> Its only guard is
> `tests/test_cowork_contract.py::test_api_version_is_present_and_stable` …
> **That is a TAUTOLOGY against the literal itself.** It pins the constant to
> its own value and the contract dict to that same constant — so it can never
> detect a change in the *contract surface*. Add a command, remove one, or
> change any command's params or `side_effect` classification, and
> `API_VERSION` remains `"1.0"` and the test still passes green.
> **Consequence: contract drift is currently UNDETECTED**, and the MCP tool
> schemas are derived from that same undetected-drift surface.

And from P-062's close (residue item 5):

> **`API_VERSION` is now 1.1** — the contract-fingerprint guard candidate
> (hash the contract surface) REMAINS OPEN and is now **mildly more urgent**:
> two hand-bumps in the literal's lifetime.

The literal now lives at `cowork.py:29` (`API_VERSION = "1.1"`), hand-bumped
twice (1.0 at P-023, 1.1 at P-062). The MCP tool schemas
(`cowork_mcp/adapter.py` derives them from `describe_contract()`) ride on that
same undetected surface. P-023's watch-item asked for "a hash of the contract
surface".

### Scope (builder verifies exact shapes against real code before writing)

1. **`logic_mix_os/cowork.py`:** a pure `contract_fingerprint()` — sha256 hex
   over a CANONICAL serialization (sorted, stable `json.dumps` with
   `sort_keys`) of the contract surface: for every command,
   (name, params, side_effect) at minimum. Builder decides whether
   phase/description belong in the surface and DOCUMENTS the choice
   (guideline: fingerprint what clients depend on — behavioral surface, not
   prose; description likely EXCLUDED so wording tweaks don't re-pin). Expose
   it in `describe_contract()` output as `contract_fingerprint`.
2. **Tests (`tests/test_cowork_contract.py`):**
   (a) pin the CURRENT fingerprint hex as a golden constant;
   (b) assert `describe_contract` carries it and it matches a recomputation;
   (c) NON-VACUITY: prove the fingerprint MOVES under a synthetic surface
   mutation (e.g. monkeypatched extra command / changed side_effect) and the
   pinned test would go red;
   (d) couple it to the version: the failure message must TELL the developer
   the protocol — "contract surface changed: bump API_VERSION and re-pin the
   fingerprint".
3. **KNOWN PIN RISKS — builder checks FIRST (P-062 lesson: the count pins live
   in FIVE places):** describe_contract output-shape pins in
   `test_cowork_contract.py`; the MCP adapter/e2e tests (`test_cowork_mcp.py`,
   `test_mcp_e2e_session.py`) if the initialize/tools surface reflects
   describe_contract's top-level keys; `COWORK_CONTRACT.md` (document the
   fingerprint field + the bump-and-re-pin protocol); README if it enumerates
   contract fields (P-054/P-055 guards decide).
4. **★ API_VERSION question — builder adjudicates and documents:** adding
   `contract_fingerprint` to `describe_contract()` output is itself an
   additive contract change — per P-023's own rule that suggests **1.1 → 1.2**
   WITH the new fingerprint pinned at the post-change surface. Decide, justify
   in the commit body, keep all version artifacts consistent (`cowork.py` +
   tests + `COWORK_CONTRACT.md`).

### Out of scope

Everything else — analyzers, doctrine, planners, pipeline, renderers, goldens,
`examples/`, fixtures, `cowork_mcp/` behavior beyond what reflects
`describe_contract()` automatically. No new dependency (hashlib is stdlib).

### Commit plan

Expect **ONE atomic commit** (guard + pins inseparable); ≤2 allowed.

### Baseline (measured at `4386a18` / identical tree to `5d52253`)

- Suite: **1470 passed / 0 failed / 0 errors**.
- Regression: **93/93**, `critical_failures []`.
- Env: pyloudnorm ABSENT; fixtures generated; bare `python3 -m pytest`.

### Working contract

- Verify branch base before building (restart base: default `5d52253`).
- ≤2 commits; Commit-1 green in isolation.
- Full proof + safety grep before close (qa reports exact counts).
- **No merge / push / deploy without explicit go.**

### Open gates (carried)

- **HAPPY MAN RE-RUN #2** — user-side, now unblocked by the PR #38 merge:
  analyze, then `execution-brief --dir <out>`.
- **P-063's own merge after close** — no PR/merge without explicit go.
- **PR #12 — RESOLVED:** CLOSED on the user's go this session (2026-07-30),
  per the recorded recommendation (`86a3242`). No longer an open gate.

---
_Staged 2026-07-30 (P-063 SET-ACTIVE, build-os/ only). One packet at a time:
builder → qa → reviewer → archivist → receipt._
