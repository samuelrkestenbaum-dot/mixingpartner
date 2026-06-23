# Logic Mix OS

A **local-first mix decision system** for Logic Pro stems. Given a folder of
exported stems and a `project_manifest.json`, it produces a section-aware,
emotionally intelligent, **Logic-native mix plan** in the style of Roy Halee and
Phil Ramone — specific enough that a human mixer (or Claude Cowork) can open
Logic Pro and know exactly what to do.

It is **not** an auto-mixer, a preset generator, or a mastering tool. It is a
producer-engineer *judgment* layer:

- protect the vocal,
- honour the performance,
- create depth,
- distinguish **heard** from **felt**,
- make sections **contrast**,
- avoid foreground clutter,
- deconstruct stock loops,
- prefer **automation over compression**, **depth over EQ**, **subtraction over addition**,
- and keep the song's emotional truth at the centre.

## Guarantees (hard constraints)

- **Local only** — no network, no uploads.
- **Non-destructive** — never writes to your source audio; recommends duplicates/presets.
- **No Logic automation in v1** — it produces a plan and a checklist; you (or Cowork) execute.
- **Deterministic** — same inputs produce the same JSON/Markdown artifacts.
- **Honest** — every recommendation carries evidence, confidence, and a risk class. Class 5 (destructive) actions are never recommended.

## Install

Only `numpy` is required. `soundfile`, `pyloudnorm`, `scipy`, and `jsonschema`
are optional and improve format support / loudness accuracy / validation — the
tool degrades gracefully without them (stdlib `wave` loader, FFT-domain loudness
estimate, built-in schema checker).

```bash
cd logic-mix-os
pip install -e .          # core (numpy only)
pip install -e ".[full,dev]"   # optional: soundfile, pyloudnorm, scipy, pytest
```

## Quick start

The repository ships a fixture generator instead of large binary audio. Generate
the three example projects (deterministic, seeded):

```bash
python fixtures/generate_fixtures.py
```

Then run a full analysis:

```bash
logic-mix-os analyze \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --out ./output/dense
```

(Or without installing: `python -m logic_mix_os.cli analyze ...`.)

A ready-made example of the output lives in [`examples/sample_output/`](examples/sample_output).

## CLI

**Analysis & plan**

| Command | Purpose |
|---|---|
| `analyze` | Full analysis → every JSON/Markdown artifact + dashboard |
| `detect-identities` | Source-material + instrument-identity detection |
| `analyze-sections` | Per-section metrics + contrast |
| `generate-plan` | Generate the mix plan |
| `render-checklist --plan mix_plan.json` | Logic checklist from a saved plan |
| `validate-output --output DIR` | Validate an output directory against the schemas |
| `compare-reference --bounce a.wav --reference b.wav` | Reference-track delta |
| `audit` | Source-aware auditors (live / synth / sampler / loop) |
| `status` | Operator "control room" status surface (text) |
| `dashboard` | Local self-contained HTML control room (the §50 screen map) |

**Creative & governance**

| Command | Purpose |
|---|---|
| `creative [--mode]` | Variant branches (A/B/C/D) + scoring + governed winners |
| `governance` | Truth lock, listener panel, stop conditions |
| `mixer-feedback --tone` | Diagnosis as mixer-facing feedback (5 tones) |
| `suggest-creative-variants --plan mix_plan.json` | Quick creative hypotheses |

**Memory, album, orchestration, bridge**

| Command | Purpose |
|---|---|
| `memory-record --memory-dir --name` | Record a mix pass (score deltas + ledger) |
| `memory-show --memory-dir` | Mix-pass history, taste profile, ledger size |
| `feedback --memory-dir --label` | Record taste feedback → taste profile |
| `album --projects DIR` | Album-level coherence across songs |
| `cowork --list` / `cowork --name CMD` | Claude Cowork command surface (32 commands) |
| `export-actions --plan --format json\|applescript\|shortcuts` | Bridge export |
| `bridge-dryrun --plan [--review-mode]` | Simulate applying actions (never executes) |
| `regression [--fixtures] [--update-golden]` | Golden-output + doctrine regression |

Common flags: `--stems`, `--manifest`, `--out`, plus optional `--bounce` and `--reference`.

The `dashboard` command writes a single self-contained `dashboard.html` (inline
CSS, no JS, no server, no network) realising the section-50 control room — open
it with `file://`. `status` is the terminal-native equivalent.

## Inputs

- A folder of exported stems (WAV; AIFF/FLAC/OGG with `soundfile`).
- A `project_manifest.json` (see [`examples/project_manifest.example.json`](examples/project_manifest.example.json)) describing
  track names, optional `source_kind` / `known_identity` hints, tempo, key,
  intent (emotional truth + negative constraints), and section markers.
- Optional stereo bounce (`--bounce`) for section analysis — otherwise a summed
  mixdown of the stems is used.
- Optional reference track (`--reference`).

## Outputs

Written to `--out`:

**JSON** — `source_material.json`, `track_identity.json`, `track_analysis.json`,
`section_analysis.json`, `depth_map.json`, `masking_report.json`,
`mix_plan.json`, `doctrine_score.json` (+ `reference_delta.json` if a reference
is supplied).

**Markdown** — `source_material_report.md`, `track_identity_report.md`,
`halee_ramone_mix_verdict.md`, `logic_action_checklist.md`,
`next_pass_recommendations.md` (+ bonus `automation_plan.md`,
`section_contrast_report.md`).

## How it works (the three maps)

Every decision is evaluated through three simultaneous maps:

1. **Technical** — loudness, dynamics, EQ balance, stereo width, phase,
   transients, masking, mud/harshness/sibilance.
