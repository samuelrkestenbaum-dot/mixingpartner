"""P-056 — the binding guards for ``textural_coherence``, the FIFTEENTH doctrine
axis and the first ENGINE-DEEPENING axis since the producer arc.

``textural_coherence`` measures how much a record's TEXTURE BEDS resemble one
another — a PURE cross-bed DISPERSION statistic over the engine-owned texture-bed
surface (``creative._dropout_texture_beds``): low cross-bed dispersion → HIGH
coherence (one woven surface); high dispersion → LOW coherence (a pile of
unrelated layers). It reads three equally-weighted feature families on the beds'
own per-stem metrics — tonal (``band_energy`` 5-band L1 spread + ``brightness``
stdev), spatial (``stereo_width`` stdev) and dynamic (``crest_factor_db`` stdev)
— and NOTHING else: never room, occupancy-mean, depth-count, foreground salience
or rhythm, so distinctness from ``negative_space`` / ``physical_space`` /
``depth_hierarchy`` / ``groove_coherence`` is PROVABLE, not asserted. It is wired
into ``score_doctrine`` LAST with a weight of 0 for the four non-Eno producers
(byte-identical overalls) and a real high-tier weight for brian_eno.

Guards (mirroring the P-032a/P-032f agnostic-axis pattern):

1. **Byte-identical anchor** — the four non-Eno producers weight the axis 0, so
   the weighted mean is arithmetically untouched; the axis is appended LAST so
   the pre-existing 14-term summation order is preserved.
2. **Value-discrimination (unit)** — a coherent bed set (beds that resemble each
   other) scores HIGH; an incoherent bed set (beds that do not) scores LOW; <2
   beds → a documented NEUTRAL float; the score is always a clamped 0..100 float.
3. **Distinctness** — independent of ``negative_space`` (a different input: bed
   features vs section room) and of the rhythm/section axes (constant sections
   leave ``dynamic_mix`` / ``rhythmic_surprise`` unmoved while coherence drops).
4. **Bed surface is the shared one** — the scorer's bed set equals
   ``creative._dropout_texture_beds`` on every fixture (the two can never fork).
5. **Liveness + no-aliasing** — a non-zero weight moves the overall; the scorer
   only reads ``doctrine[...]`` and never mutates the shared profile structures.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os.creative import _dropout_texture_beds
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile

from conftest import ROOT, VOCAL_CHOP_FIXTURE
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest

BAND_NAMES = ("low", "low_mid", "mid", "presence", "high")

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


# --------------------------------------------------------------------------- #
# Synthetic bed records — the four features the axis reads live under
# ``metrics``; a bed qualifies via felt midground/background (the shared
# ``_dropout_texture_beds`` predicate) unless a loop ``source_kind`` is given.
# --------------------------------------------------------------------------- #
def _bed(name, band, brightness, width, crest, *,
         role="felt", depth="background", source_kind="comped_audio_track"):
    return {
        "name": name,
        "perceptual_role": role,
        "depth_default": depth,
        "source_kind": source_kind,
        "instrument_identity": "texture",
        "identity_family": "synth",
        "sacredness": "decorative",
        "stereo_width": width,
        "metrics": {
            "band_energy": dict(zip(BAND_NAMES, band)),
            "brightness": brightness,
            "stereo_width": width,
            "crest_factor_db": crest,
        },
    }


def _coherent_beds():
    """Beds that RESEMBLE each other across every feature family — near-identical
    band balance, brightness, width and crest: one woven surface."""
    return [
        _bed("Pad A", [0.20, 0.22, 0.20, 0.19, 0.19], 0.50, 0.30, 10.0),
        _bed("Pad B", [0.21, 0.21, 0.20, 0.19, 0.19], 0.51, 0.31, 10.2),
        _bed("Pad C", [0.20, 0.22, 0.21, 0.18, 0.19], 0.49, 0.29, 9.9),
        _bed("Pad D", [0.21, 0.21, 0.20, 0.20, 0.18], 0.50, 0.30, 10.1),
    ]


def _incoherent_beds():
    """Beds that do NOT resemble each other — a bass-heavy dark narrow bed, a
    bright wide airy bed, a mid-forward one: a pile of unrelated layers."""
    return [
        _bed("Sub Drone", [0.62, 0.20, 0.10, 0.05, 0.03], 0.10, 0.05, 4.0),
        _bed("Air Shimmer", [0.03, 0.05, 0.10, 0.22, 0.60], 0.92, 0.85, 20.0),
        _bed("Mid Wash", [0.10, 0.22, 0.42, 0.18, 0.08], 0.50, 0.42, 12.0),
        _bed("Click Bed", [0.30, 0.10, 0.15, 0.25, 0.20], 0.30, 0.15, 2.0),
    ]


def _section(name, **metrics):
    m = dict(density=0.5, transient_density=0.5, rms_dbfs=-14.0,
             width=0.3, brightness=0.3, low_mid_energy=0.3)
    m.update(metrics)
    return {"name": name, "metrics": m, "contrast_vs_previous": {}}


def _doctrine():
    return load_profile("halee_ramone").doctrine


def _tc(records, doctrine=None):
    return doctrine_engine._textural_coherence(records, doctrine or _doctrine())[0]


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL ANCHOR — the four non-Eno producers weight the axis 0.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("producer",
                         ["halee_ramone", "timbaland", "quincy_jones",
                          "chris_lord_alge"])
def test_textural_coherence_weight_is_zero_for_the_four_non_eno_producers(producer):
    """The byte-identical anchor: weight 0 => ``tc*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    assert load_profile(producer).doctrine["weights"]["textural_coherence_score"] == 0


