# Receipt — P-031: confidence framework (per-area honesty labeling)

- **Packet:** P-031 — confidence framework: per-interpretation-AREA honesty
  labeling (`confidence_map`: `area` / `level` ∈ {high, limited, deferred} /
  `reason`), a REQUIRED profile field, machine-readable in the profile AND
  rendered on the report surface.
- **Date closed:** 2026-07-02
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`; packet base = parent
  `4d4b57d` (active-packet confirmation), atop `4c6285b` (P-032f close).
  Merge base for landing decisions unchanged: `e79426a` (PR #16 — nothing since
  P-025 has been merged).
- **Verdict:** qa **GREEN**; reviewer **PASS** (one must-fix round —
  fix-then-pass, fully resolved). **Codex NOT available — single-model review,
  both rounds.**

## Scope

**In:**

- A REQUIRED top-level `confidence_map` profile field: a list of
  interpretation-AREA entries, each `area` (string) / `level` (exactly one of
  `high` / `limited` / `deferred`) / `reason` (non-empty string), structurally
  validated in `producer_profile.py::_validate` (missing field, unknown levels,
  empty reasons, non-string areas all rejected — no silent defaults). The
  P-025 profile-level `metadata` stamp (provenance/confidence/risk_class)
  STAYS; the map complements it (global provenance + per-area trust).
- halee_ramone's OWN authored honest map (8 entries), machine-checked against
  its weights and verbatim-pinned.
- Rendering: `score_doctrine` returns additive per-call `confidence` copies;
  the verdict markdown gains a "## Confidence" section grouped by the
  `CONFIDENCE_LEVELS` single source of truth; `doctrine_score.schema.json`
  gains the `confidence` property. Per-call profile threading (P-029) — a
  passed profile's map renders, not the module default's.

**Explicitly out:**

- ANY judgment change — no score, variant, promotion, or recommendation
  changes (labeling, never judgment; byte-identical discipline).
- Authoring `timbaland.json` (P-032h) and the differential proof (P-032i).
- Tightening validation against duplicate areas / extra entry keys (reviewer
  judgment note — deferred, see Residue).

**Scope provenance:** USER-UPGRADED at P-032f close — not a single
profile-level stamp but a per-area map, so the second producer ships
"different / profile-authored / confidence-stamped / honesty-labeled /
safety-invariant." The docstring honesty of seven packets (P-032e/a/b/d/c/g/f)
became first-class, validated, rendered, and impossible to silently delete.

## Commits (2 + 1 review-fix; ≤2-commit contract met on the build commits, the
third is the reviewer's fix-then-pass path used as designed)

| Commit | Summary |
| --- | --- |
| `51a107c` | Commit-1 — `confidence_map` schema + structural validation in `producer_profile.py` + halee_ramone's authored map + 19 tests (`producer_profile.py` +51, `halee_ramone.json` +40, `tests/test_confidence_map.py` +327). **GREEN IN ISOLATION: 591 passed + 68/68** — verified in REAL WORKTREES by builder, qa, AND reviewer independently. |
| `4af24e2` | Commit-2 — `score_doctrine` returns additive per-call `confidence` copies; verdict markdown "## Confidence" section grouped by the `CONFIDENCE_LEVELS` single source of truth; `doctrine_score` schema property; +9 tests (`doctrine_engine.py` +7, `markdown_renderer.py` +24, schema +15, tests +181). |
| `b869ebd` | Review-fix (fix-then-pass) — split "per-section true-sub movement" into its OWN deferred entry with the ACCURATE band-resolution reason (sections expose low_mid 120–500 Hz only; true-sub 20–120 Hz not measurable at section grain), removed from the onset-timing composite; verbatim pin mirrored; counts identical (2 files: `halee_ramone.json` + `tests/test_confidence_map.py`, 25 insertions / 10 deletions). |

Push state at close: `51a107c` + `4af24e2` pushed to the dev branch;
`b869ebd` local at archivist close (the orchestrator pushes at close). NOT
merged.

## The authored halee_ramone map (8 entries: 2 high / 1 limited / 5 deferred)

- **high** — the live interpretation axes (weights machine-checked > 0); AND
  the seven agnostic axes as measurement (weights machine-checked == 0,
  "deliberately weight-0" stated as the reason).
- **limited** — vocal blend (the inert-blend corollary from P-032f, accurate:
  the analyzer does not yet emit non-lead vocal masking events on real data).
- **deferred** — cultural loop recognizability; true hook recurrence; motif
  provenance; onset-timing strong forms (typing, fills, interlock);
  per-section true-sub movement (band resolution — the review-fix entry).

## QA proof (exact counts)

- **Suite:** 572 → **600 passed** (+28 = 19 Commit-1 + 9 Commit-2), 0 failed /
  skipped. **Regression:** 68/68 (0 critical / 0 warnings) — UNCHANGED.
- **Commit-1 isolation:** `51a107c` green in a REAL worktree = **591 passed +
  68/68** (verified independently by builder, qa, AND reviewer).
- **Byte-identity (independent, like-for-like inputs):** 14 doctrine
  components + overalls 73.8 / 70.7 / 74.3 unchanged; creative EMPTY diff;
  whole artifact-tree diff = EXACTLY {`doctrine_score.json` + `confidence`
  key; verdict md + section with 0 lines removed} × 3 fixtures.
- **Honesty pins load-bearing:** delete-entry sabotage → 7 failures.
- **Rendering liveness:** qa's OWN synthetic profile — its entries render,
  zero reference leaks; both sabotages reproduce (default-sourcing → exactly
  1 fail; hardcoded renderer → exactly 3).
- **Validation:** 8/8 spot-checked malformed shapes → ValueError.
- **Safety grep:** NONE. **Observational language:** zero hits across all
  reasons.
- **Cowork ride-along:** the addition is additive AND contract-aligned
  ("recommendations carry ... a confidence" — `COWORK_CONTRACT.md`); no
  key-set pin broken.
- **UI smoke:** N/A (no UI surface; the verdict markdown addition is covered
  by the rendering-liveness + artifact-tree proofs above).

## Reviewer verdict

**PASS after one must-fix round (fix-then-pass, fully resolved).**

- Labeling-never-judgment PROVEN — only additive output deltas.
- The map was fact-checked against the code; the ONE inexactness found
  (per-section true-sub misattributed to onset timing vs the real
  band-resolution boundary) was **exactly the kind of catch the packet exists
  for** — fixed via the pin's conscious-edit path (`b869ebd`), re-verified:
  8 entries, pins STRONGER (five deferred entries verbatim-pinned vs four),
  standing-strings sweep intact, nothing loosened.
- Per-call threading sabotage-proven; 11 extra adversarial validation shapes
  all rejected; golden blindness read STRUCTURALLY (`SCORE_KEYS` +
  categorical — no map vocabulary can reach the golden).
- **Trajectory check:** `timbaland.json` can express the user's example
  labeling with ZERO schema change — the liveness test literally exercises
  the second-profile path.
- **Judgment notes (non-blocking, carried to residue):** duplicate areas +
  extra entry keys are accepted by validation (verbatim pins catch this for
  authored profiles); P-032h should pin timbaland's map too; consider
  tightening in a future validation packet.
- **Codex second-eyes:** NOT available — single-model review, both rounds.

## ★ Milestone

**THE HONESTY LAYER IS IN PLACE.** Every future profile MUST carry a validated
`confidence_map` (required field, no silent defaults); the reference profile's
own map is authored, machine-checked against its weights, and pinned; the
report surface renders per-call. The second producer can now ship
honesty-labeled by construction.

## Residue / follow-ups

1. **NEW (reviewer judgment notes):** `confidence_map` validation accepts
   duplicate areas + extra entry keys — P-032h should verbatim-pin
   timbaland's map like halee_ramone's; consider tightening in a future
   validation packet.
2. **Process precedent:** the fix-then-pass conscious-edit path through a
   verbatim pin works as designed (`b869ebd`) — the standard route for
   pin-guarded content changes.
3. **Standing carry-forwards retained:** liveness-docstring sweep now
   potentially SEVEN files (check `tests/test_confidence_map.py` too); shared
   groove dict; NaN-floor guard; `lead_names` derivation; `loop_deconstruct`
   literal kind; `creative.py:98` vocal-name match; the inert-blend corollary
   binding P-032i expectations.

## Open boundaries

- `51a107c` + `4af24e2` pushed to the dev branch; `b869ebd` local at this
  close (the orchestrator owns the close push). **NOT merged** — the whole
  producer-agnostic epic (P-025 → P-031) remains un-landed on default; merge
  base `e79426a` (PR #16). Any PR / merge into the protected default needs the
  user's explicit go. No merge / deploy / secret action taken in this close.

## Next

**P-032h — author `timbaland.json` (THE PAYOFF PACKET):** declare
`protect_iconic_loops` + `vocal_blend_policy` + its OWN `confidence_map`
(high groove/space/low-end/loop; limited vocal-blend per the inert corollary;
deferred cultural/hook/motif); mind the axis ceilings (lem 84 / vrf 85); the
`_DEFAULT_PROFILE` no-aliasing carry-forward (second live profile —
copy-before-mutate); weights = the user's approved Timbaland value system
(protect groove_identity / negative_space / low_end_motion / section_contrast;
relax vocal_centrality / lush_depth / loop_deconstruct bias — relax ≠ remove);
provenance hand-curated-documented → confidence HIGH per the honesty policy.
Then P-032i (differential proof; NO vocal-blend delta expected).
