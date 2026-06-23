"""Top-level pytest conftest.

Puts the project root on ``sys.path`` (so ``import logic_mix_os`` works without
an install) and ensures the synthetic fixtures exist before any test runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fixtures.generate_fixtures import ensure_fixtures  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _ensure_fixtures():
    ensure_fixtures()


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return ROOT / "fixtures"


FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]


@pytest.fixture(scope="session")
def analyzed(_ensure_fixtures):
    """Run the full pipeline once per fixture and cache the results."""
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest

    results = {}
    for name in FIXTURE_NAMES:
        manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
        results[name] = analyze(str(ROOT / "fixtures" / name / "stems"), manifest)
    return results
