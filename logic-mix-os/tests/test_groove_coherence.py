"""P-032b — the binding guards for ``groove_coherence``, the THIRD new producer-
agnostic doctrine axis, and the FIRST live-wire relocation in the P-032.x arc.

Unlike ``beat_identity`` (P-032e) and ``negative_space`` (P-032a) — pure additive
scorers over signals already visible to doctrine — ``groove_coherence`` reads a
signal (``analyze_groove`` → ``overall_regularity`` = per-track ``1 − CoV(IOIs)``)
that used to be computed AFTER ``score_doctrine`` in the pipeline. To feed it to
doctrine the pipeline now computes ``groove`` ONCE, BEFORE doctrine, threads it in
via a new ``score_doctrine(..., groove=…)`` keyword, and REUSES the exact same
object in ``result.expanded["groove"]`` — a behavior-preserving relocation.

HONEST NAMING: ``overall_regularity`` measures rhythmic tightness/CONSISTENCY, not
"identity coherence" in the full sense. This axis scores groove
regularity/consistency as a *proxy* for coherence, and it does NOT bake in a
"tighter = better" bias — the agnostic layer stays neutral; a *producer* chooses
whether/how to weight it. It is wired at weight 0 for ``halee_ramone`` so the
reference producer's output stays BYTE-IDENTICAL.

Five guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default halee_ramone)
   leaves every PRE-EXISTING component score (now 9) AND
   ``overall_mix_readiness_score`` unchanged vs the pinned base, and the golden
   regression still reports 68/68. AND ``result.expanded["groove"]`` is
   byte-unchanged vs the pinned base (the relocation is behavior-preserving).
2. **No-re-run live-wire (THE P-016 GUARD)** — during a full ``analyze()``,
   ``analyze_groove`` is called EXACTLY ONCE (spy/patch a call counter) — proving
   it is computed before doctrine and REUSED, not re-run. AND ``score_doctrine``
   actually receives the real groove: ``groove_coherence`` in the doctrine output
   reflects the real ``overall_regularity`` on ``dense_chorus_with_loops`` (NOT
   the None-fallback).
3. **Value-discrimination (unit)** — a coherent/regular groove dict → HIGH
   groove_coherence; ``overall_regularity=None``/incoherent → neutral/low.
4. **Liveness (load-bearing)** — a profile weighting ``groove_coherence_score``
   non-zero CHANGES ``analyze()``'s overall on ``dense_chorus_with_loops``; a
   sabotage (passing ``groove=None`` into ``score_doctrine``, i.e. breaking the
   threading) makes the liveness + no-re-run assertions FAIL while byte-identical
   stays green (P-016/P-029).
5. **No-aliasing** — the scorer only reads ``doctrine[...]``/``groove[...]``; it
   never mutates the shared profile structures or the groove dict.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

import logic_mix_os.pipeline as pipeline
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The nine pre-existing component score keys (the byte-identical anchor set):
# the seven original components + beat_identity_score (P-032e) +
# negative_space_score (P-032a). groove_coherence_score is appended after these.
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
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned BASE values captured from the tree at P-032b's base (before this packet):
# every pre-existing component score + overall + ``expanded["groove"]``. The
# relocation must leave all of these byte-unchanged.
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
        "overall_mix_readiness_score": 74.3,
    },
}

BASE_GROOVE = {
    "simple_vocal_piano_song": {
        "per_track": [],
        "overall_regularity": None,
        "summary": "No rhythm stems detected.",
    },
    "dense_chorus_with_loops": {
        "per_track": [
            {"track": "Kick", "onsets": 5, "regularity": 0.989, "feel": "machine-tight"},
            {"track": "Snare", "onsets": 2, "regularity": None, "feel": "too few onsets to judge"},
        ],
        "overall_regularity": 0.989,
        "summary": "Overall groove regularity 0.989 (tight).",
    },
    "splice_loop_problem": {
        "per_track": [],
        "overall_regularity": None,
        "summary": "No rhythm stems detected.",
    },
}


# --------------------------------------------------------------------------- #
# Test helpers — synthetic groove dicts for the unit / discrimination guards.
# --------------------------------------------------------------------------- #
def _groove(overall, per_track=None):
    return {
        "per_track": per_track or [],
        "overall_regularity": overall,
        "summary": "synthetic",
    }


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged, AND the
#    relocated groove is behavior-preserving.
# --------------------------------------------------------------------------- #
def test_groove_coherence_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``gc*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["groove_coherence_score"] == 0


def test_groove_coherence_appended_last_preserves_summation_order(analyzed):
    """The new term is LAST in ``component_scores`` and every PRE-EXISTING key
    (the 9 anchors) keeps its exact value + position."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[:9] == EXISTING_COMPONENT_KEYS
        assert keys[-1] == "groove_coherence_score"


