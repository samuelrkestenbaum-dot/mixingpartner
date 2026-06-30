# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-011
- **Title:** Album delta consolidation — `album.py` emits per-song deltas; `cli.py` stops recomputing
- **Authority:** build (mechanical refactor — hardens the cross-song axis; golden-safe)

## Why

P-010 left the album means computed in TWO places: `album.py:54-58` (its own
outlier detection) and `cli.py:360-368` (re-derives the same means to feed
`album_context`). Currently byte-identical (P-010 QA proved it), but that's a
two-place truth that can silently drift under future album work. P-011
single-sources it: `album.py` emits the per-song deltas it already has in scope;
`cli.py` consumes them. Also folds in the cosmetic CLI float-round the P-010
reviewer flagged.

## Goal / "done" criteria (single, testable)

- `album.py::analyze_album` additively emits per-song `brightness_delta` /
  `lufs_delta` (new keys; existing output a strict superset). `cli.py::_run_album`
  consumes those instead of recomputing `statistics.mean` — the duplicate mean
  block is removed. A new test asserts `album.py`'s emitted delta **equals** the
  value `cli.py` computed before. Regression stays 68/68; existing album/CLI tests
  green.

## Backward-compat

- The emitted delta keys are **additive** → `analyze_album`'s prior keys unchanged.
- Goldens read `doctrine_score` + `next_pass_titles` only — NOT album deltas — so
  **no golden moves; regression stays 68/68.**
- The consolidated delta is **provably equal** to today's `cli.py` recompute (same
  source dicts, same non-None filter, same `statistics.mean`) → the `album` report's
  `coherence_score`/`outliers`/`verdict` and the per-song `Album coherence` items
  are unchanged in VALUE.
- **The ONE intentional output change:** the cosmetic float-round (Commit-2) changes
  the *displayed* delta text in the `"Album coherence"` detail/evidence (long float
  → `round(value, 2)`). Covered by a test; flagged as deliberate, not a regression.

## In scope

**Commit-1 (album.py emit + test — byte-identical consolidation):**
1. `logic_mix_os/album.py::analyze_album` — additively emit per-song
   `brightness_delta = song.brightness − b_mean` and `lufs_delta = song.lufs − l_mean`
   (reuse the means already computed at `:54-58`; `None` when a metric/mean is
   unavailable). No change to existing keys / outlier logic.
2. `logic_mix_os/cli.py::_run_album` — consume `analyze_album`'s emitted deltas to
   build the per-song `album_context`; **remove** the duplicate `statistics.mean`
   recompute block (`:360-368`). The `album` report stays value-identical.
3. `tests/test_album_context.py` or `tests/test_cli.py` — a test asserting the
   `album.py`-emitted delta equals the prior consumer-computed delta (provenance
   single-sourced).

**Commit-2 (cosmetic float-round — the one intentional display change):**
4. The `"Album coherence"` detail/evidence display in `_album_outlier_item`
   (`next_pass_planner.py`) — `round(value, 2)` for the signed delta in the rendered
   text (planner-level tests use clean literals, so update/extend as needed). + a
   test asserting a long-float delta renders rounded.

## Out of scope (explicit)

- **Deeper creative scoring / `_KIND_SCORES`** — a curated Halee/Ramone aesthetic +
  golden-unguarded → a PRODUCT/AESTHETIC DECISION for the user, NOT this packet.
- Event-logging producers (product decision); loop-strengthening (separate);
  governance/memory/the learning-loop seams.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `111f115` (clean). Default
  `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** `album.py` emit + `cli.py` consume
   + provenance test; the `album` report stays value-identical; suite green;
   regression 68/68.
2. **Commit 2:** the cosmetic float-round + its test.

## Regression-safety

- Goldens (`regression.py:255`) run plain `analyze()` / read `doctrine_score` +
  `next_pass_titles`, never album deltas or `per_song_next_pass` text → 68/68 holds.
  The new `album.py` keys are additive; the consolidated delta equals today's value.

## Guardrails

- Build authority; deterministic; local-only; no network/subprocess/DAW/`.logicx`.
  No behavior change beyond the deliberate, tested float-round display.

---
_Confirmed P-011 — the conservative in-authority move (deck-clearing for the
cross-song axis) while the deeper-creative-scoring AESTHETIC DECISION is surfaced
to the user. Builder implements exactly this; archivist clears on close._
