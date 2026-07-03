# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 ("Yes — pick
  another producer, but merge P-044 first… My producer pick: Brian Eno").
  P-044 merged FIRST as PR #23 → default tip `fe8d947`, per the user's
  sequencing ("P-044 is a complete governed-risk packet. It should not
  ride with a fourth producer.").
- **ID / Title:** **P-045 — The Fourth Producer: Brian Eno (profile-only)**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `fe8d947` (= PR #23 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1000** / regression **93/93** / both
  committed sample trees byte-stable / all three existing producers'
  flows byte-stable everywhere.

## The user's decision (verbatim authority)

- **Producer: Brian Eno.** Profile file: `brian_eno.json`
  (→ `logic-mix-os/logic_mix_os/doctrine/producers/brian_eno.json`).
- **Grounding standard:** *hand-curated-from-documented-technique →
  `high` confidence.* Reference-track-derived judgments are allowed only
  if labeled low/experimental. **LLM-synthesized taste is draft-only and
  must not ship as high confidence.**
- **Product intent:** Eno proves the producer-profile system is not
  merely classic vocal/space, beat/groove, orchestration/ensemble — it
  can also model: **atmosphere · texture · restraint · generative space ·
  ambient patience · non-linear emotional development.** The aesthetic
  map: Halee/Ramone = emotional hierarchy + physical space; Timbaland =
  groove identity + negative space + contrast; Quincy = orchestration +
  ensemble lift; **Eno = atmosphere + texture + restraint + generative
  space.** "He widens the aesthetic map instead of just adding another
  point near the existing cluster."
- **Expected profile posture (the user's list):** atmosphere over
  foreground urgency; texture as composition; negative space; restraint;
  slow emotional evolution; sonic environment; **ensemble as field rather
  than hierarchy**; acceptance of ambiguity; depth/space without
  necessarily using Halee/Ramone-style intimacy; **experimental mode as
  exploration rather than aggression.** "He should not simply be 'more
  reverb' or 'more ambient.'"
- **Likely weighting posture (the user's, guidance not prescription):**
  HIGHER: negative_space · atmosphere/depth · textural coherence ·
  sectional patience · contrast through absence · experimental openness.
  LOWER: vocal-centrality dominance · beat_identity dominance ·
  low-end-forward motion · aggressive excitement · loop_deconstruct
  reflex. **"Only use axes that already exist unless the packet
  explicitly proves a schema gap. This should be profile-only if the
  system is behaving correctly."** (Concepts with no existing axis —
  e.g. textural coherence as its own measurement — are honestly DEFERRED
  in the confidence map, not faked.)

## Required declarations (the user's — NO silent inheritance)

`brian_eno.json` must explicitly declare ALL required producer
philosophy fields:

1. **loop philosophy** (`protect_iconic_loops` + the authored
   loop_context status→score polarity);
2. **vocal masking / blend philosophy** (`vocal_blend_policy`
   {acceptable_blend, confidence_floor});
3. **default creative mode** (`default_creative_mode` + his OWN-named
   `search_modes`);
4. **mode reach** — every mode authors `allowed_risk`/`bias`/
   `favor_kinds`/`suppress_kinds` explicitly (the P-042 surface);
5. **extended-kind reach** — every mode authors `reach_kinds`
   explicitly (the P-043/P-044 surface: arrangement_lift,
   ensemble_rebalance, negative_space_dropout — whether and where Eno
   reaches each is an AUTHORED taste decision with documented
   grounding; "contrast through absence" is his center, but reach is
   opt-in, never inherited);
6. **safety / veto policy** — strict superset or unchanged invariant.
   Plus the honesty stamp (`provenance: "hand-curated-documented"`,
   `confidence: "high"`, risk_class 0) and the verbatim-pinned
   `confidence_map`.

## Safety (invariant — the standing doctrine)

Do NOT relax: safety, governance, non-destructive guarantees, vetoes,
source integrity, audit, approval boundaries, **dropout protections**
(the engine-owned filter is profile-blind — Eno cannot and must not
author around it; the safety line stands: dropout is an arrangement
proposal, not a destructive operation). A producer profile may change
taste interpretation only. It may never weaken safety.

## Differential proof (the user's eight, verbatim)

Run same stems through halee_ramone, timbaland, quincy_jones,
brian_eno. Prove:

1. Brian Eno differs from Halee/Ramone.
2. Brian Eno differs from Timbaland.
3. Brian Eno differs from Quincy.
4. Eno is coherent, not averaged mush (his own poles — e.g. axes where
   he is NOT strictly inside the existing three's envelope, and an
   axis-emphasis ordering none of them has).
5. Eno's confidence map honestly labels documented technique vs
   inference.
6. Existing profiles do not drift (byte-stable JSONs; existing pinned
   values unchanged; both sample trees untouched).
7. Safety/governance remains invariant (same veto/audit surface).
8. **Dropout behavior remains governed and does not become
   destructive** (if Eno authors dropout reach: the protection filter
   still binds, the caps bind against HIS authored rows, plan-only
   prose unchanged; if he doesn't: prove zero dropout emission on all
   his modes).

## Acceptance bar (the user's, verbatim)

- fourth producer is dynamically discovered
- no code changes required unless a schema bug is found
- existing producers remain stable
- Eno output is recognizably distinct
- **Eno is texture/atmosphere/restraint-driven, not just reverb-heavy**
- confidence labels are honest
- safety/governance unchanged
- differential proof is permanent

## Non-scope (the user's, verbatim)

No fifth producer. No tuning Halee/Ramone. No tuning Timbaland. No
tuning Quincy. No new analyzers. No new move families. **No widening of
dropout protections.** No CLI behavior changes. No safety/governance
changes. No merge until qa + reviewer dual-green (the merge stays a
user gate).

## Orchestrator recon (binding on the builder)

- The P-041 pattern extended: several existing tests parametrize over
  ALL shipped profiles (explicit-authoring guards, nudge-cap
  invariants, reconstruction rules) — the suite will grow PASSIVELY
  when brian_eno.json lands; enumerate the passive growth exactly (the
  P-043 arithmetic discipline). The CLI unknown-producer listing is
  `in`-asserted (additive-safe since P-041).
- Eno's JSON must carry the COMPLETE current schema: metadata,
  kind_scores for ALL 10 kinds (incl. honest rows for the three
  extended kinds — rows everywhere, no silent inheritance),
  risk_penalty, caps, nudge/promotion tables, search_modes with every
  per-mode field authored, philosophy, truth_alignment for all 10 kinds
  × 3 leans, taste_max_delta, taste_kind_bias, aesthetic_kill_switches
  (safety-relevant lines kept), taste_triangle, veto_thresholds (not
  weaker), the full doctrine block (14 axis weights + baselines +
  penalty_coeffs + all scorer params), default_creative_mode,
  protect_iconic_loops, vocal_blend_policy, confidence_map.
- Documented-technique bases available to the builder (each real,
  citable): Oblique Strategies and the studio-as-instrument practice;
  the Ambient 1: Music for Airports liner-notes manifesto ("as
  ignorable as it is interesting"); generative music writings and
  talks; the documented production collaborations (Bowie's Berlin
  trilogy, U2 with Lanois, Talking Heads) and his published
  interviews/diary (A Year with Swollen Appendices). Inference beyond
  documented technique → labeled low/limited/deferred, never high.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** `brian_eno.json` + the profile's own guard tests
  (schema completeness, all required declarations, verbatim
  confidence-map pin, honesty stamp, safety-invariance assertions,
  mode/reach authoring) — full suite green in isolation, zero effect on
  existing producers.
- **Commit-2:** the permanent FOUR-WAY differential proof (all 8 user
  requirements, incl. the dropout-governance requirement) — full suite
  green.

---
_Set active by the orchestrator on the user's explicit go (2026-07-03),
after the P-044 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
