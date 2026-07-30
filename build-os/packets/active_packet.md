# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — **P-062 — Multi-Lens Execution Brief** (set active
  2026-07-30, explicit user go). Branch
  `claude/logic-mix-os-p061-detector-0dvr2t` @ set-active atop `ba127ff`;
  `git merge-base HEAD 9cfe990` = **`9cfe990`** (verified at set-active).
- Route: **builder → qa → reviewer → archivist**; receipt on close at
  `build-os/receipts/P-062-multi-lens-execution-brief.md`.

## P-062 — Multi-Lens Execution Brief

**"From every angle" planning surface** — the Manus-pattern harness encoded as a
**deterministic artifact**: harness ours, measurements ground truth, LLM
narrates but **never scores**.

### Why

The user wants Manus-style multi-angle song analysis as **planning for
execution** of the actual mix. Manus = orchestration harness over Claude; the
analysis quality is harness + Claude. **Decision (user-agreed): no hosted
LLM/agent in the engine** — instead a deterministic multi-lens brief with a
**draft-only host-synthesis prompt block**, per the standing P-025/P-031
confidence policy (LLM = draft-only, NEVER high-confidence).

### In scope

1. **NEW `logic_mix_os/renderers/execution_brief_renderer.py`** — core
   `render_execution_brief(<parsed payload dicts>) -> str` producing ONE
   markdown brief with:
   - **SIX LENSES**, evidence numbers quoted **verbatim** from the payloads:
     - *Arrangement/section*: `section_analysis.json` (list of {section_id,
       name, start_time, end_time, emotional_goal, metrics,
       contrast_vs_previous}) + `expanded_analysis.json["arrangement_density"]`.
     - *Masking/spectral*: `masking_report.json` ({doctrine_rule, events[],
       per_track_masking_risk, summary}; summary has critical_count /
       moderate_count / blend_count / total_events / vocal_band_masking_count;
       events have elements, frequency_range, section, severity, overlap,
       reason, recommendation).
     - *Dynamics/energy*: `doctrine_score.json` dynamic_mix_score /
       section_contrast_score + evidence.dynamic_mix /
       evidence.section_contrast; energy tags in
       `expanded_analysis["listener_experience"]`.
     - *Vocal*: vocal_centrality_score, vocal_role_fit_score + evidence,
       summary.vocal_band_masking_count,
       `expanded_analysis["vocal_performance"]`.
     - *Space/depth*: physical_space_score, depth_hierarchy_score + evidence,
       `depth_map.json`.
     - *Translation/texture*: `expanded_analysis["translation"]` /
       `["mono_compatibility"]` (also translation_score /
       mono_compatibility_score on mix_plan), textural_coherence_score,
       low_end_motion_score.
   - **CROSS-LENS CONTRADICTIONS**: deterministic rule-based (e.g. high section
     contrast but flat physical space), **no LLM**.
   - **EXECUTION ORDER**: `mix_plan.json` per_track_actions ({diagnosis,
     actions, automation, send_reverb, risk_class}), per_section_actions,
     automation_plan, mute_candidates, next_pass ({priority, title, detail})
     re-organized into ordered phases: gain/static balance → masking carves →
     space/depth → section/automation → creative variants; cross-referenced to
     `render_logic_checklist` items.
   - **HOST-SYNTHESIS PROMPT BLOCK**: clearly fenced, instructs any LLM host
     (Cowork/Claude session or pasted elsewhere) how to do the multi-angle
     narrative synthesis ON TOP of the brief; **stamped DRAFT-ONLY** per
     policy.
   - **Producer-voiced** from `doctrine_score.json` producer + confidence
     fields (no profile reload).
2. **`cli.py`** — new `execution-brief` subparser: artifact-directory in, one
   markdown out. **OPT-IN** — `write_artifacts` (pipeline.py:353) is NOT
   touched. Precedent: `render-checklist` (cli.py:498) reads mix_plan.json
   from disk.
3. **`cowork.py`** — `render_execution_brief` registry row + `_SESSION_FLOW`
   placement. In-session handler renders from ProjectAnalysis (pattern
   cowork.py:351) via the dict-taking core.
