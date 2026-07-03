"""P-039 — Producer Selection CLI Exposure + Demo-Safe Invocation.

The ``producer=`` lever has been live in the library since P-029; this packet
makes it REACHABLE from the product surface. The user's acceptance bar,
verbatim — every clause pinned here:

    same stems
    explicit producer arg
    clear selected producer in artifacts
    Halee/Ramone remains default
    Timbaland reachable without code changes
    safety/governance unchanged
    regression clean

Guard groups:

1. **The exact command set** — ``--producer`` (default ``halee_ramone``) on
   EXACTLY the analyze-family commands (every command whose handler calls
   ``analyze()``), added through the shared-argument mechanism; help text
   names the semantics, never a hardcoded profile list (the P-038 ``--mode``
   precedent).
2. **The demo, end-to-end** — the REAL CLI entry (``cli.main`` with argv) on
   the same stems, with and without ``--producer timbaland``: both trees
   valid, each names its producer (JSON + verdict line), the known
   differential (76.3 vs 60.9 on vocal_chop_groove — the P-035 pins), and the
   default run byte-matches a no-arg LIBRARY run (Halee/Ramone remains
   default, byte-for-byte).
3. **Friendly error** — an unknown name surfaces the loader's clean
   FileNotFoundError as a friendly CLI error naming the available profiles
   (scanned from the producers directory), exit code non-zero, NO traceback —
   proven at the real process boundary (subprocess) and in-process.
4. **The identity surface** — ``doctrine_score.producer`` carries
   {name, display_name, provenance, confidence} from the PER-CALL profile's
   metadata (the P-029/P-031 threading pattern): fresh, never an alias; a
   synthetic profile's identity renders through the REAL ``analyze()`` path
   (sabotage — sourcing from the module default — fails here); the verdict /
   status / dashboard lines are data-driven (absent key => absent line).
5. **Schema + golden blindness** — the schema documents the additive key (no
   additionalProperties conflict, never required); ``build_snapshot``
   (categorical + the original score keys) cannot see the addition and the
   goldens still match with 0 criticals (regression stays 93/93 — pinned by
   the existing corpus tests).
6. **The cowork rider** — ``build_context(producer=…)`` threads the selection
   into the shared analysis; the cowork CLI command carries ``--producer``.

Safety/governance unchanged: the composed kill-switch lists in BOTH demo
trees lead with the five hardcoded safety switches verbatim (the P-032i pin,
re-asserted at the CLI-artifact level); every other safety pin runs untouched
elsewhere in the suite.
"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import shutil
import subprocess
import sys

import pytest

from logic_mix_os import cli
from logic_mix_os import cowork as cowork_module
from logic_mix_os.cowork import build_context, run_command
from logic_mix_os.doctrine import doctrine_engine
from logic_mix_os.doctrine.producer_profile import ProducerProfile, load_profile
from logic_mix_os.pipeline import analyze, write_artifacts
from logic_mix_os.project import load_manifest
from logic_mix_os.regression import build_snapshot, compare_snapshots
from logic_mix_os.renderers import markdown_renderer
from logic_mix_os.renderers.html_dashboard import render_dashboard
from logic_mix_os.renderers.operator_view import render_status
from logic_mix_os.validation.output_validator import (
    load_schema,
    validate_instance,
    validate_output,
)

from conftest import FIXTURE_NAMES, ROOT, VOCAL_CHOP_FIXTURE
from test_differential_proof import SAFETY_KILL_SWITCHES

# The exact analyze-family set: every CLI command whose handler calls
# ``analyze()`` (directly, per-project for album, or through the cowork
# ``build_context``). ``compare-reference`` is consciously EXCLUDED — its
# handler calls ``compare_to_reference`` directly, never ``analyze()`` — as is
# ``regression`` (the golden corpus is reference-producer by definition).
PRODUCER_COMMANDS = {
    "analyze",
    "detect-identities",
    "analyze-sections",
    "generate-plan",
    "status",
    "creative",
    "governance",
    "mixer-feedback",
    "memory-record",
    "audit",
    "dashboard",
    "album",
    "cowork",
}

# The identity surfaces, pinned verbatim from the two authored profiles'
# metadata (name / display_name / provenance / confidence — never risk_class).
REF_IDENTITY = {
    "name": "halee_ramone",
    "display_name": "Roy Halee / Phil Ramone",
    "provenance": "hand-curated-documented",
    "confidence": "high",
}
TIM_IDENTITY = {
    "name": "timbaland",
    "display_name": "Timbaland",
    "provenance": "hand-curated-documented",
    "confidence": "high",
}

REF_VERDICT_LINE = "**Producer profile:** Roy Halee / Phil Ramone (halee_ramone)"
TIM_VERDICT_LINE = "**Producer profile:** Timbaland (timbaland)"

# The known differential on the demo fixture (the P-035 pins: each overall is
# its own profile's weighted mean — see tests/test_vocal_chop_groove.py).
DEMO_OVERALLS = {"halee_ramone": 76.3, "timbaland": 60.9}

_DEMO_STEMS = str(ROOT / "fixtures" / VOCAL_CHOP_FIXTURE / "stems")
_DEMO_MANIFEST = str(ROOT / "fixtures" / VOCAL_CHOP_FIXTURE / "project_manifest.json")

_SIMPLE_STEMS = str(ROOT / "fixtures" / "simple_vocal_piano_song" / "stems")
_SIMPLE_MANIFEST = str(
    ROOT / "fixtures" / "simple_vocal_piano_song" / "project_manifest.json"
)


def _subcommands():
    parser = cli.build_parser()
    sub = next(
        a for a in parser._actions if isinstance(a, argparse._SubParsersAction)
    )
    return sub.choices


def _producer_action(sp):
    return next(
        (a for a in sp._actions if "--producer" in a.option_strings), None
    )


# =========================================================================== #
# 1. THE EXACT COMMAND SET — the shared argument, the semantics-only help.
# =========================================================================== #
def test_producer_flag_on_exactly_the_analyze_family_commands():
    """``--producer`` exists on EXACTLY the analyze-family commands, with the
    reference profile as the default on every carrier."""
    carriers = set()
    for name, sp in _subcommands().items():
        action = _producer_action(sp)
        if action is not None:
            carriers.add(name)
            assert action.default == "halee_ramone", name
    assert carriers == PRODUCER_COMMANDS


def test_producer_help_names_the_semantics_not_a_profile_list():
    """The P-038 ``--mode`` precedent: the help text describes what the value
    IS (a profile name resolved from the local producers directory), never a
    hardcoded list of available profiles."""
    for name in PRODUCER_COMMANDS:
        action = _producer_action(_subcommands()[name])
        assert action.help, name
        assert "timbaland" not in action.help.lower(), name


# =========================================================================== #
# 1b. THE PER-CARRIER THREADING GUARD (P-039 review fix) — the resolved
# producer provably REACHES the analysis on EVERY carrier.
# =========================================================================== #
def _carrier_argv(command, tmp_path):
    """The argv that drives one carrier end-to-end through ``cli.main`` with
    ``--producer timbaland`` (writing surfaces routed into tmp_path)."""
    io = ["--stems", _SIMPLE_STEMS, "--manifest", _SIMPLE_MANIFEST]
    tim = ["--producer", "timbaland"]
    if command == "album":
        projects = tmp_path / "projects"
        (projects / "song_a").mkdir(parents=True)
        shutil.copy(_SIMPLE_MANIFEST, projects / "song_a" / "project_manifest.json")
        return ["album", "--projects", str(projects), *tim]
    if command == "cowork":
        return ["cowork", "--name", "intake_project", *io, *tim]
    if command == "memory-record":
        return ["memory-record", *io, "--memory-dir", str(tmp_path / "mem"),
                "--name", "pass_1", *tim]
    if command == "dashboard":
        return ["dashboard", *io, "--out", str(tmp_path / "dash.html"), *tim]
    if command in ("status", "mixer-feedback"):
        return [command, *io, *tim]
    # analyze / detect-identities / analyze-sections / generate-plan /
    # creative / governance / audit — these write artifacts: keep --out in tmp.
    return [command, *io, "--out", str(tmp_path / "out"), *tim]


@pytest.mark.parametrize("command", sorted(PRODUCER_COMMANDS))
def test_resolved_producer_reaches_every_carriers_analysis(
    command, analyzed, tmp_path, monkeypatch, capsys
):
    """THE SILENT-IGNORE GUARD (the P-039 review fix): flag PRESENCE alone
    cannot catch a handler that accepts ``--producer`` and then drops it —
    the reviewer demonstrated exactly that sabotage (the ``producer=``
    threading removed from ``_run_governance``'s ``analyze()`` call) shipping
    green through the whole suite. This test closes it for EVERY carrier: a
    spy on the ``producer`` kwarg arriving at the handler's analysis entry
    point (``cli.analyze`` for the direct carriers; ``cowork.analyze`` behind
    ``build_context`` for the cowork carrier) records what each handler
    ACTUALLY passed, and every recorded value must be the RESOLVED timbaland
    ``ProducerProfile``. Album is asserted for BOTH of its per-song passes
    (exactly 2 recorded calls — pass 1 album-context-free, pass 2
    album-aware); every other carrier records exactly 1.

    The spy short-circuits the real analysis by returning a canned, fully
    real ``ProjectAnalysis`` (the session ``analyzed`` fixture) so all 13
    handlers still run their complete downstream surface logic at near-zero
    cost — honestly a stand-in: the REAL end-to-end differential stays
    proven by the demo / status / cowork tests in this file.

    Sabotage-verified both ways before landing: with the ``producer=``
    threading dropped from ``_run_governance``'s ``analyze()`` call (the
    reviewer's exact cut) the governance case FAILS here (the spy sees no
    producer kwarg); with the ``producer=producer`` threading dropped from
    album's PASS-2 call the album case FAILS here; at HEAD all 13 pass."""
    canned = analyzed["simple_vocal_piano_song"]
    seen = []

    def spy(*args, **kwargs):
        seen.append(kwargs.get("producer"))
        return canned

    monkeypatch.setattr(cli, "analyze", spy)
    monkeypatch.setattr(cowork_module, "analyze", spy)

    rc = cli.main(_carrier_argv(command, tmp_path))
    capsys.readouterr()  # drain the handler's printed surface
    assert rc == 0

    expected_calls = 2 if command == "album" else 1
    assert len(seen) == expected_calls, (command, seen)
    for producer in seen:
        assert isinstance(producer, ProducerProfile), command
        assert producer.metadata["name"] == "timbaland", command


