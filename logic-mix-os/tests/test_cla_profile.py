"""P-050 Commit-1 — ``chris_lord_alge.json``, the FIFTH producer profile: the
IMPACT / EXCITEMENT pole, and the hardest test the safety doctrine has faced.

The user's decision, verbatim authority: **Chris Lord-Alge**, grounded as
*hand-curated-from-documented-technique -> high confidence*. The pole is
IMPACT / EXCITEMENT — energy-forward, loud/present, punchy, dense,
commit-and-slam, the anti-Eno: he FILLS space where Eno carves it, chases
IMPACT where Quincy arranges, is modern/loud/forward where Halee/Ramone is
vintage/intimate, and where Timbaland pockets the groove CLA slams the
section.

THE CENTRAL STRESS-TEST (why CLA matters): his whole identity — aggressive
loudness, heavy compression, density — is the exact thing the safety layer
restrains. The doctrine holds and the profile bends around it. His
loudness-forward identity is expressed ONLY through weighting
(section-contrast / beat-identity / vocal-centrality / dynamic-movement /
low-end-motion UP; negative-space / physical-space / depth DOWN) and
recommendation LANGUAGE — and the safety surface is INVARIANT: the loudness
kill-switch "Never chase reference loudness at the mix stage." is kept
VERBATIM, the veto thresholds are unchanged, every cap is equal-or-stricter,
and loudness maximization is DEFERRED out of scope at doctrine time by design
(a loudness-maximalist who still cannot weaken the loudness rail).

These are Commit-1's guards (the profile's OWN test file — the
test_eno_profile.py pattern, grown for the schema as it stands after
P-042/P-043/P-044/P-045):

1.  Loads + validates; every required field; dynamically discovered.
2.  The honesty stamp, pinned verbatim.
3.  The SIX required declarations, explicitly authored.
4.  The authored value system — all 14 weights pinned; the coherence shape
    machine-checked against ALL FOUR existing profiles (his poles outside
    their envelope; an argmax — section_contrast — no existing profile has).
5.  Rows everywhere — 10 kinds x (kind_scores + 3 truth leans), dropout on
    the P-044 honesty floor.
6.  The confidence map, verbatim-pinned; 6 high / 1 limited / 8 deferred.
7.  Observational language — zero judgment words across the whole JSON.
8.  No-aliasing — fresh loads; mutation cannot reach a reload.
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
_CLA_PATH = _ROOT / "logic_mix_os" / "doctrine" / "producers" / "chris_lord_alge.json"

EXISTING = ("halee_ramone", "timbaland", "quincy_jones", "brian_eno")
DROPOUT = "negative_space_dropout"
LOUDNESS_KILL_SWITCH = "Never chase reference loudness at the mix stage."

# --------------------------------------------------------------------------- #
# The authored value system, PINNED VERBATIM.
# --------------------------------------------------------------------------- #
# Impact over restraint / vocal on top and loud / punchy forward drums /
# section-contrast and dynamic movement as the center of gravity / density and
# forward staging over space and depth. section_contrast (1.7) is THE argmax —
# a pole no existing profile has as its heaviest axis (no existing producer
# even tops section_contrast). Every axis stays live: de-emphasis, never
# removal.
C_WEIGHTS = {
    "physical_space_score": 0.4,
    "emotional_hierarchy_score": 0.7,
    "vocal_centrality_score": 1.3,
    "depth_hierarchy_score": 0.4,
    "section_contrast_score": 1.7,
    "static_mix_score": 0.7,
    "dynamic_mix_score": 1.3,
    "beat_identity_score": 1.5,
    "negative_space_score": 0.2,
    "groove_coherence_score": 0.5,
    "rhythmic_surprise_score": 0.3,
    "low_end_motion_score": 1.2,
    "loop_context_score": 0.5,
    "vocal_role_fit_score": 0.8,
}

# The axes where CLA is OUTSIDE the existing four's envelope — ABOVE all four
# (his own poles: impact, punch, the loud forward voice, energy movement).
ABOVE_ALL_FOUR = (
    "section_contrast_score",   # THE argmax — impact as the center of gravity
    "beat_identity_score",      # punchy forward drums
    "vocal_centrality_score",   # the vocal on top and loud
    "dynamic_mix_score",        # energy movement / impact
    "low_end_motion_score",     # the low end drives with weight
    "vocal_role_fit_score",     # vocal-forward
)

# … and BELOW all four (the density/forward posture: filled not carved, up
# front not deep or spacious).
BELOW_ALL_FOUR = (
    "physical_space_score",     # forward and present, not spacious
    "depth_hierarchy_score",    # flat-forward, everything up front
    "static_mix_score",         # dynamic and energy, not static balance
)

# CLA's own promotion evidence line (his own voice: commit to a dominating
# loop and drive it forward as the record's energy).
C_PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — commit to it and "
    "drive it forward as the record's energy (source material respected) "
    "rather than leaving it static"
)

# CLA's own width-crowding nudge line (his authored evidence voice).
C_WIDTH_NUDGE = (
    "vocal_belief -6: stereo image is already width-crowded — more width "
    "trades the forward punch for size"
)

# The FULL authored mode table (declaration 4 + 5), pinned verbatim: every
# mode authors every field — allowed_risk, favor, suppress AND reach.
C_MODE_TABLE = {
    "conservative": {
        "allowed_risk": "low",
        "favor_kinds": [],
        "suppress_kinds": ["subtractive_drop"],
        "reach_kinds": [],
    },
    "front_and_center": {
        "allowed_risk": "low",
        "favor_kinds": [],
        "suppress_kinds": [],
        "reach_kinds": [],
    },
    "commit_and_slam": {
        "allowed_risk": "medium",
        "favor_kinds": [],
        "suppress_kinds": [],
        "reach_kinds": [],
    },
    "drum_slam": {
        "allowed_risk": "medium",
        "favor_kinds": ["drum_room_bloom"],
        "suppress_kinds": ["subtractive_drop"],
        "reach_kinds": [],
    },
    "big_chorus": {
        "allowed_risk": "medium",
        "favor_kinds": ["width_bloom"],
        "suppress_kinds": [],
        "reach_kinds": ["arrangement_lift"],
    },
    "experimental": {
        "allowed_risk": "high",
        "favor_kinds": ["width_bloom", "drum_room_bloom"],
        "suppress_kinds": ["subtractive_drop"],
        "reach_kinds": ["arrangement_lift"],
    },
}
C_REACHING_MODES = ("big_chorus", "experimental")

# The authored chris_lord_alge confidence map, VERBATIM (the P-031 reviewer
# discipline: this pin is the guard; any edit is a conscious, test-visible
# decision).
C_AUTHORED_MAP = [
    {
        "area": "vocal-forward interpretation (vocal centrality, vocal role fit)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the vocal-always-on-top-and-loud practice encoded in the Waves CLA Vocals signature chain and stated across his Mix With The Masters / PLAP masterclasses and his Sound on Sound / EQ / Mix interviews: the lead sits in front and present, so these axes are live and weighted above every existing profile",
    },
    {
        "area": "drum punch and beat-identity interpretation (beat identity, low-end motion)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the parallel-crushed drum practice encoded in the Waves CLA Drums signature chain and demonstrated in the MWTM/PLAP masterclasses (Green Day, My Chemical Romance): the kit lands forward and the low end drives with weight, so these axes are live and weighted above every existing profile",
    },
    {
        "area": "section contrast and impact interpretation (section contrast, dynamic movement)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the commit-and-slam, big-chorus impact documented across the discography (Green Day, Muse, Springsteen, U2) and his published interviews: the chorus lands bigger than the verse, so section contrast is this profile's center of gravity, weighted above every existing profile",
    },
    {
        "area": "density and forward staging as retained measurement (physical space, depth hierarchy, negative space)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the fill-the-space, forward-and-present staging documented across his mixes and interviews: the record is dense and up front rather than deep or spacious, so these axes stay live at this profile's lowest weights — the anti-restraint posture, a taste-layer de-emphasis and never a removal",
    },
    {
        "area": "loop context interpretation (static vs iconic)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the modern-production respect for a signature hook as the song's identity: a static dominant loop reads as material to commit to and drive (authored 18.0), an iconic-functioning loop is protected as identity (authored 92.0, protect_iconic_loops: true), and every detection floor stays on the shared basis",
    },
    {
        "area": "move translation risk (the per-move translation-risk column)",
        "level": "high",
        "reason": "hand-curated from documented Chris Lord-Alge technique — the mixes-carry-the-same-impact-on-every-system value stated across his interviews and the Waves signature-chain notes: it is expressed as the per-move translation-risk column, so the width and dropout moves carry their honest translation risk in this profile's curated rows",
    },
    {
        "area": "vocal blend interpretation",
        "level": "limited",
        "reason": "the opt-in is authored from documented technique — the loud, stacked background-vocal wall behind a forward lead — and the gate is live and measured on real exported-stem data: a qualified vocal chop and stack under masking read 85.0 on vocal_role_fit against the reference's 65.0 at this profile's authored 0.85 confidence floor (the strictest shipped); the level stays limited because coverage is bounded: events arise only from the masker-instrument set, info-tier events are emitted but not consumed, and vocal-band events carry no per-track masking risk",
    },
    {
        "area": "loudness maximization",
        "level": "deferred",
        "reason": "absolute program loudness / LUFS is deliberately NOT a doctrine axis and stays a safety concern (the loudness kill-switch is retained verbatim): loudness maximization is out of scope at doctrine time by design, expressed as weighting and language rather than measured as taste",
    },
    {
        "area": "saturation and harmonic energy as its own measurement",
        "level": "deferred",
        "reason": "whether harmonic saturation adds perceived energy is not measurable as its own axis on exported stems at doctrine time; the excitement kind-score dims are the closest shipped proxy",
    },
    {
        "area": "whole-mix translation across playback systems",
        "level": "deferred",
        "reason": "whether the finished mix lands with the same impact on every playback system is a multi-system property not measurable on exported stems at doctrine time; the per-move translation-risk column is the closest shipped proxy",
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
DOCUMENTED_STAMP = "hand-curated from documented Chris Lord-Alge"

# CLA-DISTINCT confidence strings (the leak-guard vocabulary for the
# differential suite; the shared deferred entries are engine boundaries and
# legitimately identical across profiles).
CLA_ONLY_STRINGS = (
    "documented Chris Lord-Alge technique",
    "Waves CLA",
)

_SCORE_DIMS = ("technical", "physical_space", "emotional_hierarchy",
               "contrast", "vocal_belief", "excitement", "taste")


def _c_raw() -> dict:
    with open(_CLA_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _overall(raw, kind):
    r = raw["kind_scores"][kind]
    return round(sum(r[d] for d in _SCORE_DIMS) / 7
                 - raw["risk_penalty"][r["translation"]], 1)


# --------------------------------------------------------------------------- #
# 1. LOADS + VALIDATES.
# --------------------------------------------------------------------------- #
def test_loads_and_passes_every_structural_check():
    p = load_profile("chris_lord_alge")
    assert p.metadata["name"] == "chris_lord_alge"
    _validate(_c_raw(), "chris_lord_alge")  # must not raise


def test_raw_json_carries_every_required_field():
    raw = _c_raw()
    for f in _REQUIRED_DATA_FIELDS:
        assert f in raw, f"chris_lord_alge.json missing required field {f!r}"
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        assert key in raw["doctrine"]


def test_dynamically_discovered_from_the_producers_directory():
    """The fifth producer is DISCOVERED, never registered — the same directory
    scan the CLI's friendly error uses finds all five profiles."""
    from logic_mix_os.cli import _PRODUCERS_DIR

    names = sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json"))
    assert "chris_lord_alge" in names
    for existing in EXISTING:
        assert existing in names


