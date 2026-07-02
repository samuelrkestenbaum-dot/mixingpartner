"""P-033 — wire ``pipeline._default_creative_mode`` to the producer profile:
the authored ``default_creative_mode`` table becomes a REAL product lever.

Before this packet the table was REQUIRED (P-025) and authored by BOTH
profiles but pipeline-inert: ``_default_creative_mode`` hardcoded the
reference's mode names, so timbaland's authored ``intimate_mode:
"conservative"`` was unreachable and ``run_creative_engine`` substituted a
hardcoded ``"dramatic_contrast"`` (a KeyError for any profile without that
mode name). Five binding guards:

1. **BYTE-IDENTICAL (reference)** — the reference profile's authored table
   coincides string-for-string with the map the pipeline used to hardcode
   (pinned verbatim), so the reference resolves identically: the resolved
   mode per fixture is pinned by name, the doctrine overalls hold
   (73.8 / 70.7 / 74.3), the full creative surface equals the base capture,
   and NO fallback evidence appears on any real fixture under either
   producer.
2. **LIVENESS (the P-016 lesson — end-to-end)** — a REAL
   ``analyze(producer="timbaland")`` on the intimate-truth fixture selects
   timbaland's AUTHORED ``"conservative"`` (mode + bias), not a substitute.
   Re-hardcoding the map (or dropping the profile read) makes the resolved
   mode land back on the ``dramatic_contrast`` substitute and FAILS here
   while the reference guards stay green.
3. **FALLBACK SAFETY** — a profile whose table maps to a missing mode name,
   and a profile whose ``search_modes`` lacks ``"dramatic_contrast"``
   entirely (the exact crash scenario of the old hardcoded substitute),
   resolve deterministically through the profile's OWN tables with the
   substitution surfaced observationally — no KeyError anywhere.
4. **PER-CALL THREADING** — the PASSED profile's table is consulted, never
   the module default's (fails if the profile is accepted but ignored).
5. **NO-ALIASING** — the module ``_DEFAULT_PROFILE``s (pipeline's included,
   new in this packet) are untouched after interleaved runs.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os import creative, pipeline
from logic_mix_os.creative import run_creative_engine
from logic_mix_os.doctrine.producer_profile import load_profile
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest
from logic_mix_os.renderers.creative_renderer import render_creative

from conftest import FIXTURE_NAMES, ROOT
from test_protect_iconic_loops import BASE_CREATIVE_SURFACE

# The truth->mode map the pipeline hardcoded before P-033, pinned VERBATIM.
# The reference profile's authored table must equal it string-for-string —
# that coincidence is WHY the reference path is byte-identical by
# construction (and why the inertness was invisible until P-032h).
OLD_HARDCODED_MAP = {
    "intimate_truth_words": [
        "intimate", "vulnerable", "conflicted", "ache",
        "quiet", "restrained", "composed",
    ],
    "intimate_mode": "ramone_vocal_truth",
    "default_mode": "dramatic_contrast",
}

# The reference's resolved mode per fixture — identical pre/post wiring.
# P-038 renamed the reference's producer-named mode values off the producer
# names (ramone_vocal_truth -> vocal_truth); the resolution path is unchanged.
REFERENCE_RESOLVED_MODES = {
    "simple_vocal_piano_song": "vocal_truth",
    "dense_chorus_with_loops": "dramatic_contrast",
    "splice_loop_problem": "dramatic_contrast",
}

# Timbaland's resolved mode per fixture — its OWN authored table values,
# reachable end to end for the first time in this packet. Only the intimate
# fixture moves (dramatic_contrast -> the authored intimate_mode); the two
# non-intimate fixtures resolve to timbaland's authored default_mode, which
# is the same name the old substitute happened to land on.
TIMBALAND_RESOLVED_MODES = {
    "simple_vocal_piano_song": "conservative",
    "dense_chorus_with_loops": "dramatic_contrast",
    "splice_loop_problem": "dramatic_contrast",
}

REFERENCE_OVERALLS = {
    "simple_vocal_piano_song": 73.8,
    "dense_chorus_with_loops": 70.7,
    "splice_loop_problem": 74.3,
}


def _analyze(name: str, **kw):
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    return analyze(str(ROOT / "fixtures" / name / "stems"), manifest, **kw)


@pytest.fixture(scope="module")
def tim_analyzed():
    """The full pipeline once per fixture with ``producer="timbaland"``."""
    return {name: _analyze(name, producer="timbaland") for name in FIXTURE_NAMES}


# =========================================================================== #
# 1. BYTE-IDENTICAL (reference) — prove the coincidence, then the surfaces.
# =========================================================================== #
def test_reference_table_coincides_with_the_old_hardcoded_map():
    """The reference's authored ``default_creative_mode`` equals the map the
    pipeline used to hardcode, string for string — the construction that
    kept the reference path byte-identical across the P-033 wiring.

    P-038 (conscious flip): the reference renamed its producer-named mode
    values (``ramone_vocal_truth`` -> ``vocal_truth``), so the coincidence
    now holds modulo exactly that one rename — pinned explicitly so the
    historical map stays verbatim and the rename stays visible."""
    assert load_profile("halee_ramone").default_creative_mode == dict(
        OLD_HARDCODED_MAP, intimate_mode="vocal_truth"
    )


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_reference_resolved_mode_identical_pre_post(name, analyzed):
    """The reference's resolved mode per fixture, pinned by name (the pre-
    wiring values, captured at the packet base): the end-to-end surface AND
    the function itself — no-profile (module default) and explicit-reference
    calls all agree."""
    res = analyzed[name]
    expected = REFERENCE_RESOLVED_MODES[name]
    assert res.creative["search_mode"] == expected
    assert pipeline._default_creative_mode(res.project.intent) == expected
    assert pipeline._default_creative_mode(
        res.project.intent, load_profile("halee_ramone")
    ) == expected


def test_reference_surfaces_unchanged(analyzed):
    """Doctrine + creative surfaces on the reference path still equal the
    pinned base captures (overalls 73.8 / 70.7 / 74.3; every branch winner,
    every variant kind + overall + fired nudges), and no fallback evidence
    appears anywhere."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        assert ds["overall_mix_readiness_score"] == REFERENCE_OVERALLS[name]

        cr = analyzed[name].creative
        pinned = BASE_CREATIVE_SURFACE[name]
        assert cr["search_mode"] == pinned["search_mode"]
        assert "search_mode_fallback" not in cr
        assert [b["problem_id"] for b in cr["branches"]] == list(pinned["branches"])
        for b in cr["branches"]:
            winner, variants = pinned["branches"][b["problem_id"]]
            assert b["winning"]["winning_variant"] == winner, (name, b["problem_id"])
            for v, (vid, kind, overall, nudges) in zip(b["variants"], variants):
                assert v["variant_id"] == vid
                assert v["kind"] == kind
                assert v["scores"]["overall_score"] == pytest.approx(overall, abs=1e-9)
                assert v["scores"].get("score_nudges") == nudges, (name, vid)


