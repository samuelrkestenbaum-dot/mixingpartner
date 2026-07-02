"""P-032f Commit-1 — the binding guards for the vocal-role detection layer:
``vocal_type_classifier`` + the additive record fields + ``vocal_role_fit``,
the SEVENTH (and last) new producer-agnostic doctrine axis.

THE DOCTRINE PIN, vocal half (user-mandated architecture, 2026-07-01): **the
engine DETECTS vocal function; the profile decides masking philosophy.** The
classifier reads per-stem physics already on the pipeline record and emits an
OBSERVATIONAL function type — ``vocal_lead`` / ``vocal_hook_candidate`` /
``vocal_percussive`` / ``vocal_stack`` / ``vocal_uncertain`` — with a
confidence in [0, 1]. What a profile DOES with the reading (the acceptable-
blend rule) is Commit-2; nothing in this commit consults a profile for
detection.

THE FAIL-CLOSED MANDATE (Decision 2, stricter): weak or conflicting signals
are UNCERTAIN, never a guessed chop/stack — and a stem the identity detector
called ``lead_vocal`` is ALWAYS ``vocal_lead``, whatever its physics look
like (identity wins; a misread can never strip lead protection).

THE HONESTY CAP: the strongest hook claim is ``vocal_hook_candidate`` — a
PROVEN hook needs a recurrence/provenance signal that does not exist at
doctrine time. Deferred (with lyric meaning and per-onset stutter rate),
never faked.

It is wired at weight 0 for ``halee_ramone`` so the reference producer's
output stays BYTE-IDENTICAL on BOTH mandated surfaces: the doctrine score
surface (all 13 pre-existing components + overall — 73.8 / 70.7 / 74.3) and
the creative variant/promotion surface (the full pinned base capture).

Guard groups, mirroring the packet:

1. **Classifier discrimination + fail-closed + hook cap** (unit).
2. **Additive record fields** — every record carries ``vocal_type`` +
   ``vocal_type_confidence``; non-vocal stems carry EXPLICIT None.
3. **Byte-identity, BOTH surfaces** — doctrine pins + the full creative base
   capture + regression 68/68.
4. **Axis value-discrimination** (unit) — lead forward/clear high; lead
   masked low; non-lead vocal masking read observationally; the masked-lead
   pathway counted ONCE (through the lead reading, never re-read through the
   other stem).
5. **Observational language + honest deferrals** (user-mandated).
6. **Liveness / sabotage** — a non-zero weight makes the axis a real lever.
7. **No-aliasing** — the scorer reads, never mutates.
"""

from __future__ import annotations

import copy
import dataclasses
import json

import pytest

from logic_mix_os.analyzers.vocal_type_classifier import (
    VOCAL_TYPES,
    classify_vocal_type,
    is_vocal_record,
)
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile

# The thirteen pre-existing component score keys (the byte-identical anchor
# set): the seven originals + the six P-032.x axes already landed.
# vocal_role_fit_score is appended after these.
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
    "loop_context_score",
]

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# Pinned BASE values captured from the tree at P-032f's base (`89e792e`,
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
        "loop_context_score": 50.0,
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
        "loop_context_score": 15.0,
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
        "loop_context_score": 15.0,
        "overall_mix_readiness_score": 74.3,
    },
}

# The user's banned judgment vocabulary — the engine reads, it never rules.
JUDGMENT_WORDS = ("bad", "problem", "should", "fix", "better", "worse", "wrong")


