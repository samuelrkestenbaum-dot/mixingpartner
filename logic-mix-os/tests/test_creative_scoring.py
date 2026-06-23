"""Layer 2 — context-sensitive creative variant scoring (Hardening Packet 1)."""

from __future__ import annotations

from logic_mix_os.creative import score_variant
from logic_mix_os.renderers.creative_renderer import render_creative


def ctx(**over):
    base = dict(contrast_deficit=0.5, overcrowding=0.5, masking_pressure=0.2, vocal_risk=0.2,
                loop_pressure=0.3, width_room=0.5, static_dynamic_gap=0.5, intimate=0.0, lean="neutral")
    base.update(over)
    return base


def var(kind, problem):
    return {"kind": kind, "problem": problem, "name": kind}


def test_width_bloom_better_with_room_and_no_wash_risk():
    good = score_variant(var("width_bloom", "chorus_lift"),
                         ctx(contrast_deficit=0.9, width_room=0.9, masking_pressure=0.0, overcrowding=0.2, intimate=0.0))
    bad = score_variant(var("width_bloom", "chorus_lift"),
                        ctx(contrast_deficit=0.9, width_room=0.1, masking_pressure=0.8, overcrowding=0.8, intimate=1.0))
    assert good["overall_score"] > bad["overall_score"]
    assert good["vocal_belief_score"] > bad["vocal_belief_score"]


def test_subtractive_better_when_foreground_crowded():
    crowded = score_variant(var("subtractive_drop", "density"), ctx(overcrowding=0.9, masking_pressure=0.6))
    sparse = score_variant(var("subtractive_drop", "density"), ctx(overcrowding=0.1, masking_pressure=0.0))
    assert crowded["overall_score"] > sparse["overall_score"]


def test_vocal_ride_better_when_vocal_at_risk():
    risky = score_variant(var("vocal_ride", "vocal_belief"), ctx(vocal_risk=0.9))
    safe = score_variant(var("vocal_ride", "vocal_belief"), ctx(vocal_risk=0.0))
    assert risky["overall_score"] > safe["overall_score"]
    assert risky["vocal_belief_score"] >= safe["vocal_belief_score"]


def test_same_kind_scores_differ_by_problem_need():
    c = ctx(contrast_deficit=0.9, overcrowding=0.3, loop_pressure=0.1)
    a = score_variant(var("subtractive_drop", "chorus_lift"), c)  # need = contrast_deficit (high)
    b = score_variant(var("subtractive_drop", "loop"), c)         # need = loop_pressure (low)
    assert a["overall_score"] != b["overall_score"]


def test_each_variant_carries_evidence():
    s = score_variant(var("width_bloom", "chorus_lift"), ctx())
    assert s["evidence"]
    assert all("signal" in e and "value" in e for e in s["evidence"])


def test_intimacy_pass_rewarded_for_intimate_truth():
    intimate = score_variant(var("intimacy_pass", "vocal_belief"), ctx(intimate=1.0, static_dynamic_gap=1.0))
    neutral = score_variant(var("intimacy_pass", "vocal_belief"), ctx(intimate=0.0, static_dynamic_gap=0.0))
    assert intimate["overall_score"] > neutral["overall_score"]


# --- integration over the fixture ------------------------------------------ #
def test_subtractive_not_identical_across_branches(analyzed):
    r = analyzed["dense_chorus_with_loops"]
    scores = [v["scores"]["overall_score"]
              for b in r.creative["branches"] for v in b["variants"] if v["kind"] == "subtractive_drop"]
    assert len(scores) >= 2
    assert len(set(scores)) > 1, "same move kind must not score identically across unrelated branches"


def test_creative_report_shows_evidence(analyzed):
    md = render_creative(analyzed["dense_chorus_with_loops"].creative)
    assert "Why (top signal)" in md
    assert "Scoring evidence for this song" in md


def test_winner_reason_cites_evidence(analyzed):
    for b in analyzed["dense_chorus_with_loops"].creative["branches"]:
        assert "driven by" in b["winning"]["reason"] or "best fit for this song" in b["winning"]["reason"]


def test_context_present_in_creative_output(analyzed):
    ctx_out = analyzed["dense_chorus_with_loops"].creative["context"]
    for k in ("contrast_deficit", "overcrowding", "masking_pressure", "vocal_risk", "loop_pressure", "width_room"):
        assert 0.0 <= ctx_out[k] <= 1.0
