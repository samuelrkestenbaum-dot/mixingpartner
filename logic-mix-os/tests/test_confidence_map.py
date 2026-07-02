"""P-031 — the binding guards for the per-area confidence framework:
``confidence_map`` (Commit-1: schema + authored map + validation;
Commit-2: the map rendered on the report surface).

THE USER-UPGRADED SCOPE (binding): per-interpretation-AREA confidence, not a
single profile-level stamp. Every producer profile must carry a REQUIRED
``confidence_map`` — an ordered list of ``{area, level, reason}`` entries with
``level`` exactly one of ``high`` / ``limited`` / ``deferred`` — so the
standing honest deferrals documented in docstrings across seven packets become
FIRST-CLASS, machine-readable profile data.

**THIS PACKET IS LABELING, NEVER JUDGMENT.** No scorer reads the map; no
score, variant, promotion, or recommendation may change. The byte-identity
guards below (both mandated surfaces, all 3 fixtures, regression 93/93 (P-035 moved the corpus count consciously: +25 checks from the vocal_chop_groove fixture)) are
the health metric.

Guard groups, mirroring the packet:

1. **Field discipline** — REQUIRED top-level field; missing map / unknown
   level / empty reason / non-string area / empty list all rejected by the
   loader (no silent defaults — the P-032f attack-4 discipline; an honesty
   layer with zero entries is not honest).
2. **Honesty pins** — halee_ramone's authored map verbatim-pinned: the
   ``limited`` inert-blend entry (the P-032f reviewer corollary) and the
   standing deferrals (cultural loop recognizability / true hook recurrence /
   motif provenance / onset-timing strong forms / per-section true-sub
   movement — the latter deferred on BAND RESOLUTION: sections expose
   ``low_mid_energy`` 120-500 Hz only, per the P-032c boundary, NOT on onset
   timing) so a future packet cannot silently delete the honesty labels. The
   ``high`` claims are checked against machine facts (live axes weighted;
   agnostic axes weight-0 as stated).
3. **Byte-identity, BOTH surfaces** — doctrine pins (73.8 / 70.7 / 74.3 + all
   14 components) + the full creative base capture + regression 93/93 (P-035 moved the corpus count consciously: +25 checks from the vocal_chop_groove fixture).
4. **No-aliasing** — every load parses fresh; mutating a loaded map can never
   reach a reload or the module default.
5. **Observational language** — zero judgment words across every authored
   area and reason.
6. **The machine-readable copy** (Commit-2) — ``doctrine_score`` carries a
   ``confidence`` key copied VERBATIM from the PASSED profile (per-call, the
   P-029 threading), fresh — never an alias; the schema documents it.
7. **Rendering + liveness** (Commit-2) — the verdict markdown gains a compact
   "Confidence" section grouped by level; a synthetic profile with a
   DIFFERENT map, driven through the REAL ``analyze()`` path and
   ``write_artifacts``, renders ITS entries (sabotage — sourcing the section
   from the module default or hardcoding it — fails here while byte-identity
   stays green); the section is data-driven (absent key => absent section);
   the renderer reads, never mutates.
8. **Golden blindness** — ``build_snapshot`` (categorical + the original
   score keys) cannot see the addition: the live snapshot carries no map
   vocabulary and still matches the stored golden, 0 criticals.
"""

from __future__ import annotations