# --------------------------------------------------------------------------- #
# Test helpers — pipeline-shaped synthetic records / events.
# --------------------------------------------------------------------------- #
def _rec(name: str, identity: str = "backing_vocal", family: str = "vocal",
         depth: str = "midground", role: str = "heard", width: float = 0.2,
         td: float = 0.2, crest: float = 10.0, presence: float = 0.2,
         source: str = "live_audio_recording", classify: bool = True) -> dict:
    """A synthetic per-track record shaped like the pipeline's, with the
    P-032f additive fields filled exactly the way ``pipeline.analyze`` fills
    them (classifier output, or explicit None for non-vocal stems)."""
    r = {
        "track_id": name.lower().replace(" ", "_"),
        "name": name,
        "instrument_identity": identity,
        "identity_family": family,
        "perceptual_role": role,
        "sacredness": "important",
        "source_kind": source,
        "depth_default": depth,
        "depth_by_section": {},
        "stereo_width": width,
        "band_energy": {},
        "vocal_presence_energy": presence,
        "brightness": 0.5,
        "metrics": {"transient_density": td, "crest_factor_db": crest},
        "source_warnings": [],
    }
    if classify:
        out = classify_vocal_type(r)
        r["vocal_type"] = out["vocal_type"] if out else None
        r["vocal_type_confidence"] = out["confidence"] if out else None
    return r


def _lead(depth: str = "intimate") -> dict:
    return _rec("Lead Vocal", identity="lead_vocal", depth=depth, role="heard",
                width=0.05, td=0.35, crest=9.0, presence=0.3,
                source="comped_audio_track")


def _chop() -> dict:
    """A full-strength percussive read: transient-dense, defined hits, chop
    source (3/3 supporting signals → confidence 0.95)."""
    return _rec("Vox Chops", depth="background", role="felt", width=0.2,
                td=0.8, crest=16.0, presence=0.18, source="splice_sample")


def _stack() -> dict:
    """A full-strength stack read: wide, sustained, backing identity (3/3
    supporting signals → confidence 0.95)."""
    return _rec("BV Stack", depth="background", role="felt", width=0.7,
                td=0.2, crest=9.0, presence=0.18, source="comped_audio_track")


def _hook() -> dict:
    """A full-strength hook-candidate read: forward, heard, presence-band
    energy, not transient-dense (4/4 supporting signals → 0.95)."""
    return _rec("Hook Vox", depth="foreground", role="heard", width=0.3,
                td=0.3, crest=10.0, presence=0.25, source="comped_audio_track")


def _piano() -> dict:
    return _rec("Piano", identity="piano", family="keys", role="heard",
                width=0.3, td=0.3, crest=12.0, presence=0.1)


def _mask(a: str, b: str) -> dict:
    return {
        "elements": [a, b],
        "frequency_range": "1.5kHz-4kHz",
        "section": "chorus_1",
        "classification": "bad_masking",
        "severity": "critical",
        "overlap": 0.2,
    }


def _vrf(records, events=None, doctrine=None):
    doctrine = doctrine or load_profile("halee_ramone").doctrine
    return doctrine_engine._vocal_role_fit(records, events or [], doctrine)


def _constants():
    return load_profile("halee_ramone").doctrine["scorers"]["vocal_role_fit"]


# --------------------------------------------------------------------------- #
# 1. CLASSIFIER — discrimination, fail-closed, identity-wins, the hook cap.
# --------------------------------------------------------------------------- #
def test_transient_dense_chop_reads_percussive_with_confidence():
    out = classify_vocal_type(_chop())
    assert out["vocal_type"] == "vocal_percussive"
    assert out["confidence"] == 0.95


def test_wide_sustained_backing_reads_stack_with_confidence():
    out = classify_vocal_type(_stack())
    assert out["vocal_type"] == "vocal_stack"
    assert out["confidence"] == 0.95


def test_forward_heard_sung_backing_reads_hook_candidate():
    out = classify_vocal_type(_hook())
    assert out["vocal_type"] == "vocal_hook_candidate"
    assert out["confidence"] == 0.95


def test_lead_identity_reads_vocal_lead_with_high_confidence():
    out = classify_vocal_type(_lead())
    assert out["vocal_type"] == "vocal_lead"
    assert out["confidence"] == 0.95


