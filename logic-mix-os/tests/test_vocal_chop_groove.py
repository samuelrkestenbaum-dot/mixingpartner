"""P-035 — the 4th fixture (``vocal_chop_groove``) + the REAL-DATA vocal-blend
differential: the vocal arc's payoff, measured on real synthesized audio.

P-032f authored the blend policy (mechanically live, dormant); P-034 gave the
analyzer the non-lead ``vocal_band_masking`` capacity (fixture-inert by
construction); this packet builds the first fixture with non-lead vocal stems
and proves the WHOLE CHAIN end to end on audio the pipeline actually reads:

  vocal-type classification (chop -> ``vocal_percussive`` 0.95, stack ->
  ``vocal_stack`` 0.95, lead -> ``vocal_lead`` 0.95)
    -> non-lead ``vocal_band_masking`` events (2 moderate in the verse, where
       the bright electric guitar stands forward/heard in front of the tucked
       chop and stack; 2 info in the chorus, where the guitar steps back)
    -> the profile blend gate (halee_ramone protects: vocal_role_fit 65.0;
       timbaland accepts the blend: 85.0 — the P-032i corollary's LIVE half).

THE FIXTURE DESIGN (all constraints real, none faked):

* ``BGV Chop`` — backing-vocal identity BY NAME ('bgv'), ``one_shot_sample``
  by manifest source-kind hint (legitimate manifest metadata, same idiom as
  the other fixtures' ``comped_audio_track`` hints), transient-dense
  (td 0.81 >= 0.55) with defined hits (crest 19.2 dB >= 12) BY SYNTHESIS —
  the 3-of-3 signal set the 0.75 blend-gate confidence floor requires
  (2-of-3 = 0.667 fails it).
* ``Backing Vocals Stack`` — wide (0.80 >= 0.5), sustained (td 0.06 <= 0.35),
  backing identity: 3-of-3 -> ``vocal_stack`` 0.95.
* ``Electric Guitar`` — ★ the BINDING P-034 reviewer advisory: the mandatory
  forward/heard masker-set instrument, chord partials in the vocal presence
  band (1.5-4 kHz), overlap >= 0.1 against BOTH non-lead vocal stems.
* The depth planner puts the guitar forward in the VERSE and tucks the
  chop/stack behind it — the placement Commit 1's analyzer decision (the
  P-034 buried-vocal deferral, consciously flipped) reads as the moderate
  tier. The chop's loop source-kind keeps it midground by default, so the
  loops-not-foregrounded doctrine invariants hold untouched.

BYTE-IDENTITY DISCIPLINE: the original three fixtures' stems, manifests and
goldens are byte-unchanged (per-builder seeds; the golden was written by a
targeted script, never ``--update-golden``), their pins (73.8/70.7/74.3,
68.4/52.6/49.7, vocal_role_fit 85.0 everywhere) unmoved — re-asserted here
and in the consciously-flipped P-032i pin. The regression corpus moves
68/68 -> 93/93 CONSCIOUSLY (the 4th fixture's own 25 checks).

THE THREE P-034 DEFERRALS, REVISITED AGAINST THIS REAL DATA (scope item 4):

(a) ``per_track_masking_risk`` contribution — KEPT EXCLUDED: the fixture
    fires 4 vocal_band_masking events and every track's risk stays 0.0;
    risk feeds ``track_analysis`` consumed broadly, and nothing in the real
    data argues a non-lead vocal-band overlap is per-track RISK rather than
    a vocal-role reading (pinned below).
(b) the ``severity != "info"`` consumption filter — KEPT: the chorus emits
    real info-tier events (guitar midground/heard behind the forward
    chop/stack — the controlled-overlap reading, exactly the shape the
    doctrine calls acceptable for the lead itself) and the vocal-role axis
    consciously does NOT consume them: each stem reads exactly 1 masking
    involvement (the verse moderate), not 2 (pinned below).
(c) the buried-vocal reading — FLIPPED, in Commit 1 of this packet: the
    fixture surfaced the question in the strongest form (the depth planner
    NEVER co-fronts a non-lead vocal with a masker-set instrument, so the
    moderate tier was structurally unreachable end to end); see
    ``test_vocal_band_masking.test_buried_vocal_under_forward_masker_now_emits``.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from logic_mix_os.constants import LOOP_SAMPLE_KINDS
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import write_artifacts
from logic_mix_os.regression import run_regression_suite
from logic_mix_os.validation.output_validator import validate_output

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE

PRODUCERS = ("halee_ramone", "timbaland")

# The 14 shared component axes (same substrate as test_differential_proof).
COMPONENT_KEYS = [
    "physical_space_score", "emotional_hierarchy_score", "vocal_centrality_score",
    "depth_hierarchy_score", "section_contrast_score", "static_mix_score",
    "dynamic_mix_score", "beat_identity_score", "negative_space_score",
    "groove_coherence_score", "rhythmic_surprise_score",
    "low_end_motion_score", "loop_context_score", "vocal_role_fit_score",
]

# THE FULL COMPONENT PICTURE on the 4th fixture, pinned per producer. The two
# value systems share every measured component except the two AUTHORED
# divergences: the loop-context static polarity (the chop reads as a STATIC
# dominant loop: reference 15.0 vs timbaland's authored 10.0 — same channel
# as the two loop fixtures) and the vocal-role blend gate (65.0 protected vs
# 85.0 accepted — THE PAYOFF). The groove/beat/rhythmic axes read genuinely
# (a beat exists): beat_identity 63.6, groove_coherence 99.4,
# rhythmic_surprise 35.6, low_end_motion 60.0.
EXPECTED_COMPONENTS = {
    "halee_ramone": {
        "physical_space_score": 81.3,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82,
        "static_mix_score": 80.0,
        "dynamic_mix_score": 28.2,
        "beat_identity_score": 63.6,
        "negative_space_score": 19.4,
        "groove_coherence_score": 99.4,
        "rhythmic_surprise_score": 35.6,
        "low_end_motion_score": 60.0,
        "loop_context_score": 15.0,
        "vocal_role_fit_score": 65.0,
    },
    "timbaland": {
        "physical_space_score": 81.3,
        "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0,
        "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82,
        "static_mix_score": 80.0,
        "dynamic_mix_score": 28.2,
        "beat_identity_score": 63.6,
        "negative_space_score": 19.4,
        "groove_coherence_score": 99.4,
        "rhythmic_surprise_score": 35.6,
        "low_end_motion_score": 60.0,
        "loop_context_score": 10.0,
        "vocal_role_fit_score": 85.0,
    },
}

# Same stems, two judgments — the 4th fixture's overalls, each recomputable
# as its own profile's weighted mean (proven below).
EXPECTED_OVERALLS = {"halee_ramone": 76.3, "timbaland": 60.9}

# The original three fixtures' pinned judgments — unmoved (scope item 5).
ORIGINAL_OVERALLS = {
    "simple_vocal_piano_song": {"halee_ramone": 73.8, "timbaland": 68.4},
    # dense's halee/timbaland overalls moved +1.1/+1.6 at P-060 (the authorized
    # section-count-invariance corpus move: dense's Kick/Bass critical low-end
    # counted 2x->1x); simple + splice unmoved.
    "dense_chorus_with_loops": {"halee_ramone": 71.8, "timbaland": 54.2},
    "splice_loop_problem": {"halee_ramone": 74.3, "timbaland": 49.7},
}

# The anti-drift set for the 4th fixture: exactly these doctrine_score keys
# diverge between the producers, each divergence explained:
#   overall / confidence          — each profile's own mean / authored map;
#   producer                      — the P-039 identity surface (a conscious
#                                   widening, like confidence): each artifact
#                                   names its own selecting profile BY DESIGN;
#   loop_context_score            — the authored static polarity (15 vs 10);
#   vocal_role_fit_score          — THE BLEND GATE (65 protected vs 85 accepted);
#   evidence                      — the vocal_role_fit evidence lines carry the
#                                   per-profile reading (clarity protection vs
#                                   accepted blend) — isolated to that one axis
#                                   and itself attributable to the authored
#                                   policy (pinned below).
DIVERGENT_DOCTRINE_KEYS = {
    "confidence", "evidence", "loop_context_score",
    "overall_mix_readiness_score", "producer", "vocal_role_fit_score",
}

REF_PROTECTION_LINE = "read under full clarity protection: reduced role fit"
TIM_BLEND_LINE = "accepted as blend under profile policy"


def _rec(res, name):
    return next(r for r in res.records if r["name"] == name)


def _vband(res):
    return [e for e in res.masking_report["events"]
            if e["classification"] == "vocal_band_masking"]


# =========================================================================== #
# 1. THE CLASSIFICATIONS — the packet's verification items (a), (b), (d).
# =========================================================================== #
def test_stem_classifications_on_real_audio(chop_groove_analyzed):
    """The chop clears the blend gate's floor on REAL synthesized audio:
    3-of-3 percussive signals (transient-dense, defined hits, chop source)
    -> ``vocal_percussive`` at 0.95 >= the 0.75 floor. The stack reads
    ``vocal_stack`` at 0.95 (wide, sustained, backing identity). The lead
    stays ``vocal_lead`` (identity wins). Non-vocal stems carry explicit
    None. The detection basis is SHARED: both producers read the identical
    classification (physics, not judgment)."""
    for producer in PRODUCERS:
        res = chop_groove_analyzed[producer]

        lead = _rec(res, "Lead Vocal")
        assert lead["instrument_identity"] == "lead_vocal"
        assert lead["vocal_type"] == "vocal_lead"
        assert lead["vocal_type_confidence"] == 0.95

        chop = _rec(res, "BGV Chop")
        assert chop["instrument_identity"] == "backing_vocal"
        assert chop["source_kind"] == "one_shot_sample"
        assert chop["source_kind"] in LOOP_SAMPLE_KINDS  # the 3rd signal
        assert chop["metrics"]["transient_density"] >= 0.55
        assert chop["metrics"]["crest_factor_db"] >= 12.0
        assert chop["vocal_type"] == "vocal_percussive"
        assert chop["vocal_type_confidence"] == 0.95
        floor = load_profile("timbaland").vocal_blend_policy["confidence_floor"]
        assert chop["vocal_type_confidence"] >= floor == 0.75

        stack = _rec(res, "Backing Vocals Stack")
        assert stack["instrument_identity"] == "backing_vocal"
        assert stack["stereo_width"] >= 0.5
        assert stack["metrics"]["transient_density"] <= 0.35
        assert stack["vocal_type"] == "vocal_stack"
        assert stack["vocal_type_confidence"] == 0.95

        for name in ("Electric Guitar", "Kick", "Snare"):
            rec = _rec(res, name)
            assert rec["vocal_type"] is None
            assert rec["vocal_type_confidence"] is None


def test_chop_stays_out_of_the_foreground_by_default(chop_groove_analyzed):
    """The loop-source chop honours the source-material doctrine: midground
    default depth (never a foregrounded stock one-shot) with the loop
    warnings attached — the same invariants the regression corpus enforces,
    asserted here at the record surface."""
    chop = _rec(chop_groove_analyzed["halee_ramone"], "BGV Chop")
    assert chop["depth_default"] == "midground"
    assert chop["source_warnings"]


# =========================================================================== #
# 2. THE EVENTS — verification item (c): moderate, lead-free, both tiers live.
# =========================================================================== #
def test_vocal_band_masking_events_fire_on_real_audio(chop_groove_analyzed):
    """Exactly 4 ``vocal_band_masking`` events, physics-identical under both
    producers (the masking analyzer is producer-agnostic):

    * verse_1 — 2 MODERATE: the guitar stands forward/heard in front of the
      tucked chop (overlap 0.2191) and stack (0.1655), both >= the 0.1
      conflict floor and >= the advisory's 0.1 requirement;
    * chorus_1 — 2 INFO: the chop/stack step forward and the guitar steps
      back to midground (the controlled-overlap tier, consciously NOT
      consumed by the vocal-role axis — deferral (b)).

    The LEAD is in none of them, and severity never exceeds moderate."""
    ref = chop_groove_analyzed["halee_ramone"]
    tim = chop_groove_analyzed["timbaland"]
    assert ref.masking_report == tim.masking_report  # shared physics

    vband = _vband(ref)
    assert len(vband) == 4
    for e in vband:
        assert "Lead Vocal" not in e["elements"]
        assert e["severity"] in {"moderate", "info"}
        assert e["frequency_range"] == "1.5kHz-4kHz"

    moderate = [e for e in vband if e["severity"] == "moderate"]
    assert len(moderate) == 2
    by_stem = {e["elements"][0]: e for e in moderate}
    assert set(by_stem) == {"BGV Chop", "Backing Vocals Stack"}
    for stem_name, overlap in (("BGV Chop", 0.2191),
                               ("Backing Vocals Stack", 0.1655)):
        e = by_stem[stem_name]
        assert e["elements"] == [stem_name, "Electric Guitar"]
        assert e["section"] == "verse_1"
        assert e["overlap"] == overlap
        assert e["overlap"] >= 0.1
        assert e["depth_layers"] == ["background", "foreground"]

    info = [e for e in vband if e["severity"] == "info"]
    assert len(info) == 2
    assert all(e["section"] == "chorus_1" for e in info)
    assert all(e["depth_layers"] == ["foreground", "midground"] for e in info)

    s = ref.masking_report["summary"]
    assert s["vocal_band_masking_count"] == 4
    assert s["moderate_count"] == 2
    assert s["critical_count"] == 0


# =========================================================================== #
# 3. THE PAYOFF — the real-data blend differential (scope item 3).
# =========================================================================== #
def test_the_real_data_blend_differential(chop_groove_analyzed):
    """THE P-032f INERT-BLEND COROLLARY'S LIVE HALF, on real audio: the same
    stems, the same events, two authored philosophies —

    * halee_ramone (``acceptable_blend: false``): both qualified non-lead
      vocal stems read under full clarity protection — 1 penalized masking
      involvement each -> ``vocal_role_fit_score`` 65.0 (70 baseline + 15
      lead-forward bonus - 2 x 10);
    * timbaland (``acceptable_blend: true``, floor 0.75, both stems at
      0.95): the same involvements are accepted as blend -> 85.0.

    The lead reading is identical under both (forward, clear of conflicts —
    no policy can touch the lead by construction)."""
    assert load_profile("halee_ramone").vocal_blend_policy["acceptable_blend"] is False
    assert load_profile("timbaland").vocal_blend_policy["acceptable_blend"] is True

    ref_ds = chop_groove_analyzed["halee_ramone"].doctrine_score
    tim_ds = chop_groove_analyzed["timbaland"].doctrine_score
    assert ref_ds["vocal_role_fit_score"] == 65.0
    assert tim_ds["vocal_role_fit_score"] == 85.0

    ref_ev = ref_ds["evidence"]["vocal_role_fit"]
    tim_ev = tim_ds["evidence"]["vocal_role_fit"]
    assert sum(REF_PROTECTION_LINE in line for line in ref_ev) == 2
    assert not any(TIM_BLEND_LINE in line for line in ref_ev)
    assert sum(TIM_BLEND_LINE in line for line in tim_ev) == 2
    assert not any(REF_PROTECTION_LINE in line for line in tim_ev)
    # Each stem reads exactly ONE masking involvement (the verse moderate):
    # the chorus info tier is consciously NOT consumed — deferral (b), kept.
    assert any("'BGV Chop' (vocal_percussive, confidence 0.95): "
               "1 masking involvement(s)" in line for line in tim_ev)
    assert any("'Backing Vocals Stack' (vocal_stack, confidence 0.95): "
               "1 masking involvement(s)" in line for line in tim_ev)
    assert any("overlaps 1 forward element(s)" in line for line in ref_ev)
    # The lead reading is shared verbatim.
    lead_line = ("Lead vocal 'Lead Vocal' sits forward and clear of masking "
                 "conflicts — the lead owns the presence band.")
    assert lead_line in ref_ev and lead_line in tim_ev


def test_the_overall_delta_is_traceable_to_authored_values(chop_groove_analyzed):
    """FULL ATTRIBUTABILITY on the 4th fixture (the P-032i obligation (b)
    idiom, consciously extended for the NEW divergence channel):

    * each producer's overall recomputes exactly as its own profile's
      weighted mean (76.3 / 60.9);
    * timbaland's judgment RECONSTRUCTS from the reference's measurements
      plus timbaland's authored values alone — substitute the authored
      static-loop polarity (15 -> 10) AND the authored blend acceptance
      (vocal_role_fit 65 -> 85), apply timbaland's weights, land on 60.9;
    * the blend gate is WORTH +0.7 overall to timbaland (weight 0.4):
      with the reference's protected 65.0 in its own weights the overall
      would read 60.2;
    * the reference's own overall CANNOT move with the axis (authored
      weight 0): swapping 85.0 in leaves 76.3."""
    ref_ds = chop_groove_analyzed["halee_ramone"].doctrine_score
    tim_ds = chop_groove_analyzed["timbaland"].doctrine_score

    def weighted_overall(producer, components):
        weights = load_profile(producer).doctrine["weights"]
        present = {k: components[k] for k in weights if components.get(k) is not None}
        return doctrine_engine._clamp(
            sum(present[k] * weights[k] for k in present)
            / sum(weights[k] for k in present)
        )

    for producer, ds in (("halee_ramone", ref_ds), ("timbaland", tim_ds)):
        own = {k: ds[k] for k in COMPONENT_KEYS}
        assert ds["overall_mix_readiness_score"] == EXPECTED_OVERALLS[producer]
        assert weighted_overall(producer, own) == EXPECTED_OVERALLS[producer]

    # Reconstruction from the reference's measurements + authored values.
    rebuilt = {k: ref_ds[k] for k in COMPONENT_KEYS}
    rebuilt["loop_context_score"] = 10.0   # authored static polarity
    rebuilt["vocal_role_fit_score"] = 85.0  # authored blend acceptance
    assert weighted_overall("timbaland", rebuilt) == 60.9

    # The counterfactual: timbaland WITHOUT its blend opt-in.
    protected = {k: tim_ds[k] for k in COMPONENT_KEYS}
    protected["vocal_role_fit_score"] = 65.0
    assert weighted_overall("timbaland", protected) == 60.2

    # The reference surface cannot move with the axis (weight 0).
    swapped = {k: ref_ds[k] for k in COMPONENT_KEYS}
    swapped["vocal_role_fit_score"] = 85.0
    assert weighted_overall("halee_ramone", swapped) == 76.3


def test_component_picture_and_divergence_audit(chop_groove_analyzed):
    """The full 14-component picture pinned under both producers (the
    groove-fixture axes read meaningfully: beat_identity 63.6,
    groove_coherence 99.4, rhythmic_surprise 35.6, low_end_motion 60.0),
    and the anti-drift audit: the producers diverge on EXACTLY the
    explained set — with the ``evidence`` divergence isolated to the
    ``vocal_role_fit`` axis (itself attributable to the authored policy)
    and ``warnings`` identical."""
    ref_ds = chop_groove_analyzed["halee_ramone"].doctrine_score
    tim_ds = chop_groove_analyzed["timbaland"].doctrine_score

    for producer, ds in (("halee_ramone", ref_ds), ("timbaland", tim_ds)):
        assert {k: ds[k] for k in COMPONENT_KEYS} == EXPECTED_COMPONENTS[producer]

    assert set(ref_ds) == set(tim_ds)
    diverged = {k for k in ref_ds if ref_ds[k] != tim_ds[k]}
    assert diverged == DIVERGENT_DOCTRINE_KEYS, diverged
    ev_diverged = {k for k in ref_ds["evidence"]
                   if ref_ds["evidence"][k] != tim_ds["evidence"][k]}
    assert ev_diverged == {"vocal_role_fit"}
    assert ref_ds["warnings"] == tim_ds["warnings"]
    # The static-loop reading behind the loop_context divergence is real:
    # the chop is the dominant loop and the mix does not evolve around it.
    assert any("reads STATIC" in line
               for line in ref_ds["evidence"]["loop_context"])


def test_side_by_side_snapshot_pinned(chop_groove_analyzed):
    """The 4th fixture's receipt-printable comparison surface, via the same
    ``differential_snapshot`` helper the P-032i suite pins for the original
    three (which stay pin-to-3 by conscious decision — see
    test_differential_proof.EXPECTED_SNAPSHOT)."""
    from test_differential_proof import differential_snapshot

    snap = differential_snapshot(
        chop_groove_analyzed["halee_ramone"], chop_groove_analyzed["timbaland"]
    )
    assert snap == {
        "halee_ramone": {
            "overall": 76.3,
            "lowest_components": [
                ("loop_context_score", 15.0),
                ("negative_space_score", 19.4),
                ("dynamic_mix_score", 28.2),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "loop": "loop_B",
                "depth": "depth_A", "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
        "timbaland": {
            "overall": 60.9,
            "lowest_components": [
                ("loop_context_score", 10.0),
                ("negative_space_score", 19.4),
                ("dynamic_mix_score", 28.2),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "loop": "loop_B",
                "depth": "depth_A", "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
    }


# =========================================================================== #
# 4. THE P-034 DEFERRALS — the conscious decisions, pinned against real data.
# =========================================================================== #
def test_deferral_a_risk_stays_untouched_by_the_new_classification(
    chop_groove_analyzed,
):
    """Deferral (a), KEPT: 4 real vocal_band_masking events and every
    track's ``per_track_masking_risk`` stays 0.0 (no bad_masking / low-end
    pair exists on this fixture) — the new classification still contributes
    nothing to the broadly-consumed risk metric."""
    res = chop_groove_analyzed["halee_ramone"]
    assert len(_vband(res)) == 4
    assert all(v == 0.0 for v in res.masking_report["per_track_masking_risk"].values())
    for entry in res.track_analysis:
        assert entry["metrics"]["masking_risk"] == 0.0


def test_deferral_b_info_tier_stays_unconsumed_on_real_data(
    chop_groove_analyzed,
):
    """Deferral (b), KEPT: the chorus's real info-tier events (the guitar
    behind the forward chop/stack — the exact overlap shape the doctrine
    calls controlled for the LEAD itself) reach neither the penalty nor the
    blend gate: with the two info events removed, the vocal-role reading is
    IDENTICAL under both producers."""
    for producer in PRODUCERS:
        res = chop_groove_analyzed[producer]
        prof = load_profile(producer)
        events = res.masking_report["events"]
        without_info = [e for e in events
                        if not (e["classification"] == "vocal_band_masking"
                                and e["severity"] == "info")]
        assert len(without_info) == len(events) - 2
        full = doctrine_engine._vocal_role_fit(
            res.records, events, prof.doctrine, prof.vocal_blend_policy)
        trimmed = doctrine_engine._vocal_role_fit(
            res.records, without_info, prof.doctrine, prof.vocal_blend_policy)
        assert full == trimmed


# =========================================================================== #
# 5. BYTE-IDENTITY (scope item 5) + the corpus at its NEW count.
# =========================================================================== #
def test_original_three_fixtures_unmoved(analyzed):
    """The original corpus is byte-stable through this packet: the pinned
    overalls, vocal_role_fit 85.0, and ZERO vocal_band_masking events on
    all three reference analyses (no non-lead vocal stems exist there —
    Commit 1's analyzer decision is inert on them by construction)."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        assert ds["overall_mix_readiness_score"] == ORIGINAL_OVERALLS[name]["halee_ramone"]
        assert ds["vocal_role_fit_score"] == 85.0
        assert _vband(analyzed[name]) == []
        assert "vocal_band_masking" not in json.dumps(
            analyzed[name].masking_report, sort_keys=True)


def test_regression_corpus_green_at_the_new_count():
    """THE CONSCIOUS COUNT MOVE: 68/68 -> 93/93. The 4th fixture contributes
    25 checks (6 tracks + masking classes + section warnings + 8 score keys
    + 9 applicable doctrine invariants) against its own golden — written by
    a targeted script; the original three goldens were never regenerated."""
    report = run_regression_suite(ROOT / "fixtures")
    assert report["tests_run"] == 93
    assert report["passed"] == 93
    assert report["failed"] == 0
    assert report["critical_failures"] == []
    golden = ROOT / "fixtures" / VOCAL_CHOP_FIXTURE / "golden" / "snapshot.json"
    assert golden.exists()


def test_new_fixture_artifacts_validate(chop_groove_analyzed, tmp_path):
    """The 4th fixture's rendered artifact trees pass the full output
    validation under BOTH producers, and the doctrine artifact carries the
    live vocal_band_masking vocabulary honestly."""
    for producer in PRODUCERS:
        out = tmp_path / producer
        write_artifacts(chop_groove_analyzed[producer], out)
        report = validate_output(out)
        assert report["ok"], (producer, report["errors"])
        masking = json.loads(
            (out / "masking_report.json").read_text(encoding="utf-8"))
        assert masking["summary"]["vocal_band_masking_count"] == 4


def test_generator_is_deterministic_and_seed_isolated():
    """Two builds from the fixed per-builder seed are byte-identical (stems
    AND manifest), and the builder draws from its OWN seed (1003) — appended
    after the original three, so their bytes can never shift."""
    from fixtures.generate_fixtures import build_vocal_chop_groove

    a = build_vocal_chop_groove(np.random.default_rng(1003))
    b = build_vocal_chop_groove(np.random.default_rng(1003))
    assert a["manifest"] == b["manifest"]
    assert set(a["stems"]) == set(b["stems"]) == {
        "Lead Vocal", "BGV Chop", "Backing Vocals Stack",
        "Electric Guitar", "Kick", "Snare",
    }
    for name in a["stems"]:
        assert np.array_equal(a["stems"][name], b["stems"][name]), name
