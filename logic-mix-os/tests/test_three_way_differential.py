"""P-041 Commit-2 — THE THREE-WAY DIFFERENTIAL PROOF: Halee/Ramone vs
Timbaland vs Quincy Jones, same stems — the proof the framework is not a
two-pole switch.

Same four fixtures (the three originals + ``vocal_chop_groove``, the live
blend fixture), three producers, one shared measurement substrate. The six
user requirements, each pinned permanently:

1. **Quincy differs from Halee/Ramone** — a different overall on every
   fixture, through the REAL pipeline, resolved dynamically by name.
2. **Quincy differs from Timbaland** — same, against the second pole.
3. **Quincy is coherent, not averaged mush** — his own poles sit ABOVE both
   profiles (depth hierarchy / section contrast / dynamic movement / vocal
   role fit — plus the iconic polarity BELOW both and the blend floor above
   both), his top-axis emphasis is one neither profile has, and his plan
   surface speaks his own authored voice (his own search-mode names on both
   the intimate and default paths, his own curated variant values, his own
   evidence lines).
4. **Safety invariant** — the same veto/audit surface: the 5 hardcoded
   SAFETY kill-switches lead his composed list verbatim in order; veto
   thresholds identical across all three profiles; no class-5 anywhere in
   his plans; every variant non-destructive; his artifacts schema-valid.
5. **Confidence labels honest** — the verbatim map pin
   (test_quincy_profile.Q_AUTHORED_MAP) is the guard; here: every ``high``
   entry names its documented-technique basis, the rendered artifacts carry
   HIS map, and no profile's distinct voice leaks into another's artifacts.
6. **Existing profiles do not drift** — the halee_ramone / timbaland pins
   (73.8/70.7/74.3/76.3 and 68.4/52.6/49.7/60.9, the authored loop polarity
   15/10, the blend split 65/85) all hold byte-stable with the third profile
   live; regression stays 93/93.

Plus FULL ATTRIBUTABILITY (the P-032i anti-drift idiom, now three-way): the
doctrine surface is audited key by key against BOTH existing producers —
Quincy diverges on EXACTLY the explained set (his own weighted mean, his own
authored map, his own identity, the authored loop polarity, the authored
blend acceptance) and NOTHING else; his overall reconstructs from the
reference's measurements plus his authored values alone.
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os import governance
from logic_mix_os.constants import RISK_CLASSES
from logic_mix_os.creative import _apply_promotions, _foregrounded_loop, run_creative_engine
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest
from logic_mix_os.validation.output_validator import (
    load_schema,
    validate_instance,
    validate_output,
)

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE
from test_differential_proof import SAFETY_KILL_SWITCHES, TIMBALAND_ONLY_STRINGS
from test_protect_iconic_loops import (
    PROMOTION_REASON,
    _loop_branch,
    _loop_status,
    _variant_by_id,
    _with_iconic_loop,
    _with_masked_lead,
)
from test_quincy_profile import (
    DOCUMENTED_STAMP,
    Q_AUTHORED_MAP,
    Q_PROMOTION_REASON,
    Q_WEIGHTS,
    QUINCY_ONLY_STRINGS,
)
from test_timbaland_profile import REFERENCE_ONLY_STRINGS, TIM_PROMOTION_REASON

PRODUCERS = ("halee_ramone", "timbaland", "quincy_jones")
ALL_FIXTURES = tuple(FIXTURE_NAMES) + (VOCAL_CHOP_FIXTURE,)
LOOP_FIXTURES = ("dense_chorus_with_loops", "splice_loop_problem")

COMPONENT_KEYS = [
    "physical_space_score", "emotional_hierarchy_score", "vocal_centrality_score",
    "depth_hierarchy_score", "section_contrast_score", "static_mix_score",
    "dynamic_mix_score", "beat_identity_score", "negative_space_score",
    "groove_coherence_score", "rhythmic_surprise_score",
    "low_end_motion_score", "loop_context_score", "vocal_role_fit_score",
    # P-057 — the 15th axis (bed-similarity dispersion) now WEIGHTED for Quincy
    # (0.6), so his overall reconstruction must include it (Halee/Timbaland keep
    # it at weight 0, so their overalls are unmoved).
    "textural_coherence_score",
]

# Same stems, THREE judgments — every overall pinned to the decimal (the
# halee_ramone / timbaland columns are the standing P-032h/P-035 pins,
# re-asserted with the third profile live = requirement 6; the quincy_jones
# column was measured by running the engine, then pinned = the packet's
# deterministic discipline). P-057 MOVED the quincy_jones column (70.0 -> 69.2 /
# 62.1 -> 60.4 / 61.9 -> 61.6 / 68.8 -> 68.2): he opts into the 15th axis,
# textural_coherence_score, at a support-tier 0.6, which reads 55/27/55/55 and
# pulls his weighted mean down (halee/timbaland keep the axis at weight 0, so
# their columns are byte-identical).
THREE_WAY_OVERALLS = {
    "simple_vocal_piano_song": {
        "halee_ramone": 73.8, "timbaland": 68.4, "quincy_jones": 69.2,
    },
    "dense_chorus_with_loops": {
        "halee_ramone": 71.8, "timbaland": 54.2, "quincy_jones": 61.6,
    },
    "splice_loop_problem": {
        "halee_ramone": 74.3, "timbaland": 49.7, "quincy_jones": 61.6,
    },
    "vocal_chop_groove": {
        "halee_ramone": 76.3, "timbaland": 60.9, "quincy_jones": 68.2,
    },
}

# Quincy's FULL 14-component picture, pinned per fixture (measured, then
# pinned). Every component equals the shared substrate except the two
# AUTHORED divergence channels: the loop-context polarity (static -> his
# authored 12.0 wherever the reference reads 15.0) and the blend gate on the
# 4th fixture (85.0 accepted vs the reference's 65.0 protected, at his
# authored 0.8 floor over the 0.95-confidence classifications).
QUINCY_COMPONENTS = {
    "simple_vocal_piano_song": {
        "physical_space_score": 58.0,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 40.0,
        "section_contrast_score": 100.0,
        "static_mix_score": 80.0,
        "dynamic_mix_score": 52.7,
        "beat_identity_score": 89.1,
        "negative_space_score": 62.3,
        "groove_coherence_score": 45.0,
        "rhythmic_surprise_score": 51.1,
        "low_end_motion_score": 60.0,
        "loop_context_score": 50.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback (P-057)
    },
    "dense_chorus_with_loops": {
        "physical_space_score": 67.6,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 65.3,
        "section_contrast_score": 82,
        "static_mix_score": 72.0,
        "dynamic_mix_score": 23.4,
        "beat_identity_score": 52.7,
        "negative_space_score": 15.0,
        "groove_coherence_score": 99.1,
        "rhythmic_surprise_score": 20.0,
        "low_end_motion_score": 35.1,
        "loop_context_score": 12.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 27.0,  # 2 beds — incoherent (P-057)
    },
    "splice_loop_problem": {
        "physical_space_score": 81.3,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82,
        "static_mix_score": 70.0,
        "dynamic_mix_score": 23.1,
        "beat_identity_score": 46.0,
        "negative_space_score": 20.0,
        "groove_coherence_score": 45.0,
        "rhythmic_surprise_score": 27.8,
        "low_end_motion_score": 25.0,
        "loop_context_score": 12.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback (P-057)
    },
    "vocal_chop_groove": {
        "physical_space_score": 81.3,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82,
        "static_mix_score": 80.0,
        "dynamic_mix_score": 28.2,
        "beat_identity_score": 63.6,
        "negative_space_score": 19.4,
        "groove_coherence_score": 99.4,
        "rhythmic_surprise_score": 35.6,
        "low_end_motion_score": 60.0,
        "loop_context_score": 12.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback (P-057)
    },
}

# THE ANTI-DRIFT SETS: exactly these doctrine_score keys may diverge between
# quincy_jones and each existing producer, per fixture — every divergence
# explained (his own weighted mean / his own authored map / the P-039
# identity surface / the authored loop polarity / the authored blend gate,
# whose evidence divergence is isolated to the vocal_role_fit axis). A future
# change that widens any set lands here as a conscious decision, never drift.
DIVERGENT_VS_REFERENCE = {
    "simple_vocal_piano_song": {
        "overall_mix_readiness_score", "confidence", "producer",
    },
    "dense_chorus_with_loops": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "splice_loop_problem": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "vocal_chop_groove": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score", "vocal_role_fit_score", "evidence",
    },
}
# Against timbaland the blend readings AGREE (both accept: 85.0, identical
# evidence lines — quincy's stricter 0.8 floor is still cleared by the 0.95
# classifications), so the chop fixture diverges only on the loop polarity
# (12.0 vs 10.0) plus the standing three.
DIVERGENT_VS_TIMBALAND = {
    "simple_vocal_piano_song": {
        "overall_mix_readiness_score", "confidence", "producer",
    },
    "dense_chorus_with_loops": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "splice_loop_problem": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "vocal_chop_groove": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
}

QUINCY_IDENTITY = {
    "name": "quincy_jones",
    "display_name": "Quincy Jones",
    "provenance": "hand-curated-documented",
    "confidence": "high",
}

# Quincy's plan surface, pinned (measured, then pinned): his own authored
# search modes on both resolution paths, and his branch winners.
QUINCY_SEARCH_MODES = {
    "simple_vocal_piano_song": "space_for_the_singer",   # his intimate_mode
    "dense_chorus_with_loops": "arrangement_lift",       # his default_mode
    "splice_loop_problem": "arrangement_lift",
    "vocal_chop_groove": "arrangement_lift",
}
QUINCY_WINNERS = {
    "simple_vocal_piano_song": {"vocal_belief": "vocal_A"},
    "dense_chorus_with_loops": {
        "chorus_lift": "chorus_lift_B", "density": "density_B",
        "loop": "loop_B", "depth": "depth_A", "vocal_belief": "vocal_A",
    },
    "splice_loop_problem": {
        "chorus_lift": "chorus_lift_B", "loop": "loop_B",
        "vocal_belief": "vocal_A",
    },
    "vocal_chop_groove": {
        "chorus_lift": "chorus_lift_B", "loop": "loop_B",
        "depth": "depth_A", "vocal_belief": "vocal_A",
    },
}

# The three-way variant-value spread on the shared loop branch (each
# producer's own curated table, same variants): loop_B and loop_A per
# producer — pairwise distinct where the tables author distinct values.
LOOP_B_BY_PRODUCER = {"halee_ramone": 85.3, "timbaland": 86.7, "quincy_jones": 85.6}
LOOP_A_BY_PRODUCER = {"halee_ramone": 81.9, "timbaland": 80.7, "quincy_jones": 81.9}

# Quincy's own width-crowding nudge line (his authored evidence voice).
Q_WIDTH_NUDGE = (
    "vocal_belief -6: stereo image is already width-crowded — widening now "
    "trades ensemble separation for size"
)


# --------------------------------------------------------------------------- #
# Shared expensive fixtures: quincy on all 4 fixtures; timbaland on the three
# originals (the chop runs come from the session ``chop_groove_analyzed``).
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def q_analyzed():
    """The full pipeline once per fixture with ``producer="quincy_jones"`` —
    resolved DYNAMICALLY by name (the no-code-changes acceptance clause)."""
    results = {}
    for name in ALL_FIXTURES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="quincy_jones"
        )
    return results


@pytest.fixture(scope="module")
def tim_analyzed(chop_groove_analyzed):
    """Timbaland on all 4 fixtures (3 fresh + the session chop run)."""
    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="timbaland"
        )
    results[VOCAL_CHOP_FIXTURE] = chop_groove_analyzed["timbaland"]
    return results


@pytest.fixture(scope="module")
def ref_analyzed(analyzed, chop_groove_analyzed):
    """The reference on all 4 fixtures (session-scoped runs, re-keyed)."""
    results = dict(analyzed)
    results[VOCAL_CHOP_FIXTURE] = chop_groove_analyzed["halee_ramone"]
    return results


def _weighted_overall(producer: str, components: dict) -> float:
    weights = load_profile(producer).doctrine["weights"]
    present = {k: components[k] for k in weights if components.get(k) is not None}
    return doctrine_engine._clamp(
        sum(present[k] * weights[k] for k in present)
        / sum(weights[k] for k in present)
    )


def _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed):
    return {
        "halee_ramone": ref_analyzed[name],
        "timbaland": tim_analyzed[name],
        "quincy_jones": q_analyzed[name],
    }


# =========================================================================== #
# Requirements 1 + 2 — Quincy differs from BOTH, on every fixture, pinned.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_three_way_overalls_pinned_and_pairwise_distinct(
    name, ref_analyzed, tim_analyzed, q_analyzed
):
    """Same stems, three judgments: every producer's overall lands its pinned
    value, and the three values are PAIRWISE distinct — three value systems,
    not a two-pole switch and not a rebadged pole."""
    results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed)
    seen = {}
    for producer, res in results.items():
        overall = res.doctrine_score["overall_mix_readiness_score"]
        assert overall == THREE_WAY_OVERALLS[name][producer], (name, producer)
        seen[producer] = overall
    assert len(set(seen.values())) == 3, (name, seen)


def test_dynamically_discovered_identity_reaches_every_artifact(q_analyzed):
    """The acceptance clause pair 'dynamically discovered / no code changes':
    ``analyze(producer="quincy_jones")`` resolved the profile BY NAME from the
    producers directory (the fixture above), and every analysis carries
    Quincy's identity surface — the four metadata fields, never risk_class."""
    for name, res in q_analyzed.items():
        producer = res.doctrine_score["producer"]
        assert producer == QUINCY_IDENTITY, name
        assert "risk_class" not in producer, name


