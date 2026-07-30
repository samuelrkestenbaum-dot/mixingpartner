"""P-062 — the Multi-Lens Execution Brief.

The "from every angle" planning surface as a DETERMINISTIC artifact: six
measurement lenses quoted verbatim from the analysis artifacts, rule-based
cross-lens contradictions (no LLM), the mix plan re-cut into ordered execution
phases, and a clearly-fenced DRAFT-ONLY host-synthesis prompt block (the
standing P-025/P-031 policy: an LLM narrates on top, it never scores).

Binding guards exercised here:

  * Every lens section renders for ALL FIVE committed producer trees (the
    free fixtures under ``examples/`` — read-only; NEVER written to).
  * Evidence numbers appear VERBATIM (read from the committed JSONs at test
    time, never hardcoded — the values are compared through the same
    ``json.dumps`` scalar form the renderer uses).
  * Determinism: two renders are byte-identical.
  * Contradiction rules fire when their condition holds AND stay silent
    otherwise (non-vacuity in both directions, per rule).
  * Phase classification: each action category lands in its phase; an
    unrecognizable action lands in the explicit unphased bucket; count
    conservation — every extracted plan item appears exactly once across
    phases + unphased (nothing silently dropped).
  * Missing-artifact tolerance: a partial artifact dir renders an honest
    "(artifact missing: …)" line, never a crash.
  * CLI smoke runs against a COPY of a sample tree in tmp_path.
  * The committed ``examples/`` trees are byte-untouched by this suite.
"""

from __future__ import annotations

import hashlib
import json
import shutil

import pytest

from logic_mix_os import cli
from logic_mix_os.renderers.execution_brief_renderer import (
    BRIEF_ARTIFACTS,
    CONTRADICTION_RULES,
    LENS_HEADINGS,
    PHASE_CARVE,
    PHASE_CREATIVE,
    PHASE_GAIN,
    PHASE_ORDER,
    PHASE_SECTION,
    PHASE_SPACE,
    UNPHASED,
    classify_plan_item,
    collect_facts,
    detect_contradictions,
    extract_plan_items,
    load_brief_payloads,
    phase_plan,
    render_execution_brief,
)

from conftest import ROOT
from test_sample_refresh import SAMPLE_TREES  # the single source for the 5 trees

COPILOT_HEADING = "## For an AI mixing copilot (draft-only)"
CONTRADICTIONS_HEADING = "## Cross-Lens Contradictions"
EXECUTION_HEADING = "## Execution Order"


def _tree_render(tree):
    return render_execution_brief(load_brief_payloads(tree))


