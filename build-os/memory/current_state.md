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
  `694d19d`; active dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **125 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **Last closed packet:** **P-007** — Taste profile feeds governance (first
  closure of the learning loop). The recorded operator taste profile
  (`memory._derive_taste` statements) now **biases variant governance** —
  opt-in, bounded, evidence-tagged. An optional `taste_profile` arg (default
  `None`) threads through `govern_variant` / `govern_branches` / `run_governance`;
  a pure `_apply_taste` helper + a `_TASTE_KIND_BIAS` map (verbatim `_TASTE_MAP`
  statements) apply a bounded identity shift clamped to `TASTE_MAX_DELTA = 15`
  (strictly `< 30`, the truth nudge); a `taste_adjustments` evidence field is
  present **only** when an adjustment applies (absent — not `[]` — otherwise). Two
  operators with different taste now get different governed winners from the same
  song (proven: narrower taste flips `chorus_lift_A` → `chorus_lift_C`). Single
  product commit `bd08f28` (`governance.py` +75/−6, `tests/test_governance_taste.py`
  new, 13 tests). Suite 112→125; regression 68/68 held. Default path
  **byte-identical** (the HARD backward-compat gate); bound verified (10 stacked
  statements clamp to +15); safety surfaces untouched. Reviewer: **pass**
  (inviolability proven — a doctrine-vetoed `width_bloom`, `align=45<50`, stays
  rejected even with maxed wider taste raising identity to 84; Codex not
  available). Receipt: `build-os/receipts/P-007-taste-feeds-governance.md`.
  - **MILESTONE — first closure of the learning loop:** recorded taste now
    influences recommendations (opt-in, bounded `±15`, evidence-tagged,
    doctrine-inviolable). Memory is **no longer purely write-only on the
    governance axis** — a real consumer of recorded signals exists. This is the
    *consumer* half of the loop; the *outcome* half (history → next-pass) is the
    natural follow-on (P-008).
- **Now:** **none active.** No product packet in flight.
- **Next:** **P-008 — history-aware next pass** is the trajectory follow-on (the
  OUTCOME side of the loop): `plan_next_pass` should consume `mix_pass_history`
  (improved / got_worse / revert_candidates) so the system does not re-recommend
  a move that regressed. Also available — **P-007b** (wire a live per-operator
  `taste_profile` from `memory_dir` into a pipeline/cowork run) and the net-new
  **event-logging** producers (`taste_feedback` / `validation_check`, now more
  justified since a consumer exists, still behind the same product decision).
  **User's call** which to open.

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
_Updated by the archivist on close. Last advanced on P-007 close (2026-06-29)._
