# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-012
- **Title:** Creative-scoring evidence-nudge layer — option B, PENALTY-ONLY (bounded, transparent, reviewable)
- **Authority:** build (the user chose option B; PENALTY-ONLY per orchestrator recommendation)

## ⚠️ This packet DELIBERATELY changes default recommendations when a nudge fires

Unlike P-007…P-011, this is **NOT byte-identical by default** — that's the point of
option B. It's the user's reviewed aesthetic change; it lands on the unmerged PR
#13 for review before merge. The variant-scoring path is **golden-unguarded**
(`regression.py` reads `doctrine_score`, never `score_variant`), so **unit tests
are the binding guard, not the 68/68 golden** (which stays 68/68 regardless).

## Scoring math (verified)

- `score_variant` (`creative.py:248-261`): `overall` = mean over 7 numeric dims
  minus a risk penalty. So a single-dim nudge of magnitude N moves `overall` by
  **N/7**. The existing `width_bloom`+`lead_masked` → `vocal_belief −8` moves overall
  by −1.14. Downstream: `governance.py:243` ranks variants by `overall_score`
  (→ governed winner); `creative.py:286` `winning_variant` = max overall.

## Goal / "done" criteria

- Refactor the existing context nudge into a pure `_apply_nudges(kind, base, result)
  → list[(dim, delta, reason)]`; add `CREATIVE_NUDGE_CAP = 2.0` (overall-pts) and a
  `_NUDGE_TABLE` (the 2 penalty rows below); clamp the **summed overall delta** to
  `±CREATIVE_NUDGE_CAP`; `score_variant` returns `score_nudges: [reasons]` ONLY when
  ≥1 nudge fires; `overall_score` stays `[0,100]`. The curated `_KIND_SCORES` base is
  untouched. Existing `width_bloom`+`lead_masked −8` reproduced as table row #1.

## THE NUDGE TABLE (penalty-only — rows 1+2)

| # | Kind(s) | Evidence condition (exact `result` read) | Dim | Mag | Evidence string |
|---|---|---|---|---|---|
| 1 | `width_bloom`, `vocal_ride`, `intimacy_pass` | any `result.masking_report["events"]` with `classification=="bad_masking"` AND an element containing `"vocal"` (verbatim `creative.py:252-255` predicate) | `vocal_belief` | **−8** | `"vocal_belief -8: lead vocal is masked (bad_masking) — pushing a vocal-forward move is risky"` |
| 2 | `width_bloom` | any `result.masking_report["events"]` with `classification=="width_crowding"` | `vocal_belief` | **−6** | `"vocal_belief -6: stereo image is already width-crowded"` |

- Worst-case stack = rows 1+2 on `width_bloom` = −14 raw = **−2.0 overall = exactly
  the cap** (the clamp must bind here). Penalty-only → a nudge can only LOWER a
  score, never promote a variant.

## Out of scope (explicit)

- **No `_KIND_SCORES` rewrite** (that's option C).
- **Reward nudges (the orchestrator's rows 3+4** — `depth_cleanup +6 halee` /
  `subtractive_drop +4 taste` on `crowded_sections`) are **DEFERRED** — a possible
  later additive packet if the user wants reward nudges; NOT in P-012.
- No governance/memory/pipeline/next-pass/album changes; do not alter the
  `verdict`/`check vocal wash` text logic (dims flow through it unchanged).

## Real-fixture impact (for the user's review)

- **ZERO** `winning_variant` / `governed_winner` changes on the current 3 fixtures
  (simulated). Row #1 never fires (`lead_masked=False` on all 3 — like the existing
  latent −8); row #2 fires visibly on `dense_chorus_with_loops` but the bounded
  effect (≤0.86 overall) can't overturn the base gaps (2.4–4.2). Latent-but-armed
  for a song that actually presents a masked vocal / crowded width.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `4dfe142` (clean). Default
  `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** `creative.py` nudge layer +
   `tests/test_creative_nudges.py` (the full safety-invariant suite); passes its own
   tests standalone AND `tests/test_creative.py`/`test_creative_attribution.py`/
   `test_governance_taste.py` stay green; regression 68/68.
2. **Commit 2 (optional):** only if the reviewer wants extra fixture-level
   governed-winner assertions.

## Safety-invariant tests (BINDING — golden can't catch this)

- (a) **Cap:** for every kind × evidence combo, `|nudged_overall − base_overall| ≤
  2.0`; assert the `width_bloom` rows-1+2 worst case lands at exactly the cap.
- (b) **Fires-only-on-evidence + emits line:** signal absent → no `score_nudges` key,
  dims == base; present → exact evidence string + the named dim moved by the table
  magnitude.
- (c) **Base-ranking preservation:** two synthetic variants whose base `overall`
  differ by `> cap`, max adverse nudges → relative order unchanged (proves it only
  re-orders near-ties).
- (d) **Determinism;** (e) **clamp** `overall ∈ [0,100]` under extreme bases;
  (f) **real-fixture impact:** drive the 3 fixtures through `run_creative_engine`/
  `govern_branches` → assert current `winning_variant`/`governed_winner` unchanged
  (pins "no silent recommendation flip on real data").

## Guardrails

- Build authority; deterministic; bounded (cap binds); transparent (evidence line
  per nudge); penalty-only; no network/subprocess/DAW/`.logicx`; curated base
  untouched. STOP at push/merge (unmerged PR #13 = the user's review gate).

---
_Confirmed P-012 (option B, penalty-only) on the user's "keep going". The nudge
table was shown to the user for review; lands on the unmerged PR for sign-off
before merge. Builder implements exactly this; archivist clears on close._
