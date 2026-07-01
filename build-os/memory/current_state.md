# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

## ★ Architecture doctrine (USER-ISSUED, 2026-07-01 — standing, applies to every producer-profile packet)

> **Axes are shared measurable substrate. Taste is the weighting layer.
> Safety/governance is invariant.**

- Every new producer profile REUSES the same measured axes where possible, then
  changes: **weights, thresholds, promotion rules, penalty interpretation,
  recommendation language.**
- A profile NEVER changes: **safety, non-destructive guarantees, audit,
  rollback, source integrity.**
- The engine DETECTS agnostically; the profile DECIDES. (P-032g exemplar:
  engine says "dominant loop + low contrast = static / dominant loop +
  groove-carrying identity = iconic"; Halee/Ramone may deconstruct, Timbaland
  may protect — the reversal lives in JSON, never in engine code.)
- Axis semantics are RELATIONAL, not quantitative ("clean low-end relationship
  beats high low-end quantity"); scorer language stays neutral so different
  profiles can interpret the same axis differently (e.g. low-end: Timbaland =
  pocket/impact/negative-space/sub-kick relationship; Halee/Ramone =
  balance/natural foundation; modern pop = translation/controlled sub density;
  trap = sub identity/808 envelope/space around transient).
- The landed axes under this doctrine: beat_identity = fingerprint;
  negative_space = rhythmic absence; groove_coherence = pocket stability;
  rhythmic_surprise = movement/interruption; low_end_motion = kick/sub/room
  relationship (✓ landed, P-032c); loop_context = static-vs-iconic hinge
  (✓ landed, P-032g — THE HINGE: detection in the engine, the status→score map
  + the `protect_iconic_loops` gate decision in profile JSON).
- This is not a Timbaland profile being built — it is a producer-profile
  FRAMEWORK emerging under the Timbaland work.

## Project

- **What this repo is:** Logic Mix OS — a local-first, deterministic mix-decision
  system that turns exported Logic Pro stems + a `project_manifest.json` into a
  section-aware, Logic-native **mix plan** (Roy Halee / Phil Ramone judgment
  layer). Not an auto-mixer, preset generator, or mastering tool. All product
  code lives under `logic-mix-os/`.
- **Primary branch / base:** default branch `claude/dreamy-turing-z0oxll`;
  active dev branch `claude/logic-mix-os-hardening-12-7hbeh1`. **The accumulated
  cowork arc (P-017 guard + P-018 → P-023) is now MERGED to default via PR #16 —
  merge commit `e79426a`, which is the CURRENT default-branch tip and the base for
  P-025** (confirmed: `git merge-base HEAD e79426a` = `e79426a`; the P-025
  active-packet confirmation `4e9eaa2` sits directly on top of it). (Earlier
  bases: **PR #15** merge `6c40e2b` was the P-017 base; **PR #13** merge `0f4e7e9`
  landed P-001…P-012 + the canonical-alignment audit; the older shared ancestor is
  `694d19d`.) On top of the `e79426a` base the dev branch now carries the
  producer-agnostic epic: **P-025 (`195127c` + `e6cb038`, product — the
  `ProducerProfile` schema + pure `load_profile()` + the VERBATIM-extracted
  `halee_ramone.json` reference, byte-identical round-trip guard, honesty metadata
  stamp; COMPLETELY UNWIRED)** then **P-026 (`c4a092d`, product — creative.py
  sources its 8 producer-specific globals FROM `load_profile("halee_ramone")`, the
  hardcoded literals DELETED)** then **P-027 (`e4786ca` + `7b1c26d`, product —
  `governance.py` sources its producer-specific judgment from the profile AND the
  profile is WIDENED, per Finding A, with `taste_triangle` + `veto_thresholds`,
  now sourced too; the 5 SAFETY kill-switches STAY hardcoded — producer-agnostic;
  byte-identical, no-aliasing-proven; `doctrine_engine.py` / `pipeline.py`
  byte-unchanged, regression UNCHANGED)** then **P-028 (`29b9dfe` + `72e98a7`,
  product — `doctrine_engine.py` sources ALL 8 scorers' aesthetic constants from
  the profile: Part A sources the P-025-captured `weights` + `_halee`/`_ramone`
  baselines/coeffs, Part B WIDENS the profile with `doctrine.scorers` (5 function
  groups) and sources them; the PHYSICS/measurement code + presentation thresholds
  STAY hardcoded — producer-agnostic; byte-identical, no-aliasing-proven;
  `creative.py` / `governance.py` / `pipeline.py` byte-unchanged, regression
  UNCHANGED)** then **P-029 (`42d6ebd` + `ea1aaa9`, product — THE PIVOT:
  `pipeline.analyze(..., producer="halee_ramone")` accepts a name OR a
  `ProducerProfile` object, loads ONCE per call, and threads `profile=` to
  `score_doctrine` / `run_creative_engine` / `run_governance`, which thread it to
  ALL leaf scorers; each reads its producer-specific values from the PASSED
  profile, defaulting to the module `_DEFAULT_PROFILE` when `profile is None`;
  KILL_SWITCHES recomposed per call = 5 hardcoded SAFETY switches + the profile's
  aesthetic switches; byte-identical default, selection proven GENUINELY LIVE +
  load-bearing across all 3 layers; physics/analyzers untouched, regression
  UNCHANGED)**. **P-028 COMPLETED THE EXTRACTION PHASE and P-029 IS THE PIVOT — the
  profile is now a LIVE, SELECTABLE LEVER end-to-end.** The P-025 + P-026 + P-027 +
  P-028 + P-029 product commits are local-only (not pushed / merged). P-029's parent
  chain: `ea1aaa9` → `42d6ebd` → `d05105d` (active-packet confirmation) → `4fdae41`
  (P-028 close). P-028's parent chain: `72e98a7` → `29b9dfe` → `d5260a6`
  (active-packet confirmation) → `23850f7` (P-027 close). **★ ON TOP of P-029, the
    dev branch now also carries P-032e (`8239f42` + `9d6764e`, product — the FIRST
    NEW producer-agnostic doctrine axis `beat_identity`, strength-form, weight-0 for
    halee_ramone so byte-identical), local-only, base `6d34c30` = the P-029 close.
    P-032e's parent chain: `9d6764e` → `8239f42` → `2491f42` (active-packet
    confirmation) → `6d34c30` (P-029 close). ★ ON TOP of P-032e, the dev branch now
    ALSO carries P-032a (`3edcd9c`, single product commit — the SECOND new
    producer-agnostic doctrine axis `negative_space`, absolute arrangement
    room/sparsity, weight-0 for halee_ramone so byte-identical), local-only, base
    `6d34c30`, atop the set-active `836bd22`. P-032a's parent chain: `3edcd9c` →
    `836bd22` (active-packet confirmation) → `8a2892b` (P-032e close) → `9d6764e`.
    ★ ON TOP of P-032a, the dev branch now ALSO carries P-032b (`e9f793f`, single
    product commit — the THIRD new producer-agnostic doctrine axis
    `groove_coherence` PLUS the `analyze_groove` LIVE-WIRE relocation to before
    `score_doctrine`, weight-0 for halee_ramone so byte-identical), local-only,
    atop the set-active `bd98777`. P-032b's parent chain: `e9f793f` → `bd98777`
    (active-packet confirmation) → `3e991a5` (P-032a close) → `3edcd9c`.
    ★ ON TOP of P-032b, the dev branch now ALSO carries P-032d (`8a81516`,
    single product commit — the FOURTH new producer-agnostic doctrine axis
    `rhythmic_surprise` in its weak, section-aggregate form — cross-section
    transient-density variation (pstdev spread + largest adjacent swing),
    weight-0 for halee_ramone so byte-identical), local-only, atop the
    set-active `8c03f14`. P-032d's parent chain: `8a81516` → `8c03f14`
    (active-packet confirmation) → `2fdf77d` (P-032b close) → `e9f793f`.
    ★ ON TOP of P-032d, the dev branch now ALSO carries P-032c (`ab14ac7`,
    single product commit — the FIFTH new producer-agnostic doctrine axis
    `low_end_motion`, the low-end POCKET — kick/sub relationship + room around
    the bass, presence a GATE only (level structurally cannot leak into the
    score), weight-0 for halee_ramone so byte-identical), local-only, atop the
    build-os doctrine pin `b7e116a` and the set-active `fe5f6b4`. P-032c's
    parent chain: `ab14ac7` → `b7e116a` (doctrine pin, build-os only) →
    `fe5f6b4` (active-packet confirmation) → `89e7106` (P-032d close).
    ★ ON TOP of P-032c, the dev branch now ALSO carries P-032g (`835e907` +
    `e9e804d`, two product commits — the SIXTH new producer-agnostic doctrine
    axis `loop_context` (static-vs-iconic — THE HINGE, 13th component) + the
    FIRST profile-decided creative gate `protect_iconic_loops` (REQUIRED
    profile field; halee_ramone=false = current behavior), DUAL byte-identical
    for halee_ramone — doctrine AND creative), local-only, atop the set-active
    `6af00fa`. P-032g's parent chain: `e9e804d` → `835e907` → `6af00fa`
    (active-packet confirmation) → `211e04c` (P-032c close).**
    The base for MERGE decisions is still `e79426a` = PR #16 (nothing since P-025
    has been merged).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression` — **NOTE: run `fixtures/generate_fixtures.py`
  (or pytest via conftest) first in a fresh checkout; `fixtures/` content is
  GENERATED, not committed, so a bare worktree shows FALSE critical failures.**
- **Green baseline (verified 2026-07-01, P-032g):** suite **512 passed** (0 failed /
  skipped); regression **68/68** (0 critical / 0 warnings) — UNCHANGED (P-032g
  default path is DUAL byte-identical — doctrine AND creative; loop_context
  weight-0 + protect_iconic_loops=false for halee_ramone). Commit-1 (`835e907`)
  green in isolation = **499 passed + 68/68** in a real worktree check. (Prior
  baseline was 473 at P-032c; P-032g added +39 = 26 (`tests/test_loop_context.py`)
  + 13 (`tests/test_protect_iconic_loops.py`): DUAL byte-identity, independent —
  (a) doctrine 0 mismatches × 3 fixtures (overalls 73.8 / 70.7 / 74.3;
  `loop_context_score` 50.0 / 15.0 / 15.0 at weight 0) AND (b) creative full
  `result.creative` sorted-key JSON base vs HEAD → EMPTY diff / `cmp`
  byte-identical; flag liveness LIVE (A/B 85.9/loop_A(False) ↔
  81.9/loop_B(True); STATIC+protect → still fires; masked-lead+iconic+protect
  → still fires — Ramone gate FIRST); shared basis identity-asserted
  (`creative.read_loop_context is doctrine_engine.read_loop_context`); cautions
  untouched (`loop_foregrounded`=6, promotion table verbatim,
  `test_packet_cautions_untouched`); observational language (zero judgment
  words across all 7 reachable statuses) + honest-scope. Earlier: 451 → 473
  at P-032c; 433 → 451 at P-032d;
  413 → 433 at P-032b; 396 → 413 at P-032a; 384 → 396 at P-032e; 370 → 384
  at P-029; 351 → 370 at P-028; 331 → 351 at P-027; 319 → 331 at P-026;
  293 → 319 at P-025.)

## Where we are

- **★★ P-032g LANDS THE HINGE — `loop_context` (static-vs-iconic), the SIXTH
  new producer-agnostic doctrine axis (the 13th component), PLUS
  `protect_iconic_loops`, the FIRST profile-decided creative gate — DUAL
  byte-identical for halee_ramone (doctrine AND creative — the USER-MANDATED
  surface); qa GREEN + reviewer PASS (no must-fix).** The doctrine-pin
  exemplar realized: **the engine DETECTS agnostically** (static = dominant +
  no evolution; iconic = dominant + groove/fingerprint function — an ACOUSTIC
  PROXY; cultural recognizability deferred), **the profile DECIDES**
  (`protect_iconic_loops`, a REQUIRED profile field; halee_ramone=false =
  current behavior). **13 component axes; 6 of the 7 Timbaland weight-up axes
  landed. Last-closed = P-032g.**
  - **★ REVIEWER'S DOCTRINE FINDING (recorded prominently):** the
    status→score map (iconic 90 / evolving 60 / neutral 50 / unassessed 45 /
    static 15) lives in `doctrine.scorers.loop_context` IN THE PROFILE JSON —
    even the axis's POLARITY is profile-authored; the engine's fixed
    contribution is status DETECTION only. A future profile could invert the
    entire mapping without touching code. "The strongest possible form of the
    doctrine, not a leak."
  - **Two commits:** `835e907` (Commit-1 — pure additive `_loop_context`
    scorer + shared `read_loop_context()` helper, 8 files, 957+/3−, GREEN IN
    ISOLATION: 499 passed + 68/68 in a real worktree check) + `e9e804d`
    (Commit-2 — the creative gate: `_protected_iconic_loop()` in
    `_apply_promotions`, flag as REQUIRED profile field, 4 files, 481+/2−).
    Parent `6af00fa` (set-active), atop `211e04c` (P-032c close).
  - **★ qa GREEN:** suite 473 → **512** (+39: 26+13); regression **68/68, 0
    warnings**; **DUAL byte-identity, independent:** (a) doctrine — 0
    mismatches × 3 fixtures, overalls 73.8 / 70.7 / 74.3,
    `loop_context_score` 50.0 / 15.0 / 15.0 at weight 0 (both loop fixtures
    read STATIC — thematically exact); (b) creative — full `result.creative`
    sorted-key JSON base vs HEAD → EMPTY diff, `cmp` byte-identical. Flag
    liveness LIVE: A/B 85.9/loop_A(False) ↔ 81.9/loop_B(True); STATIC+protect
    → still fires; masked-lead+iconic+protect → still fires (Ramone gate
    FIRST). Shared basis identity-asserted (`creative.read_loop_context is
    doctrine_engine.read_loop_context`). Cautions untouched
    (`loop_foregrounded`=6; promotion table verbatim;
    `test_packet_cautions_untouched`). Observational language: zero judgment
    words across all 7 reachable statuses (the one "bad_masking" hit is a
    data-vocabulary key read, not emitted language). Safety grep NONE.
  - **★ reviewer PASS (no must-fix):** default path PROVEN unreachable (the
    flag is checked before any input; 5,000-trial randomized search through
    the gated promotion path → 0 divergences); protection structurally cannot
    beat a masked lead (ordering flag → `_lead_masked` → iconic; no
    short-circuit path); FIVE own sabotages ALL caught (drop axis / hardcode /
    ignore flag / drop the Ramone gate / fork the detection); required-field
    judgment ENDORSED (every producer JSON must state its loop philosophy
    explicitly — `timbaland.json` will declare it in writing); evolution
    floors are threshold GATES only (spreads in zero arithmetic — no
    `_dynamic_mix` re-derivation). **Codex NOT available — single-model
    review.**
  - **Constants (`doctrine.scorers.loop_context`):** status scores
    no_loop/not_dominant 50, dominant_unassessed 45, dominant_evolving 60,
    static 15, iconic 90; floors width 0.6, transient_lift 0.15,
    groove_transient 0.35, crest 12.0, rms 1.0 dB / width 0.05 / brightness
    0.05.
  - **★ HONEST DEFERRALS (test-guarded out of evidence, NOT faked):**
    cultural/recognizability iconic-ness (needs provenance/manifest — the
    acoustic proxy is what ships); per-loop bar-level variation;
    onset-sequence needs.
  - **★ NEW RESIDUE (carried to residue.md):** liveness-docstring-overclaim
    family now SIX files (+`tests/test_loop_context.py:566-570`); the gate
    keys on the literal kind `"loop_deconstruct"` (creative.py:232 — if
    promotion kinds generalize, move gating into the table row); the
    `dominant_unassessed` docstring slightly loose (per-metric, not
    per-section); `read_loop_context` shares the defensive None-value edge
    family.
  - **★★ MILESTONE — 13 component axes; 6 of the 7 Timbaland weight-up axes
    landed. The reusable pattern is established: a profile-decided creative
    gate on a shared detection basis (P-032f / P-032h will reuse it).**
  - **★ TIMBALAND SUB-ARC (P-032.x) — remaining order:** P-032e ✓ → P-032a ✓
    → P-032b ✓ → P-032d ✓ → P-032c ✓ → **P-032g ✓ → P-032f (vocal-role —
    NEXT, ★ USER-GATED: the orchestrator must present the "masked chop/stack
    = acceptable-blend" aesthetic rule + the protect-as-lead-when-uncertain
    conservative default to the USER for explicit go BEFORE any building)** →
    **[fold P-031 confidence here]** → P-032h (author `timbaland.json`, first
    non-byte-identical output) → P-032i (Timbaland-vs-Halee/Ramone
    differential proof). P-030 (rename dims) orthogonal/last. **P-032g
    local-only, NOT merged** (merge base still `e79426a` = PR #16). Receipt:
    `build-os/receipts/P-032g-loop-context-hinge.md`.

- **★★ P-032c LANDS THE FIFTH NEW PRODUCER-AGNOSTIC DOCTRINE AXIS —
  `low_end_motion` (the low-end POCKET: kick/sub relationship + room around
  the bass) — BYTE-IDENTICALLY FOR halee_ramone; DUAL-GREEN AGAINST THE
  USER'S EXPLICIT ACCEPTANCE INVARIANT, closed with the reviewer's AST +
  20,000-configuration adversarial proof (the strongest close of the arc).**
  A producer-profile PRIMITIVE under the pinned architecture doctrine (axes =
  shared measurable substrate; taste = weighting layer; safety invariant):
  different profiles will interpret the pocket differently (Timbaland:
  pocket/impact/negative-space/sub-kick; Halee/Ramone: balance/natural
  foundation; modern pop: translation/controlled sub density; trap: sub
  identity/808 envelope/space around transient) — this table is in the scorer
  docstring. **The doctrine engine now carries 12 component axes**, all five
  new axes weight-0 for halee_ramone (output BYTE-IDENTICAL). **Last-closed =
  P-032c.**
  - **★ THE USER'S ACCEPTANCE INVARIANT (ALL PROVEN): a clean low-end
    relationship BEATS high low-end quantity.** (1) mud loses despite MORE
    bass: total low 4.40 vs 1.22, 6 carriers, 2 criticals → **0.0** vs clean
    pocket **80.0**; (2) blob loophole CLOSED (fewer-carriers direction): a
    single smeared blob (1 carrier, per-stem low 0.95) → **28.0**, colliding
    → **14.0**, both < the SAME solo carrier clean+defined → **60.0** — the
    reservation is QUALIFIED by pocket behavior (crest ≥ 10 dB AND no
    critical collision), never carrier count; (3) presence leakage FENCED:
    boosted-low variants EXACT-equal (80.0 == 80.0, 60.0 == 60.0); (4)
    static_mix distinctness: 4-pad pile-up with no conflicts → static 80.0
    (healthy hygiene) vs lem 16.0; (5) byte-identity 73.8 / 70.7 / 74.3
    untouched.
  - **★ REVIEWER PASS — ADVERSARIAL PROOF:** AST — the low-band level appears
    in ZERO arithmetic nodes, only 2 threshold comparisons (level structurally
    CANNOT leak into the score); 20,000-configuration adversarial search —
    max score with ANY critical collision = 38.0 (below the 40.0 baseline);
    maxed-out mud = 0.0 vs 80.0; structural bound: only the QUALIFIED reserve
    can push past 64, so no quantity-beats-relationship path exists. Three own
    sabotages (hardcode / drop / weight-flip) ALL caught. **Codex NOT
    available — single-model review.**
  - **Constants (`doctrine.scorers.low_end_motion`):**
    `low_floor`/`stack_floor` 0.2, `baseline` 40, `reserved_bonus` 20
    (`reserved_max` 2), `defined_crest_db` 10.0, `blob_penalty` 12,
    `stack_penalty` 12, critical/moderate conflict penalties 14/6,
    `complement_coeff` 2.0 (cap 12 dB), `no_low_end` 25, `neutral` 40. Score
    landscape: clean pocket 80 > defined solo 60 > pile-with-spread 52 >
    neutral 40 > any-critical ≤ 38 > blob 28 > no_low_end 25 > worst mud 0.
    **Design note: the theoretical ceiling is 84 (40+20+24), never 100** —
    fine, but relevant when authoring `timbaland.json` weights (P-032h).
  - **★ qa GREEN:** suite 451 → **473 passed** (+22; base independently
    verified at `fe5f6b4`); regression **68/68, 0 warnings**; byte-identical
    INDEPENDENT capture: 36/36 pre-existing values repr-identical × 3
    fixtures; new `low_end_motion_score` = 60.0 / 21.1 / 25.0 at weight 0;
    DROP sabotage → 2 liveness FAIL / anchors PASS; HARDCODE → 4
    discrimination FAIL / anchors PASS; safety grep NONE FOUND; honest-scope
    verified (`identity_family` = tie-break only, `instrument_identity` never
    read; `sections_analysis` accepted per the signature, 0 reads,
    documented).
  - **★ HONEST DEFERRALS (docstring, NOT faked):** kick/sub temporal
    interlock (bass excluded from RHYTHM_IDENTITIES — no bass onsets);
    low-end motif detection; per-section true-sub movement (sections expose
    low_mid only).
  - **Single commit `ab14ac7`** on parent `b7e116a` (build-os-only doctrine
    pin; the code base is effectively the set-active `fe5f6b4`) — HEAD IS
    Commit-1 → green in isolation (473). 8 files, 837 insertions / 4
    deletions. qa **GREEN**; reviewer **PASS**. **P-032c local-only, NOT
    merged** (merge base still `e79426a` = PR #16). **Trailer note:** the
    commit carries `Co-Authored-By: Claude Fable 5` — the harness-sanctioned
    attribution for the current session model (the mandate changed
    mid-session); accepted by the orchestrator; parallel to the earlier
    Opus-4.8 reconciliation. Future packets use the current harness trailer;
    do NOT re-flag.
  - **★ NEW RESIDUE (carried to residue.md):** the
    liveness-docstring-overclaim family now spans FIVE test files (add
    `tests/test_low_end_motion.py:518-526`); lem's 84-point theoretical
    ceiling + the defensive `r.get("metrics",{})` None edge — ride-alongs
    for a future doctrine-touching packet.
  - **★★ MILESTONE — 12 component axes; 5 of the 7 Timbaland "weight up"
    axes landed** (beat_identity, negative_space, groove_coherence,
    rhythmic_surprise, low_end_motion), all
    append-last/weight-0/profile-sourced, ZERO plumbing debt.
  - **★ TIMBALAND SUB-ARC (P-032.x) — RESEQUENCED remaining order:** **P-032e
    ✓ → P-032a ✓ → P-032b ✓ → P-032d ✓ → P-032c ✓ → P-032g (loop
    static-vs-iconic — THE HINGE, NEXT: USER-MANDATED dual byte-identity
    surface — doctrine overall AND creative variant scores +
    `loop_deconstruct` promotion firing behavior byte-identical under
    Halee/Ramone defaults; engine language OBSERVATIONAL; the profile flag
    defaults to CURRENT behavior) → P-032f (vocal-role — HIGH risk, LAST, ★
    USER-GATED)** → **[fold P-031 confidence here]** → P-032h (author
    `timbaland.json`, first non-byte-identical output) → P-032i
    (Timbaland-vs-Halee/Ramone differential proof). P-030 (rename dims)
    orthogonal/last. Receipt:
    `build-os/receipts/P-032c-low-end-motion.md`.

- **★★ P-032d LANDS THE FOURTH NEW PRODUCER-AGNOSTIC DOCTRINE AXIS —
  `rhythmic_surprise` (weak, section-aggregate form) — BYTE-IDENTICALLY FOR
  halee_ramone; the FIRST packet of the RESEQUENCED remaining order
  (d → c → g → f), the smallest/safest lift (one input, ZERO new plumbing —
  confirmed in practice).** **The doctrine engine now carries 11 component
  axes** (7 original + beat_identity + negative_space + groove_coherence +
  rhythmic_surprise), all four new axes weight-0 for halee_ramone (so output is
  BYTE-IDENTICAL). **Last-closed = P-032d.**
  - **What P-032d shipped:** a new agnostic scorer
    `_rhythmic_surprise(sections_analysis, doctrine)` in `doctrine_engine.py`
    measuring cross-section transient-density variation — pstdev SPREAD of
    section `transient_density` (the `_dynamic_mix` idiom applied to the ONE
    signal it never reads) + the LARGEST adjacent section-to-section SWING
    ("the beat drops out / the fill hits" in aggregate form). Always returns a
    clamped float; <2 sections → documented fallback. Constants (in
    `doctrine.scorers.rhythmic_surprise`): `insufficient_sections_score 40.0`,
    `baseline 20.0`, `spread_coeff 160`, `swing_coeff 60`. Live fixture scores
    (weight-0, informational): **51.1** (simple — some sectional variation) /
    **20.0** (dense — the real-world high-mean/ZERO-variance constant bed) /
    **27.8** (splice).
  - **★ BYTE-IDENTICAL (INDEPENDENT — qa's own capture):** 33/33 pre-existing
    values × 3 fixtures unchanged (overalls 73.8 / 70.7 / 74.3); regression
    **68/68, 0 warnings — UNCHANGED**. `rhythmic_surprise_score` appended LAST
    to `component_scores` (after `groove_coherence_score`; the 10-term
    summation order preserved) with `weights["rhythmic_surprise_score"] = 0`.
  - **★ DISTINCTNESS — ALL 4 GUARDS PASS AND INDEPENDENTLY RECOMPUTED (qa):**
    high-mean/zero-variance constant transient bed → **20.0** (LOW — the
    design crux); mean-invisibility (a mean shift alone leaves rs
    20.0 == 20.0); negative_space-OPPOSITE (ns 78.0 vs rs 20.0 — mean vs
    variance statistics); dynamic_mix-DISTINCT (dyn 100.0 vs rs 20.0 —
    rms/width/brightness vs transient_density). The ONLY axis keyed on the
    VARIATION of section transient_density.
  - **★ LIVENESS LOAD-BEARING (the P-016/P-029 lesson):** drop-axis
    monkeypatch sabotage → liveness 2 FAILED / byte-identical 5 passed — the
    axis is genuinely wired; byte-identical alone would not catch an
    accepted-but-ignored axis.
  - **★ HONEST SCOPE (weak form, test-guarded, deliberately NOT faked):**
    evidence strings say "weak, section-aggregate form"; AST/grep-verified the
    scorer reads sections + doctrine ONLY. Deferred in the docstring: fill
    detection, unexpected-hit detection, per-onset IOI deviation (all need
    onset timing/sequence — groove territory). Must NOT read
    `overall_regularity` (that is `_groove_coherence`'s input) — ENFORCED.
  - **★ REVIEWER PASS (no must-fix) — ran THREE own sabotages, ALL caught:**
    (A) hardcode the scorer to a constant → 7 discrimination/fallback/evidence
    tests fail; (B) drop the axis from `component_scores` → 3 fail incl. BOTH
    liveness tests; (C) flip the halee weight 0→2 → 8 fail across three guard
    files. Constants sanity: smooth mid-range discrimination (swing 0.1 → 34,
    0.3 → 62, 0.5 → 90), clamps at 100 for swings ≳0.57 — consistent with the
    sibling idiom, not degenerate. **Codex NOT available — single-model
    review.**
  - **Single commit `8a81516`** (atop set-active `8c03f14`, branch
    `claude/logic-mix-os-hardening-12-7hbeh1` — HEAD IS Commit-1, green in
    isolation by construction). Suite **433 → 451 passed** (+18; 0 failed /
    skipped; base independently verified at `8c03f14` in a throwaway worktree
    = 433); regression **68/68, 0 warnings — UNCHANGED**. Safety grep NONE
    FOUND (535 insertions / 6 deletions, 8 in-packet files). qa **GREEN**;
    reviewer **PASS (no must-fix)**. **P-032d local-only**, not pushed/merged
    (merge base still `e79426a` = PR #16).
  - **★ NEW COSMETIC RESIDUE (reviewer, carried to residue):** (1)
    `test_liveness_direction_tracks_the_rhythmic_surprise_score`'s docstring
    OVERCLAIMS (a hardcoded constant still moves the mean directionally; the
    discrimination tests are what catch hardcoding) — SAME family as the
    standing liveness-docstring-overclaim note; fold ONE docstring sweep across
    ALL FOUR axis test files into a future doctrine-touching packet. (2) in
    `_rhythmic_surprise`, None-filtering BEFORE the adjacency zip means a
    missing middle `transient_density` would compute a swing across
    NON-adjacent sections — defensive-only (the pipeline always emits the
    metric); same future-packet ride-along.
  - **★★ MILESTONE — the engine now carries 11 component axes; 4 of the 7
    Timbaland "weight up" axes have now landed** (beat_identity,
    negative_space, groove_coherence, rhythmic_surprise), all
    append-last/weight-0/profile-sourced, ZERO plumbing debt.
  - **★ TIMBALAND SUB-ARC (P-032.x) — RESEQUENCED remaining order:** **P-032e
    ✓ → P-032a ✓ → P-032b ✓ → P-032d ✓ → P-032c (low_end_motion — NEXT: pure
    additive, 5 in-arg inputs; distinctness-vs-static_mix needs care —
    POSITIVE relationship vs hygiene penalty; presence is a GATE only — "more
    bass" must not win) → P-032g (loop static-vs-iconic) → P-032f (vocal-role
    — HIGH risk, LAST, ★ USER-GATED)** → **[fold P-031 confidence here]** →
    P-032h (author `timbaland.json`, first non-byte-identical output) →
    P-032i (Timbaland-vs-Halee/Ramone differential proof). P-030 (rename dims)
    orthogonal/last. Receipt:
    `build-os/receipts/P-032d-rhythmic-surprise.md`.

- **★★ P-032b LANDS THE THIRD NEW PRODUCER-AGNOSTIC DOCTRINE AXIS —
  `groove_coherence` — AND THE `analyze_groove` LIVE-WIRE, BYTE-IDENTICALLY FOR
  halee_ramone; the RISKIEST packet of the sub-arc so far (moved code, not just
  added), TRIPLE-VERIFIED (qa GREEN + reviewer PASS + a 3-skeptic adversarial
  pass with ALL claims HELD).** This is the packet where onset-regularity/IOI —
  deferred from P-032e AND P-032a — finally reached doctrine. **The doctrine
  engine now carries 10 component axes (7 original + beat_identity +
  negative_space + groove_coherence), all three new axes weight-0 for
  halee_ramone (so output is BYTE-IDENTICAL). Last-closed = P-032b.**
  - **What P-032b shipped — the LIVE-WIRE (the P-016 lesson made structural):**
    `pipeline.py` relocates `analyze_groove` to BEFORE `score_doctrine`
    (pipeline.py:180 vs :183), threads `groove=groove` into
    `score_doctrine(..., groove: Optional[Dict] = None)` (keyword, default None —
    every existing caller stays byte-identical), and REUSES the exact same
    groove object in `result.expanded["groove"]` (:208) — computed exactly ONCE
    (exactly one `analyze_groove(` call site; spy-counted no-re-run guard). Plus
    the new agnostic scorer `_groove_coherence(groove, doctrine)` as the 10th
    doctrine component.
  - **★ BYTE-IDENTICAL (INDEPENDENT — qa's own capture, not builder pins):** all
    9 pre-existing component scores + overall + `expanded["groove"]`, all 3
    fixtures → diff EMPTY (overalls 73.8 / 70.7 / 74.3 unchanged); regression
    **68/68, 0 critical, 0 warnings — UNCHANGED**.
  - **★ LIVENESS + SABOTAGE (load-bearing — reviewer-verified by INJECTED
    REGRESSIONS in an isolated worktree):** gc(0.989) = 99.1, neutral 45.0;
    re-adding a second `analyze_groove` call turns
    `test_analyze_groove_called_exactly_once` red (2==1); threading `groove=None`
    turns `test_score_doctrine_receives_the_real_groove` red (45.0 ≠ 99.1) —
    both guards genuinely load-bearing. None-handling: an `is None` guard, so a
    real 0.0 regularity → 15.0, not swallowed; no KeyError path. Guard updates
    legitimate (negative_space now index 8 with the `keys[:8]` anchor intact).
  - **★ ADVERSARIAL VERIFICATION (3 independent skeptics — ALL claims HELD):**
    (1) *byte-identical/float-determinism* — 9-component recomputation
    bit-identical on all fixtures; `gc*0 == 0.0` exactly; the `nan*0` poisoning
    path is UNREACHABLE (`_clamp` neutralizes non-finites; `analyze_groove` can
    only emit None or float[0,1]); relocation side-effects — all 8 non-groove
    `expanded` keys byte-identical. (2) *compute-once/threading* — call-count 1
    across ALL branches (ref-delta, creative, memory); `expanded["groove"]` IS
    the object passed to doctrine (`is`-identity); nothing mutates it on the
    real path; the `groove=None` sabotage collapses 99.1 → 45.0. (3) *None/edge
    robustness* — every None/empty/missing-key case → clamped neutral 45.0;
    boundaries clamp to [0,100]; out-of-contract crash inputs (strings/lists)
    proven UNREACHABLE from the sole producer.
  - **★ HONEST NAMING (test-guarded, deliberately NOT overclaimed):**
    `overall_regularity` measures rhythmic tightness/CONSISTENCY —
    regularity/consistency scored as a **PROXY for coherence**, never "tighter
    is better"; the agnostic layer stays neutral and the *producer* decides the
    weighting. Constants (all in `doctrine.scorers.groove_coherence`):
    `neutral 45.0` (absence neither rewarded nor punished), `baseline 15.0`,
    `regularity_scale 85.0` (linear map: regularity 0 → 15, 1.0 → 100; dense
    fixture 0.989 → 99.1).
  - **Single commit `e9f793f`** (atop set-active `bd98777`, branch
    `claude/logic-mix-os-hardening-12-7hbeh1` — HEAD IS Commit-1, green in
    isolation by construction). Suite **413 → 433 passed** (+20; 0 failed /
    skipped; verified at HEAD AND independently at base `bd98777` in a throwaway
    worktree); regression **68/68 — UNCHANGED**. Safety grep NONE FOUND (582
    insertions / 13 deletions, 9 in-packet files). qa **GREEN**; reviewer
    **PASS (no must-fix)**. **Codex NOT available — single-model review.**
    **P-032b local-only**, not pushed/merged (merge base still `e79426a` =
    PR #16).
  - **★ NEW COSMETIC RESIDUE (adversarial skeptic):** `result.expanded["groove"]`
    IS the same dict passed to `score_doctrine` (shared mutable state); nothing
    mutates it today (deepcopy-proven), but a FUTURE doctrine change mutating its
    `groove` arg would silently corrupt the expanded artifact — consider a
    defensive copy or a read-only test pin in a future doctrine-touching packet.
  - **★★ MILESTONE — the engine now carries 10 component axes** (7 original +
    beat_identity + negative_space + groove_coherence), all three new ones
    weight-0 byte-identical for the reference producer. **The onset/IOI signal
    is now LIVE at doctrine time — unblocking the axes that need rhythm
    timing.**
  - **★ TIMBALAND SUB-ARC (P-032.x) — RESEQUENCED REMAINING ORDER (from the
    read-only scoping workflow, evidence-backed):** **P-032e ✓ → P-032a ✓ →
    P-032b ✓ → P-032d (rhythmic_surprise — NEXT, smallest/safest: one input,
    section transient_density variance, pure additive, zero new plumbing) →
    P-032c (low_end_motion — pure additive, 5 in-arg inputs;
    distinctness-vs-static_mix needs care: POSITIVE relationship vs hygiene
    penalty) → P-032g (loop static-vs-iconic — medium: scorer + creative.py
    promotion gate behind a profile flag; SECOND byte-identity surface =
    creative variant/promotion scores) → P-032f (vocal-role — HIGH risk, LAST;
    ★ USER-GATED: needs explicit go on the "masked chop/stack =
    acceptable-blend" aesthetic rule + the conservative default
    protect-as-lead-when-uncertain)** → **[fold P-031 confidence here]** →
    P-032h (author `timbaland.json`, first non-byte-identical output) → P-032i
    (Timbaland-vs-Halee/Ramone differential proof). P-030 (rename dims)
    orthogonal/last. Receipt:
    `build-os/receipts/P-032b-groove-coherence-livewire.md`.

- **★★ P-032a LANDS THE SECOND NEW PRODUCER-AGNOSTIC DOCTRINE AXIS —
  `negative_space` — BYTE-IDENTICALLY FOR halee_ramone; the Timbaland sub-arc
  (P-032.x) continues past the crux.** After P-032e front-loaded the hard/risky
  `beat_identity` crux, P-032a takes the LOWEST-RISK remaining axis (all inputs
  already visible to `score_doctrine`) and adds `negative_space`: absolute
  arrangement room/sparsity ("silence is arrangement"), deliberately DISTINCT from
  `_dynamic_mix` (section-to-section movement). **The doctrine engine now carries
  9 component axes (7 original + beat_identity + negative_space), both new axes
  weight-0 for halee_ramone (so output is BYTE-IDENTICAL). Last-closed = P-032a.**
  - **What P-032a shipped:** a new agnostic scorer `_negative_space(records,
    sections, mix_metrics, doctrine)` in `doctrine_engine.py` composing ABSOLUTE
    ROOM as a STRENGTH from section-aggregate physics — low mean section spectral
    `density` (room), a genuine dropout section (`min_section_density` / min RMS
    meaningfully below max — "silence as arrangement"), and transient breathing
    room (low mean section `transient_density`). Always returns a clamped float
    (documented neutral fallback = 40.0 when no section/mix data) — mirrors
    `_beat_identity`'s always-float discipline. Constants read (read-only) from
    `doctrine["scorers"]["negative_space"]`.
  - **★ BYTE-IDENTICAL MECHANISM (identical to P-032e):** `negative_space_score`
    appended **LAST** to `component_scores` (after `beat_identity_score`) →
    summation order preserved → overall bit-identical; `weights["negative_space_score"]
    = 0` in `halee_ramone.json`. Proven **0 mismatches / 27 comparisons** vs
    set-active base `836bd22` (overalls 73.8 / 70.7 / 74.3 unchanged); regression
    **68/68, 0 critical, 0 warnings — UNCHANGED**.
  - **★ DISTINCTNESS PROVEN (the design guard — non-tautological):** a
    dense-but-moving case scores `dynamic_mix = 100.0` vs `negative_space = 15.0`
    — an **85-pt gap** — so a wall-to-wall-dense mix that varies section-to-section
    is HIGH on dynamic_mix but LOW on negative_space. Genuinely orthogonal, not a
    re-derivation of dynamic_mix.
  - **★ LIVENESS LOAD-BEARING (the P-016/P-029 lesson honored):** a profile
    weighting `negative_space_score` non-zero MOVES the `analyze()` overall;
    sabotage FAILS liveness while byte-identical stays green (drop the threading →
    liveness FAIL/KeyError; hardcode the constant → 8 fail + 5 err) —
    byte-identical alone would NOT catch an accepted-but-ignored axis. Live fixture
    scores (weight-0, informational): **62.3** (roomy simple_vocal_piano) / **15.0**
    (dense_chorus) / **20.0** (splice) — sparse ≥ 75, wall-to-wall ≤ 35, neutral
    fallback 40. Zero effect on halee_ramone overall (weight 0).
  - **★ HONEST DEFERRAL (documented in the scorer docstring, deliberately NOT
    faked):** sample-level **inter-onset silence gaps** (space between individual
    hits) need onset timing, not visible at `score_doctrine` time (it lives in the
    post-doctrine groove analyzer) — deferred to **P-032b**'s groove live-wire.
    negative_space works at the **section-aggregate grain only** — no instrument
    labels, no onset timing.
  - **★ AGNOSTIC-FIRST:** physics/measurement stays hardcoded & agnostic; only the
    *weight* lives in the profile (all 8 tunables — `neutral 40.0`, `baseline 15.0`,
    `density_ceiling 1.0`, `room_coeff 50`, `transient_ceiling 1.0`,
    `breathing_coeff 20`, `dropout_coeff 25`, `dropout_floor 0.1` — in
    `doctrine.scorers.negative_space`). `producer_profile._validate`
    required-scorers now includes `negative_space` (structurally bound).
    `doctrine_score.schema.json` gained the optional `negative_space_score`
    property. No-aliasing: the scorer only reads `doctrine[...]`, never mutates.
  - **Single commit `3edcd9c`** (base `6d34c30`, atop set-active `836bd22`) —
    scorer + `doctrine.scorers.negative_space` constants + weight-0 + `_validate`
    + `tests/test_negative_space.py` (17 tests) + 3 doctrine-key-pin updates
    (`test_producer_profile.py` scorers-set, `test_doctrine_profile_sourced.py`
    `_WEIGHTS` value-pin, `test_beat_identity.py` beat_identity now index 7). **One
    logically-atomic commit; no Commit-2 needed.** Suite **396 → 413 passed** (+17;
    0 failed/skipped/warnings, green under `-W error`); regression **68/68, 0
    critical, 0 warnings — UNCHANGED**. Safety grep clean; honest-scope confirmed;
    UI N/A. qa **GREEN**; reviewer **PASS** (all 8 scrutiny points; byte-identical
    empirically proven base→HEAD; distinctness non-tautological; honesty gate
    genuine; liveness load-bearing at suite level; agnostic-first; no-aliasing;
    guard updates legitimate tightening; Product Trajectory Check pass; no
    must-fix). **Codex NOT available — single-reviewer verdict.** **P-032a
    local-only** (`3edcd9c` on the dev branch atop the `6d34c30` P-029-close base),
    not pushed/merged.
  - **★★ MILESTONE — the SECOND new producer-agnostic measurement axis. The engine
    now carries 9 component axes**, the second added byte-identically for the
    reference producer. **The producer-agnostic architecture (P-029) continues to
    prove EXTENSIBLE, not just parameterizable.**
  - **★ NON-BLOCKING NOTE (reviewer, carried to residue):** the two `liveness`
    test docstrings in `tests/test_negative_space.py` (~lines 536-540, 553-557)
    OVERCLAIM — a general hardcoded-constant sabotage is actually caught by the
    *discrimination* tests, not the liveness tests themselves. The SAME imprecision
    exists in the already-closed `test_beat_identity.py`. Cosmetic only (guard SET
    sound); fold a one-line docstring fix for BOTH files into a future
    doctrine-touching packet.
  - **★ TIMBALAND SUB-ARC (P-032.x):** **P-032e ✓ (beat_identity — crux) → P-032a
    ✓ (negative_space)** → **P-032b (groove_coherence live-wire — NEXT; the RISKIER
    packet: relocate `analyze_groove` to BEFORE `score_doctrine` + a no-re-run
    live-wire test, then the groove-coherence scorer — where onset-regularity/IOI,
    deferred from P-032e AND P-032a, finally reaches doctrine)** → P-032c
    (low_end_motion/pocket) → P-032d (rhythmic_surprise, weak-form) → P-032f
    (vocal-role refinement) → P-032g (loop static-vs-iconic context) → **[fold
    P-031 confidence here]** → P-032h (author `timbaland.json`, first
    non-byte-identical output) → P-032i (Timbaland-vs-Halee/Ramone differential
    proof). P-030 (rename dims) orthogonal/last. Receipt:
    `build-os/receipts/P-032a-negative-space.md`.

- **★★ P-032e LANDS THE FIRST NEW PRODUCER-AGNOSTIC DOCTRINE AXIS — `beat_identity`
  — AND PROVES THE ARCHITECTURE (P-029) IS EXTENSIBLE, NOT JUST PARAMETERIZABLE.**
  The Timbaland sub-arc (P-032.x) is now UNDERWAY, and the user front-loaded the
  hardest/riskiest axis — beat_identity, the central-rhythmic-fingerprint STRENGTH —
  to de-risk the whole sub-arc early: prove the signal is *honestly measurable on
  exported stems* before investing in the easier axes. **The doctrine engine now
  carries 8 component axes (7 original + beat_identity), with beat_identity weight-0
  for halee_ramone (so its output is BYTE-IDENTICAL). Last-closed = P-032e.**
  - **What P-032e shipped:** a new agnostic scorer `_beat_identity(records, events,
    doctrine)` in `doctrine_engine.py` measuring fingerprint STRENGTH from transient
    physics alone — agnostic rhythmic-candidate identification by `transient_density`
    (NOT by instrument label), presence vs a `no_beat` floor, distinctness above the
    track median, definition via `crest_factor_db`, and a foreground/unmasked bonus
    (buried/masked → penalty). Constants read (read-only) from
    `doctrine["scorers"]["beat_identity"]`.
  - **★ BYTE-IDENTICAL MECHANISM:** `beat_identity_score` is appended **LAST** to
    `component_scores` (preserves the pre-existing 7-term summation order → overall
    bit-identical) with `weights["beat_identity_score"] = 0` in `halee_ramone.json`
    (`beat·0` numerator, `+0` denominator → weighted mean unchanged). Proven **0/24
    mismatches** vs clean base `6d34c30` (overalls 73.8 / 70.7 / 74.3 unchanged);
    regression **68/68, 0 critical, 0 warnings — UNCHANGED**.
  - **★ LIVENESS LOAD-BEARING (the P-016/P-029 lesson honored):** a synthetic profile
    weighting `beat_identity_score` non-zero MOVES the `analyze()` overall and its
    direction tracks the beat score; **sabotage (hardcode beat / drop the threading)
    FAILS the liveness tests while byte-identical stays green** — byte-identical alone
    would NOT catch an accepted-but-ignored axis. Value-discrimination proven: a
    punchy/foregrounded/distinct rhythmic stem → HIGH; no rhythmic element → `no_beat`
    floor. Live fixture scores (weight-0, informational): **89.1 / 52.7 / 46.0** — a
    sensible discriminating spread.
  - **★ HONEST BOUNDARIES (documented in-code, deliberately NOT faked — the CRUX):**
    (1) fingerprint TYPING (mouth-sound/tabla/synth-knock) — not measurable on
    exported stems; (2) onset REGULARITY / IOI — real but not visible at
    `score_doctrine` time (lives in the post-doctrine groove analyzer), deferred to
    **P-032b**'s groove live-wire; (3) "more undeniable after a move" — needs a
    before/after render, out of scope in plan-only v1. Candidacy is by transient
    physics ONLY.
  - **★ AGNOSTIC-FIRST:** physics/measurement stays hardcoded & agnostic; only the
    *weight* lives in the profile. `producer_profile._validate` required-scorers now
    includes `beat_identity` (structurally bound). `doctrine_score.schema.json` gained
    the optional `beat_identity_score` property (documentation; no
    `additionalProperties: false`). No-aliasing: the scorer only reads `doctrine[...]`,
    never mutates the profile (two no-aliasing tests).
  - **Two commits `8239f42` (scorer + constants + weight-0 + `_validate` + 12-test
    `test_beat_identity.py` + 2 guard updates — green in isolation = 396) + `9d6764e`
    (schema doc).** Suite **384 → 396 passed** (+12; 0 failed/skipped/warnings, green
    under `-W error`); regression **68/68, 0 critical, 0 warnings — UNCHANGED**. Safety
    grep clean; honest-scope confirmed; UI N/A. qa **GREEN**; reviewer **PASS** (all 7
    scrutiny points; byte-identical proven numerically over 100k trials; liveness
    verified load-bearing by an in-memory sabotage; guard updates are legitimate
    tightening; Product Trajectory Check pass; no must-fix). **Codex NOT available —
    single-model review.** **P-032e local-only** (`8239f42`, `9d6764e` on the dev
    branch on top of the `6d34c30` P-029-close base), not pushed/merged.
  - **★★ MILESTONE — THE FIRST NEW PRODUCER-AGNOSTIC MEASUREMENT AXIS beyond the
    original Halee/Ramone set.** The engine can now *hear* a Timbaland-relevant
    dimension, added byte-identically for the reference producer. **The
    producer-agnostic architecture (P-029) is proven EXTENSIBLE, not just
    parameterizable.**
  - **★ TIMBALAND SUB-ARC (P-032.x) — the CRUX landed FIRST:** **P-032e ✓
    (beat_identity — front-loaded crux)** → P-032a (negative_space — RECOMMENDED NEXT,
    lowest-risk, all inputs already visible to doctrine) → P-032b (groove_coherence
    live-wire — where onset-regularity/IOI gets plumbed in) → P-032c
    (low_end_motion/pocket) → P-032d (rhythmic_surprise, weak-form) → P-032f
    (vocal-role refinement) → P-032g (loop static-vs-iconic context) → **[fold P-031
    confidence here]** → P-032h (author `timbaland.json`, first non-byte-identical
    output) → P-032i (Timbaland-vs-Halee/Ramone differential proof). P-030 (rename
    dims) orthogonal/last. Receipt:
    `build-os/receipts/P-032e-beat-identity.md`.

- **★★ P-029 IS THE PIVOT — THE PRODUCER PROFILE IS NOW A LIVE, SELECTABLE LEVER
  END-TO-END: `analyze(producer=…)` SELECTS WHICH PROFILE DRIVES THE JUDGMENT.**
  The EXTRACTION PHASE (P-026/27/28) made the judgment layer read from a module
  `_DEFAULT_PROFILE` singleton; **P-029 threads a PER-CALL profile through the whole
  pipeline** so a different producer produces a different plan — the profile stops
  being a mirror of today's hardcoded values and becomes a real lever.
  **Last-closed = P-029.**
  - **What P-029 shipped — the threading:** `pipeline.analyze(..., producer: str |
    ProducerProfile = "halee_ramone")` accepts a NAME or a ready `ProducerProfile`
    object (via `isinstance` dispatch — name → `load_profile`, object → used
    directly), loads the profile ONCE per call, and threads `profile=` to the three
    judgment entry points, which thread it to EVERY leaf scorer: doctrine
    (`score_doctrine` + the 7 scorers `_halee`/`_ramone`/`_vocal_centrality`/
    `_depth_hierarchy`/`_section_contrast`/`_static_mix`/`_dynamic_mix` + weights),
    creative (`run_creative_engine` → `score_variant`/`_apply_nudges`/
    `_apply_promotions`), governance (`run_governance` → `govern_branches`/
    `govern_variant`/`taste_triangle`/`_apply_taste`). Each leaf reads its
    producer-specific values from the PASSED profile, defaulting to the module
    `_DEFAULT_PROFILE` when `profile is None` — so existing direct callers + the
    no-arg path stay byte-identical.
  - **★ KILL_SWITCHES recomposed PER CALL (the load-bearing safety boundary):** the
    5 hardcoded producer-AGNOSTIC SAFETY switches + the passed profile's aesthetic
    switches, in the same order — **a swapped producer can NEVER drop a safety
    guarantee**, and the default composed list is byte-identical (no safety string
    in the JSON). **No judgment VALUE changed; physics/analyzers untouched.**
  - **Byte-identical default PROVEN:** reviewer INDEPENDENTLY byte-diffed the default
    `analyze()` doctrine + creative + governance across all 3 fixtures pre-P-029 vs
    HEAD → IDENTICAL. no-arg == `producer="halee_ramone"` == the reference object.
    Regression **68/68, 0 critical, 0 warnings — UNCHANGED.** Existing tests UNEDITED.
  - **★★ SELECTION IS GENUINELY LIVE across all 3 layers** — through the REAL
    `analyze()` path with synthetic one-value-mutated profiles (NO monkeypatch):
    doctrine `baselines.halee` −20 → `halee_score` delta exactly 20; creative boosted
    `vocal_ride` kind_score → that variant's real `overall_score` → 100; governance
    `truth_alignment["intimate"]["vocal_ride"]` 88→60 → governed
    `emotional_truth_alignment` 60. **LOAD-BEARING proven BOTH ways (the P-016
    lesson):** sabotaging each layer's threading fails ITS liveness test while
    byte-identical/determinism stay green — byte-identical alone would NOT catch an
    accepted-but-ignored profile. **Reviewer grep: ZERO module-global producer-value
    reads inside any scorer body on the hot path — no leaf missed.**
  - **Two commits `42d6ebd` (doctrine + creative + pipeline wiring + byte-identical +
    doctrine/creative liveness — green in isolation = 383) + `ea1aaa9` (governance
    threading + governance liveness).** Suite **370 → 384 passed** (+14; 0
    failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
    0 warnings — UNCHANGED.** Scope: exactly 5 files (4 product + 1 new test);
    physics/analyzers/bridge/planners untouched. Safety grep clean; UI N/A. qa
    **GREEN**; reviewer **pass**. **Codex NOT available — single-reviewer verdict.**
    **P-029 local-only** (commits `42d6ebd`, `ea1aaa9` on the dev branch on top of
    the P-028 commits on top of the `e79426a` base), not pushed/merged.
  - **★★ MILESTONE — THE PIVOT: the producer-agnostic ARCHITECTURE is COMPLETE and
    VALIDATED.** `analyze(producer=…)` genuinely drives a DIFFERENT plan for a
    DIFFERENT profile, proven across doctrine + creative + governance and proven
    load-bearing. The architecture = reference-profile-driven judgment + a
    producer-AGNOSTIC physics/safety chassis + per-call producer selection. The
    profile is now a LIVE, SELECTABLE LEVER end-to-end.
  - **★ ALIASING CARRY-FORWARD (reviewer, non-blocking — for P-032):** the
    module-level `_DEFAULT_PROFILE` singleton STILL exists in all 3 consumer modules
    as the `None`-default fallback, so the per-module copy-before-mutate no-aliasing
    discipline still carries on the DEFAULT path. When P-032 loads a SECOND live
    profile per call, KEEP the aliasing discipline in mind — do NOT mutate a loaded
    profile's structures in place.
  - **★ EPIC ARC (updated):** **P-025 ✓ (foundation) → P-026 ✓ (creative sourced) →
    P-027 ✓ (governance sourced + WIDENED) → P-028 ✓ (doctrine sourced + WIDENED —
    extraction phase COMPLETE) → P-029 ✓ (THE PIVOT — profile is a live, selectable
    lever; `analyze(producer=…)` real; architecture complete & validated)** →
    **P-030 (rename the `halee`/`ramone` dims off the producer names)** → P-031
    (confidence framework — consume the metadata stamp) → **P-032 (FIRST SECOND
    PRODUCER — the payoff; USER-GATED: WHICH producer + grounding per the honesty
    policy)** → P-033 (expose producer selection). Receipt:
    `build-os/receipts/P-029-parameterize-pipeline-by-per-call-producer-profile.md`.

- **★★ P-028 SOURCES `doctrine_engine.py` FROM THE REFERENCE PROFILE (WIDENED — THE
  LAST & LARGEST EXTRACTION) AND COMPLETES THE EXTRACTION PHASE OF THE
  PRODUCER-AGNOSTIC EPIC.** P-026 sourced `creative.py`; P-027 sourced `governance.py`
  (widened); **P-028 sources `doctrine_engine.py` (widened)** — so the ENTIRE
  producer-specific judgment layer is now driven by the reference `ProducerProfile`,
  byte-identical, with the physics chassis + safety kill-switches cleanly separated
  and left hardcoded. **Last-closed = P-028.**
  - **What P-028 shipped — Part A (source already-captured values):** `doctrine_engine.py`
    gains `_DEFAULT_PROFILE = load_profile("halee_ramone")` and SOURCES `score_doctrine`'s
    component **weights** (halee 1.0 / ramone 1.2 / vocal_centrality 1.2 / depth 1.0 /
    contrast 1.0 / static 1.0 / dynamic 0.8) + `_halee`/`_ramone` **baselines (86.0)** +
    penalty coeffs FROM `_DEFAULT_PROFILE.doctrine.*` — the values P-025 already captured
    and round-trip-guarded; the inline literals are relocated behind the profile.
  - **Part B — WIDEN the profile (Finding A, the doctrine portion):** `ProducerProfile` +
    `halee_ramone.json` + the loader validation + the round-trip gain a new
    `doctrine.scorers` group (5 function groups), captured VERBATIM, then each scorer
    reads its constants from `_DEFAULT_PROFILE.doctrine["scorers"]` —
    `_vocal_centrality` (no_lead 35.0 / baseline 70.0 / sacred_bonus 10 / forward_bonus 10
    / masked_coeff 6), `_depth_hierarchy` (baseline 40 / per_distinct 12 /
    forward_threshold 0.6 / forward_occupancy 60), `_section_contrast` (baseline 100 /
    lift_fail_penalty 18), `_static_mix` (baseline 80.0 / peak_ceiling -0.1 / peak_penalty
    10 / dominant_band_threshold 0.55 / dominant_band_penalty 10 / crit_low_coeff 8 /
    no_lead_penalty 8), `_dynamic_mix` (insufficient_sections_score 40.0 / baseline 30 /
    rms_coeff 8 / width_coeff 140 / bright_coeff 140 / lift_fail_penalty 10).
  - **★ THE PHYSICS / AESTHETIC BOUNDARY (load-bearing — what did NOT move):** only the
    aesthetic CONSTANTS moved. The PHYSICS/measurement code stays IN the functions —
    `fg_frac`, band max, `pstdev` spread, distinct depth-band counting, section detection
    — and the measurement/presentation thresholds (`stereo_width > 0.6`, `distinct <= 1`,
    the `score < 55` evidence gate) stay hardcoded (producer-AGNOSTIC, not producer
    taste). Clean literal→`c["…"]` substitution; formula shape/order preserved; int/float
    types match. The formula's numeric result is unchanged.
  - **Byte-identical by construction:** existing doctrine tests pass UNEDITED; regression
    **68/68, 0 critical, 0 warnings — UNCHANGED** (the corpus byte-identical proof —
    doctrine feeds `doctrine_score`, golden-pinned). Reviewer INDEPENDENTLY confirmed live
    `doctrine_score` byte-matches the golden on all 3 fixtures, incl.
    `overall_mix_readiness_score`. Round-trip NON-VACUOUS (an 18→17 flip fails the test +
    shifts `_section_contrast` 64→66).
  - **No-aliasing PROVEN (the per-module safety invariant — DISCHARGED for doctrine):**
    grep confirmed no in-place mutation of the sourced structures; the no-aliasing test
    runs `score_doctrine` on a fixture (+ crafted multi-penalty inputs) and asserts the
    shared `_DEFAULT_PROFILE` structures are byte-unchanged afterward. Determinism holds.
    `creative.py` / `governance.py` / `pipeline.py` byte-unchanged.
  - **Two commits `29b9dfe` (Part A + no-aliasing test — green in isolation = 364) +
    `72e98a7` (Part B widen + source + round-trip).** Suite **351 → 370 passed** (+19; 0
    failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical, 0
    warnings — UNCHANGED.** Safety grep clean; UI N/A. qa **GREEN**; reviewer **pass.**
    **Codex NOT available — single-reviewer verdict.** **P-028 local-only** (commits
    `29b9dfe`, `72e98a7` on the dev branch on top of the P-027 commits on top of the
    `e79426a` base), not pushed/merged.
  - **★★ MILESTONE — THE EXTRACTION PHASE IS COMPLETE.** The entire producer-specific
    judgment layer — creative (P-026), governance (P-027, widened), doctrine (P-028,
    widened) — is now sourced from the reference `ProducerProfile`, BYTE-IDENTICAL, with
    the producer-AGNOSTIC physics chassis + safety kill-switches cleanly separated and left
    hardcoded. **The reference profile now FULLY DRIVES the judgment layer.** **Finding A
    is FULLY RESOLVED** (governance + doctrine secondary constants all captured). **The
    aliasing-proof requirement is DISCHARGED for all 3 consumer modules** (creative,
    governance, doctrine).
  - **★ WATCH-ITEM (reviewer):** a few measurement-vs-aesthetic thresholds
    (`stereo_width > 0.6`, `distinct <= 1`, `score < 55`) are correctly left HARDCODED as
    physics/presentation, NOT producer taste — keep them OUT of the profile when P-029
    threads the profile per-call.
  - **★ EPIC ARC (updated):** **P-025 ✓ (foundation) → P-026 ✓ (creative sourced) →
    P-027 ✓ (governance sourced + WIDENED) → P-028 ✓ (doctrine sourced + WIDENED — the
    LAST & LARGEST; extraction phase COMPLETE)** → **P-029 (THE PIVOT — parameterize the
    pipeline by a per-call producer; `analyze(producer=...)` selects a profile; default =
    reference, byte-identical; ALSO the structural fix that ends the module-singleton
    aliasing risk)** → P-030 (rename the `halee`/`ramone` dims off the producer names) →
    P-031 (confidence framework — consume the metadata stamp) → P-032 (second producer) →
    P-033 (expose producer selection). Receipt:
    `build-os/receipts/P-028-doctrine-sources-values-from-reference-profile.md`.

- **★★ P-027 SOURCES `governance.py` FROM THE REFERENCE PROFILE AND WIDENS THE
  PROFILE (FINDING A) — THE JSON IS THE SINGLE SOURCE OF TRUTH, BYTE-IDENTICAL, WITH
  THE SAFETY CHASSIS KEPT SEPARATE.** Third extraction step of the producer-agnostic
  epic. P-026 sourced `creative.py`; **P-027 sources `governance.py`** AND widens the
  profile with governance's secondary aesthetic constants. **Last-closed = P-027.**
  - **What P-027 shipped — Part A (source already-captured values):** `governance.py`
    gains `_DEFAULT_PROFILE = load_profile("halee_ramone")` and SOURCES
    `_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS` / `TASTE_MAX_DELTA` FROM it; the inline
    literals are DELETED. **The kill-switch SPLIT (the load-bearing safety boundary):**
    `KILL_SWITCHES = _SAFETY_KILL_SWITCHES + _DEFAULT_PROFILE.aesthetic_kill_switches`
    — the **5 SAFETY switches (items 1–5, Class-5 / non-destructive) STAY HARDCODED**
    (producer-AGNOSTIC; must NEVER enter a swappable profile); the **4 AESTHETIC
    switches (items 6–9)** come from the profile; the composed 9-item list is
    byte-identical to the pre-P-027 literal (no safety string appears in the JSON).
  - **Part B — WIDEN the profile (Finding A):** `ProducerProfile` + `halee_ramone.json`
    + the P-025 round-trip gain `taste_triangle` (`intimate_width_penalty: 30`,
    `emotion_dims: [ramone_score, listener_excitement_score, vocal_belief_score]`) and
    `veto_thresholds` (`reject_below: 45`, `align_veto_below: 50`, `align_fallback:
    75`). `taste_triangle` / `govern_variant` now READ these from `_DEFAULT_PROFILE`;
    the emotion blend reproduces `round((ramone + listener_excitement + vocal_belief)
    / 3)` EXACTLY (same fixed dim order, same `round()`).
  - **Byte-identical by construction:** the existing governance/taste tests
    (`test_governance.py`, `test_governance_taste.py`, `test_live_wire.py`; the
    P-007/8/9 taste tests) pass **UNEDITED** — same governance output on the seeded
    fixtures, now sourced from the JSON. **Emotion-blend round() proven byte-identical:**
    reviewer checked ALL **1,030,301** integer triples (0 mismatches); qa checked
    51,520 triples + named `.5`-boundary cases where banker's rounding matters.
  - **No-aliasing PROVEN (the per-module safety invariant — DISCHARGED, binding from
    P-026):** grep confirmed no in-place mutation of the sourced globals;
    `_apply_taste` / `govern_variant` mutate only a LOCAL `triangle`; the no-aliasing
    test confirms the shared `_DEFAULT_PROFILE` structures are byte-unchanged after
    governance runs on a real fixture. Determinism holds. Widened fields round-trip
    non-vacuously (a 30→25 mutation is caught).
  - **No signature/mechanism change; no per-call producer selection yet** (P-029).
    `creative.py` (done) / `doctrine_engine.py` (P-028) / `pipeline.py` (P-029)
    **byte-unchanged.**
  - **Two commits `e4786ca` (Part A + no-aliasing test — green in isolation = 343) +
    `7b1c26d` (Part B widen + source + round-trip).** Suite **331 → 351 passed** (+20;
    0 failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
    0 warnings — UNCHANGED.** Safety grep clean; UI N/A. qa **GREEN**; reviewer
    **pass.** **Codex NOT available — single-reviewer verdict.** **P-027 local-only**
    (commits `e4786ca`, `7b1c26d` on the dev branch on top of the P-026 commit on top
    of the P-025 commits on top of the `e79426a` base), not pushed/merged.
  - **★ STABLE FACT (recorded this close):** **safety kill-switches (Class-5 /
    non-destructive) are producer-AGNOSTIC and stay HARDCODED in `governance.py`
    (`_SAFETY_KILL_SWITCHES`); only AESTHETIC switches are profile-swappable — a
    safety switch must NEVER enter a `ProducerProfile`.** This boundary lets the
    profile become swappable without ever letting a producer disable a safety guard.
  - **★ TRAILER RECONCILED (stop the recurring flag):** the reviewer re-flagged the
    mandated `Co-Authored-By: Claude Opus 4.8` trailer as a "model identifier" vs the
    packet-spec "NO model identifier" line — NO violation: the harness / `CLAUDE.md`
    MANDATE that exact trailer; "Claude Opus 4.8" is the sanctioned trailer form,
    DISTINCT from the exact model ID the identity rule bars. **Action: DROP the "NO
    model identifier" line from FUTURE packet specs (P-028+)** — recorded in residue.
  - **★ WATCH-ITEM (reviewer, mild):** `taste_triangle.emotion_dims` couples the
    profile to the runtime `scores` dict keys — watch this coupling when P-028
    generalizes scoring / P-029 threads the profile per-call.
  - **★ WATCH-ITEM (aliasing, from P-026):** DISCHARGED for governance (P-027);
    remains BINDING for **P-028 (doctrine)** — each extraction packet must
    independently prove its consumers never mutate a sourced global in place. P-029
    (per-call profile) is the structural fix.
  - **★ EPIC ARC (updated):** **P-025 ✓ (foundation) → P-026 ✓ (creative sourced) →
    P-027 ✓ (governance sourced + WIDENED; safety chassis kept separate)** → **P-028
    (doctrine extraction, WIDENED — the LAST and LARGEST; capture ALL doctrine scoring
    functions' constants; +aliasing-proof)** → P-029 (parameterize the pipeline /
    per-call profile) → P-030 (rename the `halee` / `ramone` dims off the producer
    names) → P-031 (confidence framework — consume the metadata stamp) → P-032 (second
    producer) → P-033 (expose producer selection). Receipt:
    `build-os/receipts/P-027-governance-sources-values-from-reference-profile.md`.

- **★★ P-026 LANDS THE FIRST WIRING OF THE PRODUCER-AGNOSTIC EPIC: `creative.py`
  NOW SOURCES ITS PRODUCER-SPECIFIC VALUES FROM THE REFERENCE PROFILE — THE JSON IS
  THE SINGLE SOURCE OF TRUTH, BYTE-IDENTICAL.** P-025 extracted the reference
  `ProducerProfile` (`halee_ramone.json`) and proved byte-identical round-trip but
  nothing consumed it; **P-026 makes `creative.py` the first consumer.**
  **Last-closed = P-026.**
  - **What P-026 shipped:** `creative.py` gains `_DEFAULT_PROFILE =
    load_profile("halee_ramone")` and SOURCES its **8 producer-specific globals**
    FROM the profile — `_KIND_SCORES`, `_NUDGE_TABLE`, `_PROMOTION_TABLE`,
    `CREATIVE_NUDGE_CAP` (2.0), `CREATIVE_PROMOTION_CAP` (4.0), `_RISK_PENALTY`,
    `SEARCH_MODES`, `PHILOSOPHY`. The **hardcoded literals are DELETED** — the
    `halee_ramone.json` is now their **single source of truth.** Same names/shapes,
    so every downstream consumer is untouched; nudge/promotion kinds stay SETS (the
    loader rehydrates them).
  - **Byte-identical by construction (the whole point):** the reference profile ==
    the old literals (P-025's round-trip + the 68/68 regression guarantee it). **The
    P-012 / P-013 / P-015 / P-016 creative tests pass UNEDITED (69 combined)** — the
    same `analyze()` / `score_variant` output on the seeded fixtures, now sourced
    from the JSON. Values spot-checked against the JSON AND the pre-P-026 git
    literals (match).
  - **No-aliasing PROVEN (the per-module safety invariant):** `score_variant` copies
    each `_KIND_SCORES` row via `dict(_KIND_SCORES.get(...))` BEFORE mutating; qa
    forced a nudge AND a promotion to fire, then confirmed the shared
    `_DEFAULT_PROFILE.kind_scores` is byte-unchanged; determinism holds.
  - **No signature/mechanism change; no per-call producer selection yet** (that is
    P-029 — this packet only relocates the SOURCE of the values behind a single
    `_DEFAULT_PROFILE`). `governance.py` / `doctrine_engine.py` / `pipeline.py`
    **byte-unchanged** (P-027 / P-028 / P-029 own those).
  - **Single commit `c4a092d`** (parent `84d208d` = the active-packet confirmation)
    — `creative.py` (+47/−71) + new `test_creative_profile_sourced.py` (12 tests).
    **Green in isolation = 331.** Suite **319 → 331 passed** (+12; 0
    failed/skipped/warnings, green under `-W error`); regression **68/68, 0
    critical, 0 warnings — UNCHANGED** (parent `84d208d` also 68/68 once fixtures
    are generated). Scope: `creative.py` + the one new test only. Safety grep clean;
    UI N/A. qa **GREEN**; reviewer **pass**. **Codex NOT available — single-reviewer
    verdict.** **P-026 local-only** (commit `c4a092d` on the dev branch on top of the
    P-025 commits on top of the `e79426a` base), not pushed/merged.
  - **★ WATCH-ITEM (reviewer — binding for P-027 / P-028):** the copy-before-mutate
    no-aliasing safety is a **PER-MODULE invariant, not a structural guarantee.** As
    this sourcing pattern repeats for governance (P-027) and doctrine (P-028), EACH
    extraction packet MUST independently PROVE its consumers never mutate a sourced
    global in place — grep for in-place mutation + a no-aliasing test like P-026's.
    P-029 (per-call profile) reduces this risk. Recorded in residue as binding.
  - **★ EPIC ARC (as of P-026 close):** P-025 ✓ → P-026 ✓ → P-027 (governance,
    WIDENED + aliasing-proof) → P-028 (doctrine, WIDENED + aliasing-proof) → P-029
    (per-call profile) → P-030 (rename dims) → P-031 (confidence) → P-032 (second
    producer) → P-033 (expose selection). **[SUPERSEDED — see the P-027 block above:
    P-027 is now ✓; NEXT = P-028.]** Receipt:
    `build-os/receipts/P-026-creative-sources-values-from-reference-profile.md`.

- **★★ A NEW EPIC OPENS — THE PRODUCER-AGNOSTIC EPIC — AND P-025 LANDS ITS
  FOUNDATION: TODAY'S HARDCODED HALEE/RAMONE JUDGMENT IS NOW A FROZEN,
  ROUND-TRIP-GUARDED, UNWIRED `ProducerProfile`.** The new epic: make the engine
  PRODUCER-AGNOSTIC — select any producer (Timbaland, Quincy, Ramone, …) and the
  same stems get driven toward that producer's state. The producer-agnostic
  *physics* (analyzers, safety kill-switches, the bounded-nudge mechanism, the
  determinism/evidence contract, the move-kind vocabulary) stays FIXED; the
  producer-specific *judgment* becomes a swappable **`ProducerProfile`.** That
  judgment is **100% hardcoded in Python today** (the pre-existing
  `roy_halee.json` / `phil_ramone.json` are PROSE the scorer never reads) — so the
  reference profile had to be **extracted FROM CODE.** **Last-closed = P-025.**
  - **What P-025 shipped (data + loader ONLY — no wiring):** a frozen
    **`ProducerProfile`** dataclass + a pure **`load_profile(name="halee_ramone")`**
    (`logic_mix_os/doctrine/producer_profile.py`) + the VERBATIM reference
    **`logic_mix_os/doctrine/producers/halee_ramone.json`** holding today's
    producer-specific values. Metadata stamp `{name: halee_ramone, display_name:
    "Roy Halee / Phil Ramone", provenance: hand-curated-documented, confidence:
    high, risk_class: 0}` — the honesty scaffolding for the confirmed sourcing
    policy (consumed in P-031).
  - **The byte-identical ROUND-TRIP guard (the load-bearing safety net for the
    whole extraction arc):** **exact-equal** for clean module constants
    (`kind_scores` = `_KIND_SCORES`, `nudge_table` / `promotion_table`, caps
    `2.0` / `4.0`, `_RISK_PENALTY`, `SEARCH_MODES`, `PHILOSOPHY`, `_TRUTH_ALIGNMENT`,
    `_TASTE_KIND_BIAS`, `TASTE_MAX_DELTA`, aesthetic kill-switches
    `KILL_SWITCHES[5:9]` = items 6–9; **safety items 1–5 correctly EXCLUDED** —
    they are producer-agnostic and stay universal); **indirect** for the
    INLINE-COMPUTED values (`doctrine.weights` / `baselines` 86.0 / `penalty_coeffs`
    / `default_creative_mode`), asserted by driving `_halee` / `_ramone` /
    `_default_creative_mode` one condition at a time. **Proven NON-VACUOUS:** qa
    mutated `ramone.vocal_masked` 6→7 → the test FAILS.
  - **The NO-WIRING guarantee (load-bearing):** `creative.py` / `governance.py` /
    `doctrine_engine.py` / `pipeline.py` are **byte-for-byte unchanged** (verified
    absent from the `e79426a..HEAD` diff); NOTHING in the runtime imports
    `load_profile`; the regression is UNCHANGED because nothing consumes the
    profile. Extract, don't change.
  - **Two commits `195127c` (Commit-1: schema + loader + JSON + round-trip /
    determinism tests; green in isolation = 311) + `e6cb038` (Commit-2:
    extraction-completeness + schema/metadata tests).** Suite **293 → 319 passed**
    (+26; 0 failed/skipped/warnings, green under `-W error`); regression **68/68,
    0 critical, 0 warnings — UNCHANGED** across both commits. Scope: 3 new files
    only; the 4 judgment sources byte-unchanged. Round-trip is an honest set-vs-set
    compare, not loosened. Safety grep clean; UI N/A. qa **GREEN**; reviewer
    **pass** (hand-verified every extracted value byte-accurate against source).
    **Codex NOT available — single-reviewer verdict.** **P-025 local-only**
    (commits `195127c`, `e6cb038` on the dev branch on top of the `e79426a` PR #16
    base), not pushed/merged.
  - **★ COMPLETENESS carry-forward (reviewer Finding A — IMPORTANT for the arc):**
    P-025 captured what its scope declared; additional producer-aesthetic constants
    were deferred by design (not drift). **P-027 ✓ RESOLVED the governance portion**
    — the profile now holds `taste_triangle` (`intimate_width_penalty: 30` +
    `emotion_dims`) + `veto_thresholds` (`reject_below: 45` / `align_veto_below: 50`
    / `align_fallback: 75`), all sourced + round-trip-guarded. **REMAINING for
    P-028:** capture ALL doctrine scoring functions' constants (`_vocal_centrality`
    / `_depth_hierarchy` / `_section_contrast` / `_static_mix` / `_dynamic_mix` —
    baselines 80.0/70.0/40, penalties, coefficients), not just `_halee` / `_ramone`.
  - **★ EPIC ARC (the active roadmap):** **P-025 ✓ (foundation) → P-026 ✓
    (creative sources its values from the profile, byte-identical)** → P-027
    (governance extraction, **WIDENED** + **aliasing-proof**) → P-028 (doctrine
    extraction, **WIDENED** + **aliasing-proof**) → P-029
    (parameterize the pipeline to consume the profile) → P-030 (rename the
    `halee`/`ramone` dims off the producer names) → P-031 (confidence framework —
    consume the metadata stamp) → P-032 (second producer) → P-033 (expose producer
    selection). The prior cowork arc closed at PR #16; the optional P-024 (MCP
    transport) remains a standing, un-opened candidate.

- **★ THE ARC'S TRANSPORT BEGINS — P-023 MAKES THE RAW-CLI AGENT TRANSPORT A
  VERSIONED, SELF-DESCRIBING CONTRACT (option C, step 1 — the first of two
  transport steps).** P-021 proved the cowork CLI is agent-drivable end-to-end;
  P-023 turns that surface into a STABLE, VERSIONED, SELF-DESCRIBING contract
  Claude Cowork can introspect instead of reverse-engineering. The user chose
  **option C (sequenced): documented raw-CLI contract now, MCP server as the
  follow-on P-024.** Last-closed = P-023.
  - **`describe_contract` (registry 34 → 35)** returns pure deterministic JSON
    `{api_version, invocation, commands:{name:{purpose, phase, params,
    side_effect}}}`. `API_VERSION = "1.0"` is a stable string an agent can pin.
  - **`params` DERIVED from each handler's real `inspect.signature`** — dropping
    the leading context arg BY POSITION (def-handlers name it `ctx`, lambdas name
    it `c`) and skipping `**k` — so the contract CANNOT DRIFT from the code
    (`record_mix_pass` → `[name, reverted]`, `detect_masking` → `[]`).
  - **`side_effect` makes live-vs-dead a FIRST-CLASS CONTRACT FACT** (was
    telegraphed by `desc` through P-020, executably pinned by a test in P-021 —
    now a declared contract field): exactly 4 writers — `record_mix_pass` →
    `writes:history(live)`, `update_taste_calibration` → `writes:taste(live)`,
    `write_mix_decision` → `writes:ledger(dead)`, `override_track_identity` →
    `mutates:session` — all other 31 commands `none`. Verified against handler
    BODIES by both qa and reviewer (reviewer scanned all 31 `none` commands; no
    mislabel).
  - **Completeness invariant HELD at 35:** `describe_contract` parked in
    `_SESSION_FLOW.auxiliary` (mirroring P-020's `describe_session`), so P-020's
    exact-cover invariant still holds — contract keys == 35 registry keys
    (orphan/phantom fail).
  - **`COWORK_CONTRACT.md`** — a concise integrator-facing doc (invocation
    pattern, api-version/stability guarantee, side_effect vocabulary, product
    guarantees local/non-destructive/plan-only/evidence+risk/Class-5-never, the
    8-phase session flow), pointing at `describe_contract` / `describe_session` as
    the machine-readable source of truth. Verified accurate against the code.
  - **Two commits `60b3b92` (Commit-1: `API_VERSION` + `describe_contract` +
    helpers + `tests/test_cowork_contract.py` + registry 34→35; green in
    isolation = 293) + `dcc4c5b` (Commit-2: `COWORK_CONTRACT.md`).** Suite
    **277 → 293 passed** (+16; 0 failed/skipped/warnings, green under `-W error`);
    regression **68/68, 0 critical, 0 warnings** held (additive read-only →
    goldens untouched). Params match real signatures (no drift); side_effect
    honesty verified against bodies; versioned + deterministic; registry 35, both
    count assertions 34→35, no stale 34. Scope: only 5 authorized files; `cli.py`/
    creative/governance/ledger/memory/pipeline untouched; existing tests changed
    only the count assertion. Safety grep clean; UI N/A. qa **GREEN**; reviewer
    **pass**. **Codex NOT available — single-reviewer verdict.** **P-023
    local-only** (commits `60b3b92`, `dcc4c5b` on the dev branch on top of the
    `6c40e2b` PR #15 base), not pushed/merged.
  - **Reviewer watch-item carried to P-024 (non-blocking):** `API_VERSION` is a
    hand-maintained string with NO test that fails when a command's `params` /
    `side_effect` changes without a version bump — so the VERSION can drift from
    the surface even though params/side_effect cannot drift from code. **P-024
    (the MCP server) is where to add a version-fingerprint guard** (a test pinning
    a hash of the contract surface). P-024 can also reuse `describe_contract`'s
    per-command metadata directly as MCP tool schemas.
  - **★ ARC STATUS:** P-019 ✓ (loop closeable inside cowork), P-020 ✓
    (self-describing session flow), **P-021 ✓ (MILESTONE — end-to-end drive +
    loop-close proven)**, **P-023 ✓ (option C step 1 — versioned self-describing
    raw-CLI contract).** **The ONLY remaining arc step is P-024 (option C step 2 —
    a thin MCP server wrapping the same registry, reusing `describe_contract`
    metadata for tool schemas + the version-fingerprint guard) — the FINAL step.**
    After P-024, the arc to the Cowork-usable final state is COMPLETE; landing the
    accumulated P-017-guard → P-024 work on default is the natural close
    (USER-GATED). **P-022 stays OPTIONAL / UNNEEDED.**


- **★★ MILESTONE — P-021 PROVES THE COWORK SURFACE IS AGENT-DRIVABLE END-TO-END
  (arc step 3 of 5; the step that PROVES it).** The canonical target — Logic Mix
  OS as a tool Claude Cowork can drive END-TO-END in a Logic Pro mixing session
  (plan-only v1) — is now essentially **MET AT THE DECISION-SYSTEM LEVEL.** P-021
  (TESTS-ONLY) drives a full mixing session THROUGH the cowork surface only
  (`build_context` + `run_command`), in `describe_session`'s canonical order, and
  the learning loop CLOSES within the surface. No product change; no honesty-clause
  gap found — every phase's essential command was reachable and the loop closed
  across the full session.
  - **The driven spine (8 phases, via `run_command`, NOT bypassing to
    `analyze()` / `record_pass`):** intake → `intake_project`, classify →
    `classify_tracks`, diagnose → `detect_masking`, plan → `generate_mix_plan`,
    checklist → `render_logic_checklist`, validate → `validate_mix_pass`,
    record-outcome → `record_mix_pass` (LIVE), next-pass → `suggest_next_pass`.
    Each output JSON-serializable + shape-asserted; the chain never drops out of
    the surface.
  - **The loop CLOSES (milestone assertion — load-bearing + non-tautological):**
    `record_mix_pass(..., reverted=True)` on the LIVE channel → a FRESH
    `build_context(memory_dir=...)` → `suggest_next_pass` surfaces the confirmed
    "Revert last pass" (evidence contains "confirm"), NO hand re-run. **Proven
    load-bearing** (qa AND reviewer independently — dropping `reverted` / routing
    off the live channel → the assertion FAILS; reviewer via monkeypatch) and
    **non-tautological** (the identical score-IMPROVED sequence with
    `reverted=False` surfaces NO revert).
  - **Live-vs-dead pinned as an EXECUTABLE fact (resolves the carried P-020 clarity
    nudge):** `write_mix_decision` (DEAD ledger — writes only `decision_ledger.json`,
    runtime-verified) does NOT change next-pass; `record_mix_pass` (LIVE history)
    does. Only `record_mix_pass` closes the loop.
  - **Honest skips (none an essential linear phase):** `compare_to_reference`
    (needs a reference bounce → `{"note": "no reference supplied"}`),
    `override_track_identity` (param-heavy / mutating), `build_missing_tool` /
    `run_creative_engine` / `describe_session` (auxiliary / off-axis).
  - **PRECISION (do NOT overstate):** the coverage-honesty test
    (`test_walkthrough_covers_the_registry_honestly`) guards PHASE-COMPLETENESS
    (every `describe_session` phase has a driven essential command belonging to it)
    + test-1's exact 8-phase order pin — it does NOT assert a full
    `driven ∪ skipped == 34` registry partition (it references 13 of 34). The full
    34-command exact-cover partition is guarded SEPARATELY by P-020's
    `test_cowork_session_flow.py` (31 phases + 3 auxiliary = 34). Together the two
    files tell the truth about registry coverage.
  - **Single commit `dce156b` (TESTS-ONLY):** adds exactly ONE file
    `tests/test_cowork_session_walkthrough.py` (8 tests, +372); no product/runtime
    file changed, no existing test edited. Suite **269 → 277 passed** (+8; 0
    failed/skipped/warnings, green under `-W error`); regression **68/68, 0
    critical, 0 warnings** held; Commit-1 green in isolation (277; single commit =
    tip); determinism confirmed (two contexts → byte-identical plan/next-pass);
    safety grep clean; UI N/A. qa **GREEN**; reviewer **pass** (empirically
    re-verified load-bearing via monkeypatch; genuine drive, not a bypass; honest
    skips). **Codex NOT available — single-reviewer verdict.** **P-021 local-only**
    (commit `dce156b` on the dev branch on top of the `6c40e2b` PR #15 base), not
    pushed/merged.
  - **★ SYNTHESIS (the strategic headline):** the canonical target is essentially
    MET at the decision-system level — an agent using ONLY the cowork surface can
    drive the complete plan-only session (intake → … → next-pass) AND learn from
    outcomes (record → loop closes), entirely within the surface, proven
    executably. What remains is genuinely only **transport packaging** — **P-023**
    (MCP server vs documented raw-CLI contract), a USER-GATED architecture
    decision. **P-022 stays OPTIONAL / UNNEEDED** — the honesty clause surfaced no
    real gap requiring it.

- **★ THE ARC ADVANCES — P-020 MAKES THE COWORK SURFACE SELF-DESCRIBING AS AN
  ORDERED, PHASE-GROUPED SESSION FLOW (arc step 2 of 5).** `list_commands` is a flat
  alphabetized catalog; an agent could not read the canonical end-to-end SEQUENCE
  from it. **P-020 adds a pure `_SESSION_FLOW` structure + a read-only
  `describe_session` command (registry 33 → 34)** that returns the SAME registry as
  `{"phases": [...ordered...], "auxiliary": [...]}` in the canonical order **intake
  → classify → diagnose → plan → checklist → validate → record-outcome →
  next-pass**. **31 commands** map onto the 8 linear phases; **3 are honestly
  `auxiliary`** (off the linear axis): `run_creative_engine` (parallel creative
  exploration), `build_missing_tool` (meta tooling-gap helper), `describe_session`
  (self-describing). Honesty clause honored — no fabricated flow; `suggest_next_pass`
  placed ONCE (in `next-pass`), not double-listed.
  - **Completeness INVARIANT (the load-bearing guard):** every `COMMANDS` key
    appears EXACTLY ONCE across phases + auxiliary (exact cover — no orphan, no
    duplicate), keeping the flow honest as commands are added. Proven load-bearing
    (orphan/duplicate → the test fails); qa independently verified the partition
    **31 + 3 = 34 = len(COMMANDS)**.
  - **Additive / read-only:** `list_commands` / `run_command` / every existing
    handler are BYTE-UNCHANGED; `describe_session` is deterministic (byte-identical
    across calls) and DEEP-COPIES its output so callers can't mutate the module
    structure. Single commit `942a68a` (purely additive `cowork.py` +100, new
    `tests/test_cowork_session_flow.py` 10 tests, the one intended `test_cowork.py`
    count assertion 33→34). Suite **259 → 269** (+10; green under `-W error`);
    regression **68/68, 0 critical**; Commit-1 green in isolation (269; single
    commit = tip). qa **GREEN**; reviewer **pass** (verified every command placement
    against its real handler; two defensible judgment calls — `score_mix` and
    `compare_to_reference` in `plan`). **Codex NOT available — single-reviewer
    verdict.** **Reviewer non-blocking flag carried to P-021:** `write_mix_decision`
    (dead ledger) and `record_mix_pass` (live history) both sit under
    `record-outcome` but the dead/live distinction is NOT surfaced in
    `describe_session`'s output — add a one-line clarity nudge in the P-021
    walkthrough. **P-020 local-only** (commit `942a68a` on the dev branch on top of
    the `6c40e2b` PR #15 base), not pushed/merged.

- **★ THE CANONICAL TARGET HAS AN ARC — P-019 LANDS ITS FIRST STEP: THE LEARNING
  LOOP IS NOW CLOSEABLE INSIDE THE COWORK SURFACE (read/write SYMMETRIC).** The
  canonical target is Logic Mix OS as a tool Claude Cowork can drive END-TO-END in
  a Logic Pro mixing session (plan-only v1; the agent/human executes). The
  orchestrator opened an arc to that state — **P-019 → P-023** — and **P-019 is the
  FIRST step, now DONE.** Until now the cowork surface was coherent for the FORWARD
  half (intake → classify → diagnose → plan → checklist → validate →
  `suggest_next_pass`) and the READ side of the learning loop was live through
  cowork (P-009), but the registry had **NO command to RECORD a pass outcome** —
  the P-018 confirmed-outcome signal was reachable only via the SEPARATE
  `memory-record` CLI verb. P-019 adds a **`record_mix_pass`** command (registry
  **32 → 33**) whose handler records a pass on the LIVE history channel
  (`ctx["memory"].record_pass(name, ctx["result"], reverted=...)` →
  `mix_pass_history.json`), passing through the P-018 `reverted` ground-truth flag
  (opt-in, default False), returning the record JSON — with a clean
  `{"error": "no memory_dir configured"}` when no memory dir (mirrors
  `_write_mix_decision`). **So an agent driving through cowork can now RECORD an
  outcome and see `suggest_next_pass` change WITHOUT leaving the surface** — the
  read/write cowork surface is symmetric. Routes to the LIVE channel, NOT the dead
  decision ledger.
  - **One surface finding, resolved minimally (NOT a wall):** the cowork
    `--params '{...}'` path unpacks user JSON into `run_command(name, ctx, **params)`,
    so a handler param named `name` collided with the dispatcher's positional
    `name`. Fixed by making the dispatcher's `name`/`ctx` **positional-only**
    (`run_command(name, ctx, /, **params)`) — behavior-preserving: a repo-wide grep
    found ZERO callers passing `name=`/`ctx=` by keyword (the sole product caller
    `cli.py:237` passes positionally). Param-naming, not a missing wire.
  - **LIVENESS proven load-bearing (the P-016/P-018 lesson honored):**
    `test_loop_closes_through_cowork_no_rerun` records a confirmed revert via
    `run_command("record_mix_pass", ...)` on a score-IMPROVED override case, then a
    FRESH `build_context(memory_dir=...)` → `run_command("suggest_next_pass")`
    surfaces the confirmed "Revert last pass" — **NO hand re-run.** Both qa and
    reviewer INDEPENDENTLY broke the wiring (handler off the live channel) → the
    test FAILS; restored → PASSES. The loop closes THROUGH the cowork surface.
  - **Routes to the live channel (runtime probe):** only `mix_pass_history.json`
    created, never `decision_ledger.json`. **Byte-identical default:**
    date-neutralised canonical JSON equal to the standalone `memory-record`.
  - Two commits (≤2): `b7572b7` Commit-1 (handler + registry row + positional-only
    + unit tests; green in isolation = 257) + `de5679f` Commit-2 (no-re-run
    liveness guard). Scope: only 3 files (`cowork.py` additive,
    `test_cowork.py` count assertion 32→33, new `tests/test_cowork_record.py`);
    `memory.py`/`cli.py`/`pipeline.py`/ledger/creative/governance UNTOUCHED. qa
    **GREEN**; reviewer **pass** (handler correct + routes live [verified by
    breaking it]; positional-only safe/minimal; loop closes through cowork;
    non-tautological override case). **Codex NOT available — single-reviewer
    verdict.**

- **★ THE OUTCOME→LEARNING AXIS IS NOW OPEN — P-018 SHIPS THE FIRST
  CONFIRMED-OUTCOME SIGNAL IN THE LEARNING LOOP (a PIVOT off the complete
  judgment-tuning path onto the feedback frontier; user said "Yes").** Until
  now every loop signal was score-INFERRED (`record_pass` guesses "that
  regressed, maybe revert" from score deltas). P-018 adds a CONFIRMED one. An
  opt-in `memory-record --reverted` records a confirmed operator revert on a
  pass (`record_pass(..., reverted=True)` → `mix_pass_history.json`); the live
  `_apply_history` consumer (already threaded to real `analyze(--memory-dir)`
  via P-009) then, on a confirmed revert, DEMOTES the recommended-then-reverted
  moves and surfaces exactly ONE confirmed "Revert last pass" item at priority
  95 — **regardless of the score-delta `got_worse` inference (OVERRIDE)**, with
  an early-return that prevents double-up with the score-inferred revert. Distinct
  honest evidence line ("…because the operator confirmed reverting the last
  pass" — contains "confirm", vs the score-inferred "recorded revert
  candidate(s): …").
  - **OVERRIDE semantics (chosen by the orchestrator-in-chief; user may redirect
    at the merge gate):** a confirmed operator revert is GROUND TRUTH and takes
    precedence over the score-inferred guess when they disagree — the
    doctrine-honest, operator-serving choice (a confirmed action outranks a
    heuristic proxy).
  - **Why THIS seam (the dead-ledger finding):** the decision LEDGER
    (`add_decision` → `decision_ledger.json`) has ZERO analyze-path consumers
    (`mem.ledger()` is display-only at `cli.py:315`), so a producer for any
    reserved ledger event would be INERT — the hollow trap. The ONLY reachable
    LIVE seam was the history axis (`record_pass` → `_apply_history`), which is
    why the confirmed revert lands there.
  - **Opt-in / byte-identical by default:** no `--reverted` → the `reverted` key
    is not written and `next_pass` is unchanged vs today.
  - **LIVENESS proven load-bearing (the P-016 lesson honored):** the no-re-run
    liveness test asserts on real `analyze(memory_dir=...)` `next_pass` and FAILS
    with the pre-P-018 `_apply_history` (confirmed revert doesn't reach analyze
    output = would be inert) and PASSES at tip — NOT inert. **Override
    non-vacuous:** with an IMPROVED score delta (`got_worse` empty) but
    `reverted=True`, the confirmed item still surfaces at rank 0 and the reverted
    move is demoted — proving override, not an echo of the score signal.
  - Two commits (≤2): `736fa8b` Commit-1 (`record_pass` field + `_apply_history`
    override + 9 unit tests; green in isolation = 249) + `6134d27` Commit-2
    (`--reverted` CLI wire + 4 no-re-run liveness/CLI tests). qa **GREEN**
    (mutation-verified liveness + non-vacuous override); reviewer **pass**
    (override bounded/deterministic; early-return skips only the score-inferred
    revert; demotes exactly the reverted pass's recommended moves). **Codex NOT
    available — single-reviewer verdict.**

- **★ THE JUDGMENT LAYER IS AT A DOCTRINE-HONEST EQUILIBRIUM — P-017 (the FIRST
  base-value re-curation attempt) CLOSED AS A VERIFIED NEGATIVE FINDING.** The user
  chose "A": try a minimal, doctrine-honest re-curation of
  `_KIND_SCORES["depth_cleanup"]` so the depth/hierarchy move wins the `density`
  branch over `subtractive_drop` — with a hard honesty constraint (never inflate a
  dim to force a win). **FINDING: an honest re-curation CANNOT flip `density` —
  arithmetically forced by the DOCTRINE, verified adversarially.** `_KIND_SCORES`
  is **LEFT UNTOUCHED (no product change)**; the honesty clause held (P-014
  discipline: honesty beats the flip). The builder committed ONLY a 12-test
  characterization guard.
  - **The forced arithmetic:** `overall = mean(7 dims) − risk_penalty`.
    `depth_cleanup` base overall **81.14** (dim sum 568) vs `subtractive_drop`
    **85.29** (dim sum 597, low risk) → gap **4.14**. The one doctrine-defensible
    under-valuation is `contrast` (dc 72 vs sd 88): `contrast → 88` = **83.43**
    (short 1.86); `contrast → 100` (impossible ceiling) = **85.14** — STILL below
    85.29. A FULL honest re-curation (contrast→88, technical→85, ramone→86,
    taste→86; halee stays 90=max, vocal_belief stays 86; **excitement LOCKED at
    66**) reaches only **83.86** (short 1.43). The entire residual deficit lives in
    `excitement` (66 vs 78), OFF-LIMITS to inflate (subtle depth work is honestly
    un-flashy). The only flips require inflating `excitement` or re-labeling a depth
    pass as vocal-forward — both dishonest.
  - **The committed guard (load-bearing, non-tautological):**
    `tests/test_density_recuration.py` (12 tests, +183, commit `1b03ad3`) pins the
    5-branch winner table UNCHANGED on the real `analyze()` path + the honest-ceiling
    arithmetic + `_KIND_SCORES` untouched. Proven load-bearing: injecting an inflated
    `depth_cleanup` (contrast=88+excitement=90, or all dims=100) makes the density
    guard FAIL (density flips to `density_A`) — it genuinely catches an
    accidental/dishonest density flip. Committing executable arithmetic is defensible
    (unlike P-014's no-commit finding) because the finding IS arithmetic and the
    variant-scoring path is golden-unguarded.
  - **THREE LEVERS CONVERGE (the equilibrium):** penalty (P-012/P-015) — saturated,
    only the `vocal_belief` near-tie (gap 1.71<cap 2.0) flippable, P-015 made it
    decisive; reward/promotion (P-016) — saturated at cap 4.0, only `loop` (gap 3.43)
    cleanly reachable, P-016 made it decisive (density gap 4.14 unreachable +
    circular gate; drum_room_bloom hollow); base-value re-curation (P-017) — honest
    re-curation cannot flip density either. **Conclusion: subtractive_drop's default
    dominance is legitimate; the masked-vocal and foregrounded-loop overrides are the
    only doctrinally-warranted flips; there is NO honest further flip move inside the
    current dimension set.** The one remaining honest thread is a SYMMETRIC
    re-judgment (is subtractive_drop itself slightly over-valued?) — user-gated,
    un-signed-off, NOT staged.

- **THE PENALTY-ONLY LINE IS CROSSED — P-016 SHIPS THE FIRST REWARD/PROMOTION
  NUDGE (loop branch), EVIDENCE-GATED AND NOW LIVE IN PRODUCTION (MERGED via PR
  #15, merge commit `6c40e2b`).** User-delegated (direction A "open the base-scoring
  decision space" + fork (i) "evidence-gated" + "keep skating"; the
  build-orchestrator routed it). When the analyzers flag a genuinely foregrounded /
  dominating loop — the REAL `source_auditors` `"foregrounded loop"` red_flag
  corroborated by `provenance` `high_risk` — a bounded promotion
  (`CREATIVE_PROMOTION_CAP = 4.0`, a SEPARATE constant from the ±2.0 penalty
  `CREATIVE_NUDGE_CAP`) lifts `loop_deconstruct` past `subtractive_drop` to win the
  `loop` branch: `loop_deconstruct` 81.9 → **85.9** (raw +5.0 clamped to exactly
  +4.0 = the cap binds) > `subtractive_drop` 85.3 → loop winner flips `loop_B` →
  `loop_A` by 0.6 (governed winner also flips, no veto). **No such evidence →
  `subtractive_drop` stays the default.** Grounded in the system's OWN
  `anti_template` doctrine ("vary the move per problem") + `loops_not_foregrounded`
  + `source_material_respected` + the kill-switch "never allow a stock loop to
  dominate the song identity." Bounded, transparent (emits a `loop_promotion`
  `score_nudges` line), pure/deterministic, layered on an UNTOUCHED `_KIND_SCORES`
  and an UNTOUCHED penalty path.
  - **★ THE P-009-STYLE CATCH (record prominently):** Commit-1's mechanism was
    **INERT in production** — the orchestrator-in-chief caught it before close. In
    `pipeline.analyze()`, `run_creative_engine` ran BEFORE `provenance` /
    `source_audits` were populated, so the promotion predicate always read empty
    evidence and NEVER fired in the real `analyze()` output; Commit-1's tests
    passed only because they RE-RAN `run_creative_engine` on the finished result.
    **Commit-2 fixed it** with a minimal live-wire: relocated `analyze_provenance`
    + `audit_all` to just BEFORE `run_creative_engine` (a pure relocation — their
    inputs are populated ~90 lines earlier), plus two production-liveness tests
    that assert on the real `analyze()` `result.creative` / `result.governance`
    WITHOUT any re-run (they FAIL pre-reorder, PASS after). The promotion is now
    genuinely live.
  - **Reorder SAFE BY CONSTRUCTION:** `governance.py` has ZERO references to
    `provenance` / `source_audits`; `creative.py`'s ONLY reads are inside the new
    `_foregrounded_loop` predicate → nothing but the promotion consumes those
    attrs in the reordered region → default output cannot change. Backed by a
    12-artifact byte-identical diff across all 3 seeded fixtures.

- **THE P-012 NUDGE IS NO LONGER TRANSPARENCY-ONLY — P-015 MAKES IT DECISIVE ON
  THE MASKED-VOCAL NEAR-TIE (USER-SIGNED-OFF AESTHETIC CHANGE).** P-014 proved a
  near-tie creative FLIP was structurally UNREACHABLE test-only **under the
  then-current curation**. The user chose **"Option 1 — Proceed, corrected"**
  (2026-06-30). **P-015** edits `creative.py` `_NUDGE_TABLE` row-0 (`lead_masked`)
  ONLY: **(1) exempt `intimacy_pass`** (an intimacy pass is the CORRECT response to
  a masked lead vocal) and **(2) strengthen the penalty `−8` → `−14`** (`= −2.0`
  overall = EXACTLY the existing `CREATIVE_NUDGE_CAP = 2.0`, UNCHANGED). Net: in
  the `vocal_belief` branch under a masked lead vocal, `vocal_ride` (vocal_A)
  82.9 → **80.9** (cap binds), `intimacy_pass` (vocal_B) 81.1 unchanged (exempt) →
  **winner FLIPS `vocal_ride` → `intimacy_pass`** by 0.2. **Bounded — cannot
  overturn a clear ranking** (`subtractive_drop` still wins its branches).

- **THE P-012 CREATIVE NUDGE IS PROVEN ON REAL DATA THROUGH `analyze()`.** With
  **P-013** (tests-only), the bounded penalty-only evidence-nudge layer is lifted
  from the unit level to the **live `pipeline.analyze()` production path** — on
  `dense_chorus_with_loops` the row-1 nudge (`vocal_belief −6`) fires on the
  `chorus_lift` `width_bloom` variant, lowering `overall_score` 75.7 → 74.9 (inside
  the ±2.0 cap), winner unchanged (option-(a)). The P-013 visibility tests still
  pass unchanged after P-015, P-016, and P-017.

- **THE CREATIVE-SCORING AESTHETIC DECISION IS RESOLVED (option B, P-012), MERGED
  (PR #13), MADE DECISIVE (P-015), EXTENDED TO REWARD (P-016, MERGED PR #15), AND
  ITS BASE-VALUE LEVER PROBED (P-017 — no honest flip).** The bounded, transparent,
  capped evidence-nudge layer ON TOP of the curated `_KIND_SCORES` (values
  UNCHANGED) is live on default via PR #13; P-015 tunes row-0 to be decisive on the
  masked-vocal near-tie; **P-016 crosses into REWARD with the first promotion row
  (loop branch), now on default via PR #15;** **P-017 confirmed the base values
  themselves are doctrine-honest (no flip of density is honestly reachable).** The
  judgment layer is now at equilibrium.

- **THE ALBUM-MEANS TRUTH IS SINGLE-SOURCED.** Via **P-011**, the album means live
  in exactly ONE place: `album.py::analyze_album` additively emits per-song
  `brightness_delta` / `lufs_delta` and `cli.py::_run_album` consumes them; the
  duplicate `statistics.mean` recompute is gone. The `album` report stays
  value-identical.
- **MILESTONE (still standing) — THE CROSS-SONG COHERENCE AXIS IS OPEN.** Via
  **P-010**, a song's plan (through the `album` command) reflects its album
  siblings: album-aware per-song guidance, opt-in / bounded / evidence-tagged. **The
  product is no longer strictly song-isolated.**
- **MILESTONE (still standing) — THE LEARNING LOOP IS REAL IN PRODUCTION.** The
  full arc **P-007 (consumer) → P-008 (outcome) → P-009 (live wire)** is closed
  end-to-end: a real `cowork --memory-dir` run both **learns** and **personalizes**.
- **POSITIVE ALIGNMENT FINDING (from P-013) — taste cannot flip a governed winner
  on curated data, BY DESIGN.** `_apply_taste` moves only the `taste_triangle`
  identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and is
  align-vetoed before it can reorder a truth-ranked winner. The reachable taste
  claim is proven on real data by
  `tests/test_live_wire.py::test_taste_axis_changes_governance`.
- **Last closed packet:** **P-028** (doctrine sourced from the reference profile,
  WIDENED — the last & largest extraction; the EXTRACTION PHASE is COMPLETE). See the
  P-028 block at the TOP of "Where we are" for the authoritative snapshot. The
  chronological narrative below is retained as HISTORY (P-021 → P-020 → …).
- **[HISTORY] P-021** — verified end-to-end agent walkthrough
  through the cowork surface (TESTS-ONLY) — **the MILESTONE** (THIRD step of the arc
  P-019→P-023; the step that PROVES the Cowork-usable end-to-end state). Drives a
  full plan-only mixing session THROUGH the cowork surface only (`build_context` +
  `run_command`), in `describe_session`'s canonical order, and closes the learning
  loop within the surface. **The driven spine (8 phases, via `run_command`, NOT
  bypassing to `analyze()`/`record_pass`):** intake→`intake_project`,
  classify→`classify_tracks`, diagnose→`detect_masking`, plan→`generate_mix_plan`,
  checklist→`render_logic_checklist`, validate→`validate_mix_pass`,
  record-outcome→`record_mix_pass` (LIVE), next-pass→`suggest_next_pass` (each
  JSON-serializable + shape-asserted). **The loop CLOSES (milestone assertion):**
  `record_mix_pass(..., reverted=True)` (LIVE) → FRESH `build_context(memory_dir=...)`
  → `suggest_next_pass` surfaces the confirmed "Revert last pass" (evidence contains
  "confirm"), NO hand re-run — **proven load-bearing** (qa AND reviewer independently;
  reviewer via monkeypatch) and **non-tautological** (identical score-IMPROVED
  sequence with `reverted=False` → NO revert). **Live-vs-dead pinned executably**
  (resolves the carried P-020 nudge): `write_mix_decision` (DEAD ledger) does NOT
  change next-pass; `record_mix_pass` (LIVE history) does. **Honest skips**
  (`compare_to_reference` needs a reference, `override_track_identity`,
  `build_missing_tool`/`run_creative_engine`/`describe_session`) — none an essential
  phase. **PRECISION:** the coverage-honesty test guards PHASE-COMPLETENESS + the
  8-phase order (references 13 of 34), NOT a full 34-registry partition — P-020's
  `test_cowork_session_flow.py` holds the 34-command exact cover (31+3=34); together
  they tell the truth about coverage. **Single commit `dce156b`** (TESTS-ONLY; one
  new file `tests/test_cowork_session_walkthrough.py`, 8 tests, +372; no
  product/runtime file changed, no existing test edited; single commit = tip, green
  in isolation = 277). Suite **269 → 277 passed** (+8; 0 failed/skipped/warnings,
  green under `-W error`); regression **68/68, 0 critical, 0 warnings** held;
  determinism confirmed; safety grep clean; UI N/A. qa **GREEN**; reviewer **pass**
  (empirically re-verified load-bearing via monkeypatch; genuine drive; honest skips).
  **Codex NOT available — single-reviewer verdict.** **★ SYNTHESIS:** the canonical
  target is essentially MET at the decision-system level; only P-023 transport
  packaging (USER-GATED) remains; **P-022 optional/unneeded (no gap surfaced).**
  **P-021 is local-only** (commit `dce156b` on the dev branch on top of the `6c40e2b`
  PR #15 base), not pushed/merged. Receipt:
  `build-os/receipts/P-021-verified-end-to-end-cowork-walkthrough.md`.
- **P-020 (prior close)** — `describe_session` session-flow
  discoverability (SECOND step of the arc P-019→P-023 to the Cowork-usable
  end-to-end state). Adds a pure `_SESSION_FLOW` structure + a read-only
  `describe_session` command to the cowork registry (count **33 → 34**) that returns
  the SAME registry as an ORDERED, phase-grouped session flow
  `{"phases": [...], "auxiliary": [...]}` in the canonical order **intake → classify
  → diagnose → plan → checklist → validate → record-outcome → next-pass**. **31
  commands** map onto the 8 linear phases; **3 are honestly `auxiliary`** (off the
  linear axis: `run_creative_engine`, `build_missing_tool`, `describe_session`).
  Honesty clause honored (no fabricated flow; `suggest_next_pass` placed ONCE).
  **Completeness INVARIANT (load-bearing):** every `COMMANDS` key covered EXACTLY
  ONCE across phases + auxiliary (exact cover; orphan/duplicate → test fails); qa
  independently verified **31 + 3 = 34 = len(COMMANDS)**. Additive / read-only:
  `list_commands` / `run_command` / every existing handler byte-unchanged;
  `describe_session` deterministic + deep-copies its output. Single commit
  **`942a68a`** (purely additive `cowork.py`; new `tests/test_cowork_session_flow.py`,
  10 tests; the one intended `test_cowork.py` count assertion 33→34; single commit =
  tip, green in isolation = 269). Suite **259 → 269 passed** (+10; 0
  failed/skipped/warnings, green under `-W error`); regression **68/68, 0 critical,
  0 warnings** held (additive read-only → goldens untouched); registry 34, no stale
  33; safety grep clean; UI N/A; existing cowork + P-008/P-009/P-018/P-019 tests
  green. qa **GREEN**; reviewer **pass** (verified every command placement against
  its real handler; two defensible judgment calls — `score_mix` and
  `compare_to_reference` in `plan`). **Codex NOT available — single-reviewer
  verdict.** **Reviewer non-blocking flag carried to P-021:** the live-vs-dead-ledger
  distinction (`record_mix_pass` live history vs `write_mix_decision` dead ledger,
  both under `record-outcome`) is NOT surfaced in `describe_session`'s output — add a
  one-line clarity nudge in the P-021 walkthrough. **P-020 is local-only** (commit
  `942a68a` on the dev branch on top of the `6c40e2b` PR #15 merge base), not
  pushed/merged at close. Receipt:
  `build-os/receipts/P-020-describe-session-flow-discoverability.md`.
- **P-019 (prior close)** — `record_mix_pass` closes the learning loop INSIDE the
  cowork surface (FIRST step of the arc). Adds a `record_mix_pass` command (registry
  32→33) whose handler records a pass on the LIVE history channel
  (`record_pass(name, result, reverted=...)` → `mix_pass_history.json`), so an agent
  can close the loop (record → see `suggest_next_pass` change) without leaving the
  surface. Surface finding resolved minimally (dispatcher `name`/`ctx` positional-only;
  behavior-preserving, zero keyword callers). Two commits `b7572b7` (Commit-1: green
  in isolation = 257) + `de5679f` (Commit-2: no-re-run liveness guard). Suite **253 →
  259 passed** (+6); regression **68/68, 0 critical** held; byte-identical default;
  liveness proven load-bearing; routes to the live channel (only
  `mix_pass_history.json`, never `decision_ledger.json`). qa **GREEN**; reviewer
  **pass**. **Codex NOT available — single-reviewer verdict.** **P-019 local-only**
  (commits `b7572b7`, `de5679f` on the dev branch on top of the `6c40e2b` PR #15 base),
  not pushed/merged. Receipt:
  `build-os/receipts/P-019-record-mix-pass-closes-loop-in-cowork.md`.
- **Now:** **none active.** No product packet in flight.
- **Next — THE ARC IS DOWN TO ITS LAST STEP: P-023 TRANSPORT (USER-GATED).**
  P-019 closed the learning loop inside the cowork surface (step 1); P-020 made the
  surface self-describing as an ordered, phase-grouped session flow (step 2);
  **P-021 PROVED the surface is agent-drivable end-to-end and the loop closes within
  it (step 3 — the MILESTONE).** The canonical target is now essentially MET at the
  decision-system level, so what remains is only transport packaging:
  - **P-022 — OPTIONAL / UNNEEDED.** The P-021 honesty clause surfaced NO real gap
    requiring session-efficiency / override-propagation work. Do NOT open unless a
    concrete gap emerges.
  - **P-023 — the ONLY remaining arc step: USER-GATED transport decision — MCP
    server vs a documented raw-CLI contract as the agent transport. Do NOT open
    blind; sequenced LAST; needs an explicit user ask.**
- **Also standing — the judgment layer is at a DOCTRINE-HONEST EQUILIBRIUM (flip
  program complete); the OUTCOME→learning axis is OPEN (P-018 + P-019).** The
  penalty, reward, and base-value re-curation levers have all converged:
  subtractive_drop's dominance is legitimate and no honest further flip exists in
  the current dimension set. Remaining threads:
  - **★ Outcome-enum generalization (reviewer's P-018 trajectory note — candidate,
    NOT staged):** widen the `reverted: bool` field to a small outcome enum
    (`reverted`/`kept`/`refined`) to round out the outcome→learning loop — widens
    WITHOUT breaking the byte-identical default; user-gated for the semantics.
  - **The ledger is DEAD (P-018 finding):** `add_decision`/`decision_ledger` has
    NO analyze-path consumer (display-only). A confirmed-outcome producer is only
    real if it lands on a LIVE channel (history or taste), not the ledger.
  - **★ The one open honest thread — SYMMETRIC re-judgment (user-gated, NOT
    staged):** is `subtractive_drop` at 85.29 (high on every dim) itself slightly
    OVER-valued? Lowering it (rather than inflating a rival) would be a different,
    un-signed-off packet. Surface to the user; do NOT open without an explicit ask.
  - **Reward-family (further reward rows) and re-curation-for-flips are now CLOSED
    as saturated / equilibrium** — not candidates unless the dimension set itself
    changes.
  - **Wider `--memory-dir` CLI surface** (from P-009 — partly a product question);
    net-new **event-logging** producers (behind a product decision);
    **taste-flip-via-product-change** (user-gated, separate packet). Off-path,
    deferred.

## Stable facts (slow-changing)

- **Hard product constraints (from logic-mix-os/README):** local only / no
  network / no uploads; non-destructive (never writes source audio); no Logic
  automation in v1 (plan + checklist only); deterministic (same inputs → same
  artifacts); every recommendation carries evidence + confidence + risk class;
  Class-5 (destructive) actions are never recommended.
- **Standing guardrails (carried from prior sessions):** no real DAW / Logic /
  AppleScript / subprocess / `.logicx` write / network in tests; fake adapters
  only; keep any `RealLogicSessionAdapter` non-instantiable.
- **★ THE JUDGMENT LAYER IS AT A DOCTRINE-HONEST EQUILIBRIUM (P-017-verified):**
  the penalty (P-015), reward (P-016), and base-value re-curation (P-017) levers
  all converge on the same place. `subtractive_drop`'s default dominance is
  legitimate (subtraction IS the safe default and genuinely out-scores the
  alternatives on the ranked axis); the masked-vocal near-tie override (P-015
  penalty) and the foregrounded-loop promotion (P-016 reward) are the ONLY
  doctrinally-warranted flips; **there is NO honest further flip move inside the
  current dimension set.** The only remaining honest thread is a symmetric
  re-judgment (is subtractive_drop itself over-valued?) — user-gated, un-signed-off.
- **★ An evidence-gated creative nudge is only LIVE if its evidence is computed
  BEFORE `run_creative_engine` (P-016 live-wire lesson).** Masking is pre-creative,
  so P-015 was ALWAYS live; `provenance` / `source_audits` were POST-creative until
  P-016's reorder moved them just before creative. **A green test that RE-RUNS the
  engine on the finished result can MASK production inertness** (the P-009 failure
  mode) — always add a no-re-run liveness assertion on the real
  `result.creative` / `result.governance`.
- **Variant-scoring path is golden-unguarded:** `regression.py` reads
  `doctrine_score`, never `score_variant`, so the 68/68 golden cannot catch a
  creative-scoring change. **Unit + visibility + liveness + characterization tests
  are the binding guard for any `creative.py`/`score_variant`/`_KIND_SCORES`
  change** (P-012's `tests/test_creative_nudges.py`, P-013's
  `tests/test_creative_nudge_visibility.py`, P-015's `tests/test_decisive_nudge.py`,
  P-016's `tests/test_loop_promotion.py` including the two production-liveness
  tests, and **P-017's `tests/test_density_recuration.py`** which pins the 5-branch
  winner table + `_KIND_SCORES` untouched — an inflated `depth_cleanup` makes it
  FAIL).
- **Taste is structurally below truth (P-013-verified):** `_apply_taste` moves only
  the identity axis (clamped ±15), maps only to `width_bloom`/`drum_room_bloom`, and
  is align-vetoed — so taste cannot reorder a truth-ranked governed winner on
  curated data. Working as intended.
- **The creative penalty nudge CAN reorder EXACTLY the `vocal_belief` branch under
  `lead_masked`, within the ±2.0 cap (P-015):** row-0 penalizes `vocal_ride` (`−14`
  raw = `−2.0` overall, the cap) but EXEMPTS `intimacy_pass`, so the 1.71-gap
  near-tie flips to `intimacy_pass` (vocal_B). Binding guard:
  `tests/test_decisive_nudge.py` + updated `tests/test_creative_nudges.py`.
- **The creative PROMOTION (reward) nudge CAN reorder EXACTLY the `loop` branch
  when a loop is genuinely foregrounded, within the +4.0 promotion cap (P-016 —
  the FIRST reward nudge, MERGED via PR #15):** the `_PROMOTION_TABLE` row lifts
  `loop_deconstruct` (81.9 → 85.9, raw +5.0 clamped to exactly +4.0) past
  `subtractive_drop` (85.3); gated on the REAL `source_auditors` `"foregrounded
  loop"` red_flag corroborated by `provenance` `high_risk`; NOW LIVE via the
  pipeline reorder. `CREATIVE_PROMOTION_CAP = 4.0` is a SEPARATE constant from the
  ±2.0 penalty `CREATIVE_NUDGE_CAP`; the penalty table/path is byte-untouched.
  Bounded — cannot overturn a gap ≥ 4.0, and `loop_deconstruct` competes only in
  the `loop` branch. Binding guard: `tests/test_loop_promotion.py`.
- **The `density` branch CANNOT be honestly flipped by base-value re-curation
  (P-017-verified):** `depth_cleanup` (81.14) trails `subtractive_drop` (85.29) by
  4.14; the only doctrine-defensible under-valuation is `contrast` (72→88 = 83.43;
  even →100 = 85.14, still below); the residual deficit lives entirely in
  `excitement` (66 vs 78), which is off-limits to inflate. `_KIND_SCORES` stays
  UNTOUCHED. Binding guard: `tests/test_density_recuration.py`.
- **★ THE DECISION LEDGER IS DISPLAY-ONLY — the LIVE learning channels are HISTORY
  and TASTE (P-018 finding):** `add_decision` → `decision_ledger.json` has NO
  analyze-path consumer; `mem.ledger()` is called only at `cli.py:315` (display).
  So a producer for any reserved ledger event (`manual_note`/`taste_feedback`/
  `mix_decision`/`validation_check`) would be INERT (the hollow-packet trap). The
  LIVE learning channels are HISTORY (`mix_pass_history.json` → `_apply_history`)
  and TASTE (`taste_profile.json` → governance). **A confirmed-outcome producer is
  only real if it lands on one of those, NOT the ledger.**
- **The confirmed-revert OVERRIDE CAN change real `analyze(--memory-dir)`
  `next_pass` (P-018 — the FIRST confirmed-outcome signal):** an opt-in
  `record_pass(reverted=True)` (via `memory-record --reverted`) makes
  `_apply_history` demote the reverted move + surface one confirmed "Revert last
  pass" item at priority 95 **regardless of the score-inferred `got_worse`**
  (early-return anti-double-up; distinct evidence line containing "confirm").
  Opt-in / byte-identical by default. Binding guard:
  `tests/test_confirmed_revert.py` (unit + override non-vacuity) +
  `tests/test_confirmed_revert_live.py` (no-re-run liveness — FAILS pre-P-018,
  PASSES at tip). The variant/golden path won't catch memory/next-pass changes, so
  these unit + liveness tests are the binding guard (mirrors the P-016 live-wire
  lesson: assert on real `analyze` output with NO re-run).
- **Orchestration:** this repo runs Build OS at project scope (`.claude/` +
  `build-os/`). Route every task via the build-orchestrator; ≤2 commits/packet;
  Commit-1 green in isolation; STOP at any push/merge/deploy/secret boundary for
  explicit go.
- **★ REGRESSION REQUIRES GENERATED FIXTURES — a bare worktree shows FALSE
  critical failures (P-025 env fact).** `fixtures/` content is GENERATED, not
  committed. Run `fixtures/generate_fixtures.py` (or pytest via conftest) BEFORE
  `python -m logic_mix_os.cli regression` in a fresh / detached checkout. Observed
  during P-025: the base `e79426a` (PR #16 tip) reported "22 critical" in a
  detached worktree WITHOUT generated fixtures — a worktree artifact, NOT a real
  breakage; with fixtures generated it passes **68/68** (orchestrator re-ran it
  directly). The default branch is HEALTHY. Do NOT re-litigate this as a defect.
- **★ THE PRODUCER-SPECIFIC JUDGMENT IS 100% HARDCODED IN PYTHON — the prose
  `roy_halee.json` / `phil_ramone.json` are NEVER read by the scorer (P-025
  finding).** The real judgment lives in `creative.py` / `governance.py` /
  `doctrine_engine.py` constants + inline-computed coefficients. P-025 extracted
  the actual values into a frozen `ProducerProfile` (`load_profile()` +
  `doctrine/producers/halee_ramone.json`), guarded byte-identical by a round-trip
  test — but WIRED NOTHING. Any future producer-agnostic change relies on that
  round-trip guard; extract from CODE, never from the prose files.
- **★ CONFIRMED HONESTY / SOURCING POLICY (standing product decision, governs
  P-031 / P-032):** hand-curated → high-confidence; derived → low-confidence
  (labeled); LLM → draft-only, NEVER high-confidence. The `halee_ramone` reference
  is `hand-curated-documented` → `high` / `risk_class 0`, consistent with the
  policy. The profile metadata stamp exists now (P-025) but is not enforced /
  propagated until P-031.

---
_Updated by the archivist on close. Last advanced on P-032d close (2026-07-01) — the FOURTH new producer-agnostic doctrine axis `rhythmic_surprise` (weak, section-aggregate form) lands byte-identically for halee_ramone; the engine now carries 11 component axes; 4 of the 7 Timbaland "weight up" axes landed, zero plumbing debt. Next: P-032c (low_end_motion)._
