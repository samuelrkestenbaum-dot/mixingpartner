"""P-025 — the binding guard for the producer-agnostic extraction.

This test suite is the load-bearing proof that ``halee_ramone.json`` (loaded via
``load_profile``) reconstructs TODAY's producer-specific judgment BYTE-IDENTICALLY
from the still-hardcoded modules. Nothing consumes the profile yet (P-026→P-029
will wire it); these tests compare the loaded profile against the live module
dicts directly.

Round-trip assertions are of two kinds:

* **exact-equal** — the source value is a clean module-level constant, so the
  loaded field must ``==`` it exactly (ordering/tuples-vs-lists normalized
  honestly, never loosened to pass).
* **indirect** — the source value is computed INLINE inside a function (the
  doctrine component weights, the 86.0 baselines, and the ``_halee``/``_ramone``
  penalty coefficients are locals, not constants). Refactoring the source to
  expose them would break the byte-identical / no-wiring contract of P-025, so we
  instead DRIVE the real function with crafted inputs and assert the captured
  coefficient reproduces the function's own arithmetic. Flagged for P-026→P-028,
  which own those sources.
"""

from __future__ import annotations

import copy

from logic_mix_os import creative, governance
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import ProducerProfile, load_profile


# --------------------------------------------------------------------------- #
# Byte-identical ROUND-TRIP — exact-equal (clean module-level constants)
# --------------------------------------------------------------------------- #
def test_kind_scores_round_trip_exact():
    """The 7 kinds × 9 dims (incl. the verbatim ``halee``/``ramone`` dim names)."""
    assert load_profile().kind_scores == creative._KIND_SCORES


def test_nudge_table_round_trip_exact():
    """The penalty-nudge rows. ``kinds`` is a set in-source; the loader must
    normalize the JSON list back to a set so the comparison is honest, not loose."""
    assert load_profile().nudge_table == creative._NUDGE_TABLE


def test_promotion_table_round_trip_exact():
    assert load_profile().promotion_table == creative._PROMOTION_TABLE


def test_caps_round_trip_exact():
    p = load_profile()
    assert p.creative_nudge_cap == creative.CREATIVE_NUDGE_CAP
    assert p.creative_promotion_cap == creative.CREATIVE_PROMOTION_CAP


def test_risk_penalty_round_trip_exact():
    assert load_profile().risk_penalty == creative._RISK_PENALTY


def test_search_modes_round_trip_exact():
    assert load_profile().search_modes == creative.SEARCH_MODES


def test_philosophy_round_trip_exact():
    assert load_profile().philosophy == creative.PHILOSOPHY


def test_truth_alignment_round_trip_exact():
    assert load_profile().truth_alignment == governance._TRUTH_ALIGNMENT


def test_taste_kind_bias_round_trip_exact():
    """``_TASTE_KIND_BIAS`` uses ``±TASTE_MAX_DELTA`` (i.e. ±15) inline; the JSON
    stores the resolved numbers, which must reconstruct the live dict exactly."""
    assert load_profile().taste_kind_bias == governance._TASTE_KIND_BIAS


def test_taste_max_delta_round_trip_exact():
    assert load_profile().taste_max_delta == governance.TASTE_MAX_DELTA


def test_aesthetic_kill_switches_round_trip_exact():
    """Only the AESTHETIC subset (items 6-9 == indices 5-8) is producer-specific.
    The SAFETY switches (items 1-5) are producer-agnostic and MUST NOT appear."""
    aesthetic = governance.KILL_SWITCHES[5:9]
    assert load_profile().aesthetic_kill_switches == aesthetic
    # And exactly those four, verbatim.
    assert aesthetic == [
        "Never chase reference loudness at the mix stage.",
        "Never widen the full mix to solve chorus lift.",
        "Never make the lead vocal less intelligible unless explicitly approved.",
        "Never allow a stock loop to dominate the song identity by accident.",
    ]


def test_safety_kill_switches_excluded():
    """The five safety kill-switches (non-destructive/Class-5, producer-agnostic)
    must NOT be captured in the profile — they stay universal."""
    profile_switches = set(load_profile().aesthetic_kill_switches)
    for safety in governance.KILL_SWITCHES[0:5]:
        assert safety not in profile_switches


