"""P-032f Commit-2 — the profile-gated acceptable-blend rule:
``vocal_blend_policy`` + ``accepted_blend_under_policy``.

THE USER'S APPROVED RULE (verbatim, binding)::

    lead or uncertain            -> protect clarity (full lead-grade protection)
    hook_candidate               -> protect impact/clarity unless a profile
                                    explicitly says otherwise LATER (NOT this packet)
    chop/stutter/adlib or stack
      + profile opt-in
      + confidence threshold met -> acceptable blend MAY apply

Decision 1 (B): blend is PROFILE-AUTHORED — a REQUIRED top-level field
(the P-032g ``protect_iconic_loops`` pattern), so every producer's masking
philosophy is explicit in its JSON, never silently defaulted. Halee/Ramone
declares ``acceptable_blend: false`` and stays byte-identical on BOTH
surfaces. Decision 2 (stricter): UNCERTAIN is never blend-eligible, below
the profile's explicit ``confidence_floor`` is never blend-eligible —
misclassification fails CLOSED toward vocal protection.

WHERE THE RULE BITES (scouted honestly): masking-as-fault for a chop/stack
vocal manifests in the ``vocal_role_fit`` doctrine axis — the ONE surface
that reads a non-lead vocal's OWN masking involvement. Every OTHER
manifestation of vocal-band masking in the engine (the ``_ramone`` /
``_vocal_centrality`` penalties, the creative ``lead_masked`` nudges, the
action-generator presence-band carve, per-track masking risk) is the
MASKED-LEAD pathway — the current masking analyzer emits vocal-band events
only against the lead — and the user's safety rails place that pathway
beyond profile authority, so the gate cannot bite there BY DESIGN. Inside
the axis the separation is structural: events including a lead stem belong
to the lead reading and are never offered to the gate.

THE SIX USER-MANDATED ADVERSARIAL ATTACKS (any success = must-fix) are each
attempted below and must FAIL:

1. an uncertain vocal gets acceptable-blend treatment;
2. a lead is misread as percussion and loses protection;
3. Halee/Ramone creative recommendations drift before ``timbaland.json``;
4. the profile field is omitted and silently defaults;
5. acceptable blend activates without the confidence threshold;
6. hook_candidate gets buried without explicit profile authority.

Plus positive liveness (opt-in + qualified chop/stack + above floor → blend
applies, visible in the gated surface; the A/B flag flip is the lever) and
the masked-lead override guard (opt-in changes NOTHING on the lead pathway).
"""

from __future__ import annotations

import copy
import dataclasses
import json
import pathlib

import pytest

from logic_mix_os.analyzers.vocal_type_classifier import (
    BLEND_ELIGIBLE_TYPES,
    accepted_blend_under_policy,
    classify_vocal_type,
)
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import (
    _REQUIRED_DATA_FIELDS,
    _validate,
    load_profile,
)
from test_vocal_type import (
    FIXTURE_NAMES,
    JUDGMENT_WORDS,
    _chop,
    _constants,
    _hook,
    _lead,
    _mask,
    _piano,
    _rec,
    _stack,
)

_ROOT = pathlib.Path(__file__).resolve().parent.parent

BLEND_LINE = "accepted as blend under profile policy"


def _policy(optin: bool = True, floor: float = 0.75) -> dict:
    return {"acceptable_blend": optin, "confidence_floor": floor}


def _vrf(records, events=None, policy=None, doctrine=None):
    doctrine = doctrine or load_profile("halee_ramone").doctrine
    return doctrine_engine._vocal_role_fit(records, events or [], doctrine, policy)


