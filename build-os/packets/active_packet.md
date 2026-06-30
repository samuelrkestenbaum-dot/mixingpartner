# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-007
- **Title:** Taste profile feeds governance (first closure of the learning loop)
- **Authority:** build

## Why (trajectory)

The product claims to learn the operator's taste, but `memory._derive_taste`'s
profile is never consumed — memory is write-only. P-007 makes the recorded taste
profile **bias variant governance**, opt-in and bounded, so two operators with
different taste get different governed winners from the same song.

## ⚠️ HARD BACKWARD-COMPAT GATE

When NO `taste_profile` is supplied, governance MUST be **byte-identical to today**
— all **112 tests + 68 doctrine-regression invariants stay green, unchanged**. The
adjustment applies ONLY when a profile is explicitly passed. (P-002 "optional,
only-when-supplied" pattern.) The `taste_adjustments` key is **absent** (not `[]`)
when nothing is applied.

## Goal / "done" criteria (single, testable)

- Calling `run_governance`/`govern_branches`/`govern_variant` with no `taste_profile`
  → output byte-identical to today. Calling with a constructed profile → a
  matching-kind variant's `taste_triangle["identity"]` / governed winner shifts in
  the mapped direction by at most `TASTE_MAX_DELTA`, each shift carries an
  `"adjusted for operator taste: …"` evidence line, and **no** taste profile can
  clear a truth-lock veto or a kill-switch / risk-class-5 refusal.

## Injection point (verified)

- `govern_variant` (`governance.py:152`): add `taste_profile: Optional[List[str]] = None`.
  After `triangle = taste_triangle(...)` (`:154`), when `taste_profile` is truthy,
  apply one **bounded** adjustment to `triangle["identity"]`, re-clamp `[0,100]`,
  recompute the verdict, append the evidence line. `None`/empty → body byte-identical.
- Thread the optional arg (default `None`) through `govern_branches` (`:171`, passes
  to `:178`) and `run_governance` (`:288`, passes to `:291`).
- **NO pipeline re-plumbing:** `pipeline.py:206` keeps calling `run_governance(result, result.creative)` → default `None` → identical. `analyze()` signature untouched (so `conftest.analyzed` + `regression.run_regression_suite`, which call `analyze()` with no profile, are unaffected).

## Adjustment (bounded, deterministic, evidence-tagged)

- New module-level pure helper `_TASTE_KIND_BIAS` mapping a profile statement →
  (variant kind, signed identity delta), derived from the exact statements
  `_TASTE_MAP` emits (`memory.py:25-34`):
  - `"tends to prefer narrower stereo images"` → down-weight `width_bloom` (and `drum_room_bloom`) identity.
  - `"prefers wider images"` → up-weight `width_bloom` identity.
  - Other statements map to no governance kind in this pass (out of scope — creative/EQ surfaces).
- **Hard bound:** total taste adjustment to `identity` clamped to `±TASTE_MAX_DELTA = 15` (strictly `< 30`, the existing intimate truth nudge), re-clamped `[0,100]`.
- **Deterministic:** pure fn of `(variant["kind"], statements)`; statements applied in fixed order; no time/I/O/random.
- **Evidence:** applied adjustments append to a new `taste_adjustments` field, e.g. `"adjusted for operator taste: down-weighted width_bloom (prefers narrower images), identity 70->55"`. Field ABSENT when nothing applied.

## Inviolability (taste can nudge, never override)

- Truth-lock (`governance.py:63-76`) + the `align < 50` veto (`:159`) + the truth `-30` nudge fire first; taste only moves `identity`, bounded `<30`.
- Kill-switch / `validate_action_safety` (`:251-260`) / risk-class-5 are a separate path `govern_variant` never calls — taste cannot reach them. Assert via test.

## In scope (exactly two)

- `logic_mix_os/governance.py` — optional arg on the 3 functions + the `_TASTE_KIND_BIAS` helper + bounded adjustment + `taste_adjustments` evidence field.
- `tests/test_governance_taste.py` (new).

## Out of scope (explicit)

- Pipeline re-plumbing / `analyze()` signature; any `cowork`/`cli`/`memory_dir`→governance live opt-in surface (**deferred as P-007b**); P-008 history-aware next pass; new event-logging; creative `_KIND_SCORES`; `_TRUTH_ALIGNMENT` table edits.

## Test plan (no DAW/network — constructed profiles + existing fixtures)

- **(a) default unchanged:** `govern_variant(v, c, lean)` == `govern_variant(v, c, lean, taste_profile=None)` (equal dicts, no `taste_adjustments` key); plus an `analyzed`-fixture assertion that `governance["governed_branches"]` is unchanged.
- **(b) profile shifts winner + evidence:** construct a `width_bloom` branch (reuse `dense_chorus_with_loops` variants à la `test_governance.py:40-51`); `govern_branches(..., "neutral", taste_profile=["tends to prefer narrower stereo images"])` → `width_bloom` identity lower than no-profile by `≤ TASTE_MAX_DELTA`, evidence line present, governed winner changes where it crosses keep/reject.
- **(c) taste cannot override doctrine:** intimate lean + `["prefers wider images"]` still does NOT make width_bloom the winner; `validate_action_safety({"risk_class":5,...})["blocked"]` unchanged regardless of taste input.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `68e88d0` (clean). Default `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** new `tests/test_governance_taste.py` + the minimal `governance.py` change in one commit; passes its own tests standalone; full suite 112→~115; regression 68/68.
2. **Commit 2 (optional):** only on reviewer refinement.

## Regression-safety argument

1. Doctrine regression NEVER reads `result.governance` (`regression.py:49-83`, `:151-230`) → a governance change cannot move the 68 invariants.
2. Default path byte-identical (arg defaults `None`; pipeline/`analyze` unchanged; adjustment gated behind `if taste_profile:`; `taste_adjustments` omitted when absent).
3. Bound (`±15 < 30`) + untouched kill-switch path → taste cannot override doctrine even on the opt-in path (test c).

## Guardrails

- Build authority; deterministic; no network/subprocess/AppleScript/`.logicx`/`RealLogicSessionAdapter`; truth-lock + kill-switches inviolable.

---
_Confirmed P-007 on the user's "skate to where the puck is going" — trajectory
work (closing the learning loop), not hardening. Builder implements exactly this;
archivist clears on close._
