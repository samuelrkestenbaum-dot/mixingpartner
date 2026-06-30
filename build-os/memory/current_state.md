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
  (P-012 product base `4dfe142`; P-012 product commit `0df436c` local-only).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-29):** suite **202 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED — via option B.** With
  **P-012**, the standing OPEN USER DECISION ("deeper creative scoring") is
  closed by the user's chosen path: a bounded, transparent, **capped,
  penalty-only** evidence-nudge layer ON TOP of the curated `_KIND_SCORES` (the
  curated values are UNCHANGED). `score_variant` applies, via a pure
  `_apply_nudges`/`_NUDGE_TABLE`, two evidence-gated penalties — `vocal_belief −8`
  when the lead vocal is masked (`bad_masking`, generalizing the old `width_bloom`
  caution to `vocal_ride`/`intimacy_pass` too) and `vocal_belief −6` when the
  image is `width_crowding` — with the summed overall delta clamped to
  `±CREATIVE_NUDGE_CAP = 2.0` and `score_nudges: [reason]` emitted only when a
  nudge fires. **This DELIBERATELY changes default scoring when a nudge fires (NOT
  byte-identical by default) but provably cannot overturn a clear base ranking**
  (cap 2.0 < typical 2.4–4.2 base gaps). It is **latent-but-armed** — fires on no
  current fixture's winner, ready for a real masked-vocal / crowded-width song —
  and **awaiting the user's sign-off at the PR #13 merge** (the user's reviewed
  aesthetic change). The deferred **REWARD nudges** (orchestrator rows 3+4) are a
  possible later additive packet.
- **THE ALBUM-MEANS TRUTH IS SINGLE-SOURCED.** With **P-011**, the album means
  live in exactly ONE place: `album.py::analyze_album` additively emits per-song
  `brightness_delta` / `lufs_delta` and `cli.py::_run_album` consumes them; the
  duplicate `statistics.mean` recompute is gone — the two-place drift risk is
  killed. The `album` report stays value-identical.
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
- **Last closed packet:** **P-012** — Creative-scoring evidence-nudge layer
  (option B, penalty-only). Pure `_apply_nudges`/`_NUDGE_TABLE` on top of the
  untouched `_KIND_SCORES`; two evidence-gated penalties (`vocal_belief −8` on
  masked vocal across `width_bloom`/`vocal_ride`/`intimacy_pass`; `vocal_belief −6`
  on `width_crowding` for `width_bloom`); summed overall delta clamped to
  `±2.0`; `score_nudges` emitted only on fire. Single product commit `0df436c`
  (`creative.py` +89/−11; `tests/test_creative_nudges.py` new, 43 cases). Suite
  159→**202**; regression **68/68** held (variant-scoring path is golden-unguarded
  — unit tests are the binding guard); Commit-1 green in isolation (`0df436c`:
  202 passed, 70 targeted, 68/68); **CAP BINDS EXACTLY** (`width_bloom` both rows:
  75.7 → 73.7 = base−2.0, raw −14 clamped); **NO RECOMMENDATION FLIP** on the 3
  fixtures (dense fires row 2 on the LOSING `chorus_lift_A`; winner stays
  `chorus_lift_B`; row 1 never fires); scope = exactly 2 files; `_KIND_SCORES`
  values unchanged; governance/memory/pipeline/album/next_pass untouched; safety
  grep none; UI N/A. Reviewer: **pass** — adversarially proven (forced −70 raw /
  −10.0 overall STILL clamped to base−2.0; layer-ON vs layer-OFF confirms the
  dense fixture genuinely fires yet no winner flips → non-tautological;
  penalty-only across all kinds; predicates verbatim-reused; test-first
  `ImportError` reproduced; Codex not available). **NOT byte-identical by
  default — deliberate — but cannot overturn a clear base ranking.** Awaiting the
  user's sign-off at PR #13 merge. Receipt:
  `build-os/receipts/P-012-creative-scoring-nudge-layer.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — THE USER'S AESTHETIC DECISION IS RESOLVED (option B shipped, awaiting
  PR #13 sign-off). The remaining moves are small in-authority follow-ups + one
  user-gated additive.** Candidates:
  - **Reward nudges (orchestrator rows 3+4)** — `depth_cleanup +6 halee` /
    `subtractive_drop +4 taste` on non-empty `crowded_sections`. Possible later
    ADDITIVE packet IF the user wants reward (promotion) nudges; P-012 is
    penalty-only by design. User-gated.
  - **Borderline near-tie / taste fixtures (informational)** — a fixture that
    demonstrates an INTENDED near-tie flip through `analyze()` (option-B behavior
    visible on real data), and the carried borderline-TASTE fixture from P-009.
    Small additive tests, in authority.
  - **Wider `--memory-dir` CLI surface** (from P-009 — partly a product question);
    net-new **event-logging** producers (behind a product decision). Deferred.

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **Variant-scoring path is golden-unguarded:** `regression.py` reads
  `doctrine_score`, never `score_variant`, so the 68/68 golden cannot catch a
  creative-scoring change. **Unit tests are the binding guard for any
  `creative.py`/`score_variant` change** (P-012's `tests/test_creative_nudges.py`).
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-012 close (2026-06-29)._