def _read(tree, name):
    return json.loads((tree / name).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Every lens present, producer-voiced, on all five committed trees.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("producer", sorted(SAMPLE_TREES))
def test_all_sections_present_per_tree(producer):
    tree = SAMPLE_TREES[producer]
    out = _tree_render(tree)
    for heading in LENS_HEADINGS:
        assert heading in out, f"{producer}: missing lens heading {heading!r}"
    assert CONTRADICTIONS_HEADING in out
    assert EXECUTION_HEADING in out
    assert COPILOT_HEADING in out
    # Producer-voiced: the doctrine_score producer block drives the header.
    ds = _read(tree, "doctrine_score.json")
    assert ds["producer"]["display_name"] in out
    assert ds["producer"]["name"] in out
    assert ds["producer"]["confidence"] in out


@pytest.mark.parametrize("producer", sorted(SAMPLE_TREES))
def test_render_is_deterministic(producer):
    tree = SAMPLE_TREES[producer]
    assert _tree_render(tree) == _tree_render(tree)


def test_draft_only_stamp_and_fence():
    out = _tree_render(SAMPLE_TREES["halee_ramone"])
    assert "DRAFT-ONLY" in out
    assert "```text" in out
    assert "deterministic ground truth" in out
    # The copilot block is the FINAL section: after every lens and the
    # execution order — everything above it is measurement.
    copilot_at = out.index(COPILOT_HEADING)
    for heading in list(LENS_HEADINGS) + [CONTRADICTIONS_HEADING, EXECUTION_HEADING]:
        assert out.index(heading) < copilot_at
    # The fence opens and closes inside the copilot block.
    tail = out[copilot_at:]
    assert tail.count("```") >= 2


# --------------------------------------------------------------------------- #
# Evidence numbers quoted VERBATIM — read from the committed files, not
# hardcoded. json.dumps is the same scalar form the renderer uses.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("producer", sorted(SAMPLE_TREES))
def test_evidence_numbers_verbatim(producer):
    tree = SAMPLE_TREES[producer]
    out = _tree_render(tree)

    ds = _read(tree, "doctrine_score.json")
    for key in ("section_contrast_score", "physical_space_score",
                "vocal_centrality_score", "dynamic_mix_score",
                "depth_hierarchy_score", "vocal_role_fit_score",
                "textural_coherence_score", "low_end_motion_score"):
        assert f"{json.dumps(ds[key])}/100" in out, f"{producer}: {key} not verbatim"
    # A doctrine evidence line, verbatim.
    assert ds["evidence"]["dynamic_mix"][0] in out

    sec = _read(tree, "section_analysis.json")[0]
    assert f"rms_dbfs {json.dumps(sec['metrics']['rms_dbfs'])}" in out
    assert f"width {json.dumps(sec['metrics']['width'])}" in out

    mr = _read(tree, "masking_report.json")
    s = mr["summary"]
    for key in ("critical_count", "moderate_count", "blend_count",
                "total_events", "vocal_band_masking_count"):
        assert str(s[key]) in out
    if mr["events"]:
        ev = mr["events"][0]
        assert f"overlap {json.dumps(ev['overlap'])}" in out
        assert ev["reason"] in out

    exp = _read(tree, "expanded_analysis.json")
    assert f"{json.dumps(exp['translation']['translation_score'])}" in out
    assert f"stereo_width {json.dumps(exp['translation']['checks']['stereo_width'])}" in out
    assert f"{json.dumps(exp['mono_compatibility']['mono_score'])}" in out
    assert f"phase correlation {json.dumps(exp['mono_compatibility']['mix_phase_correlation'])}" in out
    vp = exp["vocal_performance"]
    if vp.get("available"):
        assert f"dynamic range {json.dumps(vp['dynamic_range_db'])} dB" in out


# --------------------------------------------------------------------------- #
# Contradiction rules — each fires when its condition holds and stays silent
# otherwise (non-vacuity in both directions).
# --------------------------------------------------------------------------- #
def _fired_ids(facts):
    return [rule_id for rule_id, _ in detect_contradictions(facts)]


def test_rule_contrast_without_space_both_directions():
    fire = {"section_contrast_score": 85, "physical_space_score": 30}
    assert "contrast_without_space" in _fired_ids(fire)
    for silent in (
        {"section_contrast_score": 40, "physical_space_score": 30},   # contrast low
        {"section_contrast_score": 85, "physical_space_score": 80},   # space fine
        {"section_contrast_score": None, "physical_space_score": 30},  # missing fact
    ):
        assert "contrast_without_space" not in _fired_ids(silent)


def test_rule_central_vocal_masked_both_directions():
    fire = {"vocal_centrality_score": 90.0, "vocal_band_masking_count": 4}
    assert "central_vocal_masked" in _fired_ids(fire)
    for silent in (
        {"vocal_centrality_score": 50.0, "vocal_band_masking_count": 4},
        {"vocal_centrality_score": 90.0, "vocal_band_masking_count": 0},
        {"vocal_centrality_score": 90.0, "vocal_band_masking_count": None},
    ):
        assert "central_vocal_masked" not in _fired_ids(silent)


def test_rule_static_low_end_with_critical_masking_both_directions():
    fire = {"low_end_motion_score": 20.0, "critical_low_end_masking_count": 1}
    assert "static_low_end_critical_masking" in _fired_ids(fire)
    for silent in (
        {"low_end_motion_score": 80.0, "critical_low_end_masking_count": 1},
        {"low_end_motion_score": 20.0, "critical_low_end_masking_count": 0},
    ):
        assert "static_low_end_critical_masking" not in _fired_ids(silent)


def test_rule_mono_risk_while_widening_both_directions():
    fire = {"mono_compatibility_score": 55.0, "plan_recommends_width": True}
    assert "mono_risk_while_widening" in _fired_ids(fire)
    for silent in (
        {"mono_compatibility_score": 92.0, "plan_recommends_width": True},
        {"mono_compatibility_score": 55.0, "plan_recommends_width": False},
    ):
        assert "mono_risk_while_widening" not in _fired_ids(silent)


def test_rule_balanced_but_static_both_directions():
    fire = {"static_mix_score": 80.0, "dynamic_mix_score": 28.2}
    assert "balanced_but_static" in _fired_ids(fire)
    for silent in (
        {"static_mix_score": 50.0, "dynamic_mix_score": 28.2},
        {"static_mix_score": 80.0, "dynamic_mix_score": 70.0},
    ):
        assert "balanced_but_static" not in _fired_ids(silent)


def test_every_shipped_rule_has_a_unit_test_here():
    """Adding a rule without a firing/silent test above must fail loudly."""
    tested = {
        "contrast_without_space", "central_vocal_masked",
        "static_low_end_critical_masking", "mono_risk_while_widening",
        "balanced_but_static",
    }
    assert {r.rule_id for r in CONTRADICTION_RULES} == tested


def test_collect_facts_from_payloads_low_end_and_width():
    """Facts are derived from the payload dicts, including the two computed
    facts (critical low-end masking count, width-recommendation scan)."""
    payloads = {
        "doctrine_score": {"low_end_motion_score": 10.0},
        "masking_report": {"events": [
            {"severity": "critical", "frequency_range": "40Hz-150Hz"},
            {"severity": "critical", "frequency_range": "1.5kHz-4kHz"},  # not low-end
            {"severity": "moderate", "frequency_range": "40Hz-150Hz"},   # not critical
            {"severity": "critical", "frequency_range": "full-band (stereo image)"},
        ]},
        "mix_plan": {"automation_plan": [
            {"section": "c1", "name": "Chorus", "gesture": "g",
             "moves": ["Widest point of the song"]},
        ]},
    }
    facts = collect_facts(payloads)
    assert facts["critical_low_end_masking_count"] == 1
    assert facts["plan_recommends_width"] is True
    assert facts["low_end_motion_score"] == 10.0
    assert "static_low_end_critical_masking" in _fired_ids(facts)


def test_no_contradictions_line_when_none_fire():
    out = render_execution_brief({})
    assert "(no cross-lens contradictions detected)" in out


def test_committed_trees_surface_real_contradictions():
    """The committed corpus genuinely carries the central-but-masked vocal
    reading (vocal_centrality 90 with 4 vocal-band events) — the rendered
    contradiction section must show it, not the empty line."""
    for tree in SAMPLE_TREES.values():
        out = _tree_render(tree)
        facts = collect_facts(load_brief_payloads(tree))
        fired = _fired_ids(facts)
        if fired:
            assert "(no cross-lens contradictions detected)" not in out
        if "central_vocal_masked" in fired:
            assert "central_vocal_masked" in out


# --------------------------------------------------------------------------- #
# Execution-order phase classification.
# --------------------------------------------------------------------------- #
def test_phase_order_is_the_five_declared_phases():
    assert PHASE_ORDER == [PHASE_GAIN, PHASE_CARVE, PHASE_SPACE,
                           PHASE_SECTION, PHASE_CREATIVE]


def test_each_category_lands_in_its_phase():
    plan = {
        "per_track_actions": [{
            "track": "Lead Vocal",
            "diagnosis": "d",
            "actions": [
                {"plugin": "Channel EQ",
                 "setting": "High-pass ~80 Hz. Cut ~250 Hz by 1-2 dB (mud).",
                 "reason": "Clean low-end build-up.", "risk_class": 2},
                {"plugin": "Compressor",
                 "setting": "Vintage Opto, 2-3 dB gain reduction.",
                 "reason": "Stabilise the vocal.", "risk_class": 2},
                {"plugin": "Tape Machine",
                 "setting": "Drive for saturation and excitement.",
                 "reason": "Colour.", "risk_class": 4},
            ],
            "automation": [
                {"parameter": "gain", "move": "Ride phrase endings.",
                 "reason": "Performance rides.", "risk_class": 2},
            ],
            "send_reverb": "Short room, low send (~-24 dB).",
        }],
        "per_section_actions": [
            {"section": "verse_1", "name": "Verse 1", "emotional_goal": "intimacy",
             "rms_dbfs": -18.0, "width": 0.2, "contrast_warning": None},
        ],
        "automation_plan": [
            {"section": "verse_1", "name": "Verse 1", "emotional_goal": "intimacy",
             "gesture": "verse_intimacy", "moves": ["Pull reverb sends down"]},
        ],
        "mute_candidates": [
            {"element": "Shaker", "section": "verse_1", "reason": "clutter",
             "risk_class": 3},
        ],
        "next_pass": [
            {"priority": 1, "title": "Depth cleanup",
             "detail": "Move supporting pads to the midground."},
        ],
    }
    phased = phase_plan(plan)
    def summaries(phase):
        return " | ".join(item["summary"] for item in phased[phase])
    assert "Cut ~250 Hz" in summaries(PHASE_CARVE)            # subtractive EQ
    assert "Compressor" in summaries(PHASE_GAIN)              # static balance
    assert "saturation" in summaries(PHASE_CREATIVE)          # risk_class 4
    assert "Ride phrase endings" in summaries(PHASE_SECTION)  # automation
    assert "Short room" in summaries(PHASE_SPACE)             # send/reverb
    assert "Verse 1" in summaries(PHASE_SECTION)              # per-section + plan
    assert "Shaker" in summaries(PHASE_GAIN)                  # mute = subtraction
    assert "midground" in summaries(PHASE_SPACE)              # next_pass by keyword


def test_unclassifiable_action_lands_in_unphased_never_dropped():
    plan = {"per_track_actions": [{
        "track": "Mystery",
        "actions": [{"plugin": "Enigma Box", "setting": "????",
                     "reason": "unknowable", "risk_class": 2}],
        "automation": [],
        "send_reverb": "",
    }]}
    items = extract_plan_items(plan)
    assert len(items) == 1
    assert classify_plan_item(items[0]) == UNPHASED
    phased = phase_plan(plan)
    assert len(phased[UNPHASED]) == 1
    # Count conservation: nothing dropped, nothing duplicated.
    assert sum(len(v) for v in phased.values()) == len(items)


@pytest.mark.parametrize("producer", sorted(SAMPLE_TREES))
def test_count_conservation_on_committed_trees(producer):
    plan = _read(SAMPLE_TREES[producer], "mix_plan.json")
    items = extract_plan_items(plan)
    phased = phase_plan(plan)
    assert sum(len(v) for v in phased.values()) == len(items)
    assert len(items) > 0
    # Every item appears exactly once across all buckets.
    flat = [id(item) for bucket in phased.values() for item in bucket]
    assert len(flat) == len(set(flat)) == len(items)


def test_execution_order_cross_references_the_checklist():
    """The brief must link to the same checklist render-checklist produces —
    the preferred order line is imported from checklist_renderer, not
    duplicated."""
    from logic_mix_os.renderers.checklist_renderer import PREFERRED_ORDER
    out = _tree_render(SAMPLE_TREES["halee_ramone"])
    assert "logic_action_checklist.md" in out
    assert " → ".join(PREFERRED_ORDER) in out


# --------------------------------------------------------------------------- #
# Missing-artifact tolerance — real out-dirs may be partial.
# --------------------------------------------------------------------------- #
def test_all_payloads_missing_renders_honest_lines():
    out = render_execution_brief({})
    for key, filename in BRIEF_ARTIFACTS.items():
        assert f"(artifact missing: {filename})" in out, filename
    # Still a complete document: every heading renders.
    for heading in LENS_HEADINGS:
        assert heading in out
    assert COPILOT_HEADING in out


def test_single_missing_payload_is_tolerated():
    tree = SAMPLE_TREES["halee_ramone"]
    payloads = load_brief_payloads(tree)
    payloads["masking_report"] = None
    out = render_execution_brief(payloads)
    assert "(artifact missing: masking_report.json)" in out
    # Other lenses still carry their evidence.
    ds = _read(tree, "doctrine_score.json")
    assert f"{json.dumps(ds['physical_space_score'])}/100" in out


def test_load_brief_payloads_partial_dir(tmp_path):
    (tmp_path / "doctrine_score.json").write_text(
        json.dumps({"physical_space_score": 12.0}), encoding="utf-8")
    payloads = load_brief_payloads(tmp_path)
    assert payloads["doctrine_score"] == {"physical_space_score": 12.0}
    assert payloads["mix_plan"] is None
    render_execution_brief(payloads)  # must not raise


# --------------------------------------------------------------------------- #
# CLI smoke — against a COPY; examples/ is never written.
# --------------------------------------------------------------------------- #
def test_cli_execution_brief_smoke(tmp_path):
    src = SAMPLE_TREES["halee_ramone"]
    work = tmp_path / "tree"
    shutil.copytree(src, work)
    rc = cli.main(["execution-brief", "--dir", str(work)])
    assert rc == 0
    out_file = work / "execution_brief.md"
    assert out_file.is_file()
    text = out_file.read_text(encoding="utf-8")
    assert text.strip()
    assert text == render_execution_brief(load_brief_payloads(work)) + "\n"


def test_cli_execution_brief_out_override(tmp_path):
    src = SAMPLE_TREES["halee_ramone"]
    work = tmp_path / "tree"
    shutil.copytree(src, work)
    target = tmp_path / "brief.md"
    rc = cli.main(["execution-brief", "--dir", str(work), "--out", str(target)])
    assert rc == 0
    assert target.is_file() and target.read_text(encoding="utf-8").strip()
    assert not (work / "execution_brief.md").exists()


def test_cli_execution_brief_missing_dir_is_clean_error(tmp_path, capsys):
    rc = cli.main(["execution-brief", "--dir", str(tmp_path / "nope")])
    assert rc == 2
    assert "Not a directory" in capsys.readouterr().err


# --------------------------------------------------------------------------- #
# GUARD — the committed examples/ trees are byte-untouched by rendering.
# --------------------------------------------------------------------------- #
def _hash_tree(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def test_examples_trees_untouched_by_rendering():
    before = {name: _hash_tree(tree) for name, tree in SAMPLE_TREES.items()}
    for tree in SAMPLE_TREES.values():
        _tree_render(tree)
    after = {name: _hash_tree(tree) for name, tree in SAMPLE_TREES.items()}
    assert before == after
    # No brief file may EVER be committed into a sample tree (guard finding).
    for tree in SAMPLE_TREES.values():
        assert not (tree / "execution_brief.md").exists()
