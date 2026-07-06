"""P-045 Commit-2 — THE FOUR-WAY DIFFERENTIAL PROOF: Halee/Ramone vs
Timbaland vs Quincy Jones vs Brian Eno, same stems — the proof the producer
framework widens the aesthetic map instead of clustering.

Same four fixtures, FOUR producers, one shared measurement substrate. The
user's eight requirements, each pinned permanently (run first, captured,
then pinned — the packet's deterministic discipline):

1. **Eno differs from Halee/Ramone** — a different overall on every fixture,
   through the REAL pipeline, resolved dynamically by name.
2. **Eno differs from Timbaland** — same, against the groove pole.
3. **Eno differs from Quincy** — same, against the arrangement pole. All
   four overalls PAIRWISE distinct on every fixture.
4. **Eno is coherent, not averaged mush** — SEVEN weight axes outside the
   existing three's envelope (three above all, four below all — past the
   at-least-2 floor), an argmax (negative_space) none of the three has, the
   strictest blend floor, the highest static-loop polarity; his overall
   reconstructs from the reference's measurements plus his authored values
   alone; and his plan surface speaks his own authored voice (his own mode
   names on both resolution paths, his own curated values, his own evidence
   lines — and a branch WINNER no other producer picks: the intimacy pass).
5. **Confidence honesty** — the verbatim map pin (test_eno_profile.
   E_AUTHORED_MAP) is the guard; here: every ``high`` entry the pipeline
   ships names its documented-technique basis, the rendered artifacts carry
   HIS map, and no producer's distinct voice leaks into another's artifacts
   (four-way).
6. **Existing profiles do not drift** — the three shipped JSONs are
   byte-unchanged (sha256 blob pins), the standing three-producer overalls
   re-assert byte-stable with the fourth profile live (73.8/70.7/74.3/76.3,
   68.4/52.6/49.7/60.9, 70.0/62.1/61.9/68.8), the committed sample trees'
   headlines re-read unchanged (the byte-level staleness pin stays green in
   tests/test_sample_refresh.py), and regression stays 93/93 (pinned in
   tests/test_three_way_differential.py on the same session corpus).
7. **Safety invariant** — the same veto/audit surface four-way: identical
   veto thresholds, the 5 hardcoded SAFETY kill-switches leading verbatim in
   order, no class-5 anywhere in Eno's plans, every variant non-destructive,
   his artifacts schema-valid — and the P-041 reviewer pattern: the doctrine
   surface audited key by key against every existing producer, diverging on
   EXACTLY the explained authored-taste set and nothing else.
8. **Dropout stays governed** — Eno reaches ``negative_space_dropout`` on
   exactly ``generative_drift`` + ``experimental``: on his reaching modes x
   all four fixtures the ENGINE-owned protection filter holds (no forbidden
   names, no empty emission), the plan-only prose is the pinned P-044 text
   byte-for-byte (engine-owned — a profile cannot reword it), the cap binds
   against HIS honest medium row at runtime (fail-closed, the P-044
   pattern), the masked-lead / only-protected synthetics hold under his
   REAL reaching modes, and his four non-reaching modes (plus no-mode and
   an unknown mode) emit ZERO dropout ids anywhere.

Plus the creative differential: every Eno mode's candidate set reconstructs
from his JSON on disk under the P-043 reach rule — extended to all FOUR
producers — and the shared-name modes (``conservative`` and
``experimental`` exist in all four profiles) emit FOUR pinned,
pairwise-distinct chorus_lift sets on the same stems.
"""

from __future__ import annotations

import hashlib
import json

import pytest

from logic_mix_os import governance, pipeline
from logic_mix_os.constants import RISK_CLASSES
from logic_mix_os.creative import (
    _apply_promotions,
    _dropout_protected_names,
    _foregrounded_loop,
    generate_variants,
    run_creative_engine,
)
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
from test_differential_proof import SAFETY_KILL_SWITCHES, TIMBALAND_ONLY_STRINGS
from test_eno_profile import (
    DOCUMENTED_STAMP,
    E_AUTHORED_MAP,
    E_MODE_TABLE,
    E_PROMOTION_REASON,
    E_REACHING_MODES,
    E_WEIGHTS,
    E_WIDTH_NUDGE,
    ENO_ONLY_STRINGS,
)
from test_mode_forking import (
    ENGINE_POOL,
    PROBLEM_IDS,
    _expected_kind_set,
    _ids,
    _kinds,
    _raw,
)
from test_move_vocabulary_expansion import _fork, _mode, _with_mode
from test_negative_space_dropout import (
    CHORUS_F_CHANGES,
    DENSITY_E_CHANGES,
    _lead,
    _rec,
    _with_records,
)
from test_protect_iconic_loops import (
    _loop_branch,
    _loop_status,
    _variant_by_id,
    _with_iconic_loop,
    _with_masked_lead,
)
from test_quincy_profile import QUINCY_ONLY_STRINGS
from test_three_way_differential import THREE_WAY_OVERALLS
from test_timbaland_profile import REFERENCE_ONLY_STRINGS

PRODUCERS = ("halee_ramone", "timbaland", "quincy_jones", "brian_eno")
EXISTING = ("halee_ramone", "timbaland", "quincy_jones")
ALL_FIXTURES = tuple(FIXTURE_NAMES) + (VOCAL_CHOP_FIXTURE,)
LOOP_FIXTURES = ("dense_chorus_with_loops", "splice_loop_problem")
STATIC_FIXTURES = LOOP_FIXTURES + (VOCAL_CHOP_FIXTURE,)
DROPOUT = "negative_space_dropout"
DENSE = "dense_chorus_with_loops"

COMPONENT_KEYS = [
    "physical_space_score", "emotional_hierarchy_score", "vocal_centrality_score",
    "depth_hierarchy_score", "section_contrast_score", "static_mix_score",
    "dynamic_mix_score", "beat_identity_score", "negative_space_score",
    "groove_coherence_score", "rhythmic_surprise_score",
    "low_end_motion_score", "loop_context_score", "vocal_role_fit_score",
    "textural_coherence_score",  # P-056 — the 15th axis (bed-similarity dispersion)
]

