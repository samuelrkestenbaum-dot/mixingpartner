# Receipt — P-009: Live wire — thread real memory into the production analysis path (subsumes P-007b + P-008b)

- **Date:** 2026-06-29
- **Authority:** build (trajectory-realizing — makes the P-007/P-008 learning loop real in production)
- **Branch base (merge-base):** product base `45437d2`; default branch
  `claude/dreamy-turing-z0oxll` @ `694d19d` (`git merge-base` confirmed `694d19d`).

## What it does

`analyze()` gained an opt-in **trailing** `memory_dir` param. When it is set,
`analyze()` builds `ProjectMemory` **once** and threads:
- `history()` → `plan_next_pass` (history axis), and
- `taste_profile()["profile"]` → `run_governance` (taste axis).

`cowork.py:28` now passes `memory_dir` into its `analyze()` call. Since the CLI
`cowork --memory-dir` → `build_context` chain already existed, a **REAL**
`cowork --memory-dir` run now both **learns** (history demotes regressed moves /
surfaces revert) and **personalizes** (taste down-weights). When no `memory_dir`
is supplied the default path is **byte-identical** to today.

## Scope

- **In (exactly three files):**
  - `logic_mix_os/pipeline.py` (+18: trailing `memory_dir` param +
    `from .memory import ProjectMemory` + construct-once block binding
    `_history`/`_taste` + threading `history=_history` into `plan_next_pass`
    and `taste_profile=_taste` into `run_governance`).
  - `logic_mix_os/cowork.py` (+1 arg at `:28` — `memory_dir=memory_dir` into the
    one `analyze(...)` call).
  - `tests/test_live_wire.py` (new — 5 end-to-end tests, no DAW / no network).
- **Out (explicit):** the other 13 CLI `analyze` call sites (no new flags);
  album coherence (`analyze_album`); creative `_KIND_SCORES`; the bridge apply /
  Class-3 path; net-new event-logging producers; `memory.py` (accessors already
  match the consumer shapes); any push/merge to PR #13.

## Commits

- `27bfebf` P-009: live-wire real memory into the production analysis path
  (single **product** commit — the 3 in-scope files: `cowork.py` +3/−1,
  `pipeline.py` +18, `tests/test_live_wire.py` +254 new).
- `252bcca` Confirm P-009 (live wire: memory into analyze) as active packet
  (**non-product** — `build-os/packets/active_packet.md` only).

## QA proof (GREEN)

- **Suite:** `python -m pytest` → **143 passed**, 0 failed / 0 skipped / 0 warnings.
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68**, 0 critical,
  0 warnings.
- **Commit-1 iso:** worktree checked out at `27bfebf` (the single product commit) →
  **143 passed**, 21 targeted, regression **68/68** → green in isolation.
- **Default path BYTE-IDENTICAL:** full `ProjectAnalysis` exact string-equal across
  the no-arg call / `memory_dir=None` / empty fresh dir. The `"evidence"` keys
  present in the dump are **PRE-EXISTING baseline fields** (identical count at base),
  **NOT** a P-009 leak — there is no history/taste key on the memoryless path.
- **Positive control (end-to-end, live):** with a seeded store —
  history axis → `"Revert last pass"` surfaces + Section-contrast move demoted;
  taste axis → `taste_adjustments` evidence appears + width-bloom identity
  lowered 80→65. Confirmed live through `analyze()` AND through the cowork
  surface (`build_context(..., memory_dir=seeded)`).
- **Scope grep:** changed set is exactly the 3 declared files;
  `memory` / `governance` / `next_pass_planner` / `cli` / `regression` untouched.
- **Safety grep:** clean — the only `applescript` / `open` hits are pre-existing,
  outside the P-009 hunks (no real DAW / AppleScript / subprocess / `.logicx`
  write / network introduced).
- **UI smoke:** N/A (no UI surface touched).

## Review

