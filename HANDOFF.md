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

### ★ P-062 — Multi-Lens Execution Brief (CLOSED 2026-07-30, dual-green)

The "from every angle" planning surface, built on the user's direction after the
Manus discussion (Manus = orchestration harness over Claude; the harness was
encoded as a **deterministic artifact** rather than wiring any hosted LLM into
the engine — P-025/P-031 policy: measurements decide, language explains, LLM =
draft-only).

- **What it is:** `execution-brief` — opt-in CLI (`--dir <artifacts>`) + the 36th
  cowork registry command. Six lenses quoting artifact numbers verbatim, five
  deterministic cross-lens contradiction rules, the mix plan re-cut into five
  execution phases (gain/static → masking carves → space/depth →
  section/automation → creative), and a fenced DRAFT-ONLY host-synthesis prompt
  block for any LLM copilot. `write_artifacts` untouched — corpus byte-identical
  **by construction** (the 30-file/16-tree pins never moved).
- **Commits:** `3e7ccc9` (renderer + CLI + tests, green in isolation 1467/0) +
  `3a7144f` (cowork surface 35→36, `API_VERSION` 1.0→1.1 per P-023's own rule,
  reviewer must-fix folded in by amend — nothing had been pushed, Commit-1
  untouched).
- **Gates:** QA GREEN (suite **1470/0/0**, regression 93/93, independent detached
  Commit-1 isolation, two count-conservation mutations proven red, determinism
  sha-proven). Reviewer **fix-then-pass → pass**: caught `_WIDTH_KEYWORDS`
  containing "width"/"widest", which appear in the repo's own *narrowing* planner
  strings — the mono rule could have asserted "the plan recommends widening" when
  the plan says narrow. Fixed to `("widen","wider","mid-side","mid/side")` +
  a silent-direction test. Single-reviewer both rounds (codex absent).
- **Receipt:** `build-os/receipts/P-062-multi-lens-execution-brief.md`.
- **Use on Happy Man:** after `analyze`, run
  `python3 -m logic_mix_os.cli execution-brief --dir <out dir>` — or request it
  in a Cowork session.

### The original two real-audio bugs (both halves now fixed)

The engine ran on a real 49-track song ("Happy Man") and real audio exposed two
bugs the synthetic fixtures could not:

1. **Section-count scaling** ("masked by 48" = 4 conflicts × 12 sections) →
   **FIXED by P-060** (dual-green: suite 1414, regression 93/93). Closed, pushed,
   **merge still gated.**
