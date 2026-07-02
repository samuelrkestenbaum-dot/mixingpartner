"""P-032h — THE PAYOFF PACKET: ``timbaland.json``, the second live producer
profile and the FIRST non-byte-identical output of the producer-agnostic epic.

Everything the seven measurement packets + P-031 built converges here. The
second producer ships **different / profile-authored / confidence-stamped /
honesty-labeled / safety-invariant**, and these are the guards for each word:

1. **Loads + validates** — ``load_profile("timbaland")`` passes every
   structural check; the three REQUIRED declarations
   (``protect_iconic_loops`` / ``vocal_blend_policy`` / ``confidence_map``)
   are present with the authored values; the metadata carries the confirmed
   honesty stamp (hand-curated-documented -> HIGH).
2. **Byte-identity of the DEFAULT** — authoring a second JSON must not touch
   the reference path: the pinned doctrine surface (73.8 / 70.7 / 74.3 + all
   14 components), the full creative base capture, and regression 93/93 (the P-035 corpus — see conftest.py) all
   hold on the DEFAULT producer.
3. **THE DIFFERENTIAL IS ALIVE** — ``analyze(producer="timbaland")`` produces
   a DIFFERENT ``overall_mix_readiness_score`` on every fixture; on the loop
   fixtures (both reading STATIC) the static-loop pressure is felt in the
   overall (timbaland weights ``loop_context`` > 0 AND authors its polarity:
   static 10 < the reference's 15); the divergence is ATTRIBUTABLE (component
   scores equal except the profile-authored loop_context polarity; the
   overall is exactly timbaland's weighted mean).
4. **The gates flip live** — on the P-032g iconic-loop scenario, timbaland
   (protect=true) suppresses the ``loop_deconstruct`` promotion while
   halee_ramone fires it; a STATIC loop still gets the contrast pressure
   under timbaland; the masked-lead override holds for BOTH profiles.
5. **The confidence map is verbatim-pinned** (the P-031 reviewer note:
   validation accepts duplicate areas / extra keys — the pin is the guard),
   and its claims are machine-checked against the authored weights.
6. **Safety invariance** — KILL_SWITCHES for timbaland = the 5 hardcoded
   SAFETY switches + timbaland's aesthetic list (a superset of the
   reference's); every comparable safety-adjacent structure is
   equivalent-or-stricter; risk-class semantics unchanged.
7. **No-aliasing with TWO live profiles** — the standing carry-forward at its
   moment: load both, run ``analyze`` with each profile OBJECT, and neither
   profile's structures nor the module ``_DEFAULT_PROFILE`` moves.
8. **Confidence rendering** — ``analyze(producer="timbaland")`` artifacts
   carry TIMBALAND's map (never the reference's) in ``doctrine_score.json``
   and the verdict markdown.
"""

from __future__ import annotations

import copy
import json
import pathlib

import pytest

from logic_mix_os import creative, governance
from logic_mix_os.creative import _apply_promotions, _foregrounded_loop, run_creative_engine
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import (
    CONFIDENCE_LEVELS,
    _REQUIRED_DATA_FIELDS,
    _validate,
    load_profile,
)
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest

from conftest import FIXTURE_NAMES, ROOT
from test_protect_iconic_loops import (
    BASE_CREATIVE_SURFACE,
    PROMOTION_REASON,
    _loop_branch,
    _loop_status,
    _variant_by_id,
    _with_foregrounded_loop,
    _with_iconic_loop,
    _with_masked_lead,
)
from test_vocal_type import BASE_COMPONENT_SCORES, judgment_word_hits

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_TIMBALAND_PATH = _ROOT / "logic_mix_os" / "doctrine" / "producers" / "timbaland.json"

# --------------------------------------------------------------------------- #
# The authored value system, PINNED VERBATIM.
# --------------------------------------------------------------------------- #
# The user's APPROVED Timbaland weighting: protect groove identity / negative
# space / low-end movement / section contrast; relax vocal centrality / the
# lush-depth bias / the naturalistic-space bias — relax != remove (all > 0).
# The two ceilinged axes (low_end_motion tops at 84, vocal_role_fit at 85 —
# never 100) carry deliberately MODERATED weights so the ceilings do not
# systematically drag the weighted mean.
TIM_WEIGHTS = {
    "physical_space_score": 0.5,
    "emotional_hierarchy_score": 0.7,
    "vocal_centrality_score": 0.6,
    "depth_hierarchy_score": 0.5,
    "section_contrast_score": 1.2,
    "static_mix_score": 0.9,
    "dynamic_mix_score": 1.0,
    "beat_identity_score": 1.3,
    "negative_space_score": 1.2,
    "groove_coherence_score": 1.1,
    "rhythmic_surprise_score": 1.0,
    "low_end_motion_score": 0.9,
    "loop_context_score": 0.8,
    "vocal_role_fit_score": 0.4,
}

