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


def _detect(loaded_by_id, duration, sr=SR):
    mix = _mixdown(list(loaded_by_id.values()), duration, sr)
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
        # P-061: the merge is exercised by a short section between two REAL
        # arrangement events, not by a sub-persistence blip. Two staggered
        # entrances 4s apart (both stems then play to the end, so both are well
        # past the persistence floor and neither is debounced away) carve a 4s
        # middle section, which is < MIN_SECTION_SEC and must merge leftward.
        duration = 40.0
        loaded = {
            "t0_pad": _stem([(0, duration)], duration, seed=0),
            "t1_early": _stem([(8, duration)], duration, seed=1),
            "t2_late": _stem([(12, duration)], duration, seed=2),
        }
        sections = _detect(loaded, duration)
        lengths = [s.end - s.start for s in sections]
        assert lengths, sections
        assert min(lengths) >= MIN_SECTION_SEC - 1e-6, lengths
        # NON-VACUITY: three raw boundaries (0 / 8 / 12) collapse to exactly two
        # sections. Without the merge this would be 3; a wholesale collapse
        # would be 1. Only a real single merge yields 2.
        assert len(sections) == 2, [(s.start, s.end) for s in sections]
        assert [s.start for s in sections] == [0.0, 12.0], sections

    def test_max_sections_cap(self):
        # P-061: RE-SPACED so the cap is genuinely the binding guardrail. The
        # old spacing (13 entrances 6s apart) is below the raised
        # MIN_SECTION_SEC, so the merge would consume the boundaries BEFORE
        # _cap_sections ever ran and the test would pass vacuously.
        duration = 160.0
        # 15 staircase entrances 10s apart -> 16 boundaries with t=0. Every
        # section is 10s > MIN_SECTION_SEC, so the merge is a no-op and the cap
        # alone does the work.
        loaded = {"t00_pad": _stem([(0, duration)], duration, sr=8000, seed=99)}
        for i in range(15):
            loaded[f"t{i + 1:02d}"] = _stem(
                [(10 * (i + 1), duration)], duration, sr=8000, seed=i
            )
        sections = _detect(loaded, duration, sr=8000)
        # NON-VACUITY: an EXACT count, not an inequality. 16 boundaries survive
        # the merge, so a neutered _cap_sections yields 16 and fails here; only
        # a firing cap yields exactly MAX_SECTIONS.
        assert len(sections) == MAX_SECTIONS, len(sections)


class TestOverSegmentationCalibration:
    """P-061 — the detector must not shred a song into ornament-sized pieces.

    A ~200s arrangement whose only sub-sectional material is a set of 3-4s
    guitar stabs and percussion fills. Under the P-059 constants this produced
    **12 sections** — hitting MAX_SECTIONS — with 4.00s / 4.00s / 7.00s
    micro-sections carved out purely by those stabs, and (because the cap then
    had to drop boundaries) a single 64s super-block from 104s to 168s: the
    middle shredded while the tail was under-segmented. That per-section
    rms/width/crest spread is exactly what pinned the doctrine engine's
    ``_dynamic_mix`` and ``_section_contrast`` at a fake 100/100.

    The honest reading of this arrangement is the 9 blocks bounded by the real
    entrances/exits; the stabs and fills are ORNAMENTS inside them.
    """

    DURATION = 200.0
    SR = 8000

    # The real arrangement events — and the ONLY legitimate boundaries.
    TRUE_STARTS = [0.0, 16.0, 32.0, 72.0, 88.0, 120.0, 136.0, 168.0, 184.0]
    # Ornament centres: 3-4s stabs/fills that must NOT create a boundary.
    ORNAMENTS = [40.0, 44.0, 56.0, 60.0, 92.0, 95.0, 104.0, 108.0, 150.0, 153.0,
                 160.0, 163.0]

    def _song(self):
        d = self.DURATION
        s = self.SR
        return {
            "a_pad": _stem([(0, 200)], d, sr=s, seed=1),
            "b_drums": _stem([(16, 72), (88, 168), (184, 200)], d, sr=s, seed=2),
            "c_bass": _stem([(16, 200)], d, sr=s, seed=3),
            "d_vox": _stem([(32, 72), (88, 120), (136, 168)], d, sr=s, seed=4),
            # 3-4s ornaments — the over-segmentation trigger.
            "e_gtr": _stem([(56, 60), (104, 108), (150, 153)], d, sr=s, seed=5),
            "f_perc": _stem([(40, 44), (92, 95), (160, 163)], d, sr=s, seed=6),
        }

    def test_no_micro_sections(self):
        sections = _detect(self._song(), self.DURATION, sr=self.SR)
        lengths = [s.end - s.start for s in sections]
        assert min(lengths) >= MIN_SECTION_SEC - 1e-6, lengths
        # the specific regression: the old 4.00s / 4.00s / 7.00s slivers.
        assert all(length >= 8.0 for length in lengths), lengths

    def test_ornaments_create_no_boundary(self):
        """The heart of it: a 3-4s stab is not an arrangement event."""
        sections = _detect(self._song(), self.DURATION, sr=self.SR)
        starts = [s.start for s in sections]
        for orn in self.ORNAMENTS:
            assert all(abs(st - orn) > 1.0 for st in starts), (orn, starts)

    def test_boundaries_are_the_real_arrangement_events(self):
        sections = _detect(self._song(), self.DURATION, sr=self.SR)
        starts = [s.start for s in sections]
        assert len(sections) == len(self.TRUE_STARTS), starts
        for got, want in zip(starts, self.TRUE_STARTS):
            assert abs(got - want) <= 0.5, (starts, self.TRUE_STARTS)

    def test_section_count_is_materially_lower_and_not_cap_clipped(self):
        sections = _detect(self._song(), self.DURATION, sr=self.SR)
        # was 12 (= MAX_SECTIONS) under the P-059 constants.
        assert len(sections) == 9, len(sections)
        # Structure is arrangement-driven, NOT cap-clipped: the cap never binds,
        # so no boundary was dropped for being "low novelty".
        assert len(sections) < MAX_SECTIONS, len(sections)

    def test_no_cap_induced_super_block(self):
        """The tail must not collapse into one giant block."""
        sections = _detect(self._song(), self.DURATION, sr=self.SR)
        lengths = [s.end - s.start for s in sections]
        # the old bug produced a single 64s block spanning 104s -> 168s while
        # the middle was shredded. The longest HONEST block here is 32s->72s.
        assert max(lengths) <= 40.0 + 1e-6, lengths
        for s in sections:
            assert not (s.start <= 104.0 and s.end >= 168.0), (s.start, s.end)

    def test_calibration_is_deterministic(self):
        a = _detect(self._song(), self.DURATION, sr=self.SR)
        b = _detect(self._song(), self.DURATION, sr=self.SR)
        assert [(s.start, s.end, s.energy_tag) for s in a] == \
               [(s.start, s.end, s.energy_tag) for s in b]


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
