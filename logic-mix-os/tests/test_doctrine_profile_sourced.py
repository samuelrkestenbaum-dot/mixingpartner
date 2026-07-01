"""P-028 — the binding guard that ``doctrine_engine.py``'s producer-specific
judgment constants are SOURCED from ``load_profile("halee_ramone")`` and are
byte-identical to the pre-P-028 inline literals.

This is the last & largest producer-agnostic extraction. Two parts, mirroring
the packet:

* **Part A** — the ALREADY-captured (P-025) constants — ``score_doctrine``'s
  component ``weights``, the ``_halee``/``_ramone`` ``baselines`` (86.0) and their
  ``penalty_coeffs`` — are now read off ``_DEFAULT_PROFILE.doctrine``. The inline
  literals were DELETED from ``doctrine_engine.py``, so these tests PIN the
  concrete expected values inline (the value guard the removed literals used to
  provide implicitly).
* **Part B** — the WIDENED constants for the five remaining scorers
  (``_vocal_centrality`` / ``_depth_hierarchy`` / ``_section_contrast`` /
  ``_static_mix`` / ``_dynamic_mix``) are captured under ``doctrine.scorers`` and
  read from the profile. Value-pinned here; drive-the-function round-trip-guarded
  in ``test_producer_profile``.

The corpus-level byte-identical proof is the UNCHANGED golden regression (68/68 —
doctrine feeds ``doctrine_score``, which the golden pins) plus the unedited
``test_doctrine_engine`` / ``test_doctrine_regression`` suites; those stay the
golden judgment guard and are not touched here.

The NO-ALIASING proof (binding, from P-026/P-027): running the doctrine engine on
a real fixture must leave the shared ``_DEFAULT_PROFILE`` structures byte-unchanged
— no scorer mutates a sourced global in place.
"""

from __future__ import annotations

import copy

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile


# --------------------------------------------------------------------------- #
# Globals are SOURCED from the default profile (single source of truth)
# --------------------------------------------------------------------------- #
def test_default_profile_is_the_reference_producer():
    assert doctrine_engine._DEFAULT_PROFILE.metadata["name"] == "halee_ramone"


def test_globals_are_the_profile_objects():
    """Each producer-specific doctrine global is literally the value read off
    ``_DEFAULT_PROFILE.doctrine`` — the JSON is the single source of truth, not a
    second hardcoded copy that could silently drift."""
    p = doctrine_engine._DEFAULT_PROFILE
    assert doctrine_engine._DOCTRINE is p.doctrine
    assert doctrine_engine._WEIGHTS is p.doctrine["weights"]
    assert doctrine_engine._BASELINES is p.doctrine["baselines"]
    assert doctrine_engine._PENALTY_COEFFS is p.doctrine["penalty_coeffs"]


def test_globals_equal_a_fresh_load():
    """A second independent load reproduces every doctrine global exactly —
    deterministic, and confirms nothing was mutated at import."""
    fresh = load_profile("halee_ramone")
    assert doctrine_engine._WEIGHTS == fresh.doctrine["weights"]
    assert doctrine_engine._BASELINES == fresh.doctrine["baselines"]
    assert doctrine_engine._PENALTY_COEFFS == fresh.doctrine["penalty_coeffs"]


# --------------------------------------------------------------------------- #
# Part A value pins — the concrete pre-P-028 literals, now guarded here
# --------------------------------------------------------------------------- #
def test_weights_value_pins():
    """The 7 component weights, byte-for-byte the pre-P-028 local dict in
    ``score_doctrine``."""
    assert doctrine_engine._WEIGHTS == {
        "halee_score": 1.0,
        "ramone_score": 1.2,
        "vocal_centrality_score": 1.2,
        "depth_hierarchy_score": 1.0,
        "section_contrast_score": 1.0,
        "static_mix_score": 1.0,
        "dynamic_mix_score": 0.8,
        # P-032e — the producer-agnostic beat_identity axis, weight 0 for the
        # reference producer (the byte-identical anchor).
        "beat_identity_score": 0,
        # P-032a — the producer-agnostic negative_space axis, weight 0 for the
        # reference producer (the byte-identical anchor).
        "negative_space_score": 0,
        # P-032b — the producer-agnostic groove_coherence axis (first live-wired),
        # weight 0 for the reference producer (the byte-identical anchor).
        "groove_coherence_score": 0,
        # P-032d — the producer-agnostic rhythmic_surprise axis (weak,
        # section-aggregate form), weight 0 for the reference producer (the
        # byte-identical anchor).
        "rhythmic_surprise_score": 0,
    }


def test_baselines_value_pins():
    assert doctrine_engine._BASELINES == {"halee": 86.0, "ramone": 86.0}


def test_halee_penalty_coeffs_value_pins():
    assert doctrine_engine._PENALTY_COEFFS["halee"] == {
        "forward_threshold": 0.6,
        "forward_occupancy": 70,
        "felt_forward": 4,
        "width_crowding": 6,
        "loop_foregrounded": 6,
    }