def _blend_profile(optin: bool = True, floor: float = 0.75, weight: float = 0.0):
    """A halee_ramone copy whose ONLY changes are the blend policy (and,
    optionally, a non-zero vocal_role_fit weight) — any behavior delta is
    attributable to exactly those levers."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    if weight:
        doctrine["weights"]["vocal_role_fit_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine,
                               vocal_blend_policy=_policy(optin, floor))


def _below_floor_chop() -> dict:
    """A REAL classifier reading below the reference floor: transient-dense +
    defined but from a live source (2 of 3 supporting signals → 0.667 <
    0.75). Not hand-set — the honest below-threshold construction."""
    r = _rec("Live Vox Chops", depth="background", role="felt", width=0.2,
             td=0.8, crest=16.0, presence=0.18, source="live_audio_recording")
    assert r["vocal_type"] == "vocal_percussive"
    assert r["vocal_type_confidence"] == 0.667
    return r


# --------------------------------------------------------------------------- #
# 1. THE FIELD — required, explicit, structurally validated (P-032g pattern).
# --------------------------------------------------------------------------- #
def test_halee_ramone_declares_blend_false_with_explicit_floor():
    """The reference profile's authored philosophy: NO acceptable blend
    (current behavior, byte-identical), with the explicit confidence floor
    already declared for any later opt-in profile to inherit the shape."""
    p = load_profile("halee_ramone")
    assert p.vocal_blend_policy == {"acceptable_blend": False, "confidence_floor": 0.75}


def test_field_is_in_the_required_data_fields():
    assert "vocal_blend_policy" in _REQUIRED_DATA_FIELDS


def test_attack_4_omitted_field_is_rejected_never_silently_defaulted():
    """ATTACK 4 (must fail): a profile JSON without ``vocal_blend_policy``
    is structurally invalid — the loader REJECTS it. The masking philosophy
    must be explicit in every producer's JSON."""
    raw = json.load(open(
        _ROOT / "logic_mix_os" / "doctrine" / "producers" / "halee_ramone.json",
        encoding="utf-8",
    ))
    del raw["vocal_blend_policy"]
    with pytest.raises(ValueError, match="vocal_blend_policy"):
        _validate(raw, "halee_ramone")


def test_policy_structure_is_validated():
    """The declared shape is enforced: a dict with an explicit bool opt-in
    and a real confidence floor in [0, 1]."""
    def raw_with(policy):
        raw = json.load(open(
            _ROOT / "logic_mix_os" / "doctrine" / "producers" / "halee_ramone.json",
            encoding="utf-8",
        ))
        raw["vocal_blend_policy"] = policy
        return raw

    for broken in (
        "false",                                            # not an object
        {"acceptable_blend": False},                        # missing floor
        {"confidence_floor": 0.75},                         # missing flag
        {"acceptable_blend": "no", "confidence_floor": 0.75},   # non-bool flag
        {"acceptable_blend": False, "confidence_floor": 1.5},   # out of range
        {"acceptable_blend": False, "confidence_floor": -0.1},  # out of range
        {"acceptable_blend": False, "confidence_floor": True},  # bool floor
        {"acceptable_blend": False, "confidence_floor": "0.75"},  # str floor
    ):
        with pytest.raises(ValueError, match="vocal_blend_policy"):
            _validate(raw_with(broken), "halee_ramone")


# --------------------------------------------------------------------------- #
# 2. THE SIX ADVERSARIAL ATTACKS — each must FAIL (the defense holds).
# --------------------------------------------------------------------------- #
def test_attack_1_uncertain_never_blends_even_with_high_stated_confidence():
    """ATTACK 1 (must fail): uncertain + opt-in + a stated 0.99 confidence.
    Uncertain is CATEGORICALLY ineligible — the type gate refuses before any
    confidence comparison (Decision 2: uncertainty protects the vocal)."""
    uncertain = _rec("Ad Lib", td=0.45, width=0.2, role="felt", presence=0.1)
    assert uncertain["vocal_type"] == "vocal_uncertain"
    uncertain["vocal_type_confidence"] = 0.99  # the adversarial hand-set

    assert accepted_blend_under_policy(uncertain, _policy(optin=True, floor=0.75)) is False

    c = _constants()
    events = [_mask(uncertain["name"], "Synth Lead")]
    score, ev = _vrf([_lead(), uncertain], events=events, policy=_policy(True))
    assert score == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
    assert not any(BLEND_LINE in e for e in ev)
    assert any("clarity protection" in e.lower() for e in ev)


