"""P-034 — the analyzer capacity: NON-LEAD vocal-band masking events under
their own classification (``vocal_band_masking``), consumed ONLY by the
vocal-role surface, plus the ``creative._lead_masked`` name-match fix.
Fixture-inert: all three current fixtures have NO non-lead vocal stems, so
zero new events fire on real data and every surface stays byte-identical.

THE PRE-REGISTERED SURFACE MAP (binding, from the packet):

* NEW classification ``vocal_band_masking`` — emitted for a non-lead vocal
  stem (identity ``backing_vocal`` OR a non-None ``vocal_type``, the lead
  excluded on identity AND type) sitting FORWARD in a section, checked
  against the SAME forward harmonic/melodic instrument set the lead pathway
  (``_vocal_conflict``) uses. The LEAD is NEVER in these events —
  lead-inclusive vocal masking stays ``bad_masking``, untouched.
* Consumers that move: the masking_report artifact (events + the
  conditional summary count, when they exist); ``_vocal_role_fit``'s
  non-lead pathway (keys on the new classification); the blend gate.
* Consumers pinned IMMOVABLE (each filters by specific classification):
  ``_emotional_hierarchy`` / ``_vocal_centrality`` (lead-inclusive
  ``bad_masking`` only), ``_static_mix`` (``low_end_conflict``),
  ``_physical_space`` (``width_crowding``), ``_beat_identity`` /
  ``_loop_context`` (``bad_masking``), the planners/action generators
  (``bad_masking`` / ``low_end_conflict`` / ``width_crowding``), the golden
  snapshots.

THE EMISSION DESIGN DECISIONS (builder's calls, documented and pinned):

1. FORWARD-ONLY: the non-lead stem must sit in a forward depth for any
   event — an exact mirror of the lead gate (``_depth(lead, sid) in
   FORWARD_DEPTHS``). A buried (midground/background) vocal emits NOTHING
   in this packet; what overlap over a deliberately-buried chop/stack means
   is a profile-philosophy question deferred to P-035's real fixture.
2. VOCAL-vs-VOCAL PAIRS DO NOT FIRE: two non-lead vocal stems overlapping
   in the presence band is the normal construction of a stack/arrangement
   (intentional layering), not masking — and emitting both [A,B] and [B,A]
   would double-count one physical overlap. The masker set is the lead
   pathway's set minus every vocal stem (the lead is also never a masker:
   the lead owning the presence band is the doctrine, not a conflict).
3. SEVERITY CAPPED AT MODERATE: the lead pathway's 0.16 critical tier is
   deliberately NOT mirrored — what a non-lead vocal-band conflict is WORTH
   is a profile decision, and ``critical_count`` is never inflated. The
   sub-conflict tier (other element not forward/heard, overlap >= 0.05)
   mirrors the lead pathway's info reading, same classification, severity
   ``info``.
4. NO ``per_track_masking_risk`` CONTRIBUTION: risk feeds
   ``track_analysis`` metrics consumed broadly; the new classification
   stays out of it in this packet (byte-inert by construction) and P-035
   revisits the question consciously with the fixture that makes it real.
5. SUMMARY COUNTED HONESTLY, CONDITIONALLY: ``vocal_band_masking_count``
   appears in the summary ONLY when >= 1 such event exists (the
   ``score_nudges`` evidence-key discipline), so the summary of every
   current fixture is byte-identical. Moderate-tier events land in
   ``moderate_count`` (they ARE moderate); ``critical_count`` never moves.

THE CREATIVE FIX: ``_lead_masked`` derives the lead's NAME from record
identity (``instrument_identity == "lead_vocal"``) and matches events
containing THAT name — the substring '"vocal" in element' match is gone, so
a lead-free vocal-named event (and the entire new classification) can never
falsely trigger the masked-lead gate, while a genuine lead event (whatever
the lead is named) still does.
"""

from __future__ import annotations

import copy
import json

import pytest

from logic_mix_os import creative
from logic_mix_os.analyzers.masking_analyzer import (
    VOCAL_MASKER_IDENTITIES,
    analyze_masking,
)
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import analyze
from logic_mix_os.planners.logic_action_generator import generate_logic_actions
from logic_mix_os.planners.next_pass_planner import plan_next_pass
from logic_mix_os.project import load_manifest

