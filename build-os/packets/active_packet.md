# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

## Last-closed

- **P-026 — Source `creative.py`'s producer-specific values from the reference
  profile (byte-identical, single-source-of-truth).** CLOSED 2026-07-01 — qa GREEN,
  reviewer pass (Codex unavailable — single-reviewer verdict). `creative.py` now
  sources its 8 producer-specific globals FROM `load_profile("halee_ramone")`; the
  hardcoded literals are DELETED, so `halee_ramone.json` is their single source of
  truth. Byte-identical (P-012/13/15/16 creative tests pass UNEDITED; regression
  68/68 UNCHANGED), no-aliasing-proven. Single commit `c4a092d` (parent `84d208d`,
  base `e79426a`); suite 319 → 331 (+12). **Local-only — not pushed/merged.**
  Receipt: `build-os/receipts/P-026-creative-sources-values-from-reference-profile.md`.

## Next (staged, NOT yet active — awaiting orchestrator confirmation)

- **P-027 — governance extraction (WIDENED per Finding A + ALIASING-PROOF
  required).** Source `governance.py`'s producer-specific values from the profile,
  byte-identical, the same way P-026 did for `creative.py`. **WIDEN** per P-025's
  Finding A to ALSO capture: the inline `taste_triangle` rule
  (`width_bloom + intimate → identity -= 30`, ~L179–182), the `<45` reject / `<50`
  align-veto / `75` align-fallback thresholds, and the `emotion` blend (~L176), on
  top of `_TRUTH_ALIGNMENT` / `_TASTE_KIND_BIAS` / `TASTE_MAX_DELTA` / the aesthetic
  kill-switches. **BINDING (from P-026):** must independently PROVE governance's
  consumers never mutate the sourced globals in place — grep for in-place mutation +
  a no-aliasing test like P-026's. Byte-identical; guarded by the P-025 round-trip.

---
_Cleared by the archivist on P-026 close (2026-07-01). No packet active; P-027 is
staged as Next. One packet at a time._
