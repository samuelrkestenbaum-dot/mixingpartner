# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-04 (AskUserQuestion:
  "Merge P-049, then open CLA" + pole "Impact / excitement pole"). P-049
  merged FIRST as PR #28 → default tip `2b0ad1a`, per the user's
  sequencing (a producer is its own proof object).
- **ID / Title:** **P-050 — The Fifth Producer: Chris Lord-Alge
  (profile-only)**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `2b0ad1a` (= PR #28 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1145** / regression **93/93** / the
  FOUR existing producers' flows byte-stable / the four committed sample
  trees + nine mode demos byte-stable / ZERO .py under `logic_mix_os/`
  (profile-only unless a schema bug is discovered → STOP and report).

## The user's decision (verbatim authority)

- **Producer: Chris Lord-Alge.** Profile file: `chris_lord_alge.json`
  (→ `logic-mix-os/logic_mix_os/doctrine/producers/chris_lord_alge.json`;
  confirm the exact stem the loader/CLI will discover — the file stem IS
  the `--producer` name).
- **Pole: the IMPACT / EXCITEMENT pole.** Weight listener-excitement,
  vocal presence, punch (beat_identity), section-contrast UP; restraint /
  negative-space / depth DOWN — the energy-forward **anti-Eno**, with a
  **distinct argmax** from all four existing producers. Recommendation
  language leans commit-and-slam. He *fills* space where Timbaland carves
  it, chases *impact* where Quincy arranges, and is modern/loud/forward
  where Halee/Ramone is vintage/intimate.
- **Grounding standard (standing):** hand-curated-from-documented-technique
  → `high`. Reference-track-derived judgments only if labeled
  low/experimental. **LLM-synthesized taste is draft-only and must NOT
  ship as `high`.**

## ★★ THE CENTRAL STRESS-TEST (why CLA matters — do not soften)

CLA's whole identity — aggressive loudness, heavy compression, density —
is **the exact thing the safety layer restrains.** The doctrine
(pinned): *the engine detects; the profile decides taste; safety /
governance is INVARIANT.* CLA is the hardest test that doctrine has
faced. His profile expresses loudness-forward identity ONLY through
weighting (excitement / vocal-presence / punch / density UP; restraint /
space DOWN) and recommendation LANGUAGE — and MUST keep, verbatim and
unweakened:

- the safety kill-switch **"Never chase reference loudness at the mix
  stage."** (present verbatim in the reference + timbaland — it is a
  SAFETY line, not taste; CLA keeps it exactly, and it is the packet's
  signature proof: a loudness-maximalist who still cannot weaken the
  loudness rail);
- every other safety-relevant kill-switch line;
- non-destructive guarantees, the dropout protection filter
  (engine-owned, profile-blind), vetoes, audit, rollback, source
  integrity, approval boundaries;
- `veto_thresholds` not weaker than the reference; risk_penalty / caps
  equal-or-stricter.

A producer profile may change taste interpretation ONLY. It may never
weaken safety. **If authoring the impact pole ever seems to require
relaxing the loudness kill-switch or any safety surface — that is the
STOP line: the doctrine holds, the profile bends around it.**

## Required declarations (NO silent inheritance — the six)

`chris_lord_alge.json` must explicitly declare ALL required producer
philosophy fields:

1. **loop philosophy** (`protect_iconic_loops` + the authored
   loop_context status→score polarity);
2. **vocal masking / blend philosophy** (`vocal_blend_policy`
   {acceptable_blend, confidence_floor});
3. **default creative mode** (`default_creative_mode` + his OWN-named
   `search_modes` — names from documented CLA vocabulary, reading as CLA,
   not renamed copies);
4. **mode reach** — every mode authors `allowed_risk` / `bias` /
   `favor_kinds` / `suppress_kinds` explicitly (the P-042 surface);
5. **extended-kind reach** — every mode authors `reach_kinds` explicitly
   (arrangement_lift / ensemble_rebalance / negative_space_dropout).
   AUTHORED taste decision with documented grounding: negative-space
   dropout is likely NOT his grammar (he fills space, not carves it) —
   author `[]` with the reasoning, or justify hard from documented
   technique; if he reaches ANY family, the cap binds against HIS honest
   rows and the differential proves the protection filter still holds on
   his reaching modes;
6. **safety / veto policy** — strict superset or unchanged invariant (the
   stress-test above).
   Plus the honesty stamp (`provenance: "hand-curated-documented"`,
   `confidence: "high"`, risk_class 0) and the verbatim-pinned
   `confidence_map`.

## The five-way differential (permanent proof)

Same stems through halee_ramone, timbaland, quincy_jones, brian_eno,
chris_lord_alge on all 4 fixtures. Prove:

