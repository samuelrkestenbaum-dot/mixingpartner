"""P-012 — creative-scoring evidence-nudge layer (option B, PENALTY-ONLY).

These tests are the BINDING guard for the nudge layer. The variant-scoring
path is golden-unguarded (``regression.py`` reads ``doctrine_score``, never
``score_variant``), so the 68/68 golden can never catch a regression here.

Contracts pinned:
  (a) cap: ``|nudged_overall - base_overall| <= CREATIVE_NUDGE_CAP`` for every
      kind x evidence combo; the ``width_bloom`` rows-1+2 worst case lands at
      EXACTLY -2.0 (the cap), never beyond.
  (b) fires-only-on-evidence + emits the exact evidence line; signal absent ->
      no ``score_nudges`` key and dims == curated base.
  (c) base-ranking preservation: two synthetic variants whose base overall
      differ by > cap keep their relative order under max adverse nudges.
  (d) determinism: identical dict (incl. ``score_nudges`` order) on repeat.
  (e) clamp: ``overall_score`` stays in [0, 100] under extreme synthetic bases.
  (f) real-fixture impact: the 3 fixtures' ``winning_variant`` /
      ``governed_winner`` are UNCHANGED by the layer (no silent flip).
"""

from __future__ import annotations

import copy
from pathlib import Path
from types import SimpleNamespace

import pytest

from logic_mix_os.creative import (
    CREATIVE_NUDGE_CAP,
    _KIND_SCORES,
    _NUDGE_TABLE,
    _RISK_PENALTY,
    _apply_nudges,
    run_creative_engine,
    score_variant,
    winning_variant,
)
from logic_mix_os.governance import emotional_truth_lock, govern_branches


_NUMERIC = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]

# Verbatim evidence strings from the nudge table (the contract surface).
ROW1_REASON = (
    "vocal_belief -8: lead vocal is masked (bad_masking) — "
    "pushing a vocal-forward move is risky"
)
ROW2_REASON = "vocal_belief -6: stereo image is already width-crowded"


# --------------------------------------------------------------------------- #
# Fake-result builders: only the masking_report["events"] shape score_variant
# reads. An "event" needs classification + elements.
# --------------------------------------------------------------------------- #
def _event(classification, elements):
    return {"classification": classification, "elements": list(elements)}


def _result(*events):
    return SimpleNamespace(masking_report={"events": list(events)})


def _lead_masked_event():
    # bad_masking with an element containing "vocal" -> fires row 1.
    return _event("bad_masking", ["Lead Vocal", "Rhythm Guitar"])


def _width_event():
    return _event("width_crowding", ["Synth", "Guitar L", "Guitar R"])


def _base_overall(kind):
    b = _KIND_SCORES[kind]
    return sum(b[k] for k in _NUMERIC) / len(_NUMERIC) - _RISK_PENALTY[b["translation"]]


def _variant(kind):
    return {"variant_id": f"v_{kind}", "kind": kind, "name": kind, "changes": []}


# --------------------------------------------------------------------------- #
# Table sanity — the two penalty rows exist and are penalty-only.
# --------------------------------------------------------------------------- #
def test_table_is_penalty_only_and_has_two_rows():
    assert CREATIVE_NUDGE_CAP == 2.0
    assert len(_NUDGE_TABLE) == 2
    # Every row in the table is a penalty (negative delta) — option B is
    # PENALTY-ONLY; a nudge can only LOWER a score, never promote a variant.
    for row in _NUDGE_TABLE:
        assert row["delta"] < 0, row


# --------------------------------------------------------------------------- #
# (a) Cap — bounded on the overall axis.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kind", sorted(_KIND_SCORES))
@pytest.mark.parametrize(
    "events",
    [
        (),
        (_lead_masked_event(),),
        (_width_event(),),
        (_lead_masked_event(), _width_event()),
    ],
)
def test_cap_binds_for_every_kind_evidence_combo(kind, events):
    base_overall = _base_overall(kind)
    scores = score_variant(_variant(kind), _result(*events))
    nudged_overall = scores["overall_score"]
    # Cap holds on the overall axis (allow rounding slack of 0.05).
    assert abs(nudged_overall - round(base_overall, 1)) <= CREATIVE_NUDGE_CAP + 0.05


