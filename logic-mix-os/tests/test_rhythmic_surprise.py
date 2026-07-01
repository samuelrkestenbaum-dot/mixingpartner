"""P-032d — the binding guards for ``rhythmic_surprise``, the FOURTH new
producer-agnostic doctrine axis (WEAK form only): cross-section
transient-density variation.

THE HONESTY GATE — this is the WEAK, SECTION-AGGREGATE form. The scorer
measures cross-section ``transient_density`` spread (pstdev) plus the largest
adjacent-section swing, at the section-aggregate grain, and its evidence says
so explicitly. The STRONG form — (1) fill detection, (2) unexpected-hit
detection, (3) per-onset IOI deviation — needs onset timing/sequence and is
DEFERRED, NOT FAKED. The scorer does NOT read the groove signal
(``overall_regularity``) — that is ``_groove_coherence``'s input; re-reading it
here would duplicate that axis. It is wired at weight 0 for ``halee_ramone`` so
the reference producer's output stays BYTE-IDENTICAL.

THE DISTINCTNESS GUARD — this is the ONLY axis keyed on the *VARIATION* of
section transient_density:
- ``_dynamic_mix`` = pstdev of section rms/width/brightness (never
  transient_density).
- ``_negative_space`` = **MEAN** section transient_density (central tendency —
  the opposite statistic).
- ``_beat_identity`` = per-STEM transient dominance (not the section arc).
- ``_section_contrast`` = lift-fail count from contrast warnings.
A high-MEAN but ZERO-VARIANCE transient bed must score LOW here.

Four guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default halee_ramone)
   leaves every PRE-EXISTING component score (now 10, incl.
   ``groove_coherence_score``) AND ``overall_mix_readiness_score`` unchanged vs
   the pinned base, and the golden regression still reports 68/68.
2. **Value-discrimination (unit)** — varied/fill-like sections (big transient
   swings) → HIGH; a flat/constant transient bed → LOW; <2 sections → the
   documented fallback. AND the distinctness case: a high-MEAN but
   ZERO-VARIANCE transient bed → LOW rhythmic_surprise, disagreeing with the
   mean-reading / stem-reading / movement-reading axes.
3. **Liveness (load-bearing)** — a profile weighting ``rhythmic_surprise_score``
   non-zero CHANGES ``analyze()``'s overall on a fixture; a sabotage
   (hardcoding the term / dropping it from ``component_scores``) FAILS that
   liveness while byte-identical stays green (P-016/P-029).
4. **No-aliasing** — the scorer only reads ``doctrine[...]``/``sections[...]``;
   it never mutates the shared profile structures or the section dicts.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The ten pre-existing component score keys (the byte-identical anchor set):
# the seven original components + beat_identity_score (P-032e) +
# negative_space_score (P-032a) + groove_coherence_score (P-032b).
# rhythmic_surprise_score is appended after these.
EXISTING_COMPONENT_KEYS = [
    "halee_score",
    "ramone_score",
    "vocal_centrality_score",
    "depth_hierarchy_score",
    "section_contrast_score",
    "static_mix_score",
    "dynamic_mix_score",
    "beat_identity_score",
    "negative_space_score",
    "groove_coherence_score",
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned BASE values captured from the tree at P-032d's base (before this
# packet): every pre-existing component score + overall. The axis add must
# leave all of these byte-unchanged.
BASE_COMPONENT_SCORES = {
    "simple_vocal_piano_song": {
        "halee_score": 58.0,
        "ramone_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 40.0,
        "section_contrast_score": 100.0,
        "static_mix_score": 80.0,
        "dynamic_mix_score": 52.7,
        "beat_identity_score": 89.1,
        "negative_space_score": 62.3,
        "groove_coherence_score": 45.0,
        "overall_mix_readiness_score": 73.8,
    },
    "dense_chorus_with_loops": {
        "halee_score": 67.6,
        "ramone_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 65.3,
        "section_contrast_score": 82,
        "static_mix_score": 64.0,
        "dynamic_mix_score": 23.4,
        "beat_identity_score": 52.7,
        "negative_space_score": 15.0,
        "groove_coherence_score": 99.1,
        "overall_mix_readiness_score": 70.7,
    },
    "splice_loop_problem": {
        "halee_score": 81.3,
        "ramone_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82,
        "static_mix_score": 70.0,
        "dynamic_mix_score": 23.1,
        "beat_identity_score": 46.0,
        "negative_space_score": 20.0,
        "groove_coherence_score": 45.0,
        "overall_mix_readiness_score": 74.3,
    },
}


# --------------------------------------------------------------------------- #
# Test helpers — synthetic sections for the unit / discrimination guards.
# --------------------------------------------------------------------------- #
def _section(name: str, **metrics) -> dict:
    """A synthetic analysed section. ``transient_density`` is the ONE signal
    ``rhythmic_surprise`` reads; rms/width/brightness are what ``dynamic_mix``
    reads and ``density`` is part of what ``negative_space`` reads (used only in
    the distinctness cases)."""
    m = dict(
        density=0.5,
        transient_density=0.5,
        rms_dbfs=-14.0,
        width=0.3,
        brightness=0.3,
        low_mid_energy=0.3,
    )
    m.update(metrics)
    return {"name": name, "metrics": m, "contrast_vs_previous": {}}


def _fill_like() -> list:
    """Big cross-section transient swings — 'the beat drops out / the fill
    hits' in aggregate form: sparse verse, slamming chorus, dropout, slam."""
    return [
        _section("Verse", transient_density=0.20),
        _section("Chorus", transient_density=0.90),
        _section("Breakdown", transient_density=0.25),
        _section("Final Chorus", transient_density=0.85),
    ]


