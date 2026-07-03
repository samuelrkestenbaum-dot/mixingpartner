# Receipt — P-047: Directory-Driven Producer Sweeps + Docs Residues

- **Packet:** P-047 — Directory-Driven Producer Sweeps + Docs Residues.
  The P-045 reviewer residue (the headline item — the profile-sweeping
  guards parametrized a HARDCODED three-producer tuple, so brian_eno was
  not swept by the structural guards and a fifth producer would not grow
  the sweeps passively) + the P-046 docs residues, cleared in one TEST +
  DOCS hardening packet. The sweep tuple is now DIRECTORY-DRIVEN from
  the product's single source of truth; eno's data rows landed at every
  per-producer site; the stale docs prose is gone. **ZERO runtime
  changes by definition** — no engine code, profiles, fixtures, goldens,
  or committed sample trees touched.
- **User authority:** opened on the user's "Go" (2026-07-03) after the
  P-046 merge (PR #25 → default tip `24b5ca7`), down the orchestrator's
  presented recommendation (the hardening/docs pairing flagged at the
  last two closes).
- **Date:** 2026-07-03
- **Status:** CLOSED — qa GREEN **(11/11, zero discrepancies)** +
  reviewer **PASS (no must-fix)**.

## Scope

**In (the confirmed packet spec):**

1. **Directory-driven sweeps (Commit-1):**
   `PRODUCERS = tuple(sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json")))`
   — the IDENTICAL expression `cli.py:50` uses on the product's single
   source of truth; the old hand-rolled second path DELETED (the P-045
   drift vector is gone). The NEW guard
   `test_producer_sweep_is_directory_driven_with_the_known_minimum`:
   sorted, duplicate-free, the four known names as MINIMUM containment,
   no maximum — nothing blocks a fifth producer.
2. **Eno's data rows at every per-producer site** — captured from the
   real engine, then pinned: AUTHORED_DROPOUT {medium, low, 78.9, truth
   64/82/78}; AUTHORED_TRANSLATION {low, medium, medium};
   AUTHORED_OVERALLS {72.0, 62.6}; conservative set {chorus_lift_B,
   chorus_lift_D} (the pairwise-distinct count STRENGTHENED 3→4);
   experimental emission [B,A,C,F] / [density_B,A,E] / [vocal_A,B] (the
   vocal set coincides with halee's — honest coincidence documentation,
   both sets pinned by equality); the affinity ordering extended to the
   FULL four-producer chain timbaland 80.9 > eno 78.9 > quincy 73.7 >
   halee 60.6 with the original t>q>h chains KEPT verbatim. As the
   contract predicted, eno now carries the same structural sweep
   coverage the three have (the P-045 marginal residues' sweep aspect,
   closed as a consequence).
3. **Docs residues (Commit-2):** README "the four example projects"
   (generator verified: exactly 4 builders); the four-way docstring
   (2-of-4 committed trees re-read there); ~10 stale-prose sites across
   the sweep files. Prose-only everywhere — ZERO collection changes,
   verified per file C1 == HEAD.
4. **STOP-condition integrity (the contract's binding recon, held):**
   the fail-first run after the tuple swap produced exactly 6
   missing-data-row failures and ZERO structural failures on eno —
   P-045's claimed equivalents were REAL (corroborated by the reviewer
   against the four-way suite's existing eno coverage). Nothing was
   papered over.

**Explicitly out (binding non-scope, held):**

- ZERO changes to engine code, profiles, fixtures, goldens, committed
  sample trees — held: **ZERO .py under `logic_mix_os/`**, zero
  profiles/fixtures/goldens, the four committed trees byte-untouched.
- No new guards beyond the sweep extension's natural growth (making
  EXISTING proofs producer-complete, not a new-proof packet) — held
  (the one new discovery guard IS the sweep extension's own integrity
  check).
- No behavior changes of any kind; no fifth producer.
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `3322c88` — "P-047 Commit-1: directory-driven producer sweeps + eno
    data rows" — 3 files (the three sweep test files), +77/−4.
    **Commit-1 GREEN IN ISOLATION at 1122.**
  - `f9736f3` — "P-047 Commit-2: docs residues — four-fixture README,
    four-tree docstring, stale sweep prose" — 5 files, +48/−37;
    prose-only everywhere, ZERO collection changes (verified per file
    C1 == HEAD). (Reviewer briefing correction, recorded: Commit-2 also
    carries the prose-only hunks in the three sweep files — within
    scope, collection-neutral.)
  - Combined: **exactly 5 files, +125/−41 (347-line diff)** — the three
    sweep test files (`tests/test_mode_forking.py`,
    `tests/test_move_vocabulary_expansion.py`,
    `tests/test_negative_space_dropout.py`) + `README.md` +
    `tests/test_four_way_differential.py` (docs-only hunks).
- **Parent:** `37e4120` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `24b5ca7` (= the PR #25 merge —
  P-046). Verified at close: `git merge-base HEAD 24b5ca7` = `24b5ca7`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the
  final SHAs. **NOT merged** — the merge of P-047 is a user gate.

## QA proof (GREEN — 11/11, zero discrepancies)

- **Suite:** 1110 → **1122 passed, 0 failed** (+4/+5/+3 per file = 11
  new `[brian_eno]` sweep instances + the NEW discovery guard);
  regression **93/93**; **Commit-1 iso 1122**.
- **★ The fifth-producer property PROVEN:** a synthetic
  `test_fifth.json` (neutral halee clone) dropped into a worktree's
  producers dir → collection GREW passively (36→39, 41→46, 50→53); run
  = 5 failed / 133 passed, ALL FIVE `KeyError: 'test_fifth'` on
  per-producer data tables — zero structural-guard failures
  (test_mode_forking 39/39 green on the neutral clone). The sweep
  reaches a fifth producer BY CONSTRUCTION; the cost is exactly the
  conscious data-table rows.
- **Node-ID diff parent→HEAD:** the additions are exactly the guard +
  11 `[brian_eno]` params.
- **Sabotage 3/3:** eno row removed → 3 exact KeyError failures;
  `brian_eno.json` deleted → the containment guard FAILS + 50 failed /
  49 errors in exactly the predicted shape (the 11 sweep params
  disappear from collection; the eno-hardcoded suites fail on load);
  the tuple reverted to the hardcoded three → **the guard test
  FAILS** — the guard prevents silent regression to the old world.
- **Eno rows independently reconstructed** from raw JSON + live engine
  (78.9 = mean of 7 dims − medium penalty, to the decimal).
- **Safety grep: 0** across the full diff; docs accuracy verified.
- **UI/product-surface smoke: N/A by construction** — TEST + DOCS
  packet; the four committed sample trees byte-untouched (the product
  surface is unchanged by definition).

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- **Discovery design SOUND:** single source of truth, the drift vector
  deleted, minimum-only guard; a fifth producer fails ONLY
  per-producer data sites — conscious-extension-by-design.
- **Assertion strength: NOTHING removed or loosened** — every removed
  line enumerated (the tuple, the duplicate path, `==3`→`==4`, prose).
- **The under-specified decisions all judged right:** eno's row-free
  DEFAULT_FLOW_IDS fallthrough traced and judged the STRONGER design
  (any default-flow drift fails the equality; keeps future neutral
  producers passing passively); the stale test NAMES left (node-ID
  stability) — follow-up residue; the halee-only artifact-keys pin
  left (outside "make existing proofs producer-complete").
- **One briefing correction recorded:** Commit-2 also carries the
  prose-only hunks in the three sweep files — within scope,
  collection-neutral.
- **Trajectory:** a fifth producer now costs exactly its JSON
  (auto-discovered, auto-swept) + its own profile/differential files +
  conscious data-table rows at enumerable sites.

## Residue (carried to `build-os/memory/residue.md`)

- **✓ RESOLVED by this packet:** the P-045 reviewer residue (c) — the
  hardcoded `PRODUCERS` 3-tuples, the named future-packet candidate —
  and the P-046 docs residues (README fixture count; the four-way
  docstring), plus the sweep files' stale prose.
- **NEW accepted notes (recorded not fixed):**
  1. **Two stale test NAMES in `test_negative_space_dropout.py`:**
     `test_all_three_profiles_author_honest_dropout_rows` sweeps four;
     `test_same_mode_same_stems_only_timbaland_emits_dropout` stale
     since P-045 — name-only, the assertions are true and non-vacuous;
     rename = node-ID churn; a future touch.
  2. **`_PRODUCER_TOKENS` at `test_mode_forking.py:873` has no
     eno/brian token** — the fork-path code-purity guard wouldn't flag
     a hypothetical eno-named engine branch (pre-existing since P-045;
     the same holds for any fifth name) — fold the token list into the
     next hardening touch.
  3. **`test_same_mode_same_stems_each_producer_emits_only_its_authored_reach`
     would silently skip (collect-but-not-assert) a fifth producer's
     emission** — marginal: the loud KeyErrors elsewhere force
     conscious extension.
- All prior standing notes (incl. the ★★ groove-carrier trajectory
  watch-item and the dropout safety line) and the three named lessons
  retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-047** — `37e4120` +
  `3322c88` + `f9736f3` (+ this close commit) atop `24b5ca7`
  (= PR #25) — awaits the user's explicit word. The commits are pushed
  to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING.** The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): the P-047 merge ·
  quincy/halee authored dropout reach · the future-analyzer candidates
  from Eno's honest deferrals (textural coherence · generative process
  · ambient patience) · a fifth producer (now cheaper than ever —
  auto-swept) · the small test-name/token-list hardening touch (the
  three new accepted notes above) · anything else the user calls. Do
  NOT open anything blind.

---
_Closed by the archivist (2026-07-03). qa GREEN (1122 / 93/93 /
Commit-1 iso 1122 / the fifth-producer property proven by synthetic
passive growth / sabotage 3/3 incl. the reverted-tuple guard bite /
safety grep 0) + reviewer PASS (no must-fix; single-model — Codex
unavailable). The sweeps are producer-complete and future-proof —
every structural guard now discovers profiles from the producers
directory, and a fifth producer grows the sweeps passively at exactly
the cost of its conscious data rows._
