"""P-044 — NEGATIVE-SPACE DROPOUT MOVE FAMILY (candidate-planning only).

The user's decision, verbatim authority: "This family is higher-risk because
it sounds like 'mute/drop something,' so the first implementation must be
candidate-planning only, not execution semantics."

THE DOCTRINE (the user's safety line, verbatim): **"dropout is an arrangement
proposal, not a destructive operation."**

The packet's shape, proven here:

* EXACTLY ONE new extended kind — ``negative_space_dropout`` — appended to
  both vocabularies (10 kinds; 3 extended), reach-gated exactly like the
  P-043 families (tests/test_move_vocabulary_expansion.py carries the
  seam-level proofs, consciously extended to the third kind).
* WHAT IT MAY ADDRESS (the user's list — nothing else): supporting clutter ·
  non-lead decorative layers · sectional over-density · rhythmic contrast
  opportunities · background texture reduction. The curated variants'
  candidate surfaces (``_dropout_texture_beds`` / ``_dropout_clutter``) are
  built from exactly these reads. A loop-problem dropout variant is
  CONSCIOUSLY absent (the loop's source integrity is on the
  must-never-touch list).
* WHAT IT MUST NEVER TOUCH — the ENGINE-owned, PROFILE-BLIND structural
  protection filter (``_dropout_protected_names``) excludes, on REAL
  record/analysis signals: the lead vocal (identity-derived), hook
  candidates (``vocal_hook_candidate``), vocals under masked-lead-grade
  protection (``vocal_uncertain`` + every vocal while the lead is
  bad-masked), the core groove carriers / kick+sub foundation (kick + snare
  identities, bass family), and the primary emotional-hierarchy (sacred)
  elements. NO FALLBACK INTO PROTECTED TERRITORY: with no unprotected
  target the variant DOES NOT EMIT — dropout never degrades toward
  protected elements or phantom targets (unlike ``_resolve``'s documented
  degrade chain for the other families).
* NO EXECUTION SEMANTICS: the curated text stays inside the established
  plan-text vocabulary (duplicate + region-mute, the P-043 phrasing), is
  pinned VERBATIM, carries the ``non_destructive_duplicate_track``
  reversibility tag, and a lexical guard refuses imperative machinery words
  (apply/execute/render/bounce/delete/...).
* ROWS EVERYWHERE, HONEST RISK: all three shipped profiles author
  ``kind_scores`` + ``truth_alignment`` rows (timbaland high-affinity — this
  IS his documented negative-space philosophy; halee low-affinity at HIGH
  translation risk — under her translate-everywhere lens a full-layer hole
  is the riskiest move in the widened vocabulary; quincy moderate-low at
  medium). The cap binds against these honest rows at load AND at runtime,
  in both directions (refused where over-posture, admitted where within).
* WHO REACHES IT: Timbaland only, on exactly ``experimental`` /
  ``dramatic_contrast`` / ``negative_space`` (the user's list) —
  Halee/Ramone and Quincy author zero dropout reach; their gate is proven
  with synthetic profiles (data-not-producer, both directions), never by
  touching their taste.
"""

from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

from logic_mix_os import pipeline
from logic_mix_os.constants import (
    CREATIVE_EXTENDED_KINDS,
    CREATIVE_VARIANT_KINDS,
)
from logic_mix_os.creative import (
    _dropout_clutter,
    _dropout_protected_names,
    _dropout_texture_beds,
    _extended_variants,
    generate_variants,
    run_creative_engine,
    score_variant,
)
from logic_mix_os.doctrine.producer_profile import _validate, load_profile
from logic_mix_os.governance import govern_variant

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE
from test_mode_forking import (
    DENSE,
    ENGINE_POOL,
    PROBLEM_IDS,
    PRODUCERS,
    TIMBALAND_DEFAULT_FLOW_IDS,
    _branch,
    _ids,
    _kinds,
    _raw,
)
from test_move_vocabulary_expansion import (
    EXTENDED_POOL,
    _fork,
    _mode,
    _with_mode,
)

DROPOUT = "negative_space_dropout"
_PACKAGE = ROOT / "logic_mix_os"

# The curated dropout emission per problem on the DENSE fixture (variant ids;
# the kind is DROPOUT for all of them). The loop and depth problems carry NO
# dropout variant — the loop omission is CONSCIOUS (source integrity).
DROPOUT_POOL = {
    "chorus_lift": ["chorus_lift_F"],
    "density": ["density_E"],
    "loop": [],
    "depth": [],
    "vocal_belief": [],
}

# THE CURATED PLAN TEXT, verbatim — the no-execution-semantics pin. Every
# verb lives inside the established plan-text vocabulary (duplicate +
# region-mute is the P-043 ``arrangement_lift`` phrasing; "Mute" has been in
# the neutral pool since section 58).
CHORUS_F_CHANGES = [
    "Duplicate the texture bed and region-mute the duplicate through the final pre-chorus bar",
    "Let the chorus downbeat restore it so the re-entry reads as impact",
    "Keep the original track untouched — the dropout lives on the muted duplicate",
]
DENSITY_E_CHANGES = [
    "Pick ONE decorative/clutter layer from the affected tracks",
    "Duplicate it and region-mute the duplicate for one full section",
    "Leave the hole open — resist refilling it with another layer",
]

