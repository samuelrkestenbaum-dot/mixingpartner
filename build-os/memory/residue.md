# Residue

> What was deferred, left behind, or noted as risk — the stuff that didn't fit in
> the last packet but must not be forgotten. The orchestrator reads this to avoid
> dropping threads; the archivist appends/clears it on close.

## ★★★ STATUS (P-048 close, 2026-07-03): residue = accepted standing notes only — THE PRODUCT SURFACE IS COMPLETE FOR THE CURRENT SUBSTRATE

- **P-048 (PRODUCT-SURFACE REFRESH — Producer + Mode Demo Artifacts,
  docs/samples/demo clarity only, ZERO runtime behavior changes;
  opened on the user's go 2026-07-03, verbatim: "Merge P-047 now.
  Then do product-surface refresh… This is the right next skate:
  make the now-powerful system explain itself before adding more
  depth." — P-047 merged FIRST as PR #26 → default tip `645c925`,
  then this packet) closed 2026-07-03:** qa GREEN (11/11, zero
  discrepancies) + reviewer PASS (no must-fix). Commits `4725169`
  (Commit-1 — the NINE committed mode demos under
  `examples/mode_demos/` [each the "creative pair" — creative.json
  + creative_report.md from a real CLI `creative` run on the dense
  fixture, the only fixture firing all five creative problems; 18
  artifacts, 265,305 bytes; zero normalization — no path echo in
  the pair] + the NEW `tests/test_mode_demo_refresh.py` [21 tests:
  9 staleness + 9 surface + 3 story, expected values IMPORTED from
  the standing pinned tables — single source of truth] + the
  hardening touch [two honest test renames, byte-identical
  assertions; `_PRODUCER_TOKENS` gained "brian" — bare "eno"
  false-positives on "enough", verified]; 21 files, +7943/−4;
  GREEN IN ISOLATION at **1143**) + `44381a8` (Commit-2 — README
  only: the ownership doctrine line VERBATIM exactly once ["engine
  owns move vocabulary / profile owns mode reach / governance owns
  safety cap"] + the committed mode-demo section +
  directory-driven discovery; +132/−2; ZERO collection changes —
  node-id lists diffed identical C1 vs HEAD) on parent `0c47fb7`,
  atop merge base `645c925` (= PR #26 — P-047 merged FIRST). ZERO
  .py under logic_mix_os/, zero profiles/fixtures/goldens, the
  FOUR existing trees byte-untouched (their pins 12/12). PUSHED
  BEFORE qa/reviewer (standing go — both gates validated the final
  SHAs), NOT merged. Suite **1143** / regression **93/93** /
  Commit-1 iso **1143** / freshness INDEPENDENT — all NINE
  verbatim README invocations via the real CLI → **9/9 creative
  pairs byte-identical** (cmp, zero normalization) / the hardening
  MUTATION-PROVEN load-bearing (an injected `brian_eno` engine
  branch FAILS the code-purity guard at HEAD, passes UNDETECTED at
  base) / sabotage EXACT (flipped byte → exactly 2; deleted demo
  dir → exactly 3; README id edit → nothing fails — the standing
  accepted README-drift posture, confirmed; rename reverted →
  nothing fails — docs-hygiene, confirmed) / README sweep
  "unpinned claims: none material" (the ownership line ONCE; the
  dropout line ONCE README-wide; the five-problems claim verified
  live, 1/5/3/4 branch counts) / safety grep none found. **Codex
  unavailable — single-model review.** Receipt:
  `build-os/receipts/P-048-mode-demo-artifacts.md`.
- **The user's seven demos ALL served by the nine committed
  pairs:** (1) different-producer = the four P-046 trees,
  referenced; (2–3) halee dramatic [A,B,C,D] / conservative
  [C,B,D] / deconstructive [B,C]; (4) the conservative four-way
  {A,B,C,D}/{B,C,D}/{B,C}/{B,D}; (5) quincy experimental — BOTH
  extended families live (85.3/83.1), vocal_C's governed WIN in
  committed bytes; (6) timbaland negative_space (dropout ids at
  80.9, F targeting [Synth Pad, Splice Texture Loop]) CONTRASTED
  with groove_pocket (declarations present, NO reach key, zero
  dropout ids — the only-where-authored evidence, judged STRONGER
  than a neutral mode); (7) halee reference-safety (her committed
  tree + her mode demos + a dedicated pin). Eno's role HONEST: a
  conservative demo with the vocal_B-by-suppression story (the
  builder CAUGHT AND FIXED its own overclaim pre-commit); his
  reaching modes undemoed (the user's list names
  quincy/timbaland/halee only).
- **★ THE P-047 ACCEPTED NOTES 1–2 ARE ✓ RESOLVED** (this packet's
  hardening touch: the two stale test names in
  `test_negative_space_dropout.py` renamed honestly —
  byte-identical assertions, count-neutral; the missing eno/brian
  token added as "brian" — mutation-proven load-bearing). P-047
  note 3 (the fifth-producer silent-skip margin) stands unchanged.
- **NEW accepted notes (P-048, recorded not fixed — the four
  reviewer residues, non-blocking):**
  1. **★ NAMED SUITE-WIDE HARDENING CANDIDATE — the directory-set
     guard:** nothing asserts `examples/mode_demos/` contains
     EXACTLY the nine pinned dirs — a tenth unpinned demo dir could
     land silently (matches the existing test_sample_refresh.py
     convention — the same gap suite-wide).
  2. **Hairline:** the "only shipped fixture with five problems"
     claim is verified-live but not itself pinned.
  3. **Ergonomic:** re-running a documented invocation verbatim
     writes 28 extra uncommitted files into the committed demo dir,
     which the file-set pin then flags — provenance-honest,
     slightly rough.
  4. **Coverage note:** eno's reaching modes are live-pinned but
     undemoed; 15 of 24 producer×mode combos undemoed (the nine
     cover all seven required stories) — future-surface material,
     none owed.
- **All prior standing notes RETAINED** (the banners below), incl.
  the ★★ STANDING TRAJECTORY WATCH-ITEM (a REAL groove-carrier
  signal before ANY dropout-surface widening) and the safety line
  (execution/apply semantics NEVER without explicit user
  re-gating).
- **Open boundary:** P-048's commits pushed to the dev branch
  BEFORE qa/reviewer under the orchestrator's standing go; **the
  MERGE of P-048 (`0c47fb7` + `4725169` + `44381a8` + the close
  commit, atop `645c925` = PR #26) is the OPEN USER GATE** — it
  awaits the user's explicit word.
- **NEXT: NOTHING STAGED.** The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): the P-048 merge ·
  quincy/halee authored dropout reach · the future-analyzer
  candidates from Eno's honest deferrals (textural coherence ·
  generative process · ambient patience) · a fifth producer
  (auto-discovered, auto-swept) · the directory-set-guard
  hardening candidate (note 1 above) · anything else the user
  calls. Do NOT open anything blind.
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-047 close, 2026-07-03): residue = accepted standing notes only — THE SWEEPS ARE PRODUCER-COMPLETE AND FUTURE-PROOF

- **P-047 (DIRECTORY-DRIVEN PRODUCER SWEEPS + DOCS RESIDUES — TEST +
  DOCS hardening, ZERO runtime changes by definition; opened on the
  user's "Go" 2026-07-03 after the P-046 merge [PR #25 → default tip
  `24b5ca7`], down the orchestrator's presented recommendation — the
  P-045 reviewer residue [the hardcoded three-producer sweep tuple] +
  the P-046 docs residues, one packet) closed 2026-07-03:** qa GREEN
  (11/11, zero discrepancies) + reviewer PASS (no must-fix). Commits
  `3322c88` (Commit-1 — `PRODUCERS = tuple(sorted(p.stem for p in
  _PRODUCERS_DIR.glob("*.json")))` [the IDENTICAL expression
  cli.py:50 uses on the product's single source of truth; the old
  hand-rolled second path DELETED — the P-045 drift vector is gone]
  + the NEW minimum-containment discovery guard
  `test_producer_sweep_is_directory_driven_with_the_known_minimum`
  [four known names as MINIMUM, no maximum — nothing blocks a fifth
  producer] + eno's data rows at every per-producer site, captured
  from the real engine then pinned; GREEN IN ISOLATION at **1122**)
  + `f9736f3` (Commit-2 — docs residues: four-fixture README,
  four-tree docstring, ~10 stale-prose sites across the sweep files;
  prose-only, ZERO collection changes — verified per file
  C1 == HEAD) on parent `37e4120`, atop merge base `24b5ca7` (= PR
  #25 — P-046 merged FIRST). Exactly **5 files, +125/−41**, ZERO
  .py under logic_mix_os/, zero profiles/fixtures/goldens, the four
  committed trees byte-untouched. PUSHED BEFORE qa/reviewer
  (standing go — both gates validated the final SHAs), NOT merged.
  Suite **1122** / regression **93/93** / Commit-1 iso **1122** /
  the fifth-producer property PROVEN (a synthetic `test_fifth.json`
  → passive collection growth 36→39, 41→46, 50→53; 5 exact
  KeyErrors, ZERO structural failures) / sabotage 3/3 (incl. the
  tuple reverted to the hardcoded three → the guard FAILS — silent
  regression impossible) / STOP-condition integrity held (fail-first
  = exactly 6 missing-data-row failures, zero structural — P-045's
  claimed equivalents were REAL). **Codex unavailable — single-model
  review.** Receipt:
  `build-os/receipts/P-047-directory-driven-sweeps.md`.
- **★ THE P-045 REVIEWER RESIDUE (c) IS ✓ RESOLVED** (the named
  future-packet candidate — the hardcoded `PRODUCERS` 3-tuples): the
  sweeps are now DIRECTORY-DRIVEN and a fifth producer grows them
  passively (proven); brian_eno is swept by the SAME structural
  guards as the three (the contract's consequential coverage items
  landed with the sweep extension). **THE P-046 DOCS RESIDUES
  (notes 1–2) ARE ✓ RESOLVED** (README fixture count; the four-way
  docstring), plus the sweep files' stale prose swept.
- **NEW accepted notes (P-047, recorded not fixed):**
  1. **Two stale test NAMES in `test_negative_space_dropout.py`:**
     `test_all_three_profiles_author_honest_dropout_rows` sweeps
     four; `test_same_mode_same_stems_only_timbaland_emits_dropout`
     stale since P-045 — name-only, the assertions are true and
     non-vacuous; rename = node-ID churn; fold into a future touch. **(✓
     RESOLVED by P-048, 2026-07-03: both renamed honestly in the
     hardening touch — byte-identical assertions, count-neutral;
     see the P-048 banner above.)**
  2. **`_PRODUCER_TOKENS` at `test_mode_forking.py:873` has no
     eno/brian token** — the fork-path code-purity guard wouldn't
     flag a hypothetical eno-named engine branch (pre-existing since
     P-045; the same holds for any fifth name) — fold the token
     list into the next hardening touch. **(✓ RESOLVED by
     P-048, 2026-07-03: the list gained "brian" [bare "eno"
     false-positives on "enough"] — MUTATION-PROVEN load-bearing:
     an injected `brian_eno` engine branch fails the guard at HEAD,
     passed undetected at base; see the P-048 banner above.)**
  3. **`test_same_mode_same_stems_each_producer_emits_only_its_authored_reach`
     would silently skip (collect-but-not-assert) a fifth producer's
     emission** — marginal: the loud KeyErrors elsewhere force
     conscious extension.
- **All prior standing notes RETAINED** (the banners below), incl.
  the ★★ STANDING TRAJECTORY WATCH-ITEM (a REAL groove-carrier
  signal before ANY dropout-surface widening) and the safety line
  (execution/apply semantics NEVER without explicit user re-gating).
- **Open boundary:** P-047's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-047 (`37e4120` + `3322c88` + `f9736f3` + the close commit, atop
  `24b5ca7` = PR #25) is the OPEN USER GATE** — it awaits the
  user's explicit word. **(✓ RESOLVED at P-048 open,
  2026-07-03: merged as PR #26 on the user's directive — merge
  commit `645c925`, the current default tip and the P-048 merge
  base.)**
- **NEXT: NOTHING STAGED.** The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): the P-047 merge ·
  quincy/halee authored dropout reach · the future-analyzer
  candidates from Eno's honest deferrals (textural coherence ·
  generative process · ambient patience) · a fifth producer (now
  cheaper than ever — auto-swept) · the small test-name/token-list
  hardening touch (notes 1–3 above) · anything else the user calls.
  Do NOT open anything blind. **(✓ UPDATE at P-048 close,
  2026-07-03: the user called the PRODUCT-SURFACE REFRESH —
  producer + mode demo artifacts [carrying the hardening touch;
  notes 1–2 above ✓ RESOLVED, note 3 stands]; opened and CLOSED as
  P-048 — see the P-048 banner above; NEXT = NOTHING STAGED again,
  the orchestrator presents the open directions.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-046 close, 2026-07-03): residue = accepted standing notes only — THE PRODUCT SURFACE MATCHES THE PRODUCT

- **P-046 (PRODUCT-SURFACE REFRESH — The Four-Producer Demo,
  docs/demo only; opened on the user's "go" 2026-07-03 after the
  P-045 merge [PR #24 → default tip `0a53bb5`], down the
  orchestrator's presented recommendation — the P-040 pattern
  extended to the four-producer world) closed 2026-07-03:** qa GREEN
  (12/12) + reviewer PASS (no must-fix). Commits `c94f2fe` (Commit-1
  — the two NEW 30-artifact trees `examples/sample_output_quincy/`
  [68.8; his LIVE default-mode reach surface: declarations {medium,
  reach [arrangement_lift]}, chorus_lift_E among candidates, winner
  unmoved] + `examples/sample_output_eno/` [65.5; authored-neutral
  byte-silence — zero declaration/fork keys; winner vocal_B vs the
  others' vocal_A], real-CLI renders from `vocal_chop_groove` with
  relative paths, + the staleness pin extended to FOUR at full P-040
  strength + the NEW mode-surface pin
  [`test_committed_sample_mode_surface_is_the_authored_reach` ×4] +
  test-9 2→4; 62 files, +7029/−17; GREEN IN ISOLATION at **1110**)
  + `95f65bf` (Commit-2 — README only: the "Four producers, same
  stems" four-way + modes-are-behavior + the extended families with
  the dropout safety line VERBATIM + 8 stale-wording fixes;
  +112/−28) on parent `8674a97`, atop merge base `0a53bb5` (= PR
  #24 — P-045 merged FIRST). Exactly **63 files**, ZERO .py under
  logic_mix_os/, zero profiles/fixtures/goldens; the two EXISTING
  trees byte-untouched — NO staleness bug found (fresh renders
  byte-identical). PUSHED BEFORE qa/reviewer (standing go — both
  gates validated the final SHAs; the commits were recut once
  locally before pushing to fix a docstring inaccuracy — the gates
  judged the final tree), NOT merged. Suite **1110** / regression
  **93/93** / Commit-1 iso **1110** / freshness INDEPENDENT —
  byte-identical 30/30 × 4 with zero normalization / headlines
  76.3/60.9/68.8/65.5 / README accuracy sweep "unpinned claims
  found: none material" / sabotage bites on every tree-side flip.
  **Codex unavailable — single-model review (the reviewer
  re-rendered all four trees itself: raw byte-identical).** Receipt:
  `build-os/receipts/P-046-four-producer-demo.md`.
- **NEW accepted notes (P-046, recorded not fixed):**
  1. **Reviewer residue (1):** README line 46 — "the three example
     projects" is PRE-EXISTING fixture-count staleness (the
     generator builds four), outside this packet's producer-roster
     sweep — fold into a future docs touch.
  2. **Reviewer residue (2):** the `test_four_way_differential.py`
     docstring at ~875 now under-describes 2-of-4 committed trees —
     wording only, fold on next touch.
  3. **qa observation:** test-internal docstrings elsewhere say "two
     producers"/"all three producers" — accurate statements or
     era-comments; test-internal, not product surface.
  4. **★ The standing README-number-drift accepted gap RE-AFFIRMED
     (the P-040 note, unchanged in posture):** sabotage (c) — a
     README-side number flip stays green; accepted because the
     values are pinned at the artifact/test level and a
     markdown-parsing test stays not worth its brittleness.
  - Notes 1–2 pair naturally with the P-045 directory-driven
    `PRODUCERS`-tuple sweeps hardening — one hardening/docs packet,
    ★ USER-GATED. **(✓ RESOLVED by P-047, 2026-07-03:
    notes 1–2 FIXED — README "the four example projects" [generator
    verified: exactly 4 builders] + the four-way docstring re-worded;
    note 3's stale sweep-file prose also swept [~10 sites]; see the
    P-047 banner above.)**
- **All prior standing notes RETAINED** (the banners below), incl.
  the ★★ STANDING TRAJECTORY WATCH-ITEM (a REAL groove-carrier
  signal before ANY dropout-surface widening) and the safety line
  (execution/apply semantics NEVER without explicit user re-gating).
- **Open boundary:** P-046's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-046 (`8674a97` + `c94f2fe` + `95f65bf` + the close commit, atop
  `0a53bb5` = PR #24) is the OPEN USER GATE** — it awaits the
  user's explicit word. **(✓ RESOLVED at P-047 open, 2026-07-03:
  merged as PR #25 on the user's directive — merge commit `24b5ca7`,
  the current default tip and the P-047 merge base.)**
- **NEXT: NOTHING STAGED.** The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): the P-046 merge · the
  directory-driven sweeps hardening (the P-045 named candidate, now
  joined by P-046 notes 1–2 above) · quincy/halee authored dropout
  reach · the future-analyzer candidates from Eno's honest deferrals
  (textural coherence · generative process · ambient patience) · a
  fifth producer · anything else the user calls. Do NOT open
  anything blind. **(✓ UPDATE at P-047 close, 2026-07-03: the
  user called the directory-driven sweeps + docs residues hardening —
  opened and CLOSED as P-047 — see the P-047 banner above; NEXT =
  NOTHING STAGED again, the orchestrator presents the open
  directions.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-045 close, 2026-07-03): residue = accepted standing notes only — THE PRODUCER ROSTER IS FOUR