def test_taste_triangle_round_trip_exact():
    """P-027 Part B: the taste-triangle rules widened into the profile. The
    intimate-width penalty and the emotion-blend dims were inline literals in
    ``governance.taste_triangle`` (``identity -= 30`` and the mean of three named
    scores). The JSON must reconstruct them exactly."""
    tt = load_profile().taste_triangle
    assert tt["intimate_width_penalty"] == 30
    assert tt["emotion_dims"] == [
        "ramone_score", "listener_excitement_score", "vocal_belief_score",
    ]


def test_veto_thresholds_round_trip_exact():
    """P-027 Part B: the governance veto thresholds widened into the profile —
    inline literals in ``taste_triangle`` (reject line) and ``govern_variant``
    (align veto + fallback)."""
    vt = load_profile().veto_thresholds
    assert vt["reject_below"] == 45
    assert vt["align_veto_below"] == 50
    assert vt["align_fallback"] == 75


def test_taste_triangle_round_trip_indirect():
    """The widened taste-triangle rules were computed INLINE in
    ``governance.taste_triangle``. Drive the real function and assert the captured
    profile values reproduce its arithmetic byte-for-byte (the honest indirect
    round-trip, per the P-025 pattern)."""
    tt = load_profile().taste_triangle
    vt = load_profile().veto_thresholds

    def _variant(kind, ramone, excite, belief, taste):
        return {
            "variant_id": "x", "kind": kind, "name": kind, "changes": [],
            "scores": {
                "ramone_score": ramone, "listener_excitement_score": excite,
                "vocal_belief_score": belief, "technical_score": 80,
                "taste_alignment_score": taste, "overall_score": 90.0,
            },
        }

    # emotion == round(mean of the three captured emotion_dims), in that order.
    v = _variant("vocal_ride", 91, 80, 60, 90)
    tri = governance.taste_triangle(v, "neutral")
    dims = tt["emotion_dims"]
    expected_emotion = round(sum(v["scores"][d] for d in dims) / len(dims))
    assert tri["emotion"] == expected_emotion

    # width_bloom under an intimate lean gets identity -= intimate_width_penalty.
    v_wb = _variant("width_bloom", 80, 80, 80, 90)
    intimate = governance.taste_triangle(v_wb, "intimate")
    neutral = governance.taste_triangle(v_wb, "neutral")
    assert neutral["identity"] - intimate["identity"] == tt["intimate_width_penalty"]

    # reject_below drives the keep/reject verdict on identity and emotion.
    below = _variant("vocal_ride", 80, 80, 80, vt["reject_below"] - 1)
    at = _variant("vocal_ride", 80, 80, 80, vt["reject_below"])
    assert governance.taste_triangle(below, "neutral")["verdict"] == "reject"
    assert governance.taste_triangle(at, "neutral")["verdict"] == "keep"


def test_veto_thresholds_round_trip_indirect():
    """The align veto (``align < 50``) and the align fallback (unknown kind => 75)
    were inline in ``govern_variant``. Drive it and assert the captured thresholds
    reproduce the vetoes byte-for-byte."""
    vt = load_profile().veto_thresholds

    def _variant(kind, taste=90):
        return {
            "variant_id": "x", "kind": kind, "name": kind, "changes": [],
            "scores": {
                "ramone_score": 80, "listener_excitement_score": 80,
                "vocal_belief_score": 80, "technical_score": 80,
                "taste_alignment_score": taste, "overall_score": 90.0,
            },
        }

    # align_fallback: an unknown kind falls back to the captured default (75).
    g = governance.govern_variant(_variant("no_such_kind"), [], "neutral")
    assert g["emotional_truth_alignment"] == vt["align_fallback"]

    # align_veto_below: width_bloom under an intimate lean has align 45 (< 50) and
    # is doctrine-vetoed; the captured threshold reproduces that veto.
    g_wb = governance.govern_variant(_variant("width_bloom", taste=99), [], "intimate")
    align = governance._TRUTH_ALIGNMENT["intimate"]["width_bloom"]
    assert align < vt["align_veto_below"]
    assert g_wb["vetoed"] is True


