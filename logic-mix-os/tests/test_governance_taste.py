"""Taste-profile governance tests (P-007 — first closure of the learning loop).

The recorded operator taste profile (the statements ``memory._TASTE_MAP`` emits)
may *bias* variant governance, opt-in and bounded. These tests pin three
contracts:

  (a) default path (no ``taste_profile``) is byte-identical to today,
  (b) an explicit profile shifts a matching-kind variant's ``identity`` and the
      governed winner, carrying an evidence line, bounded by ``TASTE_MAX_DELTA``,
  (c) taste can nudge but never override doctrine (truth-lock veto + kill-switch).
"""

from __future__ import annotations

import copy

from logic_mix_os.governance import (
    TASTE_MAX_DELTA,
    govern_branches,
    govern_variant,
    run_governance,
    validate_action_safety,
)


# --------------------------------------------------------------------------- #
# Fixture builders (mirror the shape creative.py emits — see
# creative._variant / score_variant; only the fields governance reads).
# --------------------------------------------------------------------------- #
def _variant(variant_id: str, kind: str, name: str, *, taste: int,
             overall: float, changes=None) -> dict:
    return {
        "variant_id": variant_id,
        "kind": kind,
        "name": name,
        "changes": changes if changes is not None else [],
        "scores": {
            "ramone_score": 80,
            "listener_excitement_score": 80,
            "vocal_belief_score": 80,
            "technical_score": 80,
            "taste_alignment_score": taste,
            "overall_score": overall,
        },
    }


def _intent(truth: str = "") -> dict:
    return {"singular_emotional_truth": truth, "negative_constraints": []}


def _width_bloom_branch() -> dict:
    """A chorus-lift branch where a ``width_bloom`` variant is the top-ranked
    survivor under a neutral lean, with a runner-up that also survives so the
    governed winner can move when taste pushes width_bloom under the keep line.

    width_bloom identity (taste_alignment_score) = 55 → keep under neutral
    (>= 45). A -15 narrowing nudge drops it to 40 → reject, handing the win to
    the runner-up.
    """
    return {
        "problem_id": "chorus_lift",
        "problem": "Chorus does not lift enough emotionally.",
        "variants": [
            _variant("chorus_lift_A", "width_bloom", "Width Bloom",
                     taste=55, overall=90.0, changes=["Widen supporting bus 60%->75%"]),
            _variant("chorus_lift_C", "vocal_ride", "Vocal-Ride Lift",
                     taste=80, overall=85.0, changes=["Ride lead vocal +1 dB into chorus"]),
        ],
    }


def _single_variant_lean(variant, constraints, truth_lean, **kw):
    return govern_variant(variant, constraints, truth_lean, **kw)


# --------------------------------------------------------------------------- #
# (a) default path unchanged — byte-identical, no taste_adjustments key.
# --------------------------------------------------------------------------- #
def test_govern_variant_default_is_byte_identical():
    v = _variant("chorus_lift_A", "width_bloom", "Width Bloom",
                 taste=55, overall=90.0, changes=["Widen supporting bus 60%->75%"])
    base = govern_variant(copy.deepcopy(v), [], "neutral")
    explicit_none = govern_variant(copy.deepcopy(v), [], "neutral", taste_profile=None)

    assert base == explicit_none
    assert "taste_adjustments" not in base
    assert "taste_adjustments" not in explicit_none


def test_govern_variant_default_omits_taste_adjustments_for_all_leans():
    for lean in ("neutral", "intimate", "big"):
        for kind in ("width_bloom", "vocal_ride", "drum_room_bloom"):
            v = _variant("x", kind, kind, taste=70, overall=88.0)
            g = govern_variant(v, [], lean)
            assert "taste_adjustments" not in g, (lean, kind)


def test_govern_branches_default_byte_identical():
    branch = _width_bloom_branch()
    intent = _intent()
    base = govern_branches([copy.deepcopy(branch)], intent, "neutral")
    explicit_none = govern_branches([copy.deepcopy(branch)], intent, "neutral",
                                    taste_profile=None)
    assert base == explicit_none
    for b in base:
        assert "taste_adjustments" not in b["governance"]


def test_run_governance_default_unchanged(analyzed):
    """The full-pipeline governed_branches must be identical with and without an
    explicit ``taste_profile=None`` — proves the pipeline default path is intact.
    """
    res = analyzed["dense_chorus_with_loops"]
    base = run_governance(res, res.creative)
    explicit_none = run_governance(res, res.creative, taste_profile=None)
    assert base["governed_branches"] == explicit_none["governed_branches"]
    # And matches what the pipeline already stored on the result.
    assert base["governed_branches"] == res.governance["governed_branches"]


# --------------------------------------------------------------------------- #
# (b) an explicit profile shifts identity + winner, with bounded evidence.
# --------------------------------------------------------------------------- #
def test_narrower_taste_lowers_width_bloom_identity_bounded():
    v = _variant("chorus_lift_A", "width_bloom", "Width Bloom",
                 taste=70, overall=90.0)
    no_profile = govern_variant(copy.deepcopy(v), [], "neutral")
    with_profile = govern_variant(
        copy.deepcopy(v), [], "neutral",
        taste_profile=["tends to prefer narrower stereo images"],
    )

    base_id = no_profile["taste_triangle"]["identity"]
    new_id = with_profile["taste_triangle"]["identity"]
    assert new_id < base_id
    assert base_id - new_id <= TASTE_MAX_DELTA
    # Evidence line present, names the reason and the kind.
    adj = with_profile["taste_adjustments"]
    assert adj, "expected a taste_adjustments evidence line"
    line = " ".join(adj).lower()
    assert "adjusted for operator taste" in line
    assert "width_bloom" in line