# --------------------------------------------------------------------------- #
# 2. THE HONESTY STAMP.
# --------------------------------------------------------------------------- #
def test_metadata_is_the_confirmed_honesty_stamp():
    assert load_profile("chris_lord_alge").metadata == {
        "name": "chris_lord_alge",
        "display_name": "Chris Lord-Alge",
        "provenance": "hand-curated-documented",
        "confidence": "high",
        "risk_class": 0,
    }


# --------------------------------------------------------------------------- #
# 3. THE SIX REQUIRED DECLARATIONS.
# --------------------------------------------------------------------------- #
def test_declaration_one_loop_philosophy_authored():
    """REQUIRED declaration 1 — the loop philosophy, in writing: the
    modern-production respect for a signature hook as the song's identity —
    so an iconic-functioning loop is PROTECTED (``protect_iconic_loops:
    true``, asserted on the raw file so the value is explicit, not
    defaulted)."""
    raw = _c_raw()
    assert raw["protect_iconic_loops"] is True
    assert load_profile("chris_lord_alge").protect_iconic_loops is True


def test_declaration_one_loop_polarity_authored_on_the_shared_basis():
    """The authored status->score polarity: static 18.0 — above the reference
    (a static loop is material to commit to and drive, not a flaw) — and
    iconic 92.0 (a signature hook protected as identity). Every DETECTION
    floor is identical to ALL FOUR profiles: one shared basis, never
    forked."""
    c = load_profile("chris_lord_alge").doctrine["scorers"]["loop_context"]
    others = {p: load_profile(p).doctrine["scorers"]["loop_context"]
              for p in EXISTING}
    assert c["static"] == 18.0
    assert c["iconic"] == 92.0
    assert c["static"] < c["dominant_evolving"]  # a driven loop still ranks below evolving
    for floor in ("width_floor", "transient_lift_floor", "groove_transient_floor",
                  "definition_crest_db", "evolution_rms_floor_db",
                  "evolution_width_floor", "evolution_brightness_floor"):
        for p, lc in others.items():
            assert c[floor] == lc[floor], (p, floor)
    for neutral in ("no_loop", "not_dominant", "dominant_unassessed",
                    "dominant_evolving"):
        for p, lc in others.items():
            assert c[neutral] == lc[neutral], (p, neutral)


