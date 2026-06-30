"""Live-wire tests for P-009 — real memory threaded into the production path.

P-007 (taste -> governance) and P-008 (history -> next-pass) were INERT in
production: ``pipeline.analyze()`` never received memory, so every real run
passed ``taste_profile=None`` / ``history=None``. P-009 adds one opt-in
``memory_dir`` param to ``analyze()`` and threads it at the cowork prod surface
(``cowork.build_context`` -> ``analyze``). These tests prove, end-to-end and with
REAL ``ProjectMemory`` writes, that:

  (a) the no-memory default path is byte-identical to today (HARD gate),
  (b) a pre-seeded history measurably changes ``mix_plan["next_pass"]``,
  (c) a pre-seeded taste profile measurably changes governance,
  (d) the cowork prod surface (``build_context`` -> ``run_command``) reaches the
      same wire, proving ``cowork.py``'s ``analyze(...)`` call threads memory.

No DAW / network / subprocess: the wire is local JSON I/O of the app's own store.
Deterministic.
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
# Shared seeders (REAL ProjectMemory writes)
# --------------------------------------------------------------------------- #
def _seed_history(memory_dir) -> ProjectMemory:
    """Seed a store so the LATEST pass regressed ``section_contrast_score``.

    Records two real passes through ``ProjectMemory.record_pass``: a baseline,
    then a worse pass whose ``section_contrast_score`` is 20 lower. ``record_pass``
    diffs against the previous pass, so the latest record's ``got_worse`` /
    ``revert_candidates`` carry ``"section_contrast_score ...->..."`` and its
    ``next_recommended`` (taken from the analyzed mix plan) contains the move
    title ``"Section contrast"`` — exactly the (regressed-target, recommended-title)
    pair ``next_pass_planner._apply_history`` demotes.
    """
    mem = ProjectMemory(memory_dir)
    s, m = _stems(), _manifest()

    res_baseline = analyze(s, m)
    mem.record_pass("baseline", res_baseline)

    res_worse = analyze(s, m)
    baseline_sc = res_baseline.doctrine_score.get("section_contrast_score") or 80
    res_worse.doctrine_score["section_contrast_score"] = baseline_sc - 20
    mem.record_pass("worse", res_worse)
    return mem


def _seed_taste(memory_dir) -> ProjectMemory:
    """Seed a store so the taste profile contains the 'narrower' statement.

    ``add_feedback("too wide")`` twice crosses the >=2 recurrence threshold
    (``memory.py``), so ``taste_profile()["profile"]`` derives
    ``"tends to prefer narrower stereo images"`` — the statement governance's
    ``_apply_taste`` consumes to down-weight width/room variants.
    """
    mem = ProjectMemory(memory_dir)
    mem.add_feedback("too wide", context="chorus")
    mem.add_feedback("too wide", context="bridge")
    return mem


# --------------------------------------------------------------------------- #
# (a) Byte-identical default path (HARD backward-compat gate)
# --------------------------------------------------------------------------- #
def test_default_path_byte_identical(tmp_path):
    """analyze(s,m) == analyze(s,m, memory_dir=None) == analyze(s,m, empty dir).

    All three runs are memoryless (an empty fresh store degrades to a no-op:
    history()=[] and profile=[] are falsy). The next-pass and governed branches
    must be deep-equal, with no ``evidence`` / ``taste_adjustments`` keys leaking.
    """
    s, m = _stems(), _manifest()
    empty_dir = tmp_path / "empty_store"

    res_noarg = analyze(s, m)
    res_none = analyze(s, m, memory_dir=None)
    res_empty = analyze(s, m, memory_dir=str(empty_dir))

    np_noarg = res_noarg.mix_plan["next_pass"]
    np_none = res_none.mix_plan["next_pass"]
    np_empty = res_empty.mix_plan["next_pass"]
    assert np_noarg == np_none == np_empty

    gb_noarg = res_noarg.governance["governed_branches"]
    gb_none = res_none.governance["governed_branches"]
    gb_empty = res_empty.governance["governed_branches"]
    assert gb_noarg == gb_none == gb_empty

    # No history evidence on the memoryless next-pass.
    for item in np_noarg:
        assert "evidence" not in item
    assert not any(it["title"] == "Revert last pass" for it in np_noarg)

    # No taste adjustments anywhere in the memoryless creative/governance surface.
    for branch in res_noarg.creative.get("branches", []):
        for variant in branch["variants"]:
            assert "taste_adjustments" not in variant.get("governance", {})


# --------------------------------------------------------------------------- #
# (b) History axis end-to-end through analyze(memory_dir=...)
# --------------------------------------------------------------------------- #
def test_history_axis_changes_next_pass(tmp_path):
    """A seeded regression demotes the implicated move and surfaces a revert.

    Memoryless: ``"Section contrast"`` is a normal mid-priority next-pass move.
    With the seeded store, its target ``section_contrast_score`` is in the latest
    pass's ``got_worse`` and its title is in ``next_recommended`` -> it is demoted
    (priority -40) below the take-5 cut, and a single ``"Revert last pass"`` move
    surfaces at the top. This is observed purely through ``analyze()``.
    """
    s, m = _stems(), _manifest()
    seeded = tmp_path / "history_store"
    _seed_history(seeded)

    res_no = analyze(s, m)
    res_hist = analyze(s, m, memory_dir=str(seeded))

    np_no = res_no.mix_plan["next_pass"]
    np_hist = res_hist.mix_plan["next_pass"]

    # Sanity: the memoryless run actually has "Section contrast" to demote.
    no_titles = [it["title"] for it in np_no]
    assert "Section contrast" in no_titles
    assert not any(it["title"] == "Revert last pass" for it in np_no)

    # History axis is live: a "Revert last pass" move surfaces with evidence...
    revert = next((it for it in np_hist if it["title"] == "Revert last pass"), None)
    assert revert is not None, "history-aware run must surface a revert move"
    assert "section_contrast_score" in revert["evidence"]

    # ...and the implicated "Section contrast" move is demoted out of the take-5.
    hist_titles = [it["title"] for it in np_hist]
    assert "Section contrast" not in hist_titles

    # The two runs differ — proves the seeded memory reached the planner.
    assert np_hist != np_no


# --------------------------------------------------------------------------- #
# (c) Taste axis end-to-end through analyze(memory_dir=...)
# --------------------------------------------------------------------------- #
def test_taste_axis_changes_governance(tmp_path):
    """A seeded 'narrower' taste down-weights width/room variant identity.

    The narrower-taste profile feeds ``run_governance(..., taste_profile=...)``,
    which down-weights the ``width_bloom`` / ``drum_room_bloom`` variant identity
    (clamped to -15) and annotates a ``taste_adjustments`` evidence line. This is
    observed purely through ``analyze()``'s governance-driven creative surface:
    the memoryless run has NO such adjustment; the seeded run does.
    """
    s, m = _stems(), _manifest()
    seeded = tmp_path / "taste_store"
    mem = _seed_taste(seeded)
    assert "tends to prefer narrower stereo images" in mem.taste_profile()["profile"]

    res_no = analyze(s, m)
    res_taste = analyze(s, m, memory_dir=str(seeded))

    def width_variant(res):
        for branch in res.creative.get("branches", []):
            for v in branch["variants"]:
                if v["kind"] == "width_bloom":
                    return v
        return None

    wb_no = width_variant(res_no)
    wb_taste = width_variant(res_taste)
    assert wb_no is not None and wb_taste is not None

    gov_no = wb_no["governance"]
    gov_taste = wb_taste["governance"]

    # Memoryless: no taste adjustment recorded.
    assert "taste_adjustments" not in gov_no

    # Seeded: governance down-weighted the width variant's identity and left a
    # taste_adjustments evidence line referencing the narrower-image preference.
    assert "taste_adjustments" in gov_taste
    assert any("narrower stereo images" in line for line in gov_taste["taste_adjustments"])
    assert gov_taste["taste_triangle"]["identity"] < gov_no["taste_triangle"]["identity"]

    # The governance surface differs between the two runs — taste reached it.
    assert res_taste.governance["governed_branches"] != res_no.governance["governed_branches"] \
        or gov_taste != gov_no


# --------------------------------------------------------------------------- #
# (d) Prod surface: cowork.build_context -> run_command reaches the same wire
# --------------------------------------------------------------------------- #
def test_cowork_surface_threads_history(tmp_path):
    """``build_context(..., memory_dir=seeded)`` -> ``suggest_next_pass`` is
    history-aware — proving ``cowork``'s ``analyze(...)`` call threads memory."""
    s, m = _stems(), _manifest()
    seeded = tmp_path / "cowork_history_store"
    _seed_history(seeded)

    ctx_no = build_context(stems=s, manifest=m)
    ctx_mem = build_context(stems=s, manifest=m, memory_dir=str(seeded))

    np_no = run_command("suggest_next_pass", ctx_no)
    np_mem = run_command("suggest_next_pass", ctx_mem)

    assert not any(it["title"] == "Revert last pass" for it in np_no)
    assert any(it["title"] == "Revert last pass" for it in np_mem)
    assert np_mem != np_no


def test_cowork_surface_threads_taste(tmp_path):
    """``build_context(..., memory_dir=seeded)`` -> ``run_governance`` is taste-
    aware — proving the cowork prod surface threads the taste profile too."""
    s, m = _stems(), _manifest()
    seeded = tmp_path / "cowork_taste_store"
    _seed_taste(seeded)

    ctx_no = build_context(stems=s, manifest=m)
    ctx_mem = build_context(stems=s, manifest=m, memory_dir=str(seeded))

    # run_governance returns result.governance; the taste effect is visible on the
    # shared creative variant governance the same analyze() produced.
    def width_gov(ctx):
        for branch in ctx["result"].creative.get("branches", []):
            for v in branch["variants"]:
                if v["kind"] == "width_bloom":
                    return v["governance"]
        return {}

    run_command("run_governance", ctx_no)
    run_command("run_governance", ctx_mem)

    assert "taste_adjustments" not in width_gov(ctx_no)
    assert "taste_adjustments" in width_gov(ctx_mem)
