# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-037 confirmed by the orchestrator-in-chief on the
  USER'S GO (2026-07-02, "Go for it" = sweep the residue). Handed to builder.
- **Packet id:** P-037
- **Title:** residue sweep 1 of 2 — the CODE-BEHAVIOR sweep (defensive fixes +
  validation tightening); byte-identical on every artifact surface.

## Scope (each item small, together one packet; ALL from residue.md)

1. **`logic_action_generator.py:38`** — replace the name-based
   `"vocal" in el.lower()` substring match with the identity-derived lead-name
   check (the same fix creative.py:98 got in P-034; reuse/mirror that
   implementation — shared basis where practical). Unreachable-today by the
   classification gate, but the smell goes.
2. **Validation tightening in `producer_profile.py` `_validate`:**
   - `search_modes` must be non-empty (closes the StopIteration path in
     `_profile_default_mode`);
   - `default_creative_mode` structural check — the three keys the pipeline
     hard-dereferences (`intimate_truth_words` / `intimate_mode` /
     `default_mode`) present with sane types;
   - `confidence_map`: reject duplicate `area` strings and unknown extra keys
     in entries (the P-031 reviewer judgment notes — tightening, now
     conscious);
   - `vocal_blend_policy.confidence_floor`: reject non-finite (NaN/inf) —
     belt to the existing range check.
3. **The raw-gate NaN self-guard** — `accepted_blend_under_policy` guards
   `0.0 <= floor <= 1.0` (and finiteness) before the comparison (qa's P-032f
   note: unreachable via validated loads, cheap defense for raw dicts).
4. **`lead_names` derivation in `_vocal_role_fit`** — derive from
   `instrument_identity == "lead_vocal"` rather than `vocal_type` (the P-032f
   reviewer note: removes the one hand-mangle-able link; identical results on
   all pipeline data — prove byte-identity).
5. **The shared groove dict defensive copy** — `expanded["groove"]` gets a
   fresh copy (or a read-only test pin — builder's call, documented) so a
   future doctrine mutation cannot silently corrupt the expanded artifact
   (the P-032b skeptic's cosmetic note). Byte-identical output.
6. **`JUDGMENT_WORDS` word-boundary matching** — the guard matches whole words
   (regex `\b`) instead of substrings, freeing "fixture" et al. for profile
   prose; verify every existing guard use still passes and the guard still
   catches the actual judgment words (add a case proving "fixture" no longer
   trips it and "fix" still does).

## The bar

- **Byte-identical on EVERY artifact surface** (4 fixtures × 2 producers) —
  these are defensive/validation changes; no emitted byte may move. Suite
  green from the **754** baseline (new validation tests grow it); regression
  **93/93**.
- New validation rejections need tests (each malformed shape → ValueError);
  both shipped profiles must still load (they are well-formed — verify).
- ≤2 commits, Commit-1 green in isolation; `python fixtures/generate_fixtures.py`
  FIRST; observational language; trailers
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + the
  Claude-Session link; NO push/merge/remotes.
- Anything beyond these six items: STOP and report. (The prose/naming items —
  docstrings, cli help text, the producer-named VALUES, the count-pin
  parentheticals, the P-036 observations — are P-038's, NOT this packet's.)

## Last-closed / context

- **P-036 ✓ CLOSED** — the honesty layer current. One packet on the branch atop
  merge base `dc921ec` (= PR #18). Suite 754 / 93/93.

## Backlog after

- **P-038 — residue sweep 2 of 2 (naming/prose):** the three producer-named-
  VALUE surfaces (scoped with care — search-mode names appear in emitted
  creative.json; warning doctrine tags may be golden-pinned), the
  liveness-docstring sweep, cli.py --mode text, the count-pin parenthetical
  tidy, fallback-reason wording, the two P-036 observations. Then the batch
  merge decision (P-036 + P-037 + P-038) on the user's word.

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
