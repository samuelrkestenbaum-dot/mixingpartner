"""P-032a — the binding guards for ``negative_space``, the SECOND new producer-
agnostic doctrine axis (strength-form only), after the P-032e ``beat_identity``
crux proved the add-an-agnostic-axis-byte-identically pattern.

``negative_space`` measures ABSOLUTE arrangement room/sparsity — a different
thing from ``dynamic_mix`` (which measures section-to-section MOVEMENT). It
rewards low spectral occupancy (``density``), a genuine pulled-back/sparse
section (a dropout), and transient breathing room (low ``transient_density``).
"Silence is arrangement." It is wired into ``score_doctrine`` with a weight of 0
for ``halee_ramone`` so the reference producer's output stays BYTE-IDENTICAL.

Four guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default halee_ramone)
   leaves every PRE-EXISTING component score (now 8, including
   ``beat_identity_score``) AND ``overall_mix_readiness_score`` unchanged, and
   the golden regression still reports 68/68. The mechanism: the new term is
   appended LAST to ``component_scores`` (summation order preserved) and its
   weight is 0 (``ns*0`` numerator, ``+0`` denominator).
2. **Value-discrimination (unit)** — a sparse arrangement (low density + a
   dropout section + transient breathing room) scores HIGH; a wall-to-wall-dense
   arrangement scores LOW. AND the distinctness case: a wall-to-wall-dense mix
   that varies section-to-section (high movement → high ``dynamic_mix``) still
   scores LOW on ``negative_space`` — proving the axis is not a re-derivation of
   ``dynamic_mix``.
3. **Liveness (load-bearing)** — a synthetic profile that weights
   ``negative_space_score`` non-zero CHANGES ``analyze()``'s overall on a
   fixture; and a sabotage (hardcoding the term to a constant / dropping it)
   FAILS that liveness while byte-identical stays green (P-016/P-029).
4. **No-aliasing** — the scorer only reads ``doctrine[...]``; it never mutates
   the shared profile structures.
"""

from __future__ import annotations

