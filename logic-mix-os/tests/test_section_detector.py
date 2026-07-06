"""P-059 — Audio-driven section detection proof suite.

Two things are proved here:

1. **The detector infers arrangement sections from what enters/exits.** A
   synthetic multi-section arrangement (drums enter, bass enters, a pad plays
   THROUGHOUT, vocal enters, drums exit at a drop) yields boundaries at exactly
   those events and nowhere spurious; the always-on pad contributes zero
   boundaries; the guardrails (sub-min merge, max-section cap) hold; and the
   run is deterministic.

2. **The byte-stability guard holds.** ``pipeline.analyze`` enters the detector
   ONLY when the manifest supplies fewer than two sections. A >=2-section
   manifest never calls ``detect_sections`` and its section-analysis carries no
   ``inferred`` / ``energy_tag`` keys — so every pinned corpus stays
   byte-identical (the golden / differential / sample-refresh suites confirm the
   rest).
"""

from __future__ import annotations

import copy
from unittest import mock

import numpy as np
import pytest

from conftest import ROOT

from logic_mix_os.analyzers.audio_loader import LoadedAudio
from logic_mix_os.analyzers.section_detector import (
    MAX_SECTIONS,
    MIN_SECTION_SEC,
    detect_sections,
)
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest

SR = 16000


def _stem(events, duration, sr=SR, amp=0.1, seed=0):
    """A mono stem: white noise at ``amp`` inside each ``(start, end)`` window,
    silence elsewhere. Deterministic (seeded)."""
    n = int(duration * sr)
    rng = np.random.default_rng(seed)
    x = np.zeros(n, dtype=np.float64)
    for start, end in events:
        a = int(start * sr)
        b = min(n, int(end * sr))
        x[a:b] = rng.standard_normal(b - a) * amp
    return LoadedAudio(samples=x, sample_rate=sr, path=None)


def _mixdown(stems, duration, sr=SR):
    n = int(duration * sr)
    acc = np.zeros(n, dtype=np.float64)
    for s in stems:
        m = np.asarray(s.samples, dtype=np.float64)
        acc[: m.size] += m[:n]
    return LoadedAudio(samples=np.column_stack([acc, acc]), sample_rate=sr, path=None)


def _detect(loaded_by_id, duration):
    mix = _mixdown(list(loaded_by_id.values()), duration)
    return detect_sections(loaded_by_id, mix, duration)


class TestArrangementDetection:
    """The headline: sections come from arrangement events, not energy dips."""

    DURATION = 40.0

    def _arrangement(self):
        # pad plays THROUGHOUT -> never toggles -> contributes NO boundary.
        # drums enter @8 and EXIT @32 (the drop); bass @16; vocal @24.
        return {
            "t2_bass": _stem([(16, self.DURATION)], self.DURATION, seed=2),
            "t1_drums": _stem([(8, 32)], self.DURATION, seed=1),
            "t0_pad": _stem([(0, self.DURATION)], self.DURATION, seed=0),
            "t3_vocal": _stem([(24, self.DURATION)], self.DURATION, seed=3),
        }

    def test_boundaries_at_arrangement_events_only(self):
        sections = _detect(self._arrangement(), self.DURATION)
        starts = [s.start for s in sections]

        # Five sections: 0 | drums-in | bass-in | vocal-in | drums-out.
        assert len(sections) == 5, starts
        expected = [0.0, 8.0, 16.0, 24.0, 32.0]
        for got, want in zip(starts, expected):
            assert abs(got - want) <= 0.3, (starts, expected)

        # No spurious boundary anywhere else (e.g. mid-section energy wobble).
        for spurious in (4.0, 12.0, 20.0, 28.0, 36.0):
            assert all(abs(s - spurious) > 0.5 for s in starts), (spurious, starts)

    def test_always_on_pad_adds_no_boundary(self):
        # Pad alone -> a single whole-song section (its constant presence is not
        # an arrangement event).
        only_pad = {"t0_pad": _stem([(0, self.DURATION)], self.DURATION, seed=0)}
        sections = _detect(only_pad, self.DURATION)
        assert len(sections) == 1
        assert sections[0].start == 0.0

    def test_energy_tags_are_relative_and_honest(self):
        sections = _detect(self._arrangement(), self.DURATION)
        tags = [s.energy_tag for s in sections]
        assert all(t in {"high", "med", "low"} for t in tags)
        # sparsest section (pad only) reads low; densest (all four) reads high.
        assert tags[0] == "low"
        assert tags[3] == "high"
        # honest structural labels — never semantic naming.
        assert [s.name for s in sections] == [f"Section {i}" for i in range(1, 6)]
        assert all(s.inferred is True for s in sections)
        assert all(s.emotional_goal is None for s in sections)

    def test_deterministic(self):
        a = _detect(self._arrangement(), self.DURATION)
        b = _detect(self._arrangement(), self.DURATION)
        assert [(s.section_id, s.start, s.end, s.energy_tag, s.inferred) for s in a] == \
               [(s.section_id, s.start, s.end, s.energy_tag, s.inferred) for s in b]


