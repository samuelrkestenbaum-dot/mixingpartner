"""P-032g — the binding guards for ``loop_context``, the SIXTH new
producer-agnostic doctrine axis: loop static-vs-iconic — THE HINGE.

THE DOCTRINE PIN (user-issued architecture doctrine, 2026-07-01): **the engine
DETECTS agnostically; the profile DECIDES.** This axis is its exemplar — the
central philosophical reversal of the producer-profile framework. A dominating
loop is a POTENTIAL SIGNAL, not a verdict: one profile may treat it as a
liability to deconstruct, another as the very identity of the record to
protect. The reversal lives in profile JSON, never in engine code, so the
engine's reading here is strictly OBSERVATIONAL:

* dominant loop + no sectional evolution around it  = **static**
* dominant loop + groove/fingerprint FUNCTION       = **iconic**

ZERO JUDGMENT WORDS (USER-MANDATED): the scorer/evidence never says "bad",
"problem", "should", or "fix" — it reports what IS. The profile decides
deconstruct-vs-protect (the creative gate is Commit-2 of this packet).

HONEST SCOPE — "iconic" is an ACOUSTIC PROXY: measurable groove-carrying
function (transient character + envelope definition + heard/unmasked while the
mix evolves around the loop). It is NOT cultural recognizability — that is
provenance/manifest territory and is explicitly deferred, never faked.

It is wired at weight 0 for ``halee_ramone`` so the reference producer's
output stays BYTE-IDENTICAL (the FIRST of the packet's TWO byte-identity
surfaces; the creative surface is Commit-2's).

Five guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default
   halee_ramone) leaves every PRE-EXISTING component score (now 12, incl.
   ``low_end_motion_score``) AND ``overall_mix_readiness_score`` unchanged vs
   the pinned base, and the golden regression still reports 68/68.
2. **Value-discrimination (unit)** — a static-dominating loop (dominant + no
   sectional evolution) → LOW; an iconic-functioning loop (dominant +
   groove-carrying + heard/unmasked + evolution around it) → HIGH; no loop →
   the documented neutral; plus the ambiguous mid readings.
3. **Observational-language guard** — the evidence contains ZERO judgment
   words (the ``test_groove_coherence`` "tighter is better" guard idiom,
   applied to the user's banned list).
4. **Liveness (load-bearing)** — a profile weighting ``loop_context_score``
   non-zero CHANGES ``analyze()``'s overall on a fixture; a sabotage
   (hardcoding the term / dropping it from ``component_scores``) FAILS that
   liveness while byte-identical stays green (P-016/P-029).
5. **No-aliasing** — the scorer only reads ``doctrine[...]`` / ``records[...]``
   / ``sections[...]`` / ``masking_report[...]``; it never mutates the shared
   profile structures or the input dicts.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The twelve pre-existing component score keys (the byte-identical anchor set):
# the seven original components + beat_identity_score (P-032e) +
# negative_space_score (P-032a) + groove_coherence_score (P-032b) +
# rhythmic_surprise_score (P-032d) + low_end_motion_score (P-032c).
# loop_context_score is appended after these.
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
    "rhythmic_surprise_score",
    "low_end_motion_score",
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned BASE values captured from the tree at P-032g's base (`6af00fa`,
# before this packet): every pre-existing component score + overall. The axis
# add must leave all of these byte-unchanged.
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
        "rhythmic_surprise_score": 51.1,
        "low_end_motion_score": 60.0,
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
        "rhythmic_surprise_score": 20.0,
        "low_end_motion_score": 21.1,
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
        "rhythmic_surprise_score": 27.8,
        "low_end_motion_score": 25.0,
        "overall_mix_readiness_score": 74.3,
    },
}

# The user's banned judgment vocabulary — the engine reads, it never rules.
JUDGMENT_WORDS = ("bad", "problem", "should", "fix", "better", "worse", "wrong")


# --------------------------------------------------------------------------- #
# Test helpers — synthetic records/sections/events for the unit guards.
# --------------------------------------------------------------------------- #
def _rec(name: str, source_kind: str = "live_audio_recording",
         depth: str = "midground", width: float = 0.2, role: str = "heard",
         td: float = 0.5, crest: float = 15.0) -> dict:
    """A synthetic per-track record shaped like the pipeline's. The loop-context
    read uses ``source_kind`` (loop presence), ``depth_default`` /
    ``stereo_width`` / ``metrics.transient_density`` (dominance), and
    ``metrics.crest_factor_db`` / ``perceptual_role`` (the iconic read)."""
    return {
        "track_id": name.lower().replace(" ", "_"),
        "name": name,
        "instrument_identity": "unknown",
        "identity_family": "unknown",
        "perceptual_role": role,
        "sacredness": "supportive",
        "source_kind": source_kind,
        "depth_default": depth,
        "depth_by_section": {},
        "stereo_width": width,
        "metrics": {
            "transient_density": td,
            "crest_factor_db": crest,
        },
    }


def _sections(evolving: bool) -> list:
    """Three sections whose ONLY difference is sectional movement: the evolving
    variant's RMS spread clears the evolution floor; the static variant's
    spreads all sit under the floors."""
    rms = [-16.0, -9.0, -12.0] if evolving else [-12.0, -11.9, -12.1]
    return [
        {"metrics": {"rms_dbfs": r, "width": 0.30, "brightness": 0.40},
         "contrast_vs_previous": {}}
        for r in rms
    ]


def _bed() -> list:
    """A non-loop bed the loop is judged against."""
    return [
        _rec("Lead Vocal", depth="intimate", width=0.0, role="heard", td=0.4, crest=9.0),
        _rec("Pad", depth="background", width=0.4, role="felt", td=0.2, crest=10.0),
        _rec("Bass", depth="foreground", width=0.0, role="structural", td=0.3, crest=11.0),
    ]


def _iconic_loop() -> dict:
    """A loop with every groove-function property: dominant (foregrounded, wide,
    transient lift over the bed), punchy and defined, heard and unmasked."""
    return _rec("Chop Loop", source_kind="splice_sample", depth="foreground",
                width=0.7, role="heard", td=0.9, crest=18.0)


def _masking(loop_name: str) -> list:
    return [{
        "elements": [loop_name, "Lead Vocal"],
        "classification": "bad_masking",
        "severity": "critical",
        "section": "chorus_1",
    }]


def _lc(records, sections=None, events=None, doctrine=None):
    doctrine = doctrine or load_profile("halee_ramone").doctrine
    return doctrine_engine._loop_context(
        records, sections if sections is not None else [],
        {"events": events or []}, doctrine,
    )


def _read(records, sections=None, events=None):
    c = load_profile("halee_ramone").doctrine["scorers"]["loop_context"]
    return doctrine_engine.read_loop_context(
        records, sections if sections is not None else [], events or [], c,
    )


def _constants():
    return load_profile("halee_ramone").doctrine["scorers"]["loop_context"]


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged.
# --------------------------------------------------------------------------- #
def test_loop_context_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``lc*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["loop_context_score"] == 0


def test_loop_context_appended_last_preserves_summation_order(analyzed):
    """The new term is LAST in ``component_scores`` and every PRE-EXISTING key
    (the 12 anchors) keeps its exact value + position."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[:12] == EXISTING_COMPONENT_KEYS
        # P-032f appended vocal_role_fit_score after this axis, so the anchor
        # is positional (index 12), no longer the tail.
        assert keys[12] == "loop_context_score"