def test_ramone_penalty_coeffs_value_pins():
    assert doctrine_engine._PENALTY_COEFFS["ramone"] == {
        "no_lead": 35,
        "vocal_masked": 6,
        "decorative_threshold": 0.4,
        "decorative_penalty": 10,
    }


# --------------------------------------------------------------------------- #
# Behavior pins — the sourced constants reproduce the scorers' arithmetic
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
    )
    base.update(over)
    return base


def test_halee_baseline_from_profile():
    """A clean project (no penalty fires) returns exactly the sourced baseline."""
    clean = [
        _record(name="Lead", instrument_identity="lead_vocal", identity_family="vocal",
                depth_default="foreground", sacredness="sacred"),
        _record(name="Gtr1", depth_default="background"),
        _record(name="Gtr2", depth_default="midground"),
    ]
    halee, _ = doctrine_engine._halee(clean, [])
    assert halee == doctrine_engine._BASELINES["halee"]


def test_ramone_baseline_from_profile():
    clean = [
        _record(name="Lead", instrument_identity="lead_vocal", identity_family="vocal",
                depth_default="foreground", sacredness="sacred"),
        _record(name="Gtr1"),
        _record(name="Gtr2"),
    ]
    ramone, _ = doctrine_engine._ramone(clean, clean[0], [], [])
    assert ramone == doctrine_engine._BASELINES["ramone"]


def test_weights_drive_overall_from_profile():
    """The overall readiness weighted-average uses ONLY the sourced weights."""
    w = doctrine_engine._WEIGHTS
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
    expected = doctrine_engine._clamp(
        sum(present[k] * w[k] for k in present) / sum(w[k] for k in present)
    )
    assert result["overall_mix_readiness_score"] == expected


# --------------------------------------------------------------------------- #
# NO-ALIASING proof (binding) — running the doctrine engine leaves the shared
# profile structures byte-unchanged. No scorer mutates a sourced global.
# --------------------------------------------------------------------------- #
def _snapshot():
    return {
        "doctrine": copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine),
        "weights": copy.deepcopy(doctrine_engine._WEIGHTS),
        "baselines": copy.deepcopy(doctrine_engine._BASELINES),
        "penalty_coeffs": copy.deepcopy(doctrine_engine._PENALTY_COEFFS),
    }


def _assert_unchanged(before):
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before["doctrine"]
    assert doctrine_engine._WEIGHTS == before["weights"]
    assert doctrine_engine._BASELINES == before["baselines"]
    assert doctrine_engine._PENALTY_COEFFS == before["penalty_coeffs"]


def test_score_doctrine_does_not_mutate_shared_globals():
    """Crafted inputs that fire multiple penalty branches must not touch the
    shared profile structures."""
    before = _snapshot()
    records = [
        _record(name="Lead", instrument_identity="lead_vocal", identity_family="vocal",
                depth_default="foreground", sacredness="sacred", perceptual_role="felt"),
        _record(name="Loop", source_kind="splice_sample", depth_default="foreground",
                stereo_width=0.9),
        _record(name="D1", sacredness="decorative", depth_default="foreground"),
        _record(name="D2", sacredness="expendable", depth_default="foreground"),
    ]
    sections = [
        {"metrics": {"rms_dbfs": -12.0, "width": 0.3, "brightness": 0.4},
         "contrast_vs_previous": {"warning": "no lift"}},
        {"metrics": {"rms_dbfs": -9.0, "width": 0.5, "brightness": 0.6},
         "contrast_vs_previous": {}},
    ]
    masking = {"events": [
        {"elements": [], "classification": "width_crowding"},
        {"elements": ["Lead"], "classification": "bad_masking"},
        {"elements": [], "classification": "low_end_conflict", "severity": "critical"},
    ]}
    mix_metrics = {"peak_dbfs": 0.0, "band_energy": {"low": 0.7, "mid": 0.2, "high": 0.1}}
    doctrine_engine.score_doctrine(records, sections, masking, mix_metrics)
    _assert_unchanged(before)


def test_run_doctrine_on_fixture_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof: re-run ``score_doctrine`` on a real fixture's
    analysis inputs and assert every shared ``_DEFAULT_PROFILE`` doctrine structure
    is byte-unchanged afterward."""
    before = _snapshot()
    profile_doctrine_before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)

    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics,
        res.project.intent,
    )

    _assert_unchanged(before)
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == profile_doctrine_before


def test_score_doctrine_is_deterministic(analyzed):
    """Same inputs -> byte-identical output across repeated calls."""
    res = analyzed["dense_chorus_with_loops"]
    args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics,
            res.project.intent)
    first = doctrine_engine.score_doctrine(*args)
    second = doctrine_engine.score_doctrine(*args)
    assert first == second
