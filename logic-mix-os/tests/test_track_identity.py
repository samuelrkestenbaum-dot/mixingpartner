"""Identity, source-material, felt/heard, and depth acceptance tests."""

from __future__ import annotations

from logic_mix_os.constants import DEPTH_LAYERS


def _by_name(items):
    return {x["name"]: x for x in items}


def test_lead_vocal_detected_as_vocal(analyzed):
    res = analyzed["simple_vocal_piano_song"]
    ident = _by_name(res.track_identity)["Lead Vocal"]
    assert ident["identity_family"] == "vocal"
    assert ident["instrument_identity"] in {"lead_vocal", "backing_vocal"}
    assert 0.0 <= ident["confidence"] <= 1.0


def test_piano_detected_as_keys(analyzed):
    res = analyzed["simple_vocal_piano_song"]
    ident = _by_name(res.track_identity)["Piano"]
    assert ident["identity_family"] == "keys"
    assert ident["instrument_identity"] in {"piano", "electric_piano", "organ"}


def test_splice_loop_detected_as_loop_or_texture(analyzed):
    res = analyzed["splice_loop_problem"]
    ident = _by_name(res.track_identity)["Splice Loop"]
    source = _by_name(res.source_material)["Splice Loop"]
    assert (
        ident["identity_family"] in {"loop", "texture"}
        or source["source_kind"] in {"splice_sample", "imported_sample_loop", "texture_loop", "apple_loop"}
    )


def test_full_width_loop_is_warned_against(analyzed):
    res = analyzed["splice_loop_problem"]
    source = _by_name(res.source_material)["Splice Loop"]
    assert source["warnings"], "a foregrounded full-width loop should produce warnings"
    assert any("width" in w.lower() for w in source["warnings"])


def test_every_track_has_identity_and_confidence(analyzed):
    for res in analyzed.values():
        for ident in res.track_identity:
            assert ident["instrument_identity"]
            assert ident["identity_family"]
            assert isinstance(ident["confidence"], (int, float))


def test_lead_vocal_depth_is_close(analyzed):
    res = analyzed["simple_vocal_piano_song"]
    depth = _by_name(res.depth_map)["Lead Vocal"]
    assert depth["default_depth"] in {"intimate", "foreground"}
    # across all sections the vocal stays intimate or foreground
    for layer in depth["depth_by_section"].values():
        assert layer in {"intimate", "foreground"}


def test_pads_and_textures_are_felt_or_background(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    roles = _by_name(res.roles)
    depth = _by_name(res.depth_map)
    for name in ["Synth Pad", "Splice Texture Loop"]:
        is_felt = roles[name]["perceptual_role"] in {"felt", "candidate_for_mute", "transitional"}
        is_back = depth[name]["default_depth"] in {"midground", "background"}
        assert is_felt or is_back, f"{name} should be felt or pushed back"


def test_every_track_assigned_a_depth_layer(analyzed):
    for res in analyzed.values():
        for d in res.depth_map:
            assert d["default_depth"] in DEPTH_LAYERS
