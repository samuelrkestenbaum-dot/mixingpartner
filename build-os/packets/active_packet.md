# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-036 confirmed by the orchestrator-in-chief on the
  USER'S GO (2026-07-02, "Both" = merge PR #18 ✓ + this packet). Handed to
  builder.
- **Packet id:** P-036
- **Title:** re-author the stale vocal-blend confidence entries — the honesty
  layer catches up with P-035's reality.

## Why (the P-035 reviewer's queue-jump recommendation)

Both profiles' `confidence_map` "limited — vocal blend interpretation" entries
still claim: the analyzer "emits vocal-band events only against the lead
today" and the policy is "mechanically live but dormant on real exported-stem
data." **Both halves are now FALSE** — P-034 delivered non-lead vocal-band
events, P-035 made the blend differential live and measured on real audio
(65.0 vs 85.0 on `vocal_chop_groove`). No scorer consumes the map (contained),
but the product's brand is honest labeling: its own labels are corrected first.

## Spec (small packet — labeling only, never judgment)

1. **Re-author the vocal-blend entry in BOTH profiles**
   (`doctrine/producers/halee_ramone.json` + `timbaland.json`):
   - Rewrite the `reason` to the LIVE status: the analyzer emits non-lead
     vocal-band events (`vocal_band_masking`); the blend policy is live and
     measured on real fixture data; state each profile's own stance in its own
     voice (the reference protects clarity / declines blend; timbaland accepts
     qualified blend — measured).
   - **Re-judge the `level` honestly per profile:** assess whether `limited`
     still fits or the entry is now `high` (the interpretation is live,
     hand-curated, and measured — but consider what remains genuinely limited:
     e.g. the moderate tier reachable only via the either-side-forward reading;
     the info tier unconsumed; coverage limited to the masker-instrument set).
     Pick per profile, justify in the reason, observational wording.
2. **Flip the verbatim map pins consciously** — `TIM_AUTHORED_MAP`
   (tests/test_timbaland_profile.py) and halee_ramone's AUTHORED_MAP
   (tests/test_confidence_map.py): exactly the changed entries, the pins'
   designed conscious-edit path, nothing else in the maps touched, no
   assertion weakened.
3. **BYTE-IDENTITY everywhere else:** the maps render into `doctrine_score.json`
   + the verdict markdown on EVERY fixture — so the rendered confidence
   section changes are the ONLY artifact deltas allowed (the changed entries'
   text), on all 4 fixtures × both producers; every score/variant/promotion/
   recommendation numerically identical; regression **93/93** (the golden
   snapshots pin scores/categoricals, not confidence text — verify, don't
   assume).

## Tests

1. The updated pins (verbatim, both files).
2. Byte-identity of all score surfaces (4 fixtures × 2 producers) + regression
   93/93.
3. The artifact delta audit: base vs HEAD artifact trees — ONLY the confidence
   section/key text moves, nothing else.
4. The honesty machine-checks still hold (high claims vs weights; the P-031
   idiom) — if an entry moves to `high`, the machine-check must cover it or be
   consciously extended.
5. Observational language on the new reasons.

## Rigor bar (established)

- `python fixtures/generate_fixtures.py` FIRST (4 fixtures); **≤2 commits,
  Commit-1 green in isolation**; full suite green from the **754** baseline;
  regression **93/93**; observational language; trailers
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the Claude-Session
  link; NO push/merge/remotes (orchestrator pushes). Anything beyond the two
  entries + pins + proofs: STOP and report.

## Last-closed / context

- **PR #18 MERGED** — post-epic hardening (P-033, P-030, P-034, P-035) is on
  default; merge commit `dc921ec` = the new default tip and this branch's
  restart base + THE NEW MERGE BASE for landing decisions. Suite 754;
  regression 93/93; the analyzer-extension arc complete.

## Backlog after

- The residue sweeps (the three producer-named-VALUE surfaces,
  `logic_action_generator.py:38`, validation tightening, liveness docstrings,
  `cli.py` `--mode` text, the P-035 count-pin parenthetical tidy — see
  `build-os/memory/residue.md`).

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