def test_no_fallback_evidence_on_any_real_fixture(analyzed, tim_analyzed):
    """Both shipped profiles author complete tables (every mapped mode name
    exists in their own ``search_modes``), so the fallback key appears on NO
    real fixture under EITHER producer — the artifact surfaces carry zero new
    bytes outside the intimate-fixture mode itself."""
    for results in (analyzed, tim_analyzed):
        for name in FIXTURE_NAMES:
            assert "search_mode_fallback" not in results[name].creative, name


# =========================================================================== #
# 2. LIVENESS — the authored intimate mode, reachable END TO END.
# =========================================================================== #
def test_intimate_truth_selects_timbalands_authored_mode_end_to_end(tim_analyzed):
    """THE PACKET'S PAYOFF: the REAL ``analyze(producer="timbaland")`` on the
    intimate-truth fixture resolves to timbaland's AUTHORED
    ``intimate_mode`` — mode name AND its authored bias — with no fallback.
    Re-hardcoding the truth->mode map (or dropping the profile read at the
    ``analyze`` call site) resolves the REFERENCE's intimate mode
    ("vocal_truth" — "ramone_vocal_truth" before the P-038 rename), which
    timbaland does not carry, lands on the substitute instead, and FAILS
    here."""
    tim = load_profile("timbaland")
    authored = tim.default_creative_mode["intimate_mode"]
    assert authored == "conservative"

    cr = tim_analyzed["simple_vocal_piano_song"].creative
    assert cr["search_mode"] == authored
    assert cr["search_mode_bias"] == tim.search_modes["conservative"]["bias"]
    assert "search_mode_fallback" not in cr


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_timbaland_resolved_modes_are_its_authored_table_values(name, tim_analyzed):
    """Every fixture resolves through timbaland's OWN authored table: the
    intimate fixture to its ``intimate_mode``, the other two to its
    ``default_mode`` — pinned by name."""
    assert tim_analyzed[name].creative["search_mode"] == TIMBALAND_RESOLVED_MODES[name]


