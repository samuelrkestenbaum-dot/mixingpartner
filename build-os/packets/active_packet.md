# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-028
- **Title:** Source `doctrine_engine.py`'s producer constants from the profile (byte-identical, WIDENED — the last & largest extraction)

## Why (producer-agnostic epic — final extraction)

Last extraction step. Source `doctrine_engine.py`'s producer-specific judgment
from `load_profile("halee_ramone")` (same byte-identical pattern as P-026/P-027)
AND — per Finding A — WIDEN the profile to capture ALL doctrine scoring functions'
constants, not just `_halee`/`_ramone`. After this, the reference profile fully
drives the judgment layer; regression 68/68 is the `halee_ramone`-profile guard.

## Authority

**Build / feature — in authority, byte-identical.** **Merge to default gated on
explicit go; dev-branch commits under standing push-go.**

## Scope (the builder implements EXACTLY this)

### Source ALL of `doctrine_engine.py`'s producer constants from the profile
1. `doctrine_engine.py` gets `_DEFAULT_PROFILE = load_profile("halee_ramone")`.
2. **Already-captured (P-025) — now SOURCE them:** `score_doctrine`'s component
   `weights` (halee 1.0 / ramone 1.2 / vocal_centrality 1.2 / depth 1.0 / contrast
   1.0 / static 1.0 / dynamic 0.8), and `_halee`/`_ramone`'s baselines (86.0) +
   penalty coeffs — read from `_DEFAULT_PROFILE.doctrine.*` instead of inline.
3. **WIDEN + source the 5 remaining scoring functions' constants** (read each
   function body and capture EVERY producer-aesthetic literal — the grep below is
   a guide, not exhaustive; confirm against the code):
   - `_vocal_centrality`: no_lead return `35.0`, baseline `70.0`, the two `+10`
     bonuses, the `-6*len(bad)` masked penalty.
   - `_depth_hierarchy`: baseline `40 + distinct*12`, `fg_frac>0.6 →
     -(fg_frac-0.6)*60`, the `distinct<=1` handling.
   - `_section_contrast`: `100 - 18*lift_fail` (baseline 100, per-fail 18).
   - `_static_mix`: baseline `80.0`, `peak_dbfs>-0.1 → -10`, `bands[dominant]>0.55
     → -10`, `-8*len(crit_low)`, the `-8`.
   - `_dynamic_mix`: `<2 sections → 40.0`, baseline `30 + rms_std*8 +
     width_std*140 + bright_std*140`, `-10*lift_fail`.
   Extend `ProducerProfile` + `halee_ramone.json` + the round-trip test with a
   coherent `doctrine.scorers` structure (per-function: baseline/bonuses/
   penalties/coeffs/thresholds), captured VERBATIM. Then rewrite each function to
   READ its constants from `_DEFAULT_PROFILE` — byte-identical.
   - Keep the PHYSICS/measurement logic (fg_frac computation, band analysis,
     pstdev, section detection) in the function — only the aesthetic CONSTANTS
     move to the profile. The formula SHAPE stays; only its numbers are sourced.

### Invariants
- **Byte-identical:** existing doctrine/`doctrine_score` tests + regression 68/68
  pass UNCHANGED. The 68 golden regression is the corpus-level byte-identical
  proof (doctrine feeds `doctrine_score`, which the golden pins). If ANY
  `doctrine_score` value changes, STOP and report — a wrong captured constant.
- **NO-ALIASING PROOF (BINDING):** grep `doctrine_engine.py` for in-place mutation
  of the sourced structures; add a no-aliasing test (run `score_doctrine` on a
  fixture, assert the shared `_DEFAULT_PROFILE` structures byte-unchanged after) +
  a determinism check.
- Do NOT touch `creative.py`/`governance.py` (done) or `pipeline.py` (P-029). No
  per-call profile threading yet.

### Tests — test-first
- Round-trip for the NEW `doctrine.scorers` fields (exact + drive-the-function
  indirect, like P-025's doctrine round-trips), extending `tests/test_producer_profile.py`.
- Value-pins + the no-aliasing test (extend/new doctrine test file).
- Byte-identical: existing doctrine tests + regression 68/68 UNCHANGED.

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network.

## Constraints

- **≤2 commits.** Split cleanly (e.g. Commit-1: source the already-captured
  weights/halee/ramone + no-aliasing test, green in isolation; Commit-2: widen +
  source the 5 remaining functions + round-trip). Commit-1 green in isolation.
- **Byte-identical** — if any `doctrine_score` output or regression changes, STOP
  and report (a captured constant is wrong). This is the whole point.
- **No external mutation.** Author/committer `Claude <noreply@anthropic.com>`;
  trailers required (`Co-Authored-By: Claude Opus 4.8` is the mandated form —
  include it).

## Expected proof (qa to report exact)

- Full suite **351 → 351+N passed** (0 failed/skipped/warnings, green under
  `-W error`) — existing doctrine tests pass UNEDITED.
- Regression **68/68, 0 critical, 0 warnings** held — the corpus byte-identical
  proof (doctrine drives `doctrine_score`, golden-pinned).
- Commit-1 green in isolation.
- **Byte-identical doctrine proven** (regression 68/68 + `doctrine_score`
  unchanged on fixtures) + **no-aliasing proven** + the 5 widened scoring
  functions now profile-sourced & round-trip-guarded. `creative.py`/`governance.py`/
  `pipeline.py` untouched. Safety grep clean; UI N/A.

## Honesty clause
If a doctrine constant is woven into a formula such that it can't be cleanly
sourced without changing the formula's numeric result, STOP and report with
evidence rather than forcing it (byte-identical is non-negotiable here — the
golden regression will catch any drift, so a drift is a hard stop, not a paper-over).

---
_Confirmed as active by the orchestrator-in-chief (P-028), the last & largest
extraction of the producer-agnostic epic. One packet at a time._