def test_attack_2_lead_protection_holds_both_ways():
    """ATTACK 2 (must fail): a lead misread as percussion loses protection.
    Arm 1 — the classifier: lead IDENTITY with fully percussive physics is
    still ``vocal_lead`` (identity wins; physics never demote the lead).
    Arm 2 — the gate: even a hand-FORCED percussive type + 0.99 confidence
    on a lead-identity stem is refused on identity, before the type read."""
    misread = _rec("Lead Vocal", identity="lead_vocal", depth="foreground",
                   role="heard", width=0.1, td=0.9, crest=18.0, presence=0.2,
                   source="splice_sample")
    assert misread["vocal_type"] == "vocal_lead"          # arm 1: identity wins

    forced = dict(misread, vocal_type="vocal_percussive", vocal_type_confidence=0.99)
    assert accepted_blend_under_policy(forced, _policy(optin=True)) is False  # arm 2

    # And the axis keeps penalizing the challenged lead under full opt-in.
    c = _constants()
    events = [_mask("Lead Vocal", "Piano")]
    optin, _ = _vrf([_lead(), _piano()], events=events, policy=_policy(True))
    optout, _ = _vrf([_lead(), _piano()], events=events, policy=_policy(False))
    assert optin == optout == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])


def test_attack_3_halee_ramone_defaults_no_drift(analyzed):
    """ATTACK 3 (must fail): drift under the reference defaults before
    ``timbaland.json`` exists. Doctrine surface: the pinned overalls
    (73.8 / 70.7 / 74.3) hold and re-scoring under an explicitly-loaded
    halee_ramone profile is identical to production. Creative surface: the
    serialized ``result.creative`` never mentions the blend vocabulary, and
    the full pinned base capture is re-asserted by
    ``test_vocal_type.test_creative_surface_is_byte_identical_to_base_capture``
    on this same tree. The axis itself is identical between no-policy and
    the reference flag-false policy."""
    pinned_overall = {
        "simple_vocal_piano_song": 73.8,
        "dense_chorus_with_loops": 70.7,
        "splice_loop_problem": 74.3,
    }
    prof = load_profile("halee_ramone")
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        ds = res.doctrine_score
        assert ds["overall_mix_readiness_score"] == pinned_overall[name]
        assert not any(BLEND_LINE in e for e in ds["evidence"]["vocal_role_fit"])

        rescored = doctrine_engine.score_doctrine(
            res.records, res.section_analysis, res.masking_report,
            res.mix_metrics, res.project.intent, profile=prof,
            groove=res.expanded["groove"],
        )
        assert rescored == ds

        blob = json.dumps(res.creative, sort_keys=True)
        assert "blend under profile policy" not in blob
        assert "vocal_blend_policy" not in blob

    # Flag-false policy == no policy at all, on a masked qualified chop.
    events = [_mask("Vox Chops", "Synth Lead")]
    records = [_lead(), _chop()]
    assert _vrf(records, events=events, policy=None) == \
        _vrf(records, events=events, policy=prof.vocal_blend_policy)


def test_attack_5_below_threshold_never_blends():
    """ATTACK 5 (must fail): opt-in true but the stem's REAL classifier
    confidence (0.667) sits below the profile floor (0.75) — full lead-grade
    protection, no blend."""
    low = _below_floor_chop()
    assert accepted_blend_under_policy(low, _policy(optin=True, floor=0.75)) is False

    c = _constants()
    events = [_mask(low["name"], "Synth Lead")]
    score, ev = _vrf([_lead(), low], events=events, policy=_policy(True, 0.75))
    assert score == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
    assert not any(BLEND_LINE in e for e in ev)


def test_attack_6_hook_candidate_never_blends_without_explicit_authority():
    """ATTACK 6 (must fail): a hook_candidate buried as blend. Hook
    protection is NOT profile-authorable in this packet — the type gate
    refuses hook_candidate even at full opt-in and any confidence."""
    hook = _hook()
    assert hook["vocal_type"] == "vocal_hook_candidate"
    assert accepted_blend_under_policy(hook, _policy(optin=True)) is False
    forced = dict(hook, vocal_type_confidence=0.99)
    assert accepted_blend_under_policy(forced, _policy(optin=True)) is False

    c = _constants()
    events = [_mask(hook["name"], "Synth Lead")]
    score, ev = _vrf([_lead(), hook], events=events, policy=_policy(True))
    assert score == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
    assert not any(BLEND_LINE in e for e in ev)
    assert any("clarity protection" in e.lower() for e in ev)