def test_identity_wins_percussive_physics_cannot_demote_the_lead():
    """FAIL-CLOSED (attack-2 shape, classifier arm): a lead-identity stem
    with fully percussive-looking physics — transient-dense, defined, chop
    source — is STILL ``vocal_lead``. Physics never demote the lead."""
    misread = _rec("Lead Vocal", identity="lead_vocal", depth="foreground",
                   role="heard", width=0.1, td=0.9, crest=18.0, presence=0.2,
                   source="splice_sample")
    out = classify_vocal_type(misread)
    assert out["vocal_type"] == "vocal_lead"
    assert out["confidence"] == 0.95


def test_weak_signals_fail_closed_to_uncertain():
    """One weak corroborating signal (backing identity alone) is UNDER the
    minimum strength: uncertain, never a guessed stack."""
    weak = _rec("Ad Lib", depth="midground", role="felt", width=0.2,
                td=0.45, crest=10.0, presence=0.1)
    out = classify_vocal_type(weak)
    assert out["vocal_type"] == "vocal_uncertain"
    assert out["confidence"] < 0.6


def test_conflicting_signals_fail_closed_to_uncertain_never_blend_eligible():
    """A wide + forward + heard + sustained backing vocal ties the stack and
    hook readings at full strength — a GENUINE conflict. Fail closed:
    uncertain, never percussive, never stack."""
    conflicted = _rec("Wide Fwd BVs", depth="foreground", role="heard",
                      width=0.7, td=0.2, crest=9.0, presence=0.25)
    out = classify_vocal_type(conflicted)
    assert out["vocal_type"] == "vocal_uncertain"
    assert out["vocal_type"] not in {"vocal_percussive", "vocal_stack"}


def test_confidence_is_always_within_bounds_and_capped():
    """Confidence ∈ [0, 1] on every reading, and never above the honesty cap
    (exported-stem heuristics are never certain)."""
    cases = [_lead(), _chop(), _stack(), _hook(),
             _rec("Ad Lib", td=0.45, width=0.2, role="felt", presence=0.1),
             _rec("Wide Fwd BVs", depth="foreground", role="heard", width=0.7,
                  td=0.2, presence=0.25)]
    for r in cases:
        out = classify_vocal_type(dict(r, vocal_type=None))
        assert 0.0 <= out["confidence"] <= 0.95


def test_non_vocal_stems_return_none():
    for r in (_piano(),
              _rec("Kick", identity="kick", family="drums", role="structural"),
              _rec("Splice Loop", identity="loop", family="loop", role="felt",
                   source="splice_sample")):
        assert not is_vocal_record(r)
        assert classify_vocal_type(r) is None


def test_hook_cap_the_strongest_claim_is_hook_candidate():
    """THE HONESTY CAP: no proven-hook type exists anywhere in the
    vocabulary, and the strongest possible hook evidence still yields only
    ``vocal_hook_candidate``. The deferral (recurrence/provenance) is stated
    in the docstring."""
    assert VOCAL_TYPES == (
        "vocal_lead", "vocal_hook_candidate", "vocal_percussive",
        "vocal_stack", "vocal_uncertain",
    )
    assert not any("proven" in t for t in VOCAL_TYPES)
    out = classify_vocal_type(_hook())
    assert out["vocal_type"] == "vocal_hook_candidate"

    import logic_mix_os.analyzers.vocal_type_classifier as vtc
    doc = (vtc.__doc__ or "").lower()
    assert "recurrence" in doc
    assert "hook_candidate" in doc.replace("``", "")


def test_classifier_is_pure_and_deterministic():
    r = _chop()
    before = copy.deepcopy(r)
    outs = {json.dumps(classify_vocal_type(r), sort_keys=True) for _ in range(5)}
    assert len(outs) == 1
    assert r == before  # never mutates the record


# --------------------------------------------------------------------------- #
# 2. ADDITIVE RECORD FIELDS — the pipeline wiring contract.
# --------------------------------------------------------------------------- #
def test_every_record_carries_both_fields(analyzed):
    """Both keys are ALWAYS present; non-vocal stems carry EXPLICIT None
    (the documented contract), vocal stems a valid type + bounded
    confidence."""
    for name in FIXTURE_NAMES:
        for r in analyzed[name].records:
            assert "vocal_type" in r and "vocal_type_confidence" in r
            if r["vocal_type"] is None:
                assert r["vocal_type_confidence"] is None
            else:
                assert r["vocal_type"] in VOCAL_TYPES
                assert 0.0 <= r["vocal_type_confidence"] <= 1.0


