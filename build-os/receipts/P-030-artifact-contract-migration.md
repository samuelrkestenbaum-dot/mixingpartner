# Receipt — P-030: the artifact-contract migration

- **Packet:** P-030 — the artifact-contract migration (THE USER'S DECISION:
  **Option A + memory.py dual-read + verdict filename fold-in**):
  `halee_score` → `physical_space_score`, `ramone_score` →
  `emotional_hierarchy_score`, the internal/evidence/profile keys renamed
  (`baselines.physical_space`, `penalty_coeffs.emotional_hierarchy`, the
  evidence keys, the reference taste-triangle dim), and
  `halee_ramone_mix_verdict.md` → **`mix_verdict.md`** (neutral). **Clean break
  for public artifacts — NO emitted aliases;** the ONLY compatibility carve-out
  is memory.py's read-only dual-read of persisted local history. The
  long-standing pre-second-producer debt (kept verbatim since P-025 by the
  byte-identical-first decision) is now paid: **a producer-agnostic engine
  emits a producer-agnostic contract.**
- **Date closed:** 2026-07-02
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`; packet base = parent
  `8f14d4d` (active-packet confirmation), atop the P-033 close, atop the merged
  default `58d21dd` (PR #17 — the merge base for landing decisions, verified
  `git merge-base HEAD 58d21dd` = `58d21dd`).
- **Verdict:** qa **GREEN**; reviewer **PASS (no must-fix)**. **Codex NOT
  available — single-model review.**

## Scope

**In (the user-specified surfaces, all touched):**

- **Commit-1 (product):** doctrine engine · creative scoring · mix_planner ·
  memory.py (the dual-read carve-out) · the regression invariant read · cli ·
  all 3 renderers (markdown / operator_view / html_dashboard) · both JSON
  schemas (doctrine_score + mix_plan) · BOTH producer JSONs
  (`halee_ramone.json` + `timbaland.json`) · pipeline verdict filename ·
  output validator · README (the new key meanings documented).
- **Commit-2 (pins):** regression SCORE_KEYS · the 3 CONSCIOUSLY regenerated
  goldens · 5 samples incl. the verdict-sample rename · 26 updated test files ·
  the NEW 17-test `tests/test_contract_migration.py` (the user's required
  tests 1–17).

**Explicitly out (user-specified non-scope, honored):**

- No scoring-math / weight / behavior changes for EITHER producer beyond key
  names. No safety/governance changes. No emitted-artifact aliases. No
  analyzer extension. No residue sweeps.
- Producer-named VALUES (search-mode names, action prose, doctrine tags) —
  ruled in-scope-as-built by the reviewer's judgment call (see below), routed
  to the residue sweep.

## Commits (two, the user-specified split — ≤2-commit contract met)

| Commit | Summary |
| --- | --- |
| `21c0ab0` | P-030: rename the producer-named contract keys to aesthetic-descriptive names. **Commit-1, product surfaces, 18 files** (+118/−78): engine, both producer JSONs, creative, mix_planner, memory.py dual-read, regression invariant read, cli, all 3 renderers, both schemas, pipeline filename, validator, README. |
| `0c7885e` | P-030: migrate the pins — tests, samples, and the conscious golden regeneration. **Commit-2, 36 files** (+534/−197): SCORE_KEYS, 3 consciously regenerated goldens, 5 samples + the verdict-sample rename, 26 updated test files, the new 17-test `tests/test_contract_migration.py`. |

Parent `8f14d4d` (set-active). Push state at close: **both commits PUSHED to
the dev branch. NOT merged** (merge base `58d21dd` = PR #17).

**Commit-1 isolation (the HONEST boundary, as the packet spec pre-declared):**
a contract migration cannot be fully green at Commit-1 against unmodified
pins. At `21c0ab0`: **136 failed / 542 passed**, with EVERY failure classified
into the 6 old-key-pin signature classes and **ZERO behavioral** — the product
imports, the pipeline runs, and new-key artifacts are emitted at Commit-1.

## ★ THE HEALTH BAR HELD (qa's core proof)

> same math · same scores · same differential behavior · new
> producer-agnostic contract · old persisted memory still readable · new
> emitted artifacts clean

- **All 90 numeric values across the 6 producer×fixture runs IDENTICAL under
  the old→new key map** — ref 73.8 / 70.7 / 74.3; tim 68.4 / 52.6 / 49.7;
  every component.
- **Golden diff = EXACTLY the two key-rename lines per fixture**, values
  byte-identical — the conscious-regeneration proof.
- Same differential behavior across both producers.

## QA proof (GREEN)

- **Suite:** **705 passed** (678 + 27 migration instances); 0 failed /
  skipped.
- **Regression:** **68/68 vs the REGENERATED goldens** (0 critical /
  0 warnings).
- **The 17 required migration tests pass**, with 4 live spot-checks.
- **Memory dual-read, all 4 behaviors proven:** reads new-key history; reads
  seeded OLD-key history with the file NOT rewritten; prefers new keys on
  conflicting values; never WRITES old keys.
- **Commit-1 boundary honest:** 136 failed / 542 passed at `21c0ab0`, every
  failure classified into the 6 old-key-pin signature classes, ZERO
  behavioral.
- **Grep proof clean:** the old keys survive ONLY in memory.py:27,32-33 (the
  dual-read carve-out) + the migration test — exactly the user's allowed
  locations.
- **Renderer labels producer-agnostic, verified live.**
- **Safety grep:** none.
- **UI smoke:** N/A (no UI surface); the rendered-artifact surfaces
  (renderers, dashboard sample, verdict markdown) covered by the live
  renderer-label check + the sample/golden diffs.

## Reviewer verdict (PASS, no must-fix)

- **The strongest no-judgment-change proof — a MECHANICAL canonical-rename
  comparison over the entire diff** (apply old→new to every removed line,
  diff vs the added lines): **zero numeric constants changed, zero
  reordering.**
- `component_scores` insertion order preserved (positions 1-2); the reference
  `emotion_dims` renamed IN PLACE with untouched blend arithmetic.
- Value identity independently verified.
- **Sabotage** (re-emit `halee_score`) caught by 10 failing instances across
  4 migration tests.
- **Pins updated-never-weakened** — the dashboard pin STRENGTHENED
  (new-present AND old-absent).
- COWORK_CONTRACT.md names no score keys (no doc miss); schemas validated
  live.
- **Codex NOT available — single-model review.**

### ★ Reviewer judgment call (recorded)

Producer-named search-mode NAMES (`halee_depth` / `ramone_vocal_truth`)
survive as profile-internal vocabulary and appear in emitted creative.json as
VALUES — **ruled in-scope-as-built**: the user's rule bans old-KEY aliases;
mode names are values; profile vocabulary is protected. Routed to the residue
sweep with two siblings: the engine action prose ("Halee naturalism…" /
"Ramone-style…") and the warning doctrine tags
(`phil_ramone_vocal_centrality` / `phil_ramone_restraint`) emitted as values.

## Residue (recorded in `build-os/memory/residue.md`)

1. **NEW (the reviewer judgment call):** the three producer-named-VALUE
   surfaces (search-mode names in emitted creative.json; action prose;
   warning doctrine tags) → residue-sweep candidates; explicitly NOT contract
   keys.
2. The P-030 rename-debt entry marked **✓ RESOLVED** — the long-standing
   "rename dims before a second producer" caution, done AFTER (not before)
   per the byte-identical-first strategy, and the migration proved clean.
3. **NEW (cosmetic, self-healing):** stale gitignored .pyc caches qa saw.
4. All other standing carry-forwards retained.

## Open boundaries (USER-GATED — nothing crosses without explicit go)

- **Merge:** P-030 (`21c0ab0` + `0c7885e`) sits on the dev branch, pushed,
  NOT merged to default. Merging awaits the user's explicit go.
- No deploy / publish / secrets touched.

## Next (the remaining post-merge backlog)

**The analyzer extension** (non-lead vocal-band events → makes the vocal-blend
policy live on real data + the creative.py:98 name-match fix) → **the residue
sweeps** (now including the three producer-named-VALUE surfaces from the
reviewer's judgment call). Staged-not-active; nothing activates until the
orchestrator confirms.

---
_Closed by the archivist (2026-07-02). qa GREEN + reviewer PASS (no
must-fix); Codex not available — single-model review._
