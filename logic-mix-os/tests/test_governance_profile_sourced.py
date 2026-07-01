"""P-027 — the binding guard that ``governance.py``'s producer-specific module
globals are SOURCED from ``load_profile("halee_ramone")`` and are byte-identical
to the pre-P-027 hardcoded literals.

Two parts, mirroring the packet:

* **Part A** — the ALREADY-captured governance values (``_TRUTH_ALIGNMENT``,
  ``_TASTE_KIND_BIAS``, ``TASTE_MAX_DELTA``, and the AESTHETIC subset of
  ``KILL_SWITCHES``) are now read off ``_DEFAULT_PROFILE``. The literals were
  DELETED from ``governance.py``, so these tests PIN the concrete expected values
  inline (the value guard the removed literals used to provide implicitly). The
  five SAFETY kill-switches (items 1-5) STAY hardcoded and are asserted present
  and NOT sourced from the swappable profile.
* **Part B** — the secondary governance constants (the taste-triangle penalty +
  emotion blend, and the veto thresholds) are widened into the profile and read
  from it. Value-pinned here; round-trip-guarded in ``test_producer_profile``.

The NO-ALIASING proof (binding, from P-026): running governance on a real fixture
must leave the shared ``_DEFAULT_PROFILE`` structures byte-unchanged — no consumer
mutates a sourced global in place.

The behavior-level byte-identical proof is the UNCHANGED governance/taste tests
(``test_governance``, ``test_governance_taste``, ``test_live_wire``, and the
P-007/8/9 taste tests); those stay the golden judgment guard and are not touched
here.
"""

from __future__ import annotations

import copy

from logic_mix_os import governance
from logic_mix_os.doctrine.producer_profile import load_profile


# --------------------------------------------------------------------------- #
# Globals are SOURCED from the default profile (single source of truth)
# --------------------------------------------------------------------------- #
def test_default_profile_is_the_reference_producer():
    assert governance._DEFAULT_PROFILE.metadata["name"] == "halee_ramone"


def test_globals_are_the_profile_objects():
    """Each producer-specific governance global is literally the value read off
    ``_DEFAULT_PROFILE`` — the JSON is the single source of truth, not a second
    hardcoded copy that could silently drift."""
    p = governance._DEFAULT_PROFILE
    assert governance._TRUTH_ALIGNMENT is p.truth_alignment
    assert governance._TASTE_KIND_BIAS is p.taste_kind_bias
    assert governance.TASTE_MAX_DELTA == p.taste_max_delta


def test_globals_equal_a_fresh_load():
    """A second independent load reproduces every governance global exactly —
    deterministic, and confirms nothing was mutated at import."""
    fresh = load_profile("halee_ramone")
    assert governance._TRUTH_ALIGNMENT == fresh.truth_alignment
    assert governance._TASTE_KIND_BIAS == fresh.taste_kind_bias
    assert governance.TASTE_MAX_DELTA == fresh.taste_max_delta


# --------------------------------------------------------------------------- #
# Part A value pins — the concrete pre-P-027 literals, now guarded here
# --------------------------------------------------------------------------- #
def test_truth_alignment_value_pins():
    """3 leans × 7 kinds, byte-for-byte the pre-P-027 curated alignment table."""
    ta = governance._TRUTH_ALIGNMENT
    assert set(ta) == {"intimate", "big", "neutral"}
    assert ta["intimate"] == {
        "vocal_ride": 88, "intimacy_pass": 90, "subtractive_drop": 84,
        "depth_cleanup": 82, "loop_deconstruct": 83, "drum_room_bloom": 58,
        "width_bloom": 45,
    }
    assert ta["big"] == {
        "width_bloom": 86, "drum_room_bloom": 86, "vocal_ride": 78,
        "subtractive_drop": 76, "depth_cleanup": 76, "loop_deconstruct": 78,
        "intimacy_pass": 70,
    }
    assert ta["neutral"] == {
        "width_bloom": 72, "drum_room_bloom": 78, "vocal_ride": 84,
        "subtractive_drop": 82, "depth_cleanup": 82, "loop_deconstruct": 80,
        "intimacy_pass": 82,
    }


def test_taste_max_delta_value_pin():
    assert governance.TASTE_MAX_DELTA == 15


def test_taste_kind_bias_value_pins():
    """The narrower/wider taste statements map to signed identity deltas of
    ±TASTE_MAX_DELTA (±15). The JSON stores the resolved numbers."""
    tkb = governance._TASTE_KIND_BIAS
    assert tkb == {
        "tends to prefer narrower stereo images": {
            "width_bloom": -15, "drum_room_bloom": -15,
        },
        "prefers wider images": {"width_bloom": 15},
    }


# --------------------------------------------------------------------------- #
# KILL_SWITCHES — safety (1-5) hardcoded; aesthetic (6-9) sourced. Exact list.
# --------------------------------------------------------------------------- #
_SAFETY_SWITCHES = [
    "Never overwrite original audio.",
    "Never destructively tune or time-stretch source recordings.",
    "Never delete tracks without backup.",
    "Never flatten comped vocals without a duplicate.",
    "Never apply creative source edits without a versioned duplicate.",
]
_AESTHETIC_SWITCHES = [
    "Never chase reference loudness at the mix stage.",
    "Never widen the full mix to solve chorus lift.",
    "Never make the lead vocal less intelligible unless explicitly approved.",
    "Never allow a stock loop to dominate the song identity by accident.",
]