def test_every_preexisting_component_score_is_byte_identical(analyzed):
    """Every one of the nine pre-existing component scores + the overall equals
    the pinned base value on all three fixtures — the axis add did not move any
    existing number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_overall_is_byte_identical_to_nine_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the nine pre-existing
    components (groove_coherence excluded) equals the pipeline's overall — proof
    the weight-0 new term did not move the number."""
    w = load_profile("halee_ramone").doctrine["weights"]
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        present = {k: ds[k] for k in EXISTING_COMPONENT_KEYS if ds.get(k) is not None}
        expected = doctrine_engine._clamp(
            sum(present[k] * w[k] for k in present) / sum(w[k] for k in present)
        )
        assert ds["overall_mix_readiness_score"] == expected


def test_expanded_groove_is_behavior_preserving(analyzed):
    """THE RELOCATION GUARD: ``result.expanded["groove"]`` is byte-unchanged vs
    the pinned base on all three fixtures. Computing groove earlier and reusing it
    must yield the exact same value the old post-doctrine call produced."""
    for name in FIXTURE_NAMES:
        assert analyzed[name].expanded["groove"] == BASE_GROOVE[name]


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
# 2. NO-RE-RUN LIVE-WIRE — THE P-016 GUARD. During a full analyze(),
#    analyze_groove runs EXACTLY ONCE (computed before doctrine, reused), and
#    score_doctrine actually receives the real groove.
# --------------------------------------------------------------------------- #
def _analyze_dense_with_groove_spy(monkeypatch):
    """Run a fresh (uncached) ``analyze()`` on ``dense_chorus_with_loops`` with a
    spy wrapping ``pipeline.analyze_groove`` that counts calls. Returns
    ``(result, counter)`` where ``counter["n"]`` is the number of invocations."""
    from pathlib import Path

    from logic_mix_os.project import load_manifest

    root = Path(__file__).resolve().parent.parent
    real = pipeline.analyze_groove
    counter = {"n": 0}

    def _spy(rhythm_tracks):
        counter["n"] += 1
        return real(rhythm_tracks)

    monkeypatch.setattr(pipeline, "analyze_groove", _spy)
    manifest = load_manifest(root / "fixtures" / "dense_chorus_with_loops" / "project_manifest.json")
    res = pipeline.analyze(str(root / "fixtures" / "dense_chorus_with_loops" / "stems"), manifest)
    return res, counter


def test_analyze_groove_called_exactly_once(monkeypatch):
    """THE COMPUTE-ONCE GUARD: a full ``analyze()`` invokes ``analyze_groove``
    EXACTLY ONCE. A second call (computing it both before doctrine AND again for
    ``expanded``) is the live-wire being wrong — this catches it."""
    _res, counter = _analyze_dense_with_groove_spy(monkeypatch)
    assert counter["n"] == 1