def test_declaration_two_vocal_blend_policy_strictest_shipped_floor():
    """REQUIRED declaration 2 — the masking philosophy, in writing: the loud
    stacked background-vocal wall behind a forward lead grounds an opt-in, at
    0.85 — the STRICTEST shipped confidence floor (tied with eno's 0.85,
    above quincy's 0.8 and the 0.75 of the reference). Lead protection is
    engine-fixed and invariant; misclassification fails CLOSED toward vocal
    protection whatever this field says."""
    raw = _c_raw()
    assert raw["vocal_blend_policy"] == {
        "acceptable_blend": True,
        "confidence_floor": 0.85,
    }
    c = load_profile("chris_lord_alge")
    floors = {p: load_profile(p).vocal_blend_policy["confidence_floor"]
              for p in EXISTING}
    for p, f in floors.items():
        assert c.vocal_blend_policy["confidence_floor"] >= f, p
    assert c.vocal_blend_policy["confidence_floor"] == max(
        list(floors.values()) + [c.vocal_blend_policy["confidence_floor"]])


def test_declaration_three_default_creative_mode_and_own_named_modes():
    """REQUIRED declaration 3 — CLA's OWN mode vocabulary (front_and_center /
    commit_and_slam / drum_slam / big_chorus — names from his documented
    practice, carried by NO existing profile), his mode-name set matching
    none of the four, and both ``default_creative_mode`` entries resolving
    inside his own table (intimate words -> front_and_center; default ->
    commit_and_slam)."""
    c = load_profile("chris_lord_alge")
    names = set(c.search_modes)
    assert names == set(C_MODE_TABLE)
    assert {"front_and_center", "commit_and_slam", "drum_slam",
            "big_chorus"} <= names
    for p in EXISTING:
        other = load_profile(p)
        assert names != set(other.search_modes), p
        for own in ("front_and_center", "commit_and_slam", "drum_slam",
                    "big_chorus"):
            assert own not in other.search_modes, (p, own)
    dcm = c.default_creative_mode
    assert dcm["intimate_mode"] == "front_and_center"
    assert dcm["default_mode"] == "commit_and_slam"
    assert dcm["intimate_mode"] in c.search_modes
    assert dcm["default_mode"] in c.search_modes