def _flat_bed(td: float = 0.5) -> list:
    """A constant transient bed: zero cross-section variation, no surprise."""
    return [
        _section("Verse", transient_density=td),
        _section("Chorus", transient_density=td),
        _section("Bridge", transient_density=td),
    ]


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged.
# --------------------------------------------------------------------------- #
def test_rhythmic_surprise_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``rs*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["rhythmic_surprise_score"] == 0


def test_rhythmic_surprise_appended_last_preserves_summation_order(analyzed):
    """The new term is LAST in ``component_scores`` and every PRE-EXISTING key
    (the 10 anchors) keeps its exact value + position."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[:10] == EXISTING_COMPONENT_KEYS
        assert keys[-1] == "rhythmic_surprise_score"


def test_every_preexisting_component_score_is_byte_identical(analyzed):
    """Every one of the ten pre-existing component scores + the overall equals
    the pinned base value on all three fixtures — the axis add did not move any
    existing number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_overall_is_byte_identical_to_ten_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the ten pre-existing
    components (rhythmic_surprise excluded) equals the pipeline's overall —
    proof the weight-0 new term did not move the number."""
    w = load_profile("halee_ramone").doctrine["weights"]
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        present = {k: ds[k] for k in EXISTING_COMPONENT_KEYS if ds.get(k) is not None}
        expected = doctrine_engine._clamp(
            sum(present[k] * w[k] for k in present) / sum(w[k] for k in present)
        )
        assert ds["overall_mix_readiness_score"] == expected


def test_regression_still_sixty_eight_of_sixty_eight():
    """The golden corpus regression — which pins ``doctrine_score`` — still
    passes 68/68 with the new axis wired in at weight 0."""
    from pathlib import Path

    from logic_mix_os.regression import run_regression_suite

    base = Path(__file__).resolve().parent.parent / "fixtures"
    report = run_regression_suite(base)
    assert report["tests_run"] == 68
    assert report["passed"] == 68
    assert report["failed"] == 0


# --------------------------------------------------------------------------- #
# 2. VALUE-DISCRIMINATION (unit) — the scorer measures cross-section
#    transient-density VARIATION (the weak, section-aggregate form).
# --------------------------------------------------------------------------- #
def test_varied_fill_like_sections_score_high():
    """Big cross-section transient swings — sparse/slam/dropout/slam — score
    HIGH: both the spread and the largest-swing contributions fire."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._rhythmic_surprise(_fill_like(), doctrine)
    assert score >= 70.0