def test_live_fixture_classifications(analyzed):
    """The live readings: every fixture's 'Lead Vocal' reads vocal_lead at
    the identity-backed confidence; every other stem is a non-vocal None."""
    for name in FIXTURE_NAMES:
        for r in analyzed[name].records:
            if r["name"] == "Lead Vocal":
                assert r["vocal_type"] == "vocal_lead"
                assert r["vocal_type_confidence"] == 0.95
            else:
                assert r["vocal_type"] is None
                assert r["vocal_type_confidence"] is None


def test_record_fields_match_a_fresh_classification(analyzed):
    """The record fields are exactly the classifier's output on the same
    record — one shared detection basis, never a forked read."""
    for name in FIXTURE_NAMES:
        for r in analyzed[name].records:
            fresh = classify_vocal_type(r)
            if fresh is None:
                assert r["vocal_type"] is None
            else:
                assert r["vocal_type"] == fresh["vocal_type"]
                assert r["vocal_type_confidence"] == fresh["confidence"]


# --------------------------------------------------------------------------- #
# 3. BYTE-IDENTITY, BOTH SURFACES (user-mandated health metric).
# --------------------------------------------------------------------------- #
def test_vocal_role_fit_weight_is_zero_for_halee_ramone():
    """The byte-identical anchor: weight 0 => ``vrf*0`` numerator, ``+0``
    denominator => the weighted mean is arithmetically untouched."""
    w = load_profile("halee_ramone").doctrine["weights"]
    assert w["vocal_role_fit_score"] == 0