4. **Tests**: renderer determinism + per-producer rendering against the
   COMMITTED sample trees (they are free fixtures — 5 producer trees under
   `examples/`), contradiction-rule units, draft-only stamp assertion, CLI
   smoke, and the CONSCIOUS cowork pin updates.

### ★ GUARD FINDING — the packet's central design constraint

- Adding **ANY** file to `write_artifacts` breaks
  `tests/test_sample_refresh.py:237-238` (`committed_files == fresh_files` AND
  `len == 30`, over ALL 5 sample trees) and
  `tests/test_mode_demo_refresh.py:349` (same comparison over 11 mode-demo
  trees) — a **16-tree corpus re-pin for zero scoring benefit**. **REJECTED
  (path a).**
- **CHOSEN (path b): opt-in command reading a completed artifact dir** —
  corpus byte-identical **BY CONSTRUCTION**; P-049 directory-set guard
  (`test_sample_refresh.py:302`) and P-040/P-046 pins untouched. **The brief
  must NEVER be committed into `examples/` trees.**
- The cowork surface is ALSO pinned: `tests/test_cowork_mcp.py:424` asserts
  `len(COMMANDS) == 35`; `tests/test_cowork_session_flow.py:70` asserts every
  command in `_SESSION_FLOW`. **Commit-2 consciously bumps 35→36** + adds the
  flow entry.

### Binding out-of-scope

All `analyzers/*`, `doctrine_engine.py`, `masking_analyzer.py`, `pipeline.py`
(**INCLUDING `write_artifacts`**), `planners/*`, goldens, `examples/` committed
trees, fixtures, network, new dependency, apply-to-Logic. **Scoring corpus
byte-identical.**

### Commit plan (≤2)

- **Commit-1** = renderer + CLI + tests — **green in isolation, zero guard
  files touched**.
- **Commit-2** = cowork row + `_SESSION_FLOW` + the two pin bumps (35→36,
  flow) + tests.

### Baseline to protect (measured at `ba127ff`)

Suite **1426 passed / 0 failed / 0 warnings**; regression **93/93,
`critical_failures == []`**. Env: **pyloudnorm ABSENT** (`_HAVE_PYLN=False`,
`_HAVE_SCIPY=True`), numpy + scipy + soundfile present; `fixtures/` is
**GENERATED** (run `fixtures/generate_fixtures.py` or pytest-conftest first);
run bare `python3 -m pytest` — **NOT `pytest -q`** (addopts trap: pyproject
sets `-q` already, doubling it suppresses the count line).

## ★ OPEN GATES — carried, untouched by this packet

- **P-060 merge** (PR #38 candidate) — still THE open user gate; default
  remains `9cfe990`.
- **P-061 merge** — closed as a packet, NOT merged; no PR exists.
- **PR #12** — still OPEN against the abandoned `main` base.
- **Happy Man RE-RUN #2** — real-world confirmation for both halves.
- **Contract-fingerprint guard candidate.**
- **No push/merge/PR from this packet without separate explicit go.**

## Environment (reproduce on this or the corpus will appear to fail)

numpy + scipy + soundfile installed, **`pyloudnorm` NOT installed** — the
corpus was produced on the **scipy tier** of `dsp.integrated_loudness()`'s
pyloudnorm→scipy→FFT ladder. With pyloudnorm present, 5 `test_sample_refresh`
tests fail on ~0.5dB lufs deltas (an ENVIRONMENT artifact, not a regression).
Verify `_HAVE_PYLN=False, _HAVE_SCIPY=True`. **P-025 standing fact:**
`fixtures/` is **GENERATED** — run `fixtures/generate_fixtures.py` before
regression in a fresh / detached checkout. **★ The pytest `-q` trap:**
`pyproject` sets `addopts = "-q"`, so `pytest -q` silently suppresses the
summary count line while still exiting 0 — use bare `python3 -m pytest` or
`-o addopts=""`.

---
_Set ACTIVE by the archivist on 2026-07-30 (explicit user go; orchestrator
scoped). Predecessor P-061 record lives in
`build-os/receipts/P-061-detector-over-segmentation-calibration.md` and
`build-os/memory/residue.md`. One packet at a time: builder → qa → reviewer →
archivist → receipt._
