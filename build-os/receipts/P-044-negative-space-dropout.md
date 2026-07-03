# Receipt — P-044: Negative-Space Dropout Move Family

- **Packet:** P-044 — Negative-Space Dropout Move Family (the user's title,
  verbatim). The vocabulary's most aggressive family enters
  CANDIDATE-PLANNING ONLY: the move vocabulary widens from 9 to **10 kinds —
  7 neutral + 3 reach-gated EXTENDED** (`negative_space_dropout` joins
  `arrangement_lift` + `ensemble_rebalance`). **THE SAFETY LINE (the user's
  doctrine, verbatim): "dropout is an arrangement proposal, not a
  destructive operation."** No execution semantics anywhere — protections
  are ENGINE-owned, profile-blind, fail-closed; the P-043 loader gates
  generalize UNMODIFIED (`producer_profile.py` untouched — proven live).
  **This completes the user's Shape C arc** — B seam → narrow C → the
  aggressive family, all governed, the safety doctrine verbatim in
  code/constants/tests.
- **User authority (verbatim go, 2026-07-03):** "Merge P-043 now. Then open
  negative-space dropout, but narrowly and conservatively." — P-043 merged
  FIRST as PR #22 (default tip `80e9bd5`), then this packet. The user's
  framing (from the packet contract): "This family is higher-risk because
  it sounds like 'mute/drop something,' so the first implementation must be
  candidate-planning only, not execution semantics."
- **Date:** 2026-07-03
- **Status:** CLOSED — qa GREEN + reviewer **PASS (no must-fix; all
  adversarial attacks defeated).**

## Scope

**In (the confirmed packet spec):**

1. **`logic_mix_os/constants.py`** — the vocabulary 9→**10**;
   `CREATIVE_EXTENDED_KINDS` 2→**3** (`negative_space_dropout`); the P-043
   dropout-exclusion note consciously LIFTED per the user's go.
2. **`logic_mix_os/creative.py`** — the profile-blind
   `_dropout_protected_names` filter (~439–511) EXCLUDING: lead vocals /
   hook candidates / `vocal_uncertain` always / ALL vocals while the lead
   is masked / the kick+snare+bass family / sacred elements — with the
   FAIL-CLOSED NO-EMIT rule (no `_resolve` degrade chain: no legitimate
   target → the variant does not emit). Two curated variants —
   `chorus_lift_F` + `density_E` — byte-pinned plan text in the
   duplicate+region-mute vocabulary, reversibility-tagged. The LOOP dropout
   consciously OMITTED (source integrity — `DROPOUT_POOL["loop"] == []`
   pinned).
3. **The three producer JSONs** — rows EVERYWHERE (no silent inheritance):
   timbaland medium/80.9 (his signature family), quincy medium/73.7, halee
   HIGH/60.6 — her intimate truth 48 < her align_veto 50 → governance
   VETOES dropout under her intimate lean. **Reach ONLY timbaland**, on
   exactly `experimental` / `dramatic_contrast` / `negative_space`.
4. **Tests:** `tests/test_negative_space_dropout.py` (NEW — 47 tests) +
   conscious pin updates in 4 test files.
5. **EXACTLY 3 regenerated artifacts** in
   `examples/sample_output_timbaland/` (`creative.json` /
   `creative_report.md` / `dashboard.html`) — the conscious enumerated
   drift, verbatim README invocation, pin at full strength.

**Explicitly out (the user's non-scope, binding):**

- **No execution/mute/apply semantics** — the safety line. Exactly one new
  kind; no other families, no second dropout variant family. No new
  analyzers. No doctrine/scoring changes (doctrine scores byte-stable —
  headlines 76.3/60.9 unchanged). No safety/governance/veto changes; the
  caps and the P-042/P-043 guarantees never weakened.
- `producer_profile.py` UNCHANGED (the P-043 loader gates generalize
  unmodified — proven live). No authored reach for halee/quincy (their
  gate proven synthetically). The halee tree ABSENT from the diff
  (byte-stable everywhere).
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2 rule satisfied):**
  - `87635d3` — "P-044 Commit-1: negative_space_dropout — the kind, the
    curated variants, the structural protection filter, honest rows
    everywhere; zero behavioral change" — 10 files, +925/−59. **Commit-1
    GREEN IN ISOLATION (984 passed); zero-behavior verified THREE ways
    incl. qa's 312-cell C1 probe with 0 dropout emissions; both sample
    trees byte-untouched at C1.**
  - `f72f222` — "P-044 Commit-2: Timbaland's authored dropout reach + the
    differential proof + the conscious enumerated drift".
  - Combined: **exactly 13 files, +1354/−112** (verified `git diff --stat
    9fdb172 f72f222` at close).
