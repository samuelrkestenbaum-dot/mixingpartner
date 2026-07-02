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


# The ORIGINAL three fixtures — the shared parametrization for the pinned
# byte-identity corpus. The 4th fixture (vocal_chop_groove, P-035) lives
# DELIBERATELY outside this list: every suite keyed on these three stays
# pin-to-3 by construction, and the 4th fixture's own pins live in
# tests/test_vocal_chop_groove.py (with the conscious P-032i flip in
# tests/test_differential_proof.py reading ``chop_groove_analyzed`` below).
FIXTURE_NAMES = [
    "simple_vocal_piano_song",
    "dense_chorus_with_loops",
    "splice_loop_problem",
]

# The P-035 fixture: the first project with non-lead vocal stems — the one
# that makes the vocal_band_masking capacity and the blend policy LIVE.
VOCAL_CHOP_FIXTURE = "vocal_chop_groove"

# THE REGRESSION CORPUS COUNT — the canonical explanation, pointed to by every
# "93/93 (the P-035 corpus — see conftest.py)" pin across the suite: P-035
# moved the golden corpus count CONSCIOUSLY from 68 to 93 — +25 checks from
# the vocal_chop_groove fixture (its golden snapshot comparisons + doctrine
# invariants). Any future fixture moves this count again only as a conscious,
# documented decision — never a silent widening (the P-035 convention note).


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


@pytest.fixture(scope="session")
def chop_groove_analyzed(_ensure_fixtures):
    """The P-035 fixture under BOTH producers, once per session — the live
    half of the P-032f blend corollary: ``{producer: ProjectAnalysis}``."""
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest

    manifest = load_manifest(
        ROOT / "fixtures" / VOCAL_CHOP_FIXTURE / "project_manifest.json"
    )
    stems = str(ROOT / "fixtures" / VOCAL_CHOP_FIXTURE / "stems")
    return {
        "halee_ramone": analyze(stems, manifest),
        "timbaland": analyze(stems, manifest, producer="timbaland"),
    }
