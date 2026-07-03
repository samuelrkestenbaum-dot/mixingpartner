# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — confirmed by the USER 2026-07-03 ("My call: Merge
  P-043 now. Then open negative-space dropout, but narrowly and
  conservatively."). P-043 merged FIRST as PR #22 → default tip `80e9bd5`,
  per the user's sequencing.
- **ID / Title:** **P-044 — Negative-Space Dropout Move Family** (the
  user's title, verbatim)
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1` atop merge base
  `80e9bd5` (= PR #22 merge; verify with `git merge-base`).
- **Baseline to protect:** suite **950** / regression **93/93** / the
  halee committed sample tree byte-stable / halee + quincy flows
  byte-stable everywhere.

## The user's decision (verbatim authority)

**"This family is higher-risk because it sounds like 'mute/drop
something,' so the first implementation must be candidate-planning only,
not execution semantics."**

**THE DOCTRINE (the user's safety line, verbatim): "dropout is an
arrangement proposal, not a destructive operation."**

- **Scope decision:** build EXACTLY ONE new extended kind:
  `negative_space_dropout`.
- **What it MAY address (the user's list — nothing else):** supporting
  clutter · non-lead decorative layers · sectional over-density ·
  rhythmic contrast opportunities · background texture reduction.
- **What it MUST NOT touch — never target or imply dropping:** lead
  vocal · hook_candidate · masked lead protection · core groove carrier ·
  main kick/sub foundation · primary emotional-hierarchy element · source
  integrity.
- **Who reaches it (initial authored reach):** **Timbaland: yes —
  experimental / contrast / negative-space modes** (his mode names:
  `experimental`, `dramatic_contrast`, `negative_space`).
  **Halee/Ramone: no by default. Quincy: no by default**, unless
  explicitly authored later. "This keeps it from becoming a general
  'remove stuff' move."

## Acceptance bar (the user's, verbatim)

- `negative_space_dropout` exists as an extended curated kind
- reach-gated admission works
- Timbaland can reach it only where authored
- Halee/Ramone and Quincy do not drift
- risk caps bind
- lead/hook/core-groove protections override it
- no execution/mute/apply semantics are introduced
- sample-tree drift is conscious
- differential proof attributes changes to authored reach

## Orchestrator implementation notes (recon, binding on the builder)

- **The P-043 seam carries this**: one `CREATIVE_EXTENDED_KINDS` entry +
  curated variants + authored reach. Engine code changes should be
  limited to the curated variant content and any TARGET-PROTECTION
  helper the protections require — no seam/loader redesign.
- **Protections are structural, not prose.** The curated dropout
  variants must resolve targets through a protection filter that
  EXCLUDES: lead-vocal tracks, hook candidates, core groove carriers
  (kick/sub/main beat foundation), and the primary emotional-hierarchy
  element. If no legitimate target survives the filter, the variant does
  NOT emit (no phantom targets — existing house discipline). This must
  be provable: a test where only protected elements exist → zero dropout
  emission. The protection is ENGINE-owned (profile-agnostic) — no
  profile may author it away.
- **Plan-only semantics**: the changes text stays at the existing
  recommendation level (the plan-text vocabulary already used by the
  curated pool), reversibility-tagged like every variant
  (`non_destructive_duplicate_track` pattern); NO new apply/execute/mute
  machinery, no new artifact semantics beyond the established
  reach/fork surface.
- **Risk honesty**: this is the aggressive family — curate the
  translation/mono risks honestly (medium at minimum where honest); the
  cap must bind against the authored rows (the P-043 two-layer pattern).
  All THREE profiles author kind_scores + truth_alignment rows (rows
  everywhere, no silent inheritance); ONLY Timbaland authors reach.
- **Conscious drift, precisely bounded**: `dramatic_contrast` is
  Timbaland's DEFAULT mode, and the user explicitly authorized reach on
  it — so Timbaland's default flow and his committed sample tree
  (`examples/sample_output_timbaland/`) WILL drift. That drift is
  CONSCIOUS: regenerate his tree via the VERBATIM README invocation,
  keep the staleness pin at FULL strength, enumerate every changed
  artifact; doctrine scores must NOT move (creative layer only — the
  60.9 headline stays); if a dropout variant WINS a branch in his flow,
  that is his authored taste — enumerate the winner change honestly.
  The HALEE tree stays byte-identical; halee + quincy flows stay
  byte-identical EVERYWHERE (their acceptance clause).
- **Differential proof shape (the P-043 pattern):** same mode name +
  same stems → timbaland (authored) emits dropout candidates,
  halee/quincy do NOT on any mode; reconstruction from the JSONs on
  disk extends to the third extended kind; synthetic profiles prove
  data-not-producer; suppression beats reach; the cap refuses over-cap
  reach; the protection filter overrides reach (reached-but-protected →
  not emitted, surfaced honestly).

## Non-scope (binding)

Exactly one new kind — no other families, no second dropout variant
family. No execution/apply/mute machinery. No new analyzers. No
doctrine/scoring changes (doctrine_engine untouched; doctrine scores
byte-stable). No safety/governance/veto changes; never weaken the caps,
the P-042/P-043 guarantees, or the vocal/lead protections. No
per-producer engine branches. No authored reach for halee/quincy (their
gate is proven synthetically). No merge until qa + reviewer dual-green
(the merge stays a user gate).

## Commit shape (≤2, Commit-1 green in isolation)

- **Commit-1:** the extended kind + curated dropout variants WITH the
  structural protection filter + rows in all three profiles + guards —
  ZERO behavioral change (no shipped profile reaches), full suite green
  in isolation, both sample trees untouched.
- **Commit-2:** Timbaland's authored reach (experimental /
  dramatic_contrast / negative_space) + the differential proof + the
  conscious enumerated deltas (his tree regeneration, default-flow pin
  updates, any winner changes).

---
_Set active by the orchestrator on the user's explicit go (2026-07-03),
after the P-043 merge report. One packet at a time: builder → qa +
reviewer → archivist → receipt._
