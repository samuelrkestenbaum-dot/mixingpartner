# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-058 — Real-Session On-Ramp** (opened on the user's
  "go with recs", 2026-07-06). Base `6355743` (default tip — **P-057 already
  merged via PR #35**; the earlier stale "OPEN USER GATE" for P-057 is void).
  Verify `git merge-base HEAD 6355743` = `6355743`. PLAN-ONLY.
- **Baseline to protect:** suite **1359** / regression **93/93** / the five
  producers + sample trees + mode demos byte-stable / the engine, profiles, 15
  axes, `governance.py`, kill-switches, dropout filter, and `constants.py`
  vocabularies UNTOUCHED (READ-only).

## P-058 — Real-Session On-Ramp

Move from "the engine runs on synthetic fixtures" to "a real Cowork session can
be driven through it and the build side can read what it did." Three deliverables
— on-ramp + capture + docs only, **NO scoring change**. All four design forks
resolved (user "go with recs"): A = exclude raw audio + no audio-write; B = guess
into `source_kind` + `_needs_review`; C = new `docs/REAL_SESSION.md`; D = one
`onramp.py`.

### D1 — Manifest on-ramp (scaffolder)

- New module `logic_mix_os/onramp.py` (stdlib-only: `pathlib`, `json`, `wave`).
  `scaffold_manifest(stems_dir, *, force=False) -> dict` + `write_manifest_draft(
  stems_dir, out_path, *, force=False)`.
- **REUSE the shipped name→kind heuristic** — factor `source_material_detector`'s
  keyword/fallback logic into a shared pure helper so the scaffolder and the
  detector share ONE table (no second, drift-prone copy). Grounded in
  `constants.SOURCE_KINDS` (the closed 17-value vocabulary) — **never invent a
  kind**.
- Emits a VALID draft `project_manifest.json`: `project` (title from folder name;
  sample_rate/bit_depth probed read-only from the WAV header via stdlib `wave`;
  tempo/key blank), one `tracks[]` entry per audio file with the GUESSED
  `source_kind` written in (Fork B), a fillable one-section `sections` stub
  (0:00→end), an `intent` stub (required keys, empty values), and annotations
  `_draft: true` + a `_needs_review` list of low-confidence guesses. **Do NOT
  analyze audio to derive section timecodes** (keeps it deterministic + in-scope).
  Deterministic: sorted file order → byte-identical on re-run.
- CLI subcommand `scaffold-manifest --stems <dir> [--out <path>] [--force]`.
  **Refuses to overwrite an existing manifest without `--force`.**

### D2 — Field-session capture convention

- New tracked dir `logic-mix-os/field_sessions/` with `README.md` (the
  convention) + an inner `.gitignore` excluding audio extensions (a stray stem
  can never be committed — belt-and-suspenders atop the repo's existing
  stem-gitignore precedent).
- `bundle_field_session(memory_dir, out_bundle_dir, *, artifacts_dir=None) ->
  dict` in `onramp.py` (stdlib `shutil`/`json`, **READ/COPY only**): copies the
  three memory JSONs (`mix_pass_history.json` / `decision_ledger.json` /
  `taste_profile.json`) + the plan/verdict artifacts + writes a
  `describe_session`-style `session_summary.json`. CLI `capture-session
  --memory-dir <dir> --out <bundle> [--artifacts <dir>]`.
- **Fork A: raw audio EXCLUDED by default; NO audio-write path in this packet**
  (trimmed-reference deferred as a future gated knob).

### D3 — Cowork setup doc (docs only)

- New `docs/REAL_SESSION.md` (5 steps): `pip install -e .` → the MCP
  `{command,args}` config for Cowork/Claude Desktop → drive a first session with
  an explicit `memory_dir` → optionally re-export a bounce for re-analysis (the
  engine already supports `--bounce`/`--reference` on `analyze`/`generate-plan`
  and a `compare-reference` subcommand — verified) → `capture-session` +
  commit-back. One-line cross-link added to `docs/COWORK_MCP.md`.

## Safety boundary (binding)

No `osascript`, no shelling into a DAW, no `.logicx`/session/audio write, no
execution backend. The scaffolder writes ONLY a draft `project_manifest.json` to
a user-specified path (a dev-tool write — fine); capture only READS/COPIES
existing artifacts; no stem WAV is generated or committed. New code imports
stdlib + numpy only — **no new dependency; if one is genuinely needed, STOP AND
FLAG.**

## Non-scope (binding)

Do NOT touch: `doctrine_engine.py`, the five producer profile JSONs, the 15 axes,
`governance.py`, kill-switches, the dropout filter, `creative.py` scoring,
`constants.py` vocabularies (READ `SOURCE_KINDS`, never edit). Roster stays five —
no new producer. Sample trees + mode demos byte-stable. Tests run against the
SYNTHETIC fixtures only — no real audio shipped. Regression golden corpus stays
**93** (no new fixture enters it).

## Commit shape (≤2; Commit-1 green in isolation)

- **Commit-1 (product + tests + convention — green in isolation):** `onramp.py`
  (scaffolder + capture bundler), the two CLI subcommands, `field_sessions/`
  (README + inner `.gitignore`), the shared name→kind helper refactor, and new
  tests (`tests/test_onramp_scaffold.py`, `tests/test_field_session_capture.py`).
  Builds and passes alone.
- **Commit-2 (additive docs):** `docs/REAL_SESSION.md` + the `COWORK_MCP.md`
  cross-link. Docs prose only — no new numeric pins (avoids touching the
  README-count guards).

## Required proof (qa reports exact)

1. Full suite GREEN — baseline **1359 / 0** → 1359 + new tests (exact count).
2. **Regression 93/93 UNCHANGED.**
3. **Commit-1 green in isolation.**
4. **Safety grep = 0 reach** in the new modules (no
   `osascript`/`subprocess`/`.logicx`/audio-write/DAW mutation; imports stdlib +
   numpy only — mirror the `cowork_mcp` source-scan discipline).
5. **Scaffold→valid-manifest proof:** for EACH of the 4 fixtures,
   `scaffold_manifest(<fixture>/stems)` → JSON-valid draft with the required
   shape → `load_manifest` + `Project.from_inputs` + `analyze()` SUCCEEDS;
   determinism (byte-identical on re-run); the `--force` guard refuses to
   overwrite.
6. **Capture proof:** run a fixture session into a temp `memory_dir` (record pass
   + decision + taste) → `bundle_field_session` → bundle contains the 3 memory
   JSONs + plan/verdict artifacts + `session_summary.json`, **excludes `*.wav`**,
   idempotent.
7. **Docs present:** `docs/REAL_SESSION.md` (5 steps) + `field_sessions/README.md`.
8. **Byte-stability:** the five profiles + sample trees + mode demos
   sha256-unchanged; engine / governance / creative / constants unchanged.

## Route after builder

builder (D1+D2 → Commit-1; D3 → Commit-2) → qa (proof 1–8) → reviewer → archivist
(receipt `build-os/receipts/P-058-real-session-on-ramp.md` + memory advance).
**Commit only — no push/merge/deploy without the user's explicit go** (the
standing dev-branch push-go covers the pre-gate push).

---
_Set active by the orchestrator + confirmed on the user's "go with recs"
(2026-07-06), after the P-057 merge (PR #35 → `6355743`). One packet at a time:
builder → qa + reviewer → archivist → receipt._
