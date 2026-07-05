"""P-048 — THE MODE-DEMO REFRESH: the committed producer x mode demo pairs.

``examples/mode_demos/`` carries the MODE-level differential in committed
form, the way ``examples/sample_output*`` carries the producer-level one
(tests/test_sample_refresh.py). Eleven demo directories (P-053 added CLA's
two — ``chris_lord_alge_conservative`` widening the same-mode conservative
comparison to five producers, and ``chris_lord_alge_big_chorus``, his named
center-of-gravity mode reaching arrangement_lift), all rendered by the real
CLI from the SAME stems — the seeded ``dense_chorus_with_loops`` fixture,
chosen because it is the only fixture that fires ALL FIVE creative problems
(so the density branch, where three extended ids live, is on the surface)
and because it is the fixture every standing mode/dropout pin already runs
on (tests/test_mode_forking.py, tests/test_negative_space_dropout.py,
tests/test_move_vocabulary_expansion.py).

Each directory is the output of exactly one verbatim invocation from the
project root (after ``python fixtures/generate_fixtures.py``) — the same
invocations the README quotes::

    python -m logic_mix_os.cli creative \\
      --stems fixtures/dense_chorus_with_loops/stems \\
      --manifest fixtures/dense_chorus_with_loops/project_manifest.json \\
      [--producer <name>] --mode <mode> --out examples/mode_demos/<demo>

THE COMMITTED UNIT (the packet's judgment call): the ``creative`` command
writes the full 30-artifact tree, but the mode story lives entirely in TWO
of those files — ``creative.json`` (the machine surface: candidate ids,
declarations echo, per-branch fork reports, winners) and
``creative_report.md`` (the human surface: the mode-reach line and the
per-branch fork lines). Each demo directory keeps exactly that CREATIVE
PAIR from its run; the other 28 artifacts tell the producer-level story the
four ``sample_output*`` trees already commit in full. Committing nine full
trees would have tripled the committed example surface to say the same two
files' worth of new signal.

THE STALENESS PIN (the P-040 pattern at full strength on the kept unit):
each committed pair must byte-match a freshly generated run — no
normalization at all is needed here (unlike the sample trees' stems-path
echo, the creative pair carries no input path), and no absolute path may
appear in any committed byte. ``write_artifacts`` is pure rendering and
P-039 pinned that the CLI tree byte-matches the library ``write_artifacts``
tree, so the library run is an honest stand-in for the committed pairs'
actual CLI provenance. Determinism is real (seeded fixture; two consecutive
CLI regenerations were byte-identical at commit time for every demo).

THE SURFACE PIN re-reads the committed ``creative.json`` files DIRECTLY:
the README's mode-demo table quotes exactly these candidate-id sets,
declarations and winners, so the docs' claims stay machine-checked even
though the staleness pin already implies them transitively. Every value
here agrees with the standing live-engine pins:

* halee three-way (tests/test_mode_forking.py::
  test_same_producer_different_modes_different_candidate_sets);
* the conservative four-way (…::
  test_same_mode_different_producers_different_candidate_sets);
* quincy's experimental reach — both his families live, ``vocal_C`` WINNING
  the vocal_belief branch (tests/test_move_vocabulary_expansion.py);
* timbaland's negative_space/groove_pocket dropout contrast — targets and
  prose (tests/test_negative_space_dropout.py, DROPOUT_TARGETS on the dense
  fixture).
"""

from __future__ import annotations

import json

import pytest

from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest

from conftest import ROOT
from test_move_vocabulary_expansion import AUTHORED_OVERALLS
from test_negative_space_dropout import (
    AUTHORED_DROPOUT,
    CHORUS_F_CHANGES,
    DENSITY_E_CHANGES,
)

DEMO_FIXTURE = "dense_chorus_with_loops"
DEMO_ROOT = ROOT / "examples" / "mode_demos"
DEMO_FILES = ("creative.json", "creative_report.md")

