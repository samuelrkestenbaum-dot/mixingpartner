# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

## Last-closed

- **P-029 — Parameterize the pipeline by a per-call producer profile —
  `analyze(producer=…)` (THE PIVOT). ✓ CLOSED** — qa GREEN, reviewer pass.
  `analyze(producer=…)` now SELECTS which `ProducerProfile` drives the judgment
  (name or object; loaded once per call; threaded to doctrine + creative +
  governance and every leaf scorer). **Byte-identical default** (regression 68/68
  UNCHANGED; reviewer independently byte-diffed all 3 layers × 3 fixtures →
  IDENTICAL); **selection GENUINELY LIVE + load-bearing across all 3 layers** (the
  P-016 lesson: sabotage fails the liveness test while byte-identical stays green);
  KILL_SWITCHES recomposed per call = 5 hardcoded SAFETY + profile aesthetic.
  Two commits `42d6ebd` (green in isolation = 383) + `ea1aaa9`; suite 370 → 384
  (+14). Codex NOT available — single-reviewer. **P-029 local-only** on the dev
  branch (base `e79426a`), not pushed/merged. **★★ MILESTONE — THE PIVOT: the
  producer-agnostic ARCHITECTURE is COMPLETE and VALIDATED; the profile is now a
  LIVE, SELECTABLE LEVER end-to-end.** Receipt:
  `build-os/receipts/P-029-parameterize-pipeline-by-per-call-producer-profile.md`.

## Next (staged — not yet confirmed active)

- **P-030 — rename the `halee` / `ramone` dimension names off the producer names.**
  The dimensions were kept verbatim in P-025 per the byte-identical-first decision;
  P-030 renames them so they describe the aesthetic, not the producer, before a
  second producer lands. Byte-identical judgment (a rename only).
- **★ FLAG — the USER-GATED decision point is approaching: P-032 (the FIRST SECOND
  PRODUCER).** After P-030 (rename) and P-031 (confidence / honesty framework),
  **P-032 requires the user's decision** — WHICH producer to author + the grounding
  per the confirmed honesty/sourcing policy (hand-curated → high / derived →
  low-labeled / LLM → draft-only, NEVER high). This is the payoff of the epic and
  the first real test of producer-agnosticism; surface it for the user before
  building.
- **★ CARRY-FORWARD (reviewer, non-blocking) — for P-032:** the module-level
  `_DEFAULT_PROFILE` singleton still exists in all 3 consumer modules as the
  `None`-default fallback, so the per-module copy-before-mutate no-aliasing
  discipline still carries on the default path. When P-032 loads a SECOND live
  profile per call, do NOT mutate a loaded profile's structures in place.

## Epic arc

**P-025 ✓ (foundation) → P-026 ✓ (creative sourced) → P-027 ✓ (governance sourced +
WIDENED) → P-028 ✓ (doctrine sourced + WIDENED — extraction phase COMPLETE) →
P-029 ✓ (THE PIVOT — profile is a live, selectable lever) → P-030 (rename dims off
producer names) → P-031 (confidence framework) → P-032 (FIRST SECOND PRODUCER —
USER-GATED: which producer + grounding) → P-033 (expose producer selection).**

---
_Cleared by the archivist on P-029 close (2026-07-01). No packet in flight — the
orchestrator confirms the next (staged: P-030) before the builder starts. One
packet at a time._
