"""P-032i — THE DIFFERENTIAL PROOF: Timbaland vs Halee/Ramone, same stems —
the producer-agnostic epic's formal close.

P-032h proved the score-level differential (same stems, two judgments, fully
attributable). This suite goes BEYOND the scores to the PLAN and ARTIFACT
surfaces and formalizes the sub-arc's five proof obligations in one permanent
place:

(a) **Recognizably-different-but-COHERENT judgment AND plan surfaces** — the
    verdict markdown differs meaningfully (each producer's own overall +
    diagnosis + confidence voice); the plan surfaces differ exactly where the
    value systems diverge (search mode on the intimate fixture, the loop
    branch's variant scores, each profile's own authored evidence lines, the
    winning-plan reversal on an iconic-reading loop) — and EVERY plan under
    EITHER profile is internally coherent: real tracks, tagged risk classes,
    schema-valid, no class-5 recommendation anywhere.
(b) **Full attributability — the anti-drift guard**: the ENTIRE doctrine
    surface is audited key by key; the two producers diverge on EXACTLY the
    explained set (overall / the authored loop_context polarity on the loop
    fixtures / the profile's own confidence map); each overall recomputes as
    its own profile's weighted mean; timbaland's judgment RECONSTRUCTS from
    the reference's measurements plus timbaland's authored values alone.
    If a future profile/engine change makes the surfaces diverge for a NEW
    reason, these tests flag it for conscious review.
(c) **Safety invariance** — the 5 hardcoded SAFETY kill-switches lead both
    producers' composed lists verbatim, in order; risk-class tagging is
    present and within bounds on every recommendation in both plans; no
    destructive pattern anywhere; the masked-lead override reaches the plan
    surface under BOTH profiles.
(d) **The pre-registered expectations:** NO vocal-blend delta (the
    inert-blend corollary, still binding and pinned); and the intimate-mode
    pin, FLIPPED by P-033 exactly as pre-registered — the pipeline now reads
    the profile's own ``default_creative_mode`` table, so timbaland's
    authored ``intimate_mode`` ("conservative") is reachable end to end.
(e) **Per-profile confidence rendering at the differential level** — each
    producer's artifacts carry ITS OWN map (8 entries vs 11), the maps differ
    where authored, and neither voice leaks into the other's artifacts.

Plus the packet's comparison surface: ``differential_snapshot`` — a compact,
deterministic side-by-side dict per fixture (overall / lowest-3 components /
winning variants / search mode), pinned verbatim and printable for the
receipt. Test-local by design: adding a product-code utility was not needed,
so the reference path moves ZERO bytes in this packet.
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os import governance, pipeline
from logic_mix_os.constants import RISK_CLASSES
from logic_mix_os.creative import run_creative_engine
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest
from logic_mix_os.validation.output_validator import (
    load_schema,
    validate_instance,
    validate_output,
)

from conftest import FIXTURE_NAMES, ROOT
from test_protect_iconic_loops import (
    PROMOTION_REASON,
    _loop_branch,
    _variant_by_id,
    _with_iconic_loop,
    _with_masked_lead,
)
from test_timbaland_profile import REFERENCE_ONLY_STRINGS, TIM_PROMOTION_REASON

PRODUCERS = ("halee_ramone", "timbaland")
LOOP_FIXTURES = ("dense_chorus_with_loops", "splice_loop_problem")

# The 14 component axes (shared measurement substrate; each profile weights
# them its own way).
COMPONENT_KEYS = [
    "halee_score", "ramone_score", "vocal_centrality_score",
    "depth_hierarchy_score", "section_contrast_score", "static_mix_score",
    "dynamic_mix_score", "beat_identity_score", "negative_space_score",
    "groove_coherence_score", "rhythmic_surprise_score",
    "low_end_motion_score", "loop_context_score", "vocal_role_fit_score",
]

# Same stems, two judgments — the epic's payoff, pinned (P-032h verified these
# to the decimal by hand-recomputing the weighted means).
OVERALLS = {
    "simple_vocal_piano_song": {"halee_ramone": 73.8, "timbaland": 68.4},
    "dense_chorus_with_loops": {"halee_ramone": 70.7, "timbaland": 52.6},
    "splice_loop_problem": {"halee_ramone": 74.3, "timbaland": 49.7},
}

# THE ANTI-DRIFT GUARD's expected set: every doctrine_score key on which the
# two producers may diverge, per fixture, each divergence EXPLAINED:
#   - overall_mix_readiness_score — each profile's own weighted mean;
#   - confidence                  — each profile's own authored honesty map;
#   - loop_context_score          — ONLY on the loop fixtures: the authored
#     status->score polarity (both profiles read STATIC from the same stems;
#     the reference maps static to 15.0, timbaland authors 10.0).
# Every OTHER key (all remaining components, warnings, evidence) must be
# IDENTICAL: the axes are shared measurable substrate. A future change that
# widens this set has introduced a NEW divergence channel — this guard exists
# so that happens as a conscious, test-visible decision, never as drift.
DIVERGENT_DOCTRINE_KEYS = {
    "simple_vocal_piano_song": {"overall_mix_readiness_score", "confidence"},
    "dense_chorus_with_loops": {
        "overall_mix_readiness_score", "confidence", "loop_context_score",
    },
    "splice_loop_problem": {
        "overall_mix_readiness_score", "confidence", "loop_context_score",
    },
}

# The 5 producer-AGNOSTIC safety switches, pinned VERBATIM in this suite (not
# read from governance.py) so a weakening edit there cannot hide from here.
SAFETY_KILL_SWITCHES = [
    "Never overwrite original audio.",
    "Never destructively tune or time-stretch source recordings.",
    "Never delete tracks without backup.",
    "Never flatten comped vocals without a duplicate.",
    "Never apply creative source edits without a versioned duplicate.",
]

# Timbaland-DISTINCT confidence strings that must never appear in a reference
# artifact (the mirror of test_timbaland_profile.REFERENCE_ONLY_STRINGS; the
# 5 deferred engine-boundary entries are verbatim-shared and legitimately
# render under both).
TIMBALAND_ONLY_STRINGS = (
    "documented Timbaland technique",
    "protect_iconic_loops: true",
)

# --------------------------------------------------------------------------- #
# The packet's comparison surface: one fixture -> a compact side-by-side dict.
# --------------------------------------------------------------------------- #
def differential_snapshot(ref_result, tim_result) -> dict:
    """Deterministic side-by-side view of one fixture under both producers:
    ``{producer: {overall, lowest-3 components, winning variant per branch,
    search mode}}``. Test-local (no product code touched); the pin below
    guards it and the receipt can print it verbatim."""
    out = {}
    for producer, res in (("halee_ramone", ref_result), ("timbaland", tim_result)):
        ds = res.doctrine_score
        lowest = sorted(
            (k for k in COMPONENT_KEYS if ds.get(k) is not None),
            key=lambda k: (ds[k], k),
        )[:3]
        out[producer] = {
            "overall": ds["overall_mix_readiness_score"],
            "lowest_components": [(k, ds[k]) for k in lowest],
            "winning_variants": {
                b["problem_id"]: b["winning"]["winning_variant"]
                for b in res.creative["branches"]
            },
            "search_mode": res.creative["search_mode"],
        }
    return out


# The full snapshot, pinned verbatim: same stems, two producers, side by side.
# The winning variant IDS coincide at the plain-fixture surface (the reversal
# needs an iconic-reading loop — proven in its own test below); the VALUES
# around them — overall, the lowest components, the search mode on the
# intimate fixture — carry the authored divergence.
EXPECTED_SNAPSHOT = {
    "simple_vocal_piano_song": {
        "halee_ramone": {
            "overall": 73.8,
            "lowest_components": [
                ("depth_hierarchy_score", 40.0),
                ("groove_coherence_score", 45.0),
                ("loop_context_score", 50.0),
            ],
            "winning_variants": {"vocal_belief": "vocal_A"},
            "search_mode": "ramone_vocal_truth",
        },
        "timbaland": {
            "overall": 68.4,
            "lowest_components": [
                ("depth_hierarchy_score", 40.0),
                ("groove_coherence_score", 45.0),
                ("loop_context_score", 50.0),
            ],
            "winning_variants": {"vocal_belief": "vocal_A"},
            "search_mode": "conservative",
        },
    },
    "dense_chorus_with_loops": {
        "halee_ramone": {
            "overall": 70.7,
            "lowest_components": [
                ("loop_context_score", 15.0),
                ("negative_space_score", 15.0),
                ("rhythmic_surprise_score", 20.0),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "density": "density_B",
                "loop": "loop_B", "depth": "depth_A", "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
        "timbaland": {
            "overall": 52.6,
            "lowest_components": [
                ("loop_context_score", 10.0),
                ("negative_space_score", 15.0),
                ("rhythmic_surprise_score", 20.0),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "density": "density_B",
                "loop": "loop_B", "depth": "depth_A", "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
    },
    "splice_loop_problem": {
        "halee_ramone": {
            "overall": 74.3,
            "lowest_components": [
                ("loop_context_score", 15.0),
                ("negative_space_score", 20.0),
                ("dynamic_mix_score", 23.1),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "loop": "loop_B",
                "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
        "timbaland": {
            "overall": 49.7,
            "lowest_components": [
                ("loop_context_score", 10.0),
                ("negative_space_score", 20.0),
                ("dynamic_mix_score", 23.1),
            ],
            "winning_variants": {
                "chorus_lift": "chorus_lift_B", "loop": "loop_B",
                "vocal_belief": "vocal_A",
            },
            "search_mode": "dramatic_contrast",
        },
    },
}


# --------------------------------------------------------------------------- #
# Shared expensive fixtures: 3 timbaland analyses (module-scoped; the
# reference runs come from the session-scoped ``analyzed``) and the 6 rendered
# artifact trees (once per producer per fixture).
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def tim_analyzed():
    """The full pipeline once per fixture with ``producer="timbaland"``."""
    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(
            str(ROOT / "fixtures" / name / "stems"), manifest, producer="timbaland"
        )
    return results


@pytest.fixture(scope="module")
def rendered(analyzed, tim_analyzed, tmp_path_factory):
    """``write_artifacts`` once per (producer, fixture): the artifact trees the
    rendering-level obligations read."""
    out = {}
    for producer, results in (("halee_ramone", analyzed), ("timbaland", tim_analyzed)):
        for name in FIXTURE_NAMES:
            d = tmp_path_factory.mktemp(f"p032i_{producer}_{name}")
            write_artifacts(results[name], d)
            out[(producer, name)] = d
    return out


def _verdict(rendered, producer, name) -> str:
    return (rendered[(producer, name)] / "halee_ramone_mix_verdict.md").read_text(
        encoding="utf-8"
    )


def _track_names(res) -> set:
    return {rec["name"] for rec in res.records}


# =========================================================================== #
# (a) RECOGNIZABLY-DIFFERENT-BUT-COHERENT — judgment AND plan surfaces.
# =========================================================================== #
@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_verdict_markdown_differs_meaningfully(name, rendered):
    """The two verdicts on the same stems are recognizably different
    documents: each carries ITS OWN overall + diagnosis + confidence voice —
    while the shared measurement rows stay identical (one substrate, two
    judgments). The rendered verdict filename/title is producer-independent
    today (``halee_ramone_mix_verdict.md`` — the renderer's fixed name), so
    the difference is IN the document, where the judgment lives."""
    ref_md = _verdict(rendered, "halee_ramone", name)
    tim_md = _verdict(rendered, "timbaland", name)
    assert ref_md != tim_md

    ref_overall = OVERALLS[name]["halee_ramone"]
    tim_overall = OVERALLS[name]["timbaland"]
    assert f"Overall mix readiness {ref_overall}/100." in ref_md
    assert f"Overall mix readiness {tim_overall}/100." in tim_md
    assert f"Overall mix readiness {tim_overall}/100." not in ref_md
    assert f"Overall mix readiness {ref_overall}/100." not in tim_md

    # The shared-measurement row renders identically under both: ramone_score
    # is 86.0 on every fixture and is a COMPONENT (measurement), not judgment.
    shared_row = "| Phil Ramone (vocal centrality) | 86.0/100 |"
    assert shared_row in ref_md and shared_row in tim_md

    # Each verdict speaks its own confidence voice (the full per-entry check
    # is the rendering obligation (e) below).
    assert "documented Timbaland technique" in tim_md
    assert "documented Timbaland technique" not in ref_md
    assert "documented Halee/Ramone technique" in ref_md
    assert "documented Halee/Ramone technique" not in tim_md

    # The dashboard header carries its own overall too.
    for producer, overall in (("halee_ramone", ref_overall), ("timbaland", tim_overall)):
        html = (rendered[(producer, name)] / "dashboard.html").read_text(encoding="utf-8")
        assert f'class="big">{overall}<' in html


def test_plan_surfaces_differ_where_the_value_systems_diverge(analyzed, tim_analyzed):
    """The SPECIFIC known plan-surface differences, pinned:

    * intimate fixture — different SEARCH MODES, each profile's OWN authored
      ``intimate_mode`` (ramone_vocal_truth vs conservative — P-033 wired the
      ``default_creative_mode`` table per call; obligation (d)'s pin below
      carries the reachability proof);
    * loop fixtures — the loop branch scores from each profile's own curated
      tables (loop_B 85.3 vs 86.7; loop_A 81.9 vs 80.7);
    * dense chorus_lift_A (width_bloom, width-crowded evidence) — each profile
      emits ITS OWN authored evidence line at its own value (74.9 vs 69.7);
    * dense chorus_lift_D (drum_room_bloom) — the one move timbaland's tables
      score UP vs the reference (82.1 > 81.4): the physical drum-room lift
      matters more to a groove-first value system."""
    assert analyzed["simple_vocal_piano_song"].creative["search_mode"] == "ramone_vocal_truth"
    assert tim_analyzed["simple_vocal_piano_song"].creative["search_mode"] == "conservative"

    for name in LOOP_FIXTURES:
        ref_loop = _loop_branch(analyzed[name].creative)
        tim_loop = _loop_branch(tim_analyzed[name].creative)
        assert _variant_by_id(ref_loop, "loop_A")["scores"]["overall_score"] == pytest.approx(81.9)
        assert _variant_by_id(ref_loop, "loop_B")["scores"]["overall_score"] == pytest.approx(85.3)
        assert _variant_by_id(tim_loop, "loop_A")["scores"]["overall_score"] == pytest.approx(80.7)
        assert _variant_by_id(tim_loop, "loop_B")["scores"]["overall_score"] == pytest.approx(86.7)

    ref_cl = next(b for b in analyzed["dense_chorus_with_loops"].creative["branches"]
                  if b["problem_id"] == "chorus_lift")
    tim_cl = next(b for b in tim_analyzed["dense_chorus_with_loops"].creative["branches"]
                  if b["problem_id"] == "chorus_lift")
    ref_a = _variant_by_id(ref_cl, "chorus_lift_A")["scores"]
    tim_a = _variant_by_id(tim_cl, "chorus_lift_A")["scores"]
    assert ref_a["overall_score"] == pytest.approx(74.9)
    assert tim_a["overall_score"] == pytest.approx(69.7)
    assert ref_a["score_nudges"] == [
        "vocal_belief -6: stereo image is already width-crowded"
    ]
    assert tim_a["score_nudges"] == [
        "vocal_belief -6: stereo image is already width-crowded — added width "
        "trades focus for size"
    ]
    assert _variant_by_id(ref_cl, "chorus_lift_D")["scores"]["overall_score"] == pytest.approx(81.4)
    assert _variant_by_id(tim_cl, "chorus_lift_D")["scores"]["overall_score"] == pytest.approx(82.1)


def test_mix_plan_divergence_is_the_judgment_not_the_measurement(analyzed, tim_analyzed):
    """Anti-drift at the mix_plan surface: on every fixture the two producers'
    mix_plans differ on EXACTLY {overall_diagnosis, overall_mix_readiness_score}
    — each diagnosis opens with its own overall — and NOTHING else. Notably
    ``next_pass`` is identical: today's next-pass planner reads records /
    masking / sections (shared measurement), so the differential honestly does
    not reach it; a future planner that reads profile weights would widen this
    set as a conscious decision."""
    for name in FIXTURE_NAMES:
        ref_mp = analyzed[name].mix_plan
        tim_mp = tim_analyzed[name].mix_plan
        assert set(ref_mp) == set(tim_mp)
        diverged = {k for k in ref_mp if ref_mp[k] != tim_mp[k]}
        assert diverged == {"overall_diagnosis", "overall_mix_readiness_score"}, (
            name, diverged
        )
        assert ref_mp["overall_diagnosis"].startswith(
            f"Overall mix readiness {OVERALLS[name]['halee_ramone']}/100."
        )
        assert tim_mp["overall_diagnosis"].startswith(
            f"Overall mix readiness {OVERALLS[name]['timbaland']}/100."
        )
        assert ref_mp["next_pass"] == tim_mp["next_pass"]


def test_iconic_loop_scenario_yields_two_different_coherent_plans(analyzed):
    """THE PLAN-LEVEL REVERSAL (beyond P-032h's promotion-level proof): on the
    same iconic-reading evidence the two profiles ship two DIFFERENT winning
    PLANS for the loop — the reference's promoted Loop Deconstruct (loop_A,
    85.9: chop / high-pass / narrow / push back) vs timbaland's curated Loop
    as Accent (loop_B, 86.7: one-shot accents at transitions; the deconstruct
    promotion withheld, loop_A at its unpromoted 80.7). Each plan's keep/
    reject moves are the exact mirror of the other's, each references the real
    loop track, and each is non-destructive — two value systems, one shared
    detection basis, both coherent."""
    res = _with_iconic_loop(analyzed)
    plans = {}
    for producer in PRODUCERS:
        out = run_creative_engine(
            res, res.creative["search_mode"], profile=load_profile(producer)
        )
        plans[producer] = _loop_branch(out)

    ref_branch, tim_branch = plans["halee_ramone"], plans["timbaland"]
    assert ref_branch["winning"]["winning_variant"] == "loop_A"
    assert tim_branch["winning"]["winning_variant"] == "loop_B"
    assert _variant_by_id(ref_branch, "loop_A")["scores"]["overall_score"] == pytest.approx(85.9)
    assert _variant_by_id(tim_branch, "loop_A")["scores"]["overall_score"] == pytest.approx(80.7)
    assert _variant_by_id(tim_branch, "loop_B")["scores"]["overall_score"] == pytest.approx(86.7)

    # The two plans are mirror images: what one keeps, the other rejects.
    assert ref_branch["winning"]["keep_moves"] == tim_branch["winning"]["reject_moves"]
    assert ref_branch["winning"]["reject_moves"] == tim_branch["winning"]["keep_moves"]
    assert "Chop Splice Texture Loop into transition gestures" in ref_branch["winning"]["keep_moves"]
    assert "Turn Splice Texture Loop into one-shot accents" in tim_branch["winning"]["keep_moves"]

    # Both plans stay coherent: real track, non-destructive, evidence honest.
    names = _track_names(res)
    for branch in (ref_branch, tim_branch):
        for v in branch["variants"]:
            assert set(v["tracks_affected"]) <= names and v["tracks_affected"]
            assert v["reversibility"] == "non_destructive_duplicate_track"


def test_every_plan_is_internally_coherent_under_both_producers(analyzed, tim_analyzed):
    """Plan integrity under BOTH value systems, every fixture: creative
    variants reference real tracks and are reversible with in-range scores and
    argmax winners; per-track actions name real tracks and carry tagged,
    within-bounds risk classes; mute candidates carry element + reason + risk
    class; next_pass is a 1..n-prioritised list of at most five titled moves;
    every governed winner is a real variant of its branch."""
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            res = results[name]
            names = _track_names(res)

            for branch in res.creative["branches"]:
                variant_ids = set()
                for v in branch["variants"]:
                    variant_ids.add(v["variant_id"])
                    assert v["tracks_affected"], (name, v["variant_id"])
                    assert set(v["tracks_affected"]) <= names, (name, v["variant_id"])
                    assert v["reversibility"] == "non_destructive_duplicate_track"
                    assert 0.0 <= v["scores"]["overall_score"] <= 100.0
                    assert v["risk"] and v["validation"]
                best = max(branch["variants"], key=lambda v: v["scores"]["overall_score"])
                assert branch["winning"]["winning_variant"] == best["variant_id"]

                governed = next(
                    g for g in res.governance["governed_branches"]
                    if g["problem_id"] == branch["problem_id"]
                )
                assert governed["governed_winner"] in variant_ids

            for track in res.mix_plan["per_track_actions"]:
                assert track["track"] in names
                assert track["risk_class"] in RISK_CLASSES
                for action in track["actions"]:
                    assert action["risk_class"] in RISK_CLASSES, (name, track["track"])
                    assert action["reason"]

            for m in res.mix_plan["mute_candidates"]:
                assert m["element"] in names
                assert m["reason"]
                assert m["risk_class"] in RISK_CLASSES

            nxt = res.mix_plan["next_pass"]
            assert 0 <= len(nxt) <= 5
            for i, item in enumerate(nxt, start=1):
                assert item["priority"] == i
                assert item["title"] and item["detail"]


def test_plans_validate_against_the_schemas_under_both_producers(
    analyzed, tim_analyzed, rendered
):
    """COHERENT includes machine-checkable: both producers' mix_plans validate
    against the schema on every fixture, and every one of the six rendered
    artifact trees passes the full output validation."""
    schema = load_schema("mix_plan.schema.json")
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            assert validate_instance(results[name].mix_plan, schema) == []
    for producer in PRODUCERS:
        for name in FIXTURE_NAMES:
            report = validate_output(rendered[(producer, name)])
            assert report["ok"], (producer, name, report["errors"])


# =========================================================================== #
# (b) FULL ATTRIBUTABILITY — the anti-drift guard for all future profile work.
# =========================================================================== #
def test_doctrine_divergence_audit_no_unexplained_divergence(analyzed, tim_analyzed):
    """THE ANTI-DRIFT GUARD: audit the ENTIRE doctrine_score surface (all 14
    components + warnings + evidence + confidence + overall) key by key. The
    two producers diverge on EXACTLY the explained set per fixture — see
    DIVERGENT_DOCTRINE_KEYS. Any future change that makes a component (or
    warnings/evidence) diverge for a NEW reason lands here first, as a
    conscious review, never as silent drift."""
    for name in FIXTURE_NAMES:
        ref_ds = analyzed[name].doctrine_score
        tim_ds = tim_analyzed[name].doctrine_score
        assert set(ref_ds) == set(tim_ds)
        diverged = {k for k in ref_ds if ref_ds[k] != tim_ds[k]}
        assert diverged == DIVERGENT_DOCTRINE_KEYS[name], (name, diverged)
        assert ref_ds["overall_mix_readiness_score"] == OVERALLS[name]["halee_ramone"]
        assert tim_ds["overall_mix_readiness_score"] == OVERALLS[name]["timbaland"]


def test_each_overall_is_its_own_profiles_weighted_mean(analyzed, tim_analyzed):
    """Each producer's overall recomputes EXACTLY as its own profile's
    weighted mean over the shared components (the engine formula, mirrored
    verbatim) — the authored weights are the live lever for BOTH, end to
    end."""
    for producer, results in (("halee_ramone", analyzed), ("timbaland", tim_analyzed)):
        weights = load_profile(producer).doctrine["weights"]
        for name in FIXTURE_NAMES:
            ds = results[name].doctrine_score
            present = {k: ds[k] for k in weights if ds[k] is not None}
            expected = doctrine_engine._clamp(
                sum(present[k] * weights[k] for k in present)
                / sum(weights[k] for k in present)
            )
            assert ds["overall_mix_readiness_score"] == expected, (producer, name)


def test_timbalands_judgment_reconstructs_from_the_references_measurements(
    analyzed, tim_analyzed
):
    """The strongest attributability form: rebuild timbaland's overall from
    the REFERENCE's component scores plus timbaland's AUTHORED values alone —
    substitute only the authored static-loop polarity (both profiles read
    STATIC from the same stems; the reference maps it to 15.0, timbaland
    authors 10.0), apply timbaland's weights, and land on timbaland's actual
    overall to the decimal. Every delta traces to an authored weight or
    polarity; nothing else moved."""
    tim_profile = load_profile("timbaland")
    weights = tim_profile.doctrine["weights"]
    authored_static = tim_profile.doctrine["scorers"]["loop_context"]["static"]
    assert authored_static == 10.0

    for name in FIXTURE_NAMES:
        ref_ds = analyzed[name].doctrine_score
        components = {k: ref_ds[k] for k in COMPONENT_KEYS}
        if name in LOOP_FIXTURES:
            assert ref_ds["loop_context_score"] == 15.0  # the reference's own polarity
            components["loop_context_score"] = authored_static
        present = {k: v for k, v in components.items() if v is not None}
        expected = doctrine_engine._clamp(
            sum(present[k] * weights[k] for k in present)
            / sum(weights[k] for k in present)
        )
        actual = tim_analyzed[name].doctrine_score["overall_mix_readiness_score"]
        assert actual == expected, (name, actual, expected)


# =========================================================================== #
# (c) SAFETY INVARIANCE — across BOTH profiles on the same stems.
# =========================================================================== #
def test_kill_switches_lead_with_the_five_safety_switches_under_both(
    analyzed, tim_analyzed
):
    """At the ``analyze()`` surface, on every fixture, under BOTH producers:
    the composed kill-switch list carries the 5 hardcoded SAFETY switches
    FIRST, VERBATIM (pinned in this file, not read from governance), IN ORDER
    — followed by exactly that profile's authored aesthetic list."""
    assert governance._SAFETY_KILL_SWITCHES == SAFETY_KILL_SWITCHES
    for producer, results in (("halee_ramone", analyzed), ("timbaland", tim_analyzed)):
        aesthetic = load_profile(producer).aesthetic_kill_switches
        for name in FIXTURE_NAMES:
            ks = results[name].governance["kill_switches"]
            assert ks[:5] == SAFETY_KILL_SWITCHES, (producer, name)
            assert ks == SAFETY_KILL_SWITCHES + aesthetic, (producer, name)


def test_no_destructive_recommendation_under_either_producer(analyzed, tim_analyzed):
    """Class 5 appears NOWHERE in either producer's plans: every per-track
    action and every mute candidate stays below class 5 AND passes the
    kill-switch validator (no destructive pattern in any setting); every
    creative variant is a reversible, non-destructive plan; and the class-5
    block itself is engine-fixed regardless of the selected profile."""
    for producer, results in (("halee_ramone", analyzed), ("timbaland", tim_analyzed)):
        for name in FIXTURE_NAMES:
            res = results[name]
            for track in res.mix_plan["per_track_actions"]:
                assert track["risk_class"] < 5, (producer, name, track["track"])
                for action in track["actions"]:
                    assert action["risk_class"] < 5, (producer, name)
                    assert governance.validate_action_safety(action)["blocked"] is False
                for auto in track["automation"]:
                    assert auto["risk_class"] < 5, (producer, name)
            for m in res.mix_plan["mute_candidates"]:
                assert m["risk_class"] < 5, (producer, name)
            for branch in res.creative["branches"]:
                for v in branch["variants"]:
                    assert v["reversibility"] == "non_destructive_duplicate_track"
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


def test_masked_lead_override_reaches_the_plan_surface_under_both(analyzed):
    """THE RAMONE GATE at the PLAN surface (P-032h proved it at the promotion
    call): with the lead bad-masked on an iconic-reading loop, the full
    creative plan under BOTH profiles carries the deconstruct-pressure
    evidence line on loop_A — each profile's OWN authored reason, verbatim.
    Protection never withholds against a buried lead. The branch VERDICT stays
    profile-authored: the reference's promoted loop_A (85.9) wins its branch;
    under timbaland the promotion lifts loop_A 80.7 -> 84.7 while its curated
    accent plan (loop_B, 86.7) still ranks first — pressure applied under
    both, judgment authored per profile."""
    res = _with_masked_lead(_with_iconic_loop(analyzed))
    out_ref = run_creative_engine(
        res, res.creative["search_mode"], profile=load_profile("halee_ramone")
    )
    out_tim = run_creative_engine(
        res, res.creative["search_mode"], profile=load_profile("timbaland")
    )
    ref_branch, tim_branch = _loop_branch(out_ref), _loop_branch(out_tim)

    ref_a = _variant_by_id(ref_branch, "loop_A")["scores"]
    tim_a = _variant_by_id(tim_branch, "loop_A")["scores"]
    assert ref_a["score_nudges"] == [PROMOTION_REASON]
    assert tim_a["score_nudges"] == [TIM_PROMOTION_REASON]
    assert ref_a["overall_score"] == pytest.approx(85.9)
    assert tim_a["overall_score"] == pytest.approx(84.7)
    assert ref_branch["winning"]["winning_variant"] == "loop_A"
    assert tim_branch["winning"]["winning_variant"] == "loop_B"


# =========================================================================== #
# (d) THE PRE-REGISTERED EXPECTATIONS — one still-binding negative (the inert
# blend), and the intimate-mode pin FLIPPED by P-033 as pre-registered.
# =========================================================================== #
def test_no_vocal_blend_delta_the_inert_blend_corollary(analyzed, tim_analyzed):
    """PRE-REGISTERED NEGATIVE EXPECTATION 1 — NO vocal-blend delta.

    ``vocal_role_fit_score`` is IDENTICAL across the two producers on all
    three fixtures (85.0 everywhere), even though timbaland OPTS IN to
    acceptable blend and the reference opts out.

    WHY (the P-032f inert-blend corollary, both profiles' own ``limited``
    confidence entries state it): the masking analyzer emits vocal-band
    events only against the LEAD on real exported-stem data, so the
    blend-eligible path (qualified vocal_percussive / vocal_stack events)
    never receives an event to reinterpret — the policy is mechanically live
    but dormant. A FUTURE ANALYZER-EXTENSION PACKET that emits non-lead
    vocal-band masking events is the change that would legitimately break
    this pin; when it lands, this test must be revisited as a conscious
    decision (the two profiles' policies genuinely differ, so a delta would
    then be expected)."""
    assert load_profile("timbaland").vocal_blend_policy["acceptable_blend"] is True
    assert load_profile("halee_ramone").vocal_blend_policy["acceptable_blend"] is False
    for name in FIXTURE_NAMES:
        ref_v = analyzed[name].doctrine_score["vocal_role_fit_score"]
        tim_v = tim_analyzed[name].doctrine_score["vocal_role_fit_score"]
        assert ref_v == tim_v == 85.0, (name, ref_v, tim_v)


def test_intimate_mode_selection_the_authored_mode_is_reachable(
    analyzed, tim_analyzed
):
    """FORMERLY PRE-REGISTERED NEGATIVE EXPECTATION 2, FLIPPED BY P-033 —
    exactly the packet the old pin named as its legitimate breaker. The
    authored behavior, now pinned:

    * timbaland AUTHORS ``default_creative_mode.intimate_mode:
      "conservative"`` and "conservative" IS a real mode in its own table;
    * ``pipeline._default_creative_mode`` reads the PASSED profile's
      ``default_creative_mode`` table (P-033): the intimate fixture's truth
      resolves to "ramone_vocal_truth" under the reference (its table
      coincides string-for-string with the old hardcoded map — the
      byte-identity construction) and to "conservative" under timbaland;
    * each resolved name is real in its own profile's ``search_modes``, so
      NO fallback fires on either producer (the hardcoded
      "dramatic_contrast" substitute is gone; the profile-owned fallback
      rule and its KeyError-scenario guard live in
      test_creative_mode_wiring.py)."""
    tim = load_profile("timbaland")
    assert tim.default_creative_mode["intimate_mode"] == "conservative"
    assert "conservative" in tim.search_modes

    intent = analyzed["simple_vocal_piano_song"].project.intent
    assert pipeline._default_creative_mode(intent) == "ramone_vocal_truth"
    assert pipeline._default_creative_mode(intent, tim) == "conservative"
    assert "ramone_vocal_truth" not in tim.search_modes

    observed = tim_analyzed["simple_vocal_piano_song"].creative["search_mode"]
    assert observed == "conservative"
    assert observed == tim.default_creative_mode["intimate_mode"]
    assert "search_mode_fallback" not in tim_analyzed["simple_vocal_piano_song"].creative


# =========================================================================== #
# (e) PER-PROFILE CONFIDENCE RENDERING — at the differential level.
# =========================================================================== #
def test_confidence_maps_differ_where_authored(analyzed, tim_analyzed):
    """On every fixture each producer's ``doctrine_score.confidence`` IS its
    own authored map: 8 entries (2 high / 1 limited / 5 deferred) for the
    reference vs 11 (5 high / 1 limited / 5 deferred) for timbaland; the two
    maps differ in every non-deferred entry (even the shared 'vocal blend
    interpretation' area carries each profile's own reason), while the
    5-entry deferred tail — the engine boundaries — is verbatim-shared and
    legitimately identical."""
    ref_map = load_profile("halee_ramone").confidence_map
    tim_map = load_profile("timbaland").confidence_map
    assert len(ref_map) == 8 and len(tim_map) == 11
    assert [e["level"] for e in ref_map].count("high") == 2
    assert [e["level"] for e in tim_map].count("high") == 5
    assert ref_map[3:] == tim_map[6:]          # the shared deferred tail
    assert all(r != t for r in ref_map[:3] for t in tim_map[:6])

    for name in FIXTURE_NAMES:
        ref_conf = analyzed[name].doctrine_score["confidence"]
        tim_conf = tim_analyzed[name].doctrine_score["confidence"]
        assert ref_conf == ref_map, name
        assert tim_conf == tim_map, name
        assert ref_conf != tim_conf, name


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_artifacts_render_their_own_map_and_never_the_others(name, rendered):
    """Every rendered artifact tree carries ITS producer's map — every entry's
    area AND reason in the verdict markdown, the full map verbatim in
    doctrine_score.json — and neither profile's DISTINCT voice appears in the
    other's artifacts (the shared deferred entries render under both, by
    design)."""
    for producer, own_only, other_only in (
        ("halee_ramone", REFERENCE_ONLY_STRINGS, TIMBALAND_ONLY_STRINGS),
        ("timbaland", TIMBALAND_ONLY_STRINGS, REFERENCE_ONLY_STRINGS),
    ):
        own_map = load_profile(producer).confidence_map
        md = _verdict(rendered, producer, name)
        assert "## Confidence" in md
        for entry in own_map:
            assert entry["area"] in md, (producer, entry["area"])
            assert entry["reason"] in md, (producer, entry["area"])
        for s in own_only:
            assert s in md, (producer, s)
        for s in other_only:
            assert s not in md, (producer, s)

        dsj = json.loads(
            (rendered[(producer, name)] / "doctrine_score.json").read_text(encoding="utf-8")
        )
        assert dsj["confidence"] == own_map


# =========================================================================== #
# The comparison surface — the compact side-by-side, pinned verbatim.
# =========================================================================== #
def test_differential_snapshot_matches_the_pinned_comparison(analyzed, tim_analyzed):
    """``differential_snapshot`` on every fixture equals the pinned
    EXPECTED_SNAPSHOT: same stems, two producers, side by side — overall /
    lowest-3 components / winning variants / search mode. This is the
    receipt-printable comparison surface; any engine or profile change that
    moves it lands here as a visible diff."""
    for name in FIXTURE_NAMES:
        snap = differential_snapshot(analyzed[name], tim_analyzed[name])
        assert snap == EXPECTED_SNAPSHOT[name], (name, snap)