def test_declaration_four_every_mode_authors_the_p042_surface_verbatim():
    """REQUIRED declaration 4 (the P-042 surface): every mode authors
    ``allowed_risk`` / ``bias`` / ``favor_kinds`` / ``suppress_kinds``
    EXPLICITLY — the full table is pinned verbatim; every bias is a non-empty
    authored string; every named kind comes from the engine vocabulary; his
    "commit, don't thin" posture is authored as the subtractive_drop
    suppressions."""
    raw = _c_raw()
    assert set(raw["search_modes"]) == set(C_MODE_TABLE)
    for mode_name, entry in raw["search_modes"].items():
        pinned = C_MODE_TABLE[mode_name]
        assert entry["allowed_risk"] == pinned["allowed_risk"], mode_name
        assert entry["favor_kinds"] == pinned["favor_kinds"], mode_name
        assert entry["suppress_kinds"] == pinned["suppress_kinds"], mode_name
        assert entry["reach_kinds"] == pinned["reach_kinds"], mode_name
        assert isinstance(entry["bias"], str) and entry["bias"].strip(), mode_name
        for field in ("favor_kinds", "suppress_kinds"):
            for kind in entry[field]:
                assert kind in CREATIVE_VARIANT_KINDS, (mode_name, field, kind)
    # his "commit, don't thin" posture is authored, not implied: the
    # subtractive move is suppressed somewhere in his table
    suppressed_anywhere = {k for e in raw["search_modes"].values()
                           for k in e["suppress_kinds"]}
    assert "subtractive_drop" in suppressed_anywhere


def test_declaration_four_default_flow_modes_author_neutral_declarations():
    """The requirement-8 construction (the P-042 discipline every shipped
    profile follows): his default and intimate modes author favor/suppress/
    reach NEUTRAL — the default flow forks nothing, so his default flow rides
    the SHARED byte-stable pin (never a Quincy/Timbaland-style conscious
    delta) — while non-default modes fork and reach for real."""
    raw = _c_raw()
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


def test_declaration_five_extended_reach_is_arrangement_lift_only():
    """REQUIRED declaration 5 (the P-043/P-044 surface): every mode authors
    ``reach_kinds`` explicitly. The AUTHORED taste decision, with its
    documented grounding: arrangement_lift — his big-chorus impact through
    sectional entrances/exits — on exactly ``big_chorus`` + ``experimental``.
    negative_space_dropout reach: ZERO everywhere — he FILLS space, he does
    not carve it (authored [] rather than justified). ensemble_rebalance
    reach: ZERO everywhere — balancing an ensemble is not his vocal-forward
    grammar."""
    raw = _c_raw()
    reach = {m: e["reach_kinds"] for m, e in raw["search_modes"].items()}
    assert reach == {m: pinned["reach_kinds"]
                     for m, pinned in C_MODE_TABLE.items()}
    reaching = [m for m, r in reach.items() if r]
    assert sorted(reaching) == sorted(C_REACHING_MODES)
    for mode_name, r in reach.items():
        assert DROPOUT not in r, mode_name
        assert "ensemble_rebalance" not in r, mode_name
        for kind in r:
            assert kind == "arrangement_lift", (mode_name, kind)
            assert kind in CREATIVE_EXTENDED_KINDS, (mode_name, kind)