def test_every_preexisting_component_score_is_byte_identical(analyzed):
    """Every one of the twelve pre-existing component scores + the overall
    equals the pinned base value on all three fixtures — the axis add did not
    move any existing number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_overall_is_byte_identical_to_twelve_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the twelve
    pre-existing components (loop_context excluded) equals the pipeline's
    overall — proof the weight-0 new term did not move the number."""
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


def test_live_fixture_context_readings(analyzed):
    """The informational live readings (weight 0, so inert for halee_ramone):
    the loop-less fixture reads neutral; BOTH loop fixtures read STATIC — a
    dominant loop (wide + transient lift over the bed) with no sectional
    evolution around it. The evidence key is present and non-empty."""
    c = _constants()
    expected = {
        "simple_vocal_piano_song": doctrine_engine._clamp(c["no_loop"]),
        "dense_chorus_with_loops": doctrine_engine._clamp(c["static"]),
        "splice_loop_problem": doctrine_engine._clamp(c["static"]),
    }
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        assert ds["loop_context_score"] == expected[name]
        ev = ds["evidence"]["loop_context"]
        assert isinstance(ev, list) and ev


# --------------------------------------------------------------------------- #
# 2. VALUE-DISCRIMINATION (unit) — static-dominating LOW; iconic-functioning
#    HIGH; no loop neutral; ambiguity in the middle.
# --------------------------------------------------------------------------- #
def test_static_dominating_loop_scores_low():
    """THE STATIC READ: a dominant loop with no sectional evolution around it
    reads static and scores LOW — whatever its groove character (dominance +
    no movement IS the static definition; the mandate's first clause)."""
    c = _constants()
    score, ev = _lc(_bed() + [_iconic_loop()], sections=_sections(evolving=False))
    assert score == doctrine_engine._clamp(c["static"])
    assert score <= 25.0
    assert any("static" in e.lower() for e in ev)