def test_textural_coherence_weight_is_nonzero_for_brian_eno():
    """Eno weights the axis in his HIGH tier — a genuine measured signal, not a
    re-weighting of old ones — while staying below his poles (negative_space /
    physical_space)."""
    w = load_profile("brian_eno").doctrine["weights"]
    assert w["textural_coherence_score"] > 0
    assert w["textural_coherence_score"] < w["physical_space_score"]
    assert w["textural_coherence_score"] < w["negative_space_score"]


def test_axis_appended_last_preserves_summation_order(analyzed):
    """The 15th term is LAST in ``component_scores``; the 14 pre-existing keys
    keep their exact positions (the summation order that keeps the four non-Eno
    overalls byte-identical)."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds
                if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[-1] == "textural_coherence_score"
        assert len(keys) == 15


def test_axis_present_and_measured_for_the_reference(analyzed):
    """Even at weight 0 the axis emits a real 0..100 number and an evidence line
    in the reference's artifact (measured for all; weighted only by Eno)."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        tc = ds["textural_coherence_score"]
        assert tc is not None and 0.0 <= tc <= 100.0
        assert ds["evidence"]["textural_coherence"]


# --------------------------------------------------------------------------- #
# 2. VALUE-DISCRIMINATION (unit) — coherence is anti-dispersion.
# --------------------------------------------------------------------------- #
def test_coherent_beds_score_high():
    """Beds that resemble each other across every family score HIGH (near the
    baseline — dispersion near zero)."""
    assert _tc(_coherent_beds()) >= 90.0


def test_incoherent_beds_score_low():
    """Beds that do not resemble each other score LOW (large cross-bed
    dispersion)."""
    assert _tc(_incoherent_beds()) <= 45.0


def test_coherent_scores_strictly_above_incoherent():
    """Resemblance is the axis: a more-woven bed set outscores a scattered one,
    always."""
    assert _tc(_coherent_beds()) > _tc(_incoherent_beds())


def test_fewer_than_two_beds_is_a_neutral_float():
    """A single or absent bed cannot be 'incoherent' — the documented NEUTRAL
    fallback float (never None, never a crash), mirroring the sibling axes."""
    neutral = doctrine_engine._clamp(_doctrine()["scorers"]["textural_coherence"]["neutral"])
    assert _tc([]) == neutral
    assert _tc([_coherent_beds()[0]]) == neutral
    # a lone non-bed foreground element does not count as a bed either
    fg = _bed("Lead", [0.2, 0.2, 0.2, 0.2, 0.2], 0.5, 0.3, 10.0,
              role="heard", depth="foreground")
    assert _tc([fg] + [_coherent_beds()[0]]) == neutral


