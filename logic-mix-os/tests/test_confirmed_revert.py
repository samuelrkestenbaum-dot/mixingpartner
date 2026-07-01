"""Confirmed-revert override tests (P-018 — first CONFIRMED-outcome signal).

Today the learning loop only ever *infers* "that regressed, maybe revert" from
score deltas inside ``memory.record_pass`` (``got_worse`` / ``revert_candidates``)
and the planner's ``_apply_history`` consumes those score-delta strings. This
packet adds one CONFIRMED operator outcome: a ``reverted=True`` flag on a pass.

Semantics chosen by the orchestrator-in-chief: **OVERRIDE (Option A)**. A
confirmed operator revert is ground truth and takes precedence over the
score-inferred guess when they disagree. These tests pin, test-first:

  (1) **``record_pass`` stores ``reverted``** when the flag is set; the default
      (no flag) path is byte-identical to today (no ``reverted`` key written).
  (2) **Override — the non-tautological case:** the score delta says "improved"
      (empty ``got_worse`` / ``revert_candidates``) yet ``reverted=True`` still
      surfaces a confirmed-revert item AND demotes the reverted move. This is what
      proves override rather than an additive echo of the score signal.
  (3) **Distinct evidence:** the confirmed-revert item honestly reflects it is
      operator-CONFIRMED — its wording/evidence differs from the score-inferred
      "Revert last pass" item.
  (4) **Default/no-flag path unchanged:** ``reverted`` absent/False leaves
      ``_apply_history`` byte-identical to the score-inferred behavior.

The unit-level override tests call ``plan_next_pass`` exactly as the pipeline
does (mirroring ``test_next_pass_history``); the ``record_pass`` tests use a real
``ProjectMemory``. No DAW / network / subprocess.
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os.memory import ProjectMemory
from logic_mix_os.planners.next_pass_planner import plan_next_pass


# --------------------------------------------------------------------------- #
# Helpers (mirror test_next_pass_history's shape so the guard is comparable)
# --------------------------------------------------------------------------- #
def _plan(res, history=None):
    return plan_next_pass(
        res.records, res.doctrine_score, res.masking_report, res.section_analysis,
        history=history,
    )


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True)


def _history_entry(*, next_recommended, got_worse=None, revert_candidates=None,
                   improved=None, reverted=None):
    """A single mix-pass record in the memory.record_pass shape.

    ``reverted`` is only added to the record when it is not ``None`` so the
    default path is a byte-for-byte match to a pre-P-018 stored record.
    """
    rec = {
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
    if reverted is not None:
        rec["reverted"] = reverted
    return rec


# --------------------------------------------------------------------------- #
# (1) record_pass stores the confirmed flag; default path byte-identical.
# --------------------------------------------------------------------------- #
def test_record_pass_stores_reverted_flag(analyzed, tmp_path):
    mem = ProjectMemory(tmp_path / "mem")
    r = analyzed["dense_chorus_with_loops"]
    rec = mem.record_pass("mix_pass_01", r, reverted=True)
    assert rec["reverted"] is True
    # Persisted to disk, not just returned.
    stored = mem.history()[-1]
    assert stored["reverted"] is True


def test_record_pass_default_omits_reverted_key(analyzed, tmp_path):
    """No flag -> no ``reverted`` key at all (byte-identical stored history)."""
    mem = ProjectMemory(tmp_path / "mem")
    r = analyzed["dense_chorus_with_loops"]
    rec = mem.record_pass("mix_pass_01", r)
    assert "reverted" not in rec
    assert "reverted" not in mem.history()[-1]


def test_record_pass_explicit_false_omits_reverted_key(analyzed, tmp_path):
    """An explicit ``reverted=False`` is the same as omission — opt-in only."""
    mem = ProjectMemory(tmp_path / "mem")
    r = analyzed["dense_chorus_with_loops"]
    rec = mem.record_pass("mix_pass_01", r, reverted=False)
    assert "reverted" not in rec
    assert "reverted" not in mem.history()[-1]


# --------------------------------------------------------------------------- #
# (2) OVERRIDE — the non-tautological case: score says "improved", operator
#     reverted -> the confirmed revert STILL surfaces AND demotes.
# --------------------------------------------------------------------------- #
def test_confirmed_revert_surfaces_when_score_says_improved(analyzed):
    """The override case: no score-inferred revert candidate, but ``reverted=True``
    still surfaces a confirmed-revert item. Proves override, not additive echo."""
    res = analyzed["dense_chorus_with_loops"]

    # Score-inferred path with an "improved" delta and NO regression: today this
    # surfaces NOTHING (no demotion, no revert move).
    inferred = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=[],
        revert_candidates=[],
        improved=["section_contrast_score 62->72"],
    )
    inferred_out = _plan(res, history=[inferred])
    assert not any(i["title"] == "Revert last pass" for i in inferred_out)

    # Same "improved" pass, but the operator CONFIRMED a revert.
    confirmed = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=[],
        revert_candidates=[],
        improved=["section_contrast_score 62->72"],
        reverted=True,
    )
    confirmed_out = _plan(res, history=[confirmed])
    revert = next((i for i in confirmed_out if i["title"] == "Revert last pass"), None)
    assert revert is not None, "confirmed revert must surface even when score improved"
    # Confirmed revert measurably changes the plan vs the score-inferred (no-op) run.
    assert _canon(confirmed_out) != _canon(inferred_out)


def test_confirmed_revert_demotes_reverted_move_despite_improved_score(analyzed):
    """The reverted move (in ``next_recommended``) is demoted under override even
    though the score delta records NO regression for it."""
    res = analyzed["dense_chorus_with_loops"]
    base = _plan(res)
    base_titles = [i["title"] for i in base]
    assert "Section contrast" in base_titles
    base_rank = base_titles.index("Section contrast")

    confirmed = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=[],            # score says it did NOT get worse
        revert_candidates=[],
        reverted=True,           # ...but the operator reverted it
    )
    moved = _plan(res, history=[confirmed])
    moved_titles = [i["title"] for i in moved]
    if "Section contrast" in moved_titles:
        assert moved_titles.index("Section contrast") > base_rank
        item = next(i for i in moved if i["title"] == "Section contrast")
        assert "evidence" in item
        assert "confirm" in item["evidence"].lower()  # operator-confirmed wording
    else:
        assert "Section contrast" in base_titles  # fell out of top-5


# --------------------------------------------------------------------------- #
# (3) Distinct evidence — confirmed vs score-inferred wording.
# --------------------------------------------------------------------------- #
def test_confirmed_revert_item_distinct_from_score_inferred(analyzed):
    res = analyzed["dense_chorus_with_loops"]

    inferred = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=["section_contrast_score 70->62"],
    )
    confirmed = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=["section_contrast_score 70->62"],
        reverted=True,
    )
    inferred_revert = next(i for i in _plan(res, history=[inferred])
                           if i["title"] == "Revert last pass")
    confirmed_revert = next(i for i in _plan(res, history=[confirmed])
                            if i["title"] == "Revert last pass")

    # Same title, but honestly distinct evidence: the confirmed one is marked as
    # an operator-confirmed outcome, not a score guess.
    assert inferred_revert["evidence"] != confirmed_revert["evidence"]
    assert "confirm" in confirmed_revert["evidence"].lower()
    assert "confirm" not in inferred_revert["evidence"].lower()


def test_confirmed_revert_surfaces_exactly_one_revert_move(analyzed):
    """Override must not double up: exactly one 'Revert last pass' item even when
    BOTH the score signal and the confirmed flag would surface one."""
    res = analyzed["dense_chorus_with_loops"]
    confirmed = _history_entry(
        next_recommended=["Section contrast"],
        got_worse=["section_contrast_score 70->62"],
        revert_candidates=["section_contrast_score 70->62"],
        reverted=True,
    )
    out = _plan(res, history=[confirmed])
    reverts = [i for i in out if i["title"] == "Revert last pass"]
    assert len(reverts) == 1


# --------------------------------------------------------------------------- #
# (4) Default / no-flag path unchanged (opt-in discipline).
# --------------------------------------------------------------------------- #
def test_reverted_absent_is_byte_identical_to_score_inferred(analyzed):
    """A history entry with no ``reverted`` key produces exactly the same plan as
    today's score-inferred path (identical to test_next_pass_history's world)."""
    for name, res in analyzed.items():
        inferred = _history_entry(
            next_recommended=["Section contrast"],
            got_worse=["section_contrast_score 70->62"],
            revert_candidates=["section_contrast_score 70->62"],
        )
        # An explicit reverted=False must be equivalent to omitting it.
        inferred_false = _history_entry(
            next_recommended=["Section contrast"],
            got_worse=["section_contrast_score 70->62"],
            revert_candidates=["section_contrast_score 70->62"],
            reverted=False,
        )
        assert _canon(_plan(res, history=[inferred])) == \
            _canon(_plan(res, history=[inferred_false])), name


def test_confirmed_revert_is_deterministic(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    confirmed = _history_entry(
        next_recommended=["Section contrast", "Vocal belief"],
        got_worse=[],
        reverted=True,
    )
    a = _plan(res, history=[confirmed])
    b = _plan(res, history=[confirmed])
    assert _canon(a) == _canon(b)
