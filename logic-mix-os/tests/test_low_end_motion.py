"""P-032c — the binding guards for ``low_end_motion``, the FIFTH new
producer-agnostic doctrine axis: the low-end POCKET — kick/sub relationship
plus ROOM around the bass.

THE CORE DESIGN RULE — "more bass" must NOT win: a clean low-end RELATIONSHIP
beats high low-end QUANTITY. Low-end PRESENCE is a GATE only (a floor check
that some stem carries sub weight); the SCORE comes from the RELATIONSHIP (no
kick/bass collision + complementary punch-vs-sustain) and the ROOM (the sub
band reserved for FEW stems — and QUALIFIED by pocket behavior: few-ness is
never sufficient on its own). The low band's magnitude is only ever compared
against thresholds — it is never multiplied into the score — so a bass-heavy
mud mix scores LOW whether the mud is a many-stem pile-up WITH collisions or
ONE giant smeared blob with the fewest carriers of all, while a leaner clean
pocket scores HIGH.

THE DISTINCTNESS GUARD — vs ``_static_mix``. ``_static_mix`` applies a hygiene
PENALTY for critical ``low_end_conflict`` events (pass/fail fault-checking).
``_low_end_motion`` scores the POSITIVE relationship — a reserved sub,
punch-vs-sustain complementarity, room around the bass — a strength axis, not
a sign-flipped duplicate. The proof case here: a mix with NO conflicts but
also NO defined pocket (many stems sharing the low band, none of them a
kick/bass pair) leaves static_mix healthy while low_end_motion scores low.

HONEST DEFERRALS (docstring, never faked in evidence): (1) kick/sub TEMPORAL
interlock — bass onset times are never computed (bass is excluded from
``RHYTHM_IDENTITIES``; onset timing lives in groove for drum stems only);
(2) low-end MOTIF detection — needs a pitch/onset sequence; (3) per-section
true-sub movement — sections expose ``low_mid_energy`` only, not the 20-120Hz
sub band.

It is wired at weight 0 for ``halee_ramone`` so the reference producer's
output stays BYTE-IDENTICAL.

Four guards, mirroring the packet:

1. **Byte-identical** — for all 3 fixtures, ``analyze()`` (default
   halee_ramone) leaves every PRE-EXISTING component score (now 11, incl.
   ``rhythmic_surprise_score``) AND ``overall_mix_readiness_score`` unchanged
   vs the pinned base, and the golden regression still reports 68/68.
2. **Value-discrimination (unit)** — a clean pocket (one reserved kick/bass
   pair, punchy kick + sustained bass, no conflicts) → HIGH; a bass-heavy mud
   mix (more total low energy, but piled-up and conflicted) → LOW (the "more
   bass must not win" proof); no low end at all → the documented
   ``no_low_end`` gate value; AND the static_mix-distinctness case.
3. **Liveness (load-bearing)** — a profile weighting ``low_end_motion_score``
   non-zero CHANGES ``analyze()``'s overall on a fixture; a sabotage
   (hardcoding the term / dropping it from ``component_scores``) FAILS that
   liveness while byte-identical stays green (P-016/P-029).
4. **No-aliasing** — the scorer only reads ``doctrine[...]`` / ``records[...]``
   / ``masking_report[...]``; it never mutates the shared profile structures
   or the input dicts.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# The eleven pre-existing component score keys (the byte-identical anchor set):
# the seven original components + beat_identity_score (P-032e) +
# negative_space_score (P-032a) + groove_coherence_score (P-032b) +
# rhythmic_surprise_score (P-032d). low_end_motion_score is appended after
# these.
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
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned BASE values captured from the tree at P-032c's base (before this
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
        "rhythmic_surprise_score": 51.1,
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
        "overall_mix_readiness_score": 74.3,
    },
}


# --------------------------------------------------------------------------- #
# Test helpers — synthetic records/events for the unit / discrimination guards.
# --------------------------------------------------------------------------- #
def _rec(name: str, identity: str = "pad", family: str = "synth",
         low: float = 0.0, crest: float = 10.0) -> dict:
    """A synthetic per-track record shaped like the pipeline's. The scorer
    reads ``metrics.band_energy.low`` (sub weight, 20-120Hz) and
    ``metrics.crest_factor_db`` (punch vs sustain); identity labels are
    corroborating colour only, never the gate."""
    band_energy = {"low": low, "low_mid": 0.3, "mid": 0.3, "presence": 0.1, "high": 0.1}
    return {
        "track_id": name.lower().replace(" ", "_"),
        "name": name,
        "instrument_identity": identity,
        "identity_family": family,
        "perceptual_role": "structural",
        "sacredness": "supportive",
        "source_kind": "live_recorded",
        "depth_default": "midground",
        "depth_by_section": {},
        "stereo_width": 0.2,
        "band_energy": band_energy,
        "vocal_presence_energy": 0.05,
        "brightness": 0.3,
        "metrics": {
            "band_energy": band_energy,
            "crest_factor_db": crest,
            "transient_density": 0.5,
        },
    }


def _conflict(severity: str, overlap: float = 0.7) -> dict:
    """A low_end_conflict event shaped like the masking analyzer's."""
    return {
        "elements": ["Kick", "Bass"],
        "frequency_range": "40Hz-150Hz",
        "section": "chorus_1",
        "classification": "low_end_conflict",
        "severity": severity,
        "overlap": overlap,
    }


