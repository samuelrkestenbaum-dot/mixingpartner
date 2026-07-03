# Receipt — P-046: Product-Surface Refresh — The Four-Producer Demo

- **Packet:** P-046 — Product-Surface Refresh: The Four-Producer Demo. The
  P-040 pattern extended to the four-producer world: the samples/README
  still showed a TWO-producer surface (P-040-era) while the product had
  grown to FOUR producers (quincy_jones P-041, brian_eno P-045), behavioral
  mode forking (P-042), and three governed reach-gated extended move
  families (P-043/P-044). This packet makes the current system demonstrable
  from committed bytes: two NEW committed sample trees rendered by the REAL
  CLI (`examples/sample_output_quincy/` + `examples/sample_output_eno/`),
  the staleness pin extended to all four trees at full P-040 strength plus
  a NEW mode-surface pin, and the README's "Four producers, same stems"
  section with modes-are-behavior and the extended families. **Docs/demo
  only — ZERO product code.**
- **User authority:** opened on the user's "go" (2026-07-03) after the
  P-045 merge (PR #24 → default tip `0a53bb5`), down the orchestrator's
  presented recommendation (product-surface refresh = highest
  value-per-cost; the user's standing pattern: demo/docs packets follow
  substrate packets — P-040 followed P-039).
- **Date:** 2026-07-03
- **Status:** CLOSED — qa GREEN **(12/12)** + reviewer **PASS (no
  must-fix)**.

## Scope

**In (the confirmed packet spec):**

1. **Two NEW committed sample trees** (the P-040 pattern — rendered by the
   REAL CLI from `vocal_chop_groove`, relative stems paths only, 30
   artifacts each):
   - `examples/sample_output_quincy/` — overall **68.8**; carries his LIVE
     default-mode reach surface (declarations {medium, reach
     [arrangement_lift]}, `chorus_lift_E` among candidates, winner
     unmoved).
   - `examples/sample_output_eno/` — overall **65.5**; authored-neutral
     byte-silence — ZERO declaration/fork keys; winner `vocal_B` vs the
     others' `vocal_A`.
   Both are FAITHFUL renders — whatever the real CLI emits is the demo; no
   hand-editing.
2. **Staleness pin extension** — `tests/test_sample_refresh.py` grown to
   pin ALL FOUR trees byte-for-byte against fresh renders at the full
   P-040 strength, PLUS the NEW mode-surface pin
   (`test_committed_sample_mode_surface_is_the_authored_reach` ×4), which
   makes the README's modes-are-behavior claims machine-checked.
3. **test-9 (`test_contract_migration`) parametrized 2→4 trees.**
4. **README refresh** (docs only): "Two producers, same stems" → **"Four
   producers, same stems"** with the four verbatim invocations + the
   four-way table (overall / vocal_role_fit / loop_context); the
   **modes-are-behavior** subsection anchored on committed bytes; the
   **extended-families paragraph** with the dropout safety line VERBATIM
   ("dropout is an arrangement proposal, not a destructive operation");
   8 stale-wording fixes with a clean post-sweep grep (the P-038
   discipline). Every number equals a pinned value; no aspirational prose.

**Explicitly out (binding non-scope, held):**

- ZERO changes to engine code, profiles, analyzers, fixtures, goldens —
  held: **ZERO .py under `logic_mix_os/`**, zero profiles/fixtures/goldens
  touched.
- No new move families, no reach changes, no CLI changes, no fifth
  producer.
- The two EXISTING trees NOT regenerated — held: byte-untouched (empty
  diff on their paths), and **no staleness bug found** (fresh renders of
  the existing trees came back byte-identical).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `c94f2fe` — "P-046 Commit-1: the four-producer demo trees —
    examples/sample_output_quincy + _eno (real-CLI renders, relative
    paths) + the staleness pin extended to four" — 62 files, +7029/−17.
    **Commit-1 GREEN IN ISOLATION at 1110** (no test depends on README
    bytes).
  - `95f65bf` — "P-046 Commit-2: README — the 'Four producers, same stems'
    section + modes-are-behavior + the extended families" — README only,
    1 file, +112/−28.
  - Combined: **exactly 63 files** — 30 artifacts each in the two NEW
    trees, `tests/test_sample_refresh.py`,
    `tests/test_contract_migration.py`, `README.md`. ZERO .py under
    `logic_mix_os/`; the two EXISTING trees byte-untouched.
- **Parent:** `8674a97` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `0a53bb5` (= the PR #24 merge —
  P-045). Verified at close: `git merge-base HEAD 0a53bb5` = `0a53bb5`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the FINAL
  SHAs. (Builder note, recorded: the commits were recut once LOCALLY
  before pushing to fix a docstring inaccuracy; the gates judged the final
  tree.) **NOT merged** — the merge of P-046 is a user gate.

## QA proof (GREEN — 12/12)

- **Suite:** 1100 → **1110 passed, 0 failed** (+2 staleness params, +2
  headline params, +4 mode-surface pin, +2 contract-migration);
  regression **93/93**; **Commit-1 iso 1110**.
- **Freshness proven INDEPENDENTLY:** isolated worktree, fixtures
  regenerated, the four VERBATIM README invocations executed →
  **byte-identical 30/30 × 4** with NO normalization needed. This is also
  the product-surface smoke: the demo the README promises is exactly what
  the CLI produces.
- **Headlines exact:** overalls **76.3 / 60.9 / 68.8 / 65.5**
  (halee / timbaland / quincy / eno); vocal_role_fit **65 / 85 / 85 /
  85**; loop_context **15 / 10 / 12 / 35**.
- **README accuracy sweep:** EVERY number and claim traced to a committed
  byte or a pinned test — the timbaland declaration quote token-for-token;
  invariance 86.0/99.4 read from all four trees; the extended-family ids
  exact against the engine pools; the safety line word-for-word; the
  `--producer` default. "Unpinned claims found: none material."
- **Sabotage:** (a)+(b) one flipped byte in each NEW tree → exactly the
  right staleness pin fails; (d) quincy `reach_kinds` removed → the
  mode-surface pin + the staleness pin fail; (c) README 68.8→68.9 →
  nothing fails — **the documented P-040 accepted gap, unchanged in
  posture** (values pinned at artifact/test level; the standing residue
  note covers it).
- **Safety grep: clean** — the only pattern hits are renderer-emitted
  applescript TODO lines identical in the pre-existing trees; no absolute
  paths, no model identifiers.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- **Demo faithfulness PROVEN independently:** the reviewer re-rendered ALL
  FOUR trees itself → raw byte-identical, zero normalization — the trees
  are REAL renders, not curated; quincy's surface is exactly the live
  default; eno's byte-silence is exactly authored-neutral.
- **Pin extension full-strength, nothing weakened** — byte-for-byte the
  same assertions extended to four; the mode-surface pin is load-bearing
  in BOTH directions.
- **README honesty:** every claim traced to bytes; honesty PRESERVED and
  extended from P-040 ("same winners" became "same non-vocal winners"
  with eno's `vocal_B` divergence named); no aspirational prose.
- **Pin decisions all judged right calls:** `DEMO_OVERALLS` left as the
  P-039 in-test demo; `COMMITTED_TREE_HEADLINES` left as the P-045
  historical artifact; the module-scoped `sample_analyses` fixture
  respecting the conftest's no-silent-widening convention.
- **The absence of a non-default-mode committed tree judged CORRECT
  RESTRAINT** — the README tells users how to run `--mode` themselves.
- **Trajectory:** the product surface now MATCHES the product — four
  producers, behavioral modes, governed families, all demonstrable from
  committed bytes; the pin maps extend naturally for a fifth producer.

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, recorded not fixed (non-blocking):**
  1. **Reviewer residue (1):** README line 46 — "the three example
     projects" is PRE-EXISTING fixture-count staleness (the generator
     builds four), outside this packet's producer-roster sweep — fold
     into a future docs touch.
  2. **Reviewer residue (2):** the `test_four_way_differential.py`
     docstring at ~875 now under-describes 2-of-4 committed trees —
     wording only.
  3. **qa observation:** test-internal docstrings elsewhere say "two
     producers"/"all three producers" (accurate statements or
     era-comments — test-internal, not product surface).
  4. **The standing README-number-drift accepted gap RE-AFFIRMED:**
     sabotage (c) confirmed the P-040 posture, unchanged — the values are
     pinned at artifact/test level; a markdown-parsing test stays not
     worth its brittleness.
