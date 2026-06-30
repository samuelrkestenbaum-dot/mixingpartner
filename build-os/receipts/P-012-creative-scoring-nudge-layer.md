# Receipt — P-012: Creative-scoring evidence-nudge layer (option B, penalty-only)

- **Date:** 2026-06-29
- **Authority:** build (the user's reviewed aesthetic choice — option B, penalty-only)
- **Branch base (merge-base):** product base `4dfe142` on `claude/logic-mix-os-hardening-12-7hbeh1`;
  default `claude/dreamy-turing-z0oxll` @ `694d19d` (merge-base verified
  `694d19d`).

## What it does

A bounded, transparent, **penalty-only** evidence-nudge layer ON TOP of the
curated `_KIND_SCORES` (the curated values are **UNCHANGED**). `score_variant`
now applies, via a pure `_apply_nudges` / `_NUDGE_TABLE`, two evidence-gated
penalties:

- **Row 1** — kinds `{width_bloom, vocal_ride, intimacy_pass}` when the lead
  vocal is masked (`bad_masking` event whose element contains `"vocal"`) →
  `vocal_belief −8`. (Generalizes the curated caution that previously only hit
  `width_bloom`.)
- **Row 2** — `width_bloom` when the stereo image is `width_crowding` →
  `vocal_belief −6`.

The **SUMMED overall delta** is clamped to `±CREATIVE_NUDGE_CAP = 2.0` (on the
overall axis governance ranks on); `overall_score` stays in `[0,100]`.
`score_nudges: [reason]` is emitted ONLY when ≥1 nudge fires (transparent).

This **DELIBERATELY changes default scoring when a nudge fires — it is NOT
byte-identical by default** (unlike P-007…P-011) — but **provably cannot
overturn a clear base ranking**: the cap (2.0) is below the typical 2.4–4.2 base
gaps, so a nudge can only re-order near-ties, never flip a clear winner.
Penalty-only → a nudge can only LOWER a score, never promote a variant.

## Scope

- **In:**
  - `logic-mix-os/logic_mix_os/creative.py` — the nudge layer (+89/−11 net;
    `+100/−11` raw in the diff).
  - `logic-mix-os/tests/test_creative_nudges.py` — new, **43 cases** (292 lines),
    the binding safety-invariant suite.
- **Out (explicit):**
  - `_KIND_SCORES` **VALUES** (untouched — this is option B, not option C).
  - The deferred **REWARD nudges** (orchestrator rows 3+4 —
    `depth_cleanup +6 halee` / `subtractive_drop +4 taste` on `crowded_sections`)
    — P-012 is penalty-only by the user's recommended reading.
  - `governance` / `memory` / `pipeline` / `album` / `next_pass` — all untouched.
  - The `verdict` / `check vocal wash` text logic (dims flow through it unchanged).

## Commits

- `0df436c` P-012: creative-scoring evidence-nudge layer (option B, penalty-only)
  — single **product** commit (`creative.py` +100/−11, `tests/test_creative_nudges.py`
  new 292 lines / 43 cases).
- `7341cd5` Confirm P-012 (creative-scoring nudge layer, penalty-only) as active
  packet — **non-product** (memory-only: `build-os/packets/active_packet.md`).

## QA proof

- **Suite:** `python -m pytest` → **202 passed**, 0 failed, 0 skipped,
  0 warnings (159 prior + 43 new).
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68**,
  0 critical, 0 warnings. (Golden CANNOT read variant scores — `regression.py`
  reads `doctrine_score`, never `score_variant` — so the variant-scoring path is
  golden-unguarded; the **unit tests are the binding guard**, and 68/68 held
  regardless, confirming no doctrine-path collateral.)
- **Commit-1 iso:** worktree at `0df436c` → **202 passed**, 70 targeted,
  regression **68/68** → green.
- **CAP BINDS EXACTLY:** `width_bloom` with both rows firing — base_overall
  75.7 → 73.7 = `base − 2.0` (raw −14 → clamped to the cap). The clamp binds on
  the summed-overall axis.
- **NO RECOMMENDATION FLIP** on the 3 fixtures: `dense_chorus_with_loops` fires
  row 2 on the LOSING `chorus_lift_A`; winner stays `chorus_lift_B`; row 1 never
  fires (no masked vocal on any fixture — like the prior latent `width_bloom −8`).
  `score_nudges` absent when no nudge fires.
- **Scope check:** exactly the 2 files changed; `_KIND_SCORES` values unchanged;
  `governance` / `memory` / `pipeline` / `album` / `next_pass` untouched.
- **Safety grep:** none found (no network / subprocess / DAW / `.logicx`).
- **UI smoke:** N/A (engine-layer scoring change; no surface touched).

## Review

- **Verdict: pass** — and adversarially proven. The reviewer FORCED a −70 raw
  (−10.0 overall) penalty and the clamp STILL produced exactly `base − 2.0`,
  proving the cap binds on the summed-overall axis (not a leaky per-dim clamp).
  The reviewer compared layer-ON vs layer-OFF on real data, confirming the dense
  fixture genuinely fires a nudge yet no winner flips — i.e. the no-flip result is
  non-tautological (the layer is live, it just can't overturn the base gaps).
  Penalty-only proven across all kinds (no promote path); evidence predicates
  verbatim-reused; test-first reproduced (`ImportError` before implementation).
- **Codex second-eyes:** NOT available.
- **Product Trajectory Check:** resolves the standing OPEN USER DECISION ("deeper
  creative scoring") via the user's chosen option B — bounded / transparent /
  capped / penalty-only. Latent-but-armed: it changes nothing on today's 3
  fixtures but is ready to fire for a song that actually presents a masked vocal /
  crowded width. It lands on the **unmerged PR #13** for the user's sign-off
  before merge (the user's reviewed aesthetic change).

## Residue

- **Deferred / follow-up packets:**
  - **Reward nudges (orchestrator rows 3+4):** `depth_cleanup +6 halee` /
    `subtractive_drop +4 taste` when `crowded_sections` is non-empty — a possible
    later ADDITIVE packet IF the user wants reward (promotion) nudges. Deferred
    (P-012 is penalty-only by the user's recommended reading).
  - **Borderline near-tie fixture (informational):** a fixture that demonstrates
    an INTENDED near-tie flip through `analyze()` would make the option-B behavior
    visible on real data (today the layer fires but overturns nothing on the 3
    fixtures). Small additive test, future packet.
  - (carried) Borderline-song taste fixture (from P-009); wider `--memory-dir`
    CLI surface; net-new event-logging producers (product decision).
- **Known risks:** the variant-scoring path remains golden-unguarded by design —
  unit tests are the binding guard. Commits on this branch are unsigned
  (environment limitation; correct author/committer, GitHub shows "Unverified").

## Open boundaries (awaiting explicit go)

- **The product commit `0df436c` is local-only as of this close** (this archivist
  close did not push). It carries the user's reviewed aesthetic change and is
  **awaiting the user's sign-off at PR #13 merge**. Earlier local-only product
  commits also remain (`effccd0` + `ea9bebf` P-011; `27bfebf` P-009;
  `dc61f20` + `9ebd4ee` P-010). Any push of these updates the already-open
  **PR #13** (base `claude/dreamy-turing-z0oxll`) — do so only under the user's
  explicit push-go. No merge / deploy / secret action taken.