# =========================================================================== #
# Requirement 3 — coherent, not averaged mush: his own poles + his own voice.
# =========================================================================== #
def test_not_averaged_mush_his_own_poles_and_orderings():
    """At least 2 axes/behaviors where Quincy is NOT strictly between the
    other two — four weight poles ABOVE both (depth hierarchy, section
    contrast, dynamic movement, vocal role fit), the iconic loop polarity
    BELOW both, and the blend confidence floor ABOVE both — plus a top-axis
    emphasis (depth hierarchy first, section contrast second) neither
    existing profile has."""
    q = load_profile("quincy_jones")
    ref = load_profile("halee_ramone")
    tim = load_profile("timbaland")
    qw, rw, tw = q.doctrine["weights"], ref.doctrine["weights"], tim.doctrine["weights"]
    above_both = [k for k in qw if qw[k] > rw[k] and qw[k] > tw[k]]
    assert {"depth_hierarchy_score", "section_contrast_score",
            "dynamic_mix_score", "vocal_role_fit_score"} <= set(above_both)
    assert len(above_both) >= 2  # the requirement floor, comfortably cleared

    q_lc = q.doctrine["scorers"]["loop_context"]
    assert q_lc["iconic"] < ref.doctrine["scorers"]["loop_context"]["iconic"]
    assert q_lc["iconic"] < tim.doctrine["scorers"]["loop_context"]["iconic"]

    assert q.vocal_blend_policy["confidence_floor"] > \
        tim.vocal_blend_policy["confidence_floor"]
    assert q.vocal_blend_policy["confidence_floor"] > \
        ref.vocal_blend_policy["confidence_floor"]

    def top2(w):
        return tuple(sorted(w, key=w.get, reverse=True)[:2])

    assert top2(qw) == ("depth_hierarchy_score", "section_contrast_score")
    assert top2(qw) != top2(rw) and top2(qw) != top2(tw)
    assert max(rw, key=rw.get) != "depth_hierarchy_score"
    assert max(tw, key=tw.get) != "depth_hierarchy_score"


