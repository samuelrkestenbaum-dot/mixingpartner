"""P-013 — Option-B nudge visibility through the live ``analyze()`` path.

P-012 shipped a bounded, penalty-only evidence-nudge layer on the creative
variant scores (``creative._apply_nudges`` / ``_NUDGE_TABLE``, capped at
``CREATIVE_NUDGE_CAP = 2.0`` on the overall axis governance ranks on). That layer
is pinned at the UNIT level in ``test_creative_nudges.py`` with hand-built
``SimpleNamespace`` results. This module lifts the claim to REAL DATA: it proves
the nudge actually FIRES through the production ``pipeline.analyze()`` path on a
realistic fixture, and that the documented latent-but-armed posture holds —

    OPTION (a): the cap binds and the winner does NOT flip.

On ``dense_chorus_with_loops`` the live masking analyzer emits a real
``width_crowding`` event over the three guitars, so the row-2 nudge
(``vocal_belief -6: stereo image is already width-crowded``) fires on the
``chorus_lift`` ``width_bloom`` variant (``chorus_lift_A``) through ``analyze()``.
The nudge lowers its ``overall_score`` from the curated base 75.7 to 74.9 — a
real, evidence-backed movement that stays well inside the ±2.0 bound — yet the
governed/creative winner remains ``chorus_lift_B`` (``subtractive_drop``, 85.3),
because the base gap (~9.6) far exceeds twice the cap. The nudge is ARMED on real
data and still cannot overturn a clear ranking.

Fake adapters only: the fixture is the project's own seeded synthetic stems +
manifest run through ``analyze()``. No DAW / Logic / AppleScript / subprocess /
network.
"""

from __future__ import annotations

import pathlib

import pytest

from logic_mix_os.creative import (
    CREATIVE_NUDGE_CAP,
    _KIND_SCORES,
    _RISK_PENALTY,
    _apply_nudges,
)
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "dense_chorus_with_loops"

# Verbatim row-2 evidence string (the width_crowding nudge) — the contract surface.
ROW2_REASON = "vocal_belief -6: stereo image is already width-crowded"

_NUMERIC = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]


def _curated_base_overall(kind: str) -> float:
    """The overall score the governance ranks on, BEFORE any nudge — exactly the
    formula ``score_variant`` uses for ``base_overall`` (creative.py)."""
    b = _KIND_SCORES[kind]
    return round(sum(b[k] for k in _NUMERIC) / len(_NUMERIC) - _RISK_PENALTY[b["translation"]], 1)


@pytest.fixture(scope="module")
def dense_result():
    """One real ``analyze()`` run of the dense fixture (fake adapters: seeded
    synthetic stems + manifest, local file I/O only)."""
    manifest = load_manifest(FIXTURE / "project_manifest.json")
    return analyze(str(FIXTURE / "stems"), manifest)


def _chorus_lift_width_bloom(result) -> dict:
    branch = next(b for b in result.creative["branches"] if b["problem_id"] == "chorus_lift")
    return next(v for v in branch["variants"] if v["kind"] == "width_bloom")


# --------------------------------------------------------------------------- #
# The nudge FIRES on real data through analyze().
# --------------------------------------------------------------------------- #
def test_width_crowding_nudge_fires_through_analyze(dense_result):
    """The live masking analyzer emits a real ``width_crowding`` event, so the
    row-2 nudge fires on the production ``chorus_lift`` width_bloom variant and
    the exact evidence line is emitted — proven end-to-end, not at the unit
    level."""
    # The fixture genuinely produces a width_crowding masking event (the wire the
    # nudge predicate reads), so the row fires through analyze().
    classifications = {e["classification"] for e in dense_result.masking_report["events"]}
    assert "width_crowding" in classifications, (
        "dense fixture must produce a real width_crowding masking event to arm the nudge"
    )
    fired = _apply_nudges("width_bloom", dense_result)
    assert fired == [("vocal_belief", -6, ROW2_REASON)]

    wb = _chorus_lift_width_bloom(dense_result)
    # The transparency contract: the fired evidence line is present on the score.
    assert wb["scores"].get("score_nudges") == [ROW2_REASON]


# --------------------------------------------------------------------------- #
# OPTION (a): the cap binds — movement on the governed axis stays within ±2.0.
# --------------------------------------------------------------------------- #
def test_nudge_movement_on_governed_axis_within_bound(dense_result):
    """Assert on the value governance ranks on (``overall_score``): the live nudge
    lowers the width_bloom overall from its curated base, and the movement is real
    (non-zero) yet strictly inside the ±CREATIVE_NUDGE_CAP bound."""
    wb = _chorus_lift_width_bloom(dense_result)
    base_overall = _curated_base_overall("width_bloom")  # 75.7
    nudged_overall = wb["scores"]["overall_score"]        # 74.9 through analyze()

    movement = nudged_overall - base_overall
    # Real, evidence-backed movement (the nudge actually moved the governed axis)...
    assert movement < 0, "the width_crowding nudge must lower the governed overall score"
    assert movement != 0.0
    # ...bounded: never exceeds the cap on the overall axis governance ranks on.
    assert abs(movement) <= CREATIVE_NUDGE_CAP + 1e-9
    # And concretely, the -6 vocal_belief penalty / 7 numeric dims = ~-0.857 overall,
    # well inside the cap (it did not even need clamping).
    assert nudged_overall == pytest.approx(74.9, abs=1e-9)
    assert base_overall == pytest.approx(75.7, abs=1e-9)


# --------------------------------------------------------------------------- #
# OPTION (a): the winner does NOT flip — armed yet cannot overturn the ranking.
# --------------------------------------------------------------------------- #
def test_armed_nudge_does_not_flip_creative_winner(dense_result):
    """Even though the nudge fires and lowers width_bloom on real data, the
    creative ``winning_variant`` for ``chorus_lift`` stays ``chorus_lift_B``
    (subtractive_drop) — the latent-but-armed posture, proven end-to-end."""
    branch = next(
        b for b in dense_result.creative["branches"] if b["problem_id"] == "chorus_lift"
    )
    # The fired nudge is visible on the branch (proof it ran on this very branch)...
    wb = next(v for v in branch["variants"] if v["kind"] == "width_bloom")
    assert wb["scores"].get("score_nudges") == [ROW2_REASON]
    # ...yet the winner is the unrelated, higher-base subtractive_drop, not width_bloom.
    assert branch["winning"]["winning_variant"] == "chorus_lift_B"
    assert branch["winning"]["winning_variant"] != wb["variant_id"]


def test_armed_nudge_does_not_flip_governed_winner(dense_result):
    """The governance layer (the layer that actually ranks) likewise keeps
    ``chorus_lift_B`` as the governed winner — the bounded nudge cannot overturn a
    clear governed ranking. Asserted on the production governance surface."""
    gb = next(
        b for b in dense_result.governance["governed_branches"]
        if b["problem_id"] == "chorus_lift"
    )
    assert gb["governed_winner"] == "chorus_lift_B"


def test_base_gap_exceeds_twice_the_cap_so_no_flip_is_possible(dense_result):
    """The structural reason the winner cannot flip: the curated base gap between
    the winner (subtractive_drop) and the nudged variant (width_bloom) is larger
    than 2x the cap, so no bounded penalty on width_bloom can ever reorder them.

    This pins WHY option (a) holds — the armed nudge is mathematically incapable of
    overturning this ranking, not merely observed not to."""
    gap = _curated_base_overall("subtractive_drop") - _curated_base_overall("width_bloom")
    assert gap > 2 * CREATIVE_NUDGE_CAP, (gap, 2 * CREATIVE_NUDGE_CAP)
