# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-034 confirmed by the orchestrator-in-chief on the
  USER'S GO (2026-07-02, "Do it" = Option A, two packets). Handed to builder.
- **Packet id:** P-034
- **Title:** analyzer capacity — emit non-lead vocal-band masking events
  (NEW classification, consumed only by the vocal-role surface) + the
  `creative.py` lead-masked name-match fix. Fixture-inert; byte-identical
  everywhere.

## The two-packet plan (user-approved)

- **P-034 (THIS):** the analyzer emits non-lead vocal-band events with a NEW
  classification; `_vocal_role_fit` + the blend gate consume it; the
  `creative.py:98` name-based "vocal" match is fixed. All 3 current fixtures
  have NO non-lead vocal stems → zero new events on real data → byte-identical
  on every surface; 68/68 holds; the P-032i no-vocal-blend-delta pin does NOT
  flip here.
- **P-035 (STAGED):** a 4th fixture (`vocal_chop_groove`-style: lead + chopped
  vocal + backing stack + beat) + its golden + the CONSCIOUS pin flips + the
  real-data vocal-blend differential proof. The regression count moves off
  68/68 there, consciously.

## The pre-registered surface map (binding)

- **NEW classification `vocal_band_masking`** — emitted for a NON-LEAD vocal
  stem masked by a forward/heard element. The LEAD is NEVER in these events
  (lead-inclusive vocal masking stays `_vocal_conflict`'s `bad_masking`
  pathway, untouched).
- **Consumers that move:** the masking_report artifact (new events, when they
  exist); `_vocal_role_fit`'s non-lead pathway (now keys on the NEW
  classification; the reference reads it observationally, a qualified
  chop/stack under an opted-in profile may blend); the blend gate.
- **Consumers pinned IMMOVABLE (each filters by specific classification):**
  `_emotional_hierarchy` + `_vocal_centrality` (lead-inclusive events only),
  `_static_mix` (low_end_conflict only), the planners/action-generators
  (`bad_masking` only — the new classification must NOT generate actions in
  this packet), `_beat_identity`/`_loop_context` (bad_masking reads —
  unaffected by the new classification), golden snapshots (no fixture emits
  the new events).

## Spec (build exactly this)

1. **`masking_analyzer.py`:** for each non-lead VOCAL stem (identity
   `backing_vocal` OR a non-None `vocal_type` record field, excluding the
   lead), when it sits forward/heard, check vocal-presence overlap against the
   same forward harmonic/melodic instrument set `_vocal_conflict` uses (an
   honest mirror of the lead pathway): emit `vocal_band_masking` events —
   elements `[vocal_stem, other]`, severity `moderate`/`info` by overlap
   (mirror the existing thresholds), observational reason/recommendation
   wording (the recommendation must be philosophy-NEUTRAL: report the overlap;
   do not prescribe "fix it" — the profile decides what masking of this class
   means). Update the summary counts honestly (the new classification counted;
   do not inflate `critical_count` — cap severity at moderate in this packet).
2. **`_vocal_role_fit` + the blend gate:** the non-lead pathway keys on
   `vocal_band_masking` (the synthetic-event tests from P-032f update via the
   conscious-edit path — they currently construct lead-free `bad_masking`
   events; they now construct the honest classification). The lead pathway
   (bad_masking) untouched.
3. **`creative.py` `_lead_masked` fix:** replace the name-based
   `"vocal" in element` match with an identity-derived lead-name check, so the
   new non-lead events can never falsely trigger the lead-masked gate. Prove
   both directions: a lead-free vocal-named event does NOT trigger it; a
   genuine lead event still does.

## Tests (test-first — new `tests/test_vocal_band_masking.py` + conscious pin updates)

1. **Emission unit tests:** synthetic records — backing/chop vocal forward +
   forward heard synth with overlap → `vocal_band_masking` event, correct
   elements (lead absent), severity mapping, observational wording; below
   overlap floor → no event; vocal stem NOT forward → no event (or the honest
   info reading — builder's call, documented); the lead itself NEVER generates
   the new classification.
2. **Byte-identity:** all 3 fixtures × both producers — every surface
   (doctrine + creative + artifacts incl. masking_report) unchanged; 68/68.
3. **Consumption:** `_vocal_role_fit` reads the new classification (reference:
   observational reduced-fit; timbaland + qualified chop/stack + above floor:
   accepted blend) — the P-032f synthetic tests updated to the new
   classification, strength held.
4. **The creative.py fix:** both directions per spec item 3; the P-032g/f
   masked-lead override tests still pass untouched.
5. **Immovability pins:** a synthetic `vocal_band_masking` event does NOT
   change `_emotional_hierarchy`/`_vocal_centrality`/`_static_mix` readings and
   generates NO plan actions.
6. **No-aliasing + observational language** (the established guards).

## Rigor bar (established)

- `python fixtures/generate_fixtures.py` FIRST; **≤2 commits, Commit-1 green in
  isolation**; full suite green from the **705** baseline; regression **68/68**
  (unchanged goldens — this packet is fixture-inert); observational language;
  trailers `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link; NO push/merge/remotes (orchestrator pushes). Anything
  beyond the analyzer + consumption + fix + pins: STOP and report.

## Last-closed

- **P-030 ✓ CLOSED** — the artifact-contract migration; the health bar held
  (90/90 values identical; pure key rename). Suite 705 / 68/68 vs regenerated
  goldens. Pushed, not merged (merge base `58d21dd` = PR #17).

## Epic arc (post-merge backlog)

**P-033 ✓ → P-030 ✓ → P-034 (analyzer capacity — ACTIVE) → P-035 (the 4th
fixture + real-data blend differential — STAGED) →** the residue sweeps (incl.
the three producer-named-VALUE surfaces).

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
