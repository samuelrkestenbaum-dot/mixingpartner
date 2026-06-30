# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE
- **Packet id:** P-008
- **Title:** History-aware next pass (the OUTCOME side of the learning loop)
- **Authority:** build (trajectory work, not hardening)

## Why (trajectory)

P-007 closed the taste→governance side of the loop. P-008 closes the OUTCOME
side: `plan_next_pass` currently ignores recorded mix-pass outcomes, so it can
re-recommend a move that just made things worse. P-008 makes it history-aware —
opt-in, bounded, evidence-tagged — so a regressed move is demoted and revert
candidates surface.

## ⚠️ HARD BACKWARD-COMPAT GATE

When NO `history` is supplied, `plan_next_pass` MUST be **byte-identical to today**
— all 125 tests + 68 doctrine-regression invariants stay green, unchanged. The
history logic applies ONLY when `history` is explicitly passed. The `evidence` key
is present ONLY on candidates history actually moved (absent otherwise — P-007's
`taste_adjustments` discipline).

## Seam (verified)

- `next_pass_planner.py:17` `plan_next_pass(records, doctrine_score, masking_report,
  sections_analysis)` → add trailing `history: Optional[List[Dict]] = None`.
  `None`/`[]` → existing body unchanged + return. Provided → run existing body to
  build `candidates`, then apply a pure reprioritizer BEFORE the sort/take-5.
- **No pipeline re-plumbing:** `pipeline.py:196-198` (the only prod caller) passes
  no history → default `None` → identical. `cowork.py:137` reads pipeline output,
  unaffected. **Zero `memory.py` edits** (`history()` already serves the list;
  history is passed IN). A thin accessor need = flag-and-stop, not a silent add.

## History shape consumed (verified — `memory.py:84-94`)

- Per-pass dict: `improved` / `got_worse` / `revert_candidates` are **score-delta
  strings keyed by `SCORE_KEYS`** (e.g. `"section_contrast_score 70->62"`) — NOT
  titles. `next_recommended` IS the list of prior move **titles** (top 3).
- **The one piece of new glue:** a module-level `_MOVE_TARGET` map (planner move
  `title` → the `SCORE_KEYS` member it targets), because `got_worse` speaks score
  keys and `next_recommended` speaks titles. Pin it in code; titles with no clear
  target map to nothing (left untouched — conservative). Builder confirms exact
  pairings against `SCORE_KEYS` (`memory.py:18-22`).

## Behavior (precise, conservative, deterministic, OPT-IN)

1. Gate: `history in (None, [])` → unchanged.
2. Use only `history[-1]` (most recent pass) — bounded/predictable; document it.
3. **Demote (not delete):** parse `history[-1].got_worse` → regressed score-key set.
   For each candidate whose `_MOVE_TARGET[title]` is in that set AND whose title is
   in `history[-1].next_recommended`, subtract a fixed bounded `HISTORY_DEMOTE`
   (e.g. 40) from its priority int, floored so it never goes negative. It drops in
   rank but survives; if all regressed, relative order preserved + sane top-5.
4. **Revert surfacing:** if `history[-1].revert_candidates` non-empty, append ONE
   `"Revert last pass"` move whose `detail` names the regressed targets
   (deterministically ordered); dedup by title.
5. **Evidence:** any history-touched candidate gets an `evidence`/`reason` field,
   present ONLY when history moved it, e.g. `"demoted: prior pass recorded
   section_contrast_score 70->62 after this move"`. String-stable.
6. Deterministic: pure fn of `(candidates, history[-1])`; fixed order; no time/IO/random.

## In scope

- `logic_mix_os/planners/next_pass_planner.py` — optional `history` arg,
  `_MOVE_TARGET` map, `HISTORY_DEMOTE` bound, pure `_apply_history` helper,
  conditional `evidence` field.
- `tests/test_next_pass_history.py` (new) — P-008 planner tests.
- `tests/test_governance_taste.py` (Commit-2, additive) — the folded
  `drum_room_bloom` narrower-path test (closes the P-007 residue test gap;
  mirror `test_narrower_taste_lowers_width_bloom_identity_bounded`).

## Out of scope (explicit)

- Pipeline re-plumbing / threading history into `analyze()` (the live wire is a
  separate **P-008b**); `pipeline.py`/`cowork.py` untouched.
- `memory.py` / `record_pass` changes (the producer shape is the contract).
- P-007b live taste surface; event-logging producers; creative `_KIND_SCORES`;
  `doctrine_score`/safety surfaces.

## Test plan (no DAW/network — constructed history + fixtures)

- (1) **Byte-identical default:** for all `analyzed` fixtures, `plan_next_pass(...)`
  == `history=None` == `history=[]`, no `evidence` key.
- (2) **got_worse demotes:** history entry with `next_recommended` incl.
  `"Section contrast"` and `got_worse` incl. `"section_contrast_score 70->62"` →
  that move's rank lower than no-history (or falls out of top-5), with the evidence
  line naming the target.
- (3) **Revert surfaced:** non-empty `revert_candidates` → exactly one
  `"Revert last pass"` move naming the targets.
- (4) **All-regressed degrades gracefully:** sane non-empty top-5, no negative
  priorities.
- (5) **Determinism:** two identical calls → identical output.
- (6) **drum_room_bloom fold-in** (Commit-2, in `test_governance_taste.py`): a
  narrower-taste test on a `drum_room_bloom` variant (symmetric to width_bloom,
  currently untested).

## Branch base

- `claude/logic-mix-os-hardening-12-7hbeh1` @ HEAD `8c18df7` (clean). Default
  `claude/dreamy-turing-z0oxll` @ `694d19d`.

## Plan (≤2 commits)

1. **Commit 1 (test-first, green in isolation):** `tests/test_next_pass_history.py`
   + the `next_pass_planner.py` change in one commit; passes its own tests
   standalone; suite 125→~130; regression 68/68.
2. **Commit 2 (additive):** the `drum_room_bloom` test in `test_governance_taste.py`;
   suite stays green. (If the 3-file footprint risks discipline, split as a tiny
   P-008-fixup and say so — but it should fit.)

## Regression-safety argument

1. `compare_snapshots` (`regression.py:86-145`) **records but never diffs**
   `next_pass_titles` (captured at `:82`, ignored by the comparator).
2. Doctrine invariant #4 (`regression.py:191-195`) iterates `next_pass`, but the
   regression runs `analyze` → planner with NO history → byte-identical items.
3. Score-drift checks read `doctrine_score`, which the planner never writes.
   → 68/68 structurally immune; new behavior reachable ONLY via the explicit arg.

## Guardrails

- Build authority; deterministic; opt-in; history only REORDERS/ANNOTATES existing
  candidates — it can never manufacture a destructive or doctrine-vetoed move; no
  network/subprocess/AppleScript/`.logicx`/`RealLogicSessionAdapter`.

---
_Confirmed P-008 on the user's "keep going / skate to where the puck" — trajectory
work (outcome side of the learning loop). Builder implements exactly this;
archivist clears on close._
