"""P-032g Commit-2 — the FIRST profile-DECIDED creative gate:
``protect_iconic_loops``.

THE DOCTRINE PIN made operational: Commit-1's ``loop_context`` axis is the
engine DETECTING (static vs iconic, observationally); this gate is the profile
DECIDING. When a profile sets ``protect_iconic_loops: true`` and the loop
READS iconic — on the SAME shared detection basis as the doctrine axis
(``read_loop_context``, never forked) — the ``loop_deconstruct`` promotion
does NOT fire: the profile protects the loop as the record's identity. The
reference ``halee_ramone`` profile sets it FALSE, so current behavior is
byte-identical: Halee/Ramone still deconstructs.

THE RAMONE GATE (packet-mandated): iconic must NOT override a masked lead.
When the lead vocal is bad-masked, protection does not apply — even a
protecting profile lets the deconstruct pressure through when the loop is
burying the vocal.

USER-MANDATED DUAL BYTE-IDENTITY, surface (b): under Halee/Ramone defaults the
creative variant scores AND the ``loop_deconstruct`` promotion firing behavior
must be byte-identical across this gate's introduction. The full creative
surface (every branch winner, every variant overall score, every fired nudge)
was captured at the packet base (`6af00fa`) and is pinned here verbatim; the
promotion-fires path is additionally pinned at its base values (85.9 /
winner loop_A / the verbatim promotion reason).

Evidence discipline: the foregrounded-loop promotion evidence is produced by
the REAL source auditors / provenance analyzer re-run on a genuinely
foregrounded loop (the ``test_loop_promotion`` idiom — never a hand-set
flag). The iconic/masked-lead readings are then shaped on that deep copy
(section movement, loop envelope/role, a masking event), since the synthetic
fixtures have no genuinely-iconic loop to export; the gate's inputs are the
same wires production reads.
"""

from __future__ import annotations

import copy
import dataclasses
import pathlib

import pytest

from logic_mix_os import creative
from logic_mix_os.analyzers.provenance import analyze_provenance
from logic_mix_os.analyzers.source_auditors import audit_all
from logic_mix_os.constants import LOOP_SAMPLE_KINDS
from logic_mix_os.creative import _apply_promotions, _foregrounded_loop, run_creative_engine
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile, _validate

_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Verbatim promotion evidence string (the P-016 contract surface).
PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — deconstruct it "
    "(source material respected), don't just accent it"
)

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# The FULL default-profile creative surface, captured at the packet base
# (`6af00fa`, before the gate existed): per branch — the winner and every
# variant's (kind, overall_score, score_nudges). Byte-identity surface (b).
BASE_CREATIVE_SURFACE = {
    "simple_vocal_piano_song": {
        "search_mode": "ramone_vocal_truth",
        "branches": {
            "vocal_belief": ("vocal_A", [
                ("vocal_A", "vocal_ride", 82.9, None),
                ("vocal_B", "intimacy_pass", 81.1, None),
            ]),
        },
    },
    "dense_chorus_with_loops": {
        "search_mode": "dramatic_contrast",
        "branches": {
            "chorus_lift": ("chorus_lift_B", [
                ("chorus_lift_A", "width_bloom", 74.9,
                 ["vocal_belief -6: stereo image is already width-crowded"]),
                ("chorus_lift_B", "subtractive_drop", 85.3, None),
                ("chorus_lift_C", "vocal_ride", 82.9, None),
                ("chorus_lift_D", "drum_room_bloom", 81.4, None),
            ]),
            "density": ("density_B", [
                ("density_A", "depth_cleanup", 81.1, None),
                ("density_B", "subtractive_drop", 85.3, None),
            ]),
            "loop": ("loop_B", [
                ("loop_A", "loop_deconstruct", 81.9, None),
                ("loop_B", "subtractive_drop", 85.3, None),
            ]),
            "depth": ("depth_A", [
                ("depth_A", "depth_cleanup", 81.1, None),
            ]),
            "vocal_belief": ("vocal_A", [
                ("vocal_A", "vocal_ride", 82.9, None),
                ("vocal_B", "intimacy_pass", 81.1, None),
            ]),
        },
    },
    "splice_loop_problem": {
        "search_mode": "dramatic_contrast",
        "branches": {
            "chorus_lift": ("chorus_lift_B", [
                ("chorus_lift_A", "width_bloom", 75.7, None),
                ("chorus_lift_B", "subtractive_drop", 85.3, None),
                ("chorus_lift_C", "vocal_ride", 82.9, None),
                ("chorus_lift_D", "drum_room_bloom", 81.4, None),
            ]),
            "loop": ("loop_B", [
                ("loop_A", "loop_deconstruct", 81.9, None),
                ("loop_B", "subtractive_drop", 85.3, None),
            ]),
            "vocal_belief": ("vocal_A", [
                ("vocal_A", "vocal_ride", 82.9, None),
                ("vocal_B", "intimacy_pass", 81.1, None),
            ]),
        },
    },
}


