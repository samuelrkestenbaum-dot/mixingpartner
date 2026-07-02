# Receipt — P-039: Producer Selection CLI Exposure + Demo-Safe Invocation

- **Packet:** P-039 — Producer Selection CLI Exposure + Demo-Safe Invocation
  (the user's title and acceptance bar, verbatim). **★ THE FIRST
  POST-SUBSTRATE PRODUCT PACKET — the P-029 producer lever reaches the
  operator surface.** The puck: internal capability → operator/product
  lever → repeatable demo → then the third producer.
- **Date:** 2026-07-02
- **Status:** CLOSED — qa GREEN + reviewer **fix-then-pass → PASS** (one
  fix round: the per-carrier threading guard — fully resolved).

## Scope

**In (the confirmed packet spec):**

1. **`--producer` on exactly 13 analyze-family commands** (11 add_common +
   album + cowork), wired via the shared `add_producer` mechanism. Default
   `halee_ramone` — byte-for-byte today's behavior when omitted; value =
   any profile name resolvable by `load_profile`
   (`doctrine/producers/<name>.json`). Help text names the SEMANTICS, not
   a hardcoded profile list (the P-038 `--mode` precedent).
2. **`_resolve_producer` with the friendly no-traceback error** — an
   unknown name yields a clean CLI error NAMING the available profiles
   (exit 2, nothing written).
3. **The ADDITIVE producer identity surface**, rendered from the PER-CALL
   profile (the P-029/P-031 threading pattern):
   - `doctrine_score.json`: an additive `producer` key —
     `{name, display_name, provenance, confidence}` — **deliberately never
     `risk_class`**;
   - `mix_verdict.md`: the producer line (verdict line 3);
   - the dashboard div; the status header line.
4. **The cowork rider (the optional rider, landed):** 2-line radius; the
   cowork CONTRACT untouched; `API_VERSION 1.0` / 35 commands.
5. **Schema updated additively;** `DIVERGENT_DOCTRINE_KEYS` consciously
   widened `+producer` in BOTH pin files (the pre-scoped pin interaction).
6. **20 new tests** (`tests/test_producer_cli.py`, Commit-1) + the 13
   per-carrier threading-guard instances (the review-fix).

**Explicitly out:**

- Any non-analyze-family command (`compare-reference` never analyzes;
  `regression` is reference-by-definition — the exclusions verified in
  code by qa).
- Any behavior change to scoring, safety, or governance — every score
  surface byte-identical; the 5 safety kill-switches untouched.
- `examples/sample_output/` refresh — the NEXT packet per the user's
  sequence (staged; see Open boundaries).
- Merge/deploy/publish — user-gated.

## Commits and base

- **1 + 1 review-fix commits (≤2 rule satisfied), local at close — pushed
  AFTER close by the orchestrator (standing go), NOT merged:**
  - `b111a18` — "P-039: producer selection CLI exposure + demo-safe
    invocation" — the feature. 10 files, +608/−20: `cli.py` (+75),
    `cowork.py` (the 2-line rider + plumbing), `doctrine_engine.py` (the
    producer identity block), the 3 renderers (verdict line / dashboard
    div / status header), the schema (additive), the two pin files'
    conscious `DIVERGENT_DOCTRINE_KEYS` widening, the NEW 20-test
    `tests/test_producer_cli.py`. **Commit-1 green in isolation.**
  - `a56cb96` — "P-039 fix: per-carrier threading guard — the resolved
    producer provably reaches every analysis" — the review-fix,
    **TEST-ONLY** (1 file, +80/−1: `tests/test_producer_cli.py`).
- **Parent:** `73a134e` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `2c09428` (the post-backlog batch
  merge — P-036 + P-037 + P-038, merged git-natively on the user's word).
  Verified: `git merge-base HEAD 2c09428` = `2c09428`.

## ★ THE ACCEPTANCE BAR — every clause proven at the SUBPROCESS boundary (qa)

The user's bar, verbatim, with proof:

- **same stems ✓** — both runs exit 0; `validate-output` 13/13 each.
- **explicit producer arg ✓** — `--producer timbaland` through the real
  CLI.
- **clear selected producer in artifacts ✓** — exact producer blocks +
  verdict line 3 + dashboard + status-outside-SCORES, BOTH producers.
- **Halee/Ramone remains default ✓** — the bare CLI tree BYTE-IDENTICAL
  file-for-file to a no-arg LIBRARY run (qa's own diff).
- **Timbaland reachable without code changes ✓** — 76.3 vs 60.9 on
  `vocal_chop_groove` from the clean tree.
- **safety/governance unchanged ✓** — the 5 safety kill-switches lead
  `governance.json` VERBATIM in-order in BOTH trees; a base-code
  timbaland `governance.json` byte-identical to HEAD's; 143 safety-pin
  tests green.
- **regression clean ✓** — 93/93, zero goldens in the diff.

## QA proof (GREEN, at `b111a18`)

- **Suite:** 768 → **788** (+20 — `tests/test_producer_cli.py`).
  0 failed/skipped. (Post-review-fix final: **801** — see the reviewer
  section.)
- **Regression:** **93/93, goldens untouched** (zero golden files in the
  diff).
- **Artifact delta enumerated:** EXACTLY **3 of 30 files**
  (+`producer` key / +2 verdict lines / +1 dashboard div) + the status
  header line — **27 artifacts byte-identical, EVERY score surface
  byte-identical**. The SAME 3-file delta shape holds for the timbaland
  tree.
- **The friendly error verbatim-captured** — no traceback, names the
  available profiles, exit 2, nothing written.
- **The 13-command set verified via subprocess `--help` across ALL 22
  subcommands;** the exclusions verified in code (`compare-reference`
  never analyzes; `regression` is reference-by-definition).
- **Commit-1 isolation:** `b111a18` green in isolation (the review-fix is
  test-only on top).
- **Safety grep:** clean (see the acceptance-bar row — kill-switches
  verbatim in-order, 143 safety-pin tests green). **UI smoke:** the
  dashboard div + status header rendered and verified in the artifact
  delta (no other UI surface in this packet).

## Reviewer verdict — fix-then-pass → PASS

- **The ONE must-fix, found by LIVE SABOTAGE:** dropping the threading at
  ONE analyze site left the FULL suite green — 10 of 13 carriers were
  flag-PRESENCE-pinned only. Flag presence is not flag threading.
- **The fix (`a56cb96`, TEST-ONLY):** the per-carrier threading guard —
  13 parametrized instances spying the `producer` kwarg at `cli.analyze`
  / `cowork.analyze` through the REAL `cli.main`; album asserts BOTH
  passes; a dropped threading arrives as `None` and the
  isinstance-`ProducerProfile` check pins the RESOLVED profile on every
  path. The silent-ignore gap is now structurally impossible at all 13
  carriers.
- **Re-verification:** the reviewer re-ran its exact governance cut + the
  album pass-2 cut against the new guard — both FAIL; at HEAD all 13
  pass. Final counts verified: **801 passed / 93/93**.
- **Codex NOT available — single-model review, BOTH rounds.**
- **★ THE LESSON (the THIRD instance of the pattern, → residue, named):**
  flag PRESENCE is not flag THREADING — levers need
  reaches-the-destination guards, joining "defense claims need mutation
  tests".

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, no action:**
  1. The success-path subprocess run — the ERROR path is
     subprocess-proven; the success path runs the same `cli.main`
     in-process.
  2. The `_PRODUCERS_DIR` private-name import in `cli.py` — a public
     accessor is a possible follow-up API nicety.
- **NEW named lesson (standing, the third of the family):** flag presence
  is not flag threading — levers need reaches-the-destination guards.
- All P-038 standing notes retained; standing note 1 (stale sample prose)
  is set to be CLEARED by the staged sample refresh.

## Open boundaries

- **NOT merged.** `b111a18` + `a56cb96` are pushed to the dev branch
  AFTER this close by the orchestrator under the standing dev-branch go;
  the MERGE remains a user gate. No deploy/publish/secrets touched.
- **NEXT per the USER'S SEQUENCE = the SAMPLE REFRESH (STAGED, not
  active):** regenerate `examples/sample_output/` to show the same stems
  under BOTH producers (two trees or one tree + a differential README
  section — the orchestrator scopes with the user), which also clears the
  accepted P-038 standing note about stale sample prose (the P-039
  identity surface gives the samples self-describing trees); conscious
  test-9 (OLD_KEYS) interaction check. Then the THIRD producer, then
  deeper mode-forking.