# Same stems, FOUR judgments — every overall pinned to the decimal. The
# three existing columns are the standing P-041 pins (THREE_WAY_OVERALLS),
# re-asserted with the fourth profile live = requirement 6; the brian_eno
# column was measured by running the engine, then pinned.
# P-056: brian_eno's column MOVED (he opts into the 15th axis,
# textural_coherence_score, in his high tier); the other three columns were
# BYTE-IDENTICAL to their pre-P-056 values (their textural weight was 0 — the
# weight-0 proof). P-057: quincy_jones's column MOVED TOO (70.0 -> 69.2 /
# 62.1 -> 60.4 / 61.9 -> 61.6 / 68.8 -> 68.2) — he now opts into the same axis
# at a support-tier 0.6; halee_ramone and timbaland alone stay weight-0
# byte-identical. His new overalls were measured, then pinned.
FOUR_WAY_OVERALLS = {
    "simple_vocal_piano_song": {
        "halee_ramone": 73.8, "timbaland": 68.4, "quincy_jones": 69.2,
        "brian_eno": 64.2,
    },
    "dense_chorus_with_loops": {
        "halee_ramone": 70.7, "timbaland": 52.6, "quincy_jones": 60.4,
        "brian_eno": 54.2,
    },
    "splice_loop_problem": {
        "halee_ramone": 74.3, "timbaland": 49.7, "quincy_jones": 61.6,
        "brian_eno": 58.8,
    },
    "vocal_chop_groove": {
        "halee_ramone": 76.3, "timbaland": 60.9, "quincy_jones": 68.2,
        "brian_eno": 64.3,
    },
}

# Eno's FULL 14-component picture, pinned per fixture (measured, then
# pinned). Every component equals the shared substrate except the two
# AUTHORED divergence channels: the loop-context polarity (static -> his
# authored 35.0 wherever the reference reads 15.0) and the blend gate on the
# 4th fixture (85.0 accepted vs the reference's 65.0 protected, at his
# authored 0.85 floor over the 0.95-confidence classifications).
ENO_COMPONENTS = {
    "simple_vocal_piano_song": {
        "physical_space_score": 58.0,
        "emotional_hierarchy_score": 86.0,
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
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback
    },
    "dense_chorus_with_loops": {
        "physical_space_score": 67.6,
        "emotional_hierarchy_score": 86.0,
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
        "loop_context_score": 35.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 27.0,  # 2 beds (synth pad vs texture loop) — incoherent
    },
    "splice_loop_problem": {
        "physical_space_score": 81.3,
        "emotional_hierarchy_score": 86.0,
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
        "loop_context_score": 35.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback
    },
    "vocal_chop_groove": {
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
        "loop_context_score": 35.0,
        "vocal_role_fit_score": 85.0,
        "textural_coherence_score": 55.0,  # <2 beds → the neutral fallback
    },
}

# THE ANTI-DRIFT SETS (the P-041 reviewer pattern, fourth edition): exactly
# these doctrine_score keys may diverge between brian_eno and EACH existing
# producer, per fixture — every divergence explained (his own weighted mean /
# his own authored map / the P-039 identity surface / the authored loop
# polarity / the authored blend gate, whose evidence divergence is isolated
# to the vocal_role_fit axis). Against timbaland and quincy the blend
# readings AGREE on the chop fixture (all three opt in; Eno's stricter 0.85
# floor is still cleared by the 0.95 classifications), so only the loop
# polarity remains there.
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

ENO_IDENTITY = {
    "name": "brian_eno",
    "display_name": "Brian Eno",
    "provenance": "hand-curated-documented",
    "confidence": "high",
}

# Eno's plan surface, pinned (measured, then pinned): his own authored
# search modes on both resolution paths, and his branch winners — including
# the winner no other producer picks: ``vocal_B`` (the intimacy pass) wins
# his vocal_belief branch on EVERY fixture (environmental quiet outranks the
# phrase ride under his curated table), where all three existing producers
# pick ``vocal_A``.
ENO_SEARCH_MODES = {
    "simple_vocal_piano_song": "ambient_field",     # his intimate_mode
    "dense_chorus_with_loops": "horizontal_time",   # his default_mode
    "splice_loop_problem": "horizontal_time",
    "vocal_chop_groove": "horizontal_time",
}
ENO_WINNERS = {
    "simple_vocal_piano_song": {"vocal_belief": "vocal_B"},
    "dense_chorus_with_loops": {
        "chorus_lift": "chorus_lift_B", "density": "density_B",
        "loop": "loop_B", "depth": "depth_A", "vocal_belief": "vocal_B",
    },
    "splice_loop_problem": {
        "chorus_lift": "chorus_lift_B", "loop": "loop_B",
        "vocal_belief": "vocal_B",
    },
    "vocal_chop_groove": {
        "chorus_lift": "chorus_lift_B", "loop": "loop_B",
        "depth": "depth_A", "vocal_belief": "vocal_B",
    },
}

# The four-way variant-value spread on the shared loop branch (each
# producer's own curated table, same variants) and the width-crowding nudge
# spread on the dense chorus_lift branch — four authored tables, four values.
LOOP_B_BY_PRODUCER = {"halee_ramone": 85.3, "timbaland": 86.7,
                      "quincy_jones": 85.6, "brian_eno": 86.9}
LOOP_A_BY_PRODUCER = {"halee_ramone": 81.9, "timbaland": 80.7,
                      "quincy_jones": 81.9, "brian_eno": 78.6}
NUDGED_CHORUS_A_BY_PRODUCER = {"halee_ramone": 74.9, "timbaland": 69.7,
                               "quincy_jones": 71.3, "brian_eno": 59.7}