# --------------------------------------------------------------------------- #
# Helpers — the test_loop_promotion idiom (REAL auditors on a genuinely
# foregrounded loop), plus the iconic / masked-lead shaping on the deep copy.
# --------------------------------------------------------------------------- #
def _with_foregrounded_loop(result):
    """Deep copy of a real analyze() result in which the loop is GENUINELY
    foregrounded, with the REAL auditors/provenance re-run so THEY emit the
    real promotion evidence (never a hand-set flag)."""
    r = copy.deepcopy(result)
    loop_ids = {rec["track_id"] for rec in r.records if rec["source_kind"] in LOOP_SAMPLE_KINDS}
    assert loop_ids, "fixture must contain at least one imported loop"
    for rec in r.records:
        if rec["track_id"] in loop_ids:
            rec["depth_default"] = "foreground"
    for d in r.depth_map:
        if d["track_id"] in loop_ids:
            d["default_depth"] = "foreground"
    r.source_audits = audit_all(r.records)
    r.provenance = analyze_provenance(r.project, r.source_material, r.depth_map)
    return r


def _with_iconic_loop(analyzed):
    """A foregrounded-loop result shaped so the loop READS iconic on the
    shared detection basis: defined hits (crest over the definition floor),
    heard, unmasked — and the mix EVOLVES around it at the section grain."""
    r = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    for rec in r.records:
        if rec["source_kind"] in LOOP_SAMPLE_KINDS:
            rec["metrics"]["crest_factor_db"] = 15.0
            rec["perceptual_role"] = "heard"
    for s, rms in zip(r.section_analysis, [-16.0, -9.0]):
        s["metrics"]["rms_dbfs"] = rms
    return r


def _with_masked_lead(result):
    """The same result with the LEAD VOCAL bad-masked (the Ramone gate input).
    The loop is NOT in the event's elements, so its own iconic read stands."""
    r = copy.deepcopy(result)
    r.masking_report["events"].append({
        "elements": ["Lead Vocal", "Electric Guitar 1"],
        "classification": "bad_masking",
        "severity": "critical",
        "section": "chorus_1",
    })
    return r


def _protect_profile():
    """A halee_ramone copy whose ONLY change is protect_iconic_loops=True —
    any behavior delta is attributable to the flag alone."""
    return dataclasses.replace(load_profile("halee_ramone"), protect_iconic_loops=True)


def _loop_status(result, prof):
    c = prof.doctrine["scorers"]["loop_context"]
    status, _ = doctrine_engine.read_loop_context(
        result.records, result.section_analysis,
        result.masking_report.get("events", []), c,
    )
    return status


def _loop_branch(creative_out):
    return next(b for b in creative_out["branches"] if b["problem_id"] == "loop")


def _variant_by_id(branch, vid):
    return next(v for v in branch["variants"] if v["variant_id"] == vid)


# --------------------------------------------------------------------------- #
# 1. THE FLAG — a top-level profile field, defaulting to CURRENT behavior.
# --------------------------------------------------------------------------- #
def test_halee_ramone_default_is_false():
    """The reference profile does NOT protect: deconstruct-vs-protect is the
    profile's decision and Halee/Ramone decides deconstruct — current
    behavior, byte-identical."""
    assert load_profile("halee_ramone").protect_iconic_loops is False


def test_flag_is_a_required_profile_field():
    """A profile without the field is structurally invalid — the decision must
    be explicit in every producer's JSON, never silently defaulted."""
    import json
    raw = json.load(open(
        _ROOT / "logic_mix_os" / "doctrine" / "producers" / "halee_ramone.json",
        encoding="utf-8",
    ))
    del raw["protect_iconic_loops"]
    with pytest.raises(ValueError, match="protect_iconic_loops"):
        _validate(raw, "halee_ramone")


def test_gate_reuses_the_shared_detection_basis():
    """The creative gate reads the SAME ``read_loop_context`` the doctrine
    axis uses — one detection basis, never forked."""
    assert creative.read_loop_context is doctrine_engine.read_loop_context


