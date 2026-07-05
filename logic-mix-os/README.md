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
the four example projects (deterministic, seeded):

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

Ready-made examples of the output live in `examples/`: five committed trees
generated from the **same stems** (the seeded `vocal_chop_groove` fixture) —
[`examples/sample_output/`](examples/sample_output) under the default
Halee/Ramone profile, plus one tree per selectable producer:
[`examples/sample_output_timbaland/`](examples/sample_output_timbaland)
(`--producer timbaland`),
[`examples/sample_output_quincy/`](examples/sample_output_quincy)
(`--producer quincy_jones`),
[`examples/sample_output_eno/`](examples/sample_output_eno)
(`--producer brian_eno`) and
[`examples/sample_output_chris_lord_alge/`](examples/sample_output_chris_lord_alge)
(`--producer chris_lord_alge`). See the next section for what to compare. The
mode-level story has its own committed examples —
[`examples/mode_demos/`](examples/mode_demos), eleven producer × mode runs
from one denser fixture ("Same stems, different modes" below).

## Five producers, same stems

The five committed sample trees are the output of exactly these invocations
(from the project root, after `python fixtures/generate_fixtures.py`):

```bash
python -m logic_mix_os.cli analyze \
  --stems fixtures/vocal_chop_groove/stems \
  --manifest fixtures/vocal_chop_groove/project_manifest.json \
  --out out_ref

python -m logic_mix_os.cli analyze \
  --stems fixtures/vocal_chop_groove/stems \
  --manifest fixtures/vocal_chop_groove/project_manifest.json \
  --out out_tim --producer timbaland

python -m logic_mix_os.cli analyze \
  --stems fixtures/vocal_chop_groove/stems \
  --manifest fixtures/vocal_chop_groove/project_manifest.json \
  --out out_quincy --producer quincy_jones

python -m logic_mix_os.cli analyze \
  --stems fixtures/vocal_chop_groove/stems \
  --manifest fixtures/vocal_chop_groove/project_manifest.json \
  --out out_eno --producer brian_eno

python -m logic_mix_os.cli analyze \
  --stems fixtures/vocal_chop_groove/stems \
  --manifest fixtures/vocal_chop_groove/project_manifest.json \
  --out out_cla --producer chris_lord_alge
```

Same stems, same measurements, five judgments — the values below are the ones
pinned in the test suite:

| Reading | Halee/Ramone (reference) | Timbaland | Quincy Jones | Brian Eno | Chris Lord-Alge |
|---|---|---|---|---|---|
| Overall mix readiness | **76.3** | **60.9** | **68.8** | **65.5** | **67.8** |
| Vocal role fit | 65.0 | 85.0 | 85.0 | 85.0 | 85.0 |
| Loop context | 15.0 | 10.0 | 12.0 | 35.0 | 18.0 |

Each overall is its own profile's weighted mean over the shared component
axes. The two rows that move are the two authored divergence channels: the
vocal-blend policy (the reference reads the vocal chop/stack masking
involvements under full clarity protection at 65.0; the other four profiles'
authored opt-ins accept the same involvements as blend at 85.0) and the
static-loop polarity (all five profiles read the dominant chop loop as STATIC
from the same stems; each maps that one reading to its own authored value —
15.0 / 10.0 / 12.0 / 35.0 / 18.0).

One sentence per producer:

- **Halee/Ramone (reference)** — vocal and space: protect the lead vocal's
  clarity and believability, and build the physical depth field around it.
- **Timbaland** — groove and contrast: beat identity is his heaviest
  scoring axis, and the chop stacks are accepted into the groove as blend.
- **Quincy Jones** — orchestration and ensemble: arrangement-first lift
  (his default search mode is literally named `arrangement_lift`) and
  ensemble balance over any single element's heroics.
- **Brian Eno** — atmosphere and restraint: negative space is his heaviest
  scoring axis, a static loop is a legitimate ambient bed (his authored
  35.0), and his winning vocal move is the intimacy pass (`vocal_B`) where
  the other three ride the phrase (`vocal_A`).