def test_plan_surface_speaks_his_own_authored_voice(
    ref_analyzed, tim_analyzed, q_analyzed
):
    """The behavioral half of coherence: Quincy's plans resolve HIS OWN
    authored search modes on both paths (the intimate fixture reaches his
    ``space_for_the_singer``; every other fixture his ``arrangement_lift`` —
    mode names neither profile carries), his branch winners land his curated
    values, and no fallback fires anywhere."""
    for name in ALL_FIXTURES:
        cr = q_analyzed[name].creative
        assert cr["search_mode"] == QUINCY_SEARCH_MODES[name], name
        assert "search_mode_fallback" not in cr, name
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in cr["branches"]}
        assert winners == QUINCY_WINNERS[name], name
    for other in ("halee_ramone", "timbaland"):
        modes = load_profile(other).search_modes
        assert "space_for_the_singer" not in modes
        assert "arrangement_lift" not in modes
    # the other producers resolve their own (different) modes on the same stems
    assert ref_analyzed["simple_vocal_piano_song"].creative["search_mode"] == "vocal_truth"
    assert tim_analyzed["simple_vocal_piano_song"].creative["search_mode"] == "conservative"


def test_three_way_variant_values_from_three_curated_tables(
    ref_analyzed, tim_analyzed, q_analyzed
):
    """On the shared loop branch each producer's own curated table scores the
    SAME variants to ITS OWN values (loop_B 85.3 / 86.7 / 85.6 — pairwise
    distinct), and on the dense chorus_lift branch the width-crowding nudge
    fires each profile's OWN authored evidence line at its own value
    (74.9 / 69.7 / 71.3 — pairwise distinct)."""
    for name in LOOP_FIXTURES:
        results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed)
        for producer, res in results.items():
            branch = _loop_branch(res.creative)
            b = _variant_by_id(branch, "loop_B")["scores"]["overall_score"]
            a = _variant_by_id(branch, "loop_A")["scores"]["overall_score"]
            assert b == pytest.approx(LOOP_B_BY_PRODUCER[producer], abs=1e-9), (name, producer)
            assert a == pytest.approx(LOOP_A_BY_PRODUCER[producer], abs=1e-9), (name, producer)
        assert len(set(LOOP_B_BY_PRODUCER.values())) == 3

    dense = "dense_chorus_with_loops"
    results = _by_producer(dense, ref_analyzed, tim_analyzed, q_analyzed)
    values = {}
    for producer, res in results.items():
        cl = next(b for b in res.creative["branches"] if b["problem_id"] == "chorus_lift")
        scores = _variant_by_id(cl, "chorus_lift_A")["scores"]
        values[producer] = scores["overall_score"]
        assert scores["score_nudges"], producer  # each profile's nudge FIRED
    assert values == {"halee_ramone": pytest.approx(74.9, abs=1e-9),
                      "timbaland": pytest.approx(69.7, abs=1e-9),
                      "quincy_jones": pytest.approx(71.3, abs=1e-9)}
    q_cl = next(b for b in q_analyzed[dense].creative["branches"]
                if b["problem_id"] == "chorus_lift")
    assert _variant_by_id(q_cl, "chorus_lift_A")["scores"]["score_nudges"] == [Q_WIDTH_NUDGE]


