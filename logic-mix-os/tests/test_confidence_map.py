"""P-031 — the binding guards for the per-area confidence framework:
``confidence_map`` (Commit-1: schema + authored map + validation).

THE USER-UPGRADED SCOPE (binding): per-interpretation-AREA confidence, not a
single profile-level stamp. Every producer profile must carry a REQUIRED
``confidence_map`` — an ordered list of ``{area, level, reason}`` entries with
``level`` exactly one of ``high`` / ``limited`` / ``deferred`` — so the
standing honest deferrals documented in docstrings across seven packets become
FIRST-CLASS, machine-readable profile data.

**THIS PACKET IS LABELING, NEVER JUDGMENT.** No scorer reads the map; no
score, variant, promotion, or recommendation may change. The byte-identity
guards below (both mandated surfaces, all 3 fixtures, regression 68/68) are
the health metric.

Guard groups, mirroring the packet:

1. **Field discipline** — REQUIRED top-level field; missing map / unknown
   level / empty reason / non-string area / empty list all rejected by the
   loader (no silent defaults — the P-032f attack-4 discipline; an honesty
   layer with zero entries is not honest).
2. **Honesty pins** — halee_ramone's authored map verbatim-pinned: the
   ``limited`` inert-blend entry (the P-032f reviewer corollary) and the four
   standing deferrals (cultural loop recognizability / true hook recurrence /
   motif provenance / onset-timing strong forms) so a future packet cannot
   silently delete the honesty labels. The ``high`` claims are checked against
   machine facts (live axes weighted; agnostic axes weight-0 as stated).
3. **Byte-identity, BOTH surfaces** — doctrine pins (73.8 / 70.7 / 74.3 + all
   14 components) + the full creative base capture + regression 68/68.
4. **No-aliasing** — every load parses fresh; mutating a loaded map can never
   reach a reload or the module default.
5. **Observational language** — zero judgment words across every authored
   area and reason.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import (
    CONFIDENCE_LEVELS,
    _REQUIRED_DATA_FIELDS,
    _validate,
    load_profile,
)
from test_protect_iconic_loops import BASE_CREATIVE_SURFACE
from test_vocal_type import BASE_COMPONENT_SCORES, FIXTURE_NAMES, JUDGMENT_WORDS

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_PROFILE_PATH = _ROOT / "logic_mix_os" / "doctrine" / "producers" / "halee_ramone.json"

# The authored halee_ramone map, VERBATIM (the honesty pin: any edit to the
# authored labels is a conscious, test-visible decision — never a silent one).
AUTHORED_MAP = [
    {
        "area": "vocal centrality / depth hierarchy / section contrast / static-dynamic balance",
        "level": "high",
        "reason": "hand-curated from documented Halee/Ramone technique; these interpretation axes are live and weighted in this profile",
    },
    {
        "area": "the seven producer-agnostic axes as measurement (beat identity, negative space, groove coherence, rhythmic surprise, low-end motion, loop context, vocal role fit)",
        "level": "high",
        "reason": "measured live on every run; deliberately weight-0 in this profile — the reference judgment predates these axes and does not weight them",
    },
    {
        "area": "vocal blend interpretation",
        "level": "limited",
        "reason": "the masking analyzer emits vocal-band events only against the lead today; the blend policy is mechanically live but dormant on real exported-stem data",
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
        "area": "onset-timing strong forms (fingerprint typing, fills/unexpected-hit detection, kick/sub temporal interlock, per-section true-sub movement)",
        "level": "deferred",
        "reason": "these need per-onset timing and typing signals not measurable on exported stems at doctrine time; the section-aggregate weak forms are what ship",
    },
]


def _raw() -> dict:
    with open(_PROFILE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _raw_with(cmap) -> dict:
    raw = _raw()
    raw["confidence_map"] = cmap
    return raw


# --------------------------------------------------------------------------- #
# 1. FIELD DISCIPLINE — required, explicit, structurally validated.
# --------------------------------------------------------------------------- #
def test_field_is_in_the_required_data_fields():
    assert "confidence_map" in _REQUIRED_DATA_FIELDS


def test_levels_vocabulary_is_pinned():
    """Exactly three levels, exactly these, in this order — the honesty
    vocabulary is closed (no fourth level can appear silently)."""
    assert CONFIDENCE_LEVELS == ("high", "limited", "deferred")


def test_omitted_field_is_rejected_never_silently_defaulted():
    """The P-032f attack-4 discipline: a profile JSON without
    ``confidence_map`` is structurally invalid — the loader REJECTS it. The
    honesty labeling must be explicit in every producer's JSON."""
    raw = _raw()
    del raw["confidence_map"]
    with pytest.raises(ValueError, match="confidence_map"):
        _validate(raw, "halee_ramone")


