"""P-045 Commit-1 — ``brian_eno.json``, the FOURTH producer profile: the
proof the aesthetic map widens instead of clustering.

The user's decision, verbatim authority: **Brian Eno**, grounded as
*hand-curated-from-documented-technique -> high confidence* — no claim ships
``high`` unless tied to documented technique / documented production
philosophy, and every inference beyond that is labeled limited/deferred.
Center of gravity: **atmosphere + texture + restraint + generative space** —
"He widens the aesthetic map instead of just adding another point near the
existing cluster," and "he should not simply be 'more reverb' or 'more
ambient.'"

These are Commit-1's guards (the profile's OWN test file — the
test_quincy_profile.py pattern, extended for the schema as it stands after
P-042/P-043/P-044):

1.  **Loads + validates** — ``load_profile("brian_eno")`` passes every
    structural check; the raw JSON carries every required field; the fourth
    producer is DISCOVERED from the producers directory, never registered.
2.  **The honesty stamp** — metadata pinned verbatim.
3.  **The SIX required declarations, explicitly authored** (the P-032g/
    P-032f no-silent-inheritance discipline, plus the P-042 mode surface and
    the P-043/P-044 reach surface):
    (1) loop philosophy — ``protect_iconic_loops: true`` from the documented
    tape-loop/found-voice practice, with the authored static/iconic polarity
    (35.0 / 88.0) on the SHARED detection basis;
    (2) vocal blend philosophy — opt-in at 0.85, the STRICTEST shipped
    floor (voice as instrument/texture in the field);
    (3) default creative mode — his OWN-named ``search_modes`` +
    ``default_creative_mode`` resolving inside his own table;
    (4) mode reach — every mode authors ``allowed_risk`` / ``bias`` /
    ``favor_kinds`` / ``suppress_kinds`` explicitly, pinned verbatim;
    (5) extended-kind reach — every mode authors ``reach_kinds`` explicitly:
    negative_space_dropout on exactly ``generative_drift`` +
    ``experimental`` (contrast through absence — the documented strip-back
    practice), ZERO reach over arrangement_lift / ensemble_rebalance
    anywhere (sectional lift and ensemble hierarchy are not his grammar);
    (6) safety/veto policy — thresholds identical, kill switches a strict
    superset with every safety-relevant line, every comparable structure
    equivalent-or-stricter.
4.  **The authored value system** — all 14 weights pinned verbatim; the
    coherence SHAPE machine-checked against ALL THREE existing profiles: his
    own poles OUTSIDE their envelope (negative space / physical space /
    static balance ABOVE all three; vocal centrality / emotional hierarchy /
    section contrast / dynamic movement BELOW all three), an argmax
    (negative_space) no existing profile has, and a top-2 emphasis pair none
    of them carries.
5.  **Rows everywhere** — curated ``kind_scores`` for ALL 10 kinds and
    ``truth_alignment`` for all 10 kinds x 3 leans, with the dropout row on
    the P-044 honesty floor (never ``low`` translation risk).
6.  **The confidence map, verbatim-pinned** — 6 high / 1 limited /
    8 deferred; every ``high`` reason names its documented-technique basis;
    the deferred entries carry the five standing engine boundaries PLUS
    Eno's own three honest deferrals (textural coherence / generative
    process / ambient patience — concepts with NO existing axis, deferred
    rather than faked from existing axes; the packet's profile-only line).
7.  **Observational language** — zero judgment words across the entire JSON.
8.  **No-aliasing** — fresh loads; mutation cannot reach a reload.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from logic_mix_os import governance
from logic_mix_os.constants import (
    CREATIVE_EXTENDED_KINDS,
    CREATIVE_VARIANT_KINDS,
    TRANSLATION_RISK_LEVELS,
)
from logic_mix_os.doctrine.producer_profile import (
    CONFIDENCE_LEVELS,
    _REQUIRED_DATA_FIELDS,
    _validate,
    load_profile,
)

from test_vocal_type import judgment_word_hits

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_ENO_PATH = _ROOT / "logic_mix_os" / "doctrine" / "producers" / "brian_eno.json"

EXISTING = ("halee_ramone", "timbaland", "quincy_jones")
DROPOUT = "negative_space_dropout"

# --------------------------------------------------------------------------- #
# The authored value system, PINNED VERBATIM.
# --------------------------------------------------------------------------- #
# Atmosphere over foreground urgency / texture as composition / negative
# space / restraint / slow emotional evolution / sonic environment / ensemble
# as FIELD rather than hierarchy. Negative space (1.4) is THE argmax — a pole
# no existing profile has as its heaviest axis; physical space and static
# balance sit above all three (environment + textural weave); vocal
# centrality, emotional hierarchy, section contrast and dynamic movement sit
# BELOW all three (the field has no foreground protagonist and change is
# slow, not sectional) — every axis stays live: de-emphasis, never removal.
E_WEIGHTS = {
    "physical_space_score": 1.3,
    "emotional_hierarchy_score": 0.6,
    "vocal_centrality_score": 0.5,
    "depth_hierarchy_score": 1.1,
    "section_contrast_score": 0.3,
    "static_mix_score": 1.2,
    "dynamic_mix_score": 0.5,
    "beat_identity_score": 0.2,
    "negative_space_score": 1.4,
    "groove_coherence_score": 0.5,
    "rhythmic_surprise_score": 0.2,
    "low_end_motion_score": 0.3,
    "loop_context_score": 0.4,
    "vocal_role_fit_score": 0.6,
}

# The axes where Eno is OUTSIDE the existing three's envelope — ABOVE all
# three (his own poles: the environment, the space, the textural weave).
ABOVE_ALL_THREE = (
    "negative_space_score",   # THE argmax — restraint as the center of gravity
    "physical_space_score",   # depth/space as environment
    "static_mix_score",       # static balance as textural weave
)

# … and BELOW all three (the field posture: no foreground protagonist,
# non-linear time — every existing profile weights section_contrast >= 1.0
# and dynamic_mix >= 0.8; Eno's grammar is not lift-through-sections).
BELOW_ALL_THREE = (
    "vocal_centrality_score",
    "emotional_hierarchy_score",
    "section_contrast_score",
    "dynamic_mix_score",
)

# Eno's authored promotion evidence line (his own voice: a dominating loop is
# generative material — it evolves rather than standing still).
E_PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — treat it as "
    "generative material (source material respected) and let it evolve "
    "instead of standing still"
)

# Eno's own width-crowding nudge line (his authored evidence voice).
E_WIDTH_NUDGE = (
    "vocal_belief -6: stereo image is already width-crowded — more width "
    "dissolves the field into wash"
)

# The FULL authored mode table (declaration 4 + 5), pinned verbatim: every
# mode authors every field — allowed_risk, favor, suppress AND reach.
E_MODE_TABLE = {
    "conservative": {
        "allowed_risk": "low",
        "favor_kinds": ["depth_cleanup"],
        "suppress_kinds": ["width_bloom", "vocal_ride"],
        "reach_kinds": [],
    },
    "ambient_field": {
        "allowed_risk": "low",
        "favor_kinds": [],
        "suppress_kinds": [],
        "reach_kinds": [],
    },
    "texture_bed": {
        "allowed_risk": "low",
        "favor_kinds": ["subtractive_drop"],
        "suppress_kinds": ["drum_room_bloom"],
        "reach_kinds": [],
    },
    "horizontal_time": {
        "allowed_risk": "medium",
        "favor_kinds": [],
        "suppress_kinds": [],
        "reach_kinds": [],
    },
    "generative_drift": {
        "allowed_risk": "medium",
        "favor_kinds": ["loop_deconstruct"],
        "suppress_kinds": ["width_bloom"],
        "reach_kinds": [DROPOUT],
    },
    "experimental": {
        "allowed_risk": "high",
        "favor_kinds": ["subtractive_drop", "depth_cleanup"],
        "suppress_kinds": ["drum_room_bloom"],
        "reach_kinds": [DROPOUT],
    },
}
E_REACHING_MODES = ("generative_drift", "experimental")

# The authored brian_eno confidence map, VERBATIM (the P-031 reviewer
# discipline: this pin is the guard; any edit is a conscious, test-visible
# decision).
E_AUTHORED_MAP = [
    {
        "area": "negative space and restraint interpretation (negative space, static balance as textural weave)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno technique — the subtractive, strip-back practice documented across the Bowie Berlin-trilogy sessions and his published interviews on removing elements, and the Ambient 1: Music for Airports liner-notes manifesto (music 'as ignorable as it is interesting'): absence is composed, so these axes are live and weighted at the top of this profile — negative space above every existing profile as its center of gravity",
    },
    {
        "area": "sonic environment interpretation (physical space, depth as environment)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno technique — the studio-as-instrument practice from his published talks and writing (the studio as a compositional tool) and the treatment-led staging documented across the Bowie and U2/Lanois production collaborations: space is the composition's material, so physical space is weighted above every existing profile and depth reads as environment rather than as ensemble layering",
    },
    {
        "area": "slow evolution over sectional drama (section contrast, dynamic movement as retained measurement)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno technique — the generative-music writings and the Discreet Music liner notes document change that arrives gradually rather than section by section: these axes stay live at deliberately low weights, below every existing profile — the sectional-lift grammar is measured, never removed, and its de-emphasis is this profile's authored posture",
    },
    {
        "area": "the voice as a texture in the field (vocal centrality, emotional hierarchy as retained measurement)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno technique — the treated, instrument-like vocal practice of the Another Green World-era records and the looped wordless voices of Music for Airports: the voice sits inside the environment rather than in front of it, so these axes stay live at weights below every existing profile — a taste-layer de-emphasis only, while every engine-side vocal safety protection stays intact",
    },
    {
        "area": "loop context interpretation (static vs iconic)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno practice — the tape-loop systems of Discreet Music and the Frippertronics-era work treat a loop as generative material, and the found voices of My Life in the Bush of Ghosts function as the record's identity: a static dominant loop reads as unrealized material rather than as an arrested arrangement (authored 35.0, above every existing profile), an iconic-functioning loop is protected as identity (authored 88.0, protect_iconic_loops: true), and every detection floor stays on the shared basis",
    },
    {
        "area": "groove as field texture (beat identity, groove coherence, rhythmic surprise, low-end motion as retained measurement)",
        "level": "high",
        "reason": "hand-curated from documented Brian Eno technique — on the ambient records and in the generative writings the pulse sits inside the environment rather than carrying the record's identity: these axes stay live at this profile's lowest weights — texture, never engine",
    },
    {
        "area": "vocal blend interpretation",
        "level": "limited",
        "reason": "the opt-in is authored from documented technique — the voice treated as an instrument in the field (the Another Green World-era vocal treatments and the looped wordless voices of Music for Airports) — and the gate is live and measured on real exported-stem data: a qualified vocal chop and stack under masking read 85.0 on vocal_role_fit against the reference's 65.0 at this profile's authored 0.85 confidence floor (the strictest shipped); the level stays limited because coverage is bounded: events arise only from the masker-instrument set, info-tier events are emitted but not consumed, and vocal-band events carry no per-track masking risk",
    },
    {
        "area": "textural coherence as its own measurement",
        "level": "deferred",
        "reason": "texture as composition is central to the documented practice, yet whether the beds cohere as one woven surface is not measurable as its own axis on exported stems at doctrine time — the negative-space, static-balance and depth axes are the closest shipped proxies",
    },
    {
        "area": "generative process",
        "level": "deferred",
        "reason": "whether the material behaves as a system — rules, drift, self-variation, the Oblique Strategies working method — is a process property of the session, not measurable on exported stems at doctrine time; the loop-context evolution reading is the closest shipped proxy",
    },
    {
        "area": "ambient patience (time-domain evolution beyond section grain)",
        "level": "deferred",
        "reason": "change on the time scale the documented practice composes for spans whole records, and section analysis is the engine's finest committed time grain — slow evolution beyond that grain is not measurable at doctrine time",
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

# The documented-technique stamp every ``high`` reason must carry (the user's
# grounding standard: hand-curated-from-documented-technique -> high; nothing
# else ships high — LLM-synthesized-as-high is FORBIDDEN).
DOCUMENTED_STAMP = "hand-curated from documented Brian Eno"

# Eno-DISTINCT confidence strings (the leak-guard vocabulary for the
# differential suite; the shared deferred entries are engine boundaries and
# legitimately identical across profiles).
ENO_ONLY_STRINGS = (
    "documented Brian Eno technique",
    "Music for Airports",
)

_SCORE_DIMS = ("technical", "physical_space", "emotional_hierarchy",
               "contrast", "vocal_belief", "excitement", "taste")


def _e_raw() -> dict:
    with open(_ENO_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# 1. LOADS + VALIDATES — every structural check; every required field;
#    dynamically discovered.
# --------------------------------------------------------------------------- #
def test_loads_and_passes_every_structural_check():
    p = load_profile("brian_eno")
    assert p.metadata["name"] == "brian_eno"
    _validate(_e_raw(), "brian_eno")  # must not raise


def test_raw_json_carries_every_required_field():
    raw = _e_raw()
    for f in _REQUIRED_DATA_FIELDS:
        assert f in raw, f"brian_eno.json missing required field {f!r}"
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        assert key in raw["doctrine"]


def test_dynamically_discovered_from_the_producers_directory():
    """The acceptance bar's first clause: the fourth producer is DISCOVERED,
    never registered — the same directory scan the CLI's friendly error uses
    finds all four profiles."""
    from logic_mix_os.cli import _PRODUCERS_DIR

    names = sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json"))
    assert "brian_eno" in names
    for existing in EXISTING:
        assert existing in names


# --------------------------------------------------------------------------- #
# 2. THE HONESTY STAMP — pinned verbatim.
# --------------------------------------------------------------------------- #
def test_metadata_is_the_confirmed_honesty_stamp():
    """Hand-curated from documented technique -> HIGH, per the user's
    grounding standard (NOT LLM-synthesized; nothing reference-track-derived
    ships high)."""
    assert load_profile("brian_eno").metadata == {
        "name": "brian_eno",
        "display_name": "Brian Eno",
        "provenance": "hand-curated-documented",
        "confidence": "high",
        "risk_class": 0,
    }


# --------------------------------------------------------------------------- #
# 3. THE SIX REQUIRED DECLARATIONS — explicitly authored, never inherited.
# --------------------------------------------------------------------------- #
def test_declaration_one_loop_philosophy_authored():
    """REQUIRED declaration 1 — the loop philosophy, in writing, from the
    documented basis: the tape-loop systems (Discreet Music, the
    Frippertronics-era work) treat a loop as generative material, and the
    found voices of My Life in the Bush of Ghosts function as the record's
    identity — so an iconic-functioning loop is PROTECTED
    (``protect_iconic_loops: true``, asserted on the raw file so the value
    is explicit, not defaulted)."""
    raw = _e_raw()
    assert raw["protect_iconic_loops"] is True
    assert load_profile("brian_eno").protect_iconic_loops is True


def test_declaration_one_loop_polarity_authored_on_the_shared_basis():
    """The authored status->score polarity: static 35.0 — ABOVE every
    existing profile (a static loop is not automatically a flaw in an
    ambient grammar: it reads as unrealized generative material, not as
    arrested arrangement — but still below the neutral dominant_evolving
    60.0: the documented preference is for material that EVOLVES) — and
    iconic 88.0 (found material as identity). Every DETECTION floor is
    identical to ALL THREE profiles: one shared basis, never forked."""
    e = load_profile("brian_eno").doctrine["scorers"]["loop_context"]
    others = {p: load_profile(p).doctrine["scorers"]["loop_context"]
              for p in EXISTING}
    assert e["static"] == 35.0
    for p, lc in others.items():
        assert e["static"] > lc["static"], p          # above all three
    assert e["static"] < e["dominant_evolving"]       # evolution still ranks higher
    assert e["iconic"] == 88.0
    for floor in ("width_floor", "transient_lift_floor", "groove_transient_floor",
                  "definition_crest_db", "evolution_rms_floor_db",
                  "evolution_width_floor", "evolution_brightness_floor"):
        for p, lc in others.items():
            assert e[floor] == lc[floor], (p, floor)
    for neutral in ("no_loop", "not_dominant", "dominant_unassessed",
                    "dominant_evolving"):
        for p, lc in others.items():
            assert e[neutral] == lc[neutral], (p, neutral)


def test_declaration_two_vocal_blend_policy_strictest_shipped_floor():
    """REQUIRED declaration 2 — the masking philosophy, in writing: the
    documented voice-as-instrument practice (the Another Green World-era
    treatments, the Airports vocal loops) grounds an opt-in, at 0.85 — the
    STRICTEST shipped confidence floor (above quincy's 0.8 and the 0.75 of
    the other two). Lead protection is engine-fixed and invariant;
    misclassification fails CLOSED toward vocal protection whatever this
    field says."""
    raw = _e_raw()
    assert raw["vocal_blend_policy"] == {
        "acceptable_blend": True,
        "confidence_floor": 0.85,
    }
    e = load_profile("brian_eno")
    for p in EXISTING:
        assert e.vocal_blend_policy["confidence_floor"] > \
            load_profile(p).vocal_blend_policy["confidence_floor"], p


def test_declaration_three_default_creative_mode_and_own_named_modes():
    """REQUIRED declaration 3 — Eno's OWN mode vocabulary (ambient_field /
    texture_bed / horizontal_time / generative_drift — names from his
    documented practice, carried by NO existing profile), his mode-name set
    matching none of the three, and both ``default_creative_mode`` entries
    resolving inside his own table (intimate words -> ambient_field; default
    -> horizontal_time — slow evolution IS his default posture)."""
    e = load_profile("brian_eno")
    names = set(e.search_modes)
    assert names == set(E_MODE_TABLE)
    assert {"ambient_field", "texture_bed", "horizontal_time",
            "generative_drift"} <= names
    for p in EXISTING:
        other = load_profile(p)
        assert names != set(other.search_modes), p
        for own in ("ambient_field", "texture_bed", "horizontal_time",
                    "generative_drift"):
            assert own not in other.search_modes, (p, own)
    dcm = e.default_creative_mode
    assert dcm["intimate_mode"] == "ambient_field"
    assert dcm["default_mode"] == "horizontal_time"
    assert dcm["intimate_mode"] in e.search_modes
    assert dcm["default_mode"] in e.search_modes


def test_declaration_four_every_mode_authors_the_p042_surface_verbatim():
    """REQUIRED declaration 4 (the P-042 surface): every mode authors
    ``allowed_risk`` / ``bias`` / ``favor_kinds`` / ``suppress_kinds``
    EXPLICITLY — the full table is pinned verbatim; every bias is a
    non-empty authored string; every named kind comes from the engine
    vocabulary; the suppressions read as his restraint (width pushes, vocal
    rides and drum-room blooms withheld in the field modes)."""
    raw = _e_raw()
    assert set(raw["search_modes"]) == set(E_MODE_TABLE)
    for mode_name, entry in raw["search_modes"].items():
        pinned = E_MODE_TABLE[mode_name]
        assert entry["allowed_risk"] == pinned["allowed_risk"], mode_name
        assert entry["favor_kinds"] == pinned["favor_kinds"], mode_name
        assert entry["suppress_kinds"] == pinned["suppress_kinds"], mode_name
        assert entry["reach_kinds"] == pinned["reach_kinds"], mode_name
        assert isinstance(entry["bias"], str) and entry["bias"].strip(), mode_name
        for field in ("favor_kinds", "suppress_kinds"):
            for kind in entry[field]:
                assert kind in CREATIVE_VARIANT_KINDS, (mode_name, field, kind)
    # his restraint is authored, not implied: the foreground-urgency moves
    # are suppressed somewhere in his table
    suppressed_anywhere = {k for e in raw["search_modes"].values()
                           for k in e["suppress_kinds"]}
    assert {"width_bloom", "vocal_ride", "drum_room_bloom"} <= suppressed_anywhere


def test_declaration_four_default_flow_modes_author_neutral_declarations():
    """The requirement-8 construction (the P-042 discipline every shipped
    profile follows): his default and intimate modes author favor/suppress
    NEUTRAL — the default flow forks nothing — while at least one
    NON-default mode authors a non-neutral reach, so the fork is real."""
    raw = _e_raw()
    default_flow = {raw["default_creative_mode"]["default_mode"],
                    raw["default_creative_mode"]["intimate_mode"]}
    for mode_name in default_flow:
        entry = raw["search_modes"][mode_name]
        assert entry["favor_kinds"] == [], mode_name
        assert entry["suppress_kinds"] == [], mode_name
        assert entry["reach_kinds"] == [], mode_name
    forking = [m for m, e in raw["search_modes"].items()
               if e["favor_kinds"] or e["suppress_kinds"]]
    assert forking
    assert not default_flow & set(forking)


def test_declaration_five_extended_reach_is_dropout_only_on_two_modes():
    """REQUIRED declaration 5 (the P-043/P-044 surface): every mode authors
    ``reach_kinds`` explicitly. The AUTHORED taste decision, with its
    documented grounding: negative_space_dropout — contrast through absence,
    the documented strip-back practice — on exactly ``generative_drift`` +
    ``experimental`` (exploration, not aggression; NEVER the default flow).
    arrangement_lift / ensemble_rebalance reach: ZERO everywhere — sectional
    lift and ensemble hierarchy are the arrangement-led profile's poles, not
    his grammar (authored [] rather than justified from documented
    technique)."""
    raw = _e_raw()
    reach = {m: e["reach_kinds"] for m, e in raw["search_modes"].items()}
    assert reach == {m: pinned["reach_kinds"]
                     for m, pinned in E_MODE_TABLE.items()}
    reaching = [m for m, r in reach.items() if r]
    assert sorted(reaching) == sorted(E_REACHING_MODES)
    for mode_name, r in reach.items():
        assert "arrangement_lift" not in r, mode_name
        assert "ensemble_rebalance" not in r, mode_name
        for kind in r:
            assert kind in CREATIVE_EXTENDED_KINDS, (mode_name, kind)


def test_declaration_five_dropout_reach_lives_inside_the_governance_cap():
    """The cap binds against HIS honest row (medium translation risk): the
    shipped JSON validates (both reaching modes carry medium/high posture),
    and authoring the same reach on a LOW-posture mode is a LOUD load-time
    ValueError — the cap is governance and cannot be out-authored. Control:
    the same reach validates on his medium-posture horizontal_time."""
    _validate(_e_raw(), "brian_eno")  # the shipped reach is inside the cap

    for low_mode in ("texture_bed", "ambient_field", "conservative"):
        over = _e_raw()
        over["search_modes"][low_mode]["reach_kinds"] = [DROPOUT]
        with pytest.raises(ValueError, match="cannot be out-authored"):
            _validate(over, "brian_eno")

    control = _e_raw()
    control["search_modes"]["horizontal_time"]["reach_kinds"] = [DROPOUT]
    _validate(control, "brian_eno")


def test_declaration_six_veto_thresholds_identical_and_not_weaker():
    """REQUIRED declaration 6 — the veto surface is UNCHANGED, not merely
    not-weaker: identical reject/veto/fallback lines across all FOUR
    profiles."""
    e = load_profile("brian_eno").veto_thresholds
    assert e == {"reject_below": 45, "align_veto_below": 50,
                 "align_fallback": 75}
    for p in EXISTING:
        assert e == load_profile(p).veto_thresholds, p


def test_declaration_six_kill_switches_superset_with_every_safety_line():
    """Equivalent-or-stricter, literally: every reference aesthetic switch is
    present verbatim (including the vocal-intelligibility and stock-loop
    lines — the safety-relevant ones), plus Eno's own field-first
    additions."""
    e = load_profile("brian_eno").aesthetic_kill_switches
    ref = load_profile("halee_ramone").aesthetic_kill_switches
    assert set(ref) <= set(e)
    for line in (
        "Never make the lead vocal less intelligible unless explicitly approved.",
        "Never allow a stock loop to dominate the song identity by accident.",
        "Never widen the full mix to solve chorus lift.",
        "Never chase reference loudness at the mix stage.",
    ):
        assert line in e, line
    assert len(e) > len(ref)  # his own additions exist


def test_declaration_six_comparable_safety_structures_not_weaker():
    """Structure by structure (the P-032h idiom): risk penalties, both
    creative caps, the taste clamp, the intimate-width penalty, the retained
    width veto, the nudge penalties, the blend confidence floor, and the
    promotion reward — none weaker than the reference."""
    e = load_profile("brian_eno")
    ref = load_profile("halee_ramone")
    assert e.risk_penalty == ref.risk_penalty
    assert e.creative_nudge_cap == ref.creative_nudge_cap
    assert e.creative_promotion_cap == ref.creative_promotion_cap
    assert e.taste_max_delta <= ref.taste_max_delta
    assert (e.taste_triangle["intimate_width_penalty"]
            >= ref.taste_triangle["intimate_width_penalty"])
    # the vocal-safety dim stays inside the emotion blend
    assert "vocal_belief_score" in e.taste_triangle["emotion_dims"]
    # the intimate-width veto is retained, not relaxed past the veto line
    assert (e.truth_alignment["intimate"]["width_bloom"]
            < e.veto_thresholds["align_veto_below"])
    # nudge rows: same (kinds, evidence, dim) coverage; penalties >= reference
    def rows(table):
        return {(frozenset(r["kinds"]), r["evidence"], r["dim"]): r["delta"]
                for r in table}
    e_rows, ref_rows = rows(e.nudge_table), rows(ref.nudge_table)
    assert set(e_rows) == set(ref_rows)
    for key, ref_delta in ref_rows.items():
        assert e_rows[key] <= ref_delta, f"nudge {key} weaker than reference"
    # the blend gate's dial: the floor is never lowered
    assert (e.vocal_blend_policy["confidence_floor"]
            >= ref.vocal_blend_policy["confidence_floor"])
    # the promotion reward is not enlarged
    assert (sum(r["delta"] for r in e.promotion_table)
            <= sum(r["delta"] for r in ref.promotion_table))


def test_risk_class_semantics_unchanged():
    assert load_profile("brian_eno").metadata["risk_class"] == 0
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


# --------------------------------------------------------------------------- #
# 4. THE AUTHORED VALUE SYSTEM — pinned verbatim; the coherence shape.
# --------------------------------------------------------------------------- #
def test_weights_are_the_authored_value_system_verbatim():
    assert load_profile("brian_eno").doctrine["weights"] == E_WEIGHTS


def test_coherent_pole_outside_the_existing_envelope():
    """The shape, machine-checked against ALL THREE existing profiles: on
    his own poles Eno is NOT inside their envelope — three axes strictly
    ABOVE all three, four axes strictly BELOW all three (well past the
    at-least-2 requirement floor) — and every weight > 0: de-emphasis is
    never removal (the beat, the groove and the sections stay measured)."""
    e = load_profile("brian_eno").doctrine["weights"]
    others = [load_profile(p).doctrine["weights"] for p in EXISTING]
    outside = 0
    for key in ABOVE_ALL_THREE:
        assert all(e[key] > w[key] for w in others), (
            f"{key} is not an Eno pole (must exceed all three profiles)")
        outside += 1
    for key in BELOW_ALL_THREE:
        assert all(e[key] < w[key] for w in others), (
            f"{key} is not an Eno pole (must sit below all three profiles)")
        outside += 1
    assert outside >= 2  # the requirement floor, cleared 7 times over
    assert all(w > 0 for w in e.values())


def test_argmax_and_top2_emphasis_no_existing_profile_has():
    """The axis-emphasis ordering is HIS OWN: Eno's single heaviest axis is
    negative_space — verified NOT the argmax of any existing profile
    (halee_ramone peaks on emotional hierarchy / vocal centrality, timbaland
    on beat identity, quincy on depth hierarchy) — and his top-2
    {negative space, physical space} is an emphasis pair none of them has."""
    e = load_profile("brian_eno").doctrine["weights"]
    assert max(e, key=e.get) == "negative_space_score"

    def top2(w):
        return set(sorted(w, key=w.get, reverse=True)[:2])

    for p in EXISTING:
        w = load_profile(p).doctrine["weights"]
        argmaxes = {k for k, v in w.items() if v == max(w.values())}
        assert "negative_space_score" not in argmaxes, p
        assert top2(e) != top2(w), p
    assert top2(e) == {"negative_space_score", "physical_space_score"}


def test_weights_copy_no_existing_profile():
    e = load_profile("brian_eno").doctrine["weights"]
    for p in EXISTING:
        assert e != load_profile(p).doctrine["weights"], p


def test_every_non_authored_scorer_parameter_stays_on_the_shared_basis():
    """Attributability by construction: outside the two authored divergence
    channels (the loop_context polarity; the blend gate, which lives in
    ``vocal_blend_policy``, not in scorer constants) every scorer parameter,
    baseline and penalty coefficient equals the shared basis — so every
    component score divergence traces to an AUTHORED value, never to a
    forked measurement constant."""
    e = load_profile("brian_eno").doctrine
    ref = load_profile("halee_ramone").doctrine
    assert e["baselines"] == ref["baselines"]
    assert e["penalty_coeffs"] == ref["penalty_coeffs"]
    for fn, params in e["scorers"].items():
        if fn == "loop_context":
            continue
        assert params == ref["scorers"][fn], f"scorer {fn} forked from the shared basis"


# --------------------------------------------------------------------------- #
# 5. ROWS EVERYWHERE — all 10 kinds, all 3 leans, honest risks.
# --------------------------------------------------------------------------- #
def test_kind_scores_cover_all_ten_kinds_with_full_rows():
    """Curated rows for the ENTIRE move vocabulary — the original seven AND
    the three extended kinds — each with all 7 integer dims and honest
    translation/mono risks from the shared scale. No silent inheritance."""
    raw = _e_raw()
    assert set(raw["kind_scores"]) == set(CREATIVE_VARIANT_KINDS)
    for kind, row in raw["kind_scores"].items():
        for dim in _SCORE_DIMS:
            assert isinstance(row[dim], int), (kind, dim)
        assert row["translation"] in TRANSLATION_RISK_LEVELS, kind
        assert row["mono"] in TRANSLATION_RISK_LEVELS, kind


def test_truth_alignment_covers_all_ten_kinds_in_all_three_leans():
    raw = _e_raw()
    for lean in ("intimate", "big", "neutral"):
        assert set(raw["truth_alignment"][lean]) == set(CREATIVE_VARIANT_KINDS), lean
        for kind, v in raw["truth_alignment"][lean].items():
            assert isinstance(v, int), (lean, kind)


def test_dropout_row_is_his_highest_affinity_extended_kind_at_honest_risk():
    """The dropout row through his lens: contrast through absence IS his
    center, so the taste (92) and contrast (92) dims lead — but the
    translation risk stays MEDIUM (the P-044 honesty floor: never ``low``
    for the aggressive family). Reconstructed from the JSON: dropout's
    curated overall (78.9) outranks both other extended kinds under his own
    table (arrangement_lift 72.0, ensemble_rebalance 62.6 — sectional lift
    and ensemble hierarchy are not his grammar)."""
    raw = _e_raw()
    row = raw["kind_scores"][DROPOUT]
    assert row["translation"] == "medium"
    assert row["translation"] != "low"

    def overall(kind):
        r = raw["kind_scores"][kind]
        return round(sum(r[d] for d in _SCORE_DIMS) / 7
                     - raw["risk_penalty"][r["translation"]], 1)

    assert overall(DROPOUT) == 78.9
    assert overall("arrangement_lift") == 72.0
    assert overall("ensemble_rebalance") == 62.6
    assert overall(DROPOUT) > overall("arrangement_lift")
    assert overall(DROPOUT) > overall("ensemble_rebalance")
    # restraint IS subtractive: his top curated move overall is the
    # subtractive economy, above every bloom move
    assert overall("subtractive_drop") == 86.9
    assert overall("subtractive_drop") > overall("width_bloom")
    assert overall("subtractive_drop") > overall("drum_room_bloom")


def test_bloom_moves_are_low_taste_through_his_lens():
    """'He should not simply be more reverb': the size/urgency moves sit at
    the FLOOR of his taste column — drum_room_bloom (56) is the strict
    minimum and width_bloom (58) ties only the out-of-grammar sectional
    lift — while restraint (subtractive_drop 92, tied by the dropout's 92)
    leads and the environment move (depth_cleanup 86) sits just below."""
    scores = _e_raw()["kind_scores"]
    tastes = {kind: row["taste"] for kind, row in scores.items()}
    assert tastes["drum_room_bloom"] == min(tastes.values())
    for kind, taste in tastes.items():
        if kind in ("width_bloom", "drum_room_bloom"):
            continue
        assert taste >= tastes["width_bloom"], kind
    assert tastes["subtractive_drop"] == max(tastes.values())
    assert tastes["subtractive_drop"] > tastes["width_bloom"]
    assert tastes["depth_cleanup"] > tastes["width_bloom"]


# --------------------------------------------------------------------------- #
# 6. THE CONFIDENCE MAP — verbatim pin; the honesty split machine-checked.
# --------------------------------------------------------------------------- #
def test_eno_confidence_map_verbatim():
    """The full authored map, pinned verbatim in authoring order — THE guard
    (validation accepts silent rewording; the pin does not)."""
    assert load_profile("brian_eno").confidence_map == E_AUTHORED_MAP


def test_confidence_map_is_structurally_valid():
    cmap = load_profile("brian_eno").confidence_map
    assert cmap
    for entry in cmap:
        assert entry["level"] in CONFIDENCE_LEVELS


def test_confidence_level_distribution():
    """6 high (the five interpretation areas + the loop polarity) / 1 limited
    (vocal blend — live, measured, coverage-bounded) / 8 deferred (the five
    standing engine boundaries + Eno's own three honest deferrals)."""
    levels = [e["level"] for e in load_profile("brian_eno").confidence_map]
    assert levels.count("high") == 6
    assert levels.count("limited") == 1
    assert levels.count("deferred") == 8


def test_every_high_entry_names_its_documented_technique_basis():
    """The user's grounding standard as a machine check: NO ``high`` entry
    ships without naming its documented-technique basis (the Airports
    manifesto, the studio-as-instrument writings, the generative-music
    writings, the tape-loop systems, the documented Bowie/U2
    collaborations) — anything not tied to documented technique is
    limited/deferred by construction."""
    for entry in load_profile("brian_eno").confidence_map:
        if entry["level"] == "high":
            assert DOCUMENTED_STAMP in entry["reason"], entry["area"]


def test_limited_blend_entry_matches_the_authored_policy():
    """The limited entry states its documented basis (the voice as an
    instrument in the field), its live measurement (85.0 vs 65.0 on real
    exported-stem data), his OWN authored floor (0.85) and the real coverage
    bounds — and it corresponds to the policy the profile actually
    authors."""
    p = load_profile("brian_eno")
    limited = [e for e in p.confidence_map if e["level"] == "limited"]
    assert limited == [E_AUTHORED_MAP[6]]
    reason = limited[0]["reason"]
    assert "Another Green World" in reason
    assert "measured on real exported-stem data" in reason
    assert "85.0" in reason and "65.0" in reason
    assert "0.85 confidence floor" in reason
    assert p.vocal_blend_policy == {"acceptable_blend": True,
                                    "confidence_floor": 0.85}


def test_deferred_entries_carry_the_standing_boundaries_plus_his_own_three():
    """The five standing engine boundaries ship verbatim (they are engine
    limits, not taste), PLUS Eno's own three honest deferrals — the concepts
    the user named that have NO existing axis: textural coherence as its own
    measurement, generative process, and ambient patience beyond the section
    grain. Deferred, never faked from existing axes and never a schema
    change (the packet's profile-only line)."""
    deferred = [e for e in load_profile("brian_eno").confidence_map
                if e["level"] == "deferred"]
    assert deferred == E_AUTHORED_MAP[7:]
    areas = " | ".join(e["area"] for e in deferred)
    for own in ("textural coherence", "generative process", "ambient patience"):
        assert own in areas, f"Eno's own deferral {own!r} missing"
    for standing in ("cultural loop recognizability", "true hook recurrence",
                     "motif provenance", "fingerprint typing",
                     "kick/sub temporal interlock", "per-section true-sub movement"):
        assert standing in areas, f"deferral {standing!r} missing"
    tim_deferred = [e for e in load_profile("timbaland").confidence_map
                    if e["level"] == "deferred"]
    assert deferred[3:] == tim_deferred  # the shared engine boundaries, verbatim


def test_high_claims_are_consistent_with_the_machine_facts():
    """No high entry overclaims: the 'above every existing profile' areas ARE
    weighted above all three; the 'below every existing profile' areas ARE
    below; the loop-polarity entry states the exact authored numbers and the
    exact authored protection flag."""
    e = load_profile("brian_eno").doctrine["weights"]
    others = [load_profile(p).doctrine["weights"] for p in EXISTING]
    for key in ("negative_space_score", "static_mix_score"):        # entry 1
        assert all(e[key] > w[key] for w in others), key
    assert all(e["physical_space_score"] > w["physical_space_score"]
               for w in others)                                     # entry 2
    for key in ("section_contrast_score", "dynamic_mix_score"):     # entry 3
        assert all(e[key] < w[key] for w in others), key
    for key in ("vocal_centrality_score", "emotional_hierarchy_score"):  # entry 4
        assert all(e[key] < w[key] for w in others), key
    lc = load_profile("brian_eno").doctrine["scorers"]["loop_context"]
    assert lc["static"] == 35.0 and lc["iconic"] == 88.0            # entry 5
    assert load_profile("brian_eno").protect_iconic_loops is True   # entry 5
    groove = ("beat_identity_score", "rhythmic_surprise_score")     # entry 6
    lowest = min(e.values())
    assert all(e[key] == lowest for key in groove)


def test_whole_profile_language_is_observational():
    """USER-MANDATED: zero judgment words across the ENTIRE authored JSON."""
    blob = _ENO_PATH.read_text(encoding="utf-8").lower()
    hits = judgment_word_hits(blob)
    assert not hits, f"judgment word(s) {hits} in brian_eno.json"


# --------------------------------------------------------------------------- #
# 7. HIS OWN VOICE — the authored evidence lines.
# --------------------------------------------------------------------------- #
def test_promotion_reason_is_his_own_authored_voice():
    e = load_profile("brian_eno")
    assert [r["reason"] for r in e.promotion_table] == [E_PROMOTION_REASON]


def test_nudge_reasons_are_his_own_authored_voice():
    e = load_profile("brian_eno")
    reasons = [r["reason"] for r in e.nudge_table]
    assert E_WIDTH_NUDGE in reasons
    for p in EXISTING:
        other_reasons = [r["reason"] for r in load_profile(p).nudge_table]
        assert not set(reasons) & set(other_reasons), p


# --------------------------------------------------------------------------- #
# 8. NO-ALIASING — fresh loads; mutation cannot reach a reload.
# --------------------------------------------------------------------------- #
def test_loads_are_fresh_mutation_cannot_reach_a_reload_or_other_profiles():
    e = load_profile("brian_eno")
    e.doctrine["weights"]["negative_space_score"] = 99.0
    e.confidence_map[0]["level"] = "deferred"
    e.aesthetic_kill_switches.append("mutated")
    e.search_modes["experimental"]["reach_kinds"].append("arrangement_lift")
    assert load_profile("brian_eno").doctrine["weights"] == E_WEIGHTS
    assert load_profile("brian_eno").confidence_map == E_AUTHORED_MAP
    assert "mutated" not in load_profile("brian_eno").aesthetic_kill_switches
    assert load_profile("brian_eno").search_modes["experimental"]["reach_kinds"] \
        == [DROPOUT]
    assert load_profile("halee_ramone").doctrine["weights"]["negative_space_score"] == 0
    assert load_profile("timbaland").doctrine["weights"]["negative_space_score"] == 1.2
    assert load_profile("quincy_jones").doctrine["weights"]["negative_space_score"] == 0.6