def test_iconic_loop_three_value_systems_one_detection_basis(ref_analyzed):
    """The gate, three-way, on the SAME iconic-reading evidence: all three
    profiles read 'iconic' from identical detection floors; halee_ramone and
    quincy_jones (protect=false, each authored) fire their OWN promotion
    reasons and ship the deconstruct plan (loop_A 85.9 under both tables —
    quincy's from HIS curated base, with HIS loop_B at 85.6 close behind);
    timbaland (protect=true) withholds and ships its accent plan (loop_B
    86.7, loop_A unpromoted 80.7). Three plans, three voices, one basis."""
    res = _with_iconic_loop(ref_analyzed)
    profiles = {p: load_profile(p) for p in PRODUCERS}
    assert _foregrounded_loop(res) is True
    for p in PRODUCERS:
        assert _loop_status(res, profiles[p]) == "iconic", p

    assert [f[2] for f in _apply_promotions("loop_deconstruct", res, profiles["halee_ramone"])] \
        == [PROMOTION_REASON]
    assert [f[2] for f in _apply_promotions("loop_deconstruct", res, profiles["quincy_jones"])] \
        == [Q_PROMOTION_REASON]
    assert _apply_promotions("loop_deconstruct", res, profiles["timbaland"]) == []

    branches = {
        p: _loop_branch(run_creative_engine(res, res.creative["search_mode"],
                                            profile=profiles[p]))
        for p in PRODUCERS
    }
    assert branches["halee_ramone"]["winning"]["winning_variant"] == "loop_A"
    assert branches["quincy_jones"]["winning"]["winning_variant"] == "loop_A"
    assert branches["timbaland"]["winning"]["winning_variant"] == "loop_B"

    q_a = _variant_by_id(branches["quincy_jones"], "loop_A")["scores"]
    assert q_a["overall_score"] == pytest.approx(85.9, abs=1e-9)
    assert q_a["score_nudges"] == [Q_PROMOTION_REASON]
    assert _variant_by_id(branches["quincy_jones"], "loop_B")["scores"]["overall_score"] \
        == pytest.approx(85.6, abs=1e-9)
    tim_a = _variant_by_id(branches["timbaland"], "loop_A")["scores"]
    assert tim_a["overall_score"] == pytest.approx(80.7, abs=1e-9)
    assert "score_nudges" not in tim_a


