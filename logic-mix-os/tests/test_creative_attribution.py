"""Variant attribution tests (packet P-001).

Every variant emitted by the creative engine must attribute its moves to
*real* tracks: ``tracks_affected`` has to be non-empty and a subset of the
track names actually present in ``result.records``. No hard-coded literal
(e.g. ``"Drum Overheads"`` / ``"Drum Room"``) may leak through for a project
that does not contain such a track.
"""

from __future__ import annotations

import pytest

from logic_mix_os.creative import run_creative_engine

FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


@pytest.mark.parametrize("fixture", FIXTURE_NAMES)
def test_variants_only_reference_real_tracks(analyzed, fixture):
    result = analyzed[fixture]
    real_names = {r["name"] for r in result.records}
    assert real_names, f"{fixture} produced no records"

    creative = run_creative_engine(result, result.creative["search_mode"])
    seen_a_variant = False
    for branch in creative["branches"]:
        for variant in branch["variants"]:
            seen_a_variant = True
            tracks = variant["tracks_affected"]
            assert tracks, (
                f"{fixture}/{variant['variant_id']} has empty tracks_affected"
            )
            phantom = [t for t in tracks if t not in real_names]
            assert not phantom, (
                f"{fixture}/{variant['variant_id']} references tracks "
                f"absent from result.records: {phantom} "
                f"(real tracks: {sorted(real_names)})"
            )
    assert seen_a_variant, f"{fixture} surfaced no creative variants"