def test_iconic_functioning_loop_scores_high():
    """THE ICONIC READ: the same dominant loop — groove-carrying transients,
    defined hits, heard and unmasked — with the mix EVOLVING around it reads
    iconic and scores HIGH."""
    c = _constants()
    score, ev = _lc(_bed() + [_iconic_loop()], sections=_sections(evolving=True))
    assert score == doctrine_engine._clamp(c["iconic"])
    assert score >= 80.0
    assert any("iconic" in e.lower() for e in ev)
    assert any("acoustic proxy" in e.lower() for e in ev)


def test_evolution_is_the_hinge_between_static_and_iconic():
    """The ONLY difference between the two mixes is sectional evolution; the
    reading flips from LOW to HIGH. This is the axis's central discrimination."""
    static_score, _ = _lc(_bed() + [_iconic_loop()], sections=_sections(evolving=False))
    iconic_score, _ = _lc(_bed() + [_iconic_loop()], sections=_sections(evolving=True))
    assert static_score < iconic_score
    assert iconic_score - static_score >= 50.0


def test_no_loop_returns_documented_neutral():
    """No imported loop/sample material => the documented ``no_loop`` neutral
    float. Never None, never a crash — and sectional evolution alone cannot
    move it (see the distinctness guard below)."""
    c = _constants()
    score, ev = _lc(_bed(), sections=_sections(evolving=True))
    assert score == doctrine_engine._clamp(c["no_loop"])
    assert any("no imported loop" in e.lower() for e in ev)


def test_distinctness_sectional_evolution_alone_never_moves_this_axis():
    """THE DISTINCTNESS GUARD vs ``_dynamic_mix`` / ``_rhythmic_surprise`` /
    ``_section_contrast``: those axes SCORE sectional movement itself. Here
    evolution is a context INPUT for interpreting the LOOP only — with no loop
    present, evolving vs static sections produce the IDENTICAL neutral, so the
    axis cannot be a re-derivation of any movement axis."""
    evolving_score, _ = _lc(_bed(), sections=_sections(evolving=True))
    static_score, _ = _lc(_bed(), sections=_sections(evolving=False))
    assert evolving_score == static_score


