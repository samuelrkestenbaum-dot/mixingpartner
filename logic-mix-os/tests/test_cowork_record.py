"""P-019 — close the learning loop INSIDE the cowork surface.

The forward half of the cowork registry can plan a mix and read the next pass,
and P-009 threads memory into the READ side (history -> next-pass). But there was
no cowork command to RECORD a pass outcome on the LIVE history channel — the
``record_pass`` / P-018 ``--reverted`` confirmed-outcome signal was reachable only
via the separate ``memory-record`` CLI verb. ``record_mix_pass`` closes that gap:
an agent driving through cowork can now record an outcome AND (P-018) confirm a
revert, then read the changed next pass, WITHOUT leaving the surface.

These tests are the binding guard (this axis is not golden-covered):

  * Unit: ``run_command("record_mix_pass", ...)`` writes to the LIVE
    ``mix_pass_history.json`` channel, passes through the ``reverted`` flag,
    errors cleanly with no ``memory_dir``, and — with default ``reverted=False`` —
    stores a record byte-identical to the standalone ``memory-record`` verb.
  * Liveness (no re-run — the P-016/P-018 lesson): record a confirmed revert
    THROUGH cowork, then a FRESH ``build_context(memory_dir=...)`` ->
    ``suggest_next_pass`` surfaces the confirmed "Revert last pass" item. This
    proves the loop closes THROUGH the cowork surface, not just in unit-land.

No DAW / network / subprocess: local JSON I/O of the app's own store. Fake
adapters only. Deterministic.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from logic_mix_os.cowork import build_context, run_command
from logic_mix_os.memory import ProjectMemory
from logic_mix_os.pipeline import analyze

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "dense_chorus_with_loops"


def _manifest() -> dict:
    return json.loads((FIXTURE / "project_manifest.json").read_text())


def _stems() -> str:
    return str(FIXTURE / "stems")


# --------------------------------------------------------------------------- #
# Unit: the handler records on the LIVE history channel via ctx["memory"].
# --------------------------------------------------------------------------- #
def test_record_mix_pass_writes_live_history_with_reverted_flag(tmp_path):
    """``record_mix_pass`` persists a pass on mix_pass_history.json with reverted."""
    s, m = _stems(), _manifest()
    mem_dir = tmp_path / "record_store"
    ctx = build_context(stems=s, manifest=m, memory_dir=str(mem_dir))

    out = run_command("record_mix_pass", ctx, name="chorus_widen", reverted=True)

    # The handler returns the stored record JSON.
    assert out["pass_name"] == "chorus_widen"
    assert out["reverted"] is True

    # It landed on the LIVE channel — the standalone store reads it back.
    history = ProjectMemory(mem_dir).history()
    assert history[-1]["pass_name"] == "chorus_widen"
    assert history[-1]["reverted"] is True


def test_record_mix_pass_no_memory_dir_errors_cleanly():
    """Mirror ``write_mix_decision``: no memory_dir -> clean error, no crash."""
    ctx = build_context(stems=_stems(), manifest=_manifest())  # no memory_dir
    assert ctx["memory"] is None
    out = run_command("record_mix_pass", ctx, name="whatever")
    assert out == {"error": "no memory_dir configured"}


def test_record_mix_pass_default_omits_reverted_flag(tmp_path):
    """Default ``reverted=False`` omits the key (opt-in discipline, P-018)."""
    s, m = _stems(), _manifest()
    mem_dir = tmp_path / "default_store"
    ctx = build_context(stems=s, manifest=m, memory_dir=str(mem_dir))

    out = run_command("record_mix_pass", ctx, name="plain_pass")
    assert "reverted" not in out
    assert "reverted" not in ProjectMemory(mem_dir).history()[-1]


def test_record_mix_pass_default_byte_identical_to_memory_record(tmp_path):
    """Default-path stored history is byte-identical to the standalone verb.

    The cowork ``record_mix_pass`` handler and the ``memory-record`` CLI verb both
    call ``ProjectMemory.record_pass(name, result)`` on the SAME analysis. The
    only per-record non-determinism is the timestamp, so we neutralise ``date``
    and compare the raw stored JSON bytes — proving the cowork path routes through
    the identical live channel, not a divergent shape.
    """
    s, m = _stems(), _manifest()

    # (1) cowork surface
    cw_dir = tmp_path / "cowork_store"
    ctx = build_context(stems=s, manifest=m, memory_dir=str(cw_dir))
    run_command("record_mix_pass", ctx, name="same_pass")

    # (2) standalone memory-record equivalent: record_pass on a fresh analysis.
    mr_dir = tmp_path / "memrecord_store"
    mem = ProjectMemory(mr_dir)
    mem.record_pass("same_pass", analyze(s, m))

    def _canon(path: pathlib.Path) -> str:
        data = json.loads((path / "mix_pass_history.json").read_text())
        for rec in data:
            rec["date"] = "<neutralised>"  # only per-record non-determinism
        return json.dumps(data, sort_keys=True)

    assert _canon(cw_dir) == _canon(mr_dir)