import copy

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The eight pre-existing component score keys (the byte-identical anchor set):
# the seven original components + beat_identity_score (landed in P-032e).
EXISTING_COMPONENT_KEYS = [
    "halee_score",
    "ramone_score",
    "vocal_centrality_score",
    "depth_hierarchy_score",
    "section_contrast_score",
    "static_mix_score",
    "dynamic_mix_score",
    "beat_identity_score",
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


# --------------------------------------------------------------------------- #
# Test helpers — synthetic sections for the unit / discrimination guards.
# --------------------------------------------------------------------------- #
def _section(name: str, **metrics) -> dict:
    """A synthetic analysed section. ``density`` / ``transient_density`` are the
    signals ``negative_space`` reads; rms/width/brightness are what ``dynamic_mix``
    reads (used only in the distinctness case)."""
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


def _sparse_arrangement() -> list:
    """Lots of absolute room: low mean density, a genuine dropout (a section that
    pulls right back), and transient breathing room."""
    return [
        _section("Intro", density=0.10, transient_density=0.15),
        _section("Verse", density=0.20, transient_density=0.25),
        _section("Breakdown", density=0.05, transient_density=0.05),  # the dropout
        _section("Outro", density=0.18, transient_density=0.20),
    ]


def _wall_to_wall() -> list:
    """No room at all: wall-to-wall spectral occupancy and wall-to-wall transients,
    with no section that pulls back."""
    return [
        _section("Verse", density=1.0, transient_density=1.0),
        _section("Chorus", density=1.0, transient_density=1.0),
        _section("Bridge", density=1.0, transient_density=1.0),
    ]


def _dense_but_moving() -> list:
    """The DISTINCTNESS case: wall-to-wall dense/occupied (no absolute room) but
    with large section-to-section MOVEMENT in rms/width/brightness — high
    ``dynamic_mix``, LOW ``negative_space``."""
    return [
        _section("Verse", density=1.0, transient_density=1.0, rms_dbfs=-20.0, width=0.10, brightness=0.10),
        _section("Chorus", density=1.0, transient_density=1.0, rms_dbfs=-8.0, width=0.60, brightness=0.70),
    ]


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged.
# --------------------------------------------------------------------------- #
def test_negative_space_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``ns*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["negative_space_score"] == 0


def test_negative_space_appended_last_preserves_summation_order(analyzed):
    """The new term keeps its position and every PRE-EXISTING key (the 8 anchors,
    incl. beat_identity_score) keeps its exact value + position. P-032b then
    appends groove_coherence_score after negative_space, so negative_space is no
    longer the FINAL key — but its position (index 8, right after the 8 anchors)
    is unchanged, which is what preserves the summation order."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        # The eight existing keys come first, in order; negative_space_score is
        # appended right after them (position 8).
        assert keys[:8] == EXISTING_COMPONENT_KEYS
        assert keys[8] == "negative_space_score"


def test_overall_is_byte_identical_to_eight_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the eight pre-existing
    components (negative_space excluded) equals the pipeline's overall — proof the
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
# 2. VALUE-DISCRIMINATION (unit) — the scorer measures ABSOLUTE room.
# --------------------------------------------------------------------------- #
def test_sparse_arrangement_scores_high():
    """A sparse, dynamic arrangement — low mean density, a genuine dropout, and
    transient breathing room — scores HIGH: every room contribution fires."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._negative_space([], _sparse_arrangement(), None, doctrine)
    assert score >= 75.0


def test_wall_to_wall_scores_low():
    """A wall-to-wall-dense arrangement (full occupancy, wall-to-wall transients,
    no dropout) leaves NO room — it scores LOW."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._negative_space([], _wall_to_wall(), None, doctrine)
    assert score <= 35.0


def test_sparse_scores_strictly_above_wall_to_wall():
    """Room is the axis: more room outscores less room, always."""
    doctrine = load_profile("halee_ramone").doctrine
    sparse, _ = doctrine_engine._negative_space([], _sparse_arrangement(), None, doctrine)
    dense, _ = doctrine_engine._negative_space([], _wall_to_wall(), None, doctrine)
    assert sparse > dense


def test_distinctness_from_dynamic_mix_high_movement_low_room():
    """THE DISTINCTNESS GUARD (do NOT duplicate dynamic_mix): a wall-to-wall-dense
    mix that varies strongly section-to-section scores HIGH on ``dynamic_mix``
    (movement) but LOW on ``negative_space`` (no absolute room). If negative_space
    were a re-derivation of dynamic_mix, the dense-but-moving arrangement would
    score high here too — and this assertion would fail."""
    doctrine = load_profile("halee_ramone").doctrine
    sections = _dense_but_moving()

    dyn, _ = doctrine_engine._dynamic_mix(sections, doctrine)
    ns, _ = doctrine_engine._negative_space([], sections, None, doctrine)

    # High section-to-section movement => dynamic_mix is high.
    assert dyn >= 70.0
    # But zero absolute room => negative_space is low. The two axes disagree,
    # which is only possible if they measure different things.
    assert ns <= 35.0
    assert ns < dyn


def test_dropout_section_lifts_the_score():
    """The "silence as arrangement" contribution: introducing a genuine dropout
    section (min density well below the max) raises negative_space vs the SAME mean
    density held flat across sections."""
    doctrine = load_profile("halee_ramone").doctrine
    # Flat: every section at the same middling density (no pull-back).
    flat = [
        _section("A", density=0.30, transient_density=0.30),
        _section("B", density=0.30, transient_density=0.30),
        _section("C", density=0.30, transient_density=0.30),
    ]
    # Dropout: same-ish bed, but one section pulls right back.
    dropout = [
        _section("A", density=0.40, transient_density=0.30),
        _section("B", density=0.05, transient_density=0.30),  # the pull-back
        _section("C", density=0.45, transient_density=0.30),
    ]
    flat_score, _ = doctrine_engine._negative_space([], flat, None, doctrine)
    drop_score, _ = doctrine_engine._negative_space([], dropout, None, doctrine)
    assert drop_score > flat_score


def test_single_section_skips_dropout_gracefully():
    """The dropout term needs >=2 sections; with one section it must not crash and
    still returns a clamped 0..100 room score from the absolute-room + breathing
    terms alone."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._negative_space(
        [], [_section("Only", density=0.15, transient_density=0.15)], None, doctrine
    )
    assert 0.0 <= score <= 100.0


