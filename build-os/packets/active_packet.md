# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "ok go" (2026-07-05) after the
  P-053 merge (PR #31 → default `bc67df4`). Of the open directions, this is
  the decision-free hygiene/hardening one — it clears the residue qa
  surfaced AND implements the lesson from the P-053 fix-then-pass round
  (a stale README number slipped a diff-region review; pin the class). The
  taste-gated directions (Eno analyzers, quincy/halee dropout reach, a
  sixth producer, apply-to-Logic) stay USER-GATED and are NOT touched.
- **ID / Title:** **P-054 — README Numbers Audit + Drift Guard**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `bc67df4` (= PR #31 merge — the branch was fast-forwarded to it, clean;
  verify with `git merge-base`).
- **Baseline to protect:** suite **1298** / regression **93/93** / the five
  producers + five sample trees + eleven mode demos byte-stable / ZERO
  engine/profile/analyzer/MCP/runtime change (a test + docs packet).

## Why this packet (the residue + the lesson)

Two stale README numbers reached the product surface, and P-053's
fix-then-pass proved a diff-region review misses them — only a whole-file
check against live values catches the class. This packet (a) fixes the
two known-stale items, and (b) adds a DRIFT GUARD that pins the README's
load-bearing stated numbers against their live/committed sources, so this
staleness class FAILS LOUDLY going forward instead of shipping.

## Scope (tests + docs only)

1. **Fix the known-stale README numbers:**
   - README line ~532: the regression EXAMPLE block
     `{ "tests_run": 68, "passed": 68, "failed": 0, ... }` → the live count
     **93 / 93 / 0** (verify: `run_regression_suite()` → tests_run 93 /
     passed 93 / failed 0). Stale since P-035.
   - `tests/test_mode_demo_refresh.py:~405` — the quincy story-pin DOCSTRING
     "the one committed demo where the reach moves a verdict" → honest
     wording ("one of two — alongside `chris_lord_alge_big_chorus`", the
     P-053 second reach-and-win demo). Docstring-only, collection-neutral.
2. **The DRIFT GUARD** — a new `tests/test_readme_numbers.py` that pins the
   README's load-bearing stated numbers against live/committed sources with
   TARGETED assertions (not a general prose-number parser — extract the
   specific known lines/blocks and compare):
   - **Command count:** the "N … commands" claims match `len(cowork.COMMANDS)`
     (== 35); assert the correct count is present and no stale count string
     (e.g. "32 … commands") remains — the whole-file check the P-053 sweep
     needed.
   - **Regression example:** extract the `{ "tests_run": …, "passed": …,
     "failed": … }` example block and assert it equals a live
     `run_regression_suite()` (tests_run/passed/failed) — this is the exact
     class that shipped stale; the guard makes it impossible again.
   - **The five-producer table:** assert each producer's committed overall
     (from its `examples/sample_output_*/doctrine_score.json`, or the
     `HEADLINES` pin the sample-refresh suite already owns — reuse the
     single source of truth, don't duplicate) appears in the README table
     row. This ALSO closes the standing P-046 accepted gap (README table
     numbers were not machine-pinned).
   The guard must BITE (prove it: a scratch edit of a README number → the
   guard fails; restore). Keep the extraction robust and specific so a
   legitimate future README edit that keeps the numbers correct still
   passes, but any number drifting from its live source fails loudly.

## Non-scope (binding)

ZERO changes to engine code (.py under logic_mix_os/), profiles, analyzers,
fixtures, goldens, the MCP surface, cli.py, cowork.py, the sample trees,
the mode demos. No new producers / families / analyzers / dependencies. No
safety/governance changes. No general "rewrite the README" — only the two
stale-number fixes + the guard (do NOT sweep unrelated prose). No merge
until qa + reviewer dual-green.

## Orchestrator recon (binding on the builder)

- The regression example is at README ~line 532; the two command-count
  lines are ~401 (CLI table) + ~574 (section map), both now "35" after
  P-053 — the guard pins them. `run_regression_suite()` returns
  `{tests_run, passed, failed, ...}` (currently 93/93/0). `cowork.COMMANDS`
  is the registry (len 35).
- REUSE the sample-refresh `HEADLINES`/committed `doctrine_score.json` as
  the single source for the table numbers — do NOT hardcode a second copy
  that could itself drift (the derivation-from-pins discipline of P-047/
  P-049).
- Robustness: the guard reads README text; make the extraction specific
  (anchored regex on the known block/line shapes), fail loudly with a clear
  message, and be deterministic. It must not be flaky on incidental digits
  elsewhere in the prose.
- If a README number is found stale beyond the two named (a genuine third
  case), FIX it and report it (this packet's whole point is a clean audit)
  — but do NOT expand into non-number prose edits.

## Required proof

suite clean · regression clean · zero engine/runtime change (diff-proven) ·
the two stale numbers fixed (68→93; the quincy docstring) · the drift guard
covers the command count + the regression example + the five table overalls
and BITES on any drift · the guard derives table numbers from the existing
single source (no duplicated hardcode) · whole-README grep shows no stale
"32 … commands" / no stale regression count.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the two doc fixes (68→93 + the quincy docstring) + the new
  `tests/test_readme_numbers.py` drift guard — full suite green in
  isolation (the guard is green because the fixes are applied in the same
  commit).
- **Commit-2 (only if needed):** any second stale number the audit
  surfaces + its guard coverage. If the audit is clean beyond the two, one
  commit suffices.

---
_Set active by the orchestrator on the user's "ok go" (2026-07-05), after
the P-053 merge — the decision-free residue/hardening direction. One packet
at a time: builder → qa + reviewer → archivist → receipt._
