# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 ("Merge P-047 now.
  Then do product-surface refresh… This is the right next skate: make the
  now-powerful system explain itself before adding more depth."). P-047
  merged FIRST as PR #26 → default tip `645c925`, per the user's
  sequencing.
- **ID / Title:** **P-048 — Product-Surface Refresh: Producer + Mode Demo
  Artifacts** (the user's title, verbatim)
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `645c925` (= PR #26 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **1122** / regression **93/93** / the
  FOUR committed sample trees byte-stable / ZERO runtime behavior changes
  — docs/samples/demo clarity ONLY.

## The user's intent (verbatim authority)

"The system's substrate is now ahead of its product surface." Make the
completed capabilities VISIBLE: dynamic producer discovery ·
producer-specific mode behavior · profile-authored mode reach · extended
move families · negative-space dropout · arrangement_lift /
ensemble_rebalance · honesty/confidence labels · governed safety caps.

**Required language on the product surface (verbatim):**
- "engine owns move vocabulary / profile owns mode reach / governance
  owns safety cap"
- "dropout is an arrangement proposal, not a destructive operation"

## Required demos (the user's seven, verbatim)

Add or refresh examples showing:
1. same stems + different producer
2. same stems + same producer + different mode
3. same problem + different mode → different candidate variant set
4. same mode name + different producer → profile-attributable difference
5. Quincy reaching arrangement_lift / ensemble_rebalance
6. Timbaland reaching negative_space_dropout only where authored
7. Halee/Ramone remaining default/reference-safe

## Scope (docs / samples / demo clarity — NOT runtime behavior)

Update: README usage examples · CLI examples · sample invocation
commands · sample output artifacts if already committed · producer/mode
comparison documentation · short explanations of the extended move
families, governed dropout, and directory-driven sweeps.

**Small hardening touch (rides along ONLY if clearly non-runtime /
assertion-strengthening; do not let it expand the packet):** the two
stale test names in test_negative_space_dropout.py + the missing
eno/brian token in `_PRODUCER_TOKENS` (test_mode_forking.py ~873).

## Orchestrator recon (binding on the builder)

- **P-046 already landed part of this surface** — the four committed
  default-flow trees, the "Four producers, same stems" table, the
  "Modes are behavior" section, and the extended-families paragraph
  with the safety line. Demo 1 is DONE (keep/reference it). P-048's
  genuinely NEW surface is demos 2–7: MODE-LEVEL comparison artifacts
  and their documentation — EXTEND the P-046 surface, do not duplicate
  or rewrite what is already accurate and pinned.
- **Recommended demo shape (builder finalizes):** the full 30-artifact
  tree per mode would explode the committed surface — use the LIGHTEST
  faithful unit the REAL CLI emits (e.g. the `creative` subcommand's
  output with `--producer`/`--mode`) committed under a new
  `examples/mode_demos/` (or similar) — one small committed artifact
  set per demo row, rendered by verbatim documented invocations,
  staleness-pinned byte-for-byte in the P-040 pattern, no-absolute-path
  asserted, plus a README (or examples-local doc) comparison table of
  the candidate-id sets that the pins guarantee. Every documented set
  must equal pinned reality: conservative four-way {A,B,C,D}/{B,C,D}/
  {B,C}/{B,D}; halee dramatic vs conservative vs deconstructive;
  quincy ensemble_balance/experimental reaching his families; timbaland
  negative_space (reaching) vs groove_pocket (not); eno untouched or
  included as the neutral-default contrast — CAPTURE FIRST, THEN PIN.
- **The doctrine language** goes where users will read it (the README
  mode section header/intro), verbatim, exactly once each — no
  aspirational prose; every claim checkable against committed bytes or
  pinned tests (the P-046 discipline; "unpinned claims: none material"
  is the bar).
- The FOUR existing trees are NOT regenerated (a non-byte-identical
  fresh render = discovered bug → STOP and report). Doctrine scores,
  goldens, profiles, engine code untouched.

## Required proof (the user's, verbatim)

suite clean · regression clean · zero runtime behavior changes ·
samples intentionally refreshed · README/examples match current CLI
behavior · no producer outputs drift except committed sample refreshes ·
the hardening touch, if included, is assertion-strengthening only.

## Non-scope (the user's, verbatim)

No fifth producer. No analyzers. No Quincy/Halee dropout reach. No new
move families. No scoring changes. No governance changes. No safety
changes. No CLI-semantics changes. No merge until qa + reviewer
dual-green (the merge stays a user gate).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the mode-demo artifacts (real-CLI renders) + their
  staleness/content pins + the hardening touch (test renames +
  token-list strengthening) — full suite green in isolation.
- **Commit-2:** README/examples documentation only (zero collection
  changes).

---
_Set active by the orchestrator on the user's explicit go (2026-07-03),
after the P-047 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
