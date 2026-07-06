# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-059 — Audio-Driven Section Detection** (opened on the
  user's "go", 2026-07-06: honest structural+energy labels; P-058 merged first).
  Base = dev HEAD `32d7f47` (= PR #36 — P-058 merged to default; the branch is
  fast-forwarded onto it). Verify `git merge-base HEAD 32d7f47` = `32d7f47`.
- **Baseline to protect:** suite **1390** / regression **93/93 (0 warnings)** /
  the 4 fixtures + 5 sample trees + mode demos byte-stable / the doctrine engine,
  5 profiles, governance, kill-switches, dropout filter UNTOUCHED.

## Why this packet (a REAL first-audio session surfaced it)

The user ran P-058's on-ramp on a real 49-track song and it worked — but the
engine analyzed the WHOLE song as ONE block, because it only *analyzes* sections
it is GIVEN (from the manifest) and never *detects* them from audio. Result:
`Section contrast: n/a`, `Dynamic mix: 40` — a FALSE "no dynamics" diagnosis
that is purely an artifact of the missing section map, and a blind "open in
choruses / pull back in verses" automation plan with no chorus data. The user's
directive: **infer the sections from the audio — "based on what's added at
various points"** (each stem's entry/exit over time = arrangement events =
section boundaries). This packet builds that.

## Scope — new `analyzers/section_detector.py` (deterministic, numpy + first-party dsp only)

**Primary signal = per-stem active-region → arrangement events (the user's directive):**
1. **Common frame grid** (hop `H ≈ 0.25s`) over `[0, mixdown.duration]`; per resolved
   stem (from `loaded_by_id`, sorted `track_id` for determinism) compute per-frame
   RMS dBFS (reuse `dsp.rms_dbfs` / `rms_envelope`). A short stem is silent past its
   end → reads as an EXIT (correct).
2. **Two-part silence gate:** a stem is active when
   `rms_db > max(ABS_FLOOR_DB=-50.0, stem_active_peak_db − REL_RANGE_DB=40.0)` →
   a boolean activity matrix `(n_stems × n_frames)`.
3. **Debounce/hysteresis:** a state change must persist ≥ `MIN_RUN` frames; fill
   gaps ≤ `GAP` frames (~0.5s) so a breath/rest doesn't toggle a stem.
4. **Arrangement novelty:** per frame, `novelty = #stems whose active-state changed`
   (Hamming distance of the active-set bitmask) — entrances AND exits count.
5. **Boundaries** at frames where `novelty ≥ 1`, clustered within `CLUSTER_WIN`
   (~1.0s); `t=0` is always the first boundary → `Section(section_id="section_N",
   name="Section N", start, end, emotional_goal=None)`.

**Secondary signal (accepted default):** a mixdown RMS/density novelty from
`rms_envelope(mixdown)` is a **corroborating tie-breaker ONLY** — it never creates
a boundary on its own (energy-alone reacts to WITHIN-section dynamics, exactly the
artifact that produced the false `Dynamic mix: 40`). Arrangement activity stays
primary — faithful to "based on what's added."

## Labeling (user's call = HONEST structural + energy tag)

Structural labels `section_1..N` + a **relative `energy_tag`** (high/med/low, from
each detected section's mean active-stem-count / density), every detected section
marked `inferred: true` + surfaced in a `_needs_review`-style list. **NO semantic
verse/chorus/bridge naming** — function is not honestly inferable from audio alone;
"Section 3 (high energy)" reads chorus-like without CLAIMING it. The user renames
in the manifest if desired; the doctrine engine only needs distinct, contrasting
sections, not names.

## Integration hook + byte-stability boundary (the critical invariant)

**One shared detector, guarded by `len(project.sections) <= 1`:**
- **`len(project.sections) >= 2` → UNCHANGED** `analyze_sections(project.sections,
  mixdown, lead_vocal_loaded)` — the detector is NEVER entered. Every committed
  fixture (2 sections) + sample tree (5 sections) is provably byte-identical.
- **`len(project.sections) <= 1` → `detect_sections(loaded_by_id, mixdown,
  duration)`** → feed the detected `Section` list into the SAME `analyze_sections`.
  The `inferred`/`energy_tag` stamps appear on THIS branch only (supplied-path
  output shape untouched). This is the fix for real sessions like "Happy Man".
- Regression invariant #7 (`regression.py:211`) holds: supplied-section corpora
  keep count ≥2, so `section_contrast_score` stays non-None → **93/93 untouched**.

## Guardrails

`MIN_SECTION_SEC = 4.0` (merge sub-min segments into a neighbor); `MAX_SECTIONS =
12` (keep top-novelty boundaries); always-on tracks (a full-mix bus / an eternal
pad) toggle never → contribute ZERO boundaries (robust by construction);
determinism (fixed grid + constants, no randomness, sorted stem order, times
rounded to 3 decimals).

## Non-scope (BINDING)

No doctrine scoring-math change; no producer-profile / governance / creative /
kill-switch / dropout-filter change — the detector produces BOUNDARY DATA that
feeds the EXISTING `analyze_sections`. No new dependency (numpy + first-party
`dsp` only — if one is genuinely needed, STOP AND FLAG). No audio-write, no DAW,
no Logic session (plan/data only). NEVER overrides manifest-supplied sections
(≥2). No semantic section naming. The scaffolder's audio-driven detection is
STRICTLY OPT-IN (default header-only path byte-identical, its `len==1` stub test
unchanged on the default path).

## Commit shape (≤2; Commit-1 green in isolation)

- **Commit-1 (load-bearing):** `analyzers/section_detector.py` + the guarded
  `pipeline.analyze` auto-detect wire + detector unit tests + the byte-stability
  regression proof. Green in isolation with the ENTIRE committed corpus
  byte-identical (the detector branch provably not entered).
- **Commit-2 (additive UX):** scaffolder `--detect-sections` opt-in (default OFF,
  same shared detector) + updated `test_onramp_scaffold` for the opt-in path +
  a `docs/REAL_SESSION.md` note.

## Required proof (qa reports exact)

Full suite 1390 → 1390 + new (exact); regression **93/93, 0 warnings** UNCHANGED;
safety grep 0 reach (no push/deploy/secret, no audio-write, no new import beyond
numpy + first-party); **synthetic multi-section detection test** (in-memory stems:
drums enter @t1, bass @t2, a pad plays THROUGHOUT (always-on → NO boundary), vocal
@t3, drums exit at a drop → detector finds boundaries at ~t1/t2/t3/drop within
tolerance and NOT at spurious points); **supplied-section fixtures (4) + sample
trees (5) byte-identical** (golden + differential + sample_refresh all pass; the
detector branch provably not entered); **determinism** (twice → identical `Section`
list); Commit-1 green in isolation.

## Route after builder

builder (Commit-1 detector+wire+tests; Commit-2 scaffolder opt-in) → qa → reviewer
→ archivist (receipt `build-os/receipts/P-059-audio-driven-section-detection.md`).
Commit only — no push/merge/deploy without the user's explicit go (the standing
dev-branch push-go covers the pre-gate push).

---
_Set active on the user's "go" (2026-07-06, honest labels + P-058 merged first),
after the P-058 merge (PR #36 → `32d7f47`). One packet at a time: builder → qa +
reviewer → archivist → receipt._
