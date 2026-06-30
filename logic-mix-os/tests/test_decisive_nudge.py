"""P-015 — the masked-vocal nudge is now DECISIVE through the REAL path.

This is the BINDING evidence for P-015. The variant-scoring path is
golden-unguarded (``regression.py`` reads ``doctrine_score``, never
``score_variant``), so these tests are the only guard that the user-signed-off
aesthetic change actually does what it claims.

P-012 shipped a bounded, penalty-only evidence-nudge layer. Under the OLD
curation, row-0 (``lead_masked``) penalized BOTH ``vocal_ride`` and
``intimacy_pass`` equally (-8), so the masked-vocal evidence could never reorder
the ``vocal_belief`` branch (the P-014 finding: latent, never decisive). P-015
changes the curation, user-gated:

  * ``intimacy_pass`` is EXEMPT from row-0 — an intimacy pass is the correct
    response to a masked lead vocal (focused proximity, not brute level/width).
  * the penalty is strengthened -8 -> -14, which maps to -14/7 = -2.0 overall =
    exactly ``CREATIVE_NUDGE_CAP`` (unchanged); the cap now BINDS for vocal_ride.

Net effect in the ``vocal_belief`` branch under a masked lead vocal:
``vocal_ride`` (base 82.9) drops to the cap -> 80.9, while ``intimacy_pass``
(base 81.1, now exempt) is unchanged -> the winner FLIPS from ``vocal_A``
(vocal_ride) to ``vocal_B`` (intimacy_pass) by 0.2.

The proof is driven through the real ``run_creative_engine`` / ``score_variant``
path on a real ``analyze()`` result. The only thing synthesized is the
``bad_masking`` masking event (the wire ``_lead_masked`` reads) — injected onto a
deep COPY so the shared session fixture is never mutated. Fake adapters only: the
fixture is the project's own seeded synthetic stems + manifest. No DAW / Logic /
AppleScript / subprocess / network.
"""

from __future__ import annotations

import copy

import pytest

from logic_mix_os.creative import (
    CREATIVE_NUDGE_CAP,
    _KIND_SCORES,
    _RISK_PENALTY,
    _lead_masked,
    run_creative_engine,
)

# Verbatim row-0 evidence string (the P-015 contract surface).
ROW0_REASON = (
    "vocal_belief -14: lead vocal is masked (bad_masking) — "
    "pushing the vocal forward by level/width is risky here; "
    "bring it into intimate focus instead"
)

_NUMERIC = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]


def _curated_base_overall(kind: str) -> float:
    """Overall score governance ranks on, BEFORE any nudge — the exact formula
    ``score_variant`` uses for ``base_overall``."""
    b = _KIND_SCORES[kind]
    return round(sum(b[k] for k in _NUMERIC) / len(_NUMERIC) - _RISK_PENALTY[b["translation"]], 1)


def _with_lead_masked(result):
    """Deep copy of a real analyze() result with a ``bad_masking`` vocal event
    injected — the exact wire ``_lead_masked`` reads. Copy, never mutate: the
    ``analyzed`` fixture is session-scoped and shared with the collateral tests."""
    r = copy.deepcopy(result)
    r.masking_report.setdefault("events", []).append(
        {"classification": "bad_masking", "elements": ["Lead Vocal", "Rhythm Guitar"]}
    )
    return r


def _vocal_belief_branch(creative_out):
    return next(b for b in creative_out["branches"] if b["problem_id"] == "vocal_belief")


def _variant_by_id(branch, vid):
    return next(v for v in branch["variants"] if v["variant_id"] == vid)


# --------------------------------------------------------------------------- #
# Sanity: a clean analyze() of these fixtures is NOT lead_masked (so the only
# masked-vocal signal in these tests is the one we inject).
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("fixture", ["dense_chorus_with_loops"])
def test_fixture_is_not_lead_masked_unmodified(analyzed, fixture):
    assert _lead_masked(analyzed[fixture]) is False


# --------------------------------------------------------------------------- #
# THE FLIP — layer ON: masked lead vocal -> intimacy_pass (vocal_B) wins.
# --------------------------------------------------------------------------- #
def test_lead_masked_flips_vocal_belief_winner_to_intimacy_pass(analyzed):
    """With ``lead_masked`` true, the vocal_belief branch winner is
    ``vocal_B`` (intimacy_pass). ``vocal_ride`` (vocal_A) carries the -14
    ``score_nudges`` line and sits at the cap (80.9). Asserted on the value
    governance ranks on (``overall_score`` / ``winning_variant``)."""
    res = _with_lead_masked(analyzed["dense_chorus_with_loops"])
    assert _lead_masked(res) is True
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _vocal_belief_branch(out)

    vocal_a = _variant_by_id(branch, "vocal_A")   # vocal_ride
    vocal_b = _variant_by_id(branch, "vocal_B")   # intimacy_pass
    assert vocal_a["kind"] == "vocal_ride"
    assert vocal_b["kind"] == "intimacy_pass"

    # vocal_ride carries the strengthened -14 evidence line and lands at the cap.
    assert vocal_a["scores"].get("score_nudges") == [ROW0_REASON]
    assert vocal_a["scores"]["overall_score"] == pytest.approx(80.9, abs=1e-9)
    # intimacy_pass is EXEMPT: no nudge, unchanged at its curated base 81.1.
    assert "score_nudges" not in vocal_b["scores"]
    assert vocal_b["scores"]["overall_score"] == pytest.approx(81.1, abs=1e-9)

    # The decisive flip: intimacy_pass (vocal_B) now wins, by 0.2.
    assert branch["winning"]["winning_variant"] == "vocal_B"
    assert (
        vocal_b["scores"]["overall_score"] - vocal_a["scores"]["overall_score"]
    ) == pytest.approx(0.2, abs=1e-9)


