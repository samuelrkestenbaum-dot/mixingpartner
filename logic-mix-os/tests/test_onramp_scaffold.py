"""P-058 — Manifest on-ramp (scaffolder) proof suite.

Binds the D1 deliverable: a folder of exported stems becomes a VALID draft
``project_manifest.json`` that the real pipeline accepts, reusing the shipped
name->kind heuristic (one shared table, no drift). Proves, for EACH of the four
synthetic fixtures, that ``scaffold_manifest`` -> a JSON-valid draft -> the full
``load_manifest`` + ``Project.from_inputs`` + ``analyze()`` path succeeds; that
the scaffold is deterministic (byte-identical on re-run); and that the write
guard refuses to clobber an existing manifest without ``force``.

Every scaffolded manifest is written to ``tmp_path`` only — the real fixture
manifests are never touched.
"""

from __future__ import annotations

import json

import pytest

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE

from logic_mix_os.analyzers.source_material_detector import (
    detect_source_material,
    guess_source_kind,
)
from logic_mix_os.constants import SOURCE_KINDS
from logic_mix_os.onramp import scaffold_manifest, write_manifest_draft
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import Project, Track, load_manifest

# All four synthetic fixtures — the 3 pinned corpus fixtures plus the P-035
# vocal-chop fixture. The scaffolder ignores each fixture's shipped manifest and
# rebuilds a draft from the stems folder alone.
ALL_FIXTURES = FIXTURE_NAMES + [VOCAL_CHOP_FIXTURE]


def _stems(name: str):
    return ROOT / "fixtures" / name / "stems"


@pytest.mark.usefixtures("_ensure_fixtures")
class TestScaffoldShape:
    @pytest.mark.parametrize("name", ALL_FIXTURES)
    def test_draft_has_required_shape(self, name):
        m = scaffold_manifest(_stems(name))

        # top-level draft annotations
        assert m["_draft"] is True
        assert isinstance(m["_needs_review"], list)

        # project block: title from folder, WAV-probed format, blank tempo/key
        proj = m["project"]
        assert proj["song_title"] and isinstance(proj["song_title"], str)
        assert proj["tempo"] is None and proj["key"] is None
        # the fixtures are PCM WAV, so the header probe must succeed
        assert isinstance(proj["sample_rate"], int) and proj["sample_rate"] > 0
        assert isinstance(proj["bit_depth"], int) and proj["bit_depth"] > 0

        # intent stub — required keys, empty values
        intent = m["intent"]
        assert intent == {
            "singular_emotional_truth": "",
            "references": [],
            "negative_constraints": [],
        }

        # one fillable section stub 0:00 -> (blank end)
        assert len(m["sections"]) == 1
        sec = m["sections"][0]
        assert sec["section_id"] == "section_1"
        assert sec["start_time"] == "0:00"
        assert sec["end_time"] == ""
        assert sec["emotional_goal"] == ""

        # one track per audio file, every guessed kind grounded in the vocabulary
        assert m["tracks"], "every fixture has at least one stem"
        for t in m["tracks"]:
            assert set(t) == {"file", "name", "source_kind"}
            assert t["source_kind"] in SOURCE_KINDS

        # _needs_review only ever names tracks that exist
        track_names = {t["name"] for t in m["tracks"]}
        assert set(m["_needs_review"]) <= track_names

    @pytest.mark.parametrize("name", ALL_FIXTURES)
    def test_tracks_are_sorted_by_filename(self, name):
        m = scaffold_manifest(_stems(name))
        files = [t["file"] for t in m["tracks"]]
        assert files == sorted(files)


@pytest.mark.usefixtures("_ensure_fixtures")
class TestScaffoldDrivesPipeline:
    @pytest.mark.parametrize("name", ALL_FIXTURES)
    def test_scaffold_round_trips_through_analyze(self, name, tmp_path):
        stems = _stems(name)
        out = tmp_path / "project_manifest.json"
        path = write_manifest_draft(stems, out)
        assert path == out and out.exists()

        # the draft is real, on-disk JSON the loader accepts
        loaded = load_manifest(out)
        assert loaded == scaffold_manifest(stems)

        # Project.from_inputs binds it to the stems folder without error
        project = Project.from_inputs(str(stems), loaded)
        assert project.tracks and project.resolved_tracks()

        # and the full pipeline runs on the scaffolded manifest
        result = analyze(str(stems), loaded)
        assert result.doctrine_score
        assert len(result.track_analysis) == len(loaded["tracks"])


@pytest.mark.usefixtures("_ensure_fixtures")
class TestDeterminism:
    @pytest.mark.parametrize("name", ALL_FIXTURES)
    def test_scaffold_dict_is_deterministic(self, name):
        assert scaffold_manifest(_stems(name)) == scaffold_manifest(_stems(name))

    @pytest.mark.parametrize("name", ALL_FIXTURES)
    def test_written_file_is_byte_identical_on_rerun(self, name, tmp_path):
        a = tmp_path / "a.json"
        b = tmp_path / "b.json"
        write_manifest_draft(_stems(name), a)
        write_manifest_draft(_stems(name), b)
        assert a.read_bytes() == b.read_bytes()


@pytest.mark.usefixtures("_ensure_fixtures")
class TestForceGuard:
    def test_refuses_overwrite_without_force(self, tmp_path):
        stems = _stems(FIXTURE_NAMES[0])
        out = tmp_path / "project_manifest.json"
        write_manifest_draft(stems, out)
        before = out.read_bytes()
        with pytest.raises(FileExistsError):
            write_manifest_draft(stems, out)
        assert out.read_bytes() == before  # untouched by the refused write

    def test_force_overwrites(self, tmp_path):
        stems = _stems(FIXTURE_NAMES[0])
        out = tmp_path / "project_manifest.json"
        out.write_text("{}\n", encoding="utf-8")
        write_manifest_draft(stems, out, force=True)
        assert load_manifest(out)["_draft"] is True


@pytest.mark.usefixtures("_ensure_fixtures")
class TestSharedHeuristic:
    """The scaffolder reuses the detector's ONE table — no second copy."""

    def test_guess_is_always_grounded(self):
        for name in ["Splice Loop", "Reverb Return", "Synth Lead", "Kick",
                     "Lead Vocal", "mystery-thing-42", ""]:
            kind, confidence, _evidence = guess_source_kind(name)
            assert kind in SOURCE_KINDS
            assert 0.0 <= confidence <= 1.0

    def test_scaffolder_and_detector_agree_on_name_only_tracks(self):
        # With no manifest hint, the detector's source_kind must equal the shared
        # guess over the same "<name> <basename>" string — proving one table.
        for name, filename in [
            ("Splice Loop", "Splice Loop.wav"),
            ("Kick", "Kick.wav"),
            ("Lead Vocal", "Lead Vocal.wav"),
            ("Synth Pad", "Synth Pad.wav"),
        ]:
            track = Track(track_id="t", name=name, file=filename)
            detected = detect_source_material(track, None)["source_kind"]
            expected, _c, _e = guess_source_kind(f"{name} {filename}")
            assert detected == expected, name