def test_declaration_five_reach_lives_inside_the_governance_cap():
    """The cap binds against HIS honest rows: the shipped arrangement_lift
    reach (low translation risk) validates on his medium/high reaching modes;
    and authoring his MEDIUM-risk rows (ensemble_rebalance / dropout) on a
    LOW-posture mode is a LOUD load-time ValueError — the cap is governance
    and cannot be out-authored. Controls: the same medium reach validates on
    a medium-posture mode."""
    _validate(_c_raw(), "chris_lord_alge")  # the shipped low-risk reach is inside the cap

    for medium_kind in ("ensemble_rebalance", DROPOUT):
        over = _c_raw()
        over["search_modes"]["conservative"]["reach_kinds"] = [medium_kind]
        with pytest.raises(ValueError, match="cannot be out-authored"):
            _validate(over, "chris_lord_alge")

        control = _c_raw()
        control["search_modes"]["big_chorus"]["reach_kinds"] = [medium_kind]
        _validate(control, "chris_lord_alge")


def test_declaration_six_veto_thresholds_identical_and_not_weaker():
    """REQUIRED declaration 6 — the veto surface is UNCHANGED, not merely
    not-weaker: identical reject/veto/fallback lines across all FIVE
    profiles."""
    c = load_profile("chris_lord_alge").veto_thresholds
    assert c == {"reject_below": 45, "align_veto_below": 50,
                 "align_fallback": 75}
    for p in EXISTING:
        assert c == load_profile(p).veto_thresholds, p


def test_declaration_six_kill_switches_superset_with_the_loudness_line_verbatim():
    """THE CENTRAL STRESS-TEST at the kill-switch surface: every reference
    aesthetic switch is present VERBATIM — including, first and unweakened,
    the loudness safety line "Never chase reference loudness at the mix
    stage." — plus CLA's own impact-first additions. A loudness-maximalist
    who still cannot weaken the loudness rail."""
    c = load_profile("chris_lord_alge").aesthetic_kill_switches
    ref = load_profile("halee_ramone").aesthetic_kill_switches
    assert set(ref) <= set(c)
    assert LOUDNESS_KILL_SWITCH in c
    for line in (
        LOUDNESS_KILL_SWITCH,
        "Never make the lead vocal less intelligible unless explicitly approved.",
        "Never allow a stock loop to dominate the song identity by accident.",
        "Never widen the full mix to solve chorus lift.",
    ):
        assert line in c, line
    assert len(c) > len(ref)  # his own additions exist


def test_declaration_six_comparable_safety_structures_not_weaker():
    """Structure by structure (the P-032h idiom): risk penalties, both
    creative caps, the taste clamp, the intimate-width penalty, the retained
    width veto, the nudge penalties, the blend confidence floor, and the
    promotion reward — none weaker than the reference."""
    c = load_profile("chris_lord_alge")
    ref = load_profile("halee_ramone")
    assert c.risk_penalty == ref.risk_penalty
    assert c.creative_nudge_cap == ref.creative_nudge_cap
    assert c.creative_promotion_cap == ref.creative_promotion_cap
    assert c.taste_max_delta <= ref.taste_max_delta
    assert (c.taste_triangle["intimate_width_penalty"]
            >= ref.taste_triangle["intimate_width_penalty"])
    assert "vocal_belief_score" in c.taste_triangle["emotion_dims"]
    assert (c.truth_alignment["intimate"]["width_bloom"]
            < c.veto_thresholds["align_veto_below"])

    def rows(table):
        return {(frozenset(r["kinds"]), r["evidence"], r["dim"]): r["delta"]
                for r in table}
    c_rows, ref_rows = rows(c.nudge_table), rows(ref.nudge_table)
    assert set(c_rows) == set(ref_rows)
    for key, ref_delta in ref_rows.items():
        assert c_rows[key] <= ref_delta, f"nudge {key} weaker than reference"
    assert (c.vocal_blend_policy["confidence_floor"]
            >= ref.vocal_blend_policy["confidence_floor"])
    assert (sum(r["delta"] for r in c.promotion_table)
            <= sum(r["delta"] for r in ref.promotion_table))


