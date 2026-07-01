"""P-029 — the pivot: ``analyze(producer=…)`` SELECTS which profile drives the
judgment. Two load-bearing proofs live here:

* **Byte-identical default** — the no-arg path, ``producer="halee_ramone"``, and
  passing the reference ``ProducerProfile`` object all produce the SAME analysis
  as pre-P-029. This is the guard that threading a per-call profile did not move
  the default output (the corpus-level version is the UNCHANGED golden regression
  68/68).

* **Selection-liveness** — a SECOND profile differing from ``halee_ramone`` in
  exactly ONE value flows through the REAL ``analyze()`` path and changes the
  output in the way that value predicts. This FAILS if the profile is accepted
  but ignored — byte-identical-by-default alone would NOT catch that bug (the
  P-016 lesson). The load-bearing check (that removing the threading breaks this)
  is documented in the packet receipt.

The mechanism for the second profile is a synthetic ``ProducerProfile`` built by
``dataclasses.replace`` off the reference load, mutating one doctrine coefficient
or one ``kind_score``. It is passed straight to ``analyze(producer=<profile>)``,
so it flows through the real pipeline, not a monkeypatched scorer.
"""

from __future__ import annotations

import copy
import dataclasses

import pytest

from logic_mix_os.doctrine.producer_profile import ProducerProfile, load_profile
from logic_mix_os.pipeline import analyze
from logic_mix_os.project import load_manifest

from conftest import FIXTURE_NAMES, ROOT


def _analyze(name: str, **kw):
    manifest = load_manifest(ROOT / "fixtures" / name / "project_manifest.json")
    return analyze(str(ROOT / "fixtures" / name / "stems"), manifest, **kw)


def _snap(result) -> dict:
    """A byte-comparable snapshot of every judgment artifact the profile feeds."""
    return {
        "doctrine_score": copy.deepcopy(result.doctrine_score),
        "creative": copy.deepcopy(result.creative),
        "governance": copy.deepcopy(result.governance),
        "mix_plan": copy.deepcopy(result.mix_plan),
    }


# --------------------------------------------------------------------------- #
# Byte-identical default — no-arg == producer="halee_ramone" == reference object
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_default_equals_named_reference(name):
    """The no-arg default path and ``producer="halee_ramone"`` are byte-identical
    across every judgment artifact — threading a per-call profile did not move the
    default output."""
    default = _snap(_analyze(name))
    named = _snap(_analyze(name, producer="halee_ramone"))
    assert default == named


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_default_equals_reference_profile_object(name):
    """Passing the reference ``ProducerProfile`` OBJECT (not just its name) is also
    byte-identical to the default path — the object route threads the same values."""
    ref = load_profile("halee_ramone")
    default = _snap(_analyze(name))
    via_obj = _snap(_analyze(name, producer=ref))
    assert default == via_obj


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_default_is_deterministic(name):
    """Same producer, same inputs -> byte-identical output across repeated calls."""
    first = _snap(_analyze(name, producer="halee_ramone"))
    second = _snap(_analyze(name, producer="halee_ramone"))
    assert first == second


# --------------------------------------------------------------------------- #
# Selection-liveness — a one-value-different profile changes the REAL analyze()
# output in the way that value predicts. FAILS if the profile is ignored.
# --------------------------------------------------------------------------- #
def _mutated_profile(**doctrine_over) -> ProducerProfile:
    """Reference profile with a single doctrine value changed. Everything else is
    byte-identical to ``halee_ramone`` — so any output difference is attributable
    to exactly the mutated value."""
    ref = load_profile("halee_ramone")
    doctrine = copy.deepcopy(ref.doctrine)
    for path, value in doctrine_over.items():
        # path like "baselines.halee" or "weights.halee_score"
        keys = path.split(".")
        node = doctrine
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
    return dataclasses.replace(ref, doctrine=doctrine)


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_doctrine_baseline_is_a_live_lever(name):
    """Lowering the ``halee`` baseline by exactly 20 in a second profile must lower
    the real ``halee_score`` by EXACTLY 20 vs the reference — proving
    ``analyze(producer=…)`` threads the doctrine profile to ``_halee``, not ignoring
    it. The ``_halee`` penalties are additive on top of the baseline and the
    reference score has clamp headroom on every fixture (58.0 / 67.6 / 81.3, all in
    (20, 100)), so a -20 baseline shifts the whole score down by exactly 20. This
    FAILS if the profile is accepted but ignored (the score would not move)."""
    ref = _analyze(name, producer="halee_ramone")
    lowered = _analyze(name, producer=_mutated_profile(**{"baselines.halee": 66.0}))

    ref_halee = ref.doctrine_score["halee_score"]
    low_halee = lowered.doctrine_score["halee_score"]
    # Guard the arithmetic: the reference must have clamp headroom so the -20
    # baseline is not swallowed by the [0,100] clamp — true for all fixtures.
    assert 20.0 < ref_halee < 100.0
    assert round(ref_halee - low_halee, 1) == 20.0
    # Overall readiness weights halee_score in, so it moves strictly down too.
    assert (lowered.doctrine_score["overall_mix_readiness_score"]
            < ref.doctrine_score["overall_mix_readiness_score"])


def test_kind_score_is_a_live_lever():
    """A creative lever: raising ``vocal_ride``'s curated dims to the ceiling in a
    second profile must raise that variant's ``overall_score`` in the REAL
    ``analyze()`` output vs the reference — proving the creative profile is threaded
    to ``score_variant``, not ignored."""
    name = "simple_vocal_piano_song"
    ref = load_profile("halee_ramone")
    kind_scores = copy.deepcopy(ref.kind_scores)
    # Push every numeric dim of vocal_ride to 100 (and translation to the
    # zero-penalty class) so its overall_score is maximal in the boosted profile.
    boosted_cell = dict(kind_scores["vocal_ride"])
    for dim in ("technical", "halee", "ramone", "contrast",
                "vocal_belief", "excitement", "taste"):
        boosted_cell[dim] = 100
    boosted_cell["translation"] = "low"
    kind_scores["vocal_ride"] = boosted_cell
    boosted = dataclasses.replace(ref, kind_scores=kind_scores)

    ref_result = _analyze(name, producer="halee_ramone")
    boosted_result = _analyze(name, producer=boosted)

    ref_score = _vocal_ride_overall(ref_result)
    boosted_score = _vocal_ride_overall(boosted_result)
    assert ref_score is not None and boosted_score is not None
    assert boosted_score > ref_score
    assert boosted_score == 100.0


def _vocal_ride_overall(result):
    """The overall_score of any ``vocal_ride`` variant in the creative branches."""
    for branch in result.creative.get("branches", []):
        for v in branch.get("variants", []):
            if v["kind"] == "vocal_ride":
                return v["scores"]["overall_score"]
    return None