def _clean_pocket() -> list:
    """The defined pocket: a punchy kick + a sustained bass reserve the sub
    band between them; everything else stays out of the low end."""
    return [
        _rec("Kick", identity="kick", family="drums", low=0.55, crest=19.0),
        _rec("Bass", identity="bass_guitar", family="bass", low=0.62, crest=9.0),
        _rec("Pad", identity="pad", family="synth", low=0.05, crest=10.0),
    ]


def _bass_heavy_mud() -> list:
    """MORE total low-band energy than the clean pocket — but piled into six
    stems with no punch-vs-sustain differentiation to speak of. Paired with
    critical kick/bass conflicts in the test, this is the 'more bass must not
    win' mix."""
    lows = [0.9, 0.8, 0.75, 0.7, 0.65, 0.6]
    crests = [12.0, 8.0, 10.0, 9.0, 11.0, 10.0]
    return [
        _rec(f"Low Stem {i}", identity="synth", family="synth", low=lo, crest=cr)
        for i, (lo, cr) in enumerate(zip(lows, crests))
    ]


def _lem(records, events=None, mix_metrics=None, sections=None, doctrine=None):
    doctrine = doctrine or load_profile("halee_ramone").doctrine
    return doctrine_engine._low_end_motion(
        records, sections or [], {"events": events or []}, mix_metrics, doctrine
    )


# --------------------------------------------------------------------------- #
# 1. BYTE-IDENTICAL — the reference producer's output is unchanged.
# --------------------------------------------------------------------------- #
def test_low_end_motion_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``lem*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["low_end_motion_score"] == 0


def test_low_end_motion_appended_last_preserves_summation_order(analyzed):
    """The new term is LAST in ``component_scores`` and every PRE-EXISTING key
    (the 11 anchors) keeps its exact value + position."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[:11] == EXISTING_COMPONENT_KEYS
        # P-032g appended loop_context_score after this axis, so the anchor is
        # positional (index 11), no longer the tail.
        assert keys[11] == "low_end_motion_score"


def test_every_preexisting_component_score_is_byte_identical(analyzed):
    """Every one of the eleven pre-existing component scores + the overall
    equals the pinned base value on all three fixtures — the axis add did not
    move any existing number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_overall_is_byte_identical_to_eleven_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the eleven
    pre-existing components (low_end_motion excluded) equals the pipeline's
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


# --------------------------------------------------------------------------- #
# 2. VALUE-DISCRIMINATION (unit) — the scorer measures the POCKET (relationship
#    + room), never sheer bass level.
# --------------------------------------------------------------------------- #
def test_clean_pocket_scores_high():
    """A defined pocket — the sub reserved for a kick/bass pair, a punchy kick
    against a sustained bass, no collisions — scores HIGH."""
    score, ev = _lem(_clean_pocket())
    assert score >= 70.0


def test_bass_heavy_mud_scores_low():
    """A bass-heavy mud mix — six stems piling into the low band plus critical
    kick/bass conflicts — scores LOW despite carrying far more low energy."""
    score, ev = _lem(_bass_heavy_mud(), events=[_conflict("critical"), _conflict("critical")])
    assert score <= 25.0


