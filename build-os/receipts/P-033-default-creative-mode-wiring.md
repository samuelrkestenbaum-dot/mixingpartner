# Receipt — P-033: wire `_default_creative_mode` to the producer profile

- **Packet:** P-033 — wire `_default_creative_mode` to the producer profile:
  the FIRST post-merge packet, making the authored creative-mode table a REAL
  product lever. The P-032h reviewer's trajectory finding fixed exactly as
  pre-registered: **the P-032i negative pin flipped through its designed
  conscious-edit path**
  (`test_no_intimate_mode_selection_..._unreachable` →
  `test_intimate_mode_selection_..._reachable`, STRENGTHENED — adds the
  direct resolver assertion + observed==authored + no-fallback-key).
- **Date closed:** 2026-07-02
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` (restarted from the
  PR #17 merge); packet base = parent `cb5fc8b` (active-packet confirmation),
  atop the merged default `58d21dd` (PR #17 — the producer-agnostic epic,
  P-025 → P-032i + P-031, on default). **The NEW merge base for landing
  decisions is `58d21dd`.**
- **Verdict:** qa **GREEN**; reviewer **PASS (no must-fix)**. **Codex NOT
  available — single-model review.**

## Scope

**In:**

- `pipeline.py` — `_default_creative_mode(intent, profile=None)` reads the
  PASSED profile's `default_creative_mode` table (module `_DEFAULT_PROFILE`
  when None — the P-029 consumer pattern); the only product call site threads
  the loaded profile at pipeline.py:279.
- `creative.py` — `run_creative_engine(result, mode=None, profile=None)`:
  mode=None → the profile's declared default; a requested mode absent from
  `search_modes` → `_profile_default_mode` (the declared default_mode if
  present in search_modes, else the FIRST authored mode — deterministic,
  profile-owned) + a conditional `search_mode_fallback` evidence key
  (present ONLY when fired). The dead `"dramatic_contrast"` default on
  `generate_variants` removed. **No functional hardcoded mode name remains
  in product Python.**
- `creative_renderer.py` — renders the fallback line;
  zero-bytes-when-absent.
- Tests: the NEW 18-test `tests/test_creative_mode_wiring.py` + the two
  pre-registered pin files (`tests/test_differential_proof.py`,
  `tests/test_timbaland_profile.py`), flipped via the conscious-edit path —
  updated, never weakened (STRENGTHENED).

**Explicitly out:**

- Any deepening of the mode lever into `generate_variants` (it does NOT yet
  fork on mode — see the reviewer calibration note below; a future packet).
- Validation tightening on `search_modes` non-emptiness /
  `default_creative_mode` key structure (→ the future validation-sweep
  packet; recorded in residue).
- The `cli.py:446-447` `--mode` help text (pre-existing hardcoded reference
  mode names; ties to the unstaged CLI-producer-exposure backlog).
- P-030 (rename dims), the analyzer extension, the verdict-filename
  cosmetic, the standing residue sweeps.

## Commit (single, ≤2-commit contract met)

| Commit | Summary |
| --- | --- |
| `b6c840c` | P-033: wire `_default_creative_mode` to the producer profile — the authored table is a live lever. 6 files, +476/−48 (3 product: `pipeline.py`, `creative.py`, `creative_renderer.py`; 3 test: the new 18-test `tests/test_creative_mode_wiring.py` + the two pin files). Parent `cb5fc8b` (set-active), atop `58d21dd` (PR #17 merge). **HEAD IS Commit-1 → green in isolation.** |

Push state at close: `b6c840c` local AND pushed to the dev branch. NOT merged
(the merge base for landing decisions is now `58d21dd` = PR #17).

## ★ THE PAYOFF (qa verified LIVE, before/after)

- Timbaland on `simple_vocal_piano_song`: base `dramatic_contrast` (the
  silent fallback) → HEAD **`conservative`** (the authored intimate mode,
  bias "preserve groove identity, subtle moves, protect the pocket").
- Timbaland's artifact deltas = EXACTLY simple's creative.json (mode+bias
  lines) + creative_report.md.
- dense/splice → `dramatic_contrast` both sides (its authored default_mode).
- **★ The producer lever is now COMPLETE end-to-end:** doctrine weights +
  polarity + creative judgment values + creative MODE + both gates +
  confidence rendering — all profile-authored and live.

## QA proof (GREEN)

- **Suite:** 660 → **678 passed** (+18, all in the new
  `tests/test_creative_mode_wiring.py`); 0 failed / skipped.
- **Regression:** **68/68** (0 critical / 0 warnings).
- **Commit-1 isolation:** single commit — HEAD IS Commit-1 → green in
  isolation.
- **Reference byte-identity** with neutral inputs → ZERO deltas
  (73.8 / 70.7 / 74.3; resolved modes identical; base hardcoded map ==
  reference authored table == OLD_HARDCODED_MAP string-for-string, checked
  against the ACTUAL base code).
- **Fallback safety:** incl. qa's own adversarial no-`dramatic_contrast`
  profile → no KeyError.
- **Sabotage:** re-hardcoded map → 6 guards FAIL while reference
  byte-identity stays green.
- **Still-binding pins:** the vocal-blend pin MD5-identical.
- **Safety grep:** clean.
- **UI smoke:** N/A (no UI surface); the rendered-artifact smoke is covered
  by the before/after artifact diff (creative_report.md fallback line
  renders only when fired; zero bytes when absent).

## Reviewer verdict (PASS, no must-fix)

- Wiring/threading correct per-call (sabotage-verified BOTH directions).
- Resolution order proven; `json.load` dict-order determinism confirmed
  (py3.11).
- The `generate_variants` default genuinely dead (the function body never
  reads it).
- KeyError closed on ALL THREE paths — **P-033 NARROWED the crash surface**
  (pre-P-033 ANY profile lacking `dramatic_contrast` crashed; now only a
  zero-mode profile would).
- **Codex NOT available — single-model review.**

### ★ Reviewer CALIBRATION note (record for future arc language)

The mode lever is real but **THIN** — `search_mode` steers the reported
mode/bias surface; `generate_variants` does NOT yet fork on it. P-033 makes
the authored mode REACHABLE and VISIBLE; a future packet would make modes
reshape variant generation/scoring. **Do NOT over-claim behavioral
steering.**

## Residue (recorded in `build-os/memory/residue.md`)

1. **NEW (reviewer, → the future validation-sweep packet):** `_validate`
   lacks (a) a non-empty check on `search_modes` (StopIteration on a
   zero-mode profile — NARROWED vs pre-P-033, not a regression) and (b)
   structural checks on `default_creative_mode`'s three keys, which the
   pipeline now hard-dereferences.
2. **NEW:** `cli.py:446-447` `--mode` help text hardcodes reference mode
   names (pre-existing; will go stale; ties to the unstaged
   CLI-producer-exposure backlog).
3. **NEW (cosmetic):** the fallback `reason` wording says "the profile's own
   default" even on the first-authored-mode branch.
4. **NEW (reviewer calibration):** search_mode is a thin lever —
   `generate_variants` doesn't fork on it; a future packet may deepen it.
5. The P-032h/P-032i `default_creative_mode`-inertness residue entries are
   now marked **✓ RESOLVED by P-033**.
6. All other standing carry-forwards retained.

## Open boundaries (USER-GATED — nothing crosses without explicit go)

- **Merge:** P-033 (`b6c840c`) sits on the dev branch, pushed, NOT merged to
  default. Merging awaits the user's explicit go.
- No deploy / publish / secrets touched.

## Next (the USER'S CONFIRMED post-merge order)

**P-030 (rename the halee/ramone dims off the producer names)** — touches 2
producer JSONs + `tests/test_differential_proof.py` + the
goldens/memory/renderers/schemas that pin `halee_score`/`ramone_score` (the
long-standing compat-shim caution: output keys are pinned by golden
snapshots + regression SCORE_KEYS + renderers — needs a DELIBERATE
compat/migration strategy, presented as a PLAN before building) → the
analyzer extension → the verdict-filename cosmetic → the residue sweeps.
Staged-not-active; nothing activates until the orchestrator confirms.

---
_Closed by the archivist (2026-07-02). qa GREEN + reviewer PASS (no
must-fix); Codex not available — single-model review._