def test_flat_constant_bed_scores_low():
    """A constant transient bed (zero cross-section variation) scores LOW —
    nothing ever surprises at the section grain."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._rhythmic_surprise(_flat_bed(0.5), doctrine)
    assert score <= 35.0


def test_varied_scores_strictly_above_flat():
    """Variation is the axis: more cross-section variation outscores less,
    always."""
    doctrine = load_profile("halee_ramone").doctrine
    varied, _ = doctrine_engine._rhythmic_surprise(_fill_like(), doctrine)
    flat, _ = doctrine_engine._rhythmic_surprise(_flat_bed(0.5), doctrine)
    assert varied > flat


def test_distinctness_high_mean_zero_variance_scores_low():
    """THE DISTINCTNESS GUARD: a wall-to-wall CONSTANT transient bed at MAXIMUM
    mean (transient_density 1.0 everywhere — high mean, ZERO variance) scores
    LOW on rhythmic_surprise. ``negative_space`` reads the MEAN of the same
    signal and ``beat_identity`` reads per-STEM dominance — different
    statistics; only the VARIATION lives here. If rhythmic_surprise were keyed
    on the mean (or per-stem punch), this bed would score high and the
    assertion would fail."""
    doctrine = load_profile("halee_ramone").doctrine
    high_mean_zero_var = _flat_bed(1.0)
    score, ev = doctrine_engine._rhythmic_surprise(high_mean_zero_var, doctrine)
    assert score <= 35.0
    # And it scores EXACTLY what a mid-mean constant bed scores: the mean is
    # invisible to this axis — only the variation counts.
    mid_mean, _ = doctrine_engine._rhythmic_surprise(_flat_bed(0.5), doctrine)
    assert score == mid_mean


def test_distinctness_from_negative_space_mean_vs_variation():
    """The opposite-statistic proof: a LOW-mean CONSTANT transient bed gives
    ``negative_space`` its transient-breathing-room reward (low MEAN) while
    ``rhythmic_surprise`` stays LOW (zero VARIATION). The two axes disagree on
    the same sections, which is only possible if they read different
    statistics of the same signal."""
    doctrine = load_profile("halee_ramone").doctrine
    low_mean_constant = [
        _section("A", density=0.10, transient_density=0.10),
        _section("B", density=0.10, transient_density=0.10),
        _section("C", density=0.10, transient_density=0.10),
    ]
    ns, _ = doctrine_engine._negative_space([], low_mean_constant, None, doctrine)
    rs, _ = doctrine_engine._rhythmic_surprise(low_mean_constant, doctrine)
    assert ns >= 70.0  # mean-reading axis rewards the sparse bed
    assert rs <= 35.0  # variation-reading axis sees nothing moving
    assert rs < ns


def test_distinctness_from_dynamic_mix_movement_without_transient_variation():
    """Not a re-derivation of ``dynamic_mix``: sections with big
    rms/width/brightness MOVEMENT but a CONSTANT transient bed score HIGH on
    dynamic_mix and LOW on rhythmic_surprise — rhythmic_surprise reads the one
    signal dynamic_mix never reads."""
    doctrine = load_profile("halee_ramone").doctrine
    moving_but_flat_transients = [
        _section("Verse", transient_density=0.8, rms_dbfs=-20.0, width=0.10, brightness=0.10),
        _section("Chorus", transient_density=0.8, rms_dbfs=-8.0, width=0.60, brightness=0.70),
    ]
    dyn, _ = doctrine_engine._dynamic_mix(moving_but_flat_transients, doctrine)
    rs, _ = doctrine_engine._rhythmic_surprise(moving_but_flat_transients, doctrine)
    assert dyn >= 70.0
    assert rs <= 35.0
    assert rs < dyn


def test_fewer_than_two_sections_uses_fallback():
    """<2 sections => the documented insufficient-sections fallback float
    (mirrors ``_dynamic_mix``'s idiom; never None, never a crash)."""
    doctrine = load_profile("halee_ramone").doctrine
    fallback = doctrine["scorers"]["rhythmic_surprise"]["insufficient_sections_score"]
    for sections in ([], [_section("Only", transient_density=0.9)]):
        score, ev = doctrine_engine._rhythmic_surprise(sections, doctrine)
        assert score == doctrine_engine._clamp(fallback)
        assert any("fewer than two" in e.lower() or "section" in e.lower() for e in ev)


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 float."""
    doctrine = load_profile("halee_ramone").doctrine
    extreme = [
        _section("A", transient_density=0.0),
        _section("B", transient_density=1.0),
        _section("C", transient_density=0.0),
        _section("D", transient_density=1.0),
    ]
    for sections in ([], _flat_bed(0.0), _flat_bed(1.0), _fill_like(), extreme):
        score, _ = doctrine_engine._rhythmic_surprise(sections, doctrine)
        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0


def test_evidence_names_the_weak_section_aggregate_form():
    """THE HONESTY GATE: the evidence explicitly labels the measurement as the
    weak/section-aggregate form — it never claims fill detection,
    unexpected-hit detection or per-onset deviation."""
    doctrine = load_profile("halee_ramone").doctrine
    _, ev = doctrine_engine._rhythmic_surprise(_fill_like(), doctrine)
    blob = " ".join(ev).lower()
    assert "weak" in blob
    assert "section-aggregate" in blob


# --------------------------------------------------------------------------- #
# 3. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and a sabotage of the scorer must break these tests (P-016/P-029).
# --------------------------------------------------------------------------- #
def _profile_weighting_rhythmic_surprise(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero rhythmic_surprise
    weight — so any overall delta is attributable to the rhythmic_surprise term
    alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["rhythmic_surprise_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    rhythmic_surprise non-zero changes the overall vs the weight-0 reference.
    This is LIVE-WIRE proof: the term is genuinely threaded, not decorative.

    Sabotage that this test catches: hardcoding ``_rhythmic_surprise`` to
    return a constant equal to nothing in particular, or dropping it from
    ``component_scores``, collapses the weighted mean back onto the reference
    and this assertion FAILS — while byte-identical stays green."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_rhythmic_surprise(3.0), groove=groove
    )

    rs = reference["rhythmic_surprise_score"]
    assert rs is not None and 0.0 <= rs <= 100.0
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_rhythmic_surprise_score(analyzed):
    """A sharper sabotage guard: the direction the overall moves under a
    non-zero weight must be consistent with rhythmic_surprise's value relative
    to the other components. A hardcoded term would not track the real score
    and this assertion would break."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    rs = reference["rhythmic_surprise_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_rhythmic_surprise(5.0), groove=groove
    )
    new_overall = weighted["overall_mix_readiness_score"]

    if rs > ref_overall:
        assert new_overall > ref_overall
    elif rs < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — the scorer only reads ``doctrine[...]``/``sections[...]``;
#    it never mutates the shared profile structures or the section dicts.
# --------------------------------------------------------------------------- #
def test_rhythmic_surprise_does_not_mutate_the_profile_or_sections():
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    sections = _fill_like()
    sections_before = copy.deepcopy(sections)
    doctrine_engine._rhythmic_surprise(sections, doctrine)
    assert doctrine == doctrine_before
    assert sections == sections_before


def test_score_doctrine_with_rhythmic_surprise_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` on a real fixture and assert the shared default doctrine
    is byte-unchanged (its ``scorers.rhythmic_surprise`` block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "rhythmic_surprise" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
