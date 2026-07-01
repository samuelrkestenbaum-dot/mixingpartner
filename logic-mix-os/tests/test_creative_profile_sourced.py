"""P-026 — the binding guard that ``creative.py``'s producer-specific module
globals are SOURCED from ``load_profile("halee_ramone")`` and are byte-identical
to the pre-P-026 hardcoded literals.

The literals were DELETED from ``creative.py`` (the JSON is now their single home),
so these tests PIN the concrete expected values inline. A future profile-JSON edit
that changes any of them is caught here — this is the value guard the removed
literals used to provide implicitly.

Two complementary proofs live together:

* **value pins** — the concrete numbers/shapes of each sourced global.
* **identity + shape** — each global IS the profile's object (single source of
  truth) and carries the exact type/shape the old literal had (esp. the
  nudge/promotion ``kinds`` sets that ``_apply_nudges`` / ``_apply_promotions``
  rely on).

The behavior-level byte-identical proof is the UNCHANGED P-012/13/15/16 creative
tests (``test_creative_nudges``, ``test_creative_nudge_visibility``,
``test_decisive_nudge``, ``test_loop_promotion``); those stay the golden scoring
guard and are not touched here.
"""

from __future__ import annotations

from logic_mix_os import creative
from logic_mix_os.doctrine.producer_profile import load_profile


# --------------------------------------------------------------------------- #
# Globals are SOURCED from the default profile (single source of truth)
# --------------------------------------------------------------------------- #
def test_default_profile_is_the_reference_producer():
    assert creative._DEFAULT_PROFILE.metadata["name"] == "halee_ramone"


def test_globals_are_the_profile_objects():
    """Each producer-specific global is literally the value read off
    ``_DEFAULT_PROFILE`` — the JSON is the single source of truth, not a second
    hardcoded copy that could silently drift."""
    p = creative._DEFAULT_PROFILE
    assert creative._KIND_SCORES is p.kind_scores
    assert creative._NUDGE_TABLE is p.nudge_table
    assert creative._PROMOTION_TABLE is p.promotion_table
    assert creative.CREATIVE_NUDGE_CAP == p.creative_nudge_cap
    assert creative.CREATIVE_PROMOTION_CAP == p.creative_promotion_cap
    assert creative._RISK_PENALTY is p.risk_penalty
    assert creative.SEARCH_MODES is p.search_modes
    assert creative.PHILOSOPHY == p.philosophy


def test_globals_equal_a_fresh_load():
    """A second independent load reproduces every global exactly — deterministic,
    and confirms nothing was mutated at import."""
    fresh = load_profile("halee_ramone")
    assert creative._KIND_SCORES == fresh.kind_scores
    assert creative._NUDGE_TABLE == fresh.nudge_table
    assert creative._PROMOTION_TABLE == fresh.promotion_table
    assert creative.CREATIVE_NUDGE_CAP == fresh.creative_nudge_cap
    assert creative.CREATIVE_PROMOTION_CAP == fresh.creative_promotion_cap
    assert creative._RISK_PENALTY == fresh.risk_penalty
    assert creative.SEARCH_MODES == fresh.search_modes
    assert creative.PHILOSOPHY == fresh.philosophy


# --------------------------------------------------------------------------- #
# Value pins — the concrete pre-P-026 literals, now guarded here
# --------------------------------------------------------------------------- #
def test_kind_scores_value_pins():
    """7 kinds × 9 dims, byte-for-byte the pre-P-026 curated table."""
    ks = creative._KIND_SCORES
    assert set(ks) == {
        "width_bloom", "subtractive_drop", "vocal_ride", "drum_room_bloom",
        "loop_deconstruct", "depth_cleanup", "intimacy_pass",
    }
    assert ks["width_bloom"] == dict(
        technical=82, halee=78, ramone=79, contrast=91, vocal_belief=74,
        excitement=88, taste=80, translation="medium", mono="medium",
    )
    assert ks["subtractive_drop"] == dict(
        technical=85, halee=88, ramone=86, contrast=88, vocal_belief=86,
        excitement=78, taste=86, translation="low", mono="low",
    )
    assert ks["vocal_ride"] == dict(
        technical=84, halee=84, ramone=92, contrast=70, vocal_belief=92,
        excitement=70, taste=88, translation="low", mono="low",
    )
    assert ks["drum_room_bloom"] == dict(
        technical=80, halee=89, ramone=78, contrast=82, vocal_belief=76,
        excitement=83, taste=82, translation="low", mono="low",
    )
    assert ks["loop_deconstruct"] == dict(
        technical=83, halee=87, ramone=84, contrast=78, vocal_belief=85,
        excitement=72, taste=84, translation="low", mono="low",
    )
    assert ks["depth_cleanup"] == dict(
        technical=84, halee=90, ramone=85, contrast=72, vocal_belief=86,
        excitement=66, taste=85, translation="low", mono="low",
    )
    assert ks["intimacy_pass"] == dict(
        technical=82, halee=85, ramone=88, contrast=72, vocal_belief=90,
        excitement=64, taste=87, translation="low", mono="low",
    )
    # A representative single-cell pin (matches the packet's example).
    assert ks["width_bloom"]["halee"] == 78


