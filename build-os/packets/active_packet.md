# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-040 confirmed by the orchestrator-in-chief
  (2026-07-02; next per the USER'S SEQUENCE, shape chosen by the orchestrator
  per the user's delegation). Handed to builder.
- **Packet id:** P-040
- **Title:** the SAMPLE REFRESH — the two-producer demo output
  (`examples/` regenerated: same stems, both producers, side by side).

## Why (the user's sequence + the standing note)

Sequence: P-039 ✓ (CLI exposure) → **sample refresh** → third producer →
deeper mode-forking. This packet makes the differential VISIBLE without
running anything — the repeatable demo in committed form — and it CLEARS the
accepted P-038 standing note (the samples ship stale pre-P-036/P-038 prose:
producer-named action strings, stale verdict text, old contract-era
artifacts).

## The shape (orchestrator's call, per delegation)

**Two committed trees from the SAME fixture — `vocal_chop_groove` (the
differential's showcase: 76.3 vs 60.9, the blend policy live, the groove axes
reading genuinely):**

- `examples/sample_output/` — the REFERENCE run (halee_ramone; stays the
  default-named tree so existing README links keep working);
- `examples/sample_output_timbaland/` — the TIMBALAND run;
- a short **"Two producers, same stems"** README section: the invocation pair
  (`… --out out_ref` / `… --out out_tim --producer timbaland`), a compact
  side-by-side table (overall + the 3-4 most divergent readings + the plan
  reversal in one line each), and pointers into the two trees.

## Spec

1. **Regenerate both trees via the REAL CLI** (the P-039 demo path —
   `cli.main`/subprocess on the generated fixture), then commit the artifact
   trees. Deterministic: two consecutive regenerations byte-identical
   (the fixtures are seeded; prove it).
2. **README:** update the sample-output reference (it currently points at
   `examples/sample_output` as "a ready-made example" — refresh the wording
   for the two-tree shape) + the new differential section. Observational
   language; the numbers stated are the pinned ones.
3. **Note the fixture switch honestly:** the current `sample_output` derives
   from an older fixture/contract era. Check what (if anything) in docs/tests
   depends on its SPECIFIC content beyond test-9's OLD_KEYS guard — every
   dependency updated consciously, enumerated.
4. **Pin interactions (conscious, enumerated):** `test_contract_migration`
   test-9 (samples use new keys only — the regenerated trees satisfy it
   BETTER; verify both trees are covered or extend it consciously to both);
   any test reading `examples/` paths; nothing weakened. Consider adding a
   cheap guard: the committed sample trees match a freshly generated run
   (a staleness pin — so samples can never silently rot again; judgment call
   on cost, report the decision).

## The bar

- Suite green from the **801** baseline; regression **93/93** (samples are
  not goldens — verify no interaction); the ONLY tree changes under
  `examples/` + README + any consciously-flipped test pins; product code
  ZERO changes (this is a docs/demo packet — if regeneration surfaces a
  product defect, STOP and report).
- ≤2 commits, Commit-1 green in isolation;
  `python fixtures/generate_fixtures.py` FIRST; observational language;
  trailers `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link, ONCE; NO push/merge/remotes (orchestrator pushes).

## Context

- Merge base `2c09428`; the branch carries P-039 (+close) pushed. Suite 801 /
  93/93. The P-039 identity surface makes both trees self-describing.

## The arc after (user-sequenced)

**P-040 (sample refresh — ACTIVE) → the third producer → deeper
mode-forking.**

---
_Set active by the orchestrator-in-chief (2026-07-02). One packet at a time.
Builder implements exactly this; qa proves; reviewer judges; archivist closes
with a receipt._
