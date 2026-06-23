"""Source-aware auditor tests (build packet 19, 20, 21)."""

from __future__ import annotations


def _audit_for(result, track_name):
    return next(a for a in result.source_audits["audits"] if a["track"] == track_name)


def test_every_track_audited(analyzed):
    for res in analyzed.values():
        assert len(res.source_audits["audits"]) == len(res.records)
        for a in res.source_audits["audits"]:
            assert a["auditor_type"] in {"live_track", "synth_patch", "sample_loop", "generic"}
            assert a["recommendations"]


def test_live_vocal_gets_performance_repair_language(analyzed):
    a = _audit_for(analyzed["simple_vocal_piano_song"], "Lead Vocal")
    assert a["auditor_type"] == "live_track"
    assert "clip gain before compression" in a["preferred_moves"]


def test_synth_pad_audited_as_synth_patch(analyzed):
    a = _audit_for(analyzed["dense_chorus_with_loops"], "Synth Pad")
    assert a["auditor_type"] == "synth_patch"
    assert any("filter" in r.lower() or "width" in r.lower() or "high-pass" in r.lower()
               for r in a["recommendations"])


def test_splice_loop_audited_with_red_flags(analyzed):
    a = _audit_for(analyzed["splice_loop_problem"], "Splice Loop")
    assert a["auditor_type"] == "sample_loop"
    assert a["red_flags"], "a full-width mastered loop should raise red flags"
    assert any("full-width" in f for f in a["red_flags"])
    assert any("finished record" in r for r in a["recommendations"])


def test_synth_bounce_flagged_for_rerender(analyzed):
    a = _audit_for(analyzed["dense_chorus_with_loops"], "Synth Pad")
    assert any("re-render" in r.lower() or "re-rendering" in r.lower() for r in a["recommendations"])


# --- live auditor is now branched by instrument family --------------------- #
_PHRASE_RIDE_MARKERS = ["phrase ride", "phrase-level ride", "phrase rides", "phrase energy"]


def _all_text(a):
    return " ".join(a["recommendations"] + a["preferred_moves"]).lower()


def test_drums_do_not_get_vocal_phrase_ride_advice(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    for name in ["Kick", "Snare"]:
        a = _audit_for(res, name)
        assert a["identity_family"] == "drums"
        text = _all_text(a)
        assert not any(m in text for m in _PHRASE_RIDE_MARKERS), f"{name} got vocal phrase-ride advice: {text}"
        # and it DOES get drum-appropriate guidance
        assert any(k in text for k in ["transient", "phase", "overhead", "room", "punch", "ring", "beater", "sub"])


def test_vocal_still_gets_phrase_rides(analyzed):
    a = _audit_for(analyzed["simple_vocal_piano_song"], "Lead Vocal")
    text = _all_text(a)
    assert "phrase" in text and ("ride" in text or "clip gain" in text)


def test_bass_gets_low_end_not_phrase_advice(analyzed):
    a = _audit_for(analyzed["dense_chorus_with_loops"], "Bass")
    assert a["identity_family"] == "bass"
    text = _all_text(a)
    assert any(k in text for k in ["sustain", "kick", "low-end", "low end", "note definition"])
    assert not any(m in text for m in _PHRASE_RIDE_MARKERS)


def test_guitars_get_source_tone_not_phrase_energy(analyzed):
    a = _audit_for(analyzed["dense_chorus_with_loops"], "Electric Guitar 1")
    assert a["identity_family"] == "guitars"
    text = _all_text(a)
    assert "phrase energy" not in text
    assert any(k in text for k in ["source tone", "pick", "strum", "leveling", "depth"])


def test_no_universal_preserve_human_feel_line(analyzed):
    # The old generic line appeared verbatim on every live track; it should be gone.
    for res in analyzed.values():
        for a in res.source_audits["audits"]:
            assert "preserve the human feel; integrate with shared room/depth rather than flattening dynamics" \
                not in " ".join(a["recommendations"]).lower()