def test_default_creative_mode_map_round_trip():
    """``pipeline._default_creative_mode`` is producer-specific: its truth words
    map onto producer-named search modes (``ramone_vocal_truth`` vs
    ``dramatic_contrast``). The profile captures the intimate-truth words and the
    two modes; assert it reproduces the function's behavior on both branches."""
    from logic_mix_os import pipeline

    p = load_profile().default_creative_mode
    intimate_words = p["intimate_truth_words"]
    intimate_mode = p["intimate_mode"]
    default_mode = p["default_mode"]

    # Each captured intimate word must drive the intimate branch of the real fn.
    for word in intimate_words:
        assert pipeline._default_creative_mode(
            {"singular_emotional_truth": f"a very {word} song"}
        ) == intimate_mode
    # A truth with no intimate word falls through to the default mode.
    assert pipeline._default_creative_mode(
        {"singular_emotional_truth": "a loud triumphant banger"}
    ) == default_mode


# --------------------------------------------------------------------------- #
# Byte-identical ROUND-TRIP — indirect (inline function coefficients)
# --------------------------------------------------------------------------- #
def _record(**over):
    """A minimal record dict the doctrine functions read from."""
    base = dict(
        name="t",
        instrument_identity="acoustic_guitar",
        identity_family="guitar",
        depth_default="background",
        perceptual_role="heard",
        source_kind="di_audio_track",
        sacredness="core",
        stereo_width=0.2,
    )
    base.update(over)
    return base


def test_doctrine_weights_round_trip_indirect():
    """The component weights are a LOCAL dict inside ``score_doctrine`` — not a
    constant. Capturing them exposes them; assert they equal the numbers the
    live scorer actually uses by reproducing its weighted-average with ONLY the
    profile weights and comparing to ``score_doctrine``'s ``overall``."""
    w = load_profile().doctrine["weights"]
    # A tiny project with a lead vocal so every component score is present.
    records = [
        _record(name="Lead", instrument_identity="lead_vocal", identity_family="vocal",
                depth_default="foreground", sacredness="sacred"),
        _record(name="Gtr"),
    ]
    sections = [
        {"metrics": {"rms_dbfs": -12.0, "width": 0.3, "brightness": 0.4},
         "contrast_vs_previous": {}},
        {"metrics": {"rms_dbfs": -9.0, "width": 0.5, "brightness": 0.6},
         "contrast_vs_previous": {}},
    ]
    result = doctrine_engine.score_doctrine(records, sections, {"events": []}, None)

    present = {k: result[k] for k in w if result.get(k) is not None}
    expected_overall = doctrine_engine._clamp(
        sum(present[k] * w[k] for k in present) / sum(w[k] for k in present)
    )
    assert result["overall_mix_readiness_score"] == expected_overall


def test_doctrine_baselines_round_trip_indirect():
    """The 86.0 baselines for ``_halee`` and ``_ramone`` are inline literals.
    On a CLEAN project (no penalty condition fires) each function returns exactly
    its baseline, so the captured baseline must equal that clean-project score."""
    b = load_profile().doctrine["baselines"]
    clean = [
        _record(name="Lead", instrument_identity="lead_vocal", identity_family="vocal",
                depth_default="foreground", sacredness="sacred"),
        _record(name="Gtr1", depth_default="background"),
        _record(name="Gtr2", depth_default="midground"),
    ]
    halee, _ = doctrine_engine._halee(clean, [])
    # _ramone with a lead present and low decorative fraction => baseline.
    lead = clean[0]
    ramone, _ = doctrine_engine._ramone(clean, lead, [], [])
    assert halee == b["halee"]
    assert ramone == b["ramone"]


