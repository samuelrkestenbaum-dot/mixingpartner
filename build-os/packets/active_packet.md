# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — awaiting the orchestrator to confirm the next packet.
- **Packet id:** —
- **Last-closed:** **P-027** — Source `governance.py`'s producer-specific values
  from the reference profile (byte-identical, WIDENED per Finding A). qa GREEN,
  reviewer pass (Codex unavailable — single-reviewer). Two commits `e4786ca`
  (Part A + no-aliasing test, green in isolation = 343) + `7b1c26d` (Part B widen +
  source + round-trip). Suite 331 → 351 (+20); regression 68/68 UNCHANGED. Safety
  kill-switches (1–5) STAY hardcoded; the 4 aesthetic switches + `taste_triangle` +
  `veto_thresholds` now profile-sourced. No-aliasing DISCHARGED; emotion-blend
  round() proven byte-identical (all 1,030,301 integer triples). **Local-only**
  (`e4786ca`, `7b1c26d` on the dev branch on top of P-026 `c4a092d`, on top of the
  P-025 commits, on top of the `e79426a` PR #16 base) — NOT pushed/merged. Receipt:
  `build-os/receipts/P-027-governance-sources-values-from-reference-profile.md`.

## Next (staged — the orchestrator confirms before the builder starts)

- **P-028 — doctrine extraction (WIDENED per Finding A + ALIASING-PROOF required) —
  the LAST and LARGEST extraction of the producer-agnostic epic.** Source
  `doctrine_engine.py`'s producer-specific judgment from
  `load_profile("halee_ramone")` (same byte-identical pattern as P-026/P-027), AND
  — per P-025's Finding A — WIDEN the profile to capture **ALL doctrine scoring
  functions' constants**, not just `_halee` / `_ramone`:
  - `_vocal_centrality`, `_depth_hierarchy`, `_section_contrast`, `_static_mix`,
    `_dynamic_mix` — baselines (80.0 / 70.0 / 40), penalties, and coefficients
    (e.g. `30 + rms_std*8 + width_std*140`).
  - **ALIASING-PROOF (BINDING, still open — see residue):** doctrine's consumers
    must never mutate a sourced global in place. Grep for in-place mutation of the
    sourced structures + add a no-aliasing test (fire the relevant path, assert the
    shared `_DEFAULT_PROFILE` structures are byte-unchanged) + a determinism check.
    Do NOT close P-028 without this proof.
  - **Byte-identical:** existing doctrine tests pass UNEDITED; regression 68/68 held.
  - **≤2 commits; Commit-1 green in isolation.** `creative.py` / `governance.py`
    (done) / `pipeline.py` (P-029) untouched.
  - **Spec note (from P-027):** OMIT the "NO model identifier" constraint line — the
    mandated `Co-Authored-By: Claude Opus 4.8` trailer is the sanctioned form and is
    required (it conflicts with that line and keeps tripping the reviewer).

- **Then:** P-029 (parameterize the pipeline / per-call profile — the structural fix
  for the aliasing risk) → P-030 (rename the `halee` / `ramone` dims off the producer
  names) → P-031 (confidence framework — consume the metadata stamp) → P-032 (second
  producer) → P-033 (expose producer selection).

---
_Cleared by the archivist on the P-027 close, 2026-07-01. P-027 (governance sourced
from the profile + WIDENED; the safety chassis kept hardcoded and separate) is the
last-closed; P-028 (doctrine extraction, the last and largest) is staged as Next.
One packet at a time._
