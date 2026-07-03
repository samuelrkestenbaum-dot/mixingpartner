"""P-043 — CURATED MOVE VOCABULARY EXPANSION (Shape C, narrow):
``arrangement_lift`` + ``ensemble_rebalance``.

The user's decision, verbatim authority: open Shape C but NARROWLY — exactly
these two families ("Start with the two that prove the new capability most
cleanly"); negative-space dropout is EXPLICITLY EXCLUDED. B proved the fork
seam; C widens the vocabulary just enough to make mode behavior genuinely
musical.

THE LOAD-BEARING DESIGN — REACH-GATED EMISSION: the two new kinds are
EXTENDED vocabulary. They never join the neutral emission pool. An extended
kind emits ONLY when the active mode's authored ``reach_kinds`` declaration
reaches for it:

* the ENGINE curates the families (which problems they address, their
  plan-only changes/validation text, their curated risk rows) — the
  ``_extended_variants`` pool, pinned here as EXTENDED_POOL;
* the PROFILE authors whether a mode reaches them (``reach_kinds``, a
  distinct declaration — P-042's ``favor_kinds`` stays ORDER-ONLY for the
  original seven, its "can never grow the set" guarantee intact);
* GOVERNANCE owns the cap: over-cap reach is a loud ValueError at load and
  a fail-closed refusal at runtime (``reach_capped``, the ``risk_capped``
  pattern);
* suppression beats reach; the non-empty fallback stays PROFILE-AGNOSTIC
  and NEUTRAL-POOL-ONLY (a fallback can never admit extended kinds);
* the artifact/renderer surface reports authored reach and what it actually
  added, under the evidence-key discipline (zero bytes when nothing is
  reached).

Curated risk rows exist EVERYWHERE: all three shipped profiles author
explicit ``kind_scores`` + ``truth_alignment`` rows for both new kinds even
where reach is absent — no silent inheritance. Halee/Timbaland authored
ZERO reach in P-043 (their "only if authored" gate is proven with
test-local synthetic profiles, never by touching their taste) — and they
STILL author zero reach over the two P-043 families.

P-044 (conscious extension, the user's explicit go): the vocabulary widened
by ONE more extended kind — ``negative_space_dropout``
(tests/test_negative_space_dropout.py carries its packet proof: the
structural protection filter, the plan-only guard, the honest rows, the
timbaland-only authored reach). The seam-level pins in THIS file extend to
the third kind: EXTENDED_POOL gains the dropout variants, and the P-043
"exactly two families / dropout excluded" pin is consciously lifted below.
"""

from __future__ import annotations

import dataclasses

import pytest

from logic_mix_os import pipeline
from logic_mix_os.constants import (
    CREATIVE_EXTENDED_KINDS,
    CREATIVE_VARIANT_KINDS,
    TRANSLATION_RISK_LEVELS,
)
from logic_mix_os.creative import (
    _curated_variants,
    _extended_variants,
    _fork_candidates,
    _mode_declarations,
    generate_variants,
    run_creative_engine,
    score_variant,
    winning_variant,
)
from logic_mix_os.doctrine.producer_profile import _validate, load_profile
from logic_mix_os.renderers.creative_renderer import render_creative

from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest

from conftest import FIXTURE_NAMES, ROOT
from test_mode_forking import (
    DENSE,
    ENGINE_POOL,
    PROBLEM_IDS,
    PRODUCERS,
    QUINCY_DEFAULT_FLOW_IDS,
    _branch,
    _ids,
    _kinds,
    _raw,
)

# The pre-P-043 engine vocabulary (the frozen neutral pool's seven kinds).
ORIGINAL_KINDS = (
    "width_bloom", "subtractive_drop", "vocal_ride", "drum_room_bloom",
    "loop_deconstruct", "depth_cleanup", "intimacy_pass",
)

# THE EXTENDED POOL — the engine's curated reach-gated emission per problem,
# (variant_id, kind) in curated order. The engine owns this content exactly
# as it owns ENGINE_POOL; the difference is the gate: these emit ONLY when
# the active mode's authored ``reach_kinds`` admit them.
EXTENDED_POOL = {
    "chorus_lift": [
        ("chorus_lift_E", "arrangement_lift"),
        # P-044: the dropout family (emits only where an unprotected target
        # survives its ENGINE-owned protection filter — true on the dense
        # fixture these pins run on; the filter proofs live in
        # tests/test_negative_space_dropout.py).
        ("chorus_lift_F", "negative_space_dropout"),
    ],
    "density": [
        ("density_C", "arrangement_lift"),
        ("density_D", "ensemble_rebalance"),
        ("density_E", "negative_space_dropout"),
    ],
    "loop": [],
    "depth": [],
    "vocal_belief": [("vocal_C", "ensemble_rebalance")],
}

# The three shipped profiles' authored curated rows for the extended kinds —
# the translation risks are load-bearing (the cap validates against them).
# P-044: dropout is the aggressive family — NEVER low (medium at minimum;
# halee authors HIGH under her translate-everywhere lens).
AUTHORED_TRANSLATION = {
    "halee_ramone": {"arrangement_lift": "low", "ensemble_rebalance": "low",
                     "negative_space_dropout": "high"},
    "timbaland": {"arrangement_lift": "low", "ensemble_rebalance": "medium",
                  "negative_space_dropout": "medium"},
    "quincy_jones": {"arrangement_lift": "low", "ensemble_rebalance": "low",
                     "negative_space_dropout": "medium"},
    # P-047 (the P-045 profile swept here): eno's honest rows — restraint
    # translates everywhere (lift low), the ensemble-in-layers move sits
    # against his field philosophy (medium), dropout medium like the other
    # dropout authors (never low — the P-044 honesty floor).
    "brian_eno": {"arrangement_lift": "low", "ensemble_rebalance": "medium",
                  "negative_space_dropout": "medium"},
}

