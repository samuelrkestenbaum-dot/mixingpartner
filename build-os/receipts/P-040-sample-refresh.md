# Receipt — P-040: the Sample Refresh — the two-producer demo output

- **Packet:** P-040 — the SAMPLE REFRESH: the two-producer demo in committed
  form. `examples/sample_output/` (the REFERENCE run, halee_ramone — the
  default-named tree so existing README links keep working) +
  `examples/sample_output_timbaland/` (the SAME stems, `--producer
  timbaland`), both generated via the REAL CLI from the `vocal_chop_groove`
  fixture, plus the "Two producers, same stems" README section. **Docs/demo
  only — ZERO product code.** This packet makes the P-035/P-039 differential
  VISIBLE without running anything, and it **CLEARS the P-038 standing note**
  (the old dense_chorus-era tree with stale producer-named prose was replaced
  wholesale; qa confirmed the stale strings existed at base and are absent
  now).
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer **PASS (no must-fix)**.

## Scope

**In (the confirmed packet spec):**

1. **Both trees regenerated via the REAL CLI** (the P-039 demo path) from
   `vocal_chop_groove` — the differential's showcase (76.3 vs 60.9, the blend
   policy live, the groove axes reading genuinely). 30 artifacts per tree.
2. **The staleness pin at FULL strength** (`tests/test_sample_refresh.py`):
   30-file byte equality per tree against a fresh render, with exactly ONE
   documented normalization (the abs→rel stems-path echo), the
   no-absolute-path assertion, and the headline pin machine-checking the
   README numbers.
3. **test-9 (`test_contract_migration`) parametrized over BOTH trees** —
   extended, not weakened (reviewer-verified).
4. **README:** the two-tree sample wording refresh + the new "Two producers,
   same stems" section — the verbatim invocation pair, the compact
   side-by-side table, the same-winners honesty statement, pointers into the
   two trees. Observational language; the numbers stated are the pinned ones.
5. **The fixture switch handled honestly:** the old dense_chorus-era
   `sample_output` replaced wholesale; every dependency on its specific
   content checked and consciously updated — nothing left dangling
   (reviewer-verified).

**Explicitly out:**

- ANY product code change — this is a docs/demo packet; zero
  engine/CLI/renderer lines touched.
- The third producer (the NEXT arc item — ★ USER-GATED; see Open
  boundaries).
- Deeper mode-forking (the arc item after).
- Merge/deploy/publish — user-gated. Push handled by the orchestrator after
  close (standing go).

## Commits and base

- **Two commits (≤2 rule satisfied), local at close — pushed AFTER close by
  the orchestrator (standing go), NOT merged:**
  - `33cf10d` — "P-040: the two-producer demo output — examples/ regenerated
    on vocal_chop_groove + the staleness pin" — 62 files, +4240/−1744: the
    two 30-artifact trees (`examples/sample_output/` replaced,
    `examples/sample_output_timbaland/` NEW), test-9 parametrized over both
    trees (`tests/test_contract_migration.py`, 12±), and the NEW
    `tests/test_sample_refresh.py` (118+) with the staleness pin at FULL
    strength. **Commit-1 green in isolation** (real worktree check: 806 +
    93/93).
  - `9e58e9b` — "P-040: README — the two-tree sample wording + the 'Two
    producers, same stems' section" — README only, 1 file, +49/−2.
- **Parent:** `1783683` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `2c09428` (the post-backlog batch
  merge). Verified at close: `git merge-base HEAD 2c09428` = `2c09428`. The
  branch carries P-039 + P-040 + closes.

## QA proof (GREEN — exact counts)

- **Suite:** 801 → **806 passed** (+5 — `tests/test_sample_refresh.py` + the
  test-9 parametrization over both trees); 0 failed / skipped regressions.
- **Regression:** **93/93** — samples are not goldens; non-interaction
  verified TWO ways.
- **Commit-1 isolation:** real worktree check at `33cf10d` — **806 + 93/93**.
- **Freshness proven INDEPENDENTLY:** qa regenerated both trees via the
  VERBATIM README invocations → byte-identical **30/30 + 30/30**.
- **Headlines exact:** 76.3 / 65.0 / 15.0 (reference); 60.9 / 85.0 / 10.0
  (timbaland); producer blocks present + verdict line 3 in both trees.
- **Zero absolute paths** in either committed tree.
- **Zero stale strings:** zero old keys / old mode names / stale producer
  prose — the timbaland tree carries ZERO Halee/Ramone strings; the reference
  tree's only mentions are legitimate profile-provenance. qa confirmed the
  P-038-noted stale strings EXISTED at base and are ABSENT now — the standing
  note is cleared on evidence, not assertion.
- **Sabotage:** one flipped bit in a committed sample artifact → the
  staleness pin FAILED for exactly the sabotaged tree.
- **Safety grep:** clean (the applescript TODO lines are pre-existing
  renderer output, present at base).

## Reviewer verdict — PASS (no must-fix)

- The README read as a SKEPTICAL NEWCOMER — every sentence traced to
  artifacts, code, or receipts.
- The **same-winners honesty statement ENDORSED** as strengthening the demo:
  it pre-empts "so the knob does nothing?" and points at
  `test_differential_proof.py:417`, where the plan reversal IS proven.
- The "why they differ" column verified accurate at the CODE level.
- The invariance sentence verified precise: exactly 3 of 15 score keys
  differ — the 3 table rows.
- Reproducibility verified under INDEPENDENT execution — no timestamps
  anywhere in the artifacts (not same-day luck).
- test-9 extended-not-weakened; the old tree's wholesale replacement leaves
  NOTHING dangling.
- **Both sabotage directions run:** an artifact flip is caught by BOTH pins,
  correctly parametrized; a README flip is NOT caught — judged an **ACCEPTED
  GAP**: the values are triple-pinned at the file level and a
  markdown-parsing test would be brittle for marginal value.
- **Codex NOT available — single-model review.**

## Residue (recorded, not fixes — optional recommendations)

1. **The accepted README-drift gap** — a README-side number edit is not
   machine-caught; accepted because the values are triple-pinned at the file
   level (see the reviewer's judgment above).
2. **A future echo-semantics tightening on the staleness pin** — assert the
   FRESH tree carries the abs path in exactly the two expected files; closes
   the narrow blind spot where an "absolutizes-the-echo" regression would
   stay green.
3. **The reviewer nit:** "repo root" vs "project root" wording in the
   vendored arrangement — cosmetic, fold on next touch.

## Open boundaries

- **Push:** the P-040 commits pushed to the dev branch AFTER close by the
  orchestrator under the standing go. **NOT merged** — the merge remains a
  user gate (merge base `2c09428`; the branch carries P-039 + P-040 +
  closes).
- **Next per the USER'S SEQUENCE = THE THIRD PRODUCER — ★ USER-GATED on
  WHICH producer + the grounding** (the standing honesty policy:
  hand-curated-documented → high; derived → low, labeled; LLM-synthesized →
  draft-only, never high). What it costs now: a JSON file + three required
  declarations (`protect_iconic_loops`, `vocal_blend_policy`,
  `confidence_map`) + its own verbatim map pin + a differential test + a
  sample tree/README column if desired — ZERO code changes (the P-039
  surfaces scan the producers dir). Then deeper mode-forking. The
  orchestrator presents the decision; do NOT open blind.

---
_Closed by the archivist (2026-07-02). qa GREEN (806 / 93/93 / Commit-1 iso /
freshness independent / sabotage bites / safety grep clean) + reviewer PASS
(no must-fix; single-model — Codex unavailable)._
