# Receipt — P-037: residue sweep 1 of 2 — the code-behavior sweep (defensive fixes + validation tightening), byte-identical

- **Packet:** P-037 — residue sweep 1 of 2 (CODE-BEHAVIOR): six
  defensive/validation items from `residue.md`, byte-identical on every
  artifact surface (4 fixtures × 2 producers).
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer **fix-then-pass → PASS** (one
  fix round, fully resolved).
- **★ THE REAL FINDING: NaN floors previously FAILED OPEN on raw dicts**
  (`confidence < nan` is False → blend accepted; −0.5/−inf accepted
  everything) — now fails CLOSED, verified at base by builder, qa, AND
  reviewer independently.

## Scope

**In (the six residue items, all from residue.md):**

1. **`logic_action_generator.py` identity-derived lead matching** —
   consolidated with creative onto ONE shared `lead_vocal_names()` basis
   (in `vocal_type_classifier`); **zero name-based "vocal" substring-match
   sites remain**.
2. **`producer_profile._validate` tightening** — `search_modes` non-empty;
   `default_creative_mode`'s three hard-dereferenced keys
   (`intimate_truth_words` / `intimate_mode` / `default_mode`) present with
   sane types; `confidence_map` rejects duplicate areas and enforces the
   exact entry key set {area, level, reason}; non-finite
   `confidence_floor` rejected explicitly (`math.isfinite`).
3. **The raw-gate floor self-guard** — `accepted_blend_under_policy`
   requires a real, finite floor in [0, 1] before the comparison; an
   out-of-contract floor now REFUSES blend (fails closed). THE REAL
   FINDING — see above.
4. **`lead_names` identity-derived in `_vocal_role_fit`** — derives from
   `instrument_identity == "lead_vocal"`, never the classifier's
   `vocal_type` field; identical on all pipeline data. **The mangle pin:**
   old behavior double-penalized a hand-mangled lead — 60.0 → new 70.0
   baseline with zero clarity lines (conscious flip, new test).
5. **The groove defensive snapshot** — `expanded["groove"]` is a pristine
   deepcopy of doctrine's input, equal but never an alias;
   `analyze_groove` still runs exactly once (compute-once intact). **The
   fix-then-pass round lived here** — see below.
6. **`JUDGMENT_WORDS` word-boundary + plural-suffix matching**
   (`\b{w}(?:e?s)?\b`) via one shared `judgment_word_hits` helper; 9–10
   guard sites migrated; "fixture" freed / "fix" + "fixes" + "problems"
   caught; other inflections consciously OUTSIDE the closed vocabulary
   (extend explicitly, never stem-guess).

**Explicitly out:**

- Every emitted byte (proven — byte-identity 240/240, twice).
- The naming/prose items — the three producer-named-VALUE surfaces, the
  liveness-docstring sweep, cli.py `--mode` help text, the P-035 count-pin
  parenthetical tidy, fallback-reason wording, the two P-036
  observations — ALL P-038's (residue sweep 2 of 2).

## Commits and base

- **1 + 1 review-fix (≤2 rule satisfied), both PUSHED to the dev branch
  (orchestrator standing go), NOT merged:**
  - `cb566b1` — "P-037: residue sweep 1 of 2 — code-behavior defensive
    fixes, byte-identical" — the six items; 14 files, 432+/48−.
  - `5f94456` — "P-037 fix: take the groove snapshot before doctrine
    consumes it" — the review-fix: the snapshot moved BEFORE
    `score_doctrine` + the load-bearing mutation-test pin + the amended
    `_groove_coherence` docstring; 3 files, 83+/17−.
- **Parent:** `4df134c` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `dc921ec` (= PR #18, the
  default-branch tip). Verified: `git merge-base HEAD dc921ec` = `dc921ec`.
- The branch now carries **P-036 + P-037** (+ closes) atop `dc921ec`.

## ★ The fix-then-pass round (reviewer must-fix, all on item 5)