def test_width_bloom_worst_case_lands_exactly_at_cap():
    """rows 1+2 on width_bloom = -14 raw = -2.0 overall = exactly the cap.
    Must land at exactly -2.0, not beyond."""
    base_overall = round(_base_overall("width_bloom"), 1)
    scores = score_variant(
        _variant("width_bloom"),
        _result(_lead_masked_event(), _width_event()),
    )
    delta = scores["overall_score"] - base_overall
    assert delta == pytest.approx(-CREATIVE_NUDGE_CAP, abs=1e-9)
    # Both rows fired -> two evidence lines.
    assert scores["score_nudges"] == [ROW1_REASON, ROW2_REASON]


# --------------------------------------------------------------------------- #
# (b) Fires-only-on-evidence + emits the exact evidence line.
# --------------------------------------------------------------------------- #
def test_no_evidence_no_nudge_key_and_dims_equal_base():
    for kind in _KIND_SCORES:
        scores = score_variant(_variant(kind), _result())
        assert "score_nudges" not in scores
        base = _KIND_SCORES[kind]
        # Curated base dims flow through untouched.
        assert scores["vocal_belief_score"] == base["vocal_belief"]
        assert scores["technical_score"] == base["technical"]
        assert scores["taste_alignment_score"] == base["taste"]


def test_row1_fires_only_for_listed_kinds_with_lead_masked():
    fire_kinds = {"width_bloom", "vocal_ride", "intimacy_pass"}
    for kind in _KIND_SCORES:
        scores = score_variant(_variant(kind), _result(_lead_masked_event()))
        base_vb = _KIND_SCORES[kind]["vocal_belief"]
        if kind in fire_kinds:
            assert scores["score_nudges"] == [ROW1_REASON]
            # The named dim moved by the table magnitude (-8).
            assert scores["vocal_belief_score"] == base_vb - 8
        else:
            assert "score_nudges" not in scores
            assert scores["vocal_belief_score"] == base_vb


def test_row2_fires_only_for_width_bloom_on_width_crowding():
    for kind in _KIND_SCORES:
        scores = score_variant(_variant(kind), _result(_width_event()))
        base_vb = _KIND_SCORES[kind]["vocal_belief"]
        if kind == "width_bloom":
            assert scores["score_nudges"] == [ROW2_REASON]
            assert scores["vocal_belief_score"] == base_vb - 6
        else:
            assert "score_nudges" not in scores
            assert scores["vocal_belief_score"] == base_vb


def test_apply_nudges_returns_ordered_dim_delta_reason():
    # Pure helper: row 1 then row 2, in table order, both fire on width_bloom.
    fired = _apply_nudges("width_bloom", _result(_lead_masked_event(), _width_event()))
    assert fired == [
        ("vocal_belief", -8, ROW1_REASON),
        ("vocal_belief", -6, ROW2_REASON),
    ]
    # No evidence -> nothing fires.
    assert _apply_nudges("width_bloom", _result()) == []
    # Row 2 is width_bloom-only: vocal_ride with width_crowding fires nothing.
    assert _apply_nudges("vocal_ride", _result(_width_event())) == []


# --------------------------------------------------------------------------- #
# (c) Base-ranking preservation — the bounded layer only re-orders near-ties.
# --------------------------------------------------------------------------- #
def test_base_ranking_preserved_when_base_gap_exceeds_cap():
    # width_bloom base overall ~75.7; subtractive_drop base overall ~85.3:
    # a gap of ~9.6 >> 2*cap. Force max adverse nudges on BOTH (width_bloom
    # gets both rows; subtractive_drop fires nothing) -> order must hold.
    res = _result(_lead_masked_event(), _width_event())
    wb = dict(_variant("width_bloom"))
    sd = dict(_variant("subtractive_drop"))
    wb["scores"] = score_variant(wb, res)
    sd["scores"] = score_variant(sd, res)
    assert _base_overall("width_bloom") + 2 * CREATIVE_NUDGE_CAP < _base_overall(
        "subtractive_drop"
    )
    # subtractive_drop must still outrank width_bloom after the adverse nudge.
    assert sd["scores"]["overall_score"] > wb["scores"]["overall_score"]
    win = winning_variant([wb, sd])
    assert win["winning_variant"] == "v_subtractive_drop"


