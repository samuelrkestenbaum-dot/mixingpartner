# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-010
- **Title:** Album context into per-song planning (opt-in, bounded, evidence-tagged)
- **Authority:** build (trajectory-advancing — opens the cross-song coherence axis)

## Why (trajectory)

`analyze_album` computes cross-song coherence but only post-hoc reports it; a
song's plan never sees its siblings. P-010 threads an opt-in `album_context` into
`analyze()` so an album-outlier song gets ONE bounded, evidence-tagged,
non-destructive next-pass item — turning a song tool into an album tool. Same
opt-in seam proven by P-007/P-008/P-009.

## ⚠️ HARD BACKWARD-COMPAT GATE

`album_context=None` (default) → everything byte-identical to today (143 tests +
68 invariants green; goldens' `next_pass` titles unchanged). The guidance appears
ONLY when an album_context is supplied. (The `evidence`-style key appears only on
the new item, only when added.)

## `album_context` contract (resolved)

- `album.py` computes album MEANS inline (`:57-58`) but DISCARDS per-song deltas
  (keeps only categorical `stands_out_on`). So P-010 derives the delta in the
  consumer; **`album.py` is NOT modified.**
- Shape (per-song dict): `{"brightness_delta": float|None, "lufs_delta": float|None}`.
  - `brightness_delta` = song brightness − album brightness mean (same quantity as
    `s["brightness"] - b_mean` at `album.py:61`).
  - `lufs_delta` = song lufs − album lufs mean (same as `s["lufs"] - l_mean` at `:63`).
  - `None` → no album signal for that axis → skip it. Fully-`None` → no item.

## Goal / "done" criteria (single, testable)

- With a hand-built `album_context` whose `brightness_delta` exceeds 0.15 (or
  `lufs_delta` exceeds 3), `plan_next_pass(...)` returns EXACTLY ONE new
  non-destructive item titled `"Album coherence"` whose `detail` names the signed
  album delta and which carries an `evidence` line, at a priority **strictly below**
  the song's truth-driven vocal move; AND `album_context=None` → the full `analyze()`
  artifact set is byte-identical to today.

## The ONE bounded item

- **Title:** `"Album coherence"` (fixed; deliberately NOT a `_MOVE_TARGET` key — so
  P-008's demote/revert never touches it — and not a golden title).
- **Detail:** names the signed delta, non-destructive/reversible, e.g. "This song
  sits +0.18 brighter than the album average. Consider matching the record's tonal
  centre — a gentle high-shelf / match-EQ toward the album, reversibly, before
  committing." Dark/loudness cases mirror the shape. If BOTH axes trip → ONE item
  on the larger-magnitude axis (deterministic tie-break: brightness before loudness).
- **Evidence line:** `"album outlier: brightness_delta=+0.18 vs album mean (threshold 0.15)"`.
- **Risk:** advisory, reversible, no `risk_class>=5`; no `"widen"`+`"lead vocal"`
  phrasing (so invariant #4 cannot trip).

## Outlier thresholds + priority (reuse album.py verbatim; bounded)

- Planner module constants (cite `album.py:61,63` in a comment; do NOT import album
  → avoid a planner→album dependency): `ALBUM_BRIGHTNESS_OUTLIER = 0.15`,
  `ALBUM_LUFS_OUTLIER = 3`, `ALBUM_OUTLIER_PRIORITY = 45`.
- Outlier iff `brightness_delta is not None and abs(...) > 0.15`, or
  `lufs_delta is not None and abs(...) > 3`.
- **Priority 45** — below every truth-driven move (Vocal 90, Section 80, Width 70,
  Depth 60, Low-end 50). Can NEVER outrank the vocal move. Additive (one tuple
  appended before the existing sort at `next_pass_planner.py:166`); reversible;
  modifies no existing candidate's priority.

## Determinism

- Pure function of the supplied `album_context` deltas + the two fixed thresholds.
  No time/IO/random.

## In scope

**Commit-1 (seam + planner edge + tests — green in isolation):**
1. `logic_mix_os/planners/next_pass_planner.py` — trailing `album_context: Optional[Dict] = None`
   on `plan_next_pass` (`:96-102`); the 3 constants; a pure
   `_album_outlier_item(album_context) -> Optional[Tuple[int, Dict]]`; append its tuple
   to `candidates` BEFORE the `if history:`/sort (`:163-166`) when truthy + tripping.
   Falsy → no append → byte-identical.
2. `logic_mix_os/pipeline.py` — trailing `album_context: Optional[Dict] = None` on
   `analyze()` (`:76-83`, after `memory_dir`); pass `album_context=album_context` into
   the `plan_next_pass(...)` call (`:209-212`).
3. `tests/test_album_context.py` (new) — (a) outlier context → the `"Album coherence"`
   item appears, named with signed delta + evidence, priority below vocal; (b)
   `None` + non-outlier (under threshold) → no item; (c) default-path byte-identical
   at `plan_next_pass` (titles/order vs no-arg); (d) determinism; (e) both-axes
   tie-break → brightness, one item only.

**Commit-2 (separable — two-pass CLI):**
4. `logic_mix_os/cli.py::_run_album` (`:331-353`) — two passes: pass 1 `analyze()` per
   song (as today) → `analyze_album(...)` for means; pass 2 re-run each song
   `analyze(..., album_context=<derived per-song delta>)` so the `album` command shows
   album-aware per-song guidance. + one CLI test. (If the CLI fixture work balloons,
   STOP and split as P-010b rather than a 3rd commit.)

## Out of scope (explicit)

- `album.py` itself (delta derived in the consumer); deeper creative `_KIND_SCORES`
  (separate); event-logging producers; the bridge; the other ~13 `analyze()` CLI
  call sites (incl. `_run_analyze`, `cowork`) — album-context-free by design; P-008's
  demote/revert logic.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `ed9e875` (clean, 31 ahead/0 behind).
  Default `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** files 1–3; passes its own tests
   standalone; suite 143→~148; regression 68/68.
2. **Commit 2 (separable):** file 4 + CLI test; suite green.

## Regression-safety argument

- Goldens (`regression.py:255`) run plain `analyze()` (no `album_context`) → planner
  no-op → candidate list identical. Goldens read `next_pass` TITLES only (`:82`) and
  `compare_snapshots` doesn't even diff titles (`:93-145`) → new title can't appear/be
  read on the default path → 68/68 holds. Invariant #4 (`:191-194`) doesn't run on the
  default path and the item has no `"widen"`+`"lead vocal"` collision anyway.

## Guardrails

- Build authority; deterministic; advisory/non-destructive/reversible item; no real
  DAW/network/AppleScript/`.logicx`/subprocess; bounded priority can't dominate truth
  moves; truth-lock/kill-switch unaffected (item is next-pass guidance, not a governed action).

---
_Confirmed P-010 on the user's "skate to where the puck" — opens the cross-song
coherence axis. Builder implements exactly this; archivist clears on close._
