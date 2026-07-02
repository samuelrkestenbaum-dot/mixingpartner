# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-032h confirmed by the orchestrator-in-chief
  (2026-07-02), handed to builder. THE PAYOFF PACKET.

## Last-closed

- **P-031 ✓ CLOSED (2026-07-02)** — the confidence framework: the REQUIRED
  per-area `confidence_map` (area / level ∈ {high, limited, deferred} /
  reason) is validated (no silent defaults), authored for halee_ramone
  (8 entries: 2 high / 1 limited / 5 deferred; machine-checked against the
  weights; verbatim-pinned), and rendered per-call (additive `confidence`
  key + verdict "## Confidence" section). qa GREEN (572 → 600; 68/68;
  Commit-1 iso 591; byte-identity modulo EXACTLY the additive key/section);
  reviewer PASS (one fix-then-pass round, fully resolved — `b869ebd`
  corrected the per-section true-sub deferral reason to band resolution).
  **THE HONESTY LAYER IS IN PLACE.** Commits `51a107c` + `4af24e2` (pushed)
  + `b869ebd` (local at close; orchestrator pushes). NOT merged (merge base
  `e79426a` = PR #16). Receipt:
  `build-os/receipts/P-031-confidence-framework.md`.

## Active packet spec (confirmed) — P-032h: AUTHOR `timbaland.json` (THE PAYOFF PACKET)

The first non-byte-identical output of the producer-agnostic epic: the second
live producer profile. Everything the seven measurement packets + P-031 built
converges here — the second producer ships **different / profile-authored /
confidence-stamped / honesty-labeled / safety-invariant.**

### The three REQUIRED declarations (in writing, in the JSON)

1. **`protect_iconic_loops`** — Timbaland's loop philosophy, declared
   explicitly (the P-032g hinge: the engine detects static-vs-iconic; the
   profile decides).
2. **`vocal_blend_policy`** — `acceptable_blend` + `confidence_floor`,
   declared explicitly (the P-032f gate).
3. **Its OWN `confidence_map`** (P-031, REQUIRED — no silent defaults):
   high = groove / space / low-end / loop interpretation; limited =
   vocal blend per the inert-blend corollary (the analyzer emits no non-lead
   vocal masking events on real data); deferred = cultural recognizability /
   true hook recurrence / motif provenance. **Verbatim-pin the map like
   halee_ramone's** (the reviewer judgment note: validation accepts duplicate
   areas + extra entry keys — the pin is the guard).

### Binding constraints

- **Weights = the user's APPROVED Timbaland value system:** protect
  `groove_identity` / `negative_space` / `low_end_motion` /
  `section_contrast`; relax `vocal_centrality` / `lush_depth` /
  `loop_deconstruct` bias — **relax ≠ remove.**
- **Mind the axis ceilings:** `low_end_motion` tops out at **84**,
  `vocal_role_fit` at **85** — never 100; weight-authoring must account for
  this.
- **`_DEFAULT_PROFILE` no-aliasing carry-forward** — this is the SECOND live
  profile loaded per call: copy-before-mutate; never mutate a loaded
  profile's structures in place.
- **Provenance:** hand-curated-documented → confidence HIGH per the standing
  honesty policy (hand-curated → high; derived → low, labeled; LLM →
  draft-only, never high).
- Safety invariant: the 5 SAFETY kill-switches stay hardcoded; a profile can
  never drop a safety guarantee.
- Rigor bar as established: `python fixtures/generate_fixtures.py` first;
  ≤2 commits, Commit-1 green in isolation; full suite green from the **600**
  baseline; regression 68/68; observational language; NO push/merge/remotes
  (orchestrator pushes).

### Differential expectations (binding on P-032i, which follows immediately)

P-032i proves Timbaland-vs-Halee/Ramone differentially: expect deltas from
the **groove / space / low-end / loop / surprise** axes — **NO vocal-blend
delta** on current fixtures (the P-032f reviewer corollary: the blend gate is
inert on real pipeline data until an analyzer-extension packet emits non-lead
vocal-band events).

## Epic arc

**e ✓ → a ✓ → b ✓ → d ✓ → c ✓ → g ✓ → f ✓ → P-031 ✓ (confidence — the
honesty layer) → P-032h (author `timbaland.json` — ACTIVE) → P-032i
(differential proof).** P-030 (rename dims) orthogonal/last.

---
_Cleared by the archivist on P-031 close (2026-07-02). One packet at a time.
The orchestrator confirms the staged packet before the builder touches it._