# Imperative execution-machinery words that must NEVER enter the dropout
# family's text (matched case-insensitively as substrings; "execut" covers
# execute/executing/execution, etc.). "mute" is deliberately NOT here: the
# region-mute/Mute plan vocabulary predates this packet (sections 55-67,
# P-043) — the guard refuses NEW machinery, not the established plan prose.
EXECUTION_MACHINERY = (
    "apply", "execut", "render", "bounc", "print",
    "delet", "eras", "overwrit", "destroy", "wipe",
)

# Every shipped profile's authored dropout row — translation risks are
# load-bearing (the cap binds against them); overalls reconstruct from the
# JSON (mean of the 7 dims minus the profile's own translation penalty).
AUTHORED_DROPOUT = {
    "halee_ramone": {
        "translation": "high", "mono": "low", "overall": 60.6,
        "truth": {"intimate": 48, "big": 68, "neutral": 60},
    },
    "timbaland": {
        "translation": "medium", "mono": "low", "overall": 80.9,
        "truth": {"intimate": 58, "big": 90, "neutral": 86},
    },
    "quincy_jones": {
        "translation": "medium", "mono": "low", "overall": 73.7,
        "truth": {"intimate": 52, "big": 78, "neutral": 72},
    },
    # P-047 (the P-045 profile swept here): eno's authored row — dropout is
    # his highest-affinity EXTENDED kind (78.9; restraint IS his documented
    # philosophy) at the same honest medium risk the other dropout authors
    # carry (never low — the P-044 floor). Also pinned from his own angle
    # in tests/test_eno_profile.py.
    "brian_eno": {
        "translation": "medium", "mono": "low", "overall": 78.9,
        "truth": {"intimate": 64, "big": 82, "neutral": 78},
    },
}

_SCORE_DIMS = ("technical", "physical_space", "emotional_hierarchy",
               "contrast", "vocal_belief", "excitement", "taste")

# The protection filter's expected output on every real fixture — the
# structural exclusions, pinned by name.
PROTECTED_BY_FIXTURE = {
    "simple_vocal_piano_song": {"Lead Vocal", "Bass"},
    "dense_chorus_with_loops": {"Lead Vocal", "Bass", "Kick", "Snare"},
    "splice_loop_problem": {"Lead Vocal"},
    VOCAL_CHOP_FIXTURE: {"Lead Vocal", "Kick", "Snare"},
}

# The dropout variants' resolved targets on every real fixture where the
# variant emits — real names, all outside the protected set. (The curated
# builders are problem-parametric: a fixture's pin covers every problem id,
# whether or not that problem fires on the fixture — the real emission is
# additionally gated by ``detect_creative_problems`` and authored reach.)
DROPOUT_TARGETS = {
    "simple_vocal_piano_song": {
        "density_E": ["Piano"],
    },
    "dense_chorus_with_loops": {
        "chorus_lift_F": ["Synth Pad", "Splice Texture Loop"],
        "density_E": ["Acoustic Guitar", "Electric Guitar 1",
                      "Electric Guitar 2", "Synth Pad", "Splice Texture Loop"],
    },
    "splice_loop_problem": {
        "chorus_lift_F": ["Splice Loop"],
        "density_E": ["Splice Loop", "Acoustic Guitar"],
    },
    VOCAL_CHOP_FIXTURE: {
        "chorus_lift_F": ["BGV Chop"],
        "density_E": ["BGV Chop", "Backing Vocals Stack", "Electric Guitar"],
    },
}


@pytest.fixture(scope="module")
def dense(analyzed):
    return analyzed[DENSE]


@pytest.fixture(scope="module")
def all_analyzed(analyzed, chop_groove_analyzed):
    """All four fixtures (the chop fixture under timbaland — his is the
    committed-tree run this packet consciously drifts)."""
    out = dict(analyzed)
    out[VOCAL_CHOP_FIXTURE] = chop_groove_analyzed["timbaland"]
    return out


# --------------------------------------------------------------------------- #
# Synthetic-record helpers for the protection proofs.
# --------------------------------------------------------------------------- #
def _rec(name, identity, family, *, source_kind="live_audio_recording",
         sacredness="useful", depth="midground", perceptual="felt",
         vocal_type=None):
    """A minimal pipeline-shaped record carrying every field the curated
    builders and the protection filter read."""
    return {
        "name": name, "instrument_identity": identity,
        "identity_family": family, "source_kind": source_kind,
        "sacredness": sacredness, "depth_default": depth,
        "perceptual_role": perceptual, "vocal_type": vocal_type,
    }


def _lead():
    return _rec("Lead Vocal", "lead_vocal", "vocal",
                source_kind="comped_audio_track", sacredness="sacred",
                depth="intimate", perceptual="heard", vocal_type="vocal_lead")


def _with_records(result, records, masking_events=()):
    """A synthetic analysis: the real result with swapped records/masking."""
    return dataclasses.replace(
        result, records=records,
        masking_report={"events": list(masking_events)},
    )