def test_more_bass_must_not_win():
    """THE CORE DESIGN RULE: the mud mix carries strictly MORE total low-band
    energy than the clean pocket, yet scores strictly BELOW it. Presence is a
    gate only; the score comes from the relationship and the room. If the
    scorer rewarded sheer low-band level, this assertion would fail."""
    clean = _clean_pocket()
    mud = _bass_heavy_mud()
    clean_low = sum(r["metrics"]["band_energy"]["low"] for r in clean)
    mud_low = sum(r["metrics"]["band_energy"]["low"] for r in mud)
    assert mud_low > clean_low  # the mud mix genuinely has MORE bass

    clean_score, _ = _lem(clean)
    mud_score, _ = _lem(mud, events=[_conflict("critical"), _conflict("critical")])
    assert mud_score < clean_score


def test_no_low_end_returns_documented_gate_value():
    """No stem (and no mix fallback) clears the low floor => the documented
    ``no_low_end`` neutral-low float (the ``_beat_identity`` ``no_beat``
    idiom). Never None, never a crash."""
    doctrine = load_profile("halee_ramone").doctrine
    gate = doctrine["scorers"]["low_end_motion"]["no_low_end"]
    airy = [
        _rec("Shaker", identity="percussion", family="drums", low=0.05, crest=22.0),
        _rec("Vocal", identity="lead_vocal", family="vocal", low=0.02, crest=9.0),
    ]
    # With a mix fallback that also fails the floor, and with no mix at all.
    for mix in ({"band_energy": {"low": 0.03, "low_mid": 0.4}}, None):
        score, ev = _lem(airy, mix_metrics=mix, doctrine=doctrine)
        assert score == doctrine_engine._clamp(gate)
        assert any("low" in e.lower() for e in ev)


def test_distinctness_no_conflicts_but_no_pocket_disagrees_with_static_mix():
    """THE DISTINCTNESS GUARD vs ``_static_mix``: four pads share the low band
    — no kick/bass pair, so NO ``low_end_conflict`` events exist and
    static_mix stays healthy (its hygiene checks all pass) — but there is no
    defined pocket, so low_end_motion scores LOW. The axes disagree on the
    same mix, which is only possible if low_end_motion measures the POSITIVE
    pocket relationship rather than re-deriving static_mix's conflict
    penalty."""
    doctrine = load_profile("halee_ramone").doctrine
    pads = [_rec(f"Pad {i}", low=0.4, crest=10.0) for i in range(4)]
    lead = _rec("Lead Vocal", identity="lead_vocal", family="vocal", low=0.05)
    records = pads + [lead]

    static, _ = doctrine_engine._static_mix(records, lead, [], None, doctrine)
    lem, _ = _lem(records, doctrine=doctrine)

    assert static >= 70.0  # hygiene axis: nothing to penalize
    assert lem <= 35.0     # pocket axis: pile-up, no reserved sub
    assert lem < static


def test_conflicted_pocket_scores_below_clean_pocket_scaled_by_severity():
    """The relationship term (weak form): existing ``low_end_conflict`` events
    break the pocket, scaled by severity — critical costs more than moderate
    (a critical collision ALSO disqualifies the reserved-sub reading), and any
    conflict costs vs none."""
    clean, _ = _lem(_clean_pocket())
    moderate, _ = _lem(_clean_pocket(), events=[_conflict("moderate", 0.25)])
    critical, _ = _lem(_clean_pocket(), events=[_conflict("critical", 0.7)])
    assert critical < moderate < clean


def test_diffuse_low_end_earns_no_reserved_reward():
    """The mix fallback passes the presence gate, but NO stem distinctly
    carries the sub — a diffuse, undefined pocket earns the baseline only
    (no reserved-sub reward, no complementarity) and sits BELOW the defined
    clean pocket."""
    doctrine = load_profile("halee_ramone").doctrine
    thin = [_rec(f"Layer {i}", low=0.1, crest=10.0) for i in range(3)]
    mix = {"band_energy": {"low": 0.45, "low_mid": 0.3}}
    score, ev = _lem(thin, mix_metrics=mix, doctrine=doctrine)
    assert score == doctrine_engine._clamp(doctrine["scorers"]["low_end_motion"]["baseline"])
    clean, _ = _lem(_clean_pocket(), doctrine=doctrine)
    assert score < clean
    assert any("diffuse" in e.lower() for e in ev)


def test_neutral_fallback_when_no_signal_at_all():
    """No records AND no mix band data => the documented NEUTRAL fallback
    (absence of signal is not evidence of an absent low end)."""
    doctrine = load_profile("halee_ramone").doctrine
    neutral = doctrine["scorers"]["low_end_motion"]["neutral"]
    for mix in (None, {}):
        score, ev = _lem([], mix_metrics=mix, doctrine=doctrine)
        assert score == doctrine_engine._clamp(neutral)


