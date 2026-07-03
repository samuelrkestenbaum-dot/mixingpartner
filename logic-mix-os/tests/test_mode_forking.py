"""P-042 — PROFILE-AUTHORED MODE FORKING (Shape B): mode becomes load-bearing.

Before this packet ``generate_variants(problem, result, mode)`` received the
mode but did not read it — conservative and experimental produced the same
candidate move set. This suite is the binding proof of the user's ten
requirements for the fork:

* ``generate_variants`` READS the active mode (mutation-style guard: a
  cosmetic ``mode`` argument fails here);
* different modes can emit DIFFERENT CANDIDATE SETS for the same
  producer/problem — asserted on variant-id/kind SETS, never order or labels;
* the differences are driven by profile-authored ``search_modes`` data
  (``favor_kinds`` / ``suppress_kinds``), reconstructed from the JSONs: the
  expected set is derived as ENGINE POOL minus the authored suppressions,
  never re-read from the code under test;
* the ownership split holds: the ENGINE owns the shared move vocabulary (the
  frozen curated pool, pinned here), the PROFILE owns each mode's reach,
  GOVERNANCE owns the safety cap — a favored kind whose curated translation
  risk exceeds the mode's ``allowed_risk`` is rejected at load AND refused at
  emission (the cap wins; it cannot be out-authored);
* suppression can never empty a candidate set (the documented,
  profile-agnostic fallback: the full neutral curated pool);
* NO per-producer engine branching: an AST scan of the fork path's modules
  proves no producer name appears in code outside the pre-P-042
  default-reference constant;
* reference no-drift: the DEFAULT-FLOW candidate id lists for every shipped
  producer are pinned byte-stable (the shipped default/intimate modes author
  NEUTRAL declarations — the packet's conscious choice, so requirement 8
  holds by construction and the fork is proven on non-default modes).
"""

from __future__ import annotations

import ast
import dataclasses
import json
import pathlib

import pytest

from logic_mix_os import pipeline
from logic_mix_os.constants import (
    CREATIVE_EXTENDED_KINDS,
    CREATIVE_VARIANT_KINDS,
    TRANSLATION_RISK_LEVELS,
)
from logic_mix_os.creative import (
    _curated_variants,
    _fork_candidates,
    _mode_declarations,
    generate_variants,
    run_creative_engine,
)
from logic_mix_os.doctrine.producer_profile import _validate, load_profile
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest
from logic_mix_os.renderers.creative_renderer import render_creative

from conftest import FIXTURE_NAMES, ROOT

_PACKAGE = ROOT / "logic_mix_os"
_PRODUCERS_DIR = _PACKAGE / "doctrine" / "producers"

PRODUCERS = ("halee_ramone", "timbaland", "quincy_jones")
DENSE = "dense_chorus_with_loops"

# THE ENGINE POOL — the frozen curated emission per problem, (variant_id,
# kind) in curated order. This is the shared move vocabulary every profile
# forks FROM; the reconstructive proofs below derive every expected candidate
# set from THIS pin plus the authored JSON declarations alone.
ENGINE_POOL = {
    "chorus_lift": [
        ("chorus_lift_A", "width_bloom"),
        ("chorus_lift_B", "subtractive_drop"),
        ("chorus_lift_C", "vocal_ride"),
        ("chorus_lift_D", "drum_room_bloom"),
    ],
    "density": [
        ("density_A", "depth_cleanup"),
        ("density_B", "subtractive_drop"),
    ],
    "loop": [
        ("loop_A", "loop_deconstruct"),
        ("loop_B", "subtractive_drop"),
    ],
    "depth": [
        ("depth_A", "depth_cleanup"),
    ],
    "vocal_belief": [
        ("vocal_A", "vocal_ride"),
        ("vocal_B", "intimacy_pass"),
    ],
}
PROBLEM_IDS = tuple(ENGINE_POOL)