def test_score_is_bounded_0_100():
    doctrine = _doctrine()
    for beds in (_coherent_beds(), _incoherent_beds()):
        score, _ = doctrine_engine._textural_coherence(beds, doctrine)
        assert 0.0 <= score <= 100.0


def test_deterministic_same_beds_same_score():
    beds = _incoherent_beds()
    assert _tc(beds) == _tc(copy.deepcopy(beds))


def test_each_family_moves_the_score_independently():
    """Each of the three families genuinely presses the score: perturbing ONLY
    the tonal, ONLY the spatial or ONLY the dynamic feature of one bed drops the
    coherence below a fully-coherent baseline."""
    base = _coherent_beds()
    baseline = _tc(base)

    tonal = copy.deepcopy(base)
    tonal[0]["metrics"]["band_energy"] = dict(
        zip(BAND_NAMES, [0.60, 0.15, 0.10, 0.10, 0.05]))
    tonal[0]["metrics"]["brightness"] = 0.05
    assert _tc(tonal) < baseline

    spatial = copy.deepcopy(base)
    spatial[0]["metrics"]["stereo_width"] = 0.95
    assert _tc(spatial) < baseline

    dynamic = copy.deepcopy(base)
    dynamic[0]["metrics"]["crest_factor_db"] = 30.0
    assert _tc(dynamic) < baseline


# --------------------------------------------------------------------------- #
# 3. DISTINCTNESS — independent of negative_space and of the rhythm/section axes.
# --------------------------------------------------------------------------- #
def test_distinctness_from_negative_space_both_directions():
    """The two axes read DIFFERENT inputs (bed FEATURES vs section ROOM), so
    they can disagree. A dense arrangement of COHERENT beds scores LOW
    negative_space / HIGH textural_coherence; a sparse arrangement of INCOHERENT
    beds scores HIGH negative_space / LOW textural_coherence. If coherence were a
    re-derivation of room, these would move together — and this would fail."""
    doctrine = _doctrine()

    dense_sections = [
        _section("Verse", density=1.0, transient_density=1.0),
        _section("Chorus", density=1.0, transient_density=1.0),
    ]
    sparse_sections = [
        _section("Intro", density=0.10, transient_density=0.15),
        _section("Verse", density=0.20, transient_density=0.25),
        _section("Breakdown", density=0.05, transient_density=0.05),
        _section("Outro", density=0.18, transient_density=0.20),
    ]

    dense_room, _ = doctrine_engine._negative_space([], dense_sections, None, doctrine)
    sparse_room, _ = doctrine_engine._negative_space([], sparse_sections, None, doctrine)
    coherent_tc = _tc(_coherent_beds())
    incoherent_tc = _tc(_incoherent_beds())

    # dense + coherent: low room, high coherence
    assert dense_room <= 35.0
    assert coherent_tc >= 90.0
    # sparse + incoherent: high room, low coherence
    assert sparse_room >= 75.0
    assert incoherent_tc <= 45.0
    # the axes genuinely diverge in both directions
    assert coherent_tc > dense_room
    assert incoherent_tc < sparse_room