# --------------------------------------------------------------------------- #
# 3. POSITIVE LIVENESS — the flag is a real, bounded lever.
# --------------------------------------------------------------------------- #
def test_blend_applies_for_qualified_chop_and_stack_under_optin():
    """The gated path, live: opt-in + a qualified (0.95 >= 0.75) chop or
    stack masked AWAY from the lead → the masking involvement is accepted as
    blend — no penalty, and the acceptance is visible in the evidence."""
    c = _constants()
    for stem in (_chop(), _stack()):
        assert stem["vocal_type"] in BLEND_ELIGIBLE_TYPES
        assert accepted_blend_under_policy(stem, _policy(True, 0.75)) is True
        events = [_mask(stem["name"], "Synth Lead")]
        score, ev = _vrf([_lead(), stem], events=events, policy=_policy(True))
        assert score == doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
        assert any(BLEND_LINE in e for e in ev)
        assert not any("clarity protection" in e.lower() for e in ev)


def test_confidence_exactly_at_the_floor_meets_the_threshold():
    """Threshold semantics, pinned: 'confidence threshold met' means
    ``confidence >= floor`` — a reading exactly AT the floor qualifies;
    anything below never does (attack 5)."""
    chop = _chop()
    assert accepted_blend_under_policy(chop, _policy(True, floor=0.95)) is True
    assert accepted_blend_under_policy(chop, _policy(True, floor=0.951)) is False


def test_flag_alone_is_the_lever():
    """THE A/B (user-mandated): identical records, identical events — the
    ONLY change is the profile's flag. False => clarity protection (the
    penalty); True => accepted blend (no penalty). The delta is exactly the
    masked_penalty, attributable to the authored decision alone."""
    c = _constants()
    records = [_lead(), _chop()]
    events = [_mask("Vox Chops", "Synth Lead")]
    off, ev_off = _vrf(records, events=events, policy=_policy(False))
    on, ev_on = _vrf(records, events=events, policy=_policy(True))
    assert on - off == c["masked_penalty"]
    assert any("clarity protection" in e.lower() for e in ev_off)
    assert any(BLEND_LINE in e for e in ev_on)


def test_blend_liveness_through_score_doctrine():
    """The full wire: ``score_doctrine`` under two profiles differing ONLY
    in the flag (both weighting vocal_role_fit non-zero) — the axis and the
    overall move; the lead-protection scorers (``_ramone`` /
    ``_vocal_centrality``) are identical, policy-blind."""
    records = [_lead(), _chop()]
    masking = {"events": [_mask("Vox Chops", "Synth Lead")]}
    off = doctrine_engine.score_doctrine(records, [], masking, None,
                                         profile=_blend_profile(False, weight=5.0))
    on = doctrine_engine.score_doctrine(records, [], masking, None,
                                        profile=_blend_profile(True, weight=5.0))
    assert on["vocal_role_fit_score"] > off["vocal_role_fit_score"]
    assert on["overall_mix_readiness_score"] > off["overall_mix_readiness_score"]
    assert on["ramone_score"] == off["ramone_score"]
    assert on["vocal_centrality_score"] == off["vocal_centrality_score"]


# --------------------------------------------------------------------------- #
# 4. THE MASKED-LEAD PATHWAY — never overridden, by construction.
# --------------------------------------------------------------------------- #
def test_masked_lead_pathway_is_never_overridden_by_optin():
    """SAFETY RAIL (user-mandated): when the ONLY masking is the lead's own
    event (lead + qualified stack in the same event), full opt-in changes
    NOTHING — score and evidence are identical to flag-false, the lead
    penalty stands, and no blend line appears. The lead pathway is
    structurally outside profile authority."""
    c = _constants()
    lead, stack = _lead(), _stack()
    events = [_mask(lead["name"], stack["name"])]
    off = _vrf([lead, stack], events=events, policy=_policy(False))
    on = _vrf([lead, stack], events=events, policy=_policy(True))
    assert on == off
    assert on[0] == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])
    assert not any(BLEND_LINE in e for e in on[1])
    assert any("challenged" in e.lower() for e in on[1])


def test_blend_never_relaxes_the_lead_reading_alongside_an_accepted_stem():
    """Mixed events: the lead is masked (its own event) AND a qualified chop
    is masked away from the lead. Opt-in accepts ONLY the chop's involvement;
    the lead's penalty stands at full strength in both worlds."""
    c = _constants()
    records = [_lead(), _chop()]
    events = [_mask("Lead Vocal", "Piano"), _mask("Vox Chops", "Synth Lead")]
    off, _ = _vrf(records, events=events, policy=_policy(False))
    on, ev_on = _vrf(records, events=events, policy=_policy(True))
    assert off == doctrine_engine._clamp(c["baseline"] - 2 * c["masked_penalty"])
    assert on == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])
    assert any("challenged" in e.lower() for e in ev_on)  # the lead reading stands
    assert any(BLEND_LINE in e for e in ev_on)