# =========================================================================== #
# The widened vocabulary — exactly ONE new kind, the user's scope decision.
# =========================================================================== #
def test_vocabulary_widened_by_exactly_the_dropout_kind():
    """P-044 adds EXACTLY ``negative_space_dropout`` to BOTH vocabularies —
    10 kinds total, 3 extended, nothing else new (the packet's non-scope:
    no other families, no second dropout family)."""
    assert CREATIVE_VARIANT_KINDS[-1] == DROPOUT
    assert CREATIVE_EXTENDED_KINDS == (
        "arrangement_lift", "ensemble_rebalance", DROPOUT)
    assert len(CREATIVE_VARIANT_KINDS) == 10
    assert len(set(CREATIVE_VARIANT_KINDS)) == 10
    dropoutish = [k for k in CREATIVE_VARIANT_KINDS
                  if "dropout" in k or "negative_space" in k]
    assert dropoutish == [DROPOUT]


def test_dropout_pool_is_the_pinned_curated_emission(dense):
    """The dropout family's curated emission per problem on the dense
    fixture IS the pinned DROPOUT_POOL — one variant for chorus_lift
    (background-texture withholding), one for density (sectional dropout),
    NONE for loop (conscious omission: source integrity), depth or
    vocal_belief. Both carry the house style and the reversibility tag."""
    for pid in PROBLEM_IDS:
        variants = [v for v in _extended_variants({"id": pid}, dense)
                    if v["kind"] == DROPOUT]
        assert _ids(variants) == DROPOUT_POOL[pid], pid
        for v in variants:
            assert v["reversibility"] == "non_destructive_duplicate_track"
            assert v["tracks_affected"], v["variant_id"]
            assert v["creative_hypothesis"] and v["changes"] and v["validation"]
            assert v["risk"] and v["expected_strength"]


def test_dropout_plan_text_is_pinned_verbatim_and_machinery_free(dense):
    """No execution semantics, byte-level: the curated changes lists are the
    pinned verbatim plan text, and NO dropout variant's prose (hypothesis /
    changes / risk / validation / name) contains an imperative machinery
    word. The plan vocabulary itself is established, not new: the
    duplicate + region-mute phrasing is asserted PRESENT in the P-043
    arrangement_lift curation, on the same emission."""
    ext = {v["variant_id"]: v
           for pid in PROBLEM_IDS for v in _extended_variants({"id": pid}, dense)}
    assert ext["chorus_lift_F"]["changes"] == CHORUS_F_CHANGES
    assert ext["density_E"]["changes"] == DENSITY_E_CHANGES

    for v in ext.values():
        if v["kind"] != DROPOUT:
            continue
        prose = " ".join(
            [v["creative_hypothesis"], v["risk"], v["name"],
             v["expected_strength"]] + v["changes"] + v["validation"]
        ).lower()
        for word in EXECUTION_MACHINERY:
            assert word not in prose, (v["variant_id"], word)

    # the plan vocabulary is P-043's, not new machinery of this packet:
    p043 = " ".join(ext["chorus_lift_E"]["changes"]).lower()
    assert "duplicate" in p043 and "region-mute" in p043


# =========================================================================== #
# THE PROTECTION FILTER — engine-owned, profile-blind, real signals.
# =========================================================================== #
@pytest.mark.parametrize("name", sorted(PROTECTED_BY_FIXTURE))
def test_protected_names_pinned_on_every_fixture(name, all_analyzed):
    """The filter's exclusions on every real fixture, by name: the lead
    vocal, the kick/snare + bass groove foundation, and every sacred
    element. (No fixture currently carries hook-candidate/uncertain vocals
    or a masked lead — those exclusions are proven synthetically below.)"""
    assert _dropout_protected_names(all_analyzed[name]) \
        == PROTECTED_BY_FIXTURE[name], name


@pytest.mark.parametrize("name", sorted(DROPOUT_TARGETS))
def test_dropout_targets_are_real_unprotected_and_pinned(name, all_analyzed):
    """Every dropout variant's resolved target list on every real fixture is
    the pinned REAL-record subset, disjoint from the protected set, never
    empty where the variant emits — and no dropout variant exists at all
    where the fixture offers no legitimate surface."""
    res = all_analyzed[name]
    protected = _dropout_protected_names(res)
    real_names = {r["name"] for r in res.records}
    expected = DROPOUT_TARGETS.get(name, {})
    emitted = {}
    for pid in PROBLEM_IDS:
        for v in _extended_variants({"id": pid}, res):
            if v["kind"] != DROPOUT:
                continue
            emitted[v["variant_id"]] = v["tracks_affected"]
            assert v["tracks_affected"], (name, v["variant_id"])
            assert set(v["tracks_affected"]) <= real_names, (name, v["variant_id"])
            assert set(v["tracks_affected"]) & protected == set(), \
                (name, v["variant_id"])
    assert emitted == expected, name


def test_reached_dropout_emits_nothing_when_only_protected_targets_exist(dense):
    """THE NO-FALLBACK RULE: a project whose entire dropout candidate
    surface is protected (a hook-candidate vocal chop bed — supporting
    clutter AND an imported bed, but a hook) emits ZERO dropout variants
    even under a full authored reach — no phantom target, no degrade toward
    the protected elements (the ``_resolve`` pattern is explicitly NOT
    followed). The rest of the reached emission is untouched."""
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
    # the candidate surfaces are NON-empty — protection is the refusal:
    assert "Hook Chop" in _dropout_texture_beds(records)
    assert "Hook Chop" in _dropout_clutter(records)

    prof = _with_mode("timbaland", _mode(reach=[DROPOUT]))
    for pid in PROBLEM_IDS:
        emitted = generate_variants({"id": pid}, synth, "reach", prof)
        assert DROPOUT not in _kinds(emitted), pid
        assert emitted == generate_variants({"id": pid}, synth), pid
        # surfaced honestly at the EXISTING seam: nothing reads as reached.
        _, fork = _fork(prof, "reach", pid, synth)
        assert DROPOUT not in fork["reached"], pid
        assert fork["reach_capped"] == [], pid


