# Receipt — P-007: Taste profile feeds governance (first closure of the learning loop)

- **Date:** 2026-06-29
- **Authority:** build (trajectory work — first closure of the learning loop, NOT hardening)
- **Branch base (merge-base):** product base `68e88d0` on
  `claude/logic-mix-os-hardening-12-7hbeh1`; default branch
  `claude/dreamy-turing-z0oxll` @ `694d19d` (merge-base with HEAD = `694d19d`).

## What it does

The recorded operator taste profile (`memory._derive_taste` statements) now
**biases variant governance** — opt-in, bounded, and evidence-tagged. Concretely:

- An optional `taste_profile` argument (default `None`) is threaded through
  `govern_variant` / `govern_branches` / `run_governance`.
- A pure `_apply_taste` helper plus a module-level `_TASTE_KIND_BIAS` map
  (derived **verbatim** from the statements `_TASTE_MAP` emits) translate a
  profile statement → (variant kind, signed identity delta).
- A hard bound `TASTE_MAX_DELTA = 15` (strictly **< 30**, the existing intimate
  truth nudge), re-clamped to `[0, 100]`.
- A new `taste_adjustments` evidence field appears **only when an adjustment
  actually applies** (absent — not `[]` — otherwise).

Result: two operators with different taste now get **different governed winners
from the same song**. Proven — a narrower-taste profile flips the governed
winner `chorus_lift_A` → `chorus_lift_C`.

## Scope

- **In:**
  - `logic-mix-os/logic_mix_os/governance.py` (+75/−6 net) — optional `taste_profile`
    arg on the 3 functions, the `_apply_taste` helper, the `_TASTE_KIND_BIAS` map,
    the bounded adjustment, and the `taste_adjustments` evidence field.
  - `logic-mix-os/tests/test_governance_taste.py` (new, **13 tests**).
- **Out (explicit):**
  - Pipeline re-plumbing / `analyze()` signature — **untouched**.
  - The live cowork/cli per-operator opt-in surface — **deferred as P-007b**.
  - P-008 (history-aware next pass).
  - New event-logging producers.
  - Creative `_KIND_SCORES`; `_TRUTH_ALIGNMENT` table edits.

## Commits

- `bd08f28` P-007: taste profile biases governance (opt-in, bounded) — **the
  single product commit** (governance.py + test_governance_taste.py).
- `600f8ae` Confirm P-007 (taste profile feeds governance) as active packet —
  non-product (memory/active_packet confirm).

## QA proof (GREEN)

- **Suite:** `python -m pytest` → **125 passed**, 0 failed / 0 skipped /
  0 warnings.
- **Regression:** `python -m logic_mix_os.cli regression` → **68/68, 0 critical,
  0 warnings** — the doctrine-invariant gate held.
- **Commit-1 iso:** worktree at `bd08f28` → **125 passed** (21 taste+governance),
  regression **68/68** → green in isolation.
- **Backward-compat (the HARD gate):** default path is **BYTE-IDENTICAL** across
  all 3 fixtures — `run_governance` default == `taste_profile=None` ==
  `taste_profile=[]`, and **no `taste_adjustments` key** is present. A positive
  control proved the path is live (an applied profile does produce the field /
  the shift).
- **Bound verified:** 10 stacked profile statements clamp to **+15** (no overflow
  past `TASTE_MAX_DELTA`).
- **Safety surfaces untouched:** `validate_action_safety` / kill-switches /
  `_TRUTH_ALIGNMENT` / `pipeline` / `analyze` — none modified.
- **Scope:** exactly the 2 files.
- **Safety grep:** none found.
- **UI smoke:** N/A (no UI surface touched).

## Review

- **Verdict:** **pass.**
- **Backward-compat:** byte-identical default path confirmed.
- **Inviolability proven:** an intimate-lean `width_bloom` has `align = 45 < 50`
  → vetoed **unconditionally**; pushing the taste maximally wider raised its
  identity to 84 but it was **still rejected** — taste cannot flip a
  doctrine-vetoed variant. Taste nudges identity; it never clears a truth-lock
  veto, a kill-switch, or a risk-class-5 refusal.
- **Determinism:** pure function of `(variant kind, statements)`, fixed
  application order, no time/I-O/random.
- **Verbatim mapping:** `_TASTE_KIND_BIAS` keys are the exact `_TASTE_MAP`
  statements.
- **Test-first:** the builder reproduced `ImportError` / `TypeError` before the
  implementation landed.
- **Regression structurally safe:** the doctrine regression never reads
  `.governance`, so a governance-only change cannot move the 68 invariants.
- **Codex second-eyes:** NOT available.

## Product Trajectory Check

**MILESTONE — first closure of the learning loop.** Recorded operator taste now
influences recommendations: opt-in, bounded (`±15`), evidence-tagged, and
doctrine-inviolable. Memory is **no longer purely write-only on the governance
axis** — a real consumer of recorded signals now exists. This is the *consumer*
(taste → governance) half of the loop; the *outcome* half (history →
next-pass) is the natural follow-on (P-008).

## Residue

- **Deferred / follow-up packets:**
  - **P-008 — History-aware next pass** (the OUTCOME side of the loop):
    `plan_next_pass` should consume `mix_pass_history`
    (improved / got_worse / revert_candidates) so the system does not
    re-recommend a move that regressed. The next high-leverage trajectory packet.
  - **P-007b — Live opt-in surface:** wire a real per-operator `taste_profile`
    from `memory_dir` into a pipeline/cowork run — must stay **explicit
    per-operator** so the byte-identical-by-default guarantee survives into the
    pipeline.
  - **Test gap (low priority):** the `drum_room_bloom` narrower-taste path in
    `_TASTE_KIND_BIAS` is data-symmetric with `width_bloom` but currently
    untested — add a test (fold into P-008).
  - **Event-logging producers (reframed):** now that a CONSUMER of recorded
    signals exists, wiring `validation_check` / `taste_feedback` producers is
    more justified — but still net-new feature work behind the same product
    decision. Kept deferred.
- **Known risks:**
  - Commits on this branch are **unsigned** (environment limitation — empty
    0-byte signing key; container runs as root). Author/committer are correctly
    `noreply@anthropic.com`; GitHub shows "Unverified" (missing signature only,
    not misattribution). Not a fix-it item.
  - Test env: numpy + pytest are not preinstalled; the full suite needs
    `pip install -e ".[dev]"` from `logic-mix-os/` first.

## Open boundaries (awaiting explicit go)

- **Product commit `bd08f28` is local-only as of this close** — this archivist
  did not push. Any push updates the already-open **PR #13** (base
  `claude/dreamy-turing-z0oxll`) — do so only under the user's explicit push-go.
- Out-of-authority items unchanged: real macOS/Logic test surface (no-real-DAW
  guardrail); controlled Class-3 apply path (guardrail-gated).
