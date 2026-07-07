# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-060 — Section-Count-Invariant Doctrine Scoring**
  (opened on the user's "ok go", 2026-07-06: dedup distinct conflicts; accept the
  surgical `dense` corpus move; P-061 for detector calibration next). Base = dev
  HEAD `9cfe990` (= PR #37 / P-059 merge; verify `git merge-base HEAD 9cfe990` =
  `9cfe990`). **This is the FIRST packet to intentionally move the committed
  scoring corpus** — the user signed off on the exact move below.
- **Baseline to protect:** suite **1405** / regression **93/93 (0 warnings)** —
  and, EXCEPT for the one authorized `dense_chorus_with_loops` move below, the
  whole corpus stays byte-identical (the other 3 fixtures + all 5 sample trees +
  mode demos UNCHANGED; producer profiles / governance / kill-switches / dropout
  filter / doctrine weights UNTOUCHED).

## Why (a real 49-track session exposed it)

The user re-ran real "Happy Man" after P-059 (auto-detected 12 sections) and the
verdict CRATERED: emotional_hierarchy/vocal_centrality → 0, physical_space → 2,
"masked by 48 forward elements" (was 4 = 4×12). Root cause: `analyze_masking`
(`masking_analyzer.py:90`) emits each masking conflict ONCE PER SECTION, and SIX
doctrine scorers count `len(per-section events)` raw — so a conflict duplicated
across N sections is penalized N×. Hidden by the 2-section fixtures; craters real
many-section songs. Proven even at 2 sections: `dense`'s Kick/Bass critical
low-end is counted 2× today.

## Scope — the section-count-invariance fix (FORK A = dedup distinct pairs, scorer-side)

A shared helper counts DISTINCT masking relationships —
`len({frozenset(e["elements"]) for e in filtered})` — applied AFTER each scorer's
EXISTING classification/severity predicate (filter-then-dedup, never dedup-first).
The six scorers in `doctrine/doctrine_engine.py` that currently scale with section
count, each switched to the deduped count:

| Scorer | ~line | counts today (scales) |
|---|---|---|
| `_emotional_hierarchy` | 272–275 | `len(bad_vocal)` (bad_masking incl. lead) |
| `_vocal_centrality` | 306–309 | `len(bad)` (bad_masking incl. lead) |
| `_static_mix` | 360–363 | `len(crit_low)` (critical low_end_conflict) |
| `_low_end_motion` | 832–835, 883 | `len(crit)`, `len(mod)` (low_end_conflict) |
| `_physical_space` | 238–241 | `len(width_events)` (width_crowding) |
| `_vocal_role_fit` | 1308–1372 | `len(involved)`, `len(own)` (band masking) |

`_beat_identity` (~463) and `_loop_context`/`read_loop_context` (~1046) already use
boolean `any(...)` — do NOT scale, LEAVE UNTOUCHED (they are the correct pattern
the fix emulates). `masking_report.events` STAYS per-section (the plan's
per-section recommendations are a feature — do not change event emission).

**Ordering guardrail (proven by a real fixture):** filter by the scorer's existing
predicate FIRST, then dedup the filtered list. `vocal_chop_groove` has
`(BGV Chop, Electric Guitar)` moderate in verse_1 / info in chorus_1 —
`_own_band_masking` filters `severity != "info"` first, keeping the moderate; a
dedup-before-filter would wrongly drop it. The invariance test MUST cover this.

## The authorized corpus move (surgical — ONE fixture, a correctness fix)

Measured against the real pipeline. ONLY `dense_chorus_with_loops` moves:
- **static_mix 64.0 → 72.0** (+8.0)
- **low_end_motion 21.1 → 35.1** (+14.0)
- **overall_mix_readiness 70.7 → 71.8** (+1.1)
- physical_space 67.6 → 67.6 (unchanged — its width_crowding is verse-only, already distinct)

Cause: `dense`'s `(Kick, Bass)` critical low-end conflict is emitted identically in
BOTH sections (static band_energy) — a pure duplicate 2×→1×. **UNCHANGED (proven):**
`simple_vocal_piano_song` / `splice_loop_problem` (no masking events);
`vocal_chop_groove` (its 2 moderate events are verse_1-only → genuinely
section-specific → already counted once); **all 5 sample trees** (they are
`vocal_chop_groove`-derived, 2 sections, no duplicated conflict → do NOT move).

