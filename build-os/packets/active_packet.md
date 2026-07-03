# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — opened on the user's "Go" (2026-07-03) after the
  P-046 merge report, down the orchestrator's presented recommendation
  (the hardening/docs pairing flagged at the last two closes).
- **ID / Title:** **P-047 — Directory-Driven Producer Sweeps + Docs
  Residues**
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `24b5ca7` (= PR #25 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1110** / regression **93/93** / all
  four committed sample trees byte-stable / ZERO engine or profile
  changes — this is a TEST + DOCS hardening packet; runtime behavior is
  untouched by definition.

## Why this packet (the accumulated residue it clears)

1. **★ The P-045 reviewer residue (the headline item):** the
   profile-sweeping guards parametrize a HARDCODED three-producer tuple
   (`PRODUCERS = ("halee_ramone", "timbaland", "quincy_jones")` in
   `tests/test_mode_forking.py`, imported by
   `test_move_vocabulary_expansion.py` and
   `test_negative_space_dropout.py`) — so brian_eno is NOT swept by the
   structural guards (P-045 carried equivalents inside its own files),
   and a FIFTH producer would not grow the sweeps passively. Make the
   tuple DIRECTORY-DRIVEN (scan the producers dir the way the CLI/loader
   already does) so every current and future profile is swept
   automatically.
2. The two P-045 reviewer marginal residues this closes as a
   consequence: eno's no-mode/unknown-mode zero-extended-emission
   coverage beyond dropout ids; eno gaining the same
   default-flow/explicit-authoring sweep coverage the three have.
3. **The P-046 docs residues:** README line ~46 "the three example
   projects" → four (fixture-count staleness — the generator builds 4);
   the `test_four_way_differential.py` docstring (~line 875) that
   under-describes 2-of-4 committed trees; the P-042-era "all three
   producers" comment in `test_mode_forking.py` (~line 122) that the
   sweep change naturally corrects.

## Scope

1. **Directory-driven sweeps (Commit-1):** replace the hardcoded
   3-tuple with discovery from the producers directory (sorted, stable
   order). Every per-producer DATA TABLE keyed by the old tuple
   (DEFAULT_FLOW_IDS, per-producer expected sets/values in the three
   sweep files) gains its brian_eno row with values CAPTURED from the
   real engine first — extending data, never weakening assertions. The
   sweeps will now run over eno (passive growth by design — enumerate
   the exact new parametrization counts). Where a sweep pins something
   eno legitimately does differently (authored-neutral default, his
   reach table), the pin rows express HIS authored values — the
   assertions themselves stay identical in strength.
2. **Docs residues (Commit-2):** the three wording fixes above (README
   fixture count; the four-way docstring; any comment the sweep change
   exposes as stale). Docs/docstrings only.

## Non-scope (binding)

ZERO changes to engine code (.py under logic_mix_os/), profiles,
fixtures, goldens, committed sample trees. No new guards beyond the
sweep extension's natural growth (this is not a new-proof packet — it
is making EXISTING proofs producer-complete). No behavior changes of
any kind. No fifth producer. No merge until qa + reviewer dual-green
(the merge stays a user gate).

## Orchestrator recon (binding on the builder)

- Discovery should reuse the same source of truth the product uses
  (`_PRODUCERS_DIR` scanning, as `cli._resolve_producer` does) — not a
  second hand-rolled glob that could drift. If importing the private
  name into tests is distasteful, note it: the `_PRODUCERS_DIR`
  private-name accessor is itself an accepted standing residue note
  from P-039.
- Some swept tests may embed per-producer literals inline (not in
  tables). Each such site is a conscious enumerated extension (eno row
  added) — list every one.
- If ANY sweep FAILS on eno, that is a REAL FINDING (a structural
  guarantee P-045 believed was covered equivalently but wasn't) — STOP
  and report it before changing anything; do not paper over it by
  weakening the assertion.
- The suite count will grow by the new eno parametrizations —
  enumerate the exact arithmetic per file (the house discipline).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the directory-driven discovery + all per-producer data
  rows for eno (captured, then pinned) — full suite green in isolation.
- **Commit-2:** the docs/docstring residues — no test-collection
  changes.

---
_Set active by the orchestrator on the user's "Go" (2026-07-03). One
packet at a time: builder → qa + reviewer → archivist → receipt._