# Each profile's honest curated overall for the new kinds (mean of the 7
# authored dims minus its own translation-risk penalty), reconstructed from
# the JSON in the scoring test and pinned here for the differential story.
AUTHORED_OVERALLS = {
    "halee_ramone": {"arrangement_lift": 83.3, "ensemble_rebalance": 80.6},
    "timbaland": {"arrangement_lift": 83.9, "ensemble_rebalance": 67.4},
    "quincy_jones": {"arrangement_lift": 85.3, "ensemble_rebalance": 83.1},
    # P-047: eno's curated overalls, reconstructed from his JSON exactly
    # like the other three (also pinned in tests/test_eno_profile.py).
    "brian_eno": {"arrangement_lift": 72.0, "ensemble_rebalance": 62.6},
}

_SCORE_DIMS = ("technical", "physical_space", "emotional_hierarchy",
               "contrast", "vocal_belief", "excitement", "taste")


@pytest.fixture(scope="module")
def dense(analyzed):
    return analyzed[DENSE]


def _mode(reach=(), suppress=(), favor=(), allowed="high",
          bias="test-local: P-043 reach"):
    """A test-local search-mode entry authoring the given declarations."""
    return {
        "allowed_risk": allowed,
        "bias": bias,
        "favor_kinds": list(favor),
        "suppress_kinds": list(suppress),
        "reach_kinds": list(reach),
    }


def _with_mode(base_producer: str, entry: dict, name: str = "reach"):
    """A synthetic profile: the shipped producer's judgment with ONE
    test-local mode — reach is DATA, so any producer can carry it."""
    return dataclasses.replace(load_profile(base_producer),
                               search_modes={name: entry})


def _fork(prof, mode, pid, dense):
    """Run the fork the way ``run_creative_engine`` derives its report."""
    return _fork_candidates(
        _curated_variants({"id": pid}, dense),
        _mode_declarations(prof, mode), prof,
        _extended_variants({"id": pid}, dense),
    )


# =========================================================================== #
# The widened vocabulary — the P-043 families plus the P-044 dropout kind.
# =========================================================================== #
def test_vocabulary_is_the_p043_families_plus_the_p044_dropout():
    """P-043 grew the vocabulary by EXACTLY ``arrangement_lift`` +
    ``ensemble_rebalance`` and EXPLICITLY excluded negative-space dropout
    until C proved the widened vocabulary stays governed. P-044 lifted that
    exclusion on the user's own go ("Then open negative-space dropout, but
    narrowly and conservatively"): ``negative_space_dropout`` is the third
    — and only other — extended kind. Nothing else entered."""
    assert CREATIVE_EXTENDED_KINDS == (
        "arrangement_lift", "ensemble_rebalance", "negative_space_dropout")
    assert set(CREATIVE_VARIANT_KINDS) \
        == set(ORIGINAL_KINDS) | set(CREATIVE_EXTENDED_KINDS)
    assert len(CREATIVE_VARIANT_KINDS) == 10


def test_extended_pool_is_the_pinned_curated_emission(dense):
    """The engine's extended curated emission per problem IS the pinned
    EXTENDED_POOL (ids, kinds AND order); its kind union IS the extended
    vocabulary; its ids are disjoint from the neutral pool's; and every
    entry keeps the house style — plan-only, non-destructive, real track
    targets, populated hypothesis/changes/validation."""
    real_names = {r["name"] for r in dense.records}
    neutral_ids = {vid for pool in ENGINE_POOL.values() for vid, _ in pool}
    union = set()
    for pid in PROBLEM_IDS:
        variants = _extended_variants({"id": pid}, dense)
        assert [(v["variant_id"], v["kind"]) for v in variants] \
            == EXTENDED_POOL[pid], pid
        for v in variants:
            union.add(v["kind"])
            assert v["variant_id"] not in neutral_ids
            assert v["reversibility"] == "non_destructive_duplicate_track"
            assert v["tracks_affected"], v["variant_id"]
            assert set(v["tracks_affected"]) <= real_names, v["variant_id"]
            assert v["creative_hypothesis"] and v["changes"] and v["validation"]
            assert v["risk"] and v["expected_strength"]
    assert union == set(CREATIVE_EXTENDED_KINDS)


# =========================================================================== #
# THE GATE — extended kinds NEVER appear in a neutral (un-reached) emission.
# =========================================================================== #
@pytest.mark.parametrize("producer", PRODUCERS)
def test_new_kinds_never_in_any_unreached_emission(producer, dense):
    """Every shipped mode WITHOUT authored reach (plus no-mode and an unknown
    mode) emits ZERO extended kinds on every problem — the neutral pool is
    untouched by the widening, whatever favor/suppress the mode authors.
    Data-driven from the JSON on disk, so this holds permanently: any mode
    that ever emits an extended kind must carry the authored reach."""
    prof = load_profile(producer)
    unreached = [m for m, entry in _raw(producer)["search_modes"].items()
                 if not entry.get("reach_kinds")]
    assert unreached, producer  # every producer keeps unreached modes
    for mode in unreached + [None, "no_such_mode"]:
        for pid in PROBLEM_IDS:
            emitted = _kinds(generate_variants({"id": pid}, dense, mode, prof))
            assert emitted & set(CREATIVE_EXTENDED_KINDS) == set(), \
                (producer, mode, pid)


