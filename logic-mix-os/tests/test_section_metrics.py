"""Layer 1 — per-section metric depth tests (Hardening Packet 1)."""

from __future__ import annotations

import numpy as np

from logic_mix_os.analyzers.audio_loader import LoadedAudio
from logic_mix_os.analyzers.section_analyzer import compute_section_track_metrics
from logic_mix_os.project import Section

SR = 32000


def test_activity_flag_marks_silent_section_inactive():
    # A stem silent in section A, playing in section B.
    silent = np.zeros(SR)
    t = np.arange(SR) / SR
    loud = 0.5 * np.sin(2 * np.pi * 100 * t)
    loaded = LoadedAudio(samples=np.concatenate([silent, loud]), sample_rate=SR, path="x")
    sections = [Section("a", "A", 0.0, 1.0, None), Section("b", "B", 1.0, 2.0, None)]
    stm = compute_section_track_metrics({"k": loaded}, sections, 2.0)
    assert stm["k"]["a"]["active"] is False
    assert stm["k"]["b"]["active"] is True


def test_section_track_metrics_differ_between_sections():
    t = np.arange(SR) / SR
    quiet = 0.05 * np.sin(2 * np.pi * 200 * t)
    bright_loud = 0.6 * np.sin(2 * np.pi * 6000 * t)
    loaded = LoadedAudio(samples=np.concatenate([quiet, bright_loud]), sample_rate=SR, path="x")
    sections = [Section("a", "A", 0.0, 1.0, None), Section("b", "B", 1.0, 2.0, None)]
    stm = compute_section_track_metrics({"k": loaded}, sections, 2.0)["k"]
    assert stm["a"]["rms_dbfs"] < stm["b"]["rms_dbfs"]
    assert stm["a"]["band_energy"] != stm["b"]["band_energy"]


def test_kick_silent_verse_has_no_low_end_conflict(analyzed):
    # The dense fixture's kick is silent in verse_1 and enters in chorus_1.
    events = analyzed["dense_chorus_with_loops"].masking_report["events"]
    low_end = [e for e in events if e["classification"] == "low_end_conflict"]
    sections_with_conflict = {e["section"] for e in low_end}
    assert "verse_1" not in sections_with_conflict, "kick is silent in the verse — no conflict should fire there"
    assert "chorus_1" in sections_with_conflict, "kick + bass do conflict in the chorus where both play"


def test_section_metrics_are_section_specific(analyzed):
    secs = {s["section_id"]: s["metrics"] for s in analyzed["dense_chorus_with_loops"].section_analysis}
    v, c = secs["verse_1"], secs["chorus_1"]
    # at least one of these section-level descriptors must actually differ
    assert any(abs(v[k] - c[k]) > 1e-6 for k in ("rms_dbfs", "width", "brightness", "density"))


def test_masking_varies_by_section(analyzed):
    events = analyzed["dense_chorus_with_loops"].masking_report["events"]
    by_section = {}
    for e in events:
        by_section.setdefault(e["section"], set()).add(e["classification"])
    # verse and chorus should not have an identical classification set
    assert by_section.get("verse_1") != by_section.get("chorus_1")


def test_whole_stem_fallback_when_no_section_metrics(analyzed):
    # Calling analyze_masking without section_metrics must still work (numpy-only path).
    from logic_mix_os.analyzers.masking_analyzer import analyze_masking
    r = analyzed["dense_chorus_with_loops"]
    report = analyze_masking(r.records, r.section_analysis)  # no section_metrics
    assert "events" in report and "summary" in report