# THE SHARED-NAME MODE PINS (the packet's mode-level four-way differential):
# ``conservative`` and ``experimental`` exist in all four profiles — same
# stems, same problem, FOUR pairwise-distinct candidate-id sets, each
# reconstructing from its own authored JSON.
CONSERVATIVE_CHORUS_SETS = {
    "halee_ramone": {"chorus_lift_B", "chorus_lift_C", "chorus_lift_D"},
    "timbaland": {"chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                  "chorus_lift_D"},
    "quincy_jones": {"chorus_lift_B", "chorus_lift_C"},
    "brian_eno": {"chorus_lift_B", "chorus_lift_D"},
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
}

# Eno's dropout emission under his REAL authored reach, per fixture (variant
# id -> resolved targets) — identical on both reaching modes because the
# curated pool and the protection filter are ENGINE-owned; only the reach is
# his. The simple fixture emits NOTHING: its only firing problem
# (vocal_belief) holds no dropout variant.
ENO_DROPOUT_EMISSION = {
    "simple_vocal_piano_song": {},
    "dense_chorus_with_loops": {
        "chorus_lift_F": ["Synth Pad", "Splice Texture Loop"],
        "density_E": ["Acoustic Guitar", "Electric Guitar 1",
                      "Electric Guitar 2", "Synth Pad", "Splice Texture Loop"],
    },
    "splice_loop_problem": {
        "chorus_lift_F": ["Splice Loop"],
    },
    "vocal_chop_groove": {
        "chorus_lift_F": ["BGV Chop"],
    },
}

# Eno's honest dropout value under his own table (mean of his 7 authored
# dims minus his medium translation penalty) — asserted against the JSON.
ENO_DROPOUT_OVERALL = 78.9

# REQUIREMENT 6, byte-level: the three shipped JSONs hash to their pinned
# sha256. P-056 CONSCIOUSLY re-pinned these (a test-visible decision, never
# silent drift): every profile JSON gained the additive
# ``doctrine.scorers.textural_coherence`` block + a ``textural_coherence_score``
# weight of 0 (the four non-Eno producers kept OVERALL byte-stability, not FILE
# byte-stability — the packet's explicit distinction). P-057 re-pinned the
# quincy_jones hash again — CONSCIOUSLY: he opts the axis into weight 0.6 and
# gains a textural confidence entry (halee_ramone and timbaland are unchanged).
EXISTING_JSON_SHA256 = {
    "halee_ramone":
        "fd99d9f1e31400c3c4c764e2bc3a1c7d185fb3d69292c98641170548838df25d",
    "timbaland":
        "8715541491253d4376ea5b0132e5a5d96c16710f180e1d49df1cd4affe5d04d9",
    "quincy_jones":
        "0b28f144f93b481d32a5a4608f13ab370435c421137a79c854874adcd99fc6ec",
}

# Two of the FOUR committed sample trees' headline values (the reference and
# timbaland trees — the two that predate P-046's quincy/eno trees), re-read
# directly — the byte-level staleness pin covering all four committed trees
# lives in tests/test_sample_refresh.py and stays green with the fourth
# profile live.
COMMITTED_TREE_HEADLINES = {
    "sample_output": 76.3,
    "sample_output_timbaland": 60.9,
}


# --------------------------------------------------------------------------- #
# Shared expensive fixtures: eno + quincy + timbaland on all 4 fixtures (the
# reference rides the session-scoped runs).
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def e_analyzed():
    """The full pipeline once per fixture with ``producer="brian_eno"`` —
    resolved DYNAMICALLY by name (the no-code-changes acceptance clause)."""
    results = {}
    for name in ALL_FIXTURES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="brian_eno"
        )
    return results


@pytest.fixture(scope="module")
def q_analyzed():
    results = {}
    for name in ALL_FIXTURES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="quincy_jones"
        )
    return results


@pytest.fixture(scope="module")
def tim_analyzed(chop_groove_analyzed):
    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="timbaland"
        )
    results[VOCAL_CHOP_FIXTURE] = chop_groove_analyzed["timbaland"]
    return results


@pytest.fixture(scope="module")
def ref_analyzed(analyzed, chop_groove_analyzed):
    results = dict(analyzed)
    results[VOCAL_CHOP_FIXTURE] = chop_groove_analyzed["halee_ramone"]
    return results


def _weighted_overall(producer: str, components: dict) -> float:
    weights = load_profile(producer).doctrine["weights"]
    present = {k: components[k] for k in weights if components.get(k) is not None}
    return doctrine_engine._clamp(
        sum(present[k] * weights[k] for k in present)
        / sum(weights[k] for k in present)
    )


def _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed, e_analyzed):
    return {
        "halee_ramone": ref_analyzed[name],
        "timbaland": tim_analyzed[name],
        "quincy_jones": q_analyzed[name],
        "brian_eno": e_analyzed[name],
    }


# =========================================================================== #
# Requirements 1 + 2 + 3 — Eno differs from ALL THREE, every fixture, pinned.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_four_way_overalls_pinned_and_pairwise_distinct(
    name, ref_analyzed, tim_analyzed, q_analyzed, e_analyzed
):
    """Same stems, four judgments: every producer's overall lands its pinned
    value, and the four values are PAIRWISE distinct — four value systems,
    not a rebadged pole and not an average of the existing three."""
    results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed, e_analyzed)
    seen = {}
    for producer, res in results.items():
        overall = res.doctrine_score["overall_mix_readiness_score"]
        assert overall == FOUR_WAY_OVERALLS[name][producer], (name, producer)
        seen[producer] = overall
    assert len(set(seen.values())) == 4, (name, seen)


def test_dynamically_discovered_identity_reaches_every_artifact(e_analyzed):
    """The acceptance clause pair 'dynamically discovered / no code changes':
    ``analyze(producer="brian_eno")`` resolved the profile BY NAME from the
    producers directory (the fixture above), and every analysis carries
    Eno's identity surface — the four metadata fields, never risk_class."""
    for name, res in e_analyzed.items():
        producer = res.doctrine_score["producer"]
        assert producer == ENO_IDENTITY, name
        assert "risk_class" not in producer, name


# =========================================================================== #
# Requirement 4 — coherent, not averaged mush: his own poles + his own voice.
# =========================================================================== #
def test_not_averaged_mush_poles_outside_the_three_way_envelope():
    """The requirement floor is 'at least 2 axes outside the envelope'; Eno
    clears it SEVEN times on the weight table alone (three axes strictly
    above all three existing profiles, four strictly below), plus the
    strictest blend floor and the highest static-loop polarity — and his
    argmax (negative_space) is an axis NO existing profile has as its
    heaviest."""
    e = load_profile("brian_eno")
    others = {p: load_profile(p) for p in EXISTING}
    ew = e.doctrine["weights"]
    outside = []
    for key in ew:
        vals = [others[p].doctrine["weights"][key] for p in EXISTING]
        if ew[key] > max(vals) or ew[key] < min(vals):
            outside.append(key)
    assert set(outside) >= {"negative_space_score", "physical_space_score",
                            "static_mix_score", "vocal_centrality_score",
                            "emotional_hierarchy_score",
                            "section_contrast_score", "dynamic_mix_score"}
    assert len(outside) >= 2  # the user's floor, cleared 7 times over

    assert max(ew, key=ew.get) == "negative_space_score"
    for p, other in others.items():
        w = other.doctrine["weights"]
        argmaxes = {k for k, v in w.items() if v == max(w.values())}
        assert "negative_space_score" not in argmaxes, p

    for p, other in others.items():
        assert e.vocal_blend_policy["confidence_floor"] > \
            other.vocal_blend_policy["confidence_floor"], p
        assert e.doctrine["scorers"]["loop_context"]["static"] > \
            other.doctrine["scorers"]["loop_context"]["static"], p


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_eno_component_picture_pinned(name, e_analyzed):
    ds = e_analyzed[name].doctrine_score
    assert {k: ds[k] for k in COMPONENT_KEYS} == ENO_COMPONENTS[name]


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_eno_overall_is_his_own_weighted_mean(name, e_analyzed):
    ds = e_analyzed[name].doctrine_score
    assert _weighted_overall("brian_eno", {k: ds[k] for k in COMPONENT_KEYS}) \
        == FOUR_WAY_OVERALLS[name]["brian_eno"]
    # and the live weights ARE the pinned authored table
    assert load_profile("brian_eno").doctrine["weights"] == E_WEIGHTS