2. **Detector over-segmentation** (12 sections → fake `100/100`
   contrast/dynamics) → **FIXED by P-061 — CLOSED 2026-07-26, dual-green.**
   Pushed, **merge still gated** (a separate gate from P-060's).

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

### ★ P-061 is CLOSED — both gates green (2026-07-26)

An earlier qa/reviewer dispatch against `4cbee14` stalled and never returned;
both were re-run against the final implementation HEAD `d941ecc`.

- **QA GREEN.** Suite **1426 passed / 0 failed / 0 warnings**; regression
  **93/93, `critical_failures == []`**. **Commit-1 independently green in
  isolation** (detached at `4cbee14`, fixtures regenerated: 1420 passed / 0
  failed, regression 93/93) — the item the stalled gate never delivered. Safety
  grep `"inferred"` zero files; frozen set byte-identical; no new dependency.
  Non-vacuity proven by monkeypatch: neutering `_cap_sections` → `16 == 12` sole
  failure; neutering `_merge_short_sections` → `4.0 >= 7.0` sole failure;
  reverting `_GAP_SEC` → exactly 4 failures and nothing else.
- **REVIEWER: pass**, no must-fix. **Single-reviewer only — `codex` is not
  available, so no second model reviewed this diff.**
- **Receipt:** `build-os/receipts/P-061-detector-over-segmentation-calibration.md`.

### ★ The `_GAP_SEC = 5.0` ruling — ADJUDICATED AND ACCEPTED

**A widely-repeated framing was wrong and is corrected here.** Earlier notes said
"anything in [1.5, 6.5] fixes the erasure equally well." **It does not.**
`_debounce` fills gaps THEN drops short runs, so erasure happens exactly when
phrases `< MIN_RUN` **and** rests `> GAP`. At `_GAP_SEC = 1.5` an erasure window
stays **open for rests in (1.5s, 5.0s)** — and a 1-bar rest at 120bpm is 2.0s, a
2-bar rest at 96bpm is 5.0s. Lower plateau values fix the *probe*; only
`_GAP_SEC >= _MIN_RUN_SEC` fixes the *class*, making fragment-then-erase
structurally impossible (erasure would then require sub-floor bursts separated by
super-floor rests — the definition of an ornament).

**Accepted cost, named honestly:** the boundary class now lost is the re-entry
point of a 1.5–5s dropout at which *no other stem changes state* — the classic
drum-drop-before-chorus. Accepted because the loss is **local** under-segmentation
whereas erasure is **global and silent** (an erased stem corrupts every boundary
in the song, and hits the lead vocal precisely because phrasing-with-rests is what
vocals do); because a real drop-before-chorus has other stems moving on the same
frame so the boundary survives in practice; and because the residual boundary it
replaces was an artifact of `_merge_short_sections` dropping one boundary rather
than two.

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
2. **Merge P-061 to default?** ✓ CLOSED 2026-07-26 (dual-green, receipt written);
   **the merge itself is a separate, still-open gate.** It sits on top of P-060,
   so merging P-060 first (or both together) is the natural sequence.
   - **P-062 now stacks on top as well** (closed 2026-07-30, dual-green). Three
     closed packets — P-060, P-061, P-062 — plus the Thread B config update all
     sit on this branch awaiting the user's merge word; a single PR carrying the
     branch is the natural unit.
3. **Orchestrator update** — isolated PR to default, or folded into the merge?
4. **PR #12 is still OPEN against the abandoned `main` base** ("Hardening Packet
   11 — Typed LogicActionPayload Contract"). The only open PR on the repo; PRs
   #1–#11 from that era are all closed-unmerged. **Recommendation recorded, not
   actioned** (2026-07-26): **close it** — every contemporary was closed unmerged,
   its base is abandoned so it cannot merge as-is, and the apply-to-Logic surface
   it serves is an explicitly re-gated FUTURE direction. **Counter-case:** if the
   typed-payload design is still wanted, **rebase onto current default** rather
   than closing, so the work isn't lost. Left open because this is a product call,
   not bookkeeping.
5. ~~**P-024 bookkeeping.**~~ ✓ **RETIRED 2026-07-26** — delivered by P-051
   (the MCP server) + P-052 (E2E proof). **Do not build it.** The stale "ONLY
   remaining arc step" claim is struck in `current_state.md`.
   - ★ **But one item survived the retirement and is OPEN: the
     version-fingerprint guard never landed.** Verified — zero hits for
     `sha256|hashlib|md5|blake2|fingerprint` across `cowork.py`, `cowork_mcp/*.py`
     and `tests/test_cowork_contract.py`. What exists is `API_VERSION = "1.0"`, a
     hand-maintained literal whose only guard asserts `API_VERSION == "1.0"` —
     **a tautology against itself.** Change any command's params and it still
     passes, so **contract drift is currently undetected**, and the MCP tool
     schemas derive from that same surface. Low priority, own packet: hash the
     sorted contract surface and pin it as a golden.
6. **HAPPY MAN RE-RUN #2** — the real-world confirmation for both halves.

### Residue carried out of P-061 (non-blocking, recorded by the reviewer)

- `section_detector.py:199` — the inline comment "a breath / rest must not toggle
  a stem off" is **stale** for a 5.0s window; lines 57–79 carry the real semantics.
- `test_gap_fill_does_not_outgrow_the_section_floor`'s companion *behavioural*
  test uses `rest = MIN_SECTION_SEC + 1.0`, so it guards ~8.0s rather than the
  stated 7.0s ceiling. The invariant assertion covers the stated bound.
- **`MIN_SECTION_SEC = 7.0` has only 1.0s margin** over a genuine 4-bar section at
  120bpm (7.0s ≈ 3.5 bars). A fixture-shaped constant — the one most likely to
  need revisiting on real material with tempo drift.
- **A spacing-aware `_cap_sections`** is the named future packet that would let
  `MAX_SECTIONS` drop below 12.
- ★ **The pytest `-q` trap:** `pyproject.toml` sets `addopts = "-q"`, so running
  `pytest -q` silently suppresses the summary count line while still exiting 0.
  Use bare `python3 -m pytest` (or `-o addopts=""`) to get counts. This plausibly
  contributed to the earlier gate producing no usable output.

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