def test_halee_authors_zero_reach_and_timbaland_only_the_p044_dropout():
    """The authored-reach boundary after P-044: halee_ramone still authors
    ``reach_kinds`` EXPLICITLY EMPTY on every mode (her gate is proven with
    synthetic profiles, never by touching her taste), and timbaland's ONLY
    reach is the P-044 dropout family on exactly the user's three modes —
    he still authors ZERO reach over the P-043 families
    (arrangement_lift / ensemble_rebalance), so every P-043 pin for him
    holds by authoring, not by accident. His full dropout-reach pin lives
    in tests/test_negative_space_dropout.py."""
    for mode_name, entry in _raw("halee_ramone")["search_modes"].items():
        assert entry.get("reach_kinds") == [], ("halee_ramone", mode_name)
    for mode_name, entry in _raw("timbaland")["search_modes"].items():
        reach = entry.get("reach_kinds")
        assert reach in ([], ["negative_space_dropout"]), \
            ("timbaland", mode_name)
        assert "arrangement_lift" not in reach, ("timbaland", mode_name)
        assert "ensemble_rebalance" not in reach, ("timbaland", mode_name)


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_mode_authors_reach_explicitly_and_rows_exist_everywhere(producer):
    """No silent inheritance, anywhere: every shipped mode authors
    ``reach_kinds`` explicitly (a list, valid under the loader); both new
    kinds carry FULL curated ``kind_scores`` rows (all 7 dims + honest
    translation/mono risks, pinned) and ``truth_alignment`` rows in all
    three leans — even where reach is absent."""
    raw = _raw(producer)
    _validate(raw, producer)  # the shipped JSON validates as authored
    for mode_name, entry in raw["search_modes"].items():
        assert isinstance(entry.get("reach_kinds"), list), (producer, mode_name)
    for kind in CREATIVE_EXTENDED_KINDS:
        row = raw["kind_scores"][kind]
        for dim in _SCORE_DIMS:
            assert isinstance(row[dim], int), (producer, kind, dim)
        assert row["translation"] == AUTHORED_TRANSLATION[producer][kind]
        assert row["mono"] in TRANSLATION_RISK_LEVELS
        for lean in ("intimate", "big", "neutral"):
            assert isinstance(raw["truth_alignment"][lean][kind], int), \
                (producer, kind, lean)


# =========================================================================== #
# REACH ADMITS — authored data, not producer identity.
# =========================================================================== #
@pytest.mark.parametrize("base", PRODUCERS)
def test_authored_reach_admits_the_extended_pool_on_any_producer(base, dense):
    """A synthetic profile built from EACH shipped producer's judgment with
    one test-local reaching mode emits neutral-pool + the reached extended
    variants (appended in authored reach order) on every problem — the gate
    is the DATA (``reach_kinds``), not the producer. The reverse control: the
    same profile with favor/suppress but NO reach never sees them."""
    reach_all = _with_mode(base, _mode(reach=CREATIVE_EXTENDED_KINDS))
    for pid in PROBLEM_IDS:
        neutral = generate_variants({"id": pid}, dense)
        emitted = generate_variants({"id": pid}, dense, "reach", reach_all)
        expected = [vid for vid, _ in ENGINE_POOL[pid]] \
            + [vid for vid, _ in EXTENDED_POOL[pid]]
        assert _ids(emitted) == expected, (base, pid)
        assert _ids(emitted)[:len(neutral)] == _ids(neutral), (base, pid)

    no_reach = _with_mode(base, _mode(favor=["vocal_ride"],
                                      suppress=["width_bloom"]))
    for pid in PROBLEM_IDS:
        emitted = _kinds(generate_variants({"id": pid}, dense, "reach", no_reach))
        assert emitted & set(CREATIVE_EXTENDED_KINDS) == set(), (base, pid)


def test_reach_order_is_authored_and_favor_can_front_reached_kinds(dense):
    """Reached variants append in AUTHORED reach order (curated order within
    a kind); ``favor_kinds`` keeps its P-042 order-shaping role and may
    front a reached kind — order only, never set growth."""
    ref = "halee_ramone"
    flipped = _with_mode(ref, _mode(reach=["ensemble_rebalance",
                                           "arrangement_lift"]))
    assert _ids(generate_variants({"id": "density"}, dense, "reach", flipped)) \
        == ["density_A", "density_B", "density_D", "density_C"]

    fronted = _with_mode(ref, _mode(reach=["ensemble_rebalance"],
                                    favor=["ensemble_rebalance"]))
    assert _ids(generate_variants({"id": "vocal_belief"}, dense, "reach", fronted)) \
        == ["vocal_C", "vocal_A", "vocal_B"]


def test_unknown_reach_kinds_are_inert_at_runtime(dense):
    """Runtime posture for loader-bypassing profiles (the P-042 ghost-kind
    discipline): a reach naming a kind with no extended curated variants
    admits nothing — the loader is the loud gate, the engine is
    inert-by-construction."""
    ghost = _with_mode("halee_ramone", _mode(reach=["not_a_kind"]))
    for pid in PROBLEM_IDS:
        assert generate_variants({"id": pid}, dense, "reach", ghost) \
            == generate_variants({"id": pid}, dense), pid