def test_doctrine_halee_penalty_coeffs_round_trip_indirect():
    """Drive ``_halee`` with a single triggering condition at a time and assert
    the captured coefficient reproduces the exact score drop the function applies.
    (Coefficients are inline; this is the honest indirect round-trip.)"""
    c = load_profile().doctrine["penalty_coeffs"]["halee"]
    baseline = load_profile().doctrine["baselines"]["halee"]

    # felt element forward: score -= felt_coeff * count (count=1)
    felt = [_record(name="f", perceptual_role="felt", depth_default="foreground")]
    # Also add enough background records so fg_frac stays <= 0.6 (only felt fires).
    felt += [_record(name=f"b{i}", depth_default="background") for i in range(3)]
    score, _ = doctrine_engine._halee(felt, [])
    assert score == doctrine_engine._clamp(baseline - c["felt_forward"] * 1)

    # width-crowding events: score -= width_coeff * count (count=2)
    plain = [_record(name=f"b{i}", depth_default="background") for i in range(4)]
    events = [{"classification": "width_crowding"}, {"classification": "width_crowding"}]
    score, _ = doctrine_engine._halee(plain, events)
    assert score == doctrine_engine._clamp(baseline - c["width_crowding"] * 2)

    # foregrounded full-width loop: score -= loop_coeff * count (count=1)
    loop = [_record(name="loop", source_kind="splice_sample",
                    depth_default="foreground", stereo_width=0.9)]
    loop += [_record(name=f"b{i}", depth_default="background") for i in range(3)]
    score, _ = doctrine_engine._halee(loop, [])
    assert score == doctrine_engine._clamp(baseline - c["loop_foregrounded"] * 1)

    # forward-occupancy: fg_frac > threshold => score -= (fg_frac-threshold)*coeff
    fwd = [_record(name=f"f{i}", depth_default="foreground") for i in range(4)]
    fwd += [_record(name="b", depth_default="background")]
    fg_frac = 4 / 5
    score, _ = doctrine_engine._halee(fwd, [])
    expected = baseline - (fg_frac - c["forward_threshold"]) * c["forward_occupancy"]
    # felt none, so only the occupancy penalty applies.
    assert score == doctrine_engine._clamp(expected)


def test_doctrine_ramone_penalty_coeffs_round_trip_indirect():
    c = load_profile().doctrine["penalty_coeffs"]["ramone"]
    baseline = load_profile().doctrine["baselines"]["ramone"]

    # No lead vocal: score -= no_lead
    no_lead = [_record(name="Gtr")]
    score, _ = doctrine_engine._ramone(no_lead, None, [], [])
    assert score == doctrine_engine._clamp(baseline - c["no_lead"])

    # Lead masked by N forward elements: score -= masked_coeff * N (N=2)
    lead = _record(name="Lead", instrument_identity="lead_vocal",
                   identity_family="vocal", depth_default="foreground",
                   sacredness="sacred")
    recs = [lead, _record(name="Gtr")]
    events = [
        {"elements": ["Lead"], "classification": "bad_masking"},
        {"elements": ["Lead"], "classification": "bad_masking"},
    ]
    score, _ = doctrine_engine._ramone(recs, lead, events, [])
    assert score == doctrine_engine._clamp(baseline - c["vocal_masked"] * 2)

    # Decorative fraction > threshold: score -= decorative_penalty
    lead2 = _record(name="Lead", instrument_identity="lead_vocal",
                    identity_family="vocal", depth_default="foreground",
                    sacredness="sacred")
    deco = [lead2] + [_record(name=f"d{i}", sacredness="decorative") for i in range(3)]
    score, _ = doctrine_engine._ramone(deco, lead2, [], [])
    assert score == doctrine_engine._clamp(baseline - c["decorative_penalty"])


# --------------------------------------------------------------------------- #
# P-028 Finding A — the WIDENED doctrine.scorers group: the per-function
# aesthetic constants for the five remaining scorers. EXACT value pins + the
# drive-the-function indirect round-trip (same honest pattern as the
# _halee/_ramone coeffs above): fire each scorer one condition at a time and
# assert the captured constant reproduces the function's own arithmetic.
# --------------------------------------------------------------------------- #
def test_doctrine_scorers_value_pins_exact():
    """Every widened constant, captured VERBATIM from the pre-P-028 inline
    literals — the exact-equal round-trip on the JSON structure."""
    s = load_profile().doctrine["scorers"]
    assert s["vocal_centrality"] == {
        "no_lead_score": 35.0, "baseline": 70.0,
        "sacred_bonus": 10, "forward_bonus": 10, "masked_coeff": 6,
    }
    assert s["depth_hierarchy"] == {
        "baseline": 40, "per_distinct": 12,
        "forward_threshold": 0.6, "forward_occupancy": 60,
    }
    assert s["section_contrast"] == {"baseline": 100, "lift_fail_penalty": 18}
    assert s["static_mix"] == {
        "baseline": 80.0, "peak_ceiling": -0.1, "peak_penalty": 10,
        "dominant_band_threshold": 0.55, "dominant_band_penalty": 10,
        "crit_low_coeff": 8, "no_lead_penalty": 8,
    }
    assert s["dynamic_mix"] == {
        "insufficient_sections_score": 40.0, "baseline": 30,
        "rms_coeff": 8, "width_coeff": 140, "bright_coeff": 140,
        "lift_fail_penalty": 10,
    }


