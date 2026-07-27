# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE. **P-061 — Detector Over-Segmentation Calibration is
  CLOSED (2026-07-26)** with **BOTH formal gates GREEN**. Receipt:
  `build-os/receipts/P-061-detector-over-segmentation-calibration.md`.
- **Do NOT open a new packet blind.** The next packet needs the user's explicit
  go. Candidates are listed under "Staged / candidates" below.

## What P-061 delivered (summary — full detail in the receipt)

**The OTHER HALF of the Happy Man fix.** P-060 fixed the masking crater; P-061
kills the **fake 100/100 contrast/dynamics**. On a real 49-track song the
audio-driven detector emitted **12 micro-sections**, inflating `_dynamic_mix`
(`doctrine/doctrine_engine.py:394`) and `_section_contrast` (`:351`) to a
ceiling-pinned fake 100/100. The fix makes the DETECTOR emit honest musical
sections.

| Constant | Was | **SHIPPED** | Frames (H=0.25) |
|---|---|---|---|
| `_MIN_RUN_SEC` | 0.5 | **5.0** — the load-bearing change | `MIN_RUN` 2 → 20 |
| `_GAP_SEC` | 0.5 | **5.0** (Commit-2) | `GAP` 2 → 20 |
| `_CLUSTER_SEC` | 1.0 | **2.0** (proven inert) | `CLUSTER_WIN` 4 → 8 |
| `MIN_SECTION_SEC` | 4.0 | **7.0** | 16 → 28 |
| `MAX_SECTIONS` | 12 | **12 — UNCHANGED** | — |

Seconds-level constants only; the frame integers stay **DERIVED** via
`max(1, round(_X_SEC/H))`. Live invariant asserted by test:
**`_MIN_RUN_SEC <= _GAP_SEC < MIN_SECTION_SEC`** (5.0 <= 5.0 < 7.0). 200s repro:
12 sections with 4.0/4.0/7.0s slivers + a 64s cap block → **9 sections, no
slivers, cap never binds**.

**Two implementation commits — AT the ≤2 limit:** `4cbee14` (Commit-1) +
`d941ecc` (Commit-2), atop set-active `6c81090` atop `e3d633c`. HEAD `a96a4cc`
(documentation-only audit). `git merge-base HEAD 9cfe990` = **`9cfe990`**.

**Gates:** qa **1426 / 0 / 0**, regression **93/93 `critical_failures == []`**,
**independent detached Commit-1 isolation at `4cbee14` → 1420 / 0 / 0**,
safety grep `"inferred"` **ZERO files**, three monkeypatch non-vacuity proofs each
a **SOLE failure**. Reviewer **PASS, no must-fix** — **single-reviewer only;
`codex` is NOT installed, so no second model reviewed the diff.**

**Two findings the next packet must inherit:** **(1) three packet targets were
REFUTED BY MEASUREMENT** (`MIN_SECTION_SEC` ~8–10 → 7.0; `_MIN_RUN_SEC` ~1.5 →
5.0 because 1.5s is provably INERT; `MAX_SECTIONS` ~8 → **left at 12** because a
spacing-blind `_cap_sections` MANUFACTURES super-blocks when it binds — MAX=8 gave
an 80s block, worse than the 64s bug). **(2) Commit-1 shipped a live regression**
(a phrased lead vocal ERASED, 235 frames → 0) found by probe, not by the suite —
*"Commit-1's isolation-greenness was true but blind."* Commit-2 fixed it and
DISCOVERED a true vocal-entrance boundary at 32s.

## ★ OPEN GATES — carried, NONE advanced by this close

- **★★ The merge of P-060 to default** — **still THE open user gate.** Default
  remains **`9cfe990`**; would be **PR #38**.
- **★ P-061's own merge** — a **SEPARATE later gate**. P-061 is **CLOSED as a
  packet but NOT merged**; **no PR exists** for it.
- **Thread B** — the vendored Build OS `.claude/` update to ClaudeOrchestrator
  `7ef50e8`. Diagnosed, **not applied**. User picks: (a) isolated PR to default,
  or (b) fold into the merge.
- **PR #12** — still **OPEN** against the abandoned `main` base. Not closed;
  recorded. User gate: close it or rebase it.
- **P-024** — **delivered-but-never-formally-retired** (P-051 shipped the MCP
  server it specified; P-052 proved it E2E). **NOT retired** — the note stands.
- **HAPPY MAN RE-RUN #2** — still the real-world confirmation for **both** halves
  (the crater fix AND the fake-100s fix).

## Staged / candidates for the next packet (need an explicit user go)

1. **HAPPY MAN RE-RUN #2** (user-run, not a build packet) — the real-world
   confirmation that the crater is gone AND contrast/dynamics are now honest.
   Highest information value; costs no build.
2. **Spacing-aware `_cap_sections`** — the packet P-061 named and deferred. It is
   the prerequisite for ever lowering `MAX_SECTIONS` below 12.
3. **The three non-blocking P-061 residue items** (stale comment at
   `section_detector.py:199`; the behavioural test that guards ~8.0s rather than
   the stated 7.0s; `MIN_SECTION_SEC = 7.0`'s thin 1.0s margin over a 120bpm 4-bar
   section) — small, could ride along with (2).
4. The standing user-gated directions: ambient patience (Eno-deferral #2) ·
   generative process (Eno-deferral #3) · CLA/Halee/Timbaland textural weighting ·
   the `<2 beds` fallback calibration · the real Cowork host connection (manual) ·
   apply-to-Logic (FUTURE, re-gated — never auto; the safety line stands) · a
   sixth producer (roster frozen at five).

## Environment (reproduce on this or the corpus will appear to fail)

numpy + scipy + soundfile installed, **`pyloudnorm` NOT installed** — the corpus
was produced on the **scipy tier** of `dsp.integrated_loudness()`'s
pyloudnorm→scipy→FFT ladder. With pyloudnorm present, 5 `test_sample_refresh`
tests fail on ~0.5dB lufs deltas (an ENVIRONMENT artifact, not a regression).
Verify `_HAVE_PYLN=False, _HAVE_SCIPY=True`. **P-025 standing fact:** `fixtures/`
is **GENERATED** — run `fixtures/generate_fixtures.py` before regression in a
fresh / detached checkout. **★ The pytest `-q` trap:** `pyproject` sets
`addopts = "-q"`, so `pytest -q` silently suppresses the summary count line while
still exiting 0 — use bare `python3 -m pytest` or `-o addopts=""`.

---
_Cleared by the archivist on the P-061 close (2026-07-26). **No packet is in
flight.** The full P-061 record — including the three refuted targets, the
Commit-1 regression, the `_GAP_SEC` adjudication, and every open gate — lives in
`build-os/receipts/P-061-detector-over-segmentation-calibration.md` and
`build-os/memory/residue.md`. One packet at a time: builder → qa + reviewer →
archivist → receipt._