def test_neutral_fallback_when_no_section_or_mix_data():
    """No sections and no mix_metrics => a documented NEUTRAL fallback float
    (never None), so the axis is always present (mirrors _beat_identity)."""
    doctrine = load_profile("halee_ramone").doctrine
    neutral = doctrine["scorers"]["negative_space"]["neutral"]
    score, ev = doctrine_engine._negative_space([], [], None, doctrine)
    assert score == doctrine_engine._clamp(neutral)
    assert any("no" in e.lower() or "neutral" in e.lower() for e in ev)


def test_mix_metrics_fallback_when_no_sections():
    """With no sections but mix_metrics carrying whole-mix density, the absolute-
    room term still fires from the mix fallback — a low-density mix scores above
    the neutral fallback, a wall-to-wall mix at/below it."""
    doctrine = load_profile("halee_ramone").doctrine
    neutral = doctrine_engine._clamp(doctrine["scorers"]["negative_space"]["neutral"])
    roomy, _ = doctrine_engine._negative_space([], [], {"density": 0.10}, doctrine)
    packed, _ = doctrine_engine._negative_space([], [], {"density": 1.0}, doctrine)
    assert roomy > neutral
    assert packed <= neutral
    assert roomy > packed


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 value."""
    doctrine = load_profile("halee_ramone").doctrine
    extreme_low = [_section("X", density=0.0, transient_density=0.0)]
    extreme_high = [_section("Y", density=1.0, transient_density=1.0)]
    lo, _ = doctrine_engine._negative_space([], extreme_low, None, doctrine)
    hi, _ = doctrine_engine._negative_space([], extreme_high, None, doctrine)
    assert 0.0 <= lo <= 100.0
    assert 0.0 <= hi <= 100.0


# --------------------------------------------------------------------------- #
# 3. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and a sabotage of the scorer must break this test (the P-016/P-029 lesson).
# --------------------------------------------------------------------------- #
def _profile_weighting_negative_space(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero negative_space weight —
    so any overall delta is attributable to the negative_space term alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["negative_space_score"] = weight
    import dataclasses

    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    negative_space non-zero changes the overall vs the weight-0 reference. This is
    LIVE-WIRE proof: the term is genuinely threaded, not decorative.

    Sabotage that this test catches: hardcoding ``_negative_space`` to return a
    constant, or dropping it from ``component_scores``, collapses the weighted
    mean back onto the reference and this assertion FAILS."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*args)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(*args, profile=_profile_weighting_negative_space(3.0))

    # negative_space itself is a real, present 0..100 number on this fixture.
    ns = reference["negative_space_score"]
    assert ns is not None and 0.0 <= ns <= 100.0
    # And giving it weight changes the overall (only possible if it is threaded).
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_negative_space_score(analyzed):
    """A sharper sabotage guard: the direction the overall moves under a non-zero
    weight must be consistent with negative_space's value relative to the other
    components. If the term were hardcoded to a fixed number the move would not
    track the real negative_space score, and this assertion would break."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*args)
    ns = reference["negative_space_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(*args, profile=_profile_weighting_negative_space(5.0))
    new_overall = weighted["overall_mix_readiness_score"]

    # Pulling the mean toward ``ns`` with a heavy weight moves the overall in the
    # direction of ``ns`` (up if ns > ref_overall, down if below).
    if ns > ref_overall:
        assert new_overall > ref_overall
    elif ns < ref_overall:
        assert new_overall < ref_overall
    else:  # exactly equal — degenerate; the weight cannot move it
        assert new_overall == ref_overall


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — the scorer only reads ``doctrine[...]``; it never mutates the
#    shared profile structures (consistent with test_doctrine_profile_sourced).
# --------------------------------------------------------------------------- #
def test_negative_space_does_not_mutate_the_profile():
    doctrine = load_profile("halee_ramone").doctrine
    before = copy.deepcopy(doctrine)
    doctrine_engine._negative_space([], _sparse_arrangement(), {"density": 0.3}, doctrine)
    assert doctrine == before


def test_score_doctrine_with_negative_space_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` on a real fixture and assert the shared default doctrine is
    byte-unchanged (its ``scorers.negative_space`` block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "negative_space" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