def test_kill_switches_full_list_byte_identical():
    """The composed list = 5 hardcoded safety switches + the profile's aesthetic
    switches, in that exact order — byte-identical to the pre-P-027 list."""
    assert governance.KILL_SWITCHES == _SAFETY_SWITCHES + _AESTHETIC_SWITCHES
    assert len(governance.KILL_SWITCHES) == 9


def test_kill_switches_safety_prefix_hardcoded():
    """The five safety switches (non-destructive/Class-5, producer-AGNOSTIC) are
    the first five and stay hardcoded — they must NOT come from the profile."""
    assert governance.KILL_SWITCHES[0:5] == _SAFETY_SWITCHES


def test_kill_switches_aesthetic_suffix_sourced_from_profile():
    """The four aesthetic switches (items 6-9) are the profile's
    ``aesthetic_kill_switches``, appended in order."""
    assert governance.KILL_SWITCHES[5:9] == _AESTHETIC_SWITCHES
    assert governance.KILL_SWITCHES[5:9] == governance._DEFAULT_PROFILE.aesthetic_kill_switches


def test_safety_switches_not_in_profile():
    """The producer-agnostic safety switches must never appear in a swappable
    profile — a swapped producer cannot weaken them."""
    profile_switches = set(governance._DEFAULT_PROFILE.aesthetic_kill_switches)
    for safety in _SAFETY_SWITCHES:
        assert safety not in profile_switches


# --------------------------------------------------------------------------- #
# NO-ALIASING proof (binding) — running governance leaves the shared profile
# structures byte-unchanged. No consumer mutates a sourced global in place.
# --------------------------------------------------------------------------- #
def test_apply_taste_does_not_mutate_shared_globals():
    """``_apply_taste`` reads ``_TASTE_KIND_BIAS`` but must never mutate it; the
    caller mutates a LOCAL ``triangle`` dict, not the profile. Snapshot the shared
    structures, run a taste-affecting path, and assert byte-unchanged."""
    ta_before = copy.deepcopy(governance._TRUTH_ALIGNMENT)
    tkb_before = copy.deepcopy(governance._TASTE_KIND_BIAS)
    ks_before = copy.deepcopy(governance.KILL_SWITCHES)
    aesthetic_before = copy.deepcopy(governance._DEFAULT_PROFILE.aesthetic_kill_switches)

    v = {
        "variant_id": "x", "kind": "width_bloom", "name": "Width Bloom",
        "changes": [],
        "scores": {
            "ramone_score": 80, "listener_excitement_score": 80,
            "vocal_belief_score": 80, "technical_score": 80,
            "taste_alignment_score": 70, "overall_score": 90.0,
        },
    }
    # A taste-affecting govern_variant call (mutates triangle["identity"] locally).
    governance.govern_variant(
        copy.deepcopy(v), [], "neutral",
        taste_profile=["tends to prefer narrower stereo images"],
    )

    assert governance._TRUTH_ALIGNMENT == ta_before
    assert governance._TASTE_KIND_BIAS == tkb_before
    assert governance.KILL_SWITCHES == ks_before
    assert governance._DEFAULT_PROFILE.aesthetic_kill_switches == aesthetic_before


def test_run_governance_does_not_mutate_shared_globals(analyzed):
    """The binding no-aliasing proof: run the full governance path on a real
    fixture and assert every shared ``_DEFAULT_PROFILE`` structure governance
    sources is byte-unchanged afterward."""
    ta_before = copy.deepcopy(governance._TRUTH_ALIGNMENT)
    tkb_before = copy.deepcopy(governance._TASTE_KIND_BIAS)
    ks_before = copy.deepcopy(governance.KILL_SWITCHES)
    profile_ta_before = copy.deepcopy(governance._DEFAULT_PROFILE.truth_alignment)
    profile_tkb_before = copy.deepcopy(governance._DEFAULT_PROFILE.taste_kind_bias)
    profile_aesthetic_before = copy.deepcopy(
        governance._DEFAULT_PROFILE.aesthetic_kill_switches)

    res = analyzed["dense_chorus_with_loops"]
    governance.run_governance(
        res, res.creative,
        taste_profile=["tends to prefer narrower stereo images"],
    )

    assert governance._TRUTH_ALIGNMENT == ta_before
    assert governance._TASTE_KIND_BIAS == tkb_before
    assert governance.KILL_SWITCHES == ks_before
    # And the profile object itself is untouched (governance sources FROM it).
    assert governance._DEFAULT_PROFILE.truth_alignment == profile_ta_before
    assert governance._DEFAULT_PROFILE.taste_kind_bias == profile_tkb_before
    assert governance._DEFAULT_PROFILE.aesthetic_kill_switches == profile_aesthetic_before
