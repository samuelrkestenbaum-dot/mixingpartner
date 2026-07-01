# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-016
- **Title:** Evidence-gated problem-native promotion — `loop` branch (first REWARD nudge)

## Authority

**PRODUCT-CODE aesthetic change to a default recommendation — user-delegated.**
The user chose direction (A) "open the base-scoring decision space", recommended
fork (i) "evidence-gated", and delegated the decision to the orchestrator ("you
figure out what to do using ClaudeOrchestrator" / "keep skating"). The
build-orchestrator routed and recommended this exact packet. **This crosses the
penalty-only line P-012 deliberately held — it is the FIRST reward/promotion
nudge** — which is the load-bearing design shift, on record as user-delegated.
The variant-scoring path is **golden-unguarded** (regression reads
`doctrine_score`, never `score_variant`), so the **unit tests are the binding
guard**. **Merge to default stays gated on the user's explicit go; dev-branch
commits are covered by standing push-go.**

## Doctrine anchor (the system's OWN principle — not subjective taste)

`governance.py::anti_template` warns when the same move-kind wins ≥3 problems:
"The mix may start to feel formulaic. **Repeat doctrine, not presets — vary the
move per problem.**" `subtractive_drop` currently wins `chorus_lift` + `density`
+ `loop` = 3 branches — exactly that pattern. Letting the loop-specific move win
the loop problem WHEN a loop is genuinely foregrounded drops it to 2 (below the
threshold) and is backed by `loops_not_foregrounded`, `source_material_respected`,
and the kill-switch "never allow a stock loop to dominate the song identity."

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/creative.py`, additive promotion layer
Add a bounded, evidence-gated **promotion** nudge ON TOP of the untouched
`_KIND_SCORES`, mirroring how P-012/P-015 layered penalties on an untouched base:

1. **`CREATIVE_PROMOTION_CAP = 4.0`** (overall-axis, a SEPARATE constant from the
   ±2.0 penalty `CREATIVE_NUDGE_CAP`; clamp the summed promotion overall-delta to
   `+CREATIVE_PROMOTION_CAP` exactly as the penalty path clamps to
   `−CREATIVE_NUDGE_CAP`). Do NOT change `CREATIVE_NUDGE_CAP` or any penalty row.
2. A **promotion table/row** (pure, deterministic, fixed order): kind
   `loop_deconstruct`, evidence `foregrounded_loop`, a positive delta large
   enough that the clamped overall promotion is `+4.0`, and a verbatim evidence
   `reason` line (e.g. `"loop_promotion +4.0: a foregrounded/dominating loop —
   deconstruct it (source material respected), don't just accent it"`).
3. **Evidence predicate — REUSE the real existing signal, invent nothing, monkey-
   patch nothing:** fire only when `source_auditors` has flagged a
   `"foregrounded loop"` red_flag (source_auditors.py:191), corroborated by
   `provenance` `high_risk` (provenance.py). Add a pure predicate reading these
   off the real `result` (mirror `_lead_masked`/`_width_crowded`); wire it into
   the promotion evaluation. If the exact result-shape for these signals differs
   from expectation, adapt the predicate to the REAL shape — do not fabricate a
   field.
4. **Apply in `score_variant`** alongside the penalty path: fired promotions raise
   the curated dims / overall, the SUMMED promotion overall-delta clamped to
   `+CREATIVE_PROMOTION_CAP`, and the fired reason appended to `score_nudges`
   (same evidence-key discipline: present only when ≥1 nudge fired). The **penalty
   path stays byte-untouched**; promotion and penalty are independent and both
   bounded.

**Verified arithmetic (the intended behavior):** `loop_deconstruct` 81.857 vs
`subtractive_drop` 85.286 (gap 3.4286). With the `foregrounded_loop` evidence
present, `loop_deconstruct` + 4.0 = 85.857 > 85.286 → **`loop` branch winner
FLIPS `subtractive_drop` → `loop_deconstruct`** by 0.571. With NO such evidence,
`subtractive_drop` stays the default winner. Bounded: a +4.0 promotion cannot
overturn a gap ≥ 4.0, and `loop_deconstruct` only competes in the `loop` branch,
so nothing else can shift.

### Test change — the BINDING guard (golden-unguarded path)
Prefer a new `tests/test_loop_promotion.py` (or extend `tests/test_decisive_nudge.py`),
driven through the REAL `analyze()` path (build a result whose source audit yields
a foregrounded-loop red_flag — do NOT monkeypatch the nudge):
- **Flip:** with the foregrounded-loop evidence present, the `loop` branch
  `winning_variant`/`governed_winner` is `loop_deconstruct` (loop_A), and it
  carries the `loop_promotion` `score_nudges` line; the promotion overall-delta
  binds at exactly `+4.0`.
- **Load-bearing negative control:** with NO foregrounded-loop evidence, the
  `loop` winner is `subtractive_drop` (loop_B) — the flip is caused by the
  evidence, not a base re-rank.
- **Collateral safety:** NO other branch's winner changes (chorus_lift/density
  still `subtractive_drop`, vocal_belief per P-015, depth unchanged). P-013 and
  P-015 test files pass UNCHANGED (do not edit them).
- **Cap binds:** the promotion clamps at exactly `+CREATIVE_PROMOTION_CAP` (4.0).

Fake adapters only — no real DAW / Logic / AppleScript / subprocess / `.logicx`
write / network.

## Constraints

- **≤2 commits.** Because the change alters default-winner behavior, **Commit-1
  MUST bundle the promotion mechanism + its tests so Commit-1 is green in
  isolation.** A 2nd commit reserved for doctrine-comment/polish only if it keeps
  the suite green.
- **No external mutation** — no push / merge / deploy / secret. Stop at any such
  boundary. (Standing push-go covers dev-branch commits only, NOT a merge to the
  protected default.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **green, +N** (report exact before→after; was 217).
- Regression **68/68, 0 critical, 0 warnings** held (doctrine golden — must NOT
  break; note the `loops_not_foregrounded` invariant especially still holds).
- Commit-1 green in isolation.
- Safety grep clean.
- **Flip proven AND non-tautological:** the no-evidence negative control shows
  `subtractive_drop` winning `loop`; the evidence-present case shows
  `loop_deconstruct` winning. **Promotion cap binds at exactly +4.0.** **No
  collateral flips** (other branches unchanged; P-013/P-015 tests still green).
  Reviewer runs a mutation check (revert the promotion → flip test RED, negative
  control stays GREEN).

---
_Confirmed as active by the orchestrator-in-chief (P-016), on the user's
delegation + the build-orchestrator's routing. One packet at a time._