def test_masked_lead_override_holds_for_all_three(ref_analyzed):
    """THE RAMONE GATE is producer-agnostic: with the lead bad-masked on an
    iconic read, the deconstruct pressure fires under ALL THREE profiles —
    each in its own authored voice; no value system can shadow a buried
    lead."""
    res = _with_masked_lead(_with_iconic_loop(ref_analyzed))
    expected = {
        "halee_ramone": PROMOTION_REASON,
        "timbaland": TIM_PROMOTION_REASON,
        "quincy_jones": Q_PROMOTION_REASON,
    }
    for producer, reason in expected.items():
        fired = _apply_promotions("loop_deconstruct", res, load_profile(producer))
        assert [f[2] for f in fired] == [reason], producer


# =========================================================================== #
# FULL ATTRIBUTABILITY — the three-way anti-drift audit.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_quincy_component_picture_pinned(name, q_analyzed):
    ds = q_analyzed[name].doctrine_score
    assert {k: ds[k] for k in COMPONENT_KEYS} == QUINCY_COMPONENTS[name]


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_the_reference(name, ref_analyzed, q_analyzed):
    """Key-by-key doctrine audit against halee_ramone: Quincy diverges on
    EXACTLY the explained set — nothing else moved (shared substrate; the
    chop fixture's evidence divergence stays isolated to the vocal_role_fit
    axis, itself the authored blend gate)."""
    ref_ds = ref_analyzed[name].doctrine_score
    q_ds = q_analyzed[name].doctrine_score
    assert set(ref_ds) == set(q_ds)
    diverged = {k for k in ref_ds if ref_ds[k] != q_ds[k]}
    assert diverged == DIVERGENT_VS_REFERENCE[name], (name, diverged)
    if "evidence" in diverged:
        ev_diverged = {k for k in ref_ds["evidence"]
                       if ref_ds["evidence"][k] != q_ds["evidence"][k]}
        assert ev_diverged == {"vocal_role_fit"}, (name, ev_diverged)
    assert ref_ds["warnings"] == q_ds["warnings"], name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_timbaland(name, tim_analyzed, q_analyzed):
    """The same audit against the second pole: on the chop fixture the two
    opt-in policies AGREE on the blend reading (identical vocal_role_fit
    score and evidence — quincy's stricter 0.8 floor is still cleared at
    0.95), so the only component divergence anywhere is the authored loop
    polarity (12.0 vs 10.0)."""
    tim_ds = tim_analyzed[name].doctrine_score
    q_ds = q_analyzed[name].doctrine_score
    assert set(tim_ds) == set(q_ds)
    diverged = {k for k in tim_ds if tim_ds[k] != q_ds[k]}
    assert diverged == DIVERGENT_VS_TIMBALAND[name], (name, diverged)
    assert tim_ds["evidence"] == q_ds["evidence"], name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_quincy_overall_is_his_own_weighted_mean(name, q_analyzed):
    ds = q_analyzed[name].doctrine_score
    assert _weighted_overall("quincy_jones", {k: ds[k] for k in COMPONENT_KEYS}) \
        == THREE_WAY_OVERALLS[name]["quincy_jones"]
    # and the live weights ARE the pinned authored table
    assert load_profile("quincy_jones").doctrine["weights"] == Q_WEIGHTS