# The seven axes the profile weights UP (vs the reference) and the five it
# relaxes (still > 0) — the machine-checkable shape of the approved system.
WEIGHTED_UP = (
    "beat_identity_score", "negative_space_score", "groove_coherence_score",
    "rhythmic_surprise_score", "low_end_motion_score", "loop_context_score",
    "section_contrast_score", "dynamic_mix_score", "vocal_role_fit_score",
)
RELAXED = (
    "physical_space_score", "emotional_hierarchy_score", "vocal_centrality_score",
    "depth_hierarchy_score", "static_mix_score",
)

# Timbaland's authored promotion evidence line (fires on static/ambiguous
# dominant loops and on the masked-lead override — never claims a read).
TIM_PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — turn it into groove "
    "gestures (source material respected) so the record's rhythmic identity leads"
)

# The authored timbaland confidence map, VERBATIM (the P-031 reviewer note:
# validation accepts duplicate areas and extra entry keys — this pin is the
# guard against drift; any edit is a conscious, test-visible decision).
TIM_AUTHORED_MAP = [
    {
        "area": "groove and beat-identity interpretation (beat identity, groove coherence, rhythmic surprise)",
        "level": "high",
        "reason": "hand-curated from documented Timbaland technique — syncopated pocket construction and beat-first arrangement; these axes are live and weighted up in this profile",
    },
    {
        "area": "negative space, section contrast and dynamic-movement interpretation",
        "level": "high",
        "reason": "hand-curated from documented Timbaland technique — syncopated negative space and hard section flips; these axes are live and weighted up in this profile",
    },
    {
        "area": "low-end motion interpretation",
        "level": "high",
        "reason": "hand-curated from documented Timbaland technique — the sub-driven pocket and the kick/sub relationship; live and weighted, with the axis ceiling (84, never 100) reflected in a moderated weight",
    },
    {
        "area": "loop context interpretation (static vs iconic)",
        "level": "high",
        "reason": "hand-curated from documented Timbaland technique — iconic loop identity is protected as the record's identity (protect_iconic_loops: true) while a static dominant loop reads as contrast pressure; the status-to-score polarity is authored in this profile",
    },
    {
        "area": "lead-vocal centrality, depth hierarchy, arrangement realism and balance hygiene as retained measurement",
        "level": "high",
        "reason": "these axes measure lead masking, decorative clutter, depth stacking and level hygiene that stay live in this profile at reduced weight — the groove-first weighting relaxes them, never removes them",
    },
    {
        "area": "vocal blend interpretation",
        "level": "limited",
        "reason": "the masking analyzer reads the vocal band against non-lead vocals when either side of the pair is forward (the vocal stem itself, or a heard masker standing forward in front of it); the acceptable-blend policy this profile opts into is live and measured on real exported-stem data — a qualified vocal chop under masking reads 85.0 on vocal_role_fit against the reference's 65.0 (the reference draws the masked penalty once for the chop and once for the stack; the accepted blend waives both), worth +0.7 overall at the authored 0.4 weight; coverage stays bounded: events arise only from the masker-instrument set, info-tier events are emitted but not consumed, and vocal-band events carry no per-track masking risk",
    },
    {
        "area": "cultural loop recognizability",
        "level": "deferred",
        "reason": "iconic-ness as cultural recognition needs provenance/manifest signals not measurable on exported stems at doctrine time; the acoustic loop-context proxy is what ships",
    },
    {
        "area": "true hook recurrence",
        "level": "deferred",
        "reason": "a proven hook needs a recurrence signal that does not exist at doctrine time; the strongest claim ships as vocal_hook_candidate",
    },
    {
        "area": "motif provenance",
        "level": "deferred",
        "reason": "motif lineage across sources is not measurable on exported stems at doctrine time",
    },
    {
        "area": "onset-timing strong forms (fingerprint typing, fills/unexpected-hit detection, kick/sub temporal interlock)",
        "level": "deferred",
        "reason": "these need per-onset timing and typing signals not measurable on exported stems at doctrine time; the section-aggregate weak forms are what ship",
    },
    {
        "area": "per-section true-sub movement",
        "level": "deferred",
        "reason": "section analysis exposes low_mid_energy (120-500 Hz) only, so the true-sub band (20-120 Hz) is not measurable at section grain on exported stems; the low_mid section grain is what ships",
    },
]

COMPONENT_KEYS = list(TIM_WEIGHTS)