def test_the_central_stress_test_loudness_stays_in_weights_and_language():
    """THE CENTRAL STRESS-TEST, stated as one assertion set: CLA's loudness
    identity lives in WEIGHTS + LANGUAGE, never in a relaxed safety surface.
    His impact poles are weighted above the field; the loudness kill-switch
    is retained verbatim; loudness maximization is DEFERRED out of scope at
    doctrine time (there is no loudness/LUFS doctrine axis to weight) — and
    every safety cap is equal-or-stricter."""
    c = load_profile("chris_lord_alge")
    ref = load_profile("halee_ramone")
    # the identity lives in the weights (impact poles above the field)
    w = c.doctrine["weights"]
    others = [load_profile(p).doctrine["weights"] for p in EXISTING]
    for key in ("section_contrast_score", "beat_identity_score"):
        assert all(w[key] > o[key] for o in others), key
    # the loudness rail is retained verbatim
    assert LOUDNESS_KILL_SWITCH in c.aesthetic_kill_switches
    # loudness maximization is deferred out of scope, not weighted as taste
    loud = [e for e in c.confidence_map if e["area"] == "loudness maximization"]
    assert len(loud) == 1 and loud[0]["level"] == "deferred"
    assert "safety concern" in loud[0]["reason"]
    assert "loudness_score" not in w  # there is no loudness doctrine axis
    # every safety cap equal-or-stricter
    assert c.veto_thresholds == ref.veto_thresholds
    assert c.risk_penalty == ref.risk_penalty
    assert c.taste_max_delta <= ref.taste_max_delta


def test_risk_class_semantics_unchanged():
    assert load_profile("chris_lord_alge").metadata["risk_class"] == 0
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


# --------------------------------------------------------------------------- #
# 4. THE AUTHORED VALUE SYSTEM.
# --------------------------------------------------------------------------- #
def test_weights_are_the_authored_value_system_verbatim():
    assert load_profile("chris_lord_alge").doctrine["weights"] == C_WEIGHTS


def test_coherent_pole_outside_the_existing_envelope():
    """The shape, machine-checked against ALL FOUR existing profiles: on his
    own poles CLA is NOT inside their envelope — six axes strictly ABOVE all
    four, three axes strictly BELOW all four (well past the at-least-2
    requirement floor) — and every weight > 0: de-emphasis is never
    removal."""
    c = load_profile("chris_lord_alge").doctrine["weights"]
    others = [load_profile(p).doctrine["weights"] for p in EXISTING]
    outside = 0
    for key in ABOVE_ALL_FOUR:
        assert all(c[key] > o[key] for o in others), (
            f"{key} is not a CLA pole (must exceed all four profiles)")
        outside += 1
    for key in BELOW_ALL_FOUR:
        assert all(c[key] < o[key] for o in others), (
            f"{key} is not a CLA pole (must sit below all four profiles)")
        outside += 1
    assert outside >= 2  # the requirement floor, cleared many times over
    assert all(v > 0 for v in c.values())


def test_argmax_no_existing_profile_has():
    """The axis-emphasis ordering is HIS OWN: CLA's single heaviest axis is
    section_contrast — verified NOT the argmax of any existing profile
    (halee_ramone peaks on emotional hierarchy / vocal centrality, timbaland
    on beat identity, quincy on depth hierarchy, eno on negative space); and
    his lightest axis is negative_space (he FILLS space) — the anti-Eno."""
    c = load_profile("chris_lord_alge").doctrine["weights"]
    assert max(c, key=c.get) == "section_contrast_score"
    assert list(c.values()).count(max(c.values())) == 1  # unique argmax
    assert min(c, key=c.get) == "negative_space_score"

    for p in EXISTING:
        w = load_profile(p).doctrine["weights"]
        argmaxes = {k for k, v in w.items() if v == max(w.values())}
        assert "section_contrast_score" not in argmaxes, p


def test_weights_copy_no_existing_profile():
    c = load_profile("chris_lord_alge").doctrine["weights"]
    for p in EXISTING:
        assert c != load_profile(p).doctrine["weights"], p


def test_every_non_authored_scorer_parameter_stays_on_the_shared_basis():
    """Attributability by construction: outside the two authored divergence
    channels (the loop_context polarity; the blend gate, which lives in
    ``vocal_blend_policy``, not in scorer constants) every scorer parameter,
    baseline and penalty coefficient equals the shared basis — so every
    component score divergence traces to an AUTHORED value, never to a forked
    measurement constant."""
    c = load_profile("chris_lord_alge").doctrine
    ref = load_profile("halee_ramone").doctrine
    assert c["baselines"] == ref["baselines"]
    assert c["penalty_coeffs"] == ref["penalty_coeffs"]
    for fn, params in c["scorers"].items():
        if fn == "loop_context":
            continue
        assert params == ref["scorers"][fn], f"scorer {fn} forked from the shared basis"


# --------------------------------------------------------------------------- #
# 5. ROWS EVERYWHERE.
# --------------------------------------------------------------------------- #
def test_kind_scores_cover_all_ten_kinds_with_full_rows():
    raw = _c_raw()
    assert set(raw["kind_scores"]) == set(CREATIVE_VARIANT_KINDS)
    for kind, row in raw["kind_scores"].items():
        for dim in _SCORE_DIMS:
            assert isinstance(row[dim], int), (kind, dim)
        assert row["translation"] in TRANSLATION_RISK_LEVELS, kind
        assert row["mono"] in TRANSLATION_RISK_LEVELS, kind