# =========================================================================== #
# SUPPRESSION BEATS REACH; the fallback stays neutral-pool-only.
# =========================================================================== #
def test_suppression_beats_reach_at_runtime(dense):
    """A loader-bypassing mode that reaches for AND suppresses the same kind
    (the loader rejects this authoring outright) emits the neutral pool: the
    admitted variants are removed again, the fork report shows the removal
    honestly, and nothing reads as reached."""
    prof = _with_mode("halee_ramone", _mode(reach=["arrangement_lift"],
                                            suppress=["arrangement_lift"]))
    emitted = generate_variants({"id": "chorus_lift"}, dense, "reach", prof)
    assert emitted == generate_variants({"id": "chorus_lift"}, dense)

    _, fork = _fork(prof, "reach", "chorus_lift", dense)
    assert fork["reached"] == []
    assert fork["suppressed"] == ["arrangement_lift"]
    assert fork["reach_capped"] == []
    assert fork["suppression_fallback"] is False


def test_reach_suppress_contradiction_fails_loudly_at_load():
    """The same contradiction at AUTHORING time is a load-time ValueError
    naming ``search_modes`` — never a judgment-time surprise."""
    raw = _raw("halee_ramone")
    raw["search_modes"]["experimental"]["reach_kinds"] = ["arrangement_lift"]
    raw["search_modes"]["experimental"]["suppress_kinds"] = ["arrangement_lift"]
    with pytest.raises(ValueError, match="search_modes"):
        _validate(raw, "halee_ramone")


def test_fallback_never_admits_extended_kinds(dense):
    """The non-empty guarantee stays PROFILE-AGNOSTIC and NEUTRAL-POOL-ONLY.
    A (loader-bypassing) mode suppressing the ENTIRE nine-kind vocabulary
    while reaching for both extended kinds: every problem falls back to its
    FULL NEUTRAL pool — never to neutral + reached — with the honest report
    (nothing suppressed, nothing reached)."""
    prof = _with_mode("halee_ramone", _mode(
        reach=CREATIVE_EXTENDED_KINDS,
        suppress=list(CREATIVE_VARIANT_KINDS),
    ))
    for pid in PROBLEM_IDS:
        emitted = generate_variants({"id": pid}, dense, "reach", prof)
        assert emitted == generate_variants({"id": pid}, dense), pid
        _, fork = _fork(prof, "reach", pid, dense)
        assert fork["suppression_fallback"] is True, pid
        assert fork["suppressed"] == [] and fork["reached"] == [], pid


def test_reached_variants_can_carry_an_emission_the_fallback_cannot(dense):
    """A LOADER-LEGAL mode suppressing all SEVEN neutral kinds while reaching
    for both extended kinds: where the extended pool has entries the reached
    variants carry the emission alone (the set never emptied — no fallback);
    where it has none the neutral fallback fires — and stays neutral-only."""
    prof = _with_mode("halee_ramone", _mode(
        reach=CREATIVE_EXTENDED_KINDS, suppress=list(ORIGINAL_KINDS),
    ))
    for pid in PROBLEM_IDS:
        emitted = generate_variants({"id": pid}, dense, "reach", prof)
        _, fork = _fork(prof, "reach", pid, dense)
        if EXTENDED_POOL[pid]:
            assert _ids(emitted) == [vid for vid, _ in EXTENDED_POOL[pid]], pid
            assert fork["suppression_fallback"] is False, pid
            assert fork["reached"] == [k for k in CREATIVE_EXTENDED_KINDS
                                       if k in _kinds(emitted)], pid
        else:
            assert _ids(emitted) == [vid for vid, _ in ENGINE_POOL[pid]], pid
            assert fork["suppression_fallback"] is True, pid
            assert fork["reached"] == [], pid


# =========================================================================== #
# GOVERNANCE OWNS THE CAP — over-cap reach refused at load AND runtime.
# =========================================================================== #
def test_reach_cap_binds_at_load():
    """Authoring a reach whose curated translation risk ranks beyond the
    mode's ``allowed_risk`` is a LOUD load-time ValueError (timbaland's
    honest ``ensemble_rebalance: medium`` row under his low-posture
    ``groove_pocket``). Controls prove it is the RISK that is refused, not
    the mechanism: the low-risk ``arrangement_lift`` reach validates on the
    same low mode, and the same ``ensemble_rebalance`` reach validates on a
    medium mode."""
    raw = _raw("timbaland")
    raw["search_modes"]["groove_pocket"]["reach_kinds"] = ["ensemble_rebalance"]
    with pytest.raises(ValueError, match="cannot be out-authored"):
        _validate(raw, "timbaland")

    control_kind = _raw("timbaland")
    control_kind["search_modes"]["groove_pocket"]["reach_kinds"] = ["arrangement_lift"]
    _validate(control_kind, "timbaland")

    control_mode = _raw("timbaland")
    control_mode["search_modes"]["negative_space"]["reach_kinds"] = ["ensemble_rebalance"]
    _validate(control_mode, "timbaland")