def test_score_doctrine_receives_the_real_groove(monkeypatch):
    """The real groove reaches doctrine: ``dense_chorus_with_loops`` has a real
    ``overall_regularity`` (~0.989), so its ``groove_coherence_score`` must reflect
    that real value — NOT the None-fallback. If the threading were broken (groove
    not passed, or passed as None), the score would collapse to the neutral
    fallback and this assertion would fail."""
    res, _counter = _analyze_dense_with_groove_spy(monkeypatch)

    # The real signal is present on this fixture.
    assert res.expanded["groove"]["overall_regularity"] is not None

    doctrine = load_profile("halee_ramone").doctrine
    fallback, _ = doctrine_engine._groove_coherence(None, doctrine)
    real_expected, _ = doctrine_engine._groove_coherence(res.expanded["groove"], doctrine)

    gc = res.doctrine_score["groove_coherence_score"]
    assert gc == real_expected
    # A tight groove (regularity ~0.99) scores well ABOVE the None-fallback, so
    # the "real groove reached doctrine" claim is load-bearing, not vacuous.
    assert gc != fallback
    assert gc > fallback


# --------------------------------------------------------------------------- #
# 3. VALUE-DISCRIMINATION (unit) — the scorer measures groove regularity.
# --------------------------------------------------------------------------- #
def test_coherent_groove_scores_high():
    """A coherent, regular groove (high ``overall_regularity``) scores HIGH."""
    doctrine = load_profile("halee_ramone").doctrine
    score, ev = doctrine_engine._groove_coherence(_groove(0.95), doctrine)
    assert score >= 75.0
    assert any("regular" in e.lower() or "consist" in e.lower() for e in ev)


def test_incoherent_groove_scores_low():
    """An incoherent, loose groove (low ``overall_regularity``) scores LOW —
    below a coherent one. (Honest naming: this is regularity, not a value
    judgement; a producer decides whether low regularity is desirable.)"""
    doctrine = load_profile("halee_ramone").doctrine
    coherent, _ = doctrine_engine._groove_coherence(_groove(0.95), doctrine)
    incoherent, _ = doctrine_engine._groove_coherence(_groove(0.15), doctrine)
    assert incoherent < coherent


def test_none_overall_regularity_uses_neutral_fallback():
    """``overall_regularity is None`` (no rhythm stems) => a documented NEUTRAL
    fallback float (never None, never a crash)."""
    doctrine = load_profile("halee_ramone").doctrine
    neutral = doctrine["scorers"]["groove_coherence"]["neutral"]
    score, ev = doctrine_engine._groove_coherence(_groove(None), doctrine)
    assert score == doctrine_engine._clamp(neutral)
    assert any("no" in e.lower() or "neutral" in e.lower() for e in ev)


def test_groove_none_object_uses_neutral_fallback():
    """A completely absent groove (``groove is None``, i.e. the backward-compat
    default of ``score_doctrine``) => the same neutral fallback, never a crash."""
    doctrine = load_profile("halee_ramone").doctrine
    neutral = doctrine["scorers"]["groove_coherence"]["neutral"]
    score, ev = doctrine_engine._groove_coherence(None, doctrine)
    assert score == doctrine_engine._clamp(neutral)


