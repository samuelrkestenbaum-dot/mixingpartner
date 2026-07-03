"""P-041 Commit-1 — ``quincy_jones.json``, the THIRD producer profile: the
proof the framework is not a two-pole switch.

The user's decision, verbatim authority: **Quincy Jones**, grounded as
*hand-curated-from-documented-technique -> high confidence* — no claim ships
``high`` unless tied to documented technique / documented production
philosophy, and every inference beyond that is labeled limited/deferred.
Center of gravity: orchestration + ensemble hierarchy + arranged emotional
lift — between and beyond the two existing poles (Halee/Ramone = physical
space + emotional hierarchy; Timbaland = groove identity + contrast +
negative space).

These are Commit-1's guards (the profile's OWN test file):

1. **Loads + validates** — ``load_profile("quincy_jones")`` passes every
   structural check; the raw JSON carries every required field.
2. **The honesty stamp** — metadata pinned verbatim:
   ``provenance: "hand-curated-documented"`` / ``confidence: "high"`` /
   ``risk_class: 0``.
3. **The three REQUIRED declarations, explicitly authored** (the P-032g/
   P-032f no-silent-inheritance discipline):
   ``protect_iconic_loops: false`` (the loop philosophy — an arrangement-led
   practice reworks a loop rather than protecting it as identity),
   ``vocal_blend_policy {true, 0.8}`` (the documented Swedien stacked-BGV
   basis, at a floor STRICTER than timbaland's 0.75), and the
   ``confidence_map`` (verbatim-pinned below — the guard).
4. **The authored value system** — all 14 weights pinned verbatim; the
   coherence SHAPE machine-checked against both existing profiles: his own
   poles (depth hierarchy / section contrast / dynamic movement / vocal role
   fit ABOVE both), vocal centrality between the two, the groove axes below
   timbaland but never removed, and a top-axis emphasis neither profile has.
5. **The authored loop polarity on the shared detection basis** — static
   12.0 / iconic 85.0 (each his OWN number), every detection floor identical
   to BOTH existing profiles (one basis, never forked).
6. **The confidence map, verbatim-pinned** — 6 high / 1 limited / 6 deferred;
   every ``high`` reason names its documented-technique basis; the deferred
   entries carry the standing engine boundaries plus Quincy's own honest
   deferral (harmonic/instrumental conversation is not measurable).
7. **Safety invariance** — aesthetic kill-switches a strict superset of the
   reference's (every safety-relevant line verbatim); veto thresholds not
   weaker; every comparable safety-adjacent structure equivalent-or-stricter;
   risk-class semantics unchanged.
8. **Observational language** — zero judgment words across the entire JSON.
9. **His own mode posture** — ``search_modes`` under Quincy's OWN names;
   ``default_creative_mode`` resolves inside his own table.
"""

from __future__ import annotations

import json
import pathlib

from logic_mix_os import governance
from logic_mix_os.doctrine.producer_profile import (
    CONFIDENCE_LEVELS,
    _REQUIRED_DATA_FIELDS,
    _validate,
    load_profile,
)

from test_vocal_type import judgment_word_hits

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_QUINCY_PATH = _ROOT / "logic_mix_os" / "doctrine" / "producers" / "quincy_jones.json"

# --------------------------------------------------------------------------- #
# The authored value system, PINNED VERBATIM.
# --------------------------------------------------------------------------- #
# Orchestration-first / ensemble-aware / vocal-forward but not vocal-only /
# space around the groove / emotional lift through arrangement / sectional
# architecture. Depth hierarchy (ensemble layering) and section contrast
# (sectional architecture) are HIS poles — weighted above BOTH existing
# profiles; vocal centrality sits between the two; the groove axes stay live
# below the groove-first profile (support, never dominance).
Q_WEIGHTS = {
    "physical_space_score": 0.8,
    "emotional_hierarchy_score": 1.1,
    "vocal_centrality_score": 1.0,
    "depth_hierarchy_score": 1.4,
    "section_contrast_score": 1.3,
    "static_mix_score": 1.0,
    "dynamic_mix_score": 1.1,
    "beat_identity_score": 0.6,
    "negative_space_score": 0.6,
    "groove_coherence_score": 0.6,
    "rhythmic_surprise_score": 0.4,
    "low_end_motion_score": 0.5,
    "loop_context_score": 0.3,
    "vocal_role_fit_score": 0.7,
}