import copy
import dataclasses
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
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest
from logic_mix_os.renderers import markdown_renderer
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
    """The standing honest deferrals — cultural loop recognizability, true
    hook recurrence, motif provenance, the onset-timing strong forms
    (fingerprint typing / fills and unexpected-hit detection / kick-sub
    temporal interlock), and per-section true-sub movement (its OWN entry:
    the P-032c boundary is BAND RESOLUTION — sections expose low_mid_energy
    120-500 Hz only — not onset timing) — all present, verbatim, so no later
    packet can silently claim or drop them."""
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

    for live in ("physical_space_score", "emotional_hierarchy_score", "vocal_centrality_score",
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


def test_regression_still_green_full_corpus():
    """The golden corpus regression — categorical fingerprint + the original
    score keys — still passes 93/93 (P-035 moved the corpus count consciously: +25 checks from the vocal_chop_groove fixture) with the map authored."""
    from logic_mix_os.regression import run_regression_suite

    report = run_regression_suite(_ROOT / "fixtures")
    assert report["tests_run"] == 93
    assert report["passed"] == 93
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


# --------------------------------------------------------------------------- #
# 6. THE MACHINE-READABLE COPY — doctrine_score carries the per-call map.
# --------------------------------------------------------------------------- #
def test_doctrine_score_carries_the_authored_confidence_copy(analyzed):
    """Every fixture's ``doctrine_score`` carries the authored map verbatim
    under the additive ``confidence`` key — the machine-readable copy a human
    or Cowork reads next to the scores it qualifies."""
    for name in FIXTURE_NAMES:
        assert analyzed[name].doctrine_score["confidence"] == AUTHORED_MAP


def test_confidence_copy_is_fresh_never_an_alias_of_the_profile():
    """The artifact copy is freshly built per call: mutating it can never
    reach the profile (nor the module default)."""
    prof = load_profile("halee_ramone")
    ds = doctrine_engine.score_doctrine([], [], {"events": []}, None, profile=prof)
    assert ds["confidence"] == prof.confidence_map
    assert ds["confidence"] is not prof.confidence_map
    assert all(a is not b for a, b in zip(ds["confidence"], prof.confidence_map))

    ds["confidence"][0]["level"] = "deferred"
    ds["confidence"].append({"area": "x", "level": "high", "reason": "y"})
    assert prof.confidence_map == AUTHORED_MAP
    assert doctrine_engine._DEFAULT_PROFILE.confidence_map == AUTHORED_MAP


def test_doctrine_score_json_still_validates_and_schema_documents_the_shape(analyzed):
    """The artifact still validates, and the schema documents the additive
    key with the closed level vocabulary (no additionalProperties conflict —
    the doctrine_score schema declares none)."""
    from logic_mix_os.validation.output_validator import load_schema, validate_instance

    schema = load_schema("doctrine_score.schema.json")
    assert "additionalProperties" not in schema
    conf_schema = schema["properties"]["confidence"]
    assert conf_schema["items"]["properties"]["level"]["enum"] == list(CONFIDENCE_LEVELS)
    assert conf_schema["items"]["required"] == ["area", "level", "reason"]
    assert "confidence" not in schema["required"]  # additive, never breaking

    for name in FIXTURE_NAMES:
        assert validate_instance(analyzed[name].doctrine_score, schema) == []


# --------------------------------------------------------------------------- #
# 7. RENDERING + LIVENESS — the verdict section, sourced per-call.
# --------------------------------------------------------------------------- #
def test_verdict_markdown_renders_the_authored_entries(analyzed):
    """The verdict artifact gains a compact "Confidence" section carrying
    every authored area and reason, grouped by level in the closed-vocabulary
    order (high before limited before deferred)."""
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        md = markdown_renderer.render_mix_verdict(res.mix_plan, res.doctrine_score)
        assert "## Confidence" in md
        for entry in AUTHORED_MAP:
            assert entry["area"] in md, (name, entry["area"])
            assert entry["reason"] in md, (name, entry["area"])
        hi, li, de = md.index("**High**"), md.index("**Limited**"), md.index("**Deferred**")
        assert hi < li < de
        # compact `area — reason` lines, one per entry
        for entry in AUTHORED_MAP:
            assert f"- {entry['area']} — {entry['reason']}" in md


def test_rendering_liveness_a_passed_profiles_map_renders_not_the_defaults(tmp_path):
    """P-029 threading, load-bearing: a synthetic profile with a DIFFERENT
    map, driven through the REAL ``analyze()`` path and ``write_artifacts``,
    renders ITS entries in both the JSON copy and the markdown section — and
    NONE of halee_ramone's.

    Sabotage this catches: sourcing the copy/section from the module default
    (``_DEFAULT_PROFILE``) or hardcoding the section renders the reference
    entries here and FAILS — while every byte-identity guard stays green."""
    from conftest import ROOT

    synthetic_map = [
        {"area": "synthetic groove interpretation", "level": "high",
         "reason": "authored for the liveness proof"},
        {"area": "synthetic hook reading", "level": "deferred",
         "reason": "not measurable in this synthetic profile"},
    ]
    prof = dataclasses.replace(load_profile("halee_ramone"),
                               confidence_map=synthetic_map)
    name = "simple_vocal_piano_song"
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    res = analyze(str(ROOT / "fixtures" / name / "stems"), manifest, producer=prof)

    assert res.doctrine_score["confidence"] == synthetic_map
    write_artifacts(res, tmp_path)

    dsj = json.loads((tmp_path / "doctrine_score.json").read_text(encoding="utf-8"))
    assert dsj["confidence"] == synthetic_map

    md = (tmp_path / "mix_verdict.md").read_text(encoding="utf-8")
    assert "synthetic groove interpretation" in md
    assert "authored for the liveness proof" in md
    assert "synthetic hook reading" in md
    for reference_area in ("vocal blend interpretation",
                           "cultural loop recognizability",
                           "true hook recurrence", "motif provenance"):
        assert reference_area not in md, f"module default leaked: {reference_area}"


def test_verdict_section_is_data_driven_absent_key_absent_section():
    """A doctrine_score WITHOUT the key (a pre-P-031 artifact) renders no
    Confidence section — the section is data-driven, never hardcoded."""
    md = markdown_renderer.render_mix_verdict({}, {})
    assert "## Confidence" not in md
    md_empty = markdown_renderer.render_mix_verdict({}, {"confidence": []})
    assert "## Confidence" not in md_empty


def test_renderer_reads_never_mutates(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    ds_before = copy.deepcopy(res.doctrine_score)
    mp_before = copy.deepcopy(res.mix_plan)
    markdown_renderer.render_mix_verdict(res.mix_plan, res.doctrine_score)
    assert res.doctrine_score == ds_before
    assert res.mix_plan == mp_before


def test_rendered_level_order_is_the_closed_vocabulary_single_source():
    """The renderer groups by ``CONFIDENCE_LEVELS`` itself (one source of
    truth for vocabulary AND order) — a level absent from a map renders no
    empty group header."""
    ds = {"confidence": [
        {"area": "only-deferred area", "level": "deferred", "reason": "stated"},
    ]}
    md = markdown_renderer.render_mix_verdict({}, ds)
    assert "**Deferred**" in md
    assert "**High**" not in md
    assert "**Limited**" not in md


# --------------------------------------------------------------------------- #
# 8. GOLDEN BLINDNESS — the addition is invisible to build_snapshot.
# --------------------------------------------------------------------------- #
def test_build_snapshot_is_blind_to_the_confidence_addition(analyzed):
    """What the golden pins — the categorical track fingerprint, masking
    classifications, section lift warnings, the original score keys and the
    next-pass titles — cannot see the map: the live snapshot carries no map
    vocabulary and still matches the stored golden with 0 criticals."""
    from conftest import ROOT
    from logic_mix_os.regression import build_snapshot, compare_snapshots

    for name in FIXTURE_NAMES:
        snapshot = build_snapshot(analyzed[name])
        blob = json.dumps(snapshot, sort_keys=True)
        for entry in AUTHORED_MAP:
            assert entry["area"] not in blob
            assert entry["reason"] not in blob

        golden_path = ROOT / "fixtures" / name / "golden" / "snapshot.json"
        golden = json.loads(golden_path.read_text(encoding="utf-8"))
        tests, passed, critical, warnings = compare_snapshots(name, golden, snapshot)
        assert critical == []
        assert passed == tests
        assert warnings == []