def test_eno_reconstructs_from_the_references_measurements(ref_analyzed):
    """The strongest attributability form (the P-041 reconstruction pattern,
    four-way edition): rebuild Eno's overall on every fixture from the
    REFERENCE's component scores plus Eno's AUTHORED values alone —
    substitute the authored static polarity (15.0 -> 35.0) and the authored
    blend acceptance (65.0 -> 85.0 on the chop fixture), apply his weights,
    land on his pinned overall to the decimal. Every delta traces to an
    authored value; nothing else moved."""
    e_static = load_profile("brian_eno").doctrine["scorers"]["loop_context"]["static"]
    assert e_static == 35.0
    for name in ALL_FIXTURES:
        ref_ds = ref_analyzed[name].doctrine_score
        rebuilt = {k: ref_ds[k] for k in COMPONENT_KEYS}
        if ref_ds["loop_context_score"] == 15.0:      # the reference's static read
            rebuilt["loop_context_score"] = e_static
        if name == VOCAL_CHOP_FIXTURE:
            assert ref_ds["vocal_role_fit_score"] == 65.0
            rebuilt["vocal_role_fit_score"] = 85.0    # the authored blend gate
        assert _weighted_overall("brian_eno", rebuilt) \
            == FOUR_WAY_OVERALLS[name]["brian_eno"], name


def test_negative_space_weight_is_a_live_lever_not_a_label(e_analyzed):
    """Coherence is behavioral: his heaviest axis genuinely PRESSES the
    judgment. The weight-zero counterfactual (his own components, the
    negative_space term removed from his mean — what a reference-style 0
    weight would read): on the DENSE fixture (negative_space 15.0) the
    authored 1.4 weight is worth a traceable penalty well past 5 points —
    a dense record offends his grammar through exactly the axis his
    philosophy centers — while on the sparse piano fixture (62.3) the same
    term costs under one point. The differential IS the philosophy."""
    dense_ds = e_analyzed[DENSE].doctrine_score
    dense_components = {k: dense_ds[k] for k in COMPONENT_KEYS}
    without = {k: v for k, v in dense_components.items()
               if k != "negative_space_score"}
    dense_cost = round(_weighted_overall("brian_eno", without)
                       - dense_ds["overall_mix_readiness_score"], 1)
    assert dense_cost > 5.0

    simple_ds = e_analyzed["simple_vocal_piano_song"].doctrine_score
    simple_components = {k: simple_ds[k] for k in COMPONENT_KEYS}
    without = {k: v for k, v in simple_components.items()
               if k != "negative_space_score"}
    simple_cost = round(_weighted_overall("brian_eno", without)
                        - simple_ds["overall_mix_readiness_score"], 1)
    assert simple_cost < 1.0
    assert dense_cost > simple_cost


def test_plan_surface_speaks_his_own_authored_voice(
    ref_analyzed, tim_analyzed, q_analyzed, e_analyzed
):
    """The behavioral half of coherence: Eno's plans resolve HIS OWN authored
    search modes on both paths (the intimate fixture reaches his
    ``ambient_field``; every other fixture his ``horizontal_time`` — mode
    names no other profile carries), no fallback fires anywhere, his branch
    winners land his curated values — and his vocal_belief winner is
    ``vocal_B`` (the intimacy pass) on EVERY fixture, a winner NONE of the
    other three picks anywhere (they all ride the phrase: ``vocal_A``)."""
    for name in ALL_FIXTURES:
        cr = e_analyzed[name].creative
        assert cr["search_mode"] == ENO_SEARCH_MODES[name], name
        assert "search_mode_fallback" not in cr, name
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in cr["branches"]}
        assert winners == ENO_WINNERS[name], name
    for other in EXISTING:
        modes = load_profile(other).search_modes
        assert "ambient_field" not in modes, other
        assert "horizontal_time" not in modes, other
    for name in ALL_FIXTURES:
        others = {
            "halee_ramone": ref_analyzed, "timbaland": tim_analyzed,
            "quincy_jones": q_analyzed,
        }
        for producer, runs in others.items():
            winners = {b["problem_id"]: b["winning"]["winning_variant"]
                       for b in runs[name].creative["branches"]}
            assert winners["vocal_belief"] == "vocal_A", (producer, name)


def test_four_way_variant_values_from_four_curated_tables(
    ref_analyzed, tim_analyzed, q_analyzed, e_analyzed
):
    """On the shared loop branch each producer's own curated table scores the
    SAME variants to ITS OWN values (loop_B 85.3 / 86.7 / 85.6 / 86.9 —
    pairwise distinct), and on the dense chorus_lift branch the
    width-crowding nudge fires each profile's OWN authored evidence line at
    its own value (74.9 / 69.7 / 71.3 / 59.7 — pairwise distinct; Eno's
    59.7 is the lowest by far: the width bloom is his lowest-taste move AND
    draws his nudge)."""
    for name in LOOP_FIXTURES:
        results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed,
                               e_analyzed)
        for producer, res in results.items():
            branch = _loop_branch(res.creative)
            b = _variant_by_id(branch, "loop_B")["scores"]["overall_score"]
            a = _variant_by_id(branch, "loop_A")["scores"]["overall_score"]
            assert b == pytest.approx(LOOP_B_BY_PRODUCER[producer], abs=1e-9), \
                (name, producer)
            assert a == pytest.approx(LOOP_A_BY_PRODUCER[producer], abs=1e-9), \
                (name, producer)
    assert len(set(LOOP_B_BY_PRODUCER.values())) == 4
    assert len(set(LOOP_A_BY_PRODUCER.values())) == 3  # quincy/halee share 81.9

    results = _by_producer(DENSE, ref_analyzed, tim_analyzed, q_analyzed,
                           e_analyzed)
    values = {}
    for producer, res in results.items():
        cl = next(b for b in res.creative["branches"]
                  if b["problem_id"] == "chorus_lift")
        scores = _variant_by_id(cl, "chorus_lift_A")["scores"]
        values[producer] = scores["overall_score"]
        assert scores["score_nudges"], producer  # each profile's nudge FIRED
    assert values == {p: pytest.approx(v, abs=1e-9)
                      for p, v in NUDGED_CHORUS_A_BY_PRODUCER.items()}
    assert len(set(NUDGED_CHORUS_A_BY_PRODUCER.values())) == 4
    e_cl = next(b for b in e_analyzed[DENSE].creative["branches"]
                if b["problem_id"] == "chorus_lift")
    assert _variant_by_id(e_cl, "chorus_lift_A")["scores"]["score_nudges"] \
        == [E_WIDTH_NUDGE]


