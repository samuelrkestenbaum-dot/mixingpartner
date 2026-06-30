"""CLI tests (P-010 — the two-pass ``album`` command).

``logic_mix_os.cli._run_album`` now runs two passes over a folder of projects:
pass 1 analyzes each song album-context-free (driving the coherence report, as
before) and derives the album means via ``analyze_album``; pass 2 re-runs each
song with its per-song delta vs those means so the report carries album-aware
per-song next-pass guidance under ``per_song_next_pass``.

This test drives the real CLI entrypoint (``cli.main(["album", ...])``) over the
synthetic fixtures and proves the second pass reached the planner: at least one
song whose brightness/lufs is an album outlier surfaces the bounded
``"Album coherence"`` next-pass item, while the coherence report itself is
unchanged from the single-pass ``analyze_album`` over the same songs.

Local-only, deterministic. No DAW / network / subprocess.
"""

from __future__ import annotations

import json
import pathlib
import statistics

import pytest

from logic_mix_os import cli

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures"
FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


def test_album_emitted_deltas_match_prior_cli_recompute(_ensure_fixtures):
    """Provenance: ``album.py``'s emitted per-song deltas equal the value the old
    ``cli.py`` block computed (``song - statistics.mean(non-None values)``).

    P-011 single-sources the album means: ``analyze_album`` now emits each song's
    ``brightness_delta`` / ``lufs_delta`` and ``cli.py`` consumes them instead of
    recomputing ``statistics.mean``. This pins that the consolidation is EXACT —
    the emitted delta is byte-identical to what the consumer derived before.
    """
    from logic_mix_os.album import analyze_album
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest

    results, names = [], []
    for sub in sorted(FIXTURES.iterdir()):
        mp = sub / "project_manifest.json"
        if mp.exists():
            m = load_manifest(mp)
            results.append(analyze(str(sub / "stems"), m))
            names.append(sub.name)

    report = analyze_album(results, names)
    songs = report["songs"]

    # The independent ("old cli.py") recompute over the same source dicts.
    b_vals = [s["brightness"] for s in songs if s["brightness"] is not None]
    l_vals = [s["lufs"] for s in songs if s["lufs"] is not None]
    b_mean = statistics.mean(b_vals) if b_vals else None
    l_mean = statistics.mean(l_vals) if l_vals else None

    for s in songs:
        # album.py now emits these keys additively.
        assert "brightness_delta" in s
        assert "lufs_delta" in s

        expected_bd = (
            (s["brightness"] - b_mean)
            if (b_mean is not None and s["brightness"] is not None)
            else None
        )
        expected_ld = (
            (s["lufs"] - l_mean)
            if (l_mean is not None and s["lufs"] is not None)
            else None
        )
        assert s["brightness_delta"] == expected_bd, s["name"]
        assert s["lufs_delta"] == expected_ld, s["name"]


def test_album_command_emits_album_aware_per_song_guidance(tmp_path, capsys, _ensure_fixtures):
    out_path = tmp_path / "album.json"
    rc = cli.main(["album", "--projects", str(FIXTURES), "--out", str(out_path)])
    assert rc == 0

    captured = capsys.readouterr().out
    assert "Album coherence:" in captured

    report = json.loads(out_path.read_text())

    # The two-pass wiring attached album-aware per-song guidance for every project.
    assert "per_song_next_pass" in report
    per_song = report["per_song_next_pass"]
    names = {entry["name"] for entry in per_song}
    assert set(FIXTURE_NAMES).issubset(names)

    # Every emitted next-pass item is well-formed (1-based priority + title/detail).
    for entry in per_song:
        for item in entry["next_pass"]:
            assert item["priority"] >= 1
            assert item["title"] and item["detail"]

    # The cross-song coherence axis is live end-to-end: at least one outlier song
    # surfaces the bounded, evidence-tagged "Album coherence" item that the
    # single-pass (album-context-free) run could never produce.
    coherence = [
        item
        for entry in per_song
        for item in entry["next_pass"]
        if item["title"] == "Album coherence"
    ]
    assert coherence, "two-pass album run must surface at least one album-coherence hint"
    for item in coherence:
        assert "evidence" in item
        assert "vs album mean" in item["evidence"]

    # The coherence report proper is untouched by the second pass — it still equals
    # the single-pass analyze_album over the same songs.
    from logic_mix_os.album import analyze_album
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest

    results, names_ordered = [], []
    for sub in sorted(FIXTURES.iterdir()):
        mp = sub / "project_manifest.json"
        if mp.exists():
            m = load_manifest(mp)
            results.append(analyze(str(sub / "stems"), m))
            names_ordered.append(sub.name)
    expected = analyze_album(results, names_ordered)
    assert report["coherence_score"] == expected["coherence_score"]
    assert report["outliers"] == expected["outliers"]
    assert report["verdict"] == expected["verdict"]


def test_album_command_no_projects_returns_1(tmp_path, capsys):
    empty = tmp_path / "no_projects"
    empty.mkdir()
    rc = cli.main(["album", "--projects", str(empty)])
    assert rc == 1
    assert "No projects" in capsys.readouterr().out
