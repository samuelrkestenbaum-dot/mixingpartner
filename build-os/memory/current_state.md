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
  `694d19d`; active dev branch `claude/logic-mix-os-hardening-12-7hbeh1` (product
  base `45437d2`, P-009 product commit `27bfebf` local-only).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **143 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **MILESTONE — THE LEARNING LOOP IS NOW REAL IN PRODUCTION.** With **P-009**
  (live wire), a real `cowork --memory-dir` run **both learns and personalizes**:
  it records and history-demotes/reverts regressed moves (outcome axis) AND
  down-weights to recorded operator taste in governance (consumer axis). The full
  arc **P-007 (consumer) → P-008 (outcome) → P-009 (live wire)** is closed
  end-to-end. Memory is no longer dormant in production on either axis — the
  P-007/P-008 investment now reaches a real operator. **P-009 subsumes and
  completes P-007b + P-008b** (both DONE via P-009).
- **Last closed packet:** **P-009** — Live wire: thread real memory into the
  production analysis path. `analyze()` gained an opt-in **trailing** `memory_dir`
  param; when set it builds `ProjectMemory` **once** and threads `history()` →
  `plan_next_pass` and `taste_profile()["profile"]` → `run_governance`.
  `cowork.py:28` now passes `memory_dir` into its `analyze()` call, making the
  pre-existing CLI `cowork --memory-dir` → `build_context` chain live. Single
  product commit `27bfebf` (`pipeline.py` +18, `cowork.py` +1 at `:28`,
  `tests/test_live_wire.py` new = 5 e2e tests). Suite 138→**143**; regression
  68/68 held; **default path BYTE-IDENTICAL** (full `ProjectAnalysis` exact
  string-equal across no-arg / `memory_dir=None` / empty dir — the `"evidence"`
  keys in the dump are pre-existing baseline fields, NOT a P-009 leak); Commit-1
  green in isolation. Positive control confirmed live (history → "Revert last
  pass" + Section contrast demoted; taste → `taste_adjustments` + identity 80→65).
  Reviewer: **pass** (taste axis ruled GENUINELY LIVE — flows e2e + lowers
  identity; no winner flip on this fixture is a data property, decision-level flip
  proven by P-007's unit test on the same `analyze()`-driven code path; Codex not
  available). Receipt:
  `build-os/receipts/P-009-live-wire-memory-into-analyze.md`.
- **Now:** **none active.** No product packet in flight.
- **Next:** orchestrator **re-survey** — the loop trajectory is fully realized, so
  the strategic question is where to skate next. Re-ranked candidates (user is
  driving via "skate to where the puck"):
  - **Album cross-song coherence** — `analyze_album` is isolated from per-song
    planning; cross-song coherence is the next strategic direction.
  - **Deeper creative scoring** — `creative.py::_KIND_SCORES` is hardcoded;
    richer kind-scoring is the other strategic direction.
  - **Loop-strengthening follow-ups (from P-009 reviewer):** a borderline-song
    taste fixture that flips the governed winner *through `analyze()`* end-to-end;
    a wider `--memory-dir` CLI surface beyond `cowork`.
  - Net-new **event-logging** producers (`taste_feedback` / `validation_check`)
    remain behind the product decision — now with live consumers, more justified.

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
_Updated by the archivist on close. Last advanced on P-009 close (2026-06-29)._