def test_caps_value_pins():
    assert creative.CREATIVE_NUDGE_CAP == 2.0
    assert creative.CREATIVE_PROMOTION_CAP == 4.0


def test_risk_penalty_value_pin():
    assert creative._RISK_PENALTY == {"low": 0, "medium": 6, "high": 14}


def test_nudge_table_value_pins():
    """Exact rows, including the ``kinds`` SETS the loader rehydrates from JSON
    lists — ``_apply_nudges`` does ``kind in row['kinds']`` so this MUST be a set."""
    nt = creative._NUDGE_TABLE
    assert len(nt) == 2
    row0, row1 = nt
    assert row0["kinds"] == {"width_bloom", "vocal_ride"}
    assert isinstance(row0["kinds"], set)
    assert row0["evidence"] == "lead_masked"
    assert row0["dim"] == "vocal_belief"
    assert row0["delta"] == -14
    assert row0["reason"] == (
        "vocal_belief -14: lead vocal is masked (bad_masking) — "
        "pushing the vocal forward by level/width is risky here; "
        "bring it into intimate focus instead"
    )
    assert row1["kinds"] == {"width_bloom"}
    assert isinstance(row1["kinds"], set)
    assert row1["evidence"] == "width_crowding"
    assert row1["dim"] == "vocal_belief"
    assert row1["delta"] == -6
    assert row1["reason"] == "vocal_belief -6: stereo image is already width-crowded"


def test_promotion_table_value_pins():
    pt = creative._PROMOTION_TABLE
    assert len(pt) == 1
    row = pt[0]
    assert row["kinds"] == {"loop_deconstruct"}
    assert isinstance(row["kinds"], set)
    assert row["evidence"] == "foregrounded_loop"
    assert row["dim"] == "excitement"
    assert row["delta"] == 35
    assert row["reason"] == (
        "loop_promotion +4.0: a foregrounded/dominating loop — "
        "deconstruct it (source material respected), don't just accent it"
    )


def test_search_modes_value_pins():
    sm = creative.SEARCH_MODES
    assert set(sm) == {
        "conservative", "halee_depth", "ramone_vocal_truth",
        "dramatic_contrast", "deconstructive", "experimental",
    }
    assert sm["conservative"] == {
        "allowed_risk": "low",
        "bias": "preserve identity, subtle improvements, vocal belief",
    }
    assert sm["experimental"]["allowed_risk"] == "high"
    assert sm["dramatic_contrast"]["allowed_risk"] == "medium"


def test_philosophy_value_pin():
    assert creative.PHILOSOPHY == (
        "A mix is not finished when it is balanced. It is finished when the static "
        "balance supports the song and the dynamic movement makes the song feel "
        "inevitable. The best mix is the version where the song feels most "
        "inevitable, not the most processed."
    )


# --------------------------------------------------------------------------- #
# Shape / type fidelity for the in-function consumers
# --------------------------------------------------------------------------- #
def test_apply_nudges_still_gets_sets_and_fires():
    """``_apply_nudges`` does ``kind in row['kinds']``; a list would still work
    for membership but the source used sets, so we assert the type AND the firing
    behavior on a crafted result."""

    class _R:
        masking_report = {
            "events": [
                {"classification": "bad_masking", "elements": ["Lead Vocal"]},
            ]
        }

    fired = creative._apply_nudges("width_bloom", _R())
    assert fired == [
        (
            "vocal_belief",
            -14,
            "vocal_belief -14: lead vocal is masked (bad_masking) — "
            "pushing the vocal forward by level/width is risky here; "
            "bring it into intimate focus instead",
        )
    ]
    # A kind NOT in the set does not fire.
    assert creative._apply_nudges("depth_cleanup", _R()) == []


def test_apply_promotions_still_gets_sets_and_fires():
    class _R:
        source_audits = {"audits": [{"red_flags": ["foregrounded loop"]}]}
        provenance = {"summary": {"high_risk": 1}}

    fired = creative._apply_promotions("loop_deconstruct", _R())
    assert fired == [
        (
            "excitement",
            35,
            "loop_promotion +4.0: a foregrounded/dominating loop — "
            "deconstruct it (source material respected), don't just accent it",
        )
    ]
    assert creative._apply_promotions("width_bloom", _R()) == []