def test_vocal_role_fit_appended_last_preserves_summation_order(analyzed):
    """The new term is LAST in ``component_scores`` (the 14th) and every
    PRE-EXISTING key (the 13 anchors) keeps its exact value + position."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        keys = [k for k in ds if k.endswith("_score") and k != "overall_mix_readiness_score"]
        assert keys[:13] == EXISTING_COMPONENT_KEYS
        assert keys[-1] == "vocal_role_fit_score"
        assert len(keys) == 14


def test_every_preexisting_component_score_is_byte_identical(analyzed):
    """Every one of the thirteen pre-existing component scores + the overall
    (73.8 / 70.7 / 74.3) equals the pinned base value on all three fixtures —
    the axis add did not move any existing number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_overall_is_byte_identical_to_thirteen_term_weighted_mean(analyzed):
    """``overall_mix_readiness_score`` reproduced from ONLY the thirteen
    pre-existing components (vocal_role_fit excluded) equals the pipeline's
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


def test_creative_surface_is_byte_identical_to_base_capture(analyzed):
    """SURFACE (b), user-mandated: the full production ``result.creative``
    still equals the surface pinned at the P-032g base (every branch winner,
    every variant kind + overall score + fired nudges, all three fixtures) —
    an EMPTY diff. Asserted against the SAME pinned capture the P-032g guard
    uses, so a drift breaks both."""
    from test_protect_iconic_loops import BASE_CREATIVE_SURFACE

    for name in FIXTURE_NAMES:
        cr = analyzed[name].creative
        pinned = BASE_CREATIVE_SURFACE[name]
        assert cr["search_mode"] == pinned["search_mode"]
        assert [b["problem_id"] for b in cr["branches"]] == list(pinned["branches"])
        for b in cr["branches"]:
            winner, variants = pinned["branches"][b["problem_id"]]
            assert b["winning"]["winning_variant"] == winner, (name, b["problem_id"])
            assert len(b["variants"]) == len(variants)
            for v, (vid, kind, overall, nudges) in zip(b["variants"], variants):
                assert v["variant_id"] == vid
                assert v["kind"] == kind
                assert v["scores"]["overall_score"] == pytest.approx(overall, abs=1e-9), (name, vid)
                assert v["scores"].get("score_nudges") == nudges, (name, vid)


def test_no_vocal_type_leak_into_the_creative_surface(analyzed):
    """The additive record fields do not leak into any creative output —
    the serialized creative surface never mentions the new vocabulary."""
    for name in FIXTURE_NAMES:
        blob = json.dumps(analyzed[name].creative, sort_keys=True)
        assert "vocal_type" not in blob
        assert "vocal_role_fit" not in blob


# --------------------------------------------------------------------------- #
# 4. AXIS VALUE-DISCRIMINATION (unit) — observational fit readings.
# --------------------------------------------------------------------------- #
def test_no_vocal_stems_returns_documented_neutral():
    c = _constants()
    score, ev = _vrf([_piano()])
    assert score == doctrine_engine._clamp(c["no_vocals"])
    assert any("no vocal stems" in e.lower() for e in ev)


def test_lead_forward_and_clear_reads_high():
    c = _constants()
    score, ev = _vrf([_lead(), _piano()])
    assert score == doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    assert any("owns the presence band" in e.lower() for e in ev)


def test_masked_lead_reads_low():
    c = _constants()
    lead = _lead()
    score, ev = _vrf([lead, _piano()], events=[_mask(lead["name"], "Piano")])
    assert score == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])
    assert score < doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    assert any("challenged" in e.lower() for e in ev)


def test_lead_not_forward_reported_without_bonus():
    c = _constants()
    score, ev = _vrf([_lead(depth="midground")])
    assert score == doctrine_engine._clamp(c["baseline"])
    assert any("midground" in e.lower() for e in ev)


def test_masked_non_lead_vocal_reads_reduced_fit_observationally():
    """The DEFAULT philosophy (no profile policy in Commit-1): a chop/stack/
    hook/uncertain vocal masked AWAY from the lead reads as reduced role fit
    — full clarity protection, reported observationally."""
    c = _constants()
    for stem in (_chop(), _stack(), _hook()):
        clear, _ = _vrf([_lead(), stem])
        masked, ev = _vrf([_lead(), stem], events=[_mask(stem["name"], "Synth Lead")])
        assert masked == doctrine_engine._clamp(
            c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
        assert masked < clear
        assert any("clarity protection" in e.lower() for e in ev)


def test_uncertain_vocal_gets_the_same_clarity_protection():
    """Decision 2: UNCERTAIN is protected exactly like every other vocal —
    the masked reading reduces fit; nothing relaxes it."""
    c = _constants()
    uncertain = _rec("Ad Lib", td=0.45, width=0.2, role="felt", presence=0.1)
    assert uncertain["vocal_type"] == "vocal_uncertain"
    masked, ev = _vrf([_lead(), uncertain],
                      events=[_mask(uncertain["name"], "Synth Lead")])
    assert masked == doctrine_engine._clamp(
        c["baseline"] + c["lead_forward_bonus"] - c["masked_penalty"])
    assert any("clarity protection" in e.lower() for e in ev)


def test_masked_lead_pathway_is_counted_once_through_the_lead_reading():
    """An event that includes the lead is THE MASKED-LEAD PATHWAY: it drives
    the lead reading (one penalty) and is never re-read through the other
    vocal stem in the same event — no double count, and (Commit-2) no blend
    surface exists on it by construction."""
    c = _constants()
    lead, stack = _lead(), _stack()
    score, ev = _vrf([lead, stack], events=[_mask(lead["name"], stack["name"])])
    assert score == doctrine_engine._clamp(c["baseline"] - c["masked_penalty"])
    # exactly one penalized reading: the lead's; the stack contributes none.
    assert sum("challenged" in e.lower() for e in ev) == 1
    assert not any("clarity protection" in e.lower() for e in ev)


def test_live_fixture_axis_reading(analyzed):
    """The informational live reading (weight 0, inert for halee_ramone):
    every fixture's lead is forward and clear → baseline + bonus, with
    non-empty evidence including the census."""
    c = _constants()
    expected = doctrine_engine._clamp(c["baseline"] + c["lead_forward_bonus"])
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        assert ds["vocal_role_fit_score"] == expected
        ev = ds["evidence"]["vocal_role_fit"]
        assert isinstance(ev, list) and ev
        assert any("vocal roles read" in e.lower() for e in ev)


def test_score_is_bounded_0_100():
    cases = [
        ([], None),
        ([_piano()], None),
        ([_lead()], None),
        ([_lead(), _chop(), _stack(), _hook()],
         [_mask("Vox Chops", "Synth Lead"), _mask("BV Stack", "Synth Lead"),
          _mask("Hook Vox", "Synth Lead"), _mask("Lead Vocal", "Piano")]),
    ]
    for records, events in cases:
        score, _ = _vrf(records, events=events)
        assert isinstance(score, float)
        assert 0.0 <= score <= 100.0


# --------------------------------------------------------------------------- #
# 5. OBSERVATIONAL LANGUAGE + HONEST DEFERRALS (user-mandated).
# --------------------------------------------------------------------------- #
def _all_status_evidence():
    out = []
    out.append(_vrf([_piano()])[1])                                   # no vocals
    out.append(_vrf([_lead(), _piano()])[1])                          # lead clear
    out.append(_vrf([_lead(depth="midground")])[1])                   # lead back
    out.append(_vrf([_lead()], events=[_mask("Lead Vocal", "Piano")])[1])  # lead masked
    for stem in (_chop(), _stack(), _hook(),
                 _rec("Ad Lib", td=0.45, width=0.2, role="felt", presence=0.1)):
        out.append(_vrf([_lead(), stem],
                        events=[_mask(stem["name"], "Synth Lead")])[1])
    out.append(_vrf([_lead(), _stack()],
                    events=[_mask("Lead Vocal", "BV Stack")])[1])     # lead pathway
    return out


def test_engine_language_is_observational_zero_judgment_words():
    """USER-MANDATED: the evidence reports lead/chop/stack/uncertain and
    masking involvement — never 'bad', 'problem', 'should', 'fix' (nor
    better/worse/wrong) — across every reading the axis can emit."""
    for ev in _all_status_evidence():
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in evidence: {blob}"


def test_live_fixture_evidence_is_observational(analyzed):
    for name in FIXTURE_NAMES:
        ev = analyzed[name].doctrine_score["evidence"]["vocal_role_fit"]
        blob = " ".join(ev).lower()
        for word in JUDGMENT_WORDS:
            assert word not in blob, f"judgment word {word!r} in {name}: {blob}"


def test_honest_deferrals_stated_in_docstrings_never_claimed_in_evidence():
    """THE HONESTY GATE: the classifier states its deferrals — hook
    RECURRENCE/provenance (hence the hook_candidate cap), LYRIC MEANING, and
    the PER-ONSET STUTTER rate (onset timing is post-doctrine groove
    territory) — and no evidence line ever claims any of them."""
    import logic_mix_os.analyzers.vocal_type_classifier as vtc

    doc = (vtc.__doc__ or "").lower()
    for claim in ("recurrence", "provenance", "lyric", "per-onset", "stutter"):
        assert claim in doc

    axis_doc = (doctrine_engine._vocal_role_fit.__doc__ or "").lower()
    assert "observational" in axis_doc
    assert "recurrence" in axis_doc or "vocal_type_classifier" in axis_doc

    for ev in _all_status_evidence():
        blob = " ".join(ev).lower()
        for claim in ("recurrence", "lyric", "proven hook"):
            assert claim not in blob


# --------------------------------------------------------------------------- #
# 6. LIVENESS / SABOTAGE — a non-zero weight makes the axis a real lever.
# --------------------------------------------------------------------------- #
def _profile_weighting_vocal_role_fit(weight: float):
    """A halee_ramone copy whose ONLY change is a non-zero vocal_role_fit
    weight — any overall delta is attributable to the new term alone."""
    base = load_profile("halee_ramone")
    doctrine = copy.deepcopy(base.doctrine)
    doctrine["weights"]["vocal_role_fit_score"] = weight
    return dataclasses.replace(base, doctrine=doctrine)


def test_nonzero_weight_moves_the_overall(analyzed):
    """Re-scoring ``dense_chorus_with_loops`` under a profile that weights
    vocal_role_fit non-zero changes the overall vs the weight-0 reference.

    Sabotage this catches: dropping ``vocal_role_fit_score`` from
    ``component_scores`` collapses the weighted mean back onto the reference
    and this assertion FAILS — while byte-identical stays green."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_vocal_role_fit(3.0), groove=groove
    )
    vrf = reference["vocal_role_fit_score"]
    assert vrf is not None and 0.0 <= vrf <= 100.0
    assert weighted["overall_mix_readiness_score"] != reference["overall_mix_readiness_score"]


