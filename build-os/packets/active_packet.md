# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — **P-058 — Real-Session On-Ramp CLOSED (2026-07-06).**
  qa GREEN (suite 1359 → **1390 / 0**; regression **93/93** with 0 warnings;
  Commit-1 iso **1390**) + reviewer **PASS (no must-fix)**. Both gates
  independently re-ran the suite. Receipt:
  `build-os/receipts/P-058-real-session-on-ramp.md`.

## Last closed — P-058 — Real-Session On-Ramp

The pivot from "the engine runs on synthetic fixtures" to "a real Cowork session
can be driven through it and the build side can read what it did." A PLAN-ONLY
on-ramp + capture + docs packet — **NO scoring change**. Three deliverables:

- **D1 — Manifest scaffolder** (`onramp.py`): exported WAV stems → a VALID draft
  `project_manifest.json` (title from folder; `sample_rate`/`bit_depth` probed
  read-only via `wave.open("rb")`; one `tracks[]` per file with a GUESSED
  `source_kind` grounded in `SOURCE_KINDS`; a one-section stub; `_draft: true` +
  `_needs_review`). Deterministic; `--force`-guarded. The name→kind heuristic
  (`guess_source_kind`) was extracted from `source_material_detector.py` into ONE
  shared pure helper both the detector and scaffolder use — no drift.
- **D2 — Field-session capture** (`bundle_field_session` + `capture-session`):
  READ/COPY only — the 3 memory JSONs + plan/verdict artifacts +
  `session_summary.json`. Raw audio EXCLUDED (double-guarded: copy-time extension
  filter over 13 audio exts + `field_sessions/.gitignore`). Idempotent.
- **D3 — `docs/REAL_SESSION.md`** (5-step Cowork walkthrough) + a
  `docs/COWORK_MCP.md` cross-link. Every command verified against the live CLI.

**Two commits** (local + PUSHED to the dev branch under the standing go — NOT
merged): `6f25360` (Commit-1 — product + tests + convention, 7 files +724/−15,
**GREEN IN ISOLATION at 1390**) + `1671c0c` (Commit-2 — docs only, 2 files
+124). Parent chain: `1671c0c` → `6f25360` → `4ad08f0` (set-active) → merge base
`6355743` (= PR #35 — P-057 merged to default). Verified `git merge-base HEAD
6355743` = `6355743` — a clean single-packet PR. Engine / governance / creative /
constants byte-identical; no new dependency (stdlib + first-party only); safety
grep 0 reach.

## OPEN USER GATE

- **The merge of P-058** — `6f25360` + `1671c0c` (+ the close commit) atop
  `6355743` (= PR #35) — a clean single-packet PR (the branch is fast-forwarded
  onto default). Awaits the user's explicit word. Pushed to the dev branch
  (standing go, pre-gates); NOT merged; no deploy/publish/secrets touched.

## STAGED next — NOTHING opened blind

The orchestrator PRESENTS the user-gated directions. The **FIRST REAL-AUDIO
SESSION (the user exports one real song's WAV stems)** is now the HIGHEST-VALUE
item — the real-audio validation gap is UNBLOCKED (the on-ramp exists) but still
OPEN (the engine has only ever run on synthetic fixtures). Alongside it: the real
Cowork host connection (manual) · ambient patience (Eno-deferral #2) · generative
process (Eno-deferral #3) · CLA / Halee / Timbaland textural weighting · the
`<2 beds` neutral-fallback calibration · a sixth producer (roster frozen at
five) · apply-to-Logic (future, re-gated — never auto; the safety line stands) ·
anything else the user calls. Do NOT open anything blind.

---
_Cleared by the archivist on P-058 close (2026-07-06). One packet at a time:
builder → qa + reviewer → archivist → receipt._
