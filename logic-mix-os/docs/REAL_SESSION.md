# Driving a real session

The engine ships proven on synthetic fixtures. This is the end-to-end path for
driving it on a **real** song — from a folder of exported Logic stems to a
committed field-session record — without ever handing it a DAW or a byte of
copyrighted audio to keep.

> The system can ask what it recommends; it never makes Logic do it. Every Logic
> action stays a checklist / plan artifact, executed by you.

## 1. Install locally

From the package root (`logic-mix-os/`):

```
pip install -e .
```

`numpy` is the only hard dependency; `pip install -e '.[full]'` adds
`soundfile` / `pyloudnorm` / `scipy` for broader format support and more
accurate loudness. Everything below also runs as `python -m logic_mix_os.cli
<subcommand>` without the console script.

## 2. Point Cowork / Claude Desktop at the MCP server

The Cowork command surface is served over the Model Context Protocol (see
[`COWORK_MCP.md`](COWORK_MCP.md) for the full contract). Add this server config
to your MCP host (Cowork, Claude Desktop, or any JSON-RPC-over-stdio MCP host):

```json
{
  "mcpServers": {
    "logic-mix-os-cowork": {
      "command": "python",
      "args": ["-m", "logic_mix_os.cowork_mcp"]
    }
  }
}
```

The host completes the `initialize` handshake, then drives the session with
`tools/list` + `tools/call`. Reads and plans (identity, sections, masking,
depth, mix plan, doctrine scores, next-pass, creative, governance, the Logic
checklist) are free and write nothing. The side-effecting commands
(`record_mix_pass`, `update_taste_calibration`, `write_mix_decision`,
`override_track_identity`) require an explicit `memory_dir`.

## 3. Scaffold a manifest from your exported stems

Export your song's tracks as WAV stems into one folder, then:

```
python -m logic_mix_os.cli scaffold-manifest --stems ~/Music/MySong/stems
```

This writes a **draft** `project_manifest.json` next to the stems folder
(default `--out` is `<stems>/../project_manifest.json`; `--force` overwrites an
existing manifest). The draft carries one track per stem with a guessed
`source_kind`, a WAV-header-probed sample rate / bit depth, and two annotations:

- `_draft: true` — a reminder this is machine-scaffolded, not confirmed.
- `_needs_review` — the track names whose `source_kind` guess was low-confidence.

Open the draft and finish it: confirm the `_needs_review` guesses, fill in the
`sections` (start/end timecodes + `emotional_goal`) and the `intent`
(`singular_emotional_truth`, `references`, `negative_constraints`), set
`tempo` / `key`, and remove `_draft` when it is real. The scaffolder never
invents section timecodes from the audio — that judgment stays yours.

## 4. Drive a first session with an explicit `memory_dir`

Drive the session through Cowork (step 2) or straight from the CLI, always
passing a `memory_dir` so passes, decisions, and taste accumulate:

```
python -m logic_mix_os.cli memory-record \
  --stems ~/Music/MySong/stems \
  --manifest ~/Music/MySong/project_manifest.json \
  --memory-dir ~/Music/MySong/.mixos \
  --name mix_pass_01

python -m logic_mix_os.cli feedback \
  --memory-dir ~/Music/MySong/.mixos --label "too wide"
```

Write the full artifact set (mix plan, doctrine scores, governance, the Logic
checklist / verdict) for the pass with `analyze --out`. Optionally re-export a
stereo bounce of the pass from Logic and feed it back for section-accurate
analysis and a reference delta:

```
python -m logic_mix_os.cli analyze \
  --stems ~/Music/MySong/stems \
  --manifest ~/Music/MySong/project_manifest.json \
  --bounce ~/Music/MySong/bounce_pass_01.wav \
  --reference ~/Music/reference_track.wav \
  --out ~/Music/MySong/output

python -m logic_mix_os.cli compare-reference \
  --bounce ~/Music/MySong/bounce_pass_01.wav \
  --reference ~/Music/reference_track.wav
```

## 5. Capture the session and commit it back

When the session is worth recording, bundle its memory + artifacts:

```
python -m logic_mix_os.cli capture-session \
  --memory-dir ~/Music/MySong/.mixos \
  --out field_sessions/mysong-2026-07-06 \
  --artifacts ~/Music/MySong/output
```

The bundle is the three memory JSONs, the plan/verdict artifacts, and a
deterministic `session_summary.json` — **memory + text only; never audio**.
Sanity-check it (JSON/Markdown/HTML, no stems), then commit the bundle directory
under `field_sessions/`. That committed record is how the build side reads what
the engine did on a real song and decides the next packet. See
[`../field_sessions/README.md`](../field_sessions/README.md) for the convention.
