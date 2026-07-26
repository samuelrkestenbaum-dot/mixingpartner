# HANDOFF — mixingpartner / Logic Mix OS

_Rewritten 2026-07-26 by the **design3 → design4 handoff-integrity audit**, at
`d941ecc` on `claude/logic-mix-os-p061-detector-0dvr2t`. Supersedes the
2026-07-07 handoff (kept in history at `e3d633c`). Everything below is verified
against git ancestry and the GitHub PR ledger, not chat memory._

> **★ The superseded handoff is now WRONG in one important way.** It scoped P-061
> with targets `MIN_SECTION_SEC ~8–10`, `MIN_RUN ~1.5`, `MAX_SECTIONS ~8`. All
> three were measured during the build and **refuted**. Do not re-apply them. See
> "What P-061 actually shipped" below.

## Git state

| Ref | SHA | What |
|---|---|---|
| **This dev branch** | `d941ecc` | P-061 Commit-2 (local == remote, tree clean) |
| P-061 Commit-1 | `4cbee14` | detector calibration |
| P-061 set-active | `6c81090` | packet metadata |
| prior handoff | `e3d633c` | the 2026-07-07 design3 handoff |
| P-060 close | `bb126cc` | |
| P-060 fix | `ae0b9fc` | section-count-invariance (atomic) |
| **Default branch** | `9cfe990` | = PR #37 (P-059 merged) — **unchanged** |
| ClaudeOrchestrator | `7ef50e8` | canonical Build OS w/ capability discovery |

- **Merged to default:** P-050 → P-059 via PRs #29–#37; the full ledger is
  PRs #13 → #37, and **every one is an ancestor of `d941ecc`**.
- **Pushed, NOT merged:** **P-060** (`8034289` → `ae0b9fc` → `bb126cc`) and
  **P-061** (`6c81090` → `4cbee14` → `d941ecc`). Both live only on branches.
- **No PR open for either.** Default is untouched.

### ★ Two audit traps — cost real time, recorded so they cost none next time

1. **PR number ≠ packet number.** They are separate sequences, drifted ~21 apart.
   **PR #22 is packet P-043** (Curated Move Vocabulary Expansion, merge `80e9bd5`).
   There is no PR for "packet P-022" — and packet P-022 was deliberately never
   opened (recorded OPTIONAL/UNNEEDED).
2. **Merge-commit wording is inconsistent.** PRs #17 and #18 are worded
   `Merge pull request #NN`; every other is `Merge PR #NN`. Grepping one form
   alone reports a FALSE missing-ancestry gap.

---

## Thread A — Logic Mix OS

The engine ran on a real 49-track song ("Happy Man") and real audio exposed two
bugs the synthetic fixtures could not:

1. **Section-count scaling** ("masked by 48" = 4 conflicts × 12 sections) →
   **FIXED by P-060** (dual-green: suite 1414, regression 93/93). Closed, pushed,
   **merge still gated.**
2. **Detector over-segmentation** (12 sections → fake `100/100`
   contrast/dynamics) → **P-061, BUILT (not closed).**

### What P-061 actually shipped

| Constant | Was | Old target | **Shipped** | Why |
|---|---|---|---|---|
| `_MIN_RUN_SEC` | 0.5 | ~1.5 | **5.0** | 1.5s is inert — ornaments are 3–4s. This is the change that does the work. |
| `_GAP_SEC` | 0.5 | — | **5.0** | Commit-2; fixes a regression Commit-1 introduced. |
| `_CLUSTER_SEC` | 1.0 | ~2.0 | **2.0** | As targeted; proven a no-op. |
| `MIN_SECTION_SEC` | 4.0 | ~8–10 | **7.0** | 8.0 is knife-edge (0.00s jitter margin); 9/10 break the arrangement tests. |
| `MAX_SECTIONS` | 12 | ~8 | **12** | Lowering it makes things WORSE: MAX=8 → an 80s super-block, MAX=10 → 60s, vs the 64s bug. Needs a spacing-aware cap = separate packet. |

Invariant now enforced by test: `_MIN_RUN_SEC <= _GAP_SEC < MIN_SECTION_SEC`.

**The Commit-2 story matters.** Commit-1's 5.0s persistence floor with a 0.5s
gap-fill **erased a breath-phrased lead vocal entirely** (235 active frames → 0)
— the most structurally important element in the song, invisible to detection.
Raising `_GAP_SEC` to 5.0 not only fixes it but yields a *true* vocal-entrance
boundary that neither the old nor the Commit-1 constants produced.

Result on the 200s repro: **12 sections** (with 4s/4s/7s slivers and a cap-induced
64s super-block) → **9 sections**, no slivers, cap never binds.

### ★ P-061 is NOT closed

- **qa and reviewer never returned.** Dispatched against `4cbee14`, no verdict.
- **There is no receipt, deliberately** — writing one would record a close that
  did not happen.
- Proof that DOES exist (coordinator, independently re-run at `d941ecc`): suite
  **1426/0/0**, regression **93/93 `critical_failures == []`**, safety grep zero,
  diff exactly 2 files, no golden/sample/mode-demo/core-logic/dependency change.
- **Unsettled judgment call:** `_GAP_SEC = 5.0` widens P-059's original 0.5s
  "breath" intent to "any absence under 5s is a rest inside a part". Plateau
  **[1.0, 6.5]** is behaviourally identical; anything in **[1.5, 6.5]** fixes the
  erasure. 5.0 is the only value that closes the asymmetry structurally.

