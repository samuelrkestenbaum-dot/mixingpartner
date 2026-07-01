# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-023
- **Title:** Versioned, self-describing raw-CLI contract (option C, step 1 — `describe_contract` + `COWORK_CONTRACT.md`)

## Why (the arc's final stretch — transport)

The decision system is proven agent-drivable end-to-end (P-021 milestone). What
remains is TRANSPORT: how Claude Cowork reliably invokes it. The user chose
**option C (sequenced): the documented raw-CLI contract now, the MCP server as a
follow-on (P-024).** P-021 proved the CLI is agent-drivable; P-023 makes that a
STABLE, VERSIONED, SELF-DESCRIBING contract an agent can rely on and introspect —
so Cowork isn't reverse-engineering an ad-hoc CLI, it's calling a documented,
versioned surface.

## Authority

**Build / feature — in authority, additive.** A new read-only introspection
command + a documentation file. No change to any existing command's behavior.
**Merge to default stays gated on the user's explicit go; dev-branch commits
covered by standing push-go.**

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/cowork.py` (additive)
1. Add a stable **`API_VERSION`** constant (e.g. `"1.0"`).
2. Add a **`describe_contract`** command whose handler returns the machine-readable
   agent contract (pure, deterministic JSON):
   ```
   {
     "api_version": API_VERSION,
     "invocation": "python -m logic_mix_os.cli cowork --name <command> --params '<json>'",
     "commands": {
        "<name>": {
           "purpose": <existing desc string>,
           "phase":   <phase from _SESSION_FLOW, or "auxiliary">,
           "params":  [<derived from the handler signature — the kwargs beyond ctx/**k>],
           "side_effect": <one of: "none" | "writes:history(live)" | "writes:taste(live)" | "writes:ledger(dead)" | "mutates:session">
        }, ...
     }
   }
   ```
   - **`params` MUST be derived from the real handler signature** (`inspect.signature`,
     excluding `ctx`/`**k`) so the contract cannot drift from the code — do NOT
     hand-maintain a param list.
   - **`side_effect` is an honest, declared classification.** Be truthful and
     specific — this is where the live-vs-dead distinction becomes a
     FIRST-CLASS contract fact (resolving the P-020/P-021 clarity nudge at the
     contract level): `record_mix_pass` → `writes:history(live)`;
     `update_taste_calibration` → `writes:taste(live)`; `write_mix_decision` →
     `writes:ledger(dead)`; `override_track_identity` → `mutates:session`; every
     read-only analyze/plan/checklist command → `none`. Verify each against what
     the handler actually does; do NOT guess.
3. Register `describe_contract` in `COMMANDS` (count 34→35; update the count
   assertion — intended). Do NOT change `list_commands`/`describe_session`/any
   existing handler behavior; do NOT touch `record_pass`/creative/governance/the
   ledger/`cli.py` plumbing beyond registering the command.

### Documentation — `logic-mix-os/COWORK_CONTRACT.md` (new, concise)
A short human-readable contract for a Cowork integrator: the invocation pattern,
the API-version/stability guarantee (versioned, deterministic, JSON out), a
pointer to `describe_contract` / `describe_session` as the machine-readable
source of truth, the product guarantees (local, non-destructive, plan-only v1,
evidence+confidence+risk-class, Class-5 never recommended), and the canonical
session flow. Keep it tight — the machine-readable contract is the source of
truth; the doc orients a human. Do NOT duplicate all 34 command specs by hand
(point to `describe_contract`).

### Tests — the binding guard. Test-first. (new `tests/test_cowork_contract.py`)
- **Completeness invariant (load-bearing):** every key in `COMMANDS` has a
  `describe_contract` entry (no orphan) — and every contract entry is a real
  command (no phantom). Prove load-bearing (an uncovered command fails it).
- **Params match signatures:** for a sample of commands (incl. `record_mix_pass`
  with `name`/`reverted`, and a param-free read command), assert the contract
  `params` equal the handler's real signature kwargs (proves the inspect
  derivation is correct and won't drift).
- **`side_effect` honesty (pin live-vs-dead at the contract level):** assert
  `record_mix_pass` → `writes:history(live)` and `write_mix_decision` →
  `writes:ledger(dead)`; a read-only command → `none`.
- **Versioned + deterministic:** `api_version` present and a stable string; two
  calls byte-identical.
- Registry count 34→35; no stale 34. Existing cowork + P-008/9/18/19/20/21 tests
  pass UNCHANGED (only the registry-count assertion changes 34→35).

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network. Pure introspection + JSON + a Markdown doc.

## Constraints

- **≤2 commits.** Commit-1 (test-first, green in isolation): `API_VERSION` +
  `describe_contract` + the contract tests. Commit-2: `COWORK_CONTRACT.md` (+ a
  small consistency check if clean).
- **No external mutation** — no push / merge / deploy / secret. (Standing push-go
  covers dev-branch commits only.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **277 → 277+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held (additive read-only → goldens
  untouched).
- Commit-1 green in isolation.
- **Contract is complete + honest:** every command has an entry (invariant
  load-bearing); `params` match real signatures (no drift); `side_effect` pins
  live-vs-dead (`record_mix_pass` live / `write_mix_decision` dead); versioned +
  deterministic. Registry 35, no stale 34. Safety grep clean; UI N/A; prior tests
  green.

---
_Confirmed as active by the orchestrator-in-chief (P-023, option C step 1). The
MCP server is the sequenced follow-on (P-024). One packet at a time._