def test_explicit_creative_mode_still_overrides_the_profile_table():
    """The ``creative_mode`` argument keeps precedence over the profile's
    table (the pre-wiring contract): an explicit real timbaland mode wins on
    the intimate fixture."""
    res = _analyze(
        "simple_vocal_piano_song", producer="timbaland", creative_mode="negative_space"
    )
    assert res.creative["search_mode"] == "negative_space"
    assert "search_mode_fallback" not in res.creative


# =========================================================================== #
# 3. FALLBACK SAFETY — profile-owned, deterministic, observational.
# =========================================================================== #
def test_table_mapping_to_a_missing_mode_falls_back_to_the_declared_default():
    """A profile whose ``intimate_mode`` names a mode absent from its
    ``search_modes``: the engine resolves to the profile's OWN declared
    ``default_mode`` (rule step 1) and surfaces the substitution
    observationally — no KeyError."""
    tim = load_profile("timbaland")
    table = dict(tim.default_creative_mode)
    table["intimate_mode"] = "no_such_mode"
    ghost = dataclasses.replace(tim, default_creative_mode=table)

    res = _analyze("simple_vocal_piano_song", producer=ghost)
    cr = res.creative
    assert cr["search_mode"] == "dramatic_contrast"  # ghost's own declared default
    assert cr["search_mode_bias"] == ghost.search_modes["dramatic_contrast"]["bias"]
    fb = cr["search_mode_fallback"]
    assert fb["requested_mode"] == "no_such_mode"
    assert fb["resolved_mode"] == "dramatic_contrast"
    assert "no_such_mode" in fb["reason"] and "dramatic_contrast" in fb["reason"]


def test_profile_without_dramatic_contrast_never_keyerrors():
    """THE EXACT CRASH SCENARIO the P-032h reviewer flagged: the resolved
    mode name is absent AND the profile carries NO mode named
    ``dramatic_contrast`` (and its declared default is missing too) — the
    old hardcoded substitute would dereference a mode the profile does not
    have. The wired engine resolves to the FIRST mode in the profile's own
    ``search_modes`` (rule step 2, authoring order) and reports it."""
    ref = load_profile("halee_ramone")
    prof = dataclasses.replace(
        ref,
        search_modes={"only_mode": {"allowed_risk": "low", "bias": "single authored mode"}},
        default_creative_mode={
            "intimate_truth_words": ["intimate"],
            "intimate_mode": "ghost_mode",
            "default_mode": "also_ghost",
        },
    )
    res = _analyze("simple_vocal_piano_song", producer=prof)  # intimate truth
    cr = res.creative
    assert cr["search_mode"] == "only_mode"
    assert cr["search_mode_bias"] == "single authored mode"
    fb = cr["search_mode_fallback"]
    assert fb["requested_mode"] == "ghost_mode"
    assert fb["resolved_mode"] == "only_mode"


def test_declared_default_is_preferred_over_first_authored_mode(analyzed):
    """Rule order is observable: with ``dramatic_contrast`` removed from the
    reference's ``search_modes`` and the declared ``default_mode`` re-authored
    to a REAL remaining mode (``deconstructive``), a request for the removed
    name resolves to the DECLARED default — not to the first authored mode
    (``conservative``) — proving step 1 outranks step 2."""
    ref = load_profile("halee_ramone")
    sm = {k: v for k, v in ref.search_modes.items() if k != "dramatic_contrast"}
    assert next(iter(sm)) == "conservative"  # anchor: first authored mode
    table = dict(ref.default_creative_mode)
    table["default_mode"] = "deconstructive"
    prof = dataclasses.replace(ref, search_modes=sm, default_creative_mode=table)

    out = run_creative_engine(
        analyzed["splice_loop_problem"], "dramatic_contrast", profile=prof
    )
    assert out["search_mode"] == "deconstructive"
    assert out["search_mode_fallback"]["requested_mode"] == "dramatic_contrast"
    assert out["search_mode_fallback"]["resolved_mode"] == "deconstructive"


