# Receipt — P-038: residue sweep 2 of 2 — the naming/prose sweep (producer names off engine-emitted values)

- **Packet:** P-038 — residue sweep 2 of 2 (NAMING/PROSE): six items —
  producer names off engine-emitted VALUES + the honesty/precision tidies.
  **★ THE LAST BACKLOG PACKET — with this close the residue-sweep arc AND
  the entire post-merge backlog are COMPLETE; the residue list is ZERO**
  (everything remaining is an accepted standing note, recorded below).
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer **fix-then-pass → PASS** (one
  fix round: the missing mandated commit trailers — commit METADATA, not
  content — resolved by a tree-neutral amend).

## Scope

**In (the six items, all from residue.md / the confirmed packet spec):**

1. **(1a) Warning doctrine tags renamed off the producer names**
   (`phil_ramone_vocal_centrality` → `vocal_centrality`,
   `phil_ramone_restraint` → `restraint`) — found UNPINNED and never
   emitted on any fixture (the reviewer verified live that no fixture
   reaches those warning branches — why the goldens held); a NEW synthetic
   pin binds both payloads AND asserts no producer substring in any tag.
2. **(1b) Reference search-mode names renamed**
   (`halee_depth` → `spatial_depth`, `ramone_vocal_truth` →
   `vocal_truth`) — the full radius landed in ONE commit;
   `OLD_HARDCODED_MAP` kept VERBATIM as history with the P-033
   coincidence pin consciously adjusted
   (`dict(OLD_HARDCODED_MAP, intimate_mode="vocal_truth")` — the reviewer
   judged it honest: semantic identity modulo exactly the one visible
   rename).
3. **(1c) Engine action prose de-producer-named** ("Vocal belief:",
   "Naturalistic space:", "physical room lift", the source_auditors room
   line). **Profile JSON prose KEEPS its producer names** — profiles are
   named for producers; the engine is not.
4. **(2) The liveness-docstring sweep** — 6 files corrected to the
   empirically-true claim (liveness catches drop/threading sabotage; a
   hardcoded constant is caught by the value-discrimination guards — the
   reviewer validated this by live sabotage on `test_beat_identity`);
   4 candidate files verified accurate and untouched. The whole family is
   now corrected or verified-accurate.
5. **(3) `cli.py` `--mode` help de-hardcoded** — describes the semantics
   (a mode from the selected profile's `search_modes`; profile-owned
   default) instead of the reference's mode names.
6. **(4) The P-035 count-pin parenthetical tidy** — 21 sites shortened to
   a pointer; the ONE canonical explanation lives in `conftest.py`.
7. **(5) The `search_mode_fallback` reason now branch-accurate** —
   declared-default vs first-authored, the discriminator pre-existing and
   exact (AST-verified: no new logic).
8. **(6) Both profiles' blend-confidence reasons re-authored** (the two
   P-036 observations): the heard-qualifier appended (PAIRED with the
   masking_analyzer doc headline, as the residue note specified) + the
   65.0/85.0 attribution made explicit (the chop and the stack each draw
   the masked penalty once; the accepted blend waives both). Verbatim map
   pins strengthened; the P-036 pinned-OUT assertions retained.

**Explicitly out:**

- **Any behavior change** — zero, AST-verified (only string literals
  moved anywhere in the diff).
- **`examples/sample_output/` refresh** — it ships pre-P-036/P-038 prose
  (producer-named action strings, stale verdict text); not test-pinned,
  predates P-038. Consciously NOT expanded into this packet (the P-030
  precedent regenerated samples for a CONTRACT change; this is prose) —
  recorded as an accepted standing note / future doc-refresh decision.
- Merge/deploy/publish — the batch merge stays gated on the user.

## Commits and base

