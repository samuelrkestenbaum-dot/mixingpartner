# Receipt — P-061: Detector Over-Segmentation Calibration

- **Packet:** P-061 — Detector Over-Segmentation Calibration. **The OTHER HALF of
  the Happy Man fix.** P-060 fixed the masking crater; P-061 fixes the **fake
  100/100 contrast/dynamics**. On a real 49-track song ("Happy Man") the
  audio-driven section detector emitted **12 micro-sections**, and two doctrine
  scorers that read per-section dispersion therefore INFLATED with section count:
  `_dynamic_mix` (`doctrine/doctrine_engine.py:394` — `pstdev` of per-section
  rms / width / crest) and `_section_contrast` (`:351` — `contrast_vs_previous`
  lift-fail counting). More spurious sections → more dispersion and more
  "contrast" events → a **ceiling-pinned fake 100/100**. The sections were not
  real, so neither was the score. The fix makes the DETECTOR emit honest musical
  sections.
- **Date:** 2026-07-26
- **Branch:** `claude/logic-mix-os-p061-detector-0dvr2t`, HEAD `a96a4cc`.
- **Branch base (merge-base):** `git merge-base HEAD 9cfe990` = **`9cfe990`**
  (= PR #37 / P-059 merged to default) — the correct base, verified at close.
  Packet base = `e3d633c` (the P-060 close + HANDOFF tip).
- **Status:** **CLOSED — BOTH FORMAL GATES GREEN.** qa GREEN (suite **1426 passed
  / 0 failed / 0 warnings**; regression **93/93, `critical_failures == []`, 0
  warnings**; **independent detached Commit-1 isolation at `4cbee14` = 1420 / 0 /
  0**) + reviewer **PASS (no must-fix)**. An earlier qa/reviewer dispatch against
  `4cbee14` stalled and never returned; both gates were **re-run against final
  HEAD** and delivered in full, including the Commit-1-isolation item the stalled
  gate never produced.

## Scope

**In (what shipped):**

1. **`logic_mix_os/analyzers/section_detector.py` — the SECONDS-level constants
   only.** The frame integers stay **DERIVED** by design via
   `max(1, round(_X_SEC / H))` with `H = 0.25`; no frame integer was hand-edited.
2. **Re-pins + net-new tests in `tests/test_section_detector.py`** (10 → 22).

**Explicitly out (binding non-scope, held):**

- `pipeline.py`'s section guard · `doctrine_engine.py` · `masking_analyzer.py` ·
  `onramp.py` behavior — all UNTOUCHED and proven byte-identical.
- **ALL goldens / sample trees / mode demos** — byte-identical.
- **No new dependency** — `section_detector.py` imports only `typing`, `numpy`,
  and first-party.
- **No adaptive novelty floor** — constants alone were sufficient, so the scope
  decision that would have had to route back through the orchestrator never
  arose.
- **A spacing-aware `_cap_sections`** — named, deferred to its own future packet
  (see Residue), deliberately NOT smuggled in.
- Merge / PR / deploy / secrets — no PR exists for P-061; nothing merged.

## Commits and base

| Commit | Subject |
|---|---|
| `4cbee14` | P-061 Commit-1 — detector over-segmentation calibration (persistence floor is the ornament line). 2 files, +133/−16. |
| `d941ecc` | P-061 Commit-2 — gap-fill floor to match the persistence floor (phrased parts survive). 2 files, +130/−2. |

**Two implementation commits = AT the ≤2 contract limit, not over it.** Chain:
`a96a4cc` (docs: design3→design4 handoff-integrity audit, documentation only —
current HEAD) → `d941ecc` → `4cbee14` → `6c81090` (P-061 set-active,
metadata-only) → `e3d633c` (P-060 close + HANDOFF, the pre-P-061 base) →
merge-base with default `9cfe990`.

**Push state:** the two implementation commits are pushed to the dev branch under
the standing pre-gate go. **NO PR exists. Default is untouched at `9cfe990`.**

## What actually changed — constants as SHIPPED

| Constant | Was | Packet target | **SHIPPED** | Frames (H=0.25) |
|---|---|---|---|---|
| `_MIN_RUN_SEC` | 0.5 | ~1.5 | **5.0** | `MIN_RUN` 2 → **20** |
| `_GAP_SEC` | 0.5 | (untargeted) | **5.0** | `GAP` 2 → **20** |
| `_CLUSTER_SEC` | 1.0 | ~2.0 | **2.0** | `CLUSTER_WIN` 4 → **8** |
| `MIN_SECTION_SEC` | 4.0 | ~8–10 | **7.0** | 16 → **28** |
| `MAX_SECTIONS` | 12 | ~8 | **12 — UNCHANGED** | — |

`_MIN_RUN_SEC` 0.5 → 5.0 is **THE load-bearing change**. `_GAP_SEC` is Commit-2.
`_CLUSTER_SEC` 1.0 → 2.0 was proven an **inert no-op** on all scenarios.

**Live invariant, asserted by test:** `_MIN_RUN_SEC <= _GAP_SEC < MIN_SECTION_SEC`
(**5.0 <= 5.0 < 7.0**).

## ★★★ THREE PACKET TARGETS WERE REFUTED BY MEASUREMENT

This is the headline finding of P-061. The set-active text's numeric targets were
not merely tightened — three of them were **measured to be wrong** and
deliberately overridden, loudly, in source + commit message + packet.

1. **`MIN_SECTION_SEC` ~8–10 → shipped 7.0.** **8.0 is knife-edge:** measured
   jitter tolerance **0.00s** against the 32-frame (8.0s) synthetic sections —
   any debounce jitter merges a REAL section. **9.0 / 10.0 destroy the
   arrangement tests** outright. **7.0** is the largest value with genuine margin
   (**0.40s**).
2. **`_MIN_RUN_SEC` ~1.5 → shipped 5.0.** **1.5s is provably INERT** — the
   ornaments this packet exists to suppress are **3–4s** long, so the packet's own
   target **would not have fixed the bug at all.** Plateau [4.5, 8.0] identical.
3. **`MAX_SECTIONS` ~8 → left at 12.** **Refuted by measurement, and the most
   important of the three.** `_cap_sections` sorts survivors by novelty **with NO
   spacing term**, so whenever the cap BINDS it **MANUFACTURES the very artifact
   this packet removes**: MAX=8 produced an **80s super-block**, MAX=10 a **60s**
   one — both **worse than the 64s bug being fixed**. The persistence floor should
   do the work; the cap stays a safety valve. The correct fix is a **spacing-aware
   `_cap_sections` = a SEPARATE FUTURE PACKET**, named and deferred rather than
   smuggled in.

## ★★★ COMMIT-1 SHIPPED A LIVE REGRESSION THAT COMMIT-2 FIXED — recorded honestly

Commit-1 raised the persistence floor to 5.0s but **left gap-fill at 0.5s**. A
lead vocal sung in **4.0s phrases with 1.2s breaths** then fragments into
16-frame runs, **every one of which dies under the 20-frame floor** — the vocal is
**ERASED from arrangement detection entirely** (235 active frames → **0**).

**Found by coordinator probe, NOT by the suite.** Commit-1 was green in isolation
only because **no test covered the phrased-part shape**. The reviewer's phrasing:
**"Commit-1's isolation-greenness was true but blind."**

| `_MIN_RUN_SEC`/`_GAP_SEC` | vox frames after debounce | sections | vocal entrance @32s |
|---|---|---|---|
| 0.5 / 0.5 (pre-P-061) | 235 | 6 | NO |
| 5.0 / 0.5 (`4cbee14`) | **0 — ERASED** | 2 | NO |
| 5.0 / 5.0 (`d941ecc`) | **287** | 4 | **YES** |

**Commit-2's fix does not merely undo the damage.** At 5.0/5.0 the vocal survives
(287 frames) **AND** produces a **TRUE vocal-entrance boundary at 32s that NEITHER
the pre-P-061 constants NOR Commit-1 achieved**, while removing the pre-P-061
phrase confetti at 52.75 / 67.25 / 78.75s.

**200s over-segmentation repro:** 12 sections with 4.0s / 4.0s / 7.0s slivers plus
a cap-induced 64s super-block → **9 sections, no slivers, the cap never binds.**
Identical at Commit-1 and Commit-2.

## QA proof (GREEN — re-run against final HEAD)

- **Suite:** **1426 passed / 0 failed / 0 warnings** (1414 pre-P-061 baseline +
  **12 net-new**).
- **Regression:** **93/93**, `critical_failures == []`, `warnings == []`.
- **★ INDEPENDENT COMMIT-1 ISOLATION** — the item the stalled gate never
  delivered: detached at **`4cbee14`** from a clean tree with an empty stash,
  fixtures regenerated per the standing P-025 env fact → suite **1420 passed / 0
  failed / 0 warnings**, regression **93/93, `critical_failures == []`**. Returned
  to the branch cleanly. **Commit-1 IS green in isolation.**
- **Safety grep:** `"inferred"` → **ZERO files**. The frozen set is
  **byte-identical across `e3d633c..HEAD`**: `pipeline.py`, `doctrine_engine.py`,
  `masking_analyzer.py`, `onramp.py`, `pyproject.toml`, all `fixtures/*/golden`,
  all `examples/`. **No new dependency** — `section_detector.py` imports only
  `typing`, `numpy`, and first-party.
- **Dangerous-pattern grep:** none. **Debug leftovers:** none.
- **Non-vacuity by monkeypatch (no committed edit):**
  - neutering `_cap_sections` → `assert 16 == 12`, **SOLE failure**;
  - neutering `_merge_short_sections` → `assert 4.0 >= 7.0 - 1e-6`, **SOLE
    failure**;
  - reverting `_GAP_SEC` to 0.5 → **EXACTLY 4 failures in
    `TestPhrasedPartSurvives`, nothing else**.
- **Re-pin surface:** only **ONE** test file touched
  (`test_section_detector.py` **10 → 22** tests); `test_onramp_scaffold.py` has
  **ZERO re-pins** (29 tests, untouched) — well inside the packet's "up to 15
  across 2 files" upper bound. **2 pre-existing tests re-pinned, 12 net-new.**
- **UI smoke:** **N/A** — this is an analyzer/engine packet; no UI surface is
  touched (recorded as such, not silently skipped).
- **Diff:** exactly **2 product/test files** across both commits.

## Reviewer verdict — PASS (no must-fix)

**Single-reviewer only. `command -v codex` returns nothing, so NO second model
reviewed this diff.** Stated plainly: no second-model verdict is claimed.

**(A) `test_max_sections_cap` NON-VACUITY — SIGNED OFF, re-derived by hand.**
Re-spaced to **15 entrances 10s apart over 160.0s**; every run **≥ 40 frames** vs
`MIN_RUN` 20; entrances **40 frames apart** vs `CLUSTER_WIN` 8; sections **40
frames** vs the 28-frame floor, so the merge is a **genuine no-op**; pre-cap
boundary count **16 > MAX_SECTIONS 12**, so the **cap BINDS**. `==` ruled the
**CORRECT** assertion (it is `_cap_sections`'s post-condition, written in terms of
the constant), not a brittle over-pin — `<=` is exactly the shape that let this
test rot silently once.

**(B) ★ `_GAP_SEC = 5.0` ADJUDICATED AND ACCEPTED.** The reviewer **REFUTED the
"[1.5, 6.5] all fix it equally" framing** carried into the gate. `_debounce` fills
**THEN** drops, so erasure occurs exactly when **phrases < MIN_RUN and rests >
GAP**. At `_GAP_SEC = 1.5` an **erasure window stays OPEN** for rests in
(1.5s, 5.0s) — and **a 1-bar rest at 120bpm is 2.0s; a 2-bar rest at 96bpm is
5.0s**. Lower plateau values fix the **PROBE**; only **`_GAP_SEC >= _MIN_RUN_SEC`
fixes the CLASS**, making fragment-then-erase **structurally impossible** (erasure
would require sub-floor bursts separated by super-floor rests — which is the
definition of an ornament).
- **ACCEPTED COST, named honestly:** the lost boundary class is the **re-entry
  point of a 1.5–5s dropout at which NO other stem changes state** (the classic
  drum-drop-before-chorus).
- **Why accepted:** (1) the loss is **LOCAL under-segmentation** while erasure is
  **GLOBAL and silent** — an erased stem corrupts every boundary in the song, and
  it hits the **lead vocal** precisely because phrasing-with-rests is what vocals
  do; (2) in practice a real drop-before-chorus has other stems moving at the same
  frame, so the boundary survives, and the genuinely-lost case is an ornament
  inside a part; (3) the residual boundary was an artifact of
  `_merge_short_sections` dropping ONE boundary rather than two — leaning on it
  would be relying on an implementation accident.
- **Coupling decision ruled SOUND** (independent literals + a test-enforced
  invariant): `_GAP_SEC = _MIN_RUN_SEC` would auto-satisfy the lower bound while
  **silently breaching the upper one** if `_MIN_RUN_SEC` were ever raised. Also
  `round()` is **monotone**, so the seconds-level invariant guarantees
  `GAP >= MIN_RUN` at **any** `H`.

**(C) Scope — CLEAN.** Exactly 2 product/test files; frame integers still derived;
verified by object hash.

**(D) Product Trajectory Check — SERVES the honest-labelling principle.**
Labelling / tagging / primacy are untouched; the change is to **what COUNTS as an
arrangement event** — a principled definition, not a knob. **The tell:** Commit-2
**DISCOVERS a new correct boundary** (the vocal entrance) rather than merely
suppressing failures — *"tuning-until-quiet does not discover new correct
boundaries."* Holding `MAX_SECTIONS` at 12 against the packet was ruled **CORRECT
ENGINEERING, not scope evasion**: the deviation is recorded loudly in source,
commit, and packet; the correct fix is named and deferred to its own packet rather
than smuggled in; and it **REDUCES** the change surface.

**(E) Commit-message numbers re-derived independently — all check out:** frame
conversions, 3–4s ornaments = 12–16 frames, 4.0s phrase = 16 frames, 1.2s breath
≈ 4–5 frames, vocal span 288 frames vs 287 reported, "2-bar rest at 96bpm =
exactly 5.0s". Tradeoffs are **acknowledged rather than smoothed**.

## Residue — three NON-BLOCKING items the reviewer requires recorded

These are recorded, **not** a re-review loop.

1. **Stale inline comment.** `logic_mix_os/analyzers/section_detector.py:199` —
   the comment *"a breath / rest must not toggle a stem off"* is **STALE for a
   5.0s window**; the block at lines **57–79** carries the real semantics.
2. **Looser-than-its-docstring behavioural test.**
   `test_gap_fill_does_not_outgrow_the_section_floor`'s companion BEHAVIOURAL test
   uses `rest = MIN_SECTION_SEC + 1.0`, so it guards **~8.0s** rather than the
   stated **7.0s** ceiling. The invariant assertion covers the stated bound, so
   the pair is adequate — but the behavioural test is looser than it reads.
3. **`MIN_SECTION_SEC = 7.0` is a fixture-shaped constant.** It carries only
   **1.0s margin** over a genuine 4-bar section at 120bpm (7.0s is ~3.5 bars) —
   **the constant most likely to need revisiting on real material with tempo
   drift.**

**Carried forward (new):**

- **A spacing-aware `_cap_sections` is the named FUTURE PACKET** that would let
  `MAX_SECTIONS` drop below 12. Until it exists, lowering the cap actively harms
  the output.
- **★ The pytest `-q` trap.** `pyproject.toml` sets `addopts = "-q"`, so invoking
  `pytest -q` **silently suppresses the summary count line while still exiting
  0**. Use bare `python3 -m pytest` or `-o addopts=""` to get counts. This
  **plausibly contributed to the earlier stalled gate producing no usable
  output.**

## Environment fact (must survive)

Canonical corpus env: **numpy + scipy + soundfile installed, `pyloudnorm` NOT
installed.** `dsp.integrated_loudness()` prefers **pyloudnorm → scipy → FFT**; the
committed corpus was produced on the **SCIPY tier**. With `pyloudnorm` installed,
**5 `test_sample_refresh` tests fail** on ~0.5dB `lufs` / `estimated_lufs` deltas
— an **ENVIRONMENT artifact, NOT a regression**; do not "fix" the corpus for it.
Verify `_HAVE_PYLN=False, _HAVE_SCIPY=True`. The standing **P-025 fact** still
applies: `fixtures/` is **GENERATED** — run `fixtures/generate_fixtures.py` before
regression in a fresh / detached checkout (this is exactly what the Commit-1
isolation run had to do).

## Open boundaries — NOTHING here is closed by this receipt

- **★★ THE OPEN USER GATE: the merge of P-060 to default.** Still open. Default
  remains **`9cfe990`**. Would be **PR #38**.
- **★ P-061's own merge is a SEPARATE, LATER gate.** **P-061 is CLOSED as a
  packet but NOT merged.** No PR exists for it.
- **Thread B** — the vendored Build OS `.claude/` update to ClaudeOrchestrator
  `7ef50e8`. Diagnosed, **not applied**; the user must still pick (a) an isolated
  PR to default, or (b) fold it into the merge.
- **PR #12** — still **OPEN** against the abandoned `main` base. Not closed here,
  just kept recorded. User gate: close it or rebase it.
- **P-024** — delivered-but-never-formally-retired (P-051 shipped the MCP server
  it specified; P-052 proved it E2E). **NOT retired in this close** — the note
  stands.
- **HAPPY MAN RE-RUN #2** — still the real-world confirmation for **both** halves
  (P-060's crater fix and now P-061's fake-100s fix).
- **Audit facts from `a96a4cc` (must survive):** **PR #22 = packet P-043** — PR
  numbers ≠ packet numbers; **merge-commit wording is inconsistent** (#17/#18 use
  "Merge pull request #NN", the rest "Merge PR #NN"), so grepping one form yields
  a **FALSE gap**; **commit signing is impossible in this container** (0-byte key,
  no private key) and **any re-author must be scoped to `e3d633c`, never to
  `origin/<this-branch>`**.

---
_Closed by the archivist (2026-07-26) with **BOTH formal gates GREEN**. qa GREEN
(suite **1426 passed / 0 failed / 0 warnings** = 1414 baseline + 12 net-new;
regression **93/93, `critical_failures == []`, warnings `[]`**; **independent
detached Commit-1 isolation at `4cbee14` → 1420 / 0 / 0**, regression 93/93 — the
item the earlier stalled dispatch never delivered; safety grep `"inferred"` ZERO
files; frozen set byte-identical; three monkeypatch non-vacuity proofs each a SOLE
failure) + reviewer **PASS, no must-fix** — **single-reviewer only; `codex` is not
installed, so NO second model reviewed this diff.** P-061 is the OTHER HALF of the
Happy Man fix: the detector's 12 micro-sections inflated `_dynamic_mix` and
`_section_contrast` to a ceiling-pinned fake 100/100, and raising the persistence
floor (`_MIN_RUN_SEC` 0.5 → **5.0**, the load-bearing change) with a matching
gap-fill floor (`_GAP_SEC` 0.5 → **5.0**), `_CLUSTER_SEC` 1.0 → 2.0 (inert) and
`MIN_SECTION_SEC` 4.0 → **7.0** makes it emit honest musical sections — 200s repro
12 → **9 sections, no slivers, cap never binds**. **THREE PACKET TARGETS WERE
REFUTED BY MEASUREMENT** and overridden loudly: `MIN_SECTION_SEC` ~8–10 → 7.0 (8.0
has **0.00s** jitter tolerance; 9/10 destroy the tests), `_MIN_RUN_SEC` ~1.5 → 5.0
(1.5s is provably INERT — ornaments are 3–4s — so the packet's target would not
have fixed the bug at all), and `MAX_SECTIONS` ~8 → **left at 12** (`_cap_sections`
has no spacing term, so binding it MANUFACTURES the artifact: MAX=8 gave an **80s**
super-block, MAX=10 a **60s** one, both worse than the 64s bug — a spacing-aware
`_cap_sections` is a separate future packet). **Commit-1 shipped a live regression
that Commit-2 fixed, recorded honestly:** at 5.0/0.5 a lead vocal in 4.0s phrases
with 1.2s breaths fragments into 16-frame runs that all die under the 20-frame
floor — **235 frames → 0, the vocal ERASED**; found by coordinator probe, not the
suite, because no test covered the phrased-part shape — *"Commit-1's
isolation-greenness was true but blind."* Commit-2 does not merely undo it: at
5.0/5.0 the vocal survives (**287** frames) and yields a **TRUE vocal-entrance
boundary at 32s that neither the pre-P-061 constants nor Commit-1 achieved**.
Two implementation commits `4cbee14` + `d941ecc` — **AT the ≤2 limit** — atop
set-active `6c81090` atop `e3d633c`, with docs commit `a96a4cc` at HEAD; verified
`git merge-base HEAD 9cfe990` = `9cfe990`. Pushed to the dev branch; **NO PR, NOT
merged.** **P-060's merge remains THE open user gate (would be PR #38, default
still `9cfe990`); P-061's own merge is a separate later gate; Thread B, PR #12,
P-024's retirement and the HAPPY MAN RE-RUN #2 all remain OPEN and untouched.**_