# --------------------------------------------------------------------------- #
# (d) Determinism — identical dict incl. score_nudges order on repeat.
# --------------------------------------------------------------------------- #
def test_deterministic_repeat_call():
    res = _result(_lead_masked_event(), _width_event())
    v = _variant("width_bloom")
    a = score_variant(v, res)
    b = score_variant(v, res)
    assert a == b
    assert a["score_nudges"] == b["score_nudges"] == [ROW1_REASON, ROW2_REASON]


# --------------------------------------------------------------------------- #
# (e) Clamp — overall_score stays in [0, 100] under extreme synthetic bases.
# --------------------------------------------------------------------------- #
def test_overall_clamped_0_100_under_extreme_bases():
    # Patch _KIND_SCORES with a near-zero and a near-max profile, force nudges,
    # and confirm the [0,100] clamp still holds on the overall axis.
    extreme_low = dict(
        technical=0, halee=0, ramone=0, contrast=0, vocal_belief=0,
        excitement=0, taste=0, translation="high", mono="low",
    )
    extreme_high = dict(
        technical=100, halee=100, ramone=100, contrast=100, vocal_belief=100,
        excitement=100, taste=100, translation="low", mono="low",
    )
    saved = copy.deepcopy(_KIND_SCORES)
    try:
        _KIND_SCORES["width_bloom"] = extreme_low
        lo = score_variant(_variant("width_bloom"),
                           _result(_lead_masked_event(), _width_event()))
        assert 0.0 <= lo["overall_score"] <= 100.0
        _KIND_SCORES["width_bloom"] = extreme_high
        hi = score_variant(_variant("width_bloom"),
                           _result(_lead_masked_event(), _width_event()))
        assert 0.0 <= hi["overall_score"] <= 100.0
    finally:
        _KIND_SCORES.clear()
        _KIND_SCORES.update(saved)


# --------------------------------------------------------------------------- #
# (f) Real-fixture impact — no silent recommendation flip on real data.
# --------------------------------------------------------------------------- #
_FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned current behaviour (captured from today's pipeline before this layer).
_EXPECTED_CREATIVE_WINNERS = {
    "simple_vocal_piano_song": {"vocal_belief": "vocal_A"},
    "dense_chorus_with_loops": {
        "chorus_lift": "chorus_lift_B",
        "density": "density_B",
        "loop": "loop_B",
        "depth": "depth_A",
        "vocal_belief": "vocal_A",
    },
    "splice_loop_problem": {
        "chorus_lift": "chorus_lift_B",
        "loop": "loop_B",
        "vocal_belief": "vocal_A",
    },
}


@pytest.mark.parametrize("fixture", _FIXTURE_NAMES)
def test_real_fixture_winners_unchanged(analyzed, fixture):
    res = analyzed[fixture]
    creative_out = run_creative_engine(res, res.creative["search_mode"])
    expected = _EXPECTED_CREATIVE_WINNERS[fixture]
    seen = {}
    for branch in creative_out["branches"]:
        seen[branch["problem_id"]] = branch["winning"]["winning_variant"]
    assert seen == expected, f"{fixture} creative winning_variant changed: {seen}"


@pytest.mark.parametrize("fixture", _FIXTURE_NAMES)
def test_real_fixture_governed_winners_unchanged(analyzed, fixture):
    res = analyzed[fixture]
    creative_out = run_creative_engine(res, res.creative["search_mode"])
    intent = res.project.intent
    # Mirror the pipeline (run_governance): the lean comes from the truth lock.
    truth_lean = emotional_truth_lock(intent)["lean"]
    governed = govern_branches(creative_out["branches"], intent, truth_lean)
    expected = _EXPECTED_CREATIVE_WINNERS[fixture]
    got = {gb["problem_id"]: gb["governed_winner"] for gb in governed}
    assert got == expected, f"{fixture} governed_winner changed: {got}"
