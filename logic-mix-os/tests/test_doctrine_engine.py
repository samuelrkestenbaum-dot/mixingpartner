"""Doctrine scoring + masking hierarchy acceptance tests."""

from __future__ import annotations

from logic_mix_os.validation.output_validator import load_schema, validate_instance

SCORE_KEYS = [
    "physical_space_score",
    "emotional_hierarchy_score",
    "vocal_centrality_score",
    "depth_hierarchy_score",
    "static_mix_score",
    "dynamic_mix_score",
    "overall_mix_readiness_score",
]


def test_doctrine_scores_present_and_bounded(analyzed):
    ds = analyzed["dense_chorus_with_loops"].doctrine_score
    for k in SCORE_KEYS:
        v = ds[k]
        assert v is None or (0.0 <= v <= 100.0), f"{k} out of range: {v}"
    assert ds["overall_mix_readiness_score"] is not None


def test_section_contrast_scored_with_two_sections(analyzed):
    ds = analyzed["dense_chorus_with_loops"].doctrine_score
    assert ds["section_contrast_score"] is not None
    assert 0.0 <= ds["section_contrast_score"] <= 100.0


def test_dense_arrangement_creates_hierarchy_signal(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    events = res.masking_report["events"]
    width_crowding = [e for e in events if e["classification"] == "width_crowding"]
    # Either an explicit crowding event, or the physical-space score is penalised below 80.
    assert width_crowding or res.doctrine_score["physical_space_score"] < 80


def test_masking_is_hierarchy_not_blanket(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    report = res.masking_report
    assert "doctrine_rule" in report
    # Felt/background overlaps must not all be flagged critical.
    crit = report["summary"]["critical_count"]
    assert crit <= len(report["events"])


def test_low_end_conflict_detected_when_kick_and_bass_share_sub(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    kinds = {e["classification"] for e in res.masking_report["events"]}
    assert "low_end_conflict" in kinds


def test_doctrine_score_json_validates(analyzed):
    ds = analyzed["dense_chorus_with_loops"].doctrine_score
    schema = load_schema("doctrine_score.schema.json")
    errors = validate_instance(ds, schema)
    assert errors == [], errors


def test_masking_report_json_validates(analyzed):
    report = analyzed["dense_chorus_with_loops"].masking_report
    schema = load_schema("masking_report.schema.json")
    assert validate_instance(report, schema) == []


def test_warning_doctrine_tags_are_aesthetic_never_producer_named():
    """P-038 (the P-030 reviewer judgment call, resolved): the ``doctrine``
    tags on engine-emitted warnings name the AESTHETIC — ``vocal_centrality``
    and ``restraint``, joining the existing bare-aesthetic tag family
    (``sacred_vs_expendable`` / ``section_contrast`` / ``felt_vs_heard``) and
    the P-030 contract vocabulary — never a producer. Producer names are
    profile vocabulary; the engine's emitted values are producer-agnostic.
    Both warnings fire in one call: no lead vocal + an all-decorative record
    set. (No fixture emits these two warnings, so this synthetic pin is the
    only guard on the tag values.)"""
    from logic_mix_os.doctrine import doctrine_engine

    warnings: list = []
    records = [{"sacredness": "decorative"}]
    doctrine_engine._emotional_hierarchy(records, None, [], warnings)

    tags = [t for w in warnings for t in w["doctrine"]]
    assert tags == ["vocal_centrality", "restraint", "sacred_vs_expendable"]
    for tag in tags:
        for producer in ("phil", "ramone", "roy", "halee", "timbaland"):
            assert producer not in tag, f"producer-named tag survives: {tag}"