# Reference-DISTINCT confidence strings that must never leak into a timbaland
# artifact (the shared deferred entries are engine boundaries and legitimately
# identical; these two are the reference's own voice).
REFERENCE_ONLY_STRINGS = (
    "the seven producer-agnostic axes as measurement",
    "the reference judgment predates these axes",
)


def _tim_raw() -> dict:
    with open(_TIMBALAND_PATH, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def timbaland_analyzed():
    """The full pipeline once per fixture with ``producer="timbaland"``."""
    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="timbaland"
        )
    return results


# --------------------------------------------------------------------------- #
# 1. LOADS + VALIDATES — every structural check; the three declarations.
# --------------------------------------------------------------------------- #
def test_loads_and_passes_every_structural_check():
    """``load_profile("timbaland")`` succeeds (which runs ``_validate``), and
    the raw JSON independently passes ``_validate`` — the profile is
    structurally complete under the same gate as the reference."""
    p = load_profile("timbaland")
    assert p.metadata["name"] == "timbaland"
    _validate(_tim_raw(), "timbaland")  # must not raise


def test_raw_json_carries_every_required_field():
    raw = _tim_raw()
    for f in _REQUIRED_DATA_FIELDS:
        assert f in raw, f"timbaland.json missing required field {f!r}"
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        assert key in raw["doctrine"]


def test_metadata_is_the_confirmed_honesty_stamp():
    """Hand-curated from documented technique -> HIGH, per the user's
    confirmed honesty policy (hand-curated -> high; derived -> low, labeled;
    LLM -> draft-only, never high)."""
    assert load_profile("timbaland").metadata == {
        "name": "timbaland",
        "display_name": "Timbaland",
        "provenance": "hand-curated-documented",
        "confidence": "high",
        "risk_class": 0,
    }


def test_declaration_one_protect_iconic_loops_true():
    """REQUIRED declaration 1 — the loop philosophy, in writing: the P-032g
    hinge flipped. The engine detects static-vs-iconic; timbaland DECIDES to
    protect the iconic-functioning loop."""
    assert load_profile("timbaland").protect_iconic_loops is True


def test_declaration_two_vocal_blend_policy_opt_in():
    """REQUIRED declaration 2 — the masking philosophy, in writing: timbaland
    opts in (qualified chops/stacks may blend) at the reference confidence
    floor. The safety rails (lead/uncertain/hook always protected) are
    engine-fixed and untouched by this opt-in."""
    assert load_profile("timbaland").vocal_blend_policy == {
        "acceptable_blend": True,
        "confidence_floor": 0.75,
    }


def test_declaration_three_confidence_map_present_and_valid():
    """REQUIRED declaration 3 — the profile's OWN honesty map (verbatim pin in
    group 5): non-empty, every level from the closed vocabulary."""
    cmap = load_profile("timbaland").confidence_map
    assert cmap
    for entry in cmap:
        assert entry["level"] in CONFIDENCE_LEVELS


def test_weights_are_the_approved_value_system_verbatim():
    """The 14-axis weight table, pinned verbatim — the heart of the packet."""
    assert load_profile("timbaland").doctrine["weights"] == TIM_WEIGHTS


def test_weight_relations_protect_up_relax_down_never_remove():
    """The approved shape, machine-checked against the reference: the
    groove/space/low-end/loop/movement axes weigh MORE than in the reference;
    the vocal-centrality / lush-depth / naturalistic-space / hygiene axes
    weigh LESS — and every weight stays > 0 (relax != remove)."""
    tim = load_profile("timbaland").doctrine["weights"]
    ref = load_profile("halee_ramone").doctrine["weights"]
    for key in WEIGHTED_UP:
        assert tim[key] > ref[key], f"{key} not weighted up vs the reference"
    for key in RELAXED:
        assert 0 < tim[key] < ref[key], f"{key} not relaxed-but-present"
    assert all(w > 0 for w in tim.values())


def test_loop_context_polarity_is_authored_and_detection_is_shared():
    """The P-032g reviewer finding exercised: the status->score map is
    profile-authored — timbaland reads iconic HIGHER (96 > 90) and static
    LOWER (10 < 15) than the reference — while every DETECTION floor is
    identical, so both profiles read the same status from the same stems
    (one shared basis, never forked)."""
    tim = load_profile("timbaland").doctrine["scorers"]["loop_context"]
    ref = load_profile("halee_ramone").doctrine["scorers"]["loop_context"]
    assert tim["iconic"] == 96.0 and tim["iconic"] > ref["iconic"]
    assert tim["static"] == 10.0 and tim["static"] < ref["static"]
    for floor in ("width_floor", "transient_lift_floor", "groove_transient_floor",
                  "definition_crest_db", "evolution_rms_floor_db",
                  "evolution_width_floor", "evolution_brightness_floor"):
        assert tim[floor] == ref[floor], f"detection floor {floor} forked"


