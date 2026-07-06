# Field sessions

Committed-back records of **real** mixing sessions driven through Logic Mix OS —
the build side's window into what the engine actually did on a live song, without
shipping a byte of copyrighted audio.

## What a bundle is

A field-session bundle is the JSON + Markdown trail of one session, produced by:

```
python -m logic_mix_os.cli capture-session \
  --memory-dir <the session's memory dir> \
  --out field_sessions/<song-slug>-<date> \
  --artifacts <the session's analysis output dir>   # optional
```

Each bundle contains:

- the three **memory** stores — `mix_pass_history.json`, `decision_ledger.json`,
  `taste_profile.json` (whichever exist);
- the **plan / verdict artifacts** copied from the analysis output dir
  (`mix_plan.json`, `doctrine_score.json`, `governance.json`, the Logic
  checklist / verdict Markdown, the dashboard HTML, …);
- a deterministic `session_summary.json` — what was captured, plus pass /
  decision / taste counts.

## Raw audio is excluded — always

`capture-session` copies **memory + text artifacts only**. It never copies a
`.wav`/`.aif`/`.flac`/etc. file, and the `.gitignore` in this directory ignores
audio extensions as a second lock. So a bundle is safe to commit: it captures the
*decisions* a session made, never the song's stems or bounces.

## How to commit one back

1. Run `capture-session` into `field_sessions/<song-slug>-<date>/` as above.
2. Sanity-check the bundle — it should be JSON/Markdown/HTML only, no audio.
3. Commit the bundle directory. That is the record the build side reads to see
   how the engine performed on a real session and to inform the next packet.

See `docs/REAL_SESSION.md` for the full end-to-end walkthrough (install → MCP
config → scaffold a manifest → drive a session → capture the bundle).