def test_doctrine_vocal_centrality_round_trip_indirect():
    """Drive ``_vocal_centrality`` one condition at a time; the captured constants
    must reproduce its exact score."""
    c = load_profile().doctrine["scorers"]["vocal_centrality"]

    # No lead => the captured no_lead_score, verbatim.
    assert doctrine_engine._vocal_centrality(None, [])[0] == c["no_lead_score"]

    # A non-sacred, non-forward lead with no masking => bare baseline.
    plain_lead = _record(name="V", instrument_identity="lead_vocal",
                         identity_family="vocal", depth_default="background",
                         sacredness="core")
    assert doctrine_engine._vocal_centrality(plain_lead, [])[0] == \
        doctrine_engine._clamp(c["baseline"])

    # Sacred bonus only.
    sacred = _record(name="V", instrument_identity="lead_vocal",
                     identity_family="vocal", depth_default="background",
                     sacredness="sacred")
    assert doctrine_engine._vocal_centrality(sacred, [])[0] == \
        doctrine_engine._clamp(c["baseline"] + c["sacred_bonus"])

    # Forward bonus only.
    fwd = _record(name="V", instrument_identity="lead_vocal",
                  identity_family="vocal", depth_default="foreground",
                  sacredness="core")
    assert doctrine_engine._vocal_centrality(fwd, [])[0] == \
        doctrine_engine._clamp(c["baseline"] + c["forward_bonus"])

    # Masked penalty: baseline - masked_coeff * N (N=2).
    plain = _record(name="V", instrument_identity="lead_vocal",
                    identity_family="vocal", depth_default="background",
                    sacredness="core")
    events = [
        {"elements": ["V"], "classification": "bad_masking"},
        {"elements": ["V"], "classification": "bad_masking"},
    ]
    assert doctrine_engine._vocal_centrality(plain, events)[0] == \
        doctrine_engine._clamp(c["baseline"] - c["masked_coeff"] * 2)


def test_doctrine_depth_hierarchy_round_trip_indirect():
    """Drive ``_depth_hierarchy``; the captured baseline/per-distinct/forward
    constants must reproduce its score. Physics (distinct counting, fg_frac) stays
    in the function."""
    c = load_profile().doctrine["scorers"]["depth_hierarchy"]

    # Two distinct non-forward layers (fg_frac=0, no occupancy penalty).
    recs = [_record(name="a", depth_default="background"),
            _record(name="b", depth_default="midground")]
    distinct = 2
    assert doctrine_engine._depth_hierarchy(recs)[0] == \
        doctrine_engine._clamp(c["baseline"] + distinct * c["per_distinct"])

    # fg_frac > threshold => occupancy penalty applies on top of the layer score.
    fwd = [_record(name=f"f{i}", depth_default="foreground") for i in range(4)]
    fwd += [_record(name="b", depth_default="background")]
    distinct = 2  # {foreground, background}
    fg_frac = 4 / 5
    expected = (c["baseline"] + distinct * c["per_distinct"]
                - (fg_frac - c["forward_threshold"]) * c["forward_occupancy"])
    assert doctrine_engine._depth_hierarchy(fwd)[0] == doctrine_engine._clamp(expected)