def test_truth_alignment_covers_all_ten_kinds_in_all_three_leans():
    raw = _c_raw()
    for lean in ("intimate", "big", "neutral"):
        assert set(raw["truth_alignment"][lean]) == set(CREATIVE_VARIANT_KINDS), lean
        for kind, v in raw["truth_alignment"][lean].items():
            assert isinstance(v, int), (lean, kind)


def test_dropout_row_is_honest_off_grammar_at_the_p044_floor():
    """The dropout row through his lens: he FILLS space rather than carving
    it, so dropout sits low-moderate (curated overall 70.6) — below his
    big-chorus arrangement lift (84.3) and his neutral moves — but the
    translation risk stays MEDIUM (the P-044 honesty floor: never ``low`` for
    the aggressive family). arrangement_lift is his highest extended kind (his
    documented big-chorus impact); ensemble_rebalance is his lowest (off his
    vocal-forward grammar)."""
    raw = _c_raw()
    row = raw["kind_scores"][DROPOUT]
    assert row["translation"] == "medium"
    assert row["translation"] != "low"
    assert row["mono"] == "low"

    assert _overall(raw, DROPOUT) == 70.6
    assert _overall(raw, "arrangement_lift") == 84.3
    assert _overall(raw, "ensemble_rebalance") == 67.4
    assert _overall(raw, "arrangement_lift") > _overall(raw, DROPOUT)
    assert _overall(raw, "arrangement_lift") > _overall(raw, "ensemble_rebalance")


def test_bloom_moves_are_high_taste_through_his_lens():
    """'The kit slams and fills': the size/energy moves lead his taste column
    — drum_room_bloom (88) is the strict maximum and width_bloom (86) sits at
    the top with the vocal ride and the arrangement lift — while the
    subtractive/carve moves sit lower (he ADDS, not subtracts) and the
    dropout (66) is the strict minimum (he fills space)."""
    scores = _c_raw()["kind_scores"]
    tastes = {kind: row["taste"] for kind, row in scores.items()}
    assert tastes["drum_room_bloom"] == max(tastes.values())
    assert tastes[DROPOUT] == min(tastes.values())
    assert tastes["width_bloom"] > tastes["subtractive_drop"]
    assert tastes["drum_room_bloom"] > tastes["intimacy_pass"]
    assert tastes["width_bloom"] > tastes["intimacy_pass"]


# --------------------------------------------------------------------------- #
# 6. THE CONFIDENCE MAP.
# --------------------------------------------------------------------------- #
def test_cla_confidence_map_verbatim():
    """The full authored map, pinned verbatim in authoring order — THE guard
    (validation accepts silent rewording; the pin does not)."""
    assert load_profile("chris_lord_alge").confidence_map == C_AUTHORED_MAP


def test_confidence_map_is_structurally_valid():
    cmap = load_profile("chris_lord_alge").confidence_map
    assert cmap
    for entry in cmap:
        assert entry["level"] in CONFIDENCE_LEVELS


def test_confidence_level_distribution():
    """6 high (vocal-forward / drum punch / section-contrast / density /
    loop polarity / translation risk) / 1 limited (vocal blend) / 8 deferred
    (the five standing engine boundaries + CLA's own three honest deferrals:
    loudness maximization, saturation energy, whole-mix translation)."""
    levels = [e["level"] for e in load_profile("chris_lord_alge").confidence_map]
    assert levels.count("high") == 6
    assert levels.count("limited") == 1
    assert levels.count("deferred") == 8


def test_every_high_entry_names_its_documented_technique_basis():
    """The user's grounding standard as a machine check: NO ``high`` entry
    ships without naming its documented-technique basis (the Waves CLA
    signature chains, the MWTM/PLAP masterclasses, the discography, the
    published interviews) — anything not tied to documented technique is
    limited/deferred by construction."""
    for entry in load_profile("chris_lord_alge").confidence_map:
        if entry["level"] == "high":
            assert DOCUMENTED_STAMP in entry["reason"], entry["area"]


def test_limited_blend_entry_matches_the_authored_policy():
    """The limited entry states its documented basis (the loud stacked
    background-vocal wall behind a forward lead), its live measurement (85.0
    vs 65.0 on real exported-stem data), his OWN authored floor (0.85) and
    the real coverage bounds — and it corresponds to the policy the profile
    actually authors."""
    p = load_profile("chris_lord_alge")
    limited = [e for e in p.confidence_map if e["level"] == "limited"]
    assert limited == [C_AUTHORED_MAP[6]]
    reason = limited[0]["reason"]
    assert "measured on real exported-stem data" in reason
    assert "85.0" in reason and "65.0" in reason
    assert "0.85 confidence floor" in reason
    assert p.vocal_blend_policy == {"acceptable_blend": True,
                                    "confidence_floor": 0.85}


