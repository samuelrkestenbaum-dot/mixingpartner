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
        "aesthetic_kill_switches",
        "doctrine", "default_creative_mode",
    ]
    for field in required:
        assert hasattr(p, field), f"profile missing field {field!r}"
        assert getattr(p, field) is not None, f"profile field {field!r} is None"


def test_doctrine_subfields_present():
    d = load_profile().doctrine
    for key in ("weights", "baselines", "penalty_coeffs"):
        assert key in d and d[key], f"doctrine missing {key!r}"
    assert set(d["penalty_coeffs"]) == {"halee", "ramone"}


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