def test_quincy_reconstructs_from_the_references_measurements(ref_analyzed):
    """The strongest attributability form, three-way edition: rebuild
    Quincy's overall on every fixture from the REFERENCE's component scores
    plus Quincy's AUTHORED values alone — substitute the authored static
    polarity (15.0 -> 12.0) and the authored blend acceptance (65.0 -> 85.0
    on the chop fixture), apply his weights, land on his pinned overall to
    the decimal. Every delta traces to an authored value."""
    q_static = load_profile("quincy_jones").doctrine["scorers"]["loop_context"]["static"]
    assert q_static == 12.0
    for name in ALL_FIXTURES:
        ref_ds = ref_analyzed[name].doctrine_score
        rebuilt = {k: ref_ds[k] for k in COMPONENT_KEYS}
        if ref_ds["loop_context_score"] == 15.0:      # the reference's static read
            rebuilt["loop_context_score"] = q_static
        if name == VOCAL_CHOP_FIXTURE:
            assert ref_ds["vocal_role_fit_score"] == 65.0
            rebuilt["vocal_role_fit_score"] = 85.0    # the authored blend gate
        assert _weighted_overall("quincy_jones", rebuilt) \
            == THREE_WAY_OVERALLS[name]["quincy_jones"], name


def test_blend_gate_counterfactual_is_worth_a_traceable_delta(q_analyzed):
    """The chop fixture's blend gate is WORTH a traceable overall delta under
    Quincy's 0.7 weight: with the reference's protected 65.0 substituted into
    his own components the overall reads 67.0 (vs the live 68.2 — +1.2 from
    the authored opt-in; both values moved -0.6 from P-057's textural opt-in,
    the delta itself unchanged); and the static-polarity term genuinely presses
    the overall DOWN (removing loop_context from his mean raises it)."""
    ds = q_analyzed[VOCAL_CHOP_FIXTURE].doctrine_score
    protected = {k: ds[k] for k in COMPONENT_KEYS}
    protected["vocal_role_fit_score"] = 65.0
    assert _weighted_overall("quincy_jones", protected) == 67.0

    without_lc = {k: ds[k] for k in COMPONENT_KEYS if k != "loop_context_score"}
    assert _weighted_overall("quincy_jones", without_lc) \
        > ds["overall_mix_readiness_score"]


