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


# --------------------------------------------------------------------------- #
# Liveness (no re-run — the P-016/P-018 lesson): the loop CLOSES through cowork.
# --------------------------------------------------------------------------- #
def _record_confirmed_revert_through_cowork(memory_dir) -> None:
    """Drive the OUTCOME half of the loop ENTIRELY through the cowork surface.

    Two passes are recorded via ``run_command("record_mix_pass", ...)`` on a
    memory-backed context: a baseline, then a pass whose ``section_contrast_score``
    is 20 HIGHER (so the score-delta inference says the move IMPROVED — empty
    ``got_worse`` / ``revert_candidates``) but recorded ``reverted=True``. This is
    the non-tautological override case: the score signal alone would surface
    NOTHING, so any confirmed-revert item in a later next-pass proves the confirmed
    flag — recorded THROUGH cowork — reached the live planner. Mirrors
    ``test_confirmed_revert_live._seed_confirmed_revert`` but via cowork commands,
    not raw ``ProjectMemory`` calls.
    """
    s, m = _stems(), _manifest()

    ctx_base = build_context(stems=s, manifest=m, memory_dir=str(memory_dir))
    run_command("record_mix_pass", ctx_base, name="baseline")

    ctx_rev = build_context(stems=s, manifest=m, memory_dir=str(memory_dir))
    baseline_sc = ctx_rev["result"].doctrine_score.get("section_contrast_score") or 60
    # The move IMPROVED the score, yet the operator confirmed reverting it.
    ctx_rev["result"].doctrine_score["section_contrast_score"] = baseline_sc + 20
    run_command("record_mix_pass", ctx_rev, name="reverted_pass", reverted=True)


def test_loop_closes_through_cowork_no_rerun(tmp_path):
    """Record a confirmed revert THROUGH cowork, then a FRESH context's
    ``suggest_next_pass`` surfaces it — the loop closes inside the cowork surface.

    No re-run by hand: after recording via ``record_mix_pass``, a brand-new
    ``build_context(memory_dir=...)`` runs a fresh ``analyze(memory_dir=...)`` and
    ``suggest_next_pass`` reads its ``next_pass``. The confirmed "Revert last pass"
    item must appear, marked operator-confirmed. This FAILS without the new
    command's live wiring (proven by ``test_..._requires_live_wiring`` below) and
    PASSES at tip — the loop is closeable ENTIRELY within cowork.
    """
    s, m = _stems(), _manifest()
    seeded = tmp_path / "cowork_loop_store"

    # (1) OUTCOME half — recorded through cowork.
    _record_confirmed_revert_through_cowork(seeded)

    # (2) READ half — a FRESH context, no manual planner re-run.
    ctx_no = build_context(stems=s, manifest=m)
    ctx_mem = build_context(stems=s, manifest=m, memory_dir=str(seeded))

    np_no = run_command("suggest_next_pass", ctx_no)
    np_mem = run_command("suggest_next_pass", ctx_mem)

    # Sanity: the memoryless run surfaces no revert.
    assert not any(it["title"] == "Revert last pass" for it in np_no)

    # The confirmed revert — recorded via cowork — reaches the live next-pass.
    revert = next((it for it in np_mem if it["title"] == "Revert last pass"), None)
    assert revert is not None, "confirmed revert recorded via cowork must close the loop"
    assert "confirm" in revert["evidence"].lower()
    assert np_mem != np_no  # the recorded outcome measurably changed the next pass


def test_loop_close_requires_live_wiring(tmp_path):
    """The liveness test above is LOAD-BEARING: it FAILS without the live wiring.

    We simulate a handler that does NOT hit the live channel — recording to a
    DIFFERENT (empty) memory dir, exactly what a broken/misrouted handler would
    produce. The fresh next-pass then sees an empty store and surfaces no revert,
    so the ``assert revert is not None`` gate above would fail. This proves the
    loop closes because the record is genuinely persisted/threaded, not because
    the assertion is vacuous.
    """
    s, m = _stems(), _manifest()
    recorded_to = tmp_path / "confirmed_revert_store"
    read_from = tmp_path / "elsewhere_empty_store"  # handler "missed" the live dir

    _record_confirmed_revert_through_cowork(recorded_to)

    # Read a DIFFERENT store than the one written — the not-persisted/not-threaded case.
    ctx_broken = build_context(stems=s, manifest=m, memory_dir=str(read_from))
    np_broken = run_command("suggest_next_pass", ctx_broken)
    assert not any(it["title"] == "Revert last pass" for it in np_broken), \
        "with no live record threaded, the loop must NOT surface a revert"
