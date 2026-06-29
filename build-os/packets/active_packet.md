# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-006
- **Title:** `creative.py` literal cleanup — record-back Site 1 (`loops or supporting[-1:]`) + harden Site 2 prose placeholder (`"the loop"`)
- **Authority:** build

## Honest framing (from the orchestrator's verification)

- **Site 1 (`creative.py:194`, `chorus_lift_B`):** `tracks_affected = loops or supporting[-1:]`. Cannot emit a phantom (both are real-record subsets) BUT can emit an **empty** list under a constructible loop-free + support-free project → violates P-001's non-empty invariant. Also bypasses the `_resolve` seam. **Real latent gap — fix.**
- **Site 2 (`creative.py:217`, `loop` branch):** `target = loops[0] if loops else "the loop"`. `target` is used ONLY in prose (`creative_hypothesis`/`changes`), NEVER in `tracks_affected`; and the `else` branch is dead under the engine path (the `loop` problem only fires when loops exist). **Not an attribution leak — a prose-placeholder hardening:** make intent explicit so prose can never name a non-existent track.

## Goal / "done" criteria (single, testable)

- No variant can emit an **empty** `tracks_affected`, a non-`result.records` name, or the `"the loop"` placeholder string under any constructible input — proven by tests that **RED on today's code** at the leak-prone paths and pass after the fix. Existing 3-fixture invariant test stays green; suite 110 → ~112; regression 68/68.

## In scope (exact)

- `logic_mix_os/creative.py` — **lines 194 and 217 ONLY**:
  - Line 194: `loops or supporting[-1:]` → `_resolve(loops, supporting[-1:], [r["name"] for r in records][:1])` (reuse P-001's `_resolve` + the established final real-record fallback; always non-empty when any record exists).
  - Line 217: `loops[0] if loops else "the loop"` → fall back to a real-record name instead of the literal (e.g. `loops[0] if loops else (([r["name"] for r in records][:1] or ["the loop"])[0])`), so prose names a real track whenever records exist.
- `tests/test_creative_attribution.py` — add the two targeted unit tests.

## Out of scope (explicit)

- All P-001-resolved sites (`lead_target`/`drum_target` at 183-184; `chorus_lift_A/C/D`, `density_A/B`, `depth_A`, `vocal_A/B`). Do NOT touch.
- `score_variant`, `winning_variant`, `run_creative_engine`, `detect_creative_problems`, scoring weights, governance, CLI, renderers, fixtures.
- NO signature change to `_resolve`/`_lead_vocal_tracks`/`_drum_tracks`/`_supporting_elements` — reuse only; invent no parallel resolver.

## Test plan (no real DAW — constructed data only)

- `generate_variants(problem, result, mode)` reads ONLY `result.records`. Build a tiny stand-in (`SimpleNamespace(records=[...])`); each record dict needs the keys it reads: `name`, `instrument_identity`, `identity_family`, `source_kind`, `depth_default`. Do NOT call `score_variant`/the full engine.
  1. **Site 1 empty-attribution test:** records with NO loops and NO supporting (e.g. one `lead_vocal` + one drum). `generate_variants({"id": "chorus_lift"}, result)` → assert `chorus_lift_B`'s `tracks_affected` is non-empty and ⊆ real record names. REDs today (returns `[]`).
  2. **Site 2 placeholder test:** records with NO loop but ≥1 real track. `generate_variants({"id": "loop"}, result)` directly (only way to reach the `else`) → assert no variant's `creative_hypothesis`/`changes` contains the literal `"the loop"`, and `tracks_affected` ⊆ real names. REDs today (prose contains `the loop`).
- Keep `test_creative_attribution.py`'s 3-fixture invariant test green.

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `4768483` (clean, up to date). Default `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** add the two targeted unit tests AND the two one-line fixes (194, 217) in one commit; passes its own tests standalone.
2. **Commit 2 (optional):** none expected.

## Guardrails

- Build authority; deterministic; pure list logic + constructed dicts; no network/subprocess/AppleScript/`.logicx`/`RealLogicSessionAdapter`; reuse P-001 helpers.

---
_Confirmed P-006 on the user's "work the next bunch". Builder implements exactly
this; archivist clears on close._
