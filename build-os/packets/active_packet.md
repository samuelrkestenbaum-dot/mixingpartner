# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Last-closed:** **P-025** — `ProducerProfile` schema + `load_profile()` +
  extracted `halee_ramone.json` reference (data + loader ONLY, no wiring).
  CLOSED 2026-07-01 — qa GREEN, reviewer pass. Receipt:
  `build-os/receipts/P-025-producer-profile-schema-loader-halee-ramone-extraction.md`.
  FOUNDATION of the producer-agnostic epic: today's 100%-hardcoded Halee/Ramone
  judgment is now a frozen `ProducerProfile` + a pure `load_profile()` + the
  VERBATIM `halee_ramone.json` reference, byte-identical round-trip-guarded (exact
  + non-vacuous indirect) and honesty-metadata-stamped, and **COMPLETELY UNWIRED**
  (the four judgment sources byte-unchanged; regression 68/68 UNCHANGED). Two
  commits `195127c` + `e6cb038` (local-only on the dev branch on top of the
  `e79426a` PR #16 base; not pushed/merged). Suite 293 → 319 (+26). Codex
  unavailable — single-reviewer verdict.

## Next (staged, confirm via the orchestrator before opening)

- **P-026 — extract creative-scoring judgment onto the profile, byte-identical.**
  Move `creative.py`'s producer-specific structures behind the `ProducerProfile`
  surface the P-025 round-trip already pins (`kind_scores` / nudge & promotion
  tables / caps / `_RISK_PENALTY` / search modes / philosophy), keeping behavior
  BYTE-IDENTICAL — the round-trip guard is the safety net. Extract, don't change.
  No wiring beyond what a byte-identical extraction requires; no push/merge/deploy.

## The producer-agnostic epic arc (active roadmap)

- **P-025 ✓** — foundation: `ProducerProfile` schema + `load_profile()` + extracted
  `halee_ramone.json`, round-trip-guarded, UNWIRED.
- **P-026** — extract creative-scoring judgment onto the profile (byte-identical). NEXT.
- **P-027** — governance extraction, **WIDENED** (Finding A): also capture the
  inline `taste_triangle` rule `width_bloom + intimate → identity -= 30` (~L179–182),
  the `<45` reject / `<50` align-veto / `75` align-fallback thresholds, and the
  `emotion` blend definition (~L176) — beyond `_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS`
  / `TASTE_MAX_DELTA` / aesthetic kill-switches.
- **P-028** — doctrine extraction, **WIDENED** (Finding A): capture ALL doctrine
  scoring functions' constants (`_vocal_centrality` / `_depth_hierarchy` /
  `_section_contrast` / `_static_mix` / `_dynamic_mix` — baselines 80.0/70.0/40,
  penalties, coefficients), not just `_halee` / `_ramone`.
- **P-029** — parameterize the pipeline to CONSUME the profile (first wiring step;
  guarded byte-identical for `halee_ramone` by the round-trip).
- **P-030** — rename the `halee` / `ramone` dimension names off the producer names.
- **P-031** — confidence framework: consume the profile metadata stamp per the
  confirmed honesty policy (hand-curated=high / derived=low-labeled / LLM=draft-only).
- **P-032** — second producer (first real test of producer-agnosticism; honesty-policy-governed).
- **P-033** — expose producer selection (user-facing selection surface).

## Standing (not part of the active epic)

- **P-024 (MCP transport, option C step 2)** — the prior cowork arc closed at
  PR #16; P-024 (a thin MCP server wrapping the cowork registry, reusing
  `describe_contract` metadata as tool schemas + a version-fingerprint guard)
  remains an UN-OPENED candidate. Do not open blind; confirm via the orchestrator.

---
_Cleared by the archivist on P-025 close (2026-07-01). No packet in flight. Next
staged = P-026 (extract creative-scoring judgment onto the profile, byte-identical),
the second step of the producer-agnostic epic. One packet at a time._