- **The finding:** the groove copy as first shipped ran AFTER
  `score_doctrine` returned — it could not deliver the defense it claimed
  (a doctrine mutation during scoring would already be IN the copied dict).
- **The fix (`5f94456`):** the pristine deepcopy snapshot is taken
  immediately after `analyze_groove` returns, BEFORE `score_doctrine`;
  doctrine keeps the live dict, `expanded["groove"]` gets the snapshot.
- **Load-bearing verified BOTH directions:** the new mutation test (a
  `score_doctrine` wrapper that mutates its groove arg) **FAILS under the
  old placement** — the reviewer reproduced the corruption
  (`overall_regularity` −999.0 inherited by the artifact) — and passes at
  HEAD. The defensive-copy pin now compares against a snapshot captured
  INSIDE the `analyze_groove` spy, never the post-doctrine live object.
- The stale "same object is reused" docstring claim amended (the third
  must-fix item).

## QA proof (GREEN, pre-fix tree `cb566b1`)

- **Suite:** 754 → **766** (+12). 0 failed/skipped.
- **Regression:** **93/93.**
- **Byte-identity:** **240/240** files via qa's OWN harness (4 fixtures ×
  2 producers, full `write_artifacts` trees, diff EMPTY vs base).
- **The fail-open confirmed REAL at base:** 7/7 probes (NaN/−0.5/−inf
  floors accepted blend at base; refused at HEAD).
- **Validation probes:** 14/14 (each malformed shape → ValueError); both
  shipped profiles load.
- **The shared `lead_vocal_names` basis verified fork-free.**
- **Commit-1 isolation:** `cb566b1` green in isolation (verified pre-fix;
  it was HEAD at qa time).
- **Safety grep:** clean. **UI smoke:** n/a (no UI surface in this packet).

## Post-fix proof (`5f94456`)

- **Suite:** **767** (+1 — the mutation test). **Regression 93/93.**
- **Byte-identity re-proven 240/240** by the builder AND spot-verified by
  the reviewer independently (diff EMPTY vs base `4df134c`).

## Reviewer verdict — fix-then-pass → PASS

- Three must-fix items (the snapshot placement; the pin must detect the
  threat; the stale docstring claim) — **all resolved as specified**,
  load-bearing verified both directions.
- **Codex NOT available — single-model review, BOTH rounds.**
- The fix-then-pass path (the P-031 precedent) used as designed.
- **★ A growing pattern worth naming (the second time a "defensive"
  change was caught not defending):** defense claims need MUTATION TESTS,
  not placement faith (P-037 items 3 and 5).
- **Benign observation recorded (qa):** the remote-ref updates on the
  branch are the orchestrator's standing-go session pushes, not
  agent-initiated pushes.

## Residue (carried to `build-os/memory/residue.md`)

- **✓ RESOLVED by this packet:** `logic_action_generator.py:38`; the
  validation-tightening cluster (`search_modes` non-empty,
  `default_creative_mode` structure, confidence_map dupes/extra-keys, NaN
  floors — loader AND raw gate); `lead_names` derivation; the shared
  groove dict; the JUDGMENT_WORDS "fix"-substring constraint.
- **NEW (named lesson):** raw-dict NaN comparisons FAIL OPEN
  (`x < nan` is False) — audit future raw-comparison gates for the same
  shape.
- **NEW (named lesson):** defense claims need mutation tests, not
  placement faith — twice now (P-037 items 3 and 5).
- **Remaining open packet-worthy residue = exactly P-038's list**
  (residue sweep 2 of 2 — naming/prose, the LAST backlog packet).

## Open boundaries

- **NOT merged.** The dev branch carries **P-036 + P-037** (+ closes) atop
  merge base `dc921ec` (PR #18). **The batch merge decision
  (P-036 + P-037 + P-038) is the user's call** after P-038 — no merge
  without explicit go.
- Pushes were the orchestrator's standing-go session pushes; no
  deploy/publish/secrets touched.
- **P-038 STAGED, not active** — activation on the orchestrator's
  confirmation (see `build-os/packets/active_packet.md`).
