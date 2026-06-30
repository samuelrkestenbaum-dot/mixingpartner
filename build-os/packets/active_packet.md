# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-014
- **Title:** Near-tie-creative-FLIP fixture — the P-012 nudge DOES flip the winner through `analyze()` (within the ±2.0 cap)

## Scope (the builder implements EXACTLY this)

**Test-only.** Add a fixture that demonstrates the OTHER half of the P-012 nudge
posture: a genuine **near-tie** creative case where the bounded nudge, firing
through the live `analyze()` production path, **flips the creative winner**
within the `CREATIVE_NUDGE_CAP = ±2.0` bound. This is the natural complement to
P-013's option-(a) "fires-but-cannot-overturn-a-clear-ranking" — it proves the
nudge is not only *armed and transparent* but *decisive when the ranking is
genuinely close*, exactly as designed. **No product / runtime code touched —
`tests/` (and, if needed, a new tests-local fixture-data dir) only.**

What the fixture must establish, asserted on the value governance ranks on
(`overall_score`) through the real `analyze()` path — NOT on hand-built objects:

1. Two creative variants whose curated base `overall_score` gap is **< 2×cap
   (< 4.0)** so a bounded penalty *can* reorder them, with the nudge-penalized
   kind (`width_bloom` under `width_crowding`, or a masked-vocal kind under
   `bad_masking`) as the **narrow base leader**.
2. The masking/width condition **actually fires** through `analyze()` (a real
   event in the masking report — no monkeypatching the nudge in).
3. With the nudge ARMED, the penalized leader drops **below** the runner-up →
   `winning_variant` / `governed_winner` **flips** to the runner-up.
4. The movement stays **within the ±2.0 cap** (the flip is caused by a *bounded*
   nudge breaking a *near-tie*, never by an unbounded swing).
5. A **negative control is load-bearing**: with the nudge disarmed (or absent),
   the winner stays the base leader — i.e. the flip is genuinely caused by the
   nudge, not a tautology. Make this explicit in the assertions (a layer-ON vs
   layer-OFF contrast, mirroring P-013's non-tautology discipline).

### Builder latitude / honesty clause
A genuine near-tie flip may require a **new minimal synthetic fixture** (seeded
stems + manifest under `tests/`) engineered so the penalized kind narrowly leads
*and* its masking condition fires. That is in scope (tests-only). **If — after a
real attempt — a flip is structurally unreachable test-only without changing
product code** (e.g. curated `_KIND_SCORES` never lets `width_bloom` lead by a
sub-cap margin while `width_crowding` fires), **do NOT touch product code**:
report it with the same evidence rigor P-013 applied to Fixture #2, and it
becomes a recorded finding (and, if it implies a product-code aesthetic change,
a user-gated packet) rather than a forced result.

Fixtures must use **fake adapters only** — no real DAW / Logic / AppleScript /
subprocess / `.logicx` write / network.

## Constraints

- **≤2 commits** (likely 1: a single tests-only commit; a 2nd reserved if a
  new fixture-data dir + the test split cleanly). **Commit-1 green in isolation.**
- The variant-scoring path is **golden-unguarded** (regression reads
  `doctrine_score`, never `score_variant`) — so this fixture is a *binding*
  guard, not the golden. Assert on real produced values.
- **No external mutation** — no push / merge / deploy / secret. Stop at any such
  boundary for explicit go. (Standing push-go covers commits to the dev branch
  only.)

## Expected proof (qa to report exact)

- Suite **207 → ~209–212 passed** (0 failed / skipped / warnings); exact count
  at close.
- Regression **68/68, 0 critical** held.
- Commit-1 green in isolation; new test(s) alone green.
- Safety grep clean (no real DAW / Logic / AppleScript / subprocess / network /
  `.logicx` write).
- Non-tautology: the layer-OFF negative control must change the asserted winner
  (flip present with nudge ON, absent with nudge OFF).

---
_Confirmed as active by the orchestrator-in-chief (P-014), 2026-06-30. One packet
at a time._
