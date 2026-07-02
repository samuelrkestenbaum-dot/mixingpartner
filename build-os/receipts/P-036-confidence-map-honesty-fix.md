# Receipt — P-036: re-author the stale vocal-blend confidence entries (the honesty layer catches up with P-035)

- **Packet:** P-036 — re-author the stale vocal-blend `confidence_map` entries:
  the honesty layer catches up with P-035's reality (the P-035 reviewer's
  queue-jump recommendation, user-approved). **Labeling only, never judgment.**
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer PASS (no must-fix).
- **★ THE HONESTY LAYER IS CURRENT with P-034/P-035.** Every confidence claim
  in both shipped profiles is now true, code-verified, and pinned against
  regression to the stale text.

## Scope

**In:**

- **Re-author the vocal-blend entry in BOTH profiles**
  (`doctrine/producers/halee_ramone.json` + `timbaland.json`): the entry's
  `reason` ONLY — `area` and `level` untouched. New reasons state the LIVE
  facts (the either-side-forward reading; the measured 65.0/85.0 differential;
  timbaland's +0.7 at its authored 0.4 weight) AND the three real constraints
  (masker-set-bounded coverage; info tier emitted but unconsumed; no per-track
  masking risk).
- **The conscious pin flips:** halee_ramone's `AUTHORED_MAP[2]`
  (tests/test_confidence_map.py) and `TIM_AUTHORED_MAP[5]`
  (tests/test_timbaland_profile.py) — the pins' designed conscious-edit path;
  docstrings updated; live phrasing pinned IN, the falsified claims pinned OUT.
- **Byte-identity everywhere else** (proven — see QA proof).

**Explicitly out:**

- Any `level` change (both stayed `limited` — the honest call, see below), any
  score/weight/gate/engine change, anything beyond the two entries + pins +
  proofs.
- The standing residue-sweep backlog (untouched; see Residue).

## Commits and base

- **Single commit (≤2 rule satisfied; HEAD IS Commit-1 → green in
  isolation):**
  - `95de041` — "P-036: re-author the vocal-blend confidence entries — the
    honesty layer catches up with P-035" — 4 files, 34+/16−: both producer
    JSONs (the vocal-blend entry's `reason` ONLY) + both pin files (conscious
    flips + docstrings).
- **Parent:** `6c0d9bf` (active-packet confirmation), atop the merged default
  `dc921ec` (= the PR #18 merge, post-epic hardening P-033/P-030/P-034/P-035),
  on the dev branch `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `dc921ec` (= PR #18, the default-branch
  tip).
- **PUSHED to the dev branch (orchestrator-handled), NOT merged.**

## ★ The re-authored entries (the level decision)

- **Both levels stayed `limited`** — the honest call per the closed
  vocabulary: `limited` = "mechanically live but constrained on today's data —
  the constraint stated in the reason"; `high` = "live, WEIGHTED, curated"
  would OVERCLAIM for the reference (whose `vocal_role_fit` weight is 0) and
  would DROP the stated constraints for timbaland.
- Every clause of both new reasons was fact-checked TRUE by both gates (qa +
  reviewer) against code and pinned data.
- The high-claims machine-checks' scope is unchanged (the entry is not
  weight-backed; no extension needed).

## QA proof (GREEN)

- **Suite:** **754** passed (count HELD — labeling-only packet). 0
  failed/skipped.
- **Regression:** **93/93, 0 warnings.**
- **Commit-1 isolation:** single commit; HEAD IS Commit-1 → green in
  isolation.
- **Artifact-delta audit:** EXACTLY **16 of 240** files differ
  (8 × `doctrine_score.json` + 8 × `mix_verdict.md`), **one line each**; every
  score/variant/promotion/recommendation surface byte-identical (4 fixtures ×
  2 producers).
- **Pins:** 1 entry per map, reason-only; **2 assertions removed / 8 added**
  (live phrasing pinned IN; the falsified claims pinned OUT — "only against
  the lead" and "dormant" now asserted ABSENT).
- **Safety grep + judgment-word guards:** clean. **UI smoke:** n/a (no UI
  surface in this packet).

## Reviewer verdict — PASS (no must-fix)

- **Every claim table-verified** — including that the **+0.7** is correctly
  the measured artifact delta, not the unrounded 0.66 (the honest number).
- **The level decision endorsed** (both stay `limited`).
- **The pinned-OUT shape proven strictly stronger by a FULL-REGRESSION
  sabotage:** JSON + pin constant reverted TOGETHER → the pinned assertions
  still fail.
- The corollary tests still bind; byte-identity spot-verified independently.
- **Codex NOT available — single-model review.**
- **Two non-blocking observations (→ residue):**
  - **(A)** "either side of the pair is forward" elides the masker-arm's
    `heard` qualifier — repo-canonical shorthand (the analyzer doc's own
    headline); a future tidy could append "…or a heard masker stands forward".
  - **(B)** the 65.0 attribution is elliptical (the chop AND the stack are
    each penalized once) but numerically exact.

## ★ A wording constraint discovered

`JUDGMENT_WORDS` substring-matches "fix", so **"fixture" is unusable in
profile text** — "real exported-stem data" used instead (accurate; the
reviewer confirmed the dodge did not bend the truth). Word-boundary matching
would free the vocabulary — routed to the residue sweeps.

## Residue (carried to `build-os/memory/residue.md`)

- The stale-confidence-map TOP item is **✓ RESOLVED** by this packet.
- **NEW cosmetic:** reviewer observations (A) the `heard`-qualifier shorthand
  (pair with the analyzer doc line if ever tidied) and (B) the elliptical 65.0
  attribution.
- **NEW residue-sweep candidate:** the JUDGMENT_WORDS "fix"-substring
  constraint on profile prose (word-boundary matching would free the
  vocabulary).
- All standing carry-forwards retained — **the backlog is now PURELY the
  residue sweeps** (the three producer-named-VALUE surfaces;
  `logic_action_generator.py:38`; validation tightening incl. `search_modes`
  non-empty + `default_creative_mode` structural checks + the NaN-floor guard;
  the liveness-docstring sweep ~8 files; `cli.py` `--mode` text; the P-035
  count-pin parenthetical tidy; duplicate-areas/extra-keys; fallback-reason
  wording; the shared groove dict defensive copy; `lead_names` derivation).

## Open boundaries

- **NOT merged.** The dev branch carries **ONE small packet — P-036 +
  closes** — atop merge base `dc921ec` (PR #18). **Merge cadence is the
  user's call:** P-036 can ride with the next batch or merge alone on the
  user's word. No merge without explicit go.
- Push was orchestrator-handled (`95de041` pushed to the dev branch); no
  deploy/publish/secrets touched.
- No next packet staged — the orchestrator scopes the residue-sweep packets
  with the user.
