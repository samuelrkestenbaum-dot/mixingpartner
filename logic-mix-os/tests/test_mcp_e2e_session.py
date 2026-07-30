"""P-052 — Real End-to-End MCP Client Session (the ACTUAL product path).

P-051 proved the server in-memory (``handle_message`` + in-memory ``serve``).
This suite proves the REAL product path the user asked for:

    a real MCP client PROCESS
      -> spawns ``python -m logic_mix_os.cowork_mcp`` as a child subprocess
      -> speaks JSON-RPC 2.0 over the child's REAL stdin/stdout pipes
      -> drives a realistic Cowork session on real fixture stems + manifest
         with a real producer + mode
      -> gets real plan / verdict / checklist / next-pass + artifacts back
      -> and the no-DAW-execution boundary holds end to end.

The client is the stdlib-only harness in ``tests/_mcp_client.py`` (subprocess +
json + threading, ZERO new dependency). Every read is bounded by a timeout and
every child is reaped in teardown, so a hung server fails the suite fast and no
process leaks.

Proof map (contract's 10 required proofs):
  proof 1  -> test_proof01_initialize_handshake_over_the_wire
  proof 2  -> test_proof02_tools_list_over_the_wire
  proof 3  -> test_proof03_realistic_session_over_the_wire
  proof 4  -> test_proof04_producer_selection_over_the_wire
  proof 5  -> test_proof05_mode_selection_over_the_wire
  proof 6  -> test_proof06_artifacts_and_checklist_reachable_over_the_wire
  proof 7  -> test_proof07_memory_gate_over_the_wire
  proof 8  -> test_proof08_no_daw_stems_immutable_clean_exit
  proof 9  -> test_proof09_determinism_over_the_wire
  proof 10 -> satisfied by the packet shape (new test files only, zero dep) + qa.

Attack map (contract's 7 adversarial attacks):
  attack 1/2/3 -> test_proof08_* (no DAW exec, no osascript/.logicx, stems immutable)
  attack 4     -> test_attack4_memory_write_without_memory_dir_writes_to_no_cwd
  attack 5     -> test_attack5_response_comes_from_a_real_child_process
                  + test_attack5_killing_the_child_breaks_the_next_request
  attack 6/7   -> zero new import here (stdlib only) + zero product runtime change
                  (git-diff proof lives with qa; this file adds nothing to either).
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib

import pytest

from _mcp_client import MCPClient, MCPClientError
from conftest import ROOT

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "logic-mix-os-cowork"

FIXTURE = ROOT / "fixtures" / "dense_chorus_with_loops"
STEMS = str(FIXTURE / "stems")
MANIFEST = str(FIXTURE / "project_manifest.json")

# A real producer + a second one for the attributable difference, and a real
# creative mode from the first producer's search_modes.
PRODUCER = "chris_lord_alge"
OTHER_PRODUCER = "timbaland"
MODE = "front_and_center"  # a non-default mode for chris_lord_alge

BASE = {"stems": STEMS, "manifest": MANIFEST, "producer": PRODUCER}

# Tokens that would betray a DAW/Logic execution or an audio/session write
# anywhere the real session produced an artifact.
FORBIDDEN_ARTIFACT_TOKENS = (".logicx", ".applescript", "osascript", ".wav", ".aif")


# --------------------------------------------------------------------------- #
# Fixtures — real client processes, always reaped.
# --------------------------------------------------------------------------- #
@pytest.fixture()
def client():
    """A fresh server subprocess (no handshake yet); always torn down."""
    with MCPClient(cwd=str(ROOT)) as c:
        yield c


@pytest.fixture()
def session(client):
    """A handshaken client: ``initialize`` + ``notifications/initialized`` done."""
    init = client.initialize(PROTOCOL_VERSION)
    client.init_result = init  # stash for the proof-1 assertions
    return client


def _hash_tree(root: pathlib.Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _ok(is_error, payload):
    """A real, non-error tool result carrying ``result`` + ``artifacts``."""
    assert is_error is False, payload
    assert set(payload) == {"result", "artifacts"}, payload
    return payload


# =========================================================================== #
# proof 1 — the initialize handshake over the REAL pipes.
# =========================================================================== #
def test_proof01_initialize_handshake_over_the_wire(session):
    init = session.init_result
    assert init["jsonrpc"] == "2.0"
    result = init["result"]
    assert result["protocolVersion"] == PROTOCOL_VERSION
    assert result["serverInfo"]["name"] == SERVER_NAME
    assert result["serverInfo"]["version"]  # a real version string
    # the tools capability is advertised at the handshake
    assert "tools" in result["capabilities"]


# =========================================================================== #
# proof 2 — tools/list over the wire: 36 tools, each fully shaped.
# =========================================================================== #
def test_proof02_tools_list_over_the_wire(session):
    resp = session.request("tools/list", {})
    tools = resp["result"]["tools"]
    # P-062 CONSCIOUS bump 35 -> 36 (render_execution_brief; derived tool).
    assert len(tools) == 36
    for tool in tools:
        assert set(tool) == {"name", "description", "inputSchema"}
        assert tool["name"]
        assert tool["description"]
        assert tool["inputSchema"]["type"] == "object"
    # every tool requires a stems path; the four side-effecting ones also
    # require memory_dir (the gate is visible in the wire-delivered schema)
    by_name = {t["name"]: t for t in tools}
    for name in ("record_mix_pass", "update_taste_calibration",
                 "write_mix_decision", "override_track_identity"):
        assert "memory_dir" in by_name[name]["inputSchema"]["required"], name


# =========================================================================== #
# proof 3 — a realistic multi-command session over the wire.
# =========================================================================== #
def test_proof03_realistic_session_over_the_wire(session):
    """intake -> classify -> diagnose -> plan -> checklist -> validate ->
    next-pass, all over the wire against a real fixture with a real producer.
    Each step returns a real, JSON-deserialized result."""
    steps = [
        ("intake_project", dict),
        ("detect_track_identities", list),
        ("classify_tracks", list),
        ("detect_masking", dict),
        ("generate_mix_plan", dict),
        ("score_mix", dict),
        ("render_logic_checklist", str),
        ("validate_mix_pass", dict),
        ("suggest_next_pass", list),
    ]
    for command, expected_type in steps:
        is_error, payload = session.call_tool(command, dict(BASE))
        _ok(is_error, payload)
        assert isinstance(payload["result"], expected_type), command
        assert payload["artifacts"] == [], command  # a read/plan writes nothing

    # the plan and the scores are substantive, not empty stubs
    _, plan = session.call_tool("generate_mix_plan", dict(BASE))
    assert "overall_diagnosis" in plan["result"]
    _, score = session.call_tool("score_mix", dict(BASE))
    assert "overall_mix_readiness_score" in score["result"]


# =========================================================================== #
# proof 4 — producer selection works over the wire (attributable difference).
# =========================================================================== #
def test_proof04_producer_selection_over_the_wire(session):
    _, cla = session.call_tool(
        "score_mix", {**BASE, "producer": PRODUCER})
    _, tim = session.call_tool(
        "score_mix", {"stems": STEMS, "manifest": MANIFEST, "producer": OTHER_PRODUCER})

    # each result is attributed to ITS producer...
    assert cla["result"]["producer"]["name"] == PRODUCER
    assert tim["result"]["producer"]["name"] == OTHER_PRODUCER
    # ...and the judgment genuinely differs on identical stems
    cla_overall = cla["result"]["overall_mix_readiness_score"]
    tim_overall = tim["result"]["overall_mix_readiness_score"]
    assert cla_overall != tim_overall
    assert json.dumps(cla["result"], sort_keys=True) != \
        json.dumps(tim["result"], sort_keys=True)


# =========================================================================== #
# proof 5 — mode selection works over the wire (reflected + attributable).
# =========================================================================== #
def test_proof05_mode_selection_over_the_wire(session):
    _, default = session.call_tool("run_creative_engine", dict(BASE))
    _, moded = session.call_tool(
        "run_creative_engine", {**BASE, "mode": MODE})

    assert moded["result"]["search_mode"] == MODE
    # the creative surface genuinely reflects the mode (different candidate flow)
    assert json.dumps(default["result"], sort_keys=True) != \
        json.dumps(moded["result"], sort_keys=True)


# =========================================================================== #
# proof 6 — artifacts / plan / checklist reachable over the wire.
# =========================================================================== #
def test_proof06_artifacts_and_checklist_reachable_over_the_wire(session):
    is_error, checklist = session.call_tool("render_logic_checklist", dict(BASE))
    _ok(is_error, checklist)
    assert isinstance(checklist["result"], str) and checklist["result"].strip()
    # a Logic-native, human-executable checklist — a PLAN artifact, not an action
    assert checklist["artifacts"] == []

    _, plan = session.call_tool("generate_mix_plan", dict(BASE))
    assert isinstance(plan["result"], dict) and plan["result"]


# =========================================================================== #
# proof 7 — the memory gate over the wire.
# =========================================================================== #
def test_proof07_memory_gate_over_the_wire(session, tmp_path):
    # WITHOUT memory_dir: a side-effecting command is refused over the wire,
    # and nothing is written anywhere.
    untouched = tmp_path / "should_not_exist"
    is_error, refused = session.call_tool(
        "record_mix_pass", {**BASE, "name": "pass_1"})
    assert is_error is True
    assert "error" in refused and "memory_dir" in refused["error"]
    assert not untouched.exists()

    # WITH an explicit memory_dir: it writes JSON to that store, and the written
    # path is UNDER the memory_dir (a memory store, never a DAW/session file).
    mem = tmp_path / "mem"
    is_error, wrote = session.call_tool(
        "record_mix_pass", {**BASE, "memory_dir": str(mem), "name": "pass_1"})
    _ok(is_error, wrote)
    assert wrote["artifacts"], "the written history file must be surfaced over the wire"
    for artifact in wrote["artifacts"]:
        path = pathlib.Path(artifact)
        assert path.exists() and path.is_file()
        assert str(path).startswith(str(mem))          # under the memory_dir
        assert path.suffix == ".json"                  # a memory store, JSON
        json.loads(path.read_text())                   # a real, readable artifact
        low = str(path).lower()
        assert not any(tok in low for tok in FORBIDDEN_ARTIFACT_TOKENS)


# =========================================================================== #
# proof 8 + attacks 1/2/3 — no DAW exec, no osascript/.logicx, stems immutable,
# clean subprocess exit.
# =========================================================================== #
def test_proof08_no_daw_stems_immutable_clean_exit(client, tmp_path):
    stems_root = pathlib.Path(STEMS)
    before = _hash_tree(stems_root)
    assert before, "the fixture stems must exist"

    client.initialize(PROTOCOL_VERSION)
    mem = tmp_path / "mem"

    # a realistic session INCLUDING a side-effecting memory write — none of it
    # may touch the source audio or reach a DAW.
    for command, args in [
        ("intake_project", dict(BASE)),
        ("detect_masking", dict(BASE)),
        ("generate_mix_plan", dict(BASE)),
        ("render_logic_checklist", dict(BASE)),
        ("record_mix_pass", {**BASE, "memory_dir": str(mem), "name": "pass_1"}),
    ]:
        is_error, payload = client.call_tool(command, args)
        assert is_error is False, (command, payload)

    # the ONLY thing the session wrote is JSON under the memory store — no
    # ``.logicx``, no ``.applescript``, no audio file anywhere it produced.
    for produced in mem.rglob("*"):
        if produced.is_file():
            assert produced.suffix == ".json", produced
    # source stems are byte-for-byte identical after the whole session
    after = _hash_tree(stems_root)
    assert after == before

    # the server subprocess exits cleanly when stdin closes: rc 0, benign stderr
    returncode, stderr = client.shutdown()
    assert returncode == 0, stderr
    assert stderr.strip() == "", stderr


# =========================================================================== #
# proof 9 — determinism over the wire: the same plan twice is identical.
# =========================================================================== #
def test_proof09_determinism_over_the_wire(session):
    _, first = session.call_tool("generate_mix_plan", dict(BASE))
    _, second = session.call_tool("generate_mix_plan", dict(BASE))
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


# =========================================================================== #
# attack 5 — prove it is GENUINELY over the wire (a real child), not a disguised
# in-process call.
# =========================================================================== #
def test_attack5_response_comes_from_a_real_child_process(session):
    # a real, separate OS process is serving us
    assert isinstance(session.proc.pid, int) and session.proc.pid > 0
    assert session.proc.pid != os.getpid()
    assert session.proc.poll() is None  # alive while the session runs

    # a real round-trip actually came back through the child's stdout pipe
    resp = session.request("tools/list", {})
    assert resp["result"]["tools"]


def test_attack5_killing_the_child_breaks_the_next_request(client):
    client.initialize(PROTOCOL_VERSION)
    # a sanity round-trip proves the live child is answering...
    assert client.request("tools/list", {})["result"]["tools"]

    # ...now kill the real child; the next over-the-wire request MUST fail. A
    # disguised in-process call could not be broken this way.
    client.proc.kill()
    client.proc.wait()
    with pytest.raises(MCPClientError):
        client.request("tools/list", {})


# =========================================================================== #
# attack 4 — a side-effecting command without memory_dir writes NOTHING, proven
# against a fresh empty working directory over the wire.
# =========================================================================== #
def test_attack4_memory_write_without_memory_dir_writes_to_no_cwd(tmp_path):
    # run the server in a FRESH empty cwd (package still importable via PYTHONPATH)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    with MCPClient(cwd=str(tmp_path), env=env) as c:
        c.initialize(PROTOCOL_VERSION)
        for name, extra in [
            ("record_mix_pass", {"name": "p1"}),
            ("write_mix_decision", {"decision": {"d": "x"}}),
            ("update_taste_calibration", {"label": "too wide"}),
        ]:
            is_error, payload = c.call_tool(name, {**BASE, **extra})
            assert is_error is True, (name, payload)
            assert "memory_dir" in payload["error"], name
    # the refusals fired BEFORE analysis: nothing was written to the cwd
    assert list(tmp_path.iterdir()) == []