- **Verdict: pass.**
  - Backward-compat provably **byte-identical** (full `ProjectAnalysis` equal three ways).
  - Wire correct: `ProjectMemory` built **once** under the `if memory_dir is not None:`
    guard; consumer shapes match (`history()` → `plan_next_pass`,
    `taste_profile()["profile"]` → `run_governance`).
  - **Taste axis ruled GENUINELY LIVE:** the taste profile flows end-to-end and
    lowers width-bloom identity. No winner *flip* on this particular fixture is a
    **data property** (the dominant-variant margin exceeds the bounded ±15 taste
    nudge on real fixtures), NOT an inert wire — the decision-level flip is already
    proven by P-007's `test_narrower_taste_changes_governed_winner` exercising the
    same `run_governance` code path that `analyze()` now drives.
  - **History axis** has decision-level impact (demote + revert observed e2e).
  - **Test-first empirically reproduced:** 5 RED pre-impl; the cowork `AssertionError`s
    prove `cowork.py:28` is load-bearing (without the one-arg edge the prod surface
    does not learn).
  - Regression structurally safe: `regression.py:255` calls `analyze()` with no
    `memory_dir` → `_history=None` / `_taste=None` → both consumers hit their
    existing falsy-guard no-op → goldens unchanged → 68/68 holds.
- **Codex second-eyes:** NOT available.
- **Product Trajectory Check:** this packet realizes the P-007/P-008 learning-loop
  investment in production — the full arc P-007 (consumer) → P-008 (outcome) →
  P-009 (live wire) is closed end-to-end. **Subsumes and completes P-007b + P-008b.**

## Residue

- **MAJOR MILESTONE — the learning loop is now REAL IN PRODUCTION:** a real
  `cowork --memory-dir` run both **learns** (records → history-aware next pass) and
  **personalizes** (taste → governance). P-009 **subsumes and completes
  P-007b + P-008b** (both marked DONE via P-009). The arc P-007 → P-008 → P-009 is
  closed end-to-end.
- **New follow-ups (Deferred, non-blocking — from the reviewer):**
  - **Borderline-song taste fixture:** a fixture where the bounded taste nudge
    actually flips the governed winner **through `analyze()`** end-to-end (today the
    decision-level taste flip is proven only at the P-007 unit level; on real
    fixtures the dominant-variant margin exceeds ±15). Strengthens the taste axis's
    visible production impact.
  - **Wider `--memory-dir` surface:** consider whether more analyze-class CLI
    commands (beyond `cowork`) should accept `--memory-dir`.
  - **Low-priority test cleanup** (carried): `test_evidence_only_on_moved_candidates`
    in `tests/test_next_pass_history.py` — redundant always-true inner guard; fold
    into any future touch of that file.
- **Re-ranked strategic candidates** (loop trajectory now fully realized) — for
  orchestrator re-survey: **album cross-song coherence** (`analyze_album` isolated
  from per-song planning) and **deeper creative scoring** (`creative.py::_KIND_SCORES`
  hardcoded). Net-new event-logging producers remain behind the product decision
  (now with live consumers, more justified than ever).
- **Known risks:** commits on this branch are **unsigned** (empty 0-byte SSH signing
  key, container runs as root → signing impossible; author/committer correctly
  `noreply@anthropic.com`, GitHub shows "Unverified" = missing signature only, not
  misattribution — environment limitation, not a fix-it item). Test env: numpy +
  pytest require `pip install -e ".[dev]"` from `logic-mix-os/` before `pytest`.

## Open boundaries (awaiting explicit go)

- **Product commit `27bfebf` is local-only** as of this close (no push/merge/deploy).
  Pushing it (with the unpushed P-005/P-006/P-007/P-008 commits) updates the already-
  open **PR #13** (base `claude/dreamy-turing-z0oxll`) — do so only under the user's
  explicit push-go. No merge / deploy / secret action taken.
