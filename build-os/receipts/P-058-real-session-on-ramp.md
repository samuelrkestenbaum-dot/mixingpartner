# Receipt — P-058: Real-Session On-Ramp

- **Packet:** P-058 — Real-Session On-Ramp. The pivot from "the engine runs on
  synthetic fixtures" to "a real Cowork session can be driven through it and the
  build side can read what it did." **A PLAN-ONLY on-ramp + capture + docs packet
  — NO scoring change.** Three deliverables: a manifest scaffolder (D1), a
  field-session capture bundler (D2), and the Cowork walkthrough doc (D3). All
  four design forks resolved on the user's "go with recs": **A** = exclude raw
  audio + no audio-write; **B** = guess into `source_kind` + `_needs_review`;
  **C** = new `docs/REAL_SESSION.md`; **D** = one `onramp.py`.
- **User authority + decision:** opened on the user's "go with recs"
  (2026-07-06) after the P-057 merge (PR #35 → default `6355743`). The real-audio
  validation gap, the real Cowork host connection, ambient patience, generative
  process, CLA/Halee/Timbaland textural weighting, the `<2 beds` fallback, and a
  sixth producer all stayed USER-GATED and were NOT touched — this packet is the
  on-ramp ONLY.
- **Date:** 2026-07-06
- **Status:** CLOSED — qa GREEN **(suite 1359 → 1390 / 0; regression 93/93 with 0
  warnings; Commit-1 iso 1390)** + reviewer **PASS (no must-fix)**. Both gates
  independently re-ran the suite.

## Scope

**In (the confirmed packet spec — the three deliverables):**

1. **D1 — Manifest scaffolder.** NEW `logic_mix_os/onramp.py`:
   `scaffold_manifest(stems_dir)` / `write_manifest_draft(...)` + CLI
   `scaffold-manifest --stems <dir> [--out] [--force]`. A folder of exported WAV
   stems → a VALID draft `project_manifest.json`: `project` (title from folder;
   `sample_rate`/`bit_depth` probed read-only from the WAV header via
   `wave.open("rb")`), one `tracks[]` entry per file with a GUESSED `source_kind`
   (grounded in `constants.SOURCE_KINDS`, the closed 17-value vocab; defensive
   fallback to `unknown`), a fillable one-section `sections` stub, an `intent`
   stub, `_draft: true`, and a `_needs_review` list of low-confidence guesses.
   Deterministic (sorted file order → byte-identical on re-run); refuses to
   overwrite without `--force`.
2. **The detector refactor.** `guess_source_kind` extracted from
   `analyzers/source_material_detector.py` into a SHARED pure helper that both the
   detector and the scaffolder use — **ONE name→kind table, no drift-prone second
   copy.** `_infer_kind` delegates; `_KEYWORD_RULES` byte-unchanged.
3. **D2 — Field-session capture.** `bundle_field_session(memory_dir, out,
   artifacts_dir=)` + CLI `capture-session`. READ/COPY only: the 3 memory JSONs
   (`mix_pass_history` / `decision_ledger` / `taste_profile`) + plan/verdict
   artifacts (allow-list `.json/.md/.html`) + a `session_summary.json`. **Raw
   audio EXCLUDED** (double-guarded: copy-time extension filter over 13 audio
   exts + the `field_sessions/.gitignore`). Idempotent.
4. **The `field_sessions/` convention.** NEW tracked dir under `logic-mix-os/`
   with `README.md` (the convention) + an inner `.gitignore` excluding 13 audio
   extensions (belt-and-suspenders atop the copy-time filter — a stray stem can
   never be committed).
5. **D3 — `docs/REAL_SESSION.md`** (5-step Cowork walkthrough) + a
   `docs/COWORK_MCP.md` cross-link.

**Explicitly out (binding non-scope, held):**

- **No scoring change.** ZERO change to `doctrine_engine.py`, `governance.py`,
  `creative.py`, the 15 axes, kill-switches, the dropout filter, or the
  `constants.py` vocabularies (`SOURCE_KINDS` READ, never edited). All
  byte-identical, diff-proven.
- **No audio-write / no execution backend (Fork A).** No `osascript`, no shelling
  into a DAW, no `.logicx`/session/audio write. `wave.open` is read-only `"rb"`;
  no stem WAV generated or committed. Trimmed-reference audio-write deferred as a
  future gated knob.
- **No new dependency.** New code imports stdlib + first-party only — not even
  numpy. `pyproject.toml` blob-identical (absent from the diff).
- Roster stays five — no new producer. Sample trees + mode demos + fixture stems
  byte-stable. Regression golden corpus stays **93** (no new fixture enters it).
- No real audio shipped — tests run against the SYNTHETIC fixtures only.
- Merge — a user gate (see Open boundaries). No deploy/publish/secrets.

## Commits and base

- **Two commits (≤2-commit rule honored; local + PUSHED to the dev branch under
  the standing go — NOT merged):**
  - `6f25360` — "P-058: real-session on-ramp (scaffolder + field-session
    capture)" — **7 files, +724/−15**: NEW `logic_mix_os/onramp.py` (270 lines —
    D1 scaffolder + D2 capture); the detector refactor
    (`analyzers/source_material_detector.py`, +38/−15 — `guess_source_kind`
    extracted to the shared helper, `_infer_kind` delegates); the two CLI
    subcommands (`cli.py`, +45); `field_sessions/README.md` (43) +
    `field_sessions/.gitignore` (16, 13 audio exts); NEW
    `tests/test_onramp_scaffold.py` (173, 24 tests) +
    `tests/test_field_session_capture.py` (139, 7 tests). **GREEN IN ISOLATION at
    1390** (product + tests + convention land in one commit, so it is self-green).
  - `1671c0c` — "P-058: docs — REAL_SESSION.md walkthrough + COWORK_MCP
    cross-link" — **2 files, +124**: NEW `docs/REAL_SESSION.md` (120 — the 5-step
    walkthrough) + `docs/COWORK_MCP.md` (+4 — the cross-link). Docs prose only —
    no new numeric pins.
