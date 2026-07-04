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

P-043 (conscious deltas, enumerated): the engine vocabulary widened by the
two REACH-GATED extended kinds (``arrangement_lift`` / ``ensemble_rebalance``
— tests/test_move_vocabulary_expansion.py). quincy_jones authors reach on
three modes — including his DEFAULT mode, which is literally NAMED
``arrangement_lift`` (reach IS its meaning under his arrangement-led
philosophy) — so HIS default-flow pin gains exactly the reached ids
(QUINCY_DEFAULT_FLOW_IDS below) and his default artifacts carry the reach
surface; halee_ramone/timbaland author ZERO reach and every one of their
pins here is byte-identical. The reconstructive rule extends to
(pool ∪ authored reach) − suppress, with the unchanged neutral-only
fallback.

P-044 (conscious deltas, enumerated): ``negative_space_dropout`` is the
THIRD extended kind (tests/test_negative_space_dropout.py), and TIMBALAND
authors its reach on exactly ``experimental`` / ``dramatic_contrast`` /
``negative_space`` (the user's list — dramatic_contrast is his DEFAULT
mode: negative space IS his documented philosophy). His default-flow pin
therefore gains exactly the reached dropout ids
(TIMBALAND_DEFAULT_FLOW_IDS below) and his default artifacts carry the
reach surface — his committed sample tree drifted CONSCIOUSLY under the
full-strength staleness pin. halee_ramone still authors ZERO reach: her
pins and her committed tree stay byte-identical, and quincy's P-043 pins
are untouched.
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
from logic_mix_os.doctrine.producer_profile import (
    _PRODUCERS_DIR,
    _validate,
    load_profile,
)
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest
from logic_mix_os.renderers.creative_renderer import render_creative

from conftest import FIXTURE_NAMES, ROOT

_PACKAGE = ROOT / "logic_mix_os"