class TestGuardrails:
    def test_sub_min_section_is_merged(self):
        duration = 20.0
        loaded = {
            "t0_pad": _stem([(0, duration)], duration, seed=0),
            # a 3s blip (< MIN_SECTION_SEC) between two long stretches.
            "t1_blip": _stem([(8, 11)], duration, seed=1),
        }
        sections = _detect(loaded, duration)
        lengths = [s.end - s.start for s in sections]
        assert lengths, sections
        assert min(lengths) >= MIN_SECTION_SEC - 1e-6, lengths

    def test_max_sections_cap(self):
        duration = 84.0
        # 13 staircase entrances (6s apart) -> 14 boundaries with t=0, over the
        # MAX_SECTIONS cap; each section is >= 6s so nothing is merged first.
        loaded = {"t00_pad": _stem([(0, duration)], duration, sr=8000, seed=99)}
        for i in range(13):
            loaded[f"t{i + 1:02d}"] = _stem(
                [(6 * (i + 1), duration)], duration, sr=8000, seed=i
            )
        sections = _detect(loaded, duration)
        assert len(sections) <= MAX_SECTIONS, len(sections)


class TestPipelineByteStability:
    """The guard that protects every pinned output: supplied >=2 sections never
    enter the detector; <=1 section does."""

    FIXTURE = "simple_vocal_piano_song"

    def _paths(self):
        base = ROOT / "fixtures" / self.FIXTURE
        return str(base / "stems"), load_manifest(base / "project_manifest.json")

    def test_supplied_sections_do_not_enter_detector(self, _ensure_fixtures):
        stems, manifest = self._paths()
        assert len(manifest["sections"]) >= 2
        with mock.patch(
            "logic_mix_os.pipeline.detect_sections",
            side_effect=AssertionError("detector must not run for supplied sections"),
        ) as spy:
            result = analyze(stems, manifest)
        spy.assert_not_called()
        assert result.section_analysis
        for entry in result.section_analysis:
            assert "inferred" not in entry
            assert "energy_tag" not in entry

    def test_single_section_manifest_enters_detector(self, _ensure_fixtures):
        stems, manifest = self._paths()
        one = copy.deepcopy(manifest)
        one["sections"] = manifest["sections"][:1]  # header-only style: 1 section

        with mock.patch(
            "logic_mix_os.pipeline.detect_sections",
            wraps=__import__(
                "logic_mix_os.analyzers.section_detector",
                fromlist=["detect_sections"],
            ).detect_sections,
        ) as spy:
            result = analyze(stems, one)
        spy.assert_called_once()
        assert result.section_analysis
        for entry in result.section_analysis:
            assert entry["inferred"] is True
            assert entry["energy_tag"] in {"high", "med", "low"}

    def test_zero_section_manifest_enters_detector(self, _ensure_fixtures):
        stems, manifest = self._paths()
        none = copy.deepcopy(manifest)
        none["sections"] = []
        result = analyze(stems, none)
        assert result.section_analysis  # detector always yields >= 1 section
        for entry in result.section_analysis:
            assert entry["inferred"] is True
            assert entry["energy_tag"] in {"high", "med", "low"}


class TestSuppliedSectionShapeUnchanged:
    def test_analyzed_supplied_section_has_no_detector_keys(self, _ensure_fixtures):
        base = ROOT / "fixtures" / "simple_vocal_piano_song"
        result = analyze(str(base / "stems"), load_manifest(base / "project_manifest.json"))
        # the exact key set a supplied section analysis has always carried.
        for entry in result.section_analysis:
            assert set(entry) == {
                "section_id", "name", "start_time", "end_time",
                "emotional_goal", "metrics", "contrast_vs_previous",
            }
