# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-027
- **Title:** Source `governance.py`'s producer-specific values from the profile (byte-identical, WIDENED per Finding A)

## Why (producer-agnostic epic — governance extraction)

Third extraction step. Source `governance.py`'s producer-specific judgment from
`load_profile("halee_ramone")` (same byte-identical pattern as P-026 for
creative), AND — per P-025's Finding A — WIDEN the profile to also hold the
secondary governance aesthetic constants that were inline. Byte-identical,
guarded by the round-trip + regression 68/68.

## Authority

**Build / feature — in authority, byte-identical.** Extends the profile
(additively) + sources governance from it. **Merge to default gated on explicit
go; dev-branch commits under standing push-go.**

## Scope (the builder implements EXACTLY this)

### Part A — source governance's ALREADY-captured values from the profile
`governance.py` gets `_DEFAULT_PROFILE = load_profile("halee_ramone")` and sources
these from it (same names/shapes; literals deleted; JSON = single source of truth):
- `_TRUTH_ALIGNMENT = _DEFAULT_PROFILE.truth_alignment`
- `_TASTE_KIND_BIAS = _DEFAULT_PROFILE.taste_kind_bias`
- `TASTE_MAX_DELTA = _DEFAULT_PROFILE.taste_max_delta`
- the AESTHETIC subset of `KILL_SWITCHES` (items 6–9) sourced from
  `_DEFAULT_PROFILE.aesthetic_kill_switches`. **The SAFETY kill-switches (items
  1–5, non-destructive/Class-5) STAY hardcoded in governance.py — they are
  producer-AGNOSTIC and must NOT come from a swappable profile.** So `KILL_SWITCHES`
  becomes `[<5 hardcoded safety switches>] + _DEFAULT_PROFILE.aesthetic_kill_switches`
  (verify the order/content reproduces today's list EXACTLY).

### Part B — WIDEN the profile with the secondary governance constants (Finding A)
Extend `ProducerProfile` + `halee_ramone.json` + the P-025 round-trip test to
capture, and then SOURCE from the profile, these currently-inline values (verified
against `governance.py`):
- **`taste_triangle` rules:** the `width_bloom + intimate → identity -= 30` penalty
  (line 180) and the `emotion` blend = mean of `ramone_score`,
  `listener_excitement_score`, `vocal_belief_score` (line 176). Represent honestly
  in the schema (e.g. `taste_triangle: {intimate_width_penalty: 30, emotion_dims:
  ["ramone_score","listener_excitement_score","vocal_belief_score"]}`).
- **veto thresholds:** `reject_below: 45` (identity/emotion reject, line 182),
  `align_veto_below: 50` (govern_variant `align < 50`), `align_fallback: 75`
  (govern_variant `_TRUTH_ALIGNMENT.get(...).get(kind, 75)`). Represent as e.g.
  `veto_thresholds: {reject_below: 45, align_veto_below: 50, align_fallback: 75}`.
Then rewrite `taste_triangle`/`govern_variant` to READ these from
`_DEFAULT_PROFILE` instead of the inline literals — byte-identical.

### Invariants
- **Byte-identical:** no governance output changes. The existing governance/taste
  tests (`test_governance*.py`, `test_live_wire.py`, P-007/8/9 taste tests) MUST
  pass UNEDITED — that is the byte-identical proof.
- **NO-ALIASING PROOF (BINDING, from P-026):** governance's consumers must never
  mutate a sourced global in place. Grep `governance.py` for in-place mutation of
  `_TRUTH_ALIGNMENT`/`_TASTE_KIND_BIAS`/`KILL_SWITCHES`/the sourced values; add a
  no-aliasing test (run governance on a fixture, assert the shared
  `_DEFAULT_PROFILE` structures are byte-unchanged after). Note `_apply_taste`
  mutates a LOCAL `triangle` dict, not the profile — confirm.
- Do NOT touch `creative.py` (done), `doctrine_engine.py` (P-028), `pipeline.py`
  (P-029). No per-call profile threading yet.

### Tests — the binding guard. Test-first.
- Round-trip for the NEW profile fields (taste_triangle rules + veto thresholds ==
  the current inline values), extending `tests/test_producer_profile.py`.
- Value-pins for the sourced governance globals (like P-026's) + the no-aliasing
  test.
- Byte-identical: existing governance/taste tests pass UNEDITED.

Fake adapters only — no DAW / Logic / AppleScript / subprocess / `.logicx` /
network.

## Constraints

- **≤2 commits.** Commit-1: Part A (source already-captured values) + no-aliasing
  test, green in isolation. Commit-2: Part B (widen profile + source the secondary
  constants) + round-trip for the new fields.
- **Byte-identical** — if any governance output changes, STOP and report.
- **No external mutation.** Author/committer `Claude <noreply@anthropic.com>`;
  trailers required; NO model identifier in any commit message/artifact.

## Expected proof (qa to report exact)

- Full suite **331 → 331+N passed** (0 failed/skipped/warnings, green under
  `-W error`) — existing governance/taste tests pass UNEDITED.
- Regression **68/68, 0 critical, 0 warnings** held (byte-identical judgment).
- Commit-1 green in isolation.
- **Byte-identical governance proven** + **no-aliasing proven** (shared profile
  structures unmutated after governance runs). The widened secondary constants are
  now profile-sourced + round-trip-guarded. Safety kill-switches (1–5) confirmed
  STILL hardcoded (not in the profile). `creative.py`/`doctrine_engine.py`/
  `pipeline.py` untouched. Safety grep clean; UI N/A.

---
_Confirmed as active by the orchestrator-in-chief (P-027), governance extraction
(widened) of the producer-agnostic epic. One packet at a time._