def test_iconic_loop_four_value_systems_one_detection_basis(ref_analyzed):
    """The protect gate, four-way, on the SAME iconic-reading evidence: all
    four profiles read 'iconic' from identical detection floors. halee and
    quincy (protect=false) fire their OWN promotion reasons and ship the
    deconstruct plan; timbaland AND ENO (protect=true, each authored from
    its own documented basis) withhold — but ship DIFFERENT plans in
    different voices: Eno's subtractive economy (loop_B 86.9, his highest
    curated move) outranks his unpromoted deconstruct (loop_A 78.6). Four
    plans, four voices, one basis."""
    res = _with_iconic_loop(ref_analyzed)
    profiles = {p: load_profile(p) for p in PRODUCERS}
    assert _foregrounded_loop(res) is True
    for p in PRODUCERS:
        assert _loop_status(res, profiles[p]) == "iconic", p

    assert _apply_promotions("loop_deconstruct", res, profiles["brian_eno"]) == []
    assert _apply_promotions("loop_deconstruct", res, profiles["timbaland"]) == []
    for firing in ("halee_ramone", "quincy_jones"):
        assert _apply_promotions("loop_deconstruct", res, profiles[firing]), firing

    branches = {
        p: _loop_branch(run_creative_engine(res, res.creative["search_mode"],
                                            profile=profiles[p]))
        for p in PRODUCERS
    }
    assert branches["halee_ramone"]["winning"]["winning_variant"] == "loop_A"
    assert branches["quincy_jones"]["winning"]["winning_variant"] == "loop_A"
    assert branches["timbaland"]["winning"]["winning_variant"] == "loop_B"
    assert branches["brian_eno"]["winning"]["winning_variant"] == "loop_B"

    e_a = _variant_by_id(branches["brian_eno"], "loop_A")["scores"]
    assert e_a["overall_score"] == pytest.approx(78.6, abs=1e-9)
    assert "score_nudges" not in e_a  # protection withheld the promotion
    assert _variant_by_id(branches["brian_eno"], "loop_B")["scores"]["overall_score"] \
        == pytest.approx(86.9, abs=1e-9)


def test_masked_lead_override_holds_for_all_four(ref_analyzed):
    """THE RAMONE GATE is producer-agnostic, four-way: with the lead
    bad-masked on an iconic read, the deconstruct pressure fires under ALL
    FOUR profiles — Eno's protection included; no value system can shadow a
    buried lead. Eno's fired line is his own authored voice."""
    res = _with_masked_lead(_with_iconic_loop(ref_analyzed))
    for producer in PRODUCERS:
        fired = _apply_promotions("loop_deconstruct", res, load_profile(producer))
        assert len(fired) == 1, producer
    e_fired = _apply_promotions("loop_deconstruct", res, load_profile("brian_eno"))
    assert [f[2] for f in e_fired] == [E_PROMOTION_REASON]


# =========================================================================== #
# The creative differential — every Eno mode reconstructs from his JSON; the
# shared-name modes emit four pinned, pairwise-distinct sets.
# =========================================================================== #
@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_producers_every_mode_reconstructs_from_its_json(producer, analyzed):
    """The on-disk reconstruction rule, extended to FOUR producers: for EVERY
    authored mode and EVERY problem, the emitted kind set equals (the shared
    ENGINE POOL ∪ that mode's authored reach where the extended pool holds
    variants) minus that mode's authored suppressions — derived from the
    JSON on disk, never from the code under test. The three existing
    producers re-assert byte-stable with the fourth profile live."""
    dense = analyzed[DENSE]
    prof = load_profile(producer)
    for mode_name, entry in _raw(producer)["search_modes"].items():
        for pid in PROBLEM_IDS:
            emitted = _kinds(generate_variants({"id": pid}, dense, mode_name, prof))
            assert emitted == _expected_kind_set(
                pid, entry["suppress_kinds"], entry.get("reach_kinds", ())), \
                (producer, mode_name, pid)


def test_shared_name_modes_four_pairwise_distinct_sets(analyzed):
    """THE MODE-LEVEL FOUR-WAY PIN: ``conservative`` and ``experimental``
    exist in all four profiles. Same stems, same problem, four
    pairwise-distinct chorus_lift candidate-id sets per mode — Eno's
    conservative keeps the subtractive economy AND the room (an environment
    move) while withholding the width push and the vocal ride; his
    experimental explores through absence (the dropout reach) while
    suppressing the drum-room bloom (exploration, not aggression)."""
    dense = analyzed[DENSE]
    for mode, pins in (("conservative", CONSERVATIVE_CHORUS_SETS),
                       ("experimental", EXPERIMENTAL_CHORUS_SETS)):
        sets = {}
        for producer in PRODUCERS:
            out = run_creative_engine(dense, mode, profile=load_profile(producer))
            branch = next(b for b in out["branches"]
                          if b["problem_id"] == "chorus_lift")
            sets[producer] = set(_ids(branch["variants"]))
        assert sets == pins, mode
        assert len({frozenset(s) for s in sets.values()}) == 4, mode


def test_eno_default_flow_is_neutral_zero_fork_surface(e_analyzed):
    """The evidence-key discipline under Eno: BOTH his resolution paths
    (ambient_field intimate / horizontal_time default) author neutral
    declarations and zero reach, so his default flow carries NO declaration
    surface and NO per-branch fork keys — byte-silent, like the reference's
    default flow."""
    for name, res in e_analyzed.items():
        cr = res.creative
        assert "search_mode_declarations" not in cr, name
        for b in cr["branches"]:
            assert "mode_fork" not in b, (name, b["problem_id"])


# =========================================================================== #
# Requirement 5 — CONFIDENCE HONESTY at the differential level.
# =========================================================================== #
def test_artifacts_carry_enos_own_map_fresh(e_analyzed):
    e = load_profile("brian_eno")
    for name, res in e_analyzed.items():
        conf = res.doctrine_score["confidence"]
        assert conf == E_AUTHORED_MAP, name          # the verbatim guard, live
        assert conf is not e.confidence_map, name    # fresh, never an alias
    for p in EXISTING:
        assert E_AUTHORED_MAP != load_profile(p).confidence_map, p