def test_liveness_direction_tracks_the_vocal_role_fit_score(analyzed):
    """The sharper sabotage guard: the overall must move in the direction of
    vocal_role_fit's value relative to the reference overall. A hardcoded
    term would not track the real score."""
    res = analyzed["dense_chorus_with_loops"]
    base_args = (res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent)
    groove = res.expanded["groove"]

    reference = doctrine_engine.score_doctrine(*base_args, groove=groove)
    vrf = reference["vocal_role_fit_score"]
    ref_overall = reference["overall_mix_readiness_score"]
    weighted = doctrine_engine.score_doctrine(
        *base_args, profile=_profile_weighting_vocal_role_fit(5.0), groove=groove
    )
    new_overall = weighted["overall_mix_readiness_score"]
    if vrf > ref_overall:
        assert new_overall > ref_overall
    elif vrf < ref_overall:
        assert new_overall < ref_overall
    else:
        assert new_overall == ref_overall


def test_weighted_masked_vs_clear_lead_moves_the_overall():
    """The axis is a genuine LEVER, not a constant: under the SAME non-zero
    weight, the same project scores a HIGHER overall when its lead is clear
    than when its lead is masked."""
    profile = _profile_weighting_vocal_role_fit(5.0)
    records = [_lead(), _piano()]
    clear = doctrine_engine.score_doctrine(records, [], {"events": []}, None, profile=profile)
    masked = doctrine_engine.score_doctrine(
        records, [], {"events": [_mask("Lead Vocal", "Piano")]}, None, profile=profile)
    assert clear["vocal_role_fit_score"] > masked["vocal_role_fit_score"]
    assert clear["overall_mix_readiness_score"] > masked["overall_mix_readiness_score"]