# P-047: the swept producers are DISCOVERED from the shipped producers
# directory — the product's own source of truth (``cli._resolve_producer``
# scans the same ``_PRODUCERS_DIR``; the private-name import is the accepted
# P-039 standing note) — in stable sorted order, so every current AND future
# profile is swept automatically. The membership guard below pins the four
# known names as a MINIMUM, never a maximum: a fifth producer grows every
# sweep passively instead of silently escaping it.
PRODUCERS = tuple(sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json")))
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
# pre-P-042 neutral emission, order included, for every producer WITHOUT an
# authored conscious delta (quincy's P-043 and timbaland's P-044 deltas are
# pinned separately below; halee_ramone and brian_eno author neutral
# default flows and ride this shared pin).
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

# P-043 CONSCIOUS DELTA — quincy_jones only: his default mode is literally
# NAMED ``arrangement_lift``, and under his arrangement-led philosophy the
# authored reach for the ``arrangement_lift`` family IS that mode's meaning
# ("each section earns its lift through parts entering and leaving"). His
# default flow therefore gains EXACTLY the reached arrangement_lift ids
# (appended after the neutral pool — reach admits, never reorders the
# original seven); his intimate path (space_for_the_singer, zero reach) and
# every other producer's default flow stay byte-identical to the shared pin
# above.
QUINCY_DEFAULT_FLOW_IDS = {
    "simple_vocal_piano_song": DEFAULT_FLOW_IDS["simple_vocal_piano_song"],
    "dense_chorus_with_loops": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D", "chorus_lift_E"],
        "density": ["density_A", "density_B", "density_C"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "splice_loop_problem": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D", "chorus_lift_E"],
        "loop": ["loop_A", "loop_B"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
}

# P-044 CONSCIOUS DELTA — timbaland only: ``dramatic_contrast`` is his
# DEFAULT mode and the user explicitly authorized dropout reach on it
# ("Timbaland: yes — experimental / contrast / negative-space modes"), so
# his default flow gains EXACTLY the reached ``negative_space_dropout`` ids
# where the extended pool holds them and the protection filter finds an
# unprotected target (appended after the neutral pool — reach admits, never
# reorders the original seven). His intimate path (``conservative``, zero
# reach) and every branch WINNER are unchanged — the drift is
# candidate-set-only (chorus_lift_B at 86.7 still outranks the dropout's
# honest 80.9 by his own curated margin).
TIMBALAND_DEFAULT_FLOW_IDS = {
    "simple_vocal_piano_song": DEFAULT_FLOW_IDS["simple_vocal_piano_song"],
    "dense_chorus_with_loops": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D", "chorus_lift_F"],
        "density": ["density_A", "density_B", "density_E"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "splice_loop_problem": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D", "chorus_lift_F"],
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


# P-043: the extended kinds' per-problem availability — which problems the
# engine's reach-gated curated pool addresses (the full (id, kind) pin lives
# in tests/test_move_vocabulary_expansion.py::EXTENDED_POOL; this is the
# kind-set view the reconstructive rule needs).
EXTENDED_POOL_KINDS = {
    # P-044: the dropout family joined the extended pool for chorus_lift +
    # density (its variants emit on the fixtures these suites run on — the
    # protection filter finds unprotected targets there; the filter proofs
    # live in tests/test_negative_space_dropout.py).
    "chorus_lift": {"arrangement_lift", "negative_space_dropout"},
    "density": {"arrangement_lift", "ensemble_rebalance",
                "negative_space_dropout"},
    "loop": set(),
    "depth": set(),
    "vocal_belief": {"ensemble_rebalance"},
}


def _expected_kind_set(pid: str, suppress_kinds, reach_kinds=()) -> set:
    """The reconstructive rule, P-043-extended: (ENGINE POOL ∪ the authored
    reach where the extended pool holds variants) minus the authored
    suppressions — with the engine's documented non-empty fallback (a
    fully-suppressed pool emits the full NEUTRAL pool, never the reach)."""
    pool = set(_pool_kinds(pid))
    reached = set(reach_kinds) & EXTENDED_POOL_KINDS[pid]
    expected = (pool | reached) - set(suppress_kinds)
    return expected if expected else pool


@pytest.fixture(scope="module")
def dense(analyzed):
    return analyzed[DENSE]


# =========================================================================== #
# P-047 — the sweep tuple is directory-driven; the known four are a MINIMUM.
# =========================================================================== #
def test_producer_sweep_is_directory_driven_with_the_known_minimum():
    """The sweep tuple IS the shipped producers directory, sorted and
    duplicate-free. The four known profiles are pinned as a CONTAINMENT
    minimum only — nothing here may block a fifth producer from growing
    every PRODUCERS-keyed sweep passively."""
    assert PRODUCERS == tuple(sorted(PRODUCERS))
    assert len(PRODUCERS) == len(set(PRODUCERS))
    assert {"brian_eno", "halee_ramone", "quincy_jones", "timbaland"} \
        <= set(PRODUCERS)


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
    variant-id lists — order included — on all three fixtures. For
    halee_ramone that is the pre-P-042 neutral emission, byte-identical
    (she authors zero reach); brian_eno's authored-neutral default flow
    (ambient_field / horizontal_time, P-045) rides the same shared pin.
    For quincy_jones it is the P-043 CONSCIOUS delta (his default mode's
    authored reach appends exactly the arrangement_lift ids —
    QUINCY_DEFAULT_FLOW_IDS); for timbaland the P-044 CONSCIOUS delta
    (his default mode's authored dropout reach appends exactly the
    negative_space_dropout ids — TIMBALAND_DEFAULT_FLOW_IDS)."""
    prof = load_profile(producer)
    expected_flow = {
        "quincy_jones": QUINCY_DEFAULT_FLOW_IDS,
        "timbaland": TIMBALAND_DEFAULT_FLOW_IDS,
    }.get(producer, DEFAULT_FLOW_IDS)
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        out = run_creative_engine(res, mode, profile=prof)
        emitted = {b["problem_id"]: _ids(b["variants"]) for b in out["branches"]}
        assert emitted == expected_flow[name], (producer, name)


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_shipped_profile_authors_the_fields_explicitly(producer):
    """Every shipped profile authors ``favor_kinds`` + ``suppress_kinds``
    EXPLICITLY on every mode (no silent inheritance for load-bearing
    choices); its default-flow modes (declared default + intimate) author
    them NEUTRAL — the requirement-8 construction, visible in the JSON
    itself; and at least one NON-default mode authors a NON-neutral reach,
    so the fork is real for every producer. (P-043: ``reach_kinds`` is the
    separate ADMISSION field — quincy's default mode consciously authors
    one while its favor/suppress stay neutral; that delta is pinned in
    QUINCY_DEFAULT_FLOW_IDS and tests/test_move_vocabulary_expansion.py.)"""
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
    """``conservative`` exists in all four shipped profiles: on the same
    stems and problem it emits FOUR pairwise-distinct candidate-id sets —
    Timbaland's authored-neutral full pool, Halee/Ramone's width-suppressed
    pool, Quincy's width-and-drum-room-suppressed pool, Eno's
    width-and-vocal-ride-suppressed pool. And on ``experimental``,
    Timbaland's authored ``intimacy_pass`` suppression splits the
    vocal_belief set from the others. Sets, not order or labels."""
    conservative = {}
    for producer in PRODUCERS:
        out = run_creative_engine(dense, "conservative", profile=load_profile(producer))
        conservative[producer] = set(_ids(_branch(out, "chorus_lift")["variants"]))
    assert conservative["timbaland"] == {
        "chorus_lift_A", "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert conservative["halee_ramone"] == {
        "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"}
    assert conservative["quincy_jones"] == {"chorus_lift_B", "chorus_lift_C"}
    # P-047 (the P-045 profile swept here): eno's conservative suppresses
    # width_bloom AND vocal_ride — a fourth authored reach, distinct from
    # all three others on the same stems.
    assert conservative["brian_eno"] == {"chorus_lift_B", "chorus_lift_D"}
    assert len({frozenset(s) for s in conservative.values()}) == 4  # pairwise distinct

    experimental = {}
    for producer in PRODUCERS:
        out = run_creative_engine(dense, "experimental", profile=load_profile(producer))
        experimental[producer] = set(_ids(_branch(out, "vocal_belief")["variants"]))
    assert experimental["timbaland"] == {"vocal_A"}
    assert experimental["halee_ramone"] == {"vocal_A", "vocal_B"}
    # P-043 conscious delta: quincy's experimental now REACHES for the real
    # ensemble_rebalance family (replacing the P-042 subtractive_drop +
    # width_bloom approximation), so his vocal_belief set gains vocal_C —
    # three pairwise-distinct sets on this branch too.
    assert experimental["quincy_jones"] == {"vocal_A", "vocal_B", "vocal_C"}
    # P-047: eno's experimental reaches ONLY the dropout family, and the
    # extended pool holds no dropout variant for vocal_belief — so his set
    # is the authored-neutral pool, coinciding with halee's (a DATA fact:
    # the distinct-set count over the four stays 3 on this branch).
    assert experimental["brian_eno"] == {"vocal_A", "vocal_B"}
    assert len({frozenset(s) for s in experimental.values()}) == 3


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_producers_every_mode_is_attributable_to_its_json(producer, dense):
    """The full reconstructive attribution (requirements 3 + 4 + 9), every
    discovered producer: for EVERY authored mode and EVERY problem, the
    emitted kind set equals (the shared ENGINE POOL ∪ THAT mode's authored
    ``reach_kinds`` where the extended pool holds variants) minus THAT
    producer's authored ``suppress_kinds`` — derived from the JSON on disk.
    Where two producers' declarations differ, their same-mode sets differ;
    where they are both neutral (``dramatic_contrast``), the sets agree —
    the difference is the DATA, never a code path."""
    prof = load_profile(producer)
    raw_modes = _raw(producer)["search_modes"]
    for mode_name, entry in raw_modes.items():
        for pid in PROBLEM_IDS:
            emitted = _kinds(generate_variants({"id": pid}, dense, mode_name, prof))
            assert emitted == _expected_kind_set(
                pid, entry["suppress_kinds"], entry.get("reach_kinds", ())), \
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
    actually suppressed/favored. P-044 (conscious): ``negative_space`` now
    also authors the dropout reach — the mode literally NAMED for the
    family — so the echo carries ``reach_kinds`` and the fork report the
    reach keys, verbatim from the JSON."""
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
        "reach_kinds": ["negative_space_dropout"],
    }

    chorus = _branch(cr, "chorus_lift")
    assert _kinds(chorus["variants"]) == _expected_kind_set(
        "chorus_lift", authored["suppress_kinds"], authored["reach_kinds"])
    assert set(authored["suppress_kinds"]) & _kinds(chorus["variants"]) == set()
    assert chorus["mode_fork"] == {
        "suppressed": ["width_bloom", "drum_room_bloom"],
        "favored": ["subtractive_drop"],
        "risk_capped": [],
        "suppression_fallback": False,
        "reached": ["negative_space_dropout"],
        "reach_capped": [],
    }
    # a branch the declarations don't touch still explains itself honestly
    vocal = _branch(cr, "vocal_belief")
    assert vocal["mode_fork"] == {
        "suppressed": [], "favored": [], "risk_capped": [],
        "suppression_fallback": False, "reached": [], "reach_capped": [],
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


# P-043: quincy's default mode consciously authors reach; P-044: timbaland's
# default mode does too (his committed tree drifted CONSCIOUSLY under the
# full-strength staleness pin — the drift surface is pinned in
# tests/test_negative_space_dropout.py). The zero-byte discipline is now the
# ZERO-REACH producer's guarantee: halee_ramone, whose committed reference
# tree stays byte-identical.
@pytest.mark.parametrize("producer", ("halee_ramone",))
def test_artifact_keys_absent_on_default_flows(producer, analyzed):
    """The evidence-key discipline (and the committed reference tree's byte
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
# P-048: "brian" covers the fourth producer (any branch on his profile-name
# string "brian_eno" contains it). A bare "eno" token is CONSCIOUSLY not
# includable under this guard's substring matching: the established curated
# plan prose in creative.py carries "enough" ("does not lift enough
# emotionally", "May not create enough scale"), which contains "eno".
_PRODUCER_TOKENS = ("timbaland", "quincy", "halee", "ramone", "brian")


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
