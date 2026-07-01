# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-032f confirmed by the orchestrator-in-chief after the
  USER'S EXPLICIT GO (2026-07-01): **Decision 1 = B (acceptable blend,
  profile-gated only) + Decision 2 = conservative default + explicit confidence
  threshold.** Handed to builder.
- **Packet id:** P-032f
- **Title:** vocal-role refinement (`vocal_type`) — the LAST of the seven
  Timbaland weight-up axes; HIGH risk; engine detects vocal function, profile
  decides masking philosophy.

## THE USER'S APPROVED RULE (verbatim, binding)

```
lead or uncertain            → protect clarity (full lead-grade protection)
hook_candidate               → protect impact/clarity unless profile explicitly
                               says otherwise later (NOT in this packet)
chop/stutter/adlib or stack
  + profile opt-in
  + confidence threshold met → acceptable blend MAY apply
```

- **Decision 1 (B):** masking of chopped/stuttered/adlib vocals or background
  stacks may be treated as acceptable blend ONLY when a producer profile
  explicitly opts in via a REQUIRED profile field. **Halee/Ramone declares it
  false and remains byte-identical.** Timbaland may later declare true in
  `timbaland.json`; the behavior must NOT activate before that explicit opt-in.
- **Decision 2 (stricter):** when vocal type is UNCERTAIN → protect-as-lead;
  uncertain vocals must NEVER be treated as percussion/texture/acceptable-blend.
  Acceptable blend additionally requires the percussion/texture reading's
  CONFIDENCE to clear an explicit threshold stored in the profile; below it,
  full lead-grade protection. **Misclassification fails CLOSED toward vocal
  protection.**

## Required architecture (user-mandated)

- **engine detects vocal function; profile decides masking philosophy;
  safety/governance/non-destructive guarantees remain invariant.** Do NOT bake
  Timbaland taste into engine code.
- New **`vocal_type_classifier.py`** — do NOT mutate `role_classifier.py` in
  place. Only ADDITIVE record fields (`vocal_type` + its confidence).
- ONE new weight-0 doctrine axis (`_vocal_role_fit`, 14th component, appended
  LAST — established idiom).
- The classifier CAPS its strongest hook claim at **`hook_candidate`** — never
  claim proven hook status without a recurrence/provenance signal (none exists
  at doctrine time; honesty policy).
- The profile-gated blend rule follows the **P-032g pattern**: a REQUIRED
  top-level profile field (opt-in flag + confidence floor), checked FIRST so the
  gated path is unreachable under halee_ramone defaults; shared detection basis
  (the gate reuses the classifier's output, never forks the logic).

## Required byte-identity proof (user-mandated — the health metric)

Halee/Ramone must stay byte-identical on BOTH surfaces:
1. **doctrine overall score surface** — all 13 pre-existing components + overall
   × 3 fixtures; **73.8 / 70.7 / 74.3 unchanged**;
2. **creative variant / promotion / recommendation surface** — full
   `result.creative` byte-identical under defaults.
**No final score drift. No creative recommendation drift. No promotion drift.**
(If the blend rule also touches the plan/recommendation renderers, that surface
must be byte-identical under defaults too.)

## Required safety rails (user-mandated)

Acceptable blend must NEVER override:
- lead vocal protection,
- uncertain vocal protection,
- hook_candidate protection (unless explicitly profile-authored LATER — not in
  this packet),
- masked lead protection,
- safety/governance/non-destructive guarantees.

## Required adversarial tests (user-mandated — ANY success = MUST-FIX)

Reviewer and qa must ATTEMPT to prove:
1. an uncertain vocal can get acceptable-blend treatment;
2. a lead can be misread as percussion and lose protection;
3. Halee/Ramone creative recommendations drift before `timbaland.json`;
4. the profile field can be omitted and silently default;
5. acceptable blend can activate without the confidence threshold;
6. hook_candidate gets buried without explicit profile authority.

## What P-032f must prove (user-stated)

```
vocal function can be measured without changing reference taste
masking philosophy can be profile-authored
uncertainty protects the vocal
Timbaland can later treat vocal chops/stacks rhythmically
  without making the engine anti-vocal
```

## Build structure (≤2 commits)

- **Commit-1 (green in isolation):** `vocal_type_classifier.py` (agnostic
  detection from per-stem physics: transient character, chop/loop source_kind,
  band signature, stereo/stack character — types: `vocal_lead`,
  `vocal_hook_candidate`, `vocal_percussive`, `vocal_stack`, `vocal_uncertain`;
  emits confidence; non-vocal stems untouched) + additive record field wiring in
  `pipeline.py` + `_vocal_role_fit` weight-0 doctrine axis (observational
  language, reads the types + masking events) + `halee_ramone.json` constants +
  `_validate` + schema + the usual pin updates + tests (byte-identical BOTH
  surfaces, discrimination, liveness/sabotage, no-aliasing, observational
  language, honest deferrals).
- **Commit-2:** the profile-gated blend rule — REQUIRED top-level profile field
  (opt-in false + confidence floor for halee_ramone); the gate applies the
  approved rule table wherever masking-as-fault manifests for blend-eligible
  vocal classes; unreachable under defaults; tests for the six adversarial
  attacks + flag liveness (opt-in + qualified chop/stack → blend applies;
  uncertain → never; below-threshold → never; lead/hook → never; masked lead →
  never overridden).

## Scoping cautions (carried)

Interacts with 3 live scorers (`_ramone` / `_vocal_centrality` /
`_static_mix`) — their behavior for halee_ramone must not change; the new axis
reads, never rewires them. Established proof idiom applies; run
`fixtures/generate_fixtures.py` first; full suite green from the **512**
baseline; regression 68/68.

## Last-closed

- **P-032g — `loop_context` + `protect_iconic_loops` — THE HINGE. ✓ CLOSED** —
  dual-green incl. the dual byte-identity surface; the profile-decided-gate
  pattern established (THIS packet reuses it). Suite 473 → 512; 13 axes; 6/7.
  Receipt: `build-os/receipts/P-032g-loop-context-hinge.md`.

## Epic arc (Timbaland sub-arc P-032.x)

**P-032e ✓ → P-032a ✓ → P-032b ✓ → P-032d ✓ → P-032c ✓ → P-032g ✓ → P-032f
(vocal-role — ACTIVE, user gate CLEARED: B + stricter) →** [fold P-031
confidence here] → P-032h (author `timbaland.json`) → P-032i (differential
proof). P-030 (rename dims) orthogonal/last.

---
_Set active by the orchestrator-in-chief on the user's explicit go (2026-07-01).
One packet at a time. Builder implements exactly this; qa proves; reviewer
judges (the six attacks are must-fix criteria); archivist closes with a
receipt._
