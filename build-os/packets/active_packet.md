# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "Build what's next" (2026-07-04).
  Of the open directions, this is the ONLY substantive one requiring NO user
  taste/product decision (CLA's aesthetic is already authored, proven, and
  merged in PR #29) — it is the established P-046/P-048 surface-refresh
  pattern applied to the fifth producer. The taste-gated directions (a sixth
  producer, the Eno-deferral analyzers, quincy/halee dropout reach,
  apply-to-Logic) stay USER-GATED and are NOT touched here.
- **ID / Title:** **P-053 — Product-Surface Refresh: The Five-Producer
  Roster (+ residue sweep)**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop the unmerged
  P-052 (`2e4d5db`), merge base with default `f6cc9b7` (= PR #29). This
  packet STACKS on P-052 on the same dev branch; verify the chain with
  `git merge-base` + `git log`.
- **Baseline to protect:** suite **1291** / regression **93/93** / the five
  producers byte-stable / the four existing committed sample trees + nine
  mode demos byte-stable / ZERO engine/profile/analyzer change (this is a
  surface / test / docs packet).

## Why this packet (the gap)

Five producers are merged (halee_ramone · timbaland · quincy_jones ·
brian_eno · **chris_lord_alge**), but the committed product surface still
shows only FOUR: `examples/` has four sample trees (no CLA) and
`examples/mode_demos/` has nine demos (no CLA). The README says "Four
producers, same stems." The surface is stale relative to the roster —
exactly the "substrate ahead of surface" gap the user closed at P-046 and
P-048. This packet makes the surface reflect all five, faithfully, and
sweeps the two small accepted residues while in those files.

## Scope

1. **A fifth committed sample tree** — `examples/sample_output_chris_lord_alge/`
   (match the existing producer-stem naming: `_timbaland`/`_quincy`/`_eno`;
   builder confirms the exact dir name), rendered by the REAL CLI from
   `vocal_chop_groove` with `--producer chris_lord_alge`, relative stems
   paths only (the P-040 normalization if the artifacts echo stems paths),
   the full artifact tree — a FAITHFUL render, no hand-editing. Capture the
   real headline values first (CLA overall on chop = 67.8 per the five-way
   pin; vocal_role_fit / loop_context read from the rendered
   doctrine_score.json — do NOT trust prompt numbers), then pin.
2. **CLA mode demos** — extend `examples/mode_demos/` with CLA following the
   P-048 pattern: at minimum his `conservative` demo (making the "same mode,
   N producers" comparison five-wide) and one CLA-signature mode demo (e.g.
   `commit_and_slam` default vs `front_and_center`, or `drum_slam` — the
   builder picks the set that most clearly shows his impact/excitement
   behavior, captured-then-pinned). Faithful real-CLI creative pairs, the
   P-048 unit.
3. **Extend the exact-set guards (the conscious, anticipated extension):**
   - `tests/test_sample_refresh.py` — add the fifth tree to `SAMPLE_TREES`
     (the P-049 directory-set guard was DESIGNED for this: "a legitimate
     fifth tree = a one-line allowed-set extension"); the guard + the
     staleness pin auto-extend to it.
   - `tests/test_mode_demo_refresh.py` — add the new CLA demo dirs to
     `MODE_DEMOS`; the directory-set guard + staleness/surface pins
     auto-extend.
   Full P-040/P-046/P-048 strength: byte-equality vs fresh renders,
   no-absolute-path, per-tree/-demo counts, the declaration-surface pins.
4. **README refresh** (docs) — "Four producers, same stems" → "**Five**
   producers, same stems": add the CLA column (overall 67.8 + his
   vocal_role_fit / loop_context from the rendered tree — every number a
   pinned/rendered value); one center-of-gravity sentence for CLA
   (impact/excitement — the loudness-forward anti-Eno); update the
   modes-are-behavior section if CLA demos are added; sweep stale
   four/five-producer wording (the P-038 discipline).
5. **Residue sweep (fold in — both are accepted standing notes):**
   - README "32 commands" → **35** (the registry is 35 — stale since the
     cowork registry grew; verify `len(cowork.COMMANDS)`).
   - The sample-staleness-pin nested-subdir micro-hardening: add a
     `no-subdirectory` assertion to the sample-tree staleness pin (a nested
     stray subdir inside a `sample_output*` tree currently escapes the
     `is_file()` filter — the P-049 reviewer's one-line note). Apply the
     same guard to the new CLA tree.

## Non-scope (binding)

ZERO changes to engine code (.py under logic_mix_os/), profiles (all five
producer JSONs byte-unchanged), analyzers, fixtures, goldens, the MCP
surface (`cowork_mcp/`), `cli.py`, `cowork.py`. No new move families / reach
/ scoring / governance / safety changes. No sixth producer. No SDK swap /
apply-to-Logic. The FOUR existing sample trees + NINE existing mode demos
are NOT regenerated (a non-byte-identical fresh render of an existing
tree/demo = a discovered staleness bug → STOP and report). No merge until
qa + reviewer dual-green.

## Orchestrator recon (binding on the builder)

- The P-046 (sample trees) + P-048 (mode demos) receipts + their test files
  carry the exact render invocations + pin mechanics — EXTEND, don't
  reinvent. The P-049 guards were explicitly designed for a one-line
  allowed-set extension — use that path.
- Render into the repo via the real CLI with RELATIVE paths (mirror the
  existing trees' stems-path handling exactly).
- Every README number must equal a pinned/rendered value ("unpinned claims:
  none material" — the P-046/P-048 bar). No aspirational prose.
- Enumerate the exact suite growth per file.

## Required proof

suite clean · regression clean · zero engine/profile/analyzer/MCP change
(diff-proven) · the fifth tree + CLA demos are FAITHFUL real-CLI renders
(byte-equal to fresh renders) · the four existing trees + nine existing
demos byte-UNCHANGED (their pins pass without regeneration) · the P-049
directory-set guards now assert FIVE trees + the extended demo set exactly ·
the nested-subdir micro-hardening bites · README numbers all pinned ·
producer/loudness safety doctrine untouched.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the CLA sample tree + CLA mode demos + the pin/guard
  extensions + the nested-subdir micro-hardening — full suite green in
  isolation; the four existing trees + nine existing demos byte-untouched.
- **Commit-2:** README refresh + the "32→35" fix (docs only, zero
  collection change).

---
_Set active by the orchestrator on the user's "Build what's next"
(2026-07-04) — the one decision-free open direction. One packet at a time:
builder → qa + reviewer → archivist → receipt._