- **Commit-1 green in isolation:** 1390.
- **Parent / base chain:** `1671c0c` → `6f25360` → `4ad08f0` (set-active —
  "build-os: set P-058 (Real-Session On-Ramp) active — user go with recs") →
  merge base `6355743` (= PR #35 merge — P-057 already merged to default).
- **Merge base with default:** verified at close — `git merge-base HEAD 6355743`
  = `6355743`; the dev branch is fast-forwarded onto default, so a P-058 PR
  carries only `6f25360` + `1671c0c` + the close commit — a clean single-packet
  PR.
- **Push state:** PUSHED to the dev branch under the standing go **BEFORE
  qa/reviewer ran** (both gates validated the final SHAs). **NOT merged** — the
  merge of P-058 is a user gate.

## QA proof (GREEN — both gates independently re-ran the suite)

- **Suite:** 1359 → **1390 passed, 0 failed** (+31: 24 scaffold + 7 capture);
  regression **93/93** UNCHANGED with **0 warnings** (no score/confidence drift);
  the corpus is **4 fixtures**.
- **Commit-1 iso:** **1390** (product + tests + convention in one commit).
- **Per-file collect:** `test_onramp_scaffold.py` = **24**,
  `test_field_session_capture.py` = **7**.
- **The detector refactor is PURE (the one real risk — it feeds `source_kind` →
  doctrine):** same kinds and confidences (**0.82 / 0.6 / 0.55 / 0.4**), same
  evidence, same lowercase-substring semantics; `_KEYWORD_RULES` **byte-unchanged**;
  `_infer_kind` delegates to the shared helper. **80 consumer tests pass
  unchanged**; a **38-name old-vs-new equivalence battery = 0 mismatches**; the
  regression golden snapshot (per-track `source_kind` + score bands) = **93/93
  with 0 warnings** → no producer / sample-tree output moved.
- **Scaffold → valid-manifest proof (all 4 fixtures):**
  `scaffold_manifest(<fixture>/stems)` → JSON-valid draft with the required shape
  → `load_manifest` + `Project.from_inputs` + `analyze()` **SUCCEEDS**;
  deterministic (byte-identical on re-run); the `--force` guard **refuses to
  overwrite** an existing manifest.
- **Capture proof:** a fixture session recorded into a temp `memory_dir` (pass +
  decision + taste) → `bundle_field_session` → bundle contains the 3 memory JSONs
  + plan/verdict artifacts + `session_summary.json`; **a planted `.wav` in BOTH
  the artifacts dir AND the memory dir is EXCLUDED** from the bundle (the
  double-guard bites); idempotent.
- **Docs present:** `docs/REAL_SESSION.md` (5 steps) +
  `field_sessions/README.md`. Every command in `REAL_SESSION.md` reviewer-verified
  against the LIVE CLI parser (`scaffold-manifest`, `capture-session`,
  `memory-record`, `feedback`, `analyze --bounce`, `compare-reference`) + the four
  MCP side-effecting commands — no phantom flags.
- **Boundary held (structural):** safety grep of `onramp.py` + the CLI additions
  = **0 reach** (no `osascript` / `subprocess` / `.logicx` / `os.system` /
  audio-write / DAW); `wave.open` is read-only `"rb"`; imports stdlib + first-party
  only (not even numpy) — **no new dependency** (`pyproject.toml` blob-identical,
  ABSENT from the diff).
- **Byte-stability:** the diff is **10 files** (the 9 product/docs files +
  `active_packet.md`). `doctrine_engine.py`, `governance.py`, `creative.py`,
  `constants.py` vocab, the five producer JSONs, all sample trees, mode demos, and
  fixture stems are **blob-identical** (byte-unchanged).

## The user's required proof — every clause met

full suite GREEN ✓ (1359 → **1390 / 0**, +31) · regression **93/93 UNCHANGED**
with 0 warnings ✓ · Commit-1 green in isolation ✓ (1390) · safety grep = 0 reach
in the new modules ✓ (stdlib + first-party only; `wave` read-only; no
DAW/exec/audio-write) · scaffold → valid-manifest for EACH of the 4 fixtures ✓
(`load_manifest` + `Project.from_inputs` + `analyze()` succeeds; deterministic;
`--force` guard refuses) · capture bundle correct + `*.wav` EXCLUDED (both dirs) +
idempotent ✓ · docs present (`REAL_SESSION.md` 5 steps + `field_sessions/README.md`)
✓ · byte-stability (five profiles + sample trees + mode demos + engine / governance
/ creative / constants unchanged) ✓ · no new dependency ✓.

## Reviewer verdict — PASS (no must-fix)

- The detector refactor is the one real risk (it feeds `source_kind` → doctrine),
  and it is genuinely PURE: one shared table, `_infer_kind` delegating,
  `_KEYWORD_RULES` byte-unchanged, the 38-name equivalence battery clean, and the
  regression golden at 93/93 with 0 warnings — no producer output moved. The
  scaffolder never invents a kind (grounded in `SOURCE_KINDS`, defensive
  `unknown` fallback), is deterministic, and refuses to overwrite. Capture is
  READ/COPY-only with the raw-audio exclusion double-guarded. Fork A held — no
  audio-write, no DAW reach. The `REAL_SESSION.md` commands were verified line by
  line against the live CLI parser (no phantom flags).
- **Codex second-eyes:** not separately reported for P-058; consistent with the
  recent single-model posture (Codex unavailable in the prior packet). No
  second-model verdict is claimed — recorded as such.
- **Process notes (reviewer, non-blocking):** (a) `scaffold_manifest`'s `force`
  param is inert — signature parity with `write_manifest_draft`, but the function
  performs no write (see Residue 3); (b) Commit-1 landed product + tests together
  (squashed), so test-first can't be independently verified from the diff — the
  tests are substantive/non-vacuous and map to the done-criteria (see Residue 4).
  Neither is a defect.

## Residue (carried to `build-os/memory/residue.md` — accepted standing notes)

1. **★ THE REAL-AUDIO GAP IS NOW UNBLOCKED BUT NOT YET CLOSED — the standing TOP
   open item.** The on-ramp exists, but the engine has STILL only ever run on
   synthetic fixtures. The single highest-value next step is a **FIRST REAL-AUDIO
   SESSION** — and it needs the USER to export one real song's WAV stems (the one
   input the build side cannot manufacture): scaffold from real stems → run the
   pipeline → sanity-check the plan/verdict → capture + commit the bundle back →
   the build side finally iterates on real data.