# =========================================================================== #
# Requirement 4 — SAFETY INVARIANT: the same veto/audit surface.
# =========================================================================== #
def test_kill_switches_lead_with_the_five_safety_switches(q_analyzed):
    """On every fixture the composed kill-switch list under Quincy leads with
    the 5 hardcoded SAFETY switches FIRST, VERBATIM, IN ORDER (pinned in
    test_differential_proof, not read from governance) — followed by exactly
    his authored aesthetic list."""
    assert governance._SAFETY_KILL_SWITCHES == SAFETY_KILL_SWITCHES
    aesthetic = load_profile("quincy_jones").aesthetic_kill_switches
    for name, res in q_analyzed.items():
        ks = res.governance["kill_switches"]
        assert ks[:5] == SAFETY_KILL_SWITCHES, name
        assert ks == SAFETY_KILL_SWITCHES + aesthetic, name


def test_veto_thresholds_identical_across_all_three_profiles():
    """The veto surface is UNCHANGED, not merely not-weaker: all three
    profiles author identical reject/veto/fallback lines."""
    q = load_profile("quincy_jones").veto_thresholds
    assert q == load_profile("halee_ramone").veto_thresholds
    assert q == load_profile("timbaland").veto_thresholds


def test_no_destructive_recommendation_under_quincy(q_analyzed):
    """Class 5 appears NOWHERE in Quincy's plans; every action passes the
    kill-switch validator; every creative variant is reversible; the class-5
    block itself stays engine-fixed."""
    for name, res in q_analyzed.items():
        for track in res.mix_plan["per_track_actions"]:
            assert track["risk_class"] < 5 and track["risk_class"] in RISK_CLASSES
            for action in track["actions"]:
                assert action["risk_class"] < 5, (name, track["track"])
                assert governance.validate_action_safety(action)["blocked"] is False
            for auto in track["automation"]:
                assert auto["risk_class"] < 5, name
        for m in res.mix_plan["mute_candidates"]:
            assert m["risk_class"] < 5, name
        for branch in res.creative["branches"]:
            for v in branch["variants"]:
                assert v["reversibility"] == "non_destructive_duplicate_track"
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


def test_quincy_plans_and_artifacts_validate(q_analyzed, tmp_path):
    """Machine-checkable coherence: Quincy's mix_plan validates against the
    schema on every fixture, and his rendered artifact tree passes the full
    output validation."""
    schema = load_schema("mix_plan.schema.json")
    for name, res in q_analyzed.items():
        assert validate_instance(res.mix_plan, schema) == [], name
    out = tmp_path / "quincy"
    write_artifacts(q_analyzed[VOCAL_CHOP_FIXTURE], out)
    report = validate_output(out)
    assert report["ok"], report["errors"]