def test_no_high_entry_lacks_a_documented_technique_reason(e_analyzed):
    """The user's grounding standard, re-asserted on the LIVE artifact
    surface: every ``high`` entry the pipeline ships names its
    documented-technique basis; everything else is limited/deferred
    (LLM-synthesized-as-high is forbidden by construction)."""
    for name, res in e_analyzed.items():
        for entry in res.doctrine_score["confidence"]:
            if entry["level"] == "high":
                assert DOCUMENTED_STAMP in entry["reason"], (name, entry["area"])
            assert entry["level"] in ("high", "limited", "deferred")


def test_rendered_verdicts_speak_each_producers_voice_no_leaks(
    ref_analyzed, tim_analyzed, q_analyzed, e_analyzed, tmp_path
):
    """Render one fixture under all FOUR producers: each verdict carries its
    OWN map (every area and reason) and its own distinct voice — and no
    other producer's distinct voice leaks in (the shared deferred engine
    boundaries legitimately render under all four). The FOUR-WAY voice
    vocabulary is local by necessity: timbaland's three-way leak set
    included ``protect_iconic_loops: true``, which is no longer
    timbaland-distinct — Eno AUTHORS the same protection from his own
    documented basis (both loop entries state it), so the four-way
    distinct-voice set keeps only the documented-technique stamp."""
    name = "simple_vocal_piano_song"
    assert "protect_iconic_loops: true" in TIMBALAND_ONLY_STRINGS  # the 3-way set
    voices = {
        "halee_ramone": REFERENCE_ONLY_STRINGS,
        "timbaland": ("documented Timbaland technique",),
        "quincy_jones": QUINCY_ONLY_STRINGS,
        "brian_eno": ENO_ONLY_STRINGS,
    }
    results = _by_producer(name, ref_analyzed, tim_analyzed, q_analyzed,
                           e_analyzed)
    verdicts = {}
    for producer, res in results.items():
        d = tmp_path / producer
        write_artifacts(res, d)
        verdicts[producer] = (d / "mix_verdict.md").read_text(encoding="utf-8")
        dsj = json.loads((d / "doctrine_score.json").read_text(encoding="utf-8"))
        assert dsj["confidence"] == load_profile(producer).confidence_map, producer

    for producer, md in verdicts.items():
        assert "## Confidence" in md
        for entry in load_profile(producer).confidence_map:
            assert entry["area"] in md, (producer, entry["area"])
            assert entry["reason"] in md, (producer, entry["area"])
        for own in voices[producer]:
            assert own in md, (producer, own)
        for other, other_strings in voices.items():
            if other == producer:
                continue
            for s in other_strings:
                assert s not in md, f"{other} voice leaked into {producer}: {s}"


# =========================================================================== #
# Requirement 6 — EXISTING PROFILES DO NOT DRIFT (with the fourth live).
# =========================================================================== #
def test_existing_producer_jsons_are_blob_unchanged():
    """Byte-level requirement 6: the three shipped JSONs hash to their
    packet-base sha256 values — no tuning of Halee/Ramone, Timbaland or
    Quincy rode in with the fourth producer."""
    producers_dir = ROOT / "logic_mix_os" / "doctrine" / "producers"
    for name, expected in EXISTING_JSON_SHA256.items():
        digest = hashlib.sha256((producers_dir / f"{name}.json").read_bytes())
        assert digest.hexdigest() == expected, name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_existing_producers_unmoved_at_their_pinned_values(
    name, ref_analyzed, tim_analyzed, q_analyzed
):
    """The standing three-producer pins hold byte-stable with brian_eno in
    the directory: every overall, the authored loop polarities (15/10/12 on
    the static-loop fixtures) and the blend split (65/85/85 on the chop
    fixture) — and the four-way table's existing columns ARE the standing
    P-041 table."""
    for producer, runs in (("halee_ramone", ref_analyzed),
                           ("timbaland", tim_analyzed),
                           ("quincy_jones", q_analyzed)):
        ds = runs[name].doctrine_score
        assert ds["overall_mix_readiness_score"] \
            == THREE_WAY_OVERALLS[name][producer], producer
        assert FOUR_WAY_OVERALLS[name][producer] \
            == THREE_WAY_OVERALLS[name][producer], producer
    if name in STATIC_FIXTURES:
        assert ref_analyzed[name].doctrine_score["loop_context_score"] == 15.0
        assert tim_analyzed[name].doctrine_score["loop_context_score"] == 10.0
        assert q_analyzed[name].doctrine_score["loop_context_score"] == 12.0
    if name == VOCAL_CHOP_FIXTURE:
        assert ref_analyzed[name].doctrine_score["vocal_role_fit_score"] == 65.0
        assert tim_analyzed[name].doctrine_score["vocal_role_fit_score"] == 85.0
        assert q_analyzed[name].doctrine_score["vocal_role_fit_score"] == 85.0


def test_committed_sample_tree_headlines_unmoved():
    """Two of the FOUR committed demo trees re-read directly: the reference
    and timbaland headline overalls stand (the byte-level staleness pin
    covering all four committed trees lives in tests/test_sample_refresh.py
    and runs against the same committed bytes)."""
    for tree, headline in COMMITTED_TREE_HEADLINES.items():
        ds = json.loads((ROOT / "examples" / tree / "doctrine_score.json")
                        .read_text(encoding="utf-8"))
        assert ds["overall_mix_readiness_score"] == headline, tree


# =========================================================================== #
# Requirement 7 — SAFETY INVARIANT: the same veto/audit surface, four-way.
# =========================================================================== #
def test_kill_switches_lead_with_the_five_safety_switches(e_analyzed):
    """On every fixture the composed kill-switch list under Eno leads with
    the 5 hardcoded SAFETY switches FIRST, VERBATIM, IN ORDER (pinned in
    test_differential_proof, not read from governance) — followed by exactly
    his authored aesthetic list."""
    assert governance._SAFETY_KILL_SWITCHES == SAFETY_KILL_SWITCHES
    aesthetic = load_profile("brian_eno").aesthetic_kill_switches
    for name, res in e_analyzed.items():
        ks = res.governance["kill_switches"]
        assert ks[:5] == SAFETY_KILL_SWITCHES, name
        assert ks == SAFETY_KILL_SWITCHES + aesthetic, name


def test_veto_thresholds_identical_across_all_four_profiles():
    """The veto surface is UNCHANGED, not merely not-weaker: all four
    profiles author identical reject/veto/fallback lines."""
    e = load_profile("brian_eno").veto_thresholds
    for p in EXISTING:
        assert e == load_profile(p).veto_thresholds, p


def test_no_destructive_recommendation_under_eno(e_analyzed):
    """Class 5 appears NOWHERE in Eno's plans; every action passes the
    kill-switch validator; every creative variant is reversible; the class-5
    block itself stays engine-fixed."""
    for name, res in e_analyzed.items():
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