def test_neutral_fallback_sits_between_coherent_and_incoherent():
    """The None/absent neutral fallback is a deliberate mid value — it does NOT
    reward absence as coherence, nor punish it as maximal incoherence."""
    doctrine = load_profile("halee_ramone").doctrine
    coherent, _ = doctrine_engine._groove_coherence(_groove(0.95), doctrine)
    neutral, _ = doctrine_engine._groove_coherence(_groove(None), doctrine)
    incoherent, _ = doctrine_engine._groove_coherence(_groove(0.0), doctrine)
    assert incoherent < neutral < coherent


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 value."""
    doctrine = load_profile("halee_ramone").doctrine
    for reg in (None, 0.0, 0.5, 1.0):
        score, _ = doctrine_engine._groove_coherence(_groove(reg), doctrine)
        assert 0.0 <= score <= 100.0


def test_does_not_bake_in_tighter_is_better_language():
    """Honest-naming guard: the evidence names REGULARITY/CONSISTENCY, and never
    asserts that a tighter groove is objectively 'better'. The agnostic layer
    reports the feel; the producer decides how to weight it."""
    doctrine = load_profile("halee_ramone").doctrine
    _, ev = doctrine_engine._groove_coherence(_groove(0.95), doctrine)
    blob = " ".join(ev).lower()
    assert "better" not in blob


# --------------------------------------------------------------------------- #
# 4. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and breaking the threading (groove=None) must fail liveness + no-re-run.
# --------------------------------------------------------------------------- #
def _profile_weighting_groove_coherence(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero groove_coherence weight
    — so any overall delta is attributable to the groove_coherence term alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["groove_coherence_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    groove_coherence non-zero changes the overall vs the weight-0 reference. This
    is LIVE-WIRE proof: the term is genuinely threaded (with the real groove), not
    decorative.

    Sabotage that this test catches: passing ``groove=None`` into
    ``score_doctrine`` (breaking the threading) collapses groove_coherence to the
    neutral fallback; passing the real groove but hardcoding the scorer, or
    dropping it from ``component_scores``, collapses the weighted mean back onto
    the reference — either way this assertion behaves differently."""
    res = analyzed["dense_chorus_with_loops"]
    groove = res.expanded["groove"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_groove_coherence(3.0), groove=groove
    )

    gc = reference["groove_coherence_score"]
    assert gc is not None and 0.0 <= gc <= 100.0
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_groove_coherence_score(analyzed):
    """The direction the overall moves under a non-zero weight must be consistent
    with groove_coherence's value relative to the other components."""
    res = analyzed["dense_chorus_with_loops"]
    groove = res.expanded["groove"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    gc = reference["groove_coherence_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_groove_coherence(5.0), groove=groove
    )
    new_overall = weighted["overall_mix_readiness_score"]

    if gc > ref_overall:
        assert new_overall > ref_overall
    elif gc < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


def test_sabotage_breaking_threading_collapses_to_fallback(analyzed):
    """THE SABOTAGE GUARD: passing ``groove=None`` (i.e. failing to thread the
    real groove into doctrine) collapses groove_coherence to the neutral fallback.
    On ``dense_chorus_with_loops`` (real regularity ~0.989 → HIGH) that is a
    STRICTLY DIFFERENT number, so a broken live-wire is detectable here even at
    weight 0. This is what makes the threading load-bearing rather than cosmetic."""
    res = analyzed["dense_chorus_with_loops"]
    groove = res.expanded["groove"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)

    threaded = doctrine_engine.score_doctrine(*base_args, groove=groove)
    sabotaged = doctrine_engine.score_doctrine(*base_args, groove=None)

    doctrine = load_profile("halee_ramone").doctrine
    fallback, _ = doctrine_engine._groove_coherence(None, doctrine)

    assert threaded["groove_coherence_score"] != sabotaged["groove_coherence_score"]
    assert sabotaged["groove_coherence_score"] == fallback
    assert threaded["groove_coherence_score"] > fallback


# --------------------------------------------------------------------------- #
# 5. NO-ALIASING — the scorer only reads ``doctrine[...]``/``groove[...]``; it
#    never mutates the shared profile structures or the groove dict.
# --------------------------------------------------------------------------- #
def test_groove_coherence_does_not_mutate_the_profile_or_groove():
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    groove = _groove(0.9, per_track=[{"track": "Kick", "regularity": 0.9}])
    groove_before = copy.deepcopy(groove)
    doctrine_engine._groove_coherence(groove, doctrine)
    assert doctrine == doctrine_before
    assert groove == groove_before


def test_score_doctrine_with_groove_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` (threading the real groove) on a real fixture and assert the
    shared default doctrine is byte-unchanged (its ``scorers.groove_coherence``
    block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "groove_coherence" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