- Residues 1–2 pair naturally with the P-045 directory-driven
  `PRODUCERS`-tuple sweeps hardening — a natural single hardening/docs
  packet, ★ USER-GATED.
- All prior standing notes (incl. the ★★ groove-carrier trajectory
  watch-item and the dropout safety line) and the three named lessons
  retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-046** — `8674a97` + `c94f2fe` +
  `95f65bf` (+ this close commit) atop `0a53bb5` (= PR #24) — awaits the
  user's explicit word. The commits are pushed to the dev branch (standing
  go, pre-gates); NOT merged; no deploy/publish/secrets touched.
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open directions
  to the user (ALL user-gated): the P-046 merge · the directory-driven
  `PRODUCERS`-tuple sweeps hardening (P-045 residue, now joined by this
  packet's small docs residues — a natural pairing for one hardening/docs
  packet) · quincy/halee authored dropout reach · the future-analyzer
  candidates from Eno's honest deferrals (textural coherence · generative
  process · ambient patience) · a fifth producer · anything else the user
  calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-03). qa GREEN (1110 / 93/93 / Commit-1
iso 1110 / freshness independent — byte-identical 30/30 × 4 with zero
normalization / sabotage bites on every tree-side flip, README flip = the
documented accepted gap / safety grep clean) + reviewer PASS (no must-fix;
single-model — Codex unavailable; all four trees independently
re-rendered). The product surface now matches the product — four
producers (halee 76.3 · timbaland 60.9 · quincy 68.8 · eno 65.5, same
stems), behavioral modes, and governed extended families, all
machine-checked against committed bytes._
