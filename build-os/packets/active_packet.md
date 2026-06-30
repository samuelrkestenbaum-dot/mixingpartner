# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-015
- **Title:** Make the masked-vocal nudge DECISIVE — row-0 exempts intimacy_pass + strengthens to the cap (USER-SIGNED-OFF aesthetic change)

## Authority

**PRODUCT-CODE aesthetic change to default recommendations — explicitly
user-gated, and the user gave explicit go (chose "Option 1 — Proceed,
corrected" on 2026-06-30).** This is the deliberate, signed-off successor to
P-012: it changes the default creative winner on a masked-lead-vocal near-tie.
The variant-scoring path is **golden-unguarded** (regression reads
`doctrine_score`, never `score_variant`), so the **unit tests are the binding
guard** — they must be updated AND extended, not just kept green.

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/creative.py`, `_NUDGE_TABLE` row-0 only
Row-0 is the `lead_masked` (`bad_masking` with a vocal element) condition. Make
exactly TWO edits to it, and keep everything else (row-1, `_KIND_SCORES`, the
cap, the clamp, the predicates, every other kind) UNTOUCHED:

1. **Exempt `intimacy_pass`:** `kinds` `{"width_bloom", "vocal_ride",
   "intimacy_pass"}` → `{"width_bloom", "vocal_ride"}`.
2. **Strengthen the penalty:** `delta` `-8` → `-14` (which maps to an overall
   delta of `-14/7 = -2.0` — i.e. it lands EXACTLY on the existing
   `CREATIVE_NUDGE_CAP = 2.0`; the cap is unchanged and still binds).
3. **Honest `reason` string** + a code comment. Update the row-0 reason so the
   number matches (`-14`) and the doctrine is accurate, e.g.:
   `"vocal_belief -14: lead vocal is masked (bad_masking) — pushing the vocal
   forward by level/width is risky here; bring it into intimate focus instead"`.
   Add a brief comment explaining WHY `intimacy_pass` is exempt: **an intimacy
   pass is the correct response to a masked lead vocal — it brings the vocal into
   focused proximity rather than shoving it forward by brute level/width — so it
   must NOT be penalized as a risky vocal-forward move.**
4. **Fix the now-stale clamp comment** near line 329 ("width_bloom rows 1+2 = -14
   raw = -2.0 overall"): with row-0 at −14, width_bloom under BOTH rows is −20 raw
   (still clamped to −2.0 overall); vocal_ride under row-0 alone is now −14 raw =
   −2.0 overall. Keep the comment accurate to the new numbers.

**Doctrine / behavior intended (the exact, verified arithmetic):** in the
`vocal_belief` branch under a masked lead vocal, `vocal_ride` (base 82.9) drops
to the cap → **80.9**, while `intimacy_pass` (base 81.1, now exempt) is unchanged
→ **the winner FLIPS from `vocal_ride` (vocal_A) to `intimacy_pass` (vocal_B)** by
0.2. Bounded: cap stays ±2.0; this only breaks a genuine sub-cap near-tie (gap
1.71 < 2×cap) and can NEVER overturn a clear ranking (`subtractive_drop` 85.3
still wins every branch it competes in).

### Test change — the BINDING guard (golden-unguarded path)
5. **Update existing P-012 unit tests** (`tests/test_creative_nudges.py`, ~43
   cases) that encode the OLD behavior, to the NEW behavior — do NOT delete
   coverage, update intent with clear comments:
   - assertions that `intimacy_pass` is penalized under `lead_masked` → now
     assert `intimacy_pass` receives **no** nudge under `lead_masked`;
   - assertions pinned to delta `-8` / the old reason string → now `-14` / new
     reason;
   - keep/strengthen the cap-binding assertions (width_bloom still clamps to
     −2.0; vocal_ride now clamps to −2.0 under `lead_masked`).
6. **Add the decisive-flip proof** (new, the binding evidence for P-015), driven
   through the real path (`analyze()` and/or `score_variant` on a real
   `lead_masked` result), asserting on the value governance ranks on
   (`overall_score` / `winning_variant`):
   - **Flip:** with `lead_masked` true, the `vocal_belief` branch winner is
     `intimacy_pass` (vocal_B), and `vocal_ride` carries the `-14`
     `score_nudges` evidence line and sits at the cap (80.9).
   - **Load-bearing negative control:** with `lead_masked` FALSE (no masked-vocal
     event), the winner is `vocal_ride` (vocal_A) — proving the flip is caused by
     the masking evidence, not a base re-rank.
   - **Bounded — no clear-ranking overturn:** assert the cap is still ±2.0 and a
     clear-ranking branch (e.g. a `subtractive_drop` branch) does NOT flip under
     `lead_masked`.
7. **Collateral safety:** confirm NO other branch's winner changes — `chorus_lift`,
   `density`, `loop` still won by `subtractive_drop`; `depth` unchanged. The P-013
   visibility tests (`tests/test_creative_nudge_visibility.py`, chorus_lift /
   `width_crowding`) MUST still pass unchanged — verify, don't edit them.

Fake adapters only — no real DAW / Logic / AppleScript / subprocess / `.logicx`
write / network.

## Constraints

- **≤2 commits.** Because the product change intentionally breaks old-behavior
  tests, **Commit-1 MUST include the product change + the updated/added tests
  together so Commit-1 is green in isolation** (a 2nd commit reserved only if the
  new flip-fixtures split cleanly from the table edit).
- **No external mutation** — no push / merge / deploy / secret. Stop at any such
  boundary. (Standing push-go covers commits to the dev branch only; NOT a merge
  into the protected default.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Suite **207 → ~210–214 passed** (0 failed / skipped / warnings); exact at close.
- Regression **68/68, 0 critical** held (doctrine golden — the change MUST NOT
  break any doctrine invariant).
- Commit-1 green in isolation.
- Safety grep clean.
- **Decisive-flip proven AND non-tautological:** the layer-OFF / no-`lead_masked`
  negative control must show `vocal_ride` winning, the layer-ON masked case must
  show `intimacy_pass` winning. **Cap binds** (vocal_ride overall_delta = −2.0
  exactly). **No collateral flips** (other branches' winners unchanged; P-013
  tests still green).

---
_Confirmed as active by the orchestrator-in-chief (P-015), 2026-06-30, on the
user's explicit "Option 1" go. One packet at a time._
