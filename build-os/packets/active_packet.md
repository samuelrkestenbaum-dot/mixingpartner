# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-031 confirmed by the orchestrator-in-chief
  (2026-07-02), handed to builder. **Scope UPGRADED by the user at P-032f
  close: per-interpretation-AREA confidence, not a single profile-level stamp.**
- **Packet id:** P-031
- **Title:** confidence framework — per-area honesty labeling
  (high / limited / deferred, each with a stated reason), machine-readable in
  the profile, rendered on the report surface.

## Why this packet (user-stated, binding)

The second producer must not ship as merely "different." It ships as:
**different / profile-authored / confidence-stamped / honesty-labeled /
safety-invariant.** P-031 is what lets `timbaland.json` say:

```
high confidence:     groove / space / low-end / loop interpretation
limited confidence:  vocal blend on current fixtures — analyzer does not yet
                     emit non-lead vocal masking events (the inert-blend
                     corollary)
deferred:            cultural recognizability, true hook recurrence,
                     motif provenance
```

The honest deferrals documented in docstrings across seven packets become
FIRST-CLASS, machine-readable profile data that a human or Cowork actually
reads in the verdict/report artifacts — which parts of the judgment to trust,
at what strength, and WHY.

## Spec (build exactly this)

1. **Profile schema — a REQUIRED `confidence_map` structure** (top-level, the
   established required-field discipline): a list/dict of interpretation AREAS,
   each entry carrying `area` (string), `level` (exactly one of
   `high` / `limited` / `deferred`), and `reason` (non-empty string).
   Structural validation in `producer_profile.py` `_validate` (reject missing
   field, unknown levels, empty reasons, non-string areas). The existing
   profile-level `metadata` stamp (provenance/confidence/risk_class from P-025)
   STAYS — the map complements it (global provenance + per-area trust).
2. **Author halee_ramone's own honest map** — e.g. high: vocal-centrality /
   depth-hierarchy / section-contrast / static-dynamic interpretation
   (hand-curated from documented technique, live axes); high: the seven new
   agnostic axes exist but are weight-0 BY CHOICE (state that as the reason —
   the reference profile deliberately does not weight them); limited/deferred
   entries mirroring the standing honest deferrals (onset-timing strong forms,
   fingerprint typing, cultural iconic-ness, hook recurrence, motif
   provenance, per-section true-sub). Word reasons observationally.
3. **Render it on the report surface** — wherever the profile's judgment is
   presented (the verdict markdown `halee_ramone_mix_verdict.md` renderer
   and/or the doctrine_score/report JSON): a compact "Confidence" section
   listing the areas by level with reasons, sourced from the loaded profile's
   map (per-call profile, P-029 threading — a passed profile's map renders,
   not the module default's). Machine-readable copy in the JSON output
   (additive key; schema updated — no `additionalProperties:false` conflicts).
4. **BYTE-IDENTICAL DISCIPLINE — this is labeling, never judgment:** no score,
   variant, promotion, or recommendation may change. The doctrine + creative
   surfaces stay byte-identical (73.8 / 70.7 / 74.3). The ONLY output deltas
   allowed: the new confidence section/keys (additive). If the verdict
   markdown gains a section, the golden regression must still hold 68/68
   (verify what the golden pins — categorical + 7 original score keys — and
   prove the addition is invisible to it; if any pinned artifact WOULD change,
   stop and report rather than weaken a guard).

## Tests (test-first — the binding guards)

1. **Byte-identical** — doctrine + creative surfaces on all 3 fixtures
   unchanged; regression 68/68; the new keys/sections are purely additive.
2. **Validation** — missing map / unknown level / empty reason / non-string
   area all rejected by `load_profile` (no silent defaults — the P-032f
   attack-4 discipline).
3. **Rendering liveness** — a synthetic profile with a DIFFERENT map renders
   ITS areas/levels/reasons (per-call, not module default); halee_ramone's map
   renders its authored entries; sabotage (drop the threading / hardcode the
   section) fails the liveness test while byte-identical stays green.
4. **Honesty pins** — halee_ramone's map contains the inert-blend/deferred
   entries verbatim-pinned (so a future packet can't silently delete the
   honesty labels); observational language guard on all reasons.
5. **No-aliasing** — the renderer reads, never mutates, the profile map.

## Rigor bar (established)

- `python fixtures/generate_fixtures.py` FIRST; ≤2 commits, Commit-1 green in
  isolation; full suite green from the **572** baseline; regression 68/68;
  observational language; commit trailers `Co-Authored-By: Claude Fable 5
  <noreply@anthropic.com>` + the Claude-Session link; NO push/merge/remotes
  (orchestrator pushes).

## Last-closed

- **P-032f ✓ CLOSED** — dual-green, six attacks defeated; ALL SEVEN Timbaland
  weight-up axes landed (14 components); measurement phase COMPLETE. Receipt:
  `build-os/receipts/P-032f-vocal-role-blend-policy.md`.

## Epic arc

**e ✓ → a ✓ → b ✓ → d ✓ → c ✓ → g ✓ → f ✓ → P-031 (confidence — ACTIVE) →
P-032h (author `timbaland.json`: declare BOTH required philosophies + its own
confidence_map; mind ceilings lem-84/vrf-85; second-live-profile no-aliasing)
→ P-032i (differential proof: expect deltas from groove/space/low-end/loop/
surprise — NOT vocal blend, per the binding corollary).** P-030 orthogonal/last.

---
_Set active by the orchestrator-in-chief (2026-07-02). One packet at a time.
Builder implements exactly this; qa proves; reviewer judges; archivist closes
with a receipt._