**Re-pin surface:** `fixtures/dense_chorus_with_loops/golden/snapshot.json` (scores)
+ ~13 test files carrying dense's `static_mix=64.0` / `low_end_motion=21.1` /
`overall=70.7` pins (the builder verifies each literal is dense's before editing;
e.g. `test_low_end_motion`, `test_static_*`, `test_three/four/five_way_differential`,
`test_confidence_map`, `test_vocal_chop_groove`, `test_timbaland_profile`,
`test_vocal_blend_policy`, `test_vocal_band_masking`, `test_rhythmic_surprise`,
`test_groove_coherence`, `test_loop_context`, `test_vocal_type`). Every moved
number is the SAME correction (Kick/Bass = one relationship, 2×→1×).

## The NEW invariance test (the regression that would have caught this)

`tests/test_section_count_invariance.py`:
1. Synthetic records exercising ALL six scorers (lead masked by ≥2 forward
   elements + a Kick/Bass critical low-end + a width-crowding trio).
2. `score_doctrine` on the SAME records with **1 vs 6 vs 12** supplied sections,
   identical `depth_by_section` → assert every masking-driven component score is
   IDENTICAL across 1/6/12.
3. Over-correction guard: a masker forward in only 1 of N sections (the
   verse-only / info pattern) → the distinct conflict STILL registers once (not
   zero, not N×).

## Regression 93/93 (0 warnings) — kept honest

The structural `doctrine_invariants` do NOT shift (dedup changes no
classification/structure). `93/93` is `run_regression_suite`'s fixed check count;
re-pinning `dense`'s golden `scores` keeps `critical_failures == []`. `static_mix
+8.0` exceeds `SCORE_WARN=3.0` (under `SCORE_FAIL=9.0`), so the golden MUST be
re-pinned to the corrected values → 0 warnings preserved.

## Commit shape (≤2; Commit-1 green in isolation — ATOMIC by necessity)

- **Commit-1 (atomic, load-bearing):** the shared dedup helper + the six scorers
  using it (`doctrine_engine.py`) + NEW `tests/test_section_count_invariance.py` +
  ALL re-pins (dense golden `snapshot.json` scores + the ~13 dense test pins).
  Fix and re-pin are INSEPARABLE — split across commits and either half is red.
  Full suite GREEN in isolation.
- **Commit-2 (optional, additive):** a decisions/CHANGELOG note recording the
  corpus move + per-number justification (no runtime touch). May be omitted → a
  valid 1-commit packet.

## Required proof (qa reports exact)

Full suite 1405 → 1405 + the invariance test (exact); the invariance test GREEN
(1/6/12 identical + section-specific still registers once); `run_regression_suite`
**93/93, critical_failures == [], 0 warnings** after re-pin; Commit-1 green in
isolation; safety grep — NO producer-profile JSON change, NO governance /
kill-switch / dropout / doctrine-weight change, NO new dependency (numpy +
first-party only), `masking_report` events STILL per-section; the corpus-move
table (dense static_mix 64→72, low_end_motion 21.1→35.1, overall 70.7→71.8, each
justified "Kick/Bass = one relationship, 2×→1×"; all other fixtures + 5 sample
trees proven unchanged).

## Non-scope (BINDING)

BUG 2 detector over-segmentation calibration → **P-061** (next packet). Plan-only
(no apply-to-Logic). numpy + first-party only, no new dependency. NO
producer-profile / governance / kill-switch / dropout / doctrine-weight change
(the penalty COEFFICIENTS stay — only the COUNT they multiply is deduped). NO
change to per-section event emission / plan detail. Roster frozen at five.

## Route after builder

builder (atomic Commit-1) → qa → reviewer → archivist (receipt
`build-os/receipts/P-060-section-count-invariant-scoring.md`). Commit only — no
push/merge/deploy without the user's explicit go (the standing dev-branch push-go
covers the pre-gate push).

---
_Set active on the user's "ok go" (2026-07-06, dedup distinct conflicts + the
authorized surgical dense corpus move; P-061 for detector calibration next), after
the P-059 merge (PR #37 → `9cfe990`). One packet at a time: builder → qa +
reviewer → archivist → receipt._
