"""P-030 — THE ARTIFACT-CONTRACT MIGRATION PROOF.

The two doctrine dimensions historically named for the reference producers now
carry aesthetic-descriptive contract keys:

    halee_score  -> physical_space_score      (physical space / depth / spatial realism)
    ramone_score -> emotional_hierarchy_score (emotional hierarchy / vocal belief /
                                               narrative priority)

Clean break for public artifacts: no old-key aliases in emitted doctrine
artifacts, schemas, renderers, Cowork responses, samples or goldens. The ONE
compatibility carve-out is ``memory.py``'s READ-ONLY dual-read of persisted
local mix-pass history (old-key records written before the migration stay
readable; new keys are preferred when both are present; old keys are never
written). The verdict filename is neutral: ``mix_verdict.md``, not
per-producer.

Same math, same scores, same differential behavior — only the key names
carrying them changed. The profile stays named for the producers
(``halee_ramone``, display_name "Roy Halee / Phil Ramone", its prose and
search-mode vocabulary); the CONTRACT does not.

These are the user-specified 17 migration tests, in order.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from logic_mix_os import memory as memory_module
from logic_mix_os import regression
from logic_mix_os.cowork import run_command
from logic_mix_os.memory import ProjectMemory
from logic_mix_os.pipeline import write_artifacts
from logic_mix_os.renderers import html_dashboard, markdown_renderer, operator_view
from logic_mix_os.validation.output_validator import load_schema

_ROOT = Path(__file__).resolve().parent.parent

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

OLD_KEYS = ("halee_score", "ramone_score")
NEW_KEYS = ("physical_space_score", "emotional_hierarchy_score")
OLD_EVIDENCE_KEYS = ("halee", "ramone")
NEW_EVIDENCE_KEYS = ("physical_space", "emotional_hierarchy")


class _StubResult:
    """The minimal result surface ``memory.record_pass`` consumes."""

    def __init__(self, doctrine_score, mix_plan=None):
        self.doctrine_score = doctrine_score
        self.mix_plan = mix_plan if mix_plan is not None else {"next_pass": []}


def _stub(physical_space=60.0, emotional_hierarchy=60.0, overall=60.0):
    return _StubResult({
        "overall_mix_readiness_score": overall,
        "physical_space_score": physical_space,
        "emotional_hierarchy_score": emotional_hierarchy,
        "static_mix_score": 60.0,
        "dynamic_mix_score": 60.0,
        "section_contrast_score": 60.0,
        "depth_hierarchy_score": 60.0,
        "vocal_centrality_score": 60.0,
    }, {"translation_score": 60.0, "mono_compatibility_score": 60.0, "next_pass": []})


def _seed_history(tmp_path, scores):
    """Write ONE persisted mix-pass record directly (simulating stored data)."""
    mem = ProjectMemory(tmp_path / "mem")
    record = {
        "pass_name": "seeded", "date": "2026-01-01T00:00:00+00:00",
        "input_bounce": None, "scores": scores, "changes_made": [],
        "improved": [], "got_worse": [], "revert_candidates": [],
        "next_recommended": [],
    }
    mem.passes_path.write_text(json.dumps([record], indent=2) + "\n")
    return mem


# =========================================================================== #
# 1-4. The emitted doctrine_score artifact: new keys present, old keys gone.
# =========================================================================== #
@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_1_doctrine_artifacts_use_physical_space_score(name, analyzed):
    ds = analyzed[name].doctrine_score
    assert "physical_space_score" in ds
    assert isinstance(ds["physical_space_score"], float)
    assert "physical_space" in ds["evidence"]


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_2_doctrine_artifacts_use_emotional_hierarchy_score(name, analyzed):
    ds = analyzed[name].doctrine_score
    assert "emotional_hierarchy_score" in ds
    assert isinstance(ds["emotional_hierarchy_score"], float)
    assert "emotional_hierarchy" in ds["evidence"]


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_3_doctrine_artifacts_do_not_emit_halee_score(name, analyzed):
    res = analyzed[name]
    assert "halee_score" not in res.doctrine_score
    assert "halee" not in res.doctrine_score["evidence"]
    assert "halee_score" not in res.mix_plan
    for branch in res.creative["branches"]:
        for v in branch["variants"]:
            assert "halee_score" not in v["scores"], v["variant_id"]


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_4_doctrine_artifacts_do_not_emit_ramone_score(name, analyzed):
    res = analyzed[name]
    assert "ramone_score" not in res.doctrine_score
    assert "ramone" not in res.doctrine_score["evidence"]
    assert "ramone_score" not in res.mix_plan
    for branch in res.creative["branches"]:
        for v in branch["variants"]:
            assert "ramone_score" not in v["scores"], v["variant_id"]


# =========================================================================== #
# 5-6. Schemas: require the new keys; carry no old keys.
# =========================================================================== #
def test_5_schemas_require_the_new_keys():
    ds_schema = load_schema("doctrine_score.schema.json")
    for key in NEW_KEYS:
        assert key in ds_schema["required"]
        assert key in ds_schema["properties"]
    mp_schema = load_schema("mix_plan.schema.json")
    for key in NEW_KEYS:
        assert key in mp_schema["properties"]


def test_6_schemas_do_not_require_old_keys():
    for schema_file in ("doctrine_score.schema.json", "mix_plan.schema.json"):
        schema = load_schema(schema_file)
        blob = json.dumps(schema)
        for key in OLD_KEYS:
            assert key not in schema.get("required", []), (schema_file, key)
            assert key not in schema["properties"], (schema_file, key)
            assert key not in blob, (schema_file, key)


# =========================================================================== #
# 7. The Cowork surface returns the new keys only (pass-through dicts).
# =========================================================================== #
def test_7_cowork_surface_returns_new_keys_only(analyzed):
    ctx = {"result": analyzed["dense_chorus_with_loops"], "memory": None}
    scores = run_command("score_mix", ctx)
    for key in NEW_KEYS:
        assert key in scores
    validated = run_command("validate_mix_pass", ctx)
    for key in NEW_KEYS:
        assert key in validated["scores"]
    for payload in (scores, validated):
        blob = json.dumps(payload)
        for key in OLD_KEYS:
            assert key not in blob


# =========================================================================== #
# 8. Renderers display producer-agnostic labels for the two dimensions.
# =========================================================================== #
def test_8_renderers_display_producer_agnostic_labels(analyzed):
    res = analyzed["dense_chorus_with_loops"]

    # Markdown verdict: the score-table labels are observational. The profile's
    # own confidence prose (its authored voice) may name the producers — so the
    # label check is scoped to the Scores section.
    md = markdown_renderer.render_mix_verdict(res.mix_plan, res.doctrine_score)
    assert "# Mix Verdict" in md
    scores_section = md.split("## Scores", 1)[1].split("##", 1)[0]
    assert "Physical space / depth" in scores_section
    assert "Emotional hierarchy / vocal belief" in scores_section
    assert "Halee" not in scores_section and "Ramone" not in scores_section
    assert "**The physical-space test:**" in md
    assert "**The emotional-hierarchy test:**" in md

    # Operator view: the SCORES block labels are producer-agnostic. (Engine
    # action prose elsewhere on the surface is out of the LABEL contract.)
    status = operator_view.render_status(res)
    scores_block = status.split(" SCORES", 1)[1].split("\n\n", 1)[0]
    assert "Physical space" in scores_block and "Emotional hierarchy" in scores_block
    assert "Halee" not in scores_block and "Ramone" not in scores_block

    # Dashboard: the score-grid card labels are producer-agnostic.
    html = html_dashboard.render_dashboard(res)
    score_card = html.split('id="scores"', 1)[1].split("</section>", 1)[0]
    assert "Physical space" in score_card and "Emotional hierarchy" in score_card
    assert "Halee" not in score_card and "Ramone" not in score_card
    assert "Roy Halee (space)" not in html and "Phil Ramone (vocal)" not in html


# =========================================================================== #
# 9. Committed samples use the new keys only.
# =========================================================================== #
def test_9_committed_samples_use_new_keys_only():
    sample_dir = _ROOT / "examples" / "sample_output"
    for old in OLD_KEYS:
        for path in sorted(sample_dir.iterdir()):
            if path.is_file():
                assert old not in path.read_text(encoding="utf-8"), (path.name, old)
    ds = json.loads((sample_dir / "doctrine_score.json").read_text(encoding="utf-8"))
    for key in NEW_KEYS:
        assert key in ds
    for key in NEW_EVIDENCE_KEYS:
        assert key in ds["evidence"]
    for key in OLD_EVIDENCE_KEYS:
        assert key not in ds["evidence"]
    mp = json.loads((sample_dir / "mix_plan.json").read_text(encoding="utf-8"))
    for key in NEW_KEYS:
        assert key in mp
    creative = (sample_dir / "creative.json").read_text(encoding="utf-8")
    for key in NEW_KEYS:
        assert key in creative


# =========================================================================== #
# 10. Goldens: consciously regenerated on the new contract AND matching the
#     live output (same values, renamed keys).
# =========================================================================== #
@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_10_goldens_regenerated_and_match_live_output(name, analyzed):
    golden = json.loads(
        (_ROOT / "fixtures" / name / "golden" / "snapshot.json").read_text(encoding="utf-8")
    )
    for key in NEW_KEYS:
        assert key in golden["scores"], key
    for key in OLD_KEYS:
        assert key not in golden["scores"], key
    live = regression.build_snapshot(analyzed[name])
    assert live == golden


# =========================================================================== #
# 11. The regression SCORE_KEYS allow-list uses the new keys.
# =========================================================================== #
def test_11_regression_score_keys_use_new_keys():
    for key in NEW_KEYS:
        assert key in regression.SCORE_KEYS
    for key in OLD_KEYS:
        assert key not in regression.SCORE_KEYS
    # memory's score-key list migrated the same way.
    for key in NEW_KEYS:
        assert key in memory_module.SCORE_KEYS
    for key in OLD_KEYS:
        assert key not in memory_module.SCORE_KEYS


# =========================================================================== #
# 12-15. The memory.py dual-read carve-out (read-only compat for persisted
#        local history).
# =========================================================================== #
def test_12_memory_reads_new_key_history(tmp_path):
    mem = _seed_history(tmp_path, {
        "overall_mix_readiness_score": 50.0,
        "physical_space_score": 50.0, "emotional_hierarchy_score": 70.0,
    })
    record = mem.record_pass("p2", _stub(physical_space=60.0, emotional_hierarchy=60.0, overall=60.0))
    assert "physical_space_score 50.0->60.0" in record["improved"]
    assert "emotional_hierarchy_score 70.0->60.0" in record["got_worse"]


def test_13_memory_reads_old_key_history(tmp_path):
    """A pre-migration record (old producer-named keys) is still readable: the
    comparisons fire off the legacy values instead of silently skipping."""
    mem = _seed_history(tmp_path, {
        "overall_mix_readiness_score": 50.0,
        "halee_score": 50.0, "ramone_score": 70.0,
    })
    record = mem.record_pass("p2", _stub(physical_space=60.0, emotional_hierarchy=60.0, overall=60.0))
    assert "physical_space_score 50.0->60.0" in record["improved"]
    assert "emotional_hierarchy_score 70.0->60.0" in record["got_worse"]


def test_14_memory_prefers_new_keys_when_both_present(tmp_path):
    """When a stored record carries BOTH keys, the new key wins: the deltas are
    computed against the new-key values (10.0/95.0 old values would flip both
    readings if the legacy keys were preferred)."""
    mem = _seed_history(tmp_path, {
        "overall_mix_readiness_score": 50.0,
        "physical_space_score": 50.0, "halee_score": 10.0,
        "emotional_hierarchy_score": 70.0, "ramone_score": 95.0,
    })
    record = mem.record_pass("p2", _stub(physical_space=60.0, emotional_hierarchy=60.0, overall=60.0))
    assert "physical_space_score 50.0->60.0" in record["improved"]
    assert "emotional_hierarchy_score 70.0->60.0" in record["got_worse"]


def test_15_memory_never_writes_old_keys(tmp_path):
    """Even when the EXISTING history carries old keys, the newly recorded pass
    is written with the new contract only — the dual-read is read-only."""
    mem = _seed_history(tmp_path, {
        "overall_mix_readiness_score": 50.0,
        "halee_score": 50.0, "ramone_score": 70.0,
    })
    record = mem.record_pass("p2", _stub())
    for key in NEW_KEYS:
        assert key in record["scores"]
    for key in OLD_KEYS:
        assert key not in record["scores"]
    # The newly persisted record on disk carries no old keys either (the seeded
    # historical record is left untouched — read-only compat, no rewriting).
    history = json.loads(mem.passes_path.read_text())
    assert "halee_score" in history[0]["scores"]          # history untouched
    for key in OLD_KEYS:
        assert key not in history[-1]["scores"], key       # new record clean


# =========================================================================== #
# 16-17. The neutral verdict filename.
# =========================================================================== #
def test_16_verdict_filename_is_mix_verdict(tmp_path, analyzed):
    written = write_artifacts(analyzed["simple_vocal_piano_song"], tmp_path)
    assert (tmp_path / "mix_verdict.md").exists()
    assert str(tmp_path / "mix_verdict.md") in written
    assert (tmp_path / "mix_verdict.md").read_text(encoding="utf-8").startswith("# Mix Verdict")


def test_17_no_old_verdict_filename_written(tmp_path, analyzed):
    written = write_artifacts(analyzed["simple_vocal_piano_song"], tmp_path)
    assert not (tmp_path / "halee_ramone_mix_verdict.md").exists()
    assert all("halee_ramone_mix_verdict.md" not in w for w in written)
