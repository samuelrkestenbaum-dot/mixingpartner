"""Liveness + CLI wire for P-018's confirmed revert (the P-016 anti-inertness lesson).

A confirmed operator revert MUST measurably change a REAL ``analyze(memory_dir=...)``
run's ``next_pass`` output — it must not be an inert stored field. These tests
prove that end-to-end with REAL ``ProjectMemory`` writes and the production
pipeline, WITHOUT re-running the planner by hand:

  (a) **Liveness (no re-run):** a memory dir seeded with a pass recorded
      ``reverted=True`` — whose score delta says the move IMPROVED (the override
      case) — makes the real ``analyze(memory_dir=...)`` surface a confirmed
      ``"Revert last pass"`` item and demote the reverted move. The memoryless run
      surfaces neither. This is the load-bearing liveness gate: it FAILS before the
      ``_apply_history`` consumer change and PASSES after.
  (b) **CLI wire:** ``memory-record --reverted`` persists ``reverted=True`` on the
      pass, and the same store WITHOUT the flag omits the key (byte-identical
      default, opt-in discipline).

No DAW / network / subprocess: the wire is local JSON I/O of the app's own store.
Deterministic.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from logic_mix_os import cli
from logic_mix_os.memory import ProjectMemory
from logic_mix_os.pipeline import analyze

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "dense_chorus_with_loops"


def _manifest() -> dict:
    return json.loads((FIXTURE / "project_manifest.json").read_text())


def _stems() -> str:
    return str(FIXTURE / "stems")


def _seed_confirmed_revert(memory_dir) -> ProjectMemory:
    """Seed a store whose LATEST pass is a CONFIRMED revert on an IMPROVED score.

    Records two real passes: a baseline, then a pass whose
    ``section_contrast_score`` is 20 HIGHER (so the score-delta inference says the
    move IMPROVED — empty ``got_worse`` / ``revert_candidates``), but recorded with
    ``reverted=True``. This is the non-tautological override case: the score signal
    would surface NOTHING, so any confirmed-revert output in ``analyze()`` proves
    the confirmed flag — not the score guess — reached the live planner.
    """
    mem = ProjectMemory(memory_dir)
    s, m = _stems(), _manifest()

    res_baseline = analyze(s, m)
    mem.record_pass("baseline", res_baseline)

    res_better = analyze(s, m)
    baseline_sc = res_better.doctrine_score.get("section_contrast_score") or 60
    res_better.doctrine_score["section_contrast_score"] = baseline_sc + 20
    # The move IMPROVED the score, yet the operator confirmed reverting it.
    mem.record_pass("reverted_pass", res_better, reverted=True)
    return mem


# --------------------------------------------------------------------------- #
# (a) Liveness: no re-run, through real analyze(memory_dir=...)
# --------------------------------------------------------------------------- #
def test_confirmed_revert_is_live_in_analyze(tmp_path):
    """The confirmed revert genuinely changes real analyze() output (not inert).

    Override case: the seeded latest pass IMPROVED section_contrast_score, so the
    score-inferred path alone would surface no revert. Because it is recorded
    reverted=True, the live planner must surface a confirmed 'Revert last pass'
    item whose evidence marks it operator-confirmed.
    """
    s, m = _stems(), _manifest()
    seeded = tmp_path / "confirmed_revert_store"
    _seed_confirmed_revert(seeded)

    res_no = analyze(s, m)
    res_rev = analyze(s, m, memory_dir=str(seeded))

    np_no = res_no.mix_plan["next_pass"]
    np_rev = res_rev.mix_plan["next_pass"]

    # Sanity: memoryless run has no revert move and does surface Section contrast.
    no_titles = [it["title"] for it in np_no]
    assert not any(it["title"] == "Revert last pass" for it in np_no)
    assert "Section contrast" in no_titles

    # Live: the confirmed revert surfaces, marked operator-confirmed.
    revert = next((it for it in np_rev if it["title"] == "Revert last pass"), None)
    assert revert is not None, "confirmed revert must reach live analyze() output"
    assert "confirm" in revert["evidence"].lower()

    # The reverted move (Section contrast, which the reverted pass recommended) is
    # demoted despite the score saying it IMPROVED — the override reached the live
    # plan. Either it drops in rank vs the memoryless run, or it falls out of the
    # take-5; and if still present it carries the operator-confirmed evidence.
    rev_titles = [it["title"] for it in np_rev]
    no_rank = no_titles.index("Section contrast")
    if "Section contrast" in rev_titles:
        assert rev_titles.index("Section contrast") > no_rank
        sc_item = next(it for it in np_rev if it["title"] == "Section contrast")
        assert "confirm" in sc_item["evidence"].lower()
    # else: fell out of the top-5 entirely — also a valid demotion.

    # The two runs differ — proves the seeded confirmed revert reached the planner.
    assert np_rev != np_no


def test_confirmed_revert_no_flag_is_byte_identical(tmp_path):
    """A store seeded WITHOUT the confirmed flag (same improved delta) surfaces no
    revert — the confirmed-revert output above is not an artefact of the seed."""
    s, m = _stems(), _manifest()
    seeded = tmp_path / "no_flag_store"

    mem = ProjectMemory(seeded)
    res_baseline = analyze(s, m)
    mem.record_pass("baseline", res_baseline)
    res_better = analyze(s, m)
    baseline_sc = res_better.doctrine_score.get("section_contrast_score") or 60
    res_better.doctrine_score["section_contrast_score"] = baseline_sc + 20
    mem.record_pass("improved_pass", res_better)  # NO reverted flag

    res_no = analyze(s, m)
    res_seeded = analyze(s, m, memory_dir=str(seeded))

    # No confirmed flag + improved score => no revert, next_pass identical to today.
    assert res_seeded.mix_plan["next_pass"] == res_no.mix_plan["next_pass"]


# --------------------------------------------------------------------------- #
# (b) CLI wire: --reverted persists the confirmed flag; default omits it.
# --------------------------------------------------------------------------- #
def test_cli_memory_record_reverted_persists_flag(tmp_path):
    mem_dir = tmp_path / "cli_reverted_store"
    manifest_path = str(FIXTURE / "project_manifest.json")
    rc = cli.main([
        "memory-record",
        "--stems", _stems(),
        "--manifest", manifest_path,
        "--memory-dir", str(mem_dir),
        "--name", "mix_pass_reverted",
        "--reverted",
    ])
    assert rc == 0
    history = ProjectMemory(mem_dir).history()
    assert history[-1]["reverted"] is True


def test_cli_memory_record_default_omits_flag(tmp_path):
    mem_dir = tmp_path / "cli_default_store"
    manifest_path = str(FIXTURE / "project_manifest.json")
    rc = cli.main([
        "memory-record",
        "--stems", _stems(),
        "--manifest", manifest_path,
        "--memory-dir", str(mem_dir),
        "--name", "mix_pass_plain",
    ])
    assert rc == 0
    history = ProjectMemory(mem_dir).history()
    assert "reverted" not in history[-1]