def test_lead_protection_surfaces_do_not_read_the_policy():
    """Structural proof the policy cannot reach the other lead-protection
    surfaces: neither ``_ramone`` nor ``_vocal_centrality`` (nor the creative
    ``_lead_masked`` predicate) accepts a blend-policy argument."""
    import inspect

    from logic_mix_os import creative

    assert "blend_policy" not in inspect.signature(doctrine_engine._ramone).parameters
    assert "blend_policy" not in inspect.signature(doctrine_engine._vocal_centrality).parameters
    assert "blend_policy" not in inspect.signature(creative._lead_masked).parameters


# --------------------------------------------------------------------------- #
# 5. FAIL-CLOSED EDGES + SHARED BASIS + NO-ALIASING + LANGUAGE.
# --------------------------------------------------------------------------- #
def test_gate_fails_closed_on_missing_or_malformed_policy():
    chop = _chop()
    for policy in (None, {}, {"acceptable_blend": True},               # no floor
                   {"acceptable_blend": True, "confidence_floor": "x"},
                   {"acceptable_blend": True, "confidence_floor": True},
                   {"acceptable_blend": 1, "confidence_floor": 0.75},  # non-True flag
                   "true"):
        assert accepted_blend_under_policy(chop, policy) is False


def test_gate_fails_closed_on_untyped_or_confidence_free_records():
    assert accepted_blend_under_policy(_piano(), _policy(True)) is False  # None type
    no_conf = dict(_chop(), vocal_type_confidence=None)
    assert accepted_blend_under_policy(no_conf, _policy(True)) is False


def test_gate_reads_the_record_fields_never_the_physics():
    """SHARED DETECTION BASIS: the gate consumes the classifier's record
    output only — it never re-classifies. Percussive physics with a forced
    uncertain type is refused; sustained physics with a (test-forced)
    qualified stack type passes. Only the FIELDS decide."""
    perc_physics_forced_uncertain = dict(
        _chop(), vocal_type="vocal_uncertain", vocal_type_confidence=0.95)
    assert accepted_blend_under_policy(
        perc_physics_forced_uncertain, _policy(True)) is False

    sustained_physics_typed_stack = dict(
        _rec("Soft Pad Vox", role="felt", width=0.1, td=0.1, presence=0.05),
        vocal_type="vocal_stack", vocal_type_confidence=0.9)
    assert accepted_blend_under_policy(
        sustained_physics_typed_stack, _policy(True)) is True


def test_gate_and_axis_do_not_mutate_policy_records_or_profile():
    policy = _policy(True)
    policy_before = copy.deepcopy(policy)
    records = [_lead(), _chop(), _stack()]
    records_before = copy.deepcopy(records)
    events = [_mask("Vox Chops", "Synth Lead"), _mask("Lead Vocal", "BV Stack")]
    events_before = copy.deepcopy(events)
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)

    for r in records:
        accepted_blend_under_policy(r, policy)
    doctrine_engine._vocal_role_fit(records, events, doctrine, policy)

    assert policy == policy_before
    assert records == records_before
    assert events == events_before
    assert doctrine == doctrine_before


def test_default_module_profile_untouched_by_optin_runs(analyzed):
    """Scoring under an opted-in profile leaves the module default profile
    (the byte-identity anchor) byte-unchanged, its policy included."""
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.vocal_blend_policy)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics,
        res.project.intent, profile=_blend_profile(True, weight=5.0),
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.vocal_blend_policy == before
    assert before == {"acceptable_blend": False, "confidence_floor": 0.75}


def test_blend_evidence_is_observational_zero_judgment_words():
    """USER-MANDATED language guard on the NEW evidence path: the accepted-
    blend reading (and its clarity-protection counterpart) contains zero
    judgment words."""
    records = [_lead(), _chop(), _stack()]
    events = [_mask("Vox Chops", "Synth Lead"), _mask("BV Stack", "Synth Lead")]
    for policy in (_policy(True), _policy(False), None):
        _, ev = _vrf(records, events=events, policy=policy)
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in evidence: {blob}"
