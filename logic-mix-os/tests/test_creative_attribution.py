"""Variant attribution tests (packet P-001).

Every variant emitted by the creative engine must attribute its moves to
*real* tracks: ``tracks_affected`` has to be non-empty and a subset of the
track names actually present in ``result.records``. No hard-coded literal
(e.g. ``"Drum Overheads"`` / ``"Drum Room"``) may leak through for a project
that does not contain such a track.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from logic_mix_os.creative import generate_variants, run_creative_engine


def _record(name, instrument_identity, identity_family, source_kind, depth_default):
    """Minimal record dict carrying exactly the keys generate_variants reads."""
    return {
        "name": name,
        "instrument_identity": instrument_identity,
        "identity_family": identity_family,
        "source_kind": source_kind,
        "depth_default": depth_default,
    }

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


def test_chorus_lift_b_non_empty_without_loops_or_supporting():
    """Site 1 (creative.py:194 chorus_lift_B): a loop-free, support-free project
    must still attribute the subtractive drop to a real record, never an empty
    list. RED on today's `loops or supporting[-1:]` (returns [])."""
    records = [
        _record("Lead Vocal", "lead_vocal", "vocal", "comped_audio_track", "intimate"),
        _record("Kick", "kick", "drums", "live_audio_recording", "foreground"),
    ]
    result = SimpleNamespace(records=records)
    real_names = {r["name"] for r in records}

    variants = generate_variants({"id": "chorus_lift"}, result)
    variant = next(v for v in variants if v["variant_id"] == "chorus_lift_B")
    tracks = variant["tracks_affected"]

    assert tracks, "chorus_lift_B emitted an empty tracks_affected"
    phantom = [t for t in tracks if t not in real_names]
    assert not phantom, (
        f"chorus_lift_B references tracks absent from result.records: {phantom} "
        f"(real tracks: {sorted(real_names)})"
    )


def test_loop_branch_prose_never_names_placeholder_when_records_exist():
    """Site 2 (creative.py:217 loop branch): when no loop record exists but real
    tracks do, prose must name a real track, never the `"the loop"` literal.
    RED on today's `loops[0] if loops else "the loop"` (prose contains it)."""
    records = [
        _record("Rhythm Guitar", "electric_guitar", "guitar", "live_audio_recording", "midground"),
    ]
    result = SimpleNamespace(records=records)
    real_names = {r["name"] for r in records}

    variants = generate_variants({"id": "loop"}, result)
    assert variants, "loop branch surfaced no variants"
    for variant in variants:
        prose = variant["creative_hypothesis"] + " " + " ".join(variant["changes"])
        assert "the loop" not in prose, (
            f"{variant['variant_id']} prose names the literal placeholder: {prose!r}"
        )
        phantom = [t for t in variant["tracks_affected"] if t not in real_names]
        assert not phantom, (
            f"{variant['variant_id']} references tracks absent from result.records: "
            f"{phantom} (real tracks: {sorted(real_names)})"
        )