def test_doctrine_section_contrast_round_trip_indirect():
    """Drive ``_section_contrast``; ``baseline - lift_fail_penalty * fails``."""
    c = load_profile().doctrine["scorers"]["section_contrast"]

    # No lift failures => bare baseline.
    ok = [{"contrast_vs_previous": {}}, {"contrast_vs_previous": {}}]
    assert doctrine_engine._section_contrast(ok, [])[0] == \
        doctrine_engine._clamp(c["baseline"])

    # Two lift failures => baseline - penalty * 2.
    fails = [
        {"contrast_vs_previous": {"warning": "no lift"}},
        {"contrast_vs_previous": {"warning": "no lift"}},
    ]
    assert doctrine_engine._section_contrast(fails, [])[0] == \
        doctrine_engine._clamp(c["baseline"] - c["lift_fail_penalty"] * 2)


def test_doctrine_static_mix_round_trip_indirect():
    """Drive ``_static_mix`` one penalty at a time; band analysis / severity
    checks stay physics, the captured constants supply the numbers."""
    c = load_profile().doctrine["scorers"]["static_mix"]
    lead = _record(name="V", instrument_identity="lead_vocal",
                   identity_family="vocal", depth_default="foreground",
                   sacredness="sacred")

    # Clean (lead present, no metrics penalties) => bare baseline.
    balanced = {"band_energy": {"low": 0.4, "mid": 0.4, "high": 0.2}, "peak_dbfs": -3.0}
    assert doctrine_engine._static_mix([lead], lead, [], balanced)[0] == \
        doctrine_engine._clamp(c["baseline"])

    # Peak over ceiling => peak_penalty.
    hot = {"band_energy": {"low": 0.4, "mid": 0.4, "high": 0.2}, "peak_dbfs": 0.0}
    assert doctrine_engine._static_mix([lead], lead, [], hot)[0] == \
        doctrine_engine._clamp(c["baseline"] - c["peak_penalty"])

    # Dominant band over threshold => dominant_band_penalty.
    skewed = {"band_energy": {"low": 0.7, "mid": 0.2, "high": 0.1}, "peak_dbfs": -3.0}
    assert doctrine_engine._static_mix([lead], lead, [], skewed)[0] == \
        doctrine_engine._clamp(c["baseline"] - c["dominant_band_penalty"])

    # Critical low-end conflicts => crit_low_coeff * N (N=2), no mix_metrics.
    events = [
        {"classification": "low_end_conflict", "severity": "critical"},
        {"classification": "low_end_conflict", "severity": "critical"},
    ]
    assert doctrine_engine._static_mix([lead], lead, events, None)[0] == \
        doctrine_engine._clamp(c["baseline"] - c["crit_low_coeff"] * 2)

    # No lead => no_lead_penalty.
    assert doctrine_engine._static_mix([], None, [], None)[0] == \
        doctrine_engine._clamp(c["baseline"] - c["no_lead_penalty"])


def test_doctrine_dynamic_mix_round_trip_indirect():
    """Drive ``_dynamic_mix``; pstdev spread computation stays physics, the
    captured coefficients supply the multipliers/baseline. Byte-for-byte the
    function's own arithmetic (float order preserved)."""
    import statistics
    c = load_profile().doctrine["scorers"]["dynamic_mix"]

    # Fewer than two sections => the captured insufficient-sections score.
    assert doctrine_engine._dynamic_mix([])[0] == c["insufficient_sections_score"]
    one = [{"metrics": {"rms_dbfs": -10.0, "width": 0.3, "brightness": 0.4},
            "contrast_vs_previous": {}}]
    assert doctrine_engine._dynamic_mix(one)[0] == c["insufficient_sections_score"]

    # Two sections, no lift failure => baseline + weighted spreads, same order.
    secs = [
        {"metrics": {"rms_dbfs": -12.0, "width": 0.3, "brightness": 0.4},
         "contrast_vs_previous": {}},
        {"metrics": {"rms_dbfs": -6.0, "width": 0.7, "brightness": 0.9},
         "contrast_vs_previous": {}},
    ]
    rms = [s["metrics"]["rms_dbfs"] for s in secs]
    width = [s["metrics"]["width"] for s in secs]
    bright = [s["metrics"]["brightness"] for s in secs]
    rms_std = statistics.pstdev(rms)
    width_std = statistics.pstdev(width)
    bright_std = statistics.pstdev(bright)
    expected = (c["baseline"] + rms_std * c["rms_coeff"]
                + width_std * c["width_coeff"] + bright_std * c["bright_coeff"])
    assert doctrine_engine._dynamic_mix(secs)[0] == doctrine_engine._clamp(expected)

    # A lift failure subtracts lift_fail_penalty.
    secs_fail = [
        {"metrics": {"rms_dbfs": -12.0, "width": 0.3, "brightness": 0.4},
         "contrast_vs_previous": {}},
        {"metrics": {"rms_dbfs": -6.0, "width": 0.7, "brightness": 0.9},
         "contrast_vs_previous": {"warning": "no lift"}},
    ]
    expected_fail = expected - c["lift_fail_penalty"] * 1
    assert doctrine_engine._dynamic_mix(secs_fail)[0] == \
        doctrine_engine._clamp(expected_fail)