- **Chris Lord-Alge** — impact and excitement: section contrast is his
  heaviest scoring axis (his center of gravity, weighted above every other
  axis) — the loudness-forward anti-Eno. A static dominant loop is material
  to commit to and drive rather than an ambient bed (his authored 18.0,
  above the reference's 15.0), and his impact/commitment posture even moves
  the plan choice (below).

The four reference-lineage producers land the same non-vocal winners
(`chorus_lift_B` / `loop_B` / `depth_A`, both `_B` moves being
subtractive) — for them most of the divergence lives in the readings, the
overalls and the candidate sets, not the plan choice (their plan-level
reversal needs an iconic-reading loop; see
`tests/test_differential_proof.py`). Chris Lord-Alge is the first producer
to break that on these very stems: his impact/commitment weighting wins the
drum-room move (`chorus_lift_D`) over the subtractive `chorus_lift_B` and
`loop_A` (a loop-deconstruct) over `loop_B`, straight from his doctrine and
with no iconic-loop reading — his divergence reaches the plan choice, not
just the readings. What stays invariant under all five producers: the safety
surface (every tree's composed kill-switch list leads with the five
hardcoded safety switches, verbatim) and the measurements themselves (the
shared axes — e.g. emotional hierarchy 86.0, groove coherence 99.4 — read
identically in all five trees).

Start the comparison at `doctrine_score.json` (each tree names its selecting
producer and carries its own scores) and `mix_verdict.md` (the human-readable
verdict, producer line near the top) across the five `examples/sample_output*`
trees.

### Modes are behavior

A producer profile is not just weights — its authored **search modes** fork
the creative candidate set. The ownership split is the standing doctrine,
verbatim:
"engine owns move vocabulary / profile owns mode reach / governance owns safety cap".
Each mode declares what it favors (reordered to
the front of a branch), what it suppresses (removed), and what it *reaches*
for (extended move families admitted into the search), all under a declared
risk posture that the engine caps fail-closed: a mode whose posture sits
below a family's authored translation risk cannot reach it, and the refusal
is reported in `reach_capped`, never silent (`tests/test_mode_forking.py`,
`tests/test_negative_space_dropout.py`). The committed timbaland tree
carries this surface live: his default mode (`dramatic_contrast`) declares
dropout reach, so
[`examples/sample_output_timbaland/creative.json`](examples/sample_output_timbaland/creative.json)
echoes the authored declaration
(`"search_mode_declarations": {"allowed_risk": "medium", "favor_kinds": [],
"suppress_kinds": [], "reach_kinds": ["negative_space_dropout"]}`), its
chorus-lift branch reports `"reached": ["negative_space_dropout"]` with one
extra candidate (`chorus_lift_F`, a dropout proposal targeting the BGV Chop
bed) — and the winner is still `chorus_lift_B`: the reach widens the
candidate set, not the verdict. The quincy tree carries the same surface for
his `arrangement_lift` reach (admitting `chorus_lift_E`); the reference and
eno trees carry no declaration keys at all — their default modes are
authored-neutral, and a neutral mode is byte-silent. A mode can also be
selected explicitly with `creative --mode <name>` (each profile's own mode
names; a mode the profile does not carry resolves to its default, reported
observationally as `search_mode_fallback`).

### The extended move families

Three move families exist beyond the engine's neutral pool, and all three
are **reach-gated**: no variant from them ever appears unless a profile
authors that family into a mode's `reach_kinds` (and clears the risk cap) —
`arrangement_lift` (build the lift by adding or featuring arrangement
elements — quincy's default reach; `chorus_lift_E`, `density_C`),
`ensemble_rebalance` (rebalance the ensemble around the section's narrative
— quincy's ensemble modes; `vocal_C`, `density_D`), and
`negative_space_dropout` (propose silence: region-mute a duplicated,
non-protected element into a section entry, the original track untouched —
reached by timbaland's and eno's authored modes; `chorus_lift_F`,
`density_E`). The dropout family's protection filter is engine-owned — the
lead vocal, the groove foundation and sacred elements are never targeted,
and no profile can reword the proposal text — and the doctrine line is
verbatim: "dropout is an arrangement proposal, not a destructive
operation."

### Same stems, different modes — the committed mode demos

[`examples/mode_demos/`](examples/mode_demos) commits the mode-level
differential the way the five trees above commit the producer-level one:
eleven directories, one per producer × mode run, all from the **same stems**
(the seeded `dense_chorus_with_loops` fixture — the only shipped fixture
that fires all five creative problem branches). Each directory keeps the
creative pair from its run — `creative.json` (the candidate ids, the
authored declarations echo, the per-branch fork reports, the winners) and
`creative_report.md` (the human-readable half); the run's other artifacts
tell the producer-level story the sample trees above already commit in
full. Each pair is the output of exactly one of these invocations (from
the project root, after `python fixtures/generate_fixtures.py`):

```bash
python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --mode dramatic_contrast --out examples/mode_demos/halee_ramone_dramatic_contrast

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --mode conservative --out examples/mode_demos/halee_ramone_conservative

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --mode deconstructive --out examples/mode_demos/halee_ramone_deconstructive

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer timbaland --mode conservative --out examples/mode_demos/timbaland_conservative

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer quincy_jones --mode conservative --out examples/mode_demos/quincy_jones_conservative

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer brian_eno --mode conservative --out examples/mode_demos/brian_eno_conservative

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer quincy_jones --mode experimental --out examples/mode_demos/quincy_jones_experimental

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer timbaland --mode negative_space --out examples/mode_demos/timbaland_negative_space

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer timbaland --mode groove_pocket --out examples/mode_demos/timbaland_groove_pocket

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer chris_lord_alge --mode conservative --out examples/mode_demos/chris_lord_alge_conservative

python -m logic_mix_os.cli creative \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --producer chris_lord_alge --mode big_chorus --out examples/mode_demos/chris_lord_alge_big_chorus
```

The committed pairs are pinned byte-for-byte against fresh renders — and
every set in the table below is pinned directly on the committed bytes —
in `tests/test_mode_demo_refresh.py`. Candidate-id sets per branch
(`chorus_lift_A` abbreviated to `A` under its branch column, extended
reach-gated ids in **bold**; every demo's `loop` and `depth` branches emit
the same `loop_A loop_B` / `depth_A` sets — except
`chris_lord_alge_conservative`, whose suppressed subtractive move also drops
`loop_B`, leaving `loop_A`):

| Demo | `chorus_lift` | `density` | `vocal_belief` |
|---|---|---|---|
| `halee_ramone_dramatic_contrast` | A B C D | A B | A B |
| `halee_ramone_conservative` | B C D | A B | A B |
| `halee_ramone_deconstructive` | B C | A B | A B |
| `timbaland_conservative` | A B C D | A B | A B |
| `quincy_jones_conservative` | B C | A B | A B |
| `brian_eno_conservative` | B D | A B | B |
| `chris_lord_alge_conservative` | A C D | A | A B |
| `quincy_jones_experimental` | A B C D **E** | A B **C D** | A B **C** |
| `timbaland_negative_space` | B C **F** | A B **E** | A B |
| `timbaland_groove_pocket` | B C D | A B | A B |
| `chris_lord_alge_big_chorus` | A B C D **E** | A B **C** | A B |

What to read off it:

- **Same producer, different mode** (the three `halee_ramone_*` rows):
  three different chorus-lift candidate sets from one profile on one
  project — her default `dramatic_contrast` searches the full pool, her
  `conservative` suppresses the width move, her `deconstructive` also
  drops the drum-room move. A mode is a different candidate search, not a
  label on the same one.
- **Same mode name, different producer** (the five `*_conservative` rows):
  five pairwise-distinct chorus-lift sets under one mode name — each is
  the shared engine pool minus that profile JSON's authored suppress list.
  Timbaland's conservative authors nothing, so his demo carries zero
  declaration bytes — an authored-neutral mode is byte-silent even when
  selected explicitly by name (halee's `dramatic_contrast` row shows the
  same silence). Chris Lord-Alge's conservative is the only one to suppress
  the subtractive move, so it is the only conservative row without
  `chorus_lift_B` (and, uniquely, it also drops `loop_B` / `density_B`) —
  and it wins the drum-room `chorus_lift_D` where the other four win the
  subtractive `chorus_lift_B`: his "commit, the thinning-out moves are
  withheld" bias.
- **Quincy reaching both his families** (`quincy_jones_experimental`): his
  high-posture experimental admits `chorus_lift_E` / `density_C`
  (arrangement_lift, at his authored 85.3) and `density_D` / `vocal_C`
  (ensemble_rebalance, 83.1) — and `vocal_C` **wins** its branch, one of
  two committed demos where a reached move takes a verdict (CLA's
  `big_chorus`, below, is the other).
- **Chris Lord-Alge going bigger** (`chris_lord_alge_big_chorus`): his named
  center-of-gravity mode ("the chorus lands bigger than the verse") reaches
  `arrangement_lift`, so `chorus_lift_E` and `density_C` are admitted — and
  both **win** their branches, the second committed demo where a reached
  move takes a verdict and the only one where the reach wins on two
  branches. Of the eleven demos, seven win exactly the moves the neutral
  search picks; the four that deviate all deviate for an authored reason —
  eno's suppression (`vocal_B`), quincy's reach (`vocal_C`), and CLA's two
  impact demos (his conservative's drum-room `chorus_lift_D` and this
  mode's reached `chorus_lift_E` / `density_C`).
- **Dropout only where authored** (the timbaland pair): his
  `negative_space` mode reaches the dropout family — `chorus_lift_F`
  proposes region-muting a duplicate of the Synth Pad and Splice Texture
  Loop texture beds through the final pre-chorus bar, `density_E` a
  sectional dropout, both at his honest 80.9 and both outranked by his
  subtractive economy — while `groove_pocket`, same producer and same
  stems, authors no reach: no dropout id anywhere and no reach key in its
  fork reports. Halee/Ramone stays reference-safe the same way: none of
  her modes authors reach, so no extended id appears in any of her rows
  (her committed default-flow tree is
  [`examples/sample_output/`](examples/sample_output)).

The roster behind these demos is directory-driven: drop a JSON in the
producers directory (`logic_mix_os/doctrine/producers/`) — the CLI and the
structural test sweeps discover it automatically. `--producer` resolves
any name in that directory (an unknown name's error message lists what was
found there), and the suite's producer sweeps glob the same directory, so
a fifth profile joins the comparison without a code change.

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
| `cowork --list` / `cowork --name CMD` | Claude Cowork command surface (35 commands) |
| `export-actions --plan --format json\|applescript\|shortcuts` | Bridge export |
| `bridge-dryrun --plan [--review-mode]` | Simulate applying actions (never executes) |
| `regression [--fixtures] [--update-golden]` | Golden-output + doctrine regression |

Common flags: `--stems`, `--manifest`, `--out`, plus optional `--bounce` and
`--reference` — and, on every analyze-family command, `--producer` (a profile
name resolvable from the local producers directory; default `halee_ramone`,
the reference profile).

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
`mix_verdict.md`, `logic_action_checklist.md`,
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
reasoning layer. In the emitted artifact contract these two models score as
`physical_space_score` (the physical-space / depth / spatial-realism model) and
`emotional_hierarchy_score` (the emotional hierarchy / vocal-belief /
narrative-priority model) — the contract keys describe the aesthetic, while the
producer profiles keep the producers' names.

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
examples/           # example manifest + the five committed sample trees (same stems, five producers)
                    #   + mode_demos/ (eleven committed producer × mode creative pairs, same stems)
tests/              # pytest suite (4 fixtures, acceptance + unit)
```

## Tests

```bash
pytest
```

The suite covers audio-metric correctness, identity/source/felt-heard/depth
classification, doctrine scoring + masking hierarchy, mix-plan integrity, the
non-destructive guarantee, and schema validation, across four fixtures: a
simple vocal/piano song, a dense chorus with loops, a Splice-loop problem,
and a vocal-chop groove (lead + chopped/stacked backing vocals + beat — the
fixture that exercises the vocal-type/blend-policy chain end to end).
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
- **Cowork command surface (§43)** — 35 bounded commands.
- **UI (§50)** — local self-contained HTML dashboard + terminal `status`.

### What remains environment-bound

The Logic bridge is real code but **dry-run only** on this platform: actually
driving Logic Pro requires macOS + the Logic AppleScript/accessibility surface,
and the helper Audio Units (Mix Probe, Depth Layer Meter, …) must be compiled
with the macOS Audio SDKs. Those are specified and scaffolded; they cannot run
or be tested here. Everything else runs locally with `numpy` alone.
