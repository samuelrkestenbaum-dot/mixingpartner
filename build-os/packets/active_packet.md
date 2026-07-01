# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-017
- **Title:** Minimal doctrine-honest `_KIND_SCORES` re-curation — the depth/hierarchy move wins the `density` problem (FIRST base-value change)

## Authority

**PRODUCT-CODE aesthetic change to the CURATED JUDGMENT ITSELF — user-signed-off
(the user chose "A").** This is the FIRST change to a base `_KIND_SCORES` value —
crossing the line P-012/P-015/P-016 deliberately held (they layered bounded
evidence nudges on an UNTOUCHED base). The variant-scoring path is
**golden-unguarded** (regression reads `doctrine_score`, never `score_variant`)
→ **unit tests are the binding guard.** **Merge to default stays gated on the
user's explicit go; dev-branch commits are covered by standing push-go.**

## Doctrine anchor

`masking_is_hierarchy` + `anti_template`: a density/crowding problem is
fundamentally a HIERARCHY problem, and `depth_cleanup` ("push supporting elements
to midground so the foreground breathes; reserve the widest placement for one
element") is THE hierarchy move — vs `subtractive_drop` ("remove a duplicate
midrange element entirely"), the generic deletion move. By default
`subtractive_drop` (85.3) wins `density` over `depth_cleanup` (81.1) by 4.14, and
still wins 3 branches by default (chorus_lift + density + loop-default) — the
`anti_template` "formulaic / vary the move per problem" pattern. Letting the
depth move win the density problem relieves that and honors `masking_is_hierarchy`.

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/creative.py`, `_KIND_SCORES["depth_cleanup"]` ONLY
Re-curate `depth_cleanup`'s base dims so the depth/hierarchy move wins the
`density` branch — but ONLY with **doctrine-honest** values:

- **HONESTY CONSTRAINT (load-bearing):** every changed dim must be defensible as a
  genuine re-judgment of `depth_cleanup`'s character, with a one-line doctrinal
  rationale in a comment. Do NOT inflate a dim merely to cross the win threshold.
  - The clearest honest under-valuation: **`contrast` (currently 72)** — creating
    depth (foreground/midground/background separation) IS perceptual contrast;
    depth_cleanup is under-valued vs `subtractive_drop`'s 88 here, and
    `masking_is_hierarchy` + `section_contrast_considered` back it. Reconsider
    `contrast` first.
  - **`excitement` (66) is OFF-LIMITS to inflate** — subtle depth work is honestly
    un-flashy; raising it to force a win would be dishonest. Leave it unless you
    have a genuine doctrinal reason (state it).
  - `halee` (90, already max) and `taste` (85) are correctly valued — do not touch
    without rationale.
- Change the MINIMAL set of dims needed, each documented. `subtractive_drop` and
  every OTHER kind stay UNTOUCHED. The penalty layer, the promotion layer
  (`_PROMOTION_TABLE`, `CREATIVE_PROMOTION_CAP`), and both caps stay UNTOUCHED.

### HONESTY CLAUSE (P-014 discipline — the primary guard)
`depth_cleanup` trails by **4.14**. If the minimal set of **doctrine-honest** dim
re-judgments does NOT lift its overall above `subtractive_drop`'s 85.29 — i.e. the
only way to flip `density` is to inflate values beyond doctrinal defensibility —
then **STOP and report it as a FINDING**: "an honest re-curation narrows but
cannot flip the `density` branch; the curated values legitimately edge the depth
move for this problem." Do NOT force the flip with dishonest values. A
well-evidenced "the current values are defensible" is an ACCEPTABLE, valuable
outcome (like P-014). Report the before/after overalls either way.

### Collateral discipline
`depth_cleanup` competes in `density` [depth_cleanup, subtractive_drop] and
`depth` [depth_cleanup alone]. Raising it can only change the `density` winner
(the `depth` branch is single-variant). Verify NO other branch's winner moves.

### Test change — the BINDING guard (golden-unguarded path)
Prefer a new `tests/test_density_recuration.py` (or extend an existing creative
test), driven through the REAL `analyze()`/`score_variant` path:
- **Before/after winner table for ALL 5 branches** pinned as assertions (chorus_lift,
  density, loop-default, depth, vocal_belief) — proving ONLY `density` changes (if
  the flip is honest) or that NOTHING changes (if reported as a finding).
- If the flip is achieved: `density` winner is `depth_cleanup` (density_A) on the
  real path; a load-bearing assertion that this is caused by the re-curation
  (e.g. the exact new overall vs the old).
- Collateral safety: chorus_lift/loop-default/depth/vocal_belief winners unchanged;
  P-012/P-013/P-015/P-016 test files pass UNCHANGED (do not edit them).
- Regression `loops_not_foregrounded` and all doctrine invariants still hold.

Fake adapters only — no real DAW / Logic / AppleScript / subprocess / `.logicx`
write / network.

## Constraints

- **≤2 commits.** If the re-curation flips a default winner, **Commit-1 must
  bundle the value change + its tests so Commit-1 is green in isolation** (P-015
  pattern). No live-wire needed (density has no separate evidence gate — this is a
  base-value change, not an evidence nudge).
- **No external mutation** — no push / merge / deploy / secret. Stop at any such
  boundary. (Standing push-go covers dev-branch commits only.)
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite green under `-W error` (report before→after; was 228).
- Regression **68/68, 0 critical, 0 warnings** held.
- Commit-1 green in isolation.
- Safety grep clean.
- The before/after winner table (all 5 branches). Either: `density` flips to
  `depth_cleanup` with ONLY that branch changing and the new values documented as
  doctrine-honest; OR the honest-re-curation FINDING (no flip, values defensible).
  Reviewer judges whether the changed values are doctrine-HONEST or inflated —
  that judgment is the crux of this packet.

---
_Confirmed as active by the orchestrator-in-chief (P-017), on the user's "A" go
+ the build-orchestrator's routing. One packet at a time._