# demo directory -> (producer, mode). halee_ramone is the CLI default
# producer; her demos' documented invocations carry no --producer flag.
MODE_DEMOS = {
    "brian_eno_conservative": ("brian_eno", "conservative"),
    "chris_lord_alge_big_chorus": ("chris_lord_alge", "big_chorus"),
    "chris_lord_alge_conservative": ("chris_lord_alge", "conservative"),
    "halee_ramone_conservative": ("halee_ramone", "conservative"),
    "halee_ramone_deconstructive": ("halee_ramone", "deconstructive"),
    "halee_ramone_dramatic_contrast": ("halee_ramone", "dramatic_contrast"),
    "quincy_jones_conservative": ("quincy_jones", "conservative"),
    "quincy_jones_experimental": ("quincy_jones", "experimental"),
    "timbaland_conservative": ("timbaland", "conservative"),
    "timbaland_groove_pocket": ("timbaland", "groove_pocket"),
    "timbaland_negative_space": ("timbaland", "negative_space"),
}

# Each demo's authored declarations echo, verbatim from the committed bytes
# (None = an authored-neutral mode: zero declaration keys, zero fork keys —
# the P-042 byte-silence discipline; note it holds for an EXPLICIT --mode
# too: halee's dramatic_contrast and timbaland's conservative are byte-silent
# even when asked for by name).
DECLARATIONS = {
    "brian_eno_conservative": {
        "allowed_risk": "low", "favor_kinds": ["depth_cleanup"],
        "suppress_kinds": ["width_bloom", "vocal_ride"],
    },
    # P-053 CLA. His big_chorus is his named center-of-gravity mode ("the
    # chorus lands bigger than the verse") — medium posture, favors the
    # width move, and REACHES arrangement_lift (the one CLA mode with a
    # reach key in this demo set). His conservative authors a low posture
    # that SUPPRESSES the subtractive move — his "commit, the thinning-out
    # moves are withheld" bias, the only committed conservative that drops
    # subtractive_drop.
    "chris_lord_alge_big_chorus": {
        "allowed_risk": "medium", "favor_kinds": ["width_bloom"],
        "suppress_kinds": [], "reach_kinds": ["arrangement_lift"],
    },
    "chris_lord_alge_conservative": {
        "allowed_risk": "low", "favor_kinds": [],
        "suppress_kinds": ["subtractive_drop"],
    },
    "halee_ramone_conservative": {
        "allowed_risk": "low", "favor_kinds": ["vocal_ride", "depth_cleanup"],
        "suppress_kinds": ["width_bloom"],
    },
    "halee_ramone_deconstructive": {
        "allowed_risk": "medium",
        "favor_kinds": ["subtractive_drop", "loop_deconstruct"],
        "suppress_kinds": ["width_bloom", "drum_room_bloom"],
    },
    "halee_ramone_dramatic_contrast": None,
    "quincy_jones_conservative": {
        "allowed_risk": "low", "favor_kinds": ["vocal_ride"],
        "suppress_kinds": ["width_bloom", "drum_room_bloom"],
    },
    "quincy_jones_experimental": {
        "allowed_risk": "high",
        "favor_kinds": ["arrangement_lift", "ensemble_rebalance"],
        "suppress_kinds": [],
        "reach_kinds": ["arrangement_lift", "ensemble_rebalance"],
    },
    "timbaland_conservative": None,
    "timbaland_groove_pocket": {
        "allowed_risk": "low",
        "favor_kinds": ["drum_room_bloom", "subtractive_drop"],
        "suppress_kinds": ["width_bloom"],
    },
    "timbaland_negative_space": {
        "allowed_risk": "medium", "favor_kinds": ["subtractive_drop"],
        "suppress_kinds": ["width_bloom", "drum_room_bloom"],
        "reach_kinds": ["negative_space_dropout"],
    },
}