2. **The real Cowork ↔ MCP-server host connection is now DOCUMENTED
   (`REAL_SESSION.md`) but still a MANUAL user step** — pip install locally + drop
   the `{command, args}` into Cowork's config + drive a session. Never executed
   with the real host.
3. **`scaffold_manifest`'s `force` param is inert** (signature parity with
   `write_manifest_draft`; the function performs no write) — documented, harmless;
   optionally drop in a future cleanup. A process note, not a defect.
4. **Test-first provenance caveat:** Commit-1 landed product + tests together
   (squashed), so test-first can't be independently verified from the diff — the
   tests are substantive/non-vacuous and map to the done-criteria; a provenance
   note, not a defect.
5. **Prior standing notes + named lessons retained:** the P-057 residues (CLA
   textural stays DEFERRED; Halee/Timbaland textural untouched/needs grounding;
   the `<2 beds → 55.0` two-producer neutral-fallback calibration knob; the
   packet-prediction-precision note) and the remaining Eno-deferral analyzers
   (ambient patience #2, generative process #3); the ★★ groove-carrier trajectory
   watch-item; the safety line.

## Open boundaries

- **★★ THE OPEN USER GATE: the merge of P-058** — `6f25360` + `1671c0c` (+ this
  close commit) atop `6355743` (= PR #35) — a clean single-packet PR (the branch
  is fast-forwarded onto default). Awaits the user's explicit word. The commits
  are pushed to the dev branch (standing go, pre-gates); NOT merged; no
  deploy/publish/secrets touched.
- **STAGED next: NOTHING opened blind.** The orchestrator PRESENTS the user-gated
  directions, with the **FIRST REAL-AUDIO SESSION (the user exports real stems)**
  now the highest-value item, alongside: the real Cowork host connection (manual)
  · ambient patience (Eno-deferral #2) · generative process (Eno-deferral #3) ·
  CLA / Halee / Timbaland textural weighting · the `<2 beds` fallback calibration
  · a sixth producer (roster frozen at five) · apply-to-Logic (future, re-gated —
  never auto; the safety line stands) · anything else the user calls. Do NOT open
  anything blind.

---
_Closed by the archivist (2026-07-06). qa GREEN (suite 1359 → **1390 passed, 0
failed**; +31 = 24 scaffold + 7 capture; regression 93/93 with 0 warnings;
Commit-1 iso 1390; per-file collect test_onramp_scaffold.py=24 /
test_field_session_capture.py=7; the detector refactor PROVEN pure — 80 consumer
tests unchanged, a 38-name old-vs-new equivalence battery = 0 mismatches, the
golden snapshot unmoved; scaffold → `analyze()` succeeds on all 4 fixtures,
deterministic, `--force` guarded; capture excludes `*.wav` from both dirs,
idempotent; safety grep 0 reach, no new dependency, byte-stability diff-proven) +
reviewer PASS (no must-fix; single-model). P-058 makes the engine REACHABLE for a
real session: `onramp.py` turns exported WAV stems → a valid draft manifest (via
ONE shared name→kind table both the detector and scaffolder use), `capture-session`
returns a session's decisions + analysis (raw audio double-excluded) for
commit-back, and `REAL_SESSION.md` documents the Cowork host connection. A
PLAN-ONLY packet — NO scoring change; engine / governance / creative / constants
byte-identical; no new dependency. The REAL-AUDIO VALIDATION GAP is now UNBLOCKED
but OPEN, awaiting the user's real stems (the standing top open item). The merge is
the open user gate._