from conftest import FIXTURE_NAMES, ROOT
from test_vocal_type import (
    BASE_COMPONENT_SCORES,
    JUDGMENT_WORDS,
    _chop,
    _constants,
    _lead,
    _mask,
    _piano,
    _rec,
    _stack,
    _vband,
)

BLEND_LINE = "accepted as blend under profile policy"

# Same stems, two judgments — the P-032i pinned overalls, re-asserted on THIS
# tree: the analyzer capacity moved neither producer's doctrine surface.
PINNED_OVERALLS = {
    "simple_vocal_piano_song": {"halee_ramone": 73.8, "timbaland": 68.4},
    "dense_chorus_with_loops": {"halee_ramone": 70.7, "timbaland": 52.6},
    "splice_loop_problem": {"halee_ramone": 74.3, "timbaland": 49.7},
}

# The pre-P-034 summary key set — every fixture's summary must keep exactly
# this shape (the conditional count key never appears without events).
BASE_SUMMARY_KEYS = {"critical_count", "moderate_count", "blend_count", "total_events"}


# --------------------------------------------------------------------------- #
# Record builders (pipeline-shaped, via the shared test_vocal_type helpers).
# --------------------------------------------------------------------------- #
def _fwd_chop() -> dict:
    """A FORWARD percussive chop (the emission gate needs the stem forward):
    transient-dense, defined hits, chop source -> vocal_percussive 0.95."""
    return _rec("Vox Chops", depth="foreground", role="heard", width=0.2,
                td=0.8, crest=16.0, presence=0.18, source="splice_sample")


def _fwd_backing(name: str = "BV Double") -> dict:
    """A second FORWARD non-lead vocal stem (backing identity) for the
    vocal-vs-vocal decision pin."""
    return _rec(name, depth="foreground", role="heard", width=0.6,
                td=0.2, crest=9.0, presence=0.2, source="comped_audio_track")


def _synth(depth: str = "foreground", role: str = "heard",
           presence: float = 0.2, name: str = "Synth Lead") -> dict:
    return _rec(name, identity="synth", family="synth", depth=depth,
                role=role, width=0.4, td=0.3, crest=10.0, presence=presence)


def _vband_events(report: dict) -> list:
    return [e for e in report["events"] if e["classification"] == "vocal_band_masking"]


def _ref_vrf(records, events, policy=None):
    prof = load_profile("halee_ramone")
    return doctrine_engine._vocal_role_fit(
        records, events, prof.doctrine,
        policy if policy is not None else prof.vocal_blend_policy,
    )


@pytest.fixture(scope="module")
def tim_analyzed():
    """The full pipeline once per fixture with ``producer="timbaland"`` —
    the second producer of the byte-identity obligation."""
    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="timbaland"
        )
    return results


# --------------------------------------------------------------------------- #
# 1. EMISSION (unit) — fire / no-fire / severity / lead-never-present / wording.
# --------------------------------------------------------------------------- #
def test_forward_nonlead_vocal_vs_forward_heard_element_fires():
    """The conflict tier: a forward chop and a forward/heard synth overlap in
    the presence band (0.18 >= 0.1) -> ONE ``vocal_band_masking`` event with
    elements [vocal_stem, other], severity moderate, the honest overlap."""
    report = analyze_masking([_lead(), _fwd_chop(), _synth()], [])
    vband = _vband_events(report)
    assert len(vband) == 1
    e = vband[0]
    assert e["elements"] == ["Vox Chops", "Synth Lead"]
    assert e["severity"] == "moderate"
    assert e["overlap"] == 0.18
    assert e["section"] == "full"
    assert e["frequency_range"] == "1.5kHz-4kHz"


def test_severity_is_capped_at_moderate_never_critical():
    """DESIGN DECISION 3, pinned: the overlap (0.18) is over the lead
    pathway's 0.16 critical tier, yet the non-lead event stays moderate —
    and ``critical_count`` counts only the lead pathway's own events."""
    report = analyze_masking([_fwd_chop(), _synth()], [])
    vband = _vband_events(report)
    assert vband and all(e["severity"] == "moderate" for e in vband)
    assert not any(
        e["severity"] == "critical" for e in report["events"]
        if e["classification"] == "vocal_band_masking"
    )
    assert report["summary"]["critical_count"] == 0


def test_below_overlap_floor_no_event():
    report = analyze_masking([_fwd_chop(), _synth(presence=0.04)], [])
    assert _vband_events(report) == []