def test_narrower_taste_changes_governed_winner():
    intent = _intent()

    no_profile = govern_branches([_width_bloom_branch()], intent, "neutral")
    # Re-run on a fresh branch (govern_branches mutates variants in place).
    branch_with = _width_bloom_branch()
    with_profile = govern_branches(
        [branch_with], intent, "neutral",
        taste_profile=["tends to prefer narrower stereo images"],
    )

    # Without taste, the high-overall width_bloom survives and wins.
    assert no_profile[0]["governed_winner"] == "chorus_lift_A"
    # With narrower taste, width_bloom is pushed under the keep line → reject,
    # and the surviving runner-up becomes the governed winner.
    assert with_profile[0]["governed_winner"] == "chorus_lift_C"
    # The rejected width_bloom variant carries the taste evidence on its own
    # stored governance (the winner is the untaste-affected vocal_ride).
    width = next(v for v in branch_with["variants"]
                 if v["variant_id"] == "chorus_lift_A")
    assert "taste_adjustments" in width["governance"]
    assert width["governance"]["taste_triangle"]["verdict"] == "reject"


def test_wider_taste_upweights_width_bloom_identity_bounded():
    v = _variant("chorus_lift_A", "width_bloom", "Width Bloom",
                 taste=50, overall=90.0)
    no_profile = govern_variant(copy.deepcopy(v), [], "neutral")
    with_profile = govern_variant(
        copy.deepcopy(v), [], "neutral",
        taste_profile=["prefers wider images"],
    )
    base_id = no_profile["taste_triangle"]["identity"]
    new_id = with_profile["taste_triangle"]["identity"]
    assert new_id > base_id
    assert new_id - base_id <= TASTE_MAX_DELTA
    assert with_profile["taste_adjustments"]


def test_taste_delta_is_clamped_to_bound():
    # An extreme low taste score, even with a wide-image profile, never moves
    # identity by more than the bound.
    v = _variant("x", "width_bloom", "Width Bloom", taste=10, overall=90.0)
    base = govern_variant(copy.deepcopy(v), [], "neutral")["taste_triangle"]["identity"]
    new = govern_variant(copy.deepcopy(v), [], "neutral",
                         taste_profile=["prefers wider images"])["taste_triangle"]["identity"]
    assert abs(new - base) <= TASTE_MAX_DELTA
    assert TASTE_MAX_DELTA < 30


def test_identity_stays_clamped_0_100():
    v_hi = _variant("hi", "width_bloom", "Width Bloom", taste=98, overall=90.0)
    v_lo = _variant("lo", "width_bloom", "Width Bloom", taste=5, overall=90.0)
    hi = govern_variant(v_hi, [], "neutral",
                        taste_profile=["prefers wider images"])
    lo = govern_variant(v_lo, [], "neutral",
                        taste_profile=["tends to prefer narrower stereo images"])
    assert 0 <= hi["taste_triangle"]["identity"] <= 100
    assert 0 <= lo["taste_triangle"]["identity"] <= 100


def test_taste_is_deterministic():
    v = _variant("x", "width_bloom", "Width Bloom", taste=70, overall=90.0)
    profile = ["tends to prefer narrower stereo images"]
    a = govern_variant(copy.deepcopy(v), [], "neutral", taste_profile=profile)
    b = govern_variant(copy.deepcopy(v), [], "neutral", taste_profile=profile)
    assert a == b


# --------------------------------------------------------------------------- #
# (c) taste can nudge but never override doctrine.
# --------------------------------------------------------------------------- #
def test_taste_cannot_clear_truth_lock_veto():
    """Under an intimate lean, width_bloom is doctrine-vetoed (the -30 nudge +
    align veto). A wide-image taste profile must NOT promote it to winner.
    """
    branch = {
        "problem_id": "chorus_lift",
        "problem": "Chorus does not lift enough emotionally.",
        "variants": [
            _variant("chorus_lift_A", "width_bloom", "Width Bloom",
                     taste=80, overall=92.0, changes=["Widen supporting bus 60%->75%"]),
            _variant("chorus_lift_C", "vocal_ride", "Vocal-Ride Lift",
                     taste=80, overall=85.0, changes=["Ride lead vocal +1 dB into chorus"]),
        ],
    }
    intent = _intent("Intimate and conflicted, quietly falling apart.")

    governed = govern_branches(
        [copy.deepcopy(branch)], intent, "intimate",
        taste_profile=["prefers wider images"],
    )
    assert governed[0]["governed_winner"] != "chorus_lift_A"


def test_taste_does_not_reach_kill_switch():
    """validate_action_safety is a separate path govern_variant never calls;
    risk-class-5 / destructive blocks are unchanged regardless of taste input.
    """
    rc5 = validate_action_safety({"risk_class": 5, "plugin": "x", "setting": "y"})
    assert rc5["blocked"] is True
    destructive = validate_action_safety(
        {"risk_class": 2, "plugin": "EQ", "setting": "overwrite file"})
    assert destructive["blocked"] is True
    safe = validate_action_safety(
        {"risk_class": 2, "plugin": "Channel EQ", "setting": "cut 250 Hz"})
    assert safe["blocked"] is False


def test_taste_does_not_lift_align_veto_below_50():
    """An intimate lean gives width_bloom align=45 (< 50) → vetoed by doctrine.
    Taste only moves identity, so it cannot un-veto an align<50 variant.
    """
    v = _variant("x", "width_bloom", "Width Bloom", taste=99, overall=92.0)
    g = govern_variant(v, [], "intimate", taste_profile=["prefers wider images"])
    assert g["vetoed"] is True
    assert g["verdict"] == "reject"
