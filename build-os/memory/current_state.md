# Current State

> The "where are we" snapshot. The orchestrator reads this first every session.
> The archivist advances it when a packet closes. Keep it short and true.

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
  UNCHANGED)**. **P-028 COMPLETES THE EXTRACTION PHASE** — the whole judgment layer
  is now profile-driven. The P-025 + P-026 + P-027 + P-028 product commits are
  local-only (not pushed / merged). P-028's parent chain: `72e98a7` → `29b9dfe` →
  `d5260a6` (active-packet confirmation) → `23850f7` (P-027 close). P-027's parent
  chain: `7b1c26d` → `e4786ca` → `b8526a8` (active-packet confirmation) → `c4a092d`
  (P-026).
- **Build/test command:** from `logic-mix-os/` — `pip install -e ".[dev]"`
  (numpy is the only hard dependency; the `[dev]` extra adds pytest), then
  `python -m pytest` (testpaths=`tests`). Golden + doctrine regression:
  `python -m logic_mix_os.cli regression` — **NOTE: run `fixtures/generate_fixtures.py`
  (or pytest via conftest) first in a fresh checkout; `fixtures/` content is
  GENERATED, not committed, so a bare worktree shows FALSE critical failures.**
- **Green baseline (verified 2026-07-01, P-028):** suite **370 passed** (0 failed /
  skipped / warnings; green even under `-W error`); regression **68/68** (0
  critical / 0 warnings) — UNCHANGED (P-028 is byte-identical). Commit-1 green in
  isolation = 364. (Prior baseline was 351 at P-027; P-028 added +19 —
  `test_doctrine_profile_sourced.py` sourcing/value/behavior pins + no-aliasing +
  determinism, plus the `doctrine.scorers` round-trips in `test_producer_profile.py`;
  goldens & judgment untouched. Earlier: 331 → 351 at P-027; 319 → 331 at P-026;
  293 → 319 at P-025.)

## Where we are

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
_Updated by the archivist on close. Last advanced on P-025 close (2026-07-01) — the FOUNDATION step of the producer-agnostic epic (ProducerProfile extracted, round-trip-guarded, unwired)._