def test_non_forward_other_reads_info_tier():
    """The sub-conflict mirror of the lead pathway's blend reading: the other
    element sits midground/felt -> same classification, severity ``info``."""
    report = analyze_masking(
        [_fwd_chop(), _synth(depth="midground", role="felt", presence=0.09)], [])
    vband = _vband_events(report)
    assert len(vband) == 1
    assert vband[0]["severity"] == "info"
    assert vband[0]["overlap"] == 0.09


def test_buried_vocal_stem_emits_nothing():
    """DESIGN DECISION 1, pinned: the non-lead vocal stem must itself sit
    FORWARD (the exact mirror of the lead gate). A background chop under a
    forward synth emits NO event in this packet — the buried-vocal question
    is deferred to P-035's real fixture."""
    report = analyze_masking([_lead(), _chop(), _synth()], [])
    assert _vband_events(report) == []


def test_lead_is_never_in_a_vocal_band_event_and_never_generates_one():
    """The binding lead exclusion, both directions: no ``vocal_band_masking``
    event ever contains the lead's name, and a project whose only vocal is
    the lead emits none at all (the lead's own conflicts stay
    ``bad_masking``, untouched)."""
    report = analyze_masking([_lead(), _fwd_chop(), _synth()], [])
    for e in _vband_events(report):
        assert "Lead Vocal" not in e["elements"]
    # The lead's own conflict with the same synth is the bad_masking pathway.
    assert any(
        e["classification"] == "bad_masking" and "Lead Vocal" in e["elements"]
        for e in report["events"]
    )
    lead_only = analyze_masking([_lead(), _synth()], [])
    assert _vband_events(lead_only) == []


def test_vocal_vs_vocal_pairs_do_not_fire():
    """DESIGN DECISION 2, pinned: two forward non-lead vocal stems with real
    presence overlap emit NO vocal_band_masking event between them — vocal
    layering reads as arrangement, not masking (and no [A,B]/[B,A] double
    count exists)."""
    report = analyze_masking([_fwd_chop(), _fwd_backing()], [])
    assert _vband_events(report) == []


def test_masker_set_is_the_lead_pathways_set():
    """The shared instrument-set constant: one basis, never forked. The lead
    pathway's literal set is now the module constant both pathways read."""
    assert VOCAL_MASKER_IDENTITIES == {
        "piano", "electric_piano", "organ", "acoustic_guitar",
        "electric_guitar", "synth", "backing_vocal", "strings",
    }
    # A non-member forward/heard element (kick) never fires the new pathway.
    kick = _rec("Kick", identity="kick", family="drums", depth="foreground",
                role="structural", presence=0.2)
    report = analyze_masking([_fwd_chop(), kick], [])
    assert _vband_events(report) == []


def test_multiple_maskers_multiple_events_and_honest_summary():
    """Two forward/heard maskers -> two events; the summary counts the new
    classification (conditional key) and the moderate tier honestly."""
    piano = _rec("Grand Piano", identity="piano", family="keys",
                 depth="foreground", role="heard", presence=0.15)
    report = analyze_masking([_fwd_chop(), _synth(), piano], [])
    vband = _vband_events(report)
    assert len(vband) == 2
    s = report["summary"]
    assert s["vocal_band_masking_count"] == 2
    assert s["moderate_count"] == 2
    assert s["critical_count"] == 0
    assert s["total_events"] == len(report["events"])


def test_summary_key_absent_without_events():
    """DESIGN DECISION 5, pinned: no events -> no key. The summary of a
    project without non-lead vocal stems keeps the exact pre-P-034 shape."""
    report = analyze_masking([_lead(), _piano()], [])
    assert "vocal_band_masking_count" not in report["summary"]
    assert set(report["summary"].keys()) == BASE_SUMMARY_KEYS


def test_per_track_masking_risk_is_untouched_by_the_new_classification():
    """DESIGN DECISION 4, pinned: the new events contribute NOTHING to
    ``per_track_masking_risk`` (risk feeds track_analysis, consumed broadly;
    P-035 revisits consciously). The lead is midground here so no
    bad_masking risk exists either — every track's risk stays 0.0 while the
    vocal_band event fires."""
    records = [_lead(depth="midground"), _fwd_chop(), _synth()]
    report = analyze_masking(records, [])
    assert _vband_events(report)  # the new event genuinely fired
    assert all(v == 0.0 for v in report["per_track_masking_risk"].values())


