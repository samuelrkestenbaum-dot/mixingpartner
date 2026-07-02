# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-038 confirmed by the orchestrator-in-chief
  (2026-07-02; within the user's standing "Go for it" = sweep the residue,
  two packets). Handed to builder.

## Last-closed / context

- **P-037 ✓ CLOSED** — residue sweep 1 of 2 (code-behavior): six
  defensive/validation items, byte-identical on every artifact surface
  (240/240, proven twice). ★ THE REAL FINDING: NaN floors previously FAILED
  OPEN on raw dicts — now fail CLOSED. 1 + 1 review-fix commits
  (`cb566b1` + `5f94456`), qa GREEN + reviewer fix-then-pass → PASS.
  Suite baseline **767** / regression **93/93**. The branch carries
  **P-036 + P-037** (+ closes) atop merge base `dc921ec` (= PR #18) —
  pushed, NOT merged. Receipt:
  `build-os/receipts/P-037-code-behavior-sweep.md`.

## Active packet spec (confirmed): P-038 — residue sweep 2 of 2 (naming/prose)

- **Packet id:** P-038
- **Title:** residue sweep 2 of 2 — the NAMING/PROSE sweep. **THE LAST
  BACKLOG PACKET** before the batch merge decision.

### Scope (all from residue.md; prose/naming only)

1. **The three producer-named-VALUE surfaces** (the P-030 reviewer judgment
   call) — **SCOPE WITH CARE AGAINST THE GOLDENS:** the warning doctrine
   tags (`phil_ramone_vocal_centrality`/`phil_ramone_restraint`) may be
   GOLDEN-PINNED, and the search-mode names
   (`halee_depth`/`ramone_vocal_truth`) appear in emitted creative.json as
   VALUES — decide consciously per surface what may move and what the
   goldens/regression must absorb.
2. **The liveness-docstring sweep** (~8 files — the overclaiming `liveness`
   docstrings; ONE sweep across all affected files, see residue.md for the
   known list).
3. **`cli.py` `--mode` help text** — hardcodes the reference's mode names
   (goes stale as profiles diverge).
4. **The P-035 count-pin parenthetical tidy** — the mechanically-repeated
   "(P-035 moved the corpus count consciously…)" ~15× across 10 files.
5. **Fallback-reason wording** — "the profile's own default" even on the
   first-authored-mode branch (P-033 cosmetic).
6. **The two P-036 observations:** (A) the `heard`-qualifier shorthand
   ("…or a heard masker stands forward" — PAIR with the analyzer doc line);
   (B) the elliptical 65.0 attribution (tidy only if the entry is
   re-authored).

### The bar (inherit P-037's discipline)

- Suite green from the **767** baseline; regression **93/93**. Any surface
  the goldens pin moves ONLY as a conscious, documented golden/pin flip —
  never a silent regeneration.
- ≤2 commits, Commit-1 green in isolation;
  `python fixtures/generate_fixtures.py` FIRST; observational language;
  trailers `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link; NO push/merge/remotes.
- Anything beyond these six items: STOP and report.

### After P-038

- **The batch merge decision (P-036 + P-037 + P-038) on the user's word** —
  no merge without explicit go. Merge base `dc921ec` (= PR #18).

---
_P-037 cleared by the archivist on close (2026-07-02). P-038 staged, NOT
active until the orchestrator confirms on the user's go. One packet at a
time. Builder implements exactly this; qa proves; reviewer judges; archivist
closes with a receipt._
