# Receipt — P-034: analyzer capacity — non-lead vocal-band masking events (`vocal_band_masking`) + the identity-derived `_lead_masked` fix

- **Packet:** P-034 — analyzer capacity. **Packet 1 of the user-approved
  two-packet analyzer-extension plan** (P-034 capacity → P-035 the 4th fixture +
  the real-data vocal-blend differential). The masking analyzer now emits
  **non-lead vocal-band masking events** under the NEW classification
  **`vocal_band_masking`**, consumed ONLY by the vocal-role surface
  (`_vocal_role_fit` + the profile blend gate); plus the `creative.py`
  `_lead_masked` identity-derived fix. **Fixture-inert by construction;
  byte-identical everywhere.**
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer PASS (no must-fix).

## Scope

**In:**

- `masking_analyzer.py`: for each NON-LEAD vocal stem (identity `backing_vocal`
  OR a non-None `vocal_type` record field; the lead excluded on identity AND
  type), when it sits forward/heard, check vocal-presence overlap against the
  SAME forward harmonic/melodic instrument set the lead pathway uses — hoisted
  to the shared `VOCAL_MASKER_IDENTITIES` constant (one basis, never forked) —
  and emit `vocal_band_masking` events: elements `[vocal_stem, other]`, the
  lead NEVER present, severity capped at moderate (info tier for
  sub-conflict), observational philosophy-neutral wording, honest CONDITIONAL
  summary counting (`vocal_band_masking_count` present only when ≥ 1 event
  exists), `critical_count` never inflated.
- `doctrine_engine.py` `_vocal_role_fit` re-keying: the non-lead pathway (and
  through it the blend gate) keys on `vocal_band_masking` at conflict
  severity; the lead pathway (`bad_masking`) untouched. Single-basis: the old
  lead-free-`bad_masking` shape is DEAD and pinned both sides.
- `creative.py` `_lead_masked` fix: the `"vocal" in element` substring match
  replaced by an identity-derived lead-name check (set-based lead names,
  plural-safe, consistent with `doctrine_engine`'s and identity-consistent
  with the classifier) — the new classification can never falsely trigger the
  masked-lead gate; a genuine lead event still does.
- NEW 36-test `tests/test_vocal_band_masking.py`; conscious-edit-path updates
  to the P-032f synthetic tests (`test_vocal_type.py`,
  `test_vocal_blend_policy.py` — they now construct the honest
  classification); 2 stub updates (`test_creative_nudges.py`,
  `test_creative_profile_sourced.py`).

**Explicitly out (deferred by design — see "Design calls" and Residue):**

- The 4th fixture, its golden, and every conscious pin flip (P-035).
- The real-data vocal-blend differential (P-035 — the arc's payoff).
- Buried-vocal reading (forward-only emission this packet).
- Any `per_track_masking_risk` contribution from the new classification.
- The `severity != "info"` consumption filter re-examination (P-035, against
  real data).
- The `logic_action_generator.py:38` substring match (residue sweep).
- The P-032i pin's now-capacity-stale docstring line (left verbatim; the
  revisit belongs to P-035).

## Commits and base

- **Single commit (≤2 rule satisfied; HEAD IS Commit-1):**
  - `e52bc1a` — "P-034: emit non-lead vocal-band masking events + the
    identity-derived lead-masked match" — 8 files, 920+/48−
    (`masking_analyzer.py`, `doctrine_engine.py`, `creative.py`, the NEW
    662-line `tests/test_vocal_band_masking.py`, the two conscious P-032f
    edits, the two stub updates).
- **Parent:** `b53d51c` (active-packet confirmation), atop `db13d08` (P-030
  close), on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `58d21dd` (= the PR #17 merge, the
  default-branch tip) — verified.
- **Pushed to the dev branch (orchestrator-handled), NOT merged.**

## QA proof (GREEN)

- **Suite:** 705 → **741** passed (+36 = the new test file). 0 failed/skipped.
- **Regression:** **68/68, goldens untouched** — zero golden paths in the
  diff; this packet is fixture-inert by construction.
- **Commit-1 isolation:** HEAD IS Commit-1 → green in isolation (real
  worktree check: **741** + **68/68**).