def test_packet_cautions_untouched():
    """Packet-mandated: the ``_halee`` loop_foregrounded penalty coefficient
    and the halee_ramone promotion table rows/deltas are NOT modified."""
    p = load_profile("halee_ramone")
    assert p.doctrine["penalty_coeffs"]["halee"]["loop_foregrounded"] == 6
    assert p.promotion_table == [{
        "kinds": {"loop_deconstruct"},
        "evidence": "foregrounded_loop",
        "dim": "excitement",
        "delta": 35,
        "reason": PROMOTION_REASON,
    }]


# --------------------------------------------------------------------------- #
# 2. BYTE-IDENTITY SURFACE (b) — USER-MANDATED: under Halee/Ramone defaults
#    the creative variant scores + promotion firing behavior are unchanged
#    across the gate's introduction.
# --------------------------------------------------------------------------- #
def test_default_creative_surface_is_byte_identical_to_base_capture(analyzed):
    """The PRODUCTION ``result.creative`` (default profile, no re-run) equals
    the full surface captured at the packet base: every branch winner, every
    variant's kind + overall score + fired nudges, on all three fixtures."""
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


def test_default_promotion_still_fires_exactly_as_base(analyzed):
    """The firing side of surface (b): with the default profile (protect
    FALSE), a genuinely foregrounded loop still fires the promotion at its
    exact base values — 85.9, the verbatim reason, winner loop_A — even when
    the loop ALSO reads iconic. Halee/Ramone deconstructs; the gate changed
    nothing it did not own."""
    prof = load_profile("halee_ramone")
    for res in (
        _with_foregrounded_loop(analyzed["dense_chorus_with_loops"]),  # static read
        _with_iconic_loop(analyzed),                                   # iconic read
    ):
        assert _foregrounded_loop(res) is True
        out = run_creative_engine(res, res.creative["search_mode"], profile=prof)
        branch = _loop_branch(out)
        loop_a = _variant_by_id(branch, "loop_A")
        assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]
        assert loop_a["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)
        assert branch["winning"]["winning_variant"] == "loop_A"

    # And with NO profile passed at all (the module-default path).
    res = _with_iconic_loop(analyzed)
    out = run_creative_engine(res, res.creative["search_mode"])
    loop_a = _variant_by_id(_loop_branch(out), "loop_A")
    assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]


# --------------------------------------------------------------------------- #
# 3. FLAG LIVENESS — protect suppresses ICONIC; STATIC still fires; a masked
#    lead overrides protection (the Ramone gate).
# --------------------------------------------------------------------------- #
def test_protecting_profile_suppresses_promotion_on_iconic_loop(analyzed):
    """THE REVERSAL, live: same evidence, same tables — the ONLY change is the
    profile's decision. With protect_iconic_loops=True and an iconic-reading
    loop, the loop_deconstruct promotion does NOT fire; the loop branch falls
    back to its unpromoted base ranking (loop_B wins at 85.3 over 81.9)."""
    res = _with_iconic_loop(analyzed)
    prof = _protect_profile()
    assert _foregrounded_loop(res) is True          # the evidence WOULD fire
    assert _loop_status(res, prof) == "iconic"      # and the loop reads iconic

    assert _apply_promotions("loop_deconstruct", res, prof) == []
    out = run_creative_engine(res, res.creative["search_mode"], profile=prof)
    branch = _loop_branch(out)
    loop_a = _variant_by_id(branch, "loop_A")
    assert "score_nudges" not in loop_a["scores"]
    assert loop_a["scores"]["overall_score"] == pytest.approx(81.9, abs=1e-9)
    assert branch["winning"]["winning_variant"] == "loop_B"