def test_engine_with_no_mode_resolves_the_profiles_declared_default(analyzed):
    """``run_creative_engine`` without a mode resolves the profile's own
    declared default — no request was made, so no fallback evidence is
    emitted (the key stays absent, the evidence-key discipline)."""
    out_ref = run_creative_engine(analyzed["simple_vocal_piano_song"])
    assert out_ref["search_mode"] == "dramatic_contrast"
    assert "search_mode_fallback" not in out_ref

    out_tim = run_creative_engine(
        analyzed["simple_vocal_piano_song"], profile=load_profile("timbaland")
    )
    assert out_tim["search_mode"] == "dramatic_contrast"  # timbaland's own default_mode
    assert "search_mode_fallback" not in out_tim


def test_fallback_is_surfaced_where_the_mode_is_reported(analyzed):
    """The substitution is human-visible where the mode already renders: the
    creative report carries the fallback's observational reason verbatim when
    (and only when) the key is present."""
    ref = load_profile("halee_ramone")
    table = dict(ref.default_creative_mode)
    table["default_mode"] = "no_such_mode"
    prof = dataclasses.replace(ref, default_creative_mode=table)
    out = run_creative_engine(analyzed["splice_loop_problem"], "no_such_mode", profile=prof)
    assert out["search_mode_fallback"]["resolved_mode"] == "conservative"  # first authored
    md = render_creative(out)
    assert out["search_mode_fallback"]["reason"] in md

    clean = run_creative_engine(
        analyzed["splice_loop_problem"], "dramatic_contrast", profile=ref
    )
    assert "search_mode_fallback" not in clean
    assert "fallback" not in render_creative(clean).lower()


# =========================================================================== #
# 4. PER-CALL THREADING — the PASSED profile's table, never the default's.
# =========================================================================== #
def test_passed_profiles_table_is_consulted_never_the_module_defaults():
    """Sabotage guard: a profile re-authoring ``intimate_mode`` to
    ``experimental`` (a REAL reference mode) must see ``experimental`` end to
    end. If ``_default_creative_mode`` ignored the passed profile and read
    the module default, the intimate fixture would resolve
    ``vocal_truth`` (also real in this profile) — and this fails."""
    ref = load_profile("halee_ramone")
    table = dict(ref.default_creative_mode)
    table["intimate_mode"] = "experimental"
    prof = dataclasses.replace(ref, default_creative_mode=table)

    res = _analyze("simple_vocal_piano_song", producer=prof)
    assert res.creative["search_mode"] == "experimental"
    assert "search_mode_fallback" not in res.creative

    intent = {"singular_emotional_truth": "quiet and intimate"}
    assert pipeline._default_creative_mode(intent, prof) == "experimental"
    assert pipeline._default_creative_mode(intent) == "vocal_truth"


# =========================================================================== #
# 5. NO-ALIASING — reads only; every module default untouched.
# =========================================================================== #
def test_module_default_profiles_untouched_after_interleaved_runs():
    """Interleave timbaland / reference / synthetic-profile analyses and
    prove ``pipeline._DEFAULT_PROFILE`` (new in this packet) and
    ``creative._DEFAULT_PROFILE`` still equal a fresh reference load — the
    wiring reads tables, it never writes them."""
    snap_pipe_table = copy.deepcopy(pipeline._DEFAULT_PROFILE.default_creative_mode)
    snap_creative_modes = copy.deepcopy(creative._DEFAULT_PROFILE.search_modes)
    snap_creative_table = copy.deepcopy(creative._DEFAULT_PROFILE.default_creative_mode)

    ref = load_profile("halee_ramone")
    table = dict(ref.default_creative_mode)
    table["intimate_mode"] = "no_such_mode"
    synthetic = dataclasses.replace(ref, default_creative_mode=table)

    _analyze("simple_vocal_piano_song", producer="timbaland")
    _analyze("simple_vocal_piano_song")
    _analyze("simple_vocal_piano_song", producer=synthetic)

    fresh = load_profile("halee_ramone")
    assert pipeline._DEFAULT_PROFILE.metadata["name"] == "halee_ramone"
    assert pipeline._DEFAULT_PROFILE.default_creative_mode == snap_pipe_table
    assert pipeline._DEFAULT_PROFILE.default_creative_mode == fresh.default_creative_mode
    assert creative._DEFAULT_PROFILE.search_modes == snap_creative_modes
    assert creative._DEFAULT_PROFILE.search_modes == fresh.search_modes
    assert creative._DEFAULT_PROFILE.default_creative_mode == snap_creative_table
    # the synthetic profile's own table kept its (intentional) ghost entry —
    # the run read it, nothing rewrote it.
    assert synthetic.default_creative_mode["intimate_mode"] == "no_such_mode"