def test_emission_wording_is_observational_and_philosophy_neutral():
    """USER-MANDATED language: both tiers report the overlap observationally
    (zero judgment words) and the recommendation prescribes NOTHING — the
    profile decides what masking of this class means."""
    report = analyze_masking(
        [_fwd_chop(), _synth(),
         _synth(depth="midground", role="felt", presence=0.09, name="Soft Pad")],
        [],
    )
    vband = _vband_events(report)
    assert {e["severity"] for e in vband} == {"moderate", "info"}
    for e in vband:
        blob = (e["reason"] + " " + e["recommendation"]).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in: {blob}"
        assert "no action is prescribed" in e["recommendation"].lower()
        assert "producer-profile decision" in e["recommendation"].lower()
        assert f"{e['overlap']:.2f}" in e["reason"]


def test_emission_is_deterministic_and_does_not_mutate_inputs():
    records = [_lead(), _fwd_chop(), _synth()]
    sections = [{"section_id": "verse_1"}, {"section_id": "chorus_1"}]
    records_before = copy.deepcopy(records)
    sections_before = copy.deepcopy(sections)
    outs = {json.dumps(analyze_masking(records, sections), sort_keys=True)
            for _ in range(3)}
    assert len(outs) == 1
    assert records == records_before
    assert sections == sections_before
    # Two sections -> the per-section emission mirrors the lead pathway.
    report = analyze_masking(records, sections)
    assert [e["section"] for e in _vband_events(report)] == ["verse_1", "chorus_1"]


def test_no_aliasing_between_runs():
    """Consecutive runs share no state: mutating one report's event leaves
    the next run's output byte-identical."""
    records = [_fwd_chop(), _synth()]
    first = analyze_masking(records, [])
    pristine = copy.deepcopy(first)
    first["events"][0]["elements"].append("Injected")
    assert analyze_masking(records, []) == pristine


# --------------------------------------------------------------------------- #
# 2. BYTE-IDENTITY — 3 fixtures x both producers, every surface, 68/68.
# --------------------------------------------------------------------------- #
def test_no_new_events_on_any_fixture_under_either_producer(analyzed, tim_analyzed):
    """The fixture-inert guarantee, at the masking_report surface: zero
    ``vocal_band_masking`` events, the exact pre-P-034 summary shape, and no
    trace of the new vocabulary in the serialized artifact — both producers,
    all three fixtures."""
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            report = results[name].masking_report
            assert _vband_events(report) == [], name
            assert set(report["summary"].keys()) == BASE_SUMMARY_KEYS, name
            assert "vocal_band_masking" not in json.dumps(report, sort_keys=True)