def test_reach_cap_binds_at_runtime_fail_closed(dense):
    """The same cap at emission for loader-bypassing profiles: a low-posture
    mode reaching timbaland's medium-risk ``ensemble_rebalance`` is REFUSED
    — the emission is byte-identical to neutral and the refusal is surfaced
    in ``reach_capped`` (nothing reads as reached). The medium-posture
    control admits it, so the refusal is the CAP."""
    capped = _with_mode("timbaland", _mode(reach=["ensemble_rebalance"],
                                           allowed="low"))
    for pid in PROBLEM_IDS:
        assert generate_variants({"id": pid}, dense, "reach", capped) \
            == generate_variants({"id": pid}, dense), pid
    _, fork = _fork(capped, "reach", "vocal_belief", dense)
    assert fork["reach_capped"] == ["ensemble_rebalance"]
    assert fork["reached"] == []

    control = _with_mode("timbaland", _mode(reach=["ensemble_rebalance"],
                                            allowed="medium"))
    emitted = generate_variants({"id": "vocal_belief"}, dense, "reach", control)
    assert _ids(emitted) == ["vocal_A", "vocal_B", "vocal_C"]


def test_reach_without_allowed_risk_fails_closed(dense):
    """A declaring-by-reach mode without a recognized ``allowed_risk`` (only
    reachable by bypassing the loader) is capped at the MOST restrictive
    posture: timbaland's medium-risk ``ensemble_rebalance`` reach is refused
    — fail closed, never open."""
    prof = dataclasses.replace(load_profile("timbaland"), search_modes={
        "reach": {"bias": "test-local: no allowed_risk authored",
                  "reach_kinds": ["ensemble_rebalance"]},
    })
    decl = _mode_declarations(prof, "reach")
    assert decl is not None  # reach ALONE marks the mode as declaring
    assert decl["allowed_risk"] == TRANSLATION_RISK_LEVELS[0]
    assert generate_variants({"id": "vocal_belief"}, dense, "reach", prof) \
        == generate_variants({"id": "vocal_belief"}, dense)


def test_reach_declaration_validation_fails_loudly():
    """Every malformed ``reach_kinds`` shape is a load-time ValueError naming
    ``search_modes``: non-list, non-string member, unknown kind, a NEUTRAL
    kind (reach admits ONLY the extended vocabulary — the neutral pool needs
    no reach), duplicates, and a reach-declaring mode without
    ``allowed_risk``. Control first: authoring a legal reach validates."""
    legal = _raw("halee_ramone")
    legal["search_modes"]["experimental"]["reach_kinds"] = ["arrangement_lift"]
    _validate(legal, "halee_ramone")

    def broken(**edit):
        raw = _raw("halee_ramone")
        raw["search_modes"]["experimental"].update(edit)
        return raw

    for bad in (
        broken(reach_kinds="arrangement_lift"),                    # not a list
        broken(reach_kinds=["arrangement_lift", 3]),               # non-str member
        broken(reach_kinds=["no_such_kind"]),                      # outside the vocabulary
        broken(reach_kinds=["width_bloom"]),                       # NEUTRAL kind — not reachable
        broken(reach_kinds=["subtractive_drop"]),                  # NEUTRAL kind — not reachable
        broken(reach_kinds=["arrangement_lift", "arrangement_lift"]),  # duplicate
    ):
        with pytest.raises(ValueError, match="search_modes"):
            _validate(bad, "halee_ramone")

    # reach ALONE makes a mode declaring: it must carry allowed_risk.
    raw = _raw("halee_ramone")
    raw["search_modes"]["only_reach"] = {
        "bias": "test-local: reach without allowed_risk",
        "reach_kinds": ["arrangement_lift"],
    }
    with pytest.raises(ValueError, match="allowed_risk"):
        _validate(raw, "halee_ramone")


# =========================================================================== #
# SCORING through the REAL chain — honest rows, no KeyError, honest winners.
# =========================================================================== #
@pytest.mark.parametrize("producer", PRODUCERS)
def test_new_kinds_score_through_the_real_chain(producer, dense):
    """``score_variant`` consumes each profile's authored rows for the new
    kinds with NO missing-row fallback: the overall reconstructs from the
    JSON on disk (mean of the 7 authored dims minus the profile's own
    translation-risk penalty) and equals the pinned per-producer value —
    three producers, three honest judgments of the same two families. No
    nudge/promotion row names them, so ``score_nudges`` stays absent."""
    prof = load_profile(producer)
    raw = _raw(producer)
    reach_all = _with_mode(producer, _mode(reach=CREATIVE_EXTENDED_KINDS))
    for pid, vid, kind in (("chorus_lift", "chorus_lift_E", "arrangement_lift"),
                           ("vocal_belief", "vocal_C", "ensemble_rebalance")):
        variants = generate_variants({"id": pid}, dense, "reach", reach_all)
        variant = next(v for v in variants if v["variant_id"] == vid)
        scores = score_variant(variant, dense, prof)
        row = raw["kind_scores"][kind]
        expected = round(sum(row[d] for d in _SCORE_DIMS) / 7
                         - raw["risk_penalty"][row["translation"]], 1)
        assert scores["overall_score"] == expected, (producer, kind)
        assert scores["overall_score"] == AUTHORED_OVERALLS[producer][kind]
        assert scores["translation_risk"] == row["translation"]
        assert scores["mono_compatibility"] == row["mono"]
        assert "score_nudges" not in scores, (producer, kind)