# --------------------------------------------------------------------------- #
# Extraction-completeness — every named producer-specific structure has a home
# --------------------------------------------------------------------------- #
def test_extraction_completeness_all_fields_present():
    """Every producer-specific structure named in P-025 must have a profile field
    (no silent omission). If a future new producer-specific constant is added it
    must be given a home here or this list is knowingly incomplete."""
    p = load_profile()
    required = [
        "kind_scores", "nudge_table", "promotion_table",
        "creative_nudge_cap", "creative_promotion_cap", "risk_penalty",
        "search_modes", "philosophy",
        "truth_alignment", "taste_kind_bias", "taste_max_delta",
        "aesthetic_kill_switches", "taste_triangle", "veto_thresholds",
        "doctrine", "default_creative_mode",
    ]
    for field in required:
        assert hasattr(p, field), f"profile missing field {field!r}"
        assert getattr(p, field) is not None, f"profile field {field!r} is None"


def test_doctrine_subfields_present():
    d = load_profile().doctrine
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        assert key in d and d[key], f"doctrine missing {key!r}"
    assert set(d["penalty_coeffs"]) == {"halee", "ramone"}
    # P-028 Finding A: the five widened scorers each have a captured group.
    # P-032e added the sixth: the producer-agnostic ``beat_identity`` axis.
    # P-032a added the seventh: the producer-agnostic ``negative_space`` axis.
    assert set(d["scorers"]) == {
        "vocal_centrality", "depth_hierarchy", "section_contrast",
        "static_mix", "dynamic_mix", "beat_identity", "negative_space",
    }


# --------------------------------------------------------------------------- #
# Schema validity + metadata
# --------------------------------------------------------------------------- #
def test_metadata_present_and_typed():
    m = load_profile().metadata
    assert isinstance(m["name"], str)
    assert isinstance(m["display_name"], str)
    assert isinstance(m["provenance"], str)
    assert isinstance(m["confidence"], str)
    assert isinstance(m["risk_class"], int)


def test_metadata_reference_values():
    m = load_profile().metadata
    assert m["name"] == "halee_ramone"
    assert m["display_name"] == "Roy Halee / Phil Ramone"
    assert m["confidence"] == "high"
    assert m["provenance"] == "hand-curated-documented"
    # Judgment profile => low/observe risk class, not a destructive action.
    assert m["risk_class"] == 0


def test_load_profile_validates_and_rejects_unknown():
    import pytest

    with pytest.raises((FileNotFoundError, ValueError)):
        load_profile("no_such_producer")


def test_profile_is_frozen():
    """The returned profile is an immutable view — mutation is rejected."""
    import dataclasses
    import pytest

    p = load_profile()
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.philosophy = "changed"  # type: ignore[misc]


def test_load_profile_default_name():
    assert load_profile().metadata["name"] == "halee_ramone"
    assert isinstance(load_profile(), ProducerProfile)


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #
def test_two_loads_equal():
    assert load_profile() == load_profile()


def test_load_does_not_mutate_source_dicts():
    """Loading the profile must not alias/mutate the live module dicts."""
    before = copy.deepcopy(creative._KIND_SCORES)
    p = load_profile()
    # Mutating the loaded copy must not touch the source.
    p.kind_scores["width_bloom"]["technical"] = -999
    assert creative._KIND_SCORES == before