def test_doctrine_surface_byte_identical_both_producers(analyzed, tim_analyzed):
    """Every pinned doctrine value holds on this tree: the reference's 13
    component anchors + overall (test_vocal_type's pin set) and both
    producers' P-032i overalls."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, (name, key)
        assert ds["overall_mix_readiness_score"] == PINNED_OVERALLS[name]["halee_ramone"]
        tim_ds = tim_analyzed[name].doctrine_score
        assert tim_ds["overall_mix_readiness_score"] == PINNED_OVERALLS[name]["timbaland"]


def test_p032i_no_vocal_blend_delta_pin_still_stands(analyzed, tim_analyzed):
    """THE P-032i PIN, NOT FLIPPED HERE: ``vocal_role_fit_score`` is still
    85.0 under BOTH producers on all three fixtures — the analyzer CAN now
    emit the events the blend policy reads, but no current fixture has a
    non-lead vocal stem, so the differential stays dormant until P-035's
    fixture makes it real (the conscious flip lives there)."""
    for name in FIXTURE_NAMES:
        assert analyzed[name].doctrine_score["vocal_role_fit_score"] == 85.0
        assert tim_analyzed[name].doctrine_score["vocal_role_fit_score"] == 85.0


def test_creative_surface_carries_no_new_vocabulary(analyzed, tim_analyzed):
    """The creative surface under both producers is untouched by the new
    classification (the full reference pin is re-asserted by
    test_vocal_type.test_creative_surface_is_byte_identical_to_base_capture
    on this same tree)."""
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            blob = json.dumps(results[name].creative, sort_keys=True)
            assert "vocal_band_masking" not in blob


def test_plan_surfaces_carry_no_new_vocabulary(analyzed, tim_analyzed):
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            blob = json.dumps(results[name].mix_plan, sort_keys=True)
            assert "vocal_band_masking" not in blob


def test_regression_still_sixty_eight_of_sixty_eight():
    """The golden corpus — fixture-inert packet: 68/68, goldens unchanged."""
    from logic_mix_os.regression import run_regression_suite

    report = run_regression_suite(ROOT / "fixtures")
    assert report["tests_run"] == 68
    assert report["passed"] == 68
    assert report["failed"] == 0


# --------------------------------------------------------------------------- #
# 3. CONSUMPTION — the vocal-role surface keys on the new classification.
# --------------------------------------------------------------------------- #
def test_reference_policy_reads_reduced_fit_on_the_new_classification():
    """halee_ramone (flag false): a qualified chop's vocal_band_masking
    involvement reads under full clarity protection — the penalty."""
    c = _constants()
    chop = _chop()
    score, ev = _ref_vrf([_lead(), chop], [_vband(chop["name"], "Synth Lead")])
    assert score == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
    assert any("clarity protection" in e.lower() for e in ev)
    assert not any(BLEND_LINE in e for e in ev)


def test_timbaland_real_policy_accepts_the_blend():
    """The REAL opted-in profile's authored policy: the same event is
    accepted as blend — no penalty, the acceptance visible."""
    c = _constants()
    chop = _chop()
    tim_policy = load_profile("timbaland").vocal_blend_policy
    assert tim_policy["acceptable_blend"] is True
    score, ev = _ref_vrf([_lead(), chop],
                         [_vband(chop["name"], "Synth Lead")], policy=tim_policy)
    assert score == doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    assert any(BLEND_LINE in e for e in ev)


def test_info_tier_is_not_a_masking_involvement_under_either_policy():
    """The severity-tier decision, pinned: an ``info`` vocal_band event (the
    controlled-overlap reading) neither penalizes nor reaches the blend gate
    — under both philosophies."""
    c = _constants()
    chop = _chop()
    clear = doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    for policy in (load_profile("halee_ramone").vocal_blend_policy,
                   load_profile("timbaland").vocal_blend_policy):
        score, ev = _ref_vrf(
            [_lead(), chop],
            [_vband(chop["name"], "Soft Pad", severity="info")], policy=policy)
        assert score == clear
        assert not any(BLEND_LINE in e for e in ev)
        assert not any("clarity protection" in e.lower() for e in ev)


def test_lead_free_bad_masking_no_longer_reaches_the_non_lead_pathway():
    """THE CONSCIOUS RE-KEYING, pinned: the old synthetic construction (a
    lead-free ``bad_masking`` event — a shape production code never emits)
    is no longer read by the non-lead pathway; the honest classification
    is."""
    c = _constants()
    chop = _chop()
    clear = doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    old_shape, _ = _ref_vrf([_lead(), chop], [_mask(chop["name"], "Synth Lead")])
    new_shape, _ = _ref_vrf([_lead(), chop], [_vband(chop["name"], "Synth Lead")])
    assert old_shape == clear
    assert new_shape == doctrine_engine._clamp(clear - c["masked_penalty"])


def test_lead_pathway_still_keys_on_bad_masking_only():
    """The lead reading is untouched: a lead-inclusive ``bad_masking`` event
    penalizes exactly as before, and a hand-built lead-named
    ``vocal_band_masking`` event (which the analyzer never emits) does NOT
    move the lead reading."""
    c = _constants()
    genuine, _ = _ref_vrf([_lead(), _piano()], [_mask("Lead Vocal", "Piano")])
    assert genuine == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])
    adversarial, _ = _ref_vrf([_lead(), _piano()],
                              [_vband("Lead Vocal", "Piano")])
    assert adversarial == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"])


def test_full_wire_differential_through_score_doctrine_real_profiles():
    """The two REAL profiles' authored philosophies genuinely differ on the
    new classification: same records, same synthetic event — halee_ramone
    reads reduced fit (75.0), timbaland accepts the blend (85.0); the
    lead-protection scorers are identical, policy-blind."""
    records = [_lead(), _chop()]
    masking = {"events": [_vband("Vox Chops", "Synth Lead")]}
    ref = doctrine_engine.score_doctrine(
        records, [], masking, None, profile=load_profile("halee_ramone"))
    tim = doctrine_engine.score_doctrine(
        records, [], masking, None, profile=load_profile("timbaland"))
    assert ref["vocal_role_fit_score"] == 75.0
    assert tim["vocal_role_fit_score"] == 85.0
    assert ref["emotional_hierarchy_score"] == tim["emotional_hierarchy_score"]
    assert ref["vocal_centrality_score"] == tim["vocal_centrality_score"]


# --------------------------------------------------------------------------- #
# 4. THE CREATIVE FIX — identity-derived lead-name matching, both directions.
# --------------------------------------------------------------------------- #
def test_lead_free_vocal_named_event_does_not_trigger_lead_masked(analyzed):
    """DIRECTION 1: a lead-free ``bad_masking`` event whose element names
    contain the SUBSTRING 'vocal' (the old predicate's false trigger) and a
    ``vocal_band_masking`` event both leave the masked-lead gate closed."""
    res = copy.deepcopy(analyzed["dense_chorus_with_loops"])
    assert creative._lead_masked(res) is False
    res.masking_report["events"].append({
        "classification": "bad_masking",
        "elements": ["Backing Vocal Stack", "Synth Lead"],
        "severity": "moderate",
    })
    res.masking_report["events"].append(
        _vband("Vox Chops", "Synth Lead"))
    assert creative._lead_masked(res) is False


def test_genuine_lead_event_still_triggers_lead_masked(analyzed):
    """DIRECTION 2: a real lead-inclusive ``bad_masking`` event still opens
    the gate (the P-032g/f masked-lead override tests re-prove the full
    plan-surface consequences on this same tree, untouched)."""
    res = copy.deepcopy(analyzed["dense_chorus_with_loops"])
    res.masking_report["events"].append({
        "classification": "bad_masking",
        "elements": ["Lead Vocal", "Rhythm Guitar"],
        "severity": "critical",
    })
    assert creative._lead_masked(res) is True


def test_lead_match_is_identity_derived_not_name_derived(analyzed):
    """THE SHARP PROOF: rename the lead record to a name WITHOUT the 'vocal'
    substring — a bad_masking event carrying that name still triggers the
    gate (the old substring predicate could not see it)."""
    res = copy.deepcopy(analyzed["dense_chorus_with_loops"])
    lead = next(r for r in res.records if r["instrument_identity"] == "lead_vocal")
    lead["name"] = "The Voice"
    res.masking_report["events"].append({
        "classification": "bad_masking",
        "elements": ["The Voice", "Piano"],
        "severity": "critical",
    })
    assert creative._lead_masked(res) is True


def test_new_classification_never_reaches_the_nudge_layer(analyzed):
    """Even an adversarial lead-NAMED ``vocal_band_masking`` event (which the
    analyzer never emits) cannot fire the masked-lead nudge — the
    classification filter holds; no ``score_nudges`` key appears."""
    res = copy.deepcopy(analyzed["dense_chorus_with_loops"])
    res.masking_report["events"].append(_vband("Lead Vocal", "Synth Lead"))
    assert creative._lead_masked(res) is False
    variant = {"variant_id": "v", "kind": "vocal_ride", "name": "v", "changes": []}
    scores = creative.score_variant(variant, res)
    assert "score_nudges" not in scores


# --------------------------------------------------------------------------- #
# 5. IMMOVABILITY — a synthetic event moves NO pinned consumer, NO plan.
# --------------------------------------------------------------------------- #
def _with_synthetic_vband(res):
    r = copy.deepcopy(res)
    r.masking_report["events"].append(_vband("Vox Chops", "Synth Lead"))
    return r


def test_immovable_scorers_ignore_the_new_classification(analyzed):
    """Each pinned scorer, called directly with and without a synthetic
    ``vocal_band_masking`` event: byte-identical readings."""
    res = analyzed["dense_chorus_with_loops"]
    doctrine = load_profile("halee_ramone").doctrine
    lead = next(r for r in res.records if r["instrument_identity"] == "lead_vocal")
    base = res.masking_report["events"]
    extra = base + [_vband("Vox Chops", "Synth Lead")]
    report_extra = {**res.masking_report, "events": extra}

    w1, w2 = [], []
    assert doctrine_engine._emotional_hierarchy(res.records, lead, base, w1, doctrine) \
        == doctrine_engine._emotional_hierarchy(res.records, lead, extra, w2, doctrine)
    assert w1 == w2
    assert doctrine_engine._vocal_centrality(lead, base, doctrine) \
        == doctrine_engine._vocal_centrality(lead, extra, doctrine)
    assert doctrine_engine._static_mix(res.records, lead, base, res.mix_metrics, doctrine) \
        == doctrine_engine._static_mix(res.records, lead, extra, res.mix_metrics, doctrine)
    assert doctrine_engine._physical_space(res.records, base, doctrine) \
        == doctrine_engine._physical_space(res.records, extra, doctrine)
    assert doctrine_engine._beat_identity(res.records, base, doctrine) \
        == doctrine_engine._beat_identity(res.records, extra, doctrine)
    assert doctrine_engine._loop_context(res.records, res.section_analysis,
                                         res.masking_report, doctrine) \
        == doctrine_engine._loop_context(res.records, res.section_analysis,
                                         report_extra, doctrine)


def test_full_doctrine_surface_unmoved_by_a_synthetic_event(analyzed):
    """The whole ``score_doctrine`` dict — every component, evidence list,
    warning and the overall — is identical with the synthetic event present
    (the fixture has no non-lead vocal stems, so even vocal_role_fit cannot
    read it)."""
    res = analyzed["dense_chorus_with_loops"]
    extra_report = {**res.masking_report,
                    "events": res.masking_report["events"]
                    + [_vband("Vox Chops", "Synth Lead")]}
    base = doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report,
        res.mix_metrics, res.project.intent, groove=res.expanded["groove"])
    with_event = doctrine_engine.score_doctrine(
        res.records, res.section_analysis, extra_report,
        res.mix_metrics, res.project.intent, groove=res.expanded["groove"])
    assert with_event == base


def test_no_plan_actions_from_the_new_classification(analyzed):
    """The planners are immovable: logic actions and the next pass are
    byte-identical with the synthetic event present — the new classification
    generates NO action anywhere."""
    res = analyzed["dense_chorus_with_loops"]
    extra_report = {**res.masking_report,
                    "events": res.masking_report["events"]
                    + [_vband("Vox Chops", "Synth Lead")]}
    assert generate_logic_actions(res.records, extra_report) \
        == generate_logic_actions(res.records, res.masking_report)
    assert plan_next_pass(res.records, res.doctrine_score, extra_report,
                          res.section_analysis) \
        == plan_next_pass(res.records, res.doctrine_score, res.masking_report,
                          res.section_analysis)


def test_creative_surface_unmoved_by_a_synthetic_event(analyzed):
    """The full creative engine on a result carrying the synthetic event is
    byte-identical (the event is lead-free, so no nudge evidence changes)."""
    res = analyzed["dense_chorus_with_loops"]
    base = creative.run_creative_engine(res, res.creative["search_mode"])
    with_event = creative.run_creative_engine(
        _with_synthetic_vband(res), res.creative["search_mode"])
    assert with_event == base


# --------------------------------------------------------------------------- #
# 6. NO-ALIASING + OBSERVATIONAL LANGUAGE (the established guards).
# --------------------------------------------------------------------------- #
def test_axis_does_not_mutate_with_new_classification_events():
    records = [_lead(), _chop(), _stack()]
    records_before = copy.deepcopy(records)
    events = [_vband("Vox Chops", "Synth Lead"),
              _vband("BV Stack", "Soft Pad", severity="info"),
              _mask("Lead Vocal", "Piano")]
    events_before = copy.deepcopy(events)
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    for policy in (load_profile("halee_ramone").vocal_blend_policy,
                   load_profile("timbaland").vocal_blend_policy):
        doctrine_engine._vocal_role_fit(records, events, doctrine, policy)
    assert records == records_before
    assert events == events_before
    assert doctrine == doctrine_before


def test_axis_evidence_language_with_new_events_is_observational():
    records = [_lead(), _chop(), _stack()]
    events = [_vband("Vox Chops", "Synth Lead"), _vband("BV Stack", "Synth Lead")]
    for policy in (load_profile("halee_ramone").vocal_blend_policy,
                   load_profile("timbaland").vocal_blend_policy, None):
        _, ev = _ref_vrf(records, events, policy=policy)
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in evidence: {blob}"