def test_winning_variant_ranks_a_reached_emission_honestly(dense):
    """``winning_variant`` over a REACHED emission works end to end. Under a
    synthetic reach on the quincy_jones judgment the ensemble lens is worth
    the win: ``vocal_C`` (83.1) outranks the neutral pool's phrase rides —
    while the same reached emission under halee_ramone keeps ``vocal_A`` on
    top (her vocal lens outranks the ensemble move). Same engine, same
    stems: the DATA decides."""
    outcomes = {"quincy_jones": "vocal_C", "halee_ramone": "vocal_A"}
    for producer, expected_winner in outcomes.items():
        prof = load_profile(producer)
        reach = _with_mode(producer, _mode(reach=["ensemble_rebalance"]))
        variants = generate_variants({"id": "vocal_belief"}, dense, "reach", reach)
        assert _ids(variants) == ["vocal_A", "vocal_B", "vocal_C"]
        for v in variants:
            v["scores"] = score_variant(v, dense, prof)
        win = winning_variant(variants)
        assert win["winning_variant"] == expected_winner, producer


# =========================================================================== #
# Requirement-10 explainability — artifact + renderer surface for reach.
# =========================================================================== #
def test_artifact_surfaces_authored_reach_and_what_it_added(dense):
    """A reaching run's artifact explains itself: the declarations echo
    carries ``reach_kinds`` verbatim; each branch's ``mode_fork`` reports
    what was ACTUALLY reached for this emission (authored-order kinds where
    the extended pool held variants, [] where it held none)."""
    prof = _with_mode("halee_ramone", _mode(reach=CREATIVE_EXTENDED_KINDS))
    out = run_creative_engine(dense, "reach", profile=prof)
    assert out["search_mode_declarations"] == {
        "allowed_risk": "high",
        "favor_kinds": [],
        "suppress_kinds": [],
        "reach_kinds": list(CREATIVE_EXTENDED_KINDS),
    }
    expected_reached = {
        "chorus_lift": ["arrangement_lift", "negative_space_dropout"],
        "density": ["arrangement_lift", "ensemble_rebalance",
                    "negative_space_dropout"],
        "loop": [],
        "depth": [],
        "vocal_belief": ["ensemble_rebalance"],
    }
    for b in out["branches"]:
        assert b["mode_fork"]["reached"] == expected_reached[b["problem_id"]]
        assert b["mode_fork"]["reach_capped"] == []


def test_reach_keys_absent_when_no_reach_is_authored(dense):
    """The evidence-key discipline, byte-level: a forking-but-not-reaching
    mode (the reference's ``deconstructive``) carries NEITHER reach key —
    the P-042 artifact stays byte-identical; the zero-reach producer's
    default flow carries no fork surface at all; and timbaland's INTIMATE
    path (``conservative``, zero authored reach) stays byte-silent even
    though his DEFAULT mode now reaches (the P-044 conscious drift — its
    surface is pinned in tests/test_negative_space_dropout.py)."""
    ref = load_profile("halee_ramone")
    out = run_creative_engine(dense, "deconstructive", profile=ref)
    assert "reach_kinds" not in out["search_mode_declarations"]
    for b in out["branches"]:
        assert "reached" not in b["mode_fork"], b["problem_id"]
        assert "reach_capped" not in b["mode_fork"], b["problem_id"]

    ref_mode = pipeline._default_creative_mode({}, ref)
    neutral = run_creative_engine(dense, ref_mode, profile=ref)
    assert "search_mode_declarations" not in neutral
    for b in neutral["branches"]:
        assert "mode_fork" not in b, b["problem_id"]

    tim = load_profile("timbaland")
    intimate = run_creative_engine(
        dense, tim.default_creative_mode["intimate_mode"], profile=tim)
    assert "search_mode_declarations" not in intimate
    for b in intimate["branches"]:
        assert "mode_fork" not in b, b["problem_id"]


def test_renderer_explains_reach_and_stays_silent_without_it(dense):
    """Requirement 10 at the RENDERER: a reaching run renders the authored
    reach in the mode-reach line and the per-branch reached kinds; the cap
    refusal renders when it fires; a run without authored reach renders
    ZERO reach bytes."""
    prof = _with_mode("halee_ramone", _mode(reach=CREATIVE_EXTENDED_KINDS))
    md = render_creative(run_creative_engine(dense, "reach", profile=prof))
    assert ("reaches for `arrangement_lift`, `ensemble_rebalance`, "
            "`negative_space_dropout`") in md
    assert "_Mode fork: reached for `arrangement_lift`, `negative_space_dropout`._" in md
    assert ("reached for `arrangement_lift`, `ensemble_rebalance`, "
            "`negative_space_dropout`") in md

    capped = _with_mode("timbaland", _mode(reach=["ensemble_rebalance"],
                                           allowed="low"))
    md_cap = render_creative(run_creative_engine(dense, "reach", profile=capped))
    assert "reach refused by the allowed-risk cap: `ensemble_rebalance`" in md_cap
    assert "reached for" not in md_cap

    ref = load_profile("halee_ramone")
    md_fork = render_creative(run_creative_engine(dense, "deconstructive", profile=ref))
    assert "reaches for" not in md_fork and "reached for" not in md_fork
    md_neutral = render_creative(run_creative_engine(dense, "dramatic_contrast", profile=ref))
    assert "Mode reach" not in md_neutral and "reached for" not in md_neutral


