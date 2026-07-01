"""Cowork command surface + section-44 schema tests."""

from __future__ import annotations

import pytest

from logic_mix_os.bridge.exporter import export_actions
from logic_mix_os.cowork import COMMANDS, list_commands, run_command
from logic_mix_os.validation.output_validator import load_schema, validate_instance


@pytest.fixture()
def ctx(analyzed):
    return {"result": analyzed["dense_chorus_with_loops"], "memory": None}


def test_command_catalog_is_broad():
    cmds = {c["command"] for c in list_commands()}
    # a representative spread of section-43 commands
    for name in ["detect_source_materials", "detect_track_identities", "assign_depth_layers",
                 "detect_masking", "generate_mix_plan", "score_mix", "suggest_next_pass",
                 "run_creative_engine", "run_governance", "map_manipulation_capabilities"]:
        assert name in cmds
    # P-019 added record_mix_pass (32 -> 33); P-020 added describe_session (33 -> 34).
    assert len(COMMANDS) == 34


def test_commands_return_jsonable(ctx):
    import json
    for name in COMMANDS:
        if name in {"override_track_identity", "write_mix_decision", "update_taste_calibration"}:
            continue  # need params / memory
        out = run_command(name, ctx)
        json.dumps(out)  # must not raise


def test_override_identity_command():
    # Use a FRESH analysis: this command mutates state, so it must not touch the
    # shared session fixture (which the golden-snapshot test relies on).
    import pathlib
    from logic_mix_os.cowork import build_context
    from logic_mix_os.project import load_manifest
    base = pathlib.Path(__file__).resolve().parent.parent / "fixtures" / "simple_vocal_piano_song"
    ctx = build_context(str(base / "stems"), load_manifest(base / "project_manifest.json"))
    tid = ctx["result"].track_identity[0]["track_id"]
    out = run_command("override_track_identity", ctx, track_id=tid, identity="organ")
    assert out["updated"]["instrument_identity"] == "organ"
    assert out["updated"]["identity_family"] == "keys"


def test_write_mix_decision_tags_event_type(tmp_path):
    # Drive the write_mix_decision cowork command through run_command with a
    # memory-backed ctx, then read the ledger and assert the entry is tagged
    # with the mix_decision event type (P-004).
    from logic_mix_os.memory import ProjectMemory
    mem = ProjectMemory(tmp_path / "mem")
    ctx = {"result": None, "memory": mem}
    out = run_command("write_mix_decision", ctx,
                      decision={"decision": "widen chorus", "reason": "felt narrow"})
    assert out["event_type"] == "mix_decision"
    ledger = mem.ledger()
    assert ledger and ledger[-1]["event_type"] == "mix_decision"


def test_review_uncertain_uses_threshold(ctx):
    out = run_command("review_uncertain_identities", ctx, threshold=2.0)  # everything below 2.0
    assert len(out) == len(ctx["result"].track_identity)


def test_unknown_command_raises(ctx):
    with pytest.raises(KeyError):
        run_command("does_not_exist", ctx)


def test_logic_action_schema_validates(analyzed):
    actions = export_actions(analyzed["dense_chorus_with_loops"].mix_plan)
    schema = load_schema("logic_action.schema.json")
    assert validate_instance(actions, schema) == []


def test_reference_and_manipulation_schemas_load():
    for name in ["reference_delta.schema.json", "mix_decision.schema.json",
                 "mix_pass_score.schema.json", "manipulation_capabilities.schema.json",
                 "automation_plan.schema.json"]:
        schema = load_schema(name)
        assert schema.get("title")


def test_manipulation_capabilities_validate(analyzed):
    caps = run_command("map_manipulation_capabilities",
                       {"result": analyzed["dense_chorus_with_loops"], "memory": None})
    schema = load_schema("manipulation_capabilities.schema.json")
    assert validate_instance(caps, schema) == []


def test_automation_plan_validates(analyzed):
    plan = analyzed["dense_chorus_with_loops"].mix_plan["automation_plan"]
    # the per-track "rides" entry uses section "*"; schema is permissive on that
    schema = load_schema("automation_plan.schema.json")
    assert validate_instance(plan, schema) == []
