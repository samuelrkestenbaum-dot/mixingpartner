# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-061 — Detector Over-Segmentation Calibration**
  (opened on the user's explicit go via the P-060 HANDOFF, 2026-07-25). Base =
  `e3d633c` (the P-060 close + HANDOFF tip). Verified `git merge-base HEAD
  9cfe990` = `9cfe990` (= PR #37 / P-059 merged to default) — the correct base.
- **Baseline to protect (measured on THIS env at `e3d633c`):** full suite **1414
  passed / 0 failed / 0 warnings**; regression **93/93, `critical_failures ==
  []`, 0 warnings**. The ENTIRE scoring corpus stays **byte-identical** — this
  packet moves NO golden, NO sample tree, NO mode demo.
- **This is the OTHER HALF of the Happy Man fix.** P-060 fixed the crater
  (per-section masking double-count). P-061 fixes the **fake-100s**.

## ★ BASE CORRECTION (recorded — this session)

This session's designated branch `claude/logic-mix-os-p061-detector-0dvr2t`
originally pointed at **`9cfe990`** (default head, **WITHOUT P-060**). It was
**rebased onto `e3d633c`** so P-061 builds on the **post-P-060 corpus**. Any
number in this packet that touches doctrine scoring is a post-P-060 number. Do
not re-litigate against a pre-P-060 baseline.

## ★ ENVIRONMENT FACT (newly established this session — qa MUST reproduce on it)

The canonical corpus environment is **numpy + scipy + soundfile installed, and
`pyloudnorm` NOT installed.** `logic_mix_os/dsp.py:319` `integrated_loudness()`
prefers **pyloudnorm → scipy → FFT**; the committed corpus was produced on the
**SCIPY tier**. **With `pyloudnorm` installed, 5 `test_sample_refresh` tests FAIL**
on `lufs` / `estimated_lufs` deltas (~0.5 dB). That is an ENVIRONMENT artifact,
NOT a regression — do not "fix" the corpus for it. Verified baseline on the
correct env at `e3d633c`: **1414 / 0 / 0**, regression **93/93**, 0 warnings.

## Why (the fake-100s on a real 49-track song)

On real "Happy Man" (49 tracks) the audio-driven section detector emitted **12
micro-sections**. Two doctrine scorers read per-section dispersion and therefore
INFLATE with section count:

| Scorer | line | reads |
|---|---|---|
| `_dynamic_mix` | `doctrine/doctrine_engine.py:394` | `pstdev` of per-section rms / width / crest |
| `_section_contrast` | `doctrine/doctrine_engine.py:351` | `contrast_vs_previous` lift-fail counting |

More (spurious) sections → more dispersion and more "contrast" events → a **FAKE
100/100 contrast/dynamics**. The sections are not real, so neither is the score.
The fix is to make the DETECTOR emit honest musical sections.

## Real constants (verified in source — `analyzers/section_detector.py`)

**The frame integers are DERIVED from the `_*_SEC` constants by design. Move the
SECONDS-level constants, never the frame integers.**

```
H = 0.25                 # line 38  frame-grid hop, seconds
ABS_FLOOR_DB = -50.0     # line 42
REL_RANGE_DB = 40.0      # line 43
_MIN_RUN_SEC = 0.5       # line 48  -> MIN_RUN     = 2 frames   [target ~1.5s]
_GAP_SEC     = 0.5       # line 49  -> GAP         = 2 frames
_CLUSTER_SEC = 1.0       # line 50  -> CLUSTER_WIN = 4 frames   [target ~2.0s]
MIN_SECTION_SEC = 4.0    # line 56                              [target ~8-10s — SEE HAZARD 1]
MAX_SECTIONS = 12        # line 57                              [target ~8]
_TAG_LOW  = 1.0 / 3.0    # line 59
_TAG_HIGH = 2.0 / 3.0    # line 60
```

Consumers: `MIN_RUN` at line 168, `CLUSTER_WIN` at line 207, `min_frames =
MIN_SECTION_SEC / H` at line 227, `MAX_SECTIONS` at lines 241/244, the tag
thresholds at line 266.

## Byte-stability — CONFIRMED, not assumed

- The guard at `pipeline.py:185` is the **POSITIVE** form `if
  len(project.sections) >= 2:` → supplied path; **else** detect. **All 4 fixture
  manifests supply exactly 2 sections**, so **no golden / sample / mode-demo ever
  enters the detector.**
- **Safety grep re-run this session:** `grep -rln '"inferred"' --include=*.json`
  over `logic-mix-os/` returns **ZERO files**. Nothing committed carries detector
  output.
- Other call site: `onramp.py:176` (`_detect_sections`), reachable only via
  `scaffold_manifest(detect_sections=True)` — **default OFF**.

qa must re-run this grep and re-assert the golden/sample/mode-demo trees are
byte-identical after the change.

## ★ RE-PIN SURFACE — the packet's OLD "~10 detector tests" claim is REFUTED

The staged shorthand under-counted the surface. **Record this correction
explicitly: this is the P-060 scope-under-count pattern REPEATING** (P-060's
"mode demos UNCHANGED" was likewise an under-count). Assume the shorthand is
under-counted until re-measured.

| File | Tests | Detail |
|---|---|---|
| `tests/test_section_detector.py` | **10** | `TestArrangementDetection` 4 · `TestGuardrails` 2 · `TestPipelineByteStability` 3 · `TestSuppliedSectionShapeUnchanged` 1 |
| `tests/test_onramp_scaffold.py::TestDetectSectionsOptIn` | **5** | two HARD-PIN detector output on the same 40s synthetic arrangement — **line 203** `assert len(m["sections"]) == 5`, **line 221** `assert len(loaded["sections"]) >= 2` |

**TRUE surface: up to 15 tests across 2 files.** The builder re-measures with a
per-file collect before and after.

## ★ THREE NUMERIC HAZARDS — resolve NUMERICALLY, never by assumption

**1. `MIN_SECTION_SEC` ~8-10 is NOT free.** Both synthetic arrangements produce
sections of exactly **8.0s** (boundaries 0/8/16/24/32 over 40s). At **8.0** the
guard is **knife-edge**: `min_frames = 8.0 / 0.25 = 32` vs a 32-frame section —
debounce jitter can merge a REAL section at 31 frames. At **9.0 / 10.0 EVERY
section merges**, breaking `test_boundaries_at_arrangement_events_only`,
`test_energy_tags_are_relative_and_honest` (pins `tags[0] == "low"`, `tags[3] ==
"high"`, names `"Section 1..5"`) and the onramp `== 5` pin. Pick the value from
measured frame counts, and state the jitter margin.

**2. `test_max_sections_cap` GOES VACUOUS.** It builds **13 entrances 6s apart**
(`duration = 84.0`) on the stated premise at **line 141**: *"each section is >= 6s
so nothing is merged first."* Any `MIN_SECTION_SEC > 6.0` merges them BEFORE the
cap engages — the test then passes **trivially without ever exercising
`_cap_sections`**. It must be **RE-SPACED** (wider entrances + longer duration),
**not merely re-pinned**. **A non-vacuity proof is REQUIRED at review** (P-060
precedent: the reviewer proved non-vacuity by reproducing the failure with the
fix reverted).

**2b. Secondary vacuity watch (archivist observation, verified in source, NOT new
scope):** `test_sub_min_section_is_merged` uses `duration = 20.0` and asserts
`min(lengths) >= MIN_SECTION_SEC`. At a raised floor the whole 20s can collapse
to ONE section, satisfying the assertion trivially. The builder should confirm
this test still exercises a real merge, or widen its duration in the same spirit
as hazard 2.

**3. `MIN_RUN` 0.5 → 1.5s (2 → 6 frames) and `_CLUSTER_SEC` 1.0 → 2.0s (4 → 8
frames) APPEAR safe** — the 3s blip in `test_sub_min_section_is_merged` is 12
frames, and events are 8s apart — **but the builder must PROVE this, not inherit
it.** Print the actual frame runs.

## In scope

- `analyzers/section_detector.py` **constants** (the seconds-level ones).
- An **adaptive novelty floor ONLY if constants alone are insufficient** — and
  that is a **SCOPE DECISION that must route back through the orchestrator
  BEFORE being written.** Do not write it silently.
- **Re-pins in the two named test files only** (including the hazard-2 re-spacing).

## Out of scope — BINDING, DO NOT TOUCH

`pipeline.py`'s guard · `doctrine_engine.py` · `masking_analyzer.py` · ALL
goldens / samples / mode-demos · `onramp.py` **behavior** (its TESTS may re-pin).
No new dependency (numpy + first-party only). Plan-only — no apply-to-Logic.
Roster frozen at five.

## Commit shape (≤2; expect ONE)

**Expect ONE ATOMIC commit** — constants + re-pins are **INSEPARABLE** (per the
P-060 precedent: split them and either half is red). Therefore **HEAD is the
Commit-1 isolation proof.** No push / merge / deploy / secrets.

## Required proof (qa reports EXACT)

1. Full suite on the **pyloudnorm-ABSENT** env: **1414** → exact new count, 0
   failed, 0 warnings.
2. Regression **93/93, `critical_failures == []`, 0 warnings**.
3. **Commit-1 isolation** = HEAD (single atomic commit).
4. **Safety grep:** `grep -rln '"inferred"' --include=*.json` → **0 files**; the 4
   goldens + 5 sample trees + all mode demos **byte-identical**; no
   `pipeline.py` / `doctrine_engine.py` / `masking_analyzer.py` diff; no new dep.
5. **Per-file collect** for both re-pinned test files (the TRUE 15-test surface).
6. **Hazard resolution table** — the chosen `MIN_SECTION_SEC` with its measured
   frame margin, the `MIN_RUN` / `CLUSTER_WIN` frame proof, and the
   **`test_max_sections_cap` NON-VACUITY proof** (evidence `_cap_sections`
   actually engages).

## Route after builder

builder (atomic Commit-1) → qa → reviewer (non-vacuity proof REQUIRED) →
archivist (receipt `build-os/receipts/P-061-detector-over-segmentation-calibration.md`).
**Commit only.**

## OPEN USER GATE (carried, UNTOUCHED by this packet)

- **The merge of P-060 to default** — `ae0b9fc` (+ close `bb126cc`) atop
  `9cfe990` (= PR #37). Pushed to the dev branch under the standing pre-gate go;
  **NOT merged.** It remains a **SEPARATE open user gate** and this packet does
  not advance, bundle, or resolve it.
- Also carried: the **HAPPY MAN RE-RUN #2** (user-run; confirm the P-060 crater is
  gone). After P-061 lands, a re-run should also show the contrast/dynamics
  fake-100s corrected.

## ★★★ BUILT — STATUS UPDATE (HANDOFF-INTEGRITY AUDIT, 2026-07-26)

P-061 is **IMPLEMENTED AND PUSHED, BUT NOT CLOSED.** The scope above is the
SET-ACTIVE text and is preserved verbatim for the record — **several of its
numeric targets were measured to be WRONG and were deliberately overridden.**
Read this section, not the targets above, for what actually shipped.

### The two commits (packet is AT its ≤2 implementation-commit limit)

| Commit | What |
|---|---|
| `4cbee14` | Commit-1 — the calibration. Green in isolation. |
| `d941ecc` | Commit-2 — the gap-fill fix (a regression Commit-1 introduced). |

Both pushed to `claude/logic-mix-os-p061-detector-0dvr2t` (fast-forward, no
history rewritten). **No PR opened. Default untouched at `9cfe990`.**

### Constants as SHIPPED — vs the targets above

| Constant | Was | Target above | **SHIPPED** | Why the deviation |
|---|---|---|---|---|
| `_MIN_RUN_SEC` | 0.5 | ~1.5 | **5.0** | 1.5s is provably INERT — the ornaments are 3–4s, so the packet's target would not have fixed the bug at all. This is the change that does the work. Plateau [4.5, 8.0] identical. |
| `_GAP_SEC` | 0.5 | (not targeted) | **5.0** | Commit-2. NOT in the original scope — see the regression below. |
| `_CLUSTER_SEC` | 1.0 | ~2.0 | **2.0** | As targeted. Proven a no-op on all scenarios (closest surviving boundary pair 12 frames vs 8). |
| `MIN_SECTION_SEC` | 4.0 | ~8–10 | **7.0** | **Target refuted.** 8.0 is knife-edge (measured jitter tolerance **0.00s** against the 32-frame synthetic sections); 9/10 destroy the arrangement tests. 7.0 is the largest value with real margin (0.40s). |
| `MAX_SECTIONS` | 12 | ~8 | **12 (unchanged)** | **Target refuted by measurement.** `_cap_sections` drops boundaries by novelty with no regard for spacing, so whenever it binds it MANUFACTURES the very artifact this packet removes: MAX=8 produced an **80s** super-block, MAX=10 a **60s** one — both worse than the 64s bug. The floor should do the work; the cap stays a safety valve. Lowering it needs a spacing-aware `_cap_sections` = separate packet. |

Live invariant, asserted by `test_gap_fill_does_not_outgrow_the_section_floor`:
`_MIN_RUN_SEC <= _GAP_SEC < MIN_SECTION_SEC` (5.0 <= 5.0 < 7.0).

### ★ The regression Commit-1 introduced, and Commit-2's fix

Commit-1 raised the persistence floor to 5.0s but left gap-fill at 0.5s. A
lead vocal in 4.0s phrases with 1.2s breaths then fragments into 16-frame runs,
every one of which dies under the 20-frame floor — **the vocal is erased from
arrangement detection entirely.** Found by coordinator probe, not by the suite.

| `_MIN_RUN_SEC`/`_GAP_SEC` | vox frames after debounce | sections | entrance @32s |
|---|---|---|---|
| 0.5 / 0.5 (pre-P-061) | 235 | 6 | NO |
| 5.0 / 0.5 (`4cbee14`) | **0 — ERASED** | 2 | NO |
| 5.0 / 5.0 (`d941ecc`) | **287** | 4 | **YES** |

Note the last column: the fix does not merely undo the damage, it produces a
TRUE vocal-entrance boundary that **neither the old nor the Commit-1 constants
achieved**. Pre-P-061 emitted phrase confetti at 52.75/67.25/78.75s.

### Proof status — REAL, but NOT the formal gate

Independently re-verified by the coordinator at `d941ecc`: suite **1426 passed /
0 failed / 0 warnings** (1414 baseline + 12 new), regression **93/93,
`critical_failures == []`**, safety grep `"inferred"` **zero files**, diff exactly
2 files, no golden/sample-tree/mode-demo/`pipeline.py`/`doctrine_engine.py`/
`masking_analyzer.py`/dependency change. 200s repro: 12 sections with 4/4/7s
slivers + a 64s cap block → **9 sections, no slivers, cap never binds**.

**★ BUT: qa and reviewer were dispatched against `4cbee14` and NEVER RETURNED.**
So qa's independent Commit-1-isolation proof and the reviewer's verdict are both
MISSING, and **the required non-vacuity review of `test_max_sections_cap` was
never formally signed off** (the builder did prove it red/green: neutering
`_cap_sections` fails `16 != 12` and nothing else).

### Why there is NO receipt

**Deliberate.** `build-os/receipts/P-061-*.md` does not exist because the packet
is NOT closed. Writing one now would record a close that did not happen. The
receipt is the archivist's to write **after** qa + reviewer actually run.

### Open judgment call for the reviewer

`_GAP_SEC = 5.0` widens P-059's original 0.5s "breath" intent into "any absence
under 5s is a rest inside a part". Measured plateau **[1.0, 6.5]** is
behaviourally identical corpus-wide; ceiling 7.0s. **Anything in [1.5, 6.5] fixes
the erasure** — 5.0 is the only value that also makes fragment-then-erase
structurally impossible. Not settled.

### Environment (reproduce on this or the corpus will appear to fail)

numpy + scipy + soundfile installed, **pyloudnorm NOT installed** — the corpus was
produced on the scipy tier of `dsp.integrated_loudness()`'s
pyloudnorm→scipy→FFT ladder. With pyloudnorm present, 5 `test_sample_refresh`
tests fail on ~0.5dB lufs deltas. Verify: `_HAVE_PYLN=False, _HAVE_SCIPY=True`.

### Exact next action

Run **qa** then **reviewer** against `d941ecc` (not `4cbee14`), settle the
`_GAP_SEC` semantic call, then archivist → receipt → close.

---
_Set active by the archivist on the user's explicit go via the P-060 HANDOFF
(2026-07-25). SET-ACTIVE is metadata only — `build-os/` files, ONE commit, no
product code, no push. P-060 fixed the crater; **P-061 fixes the fake-100s.** One
packet at a time: builder → qa + reviewer → archivist → receipt._