# The DEFAULT-FLOW pin (requirement 8): the per-branch variant-id lists every
# shipped producer must emit on its own default-flow mode — identical to the
# pre-P-042 neutral emission, order included, for all three producers.
DEFAULT_FLOW_IDS = {
    "simple_vocal_piano_song": {
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "dense_chorus_with_loops": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "splice_loop_problem": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"],
        "loop": ["loop_A", "loop_B"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
}


def _raw(producer: str) -> dict:
    """The producer's AUTHORED JSON, read directly from disk — the
    attribution basis (never the loader, never the code under test)."""
    with open(_PRODUCERS_DIR / f"{producer}.json", encoding="utf-8") as fh:
        return json.load(fh)


def _ids(variants) -> list:
    return [v["variant_id"] for v in variants]


def _kinds(variants) -> set:
    return {v["kind"] for v in variants}


def _branch(out: dict, pid: str) -> dict:
    return next(b for b in out["branches"] if b["problem_id"] == pid)


def _pool_kinds(pid: str) -> list:
    return [kind for _, kind in ENGINE_POOL[pid]]


def _expected_kind_set(pid: str, suppress_kinds) -> set:
    """The reconstructive rule: ENGINE POOL minus the authored suppressions —
    with the engine's documented non-empty fallback (a fully-suppressed pool
    emits the full neutral pool)."""
    pool = set(_pool_kinds(pid))
    expected = pool - set(suppress_kinds)
    return expected if expected else pool


@pytest.fixture(scope="module")
def dense(analyzed):
    return analyzed[DENSE]


# =========================================================================== #
# The engine pool: frozen vocabulary, pinned emission.
# =========================================================================== #
def test_engine_pool_is_the_frozen_curated_emission(dense):
    """The neutral emission per problem IS the pinned engine pool (ids, kinds
    AND order), and the union of pool kinds IS the engine's NEUTRAL move
    vocabulary. P-043 (the conscious widening): ``CREATIVE_VARIANT_KINDS``
    now also carries the EXTENDED kinds — reach-gated, never part of the
    neutral pool — so the union pin is vocabulary-minus-extended and the
    extended kinds are asserted ABSENT from every neutral emission (their
    own pins live in tests/test_move_vocabulary_expansion.py)."""
    for pid in PROBLEM_IDS:
        variants = generate_variants({"id": pid}, dense)
        assert [(v["variant_id"], v["kind"]) for v in variants] == ENGINE_POOL[pid]
    union = {kind for pool in ENGINE_POOL.values() for _, kind in pool}
    assert union == set(CREATIVE_VARIANT_KINDS) - set(CREATIVE_EXTENDED_KINDS)
    assert union & set(CREATIVE_EXTENDED_KINDS) == set()


# =========================================================================== #
# Requirement 1 — generate_variants READS the mode (the mutation guard).
# =========================================================================== #
def test_generate_variants_reads_the_mode_mutation_guard(dense):
    """Same producer, same problem, same stems/records: a non-default mode
    with authored suppressions emits a DIFFERENT candidate set than the
    default emission. A regression that makes ``mode`` cosmetic again (or
    that turns the fork into ranking-only) fails here on the SET."""
    ref = load_profile("halee_ramone")
    neutral = generate_variants({"id": "chorus_lift"}, dense)
    forked = generate_variants({"id": "chorus_lift"}, dense, "deconstructive", ref)

    assert _kinds(forked) != _kinds(neutral)
    assert set(_ids(forked)) != set(_ids(neutral))
    # the authored suppressions are the whole difference (set-level)
    suppressed = set(_raw("halee_ramone")["search_modes"]["deconstructive"]["suppress_kinds"])
    assert _kinds(neutral) - _kinds(forked) == suppressed & _kinds(neutral)
    assert not (_kinds(forked) - _kinds(neutral))  # the fork never GROWS the set

    # the P-029 default: ``profile=None`` resolves to the reference.
    assert generate_variants({"id": "chorus_lift"}, dense, "deconstructive") == forked


def test_no_mode_and_neutral_modes_are_byte_identical(dense):
    """``mode=None``, an unknown mode, and the reference's two NEUTRAL
    default-flow modes (authored empty reach) all emit the identical neutral
    list — full dict equality, order included (pre-P-042 callers and the
    default flow are untouched)."""
    ref = load_profile("halee_ramone")
    for pid in PROBLEM_IDS:
        base = generate_variants({"id": pid}, dense)
        for mode in ("dramatic_contrast", "vocal_truth", "no_such_mode", None):
            assert generate_variants({"id": pid}, dense, mode, ref) == base, (pid, mode)


# =========================================================================== #
# Requirement 2 — different modes, different candidate SETS (same producer).
# =========================================================================== #
def test_same_producer_different_modes_different_candidate_sets(dense):
    """Halee/Ramone on the dense fixture, four modes through the REAL engine
    surface (``run_creative_engine``): the chorus_lift candidate-id sets are
    the reconstructed pool-minus-suppressions per mode, and the non-default
    modes' sets genuinely differ from the default's AND from each other."""
    ref = load_profile("halee_ramone")
    sets = {}
    for mode in ("conservative", "deconstructive", "dramatic_contrast", "experimental"):
        out = run_creative_engine(dense, mode, profile=ref)
        assert out["search_mode"] == mode
        sets[mode] = set(_ids(_branch(out, "chorus_lift")["variants"]))

    assert sets["dramatic_contrast"] == {
        "chorus_lift_A", "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert sets["conservative"] == {"chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert sets["deconstructive"] == {"chorus_lift_B", "chorus_lift_C"}
    assert sets["experimental"] == sets["dramatic_contrast"]  # suppresses nothing
    # pairwise distinct where the authored suppressions differ
    assert sets["conservative"] != sets["dramatic_contrast"]
    assert sets["deconstructive"] != sets["dramatic_contrast"]
    assert sets["deconstructive"] != sets["conservative"]


# =========================================================================== #
# Requirements 3 + 9 — the fork is ATTRIBUTABLE to the authored JSON.
# =========================================================================== #
def test_reference_fork_is_attributable_to_its_authored_json(dense):
    """The reconstructive proof (the test_three_way_differential idiom): for
    EVERY reference mode and EVERY problem, the emitted kind set equals the
    ENGINE POOL minus that mode's authored ``suppress_kinds`` — derived from
    the JSON on disk, so a code-path hack that forks without reading the
    profile data cannot pass."""
    ref = load_profile("halee_ramone")
    raw_modes = _raw("halee_ramone")["search_modes"]
    for mode_name, entry in raw_modes.items():
        for pid in PROBLEM_IDS:
            emitted = _kinds(generate_variants({"id": pid}, dense, mode_name, ref))
            assert emitted == _expected_kind_set(pid, entry["suppress_kinds"]), \
                (mode_name, pid)


def test_the_passed_profiles_declarations_drive_the_fork_not_the_references(dense):
    """Per-call threading at the engine surface (the P-029/P-039 lesson): a
    profile re-authoring a mode NAME the reference also carries must see ITS
    OWN declarations through ``run_creative_engine`` — if the seam read the
    module default instead of the passed profile, the reference's
    ``deconstructive`` reach (suppress width_bloom + drum_room_bloom) would
    leak in and this fails in both directions."""
    ref = load_profile("halee_ramone")
    modes = {k: dict(v) for k, v in ref.search_modes.items()}
    modes["deconstructive"] = {
        "allowed_risk": "medium",
        "bias": "test-local: a different deconstructive reach",
        "favor_kinds": [],
        "suppress_kinds": ["subtractive_drop"],
    }
    synthetic = dataclasses.replace(ref, search_modes=modes)

    out = run_creative_engine(dense, "deconstructive", profile=synthetic)
    kinds = _kinds(_branch(out, "chorus_lift")["variants"])
    assert "subtractive_drop" not in kinds        # the PASSED profile's suppression
    assert {"width_bloom", "drum_room_bloom"} <= kinds  # the reference's did NOT apply


# =========================================================================== #
# Favoring shapes order WITHIN the set — never the set itself.
# =========================================================================== #
def test_favor_shapes_order_within_the_set_never_grows_it(dense):
    """Favored kinds are emitted first (authored favor order), the set is
    unchanged, and favoring a kind the problem's pool does not hold adds
    nothing (favor can never grow the frozen pool)."""
    ref = load_profile("halee_ramone")
    # experimental favors [width_bloom, drum_room_bloom]: A and D move front.
    exp = generate_variants({"id": "chorus_lift"}, dense, "experimental", ref)
    assert _ids(exp) == ["chorus_lift_A", "chorus_lift_D", "chorus_lift_B", "chorus_lift_C"]
    assert _kinds(exp) == set(_pool_kinds("chorus_lift"))
    # conservative favors [vocal_ride, depth_cleanup]: vocal_ride fronts the
    # suppressed pool; depth_cleanup is absent from this pool — no growth.
    cons = generate_variants({"id": "chorus_lift"}, dense, "conservative", ref)
    assert _ids(cons) == ["chorus_lift_C", "chorus_lift_B", "chorus_lift_D"]


# =========================================================================== #
# Requirements 6 + 7 — GOVERNANCE OWNS THE CAP: allowed_risk still binds.
# =========================================================================== #
def test_allowed_risk_cap_binds_at_emission(dense):
    """A test-local profile favors ``width_bloom`` (curated translation risk
    ``medium``) on a mode whose posture is ``allowed_risk: low``: the cap
    WINS — the favor is refused, the emission is byte-identical to neutral,
    and the refusal is reported. The control run (same favor, ``medium``
    posture) proves the mechanism itself works, so the refusal is the CAP."""
    ref = load_profile("halee_ramone")

    def reach(allowed_risk):
        return dataclasses.replace(ref, search_modes={
            "reach": {
                "allowed_risk": allowed_risk,
                "bias": "test-local: reach for width_bloom",
                "favor_kinds": ["width_bloom"],
                "suppress_kinds": [],
            },
        })

    neutral = generate_variants({"id": "chorus_lift"}, dense)
    capped = generate_variants({"id": "chorus_lift"}, dense, "reach", reach("low"))
    assert capped == neutral  # the cap wins: no elevation, no set change

    prof_low = reach("low")
    _, fork = _fork_candidates(
        _curated_variants({"id": "chorus_lift"}, dense),
        _mode_declarations(prof_low, "reach"), prof_low,
    )
    assert fork["risk_capped"] == ["width_bloom"]
    assert fork["favored"] == []

    control = generate_variants({"id": "chorus_lift"}, dense, "reach", reach("medium"))
    assert _ids(control)[0] == "chorus_lift_A"  # within posture, the favor applies
    assert _kinds(control) == _kinds(neutral)


def test_allowed_risk_cap_binds_at_load():
    """The same cap at AUTHORING time: a profile JSON that favors a kind
    beyond the mode's ``allowed_risk`` fails LOUDLY at load — the cap cannot
    be out-authored. Control: the same favor under a ``medium`` posture
    validates."""
    raw = _raw("halee_ramone")
    raw["search_modes"]["vocal_truth"]["favor_kinds"] = ["width_bloom"]  # low mode
    with pytest.raises(ValueError, match="cannot be out-authored"):
        _validate(raw, "halee_ramone")

    control = _raw("halee_ramone")
    control["search_modes"]["spatial_depth"]["favor_kinds"] = ["width_bloom"]  # medium
    _validate(control, "halee_ramone")


def test_fail_closed_posture_for_loader_bypassing_profiles(dense):
    """A declaring mode without a recognized ``allowed_risk`` (only reachable
    by bypassing the loader) is capped at the MOST restrictive posture —
    fail closed, never open."""
    ref = load_profile("halee_ramone")
    prof = dataclasses.replace(ref, search_modes={
        "reach": {
            "bias": "test-local: no allowed_risk authored",
            "favor_kinds": ["width_bloom"],   # medium risk — must be refused
            "suppress_kinds": [],
        },
    })
    decl = _mode_declarations(prof, "reach")
    assert decl["allowed_risk"] == TRANSLATION_RISK_LEVELS[0]
    assert generate_variants({"id": "chorus_lift"}, dense, "reach", prof) \
        == generate_variants({"id": "chorus_lift"}, dense)


# =========================================================================== #
# Loader validation — bad declarations fail loudly, at load.
# =========================================================================== #
def test_declaration_validation_fails_loudly():
    """Every malformed declaration shape is a load-time ValueError naming
    ``search_modes`` — never a judgment-time surprise. Control first: the
    shipped reference JSON validates as authored."""
    _validate(_raw("halee_ramone"), "halee_ramone")

    def broken(**edit):
        raw = _raw("halee_ramone")
        raw["search_modes"]["vocal_truth"].update(edit)
        return raw

    for bad in (
        broken(favor_kinds="vocal_ride"),                       # not a list
        broken(favor_kinds=["vocal_ride", 3]),                  # non-str member
        broken(favor_kinds=["no_such_kind"]),                   # outside the vocabulary
        broken(suppress_kinds=["no_such_kind"]),                # outside the vocabulary
        broken(favor_kinds=["vocal_ride", "vocal_ride"]),       # duplicate
        broken(favor_kinds=["vocal_ride"],
               suppress_kinds=["vocal_ride"]),                  # contradiction
        broken(favor_kinds=["vocal_ride"], allowed_risk="extreme"),
    ):
        with pytest.raises(ValueError, match="search_modes"):
            _validate(bad, "halee_ramone")

    # a declaring mode must carry allowed_risk at all
    raw = _raw("halee_ramone")
    del raw["search_modes"]["vocal_truth"]["allowed_risk"]
    raw["search_modes"]["vocal_truth"]["suppress_kinds"] = ["width_bloom"]
    with pytest.raises(ValueError, match="allowed_risk"):
        _validate(raw, "halee_ramone")


def test_unknown_kinds_in_declarations_are_inert_at_runtime(dense):
    """Runtime posture for loader-bypassing profiles: declaration kinds
    outside the vocabulary suppress nothing and favor nothing — the loader is
    the loud gate, the engine is inert-by-construction."""
    ref = load_profile("halee_ramone")
    prof = dataclasses.replace(ref, search_modes={
        "ghost": {
            "allowed_risk": "high",
            "bias": "test-local: ghost kinds",
            "favor_kinds": ["not_a_kind"],
            "suppress_kinds": ["also_not_a_kind"],
        },
    })
    for pid in PROBLEM_IDS:
        assert generate_variants({"id": pid}, dense, "ghost", prof) \
            == generate_variants({"id": pid}, dense), pid


# =========================================================================== #
# The NON-EMPTY guarantee — suppression can never empty a candidate set.
# =========================================================================== #
def test_suppression_can_never_empty_the_set(dense):
    """A test-local profile suppressing the ENTIRE vocabulary: every problem
    still emits its full neutral curated pool (the documented,
    profile-agnostic fallback), and the fork report flags the fallback with
    nothing 'suppressed' (honesty: nothing was actually removed)."""
    ref = load_profile("halee_ramone")
    prof = dataclasses.replace(ref, search_modes={
        "nothing": {
            "allowed_risk": "high",
            "bias": "test-local: suppress everything",
            "favor_kinds": [],
            "suppress_kinds": list(CREATIVE_VARIANT_KINDS),
        },
    })
    for pid in PROBLEM_IDS:
        neutral = generate_variants({"id": pid}, dense)
        emitted = generate_variants({"id": pid}, dense, "nothing", prof)
        assert emitted == neutral, pid
        assert emitted, pid

        _, fork = _fork_candidates(
            _curated_variants({"id": pid}, dense),
            _mode_declarations(prof, "nothing"), prof,
        )
        assert fork["suppression_fallback"] is True, pid
        assert fork["suppressed"] == [], pid


# =========================================================================== #
# Requirement 8 — DEFAULT-FLOW NO-DRIFT, pinned for every shipped producer.
# =========================================================================== #
@pytest.mark.parametrize("producer", PRODUCERS)
def test_default_flow_candidate_ids_do_not_drift(producer, analyzed):
    """Each producer's own default-flow mode (its authored
    ``default_creative_mode`` resolution per fixture) emits the PINNED
    pre-P-042 variant-id lists — order included — on all three fixtures.
    The shipped profiles author NEUTRAL declarations on their default and
    intimate modes (the packet's conscious choice), so the fork lives ONLY
    on non-default modes."""
    prof = load_profile(producer)
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        out = run_creative_engine(res, mode, profile=prof)
        emitted = {b["problem_id"]: _ids(b["variants"]) for b in out["branches"]}
        assert emitted == DEFAULT_FLOW_IDS[name], (producer, name)


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_shipped_profile_authors_the_fields_explicitly(producer):
    """Every shipped profile authors ``favor_kinds`` + ``suppress_kinds``
    EXPLICITLY on every mode (no silent inheritance for load-bearing
    choices); its default-flow modes (declared default + intimate) author
    them NEUTRAL — the requirement-8 construction, visible in the JSON
    itself; and at least one NON-default mode authors a NON-neutral reach,
    so the fork is real for every producer."""
    raw = _raw(producer)
    for mode_name, entry in raw["search_modes"].items():
        assert "favor_kinds" in entry, (producer, mode_name)
        assert "suppress_kinds" in entry, (producer, mode_name)
    default_flow = {raw["default_creative_mode"]["default_mode"],
                    raw["default_creative_mode"]["intimate_mode"]}
    for mode_name in default_flow:
        entry = raw["search_modes"][mode_name]
        assert entry["favor_kinds"] == [], (producer, mode_name)
        assert entry["suppress_kinds"] == [], (producer, mode_name)
    forking = [m for m, e in raw["search_modes"].items()
               if e["favor_kinds"] or e["suppress_kinds"]]
    assert forking, producer
    assert not default_flow & set(forking), producer


# =========================================================================== #
# Requirement 4 — SAME MODE NAME, DIFFERENT PRODUCERS, different sets.
# =========================================================================== #
def test_same_mode_different_producers_different_candidate_sets(dense):
    """``conservative`` exists in all three profiles: on the same stems and
    problem it emits THREE pairwise-distinct candidate-id sets — Timbaland's
    authored-neutral full pool, Halee/Ramone's width-suppressed pool,
    Quincy's width-and-drum-room-suppressed pool. And on ``experimental``,
    Timbaland's authored ``intimacy_pass`` suppression splits the
    vocal_belief set from both others. Sets, not order or labels."""
    conservative = {}
    for producer in PRODUCERS:
        out = run_creative_engine(dense, "conservative", profile=load_profile(producer))
        conservative[producer] = set(_ids(_branch(out, "chorus_lift")["variants"]))
    assert conservative["timbaland"] == {
        "chorus_lift_A", "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert conservative["halee_ramone"] == {
        "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert conservative["quincy_jones"] == {"chorus_lift_B", "chorus_lift_C"}
    assert len({frozenset(s) for s in conservative.values()}) == 3  # pairwise distinct

    experimental = {}
    for producer in PRODUCERS:
        out = run_creative_engine(dense, "experimental", profile=load_profile(producer))
        experimental[producer] = set(_ids(_branch(out, "vocal_belief")["variants"]))
    assert experimental["timbaland"] == {"vocal_A"}
    assert experimental["halee_ramone"] == {"vocal_A", "vocal_B"}
    assert experimental["quincy_jones"] == {"vocal_A", "vocal_B"}


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_producers_every_mode_is_attributable_to_its_json(producer, dense):
    """The full reconstructive attribution (requirements 3 + 4 + 9), all
    three producers: for EVERY authored mode and EVERY problem, the emitted
    kind set equals the shared ENGINE POOL minus THAT producer's authored
    ``suppress_kinds`` for THAT mode — derived from the JSON on disk. Where
    two producers' declarations differ, their same-mode sets differ; where
    they are both neutral (``dramatic_contrast``), the sets agree — the
    difference is the DATA, never a code path."""
    prof = load_profile(producer)
    raw_modes = _raw(producer)["search_modes"]
    for mode_name, entry in raw_modes.items():
        for pid in PROBLEM_IDS:
            emitted = _kinds(generate_variants({"id": pid}, dense, mode_name, prof))
            assert emitted == _expected_kind_set(pid, entry["suppress_kinds"]), \
                (producer, mode_name, pid)


# =========================================================================== #
# The REAL CALL CHAIN (the P-039 threading lesson) + requirement 10.
# =========================================================================== #
def test_profile_declarations_reach_the_seam_through_the_real_call_chain():
    """Flag PRESENCE is not flag THREADING: a real
    ``analyze(producer="timbaland", creative_mode="negative_space")`` run —
    the same chain the CLI drives — must show timbaland's AUTHORED
    declarations forking the emission, artifact-level: the echoed
    declarations equal the JSON verbatim, the suppressed kinds are absent
    from the emitted set, and the per-branch fork report names what was
    actually suppressed/favored."""
    manifest = load_manifest(ROOT / "fixtures" / DENSE / "project_manifest.json")
    res = analyze(str(ROOT / "fixtures" / DENSE / "stems"), manifest,
                  producer="timbaland", creative_mode="negative_space")
    cr = res.creative
    authored = _raw("timbaland")["search_modes"]["negative_space"]

    assert cr["search_mode"] == "negative_space"
    assert cr["search_mode_declarations"] == {
        "allowed_risk": authored["allowed_risk"],
        "favor_kinds": authored["favor_kinds"],
        "suppress_kinds": authored["suppress_kinds"],
    }

    chorus = _branch(cr, "chorus_lift")
    assert _kinds(chorus["variants"]) \
        == _expected_kind_set("chorus_lift", authored["suppress_kinds"])
    assert set(authored["suppress_kinds"]) & _kinds(chorus["variants"]) == set()
    assert chorus["mode_fork"] == {
        "suppressed": ["width_bloom", "drum_room_bloom"],
        "favored": ["subtractive_drop"],
        "risk_capped": [],
        "suppression_fallback": False,
    }
    # a branch the suppressions don't touch still explains itself honestly
    vocal = _branch(cr, "vocal_belief")
    assert vocal["mode_fork"] == {
        "suppressed": [], "favored": [], "risk_capped": [],
        "suppression_fallback": False,
    }
    # the run is a full pipeline run — governance governed the forked sets
    assert res.governance["governed_branches"]


def test_artifact_explains_the_fork_requirement_10(dense):
    """The engine artifact carries enough mode information to explain WHY a
    candidate set differed: the authored declarations echo plus, per branch,
    what was actually suppressed and favored — pinned for the reference's
    ``deconstructive`` mode."""
    out = run_creative_engine(dense, "deconstructive", profile=load_profile("halee_ramone"))
    authored = _raw("halee_ramone")["search_modes"]["deconstructive"]
    assert out["search_mode_declarations"] == {
        "allowed_risk": "medium",
        "favor_kinds": authored["favor_kinds"],
        "suppress_kinds": authored["suppress_kinds"],
    }
    for b in out["branches"]:
        assert "mode_fork" in b, b["problem_id"]
    assert _branch(out, "chorus_lift")["mode_fork"] == {
        "suppressed": ["width_bloom", "drum_room_bloom"],
        "favored": ["subtractive_drop"],
        "risk_capped": [],
        "suppression_fallback": False,
    }
    assert _branch(out, "loop")["mode_fork"]["favored"] \
        == ["subtractive_drop", "loop_deconstruct"]
    assert _branch(out, "depth")["mode_fork"] == {
        "suppressed": [], "favored": [], "risk_capped": [],
        "suppression_fallback": False,
    }


@pytest.mark.parametrize("producer", PRODUCERS)
def test_artifact_keys_absent_on_default_flows(producer, analyzed):
    """The evidence-key discipline (and the committed sample trees' byte
    safety): neutral/default runs carry NEITHER additive key — zero new
    artifact bytes anywhere on the default flow."""
    prof = load_profile(producer)
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        out = run_creative_engine(res, mode, profile=prof)
        assert "search_mode_declarations" not in out, (producer, name)
        for b in out["branches"]:
            assert "mode_fork" not in b, (producer, name, b["problem_id"])


def test_fallback_and_risk_cap_are_surfaced_in_the_artifact(dense):
    """Honesty over silence: the non-empty fallback and the allowed-risk
    refusal both surface in the artifact when they fire."""
    ref = load_profile("halee_ramone")
    nothing = dataclasses.replace(ref, search_modes={
        "nothing": {
            "allowed_risk": "high",
            "bias": "test-local: suppress everything",
            "favor_kinds": [],
            "suppress_kinds": list(CREATIVE_VARIANT_KINDS),
        },
    })
    out = run_creative_engine(dense, "nothing", profile=nothing)
    for b in out["branches"]:
        assert b["mode_fork"]["suppression_fallback"] is True, b["problem_id"]
        assert b["mode_fork"]["suppressed"] == [], b["problem_id"]
        assert _ids(b["variants"]) == [vid for vid, _ in ENGINE_POOL[b["problem_id"]]]

    reach = dataclasses.replace(ref, search_modes={
        "reach": {
            "allowed_risk": "low",
            "bias": "test-local: reach beyond posture",
            "favor_kinds": ["width_bloom"],
            "suppress_kinds": [],
        },
    })
    out = run_creative_engine(dense, "reach", profile=reach)
    chorus = _branch(out, "chorus_lift")
    assert chorus["mode_fork"]["risk_capped"] == ["width_bloom"]
    assert chorus["mode_fork"]["favored"] == []
    assert _ids(chorus["variants"]) == [vid for vid, _ in ENGINE_POOL["chorus_lift"]]


def test_renderer_explains_the_fork_and_stays_silent_when_neutral(dense):
    """Requirement 10 at the RENDERER: a forking run renders the authored
    mode reach and the per-branch fork lines; the fallback and the cap
    refusal render when they fire; a neutral default run renders ZERO fork
    bytes (the sample trees' human-readable half stays byte-identical)."""
    ref = load_profile("halee_ramone")
    md = render_creative(run_creative_engine(dense, "deconstructive", profile=ref))
    assert "**Mode reach (profile-authored):**" in md
    assert "suppresses `width_bloom`, `drum_room_bloom`" in md
    assert "favors `subtractive_drop`, `loop_deconstruct`" in md
    assert "capped at `medium` risk" in md
    assert "_Mode fork: suppressed `width_bloom`, `drum_room_bloom`" in md

    nothing = dataclasses.replace(ref, search_modes={
        "nothing": {"allowed_risk": "high", "bias": "test-local",
                    "favor_kinds": [], "suppress_kinds": list(CREATIVE_VARIANT_KINDS)},
    })
    md_fb = render_creative(run_creative_engine(dense, "nothing", profile=nothing))
    assert "the full neutral pool was emitted (fallback)" in md_fb

    reach = dataclasses.replace(ref, search_modes={
        "reach": {"allowed_risk": "low", "bias": "test-local",
                  "favor_kinds": ["width_bloom"], "suppress_kinds": []},
    })
    md_cap = render_creative(run_creative_engine(dense, "reach", profile=reach))
    assert "favor refused by the allowed-risk cap: `width_bloom`" in md_cap

    md_neutral = render_creative(run_creative_engine(dense, "dramatic_contrast", profile=ref))
    assert "Mode reach" not in md_neutral
    assert "Mode fork" not in md_neutral


# =========================================================================== #
# Requirement 5 — NO PER-PRODUCER ENGINE BRANCHING (grep-provable, as AST).
# =========================================================================== #
# The modules that carry the fork path this packet built/touched. The ONLY
# producer-name token allowed in their CODE (string constants outside
# docstrings, plus every identifier) is the exact pre-P-042 default-reference
# constant "halee_ramone".
_FORK_PATH_MODULES = (
    _PACKAGE / "creative.py",
    _PACKAGE / "doctrine" / "producer_profile.py",
    _PACKAGE / "pipeline.py",
    _PACKAGE / "constants.py",
)
_PRODUCER_TOKENS = ("timbaland", "quincy", "halee", "ramone")


def _code_producer_mentions(path: pathlib.Path) -> list:
    """Every producer-name mention in the module's CODE: non-docstring string
    constants and all identifiers (names, attributes, arguments, function
    names). Docstrings are documentation, not branches — excluded."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) \
                    and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docstrings.add(id(body[0].value))

    mentions = []

    def _check(text):
        if any(tok in text.lower() for tok in _PRODUCER_TOKENS):
            mentions.append(text)

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in docstrings:
            _check(node.value)
        elif isinstance(node, ast.Name):
            _check(node.id)
        elif isinstance(node, ast.Attribute):
            _check(node.attr)
        elif isinstance(node, ast.arg):
            _check(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            _check(node.name)
        elif isinstance(node, ast.keyword) and node.arg:
            _check(node.arg)
    return mentions


@pytest.mark.parametrize("module", _FORK_PATH_MODULES, ids=lambda p: p.name)
def test_no_producer_names_in_the_fork_path_code(module):
    """Every producer-name mention in the fork path's code is EXACTLY the
    default-reference constant — no timbaland/quincy anywhere, no hidden
    per-producer branch, provably."""
    mentions = _code_producer_mentions(module)
    assert all(m == "halee_ramone" for m in mentions), (module.name, mentions)
