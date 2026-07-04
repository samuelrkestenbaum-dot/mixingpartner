# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "Ok go" (2026-07-04) after the
  P-048 merge report. Of the presented directions, this is the ONLY one
  requiring no user taste/product decision (pure suite hardening — the
  P-048 reviewer's named candidate); the fifth producer, the analyzer
  candidates, and quincy/halee dropout reach remain user-gated and are
  NOT touched here.
- **ID / Title:** **P-049 — Committed-Example Directory-Set Guards**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `7ae96f2` (= PR #27 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1143** / regression **93/93** / all
  committed example artifacts byte-stable / ZERO runtime changes — tests
  only.

## Why this packet (the P-048 reviewer residue, verbatim)

"Nothing asserts `examples/mode_demos/` contains EXACTLY the nine pinned
directories — a tenth unpinned demo dir could land silently. This matches
the existing convention (test_sample_refresh.py also hardcodes its tree
dict with no directory-set guard), so it is a suite-wide hardening
candidate." An unpinned committed example is a silent product-surface
liability: it ships, drifts stale, and nothing catches it.

## Scope (tests only — one conscious guard per committed-example home)

1. `tests/test_mode_demo_refresh.py`: assert `examples/mode_demos/`
   contains EXACTLY the nine pinned demo directories (and nothing else —
   no stray files at that level beyond any documented README).
2. `tests/test_sample_refresh.py`: assert the `examples/` sample-tree
   set is EXACTLY the four pinned trees (`sample_output`,
   `sample_output_timbaland`, `sample_output_quincy`,
   `sample_output_eno`) — scoped so the guard covers the sample-tree
   naming pattern without false-positiving on the OTHER legitimate
   `examples/` residents (mode_demos/, project_manifest.example.json —
   enumerate the full allowed set consciously after LOOKING at the real
   directory).
3. The guards fail LOUDLY on: a new unpinned dir, a deleted pinned dir,
   a stray file. Adding a legitimate fifth tree/tenth demo later = a
   conscious one-line extension of the allowed set (state this in the
   guard's docstring — the same conscious-extension semantics as the
   P-047 data tables).

## Non-scope (binding)

Tests only — zero changes to engine code, profiles, fixtures, goldens,
committed examples, README. No new demo artifacts. No renames. Nothing
else rides. No merge until qa + reviewer dual-green (the merge stays a
user gate).

## Commit shape (1 commit — this packet is small by design)

- **Commit-1 (only):** the two guard additions — full suite green.
  (≤2 commits allowed; one suffices. Commit-1 green in isolation is
  trivially the HEAD proof.)

## Open user gates carried (NOT this packet's to touch)

The fifth producer (who + grounding) · the future-analyzer candidates
from Eno's deferrals · quincy/halee authored dropout reach — all await
the user's call.

---
_Set active by the orchestrator on the user's "Ok go" (2026-07-04). One
packet at a time: builder → qa + reviewer → archivist → receipt._