1–4. CLA differs from EACH of the four (pairwise-distinct overalls on
   every fixture).
5. Coherent, not averaged mush: axes where CLA is OUTSIDE the four's
   envelope (≥2); his argmax distinct from all four argmaxes (halee
   {emotional_hierarchy, vocal_centrality} 1.2, timbaland beat_identity
   1.3, quincy depth_hierarchy 1.4, eno negative_space 1.4); the
   reconstructive test (his overall rebuilds from the reference's
   components + only his authored deltas — the P-041/P-045 pattern).
6. Confidence honesty: every `high` entry names a documented-technique
   basis; nothing reference-derived above low/limited; his own honest
   deferrals for concepts with no axis (never faked).
7. Existing four profiles do not drift (all four JSONs byte-unchanged
   /sha256-pinned; existing pinned overalls re-asserted; the four sample
   trees + nine demos untouched).
8. Safety invariant five-way (veto/audit/kill-switch surface identical
   except authored-taste keys) AND — the CLA-specific clause — **the
   loudness kill-switch present verbatim in his JSON; dropout stays
   governed** (if he reaches it: filter + cap hold on his reaching modes;
   if not: zero dropout emission across his modes).

## Orchestrator recon (BINDING on the builder)

- **THE P-047 CONSEQUENCE (do not miss this):** the structural producer
  sweeps are now DIRECTORY-DRIVEN (P-047). The moment
  `chris_lord_alge.json` lands, `tests/test_mode_forking.py`,
  `tests/test_move_vocabulary_expansion.py`, and
  `tests/test_negative_space_dropout.py` parametrize over CLA and will
  **KeyError on his missing per-producer data rows** (AUTHORED_TRANSLATION,
  AUTHORED_OVERALLS, AUTHORED_DROPOUT, the conservative/experimental
  expected sets, the affinity-ordering chain). CLA's rows — CAPTURED FROM
  THE REAL ENGINE first, then pinned — MUST land in the SAME Commit-1 as
  the JSON so the auto-swept guards stay green in isolation. This is the
  "conscious data-table rows at enumerable sites" the P-047 packet
  promised a fifth producer would cost. Enumerate every site.
- The JSON carries the COMPLETE current schema (study `brian_eno.json` +
  `timbaland.json` — the two most recent complete profiles; every
  top-level field, per-mode fields, kind_scores for all 10 kinds,
  truth_alignment 10×3, the full doctrine block: 14 axis weights +
  baselines + penalty_coeffs + all scorer params).
- `chris_lord_alge.json` is a producers-dir profile, NOT an `examples/`
  resident — the P-049 directory-set guards are UNAFFECTED (they guard
  `examples/`, which stays 4 trees + 9 demos + the manifest). No CLA
  sample tree / mode demo in THIS packet (profile-only; a CLA
  product-surface refresh is a possible LATER packet, the P-046/P-048
  pattern).
- Documented-technique bases (each real, citable): the Waves **CLA
  signature** plugin line (the chains literally encode his technique);
  the Mix With The Masters / PLAP masterclasses; his published Sound on
  Sound / EQ / Mix interviews; the discography (Green Day, U2,
  Springsteen, Muse, My Chemical Romance, etc.) — "commit early, print
  effects, mix into the compressor," parallel-crushed drums, bus
  compression, vocal-always-on-top-and-loud, saturation-for-energy, and
  **translation** (his mixes land on every system — a documented,
  genuinely load-bearing CLA value worth an axis-honest expression).
  Inference beyond documented technique → low/limited/deferred, never
  high.

## Non-scope (binding)

No sixth producer. No tuning halee/timbaland/quincy/eno. No new analyzers.
No new move families. No dropout-protection widening. No CLI-semantics
changes. No safety/governance changes (the loudness kill-switch and every
safety surface are INVARIANT). No CLA sample tree / mode demo (profile-
only). No merge until qa + reviewer dual-green (the merge stays a user
gate).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** `chris_lord_alge.json` + `tests/test_cla_profile.py`
  (schema completeness, all six declarations, verbatim confidence-map
  pin, honesty stamp, safety-invariance incl. the loudness kill-switch
  verbatim, mode/reach authoring) + the P-047 data-table rows for CLA
  (captured then pinned) — full suite green in isolation (the auto-swept
  guards included).
- **Commit-2:** the permanent FIVE-WAY differential (extend
  `test_four_way_differential.py` to five-way, or a new sibling — the
  builder decides, enumerated) proving all 8 requirements incl. the
  loudness-invariant clause — full suite green.

---
_Set active by the orchestrator on the user's explicit go (2026-07-04),
after the P-049 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
