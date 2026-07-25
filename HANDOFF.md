# HANDOFF — mixingpartner / Logic Mix OS

_Session handoff written 2026-07-07. Everything below is on GitHub; nothing is
uncommitted. Point a fresh session at the **dev branch**
`claude/logic-mix-os-hardening-12-7hbeh1` to continue — all Build OS memory lives
there and is self-documenting._

## Git state (all pushed)

- **Dev branch:** `claude/logic-mix-os-hardening-12-7hbeh1` @ `bb126cc` (local ==
  remote, tree clean).
- **Default branch:** `claude/dreamy-turing-z0oxll` @ `9cfe990`.
- **Merged to default:** P-050 → P-059 (PRs #29–#37).
- **Pushed but NOT merged:** **P-060** — 3 commits ahead of default
  (`8034289` set-active → `ae0b9fc` fix → `bb126cc` close).
- Continue the build on the **dev branch** (`build-os/memory/` +
  `build-os/packets/active_packet.md` carry the live state).

---

## Thread A — Logic Mix OS (the mix-decision engine)

**Context:** The engine ran on a real 49-track song ("Happy Man") for the first
time. It works and gives coherent, producer-voiced advice — but real audio
exposed **two bugs** the synthetic fixtures could not:

1. **Section-count scaling** ("masked by 48" = 4 conflicts × 12 sections) →
   **FIXED by P-060** (just closed, dual-green: suite **1414**, regression
   **93/93**). Masking conflicts were counted once per section; now deduped to
   distinct conflicts. Surgical corpus move — only dense-derived artifacts
   shifted (one correction: dense's Kick/Bass low-end 2×→1×); the 5 sample trees
   + 3 other fixtures byte-identical; no decisions changed.
2. **Detector over-segmentation** (12 sections → fake `100/100`
   contrast/dynamics) → **P-061, staged & scoped, NOT built.**

**Immediate next steps (in order):**

1. **Merge P-060 to default** — the open gate. Clean single-packet PR (dev is
   fast-forwarded onto default). Would be PR #38.
2. **Build P-061** — detector calibration. Fully scoped in
   `build-os/packets/active_packet.md`: raise `MIN_SECTION_SEC`→~8–10s, raise
   `MIN_RUN`→~1.5s, widen `CLUSTER`→~2s, lower `MAX_SECTIONS`→~8; adaptive novelty
   floor only if needed. **Byte-stable** for the scoring corpus (the detector only
   fires when `len(sections) ≤ 1`); re-pins only the ~10 detector tests.
3. **User re-runs Happy Man** for a clean read — sane vocal/emotional/space *and*
   honest contrast/dynamics.

**How the user runs it on their Mac** (already set up in `~/Desktop/mixingpartner`,
editable `pip install -e .`):

```
cd ~/Desktop/mixingpartner && git pull
python3 -m logic_mix_os.cli analyze \
  --stems ~/Desktop/"Happy Man Wav Files for German" \
  --manifest ~/Desktop/"Happy Man Wav Files for German"/project_manifest.json \
  --producer brian_eno \
  --out ~/Desktop/"Happy Man Wav Files for German"/out
```

Watch `Sections: N` (was 1 pre-detection). Producers: `halee_ramone`, `timbaland`,
`quincy_jones`, `brian_eno`, `chris_lord_alge`.

**Longer-horizon (all user-gated, in `active_packet.md`):** ambient patience
(Eno-deferral #2) · generative process (#3) · CLA/Halee/Timbaland textural
weighting · the `<2 beds` fallback calibration · the real Cowork MCP host
connection (manual) · apply-to-Logic (FUTURE, re-gated) · a breadth/severity
masking-weight pass (residue). Roster frozen at five producers.

---

## Thread B — Orchestrator capability-discovery update (diagnosed, NOT applied)

**Goal:** make mixingpartner's vendored Build OS orchestrator **discover and route
to all connected tools** (MCP servers, skills, `/`-commands, subagents) by
updating it to **ClaudeOrchestrator @ `7ef50e8`** — that commit contains the
"Discover and use already-connected capabilities" feature; its
`build-orchestrator.md` has a full **"Capability routing"** section (and the key
refinement: the orchestrator is a Read/Grep/Glob/Bash subagent, so it must **name**
the skill / `/`-command / `mcp__*` tool explicitly for the main session to run it).

**What I found (do NOT naively copy 3 files):**

- Only **3 files** in mixingpartner's `.claude/` are stale vs 7ef50e8:
  - `.claude/agents/build-orchestrator.md`
  - `.claude/hooks/session-start-build-os.sh`
  - `.claude/hooks/prompt-router.sh`
  - The other 4 agents, the 3 commands, and `settings.json` are **already at
    7ef50e8**.
- **⚠️ Gotcha:** the 7ef50e8 hooks `source hook-once.sh` and call
  `install-accelerators.sh` / `build-os/tools/specialist-handoff.sh` — **new
  dependencies mixingpartner does not have yet.** Copying just the 2 hooks would
  break them (missing `hook-once.sh`). Use the **installer**, which brings the
  deps.
- **⚠️ CLAUDE.md snag:** `install-project.sh` appends a *marker-guarded* Build-OS
  block to `CLAUDE.md`, but mixingpartner's `CLAUDE.md` already has a hand-written
  Build OS section **without** those markers → it may **duplicate**. Verify /
  dedupe the CLAUDE.md block before committing.

**Recommended approach:**

```
cd /path/to/ClaudeOrchestrator && git fetch && git checkout 7ef50e8
./install-project.sh /path/to/mixingpartner   # full engine + deps; KEEPS build-os/ state
# then: review the diff, dedupe the CLAUDE.md block, commit
```

`install-project.sh` never overwrites existing `build-os/` project state
(memory/packets/receipts) — the P-041…P-060 history is safe.

**"Make fresh Code tasks pick it up":** the updated `.claude/` must land on the
**default branch** (`claude/dreamy-turing-z0oxll`) — fresh web tasks branch from
default. Two paths, a real decision:
- **(a) Isolated PR** from a new branch off default with *only* the `.claude/`
  update (clean; recommended — no P-060 entanglement).
- **(b)** Fold it into the dev→default merge (drags P-060 along).

---

## Open decisions waiting on the user

1. **Merge P-060?** (recommended — it's the crater fix)
2. **Build P-061 next?** (recommended — the other half of the Happy Man fix)
3. **Orchestrator update** — isolated PR to default, or fold into the dev-branch
   merge?

---

## Key SHAs

| Ref | SHA | What |
|---|---|---|
| dev branch HEAD | `bb126cc` | P-060 close |
| P-060 fix | `ae0b9fc` | section-count-invariance (atomic) |
| P-060 set-active | `8034289` | packet metadata |
| default branch | `9cfe990` | PR #37 (P-059 merged) |
| ClaudeOrchestrator target | `7ef50e8` | canonical Build OS w/ capability discovery |
