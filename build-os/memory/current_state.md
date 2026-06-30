# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** Logic Mix OS — a local-first, deterministic mix-decision
  system that turns exported Logic Pro stems + a `project_manifest.json` into a
  section-aware, Logic-native **mix plan** (Roy Halee / Phil Ramone judgment
  layer). Not an auto-mixer, preset generator, or mastering tool. All product
  code lives under `logic-mix-os/`.
- **Primary branch / base:** default branch `claude/dreamy-turing-z0oxll` @
  `694d19d`; active dev branch `claude/logic-mix-os-hardening-12-7hbeh1`
  (P-011 product base `111f115`; P-011 product commits `effccd0` + `ea9bebf`
  local-only).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **159 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **THE ALBUM-MEANS TRUTH IS NOW SINGLE-SOURCED.** With **P-011**, the album
  means live in exactly ONE place: `album.py::analyze_album` additively emits
  per-song `brightness_delta` / `lufs_delta` (from the means it already computes)
  and `cli.py::_run_album` consumes them. The duplicate `statistics.mean`
  recompute (and the now-unused `import statistics`) that P-010 left in `cli.py`
  is gone — the two-place drift risk is killed. The `album` report stays
  value-identical (`coherence_score` / `outliers` / `verdict` unchanged); the only
  changed output is a deliberate display-only float-round of the
  `"Album coherence"` delta text (threshold logic still full-precision).
- **MILESTONE (still standing) — THE CROSS-SONG COHERENCE AXIS IS OPEN.** Via
  **P-010**, a song's plan (through the `album` command) reflects its album
  siblings: album-aware per-song guidance, opt-in / bounded / evidence-tagged. An
  album-outlier song receives ONE advisory `"Album coherence"` next-pass item at
  priority 45 (below every truth move — can never outrank Vocal). **The product is
  no longer strictly song-isolated.**
- **MILESTONE (still standing) — THE LEARNING LOOP IS REAL IN PRODUCTION.** The
  full arc **P-007 (consumer) → P-008 (outcome) → P-009 (live wire)** is closed
  end-to-end: a real `cowork --memory-dir` run both **learns** (records →
  history-aware next pass) and **personalizes** (taste → governance).
- **Last closed packet:** **P-011** — Album delta consolidation (mechanical
  refactor; golden-safe). `album.py::analyze_album` additively emits per-song
  `brightness_delta` / `lufs_delta`; `cli.py::_run_album` consumes them and drops
  the duplicate mean recompute + `import statistics`; `next_pass_planner.py`
  rounds the `"Album coherence"` DISPLAY delta (display-only). Commit-1 `effccd0`
  (album.py emit + cli.py consume + provenance test in `tests/test_cli.py`),
  Commit-2 `ea9bebf` (float-round + 4 tests in `tests/test_album_context.py`).
  Suite 155→**159**; regression 68/68 held; Commit-1 green in isolation
  (`effccd0`: 156 passed, 13 targeted, 68/68); **VALUE-IDENTITY proven exact**
  (emitted deltas == `song − statistics.mean(non-None)` for all 3 fixtures, 0
  mismatches; outlier threshold still full-precision — `0.151` trips `0.15`);
  scope = exactly 5 files; `creative`/`governance`/`memory`/`pipeline` untouched;
  safety grep none; UI N/A. Reviewer: **pass** (consolidation exact + additive;
  value-identity pinned; float-round display-only; kills the two-place
  album-means drift risk; Codex not available). Receipt:
  `build-os/receipts/P-011-album-delta-consolidation.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — THE CLEAN IN-AUTHORITY DECK-CLEARING WORK IS NOW DRAINED. The next
  decision is the USER'S.** The leading trajectory candidate, **deeper creative
  scoring** (`creative.py::_KIND_SCORES`), is **BLOCKED ON A USER AESTHETIC
  DECISION** — the table is a curated Halee/Ramone prior and the variant-scoring
  path is golden-unguarded (a bad change is silent). The user must pick:
  - **(a)** leave the table as-is;
  - **(b)** a bounded, evidence-tagged nudge layer ON TOP of the table
    (generalizing the `width_bloom −8`, capped so it never overturns the base),
    which the user reviews before ship; or
  - **(c)** a fuller song-derived rescoring.
  Do NOT open a creative-scoring packet until the user chooses a/b/c. Remaining
  in-authority follow-ups (borderline-song taste fixture flipping the governed
  winner through `analyze()`; wider `--memory-dir` CLI surface — partly a product
  question) and net-new event-logging producers (product decision) stay deferred.

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-011 close (2026-06-29)._