def test_empty_map_is_rejected():
    """An honesty layer with zero entries is not honest — REJECT."""
    with pytest.raises(ValueError, match="confidence_map"):
        _validate(_raw_with([]), "halee_ramone")


def test_structure_is_validated():
    """The declared shape is enforced: a non-empty list of objects, each with
    a non-empty string ``area``, a ``level`` from the closed vocabulary, and
    a non-empty string ``reason``."""
    ok = {"area": "a", "level": "high", "reason": "r"}
    for broken in (
        "high",                                                  # not a list
        {"area": "a", "level": "high", "reason": "r"},           # dict, not list
        ["high"],                                                # non-dict entry
        [None],                                                  # non-dict entry
        [{"level": "high", "reason": "r"}],                      # missing area
        [{"area": "a", "reason": "r"}],                          # missing level
        [{"area": "a", "level": "high"}],                        # missing reason
        [{"area": "", "level": "high", "reason": "r"}],          # empty area
        [{"area": "a", "level": "high", "reason": ""}],          # empty reason
        [{"area": "a", "level": "high", "reason": "   "}],       # blank reason
        [{"area": 3, "level": "high", "reason": "r"}],           # non-str area
        [{"area": "a", "level": "high", "reason": 3}],           # non-str reason
        [{"area": "a", "level": "medium", "reason": "r"}],       # unknown level
        [{"area": "a", "level": "HIGH", "reason": "r"}],         # case matters
        [{"area": "a", "level": None, "reason": "r"}],           # non-str level
        [ok, {"area": "b", "level": "certain", "reason": "r"}],  # one broken entry
    ):
        with pytest.raises(ValueError, match="confidence_map"):
            _validate(_raw_with(broken), "halee_ramone")

    # A minimal valid map passes — the matrix rejects shape, not content.
    _validate(_raw_with([ok]), "halee_ramone")


def test_every_authored_level_is_from_the_closed_vocabulary():
    for entry in load_profile("halee_ramone").confidence_map:
        assert entry["level"] in CONFIDENCE_LEVELS


# --------------------------------------------------------------------------- #
# 2. HONESTY PINS — the authored map, verbatim; claims match machine facts.
# --------------------------------------------------------------------------- #
def test_halee_ramone_authored_map_verbatim():
    """The full authored map, pinned verbatim in authoring order (order is
    load-bearing: it is the rendering order)."""
    assert load_profile("halee_ramone").confidence_map == AUTHORED_MAP


def test_limited_inert_blend_entry_is_pinned_verbatim():
    """THE P-032f REVIEWER COROLLARY, first-class: vocal blend interpretation
    is LIMITED — the analyzer emits vocal-band events only against the lead,
    so the blend policy is mechanically live but dormant on real data. A
    future packet deleting or relaxing this label breaks here."""
    limited = [e for e in load_profile("halee_ramone").confidence_map
               if e["level"] == "limited"]
    assert limited == [AUTHORED_MAP[2]]
    assert "only against the lead" in limited[0]["reason"]


def test_deferred_entries_are_pinned_verbatim():
    """The four standing honest deferrals — cultural loop recognizability,
    true hook recurrence, motif provenance, and the onset-timing strong forms
    (fingerprint typing / fills and unexpected-hit detection / kick-sub
    temporal interlock / per-section true-sub movement) — all present,
    verbatim, so no later packet can silently claim or drop them."""
    deferred = [e for e in load_profile("halee_ramone").confidence_map
                if e["level"] == "deferred"]
    assert deferred == AUTHORED_MAP[3:]

    areas = " | ".join(e["area"] for e in deferred)
    for standing in (
        "cultural loop recognizability",
        "true hook recurrence",
        "motif provenance",
        "fingerprint typing",
        "unexpected-hit detection",
        "kick/sub temporal interlock",
        "per-section true-sub movement",
    ):
        assert standing in areas, f"standing deferral {standing!r} missing"


