"""History-aware next-pass planner tests (P-008 — the OUTCOME side of the loop).

``plan_next_pass`` gains an opt-in trailing ``history`` arg. These tests pin:

  (1) **Byte-identical default:** no history == ``history=None`` == ``history=[]``
      across every ``analyzed`` fixture, with no ``evidence`` key anywhere.
  (2) **got_worse demotes:** a prior pass that recommended "Section contrast" and
      recorded ``section_contrast_score 70->62`` getting worse pushes that move's
      rank down (or out of the top-5), with an evidence line naming the target.
  (3) **Revert surfaced:** a non-empty ``revert_candidates`` surfaces exactly one
      "Revert last pass" move whose detail names the regressed targets.
  (4) **All-regressed degrades gracefully:** still a sane non-empty top-5 with no
      negative priorities.
  (5) **Determinism:** two identical calls produce identical output.

History is consumed only from ``history[-1]`` (the most recent pass). The shape
mirrors ``memory.record_pass``: ``got_worse`` / ``revert_candidates`` are
score-delta strings keyed by ``SCORE_KEYS`` (e.g. ``"section_contrast_score
70->62"``); ``next_recommended`` is the list of prior move *titles* (top 3).
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os.planners.next_pass_planner import plan_next_pass


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _plan(res, history=None):
    """Call the planner exactly as the pipeline does (pipeline.py:196-198)."""
    return plan_next_pass(
        res.records, res.doctrine_score, res.masking_report, res.section_analysis,
        history=history,
    )


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True)


def _history_entry(*, next_recommended, got_worse=None, revert_candidates=None,
                   improved=None):
    """A single mix-pass record in the memory.record_pass shape."""
    return {
        "pass_name": "p1",
        "date": "2026-01-01T00:00:00+00:00",
        "input_bounce": None,
        "scores": {},
        "changes_made": [],
        "improved": improved or [],
        "got_worse": got_worse or [],
        "revert_candidates": revert_candidates or [],
        "next_recommended": next_recommended,
    }


# --------------------------------------------------------------------------- #
# (1) Byte-identical default path.
# --------------------------------------------------------------------------- #
def test_default_path_byte_identical_no_history(analyzed):
    for name, res in analyzed.items():
        base = _plan(res)
        none = _plan(res, history=None)
        empty = _plan(res, history=[])
        assert _canon(base) == _canon(none), name
        assert _canon(base) == _canon(empty), name


def test_default_path_has_no_evidence_key(analyzed):
    for name, res in analyzed.items():
        for history in (None, []):
            for item in _plan(res, history=history):
                assert "evidence" not in item, (name, history, item)


def test_default_path_matches_stored_next_pass(analyzed):
    """The opt-out planner output equals what the pipeline already stored."""
    for name, res in analyzed.items():
        assert _canon(_plan(res)) == _canon(res.mix_plan["next_pass"])


# --------------------------------------------------------------------------- #
# (2) got_worse demotes a recommended-and-regressed move.
# --------------------------------------------------------------------------- #
def test_got_worse_demotes_section_contrast(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    base = _plan(res)
    base_titles = [i["title"] for i in base]
    assert "Section contrast" in base_titles, "fixture must surface Section contrast"
    base_rank = base_titles.index("Section contrast")

    history = [_history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
    )]
    moved = _plan(res, history=history)
    moved_titles = [i["title"] for i in moved]

    # It drops in rank, or falls out of the top-5 entirely.
    if "Section contrast" in moved_titles:
        assert moved_titles.index("Section contrast") > base_rank
        item = next(i for i in moved if i["title"] == "Section contrast")
        assert "evidence" in item
        assert "section_contrast_score" in item["evidence"]
    else:
        assert "Section contrast" in base_titles  # confirm it really fell out


def test_evidence_only_on_moved_candidates(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    history = [_history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
    )]
    moved = _plan(res, history=history)
    for item in moved:
        if item["title"] == "Section contrast" and item["title"] in [i["title"] for i in moved]:
            continue
        # untouched candidates never gain an evidence key
        if item["title"] not in ("Section contrast", "Revert last pass"):
            assert "evidence" not in item, item


def test_got_worse_without_recommendation_does_not_demote(analyzed):
    """A regressed score-key whose move was NOT in next_recommended is left
    untouched (conservative — only recommended-and-regressed moves demote)."""
    res = analyzed["dense_chorus_with_loops"]
    base = _plan(res)
    history = [_history_entry(
        next_recommended=["Vocal belief"],  # NOT Section contrast
        got_worse=["section_contrast_score 70->62"],
    )]
    moved = _plan(res, history=history)
    assert _canon(base) == _canon(moved)


# --------------------------------------------------------------------------- #
# (3) Revert candidates surface exactly one "Revert last pass" move.
# --------------------------------------------------------------------------- #
def test_revert_candidates_surface_one_revert_move(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    history = [_history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=["section_contrast_score 70->62",
                           "vocal_centrality_score 80->71"],
    )]
    moved = _plan(res, history=history)
    reverts = [i for i in moved if i["title"] == "Revert last pass"]
    assert len(reverts) == 1
    detail = reverts[0]["detail"]
    assert "section_contrast_score" in detail
    assert "vocal_centrality_score" in detail


def test_no_revert_move_when_no_revert_candidates(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    history = [_history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=[],
    )]
    moved = _plan(res, history=history)
    assert not any(i["title"] == "Revert last pass" for i in moved)


# --------------------------------------------------------------------------- #
# (4) All-recommended-regressed still yields a sane top-5.
# --------------------------------------------------------------------------- #
def test_all_regressed_degrades_gracefully(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    base_titles = [i["title"] for i in _plan(res)]
    history = [_history_entry(
        next_recommended=base_titles,
        got_worse=[
            "section_contrast_score 70->62",
            "vocal_centrality_score 80->71",
            "depth_hierarchy_score 75->60",
        ],
        revert_candidates=["section_contrast_score 70->62"],
    )]
    moved = _plan(res, history=history)
    assert 0 < len(moved) <= 5
    for i, item in enumerate(moved, start=1):
        assert item["priority"] == i
        assert item["priority"] > 0
        assert item["title"] and item["detail"]


def test_priorities_never_negative_or_zero(analyzed):
    for name, res in analyzed.items():
        history = [_history_entry(
            next_recommended=[i["title"] for i in _plan(res)],
            got_worse=[
                "section_contrast_score 70->62",
                "vocal_centrality_score 80->71",
                "depth_hierarchy_score 75->60",
            ],
        )]
        for item in _plan(res, history=history):
            assert item["priority"] >= 1, (name, item)


# --------------------------------------------------------------------------- #
# (5) Determinism.
# --------------------------------------------------------------------------- #
def test_history_is_deterministic(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    history = [_history_entry(
        next_recommended=["Section contrast", "Vocal belief"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=["section_contrast_score 70->62"],
    )]
    a = _plan(res, history=history)
    b = _plan(res, history=history)
    assert _canon(a) == _canon(b)


def test_only_last_history_entry_consulted(analyzed):
    """Only history[-1] matters — an earlier benign entry cannot change output."""
    res = analyzed["dense_chorus_with_loops"]
    last = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
    )
    one = _plan(res, history=[last])
    earlier = _history_entry(next_recommended=["Vocal belief"], got_worse=[])
    two = _plan(res, history=[earlier, last])
    assert _canon(one) == _canon(two)