# =========================================================================== #
# 2. THE DEMO, END-TO-END — same stems, two trees, the real CLI entry.
# =========================================================================== #
@pytest.fixture(scope="module")
def demo_trees(_ensure_fixtures, tmp_path_factory):
    """The packet's demo invocation, via the REAL CLI entry (``cli.main``
    with argv — the same function the ``logic-mix-os`` console script calls):
    the same stems analyzed without and with ``--producer timbaland``, plus a
    no-arg LIBRARY run for the byte-identity half."""
    base = tmp_path_factory.mktemp("p039_demo")
    out_ref, out_tim, out_lib = base / "out_ref", base / "out_tim", base / "out_lib"

    common = ["--stems", _DEMO_STEMS, "--manifest", _DEMO_MANIFEST]
    assert cli.main(["analyze", *common, "--out", str(out_ref)]) == 0
    assert cli.main(
        ["analyze", *common, "--out", str(out_tim), "--producer", "timbaland"]
    ) == 0

    result = analyze(_DEMO_STEMS, load_manifest(_DEMO_MANIFEST))
    write_artifacts(result, out_lib)
    return {"ref": out_ref, "tim": out_tim, "lib": out_lib}


def test_demo_both_trees_are_valid(demo_trees):
    """Same stems, two coherent artifact trees — both pass the full output
    validation. Timbaland reachable without code changes."""
    for key in ("ref", "tim"):
        report = validate_output(demo_trees[key])
        assert report["ok"], (key, report["errors"])