def test_the_protection_filter_is_the_deciding_variable(dense):
    """The control for the no-emit proof: the IDENTICAL project with the
    chop bed read as ``vocal_percussive`` (groove material — not a hook, not
    uncertain, not the lead) emits the dropout variant targeting EXACTLY
    that stem. Same records, same reach — the vocal-type protection signal
    is the only changed variable."""
    records = [
        _lead(),
        _rec("Groove Chop", "backing_vocal", "vocal",
             source_kind="one_shot_sample", sacredness="decorative",
             depth="midground", perceptual="heard",
             vocal_type="vocal_percussive"),
        _rec("Kick", "kick", "drums", sacredness="important",
             depth="foreground", perceptual="structural"),
    ]
    synth = _with_records(dense, records)
    assert "Groove Chop" not in _dropout_protected_names(synth)

    prof = _with_mode("timbaland", _mode(reach=[DROPOUT]))
    emitted = generate_variants({"id": "chorus_lift"}, synth, "reach", prof)
    f = next(v for v in emitted if v["kind"] == DROPOUT)
    assert f["variant_id"] == "chorus_lift_F"
    assert f["tracks_affected"] == ["Groove Chop"]

    hooked = _with_records(dense, [
        dict(records[0]),
        dict(records[1], vocal_type="vocal_hook_candidate"),
        dict(records[2]),
    ])
    assert DROPOUT not in _kinds(
        generate_variants({"id": "chorus_lift"}, hooked, "reach", prof))


def test_masked_lead_protection_covers_every_vocal(dense):
    """While the lead is bad-masked, EVERY vocal stem is excluded — a buried
    lead means no vocal layer is a legitimate dropout target. The same
    project without the masking event emits the dropout against the vocal
    stack; ``vocal_uncertain`` stays excluded either way (protected AS THE
    LEAD, the P-032f fail-closed reading)."""
    records = [
        _lead(),
        _rec("BV Stack", "backing_vocal", "vocal",
             source_kind="comped_audio_track", sacredness="decorative",
             depth="background", perceptual="felt", vocal_type="vocal_stack"),
    ]
    event = {"classification": "bad_masking", "elements": ["Lead Vocal", "Piano"]}

    masked = _with_records(dense, records, [event])
    assert _dropout_protected_names(masked) == {"Lead Vocal", "BV Stack"}
    prof = _with_mode("timbaland", _mode(reach=[DROPOUT]))
    assert DROPOUT not in _kinds(
        generate_variants({"id": "chorus_lift"}, masked, "reach", prof))

    clear = _with_records(dense, records)
    assert _dropout_protected_names(clear) == {"Lead Vocal"}
    f = next(v for v in generate_variants({"id": "chorus_lift"}, clear, "reach", prof)
             if v["kind"] == DROPOUT)
    assert f["tracks_affected"] == ["BV Stack"]

    uncertain = _with_records(dense, [
        dict(records[0]),
        dict(records[1], vocal_type="vocal_uncertain"),
    ])
    assert _dropout_protected_names(uncertain) == {"Lead Vocal", "BV Stack"}
    assert DROPOUT not in _kinds(
        generate_variants({"id": "chorus_lift"}, uncertain, "reach", prof))


def test_groove_foundation_and_sacred_elements_are_never_targets(dense):
    """The kick/snare + bass-family foundation and sacred elements are
    excluded even when their OTHER reads would qualify them as candidates
    (a decorative felt background synth bass; a sacred felt background
    pad): the structural signals outrank the clutter reads. With no other
    candidate the variants do not emit; adding one unprotected texture
    emits against exactly that texture."""
    records = [
        _lead(),
        _rec("Sub Bed", "synth_bass", "bass", sacredness="decorative",
             depth="background", perceptual="felt"),
        _rec("Sacred Pad", "pad", "synth", sacredness="sacred",
             depth="background", perceptual="felt"),
    ]
    synth = _with_records(dense, records)
    assert _dropout_protected_names(synth) \
        == {"Lead Vocal", "Sub Bed", "Sacred Pad"}
    # both ARE candidate-surface members — protection is the refusal:
    assert {"Sub Bed", "Sacred Pad"} <= set(_dropout_texture_beds(records))

    prof = _with_mode("timbaland", _mode(reach=[DROPOUT]))
    for pid in ("chorus_lift", "density"):
        assert DROPOUT not in _kinds(
            generate_variants({"id": pid}, synth, "reach", prof)), pid

    with_texture = _with_records(dense, records + [
        _rec("Air Pad", "pad", "synth", sacredness="decorative",
             depth="background", perceptual="felt"),
    ])
    f = next(v for v in generate_variants({"id": "chorus_lift"}, with_texture,
                                          "reach", prof)
             if v["kind"] == DROPOUT)
    assert f["tracks_affected"] == ["Air Pad"]


