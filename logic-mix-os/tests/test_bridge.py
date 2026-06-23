"""Logic bridge tests (build packet 41-42) — export, codegen, safe dry-run."""

from __future__ import annotations

from logic_mix_os.bridge.applescript_bridge import generate_applescript, generate_shortcuts
from logic_mix_os.bridge.executor import EXECUTION_MODES, dry_run
from logic_mix_os.bridge.exporter import export_actions


def test_export_actions_shape(analyzed):
    actions = export_actions(analyzed["dense_chorus_with_loops"].mix_plan)
    assert actions
    for a in actions:
        assert {"id", "track", "type", "plugin", "settings", "risk_class"} <= set(a)
        assert a["type"] in {"insert_plugin", "set_send", "automation", "arrangement"}


def test_applescript_is_scaffolding_only(analyzed):
    actions = export_actions(analyzed["dense_chorus_with_loops"].mix_plan)
    script = generate_applescript(actions)
    assert "does not run automatically" in script
    assert "No source audio is modified" in script
    # every executable instruction is commented out (lines start with -- or tell/blank)
    for line in script.splitlines():
        s = line.strip()
        if s and not s.startswith("--"):
            assert s.startswith("tell ") or s.startswith("end ")


def test_shortcuts_export_is_data(analyzed):
    actions = export_actions(analyzed["dense_chorus_with_loops"].mix_plan)
    sc = generate_shortcuts(actions)
    assert any(s["action"] == "SelectTrack" for s in sc)


def test_dry_run_never_executes(analyzed):
    actions = export_actions(analyzed["dense_chorus_with_loops"].mix_plan)
    log = dry_run(actions, review_mode="safe_auto_apply")
    assert log["executed"] == []  # by design, nothing is ever executed
    assert "no Logic session or audio was modified" in log["summary"]["note"]
    assert len(EXECUTION_MODES) == 4


def test_dry_run_blocks_destructive_action():
    actions = [
        {"id": "x:0", "track": "T", "type": "insert_plugin", "plugin": "X",
         "settings": "overwrite the original file", "risk_class": 2},
        {"id": "x:1", "track": "T", "type": "insert_plugin", "plugin": "Y",
         "settings": "ok", "risk_class": 5},
        {"id": "x:2", "track": "T", "type": "insert_plugin", "plugin": "Z",
         "settings": "cut 250 Hz", "risk_class": 2},
    ]
    log = dry_run(actions, review_mode="safe_auto_apply")
    assert len(log["blocked"]) == 2
    assert log["would_apply"] == ["x:2"]


def test_review_modes_change_disposition(analyzed):
    actions = export_actions(analyzed["simple_vocal_piano_song"].mix_plan)
    observe = dry_run(actions, review_mode="observe_only")
    assert observe["observed"] and not observe["would_apply"]
    approve = dry_run(actions, review_mode="approve_before_apply")
    assert approve["pending_approval"] and not approve["would_apply"]