# --------------------------------------------------------------------------- #
# 2. BYTE-IDENTITY OF THE DEFAULT — the reference path did not move.
# --------------------------------------------------------------------------- #
def test_default_doctrine_surface_unchanged(analyzed):
    """The DEFAULT producer still lands the pinned base values (all 14
    components + overalls 73.8 / 70.7 / 74.3) — authoring a second JSON
    touched nothing on the reference path."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_default_creative_surface_unchanged(analyzed):
    """The DEFAULT creative surface still equals the base capture (every
    branch winner, every variant kind + overall + fired nudges) — creative
    EMPTY diff."""
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


def test_regression_still_green_full_corpus():
    """The golden corpus regression (which runs the DEFAULT producer) still
    passes 93/93 (the P-035 corpus — see conftest.py) with the second profile authored."""
    from logic_mix_os.regression import run_regression_suite

    report = run_regression_suite(_ROOT / "fixtures")
    assert report["tests_run"] == 93
    assert report["passed"] == 93
    assert report["failed"] == 0


# --------------------------------------------------------------------------- #
# 3. THE DIFFERENTIAL IS ALIVE — the first non-byte-identical output.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_overall_differs_from_the_default_on_every_fixture(name, analyzed, timbaland_analyzed):
    """``analyze(producer="timbaland")`` produces a DIFFERENT
    ``overall_mix_readiness_score`` than the default on all three fixtures —
    real inequality, through the REAL pipeline."""
    tim = timbaland_analyzed[name].doctrine_score["overall_mix_readiness_score"]
    ref = analyzed[name].doctrine_score["overall_mix_readiness_score"]
    assert tim != ref, f"{name}: timbaland overall {tim} == reference {ref}"


def test_loop_fixtures_feel_the_static_loop_pressure(analyzed, timbaland_analyzed):
    """Direction, on the loop fixtures: both read STATIC, timbaland weights
    ``loop_context`` > 0 AND authors static at 10 (< the reference's 15) — so
    the timbaland overall sits BELOW the reference overall, and removing the
    loop_context term from timbaland's own weighted mean would RAISE it (the
    static-loop pressure is genuinely felt in the overall)."""
    w = TIM_WEIGHTS
    for name in ("dense_chorus_with_loops", "splice_loop_problem"):
        tim_ds = timbaland_analyzed[name].doctrine_score
        ref_ds = analyzed[name].doctrine_score
        assert tim_ds["loop_context_score"] == 10.0   # authored static polarity
        assert ref_ds["loop_context_score"] == 15.0   # the reference's own
        assert (tim_ds["overall_mix_readiness_score"]
                < ref_ds["overall_mix_readiness_score"])
        without_lc = {k: tim_ds[k] for k in w if k != "loop_context_score"}
        mean_without = doctrine_engine._clamp(
            sum(without_lc[k] * w[k] for k in without_lc)
            / sum(w[k] for k in without_lc)
        )
        assert mean_without > tim_ds["overall_mix_readiness_score"], name


def test_divergence_is_attributable_components_shared_judgment_swapped(analyzed, timbaland_analyzed):
    """ATTRIBUTION: the axes are shared measurable substrate — every component
    score is identical across the two producers EXCEPT ``loop_context`` on
    the loop fixtures, where the profile-authored polarity (10 vs 15) is the
    live difference. The taste divergence lives in the WEIGHTS (the overall),
    not in forked measurement."""
    for name in FIXTURE_NAMES:
        tim_ds = timbaland_analyzed[name].doctrine_score
        ref_ds = analyzed[name].doctrine_score
        for key in COMPONENT_KEYS:
            if key == "loop_context_score" and name != "simple_vocal_piano_song":
                assert tim_ds[key] != ref_ds[key]
            else:
                assert tim_ds[key] == ref_ds[key], (name, key)


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_overall_is_timbalands_weighted_mean(name, timbaland_analyzed):
    """The timbaland overall is exactly the weighted mean under TIM_WEIGHTS —
    the authored weights are the live lever, end to end."""
    ds = timbaland_analyzed[name].doctrine_score
    present = {k: ds[k] for k in TIM_WEIGHTS if ds[k] is not None}
    expected = doctrine_engine._clamp(
        sum(present[k] * TIM_WEIGHTS[k] for k in present)
        / sum(TIM_WEIGHTS[k] for k in present)
    )
    assert ds["overall_mix_readiness_score"] == expected


def test_creative_emphasis_diverges_too(analyzed, timbaland_analyzed):
    """The creative judgment is profile-authored as well: on the dense loop
    fixture the subtraction move scores from TIMBALAND's curated table (86.7,
    not the reference's 85.3), and on the intimate fixture the search mode
    resolves through timbaland's OWN authored ``default_creative_mode`` table
    to its ``intimate_mode`` ("conservative") — P-033 wired the table per
    call, the pre-registered flip of the honest fallback this test pinned
    at P-032h (the reference's intimate mode — ``vocal_truth`` since the
    P-038 rename, ``ramone_vocal_truth`` before it — exists only in the
    reference's table)."""
    tim_loop = _loop_branch(timbaland_analyzed["dense_chorus_with_loops"].creative)
    ref_loop = _loop_branch(analyzed["dense_chorus_with_loops"].creative)
    tim_b = _variant_by_id(tim_loop, "loop_B")["scores"]["overall_score"]
    ref_b = _variant_by_id(ref_loop, "loop_B")["scores"]["overall_score"]
    assert tim_b == pytest.approx(86.7, abs=1e-9)
    assert ref_b == pytest.approx(85.3, abs=1e-9)
    assert tim_b != ref_b

    assert analyzed["simple_vocal_piano_song"].creative["search_mode"] == "vocal_truth"
    assert timbaland_analyzed["simple_vocal_piano_song"].creative["search_mode"] == "conservative"
    assert "vocal_truth" not in load_profile("timbaland").search_modes
    assert load_profile("timbaland").default_creative_mode["intimate_mode"] == "conservative"
    assert "conservative" in load_profile("timbaland").search_modes


# --------------------------------------------------------------------------- #
# 4. THE GATES FLIP LIVE — protect vs deconstruct, on the SAME evidence.
# --------------------------------------------------------------------------- #
def test_gates_flip_timbaland_protects_the_iconic_loop_halee_ramone_fires(analyzed):
    """THE PAYOFF, live: identical result, identical iconic read on the shared
    detection basis — halee_ramone (protect=false) fires the loop_deconstruct
    promotion at its exact base values; timbaland (protect=true) withholds it
    (the loop is the record's identity)."""
    res = _with_iconic_loop(analyzed)
    tim = load_profile("timbaland")
    ref = load_profile("halee_ramone")
    assert _foregrounded_loop(res) is True          # the evidence WOULD fire
    assert _loop_status(res, tim) == "iconic"       # same read under BOTH
    assert _loop_status(res, ref) == "iconic"       # profiles' constants

    assert _apply_promotions("loop_deconstruct", res, tim) == []
    fired_ref = _apply_promotions("loop_deconstruct", res, ref)
    assert [f[2] for f in fired_ref] == [PROMOTION_REASON]

    out_tim = run_creative_engine(res, res.creative["search_mode"], profile=tim)
    out_ref = run_creative_engine(res, res.creative["search_mode"], profile=ref)
    loop_a_tim = _variant_by_id(_loop_branch(out_tim), "loop_A")
    loop_a_ref = _variant_by_id(_loop_branch(out_ref), "loop_A")
    assert "score_nudges" not in loop_a_tim["scores"]
    assert loop_a_ref["scores"].get("score_nudges") == [PROMOTION_REASON]
    assert loop_a_ref["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)
    assert _loop_branch(out_ref)["winning"]["winning_variant"] == "loop_A"


def test_static_loop_still_gets_the_contrast_pressure_under_timbaland(analyzed):
    """Protection is for ICONIC-functioning loops only: a STATIC-reading
    dominant loop still fires timbaland's promotion (its own authored
    evidence line) — static wallpaper gets the deconstruct pressure."""
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    tim = load_profile("timbaland")
    assert _foregrounded_loop(res) is True
    assert _loop_status(res, tim) == "static"

    fired = _apply_promotions("loop_deconstruct", res, tim)
    assert [f[2] for f in fired] == [TIM_PROMOTION_REASON]
    out = run_creative_engine(res, res.creative["search_mode"], profile=tim)
    loop_a = _variant_by_id(_loop_branch(out), "loop_A")
    assert loop_a["scores"].get("score_nudges") == [TIM_PROMOTION_REASON]
    assert loop_a["scores"]["overall_score"] == pytest.approx(84.7, abs=1e-9)


def test_masked_lead_override_holds_for_both_profiles(analyzed):
    """THE RAMONE GATE is producer-agnostic: with the lead vocal bad-masked,
    the promotion fires under BOTH profiles even on an iconic read —
    protection can never shadow a buried lead."""
    res = _with_masked_lead(_with_iconic_loop(analyzed))
    tim = load_profile("timbaland")
    ref = load_profile("halee_ramone")
    assert _loop_status(res, tim) == "iconic"   # the loop's own read stands

    fired_tim = _apply_promotions("loop_deconstruct", res, tim)
    fired_ref = _apply_promotions("loop_deconstruct", res, ref)
    assert [f[2] for f in fired_tim] == [TIM_PROMOTION_REASON]
    assert [f[2] for f in fired_ref] == [PROMOTION_REASON]


# --------------------------------------------------------------------------- #
# 5. THE CONFIDENCE MAP, VERBATIM-PINNED — claims machine-checked.
# --------------------------------------------------------------------------- #
def test_timbaland_confidence_map_verbatim():
    """The full authored map, pinned verbatim in authoring order (the P-031
    reviewer judgment note carried out: the pin guards against duplicate-area
    and extra-key drift that validation alone accepts)."""
    assert load_profile("timbaland").confidence_map == TIM_AUTHORED_MAP


def test_confidence_level_distribution():
    """5 high (groove / space+contrast / low-end / loop / retained
    measurement), 1 limited (vocal blend — live and measured since
    P-034/P-035, coverage-bounded per the P-036 re-authoring),
    5 deferred (the engine boundaries, shared with the reference)."""
    levels = [e["level"] for e in load_profile("timbaland").confidence_map]
    assert levels.count("high") == 5
    assert levels.count("limited") == 1
    assert levels.count("deferred") == 5


def test_limited_blend_entry_matches_the_opt_in_policy():
    """The honest corollary, RE-AUTHORED LIVE in P-036: the opt-in this
    profile authors is live and MEASURED on real exported-stem data — the
    P-035 differential (vocal_role_fit 85.0 vs the reference's 65.0, +0.7
    overall at the authored 0.4 weight). The entry stays LIMITED because the
    constraint is real and stated: masker-set-bounded coverage, the
    unconsumed info tier, and the per-track-risk exclusion. P-038 tidied the
    text only (the two P-036 reviewer observations): the "either side"
    shorthand now carries the masker-arm's heard qualifier, and the 65.0/85.0
    differential states its per-stem mechanics (the reference draws the
    masked penalty once per stem; the accepted blend waives both)."""
    p = load_profile("timbaland")
    limited = [e for e in p.confidence_map if e["level"] == "limited"]
    assert limited == [TIM_AUTHORED_MAP[5]]
    # the measured differential is stated, the falsified claims are gone
    assert "measured on real exported-stem data" in limited[0]["reason"]
    assert "85.0" in limited[0]["reason"] and "65.0" in limited[0]["reason"]
    assert "heard masker standing forward" in limited[0]["reason"]  # P-038
    assert "the accepted blend waives both" in limited[0]["reason"]  # P-038
    assert "only against the lead" not in limited[0]["reason"]
    assert "dormant" not in limited[0]["reason"]
    assert p.vocal_blend_policy["acceptable_blend"] is True  # opt-in + honesty


def test_deferred_entries_carry_the_standing_engine_boundaries():
    """The five deferrals are engine boundaries, not profile choices — the
    same honest limits the reference declares, present verbatim."""
    deferred = [e for e in load_profile("timbaland").confidence_map
                if e["level"] == "deferred"]
    assert deferred == TIM_AUTHORED_MAP[6:]
    areas = " | ".join(e["area"] for e in deferred)
    for standing in ("cultural loop recognizability", "true hook recurrence",
                     "motif provenance", "fingerprint typing",
                     "kick/sub temporal interlock", "per-section true-sub movement"):
        assert standing in areas, f"standing deferral {standing!r} missing"


def test_high_claims_are_consistent_with_the_machine_facts():
    """No high entry overclaims: every axis a 'weighted up' entry names IS
    weighted above the reference; every axis the 'retained measurement' entry
    names IS live at reduced weight (0 < timbaland < reference)."""
    tim = load_profile("timbaland").doctrine["weights"]
    ref = load_profile("halee_ramone").doctrine["weights"]
    for key in ("beat_identity_score", "groove_coherence_score",
                "rhythmic_surprise_score",              # entry 1
                "negative_space_score", "section_contrast_score",
                "dynamic_mix_score",                     # entry 2
                "low_end_motion_score",                  # entry 3
                "loop_context_score"):                   # entry 4
        assert tim[key] > ref[key], f"{key} claimed weighted-up but is not"
    for key in RELAXED:                                  # entry 5
        assert 0 < tim[key] < ref[key], f"{key} claimed retained-reduced but is not"


def test_whole_profile_language_is_observational():
    """USER-MANDATED: zero judgment words across the ENTIRE authored JSON —
    philosophy, reasons, biases, switches, map. The profile reports and
    decides; it never rules on other producers or styles."""
    blob = _TIMBALAND_PATH.read_text(encoding="utf-8").lower()
    hits = judgment_word_hits(blob)
    assert not hits, f"judgment word(s) {hits} in timbaland.json"


# --------------------------------------------------------------------------- #
# 6. SAFETY INVARIANCE — nothing weaker than the reference, anywhere.
# --------------------------------------------------------------------------- #
def test_kill_switches_are_the_five_safety_plus_timbalands_aesthetic(timbaland_analyzed):
    """KILL_SWITCHES for timbaland = the 5 hardcoded SAFETY switches (first,
    verbatim, in order) + timbaland's authored aesthetic list — recomposed
    per call, with the safety half untouchable."""
    tim = load_profile("timbaland")
    for res in timbaland_analyzed.values():
        ks = res.governance["kill_switches"]
        assert ks == governance._SAFETY_KILL_SWITCHES + tim.aesthetic_kill_switches
        assert ks[:5] == governance._SAFETY_KILL_SWITCHES


def test_timbaland_aesthetic_switches_are_a_superset_of_the_reference():
    """Equivalent-or-stricter, literally: every reference aesthetic switch is
    present verbatim in timbaland's list (including the vocal-intelligibility
    switch), plus timbaland's own groove-first additions."""
    tim = set(load_profile("timbaland").aesthetic_kill_switches)
    ref = set(load_profile("halee_ramone").aesthetic_kill_switches)
    assert ref <= tim
    assert "Never make the lead vocal less intelligible unless explicitly approved." in tim


def test_comparable_safety_structures_equivalent_or_stricter():
    """The explicit comparison, structure by structure: risk penalties, both
    creative caps, veto thresholds, the taste clamp, the intimate-width
    penalty + retained width veto, the nudge penalties, the blend confidence
    floor, and the promotion reward — none weaker than the reference."""
    tim = load_profile("timbaland")
    ref = load_profile("halee_ramone")
    assert tim.risk_penalty == ref.risk_penalty
    assert tim.creative_nudge_cap == ref.creative_nudge_cap
    assert tim.creative_promotion_cap == ref.creative_promotion_cap
    assert tim.veto_thresholds["reject_below"] >= ref.veto_thresholds["reject_below"]
    assert tim.veto_thresholds["align_veto_below"] >= ref.veto_thresholds["align_veto_below"]
    assert tim.veto_thresholds["align_fallback"] == ref.veto_thresholds["align_fallback"]
    assert tim.taste_max_delta <= ref.taste_max_delta
    assert (tim.taste_triangle["intimate_width_penalty"]
            >= ref.taste_triangle["intimate_width_penalty"])
    # the vocal-safety dim stays inside the emotion blend
    assert "vocal_belief_score" in tim.taste_triangle["emotion_dims"]
    # the intimate-width veto is retained, not relaxed past the veto line
    assert (tim.truth_alignment["intimate"]["width_bloom"]
            < tim.veto_thresholds["align_veto_below"])
    # nudge rows: same (kinds, evidence, dim) coverage; penalties >= reference
    def rows(table):
        return {(frozenset(r["kinds"]), r["evidence"], r["dim"]): r["delta"]
                for r in table}
    tim_rows, ref_rows = rows(tim.nudge_table), rows(ref.nudge_table)
    assert set(tim_rows) == set(ref_rows)
    for key, ref_delta in ref_rows.items():
        assert tim_rows[key] <= ref_delta, f"nudge {key} weaker than reference"
    # the blend gate's dial: the floor is never lowered
    assert (tim.vocal_blend_policy["confidence_floor"]
            >= ref.vocal_blend_policy["confidence_floor"])
    # the promotion reward is not enlarged
    assert (sum(r["delta"] for r in tim.promotion_table)
            <= sum(r["delta"] for r in ref.promotion_table))


def test_risk_class_semantics_unchanged():
    """Risk-class semantics are engine-fixed: class 5 is blocked whatever the
    selected profile says, and timbaland declares risk_class 0 (recommend-
    only, same as the reference)."""
    assert load_profile("timbaland").metadata["risk_class"] == 0
    assert load_profile("halee_ramone").metadata["risk_class"] == 0
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


# --------------------------------------------------------------------------- #
# 7. NO-ALIASING WITH TWO LIVE PROFILES — the carry-forward's moment.
# --------------------------------------------------------------------------- #
def test_two_live_profiles_no_aliasing_through_real_analyze():
    """Load BOTH profiles, run the REAL ``analyze()`` with each OBJECT, and
    prove neither profile's structures were mutated and the module
    ``_DEFAULT_PROFILE``s (all three consumers) are untouched."""
    tim = load_profile("timbaland")
    ref = load_profile("halee_ramone")
    snapshots = {
        "tim_doctrine": copy.deepcopy(tim.doctrine),
        "tim_kind_scores": copy.deepcopy(tim.kind_scores),
        "tim_map": copy.deepcopy(tim.confidence_map),
        "tim_switches": copy.deepcopy(tim.aesthetic_kill_switches),
        "ref_doctrine": copy.deepcopy(ref.doctrine),
        "ref_kind_scores": copy.deepcopy(ref.kind_scores),
        "ref_map": copy.deepcopy(ref.confidence_map),
        "ref_switches": copy.deepcopy(ref.aesthetic_kill_switches),
    }
    name = "dense_chorus_with_loops"
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    analyze(str(ROOT / "fixtures" / name / "stems"), manifest, producer=tim)
    analyze(str(ROOT / "fixtures" / name / "stems"), manifest, producer=ref)

    assert tim.doctrine == snapshots["tim_doctrine"]
    assert tim.kind_scores == snapshots["tim_kind_scores"]
    assert tim.confidence_map == snapshots["tim_map"]
    assert tim.aesthetic_kill_switches == snapshots["tim_switches"]
    assert ref.doctrine == snapshots["ref_doctrine"]
    assert ref.kind_scores == snapshots["ref_kind_scores"]
    assert ref.confidence_map == snapshots["ref_map"]
    assert ref.aesthetic_kill_switches == snapshots["ref_switches"]


def test_module_default_profiles_untouched_by_timbaland_runs(timbaland_analyzed):
    """After full timbaland analyses, every consumer module's
    ``_DEFAULT_PROFILE`` (the byte-identity anchor) still equals a fresh
    reference load — the second live profile reached nothing shared."""
    fresh = load_profile("halee_ramone")
    for mod in (doctrine_engine, creative, governance):
        dp = mod._DEFAULT_PROFILE
        assert dp.metadata["name"] == "halee_ramone"
        assert dp.doctrine == fresh.doctrine
        assert dp.kind_scores == fresh.kind_scores
        assert dp.confidence_map == fresh.confidence_map
        assert dp.aesthetic_kill_switches == fresh.aesthetic_kill_switches
        assert dp.protect_iconic_loops is False
        assert dp.vocal_blend_policy == fresh.vocal_blend_policy
    # the module-level composed default kill switches did not move either
    assert governance.KILL_SWITCHES == (
        governance._SAFETY_KILL_SWITCHES + fresh.aesthetic_kill_switches
    )


def test_loads_are_fresh_mutation_cannot_reach_a_reload_or_the_other_profile():
    tim = load_profile("timbaland")
    tim.doctrine["weights"]["beat_identity_score"] = 99.0
    tim.confidence_map[0]["level"] = "deferred"
    tim.aesthetic_kill_switches.append("mutated")
    assert load_profile("timbaland").doctrine["weights"] == TIM_WEIGHTS
    assert load_profile("timbaland").confidence_map == TIM_AUTHORED_MAP
    assert "mutated" not in load_profile("timbaland").aesthetic_kill_switches
    assert load_profile("halee_ramone").doctrine["weights"]["beat_identity_score"] == 0


# --------------------------------------------------------------------------- #
# 8. CONFIDENCE RENDERING — the artifacts carry TIMBALAND's map.
# --------------------------------------------------------------------------- #
def test_doctrine_score_carries_timbalands_map_fresh(timbaland_analyzed):
    """Every timbaland analysis carries TIMBALAND's map verbatim under the
    machine-readable ``confidence`` key — a fresh copy, never an alias."""
    tim = load_profile("timbaland")
    for res in timbaland_analyzed.values():
        conf = res.doctrine_score["confidence"]
        assert conf == TIM_AUTHORED_MAP
        assert conf is not tim.confidence_map


def test_artifacts_render_timbalands_map_not_the_references(timbaland_analyzed, tmp_path):
    """``write_artifacts`` on a timbaland analysis renders TIMBALAND's
    entries in doctrine_score.json AND the verdict markdown 'Confidence'
    section — and none of the reference's own voice leaks in."""
    res = timbaland_analyzed["simple_vocal_piano_song"]
    write_artifacts(res, tmp_path)

    dsj = json.loads((tmp_path / "doctrine_score.json").read_text(encoding="utf-8"))
    assert dsj["confidence"] == TIM_AUTHORED_MAP

    md = (tmp_path / "mix_verdict.md").read_text(encoding="utf-8")
    assert "## Confidence" in md
    for entry in TIM_AUTHORED_MAP:
        assert entry["area"] in md, entry["area"]
        assert entry["reason"] in md, entry["area"]
    assert "syncopated negative space" in md          # the cited technique family
    for leak in REFERENCE_ONLY_STRINGS:
        assert leak not in md, f"reference map leaked into the verdict: {leak}"
    hi, li, de = md.index("**High**"), md.index("**Limited**"), md.index("**Deferred**")
    assert hi < li < de
