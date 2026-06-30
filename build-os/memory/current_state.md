# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## Project

- **What this repo is:** Logic Mix OS — a local-first, deterministic mix-decision
  system that turns exported Logic Pro stems + a `project_manifest.json` into a
  section-aware, Logic-native **mix plan** (Roy Halee / Phil Ramone judgment
  layer). Not an auto-mixer, preset generator, or mastering tool. All product
  code lives under `logic-mix-os/`.
- **Primary branch / base:** default branch `claude/dreamy-turing-z0oxll`;
  active dev branch `claude/logic-mix-os-hardening-12-7hbeh1` (`git merge-base`
  with default = `694d19d`). **PR #13 (P-001…P-012 + the canonical-alignment
  audit) is MERGED to default** — merge commit `0f4e7e9`. **P-013 is the first
  post-merge packet** on the freshly-restarted dev branch; its tests-only product
  commit `172cfd0` sits on top of `0f4e7e9` and is local-only.
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-30):** suite **207 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **THE P-012 CREATIVE NUDGE IS NOW PROVEN ON REAL DATA THROUGH `analyze()`.**
  With **P-013** (tests-only), the bounded penalty-only evidence-nudge layer
  shipped in P-012 is lifted from the unit level (hand-built `SimpleNamespace`) to
  the **live `pipeline.analyze()` production path**. On `dense_chorus_with_loops`
  the live masking analyzer emits a real `width_crowding` event, so the row-2
  nudge (`vocal_belief −6`) fires on the `chorus_lift` `width_bloom` variant with
  no contrivance — lowering its `overall_score` from the curated base **75.7 →
  74.9** (movement −0.857, well inside the ±2.0 cap), yet the winner stays
  `chorus_lift_B` (base gap ~9.6 > 2× the cap). This is the documented
  **latent-but-armed option-(a)** posture, now proven end-to-end, **closing the
  golden-unguarded gap** on the variant-scoring path (the 68/68 golden reads
  `doctrine_score`, never `score_variant`). **No product code touched.**
- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED — via option B (P-012),
  AND NOW MERGED.** The bounded, transparent, capped, **penalty-only**
  evidence-nudge layer ON TOP of the curated `_KIND_SCORES` (values UNCHANGED) is
  live on the default branch via PR #13. `score_variant` applies two evidence-gated
  `vocal_belief` penalties (`−8` masked vocal across
  `width_bloom`/`vocal_ride`/`intimacy_pass`; `−6` `width_crowding` for
  `width_bloom`), summed overall delta clamped to `±2.0`, `score_nudges` emitted
  only on fire. It cannot overturn a clear base ranking (cap 2.0 < 2.4–4.2 base
  gaps). The deferred **REWARD nudges** (orchestrator rows 3+4) remain a possible
  later additive packet, **user-gated**.
- **THE ALBUM-MEANS TRUTH IS SINGLE-SOURCED.** Via **P-011**, the album means
  live in exactly ONE place: `album.py::analyze_album` additively emits per-song
  `brightness_delta` / `lufs_delta` and `cli.py::_run_album` consumes them; the
  duplicate `statistics.mean` recompute is gone. The `album` report stays
  value-identical.
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
- **POSITIVE ALIGNMENT FINDING (from P-013) — taste cannot flip a governed winner
  on curated data, BY DESIGN.** The builder brute-forced all 3 fixtures × 4 intents
  with a narrower-taste `ProjectMemory`: no governed-winner flip anywhere.
  Reviewer-verified in source — `_apply_taste` moves only the `taste_triangle`
  identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and is
  align-vetoed before it can reorder a truth-ranked winner. This is the doctrine
  "taste can never outrank a truth move," working as intended. The reachable taste
  claim is already proven on real data by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`.
- **Last closed packet:** **P-013** — Nudge-visibility fixture (tests-only). One
  new file `tests/test_creative_nudge_visibility.py` (+154 lines, **5 tests**)
  drives the P-012 creative nudge through the live `analyze()` path on
  `dense_chorus_with_loops` (real `width_crowding` event → row-2 nudge fires).
  Builder chose **option (a)**: the cap binds, the winner does NOT flip
  (overall_score 75.7 → 74.9, movement −0.857 within ±2.0; winner stays
  `chorus_lift_B`; base gap 9.6 > 2×2.0). Single tests-only commit `172cfd0` (no
  product tree change). Suite 202→**207**; regression **68/68** held;
  Commit-1 green in isolation (single tip commit; new file alone = 5 passed;
  product tree unmodified); safety grep clean (only hit a no-DAW docstring); UI
  N/A. Reviewer: **pass** — independent negative control (disarmed `_apply_nudges`
  → 3 of 5 fail, so assertions are load-bearing), independently recomputed the
  option-(a) numbers, confirmed the Fixture #2 re-scope sound. **Codex NOT
  available — single-reviewer verdict.** Fixture #2 (taste-flip through `analyze()`)
  re-scoped to a positive alignment finding (structurally unreachable test-only —
  user-gated to a product change). Receipt:
  `build-os/receipts/P-013-nudge-visibility-fixture.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — the creative-scoring decision is resolved AND merged; P-013 proved it
  on real data. Remaining moves are small in-authority additives + user-gated
  follow-ups.** Candidates:
  - **"Near-tie-creative-flip" fixture (NEW from P-013)** — a fixture where the
    creative nudge actually FLIPS the winner through `analyze()` (a true near-tie,
    distinct from P-013's no-flip option-(a) case). Reachable test-only, the
    natural next increment. Small additive test, in authority.
  - **Reward nudges (orchestrator rows 3+4)** — `depth_cleanup +6 halee` /
    `subtractive_drop +4 taste` on non-empty `crowded_sections`. Possible later
    ADDITIVE packet IF the user wants reward (promotion) nudges; P-012 is
    penalty-only by design. **User-gated.**
  - **Taste-flip-via-product-change** — making a taste-driven governed-winner flip
    reachable through `analyze()` needs a product-code aesthetic change. **User-gated,
    separate packet.** (The reachable taste claim is already covered by
    `test_live_wire.py::test_taste_axis_changes_governance`.)
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
  creative-scoring change. **Unit + visibility tests are the binding guard for any
  `creative.py`/`score_variant` change** (P-012's `tests/test_creative_nudges.py`
  + P-013's `tests/test_creative_nudge_visibility.py` driving the live `analyze()`
  path).
- **Taste is structurally below truth (P-013-verified):** `_apply_taste` moves only
  the identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and
  is align-vetoed — so taste cannot reorder a truth-ranked governed winner on
  curated data. Working as intended.
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-013 close (2026-06-30)._