def test_non_dominant_loop_reads_ambiguous_neutral():
    """A loop that sits IN the bed — not foregrounded, narrow, no transient
    lift over the bed — is not dominant: neither static nor iconic applies."""
    c = _constants()
    quiet_loop = _rec("Bed Loop", source_kind="apple_loop", depth="background",
                      width=0.3, role="felt", td=0.3, crest=10.0)
    bed = [
        _rec("Lead Vocal", depth="intimate", width=0.0, td=0.4, crest=9.0),
        _rec("Guitar", depth="foreground", width=0.3, td=0.5, crest=18.0),
        _rec("Bass", depth="foreground", width=0.0, role="structural", td=0.3, crest=11.0),
    ]
    score, ev = _lc(bed + [quiet_loop], sections=_sections(evolving=True))
    assert score == doctrine_engine._clamp(c["not_dominant"])
    status, _ = _read(bed + [quiet_loop], sections=_sections(evolving=True))
    assert status == "not_dominant"


def test_each_dominance_signal_alone_qualifies():
    """Dominance is honest physics, any one signal suffices: foregrounded
    (depth), wide (stereo field), or transient lift above the bed (punch)."""
    bed = [
        _rec("Lead Vocal", depth="intimate", width=0.0, td=0.4, crest=9.0),
        _rec("Guitar", depth="foreground", width=0.3, td=0.5, crest=18.0),
        _rec("Bass", depth="foreground", width=0.0, role="structural", td=0.3, crest=11.0),
    ]
    fore_only = _rec("Loop", source_kind="splice_sample", depth="foreground",
                     width=0.2, role="felt", td=0.3, crest=8.0)
    wide_only = _rec("Loop", source_kind="splice_sample", depth="background",
                     width=0.8, role="felt", td=0.3, crest=8.0)
    punch_only = _rec("Loop", source_kind="splice_sample", depth="background",
                      width=0.2, role="felt", td=0.95, crest=8.0)
    for loop in (fore_only, wide_only, punch_only):
        status, facts = _read(bed + [loop], sections=_sections(evolving=False))
        assert status == "static", facts


def test_dominant_loop_with_unassessable_evolution_reads_ambiguous():
    """Fewer than two sections with metrics: evolution around the loop cannot
    be assessed — the documented ambiguous fallback, never a guess."""
    c = _constants()
    score, ev = _lc(_bed() + [_iconic_loop()], sections=[])
    assert score == doctrine_engine._clamp(c["dominant_unassessed"])
    assert any("cannot be assessed" in e.lower() for e in ev)


def test_dominant_evolving_loop_without_groove_function_is_ambiguous():
    """Dominant + evolution but NO groove-carrying read (smeared envelope,
    felt not heard) => the ambiguous mid reading, not iconic."""
    c = _constants()
    smeared = _rec("Texture Loop", source_kind="texture_loop", depth="foreground",
                   width=0.7, role="felt", td=0.9, crest=7.0)
    score, ev = _lc(_bed() + [smeared], sections=_sections(evolving=True))
    assert score == doctrine_engine._clamp(c["dominant_evolving"])
    assert score < doctrine_engine._clamp(c["iconic"])
    status, _ = _read(_bed() + [smeared], sections=_sections(evolving=True))
    assert status == "dominant_evolving"


def test_masked_loop_cannot_read_iconic():
    """The iconic read requires the loop to be HEARD: a bad-masked loop —
    otherwise identical to the iconic case — falls back to the ambiguous
    reading. (Groove-carrying function you cannot hear is not a fingerprint.)"""
    loop = _iconic_loop()
    records = _bed() + [loop]
    unmasked, _ = _lc(records, sections=_sections(evolving=True))
    masked, _ = _lc(records, sections=_sections(evolving=True),
                    events=_masking(loop["name"]))
    c = _constants()
    assert unmasked == doctrine_engine._clamp(c["iconic"])
    assert masked == doctrine_engine._clamp(c["dominant_evolving"])
    assert masked < unmasked


