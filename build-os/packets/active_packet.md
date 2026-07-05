# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "Go" (2026-07-05) after the P-054
  merge (PR #32 → default `7af1e3e`). This is the LAST clean decision-free
  direction (the P-054 residue named it): the numeric drift guard is done;
  this completes the README-drift-guard family by pinning the spelled-out
  PROSE counts. **After this packet the remaining open directions all need a
  real user decision** (which producer / which analyzer / whether to
  authorize apply-to-Logic) — the orchestrator will present, not pick.
- **ID / Title:** **P-055 — README Prose-Count Guard**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `7af1e3e` (= PR #32 merge — the branch was fast-forwarded to it, clean;
  verify with `git merge-base`).
- **Baseline to protect:** suite **1302** / regression **93/93** / the five
  producers + five sample trees + eleven mode demos byte-stable / ZERO
  engine/profile/analyzer/MCP/runtime change (a test + docs packet).

## Why this packet (the P-054 residue)

P-054 pinned the README's numeric values (command count, regression
example, table) against live sources — but the spelled-out PROSE counts are
still unguarded, and they are the ones that WILL drift on the next producer
or demo addition. The README currently states (verified, all correct
today):
- "five committed trees" / "five committed sample trees" / "all five
  producers" / "five trees" (~lines 63, 81, 159, 163, 221, 497)
- "eleven producer × mode runs" / "eleven directories" / "eleven committed
  … creative pairs" (~lines 76, 222, 498)
- "the four example projects" / "across four fixtures" (~lines 46, 510)
- "Of the eleven demos, seven win exactly the moves the neutral …" (~line
  343 — a computed split)

Nothing pins these to their live sources. This packet does, so a sixth
producer / twelfth demo / different fixture count forces the prose to
update or the suite fails loudly — the same class as P-054's numbers, one
abstraction level up.

## Scope (tests + docs only)

1. **Audit the prose counts** — confirm each currently matches its live
   source (they appear correct post-P-053; if ANY is stale, FIX it and
   report — same discipline as P-054's audit).
2. **The prose-count guard** — extend `tests/test_readme_numbers.py` (or a
   sibling `tests/test_readme_prose_counts.py` — builder's call) with
   TARGETED, anchored assertions that map each spelled-out count word to an
   int and compare to a LIVE/COMMITTED source:
   - **"five" (trees / producers):** the tree-count and producer-count
     prose == `len(SAMPLE_TREES)` (imported from test_sample_refresh — the
     single source; == the number of shipped producer profiles). Pin every
     load-bearing "five … trees/producers" phrase the recon lists.
   - **"eleven" (demos / runs / directories / pairs):** == `len(MODE_DEMOS)`
     (imported from test_mode_demo_refresh).
   - **"four" (fixtures / example projects):** == the number of generated
     fixtures (derive from the generator / the fixtures dir / an existing
     fixture-list constant — the single source, not a hardcode).
   - **(If cleanly derivable) the "seven win / four deviate" split** at
     ~line 343: the count of committed demos whose winner == the neutral
     winner, derived from the committed demo bytes + the neutral baseline
     (reuse the WINNERS pin machinery). If it is NOT cleanly derivable
     without new plumbing, DO NOT force it — flag it as residue and pin the
     three length-derived classes only. Report the decision.
   - A small word→int map (three…twelve is plenty) + anchored phrase
     extraction; fail loudly naming the drifted phrase + its live source;
     robust — do NOT trip on incidental prose numbers (anchor to the
     specific "N <noun>" phrases, like P-054's approach).
   The guard must BITE: prove (scratch) that changing a prose count (e.g.
   "eleven" → "twelve") fails the guard; restore.

## Non-scope (binding)

ZERO changes to engine code (.py under logic_mix_os/), profiles, analyzers,
fixtures, goldens, the MCP surface, cli.py, cowork.py, the sample trees, the
mode demos. No new producers / families / analyzers / dependencies. No
safety/governance changes. No general README rewrite — only stale-count
fixes (if any) + the guard; do NOT sweep unrelated prose or pin non-count
words. No merge until qa + reviewer dual-green.

## Orchestrator recon (binding on the builder)

- The prose counts + their line refs are in "Why this packet" above (from
  a live grep). All appear CORRECT today — so expect the guard + possibly
  zero fixes (a clean audit). If one is stale, that is a real find → fix +
  report.
- DERIVE every expected count from the existing single source
  (`SAMPLE_TREES`, `MODE_DEMOS`, the fixture list) — NO duplicated hardcode
  (the P-047/P-049/P-054 discipline). The point is that adding producer #6
  bumps `len(SAMPLE_TREES)` and the guard then DEMANDS the prose say "six".
- Robustness: anchored on the specific "<word> <noun>" phrases; a word→int
  map; deterministic; clear failure messages. Must not false-positive on
  incidental digits/words elsewhere ("four hard constraints", section refs,
  the numeric table already guarded by P-054, etc.).
- Keep it proportionate — this is the small tail of the drift-guard family,
  not a general NLP audit.

## Required proof

suite clean · regression clean · zero engine/runtime change (diff-proven) ·
every load-bearing prose count pinned to a live/committed source (derived,
not hardcoded) · the guard BITES on a prose-count drift · the "seven win"
split either pinned or consciously flagged as residue · whole-README audit
shows no currently-stale prose count (or the stale one fixed) · the five
trees + eleven demos byte-untouched.

## Commit shape (1 commit expected; ≤2)

- **Commit-1:** the prose-count guard (+ any stale-count fix the audit
  surfaces) — full suite green in isolation. If the audit is clean, this is
  guard-only; if a fix is needed, it lands in the same commit so the guard
  is green.

---
_Set active by the orchestrator on the user's "Go" (2026-07-05), after the
P-054 merge — the last decision-free direction. One packet at a time:
builder → qa + reviewer → archivist → receipt._