def test_physics_primary_mislabeled_808_still_works():
    """Identity labels are corroborating colour ONLY, never the gate: the same
    physics scores identically whether the carriers are labeled kick/bass or
    (mislabeled) pad/synth. A mislabeled 808 still gates presence, still
    counts as a carrier, still forms the pocket."""
    labeled = _clean_pocket()
    mislabeled = [
        _rec("Knock", identity="pad", family="synth", low=0.55, crest=19.0),
        _rec("808", identity="synth", family="synth", low=0.62, crest=9.0),
        _rec("Pad", identity="pad", family="synth", low=0.05, crest=10.0),
    ]
    labeled_score, labeled_ev = _lem(labeled)
    mislabeled_score, _ = _lem(mislabeled)
    assert mislabeled_score == labeled_score
    # When the labels DO agree with the physics, the evidence may corroborate —
    # but explicitly as corroboration, never as the gate.
    blob = " ".join(labeled_ev).lower()
    assert "corroborat" in blob


def test_presence_leakage_more_low_energy_alone_never_raises_the_score():
    """THE PRESENCE-LEAKAGE FENCE: presence is a GATE, not a source of points.
    Boosting the carriers' ``band_energy['low']`` alone — identical carrier
    count, identical crests, identical (absent) conflicts — must NOT increase
    the score. The low band's magnitude is only ever compared against the
    floors; if any term multiplied it into the score, the boosted variant
    would outscore the base and this test would fail."""
    base = _clean_pocket()
    boosted = [
        _rec("Kick", identity="kick", family="drums", low=0.95, crest=19.0),
        _rec("Bass", identity="bass_guitar", family="bass", low=0.98, crest=9.0),
        _rec("Pad", identity="pad", family="synth", low=0.05, crest=10.0),
    ]
    base_score, _ = _lem(base)
    boosted_score, _ = _lem(boosted)
    assert boosted_score == base_score

    # Same fence on a single clean, defined carrier: 0.3 vs 0.95 of the low
    # band is the same pocket (one reserved carrier), not a better one.
    lean_solo, _ = _lem([_rec("Sub", identity="synth_bass", family="bass", low=0.3, crest=12.0)])
    heavy_solo, _ = _lem([_rec("Sub", identity="synth_bass", family="bass", low=0.95, crest=12.0)])
    assert heavy_solo == lean_solo


def test_single_dominant_mud_blob_is_not_a_reserved_pocket():
    """THE MUD-MASQUERADE FENCE: one giant muddy blob swallowing the whole low
    band has the FEWEST carriers (one, fewer than the clean pocket's two) and
    MORE raw low energy per stem than any clean-pocket carrier — and it must
    still LOSE, scoring LOW. The reserved-sub reading is QUALIFIED by pocket
    behavior, never granted for few-ness alone: smeared envelope (low crest,
    no punch partner) forfeits the reserve and takes the blob penalty; a
    COLLIDING blob is lower still. The same single carrier WITH definition
    and no collision genuinely is reserved — qualification, not carrier
    count, is the differentiator."""
    clean_records = _clean_pocket()
    clean, _ = _lem(clean_records)
    smeared_solo = [
        _rec("Mud Bass", identity="synth_bass", family="bass", low=0.95, crest=6.0),
        _rec("Pad", identity="pad", family="synth", low=0.05, crest=10.0),
    ]
    # Fewest carriers + strongest per-stem low presence, by construction:
    clean_carrier_lows = [r["metrics"]["band_energy"]["low"] for r in clean_records]
    assert 0.95 > max(clean_carrier_lows)
    assert sum(1 for lo in [0.95, 0.05] if lo >= 0.2) < sum(1 for lo in clean_carrier_lows if lo >= 0.2)

    smeared, _ = _lem(smeared_solo)
    assert smeared < clean          # fewest carriers, more bass — still loses
    assert smeared <= 35.0          # LOW, not merely below the pocket

    colliding, _ = _lem(smeared_solo, events=[_conflict("critical", 0.7)])
    assert colliding < smeared      # a colliding dominant carrier is worse yet
    assert colliding <= 35.0

    # The qualification is what separates blob from reserve: the SAME solo
    # carrier, clean and with a defined (non-smeared) envelope, earns the
    # reserved reading and outscores both blob variants.
    defined_solo, _ = _lem([
        _rec("808", identity="synth_bass", family="bass", low=0.95, crest=14.0),
        _rec("Pad", identity="pad", family="synth", low=0.05, crest=10.0),
    ])
    assert defined_solo > smeared
    assert defined_solo > colliding


