# Receipt — P-049: Committed-Example Directory-Set Guards

- **Packet:** P-049 — Committed-Example Directory-Set Guards. The P-048
  reviewer's ★ named suite-wide hardening candidate made real: one
  derivation-coupled EXACT-SET guard per committed-example home, so nothing
  can land in — or vanish from — the committed-example surface silently.
  **Tests only — one commit by design; ZERO runtime changes.**
- **User authority:** opened on the user's "Ok go" (2026-07-04) after the
  P-048 merge report (PR #27 → default tip `7ae96f2`) — of the presented
  directions, the ONLY one requiring no user taste/product decision (pure
  suite hardening); the fifth producer, the analyzer candidates, and
  quincy/halee dropout reach remain user-gated and were NOT touched.
- **Date:** 2026-07-04
- **Status:** CLOSED — qa GREEN **(8/8, bites 6/6)** + reviewer **PASS (no
  must-fix)**.

## Scope

**In (the packet contract, met):**

1. **`tests/test_mode_demo_refresh.py`** —
   `test_committed_mode_demo_directory_set_is_exactly_the_pinned_nine`:
   `examples/mode_demos/` contains EXACTLY the pinned nine — the allowed
   set DERIVED as `sorted(MODE_DEMOS)`, the SAME table every
   staleness/surface pin parametrizes — plus a no-non-dirs assert (beyond
   the contract: no stray files at that level either).
2. **`tests/test_sample_refresh.py`** —
   `test_committed_examples_directory_set_is_exactly_the_pinned_residents`:
   `examples/` contains EXACTLY the four pinned trees ∪ the
   consciously-enumerated `NON_TREE_RESIDENTS` {`mode_demos`,
   `project_manifest.example.json`}, plus a dirs-vs-files shape assert
   and a parents-sanity assert. Reality checked FIRST: no README exists
   at either level — none allowed.
3. **Conscious-extension semantics in both docstrings** (the P-047
   data-table convention): a fifth tree / tenth demo = a one-line
   pinned-table extension that auto-extends guard + pins together.

**Explicitly out (binding non-scope, held):**

- Tests only — zero changes to engine code, profiles, fixtures, goldens,
  committed examples, README; no new demo artifacts; no renames; nothing
  else rode. Held: scope exactly the two test files (diff-proven —
  2 files, +51/−0).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **One commit (≤2 rule satisfied; one by design):**
  - `94b7df9` — "tests: P-049 — committed-example directory-set guards" —
    2 files, +51/−0, tests only. **Single-commit packet: the HEAD run IS
    the Commit-1-isolation proof (1145).**
- **Parent:** `b6ba8d1` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `7ae96f2` (= the PR #27 merge —
  P-048). Verified at close: `git merge-base HEAD 7ae96f2` = `7ae96f2`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the final
  SHA. **NOT merged** — the merge of P-049 is a user gate.

## QA proof (GREEN — 8/8)

- **Suite:** 1143 → **1145 passed, 0 failed** (+2 exactly); regression
  **93/93**; growth arithmetic verified per file (the two touched files'
  counts 33→35 combined).
- **Scope:** exactly the two test files — nothing else in the diff.
- **Derivation verified:** the guards' allowed sets checked against BOTH
  the pinned tables and the real directory contents.
- **Bites 6/6 in an isolated worktree** — each mutation failing EXACTLY
  its one guard: a stray dir and a stray file at both levels; an unpinned
  fifth tree; a deleted pinned demo; the manifest-replaced-by-directory
  shape case.
- **Safety grep:** 0 across all +51 lines.
- **Behavioral surface untouched:** the 35 pin/guard tests green;
  doctrine untouched by construction.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- Derivation-from-pins judged "genuinely drift-proof — the strongest
  property of the diff": no divergence path exists between the guards and
  the pins they protect, in either direction.
- All four contracted failure modes covered at BOTH levels (the builder
  added the mode-demos no-non-dirs assert beyond the contract); nested
  strays confirmed already covered by the P-048/P-040 file-set pins.
- One new residual found (residue, not must-fix): a nested stray
  SUBDIRECTORY inside a sample_output* tree escapes everything — the
  sample staleness pin filters `is_file()` on both sides (unlike the
  mode-demo pin's explicit no-subdir assert); future one-line
  micro-hardening: a no-subdirs assert in the sample staleness pin.
  Symlink impersonation judged exotica (caught by the residents set or
  the byte pins).
- Minor observation: the dirs-shape assert hardcodes the "mode_demos"
  literal (duplicating a `NON_TREE_RESIDENTS` member) — a future non-tree
  dir resident needs a two-place edit, but any half-edit fails loudly;
  acceptable shape-encoding.
- Scope discipline clean; the builder's in-place bite mutations provably
  left nothing behind.
- **Trajectory:** "This closes the P-048 reviewer residue in full."

## Residue (carried to `build-os/memory/residue.md`)

- **★ The P-048 accepted note 1 (the named suite-wide hardening
  candidate — the directory-set guard) ✓ RESOLVED** by this packet: the
  committed-example surface is now EXACT-SET-GUARDED — 4 trees + 9 demos
  + the manifest example, derivation-coupled to the pinned tables.
  P-048 notes 2–4 stand unchanged.
- **NEW accepted, recorded not fixed (the two reviewer residuals,
  non-blocking):**
  1. **The nested-subdir hole in the sample staleness pin** — a nested
     stray SUBDIRECTORY inside a sample_output* tree escapes everything
     (the pin filters `is_file()` on both sides). Future one-line
     micro-hardening: a no-subdirs assert in the sample staleness pin —
     could ride any future packet.
  2. **The "mode_demos" literal duplication in the dirs-shape assert** —
     a future non-tree dir resident needs a two-place edit; any
     half-edit fails loudly; acceptable shape-encoding.
- All prior standing notes (incl. the ★★ groove-carrier trajectory
  watch-item and the dropout safety line) and the three named lessons
  retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-049** — `b6ba8d1` + `94b7df9`
  (+ this close commit) atop `7ae96f2` (= PR #27) — awaits the user's
  explicit word. The commit is pushed to the dev branch (standing go,
  pre-gates); NOT merged; no deploy/publish/secrets touched.
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open directions
  to the user (ALL user-gated — all product/taste decisions that belong
  to the user): the P-049 merge · a fifth producer (who + the grounding) ·
  the future-analyzer candidates from Eno's honest deferrals (textural
  coherence · generative process · ambient patience) · quincy/halee
  authored dropout reach · the one-line sample-pin micro-hardening
  (residue 1 above — could ride any future packet) · anything else the
  user calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-04). qa GREEN (1145 / 93/93 /
single-commit — the HEAD run IS the Commit-1-isolation proof / bites 6/6
in an isolated worktree / safety grep 0 across all +51 lines) + reviewer
PASS (no must-fix; single-model — Codex unavailable). The
committed-example surface is EXACT-SET-GUARDED — 4 trees + 9 demos + the
manifest example — and nothing can land or vanish silently._
