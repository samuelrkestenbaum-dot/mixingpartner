# Receipt — P-010: Album context into per-song planning (opt-in, bounded, evidence-tagged)

- **Date:** 2026-06-29
- **Authority:** build (trajectory-advancing — opens the cross-song coherence axis)
- **Branch base (merge-base):** product base `ed9e875` on
  `claude/logic-mix-os-hardening-12-7hbeh1`; default branch
  `claude/dreamy-turing-z0oxll` @ `694d19d` (merge-base with default = `694d19d`).

## What it does

`analyze()` gained an opt-in `album_context: {brightness_delta, lufs_delta}` param.
When a song is an album outlier — thresholds **0.15** brightness / **3** LUFS,
lifted verbatim from `album.py:61,63` (cited in a comment; `album.py` is **not**
imported, to avoid a planner→album dependency) — `plan_next_pass` appends ONE
bounded, advisory, evidence-tagged `"Album coherence"` next-pass item at **priority
45**. Priority 45 sits below every truth-driven move (Vocal 90, Section 80, Width
70, Depth 60, Low-end 50), so the item can **never** outrank the vocal move. If
both axes trip, ONE item is emitted on the larger-magnitude axis (deterministic
tie-break: brightness before loudness). The item is deliberately NOT a
`_MOVE_TARGET` key (so P-008's demote/revert never touches it) and not a golden
title.

The `album` CLI (`_run_album`) now runs **two passes**: pass 1 builds album means
via `analyze_album` (`analyze()` per song as today); pass 2 re-runs each song with
its derived per-song delta as `album_context`, so the album report shows
**album-aware per-song guidance**. The per-song delta is derived in the consumer
(`cli.py`) — **`album.py` is NOT modified**. Default (`album_context=None`) is
byte-identical to before.

## Scope

- **In (Commit-1):** `logic_mix_os/planners/next_pass_planner.py` (the 3 constants
  `ALBUM_BRIGHTNESS_OUTLIER`/`ALBUM_LUFS_OUTLIER`/`ALBUM_OUTLIER_PRIORITY`, a pure
  `_album_outlier_item`, the opt-in trailing `album_context` arg);
  `logic_mix_os/pipeline.py` (passthrough into the `plan_next_pass` call);
  `tests/test_album_context.py` (new, 10 tests).
- **In (Commit-2):** `logic_mix_os/cli.py` (`_run_album` two-pass + `import
  statistics`); `tests/test_cli.py` (new, 2 tests).
- **Out (explicit):** `album.py` itself (delta derived in the consumer); deeper
  creative `_KIND_SCORES`; net-new event-logging producers; the other ~13
  `analyze()` CLI call sites (incl. `_run_analyze`, `cowork`) — album-context-free
  by design; P-008's demote/revert logic.

## Commits

- `dc61f20` P-010: thread opt-in album_context into the next-pass planner
  (Commit-1: `pipeline.py` +2, `next_pass_planner.py` +76, `tests/test_album_context.py`
  new = 256 insertions; planner + pipeline + new test).
- `9ebd4ee` P-010: two-pass album CLI for album-aware per-song guidance
  (Commit-2: `cli.py` +28/−1, `tests/test_cli.py` new = 123 insertions, 1 deletion;
  CLI two-pass + new test).
- `7c494b4` Confirm P-010 ... as active packet — **non-product** memory commit
  (`build-os/packets/active_packet.md` only).

Diff `dc61f20^..9ebd4ee` touches **exactly** the 5 product files listed In-scope.
`album.py` source is **not** in the diff (the only "album" path is the new test
`tests/test_album_context.py`).

## QA proof (GREEN)

- **Suite:** `python -m pytest` → **155 passed**, 0 failed, 0 skipped, 0 warnings.
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68**, 0 critical,
  0 warnings.
- **Commit-1 iso:** worktree checked out at `dc61f20` → **153 passed** (30 targeted
  on the new/touched suites), regression **68/68** → green in isolation.
- **Default path BYTE-IDENTICAL:** full `ProjectAnalysis` dump exact string-equal
  with `album_context=None` vs no-arg — **91,406 == 91,406 chars**; no `"Album
  coherence"` anywhere on the default path. (The HARD backward-compat gate held.)
- **End-to-end positive control (planner):** an outlier `album_context` yields the
  `"Album coherence"` item at **rank 5 < vocal rank 1**, with the signed delta in
  the detail and a correct `evidence` line.
- **End-to-end positive control (CLI two-pass):** the `album` command flags BOTH
  real outliers in the fixture — `simple_vocal_piano_song` (−0.289) and
  `splice_loop_problem` (+0.167) — and its `coherence_score` / `outliers` /
  `verdict` **MATCH** single-pass `analyze_album` (CLI-derived means are
  byte-identical to `album.py:55-58`, so it flags the same songs).
- **Scope grep:** exactly the 5 product files changed; `album` (source),
  `governance`, `memory`, `creative` modules untouched.
- **Safety grep:** clean — no real DAW / network / AppleScript / `.logicx` write /
  subprocess introduced.
- **UI smoke:** N/A (no UI surface in this packet).

## Review

- **Verdict: pass.**
  - Backward-compat byte-identical (the hard gate).
  - Priority **45** proven safe: 6th-ranked behind 5 native truth moves → dropped
    off the surfaced list, never outranks Vocal.
  - CLI album means are byte-identical to `album.py:55-58` → flags the same songs
    as `analyze_album`.
  - Thresholds reused **verbatim** (0.15 / 3) with strict `>`.
  - Invariant-safe: the item carries no `"widen"`+`"lead vocal"` phrasing
    (invariant #4 can't trip) and no `risk_class>=5`.
  - Determinism: pure function of the supplied deltas + the two fixed thresholds;
    no time / IO / random.
  - Test-first reproduced: the missing CLI two-pass arg first raised a `TypeError`
    via the real `cli.main` entrypoint, then went green.
- **Codex second-eyes:** NOT available.
- **Product Trajectory Check:** opens the cross-song coherence axis — the product
  is no longer strictly song-isolated; a song's plan (via the `album` command) now
  reflects its album siblings, opt-in / bounded / evidence-tagged.

## Residue

- **Deferred / follow-up packets (non-blocking, from the reviewer):**
  - **CLI advisory float rounding (cosmetic):** the `"Album coherence"` detail /
    evidence print a real CLI-derived delta with a long un-rounded float repr; apply
    `round(value, 2)` for display in a future packet. Display-only — the
    planner-level tests use clean literals.
  - **Mean-derivation consolidation (P-011 candidate):** `album.py:55-58` and
    `cli.py:367-370` now both compute the album means (currently byte-identical). A
    future packet could have `album.py` optionally EMIT per-song deltas, retiring the
    consumer-side recompute and removing the duplication.
- **Known risks:** commits on this branch are unsigned (empty 0-byte SSH signing
  key; container runs as root → signing impossible). Author + committer are correct
  (`noreply@anthropic.com`); GitHub will show "Unverified" (missing signature only,
  not misattribution) — an environment limitation, not a fix-it item.

## Open boundaries (awaiting explicit go)

- P-010's product commits `dc61f20` + `9ebd4ee` are **local-only** as of this close
  (no push performed). Any push updates the already-open **PR #13** (base
  `claude/dreamy-turing-z0oxll`) and only under the user's standing/explicit
  push-go. No merge / deploy / secret action taken.
