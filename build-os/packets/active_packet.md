# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — P-030 (the artifact-contract migration) is
  **✓ CLOSED** (2026-07-02; qa GREEN, reviewer PASS with no must-fix; Codex
  not available — single-model review). Receipt:
  `build-os/receipts/P-030-artifact-contract-migration.md`. The next packet
  below is STAGED, NOT active — nothing activates until the orchestrator
  confirms.

## Last-closed

- **P-030 ✓ CLOSED** — the artifact-contract migration (Option A + memory.py
  dual-read + verdict filename fold-in): `halee_score` →
  `physical_space_score`, `ramone_score` → `emotional_hierarchy_score`,
  internal/evidence/profile keys renamed, `halee_ramone_mix_verdict.md` →
  `mix_verdict.md`. Clean break, NO emitted aliases; memory.py read-only
  dual-read the only carve-out. The health bar HELD: all 90 numeric values
  identical under both producers (ref 73.8/70.7/74.3; tim 68.4/52.6/49.7);
  golden diff = exactly the two key-rename lines per fixture. Suite **705** /
  **68/68 vs the regenerated goldens**. Commits `21c0ab0` + `0c7885e` on
  parent `8f14d4d`, PUSHED to the dev branch, NOT merged (merge base
  `58d21dd` = PR #17). The P-025-era rename debt is PAID: a producer-agnostic
  engine emits a producer-agnostic contract.

## Staged next (NOT active until the orchestrator confirms)

- **Packet id:** (to be assigned by the orchestrator)
- **Title:** the analyzer extension — emit non-lead vocal-band masking events
  from the masking analyzer.
- **Why:** this is the change that makes the vocal-blend policy LIVE on real
  data — the P-032f inert-blend corollary's NAMED legitimizing packet. Today
  the masking analyzer emits vocal-band `bad_masking` ONLY against the LEAD
  (via `_vocal_conflict`, elements always [lead, other]), so the blend gate is
  exercised only via synthetic events.
- **Binding expectations / constraints:**
  - It will **legitimately break the P-032i no-vocal-blend-delta pin** — flip
    it via the designed conscious-edit path (the P-031/P-033 precedent:
    update-never-weaken, strengthen where possible).
  - **Must also fix `creative.py:98`'s name-based "vocal" match** — the
    latent misfire risk the P-032f reviewer flagged for exactly this packet.
  - **Byte-identical discipline:** the reference profile (opted OUT of blend:
    `acceptable_blend: false`) must see NO judgment change from the new
    events beyond honest masking-report additions.
  - **Scope carefully BEFORE building:** new events WILL change
    masking_report artifacts and possibly static_mix / lead readings — a
    scoping pass on which surfaces legitimately move is required first
    (present the plan; do not open blind).
- **Backlog order (keep):** the analyzer extension → the residue sweeps (now
  including the three producer-named-VALUE surfaces from the P-030 reviewer's
  judgment call: search-mode names in emitted creative.json, engine action
  prose, warning doctrine tags — plus the standing items: liveness-docstring
  sweep ~8 files; validation tightening incl. search_modes non-empty +
  default_creative_mode structural checks + the NaN-floor guard; lead_names
  derivation; the shared groove dict; loop_deconstruct literal-kind; cli.py
  --mode help text; fallback-reason wording; duplicate-areas/extra-keys).

## Epic arc (post-merge backlog)

**P-033 ✓ → P-030 ✓ (artifact-contract migration — CLOSED) →** the analyzer
extension (STAGED, above) → the residue sweeps.

---
_Cleared by the archivist at P-030 close (2026-07-02). One packet at a time.
Nothing is active until the orchestrator confirms the next packet._