def test_deferred_entries_carry_the_standing_boundaries_plus_his_own_three():
    """CLA's own three honest deferrals lead the deferred block — the concepts
    his identity implies that NO existing axis measures: loudness
    maximization (deliberately out of scope, the stress-test signature),
    saturation/harmonic energy, and whole-mix translation across systems —
    deferred, never faked from existing axes. Then the five standing engine
    boundaries ship verbatim (they are engine limits, not taste), identical
    to timbaland's shared block."""
    deferred = [e for e in load_profile("chris_lord_alge").confidence_map
                if e["level"] == "deferred"]
    assert deferred == C_AUTHORED_MAP[7:]
    areas = " | ".join(e["area"] for e in deferred)
    for own in ("loudness maximization", "saturation and harmonic energy",
                "whole-mix translation across playback systems"):
        assert own in areas, f"CLA's own deferral {own!r} missing"
    for standing in ("cultural loop recognizability", "true hook recurrence",
                     "motif provenance", "fingerprint typing",
                     "kick/sub temporal interlock", "per-section true-sub movement"):
        assert standing in areas, f"deferral {standing!r} missing"
    tim_deferred = [e for e in load_profile("timbaland").confidence_map
                    if e["level"] == "deferred"]
    assert deferred[3:] == tim_deferred  # the shared engine boundaries, verbatim


def test_high_claims_are_consistent_with_the_machine_facts():
    """No high entry overclaims: the 'above every existing profile' areas ARE
    weighted above all four; the density/staging area's axes ARE at the
    floor; the loop-polarity entry states the exact authored numbers and the
    exact authored protection flag."""
    c = load_profile("chris_lord_alge").doctrine["weights"]
    others = [load_profile(p).doctrine["weights"] for p in EXISTING]
    for key in ("vocal_centrality_score", "vocal_role_fit_score"):        # entry 1
        assert all(c[key] > o[key] for o in others), key
    for key in ("beat_identity_score", "low_end_motion_score"):           # entry 2
        assert all(c[key] > o[key] for o in others), key
    for key in ("section_contrast_score", "dynamic_mix_score"):           # entry 3
        assert all(c[key] > o[key] for o in others), key
    for key in ("physical_space_score", "depth_hierarchy_score"):         # entry 4
        assert all(c[key] < o[key] for o in others), key
    assert c["negative_space_score"] == min(c.values())                   # entry 4
    lc = load_profile("chris_lord_alge").doctrine["scorers"]["loop_context"]
    assert lc["static"] == 18.0 and lc["iconic"] == 92.0                  # entry 5
    assert load_profile("chris_lord_alge").protect_iconic_loops is True   # entry 5


def test_whole_profile_language_is_observational():
    """USER-MANDATED: zero judgment words across the ENTIRE authored JSON."""
    blob = _CLA_PATH.read_text(encoding="utf-8").lower()
    hits = judgment_word_hits(blob)
    assert not hits, f"judgment word(s) {hits} in chris_lord_alge.json"


# --------------------------------------------------------------------------- #
# 7. HIS OWN VOICE.
# --------------------------------------------------------------------------- #
def test_promotion_reason_is_his_own_authored_voice():
    c = load_profile("chris_lord_alge")
    assert [r["reason"] for r in c.promotion_table] == [C_PROMOTION_REASON]


def test_nudge_reasons_are_his_own_authored_voice():
    c = load_profile("chris_lord_alge")
    reasons = [r["reason"] for r in c.nudge_table]
    assert C_WIDTH_NUDGE in reasons
    for p in EXISTING:
        other_reasons = [r["reason"] for r in load_profile(p).nudge_table]
        assert not set(reasons) & set(other_reasons), p


# --------------------------------------------------------------------------- #
# 8. NO-ALIASING.
# --------------------------------------------------------------------------- #
def test_loads_are_fresh_mutation_cannot_reach_a_reload_or_other_profiles():
    c = load_profile("chris_lord_alge")
    c.doctrine["weights"]["section_contrast_score"] = 99.0
    c.confidence_map[0]["level"] = "deferred"
    c.aesthetic_kill_switches.append("mutated")
    c.search_modes["big_chorus"]["reach_kinds"].append(DROPOUT)
    assert load_profile("chris_lord_alge").doctrine["weights"] == C_WEIGHTS
    assert load_profile("chris_lord_alge").confidence_map == C_AUTHORED_MAP
    assert "mutated" not in load_profile("chris_lord_alge").aesthetic_kill_switches
    assert load_profile("chris_lord_alge").search_modes["big_chorus"]["reach_kinds"] \
        == ["arrangement_lift"]
    assert LOUDNESS_KILL_SWITCH in load_profile("chris_lord_alge").aesthetic_kill_switches
    assert load_profile("halee_ramone").doctrine["weights"]["section_contrast_score"] == 1.0
    assert load_profile("brian_eno").doctrine["weights"]["negative_space_score"] == 1.4
