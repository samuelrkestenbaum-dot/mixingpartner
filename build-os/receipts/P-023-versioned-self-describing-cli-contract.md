# P-023 — Versioned, self-describing raw-CLI contract (option C, step 1)

**Date:** 2026-07-01
**Status:** CLOSED — qa GREEN, reviewer pass. Fourth step of the arc P-019→P-024 to a Claude-Cowork-usable end-to-end state — the FIRST of the two transport steps the user sequenced as **option C** (documented raw-CLI contract now; MCP server as the follow-on P-024).
**Type:** Build / feature — in authority, additive. A new read-only introspection command + a documentation file. No change to any existing command's behavior.

---

## Title

Turns the agent-drivable cowork CLI (proven end-to-end in the P-021 milestone)
into a STABLE, VERSIONED, SELF-DESCRIBING contract Claude Cowork can introspect
instead of reverse-engineering an ad-hoc surface. Adds `API_VERSION = "1.0"` and
a `describe_contract` command (registry **34 → 35**) that emits the
machine-readable agent contract, plus a concise human-facing
`COWORK_CONTRACT.md`. This is where the live-vs-dead distinction becomes a
FIRST-CLASS contract fact (not merely telegraphed by `desc` strings, as it was
through P-020, nor only executably pinned by a test, as in P-021).

## What it does (the mechanism)

