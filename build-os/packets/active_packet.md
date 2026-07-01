# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-025
- **Title:** `ProducerProfile` schema + `load_profile()` + extracted `halee_ramone.json` reference (data + loader ONLY — no wiring)

## Why (the producer-agnostic epic — foundation step)

New epic: make the engine PRODUCER-AGNOSTIC — select any producer (Timbaland,
Quincy, Ramone, …) and the same stems get driven toward that producer's state.
The orchestrator's survey established: the producer-agnostic *physics* (analyzers,
safety kill-switches, the bounded-nudge mechanism, determinism/evidence contract,
the move-kind vocabulary) stays fixed; the producer-specific *judgment* becomes a
swappable **`ProducerProfile`**. Critically, that judgment is **100% hardcoded in
Python** today (the `roy_halee.json`/`phil_ramone.json` files are prose, never
read by the scorer) — so the reference profile must be **extracted from code**.

P-025 is the FOUNDATION: create the profile schema + loader + the reference
`halee_ramone.json` holding today's producer-specific values VERBATIM, with a
byte-identical round-trip guard — **without wiring anything to consume it yet**
(that is P-026→P-029). Extract, don't change.

## Authority

**Build / feature — in authority, no honesty-decision needed.** Data + loader
only; nothing consumes the profile, so behavior is trivially byte-identical. The
honesty/sourcing policy (hand-curated=high-confidence / derived=low-confidence /
LLM=draft-only) is **CONFIRMED by the user** and applies to authoring a SECOND
profile (P-031+), not to this extraction. **Merge to default gated on explicit
go; dev-branch commits under standing push-go.**

## Scope (the builder implements EXACTLY this)

### New: `logic_mix_os/doctrine/producer_profile.py` (schema + loader) + `logic_mix_os/doctrine/producers/halee_ramone.json` (reference data)
1. Define the **`ProducerProfile`** structure (a frozen/immutable view — dataclass
   or a validated dict) capturing EVERY producer-specific value the pipeline
   currently hardcodes. From the orchestrator survey, the profile must hold:
   - **creative.py:** `kind_scores` (the `_KIND_SCORES` 7 kinds × 9 dims — keep the
     `halee`/`ramone` dim NAMES verbatim for now, per the (2a) byte-identical-first
     decision), the `nudge_table` + `promotion_table` (rows) + `CREATIVE_NUDGE_CAP`
     + `CREATIVE_PROMOTION_CAP` + `_RISK_PENALTY`, the `search_modes`, the
     `PHILOSOPHY` string.
   - **governance.py:** `truth_alignment` (`_TRUTH_ALIGNMENT`), `taste_kind_bias`
     (`_TASTE_KIND_BIAS`) + `TASTE_MAX_DELTA`, and the **aesthetic** subset of
     `KILL_SWITCHES` (items 6–9 — "never chase reference loudness", "never widen
     full mix for chorus lift", "never make vocal less intelligible", "never let a
     stock loop dominate"). The **safety** kill-switches (items 1–5,
     non-destructive/Class-5) are PRODUCER-AGNOSTIC — do NOT put them in the
     profile; they stay universal.
   - **doctrine_engine.py:** the component-score weights (halee/ramone/vocal), the
     baselines (86.0), and the penalty coefficients currently hardcoded in
     `_halee`/`_ramone`.
   - Also capture the `_default_creative_mode` mapping (truth → mode) if it's
     producer-specific.
2. **Profile metadata (honesty scaffolding — set up now, consumed in P-031):** the
   profile JSON carries `{name: "halee_ramone", display_name, provenance:
   "hand-curated-documented", confidence: "high", risk_class: <appropriate>}`.
   This bakes in the provenance+confidence+risk stamp the confirmed honesty policy
   requires — even though nothing enforces/propagates it until P-031.
3. **`load_profile(name="halee_ramone")`** reads the JSON and returns the frozen
   `ProducerProfile`. Deterministic, pure, local file read only.
4. **DO NOT WIRE IT.** `creative.py`, `governance.py`, `doctrine_engine.py`,
   `pipeline.py` are UNCHANGED — they still use their hardcoded dicts. Nothing
   imports/consumes `load_profile` in the runtime path yet. This packet is data +
   loader + tests only.

### Tests — the binding guard. Test-first. New `tests/test_producer_profile.py`.
- **Byte-identical ROUND-TRIP (the load-bearing guard):** assert the extracted
  `halee_ramone.json`, loaded via `load_profile`, reconstructs each current
  module-level structure EXACTLY — `profile.kind_scores == creative._KIND_SCORES`,
  `profile.truth_alignment == governance._TRUTH_ALIGNMENT`, the nudge/promotion
  tables == the current tables, caps == current caps, doctrine weights/baselines ==
  the current `doctrine_engine` values, etc. This proves the extraction is
  faithful (no transcription error) and is the guard P-026→P-028 will rely on.
- **Extraction-completeness:** a test asserting every producer-specific structure
  named in this packet has a profile home (so a future new producer-specific
  constant can't be silently missed). Prove it's real (if a captured value drifts
  from its source dict, the round-trip test fails).
- **Schema validity + metadata:** `load_profile` validates the JSON against the
  schema; the metadata fields (name/provenance/confidence/risk_class) are present
  and typed; `confidence == "high"` and `provenance == "hand-curated-documented"`
  for the reference.
- Determinism: two `load_profile` calls return equal profiles.

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network. Pure JSON + local file read.

## Constraints

- **≤2 commits.** Commit-1 (test-first, green in isolation): schema + loader +
  `halee_ramone.json` + the round-trip-identity test. Commit-2:
  extraction-completeness + schema/metadata tests.
- **No pipeline/judgment behavior change** — nothing consumes the profile. If
  wiring it turns out necessary to test the round-trip, it is NOT — compare the
  loaded profile to the still-hardcoded module dicts directly.
- **No external mutation** — no push / merge / deploy / secret.
- Author/committer `Claude <noreply@anthropic.com>`; trailers required; NO model
  identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **293 → 293+N passed** (0 failed/skipped/warnings, green under
  `-W error`).
- Regression **68/68, 0 critical, 0 warnings** held — UNTOUCHED (nothing wired →
  goldens + judgment identical).
- Commit-1 green in isolation.
- **Byte-identical round-trip proven:** the extracted profile reconstructs every
  current producer-specific module structure EXACTLY (the load-bearing guard for
  the whole extraction arc).
- Extraction-completeness + schema/metadata (confidence "high", provenance
  documented) asserted. `creative.py`/`governance.py`/`doctrine_engine.py`/
  `pipeline.py` behavior UNCHANGED (nothing consumes the profile). Safety grep
  clean; UI N/A.

---
_Confirmed as active by the orchestrator-in-chief (P-025), foundation step of the
producer-agnostic epic. One packet at a time._