def test_felt_role_loop_cannot_read_iconic():
    """Same gate from the perceptual side: a felt (not heard/structural) loop
    does not read iconic even with groove-carrying transients."""
    felt = _rec("Chop Loop", source_kind="splice_sample", depth="foreground",
                width=0.7, role="felt", td=0.9, crest=18.0)
    score, _ = _lc(_bed() + [felt], sections=_sections(evolving=True))
    c = _constants()
    assert score == doctrine_engine._clamp(c["dominant_evolving"])


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 float."""
    cases = [
        ([], None, None),
        (_bed(), _sections(True), None),
        (_bed() + [_iconic_loop()], _sections(True), None),
        (_bed() + [_iconic_loop()], _sections(False), None),
        (_bed() + [_iconic_loop()], [], _masking("Chop Loop")),
        ([_iconic_loop()], _sections(True), _masking("Chop Loop")),
    ]
    for records, sections, events in cases:
        score, _ = _lc(records, sections=sections, events=events)
        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0


def test_honest_deferrals_stated_in_docstring_never_claimed_in_evidence():
    """THE HONESTY GATE: the docstring states the deferrals — CULTURAL
    RECOGNIZABILITY (provenance/manifest territory, not audio), per-loop
    BAR-LEVEL variation and anything needing an onset sequence (post-doctrine
    groove territory) — and the evidence never claims any of them. 'Iconic' is
    named as an acoustic proxy for groove-carrying FUNCTION only."""
    doc = (doctrine_engine._loop_context.__doc__ or "").lower()
    assert "cultural" in doc
    assert "recognizab" in doc
    assert "bar-level" in doc
    assert "provenance" in doc
    assert "acoustic proxy" in doc

    for records, sections, events in (
        (_bed() + [_iconic_loop()], _sections(True), None),
        (_bed() + [_iconic_loop()], _sections(False), None),
        (_bed(), _sections(True), None),
    ):
        _, ev = _lc(records, sections=sections, events=events)
        blob = " ".join(ev).lower()
        for claim in ("cultural", "recognizab", "bar-level", "recogniz"):
            assert claim not in blob


# --------------------------------------------------------------------------- #
# 3. OBSERVATIONAL-LANGUAGE GUARD (USER-MANDATED) — zero judgment words in the
#    engine's evidence, across EVERY status the axis can emit and on the live
#    fixtures. The profile decides; the engine only reads.
# --------------------------------------------------------------------------- #
def _all_status_evidence():
    """Evidence lists covering every reachable status."""
    out = []
    out.append(_lc(_bed(), sections=_sections(True))[1])                      # no_loop
    quiet = _rec("Bed Loop", source_kind="apple_loop", depth="background",
                 width=0.3, role="felt", td=0.3, crest=10.0)
    bed = [
        _rec("Lead Vocal", depth="intimate", width=0.0, td=0.4, crest=9.0),
        _rec("Guitar", depth="foreground", width=0.3, td=0.5, crest=18.0),
        _rec("Bass", depth="foreground", width=0.0, role="structural", td=0.3, crest=11.0),
    ]
    out.append(_lc(bed + [quiet], sections=_sections(True))[1])              # not_dominant
    out.append(_lc(_bed() + [_iconic_loop()], sections=[])[1])               # dominant_unassessed
    out.append(_lc(_bed() + [_iconic_loop()], sections=_sections(False))[1])  # static
    out.append(_lc(_bed() + [_iconic_loop()], sections=_sections(True))[1])  # iconic
    smeared = _rec("Texture Loop", source_kind="texture_loop", depth="foreground",
                   width=0.7, role="felt", td=0.9, crest=7.0)
    out.append(_lc(_bed() + [smeared], sections=_sections(True))[1])         # dominant_evolving
    out.append(_lc(_bed() + [_iconic_loop()], sections=_sections(True),
                   events=_masking("Chop Loop"))[1])                          # masked ambiguous
    return out


def test_engine_language_is_observational_zero_judgment_words():
    """USER-MANDATED: the engine says static/iconic/dominant — never 'bad',
    'problem', 'should', 'fix' (nor better/worse/wrong). Mirrors the
    ``test_groove_coherence`` "tighter is better" guard idiom, applied to the
    full banned list across every status the axis can emit."""
    for ev in _all_status_evidence():
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in evidence: {blob}"


def test_live_fixture_evidence_is_observational(analyzed):
    """The same zero-judgment guard on the REAL pipeline evidence for all three
    fixtures (two of which read static-dominating)."""
    for name in FIXTURE_NAMES:
        ev = analyzed[name].doctrine_score["evidence"]["loop_context"]
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in {name}: {blob}"


# --------------------------------------------------------------------------- #
# 4. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and a sabotage of the scorer must break these tests (P-016/P-029).
# --------------------------------------------------------------------------- #
def _profile_weighting_loop_context(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero loop_context weight
    — so any overall delta is attributable to the loop_context term alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["loop_context_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    loop_context non-zero changes the overall vs the weight-0 reference.
    This is LIVE-WIRE proof: the term is genuinely threaded, not decorative.

    Sabotage this catches: dropping ``loop_context_score`` from
    ``component_scores`` collapses the weighted mean back onto the reference
    and this assertion FAILS — while byte-identical stays green."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_loop_context(3.0), groove=groove
    )

    lc = reference["loop_context_score"]
    assert lc is not None and 0.0 <= lc <= 100.0
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_loop_context_score(analyzed):
    """A sharper sabotage guard: the direction the overall moves under a
    non-zero weight must be consistent with loop_context's value relative to
    the other components. A hardcoded term would not track the real score and
    this assertion would break."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    lc = reference["loop_context_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_loop_context(5.0), groove=groove
    )
    new_overall = weighted["overall_mix_readiness_score"]

    if lc > ref_overall:
        assert new_overall > ref_overall
    elif lc < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