def test_protecting_profile_still_fires_on_static_loop(analyzed):
    """Protection is for ICONIC-functioning loops only: the same protecting
    profile with a STATIC-reading loop (dominant, no sectional evolution)
    lets the promotion fire exactly as the reference does."""
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    prof = _protect_profile()
    assert _foregrounded_loop(res) is True
    assert _loop_status(res, prof) == "static"

    fired = _apply_promotions("loop_deconstruct", res, prof)
    assert [f[2] for f in fired] == [PROMOTION_REASON]
    out = run_creative_engine(res, res.creative["search_mode"], profile=prof)
    branch = _loop_branch(out)
    loop_a = _variant_by_id(branch, "loop_A")
    assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]
    assert loop_a["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)
    assert branch["winning"]["winning_variant"] == "loop_A"


def test_masked_lead_overrides_protection(analyzed):
    """THE RAMONE GATE: iconic must NOT override a masked lead. With the lead
    vocal bad-masked, the promotion fires even under the protecting profile —
    the deconstruct pressure comes through when the loop context includes a
    buried vocal."""
    res = _with_masked_lead(_with_iconic_loop(analyzed))
    prof = _protect_profile()
    assert _foregrounded_loop(res) is True
    # The loop itself still reads iconic (it is not in the masking event) —
    # protection is denied by the LEAD's masking, not by a lost iconic read.
    assert _loop_status(res, prof) == "iconic"

    fired = _apply_promotions("loop_deconstruct", res, prof)
    assert [f[2] for f in fired] == [PROMOTION_REASON]
    out = run_creative_engine(res, res.creative["search_mode"], profile=prof)
    branch = _loop_branch(out)
    loop_a = _variant_by_id(branch, "loop_A")
    assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]
    assert branch["winning"]["winning_variant"] == "loop_A"


def test_flag_alone_is_the_lever(analyzed):
    """The decisive A/B: identical result, identical iconic read — the ONLY
    difference is the flag. False => promotion fires (85.9, loop_A wins);
    True => suppressed (81.9, loop_B wins). The reversal lives in the
    profile, not in engine code."""
    res = _with_iconic_loop(analyzed)
    base = load_profile("halee_ramone")
    protecting = _protect_profile()
    out_false = run_creative_engine(res, res.creative["search_mode"], profile=base)
    out_true = run_creative_engine(res, res.creative["search_mode"], profile=protecting)
    a_false = _variant_by_id(_loop_branch(out_false), "loop_A")
    a_true = _variant_by_id(_loop_branch(out_true), "loop_A")
    assert a_false["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)
    assert a_true["scores"]["overall_score"] == pytest.approx(81.9, abs=1e-9)
    assert _loop_branch(out_false)["winning"]["winning_variant"] == "loop_A"
    assert _loop_branch(out_true)["winning"]["winning_variant"] == "loop_B"


def test_protection_only_touches_the_loop_branch(analyzed):
    """Collateral safety: between protect=False and protect=True on the iconic
    result, the ONLY branch whose winner changes is ``loop`` — every other
    branch's winner and variant scores are identical."""
    res = _with_iconic_loop(analyzed)
    out_false = run_creative_engine(res, res.creative["search_mode"], profile=load_profile("halee_ramone"))
    out_true = run_creative_engine(res, res.creative["search_mode"], profile=_protect_profile())
    win_false = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_false["branches"]}
    win_true = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_true["branches"]}
    assert set(win_false) == set(win_true)
    assert {pid for pid in win_false if win_false[pid] != win_true[pid]} == {"loop"}
    for b_false, b_true in zip(out_false["branches"], out_true["branches"]):
        if b_false["problem_id"] == "loop":
            continue
        for v_false, v_true in zip(b_false["variants"], b_true["variants"]):
            assert v_false["scores"]["overall_score"] == v_true["scores"]["overall_score"]


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — the gate only reads; it never mutates the profile or the
#    result's shared structures.
# --------------------------------------------------------------------------- #
def test_gate_does_not_mutate_profile_or_result(analyzed):
    res = _with_iconic_loop(analyzed)
    prof = _protect_profile()
    doctrine_before = copy.deepcopy(prof.doctrine)
    table_before = copy.deepcopy(prof.promotion_table)
    records_before = copy.deepcopy(res.records)
    sections_before = copy.deepcopy(res.section_analysis)
    masking_before = copy.deepcopy(res.masking_report)
    _apply_promotions("loop_deconstruct", res, prof)
    run_creative_engine(res, res.creative["search_mode"], profile=prof)
    assert prof.doctrine == doctrine_before
    assert prof.promotion_table == table_before
    assert res.records == records_before
    assert res.section_analysis == sections_before
    assert res.masking_report == masking_before


def test_default_module_profile_untouched_by_gate_runs(analyzed):
    """Running the gated engine under a protecting profile leaves the module
    default profile (the byte-identity anchor) byte-unchanged."""
    before_flag = creative._DEFAULT_PROFILE.protect_iconic_loops
    before_doctrine = copy.deepcopy(creative._DEFAULT_PROFILE.doctrine)
    res = _with_iconic_loop(analyzed)
    run_creative_engine(res, res.creative["search_mode"], profile=_protect_profile())
    assert creative._DEFAULT_PROFILE.protect_iconic_loops == before_flag is False
    assert creative._DEFAULT_PROFILE.doctrine == before_doctrine
