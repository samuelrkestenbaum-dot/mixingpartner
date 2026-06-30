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
  `694d19d`; active dev branch `claude/logic-mix-os-hardening-12-7hbeh1` (P-010
  product base `ed9e875`; P-010 product commits `dc61f20` + `9ebd4ee` local-only).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **155 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **MILESTONE — THE CROSS-SONG COHERENCE AXIS IS NOW OPEN.** With **P-010**, a
  song's plan (via the `album` command) now reflects its album siblings:
  album-aware per-song guidance, opt-in / bounded / evidence-tagged. The `album`
  CLI runs two passes (pass 1 = album means; pass 2 = re-run each song with its
  delta) so an album-outlier song receives ONE advisory `"Album coherence"`
  next-pass item at priority 45 (below every truth move — can never outrank
  Vocal). **The product is no longer strictly song-isolated.** `album.py` itself
  is unchanged (the per-song delta is derived in the consumer, `cli.py`).
- **MILESTONE (still standing) — THE LEARNING LOOP IS REAL IN PRODUCTION.** The
  full arc **P-007 (consumer) → P-008 (outcome) → P-009 (live wire)** is closed
  end-to-end: a real `cowork --memory-dir` run both **learns** (records →
  history-aware next pass) and **personalizes** (taste → governance).
- **Last closed packet:** **P-010** — Album context into per-song planning
  (opt-in, bounded, evidence-tagged). `analyze()` gained an opt-in
  `album_context: {brightness_delta, lufs_delta}`; an album-outlier song
  (thresholds 0.15 brightness / 3 LUFS, verbatim from `album.py:61,63`, not
  imported) gets ONE `"Album coherence"` item at priority 45 via a pure
  `_album_outlier_item`. The `album` CLI is now two-pass. Commit-1 `dc61f20`
  (`next_pass_planner.py` + `pipeline.py` passthrough + `tests/test_album_context.py`
  new = 10 tests); Commit-2 `9ebd4ee` (`cli.py` two-pass + `import statistics` +
  `tests/test_cli.py` new = 2 tests). Suite 143→**155**; regression 68/68 held;
  **default path BYTE-IDENTICAL** (full `ProjectAnalysis` 91,406==91,406 chars, no
  `"Album coherence"` on the default path); Commit-1 green in isolation (153
  passed at `dc61f20`); CLI two-pass flags BOTH real outliers
  (`simple_vocal_piano_song` −0.289, `splice_loop_problem` +0.167) with
  coherence/outliers/verdict matching single-pass `analyze_album`. Reviewer:
  **pass** (priority 45 proven safe — 6th-ranked behind 5 native moves → dropped;
  CLI means byte-identical to `album.py:55-58`; thresholds verbatim + strict `>`;
  invariant-safe; deterministic; Codex not available). Receipt:
  `build-os/receipts/P-010-album-context-into-planning.md`.
- **Now:** **none active.** No product packet in flight.
- **Next:** orchestrator **re-survey** — user is driving via "skate to where the
  puck." Re-ranked candidates:
  - **Deeper creative scoring** — `creative.py::_KIND_SCORES` is hardcoded
    (verified NOT golden-blocked); now the **leading** trajectory candidate.
  - **`album.py` delta consolidation (P-011 candidate)** — `album.py:55-58` and
    `cli.py:367-370` both compute album means (byte-identical today); have
    `album.py` optionally EMIT per-song deltas and retire the consumer recompute.
  - **CLI advisory float rounding (cosmetic, from P-010 reviewer)** — `round(value,
    2)` for the `"Album coherence"` detail/evidence display.
  - **Loop-strengthening follow-ups (from P-009 reviewer):** a borderline-song
    taste fixture that flips the governed winner *through `analyze()`*; a wider
    `--memory-dir` CLI surface beyond `cowork`.
  - Net-new **event-logging** producers (`taste_feedback` / `validation_check`)
    remain behind the product decision.

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
_Updated by the archivist on close. Last advanced on P-010 close (2026-06-29)._
