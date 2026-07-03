# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 ("My call: Merge
  P-042 now. Then open Shape C, but narrowly: arrangement_lift +
  ensemble_rebalance only."). P-042 merged FIRST as PR #21 → default tip
  `17cc270`, per the user's sequencing.
- **ID / Title:** **P-043 — Curated Move Vocabulary Expansion: Arrangement
  Lift + Ensemble Rebalance** (the user's title, verbatim)
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `17cc270` (= PR #21 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **907** / regression **93/93** / both
  committed sample trees under the staleness pin / the P-042 default-flow
  candidate-id pins.

## The user's decision (verbatim authority)

**Open Shape C, but NARROWLY: `arrangement_lift` + `ensemble_rebalance`
only.** "Do not start with every tempting move family. Start with the two
that prove the new capability most cleanly."

| Family | The user's why |
|---|---|
| `arrangement_lift` | Gives Quincy a real authored reach beyond current approximation |
| `ensemble_rebalance` | Tests ensemble-aware producer judgment without adding unsafe/destructive behavior |

**Explicitly EXCLUDED: negative-space dropout.** "Higher risk because it
adds more aggressive subtractive/mute-like creative behavior, and it
smells more Timbaland-specific. It should come after C proves the widened
vocabulary can stay governed."

**Product intent:** "B proved the fork seam; C should now widen the
vocabulary just enough to make Quincy's mode behavior genuinely musical."
(Context: P-042's receipt names quincy-experimental's subtractive_drop +
width_bloom as the in-vocabulary APPROXIMATION of arrangement-lift /
ensemble-rebalance — these two families are the real thing.)

## Acceptance bar (the user's, verbatim)

- new move families exist
- curated risk rows exist
- profiles author reach over them
- Quincy can reach them
- Timbaland/Halee only reach them if authored
- safety caps still bind
- no producer-specific engine branches
- sample-tree drift is conscious
- differential proof attributes changes to widened vocabulary + profile
  reach

## Orchestrator implementation notes (recon, binding on the builder)

- **Reach-gating is the load-bearing design point.** "Timbaland/Halee only
  reach them if authored" + "sample-tree drift is conscious" together mean
  the two new kinds must NOT join the neutral emission pool: an extended-
  vocabulary kind emits ONLY when the active mode's authored declarations
  reach for it. P-042's `favor_kinds` is order-only ("can never grow the
  set") — so the builder designs the minimal semantic extension (e.g. a
  distinct `reach_kinds` declaration, or documented extended-kind
  semantics) WITHOUT weakening B's guarantees for the original seven
  kinds. The doctrine holds: the ENGINE curates the families (which
  problems they address, their changes/validation text, their
  translation/mono risk rows in the curated tables); the PROFILE authors
  whether a mode reaches them; the GOVERNANCE cap binds (over-cap reach
  refused loudly at load + fail-closed at runtime, exactly B's two-layer
  pattern).
- **Engine content:** `CREATIVE_VARIANT_KINDS` grows by exactly these two;
  new curated `_variant` entries in the per-problem pools for the two
  families (plan-only, non-destructive, real Logic-Pro-actionable moves in
  the house style); honest curated risk rows. All three SHIPPED profiles
  author `kind_scores` rows for both new kinds explicitly (curated risk
  rows exist everywhere — no silent inheritance), even where mode reach is
  absent.
- **Authored reach in this packet:** Quincy authors real reach (his
  experimental at minimum — it currently carries the approximation; other
  modes as his philosophy dictates). Halee/Timbaland author ZERO reach —
  their "only if authored" gate is proven via a test-local synthetic
  profile, not by touching their taste.
- **Namespace care:** Quincy's MODE named `arrangement_lift` and the new
  KIND named `arrangement_lift` are distinct namespaces — keep validation
  and prose unambiguous.
- **Drift discipline:** halee/timbaland neutral + default flows stay
  byte-identical (staleness pin untouched, no regeneration). If Quincy's
  DEFAULT mode authors reach, his default flow changes — that is a
  CONSCIOUS enumerated delta (the P-042 default-flow id pin updates with
  justification from his philosophy); if the builder keeps his default
  neutral, zero default drift anywhere. Either way: enumerated, captured,
  explained. Doctrine scores do not move (creative layer only).
- **Differential proof shape:** same mode name + same stems: quincy (with
  authored reach) emits the new kinds, halee/timbaland do NOT; the
  synthetic profile proves reach is data-not-producer; suppression works
  against the new kinds; the cap binds against the new kinds' curated
  risks; attribution reconstructs from the JSONs on disk (the B pattern).

## Non-scope (binding)

No negative-space dropout family. No other new families beyond the two.
No new analyzers. No doctrine/scoring changes (doctrine_engine untouched).
No safety/governance/veto changes; never weaken the caps or B's
guarantees for the original seven kinds. No per-producer code branches;
no hardcoded producer behavior in the engine. No merge until qa +
reviewer dual-green (the merge stays a user gate).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the engine widening (vocabulary + curated variant
  builders + reach semantics + validation) + all three profiles' explicit
  kind_scores rows + guards — with ZERO behavioral change (no shipped
  profile reaches yet), full suite green in isolation.
- **Commit-2:** Quincy's authored reach + the differential proof + any
  conscious enumerated pin deltas.

## After this packet

Negative-space dropout stays EXCLUDED until C proves the widened
vocabulary stays governed — its own user-gated decision later.

---
_Set active by the orchestrator on the user's explicit go (2026-07-03),
after the P-042 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