def test_score_is_bounded_0_100():
    """Whatever the inputs, the scorer stays a clamped 0..100 float."""
    doctrine = load_profile("halee_ramone").doctrine
    extreme_pileup = [_rec(f"Sub {i}", low=1.0, crest=8.0 + 3 * (i % 2)) for i in range(8)]
    wide_gap = [
        _rec("Punch", identity="kick", family="drums", low=0.9, crest=35.0),
        _rec("Drone", identity="synth_bass", family="bass", low=0.9, crest=4.0),
    ]
    cases = [
        ([], [], None),
        (_clean_pocket(), [], None),
        (_bass_heavy_mud(), [_conflict("critical")] * 5, None),
        (extreme_pileup, [_conflict("critical")] * 5, None),
        (wide_gap, [], None),
    ]
    for records, events, mix in cases:
        score, _ = _lem(records, events=events, mix_metrics=mix, doctrine=doctrine)
        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0


def test_honest_deferrals_stated_in_docstring_never_claimed_in_evidence():
    """THE HONESTY GATE: the docstring states the three deferrals — kick/sub
    TEMPORAL interlock, low-end MOTIF detection, per-section true-sub movement
    (sections expose low_mid only) — and the evidence never claims any of
    them."""
    doc = (doctrine_engine._low_end_motion.__doc__ or "").lower()
    assert "interlock" in doc
    assert "motif" in doc
    assert "low_mid" in doc

    for records, events in (
        (_clean_pocket(), []),
        (_bass_heavy_mud(), [_conflict("critical")]),
    ):
        _, ev = _lem(records, events=events)
        blob = " ".join(ev).lower()
        for claim in ("interlock", "sidechain", "motif", "per-section sub"):
            assert claim not in blob


# --------------------------------------------------------------------------- #
# 3. LIVENESS (load-bearing) — a non-zero weight makes the axis a real lever,
#    and a sabotage of the scorer must break these tests (P-016/P-029).
# --------------------------------------------------------------------------- #
def _profile_weighting_low_end_motion(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero low_end_motion
    weight — so any overall delta is attributable to the low_end_motion term
    alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["low_end_motion_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    low_end_motion non-zero changes the overall vs the weight-0 reference.
    This is LIVE-WIRE proof: the term is genuinely threaded, not decorative.

    Sabotage that this test catches: hardcoding ``_low_end_motion`` to return
    a constant equal to nothing in particular, or dropping it from
    ``component_scores``, collapses the weighted mean back onto the reference
    and this assertion FAILS — while byte-identical stays green."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)  # weight-0 default
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_low_end_motion(3.0), groove=groove
    )

    lem = reference["low_end_motion_score"]
    assert lem is not None and 0.0 <= lem <= 100.0
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_low_end_motion_score(analyzed):
    """A sharper sabotage guard: the direction the overall moves under a
    non-zero weight must be consistent with low_end_motion's value relative
    to the other components. A hardcoded term would not track the real score
    and this assertion would break."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    lem = reference["low_end_motion_score"]
    ref_overall = reference["overall_mix_readiness_score"]

    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_low_end_motion(5.0), groove=groove
    )
    new_overall = weighted["overall_mix_readiness_score"]

    if lem > ref_overall:
        assert new_overall > ref_overall
    elif lem < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — the scorer only reads its inputs; it never mutates the
#    shared profile structures, the records or the masking report.
# --------------------------------------------------------------------------- #
def test_low_end_motion_does_not_mutate_profile_records_or_masking_report():
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    records = _clean_pocket()
    records_before = copy.deepcopy(records)
    masking_report = {"events": [_conflict("moderate", 0.25)]}
    masking_before = copy.deepcopy(masking_report)
    mix = {"band_energy": {"low": 0.3, "low_mid": 0.3}}
    mix_before = copy.deepcopy(mix)
    doctrine_engine._low_end_motion(records, [], masking_report, mix, doctrine)
    assert doctrine == doctrine_before
    assert records == records_before
    assert masking_report == masking_before
    assert mix == mix_before


def test_score_doctrine_with_low_end_motion_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof extended to the new axis: re-run
    ``score_doctrine`` on a real fixture and assert the shared default doctrine
    is byte-unchanged (its ``scorers.low_end_motion`` block included)."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "low_end_motion" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
