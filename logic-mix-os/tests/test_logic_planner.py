"""Packet 5, Layer 1 — governed dry-run Logic action planner."""

from __future__ import annotations

import pytest

from logic_mix_os.creative import run_creative_engine
from logic_mix_os.governance_kernel import GovernanceKernel
from logic_mix_os.logic_planner import plan_logic_actions

# A hand-crafted variant recommendation exercising mapped, unmapped, and
# destructive changes in one plan.
VARIANT = {
    "variant_id": "chorus_lift_X",
    "kind": "width_bloom",
    "creative_hypothesis": "Open the chorus by blooming supporting elements while the lead stays centred.",
    "expected_strength": "emotional openness",
    "tracks_affected": ["Backing Vocals", "Lead Vocal"],
    "changes": [
        "Increase backing-vocal plate send +3 dB at chorus entry",   # -> set_send
        "High-pass supporting bus ~250 Hz",                          # -> insert_plugin (EQ)
        "Ride lead vocal +1 dB into the chorus",                     # -> automation
        "Mute decorative texture in the final pre-chorus bar",       # -> arrangement
        "Trust the performance and leave it alone",                  # -> unmapped (benign)
        "Delete source audio in place to bake the loop chop",        # -> destructive -> Class 5
    ],
}

MIX_PLAN = {
    "song_title": "Test Song",
    "per_track_actions": [
        {
            "track": "Lead Vocal", "track_id": "lead_vocal", "depth_layer": "intimate",
            "send_reverb": "Short room, very low send (~-24 dB).",
            "actions": [
                {"plugin": "Channel EQ", "setting": "High-pass ~80 Hz. Cut ~250 Hz.",
                 "reason": "Clean low-end mud.", "risk_class": 2},
            ],
            "automation": [
                {"parameter": "gain", "move": "Ride phrase endings +0.5 dB.",
                 "reason": "Vocal belief before compression.", "risk_class": 2},
            ],
        },
    ],
}

STEP_KEYS = {
    "step_id", "kind", "logic_action", "track", "target", "setting", "reason", "evidence",
    "mapping_supported", "authority_class", "authority_name", "decision", "receipt_id",
    "action_id", "rollback_plan", "reversibility", "must_not_execute_here", "ambiguous",
    "unknown_kind", "classification_reason", "cannot_apply_reason", "applied", "receipt",
}


def test_variant_input_creates_a_normalized_plan():
    plan = plan_logic_actions(VARIANT)
    assert plan["source_type"] == "variant"
    assert plan["source_id"] == "chorus_lift_X"
    assert plan["steps"] and plan["summary"]["total"] == len(VARIANT["changes"])
    assert plan["nothing_applied"] is True
    assert plan["environment"] == "dry_run_spec_only"


def test_mix_plan_input_creates_the_same_step_format():
    pv = plan_logic_actions(VARIANT)
    pm = plan_logic_actions(MIX_PLAN)
    assert pm["source_type"] == "mix_plan"
    assert pm["steps"]
    # Identical step schema regardless of input source.
    for step in pv["steps"] + pm["steps"]:
        assert set(step) == STEP_KEYS


def test_every_step_routes_through_the_kernel():
    k = GovernanceKernel()
    plan = plan_logic_actions(VARIANT, kernel=k)
    # One propose per step landed in the kernel ledger + a receipt per step.
    assert len(k.ledger()) == len(plan["steps"])
    for s in plan["steps"]:
        assert s["action_id"].startswith("act_")
        assert s["receipt_id"].startswith("rcpt_")
        assert s["receipt"]["action_id"] == s["action_id"]


def test_every_step_has_receipt_and_rollback():
    plan = plan_logic_actions(MIX_PLAN)
    for s in plan["steps"]:
        assert s["receipt"] and s["rollback_plan"]
        assert s["evidence"]  # source evidence attached


def test_class3_logic_steps_are_review_required():
    plan = plan_logic_actions(MIX_PLAN)
    # mix_plan steps are all set_send / insert_plugin / automation -> Class 3.
    assert all(s["authority_class"] == 3 for s in plan["steps"])
    assert all(s["decision"] == "review_required" for s in plan["steps"])
    assert all(s["must_not_execute_here"] is True for s in plan["steps"])


def test_class3_steps_cannot_be_marked_applied():
    k = GovernanceKernel()
    plan = plan_logic_actions(MIX_PLAN, kernel=k)
    c3 = next(s for s in plan["steps"] if s["authority_class"] == 3)
    k.approve(c3["action_id"])
    res = k.mark_applied(c3["action_id"])
    assert res["ok"] is False and "dry-run" in res["reason"].lower()


def test_destructive_markers_are_blocked():
    k = GovernanceKernel()
    plan = plan_logic_actions(VARIANT, kernel=k)
    blocked = [s for s in plan["steps"] if s["decision"] == "blocked"]
    assert blocked, "the destructive change must be blocked"
    b = blocked[0]
    assert b["authority_class"] == 5
    assert k.approve(b["action_id"])["ok"] is False
    assert k.mark_applied(b["action_id"])["ok"] is False
    assert plan["summary"]["blocked"] >= 1


def test_no_step_is_applied():
    for src in (VARIANT, MIX_PLAN):
        plan = plan_logic_actions(src)
        assert plan["nothing_applied"] is True
        assert all(s["applied"] is False for s in plan["steps"])


def test_ledger_events_appended_when_path_given(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    plan = plan_logic_actions(MIX_PLAN, ledger_path=path)
    # One propose event persisted per planned step.
    import json
    lines = [json.loads(l) for l in open(path)]
    assert len(lines) == len(plan["steps"])
    assert all(e["event_type"] == "propose" for e in lines)
    assert plan["ledger_path"] == path


def test_ledger_verifies_cleanly(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    plan = plan_logic_actions(VARIANT, ledger_path=path)
    assert plan["ledger_verification"]["ok"] is True


def test_unsupported_changes_are_surfaced():
    plan = plan_logic_actions(VARIANT)
    assert plan["unsupported"], "the unmappable change must be surfaced, not dropped"
    # The benign unmapped change still rode the fail-safe-high gate (review, not allow).
    benign = [u for u in plan["unsupported"] if u["authority_class"] == 3]
    assert benign
    # Every unmapped change is still represented as a governed step (nothing dropped).
    unsupported_ids = {u["step_id"] for u in plan["unsupported"]}
    step_ids = {s["step_id"] for s in plan["steps"]}
    assert unsupported_ids <= step_ids


def test_variant_selected_from_creative_result(analyzed):
    creative = run_creative_engine(analyzed["dense_chorus_with_loops"])
    plan = plan_logic_actions(creative)  # default: first branch's winning variant
    assert plan["source_type"] == "variant"
    assert plan["steps"]
    # A specific variant id can be selected too.
    some_vid = creative["branches"][0]["variants"][0]["variant_id"]
    plan2 = plan_logic_actions(creative, variant_id=some_vid)
    assert plan2["source_id"] == some_vid


def test_real_mix_plan_from_pipeline(analyzed):
    mix_plan = analyzed["dense_chorus_with_loops"].mix_plan
    plan = plan_logic_actions(mix_plan)
    assert plan["source_type"] == "mix_plan"
    assert plan["steps"]
    assert all(s["applied"] is False for s in plan["steps"])


def test_unrecognised_source_raises():
    with pytest.raises(ValueError):
        plan_logic_actions({"nonsense": True})
