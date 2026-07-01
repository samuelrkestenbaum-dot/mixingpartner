# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-021
- **Title:** Verified end-to-end agent walkthrough — a full session through the cowork surface (TESTS-ONLY)

## Why (the arc to the canonical target — the MILESTONE step)

Arc P-019→P-023 to "Claude Cowork drives a full mixing session end-to-end."
P-019 made the loop closeable inside cowork; P-020 made the flow discoverable
(`describe_session`). P-021 is the milestone: **prove, executably, that an agent
using ONLY the cowork command surface can drive a complete session start-to-finish
and the learning loop closes.** After this, "Cowork-usable end-to-end" is a pinned
fact, not a claim. TESTS-ONLY — no product behavior change (the surface is already
built; this proves it works as a whole).

## Authority

**Build / test-additive — in authority.** No product/runtime change (tests-only).
**Merge to default stays gated on the user's explicit go; dev-branch commits
covered by standing push-go.**

## Scope (the builder implements EXACTLY this)

### Tests-only — a new `tests/test_cowork_session_walkthrough.py`
Drive a full mixing session **through the cowork surface** (`build_context` +
`run_command` only — the agent's own command set) on a seeded fixture, following
the canonical phase order that `describe_session` returns, and prove the chain
works as ONE session:

1. **Discover-then-drive:** call `run_command("describe_session", ctx)` to get the
   ordered phases, then drive the ESSENTIAL happy-path command of each phase in
   order via `run_command` — intake → classify → diagnose → plan → checklist →
   validate → record-outcome → next-pass. (You need not run all 34 commands — pick
   the core end-to-end path; param-heavy/auxiliary commands like
   `compare_to_reference` [needs a reference], `override_track_identity`,
   `build_missing_tool` may be exercised separately or noted, not forced into the
   line.) Assert each driven command returns sane, structured (JSON-serializable)
   output — the chain runs without dropping out of the cowork surface.
2. **The loop CLOSES (the milestone assertion):** at record-outcome, call
   `run_command("record_mix_pass", ctx, ..., reverted=True)` (the LIVE channel);
   then build a FRESH `build_context(memory_dir=...)` and call
   `run_command("suggest_next_pass", ...)` — assert the confirmed "Revert last
   pass" surfaces. NO hand re-run of `record_pass`/planner. This proves an agent
   closes the loop entirely within the cowork surface (reuses the P-019 liveness
   pattern, now as part of a FULL session).
3. **Pin the live-vs-dead-ledger distinction (the carried P-020 clarity nudge —
   executable):** assert that `run_command("write_mix_decision", ...)` (the
   display-only DEAD ledger) does NOT change `suggest_next_pass` output, whereas
   `record_mix_pass` (LIVE history) DOES. This pins, executably, that only
   `record_mix_pass` closes the loop — so a future agent/reader can't mistake the
   ledger write for loop-closing.
4. **Determinism / honesty:** the walkthrough must use real seeded fixtures and the
   real `analyze()` path (fake adapters only — no DAW/Logic/AppleScript/subprocess/
   network/`.logicx`). Assert the driven session is deterministic where it should
   be (same inputs → same plan/next-pass).

### Honesty clause
If driving through the cowork surface reveals a REAL gap — a phase whose essential
command can't be reached, a command that needs state the cowork context doesn't
carry, or the loop NOT closing through the full session — STOP and report it as a
finding (like P-014 / the P-016 inert catch). The walkthrough's job is to tell the
truth about whether the surface is actually agent-drivable end-to-end; a green
test that skips the hard part is worse than an honest gap. If you find a gap that
needs a small product fix, report it — do NOT silently expand scope into product
code; that becomes a separate packet (possibly P-022).

## Constraints

- **≤2 commits** (likely 1: the walkthrough test file). **Commit-1 green in
  isolation.**
- **No product/runtime change** — tests-only. If a product fix proves necessary,
  STOP and report (honesty clause), don't fold it in silently.
- **No external mutation** — no push / merge / deploy / secret.
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **269 → 269+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held.
- Commit-1 green in isolation.
- **The milestone is proven:** a full session driven through the cowork surface
  (via `describe_session`'s order) completes, and the loop CLOSES (record via
  `record_mix_pass` → fresh context → `suggest_next_pass` shows the confirmed
  revert), with NO hand re-run — load-bearing (fails if the record isn't threaded).
- **Live-vs-dead pinned:** `write_mix_decision` does NOT change next-pass;
  `record_mix_pass` does.
- Safety grep clean; UI N/A; all prior tests (P-008/9/18/19/20 + existing) green,
  UNEDITED (this packet adds a test file; it must not need to change existing
  assertions — if it does, that's a signal to flag, not silently edit).

---
_Confirmed as active by the orchestrator-in-chief (P-021), the milestone step of
the arc to the Claude-Cowork-usable final state. One packet at a time._
