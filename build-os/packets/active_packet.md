# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-026
- **Title:** Source `creative.py`'s producer-specific values from the reference profile (byte-identical, single-source-of-truth)

## Why (producer-agnostic epic — first wiring step)

P-025 extracted the reference `ProducerProfile` (`halee_ramone.json`) and proved
byte-identical round-trip, but nothing consumes it. P-026 makes `creative.py`
SOURCE its producer-specific values FROM `load_profile("halee_ramone")` instead of
hardcoded literals — the JSON becomes the single source of truth. Byte-identical
by construction (the reference profile == today's literals, guarded by P-025's
round-trip + the 68/68 regression). **No per-call producer selection yet** — that
is P-029; here we only relocate the source of the values. Extract, don't change.

## Authority

**Build / feature — in authority, byte-identical.** No new decision. **Merge to
default gated on explicit go; dev-branch commits under standing push-go.**

## Scope (the builder implements EXACTLY this)

### Product change — `logic_mix_os/creative.py`
1. Add a module-level `_DEFAULT_PROFILE = load_profile("halee_ramone")` (imported
   once from `doctrine.producer_profile`).
2. **Source the producer-specific module globals FROM the profile** — replace the
   hardcoded literals with values read off `_DEFAULT_PROFILE`, keeping the SAME
   global names/shapes so downstream code is untouched:
   - `_KIND_SCORES = _DEFAULT_PROFILE.kind_scores`
   - `_NUDGE_TABLE = _DEFAULT_PROFILE.nudge_table`
   - `_PROMOTION_TABLE = _DEFAULT_PROFILE.promotion_table`
   - `CREATIVE_NUDGE_CAP = _DEFAULT_PROFILE.creative_nudge_cap`
   - `CREATIVE_PROMOTION_CAP = _DEFAULT_PROFILE.creative_promotion_cap`
   - `_RISK_PENALTY = _DEFAULT_PROFILE.risk_penalty`
   - `SEARCH_MODES = _DEFAULT_PROFILE.search_modes`
   - `PHILOSOPHY = _DEFAULT_PROFILE.philosophy`
   - The old hardcoded literals are DELETED (the JSON is now their home). If any
     downstream code mutates these globals in place, keep them as fresh copies (the
     loader already returns fresh collections) — do NOT alias into the frozen
     profile's internals.
3. **Do NOT change any function SIGNATURE** and do NOT thread a per-call profile
   yet (that's P-029). Do NOT touch `governance.py`/`doctrine_engine.py`/
   `pipeline.py` (P-027/P-028/P-029 own those). The variant KINDS, the scoring
   MECHANISM, and every algorithm stay byte-identical.

### Import-time note
`_DEFAULT_PROFILE` loads JSON at import — a local, deterministic, package-relative
read. If the profile file is missing/corrupt, import SHOULD fail loudly (the JSON
is now the source of truth; that's correct). Ensure the loader resolves the
package path robustly (P-025's loader already does).

### Tests — the binding guard (golden-unguarded variant path). Test-first.
- **Byte-identical proof:** the module globals AFTER sourcing from the profile
  equal the pre-P-026 hardcoded values. Since the literals are being removed,
  pin the expected values in the test (e.g. assert `_KIND_SCORES["width_bloom"]
  ["halee"] == 78`, the caps == 2.0/4.0, a nudge-table row, etc.) so a future
  profile-JSON edit that changes them is caught. (P-025's round-trip test already
  pins `profile == globals`; keep it green — update it if the globals are now
  literally the profile's objects.)
- **Behavior byte-identical:** `score_variant` / creative outputs on the seeded
  fixtures are unchanged vs pre-P-026 (the golden-unguarded path — assert on real
  `analyze()`/`score_variant` output; the P-012/13/15/16 creative tests must pass
  UNCHANGED, proving byte-identical scoring).
- Determinism preserved.

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network.

## Constraints

- **≤2 commits.** Commit-1 (green in isolation): source globals from the profile +
  byte-identical tests. Commit-2 reserved.
- **Byte-identical** — if any creative output changes, STOP and report (the round-
  trip/extraction was wrong). No behavior change is the whole point.
- **No external mutation.** Author/committer `Claude <noreply@anthropic.com>`;
  trailers required; NO model identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **319 → 319±N passed** (0 failed/skipped/warnings, green under
  `-W error`) — existing creative tests (P-012/13/15/16) pass UNCHANGED (byte-
  identical scoring).
- Regression **68/68, 0 critical, 0 warnings** held (creative feeds
  `doctrine_score`? No — variant path is golden-unguarded; but regression must
  still be 68/68 since behavior is identical).
- Commit-1 green in isolation.
- **Byte-identical creative output proven** (globals sourced from profile ==
  old literals; `score_variant` outputs unchanged on fixtures). The single source
  of truth is now the JSON; `governance.py`/`doctrine_engine.py`/`pipeline.py`
  untouched. Safety grep clean; UI N/A.

---
_Confirmed as active by the orchestrator-in-chief (P-026), first wiring step of
the producer-agnostic epic. One packet at a time._