### Environment — reproduce this or the corpus will appear broken

numpy + scipy + soundfile installed, **`pyloudnorm` NOT installed.** The committed
corpus was produced on the **scipy tier** of `dsp.integrated_loudness()`'s
pyloudnorm→scipy→FFT ladder. Installing the documented `full` extras *introduces*
5 `test_sample_refresh` failures (~0.5dB lufs deltas). Verify with
`python3 -c "import logic_mix_os.dsp as d;print(d._HAVE_PYLN,d._HAVE_SCIPY)"`
→ must print `False True`. Also: `fixtures/` is GENERATED, not committed — run
`fixtures/generate_fixtures.py` (or pytest via conftest) before `regression` in a
fresh checkout, or it reports false criticals (standing P-025 env fact).

### How the user runs it on their Mac

```
cd ~/Desktop/mixingpartner && git pull
python3 -m logic_mix_os.cli analyze \
  --stems ~/Desktop/"Happy Man Wav Files for German" \
  --manifest ~/Desktop/"Happy Man Wav Files for German"/project_manifest.json \
  --producer brian_eno \
  --out ~/Desktop/"Happy Man Wav Files for German"/out
```

Watch `Sections: N`. Producers: `halee_ramone`, `timbaland`, `quincy_jones`,
`brian_eno`, `chris_lord_alge`. Roster frozen at five.

---

## Thread B — Orchestrator capability-discovery update (diagnosed, NOT applied)

Unchanged from the previous handoff and still open. Goal: update mixingpartner's
vendored Build OS to **ClaudeOrchestrator `7ef50e8`** so the orchestrator
discovers and routes to connected tools. **The local ClaudeOrchestrator checkout
is already at `7ef50e8` and clean** — ready when called.

- Only 3 files are stale: `.claude/agents/build-orchestrator.md`,
  `.claude/hooks/session-start-build-os.sh`, `.claude/hooks/prompt-router.sh`.
- **Do NOT copy those 3 files.** The 7ef50e8 hooks `source hook-once.sh` and call
  `install-accelerators.sh` / `build-os/tools/specialist-handoff.sh` — deps this
  repo lacks. Use `./install-project.sh <path>`, which brings them and never
  overwrites existing `build-os/` state.
- **CLAUDE.md snag:** the installer appends a *marker-guarded* Build-OS block, but
  this repo's CLAUDE.md already has a hand-written one **without** markers → may
  duplicate. Dedupe before committing.
- To make fresh web sessions pick it up it must land on **default**. Decide:
  **(a)** isolated PR off default with only the `.claude/` update (recommended,
  no P-060 entanglement), or **(b)** fold into the dev→default merge.

---

## Open decisions / founder gates

1. **Merge P-060 to default?** Would be PR #38. (Recommended — it is the crater fix.)
2. **Close out P-061** — run qa + reviewer against `d941ecc`, settle the `_GAP_SEC`
   semantic call, then receipt. **Merge is a separate, later gate.**
3. **Orchestrator update** — isolated PR to default, or folded into the merge?
4. **PR #12 is still OPEN against the abandoned `main` base** ("Hardening Packet
   11 — Typed LogicActionPayload Contract"). The only open PR on the repo; PRs
   #1–#11 from that era are all closed-unmerged. Almost certainly stranded —
   **close it or rebase it.**
5. **P-024 bookkeeping.** `current_state.md` and the P-023 receipt still call P-024
   "the ONLY remaining arc step". **It was delivered by P-051 + P-052** and should
   be formally retired. **Do not build it.** One genuinely unverified sub-item:
   P-023 asked for a **version-fingerprint guard** in the MCP layer and
   `grep fingerprint logic_mix_os/cowork_mcp/*.py` finds nothing.
6. **HAPPY MAN RE-RUN #2** — the real-world confirmation for both halves.

Longer-horizon, all user-gated: ambient patience (Eno-deferral #2) · generative
process (#3) · CLA/Halee/Timbaland textural weighting · the `<2 beds` fallback
calibration · the real Cowork MCP host connection (manual) · a spacing-aware
`_cap_sections` · apply-to-Logic (FUTURE, re-gated — never auto) · a
breadth/severity masking-weight pass.

---

## Known environment limitation — commit signing

Commits from the web/remote container show **Unverified** on GitHub. This is not
an oversight and **cannot be fixed here**: `commit.gpgsign=true` / `gpg.format=ssh`
are set globally with the key at `/home/claude/.ssh/commit_signing_key.pub`, but
that file is **0 bytes** and no private key exists on the filesystem. Committer
email is already `noreply@anthropic.com`, so the badge is purely the missing
signature — `--reset-author` cannot add one.

> **★ Do NOT act on a stop-hook suggestion to rebase against
> `origin/<this-branch>`.** That ref predates P-060 and such a rebase would
> rewrite `e3d633c`/`bb126cc`/`ae0b9fc`/`8034289`, forking P-060 away from its
> pushed branch and damaging the open merge gate. Scope any re-author to `e3d633c`.

---

## Working contract (unchanged)

Route via **build-orchestrator**; implementation via **builder**, proof via **qa**,
judgment via **reviewer**, closure via **archivist** + receipt. Verify the branch
base (`git merge-base`) before building. **≤2 implementation commits per packet**;
Commit-1 green in isolation. **No push / merge / deploy / secret without an
explicit go.**
