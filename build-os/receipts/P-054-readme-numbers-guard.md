# Receipt — P-054: README Numbers Audit + Drift Guard

- **Packet:** P-054 — README Numbers Audit + Drift Guard. A test + docs packet
  that (a) fixes the two known-stale README numbers P-053 surfaced, and (b) adds
  a DRIFT GUARD (`tests/test_readme_numbers.py`) that pins the README's
  load-bearing stated numbers against their LIVE / COMMITTED sources — so the
  stale-README-number class FAILS LOUDLY going forward instead of shipping.
  **ZERO engine/profile/analyzer/MCP/runtime change.**
- **User authority:** opened on the user's "ok go" (2026-07-05) after the P-053
  merge (PR #31 → default `bc67df4`) — the decision-free hygiene/hardening
  direction of the open set: it BOTH clears the residue qa surfaced AND
  implements the P-053 fix-then-pass lesson (a stale README number slipped a
  diff-region review; pin the class, don't spot-check). The taste-gated
  directions (Eno-deferral analyzers, quincy/halee dropout reach, a sixth
  producer, apply-to-Logic) stayed USER-GATED and were NOT touched.
- **Date:** 2026-07-05
- **Status:** CLOSED — qa GREEN **(10/10; suite 1302 / 0)** + reviewer
  **PASS (no must-fix)**.

## Scope

**In (the confirmed packet spec):**

1. **Fix the two known-stale README numbers:**
   - README line ~532, the regression EXAMPLE block
     `{ "tests_run": 68, "passed": 68, "failed": 0, ... }` → the live count
     **93 / 93 / 0** (live-verified against `run_regression_suite()`). Stale
     since P-035.
   - `tests/test_mode_demo_refresh.py` (~line 405) — the quincy story-pin
     DOCSTRING "the one committed demo where the reach moves a verdict" → honest
     wording ("one of two committed reach-and-win demos … alongside
     `chris_lord_alge_big_chorus`", the P-053 second reach-and-win demo).
     Docstring-only — no assertion changed, collection-neutral.
2. **The DRIFT GUARD** — a NEW `tests/test_readme_numbers.py` (4 tests) that
   pins the README's load-bearing numbers against LIVE / COMMITTED sources with
   ANCHORED extraction (not a general digit-scan):
   - **Command count:** two authored spots (~line 401 CLI table, ~line 574
     section map) == `str(len(cowork.COMMANDS))` (= 35), PLUS a WHOLE-FILE sweep
     asserting no stale "N commands" != live — the exact whole-file check the
     P-053 sweep needed.
   - **Regression example:** the extracted `{tests_run, passed, failed}` block
     == a LIVE `run_regression_suite()`.
   - **Five-producer table:** each cell (overall + vocal-role + loop-context,
     all three rows) == the `HEADLINES` dict IMPORTED from `test_sample_refresh`
     (the single source of truth — no duplicated hardcode; the P-047/P-049
     derivation discipline). This ALSO closes the standing P-046 accepted gap
     (README table numbers were never machine-pinned).
   - **Expected sides are ALL derived from source** — no magic 35/93/76.3
     literal in any assertion (verified: literals appear only in
     comments/docstrings).

**Explicitly out (binding non-scope, held):**

- ZERO changes to engine code — **0 `.py` under `logic_mix_os/`**; the engine +
  profiles + analyzers + `cowork_mcp/` + `cli.py` + `cowork.py` byte-unchanged.
  No new producers / families / analyzers / dependencies. No safety/governance
  changes.
- ZERO `examples/` change — the five sample trees + eleven mode demos
  byte-untouched; zero fixtures/goldens.
- No general "rewrite the README" — only the two stale-number fixes + the guard
  (no unrelated prose sweep; prose-count sweeps deliberately forbidden — see
  Residue note 1).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Single commit** (the audit was clean beyond the two named items, so one
  commit; ≤2-commit rule honored):
  - `056a8cb` — "P-054: fix two stale README numbers + add README-numbers drift
    guard" — exactly **3 files**, +192/−3:
    - `logic-mix-os/README.md` (+1/−1 — the 68→93 regression-example fix)
    - `logic-mix-os/tests/test_mode_demo_refresh.py` (+3/−3 — the quincy
      docstring only; no assertion changed, collection-neutral)
    - `logic-mix-os/tests/test_readme_numbers.py` (NEW, +187 — the 4-test drift
      guard)
- **Commit-1 green in isolation:** trivially satisfied — the fixes + the guard
  land together in the single commit, so HEAD == the isolation proof; the guard
  is green because the fixes are applied in the same commit. Full suite **1302**.
- **Parent:** `6c70daa` (set-active — "build-os: set P-054 … active — user go")
  on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base with default:** `bc67df4` (= PR #31 merge — P-053 already merged
  to default). Verified at close: `git merge-base HEAD bc67df4` = `bc67df4`; the
  dev branch is fast-forwarded onto default, so a P-054 PR carries only `056a8cb`
  + the close commit — a clean single-packet PR.
- **Push state:** PUSHED to the dev branch under the standing go **BEFORE
  qa/reviewer ran** — both gates validated the final SHA. **NOT merged** — the
  merge of P-054 is a user gate.

## QA proof (GREEN — 10/10)

- **Suite:** 1298 → **1302 passed, 0 failed** (+4, all in the new
  `tests/test_readme_numbers.py`); regression **93/93**; single commit = HEAD is
  the Commit-1-isolation proof.
- **Per-file collect:** `test_readme_numbers.py` = **4**; `test_mode_demo_refresh.py`
  still **26** (the docstring edit is collection-neutral).
- **Commit-1 iso:** 1302 (single commit).
- **The guard BITES on all three areas** (independent, in isolated worktrees,
  restored between runs):
  - `35→32` → the command-count authored-spots test AND the whole-file sweep
    both FAIL.
  - `93→68` → the regression-example test FAILS.
  - `76.3→76.4` → the five-producer table test FAILS.
- **★ THE PACKET'S RAISON D'ÊTRE CONFIRMED:** the guard would have failed loudly
  on BOTH historical misses this session — the `32→35` (the leftover
  "32 commands" that slipped P-053's diff-region review → caught by the
  whole-file sweep) AND the `68→93` (the regression example stale since P-035 →
  caught by the live-suite comparison). qa + reviewer both verified this
  explicitly.
- **Robustness:** anchored regexes exclude the §32/§38/§39 section refs and the
  68.8 Quincy table cell (not the regression anchor); table parsing derives
  column order from the header + strips bold. No false positives; no third stale
  number (audited — the two named were the whole set).
- **Zero engine drift; safety grep clean** — no secrets / network / model-ids /
  abs-paths across the diff.

## The user's required proof — every clause met

suite clean ✓ (1302/0) · regression clean ✓ (93/93) · zero engine/runtime change
✓ (0 `.py` under `logic_mix_os/`; zero `examples/` change) · the two stale
numbers fixed ✓ (68→93 live-verified; the quincy docstring) · the drift guard
covers the command count + the regression example + the five table overalls and
BITES on any drift ✓ (35→32, 93→68, 76.3→76.4 each fail) · the guard derives
table numbers from the existing single source ✓ (`HEADLINES` imported from
`test_sample_refresh`, no duplicated hardcode) · whole-README grep shows no
stale "32 … commands" / no stale regression count ✓ (the whole-file sweep
enforces it as a test).

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- Guard load-bearing (not cosmetic); expected sides genuinely derived-from-source
  (no hardcode that would defeat the purpose); robust in both directions; the two
  fixes correct + minimal; non-scope clean. Verbatim: "Converts the P-053 lesson
  into a durable, live-pinned guard for the two classes that actually bit, and
  additionally closes the standing P-046 gap by machine-pinning the table off the
  existing single source."

## Residue (carried to `build-os/memory/residue.md`)

- **RESOLVED by this packet:**
  - The quincy story-pin docstring (P-053 note 1) — ✓ RESOLVED (rewritten to
    "one of two … alongside `chris_lord_alge_big_chorus`").
  - The 68→93 regression-example staleness (P-053 note 2) — ✓ RESOLVED (fixed +
    now machine-pinned to a live `run_regression_suite()`).
  - The P-053 whole-file-grep lesson (P-053 note 3) — now ENFORCED by a test
    (the whole-file "N commands" sweep), not merely a written note.
- **NEW accepted notes (recorded not fixed — both OUT of this packet's scope,
  named for the record):**
  1. **Unguarded prose-count class:** README prose counts like "five committed
     trees", "eleven producer × mode runs" / "eleven demos", "seven win exactly
     the moves", the sample-invocation count are NOT pinned (the packet
     deliberately forbade prose sweeps). A future "prose-count guard" candidate —
     the same staleness class one abstraction level up. Lower priority: prose
     counts drift less often and are more visible.
  2. **The command-count sweep is intentionally exact-phrasing**
     (`(\d+) (?:bounded )?commands`): a future subset phrasing ("12 mutating
     commands") could false-positive, or an interposed-word phrasing ("35 CLI
     commands") / a spelled-out count could false-negative. Acceptable +
     consistent with the "targeted, not a general digit parser" mandate given
     the current README shape; re-examine only if the README's command-count
     phrasing changes.
- All prior standing notes (incl. the ★★ groove-carrier trajectory watch-item,
  the CLA sha256-self-pin-on-sixth-producer note, the P-050/P-051/P-052 accepted
  notes, and the safety line) and the named lessons retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-054** — `056a8cb` (+ this close
  commit) atop `bc67df4` (= PR #31) — a clean single-packet PR (the branch is
  fast-forwarded onto default). Awaits the user's explicit word. The commit is
  pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open directions (ALL
  user-gated): the P-054 merge · a real external host driving the MCP server
  (manual) · a real MCP-SDK transport swap · the apply-to-Logic backend (FUTURE,
  re-gated) · the future-analyzer candidates from Eno's deferrals (textural
  coherence · generative process · ambient patience) · quincy/halee dropout
  reach · a sixth producer · a prose-count guard (the new residue) · anything
  else the user calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-05). qa GREEN (10/10; suite 1302 / 0 /
regression 93/93 / Commit-1 iso 1302 / per-file collect test_readme_numbers.py=4,
test_mode_demo_refresh.py=26 / the guard bites on all three areas — 35→32, 93→68,
76.3→76.4 — and would have caught BOTH historical misses this session / safety
grep clean) + reviewer PASS (no must-fix; single-model — Codex unavailable). The
README's load-bearing numbers (command count, regression example, the
five-producer table) are now MACHINE-PINNED against their live/committed sources —
stale-README-number is a CAUGHT class going forward, and the standing P-046
README-table-drift gap is CLOSED. The P-053 whole-file-grep lesson is now enforced
by a test, not just a note._