- **`describe_contract`** returns pure, deterministic JSON:
  `{api_version, invocation, commands: {name: {purpose, phase, params, side_effect}}}`.
  - **`invocation`** — the exact call pattern
    `python -m logic_mix_os.cli cowork --name <command> --params '<json>'`.
  - **`purpose`** — the registry `desc` string (single source; no second copy).
  - **`phase`** — the `_SESSION_FLOW` phase the command belongs to, else
    `"auxiliary"`.
  - **`params` — DERIVED from each handler's real `inspect.signature`**, dropping
    the leading context arg **BY POSITION** (def-handlers name it `ctx`, lambdas
    name it `c` — dropping by position handles both) and skipping `**k`. Because
    the param list is read from the code, the contract **cannot drift** from the
    handlers. Examples verified: `record_mix_pass` → `[name, reverted]`,
    `detect_masking` → `[]`, `update_taste_calibration` → `[label, context]`.
  - **`side_effect` — an HONEST, declared classification** pinning live-vs-dead as
    a first-class contract fact. Exactly **4 writers**, all other **31** commands
    `none`:
    - `record_mix_pass` → `writes:history(live)`
    - `update_taste_calibration` → `writes:taste(live)`
    - `write_mix_decision` → `writes:ledger(dead)`
    - `override_track_identity` → `mutates:session`
  - **`describe_contract` parked in `_SESSION_FLOW.auxiliary`** (a data addition
    mirroring P-020's `describe_session`), so P-020's exact-cover completeness
    invariant still holds — now at **35** (31 phase-mapped + 4 auxiliary =
    `len(COMMANDS)`).
- **`COWORK_CONTRACT.md`** (new, concise, integrator-facing): the invocation
  pattern, the api-version / stability guarantee (versioned, deterministic, JSON
  out), the `side_effect` live-vs-dead vocabulary, a pointer to
  `describe_contract` / `describe_session` as the machine-readable source of
  truth (does NOT hand-list all 35 commands), the product guarantees (local,
  non-destructive, plan-only v1, evidence + confidence + risk-class, Class-5 never
  recommended), and the 8-phase canonical session flow. Verified accurate against
  the code — invocation string, phases, and the side_effect table all cross-check.

## Scope

**In:**
- `logic_mix_os/cowork.py` (additive): `API_VERSION` constant; the
  `describe_contract` handler + its helpers (inspect-based param derivation, the
  side_effect classification); registered in `COMMANDS` (34 → 35); parked in
  `_SESSION_FLOW.auxiliary`. No existing handler's behavior/output changed.
- `logic-mix-os/COWORK_CONTRACT.md` (new): the human-readable contract.
- New `tests/test_cowork_contract.py` — the binding guard (completeness
  invariant, params-match-signatures, side_effect honesty, versioned +
  deterministic, registry 35).
- The two existing registry-count assertions in `tests/test_cowork.py` and
  `tests/test_cowork_session_flow.py` move **34 → 35** (intended; the only edits
  to existing tests).

**Explicitly out (verified UNTOUCHED):**
- `cli.py` plumbing (beyond the command being reachable via the existing cowork
  verb), `pipeline.py`, `memory.py`, `creative.py`, `governance.py`, the decision
  ledger, `record_pass`, `list_commands` / `describe_session` behavior — NONE
  changed.
- Every existing test assertion other than the two registry-count numbers.
- Any push / merge / deploy / secret action.

## Commits (branch base + hash)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Base for P-023:** `6c40e2b` — "Merge PR #15: P-016 evidence-gated
  loop-deconstruct promotion" — the default-branch tip; confirmed an ancestor of
  HEAD. (`2f6f27a` was the P-023 active-packet confirmation; `7f7e86f` was the
  P-021 close.)
- **`60b3b92`** — Commit-1 (test-first): `API_VERSION` + `describe_contract` +
  helpers + `tests/test_cowork_contract.py` (contract tests) + registry 34→35 +
  the two count-assertion moves. **Green in isolation = 293 passed.**
  Touches `cowork.py`, `test_cowork.py`, `test_cowork_contract.py` (new),
  `test_cowork_session_flow.py`.
- **`dcc4c5b`** — Commit-2: `logic-mix-os/COWORK_CONTRACT.md` (doc only, +78).

Two commits (within ≤2). Additive read-only product change + a doc.

## QA proof (exact)

- **Suite: 277 → 293 passed** (+16; 0 failed / 0 skipped / 0 warnings; green under
  `-W error`). **Commit-1 green in isolation: 293 passed.**
- **Regression: 68/68, 0 critical, 0 warnings** held (additive read-only → goldens
  untouched).
- **Completeness invariant load-bearing:** the contract keys == the 35 registry
  keys (an orphan command with no entry, or a phantom entry with no command,
  fails the test).
- **Params match real signatures (no drift):** `record_mix_pass` → `[name,
  reverted]`, `detect_masking` → `[]`, sampled across def-handlers and lambdas —
  the inspect derivation is correct and won't drift from the code.
- **side_effect honesty verified against handler BODIES:** the 4 writers labelled
  correctly; qa (and reviewer, independently — reviewer scanned all 31 `none`
  commands for write patterns) found NO mislabel.
- **Versioned + deterministic:** `api_version` present and a stable string
  (`"1.0"`); two calls byte-identical.
- **Registry 35:** both existing count assertions updated 34 → 35; no stale 34
  remains.
- **Scope clean:** only the 5 authorized files changed; `cli.py` / creative /
  governance / ledger / memory / pipeline untouched; existing tests changed only
  the count assertion.
- **Safety grep: clean.** **UI smoke: N/A** (no UI surface touched).
- **qa verdict: GREEN.**

## Reviewer verdict

**Pass.** Reviewer verified the inspect-derived `params` against the real
signatures (correct drop-by-position for both `ctx` def-handlers and `c`
lambdas), independently scanned all 31 `none`-labelled commands for write
patterns and confirmed the 4 writers are the only writers (no mislabel),
confirmed the auxiliary parking keeps P-020's exact-cover invariant satisfied at
35, and confirmed `COWORK_CONTRACT.md` is accurate against the code (invocation,
phases, side_effect table).

**Codex second-eyes: NOT available — single-reviewer verdict** (recorded).

## Residue / carry-forward (for P-024)

- **Reviewer watch-item (non-blocking) — the version can drift from the surface.**
  `API_VERSION` is a hand-maintained string with NO test that fails when a
  command's `params` / `side_effect` changes without a version bump. The `params`
  and `side_effect` values themselves cannot drift from the code (inspect-derived
  / verified), but the declared VERSION can silently lag a surface change.
  **P-024 (the MCP server) is the place to add a version-fingerprint guard** — a
  test that pins a hash of the contract surface so any surface change forces a
  conscious version decision.
- **P-024 can reuse `describe_contract` directly.** The per-command `params` /
  `side_effect` metadata is exactly the shape an MCP tool-schema needs; the MCP
  server should consume it rather than re-derive.
- **Minor note (NOT a bug):** `update_taste_calibration` exposes `[label,
  context]` via inspect — MORE honest than the hand-written `desc` "(params:
  label)". The inspect derivation is the truthful one; no change needed.

## Open boundaries (awaiting explicit go)

- **P-023 is local-only at this close** — commits `60b3b92` + `dcc4c5b` on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b`
  (PR #15) merge base. **Not pushed / merged.** Any push of these commits — and
  any subsequent PR / merge into the protected default — needs the user's
  explicit go. **No push / merge / deploy / secret action taken in this close.**
  (The build-os-only close commit is separate from the two product-repo commits
  above.)

---
_Archivist close, 2026-07-01. Option C step 1: the raw-CLI agent transport is now a versioned, self-describing contract — `describe_contract` (registry 35), inspect-derived params that cannot drift from code, an honest side_effect classification that makes live-vs-dead a first-class contract fact, plus a concise `COWORK_CONTRACT.md`. Two commits `60b3b92` + `dcc4c5b`. Suite 277 → 293 (+16); regression 68/68. Single-reviewer verdict (Codex unavailable). The ONLY remaining arc step is P-024 (thin MCP server wrapping the same registry, reusing describe_contract metadata for tool schemas) + a version-fingerprint guard._