def test_weighted_iconic_vs_static_move_the_overall_in_opposite_directions():
    """The hinge is a genuine LEVER, not a constant: under the SAME non-zero
    weight, the same project scores a HIGHER overall when its loop reads
    iconic than when it reads static. (A hardcoded scorer could not produce
    the gap.)"""
    profile = _profile_weighting_loop_context(5.0)
    records = _bed() + [_iconic_loop()]
    masking = {"events": []}
    static = doctrine_engine.score_doctrine(
        records, _sections(evolving=False), masking, None, profile=profile)
    iconic = doctrine_engine.score_doctrine(
        records, _sections(evolving=True), masking, None, profile=profile)
    assert iconic["loop_context_score"] > static["loop_context_score"]
    assert iconic["overall_mix_readiness_score"] > static["overall_mix_readiness_score"]


# --------------------------------------------------------------------------- #
# 5. NO-ALIASING — the scorer only reads its inputs; it never mutates the
#    shared profile structures, the records, the sections or the masking
#    report.
# --------------------------------------------------------------------------- #
def test_loop_context_does_not_mutate_profile_records_sections_or_masking():
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    records = _bed() + [_iconic_loop()]
    records_before = copy.deepcopy(records)
    sections = _sections(evolving=True)
    sections_before = copy.deepcopy(sections)
    masking_report = {"events": _masking("Chop Loop")}
    masking_before = copy.deepcopy(masking_report)
    doctrine_engine._loop_context(records, sections, masking_report, doctrine)
    assert doctrine == doctrine_before
    assert records == records_before
    assert sections == sections_before
    assert masking_report == masking_before


def test_score_doctrine_with_loop_context_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` on a real fixture and assert the shared default doctrine
    is byte-unchanged (its ``scorers.loop_context`` block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "loop_context" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
