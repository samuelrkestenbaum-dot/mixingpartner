# Receipt — P-004: Event-tagging — tag `cowork.py::_write_mix_decision` → `mix_decision`

- **Date:** 2026-06-29
- **Branch base (merge-base):** product base `d73bb3d`; default branch
  `claude/dreamy-turing-z0oxll` @ `694d19d` (verified `git merge-base` →
  `694d19d`). No `main` exists.

## Scope
- **In:** one-line tag at `logic_mix_os/cowork.py:93` —
  `return mem.add_decision(decision or {})` →
  `return mem.add_decision(decision or {}, event_type="mix_decision")`. No
  signature / command-surface change. Plus one new test
  `tests/test_cowork.py::test_write_mix_decision_tags_event_type` driving the
  `write_mix_decision` cowork command through `run_command` with a memory-backed
  ctx and asserting the persisted ledger entry has
  `event_type == "mix_decision"`. This closes `EVENT_TYPES` adoption across
  every **existing** decision-ledger producer.
- **Out (explicit — deferred as separate net-new feature packets):**
  `taste_feedback`, `validation_check`, `revert`, `manual_note`. These are valid
  `EVENT_TYPES` members but have **no existing ledger producer** (taste →
  `taste_calibration.json`; validation only returns; revert is a pass-record
  field; no `manual_note` writer exists). Wiring any of them into the decision
  ledger is net-new feature work, not a tagging change.

## Commits
- `a9daa72` P-004: tag _write_mix_decision ledger write as mix_decision
  (product — 1-line `cowork.py` edit + 14-line test;
  `cowork.py | 2 +-`, `test_cowork.py | 14 ++++`, 2 files / 15 insert / 1 delete)
- `9b131b6` Confirm P-004 (event-tagging _write_mix_decision) as active packet
  (non-product — `build-os/packets/active_packet.md` only)

## QA proof
- Suite:        `python -m pytest` → **108 passed**, 0 failed, 0 skipped,
  0 warnings (107 → 108; the +1 is this packet's new test).
- Regression:   `python -m logic_mix_os.cli regression` → **68/68** (0 warnings).
- Commit-1 iso: worktree checked out at `a9daa72` → **108 passed** (incl. 10
  cowork tests), regression **68/68** → green. Commit-1 is self-contained (test
  + edit ship together so the suite is green in isolation).
- Safety grep:  none found — no new network / subprocess / AppleScript /
  `.logicx` / `RealLogicSessionAdapter` surface. Scope confirmed to only
  `cowork.py` + `tests/test_cowork.py`; `memory.py` / `constants.py` / `cli.py`
  byte-identical.
- UI smoke:     N/A (no renderer / UI surface touched).

## Review
- Verdict: **pass.** Correctness — `mix_decision` is a valid `EVENT_TYPES`
  member (from P-002), so `add_decision` does not raise; command surface
  unchanged. Scope — exactly the one untagged write + one test. Test quality —
  real `run_command` path with a round-trip persisted-ledger assertion;
  test-first reproduced (pre-impl `KeyError: 'event_type'`). Backward-compat —
  additive `event_type`; no test asserts an exact key-set; all pass.
- Codex second-eyes: **not available** (single-reviewer pass).
- Product Trajectory Check: **pass** — closes `EVENT_TYPES` adoption across all
  EXISTING ledger producers. Every existing decision-ledger write now carries a
  valid tag (`mute_candidate` via P-002's `record_plan_decisions`,
  `mix_decision` via P-004's `_write_mix_decision`).

## Residue
- Deferred / follow-up packets:
  - **Net-new event-logging packets (deferred):** `taste_feedback`,
    `validation_check`, `revert`, `manual_note` — valid `EVENT_TYPES` members
    with NO producer wired into the ledger today. Each is a separate net-new
    feature packet IF the user wants those events logged.
  - **`creative.py` literal cleanup:** `chorus_lift_B` `loops or supporting[-1:]`
    (~line 194) and the loop branch `loops[0] if loops else "the loop"`
    (~line 217) — still not record-resolved. Latent on today's fixtures.
  - **`creative_renderer.py:104` readiness follow-up:** extend P-003's labelled
    READY / NOT-YET treatment to `creative_renderer.py` for full surface
    consistency (design-UI, render-only).
- Known risks: commits on this branch are **unsigned** — the configured SSH
  signing key is a 0-byte file and the container runs as root, so signing is
  impossible. Author + committer are correctly `noreply@anthropic.com`; GitHub
  shows these as "Unverified" (missing signature only, not misattribution). This
  is an environment limitation, not a fix-it item.

## Open boundaries (awaiting explicit go)
- P-003 is pushed. P-004's product commit `a9daa72`, the memory commit
  `9b131b6`, and this archivist close commit are **unpushed**. Under the user's
  **STANDING push-go** they push immediately after this close, updating the
  already-open **PR #13** (base `claude/dreamy-turing-z0oxll`). No merge / deploy
  / secret boundary pending.