- **Single product commit (≤2 rule satisfied), PUSHED to the dev branch
  (orchestrator standing go), NOT merged:**
  - Originally `e1ddfbf`; **AMENDED TREE-NEUTRALLY to `7b9eda7`** —
    "P-038: naming/prose sweep — producer names off engine-emitted
    values". The amend was MESSAGE-ONLY: the mandated trailers were
    missing (the reviewer's one must-fix). Tree hash `b49c4b2d…`
    identical before and after, parent `6f7fd99` unchanged — so every
    content proof carried over without re-execution. Force-with-lease
    under the standing dev-branch go. **25 files, +201/−88.**
- **Parent:** `6f7fd99` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `dc921ec` (= PR #18, the
  default-branch tip). Verified: `git merge-base HEAD dc921ec` =
  `dc921ec`.
- The branch now carries the **COMPLETE BATCH — P-036 + P-037 + P-038**
  (+ closes) atop `dc921ec`.

## ★ The fix-then-pass round (reviewer must-fix — commit METADATA, not content)

- **The finding:** the mandated commit trailers
  (`Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link) were missing from `e1ddfbf`'s message — the
  reviewer's ONE must-fix; all content was already clean.
- **The fix:** a TREE-NEUTRAL amend (`e1ddfbf` → `7b9eda7`) — tree hash
  `b49c4b2d…` byte-identical before/after, parent `6f7fd99` unchanged, so
  the qa content proofs carried over without re-execution.
- **The re-check:** trailer-only re-check passed —
  `git interpret-trailers` clean. One cosmetic residue: the trailer block
  is duplicated verbatim in the raw message (dedup'd by tooling when
  displayed); judged NOT worth another force-push → accepted standing
  note.

## QA proof (GREEN)

- **Suite:** 767 → **768** (+1 — the synthetic warning-tag pin).
  0 failed/skipped.
- **Regression:** **93/93, goldens untouched** (zero golden files in the
  diff).
- **Artifact-delta enumeration verified TO THE LINE with qa's OWN
  harness:** **76 changed lines, all 1-for-1 replacements, 0
  unenumerated, 0 producer leaks** — 16 confidence surfaces +
  "Vocal belief:" ×32 + "Naturalistic space:" ×20 + physical-room-lift
  ×6 + the search-mode pair confined to reference × simple ONLY.
- **Score surfaces byte-equal ×8:** overalls 73.8 / 70.7 / 74.3 / 76.3
  (reference), 68.4 / 52.6 / 49.7 / 60.9 (timbaland).
- **Renames complete:** 2 residual `phil_ramone_` hits are explanatory
  comments — allowed category, reported exactly.
- **Commit-1 isolation:** single product commit — HEAD IS Commit-1 →
  green in isolation (the proof carried over the tree-neutral amend; the
  tree is identical).
- **Safety grep:** none. **UI smoke:** n/a (no UI surface in this
  packet).

## Reviewer verdict — fix-then-pass → PASS

- **All nine scrutiny points clean on CONTENT:** zero behavior change
  AST-verified (only string literals moved); the 1(b) radius fully
  landed; live verification that no fixture reaches the renamed warning
  branches (why the goldens held); the sabotage bit — reverting a tag
  FAILED the new synthetic pin.
- **The OLD_HARDCODED_MAP judgment call endorsed:** kept verbatim as
  history; the coincidence pin's conscious adjustment is honest —
  semantic identity modulo exactly the one visible rename.
- **The liveness-docstring correction validated empirically** by live
  sabotage on `test_beat_identity` (liveness catches drop/threading;
  discrimination catches hardcoding).
- **The one must-fix was commit METADATA** (the missing trailers) —
  resolved by the tree-neutral amend; trailer-only re-check passed.
- **Codex NOT available — single-model review, BOTH rounds.**

## Residue (carried to `build-os/memory/residue.md`)

- **✓ RESOLVED by this packet:** the three producer-named-VALUE surfaces
  (1a/1b/1c); the liveness-docstring family (ALL files now corrected or
  verified-accurate); cli.py `--mode` text; the count-pin parenthetical;
  the fallback-reason wording; the two P-036 observations; the
  TRAILER-SPEC standing note (resolved in Fable 5's favor for the batch).
- **★ RESIDUE: ZERO.** Accepted standing notes only (user-level, recorded
  not fixed):
  1. `examples/sample_output/` ships pre-P-036/P-038 prose — a conscious
     doc-refresh decision for a future moment.
  2. The duplicated trailer block in `7b9eda7`'s raw message (cosmetic).
  3. The push-state observation: remote-ref updates on the dev branch are
     the orchestrator's standing-go session pushes.
- **The two named lessons retained for posterity:** raw-dict NaN
  comparisons fail open; defense claims need mutation tests.

## Open boundaries

- **NOT merged. ★★ THE OPEN USER GATE: the batch merge —
  P-036 + P-037 + P-038 (+ closes) onto merge base `dc921ec` (= PR #18) —
  awaits the user's EXPLICIT word.** No merge without go.
- Pushes (including the force-with-lease for the tree-neutral amend) were
  under the standing dev-branch go; no deploy/publish/secrets touched.
- **No packet staged.** The system is coherent and shippable. Future arcs
  (a third producer, CLI producer exposure, deeper mode-forking in
  variant generation, the sample-refresh doc pass) are USER-INITIATED
  options, not debt.