def test_protection_filter_is_profile_blind_structurally():
    """Grep-provable profile-blindness, as AST: the dropout helpers (and the
    extended-pool builder that calls them) take NO profile parameter and
    their code references NO identifier containing ``prof``/``producer`` —
    no profile data can reach, let alone widen, the filter. The signatures
    are pinned exactly."""
    assert list(inspect.signature(_dropout_protected_names).parameters) \
        == ["result"]
    assert list(inspect.signature(_dropout_texture_beds).parameters) \
        == ["records"]
    assert list(inspect.signature(_dropout_clutter).parameters) == ["records"]
    assert list(inspect.signature(_extended_variants).parameters) \
        == ["problem", "result"]

    tree = ast.parse((_PACKAGE / "creative.py").read_text(encoding="utf-8"))
    targets = {"_dropout_protected_names", "_dropout_texture_beds",
               "_dropout_clutter", "_extended_variants"}
    seen = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name in targets):
            continue
        seen.add(node.name)
        idents = []
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                idents.append(sub.id)
            elif isinstance(sub, ast.Attribute):
                idents.append(sub.attr)
            elif isinstance(sub, ast.arg):
                idents.append(sub.arg)
            elif isinstance(sub, ast.keyword) and sub.arg:
                idents.append(sub.arg)
            elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                idents.append(sub.name)
        for ident in idents:
            low = ident.lower()
            assert "prof" not in low and "producer" not in low, \
                (node.name, ident)
    assert seen == targets


# =========================================================================== #
# ROWS EVERYWHERE — honest lenses, live end to end.
# =========================================================================== #
@pytest.mark.parametrize("producer", PRODUCERS)
def test_every_shipped_profile_authors_honest_dropout_rows(producer):
    """Every shipped profile authors a FULL curated ``kind_scores`` row and
    all three ``truth_alignment`` leans for the dropout kind — no silent
    inheritance. The translation risks are the packet's honesty floor:
    NEVER low (this is the aggressive family) — timbaland/quincy/eno
    medium, halee HIGH (her translate-everywhere lens reads a full-layer
    hole as the riskiest move in the widened vocabulary)."""
    raw = _raw(producer)
    _validate(raw, producer)
    row = raw["kind_scores"][DROPOUT]
    for dim in _SCORE_DIMS:
        assert isinstance(row[dim], int), (producer, dim)
    assert row["translation"] == AUTHORED_DROPOUT[producer]["translation"]
    assert row["translation"] != "low", producer  # medium at minimum
    assert row["mono"] == AUTHORED_DROPOUT[producer]["mono"]
    for lean in ("intimate", "big", "neutral"):
        assert raw["truth_alignment"][lean][DROPOUT] \
            == AUTHORED_DROPOUT[producer]["truth"][lean], (producer, lean)


def test_affinity_ordering_is_the_packet_story():
    """The four lenses rank the family the way the packets authored them:
    timbaland (his documented philosophy) > eno (restraint-as-environment,
    P-045) > quincy (moderate-low) > halee (low-affinity) — on the curated
    overall AND on the big/neutral leans."""
    overalls = {p: AUTHORED_DROPOUT[p]["overall"] for p in PRODUCERS}
    assert overalls["timbaland"] > overalls["quincy_jones"] > overalls["halee_ramone"]
    # P-047: eno slots between the two poles — timbaland's negative space
    # is contrast-as-impact, eno's is restraint-as-environment (his second
    # documented philosophy of absence), quincy moderate-low, halee low:
    # timbaland > brian_eno > quincy_jones > halee_ramone, everywhere.
    assert overalls["timbaland"] > overalls["brian_eno"] > overalls["quincy_jones"]
    for lean in ("big", "neutral"):
        t = AUTHORED_DROPOUT["timbaland"]["truth"][lean]
        q = AUTHORED_DROPOUT["quincy_jones"]["truth"][lean]
        h = AUTHORED_DROPOUT["halee_ramone"]["truth"][lean]
        e = AUTHORED_DROPOUT["brian_eno"]["truth"][lean]
        assert t > q > h, lean
        assert t > e > q, lean


@pytest.mark.parametrize("producer", PRODUCERS)
def test_dropout_scores_through_the_real_chain(producer, dense):
    """``score_variant`` consumes each profile's authored dropout row with no
    missing-row fallback: the overall reconstructs from the JSON on disk
    (mean of the 7 authored dims minus the profile's own translation-risk
    penalty) and equals the pinned per-producer value. No nudge/promotion
    row names the kind, so ``score_nudges`` stays absent."""
    prof = load_profile(producer)
    raw = _raw(producer)
    reach = _with_mode(producer, _mode(reach=[DROPOUT]))
    variants = generate_variants({"id": "chorus_lift"}, dense, "reach", reach)
    variant = next(v for v in variants if v["variant_id"] == "chorus_lift_F")
    scores = score_variant(variant, dense, prof)
    row = raw["kind_scores"][DROPOUT]
    expected = round(sum(row[d] for d in _SCORE_DIMS) / 7
                     - raw["risk_penalty"][row["translation"]], 1)
    assert scores["overall_score"] == expected, producer
    assert scores["overall_score"] == AUTHORED_DROPOUT[producer]["overall"]
    assert scores["translation_risk"] == row["translation"]
    assert scores["mono_compatibility"] == row["mono"]
    assert "score_nudges" not in scores, producer