- **Parent:** `9fdb172` (active-packet confirmation) on the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1`.
- **Merge base for landing decisions:** `80e9bd5` (= the PR #22 merge —
  P-043 landed FIRST per the user's sequencing). Verified at close:
  `git merge-base HEAD 80e9bd5` = `80e9bd5`.
- **Push state:** PUSHED to the dev branch under the orchestrator's
  standing go **BEFORE qa/reviewer ran** — both gates validated the FINAL
  SHAs. **NOT merged** — the merge of P-044 is a user gate.

## QA proof (GREEN — twelve items, zero deviations from builder claims)

- **Suite:** 950 → **1000 passed, 0 failed**; regression **93/93**;
  **Commit-1 iso 984**.
- **Sample trees:** both trees independently re-rendered via the verbatim
  README invocations — halee **30/30 byte-identical**; timbaland **30/30
  vs the NEW committed tree**; vs pre-packet **EXACTLY 3 differ / 27
  byte-identical** (`cmp` per file). Headlines **76.3/60.9 unchanged**;
  **EVERY winner unchanged** (chorus_lift_B 86.7 / loop_B / depth_A /
  vocal_A).
- **The 312-cell differential, 0 mismatches:** dropout ids ONLY timbaland,
  ONLY his three authored modes (+ default resolution =
  dramatic_contrast); halee + quincy **0 dropout over the full
  parametrization**; the ordering property held.
- **Protection probes:** an only-protected synthetic → **ZERO emission**
  under all reaching modes × all 5 problems; **12 real emissions × 0
  forbidden names**; profile-blind by AST **and** behaviorally (synthetic
  reaching profiles cannot surface a protected name); the masked-lead rule
  holds synthetically.
- **Sabotage 4/4 bites:** filter removed → **4 failed** (the four
  protection tests); reach deleted → **3 failed**; no-emit degraded to
  fallback → **5 failed**; halee risk high→low → **6 failed** incl. BOTH
  cap tests.
- **Cap + governance live:** halee ValueErrors on all five
  low/medium-posture modes, validates only on high-posture experimental;
  runtime fail-closed `reach_capped`; `govern_variant(dropout, intimate,
  halee)` → 48 < 50 → **vetoed=True**.
- **The no-execution guard:** **0 machinery-word hits** in all dropout
  prose; reversibility tags present; doctrine byte-stability across all
  **12 producer×fixture overalls**.
- **qa discrepancies (both non-blocking → residue):** (1) task-premise —
  `_lead_masked` is False on EVERY fixture at HEAD (no real fixture
  carries a bad-masked lead), so the masked-lead exclusion is proven
  SYNTHETICALLY only; (2) removing the filter changes NO shipped artifact
  bytes (no protected name sits on the shipped fixtures' candidate
  surfaces today) — the protection guarantee rests on the 4 synthetic
  tests, which bite exactly.

## ★ The user's acceptance bar — all nine clauses met (pinned evidence)

- **exists as an extended curated kind ✓** — vocabulary 10 / extended 3.
- **reach-gated admission works ✓** — the P-043 seam, generalized
  unmodified.
- **Timbaland only where authored ✓** — his three modes exactly; zero
  elsewhere incl. his intimate path.
- **Halee/Ramone and Quincy do not drift ✓** — 0 dropout over the full
  parametrization; the halee tree + the quincy pins byte-stable.
- **risk caps bind ✓** — load + runtime, against each profile's OWN row.
- **lead/hook/core-groove protections override ✓** — engine-owned,
  profile-blind, fail-closed NO-EMIT.
- **no execution semantics ✓** — byte-pinned prose + the lexical guard.
- **sample-tree drift is conscious ✓** — 3/30 enumerated, verbatim
  invocation, pin at full strength.
- **differential proof attributes to authored reach ✓** — 312 cells, 0
  mismatches.

## Reviewer verdict — PASS (no must-fix)

- **Single-model review — Codex unavailable, stated explicitly;** the full
  suite independently re-run at **1000**.
- **Filter evasion: NO SUCCESS** — single gate, filtered BEFORE
  construction, fail-closed no-emit, exact real-signal spellings verified;
  the fixture pins are literal name lists (falsifiable, not circular).
- **Profile-widenability: no path** (residual note → residue: the AST
  guard would miss a future profile-sourced global whose name lacks
  "prof" — today's code reads none; the runtime differentials carry the
  real weight).
- **Masked-lead interpretation: FAITHFUL** — the stricter reading
  (`vocal_uncertain` unconditional + ALL vocals while the lead is masked,
  single shared predicate basis).
- **Core groove carrier: DEFENSIBLE with an honest edge** — on the chop
  fixture the beat_identity dominant IS the BGV chop the dropout targets;
  judged NOT-A-HOLE (keying on beat_identity would misfire absurdly — its
  dense-fixture "dominant" is a synth pad; kick/snare/bass is the only
  honest read of "main kick/sub foundation"; rhythmic contrast is on the
  may-address list; the neutral pool already targets those stems).
  **TRAJECTORY WATCH-ITEM (→ residue, STANDING): a real groove-carrier
  signal is required before ANY dropout-surface widening — do not fake it
  from beat_identity.**
- **Execution semantics: none smuggled** — the lexical guard is real and
  covers the right strings.
- **Conscious drift exactly as enumerated;** the halee-only narrowing of
  the artifact-keys pin judged CORRECT with NO coverage loss (timbaland's
  intimate-path byte-silence re-pinned; quincy pinned by his own P-043
  surfaces).
- **Risk rows honest** — arithmetic reconstructed from the JSONs; halee
  HIGH upheld as the SAFER authoring vs the builder-flagged medium
  alternative; timbaland 80.9 a real read landing honestly under his 86.7
  subtractive economy (the packet permitted a winner flip and his lens
  coherently doesn't produce one).
- **P-042/P-043 guarantees intact;** reconstruction stays falsifiable.
- **Trajectory: this completes the user's Shape C arc** — the vocabulary's
  most aggressive family enters candidate-planning-only,
  engine-protected, reach-gated, the safety doctrine verbatim in
  code/constants/tests. Honestly remaining, ALL user-gated: quincy/halee
  authored dropout reach; further C-family expansion; the groove-carrier
  signal before any dropout widening; execution/apply semantics NEVER
  without explicit user re-gating.

## Residue (carried to `build-os/memory/residue.md`)

- **Accepted, recorded not fixed:**
  1. qa discrepancy #1 (task-premise) — `_lead_masked` is False on every
     fixture at HEAD; the masked-lead exclusion is provable SYNTHETICALLY
     only. Fine: the synthetic tests bite exactly.
  2. qa discrepancy #2 (filter bite surface) — removing the filter changes
     no shipped artifact bytes; the protection guarantee rests on the 4
     synthetic tests, which bite exactly.
  3. Reviewer residual — the AST-guard blind spot for a future
     profile-sourced global whose name lacks "prof" (today's code reads
     none; runtime differentials carry the real weight).
  4. **★★ STANDING TRAJECTORY WATCH-ITEM:** a REAL groove-carrier signal
     before ANY dropout-surface widening — never faked from beat_identity.
  5. Execution/apply semantics NEVER without explicit user re-gating (the
     safety line is standing doctrine).
- The residue list otherwise stays **ZERO** — all prior standing notes and
  the three named lessons retained.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-044** — `9fdb172` + `87635d3` +
  `f72f222` (+ this close commit) atop `80e9bd5` (= PR #22) — awaits the
  user's explicit word. The commits are pushed to the dev branch (standing
  go, pre-gates); NOT merged; no deploy/publish/secrets touched.
- **STAGED next: NOTHING — the user's sequenced arc is COMPLETE** (CLI ✓
  samples ✓ third producer ✓ analyzer extension ✓ mode-forking B ✓
  vocabulary C narrow ✓ dropout ✓). The orchestrator PRESENTS the open
  directions to the user (ALL user-gated): quincy/halee authored dropout
  reach · further C families (behind the groove-carrier watch-item where
  applicable) · a fourth producer · product-surface work (samples/README
  refresh for the new families) · anything else the user calls. Do NOT
  open anything blind.

---
_Closed by the archivist (2026-07-03). qa GREEN (1000 / 93/93 / Commit-1
iso 984 / 312-cell differential 0 mismatches / every winner unchanged /
sabotage 4/4 / halee's governance veto live at 48 < 50 / no-execution
guard 0 hits) + reviewer PASS (no must-fix; all adversarial attacks
defeated; single-model — Codex unavailable; the full suite independently
re-run at 1000). The safety line stands: dropout is an arrangement
proposal, not a destructive operation._