# The axes where Quincy is deliberately NOT between the other two — his own
# poles (each strictly above BOTH existing profiles' weights).
ABOVE_BOTH = (
    "depth_hierarchy_score",       # ensemble layering — the center of gravity
    "section_contrast_score",      # sectional architecture
    "dynamic_mix_score",           # arranged lift as movement
    "vocal_role_fit_score",        # the ensemble vocal blend (Swedien BGVs)
)

# The axes deliberately BETWEEN the two poles.
BETWEEN = (
    "physical_space_score",        # space serves arrangement roles
    "emotional_hierarchy_score",   # arranged emotional lift, near the top
    "vocal_centrality_score",      # vocal-forward but not vocal-only
    "negative_space_score",        # moderate: space reveals roles
)

# The groove axes: below the groove-first profile, above the reference's 0 —
# groove SUPPORT without groove dominance (relax != remove).
GROOVE_SUPPORT = (
    "beat_identity_score", "groove_coherence_score",
    "rhythmic_surprise_score", "low_end_motion_score", "loop_context_score",
)

# Quincy's authored promotion evidence line (his own voice: loops become
# arranged section gestures — the arrangement carries the identity).
Q_PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — rework it into "
    "arranged section gestures (source material respected) so the arrangement "
    "carries the record's identity"
)

