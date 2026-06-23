"""Doctrine-protection + golden-output regression tests (build packet 51)."""

from __future__ import annotations

import pytest

from logic_mix_os.regression import (
    build_snapshot,
    doctrine_invariants,
    run_regression_suite,
)

FIXTURES = ["simple_vocal_piano_song", "dense_chorus_with_loops", "splice_loop_problem"]


@pytest.mark.parametrize("fixture", FIXTURES)
def test_doctrine_invariants_hold(analyzed, fixture):
    result = analyzed[fixture]
    failures = [
        f"{inv['name']}: {inv['detail']}"
        for inv in doctrine_invariants(result)
        if inv["applicable"] and inv["critical"] and not inv["ok"]
    ]
    assert not failures, f"{fixture} violated doctrine invariants: {failures}"


def test_regression_suite_passes(fixtures_dir):
    report = run_regression_suite(fixtures_dir)
    assert report["tests_run"] > 0
    assert report["critical_failures"] == [], report["critical_failures"]


def test_golden_snapshots_present_and_match(fixtures_dir, analyzed):
    import json

    for fixture in FIXTURES:
        golden_path = fixtures_dir / fixture / "golden" / "snapshot.json"
        assert golden_path.exists(), f"missing golden snapshot for {fixture}"
        golden = json.loads(golden_path.read_text())
        current = build_snapshot(analyzed[fixture])
        # categorical track fingerprint must match exactly
        assert {t["name"]: t["instrument_identity"] for t in golden["tracks"]} == \
               {t["name"]: t["instrument_identity"] for t in current["tracks"]}
        assert {t["name"]: t["default_depth"] for t in golden["tracks"]} == \
               {t["name"]: t["default_depth"] for t in current["tracks"]}


def test_specific_doctrine_protections(analyzed):
    # The Splice loop must never be foregrounded by default.
    splice = analyzed["splice_loop_problem"]
    loop = next(r for r in splice.records if "loop" in r["instrument_identity"] or r["source_kind"] == "splice_sample")
    assert loop["depth_default"] in {"midground", "background"}

    # The dense arrangement must surface a hierarchy/crowding signal.
    dense = analyzed["dense_chorus_with_loops"]
    has_crowding = any(e["classification"] == "width_crowding" for e in dense.masking_report["events"])
    assert has_crowding or dense.doctrine_score["halee_score"] < 80