# --------------------------------------------------------------------------- #
# LOAD-BEARING NEGATIVE CONTROL — layer OFF: no masked vocal -> vocal_ride wins.
# This proves the flip is CAUSED by the masking evidence, not a base re-rank.
# --------------------------------------------------------------------------- #
def test_no_lead_masked_keeps_vocal_ride_winner(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    assert _lead_masked(res) is False  # no masked-vocal event present
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _vocal_belief_branch(out)

    vocal_a = _variant_by_id(branch, "vocal_A")   # vocal_ride
    vocal_b = _variant_by_id(branch, "vocal_B")   # intimacy_pass
    # No nudge fires on either when lead_masked is false.
    assert "score_nudges" not in vocal_a["scores"]
    assert "score_nudges" not in vocal_b["scores"]
    # Base ranking: vocal_ride (82.9) outranks intimacy_pass (81.1).
    assert vocal_a["scores"]["overall_score"] == pytest.approx(82.9, abs=1e-9)
    assert vocal_b["scores"]["overall_score"] == pytest.approx(81.1, abs=1e-9)
    assert branch["winning"]["winning_variant"] == "vocal_A"


# --------------------------------------------------------------------------- #
# BOUNDED — the cap is still ±2.0 and binds vocal_ride exactly.
# --------------------------------------------------------------------------- #
def test_cap_still_two_and_binds_vocal_ride_exactly(analyzed):
    assert CREATIVE_NUDGE_CAP == 2.0
    res = _with_lead_masked(analyzed["dense_chorus_with_loops"])
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _vocal_belief_branch(out)
    vocal_a = _variant_by_id(branch, "vocal_A")   # vocal_ride
    base = _curated_base_overall("vocal_ride")    # 82.9
    movement = vocal_a["scores"]["overall_score"] - base
    # -14 raw / 7 dims = -2.0 overall = exactly the cap (binds, no clamp needed).
    assert movement == pytest.approx(-CREATIVE_NUDGE_CAP, abs=1e-9)
    assert base == pytest.approx(82.9, abs=1e-9)


# --------------------------------------------------------------------------- #
# BOUNDED — a clear-ranking branch does NOT flip under lead_masked.
# subtractive_drop (85.3) is in NO nudge row and outranks every variant by more
# than 2x the cap, so the masked-vocal evidence cannot overturn it.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("problem_id", ["chorus_lift", "density", "loop"])
def test_subtractive_drop_branch_does_not_flip_under_lead_masked(analyzed, problem_id):
    res = _with_lead_masked(analyzed["dense_chorus_with_loops"])
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = next((b for b in out["branches"] if b["problem_id"] == problem_id), None)
    assert branch is not None, problem_id
    winner = _variant_by_id(branch, branch["winning"]["winning_variant"])
    # Every one of these branches is won by a subtractive_drop variant, masked or not.
    assert winner["kind"] == "subtractive_drop"


# --------------------------------------------------------------------------- #
# COLLATERAL SAFETY — no OTHER branch's winner changes between layer OFF and ON.
# Only the vocal_belief branch flips; everything else is identical.
# --------------------------------------------------------------------------- #
def test_only_vocal_belief_branch_flips_under_lead_masked(analyzed):
    clean = analyzed["dense_chorus_with_loops"]
    masked = _with_lead_masked(clean)
    out_clean = run_creative_engine(clean, clean.creative["search_mode"])
    out_masked = run_creative_engine(masked, masked.creative["search_mode"])

    win_clean = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_clean["branches"]}
    win_masked = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_masked["branches"]}

    # Same set of branches.
    assert set(win_clean) == set(win_masked)
    # The ONLY winner that changes is vocal_belief: vocal_A -> vocal_B.
    changed = {pid for pid in win_clean if win_clean[pid] != win_masked[pid]}
    assert changed == {"vocal_belief"}
    assert win_clean["vocal_belief"] == "vocal_A"
    assert win_masked["vocal_belief"] == "vocal_B"
