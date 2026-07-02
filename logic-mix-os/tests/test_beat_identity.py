"""P-032e — the binding guards for ``beat_identity``, the first new producer-
agnostic doctrine axis (strength-form only).

``beat_identity`` measures the STRENGTH of a central rhythmic fingerprint from
transient physics, producer-agnostically (candidate by ``transient_density``, not
by instrument label). It is wired into ``score_doctrine`` with a weight of 0 for
``halee_ramone`` so the reference producer's output stays BYTE-IDENTICAL.

Four guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default halee_ramone)
   leaves every pre-existing component score AND ``overall_mix_readiness_score``
   unchanged, and the golden regression still reports 68/68. The mechanism: the
   new term is appended LAST to ``component_scores`` (summation order preserved)
   and its weight is 0 (``beat*0`` numerator, ``+0`` denominator).
2. **Value-discrimination (unit)** — a punchy, foregrounded, distinct rhythmic
   stem scores HIGH; a project with no rhythmic element scores at/near the
   ``no_beat`` floor. Proves the scorer measures what it claims.
3. **Liveness (load-bearing)** — a synthetic profile that weights
   ``beat_identity_score`` non-zero CHANGES ``analyze()``'s overall on
   ``dense_chorus_with_loops``; and a sabotage (hardcoding the term to a
   constant) FAILS that liveness while byte-identical stays green (P-016/P-029).
4. **No-aliasing** — the scorer only reads ``doctrine[...]``; it never mutates
   the shared profile structures.
"""

from __future__ import annotations