def test_governance_governs_dropout_by_the_authored_leans(dense):
    """The truth_alignment rows are LIVE in governance: under an INTIMATE
    truth halee's authored 48 falls below her align-veto line (50) and the
    dropout variant is vetoed — her lens refuses a hard hole on an intimate
    record; under timbaland's big/neutral leans his authored 90/86 keep it.
    Same variant, same engine — the authored rows decide."""
    halee = load_profile("halee_ramone")
    tim = load_profile("timbaland")
    reach = _with_mode("timbaland", _mode(reach=[DROPOUT]))
    variants = generate_variants({"id": "chorus_lift"}, dense, "reach", reach)
    variant = next(v for v in variants if v["variant_id"] == "chorus_lift_F")

    v_h = dict(variant, scores=score_variant(variant, dense, halee))
    g_h = govern_variant(v_h, [], "intimate", profile=halee)
    assert g_h["emotional_truth_alignment"] == 48
    assert g_h["vetoed"] is True

    v_t = dict(variant, scores=score_variant(variant, dense, tim))
    for lean, align in (("big", 90), ("neutral", 86)):
        g_t = govern_variant(v_t, [], lean, profile=tim)
        assert g_t["emotional_truth_alignment"] == align, lean
        assert g_t["vetoed"] is False, lean


# =========================================================================== #
# THE CAP BINDS against the honest rows — load AND runtime, both directions.
# =========================================================================== #
def test_dropout_reach_cap_binds_at_load_against_each_profiles_row():
    """Authoring dropout reach beyond a mode's posture is a LOUD load-time
    ValueError, against each profile's OWN honest row: halee's HIGH row is
    refused even on a medium mode (and validates on her high-posture
    experimental); timbaland's MEDIUM row is refused on a low mode (and
    validates on his medium-posture negative_space)."""
    halee_med = _raw("halee_ramone")
    halee_med["search_modes"]["spatial_depth"]["reach_kinds"] = [DROPOUT]
    with pytest.raises(ValueError, match="cannot be out-authored"):
        _validate(halee_med, "halee_ramone")

    halee_high = _raw("halee_ramone")
    halee_high["search_modes"]["experimental"]["reach_kinds"] = [DROPOUT]
    _validate(halee_high, "halee_ramone")

    tim_low = _raw("timbaland")
    tim_low["search_modes"]["groove_pocket"]["reach_kinds"] = [DROPOUT]
    with pytest.raises(ValueError, match="cannot be out-authored"):
        _validate(tim_low, "timbaland")

    tim_med = _raw("timbaland")
    tim_med["search_modes"]["negative_space"]["reach_kinds"] = [DROPOUT]
    _validate(tim_med, "timbaland")


def test_dropout_reach_cap_binds_at_runtime_fail_closed(dense):
    """The same cap at emission for loader-bypassing profiles, against each
    profile's own row: halee's HIGH-risk row is refused under a MEDIUM
    posture (surfaced in ``reach_capped``, nothing reads as reached) and
    admitted under high; timbaland's MEDIUM row refused under low, admitted
    under medium."""
    cases = (
        ("halee_ramone", "medium", "high"),
        ("timbaland", "low", "medium"),
    )
    for producer, refused_at, admitted_at in cases:
        capped = _with_mode(producer, _mode(reach=[DROPOUT], allowed=refused_at))
        for pid in PROBLEM_IDS:
            assert generate_variants({"id": pid}, dense, "reach", capped) \
                == generate_variants({"id": pid}, dense), (producer, pid)
        _, fork = _fork(capped, "reach", "chorus_lift", dense)
        assert fork["reach_capped"] == [DROPOUT], producer
        assert fork["reached"] == [], producer

        control = _with_mode(producer, _mode(reach=[DROPOUT], allowed=admitted_at))
        emitted = generate_variants({"id": "chorus_lift"}, dense, "reach", control)
        assert _ids(emitted) == [vid for vid, _ in ENGINE_POOL["chorus_lift"]] \
            + DROPOUT_POOL["chorus_lift"], producer


def test_suppression_beats_dropout_reach(dense):
    """A loader-bypassing mode reaching for AND suppressing the dropout kind
    emits the neutral pool — the admitted variants are removed again and the
    fork report shows it honestly (the loader rejects the authoring form of
    this contradiction outright)."""
    prof = _with_mode("timbaland", _mode(reach=[DROPOUT], suppress=[DROPOUT]))
    emitted = generate_variants({"id": "chorus_lift"}, dense, "reach", prof)
    assert emitted == generate_variants({"id": "chorus_lift"}, dense)
    _, fork = _fork(prof, "reach", "chorus_lift", dense)
    assert fork["reached"] == []
    assert fork["suppressed"] == [DROPOUT]

    raw = _raw("timbaland")
    raw["search_modes"]["experimental"]["reach_kinds"] = [DROPOUT]
    raw["search_modes"]["experimental"]["suppress_kinds"] = [DROPOUT]
    with pytest.raises(ValueError, match="search_modes"):
        _validate(raw, "timbaland")