def test_demo_each_tree_names_its_producer(demo_trees):
    """Clear selected producer in artifacts: the machine-readable identity in
    doctrine_score.json AND the human-readable verdict line near the top of
    mix_verdict.md, each tree carrying ITS OWN producer and never the
    other's."""
    for key, identity, line, other_line in (
        ("ref", REF_IDENTITY, REF_VERDICT_LINE, TIM_VERDICT_LINE),
        ("tim", TIM_IDENTITY, TIM_VERDICT_LINE, REF_VERDICT_LINE),
    ):
        ds = json.loads(
            (demo_trees[key] / "doctrine_score.json").read_text(encoding="utf-8")
        )
        assert ds["producer"] == identity, key
        md = (demo_trees[key] / "mix_verdict.md").read_text(encoding="utf-8")
        assert md.splitlines()[2] == line, key  # near the top: title, blank, line
        assert other_line not in md, key


def test_demo_the_known_differential(demo_trees):
    """Same stems, two judgments: the pinned vocal_chop_groove overalls
    (76.3 vs 60.9 — the P-035 differential) reach the CLI-written trees."""
    for key, producer in (("ref", "halee_ramone"), ("tim", "timbaland")):
        ds = json.loads(
            (demo_trees[key] / "doctrine_score.json").read_text(encoding="utf-8")
        )
        assert ds["overall_mix_readiness_score"] == DEMO_OVERALLS[producer], key