# =========================================================================== #
# THE SHIPPED DIFFERENTIAL — Quincy authors real reach; the other two do not.
# =========================================================================== #
# Quincy's authored reach, pinned per mode (the packet's decision, from his
# arrangement-led philosophy):
# * ``arrangement_lift`` — his DEFAULT mode, literally NAMED after the
#   family: "sectional entrances and exits, build the lift through the
#   arrangement" IS the arrangement_lift move — reach is the mode's meaning.
#   The default-flow drift this causes is the packet's conscious, enumerated
#   delta (QUINCY_DEFAULT_FLOW_IDS in test_mode_forking.py).
# * ``ensemble_balance`` — "the ensemble in layers around the lead" IS the
#   ensemble_rebalance move; his curated low translation risk clears the
#   mode's low posture, so the cap PROVABLY allowed this authoring.
# * ``experimental`` — carried the P-042 subtractive_drop + width_bloom
#   APPROXIMATION of these families; the approximation is REPLACED by the
#   real thing (reached AND favored to the front).
QUINCY_REACH = {
    "conservative": [],
    "ensemble_balance": ["ensemble_rebalance"],
    "space_for_the_singer": [],
    "arrangement_lift": ["arrangement_lift"],
    "orchestral_depth": [],
    "experimental": ["arrangement_lift", "ensemble_rebalance"],
}

EXTENDED_IDS = {vid for pool in EXTENDED_POOL.values() for vid, _ in pool}

EXTENDED_KINDS_BY_PROBLEM = {
    pid: {kind for _, kind in EXTENDED_POOL[pid]} for pid in PROBLEM_IDS
}


def test_quincy_authors_the_pinned_reach_and_it_validates():
    """Quincy's ``reach_kinds`` per mode IS the pinned authoring; his
    experimental favor no longer carries the in-vocabulary approximation;
    and the shipped JSON passes the full loader validation — the authored
    reach lives INSIDE the governance cap."""
    raw = _raw("quincy_jones")
    reach = {m: e["reach_kinds"] for m, e in raw["search_modes"].items()}
    assert reach == QUINCY_REACH
    exp = raw["search_modes"]["experimental"]
    assert exp["favor_kinds"] == ["arrangement_lift", "ensemble_rebalance"]
    assert "subtractive_drop" not in exp["favor_kinds"]
    assert "width_bloom" not in exp["favor_kinds"]
    _validate(raw, "quincy_jones")


def test_same_mode_same_stems_each_producer_emits_only_its_authored_reach(dense):
    """THE HEADLINE DIFFERENTIAL, P-044-extended: ``experimental`` exists in
    all three profiles. Same mode name, same stems, THREE different
    reaches: quincy_jones emits the P-043 families (reached AND favored to
    the front of each touched branch) and ZERO dropout ids; timbaland
    (P-044) emits the dropout ids and ZERO P-043-family ids; halee_ramone
    emits ZERO extended ids of any kind. Each gate holds because of what
    was and was not AUTHORED — never a code path."""
    emitted = {}
    for producer in PRODUCERS:
        out = run_creative_engine(dense, "experimental",
                                  profile=load_profile(producer))
        emitted[producer] = {b["problem_id"]: _ids(b["variants"])
                             for b in out["branches"]}
    q = emitted["quincy_jones"]
    assert q["chorus_lift"] == ["chorus_lift_E", "chorus_lift_A",
                                "chorus_lift_B", "chorus_lift_C", "chorus_lift_D"]
    assert q["density"] == ["density_C", "density_D", "density_A", "density_B"]
    assert q["vocal_belief"] == ["vocal_C", "vocal_A", "vocal_B"]
    assert q["loop"] == ["loop_A", "loop_B"]
    assert q["depth"] == ["depth_A"]
    dropout_ids = {"chorus_lift_F", "density_E"}
    for pid, ids in q.items():
        assert not set(ids) & dropout_ids, ("quincy_jones", pid)

    # timbaland: his authored favor fronts subtractive_drop, his P-044 reach
    # appends the dropout variants, his intimacy_pass suppression holds —
    # and no P-043-family id appears (he never authored that reach).
    t = emitted["timbaland"]
    assert t["chorus_lift"] == ["chorus_lift_B", "chorus_lift_A",
                                "chorus_lift_C", "chorus_lift_D", "chorus_lift_F"]
    assert t["density"] == ["density_B", "density_A", "density_E"]
    assert t["loop"] == ["loop_B", "loop_A"]
    assert t["depth"] == ["depth_A"]
    assert t["vocal_belief"] == ["vocal_A"]
    for pid, ids in t.items():
        assert not set(ids) & (EXTENDED_IDS - dropout_ids), ("timbaland", pid)

    # brian_eno (P-045, swept here since P-047): his experimental favors
    # subtractive_drop + depth_cleanup to the front, suppresses
    # drum_room_bloom, and reaches ONLY the dropout family — the dropout
    # ids append where the curated pool holds them and ZERO P-043-family
    # ids appear anywhere (he never authored that reach).
    e = emitted["brian_eno"]
    assert e["chorus_lift"] == ["chorus_lift_B", "chorus_lift_A",
                                "chorus_lift_C", "chorus_lift_F"]
    assert e["density"] == ["density_B", "density_A", "density_E"]
    assert e["loop"] == ["loop_B", "loop_A"]
    assert e["depth"] == ["depth_A"]
    assert e["vocal_belief"] == ["vocal_A", "vocal_B"]
    for pid, ids in e.items():
        assert not set(ids) & (EXTENDED_IDS - dropout_ids), ("brian_eno", pid)

    for pid, ids in emitted["halee_ramone"].items():
        assert not set(ids) & EXTENDED_IDS, ("halee_ramone", pid)


