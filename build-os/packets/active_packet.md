# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 ("My call: B —
  Profile-authored mode forking. That is the right next skate.").
- **ID / Title:** **P-042 — Profile-Authored Mode Forking (Shape B)**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `dadda12` (= PR #20 merge — P-041 landed first; verify with
  `git merge-base`).
- **Baseline to protect:** suite **873** / regression **93/93** / the two
  committed sample trees under the staleness pin.

## The user's decision (verbatim authority)

**Implement: Profile-authored mode forking.** Do NOT implement A (mode as
gate/ranking) as the final shape. Do NOT implement C (new mode-specific
move families) in this packet — C stays STAGED for a later packet after B
proves the profile-authored fork seam.

**Product intent:** Today `generate_variants(mode=...)` receives the mode
but does not read it. Modes change label/bias/scoring context, but
conservative and experimental produce the same candidate move set. This
packet makes mode behavior real:

- same problem + same producer + **different mode → different candidate
  variant set**;
- same mode name + same problem + **different producer → differences
  attributable to producer-authored profile data**.

**Architecture (the user's, verbatim):** Extend producer profile
`search_modes` entries with authored declarations such as: favored variant
kinds per mode; suppressed variant kinds per mode; optional mode-flavored
emphasis parameters; allowed-risk / allowed-authority posture if not
already present. **The engine owns the shared move vocabulary. The profile
decides what each mode reaches for. Governance owns the safety cap.**
`engine owns move vocabulary / profile owns mode reach / governance owns
safety cap.`

**Required behavior:** `generate_variants` must READ the active mode and
fork candidate generation based on profile-authored mode declarations. The
candidate set varies by mode where the profile says it should. Acceptable
behavior examples (the user's): conservative favors lower-risk / smaller
intervention variants; balanced/default keeps the normal curated center;
experimental reaches for profile-favored higher-contrast variants WITHIN
allowed risk; Timbaland experimental reaches toward negative-space /
groove-contrast variants; Quincy experimental reaches toward
arrangement-lift / ensemble-rebalance variants; **Halee/Ramone conservative
remains reference-safe and does not drift unintentionally.**

## Non-scope (the user's, verbatim)

No new mode-specific move families. No dropout/mute-only negative-space
families. No new analyzers. No changes to safety/governance/veto behavior.
No weakening of allowed-risk caps. **No per-producer code branches. No
hardcoded Timbaland or Quincy behavior in the engine.** No change to
existing default behavior **except where the profile-authored default mode
explicitly requires it AND the proof captures it**. No merge until
qa + reviewer dual-green (merge = user gate).

## Required proof (the user's ten, verbatim)

1. `generate_variants` reads the active mode.
2. Different modes can emit different candidate variant sets for the same
   producer/problem.
3. Differences are driven by profile-authored `search_modes` data.
4. Same mode name across different producers can differ because profile
   data differs.
5. No per-producer engine branching exists.
6. Existing safety/governance/veto surfaces remain invariant.
7. Allowed-risk caps still bind.
8. Default/reference behavior does not drift unintentionally.
9. The differential proof can attribute differences to profile data, not
   code-path hacks.
10. Artifacts/renderers expose enough mode information to explain why a
    candidate set differed.

## Required adversarial reviewer attacks (any success = MUST-FIX, not a nit)

The reviewer attempts to prove: (1) the mode argument is still cosmetic;
(2) mode changes only ranking, not the candidate set; (3) profile data is
ignored; (4) the engine has hidden producer-specific branches;
(5) experimental can exceed the allowed-risk cap; (6) suppressed kinds
still appear; (7) default Halee/Ramone behavior drifts without an authored
reason; (8) same-mode/different-producer differences cannot be traced to
profile data.

## Acceptance bar (the user's, verbatim)

mode becomes load-bearing · candidate sets can differ by mode ·
differences are profile-authored · safety caps still bind · no new move
families are introduced · no producer-specific engine code appears ·
existing default behavior remains explainable.

## Orchestrator implementation notes (recon, binding on the builder)

- The seam: `logic_mix_os/creative.py` — `generate_variants(problem,
  result, mode)` (line ~357) ignores `mode`; the caller (~line 570) holds
  the resolved profile — thread it (additive `profile=None` parameter,
  the P-029 `score_variant` pattern). The loader
  (`doctrine/producer_profile.py`) validates `search_modes` — extend
  validation for the new OPTIONAL declaration fields (absent = neutral =
  today's behavior, documented), while the three SHIPPED profiles author
  them EXPLICITLY (no silent inheritance for load-bearing choices).
- **Drift discipline (requirement 8 + the staleness pin):** the committed
  sample trees byte-compare to fresh renders. Authored declarations for
  each profile's DEFAULT mode must keep its default candidate set
  byte-identical, OR any conscious default-mode fork must be enumerated
  and captured (goldens/pins/sample regeneration all in-packet). Additive
  artifact keys for requirement 10 that touch rendered artifacts =
  conscious enumerated delta: regenerate BOTH trees via the verbatim
  README invocations and keep the staleness pin at full strength.
- Suppression can never empty a candidate set — the engine guarantees a
  non-empty set with a documented, profile-agnostic fallback rule, and the
  fallback's use is surfaced in the artifact (honesty over silence).
- Per-carrier threading lesson (P-039): flag PRESENCE is not flag
  THREADING — prove the profile's declarations REACH generate_variants
  through the real call chain, not just that the parameter exists.

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the engine seam (mode-reading fork in `generate_variants`
  + profile threading + loader validation) + the reference profile's
  explicit authored declarations + tests — full suite green with ZERO
  behavioral drift (byte-identity of default outputs).
- **Commit-2:** timbaland + quincy authored mode declarations + the
  mode-differential proof (same producer/different modes; same
  mode/different producers) + requirement-10 artifact surface + any
  enumerated sample regeneration — full suite green.

## After this packet

**STAGE C** — new mode-specific move families — as the next possible
product payoff, NOT built until B proves the seam.

---
_Set active by the orchestrator on the user's explicit go (2026-07-03).
One packet at a time: builder → qa + reviewer → archivist → receipt._