# --------------------------------------------------------------------------- #
# 7. NO-ALIASING — the scorer reads, never mutates.
# --------------------------------------------------------------------------- #
def test_vocal_role_fit_does_not_mutate_profile_records_or_events():
    doctrine = load_profile("halee_ramone").doctrine
    doctrine_before = copy.deepcopy(doctrine)
    records = [_lead(), _chop(), _stack()]
    records_before = copy.deepcopy(records)
    events = [_mask("Vox Chops", "Synth Lead"), _mask("Lead Vocal", "BV Stack")]
    events_before = copy.deepcopy(events)
    doctrine_engine._vocal_role_fit(records, events, doctrine)
    assert doctrine == doctrine_before
    assert records == records_before
    assert events == events_before


def test_score_doctrine_with_vocal_role_fit_does_not_mutate_shared_globals(analyzed):
    before = copy.deepcopy(doctrine_engine._DEFAULT_PROFILE.doctrine)
    res = analyzed["dense_chorus_with_loops"]
    doctrine_engine.score_doctrine(
        res.records, res.section_analysis, res.masking_report, res.mix_metrics, res.project.intent,
        groove=res.expanded["groove"],
    )
    assert doctrine_engine._DEFAULT_PROFILE.doctrine == before
    assert "vocal_role_fit" in doctrine_engine._DEFAULT_PROFILE.doctrine["scorers"]
