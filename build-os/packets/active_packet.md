# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-039 confirmed by the orchestrator-in-chief on the
  USER'S GO (2026-07-02). Handed to builder.
- **Packet id:** P-039
- **Title:** Producer Selection CLI Exposure + Demo-Safe Invocation (the
  user's title). The first packet of the post-substrate product arc.

## Why (the user's puck read, verbatim in spirit)

The puck is not "more profiles" — it is making the second producer REACHABLE
and DEMONSTRABLE from the product surface: internal capability → operator/
product lever → repeatable demo → then the third producer. The `producer=`
lever has been live in the library since P-029; the CLI has never exposed it.

## THE ACCEPTANCE BAR (user-stated, verbatim)

```
same stems
explicit producer arg
clear selected producer in artifacts
Halee/Ramone remains default
Timbaland reachable without code changes
safety/governance unchanged
regression clean
```

## Spec

1. **`--producer` on every analyze-family CLI command** (the ~13 `analyze()`
   call sites: analyze, detect-identities, analyze-sections, generate-plan,
   creative, governance, mixer-feedback, memory-record, audit, status,
   dashboard, compare-reference where applicable, album per-project if
   sensible — the builder maps the exact set). Default `halee_ramone`
   (byte-for-byte today's behavior when omitted); value = any profile name
   resolvable by `load_profile` (`doctrine/producers/<name>.json`). Unknown
   name → the loader's clean FileNotFoundError surfaced as a friendly CLI
   error naming the available profiles (list the producers dir) — no
   traceback. Help text names the SEMANTICS, not a hardcoded profile list
   (the P-038 --mode precedent).
2. **Clear selected producer in artifacts** — an ADDITIVE identity surface,
   rendered from the PER-CALL profile (the P-029/P-031 threading pattern):
   - `doctrine_score.json`: an additive `producer` key carrying
     `{name, display_name, provenance, confidence}` from the loaded profile's
     metadata (machine-readable);
   - `mix_verdict.md`: a producer line near the top (e.g. "**Producer
     profile:** Roy Halee / Phil Ramone (halee_ramone)");
   - `status` / `dashboard` surfaces: the producer named where the verdict
     is already summarized (small, consistent).
   Wording observational; the schema updated additively (no
   additionalProperties conflicts — verify).
3. **Cowork passthrough (OPTIONAL rider):** if exposing the producer through
   the cowork ctx (`cli.py` cowork command + `cowork.py`) is genuinely small
   (≤ a few lines + tests), include it; otherwise STOP on the rider only and
   report the radius — the CLI commands are the packet.
4. **Demo-safe invocation proven end-to-end:** from the repo (fixtures
   generated), BOTH of these must work and be pinned by tests:
   ```
   logic-mix-os analyze --stems … --manifest … --out out_ref
   logic-mix-os analyze --stems … --manifest … --out out_tim --producer timbaland
   ```
   — same stems, two coherent artifact trees, each naming its producer, the
   known differential values (76.3 vs 60.9 on vocal_chop_groove or the
   equivalent on the chosen fixture), zero code changes needed.

## Pin interactions (pre-scoped — flip consciously, never weaken)

- **The differential-proof divergence audit** asserts exactly which
  doctrine_score keys DIFFER between producers — the new `producer` key
  differs BY DESIGN (like `confidence` already does): extend
  DIVERGENT_DOCTRINE_KEYS consciously.
- **Artifact-delta discipline:** the additive producer key/lines change
  artifacts on ALL runs (default included) — enumerate the exact delta
  (files + lines) as P-031/P-036/P-038 did; every score surface
  byte-identical; goldens must hold **93/93** (build_snapshot is
  categorical+scores — verify the new key is invisible to it, don't assume).
- Any test pinning full doctrine_score keysets or verdict headers: conscious
  flips, enumerated.

## The bar (established rigor)

- Suite green from the **768** baseline (+ the new tests); regression
  **93/93**; both profiles load; safety/governance surfaces untouched
  (kill-switches, risk classes, non-destructive — assert unchanged under
  both producers via the existing pins).
- ≤2 commits, Commit-1 green in isolation;
  `python fixtures/generate_fixtures.py` FIRST; observational language;
  trailers `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link; NO push/merge/remotes (orchestrator pushes).
- Anything beyond the spec: STOP and report.

## Context

- Default tip `2c09428` (the post-backlog batch, merged git-natively on the
  user's word). Dev branch restarted from it. Suite 768 / 93/93 / residue
  zero.

## The arc after (user-sequenced)

**P-039 (CLI exposure — ACTIVE) → sample refresh (Halee/Ramone vs Timbaland
demo outputs in examples/) → third producer → deeper mode-forking.** (The
analyzer extension already landed as P-034/P-035.)

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
