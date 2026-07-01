# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE
- **Packet id:** —
- **Title:** —

## Last closed

- **P-016 — Evidence-gated problem-native promotion — `loop` branch (the FIRST
  reward/promotion nudge) + a production live-wire.** Closed 2026-07-01.
  User-delegated (direction A "open the base-scoring decision space" + fork (i)
  "evidence-gated" + "keep skating"; the build-orchestrator routed). Two commits:
  `b15b957` (Commit-1 — the promotion mechanism `CREATIVE_PROMOTION_CAP = 4.0` /
  `_PROMOTION_TABLE` / `_foregrounded_loop` predicate / `score_variant`
  application + binding tests; **green in isolation, 226 passed**) and `a9f4e26`
  (Commit-2 — the LIVE-WIRE: relocate `analyze_provenance` + `audit_all` to just
  before `run_creative_engine`, a pure relocation, + two production-liveness
  tests). Crosses the penalty-only line P-012/P-015 held — the FIRST reward nudge;
  bounded, evidence-gated, transparent, layered on an UNTOUCHED `_KIND_SCORES` and
  an UNTOUCHED penalty path, now LIVE in production. **★ Commit-1's mechanism was
  INERT in production (run_creative_engine ran before provenance/source_audits);
  the orchestrator-in-chief caught it and Commit-2 live-wired it** — a P-009-style
  catch. Suite **217 → 228 passed** (+11; 0 failed/skipped/warnings); regression
  **68/68, 0 critical, 0 warnings** (`loops_not_foregrounded` held). qa **GREEN**;
  reviewer **pass** (non-vacuity mutation check + reward-creep watch-item);
  **Codex NOT available — single-reviewer verdict**. **Local-only** on the dev
  branch (not pushed/merged at close). Receipt:
  `build-os/receipts/P-016-evidence-gated-loop-promotion.md`.

## Next (staged, not active — user-gated)

- **More reward nudges (now IN-DOCTRINE, precedent set by P-016)** — future reward
  rows on other branches (`density → depth_cleanup`, `chorus_lift →
  drum_room_bloom`). **User-gated per-row;** each must clear the P-016 bar
  (evidence gate + non-vacuity mutation check + collateral-safety proof + a
  **live-wire check**: evidence computed before `run_creative_engine`, asserted
  with NO re-run). Do NOT batch.
- **Deeper `_KIND_SCORES` re-curation** — the bigger creative-scoring lever,
  untouched by P-012/P-015/P-016 by design. User-gated.
- Other deferred items unchanged (wider `--memory-dir`, event-logging producers,
  taste-flip-via-product-change) — see `build-os/memory/residue.md`.

---
_Cleared by the archivist on the P-016 close. One packet at a time; the
orchestrator stages the next on the user's go._
