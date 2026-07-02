# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-033 confirmed by the orchestrator-in-chief
  (2026-07-02) on the user's explicit go, handed to builder.
- **Packet id:** P-033
- **Title:** wire `_default_creative_mode` to the producer profile — make the
  authored creative-mode table a REAL product lever; byte-identical for the
  reference.
- **Numbering note:** next free packet number. (An old roadmap idea once
  tentatively labeled P-033 — "expose producer selection on CLI surface" — was
  never confirmed and is superseded: selection is live via
  `analyze(producer=…)`; any CLI exposure remains unstaged backlog.)

## Why this packet (user-stated: the puck)

The sub-arc proved the producer lever end-to-end EXCEPT one wire: the profile
field `default_creative_mode` (required since P-025, authored by BOTH profiles)
is **pipeline-inert** — `pipeline._default_creative_mode` (pipeline.py:285-290)
hardcodes the REFERENCE's mode names, so Timbaland's authored
`intimate_mode: "conservative"` is unreachable and intimate material under
timbaland silently falls back to `"dramatic_contrast"` (creative.py:516-517).
This packet makes the second producer FEEL real: authored mode → reachable
mode. (Found by the P-032h reviewer; pre-registered in P-032i's negative pin
as THE packet that legitimately changes it.)

## Spec (build exactly this)

1. **Wire it per-call (the P-029 pattern):** `_default_creative_mode` reads the
   PASSED profile's `default_creative_mode` table (profile or `_DEFAULT_PROFILE`
   when None) instead of the hardcoded name map. The reference's declared table
   values coincide with today's hardcoded strings (why the inertness was
   invisible) → the reference path stays BYTE-IDENTICAL by construction — prove
   it, don't assume it.
2. **Close the KeyError risk (creative.py:532):** when a resolved mode name is
   absent from the profile's `search_modes`, do NOT dereference blindly and do
   NOT hardcode `"dramatic_contrast"` — fall back to a mode the profile
   ACTUALLY HAS (deterministic, documented rule; observational language), and
   surface the fallback in evidence/output where the mode is already reported.
3. **Update the pre-registered pins via the conscious-edit path** (each was
   written naming THIS packet as its legitimate breaker — update, never weaken):
   - `tests/test_differential_proof.py` — the intimate-mode-inertness negative
     pin (now: timbaland's authored mode IS reachable); the search-mode pins
     and `EXPECTED_SNAPSHOT` wherever timbaland's resolved mode changes.
   - `tests/test_timbaland_profile.py` (~:430-433) — the honestly-pinned
     fallback behavior (now the authored behavior).
   Report EVERY pin changed, old → new, with the receipt noting each.

## Tests (test-first — the binding guards)

1. **Byte-identical (reference):** doctrine + creative + artifact surfaces
   unchanged on all 3 fixtures (73.8/70.7/74.3); regression 68/68. The
   reference's mode selection provably identical pre/post wiring.
2. **Liveness (the P-016 lesson — end-to-end, not unit):** a REAL `analyze()`
   under timbaland with intimate-truth intent selects timbaland's authored
   `"conservative"` (not the fallback); sabotage (re-hardcode the map / drop
   the profile read) FAILS liveness while reference byte-identity stays green.
3. **Fallback safety:** a synthetic profile whose table maps to a mode name
   missing from its `search_modes` → no KeyError; the documented fallback rule
   applies; observational evidence.
4. **Per-call threading:** a passed profile's table is consulted, never the
   module default's (sabotage-guarded).
5. **No-aliasing:** reads only; `_DEFAULT_PROFILE` untouched after runs.

## Rigor bar (established)

- `python fixtures/generate_fixtures.py` FIRST; **≤2 commits, Commit-1 green in
  isolation**; full suite green from the **660** baseline; regression 68/68;
  observational language; commit trailers `Co-Authored-By: Claude Fable 5
  <noreply@anthropic.com>` + the Claude-Session link; NO push/merge/remotes
  (orchestrator pushes). If anything beyond the wiring + fallback + pins needs
  touching, STOP and report.

## Last-closed / context

- **PR #17 MERGED** — the producer-agnostic epic is on default (merge commit
  `58d21dd`, the new default tip and this branch's restart base). Suite 660;
  68/68; reference 73.8/70.7/74.3; sub-arc complete (10 packets).

## Epic arc (post-merge backlog order, user-confirmed)

**P-033 (default_creative_mode wiring — ACTIVE) →** P-030 (rename halee/ramone
dims; touches 2 producer JSONs + test_differential_proof.py) → analyzer
extension (non-lead vocal-band events + creative.py:98 fix) →
verdict-filename cosmetic → residue sweeps.

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
