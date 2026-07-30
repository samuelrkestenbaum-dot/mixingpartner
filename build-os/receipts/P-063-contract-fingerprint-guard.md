# Receipt — P-063: Contract-Surface Fingerprint Guard

- **Packet:** P-063 — Contract-Surface Fingerprint Guard. Closes the P-023
  reviewer watch-item ("a hash of the contract surface"): contract drift was
  UNDETECTED because the only version guard was a tautology against the
  `API_VERSION` literal itself. Drift is now detected.
- **Date:** 2026-07-30
- **Branch:** `claude/logic-mix-os-p061-detector-0dvr2t`, HEAD `56b4051`, tree
  clean.
- **Branch base:** `git merge-base HEAD 5d52253` = **`5d52253`** (the NEW
  default = the PR #38 merge). Ladder: `56b4051` (ONE atomic implementation
  commit) → `f4e26eb` (set-active) → `4386a18` (branch restart; tree identical
  to `5d52253`).
- **Status:** **CLOSED — BOTH GATES GREEN.** qa GREEN + reviewer **PASS, no
  must-fix**. **Single-reviewer — codex absent, so NO second model reviewed
  this diff** (stated plainly).

## Scope

**In (what shipped — exactly 3 files, +240/−12):**

1. **`logic_mix_os/cowork.py`** — pure `contract_fingerprint()`: sha256 over a
   canonical JSON serialization (sorted commands, `sort_keys=True`, fixed
   separators) of the behavioral surface per command: **(name, params,
   side_effect, phase)**. Exposed in `describe_contract()` as
   `contract_fingerprint`. `API_VERSION` **1.1 → 1.2** (adding the field is
   itself an additive contract change — P-023's own MINOR rule, applied to
   itself). stdlib only.
   - **phase INCLUDED** — machine-consumed `_SESSION_FLOW` guidance; a phase
     move alone moves the hash (proven).
   - **description/purpose EXCLUDED** — prose; hash-stable under rewording
     (proven). **api_version excluded** (circularity); **invocation excluded**
     (fixed template).
2. **`tests/test_cowork_contract.py`** — the tautological
   `test_api_version_is_present_and_stable` is **GONE**, replaced by a **pair
   pin**: `(API_VERSION, fingerprint) == ("1.2", golden)` with a
   `_REPIN_PROTOCOL` failure message naming all three artifacts to update.
   Golden pinned:
   `1e712171d32a9bc240fc1a67c57a63b67accb7ca4086e32dfc035f7f8301442e`.
   The golden test uses an independent `_recompute_fingerprint` (does NOT call
   the production canonicalizer). Non-vacuity + prose-stability tests included.
3. **`COWORK_CONTRACT.md`** — fingerprint field + bump-and-re-pin protocol
   documented; version artifacts consistent.

**Explicitly out (held):** analyzers, doctrine, planners, pipeline, renderers,
goldens, `examples/`, fixtures, `cowork_mcp/` behavior beyond the automatic
reflection of `describe_contract()`; no new dependency. Zero
corpus/analyzer/planner/renderer diffs — verified. No push/merge/PR/deploy.

## Commits and base

| Commit | Subject |
|---|---|
| `56b4051` | P-063: contract-surface fingerprint guard (drift now detected) — ONE atomic commit (guard + pins inseparable). |

Chain: `56b4051` → `f4e26eb` (set-active) → `4386a18` (branch restart) →
default `5d52253`. **Code-tree hash identity verified across
`5d52253`/`4386a18`/`f4e26eb`**, so HEAD-green IS Commit-1-green.

**Push state:** NOT pushed by this close (coordinator pushes). NO PR.

## QA proof (GREEN)

- **Suite:** **1477 passed / 0 failed / 0 errors** (baseline 1470 + 7).
- **Regression:** **93/93, `critical_failures == []`**.
- **Commit-1 isolation:** single-commit ladder; code-tree hash identity across
  the three metadata-only ancestors proves HEAD-green = Commit-1-green.
- **Scope/safety grep:** diff = exactly 3 files; zero
  corpus/analyzer/planner/renderer diffs; safety grep clean.
- **Live verify:** golden hex + `API_VERSION == "1.2"` live;
  `describe_contract()` carries `contract_fingerprint`.
- **Non-vacuity (reproduced independently):** a `side_effect` flip moved the
  hash (to `01474fb0…`); a synthetic command moved it; a prose reword did NOT.
- **Determinism:** identical across two processes.
- **Adapter smoke:** `cowork_mcp/adapter.py` reads only `contract["commands"]`
  (verified in source at adapter.py:166) — the new top-level key breaks
  nothing. UI smoke N/A (contract/test packet; recorded, not skipped).

## Reviewer verdict — PASS, no must-fix (single-reviewer; codex absent)

- **Surface definition verified against real consumers:** the adapter derives
  types from param defaults, so type drift IS captured; `side_effect` drives
  the description label + the `memory_dir` requirement.
- **Canonicalization collision-sound.**
- **The pair pin fails correctly in BOTH directions** —
  surface-change-without-bump AND bump-without-surface-change.
- **The golden is a true literal pin** with an independent
  `_recompute_fingerprint`.
- **Stopping point ruled correct:** automated detection, manual bump —
  auto-deriving the version from the hash would destroy the MAJOR/MINOR
  semantic.

## Residue (recorded, non-blocking)

1. **The fingerprint covers the PER-COMMAND surface only** — top-level
   `describe_contract` additive fields still rely on manual bump discipline
   (ironically demonstrated by this packet: adding `contract_fingerprint`
   itself did not move the hash; the 1.2 bump was manual). A strict top-level
   key-set pin is a possible tiny follow-up.
2. **Cosmetic:** `_REPIN_PROTOCOL` wording is slightly off in the
   bump-without-surface-change branch ("contract surface changed" opens the
   message); the remediation steps are correct.
3. **P-062 residue item 5** (contract-fingerprint guard candidate) — **RESOLVED
   by this packet.**

## Open boundaries — NOTHING here is closed by this receipt

- **Merge of P-063** (+ the PR #38-merge-record doc commits on this branch) to
  default — needs the user's explicit word.
- **HAPPY MAN RE-RUN #2** — user-side, unblocked by the PR #38 merge.
- **PR #12** — CLOSED this session (2026-07-30, on the user's go) — resolved,
  no longer an open gate.
- No push/merge/PR/deploy/secrets from this packet (coordinator pushes this
  close under its own authority).

---
_Closed by the archivist (2026-07-30) with BOTH gates GREEN. qa: suite
**1477 / 0 / 0**, regression **93/93**, single-commit ladder with code-tree
identity as the Commit-1 proof, safety grep clean, golden + 1.2 live,
non-vacuity reproduced. Reviewer: **PASS, no must-fix** (single-reviewer,
codex absent). One atomic commit `56b4051` atop `f4e26eb` atop `4386a18`;
merge-base with default `5d52253` verified. The P-063 merge and HAPPY MAN
RE-RUN #2 remain open user gates._
