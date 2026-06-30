"""Album-context next-pass planner tests (P-010 — cross-song coherence axis).

``plan_next_pass`` gains an opt-in trailing ``album_context`` arg (AFTER the
P-008 ``history`` arg). When supplied with a per-song delta dict
``{"brightness_delta": float|None, "lufs_delta": float|None}`` whose brightness
delta exceeds 0.15 (or whose lufs delta exceeds 3), the planner appends EXACTLY
ONE bounded, non-destructive, evidence-tagged item titled ``"Album coherence"``
at priority 45 — strictly below every truth-driven move (vocal 90, section 80,
width 70, depth 60, low-end 50). These tests pin:

  (a) outlier context -> exactly one ``"Album coherence"`` item, ``detail`` names
      the signed delta, it carries ``evidence``, and its emitted 1-based
      ``priority`` rank is BELOW the vocal-belief move's;
  (b) ``album_context=None`` AND a non-outlier (under-threshold) context -> no
      ``"Album coherence"`` item;
  (c) byte-identical default path: ``plan_next_pass(args...)`` deep-equals
      ``plan_next_pass(args..., album_context=None)`` (no new title);
  (d) determinism: same context twice -> identical item;
  (e) both axes trip -> ONE item only, brightness chosen (deterministic
      tie-break: brightness before loudness).

Pure function of the supplied deltas + the two fixed thresholds. No time/IO/random.
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os.planners.next_pass_planner import plan_next_pass


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _plan(res, history=None, album_context=None):
    """Call the planner exactly as the pipeline does, with the opt-in arg."""
    return plan_next_pass(
        res.records, res.doctrine_score, res.masking_report, res.section_analysis,
        history=history, album_context=album_context,
    )


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True)


def _coherence_items(plan):
    return [i for i in plan if i["title"] == "Album coherence"]


# --------------------------------------------------------------------------- #
# (a) Outlier context -> exactly one "Album coherence" item below the vocal move.
# --------------------------------------------------------------------------- #
def test_brightness_outlier_surfaces_one_album_item(analyzed):
    # ``splice_loop_problem`` surfaces only 4 truth-driven moves, leaving a take-5
    # slot for the bounded (priority-45) album item to land in.
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": 0.4, "lufs_delta": None}
    plan = _plan(res, album_context=ctx)

    items = _coherence_items(plan)
    assert len(items) == 1, plan
    item = items[0]

    # detail names the signed delta (+0.40); evidence line present.
    assert "+0.4" in item["detail"]
    assert "evidence" in item
    assert "brightness_delta" in item["evidence"]
    assert "+0.4" in item["evidence"]
    assert "threshold 0.15" in item["evidence"]

    # advisory / reversible / bounded: no destructive widen+lead-vocal phrasing,
    # no risk_class>=5 leaking in.
    assert "widen" not in item["detail"].lower()
    assert "risk_class" not in item

    # its emitted 1-based rank is strictly BELOW the vocal-belief move's.
    titles = [i["title"] for i in plan]
    assert "Vocal belief" in titles, "fixture must surface the vocal move"
    vocal = next(i for i in plan if i["title"] == "Vocal belief")
    assert item["priority"] > vocal["priority"]


def test_lufs_outlier_surfaces_album_item(analyzed):
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": None, "lufs_delta": 5}
    plan = _plan(res, album_context=ctx)

    items = _coherence_items(plan)
    assert len(items) == 1
    item = items[0]
    assert "lufs_delta" in item["evidence"]
    assert "threshold 3" in item["evidence"]
    assert "+5" in item["detail"]


# --------------------------------------------------------------------------- #
# (b) None + under-threshold context -> no album item.
# --------------------------------------------------------------------------- #
def test_no_album_item_when_context_none(analyzed):
    for name, res in analyzed.items():
        plan = _plan(res, album_context=None)
        assert _coherence_items(plan) == [], name


def test_no_album_item_when_under_threshold(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    ctx = {"brightness_delta": 0.05, "lufs_delta": 1}
    plan = _plan(res, album_context=ctx)
    assert _coherence_items(plan) == []


def test_no_album_item_when_all_none(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    ctx = {"brightness_delta": None, "lufs_delta": None}
    plan = _plan(res, album_context=ctx)
    assert _coherence_items(plan) == []


def test_no_album_item_when_empty_context(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    assert _coherence_items(_plan(res, album_context={})) == []


# --------------------------------------------------------------------------- #
# (c) Byte-identical default path: no arg == album_context=None.
# --------------------------------------------------------------------------- #
def test_default_path_byte_identical(analyzed):
    for name, res in analyzed.items():
        base = plan_next_pass(
            res.records, res.doctrine_score, res.masking_report, res.section_analysis,
        )
        none = _plan(res, album_context=None)
        assert _canon(base) == _canon(none), name
        # No "Album coherence" title and no evidence key leaks onto the default path.
        for item in none:
            assert item["title"] != "Album coherence"


# --------------------------------------------------------------------------- #
# (d) Determinism.
# --------------------------------------------------------------------------- #
def test_album_item_is_deterministic(analyzed):
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": 0.4, "lufs_delta": None}
    a = _plan(res, album_context=ctx)
    b = _plan(res, album_context=ctx)
    assert _canon(a) == _canon(b)
    assert len(_coherence_items(a)) == 1


# --------------------------------------------------------------------------- #
# (e) Both axes trip -> one item only, brightness chosen (tie-break).
# --------------------------------------------------------------------------- #
def test_both_axes_trip_chooses_brightness_one_item(analyzed):
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": 0.4, "lufs_delta": 5}
    plan = _plan(res, album_context=ctx)

    items = _coherence_items(plan)
    assert len(items) == 1, plan
    item = items[0]
    # Brightness wins the deterministic tie-break.
    assert "brightness_delta" in item["evidence"]
    assert "lufs_delta" not in item["evidence"]


def test_negative_brightness_outlier_signs_correctly(analyzed):
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": -0.4, "lufs_delta": None}
    plan = _plan(res, album_context=ctx)
    items = _coherence_items(plan)
    assert len(items) == 1
    item = items[0]
    assert "-0.4" in item["evidence"]
    assert "-0.4" in item["detail"]


# --------------------------------------------------------------------------- #
# (f) Cosmetic float-round (P-011 Commit-2): a long real-float delta renders
#     rounded to 2 dp in detail/evidence, while the outlier LOGIC still uses the
#     full-precision delta (threshold comparison unrounded).
# --------------------------------------------------------------------------- #
def test_long_float_brightness_delta_renders_rounded(analyzed):
    res = analyzed["splice_loop_problem"]
    # A realistic CLI-derived float (e.g. song - statistics.mean(...)) that the
    # old code would have rendered as a long repr like ``0.2866666...``.
    ctx = {"brightness_delta": 0.28666666666666663, "lufs_delta": None}
    plan = _plan(res, album_context=ctx)
    items = _coherence_items(plan)
    assert len(items) == 1
    item = items[0]

    # The DISPLAY is rounded to 2 dp (+0.29), never the long repr.
    assert "+0.29" in item["detail"]
    assert "+0.29" in item["evidence"]
    assert "0.2866" not in item["detail"]
    assert "0.2866" not in item["evidence"]


def test_long_float_lufs_delta_renders_rounded(analyzed):
    res = analyzed["splice_loop_problem"]
    ctx = {"brightness_delta": None, "lufs_delta": 3.144444444444445}
    plan = _plan(res, album_context=ctx)
    items = _coherence_items(plan)
    assert len(items) == 1
    item = items[0]
    assert "+3.14" in item["detail"]
    assert "+3.14" in item["evidence"]
    assert "3.1444" not in item["detail"]
    assert "3.1444" not in item["evidence"]


def test_outlier_logic_uses_full_precision_not_rounded(analyzed):
    res = analyzed["splice_loop_problem"]
    # 0.151 > 0.15 threshold on the FULL-precision value, but rounds to 0.15.
    # If the threshold compared the rounded display (0.15) it would NOT trip;
    # it must trip because the logic uses the full-precision delta.
    ctx = {"brightness_delta": 0.151, "lufs_delta": None}
    plan = _plan(res, album_context=ctx)
    items = _coherence_items(plan)
    assert len(items) == 1, "full-precision 0.151 must exceed the 0.15 threshold"