# The candidate-id lists per branch, ORDER INCLUDED (favor fronts, reach
# appends per the engine's curated order) — the README table quotes these
# as sets. The loop and depth branches are invariant across all nine demos
# at the set level ({loop_A, loop_B} / {depth_A}): no shipped mode
# suppresses their pool kinds and no extended family addresses them here.
BRANCH_IDS = {
    "brian_eno_conservative": {
        "chorus_lift": ["chorus_lift_B", "chorus_lift_D"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_B"],
    },
    # CLA big_chorus: the width favor fronts nothing new here (chorus_lift_A
    # is already width_bloom), the reach APPENDS the arrangement_lift ids
    # (chorus_lift_E, density_C) to the end of the curated order — and both
    # WIN their branches (see WINNERS): the reach takes the verdict.
    "chris_lord_alge_big_chorus": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D", "chorus_lift_E"],
        "density": ["density_A", "density_B", "density_C"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    # CLA conservative: subtractive_drop suppressed — the ONLY committed
    # conservative demo whose chorus_lift drops chorus_lift_B (subtractive)
    # and whose density/loop fall to a single non-subtractive candidate.
    "chris_lord_alge_conservative": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_C", "chorus_lift_D"],
        "density": ["density_A"],
        "loop": ["loop_A"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "halee_ramone_conservative": {
        "chorus_lift": ["chorus_lift_C", "chorus_lift_B", "chorus_lift_D"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "halee_ramone_deconstructive": {
        "chorus_lift": ["chorus_lift_B", "chorus_lift_C"],
        "density": ["density_B", "density_A"],
        "loop": ["loop_B", "loop_A"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "halee_ramone_dramatic_contrast": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "quincy_jones_conservative": {
        "chorus_lift": ["chorus_lift_C", "chorus_lift_B"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "quincy_jones_experimental": {
        "chorus_lift": ["chorus_lift_E", "chorus_lift_A", "chorus_lift_B",
                        "chorus_lift_C", "chorus_lift_D"],
        "density": ["density_C", "density_D", "density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_C", "vocal_A", "vocal_B"],
    },
    "timbaland_conservative": {
        "chorus_lift": ["chorus_lift_A", "chorus_lift_B", "chorus_lift_C",
                        "chorus_lift_D"],
        "density": ["density_A", "density_B"],
        "loop": ["loop_A", "loop_B"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "timbaland_groove_pocket": {
        "chorus_lift": ["chorus_lift_D", "chorus_lift_B", "chorus_lift_C"],
        "density": ["density_B", "density_A"],
        "loop": ["loop_B", "loop_A"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
    "timbaland_negative_space": {
        "chorus_lift": ["chorus_lift_B", "chorus_lift_C", "chorus_lift_F"],
        "density": ["density_B", "density_A", "density_E"],
        "loop": ["loop_B", "loop_A"],
        "depth": ["depth_A"],
        "vocal_belief": ["vocal_A", "vocal_B"],
    },
}

# The per-branch ``reached`` report for the two demos whose modes author
# reach — exactly where the extended pool holds a variant, empty elsewhere,
# ``reach_capped`` empty everywhere (both authored reaches live inside
# their modes' risk postures).
REACHED = {
    "chris_lord_alge_big_chorus": {
        "chorus_lift": ["arrangement_lift"],
        "density": ["arrangement_lift"],
        "loop": [], "depth": [], "vocal_belief": [],
    },
    "quincy_jones_experimental": {
        "chorus_lift": ["arrangement_lift"],
        "density": ["arrangement_lift", "ensemble_rebalance"],
        "loop": [], "depth": [],
        "vocal_belief": ["ensemble_rebalance"],
    },
    "timbaland_negative_space": {
        "chorus_lift": ["negative_space_dropout"],
        "density": ["negative_space_dropout"],
        "loop": [], "depth": [], "vocal_belief": [],
    },
}

# Branch winners. The mode fork moves candidate SETS far more than verdicts:
# most demos win the same four non-vocal moves. The exceptions are all
# authored realities — eno's conservative suppresses vocal_ride so his
# intimacy pass is the only vocal candidate left (vocal_B, the P-045 pin);
# quincy's high-posture experimental REACHES a winner (vocal_C at his
# authored 83.1 — tests/test_move_vocabulary_expansion.py); and P-053's CLA
# demos, whose impact/commitment posture wins the drum-room and reached
# arrangement_lift moves outright. Two committed demos now let a REACHED
# variant take a verdict: quincy_experimental (vocal_C) and
# chris_lord_alge_big_chorus (chorus_lift_E + density_C, arrangement_lift).
_COMMON_WINNERS = {
    "chorus_lift": "chorus_lift_B", "density": "density_B", "loop": "loop_B",
    "depth": "depth_A", "vocal_belief": "vocal_A",
}
WINNERS = {demo: dict(_COMMON_WINNERS) for demo in MODE_DEMOS}
WINNERS["brian_eno_conservative"]["vocal_belief"] = "vocal_B"
WINNERS["quincy_jones_experimental"]["vocal_belief"] = "vocal_C"
# CLA big_chorus: the reached arrangement_lift ids win chorus_lift and
# density; loop falls to loop_A (loop_deconstruct) as his impact move over
# the subtractive loop_B.
WINNERS["chris_lord_alge_big_chorus"] = {
    "chorus_lift": "chorus_lift_E", "density": "density_C", "loop": "loop_A",
    "depth": "depth_A", "vocal_belief": "vocal_A",
}
# CLA conservative: subtractive_drop suppressed, so the drum-room move wins
# chorus_lift (chorus_lift_D) and the sole survivors win density/loop.
WINNERS["chris_lord_alge_conservative"] = {
    "chorus_lift": "chorus_lift_D", "density": "density_A", "loop": "loop_A",
    "depth": "depth_A", "vocal_belief": "vocal_A",
}

# The extended-id universe on this fixture's branches (the same leak guard
# as tests/test_sample_refresh.py) and each demo's admitted subset.
EXTENDED_IDS = {"chorus_lift_E", "chorus_lift_F", "vocal_C",
                "density_C", "density_D", "density_E"}
EXTENDED_PRESENT = {demo: set() for demo in MODE_DEMOS}
EXTENDED_PRESENT["quincy_jones_experimental"] = {
    "chorus_lift_E", "density_C", "density_D", "vocal_C"}
EXTENDED_PRESENT["timbaland_negative_space"] = {"chorus_lift_F", "density_E"}
# CLA big_chorus reaches arrangement_lift only: chorus_lift_E + density_C
# (no ensemble_rebalance/dropout ids — his big_chorus authors just the one
# reach kind).
EXTENDED_PRESENT["chris_lord_alge_big_chorus"] = {"chorus_lift_E", "density_C"}


@pytest.fixture(scope="module")
def demo_analyses():
    """One real pipeline run per demo — the same producer/mode the committed
    pair was rendered from, each producer resolved dynamically by name."""
    manifest = load_manifest(
        ROOT / "fixtures" / DEMO_FIXTURE / "project_manifest.json"
    )
    stems = str(ROOT / "fixtures" / DEMO_FIXTURE / "stems")
    return {
        demo: analyze(stems, manifest, creative_mode=mode, producer=producer)
        for demo, (producer, mode) in MODE_DEMOS.items()
    }


@pytest.mark.parametrize("demo", sorted(MODE_DEMOS))
def test_committed_mode_demo_pair_matches_a_fresh_render(
    demo, demo_analyses, tmp_path
):
    """THE STALENESS PIN: each committed demo directory holds EXACTLY the
    creative pair, and both files are byte-identical to a fresh
    ``write_artifacts`` render of the same producer/mode run — no
    normalization, no absolute path anywhere in the committed bytes."""
    committed = DEMO_ROOT / demo
    fresh = tmp_path / "fresh"
    write_artifacts(demo_analyses[demo], fresh)

    assert not any(p.is_dir() for p in committed.iterdir()), demo
    committed_files = sorted(p.name for p in committed.iterdir())
    assert committed_files == sorted(DEMO_FILES), demo
    for name in DEMO_FILES:
        committed_bytes = (committed / name).read_bytes()
        assert str(ROOT).encode("utf-8") not in committed_bytes, (demo, name)
        assert committed_bytes == (fresh / name).read_bytes(), (demo, name)


@pytest.mark.parametrize("demo", sorted(MODE_DEMOS))
def test_committed_mode_demo_surface_is_the_pinned_reality(demo):
    """THE SURFACE PIN: the committed creative.json carries exactly its
    demo's mode surface — the resolved mode with NO fallback, the authored
    declarations echo (byte-silence for the two authored-neutral demos), the
    per-branch candidate-id lists order-included, the honest reach reports,
    the branch winners, and no extended id beyond the demo's admitted set."""
    cr = json.loads(
        (DEMO_ROOT / demo / "creative.json").read_text(encoding="utf-8")
    )
    _, mode = MODE_DEMOS[demo]
    assert cr["search_mode"] == mode
    assert "search_mode_fallback" not in cr

    declared = DECLARATIONS[demo]
    if declared is None:
        assert "search_mode_declarations" not in cr
        for b in cr["branches"]:
            assert "mode_fork" not in b, (demo, b["problem_id"])
    else:
        assert cr["search_mode_declarations"] == declared
        for b in cr["branches"]:
            fork = b["mode_fork"]
            assert fork["risk_capped"] == [], (demo, b["problem_id"])
            if "reach_kinds" in declared:
                assert fork["reached"] == REACHED[demo][b["problem_id"]], \
                    (demo, b["problem_id"])
                assert fork["reach_capped"] == [], (demo, b["problem_id"])
            else:
                assert "reached" not in fork, (demo, b["problem_id"])

    ids = {b["problem_id"]: [v["variant_id"] for v in b["variants"]]
           for b in cr["branches"]}
    assert ids == BRANCH_IDS[demo]

    winners = {b["problem_id"]: b["winning"]["winning_variant"]
               for b in cr["branches"]}
    assert winners == WINNERS[demo]

    all_ids = {vid for branch_ids in ids.values() for vid in branch_ids}
    assert all_ids & EXTENDED_IDS == EXTENDED_PRESENT[demo], demo


def test_committed_quincy_demo_reaches_both_his_families():
    """Demo: quincy reaching arrangement_lift AND ensemble_rebalance on one
    committed run — his experimental admits all four extended ids at his
    authored curated overalls (85.3 / 83.1, reconstructed-from-JSON pins in
    tests/test_move_vocabulary_expansion.py), and the reached ``vocal_C``
    WINS its branch — one of two committed reach-and-win demos where the
    reach moves a verdict (alongside ``chris_lord_alge_big_chorus``, whose
    reached ``chorus_lift_E`` wins its chorus_lift branch, pinned above),
    exactly the standing live pin."""
    cr = json.loads(
        (DEMO_ROOT / "quincy_jones_experimental" / "creative.json")
        .read_text(encoding="utf-8")
    )
    by_id = {v["variant_id"]: v for b in cr["branches"] for v in b["variants"]}
    for vid, kind in (("chorus_lift_E", "arrangement_lift"),
                      ("density_C", "arrangement_lift"),
                      ("density_D", "ensemble_rebalance"),
                      ("vocal_C", "ensemble_rebalance")):
        assert by_id[vid]["kind"] == kind
        assert by_id[vid]["scores"]["overall_score"] \
            == AUTHORED_OVERALLS["quincy_jones"][kind], vid
    vocal = next(b for b in cr["branches"] if b["problem_id"] == "vocal_belief")
    assert vocal["winning"]["winning_variant"] == "vocal_C"


def test_committed_timbaland_pair_is_the_only_where_authored_contrast():
    """Demo: dropout only where authored — the PAIR is the point. His
    negative_space demo (authored reach) carries both dropout proposals at
    his honest 80.9, targeting only unprotected texture/clutter names (the
    pinned dense-fixture targets), with the verbatim engine-owned plan text
    and the reversibility tag — and both branch winners stay non-dropout
    moves. His groove_pocket demo (zero authored reach) declares favor and
    suppression but NO reach key, and not one dropout id appears."""
    reaching = json.loads(
        (DEMO_ROOT / "timbaland_negative_space" / "creative.json")
        .read_text(encoding="utf-8")
    )
    by_id = {v["variant_id"]: v
             for b in reaching["branches"] for v in b["variants"]}
    f, e = by_id["chorus_lift_F"], by_id["density_E"]
    assert f["tracks_affected"] == ["Synth Pad", "Splice Texture Loop"]
    assert e["tracks_affected"] == ["Acoustic Guitar", "Electric Guitar 1",
                                    "Electric Guitar 2", "Synth Pad",
                                    "Splice Texture Loop"]
    for v in (f, e):
        assert v["kind"] == "negative_space_dropout"
        assert v["reversibility"] == "non_destructive_duplicate_track"
        assert v["scores"]["overall_score"] \
            == AUTHORED_DROPOUT["timbaland"]["overall"]
    assert f["changes"] == CHORUS_F_CHANGES
    assert e["changes"] == DENSITY_E_CHANGES

    unreaching = json.loads(
        (DEMO_ROOT / "timbaland_groove_pocket" / "creative.json")
        .read_text(encoding="utf-8")
    )
    assert "reach_kinds" not in unreaching["search_mode_declarations"]
    for b in unreaching["branches"]:
        assert "reached" not in b["mode_fork"], b["problem_id"]
        for v in b["variants"]:
            assert v["kind"] != "negative_space_dropout", v["variant_id"]


def test_committed_halee_demos_stay_reference_safe():
    """Demo: Halee/Ramone remains default/reference-safe. Her committed
    default-flow tree is examples/sample_output (pinned in
    tests/test_sample_refresh.py); across her three committed MODE demos she
    authors zero reach — no extended id anywhere, her dramatic_contrast
    stays fully byte-silent even when selected explicitly by name, and her
    winners are the reference winners on every demo."""
    for demo in ("halee_ramone_conservative", "halee_ramone_deconstructive",
                 "halee_ramone_dramatic_contrast"):
        cr = json.loads(
            (DEMO_ROOT / demo / "creative.json").read_text(encoding="utf-8")
        )
        declared = cr.get("search_mode_declarations")
        if declared is not None:
            assert "reach_kinds" not in declared, demo
        all_ids = {v["variant_id"]
                   for b in cr["branches"] for v in b["variants"]}
        assert all_ids & EXTENDED_IDS == set(), demo
        winners = {b["problem_id"]: b["winning"]["winning_variant"]
                   for b in cr["branches"]}
        assert winners == _COMMON_WINNERS, demo


def test_committed_mode_demo_directory_set_is_exactly_the_pinned_eleven():
    """THE DIRECTORY-SET GUARD (P-049): ``examples/mode_demos/`` holds
    EXACTLY the eleven pinned demo directories (P-053 added CLA's two —
    chris_lord_alge_conservative + chris_lord_alge_big_chorus — via the
    conscious MODE_DEMOS extension this guard was designed for) —
    MODE_DEMOS' own keys, so this guard derives from the same table every
    pin above parametrizes over and can never drift from the pins it
    protects — and nothing else lives at that level (no stray file of any
    kind; reality at pin time: no README lives here). It fails LOUDLY on a
    new unpinned demo dir (which would ship staleness-unpinned), on a
    deleted pinned dir, and on any stray file. A legitimate twelfth demo
    later is a CONSCIOUS one-line MODE_DEMOS extension — which
    automatically brings the staleness and surface pins above to the
    newcomer; anything failing here without that extension is a stray
    committed artifact."""
    residents = sorted(p.name for p in DEMO_ROOT.iterdir())
    assert residents == sorted(MODE_DEMOS), residents
    non_dirs = sorted(p.name for p in DEMO_ROOT.iterdir() if not p.is_dir())
    assert non_dirs == [], non_dirs
