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
  audit) is MERGED to default** — merge commit `0f4e7e9`. The post-merge dev
  branch carries P-013 (`172cfd0`, tests-only) and **P-015 (`1756f61`, product)**
  on top of `0f4e7e9`; both are local-only at this close (P-014 added no product
  commit).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression`.
- **Green baseline (verified 2026-06-30):** suite **217 passed** (0 failed /
  skipped / warnings); regression **68/68** (0 critical / 0 warnings).

## Where we are

- **THE P-012 NUDGE IS NO LONGER TRANSPARENCY-ONLY — P-015 MAKES IT DECISIVE ON
  THE MASKED-VOCAL NEAR-TIE (USER-SIGNED-OFF AESTHETIC CHANGE).** This supersedes
  the P-014 "transparency-only" framing. P-014 proved that a near-tie creative
  FLIP was structurally UNREACHABLE test-only **under the then-current curation**
  and surfaced the user-gated "make-the-nudge-decisive (curation change)" packet.
  The user chose **"Option 1 — Proceed, corrected"** (2026-06-30, after the
  orchestrator transparently corrected an arithmetic error in the original
  preview — the old `−8` penalty only moves overall by `−1.14`, insufficient to
  flip; the corrected mechanism strengthens to `−14`). **P-015** edits
  `creative.py` `_NUDGE_TABLE` row-0 (`lead_masked`) ONLY, two changes:
  **(1) exempt `intimacy_pass`** from the penalty (an intimacy pass is the CORRECT
  response to a masked lead vocal — focused proximity, not brute level/width) and
  **(2) strengthen the penalty `−8` → `−14`** (`= −14/7 = −2.0` overall = EXACTLY
  the existing `CREATIVE_NUDGE_CAP = 2.0`, which is UNCHANGED and now binds for
  `vocal_ride` too). **Net effect in the `vocal_belief` branch under a masked lead
  vocal:** `vocal_ride` (vocal_A) 82.9 → **80.9** (cap binds, overall_delta
  EXACTLY −2.0, carries the `−14` `score_nudges` line); `intimacy_pass` (vocal_B)
  81.1 unchanged (exempt) → **winner FLIPS from `vocal_ride` to `intimacy_pass`**
  by 0.2. **Bounded — still cannot overturn a clear ranking:** `subtractive_drop`
  (85.3, penalty-immune) still wins `chorus_lift` / `density` / `loop` under
  `lead_masked` (gaps 3.4–4.2 ≫ 2×cap); ONLY the `vocal_belief` branch flips —
  the doctrine "breaks a genuine near-tie, never overturns a clear ranking."
  **Negative control (load-bearing):** without `lead_masked`, `vocal_ride` wins →
  the flip is caused by the masking evidence, not a base re-rank. `_KIND_SCORES`,
  the cap, row-1, the clamp, and both predicates are UNTOUCHED.

- **THE P-012 CREATIVE NUDGE IS PROVEN ON REAL DATA THROUGH `analyze()`.** With
  **P-013** (tests-only), the bounded penalty-only evidence-nudge layer shipped in
  P-012 is lifted from the unit level (hand-built `SimpleNamespace`) to the
  **live `pipeline.analyze()` production path**. On `dense_chorus_with_loops` the
  live masking analyzer emits a real `width_crowding` event, so the row-1 nudge
  (`vocal_belief −6`) fires on the `chorus_lift` `width_bloom` variant with no
  contrivance — lowering its `overall_score` from the curated base **75.7 →
  74.9** (movement −0.857, well inside the ±2.0 cap), yet the winner stays
  `chorus_lift_B` (base gap ~9.6 > 2× the cap). This is the documented
  **latent-but-armed option-(a)** posture, proven end-to-end, **closing the
  golden-unguarded gap** on the variant-scoring path (the 68/68 golden reads
  `doctrine_score`, never `score_variant`). The P-013 visibility tests still pass
  unchanged after P-015. **No product code touched by P-013.**
- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED — option B (P-012),
  MERGED (PR #13), AND NOW DELIBERATELY MADE DECISIVE (P-015).** The bounded,
  transparent, capped, **penalty-only** evidence-nudge layer ON TOP of the curated
  `_KIND_SCORES` (values UNCHANGED) is live on the default branch via PR #13;
  P-015 (local-only) then tunes row-0 so the nudge is decisive on exactly the
  masked-vocal near-tie. The deferred **REWARD nudges** (orchestrator rows 3+4)
  remain a possible later additive packet, **user-gated**.
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
- **Last closed packet:** **P-015** — Make the masked-vocal nudge DECISIVE
  (user-signed-off aesthetic change). Single product commit `1756f61` (product
  change + updated/new tests together so Commit-1 is green in isolation):
  `creative.py` `_NUDGE_TABLE` row-0 only — exempt `intimacy_pass`, strengthen
  `−8`→`−14`, honest reason + doctrine comment + corrected stale clamp comment.
  Suite **207 → 217 passed**; regression **68/68, 0 critical, 0 warnings** held;
  Commit-1 green in isolation; safety grep clean (only a no-DAW docstring line);
  UI N/A. qa verdict **GREEN**. Reviewer **pass** — independently reproduced the
  arithmetic and ran a **mutation test confirming non-vacuity** (reverting both
  product edits → 5 binding tests went RED, the negative control correctly stayed
  GREEN → tests are load-bearing); confirmed scope discipline, no-overturn,
  evidence-line honesty, coverage not weakened. **Codex NOT available —
  single-reviewer verdict.** Non-blocking reviewer note: the mandated
  `Co-Authored-By: Claude Opus 4.8` trailer is a standing harness-required config
  tension, not a P-015 regression. **P-015 is local-only** (product commit
  `1756f61` on the dev branch on top of `0f4e7e9`), not pushed/merged at close
  (the orchestrator pushes the dev branch after). Receipt:
  `build-os/receipts/P-015-decisive-masked-vocal-nudge.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — the creative-scoring decision is resolved, merged, AND now decisive on
  the masked-vocal near-tie. Remaining moves are small in-authority additives +
  user-gated follow-ups.** Candidates:
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
  `creative.py`/`score_variant` change** (P-012's `tests/test_creative_nudges.py`,
  P-013's `tests/test_creative_nudge_visibility.py` driving the live `analyze()`
  path, and P-015's `tests/test_decisive_nudge.py` pinning the flip).
- **Taste is structurally below truth (P-013-verified):** `_apply_taste` moves only
  the identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and
  is align-vetoed — so taste cannot reorder a truth-ranked governed winner on
  curated data. Working as intended.
- **The creative nudge CAN now reorder EXACTLY the `vocal_belief` branch under
  `lead_masked`, within the cap (P-015 — supersedes the P-014 "cannot reorder any
  branch" fact):** row-0 (`lead_masked`) penalizes `vocal_ride` (`−14` raw =
  `−2.0` overall, the cap) but EXEMPTS `intimacy_pass`, so the 1.71-gap near-tie
  flips to `intimacy_pass` (vocal_B). It STILL cannot overturn a clear ranking —
  `subtractive_drop` (85.29) is penalty-immune (in no nudge row) and wins every
  branch it competes in (`chorus_lift` / `density` / `loop`); only `vocal_belief`
  flips. The cap (`CREATIVE_NUDGE_CAP = 2.0`) is unchanged. This is the doctrine
  "breaks a genuine near-tie, never overturns a clear ranking." Binding guard:
  `tests/test_decisive_nudge.py` (flip + load-bearing negative control + collateral
  safety) and the updated `tests/test_creative_nudges.py`.
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.

---
_Updated by the archivist on close. Last advanced on P-015 close (2026-06-30)._
</content>
