"""Mix plan, checklist, output integrity, and non-destructive guarantees."""

from __future__ import annotations

from logic_mix_os.pipeline import write_artifacts
from logic_mix_os.renderers.checklist_renderer import render_logic_checklist
from logic_mix_os.validation.output_validator import (
    load_schema,
    validate_instance,
    validate_output,
)


def test_mix_plan_validates(analyzed):
    plan = analyzed["dense_chorus_with_loops"].mix_plan
    schema = load_schema("mix_plan.schema.json")
    assert validate_instance(plan, schema) == []


def test_next_pass_capped_at_five(analyzed):
    for res in analyzed.values():
        nxt = res.mix_plan["next_pass"]
        assert 0 <= len(nxt) <= 5
        for i, item in enumerate(nxt, start=1):
            assert item["priority"] == i
            assert item["title"] and item["detail"]


def test_full_output_set_written_and_valid(analyzed, tmp_path):
    res = analyzed["dense_chorus_with_loops"]
    write_artifacts(res, tmp_path)
    report = validate_output(tmp_path)
    assert report["ok"], report["errors"]


def test_logic_checklist_is_executable(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    md = render_logic_checklist(res.mix_plan)
    assert "# Logic Action Checklist" in md
    assert "Non-destructive" in md
    # mentions at least one real track and a stock Logic plugin
    assert "Lead Vocal" in md
    assert "Channel EQ" in md or "Compressor" in md


def test_no_destructive_actions_recommended(analyzed):
    for res in analyzed.values():
        for track in res.mix_plan["per_track_actions"]:
            for action in track["actions"]:
                assert action["risk_class"] < 5, "Class 5 actions must never be recommended"
            assert track["risk_class"] < 5


def test_mute_candidates_have_reasons(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    for m in res.mix_plan["mute_candidates"]:
        assert m["element"]
        assert m["reason"]


def test_loop_appears_in_width_control_next_pass(analyzed):
    res = analyzed["splice_loop_problem"]
    titles = " ".join(i["title"] + " " + i["detail"] for i in res.mix_plan["next_pass"])
    assert "Splice Loop" in titles or "width" in titles.lower()


def test_depth_map_validates(analyzed):
    schema = load_schema("depth_map.schema.json")
    for res in analyzed.values():
        assert validate_instance(res.depth_map, schema) == []