def test_high_claims_are_consistent_with_the_machine_facts():
    """A ``high`` label must never overclaim. Entry 1 claims the live axes
    are weighted — their weights ARE non-zero. Entry 2 claims the seven
    agnostic axes are deliberately weight-0 — their weights ARE zero, and the
    reason SAYS so (the honesty is in the stated reason, not implied)."""
    p = load_profile("halee_ramone")
    w = p.doctrine["weights"]

    for live in ("halee_score", "ramone_score", "vocal_centrality_score",
                 "depth_hierarchy_score", "section_contrast_score",
                 "static_mix_score", "dynamic_mix_score"):
        assert w[live] > 0, f"{live} claimed live/weighted but weight is 0"

    agnostic_entry = p.confidence_map[1]
    assert "weight-0" in agnostic_entry["reason"]
    for agnostic in ("beat_identity_score", "negative_space_score",
                     "groove_coherence_score", "rhythmic_surprise_score",
                     "low_end_motion_score", "loop_context_score",
                     "vocal_role_fit_score"):
        assert w[agnostic] == 0, f"{agnostic} claimed weight-0 but is weighted"


def test_limited_blend_label_is_consistent_with_the_authored_policy():
    """The limited entry accompanies a profile that declares
    ``acceptable_blend: false`` — the label and the policy agree."""
    p = load_profile("halee_ramone")
    assert p.vocal_blend_policy["acceptable_blend"] is False


def test_map_language_is_observational_zero_judgment_words():
    """USER-MANDATED language guard over ALL authored areas and reasons: the
    map reports what is measured, weighted, dormant or deferred — never
    'bad', 'problem', 'should', 'fix' (nor better/worse/wrong)."""
    blob = json.dumps(load_profile("halee_ramone").confidence_map,
                      sort_keys=True).lower()
    for word in JUDGMENT_WORDS:
        assert word not in blob, f"judgment word {word!r} in confidence_map"


# --------------------------------------------------------------------------- #
# 3. BYTE-IDENTITY, BOTH SURFACES — labeling, never judgment.
# --------------------------------------------------------------------------- #
def test_doctrine_surface_byte_identical_all_three_fixtures(analyzed):
    """Every one of the 13 pre-existing component scores + the overall
    (73.8 / 70.7 / 74.3) equals the pinned base value on all three fixtures —
    the confidence map moved no number."""
    for name in FIXTURE_NAMES:
        ds = analyzed[name].doctrine_score
        for key, expected in BASE_COMPONENT_SCORES[name].items():
            assert ds[key] == expected, f"{name}.{key}: {ds[key]} != {expected}"


def test_creative_surface_byte_identical_to_base_capture(analyzed):
    """SURFACE (b), user-mandated: the full production ``result.creative``
    still equals the pinned base capture (every branch winner, every variant
    kind + overall score + fired nudges, all three fixtures)."""
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


def test_regression_still_sixty_eight_of_sixty_eight():
    """The golden corpus regression — categorical fingerprint + the original
    score keys — still passes 68/68 with the map authored."""
    from logic_mix_os.regression import run_regression_suite

    report = run_regression_suite(_ROOT / "fixtures")
    assert report["tests_run"] == 68
    assert report["passed"] == 68
    assert report["failed"] == 0


def test_no_confidence_map_leak_into_the_creative_surface(analyzed):
    """The map is report-surface labeling; the creative surface never
    mentions it."""
    for name in FIXTURE_NAMES:
        blob = json.dumps(analyzed[name].creative, sort_keys=True)
        assert "confidence_map" not in blob


# --------------------------------------------------------------------------- #
# 4. NO-ALIASING — every load parses fresh; mutation reaches nothing shared.
# --------------------------------------------------------------------------- #
def test_load_gives_fresh_copies_mutation_cannot_reach_a_reload():
    p = load_profile("halee_ramone")
    p.confidence_map[0]["level"] = "deferred"
    p.confidence_map.append({"area": "x", "level": "high", "reason": "y"})
    assert load_profile("halee_ramone").confidence_map == AUTHORED_MAP


def test_module_default_profile_map_is_intact():
    """The shared ``_DEFAULT_PROFILE`` singleton (the byte-identity anchor)
    carries the authored map, byte-equal to a fresh load."""
    assert doctrine_engine._DEFAULT_PROFILE.confidence_map == AUTHORED_MAP


def test_two_loads_are_equal_but_independent():
    a = load_profile("halee_ramone")
    b = load_profile("halee_ramone")
    assert a.confidence_map == b.confidence_map
    assert a.confidence_map is not b.confidence_map
    assert all(x is not y for x, y in zip(a.confidence_map, b.confidence_map))