2. **Emotional** — what each section should make the listener feel; whether the
   vocal stays believable; whether the chorus lifts; whether the bridge changes
   pressure.
3. **Physical-space** — where each element lives: *intimate / foreground /
   midground / background*.

Roy Halee supplies the physical-space model; Phil Ramone supplies the emotional
hierarchy model; Logic Pro is the execution surface; the planner is the
reasoning layer.

### Masking as hierarchy, not as a fault

Masking is only flagged **critical** when competing elements share the same depth
layer *and* perceptual role. A pad behind the vocal, room tone, or a felt texture
is **good masking** — shared fabric — and left alone.

### Pipeline stages

```
manifest + stems
  → source material (what kind of Logic object)
  → instrument identity (what is this sound)
  → audio metrics (per stem)
  → musical role + felt/heard + sacred/expendable
  → sections + section contrast
  → depth layers (per section)
  → masking (as hierarchy)
  → Halee/Ramone doctrine scoring
  → Logic-native action plan + automation
  → next-pass recommendations (≤ 5) + creative hypotheses
```

## Project layout

```
logic_mix_os/
  cli.py            # argparse CLI
  pipeline.py       # wires every stage together + writes artifacts
  constants.py      # controlled vocabularies (source kinds, identities, depths, risk classes)
  dsp.py            # numpy DSP primitives (spectra, loudness, stereo, mapping)
  project.py        # manifest model, track resolution, mixdown
  analyzers/        # audio loader, source material, identity, metrics, sections, masking, reference
  doctrine/         # Halee/Ramone JSON + scoring engine
  planners/         # role, depth, logic actions, mix plan, next pass + creative stub
  renderers/        # Markdown + checklist renderers
  validation/       # schema validation, confidence/evidence tagging
  schemas/          # JSON Schemas for every output
fixtures/           # deterministic synthetic test projects (generator + manifests)
examples/           # example manifest + committed sample output
tests/              # pytest suite (3 fixtures, acceptance + unit)
```

## Tests

```bash
pytest
```

The suite covers audio-metric correctness, identity/source/felt-heard/depth
classification, doctrine scoring + masking hierarchy, mix-plan integrity, the
non-destructive guarantee, and schema validation, across three fixtures: a
simple vocal/piano song, a dense chorus with loops, and a Splice-loop problem.
`conftest.py` regenerates the fixtures automatically if missing.

### Regression & doctrine protection

`logic-mix-os regression` guards musical judgment against silent drift, in two layers:

- **Golden snapshots** — a stable categorical fingerprint of each fixture
  (`fixtures/<name>/golden/snapshot.json`): identities, source kinds, depth
  layers, masking classifications, and section lift warnings. Categorical
  regressions are *critical*; score/confidence drift (within tolerance) is a
  *warning*. Regenerate with `regression --update-golden`.
- **Doctrine invariants** — absolute behaviours that must never regress, e.g.
  *don't foreground full-width stock loops, don't treat all masking as bad,
  don't widen the lead vocal to lift a chorus, prefer vocal rides before
  heavier compression, never recommend destructive edits, never score an
  unidentified track.*

```json
{ "tests_run": 68, "passed": 68, "failed": 0, "critical_failures": [], "warnings": [] }
```

## Risk classes

Every action is tagged with a risk class so creative/destructive moves never
bypass approval:

| Class | Meaning |
|---|---|
| 0 | observe / analyze only |
| 1 | report / checklist only |
| 2 | reversible mix recommendation |
| 3 | reversible Logic action requiring approval |
| 4 | source-level creative change requiring explicit approval |
| 5 | destructive / identity-changing — **never auto-applied** |

## Build status (the full system)

Built in coherent, tested layers following the spec's build-priority rule (§53):
decision-system depth first, then orchestration, then the execution bridge, then
the UI. All of the following are implemented and tested:

- **Core decision system** — source material, identity, roles, felt/heard,
  sacredness, sections + contrast, depth layers, masking-as-hierarchy, Halee/
  Ramone doctrine scoring, Logic actions, automation, next pass.
- **Expanded analysis (§25/29/30/31)** — translation, mono/phase, arrangement
  density, listener experience, transition quality, groove, harmonic/key, vocal
  performance, lyric alignment.
- **Creative engine (§55–67)** — static baseline + static-vs-dynamic, A/B/C/D
  variant branching with scoring, search modes, winning-variant merge.
- **Governance / taste (§68–84)** — emotional-truth lock, taste triangle,
  false-progress / overfit / anti-template detectors, reference sanity, listener
  panel, stop conditions, kill-switches, review modes, mixer-communication tones.
- **Session intelligence (§34–36)** — provenance, render dependency graph,
  plugin scanner.
- **Memory (§32/38/39)** — mix-pass history, decision ledger, taste calibration,
  reference profiles (file-backed, non-destructive).
- **Album coherence (§40)** — "one album or N productions?"
- **Source-aware auditors (§19–21)** — live / synth-MIDI / sampler / loop.
- **Logic bridge (§41–42)** — action export, AppleScript/Shortcuts codegen,
  dry-run executor (**never executes** here), helper-AU spec.
- **Cowork command surface (§43)** — 32 bounded commands.
- **UI (§50)** — local self-contained HTML dashboard + terminal `status`.

### What remains environment-bound

The Logic bridge is real code but **dry-run only** on this platform: actually
driving Logic Pro requires macOS + the Logic AppleScript/accessibility surface,
and the helper Audio Units (Mix Probe, Depth Layer Meter, …) must be compiled
with the macOS Audio SDKs. Those are specified and scaffolded; they cannot run
or be tested here. Everything else runs locally with `numpy` alone.