@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_shipped_mode_reconstructs_with_the_reach_rule(producer, dense):
    """The B-pattern attribution, P-043-extended, from the JSONs on disk:
    for EVERY authored mode and EVERY problem the emitted kind set equals
    (ENGINE POOL ∪ (authored reach ∩ the extended pool's kinds for that
    problem)) − authored suppressions, with the neutral-only fallback — so
    a code path that emitted extended kinds without reading the authored
    reach (or vice versa) cannot pass."""
    prof = load_profile(producer)
    for mode_name, entry in _raw(producer)["search_modes"].items():
        for pid in PROBLEM_IDS:
            pool = {kind for _, kind in ENGINE_POOL[pid]}
            reached = set(entry["reach_kinds"]) & EXTENDED_KINDS_BY_PROBLEM[pid]
            expected = (pool | reached) - set(entry["suppress_kinds"])
            if not expected:
                expected = pool
            emitted = _kinds(generate_variants({"id": pid}, dense, mode_name, prof))
            assert emitted == expected, (producer, mode_name, pid)


def test_quincy_experimental_through_the_full_real_chain():
    """``analyze(producer="quincy_jones", creative_mode="experimental")`` —
    the same chain the CLI drives: the artifact echoes the authored reach
    verbatim, every touched branch reports what the reach actually added,
    the extended variants carry their honest curated scores, the ensemble
    lens WINS the vocal_belief branch (creative + governed), and governance
    governed the widened sets end to end."""
    manifest = load_manifest(ROOT / "fixtures" / DENSE / "project_manifest.json")
    res = analyze(str(ROOT / "fixtures" / DENSE / "stems"), manifest,
                  producer="quincy_jones", creative_mode="experimental")
    cr = res.creative
    authored = _raw("quincy_jones")["search_modes"]["experimental"]

    assert cr["search_mode"] == "experimental"
    assert cr["search_mode_declarations"] == {
        "allowed_risk": authored["allowed_risk"],
        "favor_kinds": authored["favor_kinds"],
        "suppress_kinds": authored["suppress_kinds"],
        "reach_kinds": authored["reach_kinds"],
    }
    assert _branch(cr, "chorus_lift")["mode_fork"] == {
        "suppressed": [], "favored": ["arrangement_lift"], "risk_capped": [],
        "suppression_fallback": False,
        "reached": ["arrangement_lift"], "reach_capped": [],
    }
    assert _branch(cr, "density")["mode_fork"]["reached"] \
        == ["arrangement_lift", "ensemble_rebalance"]
    assert _branch(cr, "loop")["mode_fork"] == {
        "suppressed": [], "favored": [], "risk_capped": [],
        "suppression_fallback": False, "reached": [], "reach_capped": [],
    }

    vocal = _branch(cr, "vocal_belief")
    assert vocal["mode_fork"]["reached"] == ["ensemble_rebalance"]
    vocal_c = next(v for v in vocal["variants"] if v["variant_id"] == "vocal_C")
    assert vocal_c["scores"]["overall_score"] \
        == AUTHORED_OVERALLS["quincy_jones"]["ensemble_rebalance"]
    assert vocal["winning"]["winning_variant"] == "vocal_C"

    governed = {b["problem_id"]: b["governed_winner"]
                for b in res.governance["governed_branches"]}
    assert governed["vocal_belief"] == "vocal_C"

    md = render_creative(cr)
    assert "reaches for `arrangement_lift`, `ensemble_rebalance`" in md
    assert "_Mode fork: favored `arrangement_lift`; reached for `arrangement_lift`._" in md


def test_quincy_default_flow_drift_is_conscious_and_bounded(analyzed):
    """THE DEFAULT-MODE DECISION, proven at its blast radius: quincy's
    intimate path (space_for_the_singer, zero reach) stays byte-neutral —
    no declaration surface at all; his default path (the mode literally
    named ``arrangement_lift``) emits the pinned QUINCY_DEFAULT_FLOW_IDS,
    reports exactly the arrangement_lift reach on the branches the extended
    pool touches, and the branch WINNERS are unmoved — his economy
    (subtractive_drop, 85.6) still outranks the lift (85.3) by his own
    honest curated margin, so the drift is candidate-set-only."""
    prof = load_profile("quincy_jones")
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        out = run_creative_engine(res, mode, profile=prof)
        emitted = {b["problem_id"]: _ids(b["variants"]) for b in out["branches"]}
        assert emitted == QUINCY_DEFAULT_FLOW_IDS[name], name

        if mode == "space_for_the_singer":  # the intimate path: zero reach
            assert "search_mode_declarations" not in out, name
            for b in out["branches"]:
                assert "mode_fork" not in b, (name, b["problem_id"])
            continue
        assert mode == "arrangement_lift", name
        assert out["search_mode_declarations"] == {
            "allowed_risk": "medium", "favor_kinds": [], "suppress_kinds": [],
            "reach_kinds": ["arrangement_lift"],
        }
        for b in out["branches"]:
            expected = (["arrangement_lift"]
                        if b["problem_id"] in ("chorus_lift", "density") else [])
            assert b["mode_fork"]["reached"] == expected, (name, b["problem_id"])
            assert b["mode_fork"]["reach_capped"] == [], (name, b["problem_id"])
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in out["branches"]}
        assert winners["chorus_lift"] == "chorus_lift_B", name
        if "density" in winners:
            assert winners["density"] == "density_B", name