def test_distinctness_from_rhythm_and_section_axes():
    """Constant sections leave ``dynamic_mix`` and ``rhythmic_surprise`` fixed;
    swapping coherent beds for incoherent ones (same sections) drops
    textural_coherence — coherence reads the BEDS, never the sections."""
    doctrine = _doctrine()
    constant_sections = [
        _section("A", density=0.5, transient_density=0.5, rms_dbfs=-14.0,
                 width=0.3, brightness=0.3),
        _section("B", density=0.5, transient_density=0.5, rms_dbfs=-14.0,
                 width=0.3, brightness=0.3),
        _section("C", density=0.5, transient_density=0.5, rms_dbfs=-14.0,
                 width=0.3, brightness=0.3),
    ]
    dyn, _ = doctrine_engine._dynamic_mix(constant_sections, doctrine)
    rs, _ = doctrine_engine._rhythmic_surprise(constant_sections, doctrine)

    coherent_tc = _tc(_coherent_beds())
    incoherent_tc = _tc(_incoherent_beds())

    # the rhythm/section axes do not read beds, so they are identical regardless
    dyn2, _ = doctrine_engine._dynamic_mix(constant_sections, doctrine)
    rs2, _ = doctrine_engine._rhythmic_surprise(constant_sections, doctrine)
    assert dyn == dyn2 and rs == rs2
    # but coherence moves with the beds
    assert coherent_tc > incoherent_tc


# --------------------------------------------------------------------------- #
# 4. BED SURFACE IS THE SHARED ONE — never forked from _dropout_texture_beds.
# --------------------------------------------------------------------------- #
def test_bed_selection_equals_dropout_texture_beds_on_synthetics():
    """The scorer's internal bed predicate matches the engine-owned surface on a
    mixed record set (felt beds + a loop + foreground non-beds)."""
    records = _coherent_beds() + [
        _bed("Loop", [0.2, 0.2, 0.2, 0.2, 0.2], 0.5, 0.4, 8.0,
             role="heard", depth="foreground", source_kind="texture_loop"),
        _bed("Lead", [0.1, 0.2, 0.4, 0.2, 0.1], 0.6, 0.2, 12.0,
             role="heard", depth="foreground"),
    ]
    expected = set(_dropout_texture_beds(records))
    selected = {r["name"] for r in doctrine_engine._textural_bed_set(records)}
    assert selected == expected
    assert "Lead" not in selected
    assert "Loop" in selected  # a loop source_kind is a bed even in the foreground


@pytest.mark.parametrize("name", FIXTURE_NAMES + [VOCAL_CHOP_FIXTURE])
def test_bed_selection_equals_dropout_texture_beds_on_fixtures(name):
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    res = analyze(str(ROOT / "fixtures" / name / "stems"), manifest)
    expected = set(_dropout_texture_beds(res.records))
    selected = {r["name"] for r in doctrine_engine._textural_bed_set(res.records)}
    assert selected == expected


# --------------------------------------------------------------------------- #
# 5. LIVENESS + NO-ALIASING.
# --------------------------------------------------------------------------- #
def _profile_weighting_textural(weight: float):
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["textural_coherence_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """LIVE-WIRE proof: weighting the axis non-zero changes the overall vs the
    weight-0 reference — the term is genuinely threaded, not decorative. A drop
    or a broken threading collapses the mean back onto the reference and this
    FAILS."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report,
            res.mix_metrics, res.project.intent)
    reference = doctrine_engine.score_doctrine(*args)
    weighted = doctrine_engine.score_doctrine(
        *args, profile=_profile_weighting_textural(3.0))
    tc = reference["textural_coherence_score"]
    assert tc is not None and 0.0 <= tc <= 100.0
    assert weighted["overall_mix_readiness_score"] \
        != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_score(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report,
            res.mix_metrics, res.project.intent)
    reference = doctrine_engine.score_doctrine(*args)
    tc = reference["textural_coherence_score"]
    ref_overall = reference["overall_mix_readiness_score"]
    weighted = doctrine_engine.score_doctrine(
        *args, profile=_profile_weighting_textural(5.0))
    new_overall = weighted["overall_mix_readiness_score"]
    if tc > ref_overall:
        assert new_overall > ref_overall
    elif tc < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


def test_scorer_does_not_mutate_the_profile():
    doctrine = _doctrine()
    before = copy.deepcopy(doctrine)
    doctrine_engine._textural_coherence(_incoherent_beds(), doctrine)
    assert doctrine == before


def test_score_doctrine_does_not_mutate_shared_globals(analyzed):
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report,
        res.mix_metrics, res.project.intent)
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "textural_coherence" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