def test_demo_default_cli_run_byte_matches_the_library_run(demo_trees):
    """Halee/Ramone remains default: the no-flag CLI tree is byte-for-byte
    the no-arg library tree — same file set, every file byte-identical."""
    ref, lib = demo_trees["ref"], demo_trees["lib"]
    ref_files = sorted(p.name for p in ref.iterdir())
    lib_files = sorted(p.name for p in lib.iterdir())
    assert ref_files == lib_files
    for name in ref_files:
        assert (ref / name).read_bytes() == (lib / name).read_bytes(), name


def test_demo_safety_kill_switches_lead_both_trees(demo_trees):
    """Safety/governance unchanged: in BOTH demo trees the composed
    kill-switch list leads with the five hardcoded SAFETY switches, verbatim,
    in order (the P-032i pin re-asserted at the CLI-artifact level)."""
    for key in ("ref", "tim"):
        gov = json.loads(
            (demo_trees[key] / "governance.json").read_text(encoding="utf-8")
        )
        assert gov["kill_switches"][:5] == SAFETY_KILL_SWITCHES, key


# =========================================================================== #
# 3. FRIENDLY ERROR — unknown name, available profiles named, no traceback.
# =========================================================================== #
def test_unknown_producer_friendly_error_at_the_process_boundary(tmp_path):
    """The real process boundary: an unknown producer exits non-zero with a
    friendly one-line error naming the available profiles (scanned from the
    producers directory) — NO traceback, and nothing written."""
    out = tmp_path / "out"
    # P-041 conscious delta: the unknown name used to be "quincy_jones" —
    # that profile now EXISTS (the third producer), so the probe name moved
    # to one that stays unknown, and the listing assertion gained the newly
    # discovered profile (dynamic discovery, proven at the process boundary).
    proc = subprocess.run(
        [
            sys.executable, "-m", "logic_mix_os.cli", "analyze",
            "--stems", _DEMO_STEMS, "--manifest", _DEMO_MANIFEST,
            "--out", str(out), "--producer", "nonexistent_producer",
        ],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr
    assert "Traceback" not in proc.stdout
    assert "nonexistent_producer" in proc.stderr
    # The available profiles are LISTED (scanned, not hardcoded) — every
    # authored profile appears without pinning the directory's full future.
    assert "halee_ramone" in proc.stderr
    assert "timbaland" in proc.stderr
    assert "quincy_jones" in proc.stderr
    assert not out.exists()


def test_unknown_producer_in_process_exits_nonzero(capsys):
    """The same friendly error in-process (the shared ``_resolve_producer``
    path every carrier threads through), before any analysis runs."""
    with pytest.raises(SystemExit) as exc:
        cli.main(
            ["status", "--stems", _SIMPLE_STEMS, "--manifest", _SIMPLE_MANIFEST,
             "--producer", "nope"]
        )
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "nope" in err
    assert "halee_ramone" in err and "timbaland" in err


# =========================================================================== #
# 4. THE IDENTITY SURFACE — per-call, fresh, data-driven, sabotage-proof.
# =========================================================================== #
def test_default_doctrine_score_names_the_reference(analyzed):
    """The default path carries the reference identity on every fixture —
    machine-readable, the four identity fields only (never risk_class)."""
    for name in FIXTURE_NAMES:
        producer = analyzed[name].doctrine_score["producer"]
        assert producer == REF_IDENTITY, name
        assert "risk_class" not in producer, name


def test_producer_identity_is_per_call_and_fresh():
    """The artifact copy is built per call from the PASSED profile's metadata:
    mutating it can never reach the profile (nor the module default)."""
    prof = load_profile("timbaland")
    ds = doctrine_engine.score_doctrine([], [], {"events": []}, None, profile=prof)
    assert ds["producer"] == TIM_IDENTITY
    assert ds["producer"] is not prof.metadata
    ds["producer"]["name"] = "mutated"
    assert prof.metadata["name"] == "timbaland"
    assert doctrine_engine._DEFAULT_PROFILE.metadata["name"] == "halee_ramone"


def test_rendering_liveness_a_passed_profiles_identity_renders(tmp_path):
    """P-029 threading, load-bearing (the P-031 sabotage catch): a synthetic
    profile with a DIFFERENT identity, driven through the REAL ``analyze()``
    path and ``write_artifacts``, names ITSELF on every surface — and never
    the module default. Sourcing any surface from ``_DEFAULT_PROFILE`` (or
    hardcoding the line) fails here while byte-identity stays green."""
    ref = load_profile("halee_ramone")
    meta = dict(ref.metadata)
    meta["name"] = "synthetic_producer"
    meta["display_name"] = "Synthetic Producer"
    prof = dataclasses.replace(ref, metadata=meta)

    res = analyze(_SIMPLE_STEMS, load_manifest(_SIMPLE_MANIFEST), producer=prof)
    assert res.doctrine_score["producer"]["name"] == "synthetic_producer"

    write_artifacts(res, tmp_path)
    dsj = json.loads((tmp_path / "doctrine_score.json").read_text(encoding="utf-8"))
    assert dsj["producer"]["display_name"] == "Synthetic Producer"

    md = (tmp_path / "mix_verdict.md").read_text(encoding="utf-8")
    assert "**Producer profile:** Synthetic Producer (synthetic_producer)" in md
    assert "(halee_ramone)" not in md

    status = render_status(res)
    assert "Producer profile: Synthetic Producer (synthetic_producer)" in status
    html = render_dashboard(res)
    assert "Producer profile: Synthetic Producer (synthetic_producer)" in html


def test_status_and_dashboard_name_the_selected_producer(chop_groove_analyzed):
    """The status and dashboard surfaces name the producer where the verdict
    is summarized (the header), under BOTH producers — and never inside the
    SCORES block (the P-030 producer-agnostic LABEL contract holds)."""
    expected = {
        "halee_ramone": "Producer profile: Roy Halee / Phil Ramone (halee_ramone)",
        "timbaland": "Producer profile: Timbaland (timbaland)",
    }
    for producer, res in chop_groove_analyzed.items():
        status = render_status(res)
        assert expected[producer] in status, producer
        scores_block = status.split(" SCORES", 1)[1].split("\n\n", 1)[0]
        assert "Producer profile:" not in scores_block, producer

        html = render_dashboard(res)
        assert expected[producer] in html, producer
        score_card = html.split('id="scores"', 1)[1].split("</section>", 1)[0]
        assert "Producer profile:" not in score_card, producer


def test_status_cli_threads_the_producer(capsys):
    """The ``status`` command end-to-end: ``--producer timbaland`` reaches the
    rendered surface (identity line + timbaland's own overall)."""
    rc = cli.main(
        ["status", "--stems", _DEMO_STEMS, "--manifest", _DEMO_MANIFEST,
         "--producer", "timbaland"]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Producer profile: Timbaland (timbaland)" in out
    assert "60.9" in out


def test_producer_surfaces_are_data_driven(analyzed):
    """A doctrine_score WITHOUT the key (a pre-P-039 artifact) renders no
    producer line on any surface — data-driven, never hardcoded."""
    md = markdown_renderer.render_mix_verdict({}, {})
    assert "Producer profile" not in md

    res = analyzed["simple_vocal_piano_song"]
    clone = copy.copy(res)
    clone.doctrine_score = {
        k: v for k, v in res.doctrine_score.items() if k != "producer"
    }
    assert "Producer profile:" not in render_status(clone)
    assert "Producer profile:" not in render_dashboard(clone)


# =========================================================================== #
# 5. SCHEMA + GOLDEN BLINDNESS.
# =========================================================================== #
def test_schema_documents_the_additive_producer_key(analyzed):
    """The schema documents the additive key (four required identity fields
    inside it), never requires it at the top level (a pre-P-039 artifact
    still validates), and declares no additionalProperties conflict."""
    schema = load_schema("doctrine_score.schema.json")
    assert "additionalProperties" not in schema
    assert "producer" not in schema["required"]  # additive, never breaking
    prod = schema["properties"]["producer"]
    assert prod["required"] == ["name", "display_name", "provenance", "confidence"]
    for name in FIXTURE_NAMES:
        assert validate_instance(analyzed[name].doctrine_score, schema) == []


def test_build_snapshot_is_blind_to_the_producer_addition(analyzed):
    """What the golden pins — the categorical fingerprint + the original
    score keys — cannot see the identity surface: the live snapshot carries
    no producer vocabulary and still matches the stored golden with 0
    criticals (the corpus-level 93/93 is pinned by the existing regression
    tests)."""
    for name in FIXTURE_NAMES:
        snapshot = build_snapshot(analyzed[name])
        blob = json.dumps(snapshot, sort_keys=True)
        assert "display_name" not in blob
        assert "Producer profile" not in blob
        assert "halee_ramone" not in blob

        golden = json.loads(
            (ROOT / "fixtures" / name / "golden" / "snapshot.json").read_text(
                encoding="utf-8"
            )
        )
        tests_n, passed, critical, warnings = compare_snapshots(name, golden, snapshot)
        assert critical == []
        assert warnings == []
        assert passed == tests_n


# =========================================================================== #
# 6. THE COWORK RIDER — the producer threads through the shared context.
# =========================================================================== #
def test_cowork_context_default_is_the_reference():
    """``build_context`` without a producer stays the reference — the
    no-arg cowork path names halee_ramone and keeps its pinned overall."""
    ctx = build_context(stems=_SIMPLE_STEMS, manifest=load_manifest(_SIMPLE_MANIFEST))
    scores = run_command("score_mix", ctx)
    assert scores["producer"] == REF_IDENTITY
    assert scores["overall_mix_readiness_score"] == 73.8


def test_cowork_context_carries_the_selected_producer():
    """``build_context(producer="timbaland")`` drives the shared analysis
    with timbaland's judgment (identity + its own pinned overall)."""
    ctx = build_context(
        stems=_SIMPLE_STEMS, manifest=load_manifest(_SIMPLE_MANIFEST),
        producer="timbaland",
    )
    scores = run_command("score_mix", ctx)
    assert scores["producer"] == TIM_IDENTITY
    assert scores["overall_mix_readiness_score"] == 68.4


def test_cowork_cli_threads_the_producer(capsys):
    """The cowork CLI command end-to-end: ``--producer timbaland`` reaches
    the command surface's shared analysis."""
    rc = cli.main(
        ["cowork", "--name", "score_mix", "--stems", _SIMPLE_STEMS,
         "--manifest", _SIMPLE_MANIFEST, "--producer", "timbaland"]
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["producer"] == TIM_IDENTITY
    assert payload["overall_mix_readiness_score"] == 68.4