# =========================================================================== #
# Requirement 5 — CONFIDENCE HONESTY at the differential level.
# =========================================================================== #
def test_artifacts_carry_quincys_own_map_fresh(q_analyzed):
    q = load_profile("quincy_jones")
    for name, res in q_analyzed.items():
        conf = res.doctrine_score["confidence"]
        assert conf == Q_AUTHORED_MAP, name          # the verbatim guard, live
        assert conf is not q.confidence_map, name    # fresh, never an alias
    assert Q_AUTHORED_MAP != load_profile("halee_ramone").confidence_map
    assert Q_AUTHORED_MAP != load_profile("timbaland").confidence_map


def test_no_high_entry_lacks_a_documented_technique_reason(q_analyzed):
    """The user's grounding standard, re-asserted on the LIVE artifact
    surface: every ``high`` entry the pipeline ships names its
    documented-technique basis; everything else is limited/deferred."""
    for name, res in q_analyzed.items():
        for entry in res.doctrine_score["confidence"]:
            if entry["level"] == "high":
                assert DOCUMENTED_STAMP in entry["reason"], (name, entry["area"])
            assert entry["level"] in ("high", "limited", "deferred")


def test_rendered_verdicts_speak_each_producers_voice_no_leaks(
    ref_analyzed, tim_analyzed, q_analyzed, tmp_path
):
    """Render one fixture under all three producers: each verdict carries its
    OWN map (every area and reason) and its own distinct voice — and neither
    of the other producers' distinct voices leaks in (the shared deferred
    engine boundaries legitimately render under all three)."""
    name = "simple_vocal_piano_song"
    voices = {
        "halee_ramone": REFERENCE_ONLY_STRINGS,
        "timbaland": TIMBALAND_ONLY_STRINGS,
        "quincy_jones": QUINCY_ONLY_STRINGS,
    }
    results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed)
    verdicts = {}
    for producer, res in results.items():
        d = tmp_path / producer
        write_artifacts(res, d)
        verdicts[producer] = (d / "mix_verdict.md").read_text(encoding="utf-8")
        dsj = json.loads((d / "doctrine_score.json").read_text(encoding="utf-8"))
        assert dsj["confidence"] == load_profile(producer).confidence_map, producer

    for producer, md in verdicts.items():
        assert "## Confidence" in md
        for entry in load_profile(producer).confidence_map:
            assert entry["area"] in md, (producer, entry["area"])
            assert entry["reason"] in md, (producer, entry["area"])
        for own in voices[producer]:
            assert own in md, (producer, own)
        for other, other_strings in voices.items():
            if other == producer:
                continue
            for s in other_strings:
                assert s not in md, f"{other} voice leaked into {producer}: {s}"


# =========================================================================== #
# Requirement 6 — EXISTING PROFILES DO NOT DRIFT (with the third profile live).
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_existing_producers_unmoved_at_their_pinned_values(
    name, ref_analyzed, tim_analyzed
):
    """The standing two-producer pins hold byte-stable with quincy_jones in
    the directory: both overalls, the authored loop polarities (15/10 on the
    static-loop fixtures) and the blend split (65/85 on the chop fixture)."""
    ref_ds = ref_analyzed[name].doctrine_score
    tim_ds = tim_analyzed[name].doctrine_score
    assert ref_ds["overall_mix_readiness_score"] == THREE_WAY_OVERALLS[name]["halee_ramone"]
    assert tim_ds["overall_mix_readiness_score"] == THREE_WAY_OVERALLS[name]["timbaland"]
    if name in LOOP_FIXTURES or name == VOCAL_CHOP_FIXTURE:
        assert ref_ds["loop_context_score"] == 15.0
        assert tim_ds["loop_context_score"] == 10.0
    if name == VOCAL_CHOP_FIXTURE:
        assert ref_ds["vocal_role_fit_score"] == 65.0
        assert tim_ds["vocal_role_fit_score"] == 85.0


def test_regression_corpus_still_green_with_three_profiles():
    """The golden corpus (the DEFAULT producer) stays 93/93 — the third
    profile is purely additive to the runtime surface."""
    from logic_mix_os.regression import run_regression_suite

    report = run_regression_suite(ROOT / "fixtures")
    assert report["tests_run"] == 93
    assert report["passed"] == 93
    assert report["failed"] == 0
    assert report["critical_failures"] == []