# =========================================================================== #
# DATA, NOT PRODUCER — the synthetic gate, both directions.
# =========================================================================== #
@pytest.mark.parametrize("base", PRODUCERS)
def test_dropout_reach_is_data_not_producer(base, dense):
    """A synthetic profile built from EACH shipped producer's judgment with
    one reaching mode emits the dropout ids (appended after the pools it
    rides with); the same judgment WITHOUT the reach never sees them —
    including halee, whose HIGH row needs the high posture. The gate is the
    authored ``reach_kinds`` data, not the producer name."""
    reaching = _with_mode(base, _mode(reach=[DROPOUT]))
    for pid in PROBLEM_IDS:
        emitted = generate_variants({"id": pid}, dense, "reach", reaching)
        expected = [vid for vid, _ in ENGINE_POOL[pid]] + DROPOUT_POOL[pid]
        assert _ids(emitted) == expected, (base, pid)

    unreaching = _with_mode(base, _mode(favor=["subtractive_drop"],
                                        suppress=["width_bloom"]))
    for pid in PROBLEM_IDS:
        assert DROPOUT not in _kinds(
            generate_variants({"id": pid}, dense, "reach", unreaching)), (base, pid)


# =========================================================================== #
# THE SHIPPED REACH — Timbaland only, on exactly the user's three modes.
# =========================================================================== #
# The user's authorization, verbatim: "Timbaland: yes — experimental /
# contrast / negative-space modes" (his mode names: ``experimental``,
# ``dramatic_contrast``, ``negative_space``). "Halee/Ramone: no by default.
# Quincy: no by default." — "This keeps it from becoming a general 'remove
# stuff' move."
TIMBALAND_REACH = {
    "conservative": [],
    "groove_pocket": [],
    "negative_space": [DROPOUT],
    "dramatic_contrast": [DROPOUT],
    "low_end_sculpt": [],
    "experimental": [DROPOUT],
}
TIMBALAND_REACHING_MODES = ("experimental", "dramatic_contrast", "negative_space")

DROPOUT_IDS = {"chorus_lift_F", "density_E"}


def test_timbaland_authors_the_pinned_reach_and_it_validates():
    """Timbaland's ``reach_kinds`` per mode IS the pinned authoring — the
    dropout family on exactly the user's three modes, nothing else, nowhere
    else — and the shipped JSON passes full loader validation: his honest
    MEDIUM translation row clears the medium posture of dramatic_contrast /
    negative_space and the high posture of experimental (the authored reach
    lives INSIDE the governance cap)."""
    raw = _raw("timbaland")
    reach = {m: e["reach_kinds"] for m, e in raw["search_modes"].items()}
    assert reach == TIMBALAND_REACH
    _validate(raw, "timbaland")


def test_halee_and_quincy_author_zero_dropout_reach():
    """The other half of the user's decision: NO halee or quincy mode
    reaches the dropout family — read from the JSONs on disk, so any future
    authoring of it must consciously break this pin."""
    for producer in ("halee_ramone", "quincy_jones"):
        for mode_name, entry in _raw(producer)["search_modes"].items():
            assert DROPOUT not in entry.get("reach_kinds", []), \
                (producer, mode_name)


def test_same_mode_same_stems_timbaland_reaches_dropout_halee_quincy_never(
    dense, all_analyzed
):
    """THE HEADLINE DIFFERENTIAL: on the same stems, timbaland emits the
    dropout ids on each of his three authored modes exactly where the
    curated pool holds a variant — while halee and quincy emit ZERO dropout
    ids on EVERY authored mode, the default resolution and an unknown mode.
    The differential is attributable entirely to the authored reach.
    (The shipped roster's dropout authors are timbaland AND brian_eno —
    P-045/P-047 grew the roster past this test's original "only timbaland"
    framing; eno's reaching modes (``generative_drift`` / ``experimental``)
    carry their own emission/protection pins in
    tests/test_four_way_differential.py, so this test pins the
    timbaland-vs-zero-reach half.)"""
    tim = load_profile("timbaland")
    for mode in TIMBALAND_REACHING_MODES:
        out = run_creative_engine(dense, mode, profile=tim)
        assert out["search_mode_declarations"]["reach_kinds"] == [DROPOUT], mode
        for b in out["branches"]:
            ids = set(_ids(b["variants"]))
            assert ids & DROPOUT_IDS \
                == set(DROPOUT_POOL[b["problem_id"]]), (mode, b["problem_id"])
            assert b["mode_fork"]["reached"] \
                == ([DROPOUT] if DROPOUT_POOL[b["problem_id"]] else []), \
                (mode, b["problem_id"])
            assert b["mode_fork"]["reach_capped"] == [], (mode, b["problem_id"])

    for producer in ("halee_ramone", "quincy_jones"):
        prof = load_profile(producer)
        modes = list(_raw(producer)["search_modes"]) + [None, "no_such_mode"]
        for mode in modes:
            for pid in PROBLEM_IDS:
                emitted = generate_variants({"id": pid}, dense, mode, prof)
                assert DROPOUT not in _kinds(emitted), (producer, mode, pid)
                assert not set(_ids(emitted)) & DROPOUT_IDS, (producer, mode, pid)


@pytest.mark.parametrize("name", sorted(PROTECTED_BY_FIXTURE))
@pytest.mark.parametrize("mode", TIMBALAND_REACHING_MODES)
def test_protection_overrides_timbalands_real_authored_reach(name, mode, all_analyzed):
    """The protection filter under the SHIPPED reach, every fixture × every
    reaching mode: no protected name ever appears in a dropout variant's
    targets, and no dropout variant emits empty — the reach admits the
    family, the ENGINE decides what it may touch."""
    res = all_analyzed[name]
    protected = _dropout_protected_names(res)
    out = run_creative_engine(res, mode, profile=load_profile("timbaland"))
    for b in out["branches"]:
        for v in b["variants"]:
            if v["kind"] != DROPOUT:
                continue
            assert v["tracks_affected"], (name, mode, v["variant_id"])
            assert set(v["tracks_affected"]) & protected == set(), \
                (name, mode, v["variant_id"])


