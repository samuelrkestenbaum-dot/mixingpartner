# Receipt — P-008: History-aware next pass (the OUTCOME side of the learning loop)

- **Date:** 2026-06-29
- **Authority:** build (trajectory work — outcome side of the learning loop)
- **Branch base (merge-base):** product base `8c18df7`; default branch
  `claude/dreamy-turing-z0oxll` @ `694d19d` (merge-base with HEAD verified =
  `694d19d`).

## What it does

`plan_next_pass` now consumes recorded mix-pass history — **opt-in, bounded,
evidence-tagged** — so the system stops re-recommending a move that just
regressed and can surface a revert.

- An optional **trailing `history` arg** (default `None`). Falsy history
  (`None` / `[]`) leaves the default path **byte-identical** — existing body and
  return are unchanged.
- A module-level **`_MOVE_TARGET` map** (move `title` → a `SCORE_KEYS` member)
  bridges history's score-keyed vocabulary (`got_worse` / `revert_candidates`,
  keyed by `memory.SCORE_KEYS`) to the planner's titled candidates. Titles with
  no clear target map to nothing and are left untouched (conservative).
- **Demote (never delete):** a move whose `_MOVE_TARGET` target is in
  `history[-1].got_worse` **AND** whose title is in `history[-1].next_recommended`
  has a fixed bounded **`HISTORY_DEMOTE = 40`** subtracted from its priority,
  **floored ≥ 0**. It drops in rank but **survives** — not deleted.
- **Revert surfacing:** when `history[-1].revert_candidates` is non-empty, a
  single non-destructive **`"Revert last pass"`** move surfaces at **priority 95**,
  its `detail` naming the deterministically-ordered regressed targets; deduped by
  title.
- **Evidence:** each history-touched candidate carries an `evidence` line; the
  key is **present ONLY when history actually moved it** (absent otherwise —
  P-007's `taste_adjustments` discipline). String-stable.
- Uses only **`history[-1]`** (most recent pass) — bounded/predictable.
  Deterministic: pure function of `(candidates, history[-1])`; fixed order; no
  time / IO / random.

## Scope

- **In:**
  - `logic_mix_os/planners/next_pass_planner.py` — optional `history` arg,
    `_MOVE_TARGET` map, `HISTORY_DEMOTE` bound, pure `_apply_history` helper,
    conditional `evidence` field.
  - `tests/test_next_pass_history.py` (new, **12 tests**) — P-008 planner tests.
  - `tests/test_governance_taste.py` (Commit-2, additive) — the folded
    `drum_room_bloom` narrower-taste test (mirror of
    `test_narrower_taste_lowers_width_bloom_identity_bounded`; closes the P-007
    residue test gap).
- **Out (explicit):**
  - Pipeline re-plumbing / threading history into `analyze()` — deferred as a
    separate **P-008b** (live history wire); `pipeline.py` / `cowork.py` untouched.
  - `memory.py` / `record_pass` changes — the producer shape is the contract.
  - P-007b live taste surface; event-logging producers; creative scoring;
    `doctrine_score` / safety surfaces.

## Commits

- `d98a194` P-008: history-aware next_pass (opt-in, bounded, evidence-tagged) —
  Commit-1 (test-first): `next_pass_planner.py` (+88/−1) + new
  `tests/test_next_pass_history.py` (+234). 2 files.
- `dbf94c3` P-008: add drum_room_bloom narrower-taste test (P-007 residue gap) —
  Commit-2 (additive): `tests/test_governance_taste.py` (+25). 1 file.
- (non-product) `99eab33` Confirm P-008 (history-aware next pass) as active
  packet — `build-os/` memory only.

## QA proof

- Suite:        `python -m pytest` → **138 passed**, 0 failed, 0 skipped,
  0 warnings.
- Regression:   `python -m logic_mix_os.cli regression` → **68/68**, 0 critical,
  0 warnings.
- Commit-1 iso: worktree checked out at `d98a194` → **137 passed** (full suite),
  **20 passed** (targeted `test_next_pass_history.py`), regression **68/68** →
  **green in isolation**.
- Backward-compat (HARD gate): **default path BYTE-IDENTICAL three ways** —
  arg-omitted == `history=None` == `history=[]`, with **no `evidence` key** —
  across all 3 `analyzed` fixtures, with a positive control proving the history
  path is live.
- Scope:        exactly the 3 declared files; `memory` / `pipeline` / `cowork` /
  `governance` runtime untouched.
- Safety grep:  none found (no network / subprocess / AppleScript / `.logicx` /
  `RealLogicSessionAdapter`).
- UI smoke:     N/A (planner logic; no surface change).

## Review

- Verdict: **pass.**
- Rationale: backward-compat byte-identical verified three ways; `_MOVE_TARGET`
  keys/score-keys verified against `SCORE_KEYS`; demotion is **floored and
  survives** (never deletes); the **revert move at priority 95 > 90 ruled
  acceptable** — bounded (it displaces only the weakest real move; its `detail`
  names only recorded targets so it cannot manufacture a move; revert is
  non-destructive); determinism confirmed; test-first reproduced (12 RED→GREEN);
  regression structurally safe (`next_pass_titles` is recorded but never diffed
  by `compare_snapshots`, doctrine invariant #4 runs the no-history byte-identical
  path, score-drift reads `doctrine_score` which the planner never writes).
- Codex second-eyes: **not available.**
- Product Trajectory Check: with **P-007** (taste → governance, *consumer* side)
  AND **P-008** (outcome → next-pass, *outcome* side), **BOTH halves of the
  learning loop are now closed** — the system both personalizes to recorded taste
  and stops re-recommending moves that regressed. The natural follow-on is the
  live wire (**P-008b**) that threads real recorded history into production.

## Residue

- Deferred / follow-up packets:
  - **P-008b — Live history wire:** thread `memory.history()` into
    `pipeline.analyze()` / the planner call so a real recorded history reaches
    `plan_next_pass` in production — kept **opt-in / explicit** so the
    byte-identical-by-default guarantee survives (symmetric to P-007b). The
    natural next trajectory packet.
  - **P-007b — Live taste surface (carried):** wire a real per-operator
    `taste_profile` from `memory_dir` into a pipeline/cowork run, explicit
    per-operator.
  - **Low-priority test cleanup:** `test_evidence_only_on_moved_candidates`
    (`tests/test_next_pass_history.py`) has a redundant always-true inner guard;
    tidy when convenient — not its own packet unless the file is touched.
  - Event-logging producers (`taste_feedback` / `validation_check` / `revert` /
    `manual_note`) — still behind the unanswered product decision, now with **two**
    downstream consumers existing.
- Known risks:
  - Degenerate empty-`records` input (low priority, from P-006) — unchanged.
  - Commits on this branch are **unsigned** (empty 0-byte signing key, container
    runs as root) — environment limitation; author/committer correctly
    `noreply@anthropic.com`; GitHub shows "Unverified" (missing signature only).
  - Test env: numpy + pytest are not preinstalled (`pip install -e ".[dev]"`
    from `logic-mix-os/`).

## Open boundaries (awaiting explicit go)

- **P-008's product commits `d98a194` and `dbf94c3` are local-only as of this
  close** — no push/merge/deploy performed. Any push updates the already-open
  **PR #13** (base `claude/dreamy-turing-z0oxll`) and would also carry the prior
  local-only commits (P-005/P-006/P-007 if not yet pushed) — do so only under the
  user's explicit push-go.