- **Byte-identity (independent):** full artifact trees, BOTH producers × 3
  fixtures, base vs HEAD → `diff -r` EMPTY (12 dirs × 29 artifacts; overalls
  73.8 / 70.7 / 74.3 and 68.4 / 52.6 / 49.7); zero `vocal_band_masking`
  traces in any artifact; fixture summaries keep the exact pre-P-034 key set.
- **52 QA-authored live checks:** 17 emission, 11 consumption, 7 creative-fix
  (incl. "The Voice" and the adversarial lead-named event), 17 immovability.
- **The P-032i no-vocal-blend-delta pin:** passes with source byte-identical
  (the conscious flip belongs to P-035).
- **Conscious-edit audit:** only `_mask`→`_vband` on non-lead events; every
  assertion line verbatim — strength held.
- **Safety grep:** clean. **Observational language:** clean.
- **UI smoke:** n/a (no UI surface in this packet).

## Reviewer verdict — PASS (no must-fix)

- The emission mirror judged honest: floors/gates/rounding identical to the
  lead pathway; the hoisted `VOCAL_MASKER_IDENTITIES` string-for-string; the
  lead pathway unchanged.
- **The four design calls endorsed:** (1) vocal-vs-vocal exclusion with the
  deliberate asymmetry — backing vocals still mask the LEAD; (2)
  lead-never-a-masker; (3) severity capped at moderate with the info tier;
  (4) the conditional summary key.
- Fixture-inertness verified STRUCTURAL: every non-lead record on the current
  fixtures has `vocal_type` None and a non-`backing_vocal` identity.
- The `_vocal_role_fit` re-keying is single-basis; the old
  lead-free-`bad_masking` shape is DEAD and pinned both sides.
- The creative fix is plural-safe (set-based lead names, consistent with
  `doctrine_engine`'s) and identity-consistent with the classifier.
- Every immovable consumer filter read
  (`_emotional_hierarchy` / `_vocal_centrality` / `_static_mix` /
  planners-action-generators / `_beat_identity` / `_loop_context` / goldens).
- **TWO sabotages caught:** lead-as-subject → 5 failures; widened
  `_emotional_hierarchy` filter → both immovability pins fail.
- **Codex NOT available — single-model review.**

## Design calls recorded (each pinned as a named conscious-extension point)

- **Forward-only emission** — buried-vocal reading deferred to P-035.
- **No `per_track_masking_risk` contribution** — risk feeds track_analysis,
  consumed broadly; P-035 revisits consciously.
- **`severity != "info"` consumption filter** — P-035 re-examines against
  real data.

## ★ REVIEWER ADVISORY — BINDING ON THE P-035 FIXTURE DESIGN

> **The staged fixture as literally described ("lead + chopped vocal +
> backing stack + beat") would emit ZERO `vocal_band_masking` events** —
> vocal-vs-vocal pairs are excluded and beat identities are not in the masker
> set. **The 4th fixture MUST include at least one forward/heard masker-set
> member (synth/keys/guitar) with vocal-presence overlap ≥ 0.1 against the
> chop/stack**, or the blend differential stays dormant. This is a
> fixture-design requirement created by a sound design call — not a defect.

## Residue (carried to `build-os/memory/residue.md`)

- NEW: `logic_action_generator.py:38` substring match — gated behind
  `bad_masking`, unreachable by the new classification; joins the residue
  sweep list (same family as the fixed `creative.py:98`).
- NEW: the three P-034 deferrals above as P-035 conscious-extension points.
- The P-032f inert-blend corollary's "future analyzer-extension packet"
  entry: capacity **HALF delivered** by P-034 (the events exist,
  fixture-inert); the LIVE half belongs to P-035.
- The P-032i pin's docstring line is now capacity-stale — left verbatim;
  P-035 revisits with the conscious flip.

## Open boundaries

- **NOT merged.** The commit sits on the dev branch atop merge base `58d21dd`
  (PR #17). Merge/landing remains USER-GATED — no merge without explicit go.
- Push was orchestrator-handled (`e52bc1a` pushed to the dev branch); no
  deploy/publish/secrets touched.
- **P-035 staged, NOT active** until the orchestrator confirms on the user's
  go — it carries the binding fixture-design advisory above.
