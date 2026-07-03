# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "go" (2026-07-03) after the
  P-045 merge report, down the orchestrator's presented recommendation
  (product-surface refresh = highest value-per-cost; the user's standing
  pattern: demo/docs packets follow substrate packets — P-040 followed
  P-039).
- **ID / Title:** **P-046 — Product-Surface Refresh: The Four-Producer
  Demo**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `0a53bb5` (= PR #24 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1100** / regression **93/93** / the
  TWO EXISTING committed sample trees byte-stable (halee, timbaland — NOT
  regenerated) / zero engine or profile changes.

## Why this packet (the gap)

The samples/README still present a TWO-producer world (P-040-era):
`examples/sample_output/` (halee_ramone) + `examples/sample_output_timbaland/`
and a "Two producers, same stems" README section. Since then the product
grew: FOUR producers (quincy_jones P-041, brian_eno P-045), modes that
FORK BEHAVIOR (P-042), and three reach-gated extended move families
(P-043/P-044) — none of it visible on the product surface. This packet
makes the current system demonstrable, exactly the P-040 pattern.

## Scope

1. **Two NEW committed sample trees** (the P-040 pattern — rendered by
   the REAL CLI from `vocal_chop_groove`, relative stems paths only):
   - `examples/sample_output_quincy/` (`--producer quincy_jones`)
   - `examples/sample_output_eno/` (`--producer brian_eno`)
   Expected headline overalls (already pinned in the differential
   suites — the trees must agree): quincy **68.8**, eno **65.5**.
   Quincy's tree will carry his default-mode reach surface (his
   `arrangement_lift` default reaches the family since P-043 —
   `chorus_lift_E` in candidates + the declaration keys); Eno's default
   (`horizontal_time`) is authored-neutral → a clean zero-declaration
   tree. Both are FAITHFUL renders — whatever the real CLI emits is the
   demo; no hand-editing.
2. **Staleness pin extension**: `tests/test_sample_refresh.py` grows to
   pin ALL FOUR trees byte-for-byte against fresh renders (the full
   P-040 strength: byte equality, path normalization if needed,
   no-absolute-path assertion, per-tree file counts). The two existing
   trees stay byte-identical (their pins prove it — no regeneration).
3. **README refresh** (docs only):
   - "Two producers, same stems" → **"Four producers, same stems"**:
     the four invocations + a four-way table (overall / vocal_role_fit /
     loop_context on the chop fixture — exact values from the rendered
     trees, which must match the standing pins 76.3/60.9/68.8/65.5).
   - A **"Modes are behavior"** subsection: one non-default-mode
     invocation example (e.g. `--producer timbaland` with a reaching
     mode, or point at the committed timbaland tree's live
     `search_mode_declarations`/`mode_fork` surface it has carried since
     P-044) explaining favor/suppress/reach in a paragraph.
   - An **extended-families note**: the three reach-gated families in
     one honest paragraph, INCLUDING the safety line verbatim for
     dropout: "dropout is an arrangement proposal, not a destructive
     operation."
   - The producer-roster line wherever the README enumerates profiles
     (grep for stale two/three-producer wording — the P-038 discipline).
   - Every number in the README must equal a pinned value; no
     aspirational prose.

## Non-scope (binding)

ZERO changes to engine code, profiles, analyzers, fixtures, goldens.
No new move families, no reach changes, no CLI changes. No fifth
producer. The two EXISTING trees are not regenerated (if a fresh render
of an existing tree is NOT byte-identical, that is a discovered
staleness bug — STOP and report, do not silently regenerate). No merge
until qa + reviewer dual-green (the merge stays a user gate).

## Orchestrator recon (binding on the builder)

- The P-040 receipt + `tests/test_sample_refresh.py` carry the exact
  render invocations and the pin mechanics — extend, don't reinvent.
  Check what the P-040 headline pin asserts about README content and
  update it consciously (enumerated).
- `tests/test_producer_cli.py::DEMO_OVERALLS` pins {halee 76.3,
  timbaland 60.9} — extending it to four (or leaving it and pinning the
  new pair in the sample-refresh suite) is the builder's call,
  enumerated either way.
- Render into the repo via the real CLI with RELATIVE paths (the P-040
  abs→rel normalization lesson — check how the existing trees handle
  stems paths and mirror it exactly).
- The suite will grow only by the new/extended pins — enumerate the
  arithmetic exactly.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the two new trees + the staleness-pin extension (+ any
  DEMO_OVERALLS extension) — full suite green in isolation; the two
  existing trees byte-untouched.
- **Commit-2:** README only (the P-040 shape).

---
_Set active by the orchestrator on the user's "go" (2026-07-03). One
packet at a time: builder → qa + reviewer → archivist → receipt._
