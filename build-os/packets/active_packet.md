# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-029
- **Title:** Parameterize the pipeline by a per-call producer profile — `analyze(producer=…)` (THE PIVOT)

## Why (producer-agnostic epic — the pivot)

Extraction is complete (P-026/27/28): the judgment layer reads all producer-
specific values from `_DEFAULT_PROFILE = load_profile("halee_ramone")` (a module
singleton). P-029 threads a PER-CALL profile through the pipeline so
`analyze(producer=…)` SELECTS which profile drives the judgment — the profile
stops being a mirror of the reference and becomes a LIVE, selectable lever.
Default = the `halee_ramone` reference → **byte-identical** (guarded by regression
68/68). This is the first step where a different producer would produce a
different plan.

## Authority

**Build / feature — in authority, byte-identical default.** **Merge to default
gated on explicit go; dev-branch commits under standing push-go.**

## Scope (the builder implements EXACTLY this)

### Thread a per-call profile through the pipeline + judgment entry points
1. **`pipeline.analyze(..., producer: str = "halee_ramone")`** — add the opt-in
   param (default `"halee_ramone"`). Load `profile = load_profile(producer)` once,
   and pass it to the three judgment calls:
   - `score_doctrine(..., profile=profile)` (pipeline.py:154)
   - `run_creative_engine(result, mode, profile=profile)` (line 234)
   - `run_governance(result, result.creative, taste_profile=_taste, profile=profile)` (line 235)
2. **Entry points take `profile: Optional[ProducerProfile] = None`, defaulting to
   the module `_DEFAULT_PROFILE`** (so existing direct callers + the no-arg path
   stay byte-identical), and THREAD it to their callees:
   - `run_creative_engine` → `score_variant(variant, result, profile)`,
     `_apply_nudges(kind, result, profile)`, `_apply_promotions(...)`,
     `winning_variant`, search-mode selection — every function that currently
     reads a `creative` module global (`_KIND_SCORES`/`_NUDGE_TABLE`/
     `_PROMOTION_TABLE`/caps/`_RISK_PENALTY`/`SEARCH_MODES`) reads it from the
     passed `profile` instead.
   - `run_governance` → `govern_branches`/`govern_variant`/`taste_triangle`/
     `_apply_taste` — read `truth_alignment`/`taste_kind_bias`/`taste_max_delta`/
     `taste_triangle`/`veto_thresholds`/aesthetic kill-switches from `profile`.
   - `score_doctrine` → `_halee`/`_ramone`/`_vocal_centrality`/`_depth_hierarchy`/
     `_section_contrast`/`_static_mix`/`_dynamic_mix` — read their constants from
     `profile.doctrine`.
   Keep `_DEFAULT_PROFILE` as the DEFAULT when `profile is None`. The module
   globals (`_KIND_SCORES` etc.) may stay as the default-profile aliases for
   backward-compat, but the SCORING must read the PASSED profile when one is given.
3. **`analyze` also accepts a `ProducerProfile` object** for `producer` (name OR
   profile) — optional but convenient for tests; the builder's call. If name-only,
   the selection-liveness test needs another way to supply a second profile (see
   below).
4. Do NOT change any judgment VALUE. Do NOT touch the physics/analyzers. `pipeline`
   still writes the same artifacts. The safety kill-switches path is unchanged.

### The BINDING proof — selection is LIVE, not threaded-and-ignored (the P-016 lesson)
Byte-identical-by-default is necessary but NOT sufficient — a bug where the
profile is accepted but ignored would ALSO be byte-identical. So PROVE selection
is real:
- **Selection-liveness test:** construct/obtain a SECOND profile that differs from
  `halee_ramone` in ONE value (e.g. a `kind_score` or a doctrine coefficient),
  run the REAL `analyze()` with it (via `producer=<that profile/name>`), and
  assert the output DIFFERS from `analyze(producer="halee_ramone")` in the way
  that changed value predicts (e.g. a different `doctrine_score` component, or a
  different creative winner). The test must FAIL if the profile is ignored
  (i.e. if `analyze` doesn't actually thread the passed profile to the scorers).
  Choose the cleanest mechanism for the second profile (a synthetic
  `ProducerProfile` passed directly, a temp JSON, or a tiny test-only producer
  file) — but it must flow through the REAL `analyze()` path, not a monkeypatched
  scorer.

### Tests — test-first
- **Byte-identical default:** `analyze()` and `analyze(producer="halee_ramone")`
  produce identical artifacts vs pre-P-029 (regression 68/68; existing tests
  UNEDITED).
- **Selection-liveness** (above) — the load-bearing proof the lever is real.
- Determinism.

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network.

## Constraints

- **≤2 commits.** Split cleanly (e.g. Commit-1: thread creative + doctrine +
  pipeline wiring + byte-identical; Commit-2: governance threading + the
  selection-liveness test). Commit-1 green in isolation.
- **Byte-identical default** — if the no-arg / `producer="halee_ramone"` output
  changes at all, STOP and report.
- **No external mutation.** Author/committer `Claude <noreply@anthropic.com>`;
  trailers required (`Co-Authored-By: Claude Opus 4.8` is the mandated form).

## Expected proof (qa to report exact)

- Full suite **370 → 370+N passed** (0 failed/skipped/warnings, green under
  `-W error`) — existing tests UNEDITED.
- Regression **68/68, 0 critical, 0 warnings** held — the default-path byte-
  identical proof.
- Commit-1 green in isolation.
- **Byte-identical default proven** (no-arg == `producer="halee_ramone"` ==
  pre-P-029). **Selection-liveness proven load-bearing** (a different profile
  changes real `analyze()` output as predicted; fails if the profile is ignored).
  Physics/analyzers/safety untouched. Safety grep clean; UI N/A.

---
_Confirmed as active by the orchestrator-in-chief (P-029), the pivot of the
producer-agnostic epic — the profile becomes a live, selectable lever. One packet
at a time._
