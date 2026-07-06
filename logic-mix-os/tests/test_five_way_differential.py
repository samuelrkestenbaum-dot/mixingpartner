"""P-050 Commit-2 — THE FIVE-WAY DIFFERENTIAL PROOF: Halee/Ramone vs
Timbaland vs Quincy Jones vs Brian Eno vs Chris Lord-Alge, same stems — the
proof the producer framework keeps WIDENING the aesthetic map with a fifth,
distinct value system instead of clustering.

Same four fixtures, FIVE producers, one shared measurement substrate. This
sibling to tests/test_four_way_differential.py (which keeps its own local
four-producer tuple) adds the fifth column and proves the user's eight
requirements for CLA, each pinned permanently (run first, captured, then
pinned — the packet's deterministic discipline):

1-4. **CLA differs from EACH of the four** — a different overall on every
   fixture, through the REAL pipeline, resolved dynamically by name; all FIVE
   overalls PAIRWISE distinct on every fixture (min separation 1.0).
5. **CLA is coherent, not averaged mush** — nine weight axes outside the four's
   envelope (six above all four, three below all four — past the at-least-2
   floor), an argmax (section_contrast) none of the four has, and a branch
   WINNER no other producer picks (chorus_lift_D — the drums carry the chorus
   where all four others ride chorus_lift_B); his overall reconstructs from
   the reference's measurements plus his authored values alone.
6. **Confidence honesty** — every ``high`` entry the pipeline ships names its
   documented-technique basis; his own three deferrals (loudness maximization
   / saturation / whole-mix translation); no producer's voice leaks.
7. **Existing profiles do not drift** — the four shipped JSONs are
   byte-unchanged (sha256 blob pins), the four-way overalls re-assert
   byte-stable with the fifth profile live, the committed trees' headlines
   re-read unchanged, and the four sample trees + nine mode demos are
   untouched (their staleness pins stay green).
8. **Safety invariant five-way** — identical veto thresholds, the 5 hardcoded
   SAFETY kill-switches leading verbatim, no class-5 anywhere in CLA's plans,
   every variant non-destructive, his artifacts schema-valid — PLUS the CLA
   clause: the loudness kill-switch present VERBATIM in his JSON, and dropout
   stays governed by ZERO EMISSION (he reaches no dropout family anywhere, so
   no dropout id appears across any of his modes on any fixture).

Plus the creative differential: the shared-name modes (``conservative`` and
``experimental`` exist in all five profiles) emit FIVE pinned,
pairwise-distinct chorus_lift sets on the same stems.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json

import pytest

from logic_mix_os import governance, pipeline
from logic_mix_os.constants import RISK_CLASSES
from logic_mix_os.creative import generate_variants, run_creative_engine
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest
from logic_mix_os.validation.output_validator import (
    load_schema,
    validate_instance,
    validate_output,
)

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE
from test_differential_proof import SAFETY_KILL_SWITCHES
from test_four_way_differential import (
    COMMITTED_TREE_HEADLINES,
    COMPONENT_KEYS,
    FOUR_WAY_OVERALLS,
    _weighted_overall,
)
from test_cla_profile import (
    C_AUTHORED_MAP,
    C_MODE_TABLE,
    C_REACHING_MODES,
    C_WEIGHTS,
    DOCUMENTED_STAMP,
    LOUDNESS_KILL_SWITCH,
)
from test_mode_forking import PROBLEM_IDS, _ids, _kinds
from test_textural_coherence import _coherent_beds, _incoherent_beds

PRODUCERS = ("halee_ramone", "timbaland", "quincy_jones", "brian_eno",
             "chris_lord_alge")
EXISTING = ("halee_ramone", "timbaland", "quincy_jones", "brian_eno")
ALL_FIXTURES = tuple(FIXTURE_NAMES) + (VOCAL_CHOP_FIXTURE,)
STATIC_FIXTURES = ("dense_chorus_with_loops", "splice_loop_problem",
                   VOCAL_CHOP_FIXTURE)
DROPOUT = "negative_space_dropout"
DENSE = "dense_chorus_with_loops"

# Same stems, FIVE judgments — every overall pinned to the decimal. The four
# existing columns ARE the standing P-045 four-way table (re-asserted with the
# fifth profile live = requirement 7); the chris_lord_alge column was measured
# by running the engine, then pinned (min separation from any existing value
# is 1.0, on the simple + chop fixtures).
FIVE_WAY_OVERALLS = {
    "simple_vocal_piano_song": dict(
        FOUR_WAY_OVERALLS["simple_vocal_piano_song"], chris_lord_alge=74.8),
    "dense_chorus_with_loops": dict(
        FOUR_WAY_OVERALLS["dense_chorus_with_loops"], chris_lord_alge=59.6),
    "splice_loop_problem": dict(
        FOUR_WAY_OVERALLS["splice_loop_problem"], chris_lord_alge=58.1),
    "vocal_chop_groove": dict(
        FOUR_WAY_OVERALLS["vocal_chop_groove"], chris_lord_alge=67.8),
}

# CLA's FULL 14-component picture, pinned per fixture (measured, then pinned).
# Every component equals the shared substrate except the two AUTHORED
# divergence channels: the loop-context polarity (static -> his authored 18.0
# wherever the reference reads 15.0) and the blend gate on the 4th fixture
# (85.0 accepted vs the reference's 65.0 protected, at his authored 0.85
# floor over the 0.95-confidence classifications).
CLA_COMPONENTS = {
    "simple_vocal_piano_song": {
        "physical_space_score": 58.0, "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0, "depth_hierarchy_score": 40.0,
        "section_contrast_score": 100.0, "static_mix_score": 80.0,
        "dynamic_mix_score": 52.7, "beat_identity_score": 89.1,
        "negative_space_score": 62.3, "groove_coherence_score": 45.0,
        "rhythmic_surprise_score": 51.1, "low_end_motion_score": 60.0,
        "loop_context_score": 50.0, "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,
    },
    "dense_chorus_with_loops": {
        "physical_space_score": 67.6, "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0, "depth_hierarchy_score": 65.3,
        "section_contrast_score": 82, "static_mix_score": 64.0,
        "dynamic_mix_score": 23.4, "beat_identity_score": 52.7,
        "negative_space_score": 15.0, "groove_coherence_score": 99.1,
        "rhythmic_surprise_score": 20.0, "low_end_motion_score": 21.1,
        "loop_context_score": 18.0, "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 27.0,
    },
    "splice_loop_problem": {
        "physical_space_score": 81.3, "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0, "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82, "static_mix_score": 70.0,
        "dynamic_mix_score": 23.1, "beat_identity_score": 46.0,
        "negative_space_score": 20.0, "groove_coherence_score": 45.0,
        "rhythmic_surprise_score": 27.8, "low_end_motion_score": 25.0,
        "loop_context_score": 18.0, "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,
    },
    "vocal_chop_groove": {
        "physical_space_score": 81.3, "emotional_hierarchy_score": 86.0,
        "vocal_centrality_score": 90.0, "depth_hierarchy_score": 72.0,
        "section_contrast_score": 82, "static_mix_score": 80.0,
        "dynamic_mix_score": 28.2, "beat_identity_score": 63.6,
        "negative_space_score": 19.4, "groove_coherence_score": 99.4,
        "rhythmic_surprise_score": 35.6, "low_end_motion_score": 60.0,
        "loop_context_score": 18.0, "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,
    },
}

# Exactly these doctrine_score keys may diverge between CLA and the REFERENCE
# per fixture — every divergence explained (his own weighted mean / his own
# authored map / the identity surface / the authored loop polarity 18 vs 15 /
# the authored blend gate isolated to the vocal_role_fit axis on the chop).
DIVERGENT_VS_REFERENCE = {
    "simple_vocal_piano_song": {
        "overall_mix_readiness_score", "confidence", "producer",
    },
    "dense_chorus_with_loops": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "splice_loop_problem": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "vocal_chop_groove": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score", "vocal_role_fit_score", "evidence",
    },
}
# Against timbaland / quincy / eno (all opt into the blend), the chop readings
# AGREE on vocal_role_fit (CLA's stricter 0.85 floor is still cleared at 0.95),
# so only the authored loop polarity remains (18 vs 10 / 12 / 35).
DIVERGENT_VS_OPT_IN_PRODUCERS = {
    "simple_vocal_piano_song": {
        "overall_mix_readiness_score", "confidence", "producer",
    },
    "dense_chorus_with_loops": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "splice_loop_problem": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
    "vocal_chop_groove": {
        "overall_mix_readiness_score", "confidence", "producer",
        "loop_context_score",
    },
}

CLA_IDENTITY = {
    "name": "chris_lord_alge",
    "display_name": "Chris Lord-Alge",
    "provenance": "hand-curated-documented",
    "confidence": "high",
}

# CLA's plan surface, pinned (measured, then pinned): his own authored search
# modes on both resolution paths, and his branch winners — including the
# winner NO other producer picks: ``chorus_lift_D`` (the drum-room bloom — the
# drums carry the chorus) wins his chorus_lift branch on every loop fixture,
# where all four existing producers pick ``chorus_lift_B``.
CLA_SEARCH_MODES = {
    "simple_vocal_piano_song": "front_and_center",   # his intimate_mode
    "dense_chorus_with_loops": "commit_and_slam",    # his default_mode
    "splice_loop_problem": "commit_and_slam",
    "vocal_chop_groove": "commit_and_slam",
}
CLA_WINNERS = {
    "simple_vocal_piano_song": {"vocal_belief": "vocal_A"},
    "dense_chorus_with_loops": {
        "chorus_lift": "chorus_lift_D", "density": "density_B",
        "loop": "loop_A", "depth": "depth_A", "vocal_belief": "vocal_A",
    },
    "splice_loop_problem": {
        "chorus_lift": "chorus_lift_D", "loop": "loop_A",
        "vocal_belief": "vocal_A",
    },
    "vocal_chop_groove": {
        "chorus_lift": "chorus_lift_D", "loop": "loop_A",
        "depth": "depth_A", "vocal_belief": "vocal_A",
    },
}

# THE SHARED-NAME MODE PINS (five-way): ``conservative`` and ``experimental``
# exist in all five profiles — same stems, same problem, FIVE
# pairwise-distinct chorus_lift candidate-id sets per mode.
CONSERVATIVE_CHORUS_SETS = {
    "halee_ramone": {"chorus_lift_B", "chorus_lift_C", "chorus_lift_D"},
    "timbaland": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                  "chorus_lift_D"},
    "quincy_jones": {"chorus_lift_B", "chorus_lift_C"},
    "brian_eno": {"chorus_lift_B", "chorus_lift_D"},
    # CLA suppresses subtractive_drop (commit, don't thin) — he alone keeps
    # the width push while withholding the subtractive move.
    "chris_lord_alge": {"chorus_lift_A", "chorus_lift_C", "chorus_lift_D"},
}
EXPERIMENTAL_CHORUS_SETS = {
    "halee_ramone": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                     "chorus_lift_D"},
    "timbaland": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                  "chorus_lift_D", "chorus_lift_F"},
    "quincy_jones": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                     "chorus_lift_D", "chorus_lift_E"},
    "brian_eno": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                  "chorus_lift_F"},
    # CLA suppresses subtractive_drop AND reaches arrangement_lift (chorus_E)
    # — the big-chorus impact through the arrangement, energy not aggression.
    "chris_lord_alge": {"chorus_lift_A", "chorus_lift_C", "chorus_lift_D",
                        "chorus_lift_E"},
}

# REQUIREMENT 7, byte-level: the FOUR shipped JSONs are BLOB-UNCHANGED — the
# three P-045 pins (fe8d947 base) plus the brian_eno hash at the P-050 base.
# P-056 CONSCIOUSLY re-pinned these (every profile JSON gained the additive
# textural_coherence scorer block + weight; brian_eno additionally opts into the
# axis and flips its confidence entry). P-057 CONSCIOUSLY re-pinned the
# quincy_jones hash again (he opts the axis into weight 0.6 + gains a textural
# confidence entry); halee_ramone/timbaland/brian_eno are byte-unchanged from
# P-056. A test-visible decision, never drift.
EXISTING_JSON_SHA256 = {
    "halee_ramone":
        "fd99d9f1e31400c3c4c764e2bc3a1c7d185fb3d69292c98641170548838df25d",
    "timbaland":
        "8715541491253d4376ea5b0132e5a5d96c16710f180e1d49df1cd4affe5d04d9",
    "quincy_jones":
        "0b28f144f93b481d32a5a4608f13ab370435c421137a79c854874adcd99fc6ec",
    "brian_eno":
        "95407ae7ca8056665f58cf5356a8cd98e750ece33333a24386c01b955def256d",
}


# --------------------------------------------------------------------------- #
# Shared expensive fixture: every producer on every fixture, once per module.
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def five_analyzed():
    """The full pipeline once per (producer, fixture) — resolved DYNAMICALLY
    by name (the no-code-changes acceptance clause)."""
    out = {}
    for name in ALL_FIXTURES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        stems = str(ROOT / "fixtures" / name / "stems")
        out[name] = {p: analyze(stems, manifest, producer=p) for p in PRODUCERS}
    return out


# =========================================================================== #
# Requirements 1 + 2 + 3 + 4 — CLA differs from ALL FOUR, every fixture, pinned.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_five_way_overalls_pinned_and_pairwise_distinct(name, five_analyzed):
    """Same stems, five judgments: every producer's overall lands its pinned
    value, and the five values are PAIRWISE distinct — five value systems, not
    a rebadged pole and not an average of the existing four."""
    seen = {}
    for producer, res in five_analyzed[name].items():
        overall = res.doctrine_score["overall_mix_readiness_score"]
        assert overall == FIVE_WAY_OVERALLS[name][producer], (name, producer)
        seen[producer] = overall
    assert len(set(seen.values())) == 5, (name, seen)


def test_dynamically_discovered_identity_reaches_every_artifact(five_analyzed):
    """``analyze(producer="chris_lord_alge")`` resolved the profile BY NAME
    from the producers directory, and every analysis carries CLA's identity
    surface — the four metadata fields, never risk_class."""
    for name in ALL_FIXTURES:
        producer = five_analyzed[name]["chris_lord_alge"].doctrine_score["producer"]
        assert producer == CLA_IDENTITY, name
        assert "risk_class" not in producer, name


# =========================================================================== #
# Requirement 5 — coherent, not averaged mush: his own poles + his own voice.
# =========================================================================== #
def test_not_averaged_mush_poles_outside_the_four_way_envelope():
    """The requirement floor is 'at least 2 axes outside the envelope'; CLA
    clears it NINE times on the weight table alone (six axes strictly above
    all four existing profiles, three strictly below) — and his argmax
    (section_contrast) is an axis NO existing profile has as its heaviest."""
    c = load_profile("chris_lord_alge")
    others = {p: load_profile(p) for p in EXISTING}
    cw = c.doctrine["weights"]
    outside = []
    for key in cw:
        vals = [others[p].doctrine["weights"][key] for p in EXISTING]
        if cw[key] > max(vals) or cw[key] < min(vals):
            outside.append(key)
    assert set(outside) >= {
        "section_contrast_score", "beat_identity_score",
        "vocal_centrality_score", "dynamic_mix_score", "low_end_motion_score",
        "vocal_role_fit_score", "physical_space_score", "depth_hierarchy_score",
        "static_mix_score"}
    assert len(outside) >= 2  # the user's floor, cleared nine times over

    assert max(cw, key=cw.get) == "section_contrast_score"
    for p, other in others.items():
        w = other.doctrine["weights"]
        argmaxes = {k for k, v in w.items() if v == max(w.values())}
        assert "section_contrast_score" not in argmaxes, p


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_cla_component_picture_pinned(name, five_analyzed):
    ds = five_analyzed[name]["chris_lord_alge"].doctrine_score
    assert {k: ds[k] for k in COMPONENT_KEYS} == CLA_COMPONENTS[name]


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_cla_overall_is_his_own_weighted_mean(name, five_analyzed):
    ds = five_analyzed[name]["chris_lord_alge"].doctrine_score
    assert _weighted_overall("chris_lord_alge", {k: ds[k] for k in COMPONENT_KEYS}) \
        == FIVE_WAY_OVERALLS[name]["chris_lord_alge"]
    assert load_profile("chris_lord_alge").doctrine["weights"] == C_WEIGHTS


def test_cla_reconstructs_from_the_references_measurements(five_analyzed):
    """The strongest attributability form (the P-041 reconstruction pattern,
    five-way edition): rebuild CLA's overall on every fixture from the
    REFERENCE's component scores plus CLA's AUTHORED values alone — substitute
    the authored static polarity (15.0 -> 18.0) and the authored blend
    acceptance (65.0 -> 85.0 on the chop fixture), apply his weights, land on
    his pinned overall to the decimal. Every delta traces to an authored
    value; nothing else moved."""
    c_static = load_profile("chris_lord_alge").doctrine["scorers"]["loop_context"]["static"]
    assert c_static == 18.0
    for name in ALL_FIXTURES:
        ref_ds = five_analyzed[name]["halee_ramone"].doctrine_score
        rebuilt = {k: ref_ds[k] for k in COMPONENT_KEYS}
        if ref_ds["loop_context_score"] == 15.0:       # the reference's static read
            rebuilt["loop_context_score"] = c_static
        if name == VOCAL_CHOP_FIXTURE:
            assert ref_ds["vocal_role_fit_score"] == 65.0
            rebuilt["vocal_role_fit_score"] = 85.0     # the authored blend gate
        assert _weighted_overall("chris_lord_alge", rebuilt) \
            == FIVE_WAY_OVERALLS[name]["chris_lord_alge"], name


def test_section_contrast_weight_is_a_live_lever_not_a_label(five_analyzed):
    """Coherence is behavioral: his heaviest axis genuinely PRESSES the
    judgment. On the sparse piano fixture (section_contrast 100.0 — his
    highest component) the weight-zero counterfactual (his own components,
    the section_contrast term removed from his mean — what a reference-style
    0 weight would read) costs a traceable 4.4 points, the largest single-axis
    lever in his table; and the lift is genuinely his heaviest axis pressing
    the verdict, not a label. The differential IS the philosophy."""
    ds = five_analyzed["simple_vocal_piano_song"]["chris_lord_alge"].doctrine_score
    components = {k: ds[k] for k in COMPONENT_KEYS}
    without = {k: v for k, v in components.items() if k != "section_contrast_score"}
    cost = round(ds["overall_mix_readiness_score"]
                 - _weighted_overall("chris_lord_alge", without), 1)
    assert cost == pytest.approx(4.4, abs=0.05)  # section_contrast lifts his verdict materially
    assert cost > 4.0  # well past a rounding artifact — a live lever


def test_plan_surface_speaks_his_own_authored_voice(five_analyzed):
    """The behavioral half of coherence: CLA's plans resolve HIS OWN authored
    search modes on both paths (front_and_center intimate / commit_and_slam
    default — mode names no other profile carries), no fallback fires, his
    branch winners land his curated values — and his chorus_lift winner is
    ``chorus_lift_D`` (the drum-room bloom) on every loop fixture, a winner
    NONE of the other four picks (they all ride ``chorus_lift_B``)."""
    for name in ALL_FIXTURES:
        cr = five_analyzed[name]["chris_lord_alge"].creative
        assert cr["search_mode"] == CLA_SEARCH_MODES[name], name
        assert "search_mode_fallback" not in cr, name
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in cr["branches"]}
        assert winners == CLA_WINNERS[name], name
    for other in EXISTING:
        modes = load_profile(other).search_modes
        assert "front_and_center" not in modes, other
        assert "commit_and_slam" not in modes, other
    for name in ("dense_chorus_with_loops", "splice_loop_problem",
                 VOCAL_CHOP_FIXTURE):
        for other in EXISTING:
            winners = {b["problem_id"]: b["winning"]["winning_variant"]
                       for b in five_analyzed[name][other].creative["branches"]}
            assert winners["chorus_lift"] == "chorus_lift_B", (other, name)


# =========================================================================== #
# The creative differential — five pinned, pairwise-distinct shared-name sets.
# =========================================================================== #
def test_shared_name_modes_five_pairwise_distinct_sets(five_analyzed):
    """THE MODE-LEVEL FIVE-WAY PIN: ``conservative`` and ``experimental``
    exist in all five profiles. Same stems, same problem, five
    pairwise-distinct chorus_lift candidate-id sets per mode — each
    reconstructing from its own authored JSON."""
    dense = five_analyzed[DENSE]["halee_ramone"]
    for mode, pins in (("conservative", CONSERVATIVE_CHORUS_SETS),
                       ("experimental", EXPERIMENTAL_CHORUS_SETS)):
        sets = {}
        for producer in PRODUCERS:
            out = run_creative_engine(dense, mode, profile=load_profile(producer))
            branch = next(b for b in out["branches"]
                          if b["problem_id"] == "chorus_lift")
            sets[producer] = set(_ids(branch["variants"]))
        assert sets == pins, mode
        assert len({frozenset(s) for s in sets.values()}) == 5, mode


def test_cla_default_flow_is_neutral_zero_fork_surface(five_analyzed):
    """The evidence-key discipline under CLA: BOTH his resolution paths
    (front_and_center intimate / commit_and_slam default) author neutral
    declarations and zero reach, so his default flow carries NO declaration
    surface and NO per-branch fork keys — byte-silent, like the reference."""
    for name in ALL_FIXTURES:
        cr = five_analyzed[name]["chris_lord_alge"].creative
        assert "search_mode_declarations" not in cr, name
        for b in cr["branches"]:
            assert "mode_fork" not in b, (name, b["problem_id"])


# =========================================================================== #
# Requirement 6 — CONFIDENCE HONESTY at the differential level.
# =========================================================================== #
def test_artifacts_carry_clas_own_map_fresh(five_analyzed):
    c = load_profile("chris_lord_alge")
    for name in ALL_FIXTURES:
        conf = five_analyzed[name]["chris_lord_alge"].doctrine_score["confidence"]
        assert conf == C_AUTHORED_MAP, name          # the verbatim guard, live
        assert conf is not c.confidence_map, name    # fresh, never an alias
    for p in EXISTING:
        assert C_AUTHORED_MAP != load_profile(p).confidence_map, p


def test_no_high_entry_lacks_a_documented_technique_reason(five_analyzed):
    """The user's grounding standard, re-asserted on the LIVE artifact
    surface: every ``high`` entry the pipeline ships names its
    documented-technique basis; everything else is limited/deferred
    (LLM-synthesized-as-high is forbidden by construction)."""
    for name in ALL_FIXTURES:
        for entry in five_analyzed[name]["chris_lord_alge"].doctrine_score["confidence"]:
            if entry["level"] == "high":
                assert DOCUMENTED_STAMP in entry["reason"], (name, entry["area"])
            assert entry["level"] in ("high", "limited", "deferred")


def test_clas_own_deferrals_ship_on_the_live_surface(five_analyzed):
    """CLA's own three honest deferrals — concepts his identity implies that
    no axis measures — ship verbatim on the live artifact: loudness
    maximization (the stress-test signature, out of scope by design),
    saturation/harmonic energy, and whole-mix translation across systems."""
    conf = five_analyzed[DENSE]["chris_lord_alge"].doctrine_score["confidence"]
    deferred_areas = {e["area"] for e in conf if e["level"] == "deferred"}
    assert {"loudness maximization",
            "saturation and harmonic energy as its own measurement",
            "whole-mix translation across playback systems"} <= deferred_areas
    loud = next(e for e in conf if e["area"] == "loudness maximization")
    assert "safety concern" in loud["reason"]


# =========================================================================== #
# Requirement 7 — EXISTING PROFILES DO NOT DRIFT (with the fifth live).
# =========================================================================== #
def test_existing_producer_jsons_are_blob_unchanged():
    """Byte-level requirement 7: the four shipped JSONs hash to their
    packet-base sha256 values — no tuning of any existing producer rode in
    with the fifth."""
    producers_dir = ROOT / "logic_mix_os" / "doctrine" / "producers"
    for name, expected in EXISTING_JSON_SHA256.items():
        digest = hashlib.sha256((producers_dir / f"{name}.json").read_bytes())
        assert digest.hexdigest() == expected, name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_existing_producers_unmoved_at_their_pinned_values(name, five_analyzed):
    """The standing four-producer pins hold byte-stable with chris_lord_alge
    in the directory: every existing overall re-asserts its four-way value."""
    for producer in EXISTING:
        ds = five_analyzed[name][producer].doctrine_score
        assert ds["overall_mix_readiness_score"] \
            == FOUR_WAY_OVERALLS[name][producer], (name, producer)


def test_committed_sample_tree_headlines_unmoved():
    """Two of the FOUR committed demo trees re-read directly: the reference
    and timbaland headline overalls stand (the byte-level staleness pin
    covering all four committed trees lives in tests/test_sample_refresh.py
    and runs against the same committed bytes — unaffected by a profile-only
    fifth producer)."""
    for tree, headline in COMMITTED_TREE_HEADLINES.items():
        ds = json.loads((ROOT / "examples" / tree / "doctrine_score.json")
                        .read_text(encoding="utf-8"))
        assert ds["overall_mix_readiness_score"] == headline, tree


# =========================================================================== #
# Requirement 8 — SAFETY INVARIANT five-way + the CLA dropout clause.
# =========================================================================== #
def test_kill_switches_lead_with_the_five_safety_switches(five_analyzed):
    """On every fixture the composed kill-switch list under CLA leads with the
    5 hardcoded SAFETY switches FIRST, VERBATIM, IN ORDER — followed by
    exactly his authored aesthetic list (which itself keeps the loudness
    safety line verbatim)."""
    assert governance._SAFETY_KILL_SWITCHES == SAFETY_KILL_SWITCHES
    aesthetic = load_profile("chris_lord_alge").aesthetic_kill_switches
    for name in ALL_FIXTURES:
        ks = five_analyzed[name]["chris_lord_alge"].governance["kill_switches"]
        assert ks[:5] == SAFETY_KILL_SWITCHES, name
        assert ks == SAFETY_KILL_SWITCHES + aesthetic, name
        assert LOUDNESS_KILL_SWITCH in ks, name


def test_loudness_kill_switch_is_verbatim_in_his_json():
    """THE CLA CLAUSE of requirement 8: the loudness kill-switch is present
    VERBATIM in his authored JSON — a loudness-maximalist who still cannot
    weaken the loudness rail."""
    raw = json.loads(
        (ROOT / "logic_mix_os" / "doctrine" / "producers" / "chris_lord_alge.json")
        .read_text(encoding="utf-8"))
    assert LOUDNESS_KILL_SWITCH in raw["aesthetic_kill_switches"]


def test_veto_thresholds_identical_across_all_five_profiles():
    c = load_profile("chris_lord_alge").veto_thresholds
    for p in EXISTING:
        assert c == load_profile(p).veto_thresholds, p


def test_no_destructive_recommendation_under_cla(five_analyzed):
    """Class 5 appears NOWHERE in CLA's plans; every action passes the
    kill-switch validator; every creative variant is reversible; the class-5
    block itself stays engine-fixed."""
    for name in ALL_FIXTURES:
        res = five_analyzed[name]["chris_lord_alge"]
        for track in res.mix_plan["per_track_actions"]:
            assert track["risk_class"] < 5 and track["risk_class"] in RISK_CLASSES
            for action in track["actions"]:
                assert action["risk_class"] < 5, (name, track["track"])
                assert governance.validate_action_safety(action)["blocked"] is False
            for auto in track["automation"]:
                assert auto["risk_class"] < 5, name
        for m in res.mix_plan["mute_candidates"]:
            assert m["risk_class"] < 5, name
        for branch in res.creative["branches"]:
            for v in branch["variants"]:
                assert v["reversibility"] == "non_destructive_duplicate_track"
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


def test_cla_plans_and_artifacts_validate(five_analyzed, tmp_path):
    """Machine-checkable coherence: CLA's mix_plan validates against the schema
    on every fixture, and his rendered artifact tree passes full output
    validation."""
    schema = load_schema("mix_plan.schema.json")
    for name in ALL_FIXTURES:
        assert validate_instance(
            five_analyzed[name]["chris_lord_alge"].mix_plan, schema) == [], name
    out = tmp_path / "chris_lord_alge"
    write_artifacts(five_analyzed[VOCAL_CHOP_FIXTURE]["chris_lord_alge"], out)
    report = validate_output(out)
    assert report["ok"], report["errors"]


def test_dropout_stays_governed_by_zero_emission_across_his_modes(five_analyzed):
    """The CLA dropout clause of requirement 8: CLA reaches the dropout family
    on ZERO modes (he FILLS space, he does not carve it), so NO dropout id
    appears across ANY of his modes — every authored mode plus no-mode and an
    unknown mode — on EVERY fixture. Dropout stays governed by never being
    admitted, not by a filter he leans on."""
    prof = load_profile("chris_lord_alge")
    assert all(entry["reach_kinds"] == [] or "negative_space_dropout"
               not in entry["reach_kinds"]
               for entry in C_MODE_TABLE.values())
    assert DROPOUT not in {k for m in C_REACHING_MODES
                           for k in C_MODE_TABLE[m]["reach_kinds"]}
    for name in ALL_FIXTURES:
        res = five_analyzed[name]["chris_lord_alge"]
        for mode in list(prof.search_modes) + [None, "no_such_mode"]:
            out = run_creative_engine(res, mode, profile=prof)
            for b in out["branches"]:
                assert DROPOUT not in _kinds(b["variants"]), (name, mode, b["problem_id"])
                assert not {"chorus_lift_F", "density_E"} & set(_ids(b["variants"])), \
                    (name, mode, b["problem_id"])


# =========================================================================== #
# The P-041 divergence audit — CLA diverges on EXACTLY the authored set.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_the_reference(name, five_analyzed):
    """Key-by-key doctrine audit against halee_ramone — CLA diverges on
    EXACTLY the explained authored-taste set and nothing else (shared
    substrate; the chop fixture's evidence divergence stays isolated to the
    vocal_role_fit axis, itself the authored blend gate)."""
    ref_ds = five_analyzed[name]["halee_ramone"].doctrine_score
    c_ds = five_analyzed[name]["chris_lord_alge"].doctrine_score
    assert set(ref_ds) == set(c_ds)
    diverged = {k for k in ref_ds if ref_ds[k] != c_ds[k]}
    assert diverged == DIVERGENT_VS_REFERENCE[name], (name, diverged)
    if "evidence" in diverged:
        ev_diverged = {k for k in ref_ds["evidence"]
                       if ref_ds["evidence"][k] != c_ds["evidence"][k]}
        assert ev_diverged == {"vocal_role_fit"}, (name, ev_diverged)
    assert ref_ds["warnings"] == c_ds["warnings"], name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_the_opt_in_producers(name, five_analyzed):
    """The same audit against the three opt-in producers: all opt into the
    blend, so on the chop fixture the readings AGREE (identical vocal_role_fit
    score and evidence — CLA's stricter 0.85 floor is still cleared at 0.95)
    and the only component divergence anywhere is the authored loop polarity
    (18.0 vs 10.0 / 12.0 / 35.0)."""
    c_ds = five_analyzed[name]["chris_lord_alge"].doctrine_score
    for producer in ("timbaland", "quincy_jones", "brian_eno"):
        other_ds = five_analyzed[name][producer].doctrine_score
        assert set(other_ds) == set(c_ds)
        diverged = {k for k in other_ds if other_ds[k] != c_ds[k]}
        assert diverged == DIVERGENT_VS_OPT_IN_PRODUCERS[name], \
            (name, producer, diverged)
        assert other_ds["evidence"] == c_ds["evidence"], (name, producer)


# =========================================================================== #
# P-056 — THE FIFTEENTH-AXIS PERMANENT PROOF (textural_coherence).
#
# The engine-deepening packet's binding differential: Eno's overall MOVED on a
# new measured signal; the non-Eno producers weighting the axis at 0 are
# byte-identical (the weight-0 proof); the axis key is present + measured in ALL
# FIVE artifacts; Eno's confidence-map deferral flipped live; and the axis is
# load-bearing — zeroing his weight reverts his overall and flipping the
# dispersion sign swaps the coherent/incoherent synthetic cases.
#
# P-057 SHRANK the weight-0 set from four to THREE: quincy_jones now opts the
# axis into weight 0.6 (his own P-057 MOVE + sabotage proof lives in the
# dedicated block at the end of this file), leaving {halee_ramone, timbaland,
# chris_lord_alge} as the byte-identical weight-0 set below.
# =========================================================================== #

# Eno's PRE-AXIS overalls — his standing pre-P-056 four-way values (the 14-term
# weighted mean, textural excluded). The axis moved every one of them.
PRE_AXIS_ENO_OVERALLS = {
    "simple_vocal_piano_song": 65.4,
    "dense_chorus_with_loops": 57.8,
    "splice_loop_problem": 59.3,
    "vocal_chop_groove": 65.5,
}
# P-057: quincy_jones dropped from this set (he now weights the axis 0.6); the
# byte-identical weight-0 set is the remaining three.
_NON_ENO = ("halee_ramone", "timbaland", "chris_lord_alge")
_TEXTURAL = "textural_coherence_score"


def _mean_excluding(producer, components, drop):
    """The weighted mean over ``components`` with ``drop`` removed — a
    reference-style weight-0 view of that axis (it leaves both the numerator and
    the denominator)."""
    return _weighted_overall(producer, {k: v for k, v in components.items()
                                        if k != drop})


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_p056_eno_overall_moved_vs_pre_axis_baseline(name, five_analyzed):
    """(a) Eno's overall CHANGES vs his pre-axis baseline: the 14-term mean
    (textural excluded) reproduces his standing pre-P-056 value, the live
    15-term overall is his pinned five-way value, and the two DIFFER — the axis
    is a new measured signal, not a re-weighting of old ones."""
    ds = five_analyzed[name]["brian_eno"].doctrine_score
    comps = {k: ds[k] for k in COMPONENT_KEYS}
    pre_axis = _mean_excluding("brian_eno", comps, _TEXTURAL)
    assert pre_axis == PRE_AXIS_ENO_OVERALLS[name], name          # the 14-term baseline
    assert ds["overall_mix_readiness_score"] \
        == FIVE_WAY_OVERALLS[name]["brian_eno"], name             # the live 15-term
    assert ds["overall_mix_readiness_score"] != pre_axis, name    # the axis MOVED him


def test_p056_move_is_largest_on_the_bed_carrying_fixture(five_analyzed):
    """The move is genuinely bed-driven: the dense fixture (the only one with
    >=2 texture beds — an INCOHERENT pair at 27.0) moves Eno's overall more than
    the <2-bed fixtures, which read the neutral fallback."""
    def move(name):
        ds = five_analyzed[name]["brian_eno"].doctrine_score
        comps = {k: ds[k] for k in COMPONENT_KEYS}
        return abs(ds["overall_mix_readiness_score"]
                   - _mean_excluding("brian_eno", comps, _TEXTURAL))
    dense = move("dense_chorus_with_loops")
    assert dense > 3.0
    for lone in ("splice_loop_problem", "vocal_chop_groove"):
        assert dense > move(lone)


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_p056_four_non_eno_byte_identical_the_weight_zero_proof(name, five_analyzed):
    """(b) The weight-0 non-Eno producers are BYTE-IDENTICAL: adding the 15th
    axis at weight 0 leaves both the numerator and the denominator untouched, so
    the 15-term mean equals the 14-term mean equals the live overall — while the
    axis is still present and measured (a 0..100 number), just unweighted.
    P-057 shrank ``_NON_ENO`` from four to three (quincy_jones now weights the
    axis 0.6); this proof holds for the remaining {halee, timbaland, cla}."""
    for producer in _NON_ENO:
        ds = five_analyzed[name][producer].doctrine_score
        comps_15 = {k: ds[k] for k in COMPONENT_KEYS}
        assert load_profile(producer).doctrine["weights"][_TEXTURAL] == 0
        assert ds[_TEXTURAL] is not None and 0.0 <= ds[_TEXTURAL] <= 100.0
        assert _weighted_overall(producer, comps_15) \
            == _mean_excluding(producer, comps_15, _TEXTURAL) \
            == ds["overall_mix_readiness_score"], (name, producer)


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_p056_axis_key_present_and_measured_in_all_five_artifacts(name, five_analyzed):
    """(c) The ``textural_coherence_score`` key + its evidence line are present
    in ALL FIVE producers' artifacts (measured for all; weighted only by Eno)."""
    for producer in PRODUCERS:
        ds = five_analyzed[name][producer].doctrine_score
        assert _TEXTURAL in ds and ds[_TEXTURAL] is not None
        assert 0.0 <= ds[_TEXTURAL] <= 100.0
        assert ds["evidence"]["textural_coherence"], (name, producer)
    # measured identically across producers (the constants block is shared) —
    # the per-fixture reading does not depend on the profile's weight.
    vals = {five_analyzed[name][p].doctrine_score[_TEXTURAL] for p in PRODUCERS}
    assert len(vals) == 1, (name, vals)


def test_p056_zeroing_enos_weight_reverts_his_overall_to_the_pre_axis_value(five_analyzed):
    """(e-i) The weight is LOAD-BEARING, not decorative: re-scoring with Eno's
    weight zeroed (what the four non-Eno producers ship) reverts his overall to
    his pre-axis value on every fixture; DELETING the weight entirely is caught
    LOUDLY (the aggregate genuinely dereferences it), never silently ignored."""
    base = load_profile("brian_eno")
    zeroed_doc = copy.deepcopy(base.doctrine)
    zeroed_doc["weights"][_TEXTURAL] = 0
    zeroed = dataclasses.replace(base, doctrine=zeroed_doc)

    deleted_doc = copy.deepcopy(base.doctrine)
    del deleted_doc["weights"][_TEXTURAL]
    deleted = dataclasses.replace(base, doctrine=deleted_doc)

    for name in ALL_FIXTURES:
        res = five_analyzed[name]["brian_eno"]
        # thread the SAME groove snapshot the pipeline fed doctrine, so the
        # re-score reproduces the pipeline exactly (only the weight differs)
        groove = res.expanded.get("groove")
        args = (res.records, res.section_analysis, res.masking_report,
                res.mix_metrics, res.project.intent)
        reverted = doctrine_engine.score_doctrine(*args, profile=zeroed, groove=groove)
        assert reverted["overall_mix_readiness_score"] \
            == PRE_AXIS_ENO_OVERALLS[name], name
        # still present + measured, just unweighted (the reference posture)
        assert reverted[_TEXTURAL] is not None
        # a control: his LIVE weight (1.2) reproduces his moved five-way overall
        live = doctrine_engine.score_doctrine(*args, profile=base, groove=groove)
        assert live["overall_mix_readiness_score"] \
            == FIVE_WAY_OVERALLS[name]["brian_eno"], name
        # deleting the weight entirely is caught loudly (genuinely dereferenced)
        with pytest.raises(KeyError):
            doctrine_engine.score_doctrine(*args, profile=deleted, groove=groove)


def test_p056_flipping_the_dispersion_sign_swaps_the_distinctness_cases(monkeypatch):
    """(e-ii) The metric TRULY reads dispersion: with the real scorer a coherent
    bed set outscores an incoherent one; monkeypatching the single sign seam
    (``_coherence_from_dispersion`` -> the dispersion itself, dropping the
    ``baseline -`` inversion) SWAPS them — the coherent set now scores below the
    incoherent one. Only possible if coherence is genuinely anti-dispersion."""
    doctrine = load_profile("halee_ramone").doctrine

    def tc(beds):
        return doctrine_engine._textural_coherence(beds, doctrine)[0]

    coherent_real, incoherent_real = tc(_coherent_beds()), tc(_incoherent_beds())
    assert coherent_real > incoherent_real  # the real reading

    monkeypatch.setattr(doctrine_engine, "_coherence_from_dispersion",
                        lambda baseline, dispersion: dispersion)
    coherent_flip, incoherent_flip = tc(_coherent_beds()), tc(_incoherent_beds())
    assert coherent_flip < incoherent_flip  # the sign flip swaps the ordering


# =========================================================================== #
# P-057 — THE NON-ENO TEXTURAL WEIGHTING PERMANENT PROOF (Quincy Jones).
#
# The profile-data packet's binding differential: Quincy is the SECOND producer
# (after Eno) to opt into the 15th axis — at a support-tier 0.6 with an honest
# ``limited`` confidence entry (documented big-band/ensemble arranging, secondary
# to his distinct-readable-layer center of gravity). His overall MOVED on the
# same measured signal; the move is bed-driven (largest on the only >=2-bed
# fixture); the SHRUNK weight-0 set {halee, timbaland, cla} stays byte-identical;
# Eno is unchanged; the axis is present + measured in all five; and Quincy's
# weight is load-bearing — zeroing it reverts his overall to his pre-P-057 value,
# deleting it is caught loudly. Mirrors the P-056 Eno differential/sabotage.
# =========================================================================== #

# Quincy's PRE-P-057 overalls — his standing post-P-056 five-way values (the
# 14-term weighted mean, textural weighted 0). His 0.6 opt-in moved every one.
PRE_P057_QUINCY_OVERALLS = {
    "simple_vocal_piano_song": 70.0,
    "dense_chorus_with_loops": 62.1,
    "splice_loop_problem": 61.9,
    "vocal_chop_groove": 68.8,
}


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_p057_quincy_overall_moved_vs_pre_p057_baseline(name, five_analyzed):
    """(a) Quincy's overall CHANGES vs his pre-P-057 baseline: the 14-term mean
    (textural excluded) reproduces his standing post-P-056 value, the live
    15-term overall is his pinned five-way value, and the two DIFFER — the 0.6
    opt-in is a new measured signal pressing his mean, not a re-weighting."""
    ds = five_analyzed[name]["quincy_jones"].doctrine_score
    comps = {k: ds[k] for k in COMPONENT_KEYS}
    pre = _mean_excluding("quincy_jones", comps, _TEXTURAL)
    assert pre == PRE_P057_QUINCY_OVERALLS[name], name          # the 14-term baseline
    assert ds["overall_mix_readiness_score"] \
        == FIVE_WAY_OVERALLS[name]["quincy_jones"], name         # the live 15-term
    assert ds["overall_mix_readiness_score"] != pre, name        # the axis MOVED him


def test_p057_quincy_move_is_largest_on_the_bed_carrying_fixture(five_analyzed):
    """The move is genuinely bed-driven: the dense fixture (the only one with
    >=2 texture beds — an INCOHERENT pair at 27.0) moves Quincy's overall more
    than every <2-bed fixture (each reading the neutral 55.0 fallback)."""
    def move(name):
        ds = five_analyzed[name]["quincy_jones"].doctrine_score
        comps = {k: ds[k] for k in COMPONENT_KEYS}
        return abs(ds["overall_mix_readiness_score"]
                   - _mean_excluding("quincy_jones", comps, _TEXTURAL))
    dense = move(DENSE)
    assert dense > 1.0
    for lone in ("simple_vocal_piano_song", "splice_loop_problem",
                 "vocal_chop_groove"):
        assert dense > move(lone), lone


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_p057_three_weight_zero_non_eno_stay_byte_identical(name, five_analyzed):
    """(b) The SHRUNK weight-0 set {halee, timbaland, cla} stays BYTE-IDENTICAL
    after Quincy's opt-in: each weights the axis 0, so the 15-term mean equals
    the 14-term mean equals the live overall, and the live overall equals its
    standing four-way pin — Quincy's move did not leak into the weight-0 set."""
    assert set(_NON_ENO) == {"halee_ramone", "timbaland", "chris_lord_alge"}
    for producer in _NON_ENO:
        ds = five_analyzed[name][producer].doctrine_score
        comps = {k: ds[k] for k in COMPONENT_KEYS}
        assert load_profile(producer).doctrine["weights"][_TEXTURAL] == 0
        assert _weighted_overall(producer, comps) \
            == _mean_excluding(producer, comps, _TEXTURAL) \
            == ds["overall_mix_readiness_score"], (name, producer)


def test_p057_eno_unchanged_and_axis_weighted_by_eno_and_quincy(five_analyzed):
    """(c/d) Eno is UNCHANGED (weight 1.2 + his pinned five-way overalls), and
    the axis is now weighted by TWO producers — Eno (1.2) and Quincy (0.6) — yet
    still present + measured (a 0..100 number, an evidence line) in ALL FIVE
    artifacts, read IDENTICALLY across producers (the constants block is shared;
    the per-fixture value does not depend on the weight)."""
    assert load_profile("brian_eno").doctrine["weights"][_TEXTURAL] == 1.2
    assert load_profile("quincy_jones").doctrine["weights"][_TEXTURAL] == 0.6
    for name in ALL_FIXTURES:
        assert five_analyzed[name]["brian_eno"].doctrine_score[
            "overall_mix_readiness_score"] == FIVE_WAY_OVERALLS[name]["brian_eno"], name
        vals = set()
        for producer in PRODUCERS:
            ds = five_analyzed[name][producer].doctrine_score
            assert ds[_TEXTURAL] is not None and 0.0 <= ds[_TEXTURAL] <= 100.0
            assert ds["evidence"]["textural_coherence"], (name, producer)
            vals.add(ds[_TEXTURAL])
        assert len(vals) == 1, (name, vals)


def test_p057_quincy_confidence_entry_is_honest_limited(five_analyzed):
    """(d) Quincy's live artifact carries his P-057 textural entry at level
    ``limited`` (NOT ``high`` — the honest support-tier reading that runs partly
    counter to his center of gravity), naming its documented arranging basis and
    the dispersion measurement; Eno's SAME-area entry stays ``high`` (his center)
    — the two producers weight one axis from two honestly-labelled convictions."""
    conf = five_analyzed[DENSE]["quincy_jones"].doctrine_score["confidence"]
    entry = next(e for e in conf
                 if e["area"] == "textural coherence as its own measurement")
    assert entry["level"] == "limited"
    assert "documented Quincy Jones technique" in entry["reason"]
    assert "cross-bed dispersion statistic" in entry["reason"]
    eno_conf = five_analyzed[DENSE]["brian_eno"].doctrine_score["confidence"]
    eno_entry = next(e for e in eno_conf
                     if e["area"] == "textural coherence as its own measurement")
    assert eno_entry["level"] == "high"
    assert entry["reason"] != eno_entry["reason"]


def test_p057_zeroing_quincys_weight_reverts_his_overall_to_pre_p057(five_analyzed):
    """(e) Quincy's weight is LOAD-BEARING, not decorative: re-scoring with his
    weight zeroed (what the three weight-0 producers ship) reverts his overall to
    his pre-P-057 value on every fixture; his LIVE 0.6 weight reproduces his
    moved five-way overall; DELETING the weight entirely is caught LOUDLY (the
    aggregate genuinely dereferences it), never silently ignored."""
    base = load_profile("quincy_jones")
    zeroed_doc = copy.deepcopy(base.doctrine)
    zeroed_doc["weights"][_TEXTURAL] = 0
    zeroed = dataclasses.replace(base, doctrine=zeroed_doc)

    deleted_doc = copy.deepcopy(base.doctrine)
    del deleted_doc["weights"][_TEXTURAL]
    deleted = dataclasses.replace(base, doctrine=deleted_doc)

    for name in ALL_FIXTURES:
        res = five_analyzed[name]["quincy_jones"]
        # thread the SAME groove snapshot the pipeline fed doctrine, so the
        # re-score reproduces the pipeline exactly (only the weight differs)
        groove = res.expanded.get("groove")
        args = (res.records, res.section_analysis, res.masking_report,
                res.mix_metrics, res.project.intent)
        reverted = doctrine_engine.score_doctrine(*args, profile=zeroed, groove=groove)
        assert reverted["overall_mix_readiness_score"] \
            == PRE_P057_QUINCY_OVERALLS[name], name
        # still present + measured, just unweighted (the reference posture)
        assert reverted[_TEXTURAL] is not None
        # a control: his LIVE weight (0.6) reproduces his moved five-way overall
        live = doctrine_engine.score_doctrine(*args, profile=base, groove=groove)
        assert live["overall_mix_readiness_score"] \
            == FIVE_WAY_OVERALLS[name]["quincy_jones"], name
        # deleting the weight entirely is caught loudly (genuinely dereferenced)
        with pytest.raises(KeyError):
            doctrine_engine.score_doctrine(*args, profile=deleted, groove=groove)