def test_eno_plans_and_artifacts_validate(e_analyzed, tmp_path):
    """Machine-checkable coherence: Eno's mix_plan validates against the
    schema on every fixture, and his rendered artifact tree passes the full
    output validation."""
    schema = load_schema("mix_plan.schema.json")
    for name, res in e_analyzed.items():
        assert validate_instance(res.mix_plan, schema) == [], name
    out = tmp_path / "brian_eno"
    write_artifacts(e_analyzed[VOCAL_CHOP_FIXTURE], out)
    report = validate_output(out)
    assert report["ok"], report["errors"]


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_the_reference(name, ref_analyzed, e_analyzed):
    """The P-041 reviewer pattern: key-by-key doctrine audit against
    halee_ramone — Eno diverges on EXACTLY the explained authored-taste set
    and nothing else (shared substrate; the chop fixture's evidence
    divergence stays isolated to the vocal_role_fit axis, itself the
    authored blend gate)."""
    ref_ds = ref_analyzed[name].doctrine_score
    e_ds = e_analyzed[name].doctrine_score
    assert set(ref_ds) == set(e_ds)
    diverged = {k for k in ref_ds if ref_ds[k] != e_ds[k]}
    assert diverged == DIVERGENT_VS_REFERENCE[name], (name, diverged)
    if "evidence" in diverged:
        ev_diverged = {k for k in ref_ds["evidence"]
                       if ref_ds["evidence"][k] != e_ds["evidence"][k]}
        assert ev_diverged == {"vocal_role_fit"}, (name, ev_diverged)
    assert ref_ds["warnings"] == e_ds["warnings"], name


@pytest.mark.parametrize("name", ALL_FIXTURES)
def test_divergence_audit_vs_timbaland_and_quincy(
    name, tim_analyzed, q_analyzed, e_analyzed
):
    """The same audit against the other two poles: all three opt into the
    blend, so on the chop fixture the readings AGREE (identical
    vocal_role_fit score and evidence — Eno's stricter 0.85 floor is still
    cleared at 0.95) and the only component divergence anywhere is the
    authored loop polarity (35.0 vs 10.0 / 12.0)."""
    e_ds = e_analyzed[name].doctrine_score
    for runs in (tim_analyzed, q_analyzed):
        other_ds = runs[name].doctrine_score
        assert set(other_ds) == set(e_ds)
        diverged = {k for k in other_ds if other_ds[k] != e_ds[k]}
        assert diverged == DIVERGENT_VS_OPT_IN_PRODUCERS[name], (name, diverged)
        assert other_ds["evidence"] == e_ds["evidence"], name


# =========================================================================== #
# Requirement 8 — DROPOUT STAYS GOVERNED under Eno's authored reach.
# =========================================================================== #
@pytest.mark.parametrize("name", ALL_FIXTURES)
@pytest.mark.parametrize("mode", E_REACHING_MODES)
def test_protection_filter_holds_on_enos_reaching_modes(name, mode, e_analyzed):
    """His reaching modes x all four fixtures: every dropout variant's
    resolved targets are the pinned REAL-record subset, never empty, never
    intersecting the ENGINE-owned protected set (the lead vocal, the
    kick/snare + bass foundation, sacred elements) — and the whole emission
    per fixture IS the pinned table (the simple fixture emits ZERO dropout:
    its only firing problem holds no dropout variant)."""
    res = e_analyzed[name]
    protected = _dropout_protected_names(res)
    real_names = {r["name"] for r in res.records}
    out = run_creative_engine(res, mode, profile=load_profile("brian_eno"))
    emitted = {}
    for b in out["branches"]:
        for v in b["variants"]:
            if v["kind"] != DROPOUT:
                continue
            emitted[v["variant_id"]] = v["tracks_affected"]
            assert v["tracks_affected"], (name, mode, v["variant_id"])
            assert set(v["tracks_affected"]) <= real_names, (name, mode)
            assert set(v["tracks_affected"]) & protected == set(), \
                (name, mode, v["variant_id"])
            assert v["reversibility"] == "non_destructive_duplicate_track"
    assert emitted == ENO_DROPOUT_EMISSION[name], (name, mode)


@pytest.mark.parametrize("mode", E_REACHING_MODES)
def test_dropout_plan_prose_is_the_engine_owned_p044_text(mode, e_analyzed):
    """Plan-only prose unchanged: the dropout variants Eno's reach admits
    carry the PINNED P-044 changes text byte-for-byte — the prose is
    engine-owned; a profile authors reach, never wording."""
    res = e_analyzed[DENSE]
    out = run_creative_engine(res, mode, profile=load_profile("brian_eno"))
    by_id = {v["variant_id"]: v for b in out["branches"] for v in b["variants"]}
    assert by_id["chorus_lift_F"]["changes"] == CHORUS_F_CHANGES
    assert by_id["density_E"]["changes"] == DENSITY_E_CHANGES


def test_dropout_scores_at_his_honest_row_through_the_real_chain(e_analyzed):
    """The admitted variants score from HIS authored row with no missing-row
    fallback: the overall reconstructs from the JSON on disk (mean of his 7
    authored dims minus his medium translation penalty = 78.9) — and his
    subtractive economy (86.9) still outranks the dropout by his own curated
    margin, so every branch winner stays a non-dropout move (the reach
    widens the candidate set, never his verdicts)."""
    raw = _raw("brian_eno")
    row = raw["kind_scores"][DROPOUT]
    dims = ("technical", "physical_space", "emotional_hierarchy",
            "contrast", "vocal_belief", "excitement", "taste")
    expected = round(sum(row[d] for d in dims) / 7
                     - raw["risk_penalty"][row["translation"]], 1)
    assert expected == ENO_DROPOUT_OVERALL
    res = e_analyzed[DENSE]
    out = run_creative_engine(res, "generative_drift",
                              profile=load_profile("brian_eno"))
    for b in out["branches"]:
        for v in b["variants"]:
            if v["kind"] == DROPOUT:
                assert v["scores"]["overall_score"] == ENO_DROPOUT_OVERALL
                assert v["scores"]["translation_risk"] == "medium"
        assert b["winning"]["winning_variant"] \
            not in ("chorus_lift_F", "density_E"), b["problem_id"]