def test_timbaland_default_flow_drift_is_conscious_and_bounded(analyzed):
    """THE DEFAULT-MODE DECISION at its blast radius (the quincy P-043
    pattern): timbaland's intimate path (conservative, zero reach) stays
    byte-neutral — no declaration surface at all; his default path
    (dramatic_contrast — the user explicitly authorized reach on his
    default) emits the pinned TIMBALAND_DEFAULT_FLOW_IDS, reports exactly
    the dropout reach on the branches the curated pool touches, and every
    branch WINNER is unmoved — his economy (subtractive_drop 86.7, vocal
    rides, depth cleanup) still outranks the dropout's honest 80.9 by his
    own curated margin, so the drift is candidate-set-only."""
    prof = load_profile("timbaland")
    for name in FIXTURE_NAMES:
        res = analyzed[name]
        mode = pipeline._default_creative_mode(res.project.intent, prof)
        out = run_creative_engine(res, mode, profile=prof)
        emitted = {b["problem_id"]: _ids(b["variants"]) for b in out["branches"]}
        assert emitted == TIMBALAND_DEFAULT_FLOW_IDS[name], name

        if mode == "conservative":  # the intimate path: zero reach
            assert "search_mode_declarations" not in out, name
            for b in out["branches"]:
                assert "mode_fork" not in b, (name, b["problem_id"])
            continue
        assert mode == "dramatic_contrast", name
        assert out["search_mode_declarations"] == {
            "allowed_risk": "medium", "favor_kinds": [], "suppress_kinds": [],
            "reach_kinds": [DROPOUT],
        }
        for b in out["branches"]:
            expected = [DROPOUT] if DROPOUT_POOL[b["problem_id"]] else []
            assert b["mode_fork"]["reached"] == expected, (name, b["problem_id"])
            assert b["mode_fork"]["reach_capped"] == [], (name, b["problem_id"])
            for v in b["variants"]:
                if v["kind"] == DROPOUT:
                    assert v["scores"]["overall_score"] \
                        == AUTHORED_DROPOUT["timbaland"]["overall"]
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in out["branches"]}
        assert winners["chorus_lift"] == "chorus_lift_B", name
        if "density" in winners:
            assert winners["density"] == "density_B", name


def test_committed_trees_carry_the_conscious_drift_and_only_that():
    """The committed sample trees, in committed form: timbaland's tree (the
    CONSCIOUS P-044 drift, regenerated via the verbatim README invocation
    under the full-strength staleness pin) carries the authored reach
    surface — the declarations echo, the chorus_lift dropout candidate
    targeting the BGV Chop bed at his honest 80.9, the reach report — while
    the WINNERS and the doctrine headline (60.9) are unmoved; the reference
    tree carries ZERO reach/dropout bytes and its headline (76.3) is
    unmoved. (Byte-level staleness is pinned in tests/test_sample_refresh.py
    — this pins the drift's SHAPE.)"""
    import json

    tim = json.loads(
        (ROOT / "examples" / "sample_output_timbaland" / "creative.json")
        .read_text(encoding="utf-8"))
    assert tim["search_mode"] == "dramatic_contrast"
    assert tim["search_mode_declarations"] == {
        "allowed_risk": "medium", "favor_kinds": [], "suppress_kinds": [],
        "reach_kinds": [DROPOUT],
    }
    chorus = _branch(tim, "chorus_lift")
    assert chorus["mode_fork"]["reached"] == [DROPOUT]
    f = next(v for v in chorus["variants"] if v["variant_id"] == "chorus_lift_F")
    assert f["kind"] == DROPOUT
    assert f["tracks_affected"] == ["BGV Chop"]
    assert f["changes"] == CHORUS_F_CHANGES
    assert f["reversibility"] == "non_destructive_duplicate_track"
    assert f["scores"]["overall_score"] == AUTHORED_DROPOUT["timbaland"]["overall"]
    assert chorus["winning"]["winning_variant"] == "chorus_lift_B"
    for b in tim["branches"]:
        if b["problem_id"] != "chorus_lift":
            assert not set(_ids(b["variants"])) & DROPOUT_IDS, b["problem_id"]

    tim_ds = json.loads(
        (ROOT / "examples" / "sample_output_timbaland" / "doctrine_score.json")
        .read_text(encoding="utf-8"))
    assert tim_ds["overall_mix_readiness_score"] == 60.9  # doctrine unmoved

    ref = json.loads(
        (ROOT / "examples" / "sample_output" / "creative.json")
        .read_text(encoding="utf-8"))
    assert "search_mode_declarations" not in ref
    for b in ref["branches"]:
        assert "mode_fork" not in b, b["problem_id"]
        assert not set(_ids(b["variants"])) & DROPOUT_IDS, b["problem_id"]
    ref_ds = json.loads(
        (ROOT / "examples" / "sample_output" / "doctrine_score.json")
        .read_text(encoding="utf-8"))
    assert ref_ds["overall_mix_readiness_score"] == 76.3  # reference unmoved