# The authored quincy_jones confidence map, VERBATIM (the P-031 reviewer
# discipline: validation accepts duplicate areas and extra entry keys — this
# pin is the guard; any edit is a conscious, test-visible decision).
Q_AUTHORED_MAP = [
    {
        "area": "ensemble depth and layering interpretation (depth hierarchy)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones technique — big-band and orchestral arranging practice from the Basie/Sinatra-era chairs and his own published writing on arranging: the ensemble sits in named layers around the lead; this axis is live and weighted above both existing profiles as this profile's center of gravity",
    },
    {
        "area": "sectional architecture and arranged-lift interpretation (section contrast, dynamic movement)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones technique — the sectional builds documented across the Off the Wall/Thriller-era production literature: parts enter and exit so each section lifts the record; these axes are live and weighted above both existing profiles",
    },
    {
        "area": "vocal prominence inside the ensemble (vocal centrality, emotional hierarchy)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones technique — the serve-the-song, leave-space-for-the-singer ethos documented in his autobiography Q and in producer interviews: the lead stays prominent inside an arranged ensemble, so these axes sit deliberately between the two existing poles",
    },
    {
        "area": "groove as support (beat identity, groove coherence, rhythmic surprise, low-end motion as retained measurement)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones technique — the rhythm section holds the floor for the song rather than centering the record's identity; these axes stay live at deliberately moderated weights below the groove-first profile: support, never dominance",
    },
    {
        "area": "space and balance hygiene as retained measurement (physical space, negative space, static balance)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones technique — space is kept where it reveals an arrangement role (leave space for the singer), not composed as silence; these axes stay live at moderate weight",
    },
    {
        "area": "loop context interpretation (static vs iconic)",
        "level": "high",
        "reason": "hand-curated from documented Quincy Jones production philosophy — an arrangement-led practice, not a loop-based one: a static dominant loop reads as arrested arrangement (authored 12.0), and even an iconic-functioning loop reads as material for the arrangement rather than the record's identity (authored 85.0, protect_iconic_loops: false); the status-to-score polarity is authored in this profile while every detection floor stays on the shared basis",
    },
    {
        "area": "vocal blend interpretation",
        "level": "limited",
        "reason": "the opt-in is authored from documented technique — Bruce Swedien's stacked background-vocal ensembles in the documented Jones/Swedien engineering partnership (the Acusonic recording process: a prominent lead atop an arranged vocal ensemble) — and the gate is live and measured on real exported-stem data: a qualified vocal chop and stack under masking read 85.0 on vocal_role_fit against the reference's 65.0 at this profile's authored 0.8 confidence floor; the level stays limited because coverage is bounded: events arise only from the masker-instrument set, info-tier events are emitted but not consumed, and vocal-band events carry no per-track masking risk",
    },
    {
        "area": "harmonic and instrumental conversation (voicing, counterlines, call-and-response)",
        "level": "deferred",
        "reason": "voicing and counterline interplay are central to the documented arranging practice yet not measurable on exported stems at doctrine time — the engine carries no harmonic analysis; the depth and section axes are the closest shipped proxies",
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
# else ships high).
DOCUMENTED_STAMP = "hand-curated from documented Quincy Jones"

# Quincy-DISTINCT confidence strings (the leak-guard vocabulary for the
# differential suite; the shared deferred entries are engine boundaries and
# legitimately identical across profiles).
QUINCY_ONLY_STRINGS = (
    "documented Quincy Jones technique",
    "Jones/Swedien engineering partnership",
)


def _q_raw() -> dict:
    with open(_QUINCY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- #
# 1. LOADS + VALIDATES — every structural check; every required field.
# --------------------------------------------------------------------------- #
def test_loads_and_passes_every_structural_check():
    p = load_profile("quincy_jones")
    assert p.metadata["name"] == "quincy_jones"
    _validate(_q_raw(), "quincy_jones")  # must not raise


def test_raw_json_carries_every_required_field():
    raw = _q_raw()
    for f in _REQUIRED_DATA_FIELDS:
        assert f in raw, f"quincy_jones.json missing required field {f!r}"
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        assert key in raw["doctrine"]


def test_dynamically_discovered_from_the_producers_directory():
    """The acceptance bar's first clause: the third producer is DISCOVERED,
    never registered — the same directory scan the CLI's friendly error uses
    finds all three profiles."""
    from logic_mix_os.cli import _PRODUCERS_DIR

    names = sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json"))
    assert "quincy_jones" in names
    assert "halee_ramone" in names and "timbaland" in names


# --------------------------------------------------------------------------- #
# 2. THE HONESTY STAMP — pinned verbatim.
# --------------------------------------------------------------------------- #
def test_metadata_is_the_confirmed_honesty_stamp():
    """Hand-curated from documented technique -> HIGH, per the user's
    grounding standard (NOT LLM-synthesized; nothing reference-track-derived
    ships high)."""
    assert load_profile("quincy_jones").metadata == {
        "name": "quincy_jones",
        "display_name": "Quincy Jones",
        "provenance": "hand-curated-documented",
        "confidence": "high",
        "risk_class": 0,
    }


# --------------------------------------------------------------------------- #
# 3. THE THREE REQUIRED DECLARATIONS — explicitly authored, never inherited.
# --------------------------------------------------------------------------- #
def test_declaration_one_loop_philosophy_authored():
    """REQUIRED declaration 1 — the loop philosophy, in writing: Quincy is
    not a loop-based producer; a loop is material for the ARRANGEMENT, so he
    does not protect an iconic-functioning loop as the record's identity
    (``protect_iconic_loops: false``, authored in the JSON — asserted on the
    raw file so the value is explicit, not defaulted)."""
    raw = _q_raw()
    assert raw["protect_iconic_loops"] is False
    assert load_profile("quincy_jones").protect_iconic_loops is False


def test_declaration_two_vocal_blend_policy_opt_in_stricter_floor():
    """REQUIRED declaration 2 — the masking philosophy, in writing: the
    documented Swedien stacked-BGV practice grounds an opt-in, at a
    confidence floor STRICTER than timbaland's 0.75. Lead protection is
    engine-fixed and invariant; misclassification fails CLOSED toward vocal
    protection whatever this field says."""
    raw = _q_raw()
    assert raw["vocal_blend_policy"] == {
        "acceptable_blend": True,
        "confidence_floor": 0.8,
    }
    q = load_profile("quincy_jones")
    assert q.vocal_blend_policy["confidence_floor"] > \
        load_profile("timbaland").vocal_blend_policy["confidence_floor"]
    assert q.vocal_blend_policy["confidence_floor"] >= \
        load_profile("halee_ramone").vocal_blend_policy["confidence_floor"]


def test_declaration_three_confidence_map_present_and_valid():
    cmap = load_profile("quincy_jones").confidence_map
    assert cmap
    for entry in cmap:
        assert entry["level"] in CONFIDENCE_LEVELS


# --------------------------------------------------------------------------- #
# 4. THE AUTHORED VALUE SYSTEM — pinned verbatim; the coherence shape.
# --------------------------------------------------------------------------- #
def test_weights_are_the_authored_value_system_verbatim():
    assert load_profile("quincy_jones").doctrine["weights"] == Q_WEIGHTS


def test_coherent_pole_not_averaged_mush():
    """The shape, machine-checked against BOTH existing profiles: on his own
    poles Quincy is NOT strictly between the other two (he sits ABOVE both);
    on the between axes he sits strictly between; the groove axes stay live
    below the groove-first profile; every weight > 0 (support != removal)."""
    q = load_profile("quincy_jones").doctrine["weights"]
    ref = load_profile("halee_ramone").doctrine["weights"]
    tim = load_profile("timbaland").doctrine["weights"]
    for key in ABOVE_BOTH:
        assert q[key] > ref[key] and q[key] > tim[key], (
            f"{key} is not Quincy's own pole (must exceed both profiles)"
        )
    for key in BETWEEN:
        lo, hi = min(ref[key], tim[key]), max(ref[key], tim[key])
        assert lo < q[key] < hi, f"{key} not strictly between the two poles"
    for key in GROOVE_SUPPORT:
        assert 0 < q[key] < tim[key], f"{key} not groove-support (below timbaland, > 0)"
        assert q[key] > ref[key], f"{key} not above the reference's 0"
    assert all(w > 0 for w in q.values())


def test_top_axis_emphasis_neither_profile_has():
    """The axis-emphasis ordering is HIS OWN: Quincy's single heaviest axis is
    depth_hierarchy (ensemble layering) — neither existing profile puts its
    maximum weight there — and his top-2 {depth hierarchy, section contrast}
    is an emphasis pair neither profile has at its top."""
    q = load_profile("quincy_jones").doctrine["weights"]
    ref = load_profile("halee_ramone").doctrine["weights"]
    tim = load_profile("timbaland").doctrine["weights"]

    def top2(w):
        return set(sorted(w, key=w.get, reverse=True)[:2])

    q_top = max(q, key=q.get)
    assert q_top == "depth_hierarchy_score"
    assert ref[q_top] < max(ref.values())   # not the reference's top axis
    assert tim[q_top] < max(tim.values())   # not timbaland's top axis
    assert top2(q) == {"depth_hierarchy_score", "section_contrast_score"}
    assert top2(q) != top2(ref) and top2(q) != top2(tim)


def test_weights_copy_neither_profile():
    """The user's mandate: he must NOT copy either profile's weights — not
    the table, and not any single axis-for-axis vector overlap beyond
    coincidence (the tables differ as wholes)."""
    q = load_profile("quincy_jones").doctrine["weights"]
    assert q != load_profile("halee_ramone").doctrine["weights"]
    assert q != load_profile("timbaland").doctrine["weights"]


# --------------------------------------------------------------------------- #
# 5. THE LOOP POLARITY — his own numbers on the SHARED detection basis.
# --------------------------------------------------------------------------- #
def test_loop_context_polarity_is_authored_and_detection_is_shared():
    """Static 12.0 / iconic 85.0 — each Quincy's OWN authored number (static
    between the two existing polarities; iconic BELOW both: even an
    iconic-functioning loop reads as arrangement material, not the record's
    identity) — while every DETECTION floor is identical to BOTH profiles,
    so all three read the same status from the same stems (one shared basis,
    never forked)."""
    q = load_profile("quincy_jones").doctrine["scorers"]["loop_context"]
    ref = load_profile("halee_ramone").doctrine["scorers"]["loop_context"]
    tim = load_profile("timbaland").doctrine["scorers"]["loop_context"]
    assert q["static"] == 12.0
    assert tim["static"] < q["static"] < ref["static"]
    assert q["iconic"] == 85.0
    assert q["iconic"] < ref["iconic"] and q["iconic"] < tim["iconic"]
    for floor in ("width_floor", "transient_lift_floor", "groove_transient_floor",
                  "definition_crest_db", "evolution_rms_floor_db",
                  "evolution_width_floor", "evolution_brightness_floor"):
        assert q[floor] == ref[floor] == tim[floor], f"detection floor {floor} forked"
    for neutral in ("no_loop", "not_dominant", "dominant_unassessed",
                    "dominant_evolving"):
        assert q[neutral] == ref[neutral] == tim[neutral], f"neutral {neutral} forked"


def test_every_non_authored_scorer_parameter_stays_on_the_shared_basis():
    """Attributability by construction: outside the two authored divergence
    channels (the loop_context polarity above; the blend gate, which lives in
    ``vocal_blend_policy``, not in scorer constants) every scorer parameter,
    baseline and penalty coefficient equals the shared basis — so every
    component score divergence traces to an AUTHORED value, never to a forked
    measurement constant."""
    q = load_profile("quincy_jones").doctrine
    ref = load_profile("halee_ramone").doctrine
    assert q["baselines"] == ref["baselines"]
    assert q["penalty_coeffs"] == ref["penalty_coeffs"]
    for fn, params in q["scorers"].items():
        if fn == "loop_context":
            continue
        assert params == ref["scorers"][fn], f"scorer {fn} forked from the shared basis"


# --------------------------------------------------------------------------- #
# 6. THE CONFIDENCE MAP — verbatim pin; the honesty split machine-checked.
# --------------------------------------------------------------------------- #
def test_quincy_confidence_map_verbatim():
    """The full authored map, pinned verbatim in authoring order — THE guard
    (validation accepts silent rewording; the pin does not)."""
    assert load_profile("quincy_jones").confidence_map == Q_AUTHORED_MAP


def test_confidence_level_distribution():
    """6 high (the five interpretation areas + the loop polarity) / 1 limited
    (vocal blend — live, measured, coverage-bounded) / 6 deferred (the five
    standing engine boundaries + Quincy's own harmonic-conversation
    deferral)."""
    levels = [e["level"] for e in load_profile("quincy_jones").confidence_map]
    assert levels.count("high") == 6
    assert levels.count("limited") == 1
    assert levels.count("deferred") == 6


def test_every_high_entry_names_its_documented_technique_basis():
    """The user's grounding standard as a machine check: NO ``high`` entry
    ships without naming its documented-technique basis (arranging practice,
    the serve-the-song ethos, the production literature, the Swedien
    partnership) — anything not tied to documented technique is limited/
    deferred by construction."""
    for entry in load_profile("quincy_jones").confidence_map:
        if entry["level"] == "high":
            assert DOCUMENTED_STAMP in entry["reason"], entry["area"]


def test_limited_blend_entry_matches_the_authored_policy():
    """The limited entry states its documented basis (Swedien stacked BGVs),
    its live measurement (85.0 vs 65.0 on real exported-stem data), its OWN
    authored floor (0.8) and the real coverage bounds — and it corresponds to
    the policy the profile actually authors."""
    p = load_profile("quincy_jones")
    limited = [e for e in p.confidence_map if e["level"] == "limited"]
    assert limited == [Q_AUTHORED_MAP[6]]
    reason = limited[0]["reason"]
    assert "Bruce Swedien" in reason
    assert "measured on real exported-stem data" in reason
    assert "85.0" in reason and "65.0" in reason
    assert "0.8 confidence floor" in reason
    assert p.vocal_blend_policy == {"acceptable_blend": True, "confidence_floor": 0.8}


def test_deferred_entries_carry_the_standing_boundaries_plus_his_own():
    """The five standing engine boundaries ship verbatim (they are engine
    limits, not taste), PLUS Quincy's own honest deferral: harmonic and
    instrumental conversation — central to the documented arranging practice,
    not measurable by this engine — stays deferred rather than overclaimed."""
    deferred = [e for e in load_profile("quincy_jones").confidence_map
                if e["level"] == "deferred"]
    assert deferred == [Q_AUTHORED_MAP[7]] + Q_AUTHORED_MAP[8:]
    areas = " | ".join(e["area"] for e in deferred)
    for standing in ("harmonic and instrumental conversation",
                     "cultural loop recognizability", "true hook recurrence",
                     "motif provenance", "fingerprint typing",
                     "kick/sub temporal interlock", "per-section true-sub movement"):
        assert standing in areas, f"deferral {standing!r} missing"
    tim_deferred = [e for e in load_profile("timbaland").confidence_map
                    if e["level"] == "deferred"]
    assert deferred[1:] == tim_deferred  # the shared engine boundaries, verbatim


def test_high_claims_are_consistent_with_the_machine_facts():
    """No high entry overclaims: the 'above both' areas ARE weighted above
    both; the 'between the two poles' area IS between; the groove-support
    area IS below timbaland and above the reference; the loop-polarity entry
    states the exact authored numbers."""
    q = load_profile("quincy_jones").doctrine["weights"]
    ref = load_profile("halee_ramone").doctrine["weights"]
    tim = load_profile("timbaland").doctrine["weights"]
    for key in ("depth_hierarchy_score",                    # entry 1
                "section_contrast_score", "dynamic_mix_score"):  # entry 2
        assert q[key] > ref[key] and q[key] > tim[key], key
    for key in ("vocal_centrality_score", "emotional_hierarchy_score"):  # entry 3
        lo, hi = min(ref[key], tim[key]), max(ref[key], tim[key])
        assert lo < q[key] < hi, key
    for key in GROOVE_SUPPORT[:4]:                          # entry 4
        assert 0 < q[key] < tim[key], key
    lc = load_profile("quincy_jones").doctrine["scorers"]["loop_context"]
    assert lc["static"] == 12.0 and lc["iconic"] == 85.0    # entry 6


def test_whole_profile_language_is_observational():
    """USER-MANDATED: zero judgment words across the ENTIRE authored JSON."""
    blob = _QUINCY_PATH.read_text(encoding="utf-8").lower()
    hits = judgment_word_hits(blob)
    assert not hits, f"judgment word(s) {hits} in quincy_jones.json"


# --------------------------------------------------------------------------- #
# 7. SAFETY INVARIANCE — nothing weaker than the reference, anywhere.
# --------------------------------------------------------------------------- #
def test_aesthetic_switches_are_a_superset_with_every_safety_relevant_line():
    """Equivalent-or-stricter, literally: every reference aesthetic switch is
    present verbatim (including the vocal-intelligibility and stock-loop
    lines — the safety-relevant ones), plus Quincy's own arrangement-first
    additions."""
    q = load_profile("quincy_jones").aesthetic_kill_switches
    ref = load_profile("halee_ramone").aesthetic_kill_switches
    assert set(ref) <= set(q)
    for line in (
        "Never make the lead vocal less intelligible unless explicitly approved.",
        "Never allow a stock loop to dominate the song identity by accident.",
        "Never widen the full mix to solve chorus lift.",
        "Never chase reference loudness at the mix stage.",
    ):
        assert line in q, line
    assert len(q) > len(ref)  # his own additions exist


def test_veto_thresholds_not_weaker_than_the_reference():
    """The packet's explicit safety floor: reject_below / align_veto_below /
    align_fallback each >= the reference's values."""
    q = load_profile("quincy_jones").veto_thresholds
    ref = load_profile("halee_ramone").veto_thresholds
    assert q["reject_below"] >= ref["reject_below"]
    assert q["align_veto_below"] >= ref["align_veto_below"]
    assert q["align_fallback"] >= ref["align_fallback"]


def test_comparable_safety_structures_equivalent_or_stricter():
    """Structure by structure (the P-032h idiom): risk penalties, both
    creative caps, the taste clamp, the intimate-width penalty, the retained
    width veto, the nudge penalties, the blend confidence floor, and the
    promotion reward — none weaker than the reference."""
    q = load_profile("quincy_jones")
    ref = load_profile("halee_ramone")
    assert q.risk_penalty == ref.risk_penalty
    assert q.creative_nudge_cap == ref.creative_nudge_cap
    assert q.creative_promotion_cap == ref.creative_promotion_cap
    assert q.taste_max_delta <= ref.taste_max_delta
    assert (q.taste_triangle["intimate_width_penalty"]
            >= ref.taste_triangle["intimate_width_penalty"])
    # the vocal-safety dim stays inside the emotion blend
    assert "vocal_belief_score" in q.taste_triangle["emotion_dims"]
    # the intimate-width veto is retained, not relaxed past the veto line
    assert (q.truth_alignment["intimate"]["width_bloom"]
            < q.veto_thresholds["align_veto_below"])
    # nudge rows: same (kinds, evidence, dim) coverage; penalties >= reference
    def rows(table):
        return {(frozenset(r["kinds"]), r["evidence"], r["dim"]): r["delta"]
                for r in table}
    q_rows, ref_rows = rows(q.nudge_table), rows(ref.nudge_table)
    assert set(q_rows) == set(ref_rows)
    for key, ref_delta in ref_rows.items():
        assert q_rows[key] <= ref_delta, f"nudge {key} weaker than reference"
    # the blend gate's dial: the floor is never lowered
    assert (q.vocal_blend_policy["confidence_floor"]
            >= ref.vocal_blend_policy["confidence_floor"])
    # the promotion reward is not enlarged
    assert (sum(r["delta"] for r in q.promotion_table)
            <= sum(r["delta"] for r in ref.promotion_table))


def test_risk_class_semantics_unchanged():
    assert load_profile("quincy_jones").metadata["risk_class"] == 0
    assert governance.validate_action_safety({"risk_class": 5})["blocked"] is True


# --------------------------------------------------------------------------- #
# 8. HIS OWN MODE POSTURE — authored names, resolvable inside his own table.
# --------------------------------------------------------------------------- #
def test_search_modes_are_quincys_own_and_default_table_resolves():
    """Quincy's OWN mode names (the ensemble/arrangement vocabulary — his
    mode-name set matches neither existing profile's), and both entries of
    his ``default_creative_mode`` table resolve inside his own
    ``search_modes`` (no fallback can ever fire on the default path)."""
    q = load_profile("quincy_jones")
    names = set(q.search_modes)
    assert {"ensemble_balance", "space_for_the_singer", "arrangement_lift",
            "orchestral_depth"} <= names
    assert names != set(load_profile("halee_ramone").search_modes)
    assert names != set(load_profile("timbaland").search_modes)
    dcm = q.default_creative_mode
    assert dcm["intimate_mode"] == "space_for_the_singer"
    assert dcm["default_mode"] == "arrangement_lift"
    assert dcm["intimate_mode"] in q.search_modes
    assert dcm["default_mode"] in q.search_modes
    # neither existing profile authors these mode names
    assert "space_for_the_singer" not in load_profile("halee_ramone").search_modes
    assert "arrangement_lift" not in load_profile("timbaland").search_modes


def test_promotion_reason_is_his_own_authored_voice():
    q = load_profile("quincy_jones")
    assert [r["reason"] for r in q.promotion_table] == [Q_PROMOTION_REASON]


# --------------------------------------------------------------------------- #
# 9. NO-ALIASING — fresh loads; mutation cannot reach a reload.
# --------------------------------------------------------------------------- #
def test_loads_are_fresh_mutation_cannot_reach_a_reload_or_other_profiles():
    q = load_profile("quincy_jones")
    q.doctrine["weights"]["depth_hierarchy_score"] = 99.0
    q.confidence_map[0]["level"] = "deferred"
    q.aesthetic_kill_switches.append("mutated")
    assert load_profile("quincy_jones").doctrine["weights"] == Q_WEIGHTS
    assert load_profile("quincy_jones").confidence_map == Q_AUTHORED_MAP
    assert "mutated" not in load_profile("quincy_jones").aesthetic_kill_switches
    assert load_profile("halee_ramone").doctrine["weights"]["depth_hierarchy_score"] == 1.0
    assert load_profile("timbaland").doctrine["weights"]["depth_hierarchy_score"] == 0.5