def test_reach_report_is_honest_on_his_reaching_modes(e_analyzed):
    """The fork report under his REAL authored reach: the declarations echo
    carries his authored table verbatim, ``reached`` names the dropout kind
    exactly where the curated pool holds a variant, and ``reach_capped``
    stays empty (his medium row lives inside both postures)."""
    res = e_analyzed[DENSE]
    for mode in E_REACHING_MODES:
        out = run_creative_engine(res, mode, profile=load_profile("brian_eno"))
        authored = E_MODE_TABLE[mode]
        assert out["search_mode_declarations"] == {
            "allowed_risk": authored["allowed_risk"],
            "favor_kinds": authored["favor_kinds"],
            "suppress_kinds": authored["suppress_kinds"],
            "reach_kinds": [DROPOUT],
        }, mode
        for b in out["branches"]:
            expected = [DROPOUT] if b["problem_id"] in ("chorus_lift", "density") \
                else []
            assert b["mode_fork"]["reached"] == expected, (mode, b["problem_id"])
            assert b["mode_fork"]["reach_capped"] == [], (mode, b["problem_id"])


def test_non_reaching_modes_emit_zero_dropout_full_parametrization(e_analyzed):
    """The other half of requirement 8: over Eno's FULL mode table, every
    mode WITHOUT authored dropout reach — plus no-mode and an unknown mode —
    emits zero dropout ids on every problem of every fixture."""
    prof = load_profile("brian_eno")
    non_reaching = [m for m, entry in E_MODE_TABLE.items()
                    if not entry["reach_kinds"]]
    assert sorted(non_reaching) == sorted(
        set(E_MODE_TABLE) - set(E_REACHING_MODES))
    for name, res in e_analyzed.items():
        for mode in non_reaching + [None, "no_such_mode"]:
            for pid in PROBLEM_IDS:
                emitted = generate_variants({"id": pid}, res, mode, prof)
                assert DROPOUT not in _kinds(emitted), (name, mode, pid)
                assert not {"chorus_lift_F", "density_E"} & set(_ids(emitted)), \
                    (name, mode, pid)


def test_dropout_cap_binds_at_runtime_against_his_row_fail_closed(analyzed):
    """The cap binds against HIS honest medium row at runtime (the P-044
    fail-closed pattern, on his judgment): a loader-bypassing mode reaching
    the dropout family under a LOW posture is REFUSED — emission
    byte-identical to neutral, the refusal surfaced in ``reach_capped``,
    nothing reads as reached; the medium-posture control admits it, so the
    refusal is the CAP. (The load-time half is pinned in
    test_eno_profile.py.)"""
    dense = analyzed[DENSE]
    capped = _with_mode("brian_eno", _mode(reach=[DROPOUT], allowed="low"))
    for pid in PROBLEM_IDS:
        assert generate_variants({"id": pid}, dense, "reach", capped) \
            == generate_variants({"id": pid}, dense), pid
    _, fork = _fork(capped, "reach", "chorus_lift", dense)
    assert fork["reach_capped"] == [DROPOUT]
    assert fork["reached"] == []

    control = _with_mode("brian_eno", _mode(reach=[DROPOUT], allowed="medium"))
    emitted = generate_variants({"id": "chorus_lift"}, dense, "reach", control)
    assert _ids(emitted) == [vid for vid, _ in ENGINE_POOL["chorus_lift"]] \
        + ["chorus_lift_F"]


def test_only_protected_targets_emit_nothing_under_his_real_reach(analyzed):
    """THE NO-FALLBACK RULE under Eno's REAL reaching modes: a project whose
    entire dropout candidate surface is protected (a hook-candidate chop bed
    + the groove foundation) emits ZERO dropout variants on both of his
    authored reaching modes — no phantom targets, no degrade toward
    protected elements."""
    dense = analyzed[DENSE]
    records = [
        _lead(),
        _rec("Hook Chop", "backing_vocal", "vocal",
             source_kind="one_shot_sample", sacredness="decorative",
             depth="foreground", perceptual="heard",
             vocal_type="vocal_hook_candidate"),
        _rec("Kick", "kick", "drums", sacredness="important",
             depth="foreground", perceptual="structural"),
        _rec("Bass", "bass_guitar", "bass", sacredness="important",
             depth="foreground", perceptual="structural"),
    ]
    synth = _with_records(dense, records)
    assert _dropout_protected_names(synth) \
        == {"Lead Vocal", "Hook Chop", "Kick", "Bass"}
    prof = load_profile("brian_eno")
    for mode in E_REACHING_MODES:
        out = run_creative_engine(synth, mode, profile=prof)
        for b in out["branches"]:
            assert DROPOUT not in _kinds(b["variants"]), (mode, b["problem_id"])


def test_masked_lead_protection_holds_under_his_real_reach(analyzed):
    """The masked-lead synthetic under Eno: while the lead is bad-masked,
    EVERY vocal is excluded and his reaching modes emit no dropout; the same
    project without the masking event emits against exactly the unprotected
    vocal stack — the deciding variable is the ENGINE's protection signal,
    never his taste."""
    dense = analyzed[DENSE]
    records = [
        _lead(),
        _rec("BV Stack", "backing_vocal", "vocal",
             source_kind="comped_audio_track", sacredness="decorative",
             depth="background", perceptual="felt", vocal_type="vocal_stack"),
    ]
    event = {"classification": "bad_masking", "elements": ["Lead Vocal", "Piano"]}
    prof = load_profile("brian_eno")

    masked = _with_records(dense, records, [event])
    assert _dropout_protected_names(masked) == {"Lead Vocal", "BV Stack"}
    for mode in E_REACHING_MODES:
        out = run_creative_engine(masked, mode, profile=prof)
        for b in out["branches"]:
            assert DROPOUT not in _kinds(b["variants"]), (mode, b["problem_id"])

    clear = _with_records(dense, records)
    assert _dropout_protected_names(clear) == {"Lead Vocal"}
    for mode in E_REACHING_MODES:
        out = run_creative_engine(clear, mode, profile=prof)
        hits = [v["tracks_affected"] for b in out["branches"]
                for v in b["variants"] if v["kind"] == DROPOUT]
        assert hits and all(t == ["BV Stack"] for t in hits), mode


def test_default_mode_resolution_never_reaches_dropout(e_analyzed):
    """The reach never rides the default path: both entries of Eno's
    ``default_creative_mode`` table resolve to zero-reach modes, and the
    live default runs on every fixture carry zero dropout ids (the emission
    surface is byte-silent — pinned above)."""
    prof = load_profile("brian_eno")
    dcm = prof.default_creative_mode
    for key in ("intimate_mode", "default_mode"):
        assert prof.search_modes[dcm[key]]["reach_kinds"] == [], key
    for name, res in e_analyzed.items():
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        assert mode == ENO_SEARCH_MODES[name], name
        for b in res.creative["branches"]:
            assert DROPOUT not in _kinds(b["variants"]), (name, b["problem_id"])
