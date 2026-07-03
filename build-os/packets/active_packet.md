# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 (both gates answered
  in one directive: the P-039+P-040 pair merged first as PR #19 → default tip
  `61582b5`; then this packet as its own packet).
- **ID / Title:** **P-041 — The Third Producer: Quincy Jones (profile-only)**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `61582b5` (= PR #19 merge commit; the dev branch was fast-forwarded to it —
  verify with `git merge-base`).
- **Baseline to protect:** suite **806** / regression **93/93**.

## The user's decision (verbatim authority)

- **Producer: Quincy Jones.** Working profile file: `quincy_jones.json`
  (→ `logic-mix-os/logic_mix_os/doctrine/producers/quincy_jones.json`).
- **Grounding standard:** *hand-curated-from-documented-technique →
  `high` confidence*. **Do not ground this as LLM-synthesized. Do not ship
  any claim as `high` confidence unless it is tied to documented technique /
  documented production philosophy. Reference-track-derived judgments are
  allowed only if labeled low/experimental.**
- **Product intent:** Quincy proves the framework is not a two-pole switch.
  Target center of gravity: **orchestration-first · ensemble-aware ·
  vocal-forward but not vocal-only · space around the groove · emotional
  lift through arrangement · sectional architecture.** He sits between and
  beyond the first two: Halee/Ramone = physical space + emotional hierarchy;
  Timbaland = groove identity + contrast + negative space; **Quincy =
  orchestration + ensemble hierarchy + arranged emotional lift.**
- **Expected scoring posture** (the user's list — author, don't copy):
  ensemble balance; arrangement clarity; orchestration density WITH
  separation; vocal prominence inside ensemble context; section-level lift;
  groove support without groove dominance; harmonic/instrumental
  conversation where measurable; space that reveals arrangement roles.
  **He should not simply copy Halee/Ramone or Timbaland weights.**

## Scope (profile-only if the system is behaving)

Expected cost — and nothing more:

1. **`quincy_jones.json`** — the complete ProducerProfile schema (metadata,
   kind_scores 7×, risk_penalty, caps, nudge/promotion tables, search_modes
   with Quincy's OWN mode names, philosophy, truth_alignment,
   taste_max_delta, taste_kind_bias, aesthetic_kill_switches,
   taste_triangle, veto_thresholds, the FULL `doctrine` block — all 14 axis
   weights + baselines + penalty_coeffs + every scorer parameter set —
   default_creative_mode, and the three REQUIRED declarations).
2. **Required declarations — NO silent inheritance for load-bearing
   aesthetic choices** (the user's list, each explicitly authored):
   - **loop philosophy** (`protect_iconic_loops` + the loop_context
     status→score polarity, authored);
   - **vocal masking/blend philosophy** (`vocal_blend_policy`
     {acceptable_blend, confidence_floor} — an explicit documented-technique
     decision either way; lead protection is invariant regardless);
   - **default creative mode / mode posture** (`default_creative_mode` +
     `search_modes`);
   - **safety / veto policy as STRICT SUPERSET OR UNCHANGED invariant**
     (veto_thresholds not weaker than the reference's; kill switches keep
     every safety-relevant line).
3. **Confidence map** — per-area {high, limited, deferred} with honest
   reasons; its own **verbatim map pin** test (the guard, like
   timbaland's).
4. **Differential test** — same stems (`vocal_chop_groove` + the 3 original
   fixtures) through `halee_ramone`, `timbaland`, `quincy_jones`, proving:
   1. Quincy differs from Halee/Ramone.
   2. Quincy differs from Timbaland.
   3. Quincy is coherent, not averaged mush (his own signature — e.g. axes
      where he is NOT strictly between the other two, and an axis-emphasis
      ordering neither profile has).
   4. Quincy keeps safety invariant (same veto/audit surface).
   5. Quincy's confidence labels honestly split documented technique
      (high) from inference (low/limited/deferred).
   6. Existing profiles do not drift (existing pinned values byte-stable;
      regression 93/93 untouched).
5. **ZERO code changes** unless a schema bug is discovered (a discovered
   bug = report first; fixing it must be flagged, minimal, and covered).

Orchestrator recon (verified before open): no test pins the producers-dir
count or the exact error-listing string (`test_producer_cli.py:371` uses
`in`-assertions), so the third profile is purely ADDITIVE to the existing
806 — no existing-test edits expected. If one proves necessary, it is a
conscious enumerated delta, reported.

## Acceptance bar (the user's, verbatim)

- third producer is **dynamically discovered**
- **no code changes** required
- **existing producer outputs remain stable**
- Quincy output is **recognizably distinct**
- Quincy **confidence map is honest**
- **safety/governance unchanged**
- **differential proof is permanent**

## Safety (invariant — the standing doctrine)

Do NOT relax: safety, governance, non-destructive guarantees, vetoes,
audit behavior, rollback behavior, source integrity, approval boundaries.
A producer profile may change taste interpretation ONLY. It may never
weaken safety.

## Non-scope (the user's, verbatim)

No fourth producer. No tuning Timbaland. No tuning Halee/Ramone. No
measurement-axis changes. No CLI changes beyond the dynamic discovery
already landed. No new analyzers. No deeper mode-forking. **No merge until
qa + reviewer dual-green** (merge itself stays a user gate).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** `quincy_jones.json` + the profile's own test file (schema
  completeness, required declarations, verbatim confidence-map pin,
  grounding metadata `provenance: "hand-curated-documented"` /
  `confidence: "high"`, safety-invariance assertions) — full suite green.
- **Commit-2:** the three-way differential proof (permanent) — full suite
  green.

---
_Set active by the orchestrator on the user's explicit go (2026-07-03).
One packet at a time: builder → qa + reviewer → archivist → receipt._
