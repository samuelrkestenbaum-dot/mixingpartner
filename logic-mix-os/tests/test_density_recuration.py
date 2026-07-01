"""P-017 — minimal doctrine-honest ``_KIND_SCORES`` re-curation of the depth /
hierarchy move (``depth_cleanup``) for the ``density`` problem.

The GOAL was to let the depth move win the ``density`` branch, but ONLY with
doctrine-HONEST base-value re-judgments — honesty beats the flip. The HONESTY
CLAUSE (P-014 discipline) says: if the minimal set of defensible re-judgments
cannot lift ``depth_cleanup`` above ``subtractive_drop``'s 85.29, STOP and report
a FINDING rather than inflate to force the win.

OUTCOME: **FINDING.** An honest re-curation narrows but cannot flip the
``density`` branch; the current curated values legitimately edge the depth move
for this problem. The arithmetic (below) shows the single clearest honest
under-valuation — ``contrast`` (72 → 88), because creating foreground/midground/
background separation IS perceptual contrast (``masking_hierarchy`` +
``section_contrast_considered``) — lifts ``depth_cleanup`` from 81.14 only to
83.43, still 1.86 short of 85.29. The remaining gap lives in ``excitement``
(66 vs subtractive_drop's 78), which is OFF-LIMITS to inflate: subtle depth work
is honestly un-flashy. Even pushing ``contrast`` to the impossible max of 100
lands at 85.14 — STILL below the threshold. So no honest set of dim re-judgments
flips ``density``; ``_KIND_SCORES`` is therefore LEFT UNTOUCHED.

These assertions are the BINDING guard for that finding (the variant-scoring path
is golden-unguarded — ``regression.py`` reads ``doctrine_score``, never
``score_variant``). They pin, on the REAL ``analyze()`` / ``run_creative_engine``
path:
  (1) the full 5-branch winner table (chorus_lift, density, loop, depth,
      vocal_belief) — proving NOTHING changed;
  (2) the honest-ceiling arithmetic: the doctrine-honest ``contrast`` re-judgment
      cannot lift ``depth_cleanup`` to a density win, and neither can the
      absolute (inflated) ceiling — so the finding is unavoidable, not a failure
      to search hard enough;
  (3) that ``_KIND_SCORES`` is unchanged from its curated base (no product
      change was made).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from logic_mix_os.creative import (
    _KIND_SCORES,
    _RISK_PENALTY,
    run_creative_engine,
)

_ROOT = Path(__file__).resolve().parent.parent
_NUMERIC = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]

# The fixture that exercises ALL FIVE creative branches on the real path.
_FIVE_BRANCH_FIXTURE = "dense_chorus_with_loops"

# Pinned current real-path winner table (captured from run_creative_engine on the
# analyzed fixture BEFORE P-017). The finding is: this table is UNCHANGED, because
# no product change was made.
_EXPECTED_WINNERS = {
    "chorus_lift": ("chorus_lift_B", "subtractive_drop"),
    "density": ("density_B", "subtractive_drop"),
    "loop": ("loop_B", "subtractive_drop"),
    "depth": ("depth_A", "depth_cleanup"),
    "vocal_belief": ("vocal_A", "vocal_ride"),
}


def _base_overall(dims: dict) -> float:
    return sum(dims[k] for k in _NUMERIC) / len(_NUMERIC) - _RISK_PENALTY[dims["translation"]]


def _winner_table(analyzed):
    res = analyzed[_FIVE_BRANCH_FIXTURE]
    out = run_creative_engine(res, res.creative["search_mode"])
    table = {}
    for b in out["branches"]:
        wid = b["winning"]["winning_variant"]
        winner = next(v for v in b["variants"] if v["variant_id"] == wid)
        table[b["problem_id"]] = (wid, winner["kind"], winner["scores"]["overall_score"])
    return table


# --------------------------------------------------------------------------- #
# (1) The FULL 5-branch winner table on the REAL path is UNCHANGED — the finding
#     is "nothing flips", so every branch keeps its curated-base winner.
# --------------------------------------------------------------------------- #
def test_all_five_branches_present(analyzed):
    table = _winner_table(analyzed)
    assert set(table) == set(_EXPECTED_WINNERS), table


@pytest.mark.parametrize("problem_id", sorted(_EXPECTED_WINNERS))
def test_branch_winner_unchanged(analyzed, problem_id):
    table = _winner_table(analyzed)
    expected_id, expected_kind = _EXPECTED_WINNERS[problem_id]
    got_id, got_kind, _score = table[problem_id]
    assert (got_id, got_kind) == (expected_id, expected_kind), (
        f"{problem_id} winner changed: got {(got_id, got_kind)}, "
        f"expected {(expected_id, expected_kind)}"
    )


def test_density_branch_still_won_by_subtractive_drop(analyzed):
    """The load-bearing assertion of the FINDING: density is STILL won by
    ``density_B`` / ``subtractive_drop`` — the depth move (``density_A`` /
    ``depth_cleanup``) did NOT flip it, because no honest re-curation could."""
    table = _winner_table(analyzed)
    dens_id, dens_kind, dens_score = table["density"]
    assert dens_id == "density_B"
    assert dens_kind == "subtractive_drop"
    # subtractive_drop's curated overall is the value that legitimately edges the
    # depth move here.
    assert dens_score == pytest.approx(85.3, abs=0.05)


# --------------------------------------------------------------------------- #
# (2) The HONEST-CEILING arithmetic — the finding is unavoidable, not a failure
#     to search. ``mean(7 dims) - risk_penalty`` is the axis governance ranks on.
# --------------------------------------------------------------------------- #
def test_curated_base_gap_is_the_documented_4_14(analyzed):
    dc = _base_overall(_KIND_SCORES["depth_cleanup"])
    sd = _base_overall(_KIND_SCORES["subtractive_drop"])
    assert dc == pytest.approx(81.1429, abs=1e-3)
    assert sd == pytest.approx(85.2857, abs=1e-3)
    assert sd - dc == pytest.approx(4.1429, abs=1e-3)


def test_honest_contrast_rejudgment_narrows_but_cannot_flip():
    """The single clearest doctrine-honest re-judgment: ``contrast`` 72 -> 88
    (matching ``subtractive_drop`` — creating depth IS perceptual contrast). It
    lifts ``depth_cleanup`` from 81.14 to only 83.43, still SHORT of 85.29. This
    is the crux of the finding: the honest move narrows the gap but does not
    close it."""
    sd = _base_overall(_KIND_SCORES["subtractive_drop"])

    honest = dict(_KIND_SCORES["depth_cleanup"])
    honest["contrast"] = 88  # the honest re-judgment
    honest_overall = _base_overall(honest)

    assert honest_overall == pytest.approx(83.4286, abs=1e-3)
    # It narrows the gap from 4.14 to ~1.86 ...
    assert (sd - honest_overall) == pytest.approx(1.8571, abs=1e-3)
    # ... but does NOT reach the win threshold. Honest -> no flip.
    assert honest_overall < sd


def test_even_max_contrast_cannot_flip_without_touching_excitement():
    """Push ``contrast`` to the impossible maximum of 100 (pure inflation, well
    past any defensible re-judgment) and ``depth_cleanup`` STILL lands at 85.14 <
    85.29. The residual gap lives in ``excitement`` (66 vs 78), which is OFF-LIMITS
    to inflate because subtle depth work is honestly un-flashy. So NO honest set
    of dim re-judgments flips ``density`` — the finding is arithmetically forced,
    not a matter of searching harder."""
    sd = _base_overall(_KIND_SCORES["subtractive_drop"])

    maxed = dict(_KIND_SCORES["depth_cleanup"])
    maxed["contrast"] = 100
    maxed_overall = _base_overall(maxed)

    assert maxed_overall == pytest.approx(85.1429, abs=1e-3)
    assert maxed_overall < sd  # even the inflated ceiling cannot flip it


# --------------------------------------------------------------------------- #
# (3) NO product change was made — ``_KIND_SCORES`` is exactly its curated base.
# --------------------------------------------------------------------------- #
def test_depth_cleanup_base_is_untouched():
    """The finding produces NO product change: ``depth_cleanup``'s curated dims
    are exactly as before P-017 (excitement honestly stays 66, contrast stays
    72 — no dim was re-judged into the codebase, because none could flip the
    branch honestly)."""
    assert _KIND_SCORES["depth_cleanup"] == dict(
        technical=84, halee=90, ramone=85, contrast=72,
        vocal_belief=86, excitement=66, taste=85,
        translation="low", mono="low",
    )


def test_subtractive_drop_base_is_untouched():
    """The competing move is likewise untouched — the finding changes nothing."""
    assert _KIND_SCORES["subtractive_drop"] == dict(
        technical=85, halee=88, ramone=86, contrast=88,
        vocal_belief=86, excitement=78, taste=86,
        translation="low", mono="low",
    )