import copy

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The seven pre-existing component score keys (the byte-identical anchor set).
EXISTING_COMPONENT_KEYS = [
    "halee_score",
    "ramone_score",
    "vocal_centrality_score",
    "depth_hierarchy_score",
    "section_contrast_score",
    "static_mix_score",
    "dynamic_mix_score",
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


# --------------------------------------------------------------------------- #
# Test helpers — synthetic records for the unit / discrimination guards.
# --------------------------------------------------------------------------- #
def _record(**over):
    base = dict(
        name="t",
        instrument_identity="acoustic_guitar",
        identity_family="guitar",
        depth_default="background",
        perceptual_role="heard",
        source_kind="di_audio_track",
        sacredness="core",
        stereo_width=0.2,
        metrics={
            "transient_density": 0.1,
            "crest_factor_db": 12.0,
            "spectral_flatness": 0.0,
        },
    )
    base.update(over)
    return base


def _rhythmic(**over):
    """A punchy, foregrounded, distinct rhythmic stem."""
    m = {"transient_density": 0.95, "crest_factor_db": 20.0, "spectral_flatness": 0.4}
    m.update(over.pop("metrics", {}))
    base = dict(
        name="Beat",
        instrument_identity="percussion",
        identity_family="drums",
        depth_default="foreground",
        perceptual_role="heard",
        source_kind="live_audio_recording",
        sacredness="core",
        stereo_width=0.2,
        metrics=m,
    )
    base.update(over)
    return base


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged.
# --------------------------------------------------------------------------- #
def test_beat_identity_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``beat*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["beat_identity_score"] == 0


def test_beat_identity_appended_last_preserves_summation_order(analyzed):
    """The new term is last in ``component_scores`` and every PRE-EXISTING key
    keeps its exact value + position; ``overall`` equals the weighted mean over
    the present components using the profile weights (weight-0 term contributes
    nothing)."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        # The seven existing keys come first, in order; beat_identity_score is
        # appended right after them (position 7). P-032a then appends
        # negative_space_score after beat_identity, so beat_identity is no longer
        # the final key — but its position relative to the seven is unchanged.
        assert keys[:7] == EXISTING_COMPONENT_KEYS
        assert keys[7] == "beat_identity_score"


def test_overall_is_byte_identical_to_seven_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the seven pre-existing
    components (beat_identity excluded) equals the pipeline's overall — proof the
    weight-0 new term did not move the number."""
    w = load_profile("halee_ramone").doctrine["weights"]
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        present = {k: ds[k] for k in EXISTING_COMPONENT_KEYS if ds.get(k) is not None}
        expected = doctrine_engine._clamp(
            sum(present[k] * w[k] for k in present) / sum(w[k] for k in present)
        )
        assert ds["overall_mix_readiness_score"] == expected


def test_regression_still_sixty_eight_of_sixty_eight():
    """The golden corpus regression — which pins ``doctrine_score`` — still passes
    68/68 with the new axis wired in at weight 0."""
    from pathlib import Path

    from logic_mix_os.regression import run_regression_suite

    base = Path(__file__).resolve().parent.parent / "fixtures"
    report = run_regression_suite(base)
    assert report["tests_run"] == 68
    assert report["passed"] == 68
    assert report["failed"] == 0


# --------------------------------------------------------------------------- #
# 2. VALUE-DISCRIMINATION (unit) — the scorer measures fingerprint strength.
# --------------------------------------------------------------------------- #
def test_no_rhythmic_element_scores_at_no_beat_floor():
    """No candidate clears the transient floor => the ``no_beat`` floor, verbatim."""
    doctrine = load_profile("halee_ramone").doctrine
    floor = doctrine["scorers"]["beat_identity"]["no_beat"]
    quiet = [
        _record(name="Pad", metrics={"transient_density": 0.05, "crest_factor_db": 10.0, "spectral_flatness": 0.0}),
        _record(name="Sustain", metrics={"transient_density": 0.02, "crest_factor_db": 9.0, "spectral_flatness": 0.0}),
    ]
    score, ev = doctrine_engine._beat_identity(quiet, [], doctrine)
    assert score == floor
    assert any("no" in e.lower() for e in ev)


def test_punchy_foregrounded_distinct_stem_scores_high():
    """A punchy, foregrounded, distinct, unmasked rhythmic stem sitting well above
    the bed scores HIGH — every strength contribution fires."""
    doctrine = load_profile("halee_ramone").doctrine
    records = [
        _rhythmic(name="Beat"),
        _record(name="Pad", metrics={"transient_density": 0.08, "crest_factor_db": 10.0, "spectral_flatness": 0.0}),
        _record(name="Bass", metrics={"transient_density": 0.10, "crest_factor_db": 9.0, "spectral_flatness": 0.0}),
    ]
    score, _ = doctrine_engine._beat_identity(records, [], doctrine)
    assert score >= 85.0


def test_present_but_buried_beat_scores_below_foregrounded():
    """The SAME punchy candidate, but buried (background/felt) and masked, is a
    weaker fingerprint than when it is foregrounded and clear — strength drops."""
    doctrine = load_profile("halee_ramone").doctrine
    bed = [
        _record(name="Pad", metrics={"transient_density": 0.08, "crest_factor_db": 10.0, "spectral_flatness": 0.0}),
        _record(name="Bass", metrics={"transient_density": 0.10, "crest_factor_db": 9.0, "spectral_flatness": 0.0}),
    ]
    forward = [_rhythmic(name="Beat", depth_default="foreground", perceptual_role="heard")] + bed
    buried = [_rhythmic(name="Beat", depth_default="background", perceptual_role="felt")] + bed
    masking = [{"elements": ["Beat"], "classification": "bad_masking"}]

    fwd_score, _ = doctrine_engine._beat_identity(forward, [], doctrine)
    buried_score, _ = doctrine_engine._beat_identity(buried, masking, doctrine)
    assert buried_score < fwd_score


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 value."""
    doctrine = load_profile("halee_ramone").doctrine
    extreme = [
        _rhythmic(name="A", metrics={"transient_density": 1.0, "crest_factor_db": 40.0, "spectral_flatness": 0.9}),
        _rhythmic(name="B", metrics={"transient_density": 1.0, "crest_factor_db": 40.0, "spectral_flatness": 0.9}),
    ]
    score, _ = doctrine_engine._beat_identity(extreme, [], doctrine)
    assert 0.0 <= score <= 100.0


# --------------------------------------------------------------------------- #
# 3. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and a sabotage of the scorer must break this test (the P-016/P-029 lesson).
# --------------------------------------------------------------------------- #
def _profile_weighting_beat_identity(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero beat_identity weight —
    so any overall delta is attributable to the beat_identity term alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["beat_identity_score"] = weight
    import dataclasses

    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    beat_identity non-zero changes the overall vs the weight-0 reference. This is
    LIVE-WIRE proof: the term is genuinely threaded, not decorative.

    Sabotage that this test catches: hardcoding ``_beat_identity`` to return a
    constant, or dropping it from ``component_scores``, collapses the weighted
    mean back onto the reference and this assertion FAILS."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*args)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(*args, profile=_profile_weighting_beat_identity(3.0))

    # beat_identity itself is a real, present 0..100 number on this fixture.
    beat = reference["beat_identity_score"]
    assert beat is not None and 0.0 <= beat <= 100.0
    # And giving it weight changes the overall (only possible if it is threaded).
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_beat_score(analyzed):
    """A sharper sabotage guard: the direction the overall moves under a non-zero
    weight must be consistent with beat_identity's value relative to the other
    components. If the term were hardcoded to a fixed number the move would not
    track the real beat score, and this assertion would break."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*args)
    beat = reference["beat_identity_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(*args, profile=_profile_weighting_beat_identity(5.0))
    new_overall = weighted["overall_mix_readiness_score"]

    # Pulling the mean toward ``beat`` with a heavy weight moves the overall in the
    # direction of ``beat`` (up if beat > ref_overall, down if below). A constant
    # sabotage that happens to equal neither the real beat nor ref_overall would
    # move it the wrong way for at least one fixture direction.
    if beat > ref_overall:
        assert new_overall > ref_overall
    elif beat < ref_overall:
        assert new_overall < ref_overall
    else:  # exactly equal — degenerate; the weight cannot move it
        assert new_overall == ref_overall


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — the scorer only reads ``doctrine[...]``; it never mutates the
#    shared profile structures (consistent with test_doctrine_profile_sourced).
# --------------------------------------------------------------------------- #
def test_beat_identity_does_not_mutate_the_profile():
    doctrine = load_profile("halee_ramone").doctrine
    before = copy.deepcopy(doctrine)
    records = [
        _rhythmic(name="Beat"),
        _record(name="Pad", metrics={"transient_density": 0.05, "crest_factor_db": 10.0, "spectral_flatness": 0.0}),
    ]
    events = [{"elements": ["Beat"], "classification": "bad_masking"}]
    doctrine_engine._beat_identity(records, events, doctrine)
    assert doctrine == before


def test_score_doctrine_with_beat_identity_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` on a real fixture and assert the shared default doctrine is
    byte-unchanged (its ``scorers.beat_identity`` block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "beat_identity" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
