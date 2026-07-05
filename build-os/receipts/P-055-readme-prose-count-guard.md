# Receipt — P-055: README Prose-Count Guard

- **Packet:** P-055 — README Prose-Count Guard. A test + docs packet that pins
  the README's spelled-out PROSE counts (trees/producers, demos/runs, fixtures,
  and the win/deviate split) against their LIVE / COMMITTED single sources — the
  sibling of P-054's numeric guard, one abstraction level up. Completes the
  README-drift-guard family: P-054 pinned the numeric values (command count,
  regression example, five-producer table); P-055 pins the spelled-out prose
  counts. **ZERO engine/profile/analyzer/MCP/runtime change.**
- **User authority:** opened on the user's "Go" (2026-07-05) after the P-054
  merge (PR #32 → default `7af1e3e`) — the LAST clean decision-free direction
  (the P-054 residue named it as the "prose-count guard" candidate). The
  taste-gated directions (Eno-deferral analyzers, quincy/halee dropout reach, a
  sixth producer, apply-to-Logic) stayed USER-GATED and were NOT touched. **After
  this packet the self-serve hygiene well is dry — every remaining open direction
  needs a genuine user decision.**
- **Date:** 2026-07-05
- **Status:** CLOSED — qa GREEN **(10/10; suite 1306 / 0)** + reviewer
  **PASS (no must-fix)**.

## Scope

**In (the confirmed packet spec):**

1. **Audit the prose counts** — confirm each currently matches its live source.
   The audit was CLEAN: NO stale prose count found, so the README is
   byte-UNCHANGED (blob-identical both sides — see Commits) and the packet is
   guard-only.
2. **The prose-count guard** — a NEW `tests/test_readme_prose_counts.py`
   (4 tests) with TARGETED, anchored assertions mapping each spelled-out count
   word to an int and comparing to a LIVE / COMMITTED source, every expected
   value DERIVED (no hardcoded 5/11/4/7):
   - **"five" (trees / producers / profiles / judgments)** ==
     `len(SAMPLE_TREES)` (imported from `test_sample_refresh`) — 9 anchored
     phrases (README ~63, 81, 111, 125, 159, 163, 167, 221, 497).
   - **"eleven" (runs / directories / demos / pairs)** == `len(MODE_DEMOS)`
     (imported from `test_mode_demo_refresh`) — README ~76, 222, 343, 498.
   - **"four" (example projects / fixtures)** == `_live_fixture_count()` =
     `len(FIXTURES_DIR.glob("*/project_manifest.json"))` = 4 (tracks the
     generator's 4 builders 1:1) — README ~46, 510, plus the digit
     "(4 fixtures" ~499.
   - **The "seven win / four deviate" split** (~343) PINNED, derived
     non-circularly: deviating = count of `MODE_DEMOS` whose byte-pinned
     `WINNERS[demo]` != `_COMMON_WINNERS` = 4 (brian_eno_conservative,
     chris_lord_alge_big_chorus, chris_lord_alge_conservative,
     quincy_jones_experimental); winning = 11 − 4 = 7. Self-updates if a future
     demo shifts the split.
   - A word→int decoder map (three…twelve) for the README's spelled side;
     anchored phrase extraction; fails loudly naming the drifted phrase + its
     live source.

**Explicitly out (binding non-scope, held):**

- ZERO changes to engine code — **0 `.py` under `logic_mix_os/`**; the engine +
  profiles + analyzers + `cowork_mcp/` + `cli.py` + `cowork.py` byte-unchanged.
  No new producers / families / analyzers / dependencies. No safety/governance
  changes.
- ZERO `examples/` change — the five sample trees + eleven mode demos + the
  fixture projects byte-untouched; zero fixtures/goldens.
- No general "rewrite the README" — the audit was clean, so ZERO prose sweep and
  ZERO stale-count fix were needed (README byte-unchanged); only the guard
  landed. No pinning of non-count words.
- The two content-dependent prose-count classes were consciously NOT pinned (see
  Residue) — pinning them to a roster length would MIS-SOURCE.
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Single commit** (guard-only — the audit was clean, so one commit; ≤2-commit
  rule honored):
  - `8b3adec` — "P-055: README prose-count drift guard" — exactly **1 file**,
    +244:
    - `logic-mix-os/tests/test_readme_prose_counts.py` (NEW, +244 — the 4-test
      prose-count drift guard)
  - `README.md` is byte-UNCHANGED — the audit found nothing stale
    (blob-identical: `logic-mix-os/README.md` = `51d7a51…` at both `ccdc054`
    (parent) and `8b3adec` (HEAD)).
- **Commit-1 green in isolation:** trivially satisfied — the single commit is the
  only change, so HEAD == the isolation proof; full suite **1306**.
- **Parent:** `ccdc054` (set-active — "build-os: set P-055 (README prose-count
  guard) active — user go") on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base with default:** `7af1e3e` (= PR #32 merge — P-054 already merged
  to default). Verified at close: `git merge-base HEAD 7af1e3e` = `7af1e3e`; the
  dev branch is fast-forwarded onto default, so a P-055 PR carries only `8b3adec`
  + the close commit — a clean single-packet PR.
- **Push state:** PUSHED to the dev branch under the standing go **BEFORE
  qa/reviewer ran** — both gates validated the final SHA. **NOT merged** — the
  merge of P-055 is a user gate.

## QA proof (GREEN — 10/10)

- **Suite:** 1302 → **1306 passed, 0 failed** (+4, all in the new
  `tests/test_readme_prose_counts.py`); regression **93/93**; single commit =
  HEAD is the Commit-1-isolation proof.
- **Per-file collect:** `test_readme_prose_counts.py` = **4**.
- **Commit-1 iso:** 1306 (single commit).
- **Derived-not-hardcoded verified live:** grep for `== 4|5|7|11` on the expected
  side → none; the only digit literals are the decoder map + the `(\d+) fixtures`
  regex whose expected side is `_live_fixture_count()`.
- **The guard BITES 6/6** (independent, in isolated worktrees, restored between
  runs): five→six, eleven→twelve, four→five (spelled), (4→(5 (digit),
  seven→eight, four-deviate→five — each fails exactly its test.
- **Robustness (no false positives):** mutating the deliberately-EXCLUDED
  occurrences left the guard GREEN — the "five hardcoded safety switches" (~160),
  "all five creative problem branches" (~224), the (producers−1) "the other four
  profiles" (~123), and the conservative-residue (~320) are correctly out of
  scope. The builder's own anchor-collision fix confirmed: `the way the (\w+)
  trees above` captures only "five"; the untightened form would have wrongly
  captured "sample" from ~228.
- **Coverage complete:** every load-bearing prose count is pinned or consciously
  flagged; no silent miss.
- **Zero engine drift; safety grep clean** — the ONLY diff is the additive new
  test file; README blob-identical; no secrets / network / model-ids / abs-paths.

## The user's required proof — every clause met

suite clean ✓ (1306/0) · regression clean ✓ (93/93) · zero engine/runtime change
✓ (0 `.py` under `logic_mix_os/`; zero `examples/` change; README byte-unchanged)
· every load-bearing prose count pinned to a live/committed source, DERIVED not
hardcoded ✓ (`len(SAMPLE_TREES)`, `len(MODE_DEMOS)`, `_live_fixture_count()`,
the WINNERS-vs-`_COMMON_WINNERS` split) · the guard BITES on a prose-count drift
✓ (6/6) · the "seven win" split PINNED (cleanly derivable, non-circular) ✓ ·
whole-README audit shows no currently-stale prose count ✓ (clean — README
byte-unchanged) · the five trees + eleven demos byte-untouched ✓.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly.**
- Derivation clean; the "four" source correct (`_live_fixture_count()` tracks the
  generator's 4 builders 1:1 — the builder correctly REJECTED conftest's
  `FIXTURE_NAMES`, which is only the original three; `vocal_chop_groove` lives
  outside it by design); the seven-win split non-circular; anchors specific; the
  residue correctly reasoned. Verbatim: "Closes the README-drift-guard family."

## Residue (carried to `build-os/memory/residue.md`)

- **RESOLVED by this packet:**
  - The P-054 "prose-count guard" residue (P-054 note 1) — ✓ RESOLVED for the
    LENGTH-DERIVED class: the load-bearing "five … trees/producers", "eleven …
    demos/runs", "four … fixtures" prose counts and the seven-win/four-deviate
    split are now machine-pinned against their live/committed single sources.
- **NEW accepted notes (recorded not fixed — both consciously NOT pinned,
  correct to flag; the "content-dependent prose count" class — counts that do
  NOT track a clean `len()`):**
  1. **The "five *_conservative rows" / "five pairwise-distinct sets"**
     (README ~320/321): their true source is the count of CONSERVATIVE demos
     (5 of 11), NOT `len(SAMPLE_TREES)` — a 6th producer added WITHOUT a
     conservative demo would keep this at 5 while the roster is 6. Pinning to
     `SAMPLE_TREES` would be MIS-SOURCED; correctly flagged, not pinned.
     Structurally, demo growth still trips the eleven-demo directory-set guard.
  2. **The content-dependent (producers−1) "fours"** (README ~149 "the four
     reference-lineage producers", ~329 "the other four win…"): roster-sensitive
     but NOT clean `len()−1` values (they depend on how many producers DIVERGE
     on a branch — CLA broke the pattern, so a 6th producer might make it "three"
     or "five"). Pinning to a roster length would mis-source or need new
     plumbing; correctly left unpinned (the reviewer named this pair for the
     record).
  - Both are the same class. A future packet could pin them via the actual
    divergence computation if it ever matters; LOW PRIORITY (they're visible and
    change with real content review).
- All prior standing notes (incl. the ★★ groove-carrier trajectory watch-item,
  the CLA sha256-self-pin-on-sixth-producer note, the P-050/P-051/P-052/P-053/
  P-054 accepted notes, and the safety line) and the named lessons retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-055** — `8b3adec` (+ this close
  commit) atop `7af1e3e` (= PR #32) — a clean single-packet PR (the branch is
  fast-forwarded onto default). Awaits the user's explicit word. The commit is
  pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING — and the self-serve hygiene well is now DRY.** The
  README-drift-guard family is COMPLETE. The orchestrator PRESENTS the open
  directions, ALL of which now require a genuine USER DECISION (not just a green
  light): a sixth producer (WHO + grounding) · the future-analyzer candidates
  from Eno's deferrals (WHICH one + measurement approach — textural coherence ·
  generative process · ambient patience) · quincy/halee authored dropout reach
  (a taste call) · the apply-to-Logic backend (FUTURE, EXPLICITLY re-gated —
  never auto) · a real external host driving the MCP server (a MANUAL user step)
  · a real MCP-SDK transport swap · the content-dependent prose-count residue
  (low priority) · anything else the user calls. Do NOT open anything blind.

---
_Closed by the archivist (2026-07-05). qa GREEN (10/10; suite 1306 / 0 /
regression 93/93 / Commit-1 iso 1306 / per-file collect
test_readme_prose_counts.py=4 / the guard bites 6/6 — five→six, eleven→twelve,
four→five, (4→(5, seven→eight, four-deviate→five — with no false positive on the
deliberately-excluded fives/fours / safety grep clean) + reviewer PASS (no
must-fix; single-model — Codex unavailable). The README's spelled-out prose
counts (trees/producers, demos/runs, fixtures, the win/deviate split) are now
MACHINE-PINNED against their live/committed single sources — the
README-drift-guard family is COMPLETE: P-054 pins the numbers, P-055 pins the
prose, so roster/demo/fixture growth forces the README to update or the suite
fails loudly. This closes the self-serve hygiene well; the remaining open
directions all require a genuine user decision._
