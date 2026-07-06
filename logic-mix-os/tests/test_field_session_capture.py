"""P-058 — Field-session capture proof suite.

Binds the D2 deliverable: after a real session has recorded a pass, a decision,
and taste into an explicit ``memory_dir``, ``bundle_field_session`` copies the
three memory JSONs plus the plan/verdict artifacts into a commit-back bundle and
writes a deterministic ``session_summary.json`` — READ/COPY only, raw audio
NEVER included, idempotent on re-run.
"""

from __future__ import annotations

import json

import pytest

from conftest import FIXTURE_NAMES, ROOT

from logic_mix_os.memory import ProjectMemory
from logic_mix_os.onramp import bundle_field_session
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest

_MEMORY_JSONS = {"mix_pass_history.json", "decision_ledger.json", "taste_profile.json"}
_AUDIO_SUFFIXES = {".wav", ".wave", ".aif", ".aiff", ".flac", ".caf", ".mp3", ".m4a"}


def _run_session(mem_dir):
    """Drive a real fixture session into ``mem_dir`` (pass + decision + taste)."""
    name = FIXTURE_NAMES[0]
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    result = analyze(str(ROOT / "fixtures" / name / "stems"), manifest)
    mem = ProjectMemory(mem_dir)
    mem.record_pass("mix_pass_01", result)
    mem.record_plan_decisions(result)
    mem.add_decision({"decision": "narrow the loop", "reason": "too wide"},
                     event_type="mix_decision")
    mem.add_feedback("too wide")
    return result


def _bundle_files(bundle):
    return {p.name for p in bundle.iterdir() if p.is_file()}


@pytest.fixture()
def session(tmp_path):
    """A recorded memory_dir + a populated analysis artifacts_dir."""
    mem_dir = tmp_path / "memory"
    artifacts_dir = tmp_path / "output"
    result = _run_session(mem_dir)
    write_artifacts(result, artifacts_dir)
    # a stray exported stem living next to the artifacts — must never be bundled
    (artifacts_dir / "Lead Vocal.wav").write_bytes(b"RIFF....FAKEWAVE")
    return {"mem_dir": mem_dir, "artifacts_dir": artifacts_dir}


@pytest.mark.usefixtures("_ensure_fixtures")
class TestCaptureBundle:
    def test_bundle_has_the_three_memory_jsons(self, session, tmp_path):
        bundle = tmp_path / "bundle"
        info = bundle_field_session(session["mem_dir"], bundle,
                                    artifacts_dir=session["artifacts_dir"])
        names = _bundle_files(bundle)
        assert _MEMORY_JSONS <= names
        assert set(info["memory_files"]) == _MEMORY_JSONS
        # every copied memory file is valid JSON
        for fname in _MEMORY_JSONS:
            json.loads((bundle / fname).read_text())

    def test_bundle_has_plan_and_verdict_artifacts(self, session, tmp_path):
        bundle = tmp_path / "bundle"
        bundle_field_session(session["mem_dir"], bundle,
                             artifacts_dir=session["artifacts_dir"])
        names = _bundle_files(bundle)
        for required in ("mix_plan.json", "doctrine_score.json", "governance.json",
                         "logic_action_checklist.md", "mix_verdict.md"):
            assert required in names, required

    def test_bundle_writes_a_session_summary(self, session, tmp_path):
        bundle = tmp_path / "bundle"
        info = bundle_field_session(session["mem_dir"], bundle,
                                    artifacts_dir=session["artifacts_dir"])
        summary = json.loads((bundle / "session_summary.json").read_text())
        assert summary["counts"]["mix_passes"] == 1
        assert summary["counts"]["decisions"] >= 1
        assert summary["counts"]["taste_feedback"] == 1
        assert summary["latest_pass"] == "mix_pass_01"
        assert set(summary["captured"]["memory_files"]) == _MEMORY_JSONS
        assert "mix_plan.json" in summary["captured"]["artifacts"]
        # the returned dict mirrors what landed on disk
        assert set(info["memory_files"]) == _MEMORY_JSONS
        assert "session_summary.json" not in info["artifacts"]

    def test_no_audio_is_ever_bundled(self, session, tmp_path):
        bundle = tmp_path / "bundle"
        info = bundle_field_session(session["mem_dir"], bundle,
                                    artifacts_dir=session["artifacts_dir"])
        for p in bundle.iterdir():
            assert p.suffix.lower() not in _AUDIO_SUFFIXES, p.name
        assert not any(a.lower().endswith(".wav") for a in info["artifacts"])
        assert not (bundle / "Lead Vocal.wav").exists()

    def test_audio_in_memory_dir_is_not_copied(self, session, tmp_path):
        # even a rogue stem sitting in the memory dir is ignored: capture copies
        # ONLY the three explicitly named memory JSONs.
        (session["mem_dir"] / "rogue_stem.wav").write_bytes(b"RIFF....FAKE")
        bundle = tmp_path / "bundle"
        bundle_field_session(session["mem_dir"], bundle,
                             artifacts_dir=session["artifacts_dir"])
        assert not (bundle / "rogue_stem.wav").exists()


@pytest.mark.usefixtures("_ensure_fixtures")
class TestCaptureIsSafe:
    def test_missing_memory_files_are_skipped_gracefully(self, tmp_path):
        empty_mem = tmp_path / "empty_memory"
        empty_mem.mkdir()
        bundle = tmp_path / "bundle"
        info = bundle_field_session(empty_mem, bundle)  # no artifacts either
        assert info["memory_files"] == []
        assert info["artifacts"] == []
        # a summary is still written; nothing crashes
        summary = json.loads((bundle / "session_summary.json").read_text())
        assert summary["counts"] == {"mix_passes": 0, "decisions": 0,
                                     "taste_feedback": 0}

    def test_bundle_is_idempotent(self, session, tmp_path):
        bundle = tmp_path / "bundle"
        first = bundle_field_session(session["mem_dir"], bundle,
                                     artifacts_dir=session["artifacts_dir"])
        snapshot = {p.name: p.read_bytes() for p in bundle.iterdir() if p.is_file()}

        second = bundle_field_session(session["mem_dir"], bundle,
                                      artifacts_dir=session["artifacts_dir"])
        after = {p.name: p.read_bytes() for p in bundle.iterdir() if p.is_file()}

        assert set(snapshot) == set(after)
        assert snapshot == after  # byte-identical re-run, clean overwrite
        assert first == second