- **P-045 (THE FOURTH PRODUCER — Brian Eno, profile-only; the user's
  pick, verbatim 2026-07-03: "Yes — pick another producer, but merge
  P-044 first… My producer pick: Brian Eno" — P-044 merged FIRST as
  PR #23 → default tip `fe8d947`) closed 2026-07-03:** qa GREEN
  (12/12, ZERO deviations) + reviewer PASS (no must-fix). Commits
  `47aace7` (Commit-1 — `brian_eno.json` [333 lines: negative_space
  1.4 = his argmax, all four argmaxes distinct; SEVEN axes outside
  the three-way envelope; protect_iconic_loops TRUE with authored
  static 35.0; blend floor 0.85 the strictest shipped; dropout reach
  on exactly generative_drift + experimental; confidence map 6 high
  / 1 limited / 8 deferred — his own three no-axis concepts DEFERRED,
  not faked] + the 36-test guard suite; GREEN IN ISOLATION at
  **1036**) + `c3fa783` (Commit-2 — the permanent 64-test FOUR-WAY
  differential, all 8 user requirements incl. dropout governance) on
  parent `6df37b3`, atop merge base `fe8d947` (= PR #23 — P-044
  merged FIRST on the user's directive). Exactly **3 NEW files,
  +2382/−0**, ZERO .py under logic_mix_os/, ZERO existing-test
  edits; the three shipped JSONs sha256-identical to their `fe8d947`
  blobs (pinned PERMANENTLY in the four-way suite); both sample
  trees untouched. PUSHED BEFORE qa/reviewer (standing go — both
  gates validated the final SHAs), NOT merged. Suite **1100** /
  regression **93/93** / Commit-1 iso **1036** / ZERO passive growth
  / sabotage **5/5** / measured overalls 65.4 / 57.8 / 59.3 / 65.5 —
  pairwise distinct from all three on every fixture, reconstruction
  to the decimal. **Codex unavailable — single-model review
  (independent worktree execution: 1100 + 1036 reproduced).**
  Receipt: `build-os/receipts/P-045-brian-eno.md`.
- **NEW accepted notes (P-045, recorded not fixed):**
  1. **Reviewer residue (a):** Eno's no-mode/unknown-mode
     zero-extended assertion covers dropout ids ONLY — the other
     extended path is the profile-independent neutral fallback,
     swept three-way at code level.
  2. **Reviewer residue (b):** Eno's default-flow candidate lists
     are kind-set/winner-pinned, not id-order-pinned like the three
     — a one-line tightening on next touch.
  3. **★ Reviewer residue (c) — NAMED FUTURE-PACKET CANDIDATE:** the
     hardcoded `PRODUCERS` 3-tuples in `test_mode_forking.py`
     (imported by two other suites) should eventually become
     DIRECTORY-DRIVEN so a FIFTH producer grows the sweeps
     passively — an existing-test change, correctly out of P-045's
     scope. **(✓ RESOLVED by P-047, 2026-07-03: the tuple
     is now DIRECTORY-DRIVEN — the IDENTICAL cli.py:50 expression on
     the producers dir, the drift vector deleted, the
     minimum-containment guard added; a fifth producer PROVEN to grow
     the sweeps passively; see the P-047 banner above.)**
  4. **The honest future-analyzer candidates (from Eno's own
     deferrals — ★ USER-GATED):** textural coherence · generative
     process/Oblique Strategies · ambient patience — measurement
     axes that don't exist yet, deferred rather than faked (exactly
     the user's demand); the honest candidates for a future analyzer
     packet.
- **All prior standing notes RETAINED** (the banners below), incl.
  the ★★ STANDING TRAJECTORY WATCH-ITEM (a REAL groove-carrier
  signal before ANY dropout-surface widening) and the safety line
  (execution/apply semantics NEVER without explicit user re-gating).
- **Open boundary:** P-045's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-045 (`6df37b3` + `47aace7` + `c3fa783` + the close commit, atop
  `fe8d947` = PR #23) is the OPEN USER GATE** — it awaits the user's
  explicit word. **(✓ RESOLVED at P-046 open, 2026-07-03: merged as
  PR #24 on the user's directive — merge commit `0a53bb5`, the
  current default tip and the P-046 merge base.)**
- **NEXT: NOTHING STAGED.** The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): the P-045 merge ·
  product-surface refresh (samples/README don't yet showcase
  mode-forking, the new move families, or the four-producer roster)
  · the directory-driven sweeps hardening (note 3 above) ·
  quincy/halee authored dropout reach · the future-analyzer
  candidates (note 4 above) · a fifth producer · anything else the
  user calls. Do NOT open anything blind. **(✓ UPDATE at P-046
  close, 2026-07-03: the user called the PRODUCT-SURFACE REFRESH —
  opened and CLOSED as P-046 — see the P-046 banner above; NEXT =
  NOTHING STAGED again, the orchestrator presents the open
  directions.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-044 close, 2026-07-03): residue = accepted standing notes only — THE DROPOUT FAMILY IS GOVERNED; THE SHAPE C ARC IS COMPLETE

- **P-044 (NEGATIVE-SPACE DROPOUT MOVE FAMILY — opened NARROWLY AND
  CONSERVATIVELY on the user's word; THE SAFETY LINE, the user's
  doctrine verbatim: "dropout is an arrangement proposal, not a
  destructive operation" — candidate-planning only, NO execution
  semantics) closed 2026-07-03:** qa GREEN + reviewer PASS (no
  must-fix; all adversarial attacks defeated). Commits `87635d3`
  (Commit-1 — the kind + the curated variants [`chorus_lift_F` +
  `density_E`; the LOOP dropout consciously OMITTED —
  `DROPOUT_POOL["loop"] == []` pinned] + the profile-blind
  `_dropout_protected_names` filter with the fail-closed NO-EMIT rule
  + honest rows everywhere; ZERO behavioral change — GREEN IN
  ISOLATION at **984**) + `f72f222` (Commit-2 — Timbaland's authored
  dropout reach [exactly experimental / dramatic_contrast /
  negative_space] + the differential proof + the conscious enumerated
  drift [EXACTLY 3 regenerated timbaland artifacts; the halee tree
  ABSENT from the diff]) on parent `9fdb172`, atop merge base
  `80e9bd5` (= PR #22 — P-043 merged FIRST on the user's directive).
  Exactly 13 files, +1354/−112; `producer_profile.py` UNCHANGED (the
  P-043 loader gates generalize unmodified — proven live). PUSHED
  BEFORE qa/reviewer (standing go — both gates validated the final
  SHAs), NOT merged. Suite **1000** / regression **93/93** / Commit-1
  iso **984** / the 312-cell differential 0 mismatches / EVERY winner
  unchanged / sabotage 4/4 / halee's governance VETO live (intimate
  truth 48 < align_veto 50). **Codex unavailable — single-model
  review (the full suite independently re-run at 1000).** Receipt:
  `build-os/receipts/P-044-negative-space-dropout.md`.
- **NEW accepted notes (P-044, recorded not fixed):**
  1. **qa discrepancy #1 (task-premise):** `_lead_masked` is False on
     EVERY fixture at HEAD (no real fixture carries a bad-masked
     lead) — the masked-lead exclusion is proven SYNTHETICALLY only.
     Fine: the synthetic tests bite exactly.
  2. **qa discrepancy #2 (filter bite surface):** removing the filter
     changes NO shipped artifact bytes (no protected name sits on the
     shipped fixtures' candidate surfaces today) — the protection
     guarantee rests on the 4 synthetic tests, which bite exactly.
  3. **Reviewer residual (AST-guard blind spot):** the AST guard
     would miss a future profile-sourced global whose name lacks
     "prof" — today's code reads none; the runtime differentials
     carry the real weight.
  4. **★★ STANDING TRAJECTORY WATCH-ITEM (reviewer — binding on any
     future dropout packet):** a REAL groove-carrier signal is
     required before ANY dropout-surface widening — do NOT fake it
     from beat_identity (its dense-fixture "dominant" is a synth pad;
     kick/snare/bass is the only honest read of "main kick/sub
     foundation" today).
  5. **Execution/apply semantics NEVER without explicit user
     re-gating** — the safety line is standing doctrine.
- **All prior standing notes RETAINED** (the banners below).
- **Open boundary:** P-044's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-044 (`9fdb172` + `87635d3` + `f72f222` + the close commit, atop
  `80e9bd5` = PR #22) is the OPEN USER GATE** — it awaits the user's
  explicit word. **(✓ RESOLVED at P-045 open, 2026-07-03: merged as
  PR #23 on the user's directive — merge commit `fe8d947`, the
  current default tip and the P-045 merge base.)**
- **NEXT: NOTHING STAGED — the user's sequenced arc is COMPLETE**
  (CLI ✓ samples ✓ third producer ✓ analyzer extension ✓
  mode-forking B ✓ vocabulary C narrow ✓ dropout ✓). The
  orchestrator PRESENTS the open directions to the user (ALL
  user-gated): quincy/halee authored dropout reach · further C
  families (behind the groove-carrier watch-item where applicable) ·
  a fourth producer · product-surface work (samples/README refresh
  for the new families) · anything else the user calls. Do NOT open
  anything blind. **(✓ UPDATE at P-045 close, 2026-07-03: the user
  called the FOURTH PRODUCER — Brian Eno; opened and CLOSED as
  P-045 — see the P-045 banner above; NEXT = NOTHING STAGED again,
  the orchestrator presents the open directions.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-043 close, 2026-07-03): residue = accepted standing notes only — THE MOVE VOCABULARY IS WIDENED AND GOVERNED

- **P-043 (CURATED MOVE VOCABULARY EXPANSION — Shape C, opened
  NARROWLY: arrangement_lift + ensemble_rebalance ONLY; negative-space
  dropout EXPLICITLY EXCLUDED by the user) closed 2026-07-03:** qa
  GREEN + reviewer PASS (no must-fix; all adapted adversarial attacks
  defeated). Commits `ed94020` (Commit-1 — `CREATIVE_VARIANT_KINDS`
  7→9 + `CREATIVE_EXTENDED_KINDS`; the `reach_kinds` seam
  [extended-vocabulary-only; reached variants append after the neutral
  pool; suppression beats reach; fallback neutral-pool-only; two-layer
  cap incl. runtime `reach_capped`]; 4 new curated variants, all
  `non_destructive_duplicate_track` / anti-mute; kind_scores +
  truth_alignment rows in ALL three profiles; ZERO behavioral change —
  GREEN IN ISOLATION at **944**) + `e382d86` (Commit-2 — Quincy's
  authored reach [three modes; the P-042 approximation favor
  consciously REPLACED] + the differential proof) on parent `3110126`,
  atop merge base `17cc270` (= PR #21 — P-042 merged FIRST on the
  user's directive). Exactly 11 files, +1184/−96; halee/timbaland
  author `reach_kinds []` everywhere → zero extended emissions over 48
  runs. PUSHED BEFORE qa/reviewer (standing go — both gates validated
  the final SHAs), NOT merged. Suite **950** / regression **93/93** /
  Commit-1 iso **944** / the 234-cell reach reconstruction 0
  mismatches / ALL winners unchanged / sabotage 4/4 / a governed WIN
  through full analyze() (vocal_C at 83.1). **Codex unavailable —
  single-model review (independent worktree execution: HEAD 950 +
  C1 944 reproduced).** Receipt:
  `build-os/receipts/P-043-move-vocabulary-expansion.md`.
- **★ THE P-042 APPROXIMATION NOTE IS ✓ RESOLVED** (accepted note 3 in
  the P-042 banner below): quincy experimental's subtractive_drop +
  width_bloom favor — the in-vocabulary approximation — is consciously
  REPLACED by real authored reach over the true families.
- **NEW accepted notes (P-043, recorded not fixed):**
  1. **qa discrepancy #1 (count composition, direction safe):**
     Commit-1 iso 944 = 907 + 29 new + 8 PASSIVE growth in the
     untouched `tests/test_creative_nudges.py`; C2 net +6 = +7
     new-file / −1 mode_forking consolidation. A calibration note on
     count accounting, not a defect.
  2. **qa discrepancy #2 (pin coverage):** quincy's chop-fixture
     default flow ALSO gains chorus_lift_E — same authored mechanism,
     winner unchanged, doctrine unmoved, sample trees unaffected — but
     UNPINNED (the 4th fixture lives outside the FIXTURE_NAMES pin
     corpus); candidate one-line pin extension in a future packet.
  3. **Reviewer observation (1):** `fork["reached"]` on a
     loader-BYPASSING profile reaching a NEUTRAL kind would misreport
     it as reached (emission unaffected; the loader rejects the
     authoring) — future tightening: intersect with admitted kinds.
  4. **Reviewer observation (2):** the degenerate empty-neutral-pool +
     bypass edge — unreachable on all five shipped problem ids,
     pre-existing in shape.
- **All prior standing notes RETAINED** (the banners below).
- **Open boundary:** P-043's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-043 (`3110126` + `ed94020` + `e382d86` + the close commit, atop
  `17cc270` = PR #21) is the OPEN USER GATE** — it awaits the user's
  explicit word. **(✓ RESOLVED at P-044 open, 2026-07-03:
  merged as PR #22 on the user's directive — merge commit `80e9bd5`,
  the current default tip and the P-044 merge base.)**
- **NEXT — ★ USER-GATED: negative-space dropout as a move family**
  (the user's own sequencing: "after C proves the widened vocabulary
  can stay governed" — C has now proven exactly that; adding it = one
  `CREATIVE_EXTENDED_KINDS` entry + curated variants + authored reach,
  ZERO engine changes); STAGED in `build-os/packets/active_packet.md`
  — the decision of whether/when is the USER'S; the orchestrator
  presents scope first, does NOT open blind. **(✓ DONE at P-044
  close, 2026-07-03: opened NARROWLY AND CONSERVATIVELY on the user's
  word and CLOSED as P-044 — see the P-044 banner above; ★ THE SHAPE
  C ARC IS COMPLETE; NEXT = NOTHING STAGED — the orchestrator
  presents the open directions.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-042 close, 2026-07-03): residue = accepted standing notes only — THE MODE LEVER IS LOAD-BEARING

- **P-042 (PROFILE-AUTHORED MODE FORKING — Shape B) closed
  2026-07-03:** qa GREEN + reviewer PASS (no must-fix; all EIGHT
  user-mandated adversarial attacks defeated). Commits `9acecfd` (the
  seam: additive `profile` param; `suppress_kinds` = candidate-SET
  fork / `favor_kinds` = order-only reach / absent = byte-identical
  neutral; the frozen `CREATIVE_VARIANT_KINDS` vocabulary; loader
  validation incl. the over-cap "cannot be out-authored" ValueError;
  runtime fail-closed cap; non-empty `suppression_fallback`; the
  reference's authored declarations; GREEN IN ISOLATION at 894) +
  `9d746e3` (timbaland + quincy mode declarations, the three-way mode
  differential, the requirement-10 artifact surface) on parent
  `ab4914a`, atop merge base `dadda12` (= PR #20 — P-041 merged FIRST
  on the user's directive). Exactly 9 files, +1069/−27; every mode of
  all three producers explicitly authored; all three DEFAULT/intimate
  modes authored-neutral → defaults byte-identical. PUSHED BEFORE
  qa/reviewer (orchestrator standing go — both gates validated the
  final SHAs), NOT merged. Suite **907** / regression **93/93** /
  Commit-1 iso **894** / the 90-cell attribution reconstruction 0
  mismatches / 12 default-flow runs byte-identical / sabotage 4/4.
  **Codex NOT available — single-model review (own executed probes).**
  The standing doctrine extends to creative reach: **engine owns move
  vocabulary / profile owns mode reach / governance owns safety cap.**
  Receipt: `build-os/receipts/P-042-mode-forking.md`.
- **★ THE P-033 "THIN LEVER" CALIBRATION NOTE IS ✓ RESOLVED** —
  `generate_variants` now forks candidate generation on the mode via
  profile-authored data (annotated in place below); behavioral
  steering may now be claimed.
- **NEW accepted notes (P-042, recorded not fixed):**
  1. **Cap-semantics stated decision (reviewer finding 1):**
     `allowed_risk` caps authored ELEVATION (favor), not pool
     membership — a loader-legal low-posture mode can suppress
     everything except the one medium-risk kind and thereby
     concentrate emission on it; that kind was always in the neutral
     pool, scoring/governance unchanged. Documented semantics, not a
     hole.
  2. **Dedupe nit (reviewer finding 2):** duplicate favor_kinds from a
     loader-BYPASSING profile duplicate variant dicts in emission —
     unreachable via load_profile (the loader rejects duplicates); a
     one-line dedupe is a future hardening candidate.
  3. **Quincy experimental (subtractive_drop + width_bloom) is the
     closest IN-VOCABULARY approximation** of the user's
     "arrangement-lift / ensemble-rebalance" example — the true
     families are STAGED C; recorded as C's motivation. **(✓ RESOLVED
     by P-043, 2026-07-03: the approximation favor consciously
     REPLACED by real authored reach over the true families — see
     the P-043 banner above.)**
  4. **winning_variant tie-break (reviewer finding 4):** max =
     first-wins; favor-reordering could flip an EXACT score tie; none
     exists today, and a favored kind winning a tie is arguably
     authored intent.
  5. **qa's builder-report discrepancy:** gutted-fork sabotage — 5
     failures claimed vs **10 measured**; direction SAFE (the net is
     STRONGER than claimed). A calibration note on builder
     self-reports, not a defect.
- **All prior standing notes RETAINED** (the banners below).
- **Open boundary:** P-042's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-042 (`ab4914a` + `9acecfd` + `9d746e3` + the close commit, atop
  `dadda12` = PR #20) is the OPEN USER GATE** — it awaits the user's
  explicit word. **(✓ RESOLVED at P-043 open, 2026-07-03: merged as
  PR #21 on the user's directive — merge commit `17cc270`, the
  current default tip and the P-043 merge base.)**
- **NEXT per the USER = Shape C — new mode-specific move families**
  (extend `CREATIVE_VARIANT_KINDS` + the curated builders through a
  conscious packet; profiles then author reach with ZERO loader/fork
  changes); STAGED in `build-os/packets/active_packet.md` —
  ★ USER-GATED: not built until the user opens it; the orchestrator
  presents scope first. **(✓ DONE at P-043 close, 2026-07-03: Shape C
  opened NARROWLY on the user's word [arrangement_lift +
  ensemble_rebalance only; negative-space dropout EXPLICITLY
  EXCLUDED] and CLOSED as P-043 — see the P-043 banner above; NEXT =
  negative-space dropout, ★ USER-GATED.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-041 close, 2026-07-03): residue = accepted standing notes only — THE PRODUCER ROSTER IS THREE

- **P-041 (THE THIRD PRODUCER — Quincy Jones, profile-only) closed
  2026-07-03:** qa GREEN + reviewer PASS (no must-fix). Commits
  `f2614f9` (quincy_jones.json + its own guards, 27 tests + the
  conscious `test_producer_cli.py` delta) + `dfe8c54` (the PERMANENT
  40-test three-way differential proof) on parent `ece2b5c`, atop
  merge base `61582b5` (= PR #19 — the P-039+P-040 pair merged FIRST
  on the user's directive; both P-041 commits are TREE-IDENTICAL
  identity re-stamps of the builder's originals `3acd53f`/`f517e0b`,
  metadata-only). Exactly 4 files, +1673/−4, ZERO .py under
  logic_mix_os/; existing profiles blob-identical. PUSHED BEFORE
  qa/reviewer (orchestrator standing go — both gates validated the
  final SHAs), NOT merged. Suite **873** / regression **93/93**.
  **Codex NOT available — single-model review.** Receipt:
  `build-os/receipts/P-041-quincy-jones.md`.
- **NEW accepted notes (P-041, recorded not fixed):**
  1. **Reviewer nit:** an int among float pins in the quincy guards
     (`"section_contrast_score": 82`) — cosmetic, fold on next touch
     of `tests/test_quincy_profile.py`.
  2. **Reviewer nit:** `QUINCY_ONLY_STRINGS` doesn't include one stamp
     variant — leakage is impossible anyway via the per-producer
     equality asserts; fold on next touch.
  3. **"groove-as-support" is the SOFTEST defensible `high`** in
     quincy's confidence map — FIRST to re-examine if the user ever
     tightens the grounding standard.
  4. **The stale local `origin/main` ref (qa environment note, not a
     defect):** the true default is `claude/dreamy-turing-z0oxll` at
     `61582b5`, confirmed via the branch chain — FETCH before any
     landing decision.
- **All prior standing notes RETAINED** (the banners below).
- **Open boundary:** P-041's commits pushed to the dev branch BEFORE
  qa/reviewer under the orchestrator's standing go; **the MERGE of
  P-041 (`ece2b5c` + `f2614f9` + `dfe8c54` + the close commit, atop
  `61582b5` = PR #19) is the OPEN USER GATE** — it awaits the user's
  explicit word. **(✓ RESOLVED at P-042 open, 2026-07-03: merged
  as PR #20 on the user's directive — merge commit `dadda12`, the
  current default tip and the P-042 merge base.)**
- **NEXT per the USER'S SEQUENCE = DEEPER MODE-FORKING in variant
  generation** (`search_mode` is a THIN lever today —
  `generate_variants` does not fork on it; the P-033 reviewer
  calibration note); STAGED in `build-os/packets/active_packet.md` —
  ★ USER-GATED: the orchestrator presents the shape/scope decision;
  do NOT open blind. **(✓ DONE at P-042 close, 2026-07-03: the shape
  gate was presented and the user chose Shape B — profile-authored
  mode forking; CLOSED as P-042, the mode lever now LOAD-BEARING — see
  the P-042 banner above; NEXT = Shape C, ★ USER-GATED.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-040 close, 2026-07-02): residue = accepted standing notes only — the DEMO IS COMMITTED AND STALENESS-PINNED

- **P-040 (the SAMPLE REFRESH — the two-producer demo output) closed
  2026-07-02:** qa GREEN + reviewer PASS (no must-fix). Commits
  `33cf10d` (the two 30-artifact trees from `vocal_chop_groove` +
  test-9 over both trees + the FULL-strength staleness pin,
  62 files, +4240/−1744) + `9e58e9b` (README only, +49/−2) on parent
  `1783683`, atop merge base `2c09428`; PUSHED after close
  (orchestrator standing go), NOT merged. Suite **806** / regression
  **93/93**. Docs/demo only — ZERO product code. **Codex NOT
  available — single-model review.** Receipt:
  `build-os/receipts/P-040-sample-refresh.md`.
- **★ THE P-038 STANDING NOTE 1 IS ✓ CLEARED**
  (`examples/sample_output/` shipped stale pre-P-036/P-038 prose): the
  old dense_chorus-era tree replaced WHOLESALE; qa confirmed the stale
  strings EXISTED at base and are ABSENT now; the staleness pin
  (30-file byte equality per tree against a fresh render) makes silent
  rot IMPOSSIBLE going forward.
- **NEW accepted notes (P-040, recorded not fixed):**
  1. **The accepted README-drift gap:** a README-side number edit is
     not machine-caught (the reviewer ran the sabotage — a README flip
     stays green); accepted because the values are triple-pinned at the
     FILE level (the headline pin machine-checks the README numbers
     from the artifact side) and a markdown-parsing test would be
     brittle for marginal value.
  2. **A future echo-semantics tightening on the staleness pin:**
     assert the FRESH tree carries the abs path in exactly the two
     expected files — closes the narrow blind spot where an
     "absolutizes-the-echo" regression would stay green.
  3. **The reviewer nit:** "repo root" vs "project root" wording in
     the vendored arrangement — cosmetic, fold on next touch.
- **All P-039 + P-038 standing notes RETAINED** (the banners below),
  with the P-038 note-1 trajectory ✓ RESOLVED as above.
- **Open boundary:** P-040's commits pushed to the dev branch AFTER
  close under the orchestrator's standing go; the MERGE remains a user
  gate (the branch carries P-039 + P-040 + closes atop `2c09428`).
- **NEXT = THE THIRD PRODUCER — ★ USER-GATED on WHICH producer + the
  grounding** (the standing honesty policy: hand-curated-documented →
  high; derived → low, labeled; LLM-synthesized → draft-only, never
  high); STAGED in `build-os/packets/active_packet.md` — the
  orchestrator presents the decision; do NOT open blind. Then deeper
  mode-forking. **(✓ DONE at P-041 close, 2026-07-03: both gates
  answered in one directive — producer = Quincy Jones, grounding =
  hand-curated-from-documented-technique → high, PR #19 merged FIRST →
  `61582b5`; CLOSED as P-041 — see the P-041 banner above; NEXT =
  deeper mode-forking, ★ USER-GATED on shape/scope.)**
- **THE THREE NAMED LESSONS (standing, retained):** (1) raw-dict NaN
  comparisons FAIL OPEN; (2) defense claims need MUTATION TESTS, not
  placement faith; (3) flag PRESENCE is not flag THREADING — levers
  need reaches-the-destination guards.

## ★★★ STATUS (P-039 close, 2026-07-02): residue = accepted standing notes only — the PRODUCT ARC is running

- **P-039 (Producer Selection CLI Exposure + Demo-Safe Invocation — THE
  FIRST POST-SUBSTRATE PRODUCT PACKET) closed 2026-07-02:** qa GREEN +
  reviewer fix-then-pass → PASS (one fix round, fully resolved). Commits
  `b111a18` (the feature) + review-fix `a56cb96` (TEST-ONLY) on parent
  `73a134e`, atop merge base `2c09428` (the post-backlog batch merge —
  the P-038-era open user gate ✓ RESOLVED on the user's word); PUSHED
  after close (orchestrator standing go), NOT merged. Suite **801** /
  regression **93/93**. Receipt:
  `build-os/receipts/P-039-producer-cli-exposure.md`.
- **★★ NEW (P-039 — NAMED LESSON, standing; the THIRD of the family):
  flag PRESENCE is not flag THREADING — levers need
  REACHES-THE-DESTINATION guards.** The reviewer's live sabotage dropped
  the threading at ONE analyze site and the FULL suite stayed green (10
  of 13 carriers were flag-presence-pinned only); the fix (`a56cb96`)
  spies the producer kwarg at cli.analyze / cowork.analyze through the
  REAL cli.main at all 13 carriers — a dropped threading arrives as None
  and fails the isinstance-ProducerProfile pin on every path. Joins the
  two P-037 lessons — the same family: prove the lever REACHES its
  destination, never just that the flag exists.
- **NEW accepted notes (P-039, recorded not fixed):**
  1. **The success-path subprocess nuance:** the ERROR path is
     subprocess-proven; the success path runs the same `cli.main`
     in-process — a success-path subprocess run is a possible future
     hardening, not debt.
  2. **The `_PRODUCERS_DIR` private-name import in `cli.py`** — a public
     accessor is a possible follow-up API nicety; fold on next touch.
- **All P-038 standing notes RETAINED** (the banner below), with ONE
  trajectory update: standing note 1 (`examples/sample_output/` ships
  stale pre-P-036/P-038 prose) is set to be CLEARED by the STAGED sample
  refresh — the next packet per the USER'S SEQUENCE (sample refresh →
  third producer → deeper mode-forking); see
  `build-os/packets/active_packet.md` (conscious test-9 OLD_KEYS
  interaction check noted there). NOT active until confirmed. **(✓ DONE
  at P-040 close, 2026-07-02: the sample refresh CLOSED as P-040 and
  standing note 1 is ✓ CLEARED — see the P-040 banner above.)**
- **Open boundary:** P-039's commits pushed to the dev branch AFTER
  close under the orchestrator's standing go; the MERGE remains a user
  gate.
- **THE THREE NAMED LESSONS (standing, retained for posterity):** (1)
  raw-dict NaN comparisons FAIL OPEN (`x < nan` is False) — audit future
  raw-comparison gates for the same shape; (2) defense claims need
  MUTATION TESTS, not placement faith; (3) flag PRESENCE is not flag
  THREADING — levers need reaches-the-destination guards.

## ★★★ RESIDUE: ZERO — accepted standing notes only (P-038 close, 2026-07-02)

- **★★★ THE ENTIRE POST-MERGE BACKLOG IS COMPLETE.** P-038 (residue sweep
  2 of 2 — naming/prose, THE LAST BACKLOG PACKET) closed 2026-07-02: qa
  GREEN + reviewer fix-then-pass → PASS. **NO packet-worthy residue
  remains** — everything below this banner is history (✓ resolved in
  place), a named lesson retained for posterity, or an opportunistic
  fold-on-next-touch cosmetic. **THE OPEN USER GATE is the batch merge —
  P-036 + P-037 + P-038 (+ closes) onto merge base `dc921ec` (= PR #18) —
  on the user's explicit word.** **(✓ RESOLVED before P-039, 2026-07-02:
  merged git-natively as `2c09428` on the user's word — the current
  merge base.)**
- **ACCEPTED STANDING NOTES (user-level, recorded not fixed):**
  1. **`examples/sample_output/` ships pre-P-036/P-038 prose**
     (producer-named action strings, stale verdict text) — not
     test-pinned, predates P-038; a conscious doc-refresh decision for a
     future moment, NOT expanded into P-038 (the P-030 precedent
     regenerated samples for a CONTRACT change; this is prose).
     **✓ CLEARED by P-040 (2026-07-02): the two-producer sample
     refresh replaced the tree WHOLESALE (dense_chorus-era →
     `vocal_chop_groove`, both producers) and the FULL-strength
     staleness pin makes silent rot impossible.**
  2. **The duplicated trailer block in `7b9eda7`'s raw commit message**
     (cosmetic; dedup'd by tooling when displayed; judged not worth
     another force-push).
  3. **The push-state observation:** remote-ref updates on the dev
     branch are the orchestrator's standing-go session pushes, not
     agent-initiated pushes.
- **THE TWO NAMED LESSONS (standing, retained for posterity):** (1)
  raw-dict NaN comparisons FAIL OPEN (`x < nan` is False) — audit future
  raw-comparison gates for the same shape; (2) defense claims need
  MUTATION TESTS, not placement faith — twice a "defensive" change was
  caught not defending (P-037 items 3 and 5).

## ★★ ✓ RESOLVED by P-038 (2026-07-02) — RESIDUE SWEEP 2 of 2: THE NAMING/PROSE ITEMS (six items; producer names off engine-emitted VALUES; zero behavior change)

- **✓ RESOLVED by P-038 (single product commit — originally `e1ddfbf`,
  AMENDED TREE-NEUTRALLY to `7b9eda7` for the missing mandated trailers
  [message-only; tree `b49c4b2d…` identical; parent `6f7fd99`]; atop
  merge base `dc921ec` = PR #18; PUSHED, NOT merged; qa GREEN + reviewer
  fix-then-pass → PASS):** the six naming/prose items are CLOSED — each
  also marked ✓ in place below: (1a) warning doctrine tags renamed off
  the producer names (`phil_ramone_vocal_centrality`→`vocal_centrality`,
  `phil_ramone_restraint`→`restraint`) — found UNPINNED and never
  emitted on any fixture (reviewer-verified live: no fixture reaches
  those warning branches — why the goldens held); a NEW synthetic pin
  binds both payloads + asserts no producer substring in any tag; (1b)
  search-mode names renamed (`halee_depth`→`spatial_depth`,
  `ramone_vocal_truth`→`vocal_truth`) — the full radius in ONE commit;
  OLD_HARDCODED_MAP kept VERBATIM as history, the coincidence pin
  consciously adjusted (`dict(OLD_HARDCODED_MAP,
  intimate_mode="vocal_truth")` — reviewer-judged honest); (1c) engine
  action prose de-producer-named ("Vocal belief:", "Naturalistic
  space:", "physical room lift", the source_auditors room line) —
  profile JSON prose KEEPS its producer names (profiles are named for
  producers; the engine is not); (2) the liveness-docstring sweep — 6
  files corrected to the empirically-true claim (liveness catches
  drop/threading; discrimination catches hardcoding —
  reviewer-validated by live sabotage on test_beat_identity), 4 files
  verified accurate and untouched; (3) cli.py `--mode` help
  de-hardcoded; (4) the count-pin parenthetical tidy (21 sites → one
  canonical explanation in conftest.py); (5) the fallback reason now
  branch-accurate (declared-default vs first-authored); (6) both
  profiles' blend-confidence reasons — the heard-qualifier appended +
  the 65.0/85.0 attribution made explicit, verbatim pins STRENGTHENED,
  the P-036 pinned-OUT assertions retained. Suite 767 → **768** (+1
  synthetic pin); regression **93/93, goldens untouched**; artifact
  deltas enumerated TO THE LINE (76 changed lines, all 1-for-1, 0
  unenumerated, 0 producer leaks); score surfaces byte-equal ×8.
  Receipt: `build-os/receipts/P-038-naming-prose-sweep.md`.

## ★★ ✓ RESOLVED by P-037 (2026-07-02) — RESIDUE SWEEP 1 of 2: THE CODE-BEHAVIOR ITEMS (six defensive/validation residue items, byte-identical on every artifact surface)

- **✓ RESOLVED by P-037 (commits `cb566b1` + review-fix `5f94456` on parent
  `4df134c`, atop merge base `dc921ec` = PR #18; PUSHED, NOT merged; qa GREEN
  + reviewer fix-then-pass → PASS):** the six code-behavior residue items are
  CLOSED — each also marked ✓ in place below: (1)
  `logic_action_generator.py:38` — identity-derived lead matching on the ONE
  shared `lead_vocal_names()` basis (zero "vocal" substring-match sites
  remain); (2) the validation-tightening cluster (`search_modes` non-empty;
  `default_creative_mode`'s three hard-dereferenced keys; `confidence_map`
  duplicate-areas + exact entry keys {area, level, reason}; non-finite floors
  rejected — loader AND raw gate); (3) the raw-gate floor self-guard (THE
  REAL FINDING — see the named lesson below); (4) `lead_names`
  identity-derived in `_vocal_role_fit` (the mangle pin consciously flipped:
  60.0 → 70.0); (5) the shared groove dict — a pristine PRE-doctrine deepcopy
  snapshot (the fix-then-pass round; mutation-test pinned load-bearing); (6)
  the JUDGMENT_WORDS "fix"-substring constraint — word-boundary +
  plural-suffix matching frees "fixture". Suite 754 → **767** (+12, +1
  mutation test); regression **93/93**; byte-identity **240/240** (proven
  twice — qa's own harness pre-fix, builder + reviewer spot-check post-fix).
  Receipt: `build-os/receipts/P-037-code-behavior-sweep.md`.
- **★★ NEW (P-037 — NAMED LESSON, standing): raw-dict NaN comparisons FAIL
  OPEN.** `confidence < nan` is False, so a NaN floor ACCEPTED every blend at
  base (and −0.5/−inf accepted everything below any threshold) — the guard
  now fails CLOSED (verified at base by builder, qa, AND reviewer
  independently). **AUDIT FUTURE RAW-COMPARISON GATES** for the same shape:
  any `x < threshold`-style gate over unvalidated dict values.
- **★★ NEW (P-037 — NAMED LESSON, standing): defense claims need MUTATION
  TESTS, not placement faith.** Twice now a "defensive" change was caught not
  defending (P-037 item 3: the raw gate that failed open; P-037 item 5: the
  groove copy that, as first shipped, ran AFTER the thing it defended
  against — the fix-then-pass round). A defensive change ships with a test
  that SIMULATES the threat and FAILS on the undefended shape.
- **Remaining open packet-worthy residue = exactly P-038's list** (residue
  sweep 2 of 2 — naming/prose, the LAST backlog packet; STAGED in
  `build-os/packets/active_packet.md`, NOT active until the orchestrator
  confirms): the three producer-named-VALUE surfaces (golden-pin caution —
  warning doctrine tags may be golden-pinned; search-mode names appear in
  emitted creative.json), the liveness-docstring sweep (~8 files), cli.py
  --mode help text, the P-035 count-pin parenthetical tidy, fallback-reason
  wording, the two P-036 observations. Then the batch merge decision
  (P-036 + P-037 + P-038) on the user's word. Other standing notes below
  remain opportunistic fold-on-next-touch items, not backlog packets.
  **✓ UPDATE (P-038 close, 2026-07-02): ✓ RESOLVED IN FULL — P-038's
  list is closed and the residue list is now ZERO; see the banner at
  the head of this file.**

## ★★ ✓ RESOLVED by P-036 (2026-07-02) — THE STALE CONFIDENCE_MAP ENTRIES (was: NEXT PACKET, NEW at P-035 close; jumped the residue queue per the reviewer's recommendation)

- **Both profiles' "limited" vocal-blend `confidence_map` entries claim a
  dormancy that is now FALSE on both halves** — P-034 delivered the
  capacity and P-035 made it LIVE on real data (the `vocal_chop_groove`
  fixture; vocal_role_fit 65.0 vs 85.0). Contained — no scorer consumes
  the map — but reputationally FIRST for a product whose brand is honest
  labeling. **Shape (the reviewer's recommended follow-up):** rewrite the
  two entries' reasons to live status + re-judge levels; consciously flip
  the verbatim map pins (TIM_AUTHORED_MAP + halee_ramone's) for exactly
  those entries; byte-identical everywhere else. Small packet. STAGED in
  `build-os/packets/active_packet.md`, NOT active until confirmed.

- **✓ RESOLVED by P-036 (2026-07-02, single commit `95de041` on the merged
  default `dc921ec` = PR #18):** both entries' `reason`s re-authored to the
  live, measured status (the either-side-forward reading; the measured
  65.0/85.0 differential; timbaland's +0.7 at its authored 0.4 weight) with
  the three real constraints stated (masker-set-bounded coverage; info tier
  emitted but unconsumed; no per-track masking risk) — every clause
  fact-checked TRUE by both gates. **Both levels honestly STAYED `limited`**
  per the closed vocabulary (`high` would overclaim for the weight-0
  reference and drop timbaland's stated constraints). The verbatim map pins
  consciously flipped (2 assertions removed / 8 added — the falsified claims
  "only against the lead" and "dormant" now asserted ABSENT); byte-identical
  everywhere except exactly the 16 confidence text surfaces (8 ×
  doctrine_score.json + 8 × mix_verdict.md, one line each); suite 754 (count
  held) + 93/93. ★ THE HONESTY LAYER IS CURRENT with P-034/P-035. Receipt:
  `build-os/receipts/P-036-confidence-map-honesty-fix.md`.

## ★ RESOLVED USER DECISION (was: "read this first")

- **Deeper creative scoring (`creative.py::_KIND_SCORES`) — RESOLVED via P-012
  (option B, penalty-only).** The user chose **option B**: a bounded, transparent,
  capped, **penalty-only** evidence-nudge layer ON TOP of the curated table (the
  `_KIND_SCORES` VALUES are UNCHANGED). Shipped — `score_variant` applies two
  evidence-gated `vocal_belief` penalties (`−8` masked vocal across
  `width_bloom`/`vocal_ride`/`intimacy_pass`; `−6` `width_crowding` for
  `width_bloom`), the summed overall delta clamped to `±2.0`, `score_nudges`
  emitted only on fire. It DELIBERATELY changes default scoring when a nudge fires
  but provably cannot overturn a clear base ranking (cap 2.0 < 2.4–4.2 base gaps).
  **NOW MERGED to default via PR #13 (merge commit `0f4e7e9`)** — the user's
  reviewed aesthetic change is live. **P-013 (tests-only) then proved the nudge
  fires on REAL DATA through the live `analyze()` path** (`dense_chorus_with_loops`
  emits a real `width_crowding` event → row-2 nudge fires; overall_score
  75.7→74.9; winner unchanged — option (a)), closing the golden-unguarded gap.
  Receipts: `build-os/receipts/P-012-creative-scoring-nudge-layer.md`,
  `build-os/receipts/P-013-nudge-visibility-fixture.md`. (Options (a) leave
  as-is and (c) fuller song-derived rescoring were NOT chosen.)

- **THE BASE-VALUE RE-CURATION LEVER IS PROBED AND THE JUDGMENT LAYER IS AT A
  DOCTRINE-HONEST EQUILIBRIUM (P-017).** The user chose "A" -- attempt the FIRST
  change to a base `_KIND_SCORES` value (re-curate `depth_cleanup` so the
  depth/hierarchy move wins the `density` branch). **FINDING: an honest re-curation
  CANNOT flip `density` -- arithmetically forced by the doctrine, verified
  adversarially. `_KIND_SCORES` LEFT UNTOUCHED (no product change).** THREE
  independent levers have now converged on the same place: penalty (P-012/P-015),
  reward/promotion (P-016), and base-value re-curation (P-017) all confirm that
  `subtractive_drop`'s default dominance is legitimate, the masked-vocal near-tie
  (P-015) and foregrounded-loop promotion (P-016) are the ONLY doctrinally-warranted
  flips, and **there is NO honest further flip move inside the current dimension
  set.** The evidence/re-curation program to make judgment decisive is essentially
  COMPLETE. The one remaining honest thread is a SYMMETRIC re-judgment (is
  `subtractive_drop` itself slightly over-valued?) -- user-gated, un-signed-off, NOT
  staged. Receipt: `build-os/receipts/P-017-doctrine-honest-kind-scores-recuration.md`.

## Deferred (follow-up packets)

- **★★ THE TIMBALAND SUB-ARC (P-032.x) IS ✓ COMPLETE (2026-07-02 — formally
  closed by P-032i, the differential proof; TEN packets: P-032e → P-032a →
  P-032b → P-032d → P-032c → P-032g → P-032f → P-031 → P-032h → P-032i)** —
  **P-032e ✓ (beat_identity —
  the front-loaded CRUX) + P-032a ✓ (negative_space) + P-032b ✓
  (groove_coherence LIVE-WIRE — the RISKIEST packet so far, triple-verified) +
  P-032d ✓ (rhythmic_surprise, weak form) + P-032c ✓ (low_end_motion — the
  low-end POCKET, dual-green vs the USER'S explicit acceptance invariant;
  reviewer AST + 20k-configuration adversarial proof) + P-032g ✓
  (loop_context + protect_iconic_loops — THE HINGE: sixth axis + the FIRST
  profile-decided creative gate, DUAL byte-identical — doctrine AND creative,
  the USER-MANDATED surface; the status→score map lives in the profile JSON —
  even the axis's polarity is profile-authored) + P-032f ✓ (vocal_role_fit +
  the NEW agnostic `vocal_type_classifier.py` + `vocal_blend_policy` — the
  LAST of the seven weight-up axes, 14th component, + the SECOND
  profile-decided gate; the USER-GATED packet, cleared: Decision 1 = B +
  Decision 2 = conservative default + explicit confidence floor;
  misclassification fails CLOSED; DUAL byte-identical — doctrine AND
  creative; ALL SIX user-mandated adversarial attacks defeated by BOTH gates
  independently) LANDED — THE MEASUREMENT PHASE OF THE SUB-ARC IS
  COMPLETE.** All seven add a
  new producer-agnostic doctrine axis weight-0 for halee_ramone →
  byte-identical, proving the P-029 architecture is EXTENSIBLE. **The engine
  now carries 14 component axes** (7 original + beat_identity + negative_space
  + groove_coherence + rhythmic_surprise + low_end_motion + loop_context +
  vocal_role_fit) —
  ALL 7 of the 7 Timbaland "weight up" axes landed, all
  append-last/weight-0/profile-sourced, zero plumbing debt; the onset/IOI
  signal is LIVE at doctrine time (`analyze_groove` relocated BEFORE
  `score_doctrine`, computed exactly ONCE, same object reused in
  `expanded["groove"]`); the reusable profile-decided-creative-gate pattern is
  established AND now REUSED (P-032g → P-032f; P-032h authors BOTH flags —
  `protect_iconic_loops` AND `vocal_blend_policy`, REQUIRED). Receipts:
  `build-os/receipts/P-032e-beat-identity.md`,
  `build-os/receipts/P-032a-negative-space.md`,
  `build-os/receipts/P-032b-groove-coherence-livewire.md`,
  `build-os/receipts/P-032d-rhythmic-surprise.md`,
  `build-os/receipts/P-032c-low-end-motion.md`,
  `build-os/receipts/P-032g-loop-context-hinge.md`,
  `build-os/receipts/P-032f-vocal-role-blend-policy.md`,
  `build-os/receipts/P-031-confidence-framework.md`,
  `build-os/receipts/P-032h-author-timbaland-json.md`,
  `build-os/receipts/P-032i-differential-proof.md`.
  **Carry-forwards — NOW THE POST-SUB-ARC BACKLOG (the sub-arc is ✓
  COMPLETE; every item below is future-packet backlog, none active, no
  order dependency):**
  - **★ ORDER — ✓ ALL TEN CLOSED (final at P-032i close):**
    **P-032d ✓ → P-032c ✓ → P-032g ✓ → P-032f ✓ → P-031 ✓ → P-032h ✓ (AUTHOR
    `timbaland.json` — THE PAYOFF PACKET, DONE: the second live producer
    profile, the FIRST non-byte-identical output of the epic — same stems,
    two judgments: 68.4 / 52.6 / 49.7 vs 73.8 / 70.7 / 74.3, fully
    attributable [zero component divergence on simple; exactly
    `loop_context_score` 15.0→10.0 on the loop fixtures; the rest pure
    reweighting]; BOTH gates + the 11-entry confidence_map declared in
    writing, TIM_AUTHORED_MAP verbatim-pinned; ZERO RELAXATION adversarially
    verified; default path moved ZERO bytes; single commit `70a0b69`, 2 NEW
    files, zero engine code, pushed NOT merged — receipt
    `build-os/receipts/P-032h-author-timbaland-json.md`)** →
    **P-032i ✓ (the Timbaland-vs-Halee/Ramone DIFFERENTIAL PROOF — DONE
    2026-07-02, the formal close of the sub-arc):** same stems, both profiles — prove (a)
    recognizably-different-but-COHERENT judgment AND plan surfaces (doctrine
    + creative + the mix_plan/checklist/verdict artifacts, not just scores),
    (b) full component-level attributability, (c) safety invariance
    (kill-switches, risk classes, non-destructive, masked-lead) across both,
    (d) the binding expectations — deltas from
    groove/space/low-end/loop/surprise; NO vocal-blend delta (the inert
    corollary below); NO intimate-mode-selection claim (the
    `default_creative_mode` inertness finding — ✓ since RESOLVED by P-033,
    the pin flipped via its designed conscious-edit path), (e) the
    confidence
    maps render correctly per-profile; byte-identical discipline for the
    reference throughout — ALL PROVEN AND LANDED as the permanent 21-test
    `tests/test_differential_proof.py` (single commit `010734d`, 772+/0−,
    ZERO product code, pushed NOT merged); qa 639 → **660** + 68/68,
    obligations (a)–(e) re-derived independently LIVE (60/60 checks),
    proof-liveness sabotage bites (a SAFETY-switch reorder fails the
    verbatim pin); reviewer PASS (no must-fix). Receipt:
    `build-os/receipts/P-032i-differential-proof.md`. P-030 (rename dims —
    now touches TWO producer JSONs + `tests/test_differential_proof.py`,
    still orthogonal, slightly wider) moves to the post-sub-arc backlog.
  - **★ P-032g STAGING NOTES — ✓ DISCHARGED IN FULL (P-032g close):** the
    USER-MANDATED dual byte-identity surface was PROVEN — (a) doctrine 0
    mismatches × 3 fixtures AND (b) creative full `result.creative` sorted-key
    JSON base vs HEAD → EMPTY diff / `cmp` byte-identical; engine language
    OBSERVATIONAL (zero judgment words across all 7 reachable statuses);
    `protect_iconic_loops` is a REQUIRED profile field with halee_ramone=false
    = current behavior; the `_halee` loop_foregrounded coefficient UNTOUCHED
    (=6, promotion table verbatim, `test_packet_cautions_untouched`); iconic
    structurally cannot override a masked lead (the Ramone gate fires FIRST).
  - **★ P-032f STAGING NOTES — ✓ DISCHARGED IN FULL (P-032f close):** the
    user gate was presented and CLEARED (Decision 1 = B — acceptable blend,
    profile-gated only, via the REQUIRED `vocal_blend_policy` field;
    Decision 2 = conservative default + explicit confidence threshold). The
    rule table landed VERBATIM (lead or uncertain → protect clarity;
    hook_candidate → protect unless profile-authored LATER; chop/stack +
    opt-in + confidence ≥ floor → blend may apply); misclassification fails
    CLOSED (MIN_STRENGTH 0.6 + top-two tie → uncertain → protect-as-lead).
    NEW `vocal_type_classifier.py` (`role_classifier.py` untouched in place);
    additive record fields; hook capped at `vocal_hook_candidate`; the 3
    interacting live scorers (`_ramone` / `_vocal_centrality` /
    `_static_mix`) proven byte-identical for halee_ramone (flag-lever delta =
    exactly `masked_penalty`). The reusable P-032g gate pattern was REUSED as
    designed.
  - **★ SCOPING-WORKFLOW FINDINGS for the remaining axes (evidence-backed):**
    P-032c ✓ CONFIRMED in practice (ZERO new plumbing; kick/sub temporal
    interlock + low-end motif + per-section true-sub movement landed as
    DEFERRED honest docstring boundaries; physics primary — `identity_family`
    a corroborating tie-break only, `instrument_identity` never read);
    P-032g ✓ CONFIRMED in practice (the `creative.py` gate defaults to
    current behavior — halee_ramone declares protect_iconic_loops=false and
    the promotion fires exactly as today — and the creative-scores
    byte-identity surface was proven EMPTY-diff/`cmp`-identical;
    cultural/recognizability iconic-ness + per-loop bar-level variation +
    onset-sequence needs landed as DEFERRED honest boundaries, test-guarded
    out of evidence); P-032f ✓ CONFIRMED in practice (NEW
    `vocal_type_classifier.py`, `role_classifier.py` untouched in place;
    additive record fields; capped at `hook_candidate`; protect-as-lead when
    uncertain — fail-closed at MIN_STRENGTH 0.6 + top-two tie; the blend gate
    unreachable under halee_ramone defaults; the inert-on-real-data corollary
    recorded below).
  - **★ NEW (P-032b adversarial skeptic — cosmetic): shared mutable groove
    dict.** `result.expanded["groove"]` IS the same dict passed to
    `score_doctrine` (shared mutable state); nothing mutates it today
    (deepcopy-proven), but a FUTURE doctrine change mutating its `groove` arg
    would silently corrupt the expanded artifact. Consider a defensive copy or
    a read-only test pin in a future doctrine-touching packet.
    **✓ RESOLVED by P-037 (2026-07-02, the fix-then-pass round):**
    `expanded["groove"]` is now a pristine deepcopy SNAPSHOT taken
    BEFORE `score_doctrine` runs (the copy as FIRST shipped ran after
    doctrine and could not deliver the defense — the reviewer's
    must-fix); a mutation test simulating exactly this threat FAILS
    under the old placement (the artifact inherits −999.0) and passes
    at HEAD; `analyze_groove` still runs exactly once.
  - **★ NEW (P-032d reviewer — cosmetic): non-adjacent swing under a missing
    middle metric.** In `_rhythmic_surprise`, None-filtering happens BEFORE the
    adjacency zip, so a missing middle `transient_density` would make the
    "largest adjacent swing" compute across NON-adjacent sections.
    Defensive-only — the pipeline always emits the metric — same
    future-doctrine-packet ride-along as the docstring sweep below.
  - **★ NEW (P-032c — cosmetic ride-alongs):** (1) `_low_end_motion`'s
    theoretical score ceiling is **84** (40 baseline + 20 reserved bonus + 24
    headroom), never 100 — fine by design, but RELEVANT when authoring
    `timbaland.json` weights (P-032h). (2) the defensive `r.get("metrics",{})`
    None edge in the scorer — defensive-only; same future-doctrine-packet
    ride-along.
  - **★ NEW (P-032g — cosmetic ride-alongs):** (1) the creative gate keys on
    the literal promotion kind `"loop_deconstruct"` (`creative.py:232`) — if
    promotion kinds ever generalize, move the gating into the table row; (2)
    the `dominant_unassessed` docstring is slightly loose (per-metric, not
    per-section); (3) `read_loop_context` shares the defensive None-value edge
    family. All defensive/cosmetic — same future-doctrine-packet ride-along
    bucket.
  - **★★ NEW (P-032f reviewer COROLLARY — an HONEST BOUNDARY, not a defect;
    BINDING on P-032h/P-032i expectations):** the blend gate is INERT on real
    pipeline data — today's masking analyzer emits vocal-band `bad_masking`
    ONLY via `_vocal_conflict`, whose elements are always [lead, other], so
    the new axis is the ONLY surface where non-lead vocal masking manifests
    and the gate is exercised only via SYNTHETIC events. **Flipping
    Timbaland's `acceptable_blend` will produce ZERO real-data delta through
    this axis on current fixtures — P-032i's differential proof must NOT
    expect a vocal-blend delta** (the Timbaland delta comes from the other
    axes). A future ANALYZER-EXTENSION packet could emit non-lead vocal-band
    events to make the gate live on real data — when that packet opens, note
    that `creative.py:98`'s name-based "vocal" match is a LATENT MISFIRE
    RISK there. **★ UPDATE (P-034 close, 2026-07-02): the
    analyzer-extension capacity is HALF delivered — P-034 emits non-lead
    vocal-band events under the NEW classification `vocal_band_masking`
    (consumed ONLY by the vocal-role surface) and FIXED creative.py:98's
    latent misfire risk (identity-derived lead names), but all 3 current
    fixtures have no non-lead vocal stems, so the gate is STILL
    fixture-inert on real data — the LIVE half (the 4th fixture + the
    real-data blend differential) belongs to P-035, which carries a BINDING
    reviewer fixture-design advisory: the fixture MUST include at least one
    forward/heard masker-set member (synth/keys/guitar) with vocal-presence
    overlap ≥ 0.1 against the chop/stack, or the differential stays
    dormant.** **★★ UPDATE (P-035 close, 2026-07-02): ✓ FULLY RESOLVED —
    the corollary's whole chain is closed: policy (P-032f, dormant) →
    capacity (P-034, inert) → LIVE, MEASURED, ATTRIBUTABLE (P-035). The
    4th fixture `vocal_chop_groove` honors the binding advisory (guitar
    masker; overlaps 0.2191/0.1655 ≥ 0.1); the blend gate finally differs
    on real data — vocal_role_fit 65.0 vs 85.0, overalls 76.3 vs 60.9,
    the gate worth exactly +0.7 at tim's authored 0.4 weight. Receipt:
    `build-os/receipts/P-035-vocal-chop-groove-differential.md`.**
  - **★ NEW (P-032f — cosmetic ride-alongs):** (1) NaN-floor self-guard — add
    `0.0 <= floor <= 1.0` (qa suggested `math.isfinite`) in the raw
    `accepted_blend_under_policy` gate (the loader validates; the raw gate
    trusts its caller); (2) `lead_names` in `_vocal_role_fit` derives from
    `vocal_type` rather than `instrument_identity` — identity-derived would
    be sturdier; (3) `_validate` accepts EXTRA keys inside
    `vocal_blend_policy` (only the two required keys are checked); (4) the
    `_vocal_role_fit` score ceiling is **85**, never 100 — joins lem's 84 as
    a `timbaland.json` weight-authoring consideration (P-032h). All
    defensive/cosmetic — same future-doctrine-packet ride-along bucket.
    **✓ UPDATE (P-037 close, 2026-07-02): (1) ✓ RESOLVED — the raw-gate
    self-guard landed AND exposed THE REAL FINDING (NaN floors FAILED
    OPEN at base — `confidence < nan` is False; now fails CLOSED, plus
    negative/−inf floors refused); (2) ✓ RESOLVED — `lead_names`
    identity-derived, the hand-mangle pathway consciously pinned to the
    sturdier behavior (60.0 → 70.0); (4) was consumed by P-032h's
    weight authoring; (3) — extra keys inside `vocal_blend_policy` —
    remains an opportunistic fold-on-next-touch note (NOT in P-038's
    list).**
  - **★ NEW (P-031 reviewer — judgment notes, non-blocking):**
    `confidence_map` validation accepts DUPLICATE `area` values and EXTRA
    keys inside entries (only area/level/reason are checked) — the verbatim
    pins catch this for AUTHORED profiles, so P-032h should verbatim-pin
    `timbaland.json`'s map exactly like halee_ramone's; consider tightening
    (uniqueness + entry key-set check) in a future validation packet.
    **✓ RESOLVED by P-037 (2026-07-02): `_validate` now rejects
    duplicate `area` strings and enforces the exact entry key set
    {area, level, reason}.**
  - **★ NEW (P-031 — process precedent, standing):** the fix-then-pass
    conscious-edit path through a verbatim pin WORKS AS DESIGNED (`b869ebd`:
    the reviewer's fact-check caught ONE inexact reason — per-section
    true-sub belongs to the band-resolution boundary, not onset timing; the
    fix edited the profile AND mirrored the pin in the same commit; counts
    identical; the pins came out STRONGER — five deferred entries
    verbatim-pinned vs four). Record this as the STANDARD route for
    pin-guarded content changes.
  - **✓ RESOLVED by P-033 (2026-07-02) — (was: ★★ P-032h reviewer
    TRAJECTORY FINDING, P-016-family): `default_creative_mode` was
    pipeline-INERT.** `pipeline._default_creative_mode` hardcoded the
    REFERENCE's mode names, so timbaland's authored `intimate_mode:
    "conservative"` was UNREACHABLE (intimate material under timbaland
    silently fell back to `dramatic_contrast`), and the hardcoded fallback
    risked a KeyError for a profile lacking that mode name. **P-033 wired
    the table to the PASSED profile (byte-identical for the reference),
    made the fallback profile-owned (declared default_mode if present in
    search_modes, else the first authored mode) with a conditional
    `search_mode_fallback` evidence key, and flipped the P-032i negative
    pin through its designed conscious-edit path (STRENGTHENED). Timbaland's
    authored intimate mode is now REACHABLE: `conservative` on
    `simple_vocal_piano_song`.** Receipt:
    `build-os/receipts/P-033-default-creative-mode-wiring.md`.
  - **✓ DISCHARGED by P-030 (2026-07-02) — (was: ★ NEW P-032h — scope
    note):** P-030 (rename the halee/ramone dims off the producer names)
    touches TWO producer JSONs (`halee_ramone.json` + `timbaland.json`) —
    it DID (both JSONs migrated in Commit-1 `21c0ab0`).
  - **✓ DISCHARGED by P-030 (2026-07-02) — (was: ★ NEW P-032i reviewer —
    scope note):** P-030's expected-touch list also includes
    `tests/test_differential_proof.py` — it DID (migrated in Commit-2
    `0c7885e`, among the 26 updated test files).
  - **★ NEW (P-032i — cosmetic):** two truthiness asserts in
    `tests/test_differential_proof.py` (`v["risk"] and v["validation"]`;
    `0 <= len(nxt)`) — tighten opportunistically on the next touch of that
    file.
  - **★ NEW (P-032i — cosmetic):** the `tim_analyzed` fixture duplicates
    `test_timbaland_profile`'s module fixture (~3 extra analyses per full
    run) — promote to a session conftest fixture ONLY if a third consumer
    appears.
  - **★ NEW (P-032i builder observation — cosmetic, reported NOT patched
    per the mandated stop-and-report behavior):** the verdict filename is
    producer-independent — the legitimizing change is a future
    verdict-filename cosmetic packet.
  - **★ NEW (P-033 reviewer — validation gaps, → the future
    validation-sweep packet):** `_validate` lacks (a) a NON-EMPTY check on
    `search_modes` — a zero-mode profile would StopIteration in the
    first-authored-mode fallback (NARROWED vs pre-P-033, where ANY profile
    lacking `dramatic_contrast` crashed with KeyError; not a regression) —
    and (b) structural checks on `default_creative_mode`'s three keys
    (intimate/dense/default), which the pipeline now hard-dereferences.
    Both to the future validation-sweep packet.
    **✓ RESOLVED by P-037 (2026-07-02): (a) `search_modes` must be a
    non-empty object; (b) `default_creative_mode`'s three
    hard-dereferenced keys checked with sane types. Both shipped
    profiles still load; 14/14 malformed-shape probes → ValueError.**
  - **★ NEW (P-033 — cosmetic):** `cli.py:446-447` `--mode` help text
    hardcodes the REFERENCE's mode names (pre-existing; will go stale as
    profiles diverge) — ties to the unstaged CLI-producer-exposure backlog.
    **✓ RESOLVED by P-038 (2026-07-02): the help text now describes the
    semantics (a mode from the selected profile's `search_modes`;
    profile-owned default) instead of hardcoding the reference's mode
    names. (The CLI-producer-exposure backlog itself remains an
    unstaged, user-initiated option.)**
  - **★ NEW (P-033 — cosmetic):** the fallback `reason` wording says "the
    profile's own default" even on the first-authored-mode branch — tighten
    on the next touch of that code.
    **✓ RESOLVED by P-038 (2026-07-02): the reason now states WHICH
    resolution branch fired (declared default vs first authored mode) —
    the discriminator pre-existing and exact, AST-verified no new
    logic.**
  - **★★ NEW (P-033 reviewer CALIBRATION — record for future arc
    language):** the creative-mode lever is real but THIN — `search_mode`
    steers the reported mode/bias surface; `generate_variants` does NOT yet
    fork on it. P-033 makes the authored mode REACHABLE and VISIBLE; a
    future packet would make modes reshape variant generation/scoring. Do
    NOT over-claim behavioral steering.
    **✓ RESOLVED by P-042 (2026-07-03): `generate_variants` now READS
    the active mode and FORKS candidate generation via profile-authored
    `search_modes` declarations (`suppress_kinds` = candidate-SET fork,
    `favor_kinds` = order-only reach, absent = byte-identical neutral;
    caps bind at loader AND runtime) — the mode lever is LOAD-BEARING;
    behavioral steering may now be claimed.**
  - **★★ NEW (P-030 reviewer JUDGMENT CALL — residue-sweep candidates,
    explicitly NOT contract keys):** three producer-named-VALUE surfaces
    survive the migration — (1) the search-mode NAMES
    (`halee_depth`/`ramone_vocal_truth`), profile-internal vocabulary that
    appears in emitted creative.json as VALUES; (2) the engine action prose
    ("Halee naturalism…"/"Ramone-style…"); (3) the warning doctrine tags
    (`phil_ramone_vocal_centrality`/`phil_ramone_restraint`) emitted as
    values. Ruled in-scope-as-built (the user's rule bans old-KEY aliases;
    mode names are values; profile vocabulary is protected) — route to the
    residue sweeps.
    **✓ RESOLVED by P-038 (2026-07-02): all three surfaces
    de-producer-named — the warning doctrine tags renamed
    (`vocal_centrality` / `restraint`, + the NEW synthetic pin), the
    search-mode names renamed (`spatial_depth` / `vocal_truth`, full
    radius in one commit), the engine action prose neutralized; profile
    JSON prose consciously KEEPS its producer names (profiles are named
    for producers; the engine is not).**
  - **★ NEW (P-030 qa — cosmetic, self-healing):** stale gitignored .pyc
    caches observed during the qa run — no action needed; they regenerate.
  - **★ NEW (P-034 — residue-sweep candidate, same family as the
    FIXED creative.py:98):** `logic_action_generator.py:38` uses a
    name-based "vocal" substring match — gated behind `bad_masking`, so
    UNREACHABLE by the new `vocal_band_masking` classification today; joins
    the residue-sweep list (reported out-of-scope by the builder, the
    mandated stop-and-report behavior).
    **✓ RESOLVED by P-037 (2026-07-02): identity-derived lead matching,
    consolidated with creative onto the ONE shared `lead_vocal_names()`
    basis (vocal_type_classifier) — zero name-based "vocal"
    substring-match sites remain.**
  - **★ NEW (P-034 — the three deferrals, each pinned in-code as a
    named conscious-extension point; P-035 OWNS the revisits):** (1)
    forward-only emission — the buried-vocal reading deferred to the
    fixture that makes it real; (2) no `per_track_masking_risk`
    contribution from the new classification (risk feeds track_analysis,
    consumed broadly — revisit consciously); (3) the
    `severity != "info"` consumption filter in `_vocal_role_fit` —
    re-examine against real data. **✓ ALL THREE DECIDED by P-035
    (2026-07-02), against the real data and pinned: (1) the buried-vocal
    reading FLIPPED (Commit-1 `0b940c7` — either-side-forward; the
    moderate tier was structurally unreachable under stem-forward-only);
    (2) the risk-exclusion KEPT (4 real events, all risks 0.0); (3) the
    info-filter KEPT (the chorus infos are the lead-acceptable
    controlled-overlap shape; consuming them would protect non-lead
    vocals STRICTER than the lead — consumption-invariance pinned).**
  - **★ NEW (P-034 — cosmetic, deliberate):** the P-032i pin's
    docstring line is now capacity-STALE (the analyzer CAN emit non-lead
    vocal-band events; the current fixtures just never trigger it) —
    left VERBATIM; the revisit belongs to P-035's conscious pin flip.
    **✓ DISCHARGED by P-035 (2026-07-02) — the pin flipped exactly as
    its docstring pre-registered: the no-delta guard RETAINED on the
    original 3; the 65-vs-85 delta pinned on the 4th.**
  - **★ NEW (P-035 — convention note, standing):** FIXTURE_NAMES /
    EXPECTED_SNAPSHOT and every pinned-value suite are PINNED-TO-3 by
    conscious decision (reviewer-endorsed: scope-explosion avoidance;
    nothing load-bearing runs only via the shared parametrization — the
    4th fixture's snapshot, component picture and divergence audit live
    in `tests/test_vocal_chop_groove.py`). **Every future fixture needs
    its own file or a conscious re-parametrization** — never silently
    widen the shared parametrization.
  - **★ NEW (P-035 — cosmetic):** the mechanically-repeated "(P-035
    moved the corpus count consciously…)" parenthetical appears ~15×
    across 10 files (the count-pin updates) — a future tidy pass; fold
    into a doctrine/test-touching packet.
    **✓ RESOLVED by P-038 (2026-07-02): 21 sites shortened to a pointer;
    the ONE canonical explanation lives in `conftest.py`.**
  - **★ NEW (P-036 reviewer — cosmetic, observation A):** the re-authored
    reasons' "either side of the pair is forward" elides the masker-arm's
    `heard` qualifier — repo-canonical shorthand (the analyzer doc's own
    headline); a future tidy could append "…or a heard masker stands
    forward" — PAIR with the analyzer doc line if ever tidied.
    **✓ RESOLVED by P-038 (2026-07-02): the heard-qualifier appended,
    PAIRED with the masking_analyzer doc headline exactly as specified;
    verbatim map pins strengthened in the same commit (the P-036
    conscious-edit path).**
  - **★ NEW (P-036 reviewer — cosmetic, observation B):** the 65.0
    attribution in the re-authored reasons is elliptical (the chop AND the
    stack are each penalized once) but numerically EXACT — tidy only if the
    entry is ever re-authored again.
    **✓ RESOLVED by P-038 (2026-07-02): the entry WAS re-authored
    (observation A), so the tidy fired — the 65.0/85.0 attribution made
    explicit (the chop and the stack each draw the masked penalty once;
    the accepted blend waives both).**
  - **★ NEW (P-036 — residue-sweep candidate):** JUDGMENT_WORDS
    substring-matches "fix", so "fixture" is UNUSABLE in profile prose
    ("real exported-stem data" used instead — accurate; the reviewer
    confirmed the dodge did not bend the truth). Word-boundary matching
    would free the vocabulary — fold into a validation/sweep packet.
    **✓ RESOLVED by P-037 (2026-07-02): word-boundary + plural-suffix
    matching (regex `\b{w}(?:e?s)?\b`) via the shared
    `judgment_word_hits` helper; 9–10 guard sites migrated onto it;
    "fixture" freed, "fix"/"fixes"/"problems" still caught; other
    inflections consciously OUTSIDE the closed vocabulary — extend
    explicitly, never stem-guess.**
  - **★ LIVENESS-DOCSTRING OVERCLAIM (non-blocking — reviewer; NOW
    POTENTIALLY AN EIGHT-FILE FAMILY, fold ONE sweep):** the `liveness` test docstrings OVERCLAIM — a
    general hardcoded-constant sabotage is actually caught by the
    *discrimination* tests, not the liveness tests themselves (the direction
    test reads the score from the SAME reference dict a constant poisons; a
    hardcoded constant still moves the mean directionally). Known instances:
    `tests/test_negative_space.py` (~lines 536-540, 553-557, from P-032a);
    `tests/test_beat_identity.py` (same imprecision); **NEW from P-032d:**
    `tests/test_rhythmic_surprise.py::test_liveness_direction_tracks_the_rhythmic_surprise_score`;
    **NEW from P-032c:** `tests/test_low_end_motion.py:518-526`; **NEW from
    P-032g:** `tests/test_loop_context.py:566-570` — and CHECK
    `tests/test_groove_coherence.py` PLUS the two NEW P-032f files
    (`tests/test_vocal_type.py`, `tests/test_vocal_blend_policy.py`) AND the
    NEW P-031 file (`tests/test_confidence_map.py`) AND the NEW P-032h file
    (`tests/test_timbaland_profile.py`) for the
    same pattern when folding the fix. **Cosmetic only** (the guard SET as a whole is sound) —
    fold ONE docstring sweep across ALL affected files (up to eight) into a
    future doctrine-touching packet.
    **✓ RESOLVED by P-038 (2026-07-02): the ONE sweep landed — 6 files
    corrected to the empirically-true claim (liveness catches
    drop/threading sabotage; a hardcoded constant is caught by the
    value-discrimination guards — reviewer-validated by live sabotage on
    `test_beat_identity`); the remaining 4 candidate files checked and
    VERIFIED ACCURATE, untouched. The whole family is now corrected or
    verified-accurate.**
  - **★ DOCSTRING DRIFT (non-blocking, from P-032e):** `_beat_identity`'s docstring
    says candidacy is "optionally corroborated by crest/spectral_flatness" but the
    body reads only `crest_factor_db`, never `spectral_flatness`. The spec made
    flatness OPTIONAL, so this is HARMLESS — **fold a one-line docstring fix into a
    future doctrine-touching packet** rather than spending a commit now. Not a bug.
  - **★ HONEST DEFERRALS baked into the sub-arc (documented in-code as P-014-style
    boundaries, NOT faked — do NOT let a later packet quietly claim them):** from
    P-032e — (1) fingerprint TYPING (mouth-sound/tabla/synth-knock), not measurable
    on exported stems; (2) onset REGULARITY / IOI — **✓ RESOLVED by P-032b** (the
    groove live-wire landed; the signal now reaches doctrine via
    `groove_coherence`); (3) "more undeniable after a move" — needs a before/after
    render, plan-only v1 out of scope. From P-032a — sample-level **inter-onset
    silence gaps**: the groove object is now visible at doctrine time (P-032b),
    but `negative_space` itself still works at the section-aggregate grain only.
    From P-032g — cultural/recognizability iconic-ness (needs
    provenance/manifest — the acoustic proxy is what ships); per-loop
    bar-level variation; onset-sequence needs — all test-guarded out of
    evidence.

- **★★ THE ACTIVE ROADMAP IS THE PRODUCER-AGNOSTIC EPIC — P-025 ✓ (foundation) +
  P-026 ✓ (creative sourced) + P-027 ✓ (governance sourced + WIDENED) + P-028 ✓
  (doctrine sourced + WIDENED — the EXTRACTION PHASE is COMPLETE) + P-029 ✓
  (THE PIVOT — `analyze(producer=…)` selects the profile; it is now a LIVE,
  SELECTABLE LEVER end-to-end; architecture complete & validated).** Make the
  engine select any producer's judgment as a
  swappable `ProducerProfile` (the physics stays fixed). **P-025 ✓** extracted
  today's 100%-hardcoded Halee/Ramone judgment into a frozen `ProducerProfile` + a
  pure `load_profile()` + the VERBATIM `halee_ramone.json` reference, byte-identical
  round-trip-guarded, honesty-metadata-stamped, **COMPLETELY UNWIRED**. **P-026 ✓**
  made `creative.py` the FIRST consumer: it now SOURCES its 8 producer-specific
  globals (`_KIND_SCORES`, `_NUDGE_TABLE`, `_PROMOTION_TABLE`, `CREATIVE_NUDGE_CAP`,
  `CREATIVE_PROMOTION_CAP`, `_RISK_PENALTY`, `SEARCH_MODES`, `PHILOSOPHY`) FROM
  `load_profile("halee_ramone")` — the hardcoded literals DELETED, so
  `halee_ramone.json` is now their single source of truth. Byte-identical (the
  P-012/13/15/16 creative tests pass UNEDITED, 69 combined; regression 68/68
  UNCHANGED), no-aliasing-proven (copy-before-mutate; profile byte-unchanged after a
  nudge + promotion fire). Single commit `c4a092d`; suite 319 → 331 (+12). **P-027 ✓**
  sourced `governance.py` from the profile (`_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS` /
  `TASTE_MAX_DELTA` + the 4 AESTHETIC kill-switches) AND WIDENED the profile
  (Finding A) with `taste_triangle` (`intimate_width_penalty: 30` + `emotion_dims`) +
  `veto_thresholds` (`reject_below: 45` / `align_veto_below: 50` / `align_fallback:
  75`), now sourced too. The 5 SAFETY kill-switches STAY hardcoded
  (`_SAFETY_KILL_SWITCHES`) — producer-AGNOSTIC. Byte-identical (existing
  governance/taste tests pass UNEDITED; emotion-blend round() proven byte-identical
  across all 1,030,301 integer triples; regression 68/68 UNCHANGED), no-aliasing
  DISCHARGED (mutation local-only; shared profile byte-unchanged). Two commits
  `e4786ca` (green in isolation = 343) + `7b1c26d`; suite 331 → 351 (+20). **P-028 ✓**
  sourced `doctrine_engine.py` from the profile (all 8 scorers: Part A the
  P-025-captured `weights` + `_halee`/`_ramone` baselines/coeffs; Part B WIDENED the
  profile with `doctrine.scorers` — 5 function groups — and sourced them) while the
  PHYSICS/measurement code + presentation thresholds (`stereo_width > 0.6`,
  `distinct <= 1`, `score < 55`) STAY hardcoded (producer-AGNOSTIC). Byte-identical
  (existing doctrine tests UNEDITED; regression 68/68 UNCHANGED; reviewer confirmed
  live `doctrine_score` byte-matches the golden on all 3 fixtures incl.
  `overall_mix_readiness_score`), round-trip NON-VACUOUS (18→17 flip fails +
  shifts `_section_contrast` 64→66), no-aliasing DISCHARGED. Two commits `29b9dfe`
  (green in isolation = 364) + `72e98a7`; suite 351 → 370 (+19). **P-028 COMPLETES the
  EXTRACTION PHASE — the whole judgment layer is now profile-driven, byte-identical,
  physics chassis separate.** Receipts:
  `build-os/receipts/P-025-producer-profile-schema-loader-halee-ramone-extraction.md`,
  `build-os/receipts/P-026-creative-sources-values-from-reference-profile.md`,
  `build-os/receipts/P-027-governance-sources-values-from-reference-profile.md`,
  `build-os/receipts/P-028-doctrine-sources-values-from-reference-profile.md`.
  **The epic arc (next steps):**
  - **P-027 — governance extraction (WIDENED per Finding A + ALIASING-PROOF) — ✓
    DONE.** `governance.py` sources `_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS` /
    `TASTE_MAX_DELTA` + the 4 AESTHETIC kill-switches from the profile; the profile
    widened with `taste_triangle` + `veto_thresholds`, now sourced; the 5 SAFETY
    kill-switches STAY hardcoded (producer-agnostic). Aliasing-proof DISCHARGED.
  - **P-028 — doctrine extraction (WIDENED per Finding A + ALIASING-PROOF) — ✓
    DONE.** `doctrine_engine.py` sources ALL 8 scorers' aesthetic constants from the
    profile — Part A the P-025-captured `weights` + `_halee`/`_ramone` baselines
    (86.0) + penalty coeffs; Part B WIDENED the profile with a `doctrine.scorers`
    group (5 function groups: `_vocal_centrality` / `_depth_hierarchy` /
    `_section_contrast` / `_static_mix` / `_dynamic_mix`) captured VERBATIM and
    sourced. The PHYSICS/measurement code + presentation thresholds STAY hardcoded.
    Byte-identical (regression 68/68 UNCHANGED + `doctrine_score` byte-match),
    round-trip non-vacuous, aliasing-proof DISCHARGED. **Extraction phase COMPLETE.**
  - **P-029 — parameterize the pipeline by a per-call producer (THE PIVOT) — ✓ DONE.**
    `pipeline.analyze(..., producer="halee_ramone")` accepts a NAME or a
    `ProducerProfile` object (isinstance dispatch), loads ONCE per call, and threads
    `profile=` to `score_doctrine` / `run_creative_engine` / `run_governance`, which
    thread it to ALL leaf scorers; each reads its producer-specific values from the
    PASSED profile, defaulting to `_DEFAULT_PROFILE` when `None`. KILL_SWITCHES
    recomposed per call = 5 hardcoded SAFETY + profile aesthetic (a producer can never
    drop a safety guarantee). Byte-identical default (reviewer independently
    byte-diffed all 3 layers × 3 fixtures → IDENTICAL; regression 68/68 UNCHANGED);
    selection GENUINELY LIVE + load-bearing across doctrine (baseline −20 → halee_score
    delta 20), creative (kind_score boost → overall 100), governance
    (truth_alignment 88→60 → governed 60), all through the REAL analyze() path, proven
    both ways (sabotage fails the liveness test while byte-identical stays green — the
    P-016 lesson). Two commits `42d6ebd` (green in isolation = 383) + `ea1aaa9`; suite
    370 → 384 (+14). Codex NOT available — single-reviewer. **P-029 does NOT remove the
    `_DEFAULT_PROFILE` singleton** — it stays as the `None`-default fallback in all 3
    modules, so the per-module aliasing discipline still carries on the default path
    (carry-forward for P-032). Receipt:
    `build-os/receipts/P-029-parameterize-pipeline-by-per-call-producer-profile.md`.
  - **P-030 — rename the `halee` / `ramone` dimension names off the producer
    names: ✓ RESOLVED (2026-07-02 — the artifact-contract migration).** The
    long-standing "rename dims before a second producer" caution (kept
    verbatim since P-025 per the byte-identical-first decision) is PAID —
    done AFTER, not before, per that strategy, and the migration proved
    clean: `halee_score` → `physical_space_score`, `ramone_score` →
    `emotional_hierarchy_score`, internal/evidence/profile keys renamed,
    `halee_ramone_mix_verdict.md` → `mix_verdict.md`; clean break, NO
    emitted aliases, memory.py read-only dual-read the only carve-out; all
    90 numeric values identical under both producers; suite 705 / 68/68 vs
    the regenerated goldens. Receipt:
    `build-os/receipts/P-030-artifact-contract-migration.md`.
  - **P-031 — confidence framework: ✓ DONE (2026-07-02; scope USER-UPGRADED
    to PER-AREA at P-032f close):** the REQUIRED `confidence_map` (area /
    level ∈ {high, limited, deferred} / reason) is structurally validated (no
    silent defaults), authored for halee_ramone (8 entries: 2 high / 1
    limited / 5 deferred; verbatim-pinned; machine-checked against the
    weights), and rendered per-call (additive `confidence` key in
    doctrine_score + the verdict "## Confidence" section). The P-025 metadata
    stamp stays as the global complement. Receipt:
    `build-os/receipts/P-031-confidence-framework.md`.
  - **P-032 — second producer: ✓ PROFILE LANDED (P-032h, 2026-07-02).**
    `timbaland.json` is live — the first test of true producer-agnosticism
    PASSED at the profile level (different / fully attributable /
    safety-invariant; honesty policy obeyed: hand-curated-documented →
    HIGH, reviewer-ENDORSED). The REMAINING step is P-032i (the formal
    differential proof). Receipt:
    `build-os/receipts/P-032h-author-timbaland-json.md`.
  - **P-033 — expose producer selection** (the user-facing selection surface).
    **[NUMBERING SUPERSEDED (2026-07-02): the id P-033 was RE-USED for the
    confirmed-and-now-✓-CLOSED `_default_creative_mode` wiring packet
    (receipt: `build-os/receipts/P-033-default-creative-mode-wiring.md`).
    Selection is already LIVE via `analyze(producer=…)`; any CLI exposure
    remains UNSTAGED backlog (ties to the cli.py `--mode` help-text
    residue above).]**

- **★ FINDING A — SECONDARY PRODUCER-AESTHETIC CONSTANTS (reviewer, from P-025;
  deferred by design, NOT drift). ✓ NOW FULLY RESOLVED (governance ✓ P-027; doctrine
  ✓ P-028).** P-025 captured what its scope declared; the remaining producer-specific
  constants have now ALL been captured:
  - **→ P-027 (governance): ✓ RESOLVED.** The profile holds `taste_triangle`
    (`intimate_width_penalty: 30` + `emotion_dims: [ramone_score,
    listener_excitement_score, vocal_belief_score]`) + `veto_thresholds`
    (`reject_below: 45` / `align_veto_below: 50` / `align_fallback: 75`), all sourced +
    round-trip-guarded, byte-identical.
  - **→ P-028 (doctrine): ✓ RESOLVED.** The profile's new `doctrine.scorers` group
    holds ALL 5 remaining scoring functions' constants — `_vocal_centrality`
    (no_lead 35.0 / baseline 70.0 / bonuses 10,10 / masked_coeff 6), `_depth_hierarchy`
    (baseline 40 / per_distinct 12 / forward_threshold 0.6 / forward_occupancy 60),
    `_section_contrast` (baseline 100 / lift_fail_penalty 18), `_static_mix` (baseline
    80.0 / peak_ceiling -0.1 / peak_penalty 10 / dominant_band_threshold 0.55 /
    dominant_band_penalty 10 / crit_low_coeff 8 / no_lead_penalty 8), `_dynamic_mix`
    (insufficient_sections_score 40.0 / baseline 30 / rms_coeff 8 / width_coeff 140 /
    bright_coeff 140 / lift_fail_penalty 10), captured VERBATIM and sourced,
    byte-identical.
  **Finding A carries NO remaining deferred capture** — the reference profile now
  fully drives creative + governance + doctrine.

- **★ ALIASING-PROOF REQUIREMENT — ✓ DISCHARGED for ALL THREE consumer modules
  (creative P-026, governance P-027, doctrine P-028); a PER-MODULE invariant, NOT a
  structural guarantee (reviewer, from P-026).** P-026 proved `creative.py`
  copy-before-mutate (`kind_scores` byte-unchanged after a nudge + promotion fire).
  **P-027 DISCHARGED it for governance** (mutation local to `triangle`; shared
  `_DEFAULT_PROFILE` byte-unchanged after a fixture run). **P-028 DISCHARGED it for
  doctrine:** grep confirmed no in-place mutation of the sourced structures; the
  no-aliasing test runs `score_doctrine` on a fixture (+ crafted multi-penalty inputs)
  and asserts the shared `_DEFAULT_PROFILE` structures are byte-unchanged afterward;
  determinism holds. **So all three per-module proofs are in.** **★ UPDATE (P-029):
  P-029 threaded a per-call profile BUT DID NOT remove the module `_DEFAULT_PROFILE`
  singleton** — it remains the `None`-default fallback in all 3 consumer modules, so
  the shared-mutable-global still exists on the DEFAULT path and the per-module
  copy-before-mutate discipline STILL CARRIES. **CARRY-FORWARD for P-032:** when a
  SECOND live profile is loaded per call, keep the aliasing discipline in mind — do
  NOT mutate a loaded profile's structures in place. The full structural removal of
  the singleton is not yet done. **★ REINFORCED by
  P-032e, P-032a AND P-032b:** all three new scorers (`_beat_identity`,
  `_negative_space`, `_groove_coherence`) only READ `doctrine[...]` /
  `groove[...]` and never mutate the profile, each guarded by a no-aliasing
  test — so the per-module copy-before-mutate discipline still holds. When a SECOND
  live profile is loaded per call (P-032h authors `timbaland.json`), do NOT mutate a
  loaded profile's structures in place. **★ UPDATE (P-032h close): the SECOND live
  profile IS now real (`timbaland.json`) and the discipline HELD — the
  packet touched ZERO engine code and mutates nothing; the structural
  `_DEFAULT_PROFILE` singleton removal is STILL outstanding — carry
  forward.**

- **★ TRAILER-SPEC STANDING NOTE — DROP the "NO model identifier" line from FUTURE
  packet specs (from P-027; reconciled).** The reviewer repeatedly re-flags the
  mandated `Co-Authored-By: Claude Opus 4.8` trailer as a "model identifier,"
  conflicting with packet-spec lines that say "NO model identifier in any commit
  message/artifact." **RECONCILED — there is NO violation:** the harness / `CLAUDE.md`
  MANDATE that exact trailer session-wide; "Claude Opus 4.8" is the SANCTIONED trailer
  form, DISTINCT from the exact model ID the identity rule bars. **Action for P-028+
  spec authors:** OMIT the "NO model identifier" constraint line — it conflicts with
  the mandated trailer and keeps tripping the reviewer. The required trailers
  (`Co-Authored-By: Claude Opus 4.8` + `Claude-Session: …`) are correct and expected.
  **✓ RESOLVED in Fable 5's favor for the batch (P-038 close,
  2026-07-02): the mandated trailers for this session are
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link — P-038's one reviewer must-fix was exactly their
  ABSENCE, resolved by a tree-neutral amend (`e1ddfbf` → `7b9eda7`);
  trailer-only re-check clean (`git interpret-trailers`). The standing
  guidance holds: packet specs must NOT carry a "NO model identifier"
  line — the mandated trailers are correct and expected.**

- **★ WATCH-ITEM — `emotion_dims` couples the profile to `scores` dict keys (reviewer,
  from P-027; mild).** P-027's widened `taste_triangle.emotion_dims`
  (`["ramone_score", "listener_excitement_score", "vocal_belief_score"]`) couples the
  profile to the exact key names in the runtime `scores` dict. Byte-identical and
  correct today, but **watch this coupling when P-028 generalizes scoring and when
  P-029 threads the profile per-call** — any rename/restructure of the score keys must
  stay in lockstep with `emotion_dims`. **★ UPDATE (P-030 close): the
  coupling HELD through the contract migration** — the reference
  taste-triangle dim was renamed IN PLACE, in lockstep with the score-key
  rename (`ramone_score` → `emotional_hierarchy_score`), with untouched
  blend arithmetic (reviewer-verified). The coupling itself still exists —
  keep watching on any future score-key change.

- **★ CONFIRMED HONESTY / SOURCING POLICY — a STANDING product decision governing
  P-031 / P-032 (confirmed by the user).** hand-curated → high-confidence;
  derived → low-confidence (labeled); LLM → draft-only, NEVER high-confidence. The
  `halee_ramone` reference is `hand-curated-documented` → `high` / `risk_class 0`,
  consistent with the policy. The profile metadata stamp exists now (P-025) but is
  not enforced / propagated until P-031; authoring a SECOND profile (P-032) must
  obey this policy (no LLM-authored profile may claim `high` confidence).
  **★ UPDATE (P-031 close): the per-area enforcement is LIVE** — every
  profile now REQUIRES a validated `confidence_map` (no silent defaults),
  rendered per-call; P-032h's `timbaland.json` must author its OWN map under
  this policy (hand-curated-documented → HIGH), and should verbatim-pin it
  like halee_ramone's.

- **★ THE ARC IS DOWN TO ITS LAST STEP — P-024 (MCP SERVER, option C step 2).**
  Canonical target: Logic Mix OS as a tool Claude Cowork can drive END-TO-END in a
  Logic Pro mixing session (plan-only v1). **P-019 ✓** closed the learning loop
  INSIDE the cowork surface (`record_mix_pass`, read/write symmetric); **P-020 ✓**
  made the surface self-describing as an ordered, phase-grouped session flow
  (`describe_session`, completeness invariant load-bearing); **P-021 ✓ (the
  MILESTONE)** PROVED, executably, that an agent driving ONLY the cowork surface
  completes a full plan-only session AND closes the learning loop within the surface
  (load-bearing + non-tautological); **P-023 ✓ (option C step 1)** turned the raw-CLI
  transport into a VERSIONED, SELF-DESCRIBING contract (`describe_contract`, registry
  35, inspect-derived params, honest side_effect making live-vs-dead a first-class
  contract fact, + `COWORK_CONTRACT.md`). The user chose **option C (sequenced):
  documented raw-CLI contract now [P-023, done], MCP server as the follow-on
  [P-024].** **So the canonical target is essentially MET at the decision-system
  level and the transport is now a documented, versioned contract;** the ONLY
  remaining step is:
  - **P-024 — the ONLY remaining arc step (option C step 2, the FINAL step): a thin
    MCP server wrapping the SAME cowork registry.** Reuse `describe_contract`'s
    per-command `params` / `side_effect` metadata DIRECTLY as the MCP tool schemas
    (do NOT re-derive). **Fold in the P-023 carry-forward version-fingerprint
    guard** — a test pinning a hash of the contract surface so any change to
    `params` / `side_effect` forces a conscious `API_VERSION` decision (closes the
    reviewer watch-item that the hand-maintained version can silently lag the
    surface). Architecture/transport fork — confirm active via the orchestrator; do
    NOT open blind. **After P-024 the arc is COMPLETE; landing the accumulated
    P-017-guard → P-024 work on default is the natural close (USER-GATED).**
  - **P-022 — OPTIONAL / UNNEEDED.** The P-021 honesty clause surfaced NO real gap
    requiring session-efficiency / override-propagation work. Do NOT open unless a
    concrete gap emerges.

- **P-023 CARRY-FORWARD (non-blocking reviewer watch-item, for P-024):** the
  contract's `params` and `side_effect` cannot drift from the code (inspect-derived
  / verified against handler bodies), BUT `API_VERSION` is a hand-maintained string
  with NO test that fails when the surface changes without a version bump — so the
  declared VERSION can silently lag a surface change. **P-024 is where to add the
  version-fingerprint guard.** Minor note (NOT a bug): `update_taste_calibration`
  exposes `[label, context]` via inspect — MORE honest than the hand-written `desc`
  "(params: label)"; the inspect derivation is the truthful one.

- **✓ RESOLVED by P-021, then ELEVATED TO A CONTRACT FACT by P-023 — the
  LIVE-vs-DEAD distinction** (was the P-020 carry-forward reviewer flag). P-021's
  live-vs-dead test asserts, on the real surface, that `write_mix_decision` (the
  display-only DEAD `decision_ledger.json`, runtime-verified) does NOT change
  `suggest_next_pass`, whereas `record_mix_pass` (the LIVE history channel →
  `_apply_history`) DOES — only `record_mix_pass` closes the loop. **P-023 then made
  this a FIRST-CLASS CONTRACT FIELD:** `describe_contract`'s `side_effect` declares
  each write honestly — `record_mix_pass` → `writes:history(live)`,
  `update_taste_calibration` → `writes:taste(live)`, `write_mix_decision` →
  `writes:ledger(dead)`, `override_track_identity` → `mutates:session`, all other 31
  `none` (verified against handler bodies by qa + reviewer). So the distinction is no
  longer merely telegraphed by `desc` strings or only executably pinned by a test —
  it is a declared, machine-readable contract fact a future agent/reader cannot
  mistake. Ties into the standing LEDGER-IS-DEAD routing guard below.

- **Reward-nudges family — NOW CLOSED as SATURATED / EQUILIBRIUM (P-017).**
  P-016 shipped the FIRST reward/promotion nudge (the `loop` branch:
  `loop_deconstruct` promoted +4.0 past `subtractive_drop` when a loop is
  genuinely foregrounded), evidence-gated and LIVE in production, and it MERGED via
  PR #15. **But the further-reward-rows thread is now CLOSED:** the reward layer is
  saturated at cap 4.0 — only `loop` (gap 3.43) was cleanly reachable; `density`
  (gap 4.14) is unreachable + circular-gated; `drum_room_bloom` is hollow (no
  evidence signal). And P-017 confirmed the base-value re-curation lever cannot
  honestly flip `density` either. The three levers (penalty, reward, base-value)
  have all converged on a DOCTRINE-HONEST EQUILIBRIUM: **there is no honest further
  flip move inside the current dimension set.** Should the user ever ask for a NEW
  reward row anyway, it would still be user-gated per-row and must clear the SAME
  bar as P-016 (its own evidence gate + a non-vacuity mutation check + a
  collateral-safety proof + a live-wire check: evidence computed BEFORE
  `run_creative_engine`; asserted on the real `result.creative`/`result.governance`
  with NO re-run) — but this is no longer an in-flight candidate.
- **Near-tie-creative-FLIP fixture — RESOLVED-as-UNREACHABLE (P-014 verified
  negative finding).** This was the reachable-deferred complement to P-013's
  no-flip case; **P-014 proved a flip is structurally UNREACHABLE test-only**
  under the current `_KIND_SCORES` / `_NUDGE_TABLE`. The builder wrote ZERO code
  (honesty clause); qa adversarially CONFIRMED with THREE independent harnesses
  (inline-math, real-`score_variant`, saturated worst-case `masking_report`) —
  **all 0 flips** — plus a source re-derivation. Two structural reasons: the
  universal branch leader `subtractive_drop` (85.29) is in NO nudge row →
  penalty-immune; the one sub-cap near-tie branch (`vocal_belief`, gap 1.71)
  penalizes leader (`vocal_ride`) and runner-up (`intimacy_pass`) equally
  (identical row-0 `lead_masked −8`). **No longer a reachable candidate** — it is
  replaced by the user-gated curation packet directly below. Receipt:
  `build-os/receipts/P-014-near-tie-creative-flip-fixture.md`. (The P-014
  harnesses live in scratchpad — not committed.)
- **Make-the-nudge-decisive (curation change) — RESOLVED by P-015 (user-signed-off
  PRODUCT change).** The user chose "Option 1 — Proceed, corrected" (2026-06-30)
  and P-015 actioned route (a): `creative.py` `_NUDGE_TABLE` row-0 now **exempts
  `intimacy_pass`** and **strengthens the penalty `−8` → `−14`** (= −2.0 overall =
  the cap), so the `vocal_belief` 1.71-gap near-tie now FLIPS `vocal_ride` (vocal_A)
  → `intimacy_pass` (vocal_B) within the ±2.0 cap. The nudge is **no longer
  transparency-only** — it is decisive on exactly that near-tie, still bounded so it
  cannot overturn a clear ranking. Receipt:
  `build-os/receipts/P-015-decisive-masked-vocal-nudge.md`. **No remaining work
  here.**
- **Reviewer trajectory flag (from P-015 — non-blocking, watch-item):** the P-015
  flip margin is **thin (0.2)**, but it is **fully pinned by binding tests**
  (`tests/test_decisive_nudge.py`: flip + load-bearing negative control + collateral
  safety; updated `tests/test_creative_nudges.py`). A future re-curation of the
  creative scoring would surface as a **RED test, not a silent re-rank** — the
  golden-unguarded variant-scoring path is covered by these unit/flip tests. Carry
  this awareness into any future `creative.py` / `_NUDGE_TABLE` / `_KIND_SCORES`
  touch.
- **Reviewer watch-item (from P-016 — non-blocking, standing) — REWARD-CREEP:**
  P-016 crossed the penalty-only line with the FIRST reward nudge. Any FUTURE
  reward row must clear the same bar P-016 did: its own evidence gate + a
  non-vacuity mutation check + a collateral-safety proof + a **live-wire check**.
  Watch the trajectory — reward nudges are additive pressure on the default
  recommendation; keep each one bounded (a separate `CREATIVE_PROMOTION_CAP`),
  evidence-gated, and user-gated per-row.
- **★ STANDING LESSON (from P-016 — the P-009-style catch):** an evidence-gated
  creative nudge is only LIVE if its evidence is computed BEFORE
  `run_creative_engine`. In P-016, Commit-1's promotion was INERT in production —
  `run_creative_engine` ran before `provenance`/`source_audits` were populated, so
  the predicate always read empty evidence; the tests passed only because they
  RE-RAN the engine on the finished result (masking the inertness). Commit-2's
  live-wire (relocate `analyze_provenance` + `audit_all` just before
  `run_creative_engine`, a pure relocation) fixed it, guarded by two
  production-liveness tests that assert on the real `analyze()`
  `result.creative`/`result.governance` with NO re-run (FAIL pre-reorder, PASS
  after). Masking is pre-creative so P-015 was always live; provenance/source_audits
  were post-creative until P-016. **Rule:** for any future creative nudge, add a
  no-re-run liveness assertion — a green re-run test can mask production inertness.
- **Taste-flip through `analyze()` — STRUCTURALLY UNREACHABLE test-only
  (P-013 finding); a flip is USER-GATED to a product change.** P-013 tried to build
  a taste-driven governed-winner flip fixture and could NOT: the builder brute-forced
  all 3 fixtures × 4 intents with a narrower-taste `ProjectMemory` and found NO
  governed-winner flip anywhere. **This is a POSITIVE alignment confirmation, not a
  gap** — reviewer-verified in source: `_apply_taste` (governance.py) moves only the
  `taste_triangle` **identity** axis (clamped ±`TASTE_MAX_DELTA 15`), maps only to
  `width_bloom`/`drum_room_bloom` (`_TASTE_KIND_BIAS`), and the governed winner is
  ranked on `overall_score` behind an **align-veto**, so **taste structurally cannot
  reorder a truth-ranked winner** (doctrine: "taste can never outrank a truth move,"
  working as intended). The unit "flip" in `test_governance_taste.py` only works
  because it hand-injects branch values curated scoring never produces. **The
  reachable end-to-end taste claim (taste reaches governance + down-weights identity
  with bounded evidence) is ALREADY proven on real data** by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`. Making a real
  governed-winner flip reachable would need a product-code aesthetic change →
  **user-gated, a separate packet** (distinct from the reachable near-tie-creative
  FLIP fixture above).
- **Wider `--memory-dir` CLI surface (from P-009 reviewer — non-blocking; partly a
  product question):** consider whether more analyze-class CLI commands (beyond
  `cowork`) should accept `--memory-dir`. P-009 wired exactly one prod surface
  (`cowork.py:28`); the other 13 `analyze()` CLI call sites stay memoryless by
  design. Evaluate which, if any, warrant the live wire.
- **Low-priority test cleanup (from P-008):** `test_evidence_only_on_moved_candidates`
  in `tests/test_next_pass_history.py` has a redundant always-true inner guard;
  tidy when convenient. **Not its own packet** — fold into any future touch of
  that file.
- **Net-new event-logging packets (from P-002/P-004) — REFRAMED, still BLOCKED ON
  A PRODUCT DECISION:** `taste_feedback`, `validation_check`, `revert`,
  `manual_note` remain valid `EVENT_TYPES` members with **NO producer wired into
  the decision ledger today** (taste → `taste_calibration.json`; validation only
  returns; revert is a pass-record field; no `manual_note` writer exists).
  **Reframe (strengthened by P-009):** the recorded-signal loop now has TWO real
  downstream consumers **that are live in production** (P-007 recorded taste →
  governance and P-008 recorded history → next-pass, both wired through
  `analyze()` by P-009), so wiring `validation_check` / `taste_feedback` producers
  is **more justified than ever**. BUT this is still **net-new FEATURE work**
  behind the same unanswered product decision: **should validation / taste / revert
  / note signals actually be written to the decision ledger?** Keep deferred; do
  NOT start as packets until that product decision lands.
  **★ CORRECTION (P-018 finding — read before routing any such producer):** the
  decision LEDGER (`add_decision` → `decision_ledger.json`) has **ZERO analyze-path
  consumers** — `mem.ledger()` is display-only (`cli.py:315`). So a producer that
  merely WRITES to the ledger is **INERT** (the hollow trap). `validation_check` /
  `manual_note` producers now **need a NEW consumer — not just a ledger write.**
  The only LIVE learning channels are HISTORY (`mix_pass_history.json` →
  `_apply_history`) and TASTE (`taste_profile.json` → governance); P-018's
  confirmed `revert` correctly landed on the history channel (not the ledger).
- **★ Outcome-enum generalization (reviewer's P-018 trajectory note — non-blocking;
  a candidate, NOT staged):** capturing only `revert` leaves the outcome vocabulary
  lopsided. A future generalization to a small outcome enum
  (`reverted` / `kept` / `refined`) would round out the outcome→learning loop, and
  the P-018 `reverted: bool` field can widen to that later **WITHOUT breaking the
  byte-identical default.** Reachable, user-gated for the semantics; do NOT open
  without an explicit ask.
- **★ THE LEDGER-IS-DEAD FINDING (P-018 — a standing routing guard; now EXECUTABLY
  PINNED by P-021):** the decision LEDGER (`add_decision`/`decision_ledger`) has NO
  decision-making consumer — it is display-only (`cli.py:315`). **Do NOT route an
  inert ledger producer.** A confirmed-outcome / event producer is only real if it
  lands on a LIVE channel (history `mix_pass_history.json` → `_apply_history`, or
  taste `taste_profile.json` → governance). This is why P-018's confirmed revert
  lands on the history axis. **P-021 now pins this executably:** its live-vs-dead
  test proves `write_mix_decision` (dead ledger) does NOT change `suggest_next_pass`
  while `record_mix_pass` (live history) does — the guard is no longer a note-only,
  it is a green test.

## Genuinely real carried follow-ups (verified)

- **Real macOS/Logic test surface** — out of current authority (needs real DAW;
  blocked by the no-real-DAW guardrail).
- **Controlled Class-3 apply path** — guardrail-gated; do not open without an
  explicit apply-safety packet.

## Re-ranked strategic candidates (creative-scoring decision now resolved)

> The learning loop is real in production (P-007→P-008→P-009), the cross-song
> coherence axis is open (P-010), the album-means truth is single-sourced (P-011),
> the creative-scoring aesthetic decision is RESOLVED (P-012 option B, MERGED PR
> #13; P-015 decisive; P-016 reward, MERGED PR #15), and the judgment layer is now
> at a DOCTRINE-HONEST EQUILIBRIUM (P-017 — no honest further flip in the current
> dimension set), the OUTCOME→learning axis is OPEN (P-018 — the first
> confirmed-outcome signal is live), and the learning loop is now CLOSEABLE INSIDE
> the cowork surface (P-019 — read/write symmetric) and self-describing as an
> ordered, phase-grouped session flow (P-020 — `describe_session`, 34 commands;
> steps 1 & 2 of the arc P-019→P-023 to a Cowork-usable end-to-end state). For
> orchestrator re-survey:

- **THE FLIP PROGRAM IS ESSENTIALLY COMPLETE — DOCTRINE-HONEST EQUILIBRIUM
  (P-017).** The three levers have converged: penalty (P-012/P-015), reward
  (P-016), and base-value re-curation (P-017) all confirm `subtractive_drop`'s
  dominance is legitimate; the masked-vocal and foregrounded-loop overrides are the
  only warranted flips; **NO honest further flip exists in the current dimension
  set.** The reward-family (further rows) and re-curation-for-flips threads are
  CLOSED as saturated. **The ONE remaining honest thread — user-gated, NOT staged:**
  a SYMMETRIC re-judgment — is `subtractive_drop` at 85.29 (high on every dim)
  itself slightly OVER-valued? Lowering it (rather than inflating a rival) would be
  a different, un-signed-off packet. Surface to the user; do NOT open without an
  explicit ask.
- **★ THE OUTCOME→LEARNING AXIS IS OPEN (P-018) AND NOW CLOSEABLE INSIDE COWORK
  (P-019).** P-018 landed the first confirmed-outcome signal (`memory-record
  --reverted` overrides the score-inference and measurably changes real
  `analyze(--memory-dir)` next_pass; opt-in / byte-identical default). **P-019
  brought the RECORD side onto the cowork surface** — a `record_mix_pass` command
  (registry 32→33) records a pass on the LIVE history channel, so an agent can close
  the loop (record → see `suggest_next_pass` change) without leaving the surface
  (read/write symmetric). The reachable outcome-side next move is the **outcome-enum
  generalization** (`reverted`/`kept`/`refined`, widening the `reverted: bool`
  without breaking the default) — **user-gated for the semantics; NOT staged.** The
  in-flight roadmap now is the cowork ARC — **P-020 (`describe_session`,
  self-describing session flow) is DONE (step 2); the remainder is P-021→P-023**
  (see the Deferred section). **Standing routing guard:** route any outcome/event
  producer onto a LIVE channel (history or taste), never the display-only ledger —
  and P-020 carries a P-021 nudge to SURFACE that live-vs-dead distinction in the
  walkthrough.
- **Option-B-visibility / decisiveness** — the CREATIVE half is fully closed:
  **P-013** proved the nudge fires on real data through `analyze()` (option-(a)
  no-flip on a clear ranking), **P-014** proved a near-tie FLIP was unreachable
  *under the then-current curation*, and **P-015** (user-signed-off product change)
  made it decisive on the masked-vocal near-tie (`vocal_belief`: vocal_ride →
  intimacy_pass, within the cap). Nothing reachable remains here. The TASTE-flip
  half is **user-gated** (needs a product change; the reachable taste claim is already
  covered by `test_live_wire.py::test_taste_axis_changes_governance`).
- Wider `--memory-dir` surface remains a small in-authority move (partly product).
- Net-new **event-logging** producers remain behind the product decision.

## Done (resolved)

- **★★★ P-032h DONE — THE PAYOFF PACKET: `timbaland.json`, the second live
  producer profile, the FIRST non-byte-identical output of the epic
  (`build-os/receipts/P-032h-author-timbaland-json.md`).** Same stems, two
  judgments — 68.4 / 52.6 / 49.7 (timbaland) vs 73.8 / 70.7 / 74.3
  (reference), fully attributable (zero component divergence on simple;
  exactly `loop_context_score` 15.0→10.0 on the loop fixtures; the rest pure
  reweighting of shared measurements); default path moved ZERO bytes; gates
  flip live (protect_iconic_loops=true WITHHOLDS loop_deconstruct on iconic
  while the reference fires; static still fires; masked-lead fires under
  BOTH); ZERO RELAXATION adversarially verified; the 11-entry confidence_map
  verbatim-pinned (5 high / 1 limited / 5 deferred), provenance
  hand-curated-documented → HIGH (reviewer-ENDORSED). Single commit
  `70a0b69` (2 NEW files, 1044+/0−, zero engine code; pushed, NOT merged).
  Suite 600 → **639** (+39); regression 68/68 UNCHANGED. qa GREEN; reviewer
  PASS (no must-fix); Codex NOT available — single-model review.

- **★★ P-032d DONE — the FOURTH new producer-agnostic doctrine axis
  `rhythmic_surprise` (weak, section-aggregate form: cross-section
  transient-density variation — pstdev spread + largest adjacent swing) lands
  byte-identically for halee_ramone; first of the RESEQUENCED remaining order
  (d → c → g → f), the smallest/safest lift confirmed in practice (one input,
  zero new plumbing)** (`build-os/receipts/P-032d-rhythmic-surprise.md`). New
  agnostic scorer `_rhythmic_surprise(sections_analysis, doctrine)` in
  `doctrine_engine.py` — the 11th doctrine component, appended LAST to
  `component_scores` (after `groove_coherence_score`; 10-term summation order
  preserved) with `weights["rhythmic_surprise_score"] = 0` in
  `halee_ramone.json` + a `doctrine.scorers.rhythmic_surprise` constants block;
  `producer_profile._validate` now requires `rhythmic_surprise`;
  `doctrine_score.schema.json` documents the optional `rhythmic_surprise_score`.
  Constants: `insufficient_sections_score 40.0 / baseline 20.0 / spread_coeff
  160 / swing_coeff 60`; live fixture scores (weight-0, informational) 51.1
  (simple — some sectional variation) / 20.0 (dense — the real-world
  high-mean/ZERO-variance constant bed) / 27.8 (splice). **Byte-identical
  INDEPENDENT capture:** 33/33 pre-existing values × 3 fixtures unchanged
  (overalls 73.8 / 70.7 / 74.3); regression 68/68, 0 warnings — UNCHANGED.
  **All 4 distinctness guards pass AND independently recomputed by qa**
  (high-mean/zero-var bed → 20.0; mean-invisibility 20.0 == 20.0;
  negative_space-opposite ns 78.0 vs rs 20.0; dynamic_mix-distinct dyn 100.0
  vs rs 20.0). **Liveness load-bearing:** drop-axis monkeypatch sabotage →
  liveness 2 FAILED / byte-identical 5 passed. **Honest scope verified**
  (AST/grep: sections + doctrine only; evidence says "weak, section-aggregate
  form"; fill detection / unexpected-hit detection / per-onset IOI deviation
  deferred in the docstring; does NOT read `overall_regularity` — that is
  `_groove_coherence`'s input — ENFORCED). Single commit `8a81516` (HEAD IS
  Commit-1 → green in isolation by construction = 451; base independently
  verified at set-active `8c03f14` = 433 in a throwaway worktree); suite
  433 → 451 (+18); safety grep NONE FOUND (535 insertions / 6 deletions, 8
  in-packet files); 3 pre-existing pins updated (`test_producer_profile.py`
  scorers-set, `test_doctrine_profile_sourced.py` `_WEIGHTS` value-pin,
  `test_groove_coherence.py` groove_coherence now index 9). qa **GREEN**;
  reviewer **PASS (no must-fix)** — ran THREE own sabotages, ALL caught
  (hardcode the scorer → 7 discrimination/fallback/evidence tests fail; drop
  from `component_scores` → 3 fail incl. BOTH liveness; flip the halee weight
  0→2 → 8 fail across three guard files); constants sanity: smooth mid-range
  discrimination (swing 0.1 → 34, 0.3 → 62, 0.5 → 90), clamps at 100 for
  swings ≳0.57 — sibling-idiom-consistent, not degenerate. **Codex NOT
  available — single-model review.** **★★ MILESTONE — 11 component axes; 4 of
  the 7 Timbaland "weight up" axes landed** (beat_identity, negative_space,
  groove_coherence, rhythmic_surprise), all
  append-last/weight-0/profile-sourced, zero plumbing debt. **P-032d
  local-only** (`8a81516` atop set-active `8c03f14` on the dev branch), not
  pushed/merged (merge base still `e79426a` = PR #16). NEW cosmetic residue
  carried to Deferred: the rhythmic_surprise liveness-docstring overclaim
  (fold ONE sweep across all four axis test files) + the None-filtering /
  non-adjacent-swing note. Next per the resequenced order: **P-032c
  (low_end_motion)**.

- **★★ P-032b DONE — the THIRD new producer-agnostic doctrine axis
  `groove_coherence` + the `analyze_groove` LIVE-WIRE relocation land
  byte-identically for halee_ramone; the RISKIEST packet of the sub-arc so far
  (moved code, not just added), TRIPLE-VERIFIED (qa GREEN + reviewer PASS +
  3-skeptic adversarial pass, all claims HELD)**
  (`build-os/receipts/P-032b-groove-coherence-livewire.md`). `pipeline.py`:
  `analyze_groove` relocated to BEFORE `score_doctrine` (pipeline.py:180 vs
  :183), the groove threaded in via `score_doctrine(..., groove: Optional[Dict]
  = None)` (keyword default None — every existing caller byte-identical), and
  the SAME groove object REUSED in `result.expanded["groove"]` (:208) —
  computed exactly ONCE (the P-016 lesson made structural; exactly one
  `analyze_groove(` call site, spy-counted). New agnostic scorer
  `_groove_coherence(groove, doctrine)` is the 10th doctrine component —
  constants `neutral 45.0` (absence neither rewarded nor punished) / `baseline
  15.0` / `regularity_scale 85.0` (linear map: regularity 0 → 15, 1.0 → 100;
  dense fixture 0.989 → 99.1); honest naming test-guarded
  (regularity/consistency scored as a PROXY for coherence, never "tighter is
  better" — the agnostic layer stays neutral, the producer decides the
  weighting). **Byte-identical INDEPENDENT proof** (qa's own capture, not
  builder pins): all 9 pre-existing component scores + overall +
  `expanded["groove"]`, all 3 fixtures → diff EMPTY (overalls 73.8 / 70.7 /
  74.3); regression 68/68, 0 warnings, 0 critical. Liveness + sabotage pass
  (gc(0.989)=99.1, neutral 45.0; `groove=None` collapses 99.1 → 45.0).
  **Reviewer verified the relocation crux by INJECTED REGRESSIONS** in an
  isolated worktree (a second `analyze_groove` call →
  `test_analyze_groove_called_exactly_once` red 2==1; `groove=None` threading →
  `test_score_doctrine_receives_the_real_groove` red 45.0 ≠ 99.1 — both guards
  genuinely load-bearing); backward-compat + None-handling (`is None` guard — a
  real 0.0 → 15.0, not swallowed; no KeyError path) + guard updates legitimate
  (negative_space now index 8, `keys[:8]` anchor intact). **3-skeptic
  adversarial pass (all claims HELD):** (1) float-determinism bit-identical,
  `gc*0==0.0` exact, `nan*0` poisoning UNREACHABLE (`_clamp` neutralizes
  non-finites; `analyze_groove` emits only None or float[0,1]), all 8 non-groove
  `expanded` keys byte-identical; (2) call-count 1 across ALL branches
  (ref-delta, creative, memory), `is`-identity of the reused groove, nothing
  mutates it on the real path; (3) every None/empty/missing-key case → clamped
  neutral 45.0, boundaries clamp to [0,100], out-of-contract crash inputs
  proven UNREACHABLE from the sole producer. Single commit `e9f793f` (HEAD IS
  Commit-1 → green in isolation by construction = 433; suite also verified
  independently at base `bd98777` = 413 in a throwaway worktree); suite 413 →
  433 (+20); safety grep NONE FOUND (582 insertions / 13 deletions, 9 in-packet
  files). **Codex NOT available — single-model review.** **★★ MILESTONE — the
  engine now carries 10 component axes; the onset/IOI signal is now LIVE at
  doctrine time, unblocking the axes that need rhythm timing.** **P-032b
  local-only** (`e9f793f` atop set-active `bd98777` on the dev branch), not
  pushed/merged (merge base still `e79426a` = PR #16). NEW cosmetic residue
  carried to Deferred: the shared mutable groove dict (`expanded["groove"]` IS
  the doctrine arg). Next per the resequenced order: **P-032d
  (rhythmic_surprise)**.

- **★★ P-032a DONE — the SECOND new producer-agnostic doctrine axis
  `negative_space` (absolute arrangement room/sparsity) lands byte-identically for
  halee_ramone; the Timbaland sub-arc continues past the crux**
  (`build-os/receipts/P-032a-negative-space.md`). New agnostic scorer
  `_negative_space(records, sections, mix_metrics, doctrine)` in
  `doctrine_engine.py` composes ABSOLUTE arrangement room/sparsity as a STRENGTH
  from section-aggregate physics — low mean section spectral `density` (room), a
  genuine dropout section (`min_section_density` / min RMS meaningfully below max —
  "silence as arrangement"), and transient breathing room (low mean section
  `transient_density`) — always returning a clamped float (neutral fallback 40.0).
  Deliberately DISTINCT from `_dynamic_mix` (section-to-section movement): a
  dense-but-moving case scores `dynamic_mix = 100.0` vs `negative_space = 15.0`
  (85-pt gap), guarded by an explicit distinctness test. Wired into `score_doctrine`
  as `negative_space_score` appended LAST to `component_scores` (after
  `beat_identity_score`, summation order preserved → overall bit-identical) with
  `weights["negative_space_score"] = 0` in `halee_ramone.json` + a
  `doctrine.scorers.negative_space` constants block; `producer_profile._validate`
  now requires `negative_space`; `doctrine_score.schema.json` documents the optional
  `negative_space_score`. Constants: `neutral 40.0 / baseline 15.0 /
  density_ceiling 1.0 / room_coeff 50 / transient_ceiling 1.0 / breathing_coeff 20 /
  dropout_coeff 25 / dropout_floor 0.1`; live fixture scores (weight-0,
  informational) 62.3 / 15.0 / 20.0. **Byte-identical PROVEN** (0 mismatches / 27
  comparisons vs set-active base `836bd22`, overalls 73.8 / 70.7 / 74.3 unchanged;
  regression 68/68, 0 critical, 0 warnings UNCHANGED). **Liveness LOAD-BEARING** (a
  non-zero weight moves `analyze()` overall; sabotage fails liveness — drop
  threading → FAIL/KeyError, hardcode → 8 fail + 5 err — while byte-identical stays
  green; the P-016/P-029 lesson) + value-discrimination (incl. distinctness from
  dynamic_mix). **Honest boundary documented in-code, NOT faked:** sample-level
  inter-onset silence gaps need onset timing not visible at `score_doctrine` time
  (→ P-032b groove live-wire); section-aggregate grain only. No-aliasing (scorer
  only reads `doctrine[...]`, no-aliasing test). Single commit `3edcd9c` (green in
  isolation = 413 — HEAD IS Commit-1); suite 396 → 413 (+17; 0
  failed/skipped/warnings, green under `-W error`); 3 doctrine-key pins updated
  (`test_producer_profile.py` scorers-set, `test_doctrine_profile_sourced.py`
  `_WEIGHTS` value-pin, `test_beat_identity.py` beat_identity now index 7). Safety
  grep clean; honest-scope confirmed; UI N/A. qa **GREEN**; reviewer **PASS** (all 8
  scrutiny points; byte-identical empirically proven base→HEAD; distinctness
  non-tautological; honesty gate genuine; liveness load-bearing; agnostic-first
  (all 8 tunables in the profile); no-aliasing; guard updates legitimate
  tightening; Product Trajectory Check pass; no must-fix). **Codex NOT available —
  single-reviewer verdict.** **★★ MILESTONE — the engine now carries 9 component
  axes; the producer-agnostic architecture (P-029) continues to prove EXTENSIBLE.**
  **P-032a local-only** (`3edcd9c` on the dev branch atop the `6d34c30` P-029-close
  base), not pushed/merged. Non-blocking reviewer note carried to Deferred: the two
  `liveness` docstrings in `test_negative_space.py` (and the same in
  `test_beat_identity.py`) overclaim — cosmetic, fold a one-line fix into a future
  doctrine touch. Recommended next: **P-032b (groove_coherence live-wire)**.

- **★★ P-032e DONE — the FIRST new producer-agnostic doctrine axis `beat_identity`
  (strength-form) lands byte-identically for halee_ramone; the Timbaland sub-arc is
  underway with the crux front-loaded**
  (`build-os/receipts/P-032e-beat-identity.md`). New agnostic scorer
  `_beat_identity(records, events, doctrine)` in `doctrine_engine.py` measures the
  STRENGTH of a central rhythmic fingerprint from transient physics alone (candidacy
  by `transient_density`, NOT instrument label; presence vs a `no_beat` floor;
  distinctness above the track median; definition via `crest_factor_db`;
  foreground/unmasked bonus, buried/masked penalty). Wired into `score_doctrine` as
  `beat_identity_score` appended LAST to `component_scores` (7-term summation order
  preserved → overall bit-identical) with `weights["beat_identity_score"] = 0` in
  `halee_ramone.json` + a `doctrine.scorers.beat_identity` constants block;
  `producer_profile._validate` now requires the `beat_identity` scorer group;
  `doctrine_score.schema.json` documents the optional `beat_identity_score`. Constants:
  `no_beat 20.0 / transient_floor 0.35 / baseline 50.0 / dominance_coeff 40 /
  definition_crest_db 12.0 / definition_bonus 12 / foreground_bonus 18 /
  buried_penalty 14 / masked_penalty 12`; live fixture scores (weight-0,
  informational) 89.1 / 52.7 / 46.0. **Byte-identical PROVEN** (0/24 mismatches vs
  clean base `6d34c30`, overalls 73.8 / 70.7 / 74.3 unchanged; regression 68/68, 0
  critical, 0 warnings UNCHANGED). **Liveness LOAD-BEARING** (a non-zero weight moves
  `analyze()` overall + direction tracks the beat score; sabotage fails liveness
  while byte-identical stays green — the P-016/P-029 lesson) + value-discrimination
  (punchy/foregrounded/distinct → HIGH; none → `no_beat` floor). **Honest boundaries
  documented in-code, NOT faked:** fingerprint TYPING, onset REGULARITY/IOI (→ P-032b
  groove live-wire), and "more undeniable after a move" (before/after render) are OUT
  OF SCOPE. No-aliasing (scorer only reads `doctrine[...]`, two no-aliasing tests).
  Two commits `8239f42` (green in isolation = 396) + `9d6764e`; suite 384 → 396
  (+12; 0 failed/skipped/warnings, green under `-W error`). Safety grep clean;
  honest-scope confirmed; UI N/A. qa **GREEN**; reviewer **PASS** (all 7 scrutiny
  points; byte-identical numerically proven over 100k trials; liveness load-bearing
  by an in-memory sabotage; guard updates legitimate tightening; no must-fix). **Codex
  NOT available — single-model review.** **★★ MILESTONE — the producer-agnostic
  architecture (P-029) is proven EXTENSIBLE, not just parameterizable.** **P-032e
  local-only** (`8239f42`, `9d6764e` on the dev branch on top of the `6d34c30`
  P-029-close base), not pushed/merged. Recommended next: **P-032a (negative_space)**.

- **★★ P-029 DONE — THE PIVOT: the producer profile is now a LIVE, SELECTABLE LEVER
  end-to-end; `analyze(producer=…)` SELECTS which profile drives the judgment**
  (`build-os/receipts/P-029-parameterize-pipeline-by-per-call-producer-profile.md`).
  `pipeline.analyze(..., producer: str | ProducerProfile = "halee_ramone")` accepts a
  NAME or a ready `ProducerProfile` (isinstance dispatch), loads ONCE per call, and
  threads `profile=` to `score_doctrine` / `run_creative_engine` / `run_governance`,
  which thread it to ALL leaf scorers (doctrine's 7 scorers + weights; creative's
  `score_variant`/`_apply_nudges`/`_apply_promotions`; governance's
  `govern_branches`/`govern_variant`/`taste_triangle`/`_apply_taste`) — each reads its
  producer-specific values from the PASSED profile, defaulting to the module
  `_DEFAULT_PROFILE` when `profile is None`. **KILL_SWITCHES recomposed per call = 5
  hardcoded producer-AGNOSTIC SAFETY switches + the profile's aesthetic switches** (a
  swapped producer can NEVER drop a safety guarantee; default composed list
  byte-identical, no safety string in JSON). **No judgment VALUE changed;
  physics/analyzers untouched.** **Byte-identical default PROVEN** (reviewer
  independently byte-diffed default doctrine+creative+governance pre-P-029 vs HEAD
  across all 3 fixtures → IDENTICAL; no-arg == `producer="halee_ramone"` == reference
  object; regression **68/68, 0 critical, 0 warnings — UNCHANGED**). **Selection
  GENUINELY LIVE across all 3 layers** through the REAL analyze() path (synthetic
  one-value-mutated profiles, no monkeypatch): doctrine `baselines.halee` −20 →
  `halee_score` delta exactly 20; creative boosted `vocal_ride` kind_score → variant
  `overall_score` → 100; governance `truth_alignment["intimate"]["vocal_ride"]` 88→60
  → governed `emotional_truth_alignment` 60. **LOAD-BEARING PROVEN BOTH WAYS (the
  P-016 lesson):** sabotaging each layer's threading fails ITS liveness test while
  byte-identical/determinism stay green. **Reviewer grep: ZERO module-global
  producer-value reads inside any scorer body on the hot path — no leaf missed.** Two
  commits `42d6ebd` (doctrine + creative + pipeline wiring + byte-identical +
  doctrine/creative liveness — green in isolation = 383) + `ea1aaa9` (governance
  threading + governance liveness). Suite **370 → 384 passed** (+14; 0
  failed/skipped/warnings, green under `-W error`). Scope: exactly 5 files (4 product +
  1 new test); existing tests UNEDITED; physics/analyzers/bridge/planners untouched.
  Safety grep clean; UI N/A. qa **GREEN**; reviewer **pass**. **Codex NOT available —
  single-reviewer verdict.** **★★ MILESTONE — THE PIVOT: the producer-agnostic
  ARCHITECTURE is COMPLETE and VALIDATED** (reference-profile-driven judgment + a
  producer-AGNOSTIC physics/safety chassis + per-call producer selection). **★
  CARRY-FORWARD for P-032:** the `_DEFAULT_PROFILE` singleton STILL exists as the
  `None`-default fallback in all 3 modules — keep the aliasing discipline when a
  second live profile is loaded. **P-029 local-only** (`42d6ebd`, `ea1aaa9` on the dev
  branch on top of the `e79426a` base), not pushed/merged.

- **★★ P-028 DONE — doctrine sourced from the reference profile, WIDENED (the LAST
  & LARGEST extraction); THE EXTRACTION PHASE IS COMPLETE**
  (`build-os/receipts/P-028-doctrine-sources-values-from-reference-profile.md`).
  `doctrine_engine.py` gains `_DEFAULT_PROFILE = load_profile("halee_ramone")`; all 8
  scorers now read their aesthetic constants from the profile — **Part A** the
  P-025-captured `weights` (halee 1.0 / ramone 1.2 / vocal_centrality 1.2 / depth 1.0 /
  contrast 1.0 / static 1.0 / dynamic 0.8) + `_halee`/`_ramone` baselines (86.0) +
  penalty coeffs; **Part B WIDENED** the profile with a new `doctrine.scorers` group (5
  function groups: `_vocal_centrality` / `_depth_hierarchy` / `_section_contrast` /
  `_static_mix` / `_dynamic_mix`), each constant captured VERBATIM, then sourced. **The
  PHYSICS/measurement code (fg_frac, band max, pstdev, distinct counting, section
  detection) + the presentation thresholds (`stereo_width > 0.6`, `distinct <= 1`,
  `score < 55`) STAY hardcoded — producer-AGNOSTIC.** Clean literal→`c["…"]`
  substitution; formula shape/order preserved; int/float types match. **Byte-identical:**
  existing doctrine tests UNEDITED; regression **68/68, 0 critical, 0 warnings —
  UNCHANGED** (the corpus proof — doctrine feeds `doctrine_score`, golden-pinned;
  reviewer INDEPENDENTLY confirmed live `doctrine_score` byte-matches the golden on all
  3 fixtures incl. `overall_mix_readiness_score`). **Round-trip NON-VACUOUS** (18→17
  flip fails the test + shifts `_section_contrast` 64→66). **No-aliasing DISCHARGED**
  (grep clean; no-aliasing test + determinism). `creative.py`/`governance.py`/
  `pipeline.py` untouched. **Two commits `29b9dfe` (Part A + no-aliasing test — green in
  isolation = 364) + `72e98a7` (Part B widen + source + round-trip).** Suite **351 →
  370 passed** (+19; 0 failed/skipped/warnings, green under `-W error`). Safety grep
  clean; UI N/A. qa **GREEN**; reviewer **pass**. **Codex NOT available — single-reviewer
  verdict.** **★★ MILESTONE — the EXTRACTION PHASE is COMPLETE:** the entire
  producer-specific judgment layer (creative P-026 + governance P-027 + doctrine P-028)
  is now sourced from the reference `ProducerProfile`, BYTE-IDENTICAL, with the physics
  chassis + safety kill-switches cleanly separated and left hardcoded; **the reference
  profile FULLY DRIVES the judgment layer.** Finding A FULLY RESOLVED; aliasing-proof
  DISCHARGED for all 3 modules. **★ Reviewer observation (carry into P-029):** the
  measurement-vs-aesthetic thresholds (`stereo_width > 0.6`, `distinct <= 1`,
  `score < 55`) are correctly left hardcoded as physics/presentation, NOT producer taste
  — keep them OUT of the profile when P-029 threads the profile per-call. **P-028 is
  local-only** (commits `29b9dfe`, `72e98a7` on the dev branch on top of the P-027
  commits on top of the `e79426a` base), not pushed/merged at close.

- **★ P-025 DONE — the FOUNDATION of the producer-agnostic epic: today's
  hardcoded Halee/Ramone judgment is now a frozen, round-trip-guarded, UNWIRED
  `ProducerProfile`** (`build-os/receipts/P-025-producer-profile-schema-loader-halee-ramone-extraction.md`).
  `logic_mix_os/doctrine/producer_profile.py` (frozen dataclass + pure
  `load_profile()`) + `doctrine/producers/halee_ramone.json` (VERBATIM reference +
  honesty metadata stamp). Byte-identical round-trip guard (exact for clean
  constants incl. `KILL_SWITCHES[5:9]` with safety items 1–5 correctly EXCLUDED;
  indirect + non-vacuous for the inline-computed doctrine weights / 86.0 baselines
  / penalty_coeffs / default_creative_mode). The four judgment sources
  byte-unchanged; nothing consumes the profile; regression 68/68 UNCHANGED. Two
  commits `195127c` + `e6cb038`; suite 293 → 319 (+26). qa GREEN; reviewer pass
  (hand-verified every value byte-accurate); Codex unavailable (single-reviewer).

- **★★ THE MILESTONE — P-021 PROVES THE COWORK SURFACE IS AGENT-DRIVABLE
  END-TO-END; the canonical target is essentially MET at the decision-system level
  (THIRD step of the arc P-019→P-023) — DONE via P-021**
  (`build-os/receipts/P-021-verified-end-to-end-cowork-walkthrough.md`).
  **TESTS-ONLY — no product/runtime change; drives the already-built surface.**
  A full plan-only mixing session drives end-to-end THROUGH the cowork surface only
  (`build_context` + `run_command`), in `describe_session`'s canonical order, and
  the learning loop CLOSES within the surface. No honesty-clause gap found — every
  phase's essential command was reachable and the loop closed across the full
  session. **The driven spine (8 phases, via `run_command`, NOT bypassing to
  `analyze()`/`record_pass`):** intake→`intake_project`, classify→`classify_tracks`,
  diagnose→`detect_masking`, plan→`generate_mix_plan`,
  checklist→`render_logic_checklist`, validate→`validate_mix_pass`,
  record-outcome→`record_mix_pass` (LIVE), next-pass→`suggest_next_pass` (each
  JSON-serializable + shape-asserted). **The loop CLOSES (milestone assertion,
  load-bearing + non-tautological):** `record_mix_pass(..., reverted=True)` on the
  LIVE channel → a FRESH `build_context(memory_dir=...)` → `suggest_next_pass`
  surfaces the confirmed "Revert last pass" (evidence contains "confirm"), NO hand
  re-run. **Proven load-bearing** (qa AND reviewer independently — dropping
  `reverted`/routing off the live channel → the assertion FAILS; reviewer via
  monkeypatch) and **non-tautological** (the identical score-IMPROVED sequence with
  `reverted=False` surfaces NO revert). **Live-vs-dead pinned as an EXECUTABLE fact
  (resolves the carried P-020 clarity nudge):** `write_mix_decision` (DEAD ledger —
  writes only `decision_ledger.json`, runtime-verified) does NOT change next-pass;
  `record_mix_pass` (LIVE history) does — only `record_mix_pass` closes the loop.
  **Honest skips (none an essential linear phase):** `compare_to_reference` (needs a
  reference bounce → `{"note": "no reference supplied"}`), `override_track_identity`
  (param-heavy/mutating), `build_missing_tool`/`run_creative_engine`/
  `describe_session` (auxiliary/off-axis). **PRECISION (do NOT overstate):** the
  coverage-honesty test (`test_walkthrough_covers_the_registry_honestly`) guards
  PHASE-COMPLETENESS (every `describe_session` phase has a driven essential command
  belonging to that phase) + test-1's exact 8-phase order pin — it does NOT assert a
  full `driven ∪ skipped == 34` registry partition (it references 13 of 34). The full
  34-command exact-cover partition is guarded SEPARATELY by P-020's
  `tests/test_cowork_session_flow.py` (31 phases + 3 auxiliary = 34); together the two
  files tell the truth about registry coverage. **Single commit `dce156b`**
  (TESTS-ONLY; adds exactly one file `tests/test_cowork_session_walkthrough.py`, 8
  tests, +372; no product/runtime file changed, no existing test edited; single commit
  = tip, green in isolation = 277). **Proof:** suite **269 → 277 passed** (+8; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical, 0
  warnings** held; determinism confirmed (two contexts → byte-identical plan/next-pass);
  safety grep clean; UI N/A. qa **GREEN**; reviewer **pass** (empirically re-verified
  load-bearing via monkeypatch; genuine drive, not a bypass; honest skips). **Codex NOT
  available — single-reviewer verdict.** **★ SYNTHESIS:** the canonical target — "a
  tool Claude Cowork can use in Logic Pro," plan-only v1 — is essentially MET at the
  decision-system level; what remains is genuinely only transport packaging (**P-023**,
  MCP server vs documented raw-CLI, USER-GATED); **P-022 stays OPTIONAL/UNNEEDED** (no
  gap surfaced). **P-021 is local-only** (commit `dce156b` on the dev branch on top of
  the `6c40e2b` PR #15 base), not pushed/merged at close.

- **`describe_session` makes the cowork surface self-describing as an ordered,
  phase-grouped session flow (SECOND step of the arc P-019→P-023) — DONE via P-020**
  (`build-os/receipts/P-020-describe-session-flow-discoverability.md`). **PRODUCT-code
  feature; in-authority, additive, read-only (a grouping OVER the existing registry —
  no new product decision).** Adds a pure `_SESSION_FLOW` structure + a read-only
  `describe_session` command to the cowork `COMMANDS` registry (count **33 → 34**)
  that returns the SAME registry as `{"phases": [...ordered...], "auxiliary": [...]}`
  in the canonical order **intake → classify → diagnose → plan → checklist → validate
  → record-outcome → next-pass** (grounded in the README pipeline + the P-018/P-019
  record/validate steps). **31 commands** map onto the 8 linear phases; **3 are
  honestly `auxiliary`** — OFF the linear axis: `run_creative_engine` (parallel
  creative exploration), `build_missing_tool` (meta tooling-gap helper),
  `describe_session` (self-describing). **Honesty clause honored:** no fabricated
  flow; `suggest_next_pass` placed ONCE (in `next-pass`), not double-listed.
  **Completeness INVARIANT (the load-bearing guard):** every `COMMANDS` key appears
  EXACTLY ONCE across phases + auxiliary (exact cover — no orphan, no duplicate),
  keeping the flow honest as commands are added; proven load-bearing (orphan or
  duplicate → the invariant test FAILS), independently verified by qa
  (**31 + 3 = 34 = len(COMMANDS)**). **Additive / read-only:** `list_commands` /
  `run_command` / every existing handler are BYTE-UNCHANGED; `describe_session` is
  deterministic (byte-identical across calls) and DEEP-COPIES its output so callers
  can't mutate the module-level `_SESSION_FLOW`. **Single commit `942a68a`** (purely
  additive `cowork.py` +100, new `tests/test_cowork_session_flow.py` 10 tests, the
  one intended `test_cowork.py` count assertion 33→34; single commit = tip, green in
  isolation = 269). **Proof:** suite **259 → 269 passed** (+10; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held (additive read-only → goldens untouched); registry 34, no stale
  33 anywhere; safety grep clean; UI N/A; existing cowork + P-008/P-009/P-018/P-019
  tests green. qa **GREEN** (independent exact-partition verification 31+3=34).
  Reviewer **pass** — verified EVERY command placement against its real handler; the
  flow is truthful (two defensible judgment calls: `score_mix` and
  `compare_to_reference` placed in `plan`); the 3 auxiliaries are genuinely off-axis;
  the invariant is load-bearing. **Codex NOT available — single-reviewer verdict.**
  **Reviewer non-blocking flag → carried to P-021:** `write_mix_decision` (dead
  ledger) and `record_mix_pass` (live history) both sit under `record-outcome`, but
  the dead/live distinction is NOT surfaced in `describe_session`'s output — add a
  one-line clarity nudge in the P-021 walkthrough (see the Deferred section above).
  **P-020 is local-only** (commit `942a68a` on the dev branch on top of the `6c40e2b`
  PR #15 merge base), not pushed/merged at close.

- **`record_mix_pass` closes the learning loop INSIDE the cowork surface (FIRST
  step of the arc P-019→P-023 to a Cowork-usable end-to-end state) — DONE via
  P-019** (`build-os/receipts/P-019-record-mix-pass-closes-loop-in-cowork.md`).
  **PRODUCT-code feature; in-authority (reuses the already-live
  `record_pass`/`_apply_history` channel — no new product decision).** Adds a
  **`record_mix_pass`** command to the cowork `COMMANDS` registry (count **32 →
  33**). **The mechanism:** its handler (`cowork.py:97-106`) records a pass on the
  LIVE history channel — `ctx["memory"].record_pass(name, ctx["result"],
  reverted=...)` → `mix_pass_history.json` — passing through the P-018 `reverted`
  ground-truth flag (opt-in, default False), returning the record JSON; clean
  `{"error": "no memory_dir configured"}` when no memory dir (mirrors
  `_write_mix_decision`). So an agent driving through the cowork surface can now
  RECORD an outcome and see `suggest_next_pass` change WITHOUT leaving the surface —
  the read/write cowork surface is symmetric (the READ side was already live via
  P-009). Routes to the LIVE channel, NOT the dead decision ledger. **One surface
  finding, resolved minimally (NOT a wall):** the cowork `--params '{...}'` path
  unpacks user JSON into `run_command(name, ctx, **params)`, so a handler param
  named `name` collided with the dispatcher's positional `name`; fixed by making
  the dispatcher's `name`/`ctx` **positional-only** (`run_command(name, ctx, /,
  **params)`) — behavior-preserving (repo-wide grep found ZERO callers passing
  `name=`/`ctx=` by keyword; the sole product caller `cli.py:237` passes
  positionally). **Two commits (≤2):** `b7572b7` Commit-1 (handler + registry row +
  positional-only + unit tests; test-first, green in isolation = 257) + `de5679f`
  Commit-2 (no-re-run liveness guard). `cowork.py` is the only product file touched.
  **Proof:** suite **253 → 259 passed** (+6; 0 failed/skipped/warnings, green under
  `-W error`); regression **68/68, 0 critical, 0 warnings** held (opt-in memory path
  → goldens untouched; byte-identical default). **LIVENESS proven load-bearing (the
  P-016/P-018 lesson honored):** `test_loop_closes_through_cowork_no_rerun` records
  a confirmed revert via `run_command("record_mix_pass", ...)` on a score-IMPROVED
  override case, then a FRESH `build_context(memory_dir=...)` →
  `run_command("suggest_next_pass")` surfaces the confirmed "Revert last pass" — NO
  hand re-run. Both qa and reviewer INDEPENDENTLY broke the wiring (handler off the
  live channel) → FAILS; restored → PASSES. **Routes to the live channel (runtime
  probe):** only `mix_pass_history.json` created, never `decision_ledger.json`.
  **Byte-identical default:** date-neutralised canonical JSON equal to standalone
  `memory-record`. Registry 33, no stale 32. Scope: only 3 files (`cowork.py`
  additive, `test_cowork.py` count assertion 32→33, new `tests/test_cowork_record.py`);
  `memory.py`/`cli.py`/`pipeline.py`/ledger/creative/governance UNTOUCHED;
  P-008/P-009/P-018/existing-cowork tests green. Safety grep clean; UI N/A. qa
  **GREEN** (mutation-verified liveness + non-tautological override + live-channel
  routing probe). Reviewer **pass** (handler correct + routes live [verified by
  breaking it]; positional-only safe/minimal; loop closes through cowork;
  non-tautological override case). **Codex NOT available — single-reviewer
  verdict.** **P-019 is local-only** (commits `b7572b7`, `de5679f` on the dev branch
  on top of the `6c40e2b` PR #15 merge base), not pushed/merged at close.

- **Confirmed-revert outcome feeds the live next-pass loop (the FIRST
  confirmed-outcome signal in the learning loop) — DONE via P-018**
  (`build-os/receipts/P-018-confirmed-revert-feeds-next-pass-loop.md`).
  **PRODUCT-code feature; a PIVOT off the complete judgment-tuning path onto the
  learning-loop / feedback frontier** (user said "Yes"); orchestrator-routed;
  **OVERRIDE semantics chosen by the orchestrator-in-chief (user may redirect at
  the merge gate).** Until now every loop signal was score-INFERRED; P-018 adds a
  CONFIRMED one. **The mechanism:** an opt-in `memory-record --reverted` records a
  confirmed operator revert on a pass (`record_pass(..., reverted=True)` →
  `mix_pass_history.json`); the live `_apply_history` consumer (already threaded to
  real `analyze(--memory-dir)` via P-009) then, on a confirmed revert, DEMOTES the
  recommended-then-reverted moves and surfaces exactly ONE confirmed "Revert last
  pass" item at priority 95 — **regardless of the score-delta `got_worse`
  inference (OVERRIDE)**, with an early return that prevents double-up with the
  score-inferred revert candidate; distinct honest evidence line (contains
  "confirm", vs the score-inferred "recorded revert candidate(s): …").
  **OVERRIDE rationale:** a confirmed operator revert is GROUND TRUTH and outranks
  the heuristic proxy (Halee/Ramone operator-serving judgment). **Why THIS seam:**
  the decision LEDGER (`add_decision` → `decision_ledger.json`) has ZERO
  analyze-path consumers (display-only, `cli.py:315`), so any reserved-ledger-event
  producer would be INERT; the ONLY reachable LIVE seam was the history axis
  (`record_pass` → `_apply_history`) — hence the confirmed revert lands there.
  **Two commits (≤2):** `736fa8b` Commit-1 (`record_pass` `reverted` field +
  `_apply_history` override + 9 unit tests; test-first, green in isolation = 249) +
  `6134d27` Commit-2 (`--reverted` CLI wire + 4 no-re-run liveness/CLI tests).
  `memory.py`, `planners/next_pass_planner.py`, `cli.py` are the only product files
  touched. **Proof:** suite **240 → 253 passed** (+13; 0 failed/skipped/warnings,
  green under `-W error`); regression **68/68, 0 critical, 0 warnings** held (no
  `memory_dir` → falsy no-op → goldens untouched). **LIVENESS proven load-bearing
  (the P-016 lesson honored):** the no-re-run liveness test asserts on real
  `analyze(memory_dir=...)` `next_pass` and FAILS with the pre-P-018
  `_apply_history` (would be inert) and PASSES at tip — NOT inert. **OVERRIDE
  non-vacuous:** with an IMPROVED score delta (`got_worse` empty) but
  `reverted=True`, the confirmed "Revert last pass" still surfaces at rank 0 and
  the reverted move is demoted — override, not a score echo. **Byte-identical
  default:** no `--reverted` → next_pass identical to today; no `reverted` key when
  unused. **Scope clean:** ledger/`add_decision`/reserved ledger events, taste axis,
  `_KIND_SCORES`/creative/governance UNTOUCHED; P-008 `test_next_pass_history.py` +
  P-009 `test_live_wire.py` unedited and green (17). Safety grep clean; UI N/A. qa
  **GREEN** (independently mutation-verified liveness + non-vacuous override; qa
  self-flagged a transient stale-state artifact in one of its OWN scratch scripts —
  a qa-harness quirk, NOT a product defect — and confirmed the traced re-runs are
  authoritative). Reviewer **pass** (override bounded/deterministic; early-return
  skips only the score-inferred revert; demotes exactly the reverted pass's
  recommended moves; mutation-verified load-bearing). **Codex NOT available —
  single-reviewer verdict.** **Reviewer trajectory note (non-blocking, candidate,
  NOT staged):** a future outcome enum (`reverted`/`kept`/`refined`) would round
  out the loop — the `reverted: bool` field can widen to it WITHOUT breaking the
  byte-identical default. **P-018 is local-only** (commits `736fa8b`, `6134d27` on
  the dev branch on top of the `6c40e2b` PR #15 merge), not pushed/merged at close.

- **Base-value `_KIND_SCORES` re-curation (density → depth_cleanup) — RESOLVED as
  a VERIFIED NEGATIVE FINDING via P-017**
  (`build-os/receipts/P-017-doctrine-honest-kind-scores-recuration.md`).
  **User-signed-off ("A"); the FIRST attempt to change a base `_KIND_SCORES`
  value** (crossing the line P-012/P-015/P-016 held: they layered evidence nudges
  on an UNTOUCHED base). **FINDING: an honest re-curation of `depth_cleanup` CANNOT
  flip the `density` branch — arithmetically forced by the DOCTRINE (which dims are
  honestly movable), not a search failure. `_KIND_SCORES` LEFT UNTOUCHED — NO
  product change** (the honesty clause held; P-014 discipline). **The forced
  arithmetic:** `overall = mean(7 dims) − risk_penalty`; `depth_cleanup` 81.14
  (dim sum 568) vs `subtractive_drop` 85.29 (dim sum 597, low risk) → gap 4.14; the
  only doctrine-defensible under-valuation is `contrast` (dc 72 vs sd 88): →88 =
  83.43 (short 1.86), →100 (impossible ceiling) = 85.14 (STILL below); a FULL honest
  re-curation (contrast→88, technical→85, ramone→86, taste→86; halee stays 90=max,
  vocal_belief stays 86; **excitement LOCKED at 66**) reaches only 83.86 (short
  1.43); the entire residual deficit lives in `excitement` (66 vs 78), OFF-LIMITS to
  inflate (subtle depth work is honestly un-flashy) — the only flips require
  inflating excitement or re-labeling a depth pass as vocal-forward, both dishonest.
  **The committed guard (load-bearing, non-tautological):** the builder committed
  ONLY `tests/test_density_recuration.py` (NEW, 12 tests, +183, sole packet commit
  `1b03ad3`) pinning the 5-branch winner table UNCHANGED on the real `analyze()`
  path + the honest-ceiling arithmetic + `_KIND_SCORES` untouched; an injected
  inflated `depth_cleanup` (contrast=88+excitement=90, or all dims=100) makes it
  FAIL (density → density_A), so it genuinely catches an accidental/dishonest
  density flip. Committing executable arithmetic is defensible here (unlike P-014's
  no-commit finding) because the finding IS arithmetic and the variant-scoring path
  is golden-unguarded. **Before/after winner table (all 5 branches, real path)
  UNCHANGED:** chorus_lift→subtractive_drop 85.3; density→subtractive_drop 85.3;
  loop→subtractive_drop 85.3 (default); depth→depth_cleanup 81.1 (single-variant);
  vocal_belief→vocal_ride 82.9. **Proof:** suite **228 → 240 passed** (+12; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held; Commit-1 (the sole commit) green in isolation (new file alone
  12 passed); safety grep clean; UI N/A; P-012/P-013/P-015/P-016 test files NOT
  edited and pass (69). qa **GREEN — FINDING CONFIRMED**; reviewer **pass** (judged
  the finding doctrine-HONEST, not a masked search failure). **Codex NOT available
  — single-reviewer verdict.** **THE EQUILIBRIUM SYNTHESIS:** three levers converge
  — penalty (P-012/P-015, saturated: only vocal_belief gap 1.71<cap 2.0 flippable),
  reward (P-016, saturated at cap 4.0: only loop gap 3.43 reachable), base-value
  re-curation (P-017: density unflippable honestly) — **the judgment layer is at a
  DOCTRINE-HONEST EQUILIBRIUM; no honest further flip exists in the current
  dimension set.** The one open thread: is `subtractive_drop` itself over-valued? —
  a symmetric re-judgment, user-gated, un-signed-off, NOT staged. **P-017's guard
  commit `1b03ad3` is local-only** (dev branch on top of the `6c40e2b` PR #15
  merge), not pushed/merged at close.

- **Evidence-gated loop-deconstruct PROMOTION — the FIRST reward nudge — DONE via
  P-016** (`build-os/receipts/P-016-evidence-gated-loop-promotion.md`).
  **User-delegated PRODUCT-code change** (direction A "open the base-scoring
  decision space" + fork (i) "evidence-gated" + "keep skating"; the
  build-orchestrator routed). **This crosses the penalty-only line P-012/P-015
  held — the FIRST reward/promotion nudge.** **Two commits (≤2):**
  `b15b957` Commit-1 — `creative.py` (+88): `CREATIVE_PROMOTION_CAP = 4.0` (a
  SEPARATE constant from the ±2.0 penalty `CREATIVE_NUDGE_CAP`), a
  `_PROMOTION_TABLE` row (kind `loop_deconstruct`, evidence `foregrounded_loop`,
  `+35` excitement `= +5.0` raw clamped to exactly `+4.0`, verbatim reason), a
  `_foregrounded_loop` predicate reading the REAL wire (a `"foregrounded loop"`
  red_flag from `source_auditors` corroborated by `provenance` `high_risk`;
  getattr-defensive), and promotion application in `score_variant` (summed
  promotion overall-delta clamped to `+4.0`; `loop_promotion` reason appended to
  `score_nudges` on fire) + `tests/test_loop_promotion.py` (NEW, +233).
  **Green in isolation: 226 passed.** `a9f4e26` Commit-2 — the LIVE-WIRE:
  `pipeline.py` (+17/−3) relocates `analyze_provenance` + `audit_all` to just
  BEFORE `run_creative_engine` (a pure relocation — inputs already populated
  ~90 lines earlier) + two production-liveness tests (+70). **★ The P-009-style
  catch:** Commit-1's mechanism was INERT in production —
  `run_creative_engine` ran BEFORE `provenance`/`source_audits`, so the predicate
  always read empty evidence and the promotion NEVER fired in the real
  `analyze()` output; Commit-1's tests passed only because they RE-RAN the engine
  on the finished result. The orchestrator-in-chief caught it (the builder had
  mislabeled the ordering "by design"); Commit-2's live-wire fixed it, guarded by
  the two liveness tests that assert on the real `analyze()`
  `result.creative`/`result.governance` with NO re-run (FAIL pre-reorder, PASS
  after). **`_KIND_SCORES`, `CREATIVE_NUDGE_CAP`, the entire penalty table/path,
  and both existing predicates are byte-UNTOUCHED; `governance.py` has ZERO
  `provenance`/`source_audits` refs** → reorder SAFE BY CONSTRUCTION (backed
  by a 12-artifact byte-identical diff across all 3 seeded fixtures). **Behavior
  (qa-verified):** loop_deconstruct 81.9 → **85.9** (raw +5.0 clamped to
  exactly +4.0 = the cap binds, carries the `loop_promotion` line) >
  subtractive_drop 85.3 → **loop winner flips `loop_B` → `loop_A` by
  0.6** (governed winner also flips, no veto). **Load-bearing negative control:**
  no foregrounded-loop evidence → subtractive_drop wins (flip caused by the
  EVIDENCE). **Collateral:** ONLY the loop branch flips (chorus_lift/density still
  subtractive_drop — `subtractive_drop` now wins 2 branches, not 3, relieving
  anti_template; vocal_belief per P-015; depth unchanged); P-012/P-013/P-015 test
  files NOT edited and pass (58). **Proof:** suite **217 → 228 passed** (+11;
  0 failed/skipped/warnings, green under `-W error`); regression **68/68, 0
  critical, 0 warnings** (`loops_not_foregrounded` held); safety grep clean; UI
  N/A. **Reviewer pass** with a non-vacuity mutation check (emptying the promotion
  row → 5 promotion-dependent + 2 liveness tests RED, negative control GREEN;
  reverting ONLY the reorder → the 2 liveness tests RED) + a reward-creep
  watch-item; the `plan_depth` monkeypatch in the liveness test is a legitimate
  seam (real audit_all/analyze_provenance/run_creative_engine produce+consume the
  evidence, nothing faked). **Codex NOT available — single-reviewer
  verdict.** **P-016 is local-only** (commits `b15b957`, `a9f4e26` on the dev
  branch on top of `0f4e7e9`), not pushed/merged at close.

- **Make-the-nudge-decisive (masked-vocal near-tie) — DONE via P-015**
  (`build-os/receipts/P-015-decisive-masked-vocal-nudge.md`). **User-signed-off
  PRODUCT-code aesthetic change** (the user chose "Option 1 — Proceed, corrected",
  2026-06-30, after the orchestrator transparently corrected an arithmetic error —
  the old `−8` penalty only moves overall `−1.14`, insufficient to flip; the
  corrected mechanism strengthens to `−14`). The deliberate successor to P-012 and
  the resolution of the P-014 user-gated decision. **Single product commit
  `1756f61`** (product change + updated/new tests TOGETHER so Commit-1 is green in
  isolation, required because the change intentionally breaks old-behavior tests):
  `creative.py` `_NUDGE_TABLE` **row-0 only** — (1) exempt `intimacy_pass`
  (`kinds` `{width_bloom, vocal_ride, intimacy_pass}` → `{width_bloom,
  vocal_ride}` — an intimacy pass is the CORRECT response to a masked lead vocal,
  focused proximity not brute level/width), (2) strengthen `delta` `−8` → `−14`
  (`= −14/7 = −2.0` overall = EXACTLY `CREATIVE_NUDGE_CAP = 2.0`, unchanged, now
  binds `vocal_ride` too), plus an honest `−14` reason string, a doctrine comment,
  and a corrected stale clamp comment. `_KIND_SCORES`, the cap, row-1, the clamp,
  and both predicates are UNTOUCHED (verified by diff). **Behavior (qa-verified):**
  in the `vocal_belief` branch under a masked lead vocal, `vocal_ride` (vocal_A)
  82.9 → **80.9** (cap binds, overall_delta EXACTLY −2.0, carries the `−14`
  `score_nudges` line); `intimacy_pass` (vocal_B) 81.1 unchanged (exempt) →
  **winner FLIPS from vocal_ride to intimacy_pass** by 0.2. **Load-bearing negative
  control:** without `lead_masked`, vocal_ride wins (flip is caused by the masking
  evidence, not a base re-rank). **Bounded — no clear-ranking overturn:**
  `subtractive_drop` (85.3, penalty-immune) still wins `chorus_lift` / `density` /
  `loop` under `lead_masked` (gaps 3.4–4.2 ≫ 2×cap); ONLY the `vocal_belief`
  branch flips. **Tests (the binding guard — variant-scoring path golden-unguarded):**
  updated the ~existing P-012 cases in `tests/test_creative_nudges.py` (delta
  `−8`→`−14`, `intimacy_pass` now asserted EXEMPT, new reason, width_bloom worst
  case `−20` raw clamped to `−2.0`; added `test_intimacy_pass_exempt_from_lead_masked_nudge`
  + `test_vocal_ride_clamps_to_cap_under_lead_masked`) and ADDED
  `tests/test_decisive_nudge.py` (NEW, 8 tests: flip + load-bearing negative control
  + `test_only_vocal_belief_branch_flips_under_lead_masked` +
  `test_subtractive_drop_branch_does_not_flip_under_lead_masked`); no coverage
  deleted to turn red green. **Proof:** suite **207 → 217 passed** (0
  failed/skipped/warnings; changed files alone = 53 — `test_creative_nudges.py` 45,
  `test_decisive_nudge.py` 8); regression **68/68, 0 critical, 0 warnings** (doctrine
  golden held); Commit-1 green in isolation; safety grep clean (only a no-DAW
  docstring line); UI N/A. **Reviewer pass** — independently reproduced the
  arithmetic and ran a **mutation test confirming non-vacuity** (reverted both
  product edits → 5 binding tests went RED, the negative control correctly stayed
  GREEN → tests are load-bearing); confirmed scope discipline, no-overturn,
  evidence-line honesty, coverage not weakened. **Codex NOT available —
  single-reviewer verdict.** Non-blocking reviewer note: the mandated
  `Co-Authored-By: Claude Opus 4.8` trailer is a standing harness-required config
  tension, not a P-015 regression. **P-015 is local-only** (product commit `1756f61`
  on the dev branch on top of `0f4e7e9`), not pushed/merged at close.

- **Near-tie-creative-FLIP fixture — RESOLVED as a VERIFIED NEGATIVE FINDING via
  P-014** (`build-os/receipts/P-014-near-tie-creative-flip-fixture.md`). **No
  product code, no product/test commit.** The goal — prove the P-012 nudge is
  *decisive* and FLIPS the creative winner through `analyze()` on a genuine
  near-tie within the ±2.0 cap — is **structurally UNREACHABLE test-only** under
  the current `_KIND_SCORES` / `_NUDGE_TABLE`. The builder wrote ZERO code
  (honesty clause honored); qa adversarially tried to REFUTE it with THREE
  independent harnesses (builder inline-math + qa real-`score_variant` driver +
  a saturated worst-case `masking_report` with every classification the analyzer
  emits) — **all 0 flips** — and re-derived the arithmetic from source.
  Structural proof: `overall = mean(7 dims) − risk_penalty{low0/med6/high14}`,
  recomputed exactly as `score_variant`; base leaders are `generate_variants`
  literals keyed on `problem['id']` (fixture-invariant across 4 record sets);
  the **universal leader `subtractive_drop` (85.29) is penalty-immune** (in no
  `_NUDGE_TABLE` row), so `chorus_lift` / `density` / `loop` cannot reorder, and
  the **one sub-cap near-tie branch `vocal_belief`** (`vocal_ride` 82.86 vs
  `intimacy_pass` 81.14, gap 1.71) has BOTH hit by the identical row-0
  `lead_masked −8`, preserving the gap. **Headline reframing:** the P-012 nudge
  is a TRANSPARENCY/EVIDENCE layer — it moves the displayed governed
  `overall_score` and emits `score_nudges` but **can never reorder any branch**;
  P-013's option-(a) "cannot overturn a ranking" holds UNIVERSALLY (sharper than
  the P-012 "cannot overturn a *clear* ranking" framing). **Not a defect** — the
  nudge stays honest/bounded/penalty-only/evidence-tagged; decisive-when-close is
  latent until a user-gated curation change (see Deferred). **Suite 207 passed
  UNCHANGED; regression 68/68 held.** Commit-1-in-isolation N/A; `creative.py`
  unchanged since P-012 (`0df436c`); working tree clean; safety grep N/A.
  qa verdict **GREEN — FINDING CONFIRMED**; **Codex not available — single-reviewer
  verdict.** HEAD `596174d` (P-014 active-packet confirmation only; no product
  change). The P-014 harnesses live in scratchpad (not committed).

- **P-012 nudge proven on real data through `analyze()` (creative visibility
  fixture)** — **DONE via P-013**
  (`build-os/receipts/P-013-nudge-visibility-fixture.md`). **Tests-only** — one new
  file `tests/test_creative_nudge_visibility.py` (+154 lines, 5 tests); NO product
  code touched. Lifts the P-012 creative evidence-nudge from the unit level to the
  **live `pipeline.analyze()` production path**: on `dense_chorus_with_loops` the
  live masking analyzer emits a real `width_crowding` event, so the row-2 nudge
  (`vocal_belief −6`) fires on the `chorus_lift` `width_bloom` variant with no
  contrivance — overall_score (the governed-rank value) 75.7→**74.9** (movement
  −0.857, inside the ±2.0 cap), yet the winner stays `chorus_lift_B` (base gap ~9.6
  > 2× the cap). Builder chose **option (a)** — the cap binds, the winner does NOT
  flip — the documented latent-but-armed posture, now proven end-to-end. **Closes
  the golden-unguarded gap** on the variant-scoring path. Single tests-only commit
  `172cfd0`; suite 202→**207**; regression **68/68** held; Commit-1 green in
  isolation; safety grep clean (only hit a no-DAW docstring). Reviewer **pass** —
  independent negative control (disarmed `_apply_nudges` → 3 of 5 tests fail, so the
  assertions are load-bearing), independently recomputed the numbers, confirmed the
  Fixture #2 re-scope sound; **Codex not available — single-reviewer verdict.**
  Fixture #2 (taste-flip through `analyze()`) re-scoped to a POSITIVE alignment
  finding (taste structurally cannot flip a governed winner on curated data — see
  Deferred). P-013 is the **first post-merge packet** (PR #13 merged at `0f4e7e9`).
- **PR #13 (P-001…P-012 + canonical-alignment audit) MERGED to default** — merge
  commit `0f4e7e9` on `claude/dreamy-turing-z0oxll`. The whole P-001…P-012 line
  (including the option-B creative-scoring change) plus the AUDIT-2026-06-29
  canonical-alignment audit (verdict ALIGNED) is now on the default branch. The dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` was freshly restarted on top of
  the merge for post-merge work (P-013 onward).

- **Deeper creative scoring (option B, penalty-only)** — **DONE via P-012**
  (`build-os/receipts/P-012-creative-scoring-nudge-layer.md`).
  **The standing OPEN USER DECISION is resolved.** A bounded, transparent, capped,
  penalty-only evidence-nudge layer sits ON TOP of the curated `_KIND_SCORES`
  (values UNCHANGED): pure `_apply_nudges`/`_NUDGE_TABLE`; `vocal_belief −8` on a
  masked lead vocal (`bad_masking`) across `width_bloom`/`vocal_ride`/`intimacy_pass`
  (generalizing the old `width_bloom`-only caution); `vocal_belief −6` on
  `width_crowding` for `width_bloom`; summed overall delta clamped to
  `±CREATIVE_NUDGE_CAP = 2.0`; `score_nudges: [reason]` emitted only on fire.
  Deliberately NOT byte-identical when a nudge fires, but cannot overturn a clear
  base ranking (cap 2.0 < 2.4–4.2 gaps). Single product commit `0df436c`;
  suite 159→**202** (43 new); regression **68/68** held (variant path
  golden-unguarded — unit tests are the binding guard); Commit-1 green in
  isolation; CAP BINDS EXACTLY (75.7→73.7); NO RECOMMENDATION FLIP on the 3
  fixtures. Reviewer **pass** (adversarially proven — forced −70 raw still clamps
  to base−2.0; layer-ON vs OFF confirms non-tautological no-flip; Codex not
  available). **Awaiting the user's sign-off at PR #13 merge.** Reward nudges
  (rows 3+4) deferred; near-tie visibility fixture deferred.
- **Album delta consolidation / mean-derivation consolidation (P-011 candidate)**
  — **DONE via P-011**
  (`build-os/receipts/P-011-album-delta-consolidation.md`).
  **The two-place album-means truth is killed — single-sourced in `album.py`.**
  `album.py::analyze_album` additively emits per-song `brightness_delta` /
  `lufs_delta` (from the means it already computes); `cli.py::_run_album` consumes
  them and the duplicate `statistics.mean` recompute block (and the now-unused
  `import statistics`) is removed. VALUE-IDENTITY proven exact (emitted deltas ==
  `song − statistics.mean(non-None)` for all 3 fixtures, 0 mismatches; the `album`
  report's `coherence_score` / `outliers` / `verdict` unchanged). Commit-1
  `effccd0`; suite 155→**159**; regression 68/68 held; Commit-1 green in isolation.
- **CLI advisory float rounding (cosmetic, from P-010 reviewer)** — **DONE via
  P-011 Commit-2** (`build-os/receipts/P-011-album-delta-consolidation.md`).
  `next_pass_planner.py::_album_outlier_item` now applies `round(value, 2)` to the
  `"Album coherence"` **DISPLAY** delta text. **Display-only** — the outlier
  threshold logic still uses full precision (`0.151` trips `0.15`). Commit-2
  `ea9bebf`; 4 float-round tests in `tests/test_album_context.py`.
- **Album cross-song coherence** — **DONE via P-010**
  (`build-os/receipts/P-010-album-context-into-planning.md`).
  **MILESTONE — the cross-song coherence axis is now OPEN.** `analyze()` gained an
  opt-in `album_context: {brightness_delta, lufs_delta}`; an album-outlier song
  (thresholds 0.15 brightness / 3 LUFS, verbatim from `album.py:61,63`, not
  imported) receives ONE bounded, advisory, evidence-tagged `"Album coherence"`
  next-pass item at priority 45 (below every truth move — can never outrank Vocal),
  via a pure `_album_outlier_item`. The `album` CLI is now two-pass (pass 1 = album
  means via `analyze_album`; pass 2 = re-run each song with its derived delta) so
  the album report shows album-aware per-song guidance. **A song's plan now
  reflects its album siblings — the product is no longer strictly song-isolated.**
  Commits `dc61f20` (planner+pipeline+test, 10 tests) and `9ebd4ee` (CLI two-pass+
  test, 2 tests); suite 143→**155**; regression 68/68 held; Commit-1 green in
  isolation. NOTE: P-010 left the album means in two places — **resolved by P-011**.
- **Richer variant→track attribution** — **DONE via P-001**
  (`build-os/receipts/P-001-resolve-variant-track-attribution.md`).
- **Net-new `EVENT_TYPES` decision-ledger vocabulary** — **DONE via P-002**
  (`build-os/receipts/P-002-event-types-vocabulary.md`). `EVENT_TYPES` in
  `constants.py`, optional validated `event_type` on `add_decision`,
  `record_plan_decisions` tags `mute_candidate`, new test added.
- **Readiness-vs-refusal ledger-status UI clarity** — **DONE via P-003**
  (`build-os/receipts/P-003-readiness-vs-refusal-clarity.md`). Labelled
  `READY TO STOP` / `NOT YET — keep iterating` blocks in
  `operator_view.py::render_status` and the `html_dashboard.py` governance card,
  sourced from `result.governance["stop_conditions"]`; 5 new render-only tests.
  Render-only; no backend reach-in.
- **Event-tagging follow-up (from P-002) — in-scope part** — **DONE via P-004**
  (`build-os/receipts/P-004-event-tagging-mix-decision.md`). The one existing
  untagged ledger write (`cowork.py::_write_mix_decision`) now passes
  `event_type="mix_decision"`. **EVENT_TYPES is now applied to every EXISTING
  ledger write:** `mute_candidate` (via P-002's `record_plan_decisions`) and
  `mix_decision` (via P-004's `_write_mix_decision`). The other vocabulary
  members (`taste_feedback` / `validation_check` / `revert` / `manual_note`) have
  no existing producer and are tracked as net-new packets under Deferred above —
  NOT part of this DONE item.
- **`creative_renderer` readiness follow-up (from P-003)** — **DONE via P-005**
  (`build-os/receipts/P-005-creative-renderer-readiness.md`).
  `creative_renderer.py::render_governance`'s `## Stop Conditions` section now
  renders P-003's labelled `READY TO STOP` / `NOT YET — keep iterating` block in
  **markdown** (full `reasons` list, warning-when-ready), replacing the flat
  boolean dump at `creative_renderer.py:104`. Render-only; markdown-clean (no
  HTML); 2 new render-only tests; suite 108→110.
  **MILESTONE — surface consistency closed:** the readiness-vs-refusal treatment
  is now CONSISTENT across all THREE governance surfaces — `operator_view.py`
  (text, P-003), `html_dashboard.py` (HTML, P-003), and `creative_renderer.py`
  (markdown, P-005). The P-003 surface-consistency thread is **fully closed**.
- **`creative.py` literal cleanup** — **DONE via P-006**
  (`build-os/receipts/P-006-creative-literal-cleanup.md`). The two pre-existing
  un-resolved literals in `generate_variants` are now record-backed: Site 1
  (`creative.py:194`, `chorus_lift_B`) `loops or supporting[-1:]` →
  `_resolve(loops, supporting[-1:], [r["name"] for r in records][:1])` (closes the
  empty-`tracks_affected` path, restores P-001's non-empty + real-record-subset
  invariant, reuses the `_resolve` seam); Site 2 (`creative.py:217`, `loop`
  branch) replaces the `"the loop"` literal with a real-record-name fallback.
  Single product commit `6e98a3b`; suite 110→112; 2 new tests.
  **Every `tracks_affected` site in `generate_variants` is now record-backed and
  non-empty**, and loop-branch prose can no longer name a non-existent track
  (except under a degenerate record-free input — see Known risks below).
- **Taste profile feeds governance** — **DONE via P-007**
  (`build-os/receipts/P-007-taste-feeds-governance.md`). The recorded operator
  taste profile (`memory._derive_taste` statements) now **biases variant
  governance** — opt-in, bounded, evidence-tagged. An optional `taste_profile`
  arg (default `None`) on `govern_variant` / `govern_branches` / `run_governance`;
  a pure `_apply_taste` helper + `_TASTE_KIND_BIAS` map (verbatim `_TASTE_MAP`
  statements); `TASTE_MAX_DELTA = 15` (`< 30`, the truth nudge); a
  `taste_adjustments` evidence field present **only** when an adjustment applies.
  Two operators with different taste now get different governed winners from the
  same song (proven: narrower taste flips `chorus_lift_A` → `chorus_lift_C`).
  Single product commit `bd08f28` (`governance.py` +75/−6,
  `tests/test_governance_taste.py` new, 13 tests); suite 112→125; regression
  68/68 held; default path byte-identical (the HARD backward-compat gate).
  **This was the FIRST closure of the learning loop (the *consumer* half).**
- **`drum_room_bloom` narrower-taste test gap (from P-007)** — **DONE via P-008
  (Commit-2 `dbf94c3`).** The `drum_room_bloom` path in
  `governance._TASTE_KIND_BIAS` was data-symmetric with `width_bloom` but
  untested; a mirror of `test_narrower_taste_lowers_width_bloom_identity_bounded`
  was folded into `tests/test_governance_taste.py` (additive). Closed.
- **History-aware next pass (THE OUTCOME SIDE OF THE LEARNING LOOP)** — **DONE via
  P-008** (`build-os/receipts/P-008-history-aware-next-pass.md`). `plan_next_pass`
  now consumes recorded mix-pass history — opt-in, bounded, evidence-tagged. An
  optional trailing `history` arg (default `None` → byte-identical); a
  `_MOVE_TARGET` map bridges history's score-keyed `got_worse` to titled
  candidates; a move whose target regressed AND was recommended last pass is
  **demoted** (`HISTORY_DEMOTE = 40`, floored ≥ 0, survives — not deleted); a
  single non-destructive `"Revert last pass"` move surfaces at priority 95 when
  `revert_candidates` is non-empty; each history-touched candidate carries an
  `evidence` line (absent otherwise). Uses only `history[-1]`. Deterministic.
  Commit-1 `d98a194` (planner + new `tests/test_next_pass_history.py`, 12 tests),
  Commit-2 `dbf94c3` (drum_room_bloom test); suite 125→138; regression 68/68 held;
  default path BYTE-IDENTICAL three ways; Commit-1 green in isolation. Reviewer:
  **pass** (revert at 95>90 ruled acceptable — bounded/non-destructive/cannot
  manufacture a move; Codex not available). **This was the SECOND closure (the
  *outcome* half).**
- **P-007b — Live opt-in taste surface** — **DONE via P-009** (subsumed). The real
  per-operator `taste_profile` from `memory_dir` is now wired into the production
  analysis path: `analyze(..., memory_dir=...)` threads
  `taste_profile()["profile"]` into `run_governance`, and `cowork.py:28` passes
  `memory_dir` so the live `cowork --memory-dir` CLI run personalizes governance.
  The byte-identical-by-default guarantee survives (default `memory_dir=None` →
  `_taste=None` → existing no-op). Receipt:
  `build-os/receipts/P-009-live-wire-memory-into-analyze.md`.
- **P-008b — Live history wire** — **DONE via P-009** (subsumed). `memory.history()`
  is now threaded into `pipeline.analyze()` → `plan_next_pass` so a real recorded
  history reaches the planner in production; the live `cowork --memory-dir` run
  history-demotes regressed moves / surfaces revert. The byte-identical-by-default
  guarantee survives (default `memory_dir=None` → `_history=None` → existing
  no-op). Receipt: `build-os/receipts/P-009-live-wire-memory-into-analyze.md`.
- **Live wire — real memory into the production analysis path (THE LOOP IS NOW
  REAL IN PRODUCTION)** — **DONE via P-009**
  (`build-os/receipts/P-009-live-wire-memory-into-analyze.md`). `analyze()` gained
  an opt-in trailing `memory_dir`; when set it builds `ProjectMemory` once and
  threads `history()` → `plan_next_pass` and `taste_profile()["profile"]` →
  `run_governance`; `cowork.py:28` passes `memory_dir` so the pre-existing CLI
  `cowork --memory-dir` chain is live. Single product commit `27bfebf`; suite
  138→**143**; regression 68/68 held; **default path BYTE-IDENTICAL** (full
  `ProjectAnalysis` exact string-equal three ways — the `"evidence"` keys are
  pre-existing baseline fields, not a leak); Commit-1 green in isolation; safety
  grep clean. Reviewer: **pass** (taste axis ruled genuinely live — flows e2e +
  lowers identity; no winner flip on this fixture is a data property, decision-level
  flip proven by P-007's unit test on the same `analyze()`-driven path; Codex not
  available).
  **MAJOR MILESTONE — THE LEARNING LOOP IS NOW REAL IN PRODUCTION.** A real
  `cowork --memory-dir` run both **learns** (records → history-aware next pass)
  and **personalizes** (taste → governance). P-009 subsumes and completes
  **P-007b + P-008b**. The full arc **P-007 (consumer) → P-008 (outcome) → P-009
  (live wire)** is closed end-to-end.

## Stale / not-real (verified by orchestrator — do NOT act on as written)

- The following inherited follow-ups reference architecture that has **ZERO
  matches in this repo** and should be treated as stale: `LogicActionPayload`
  (multi-parameter), a real adapter narrowing `supported_action_types`,
  `RealLogicSessionAdapter`, dead `_RISK_HINTS` cleanup, adding to an existing
  `EVENT_TYPES` enum, full `Gravito` adapter, standalone `compare-variants`
  alias. That architecture does not exist here — verified by grep (0 matches).
  NOTE: P-002 delivered `EVENT_TYPES` as **net-new** flat vocabulary (not "added
  to an existing enum"); the stale "existing enum" framing remains wrong.
- A prior chat handoff referenced git state (a `main` branch, PR #12, branch
  `claude/hardening-11-…`) that does NOT match this repo on disk — there is no
  `main`; default is `claude/dreamy-turing-z0oxll`. Treat any inherited
  SHA/PR/packet-number claims as unverified until checked against `git`.

## Known risks / debt

- **Variant-scoring path is golden-unguarded (reinforced by P-012, P-015):**
  `regression.py` reads `doctrine_score`, never `score_variant`, so the 68/68
  golden cannot catch a `creative.py`/`score_variant` change. **Unit + visibility
  + flip tests are the binding guard** for any creative-scoring touch (P-012's
  `tests/test_creative_nudges.py` safety-invariant suite, P-013's
  `tests/test_creative_nudge_visibility.py` driving the live `analyze()` path, and
  P-015's `tests/test_decisive_nudge.py` pinning the masked-vocal flip). Treat any
  future creative-scoring change as test-binding, not golden-binding. Watch-item:
  P-015's flip margin is thin (0.2) but fully pinned — a future re-curation would
  surface as a RED test, not a silent re-rank.
- **Degenerate empty-`records` input (low priority — NOT a packet yet):** under a
  truly **empty** `records` list (an unconstructible / degenerate input on the
  engine path), P-006's Site 1 still returns `[]` and Site 2 still yields
  `"the loop"`. Acknowledged by the reviewer as out-of-scope — a possible future
  guard, not a defect. Raise as a packet only if a record-free engine path
  becomes constructible.
- Test env: numpy + pytest are not preinstalled. The full suite requires
  `pip install -e ".[dev]"` from `logic-mix-os/` (a network install) before
  `python -m pytest`.
- **Commits on this branch are unsigned.** The configured SSH signing key
  (`/home/claude/.ssh/commit_signing_key.pub`) is an empty 0-byte file and the
  container runs as `root`, so signing is impossible. Author + committer are
  correctly `noreply@anthropic.com`; GitHub will show these commits as
  "Unverified" (missing signature only, not a misattribution). This is an
  environment limitation, not a fix-it item.

## Open boundaries (awaiting explicit go)

- **P-031's product commits `51a107c` + `4af24e2` are PUSHED to the dev
  branch; the review-fix `b869ebd` is local-only as of this close** (this
  archivist close did not push; the orchestrator owns the build-os close
  commit + the standing dev-branch push — NO merge). They sit on the dev
  branch `claude/logic-mix-os-hardening-12-7hbeh1` atop the set-active
  `4d4b57d` (→ `4c6285b`, P-032f close), with the whole producer-agnostic
  epic (P-025 → P-029 → P-032e/a/b/d/c/g/f → P-031) still un-landed on
  default — merge base `e79426a` (PR #16). Any PR / merge into the protected
  default needs the user's explicit go. No merge / deploy / secret action
  taken in this close.

- **P-032c's product commit `ab14ac7` is local-only as of this close** (this
  archivist close did not push; the orchestrator owns the build-os close commit
  + the standing dev-branch push — NO merge). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` atop the build-os doctrine pin
  `b7e116a` and the set-active `fe5f6b4`, with the whole producer-agnostic epic
  (P-025 → P-029 → P-032e/a/b/d/c) still un-landed on default — merge base
  `e79426a` (PR #16). Any PR / merge into the protected default needs the
  user's explicit go. No merge / deploy / secret action taken in this close.
  P-032f remains ★ USER-GATED (explicit go needed on the "masked chop/stack =
  acceptable-blend" aesthetic rule + the conservative
  protect-as-lead-when-uncertain default).

- **P-032d's product commit `8a81516` is local-only as of this close** (this
  archivist close did not push; the orchestrator owns the build-os close commit
  + the standing dev-branch push — NO merge). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` atop the set-active `8c03f14`, with
  the whole producer-agnostic epic (P-025 → P-029 → P-032e/a/b/d) still
  un-landed on default — merge base `e79426a` (PR #16). Any PR / merge into the
  protected default needs the user's explicit go. No merge / deploy / secret
  action taken in this close.

- **P-029's product commits `42d6ebd`, `ea1aaa9` are local-only as of this close**
  (this archivist close did not push). They sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `e79426a` (PR #16) merge
  base — THE PIVOT: `analyze(producer=…)` selects the profile (byte-identical by
  default). The build-os-only close commit is separate. The accumulated
  producer-agnostic epic (P-025 → P-029) plus the earlier local-only arc remain
  un-landed on default. Any push of the product commits — and any subsequent PR /
  merge into the protected default — needs the user's explicit go. No push / merge /
  deploy / secret action taken in this close.

- **P-017 closed with NO product-code change (verified negative finding).** The
  ONLY committed change is the tests-only characterization guard
  (`tests/test_density_recuration.py`, commit `1b03ad3`) plus the `fecc4e5`
  active-packet confirmation and this build-os close. All sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge.
  **`1b03ad3` is local-only at this close.** Any push of it — and any subsequent
  PR / merge into the protected default — needs the user's explicit go. No push /
  merge / deploy / secret action taken in this close.
- **P-016 is now MERGED to default via PR #15** (merge commit `6c40e2b`, the current
  default-branch tip and the base for P-017). The earlier P-016 dev commits
  (`b15b957`, `a9f4e26`) are landed on default via that merge. That boundary is
  resolved. (Earlier stale note said "P-016 local-only on `0f4e7e9`" — superseded.)
- **P-014 closed with NO product/test commit (verified negative finding).** Only
  the build-os memory advance (this close) and the prior `596174d` active-packet
  confirmation sit on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1` on
  top of the `0f4e7e9` merge. Nothing product-side to push. Any push, and any
  subsequent PR / merge into the protected default, needs the user's explicit go.
  No push / merge / deploy / secret action taken in this close.
- **PR #13 is MERGED** (merge commit `0f4e7e9`) — the earlier local-only product
  commits (P-005…P-012: `0df436c`, `effccd0`, `ea9bebf`, `dc61f20`, `9ebd4ee`,
  `27bfebf`, etc.) are now landed on the default branch via that merge. That
  boundary is resolved.
- **P-013's tests-only product commit `172cfd0` is local-only as of this close**
  (this archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9` merge. Any push
  of it — and any subsequent PR / merge into the protected default — needs the
  user's explicit go. No push / merge / deploy / secret action taken in this close.
- **P-015's product commit `1756f61` is local-only as of this close** (this
  archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `0f4e7e9` merge — the
  user-signed-off masked-vocal-nudge change. The orchestrator pushes the dev branch
  separately. Any push of it — and any subsequent PR / merge into the protected
  default — needs the user's explicit go. No push / merge / deploy / secret action
  taken in this close.

- **P-019's product commits `b7572b7`, `de5679f` are local-only as of this close**
  (this archivist close did not push). They sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge
  base — the additive `record_mix_pass` cowork command (byte-identical by default).
  The build-os-only close commit is separate. Any push of the product commits — and
  any subsequent PR / merge into the protected default — needs the user's explicit
  go. No push / merge / deploy / secret action taken in this close.

- **P-020's product commit `942a68a` is local-only as of this close** (this
  archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge
  base — the additive, read-only `describe_session` cowork command + `_SESSION_FLOW`
  (byte-identical to every existing command). The build-os-only close commit is
  separate. Any push of the product commit — and any subsequent PR / merge into the
  protected default — needs the user's explicit go. No push / merge / deploy / secret
  action taken in this close.

- **P-021's tests-only commit `dce156b` is local-only as of this close** (this
  archivist close did not push). It sits on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `6c40e2b` (PR #15) merge
  base — the MILESTONE end-to-end walkthrough (adds exactly one file
  `tests/test_cowork_session_walkthrough.py`, +372; no product/runtime change, no
  existing test edited). The build-os-only close commit is separate. Any push of the
  commit — and any subsequent PR / merge into the protected default — needs the
  user's explicit go. No push / merge / deploy / secret action taken in this close.

- **P-025's product commits `195127c`, `e6cb038` are local-only as of this close**
  (this archivist close did not push). They sit on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` on top of the `e79426a` (PR #16) merge
  base — the `ProducerProfile` schema + `load_profile()` + extracted
  `halee_ramone.json` reference (data + loader + tests only; COMPLETELY UNWIRED —
  the four judgment sources byte-unchanged, regression 68/68 UNCHANGED). The
  build-os-only close commit is separate. Any push of the product commits — and any
  subsequent PR / merge into the protected default — needs the user's explicit go.
  No push / merge / deploy / secret action taken in this close.

---
_Append-only working notes. Last advanced on P-038 close (2026-07-02) — residue sweep 2 of 2 (naming/prose) resolves the six items (each marked ✓ in place; the TRAILER-SPEC note resolved in Fable 5's favor for the batch); ★★★ THE RESIDUE LIST IS ZERO — accepted standing notes only (the `examples/sample_output/` doc-refresh decision; the duplicated trailer block in `7b9eda7`'s raw message; the push-state observation), with the two named lessons retained for posterity (raw-dict NaN comparisons fail open; defense claims need mutation tests). **THE OPEN USER GATE: the batch merge — P-036 + P-037 + P-038 (+ closes) onto merge base `dc921ec` (= PR #18) — on the user's explicit word.**_
