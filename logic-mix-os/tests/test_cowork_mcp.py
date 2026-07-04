"""P-051 — Cowork Registry MCP Adapter: the pure-Python adapter proof suite.

This suite is the binding proof for the ADAPTER layer (no server, no MCP SDK,
no network, no subprocess). Every proof/attack that is testable without a live
server lives here, mapped explicitly:

  proof 2  -> test_tool_list_is_generated_from_describe_contract
  proof 3  -> test_tool_params_match_cowork_signatures
  proof 4  -> test_read_planning_command_works_through_adapter
  proof 5  -> test_producer_selection_works_through_adapter
  proof 6  -> test_mode_selection_works_through_adapter
  proof 7  -> test_generated_artifacts_are_reported / test_write_command_reports_its_store
  proof 8  -> test_side_effecting_commands_are_marked_clearly
  proof 9  -> test_side_effecting_commands_require_explicit_memory_dir
  proof 10 -> test_no_daw_or_logic_execution_path_exists (token + routing scan)
  proof 11 -> test_no_daw_or_logic_execution_path_exists (osascript)
  proof 12 -> test_no_daw_or_logic_execution_path_exists (.logicx)
  proof 13 -> test_no_daw_or_logic_execution_path_exists (subprocess/exec)
  proof 14 -> test_source_stems_are_byte_unchanged_after_a_run
  proof 17 -> test_existing_cowork_registry_is_unchanged
  proof 18 -> test_drift_guard_* (schema reconstructed from the contract)

  attack 1 -> test_missing_stems_is_a_clean_error_nothing_run
  attack 2 -> test_side_effecting_without_memory_dir_writes_nothing
  attack 3 -> test_drift_guard_would_bite_a_stale_param / follows a live change
  attack 4 -> test_dispatch_reaches_only_the_registry
  attack 5 -> test_no_daw_or_logic_execution_path_exists
  attack 6 -> test_no_daw_or_logic_execution_path_exists (osascript/.logicx)
  attack 7 -> test_source_stems_are_byte_unchanged_after_a_run
  attack 8 -> test_unknown_producer_is_a_clean_error / test_unknown_mode_is_a_clean_error
  attack 9 -> test_no_command_is_mislabeled

The adapter's whole contract: it can ASK the system what it recommends; it can
never make Logic do it.
"""

from __future__ import annotations

import ast
import hashlib
import json
import pathlib

import pytest

from logic_mix_os import cowork
from logic_mix_os.cowork import COMMANDS, _SIDE_EFFECTS, run_command
from logic_mix_os.cowork_mcp import adapter
from logic_mix_os.cowork_mcp.adapter import CONTEXT_INPUTS, dispatch, tool_definitions

from conftest import ROOT

DENSE = "dense_chorus_with_loops"
_MCP_DIR = pathlib.Path(adapter.__file__).resolve().parent


# --------------------------------------------------------------------------- #
# Fixtures — real stems paths (the adapter takes PATHS, not analyses).
# --------------------------------------------------------------------------- #
@pytest.fixture()
def stems() -> str:
    return str(ROOT / "fixtures" / DENSE / "stems")


@pytest.fixture()
def manifest_path() -> str:
    return str(ROOT / "fixtures" / DENSE / "project_manifest.json")


@pytest.fixture()
def base_args(stems, manifest_path) -> dict:
    return {"stems": stems, "manifest": manifest_path}


def _contract_commands() -> dict:
    return run_command("describe_contract", {"result": None, "memory": None})["commands"]


# =========================================================================== #
# proof 2 — the tool list is generated from describe_contract().
# =========================================================================== #
def test_tool_list_is_generated_from_describe_contract():
    tools = tool_definitions()
    names = [t["name"] for t in tools]
    assert names == list(_contract_commands())          # exactly the contract, in order
    assert set(names) == set(COMMANDS)                   # exactly the registry
    for t in tools:                                      # shape of every def
        assert set(t) == {"name", "description", "inputSchema"}
        assert t["inputSchema"]["type"] == "object"
    json.dumps(tools)                                    # fully JSON-serializable


# =========================================================================== #
# proof 3 + proof 18 + attack 3 — the drift guard.
# The tool schema's per-command params are reconstructed from the contract at
# TEST time and asserted equal; a stale/hardcoded param fails loudly.
# =========================================================================== #
def test_tool_params_match_cowork_signatures():
    tools = {t["name"]: t for t in tool_definitions()}
    contract = _contract_commands()
    context = set(CONTEXT_INPUTS)
    for name, entry in contract.items():
        props = set(tools[name]["inputSchema"]["properties"])
        command_props = props - context
        expected = {p["name"] for p in entry["params"]}
        assert command_props == expected, name
        # every context input is always present on every tool
        assert context <= props, name
        # declared defaults flow through from the contract (no hand-drift)
        for p in entry["params"]:
            if "default" in p:
                assert tools[name]["inputSchema"]["properties"][p["name"]]["default"] \
                    == p["default"], (name, p["name"])


def test_drift_guard_would_bite_a_stale_param():
    """If a param were hardcoded stale, the equality guard above would fire.

    ``record_mix_pass`` really carries {name, reverted}. We show that any stale
    expectation (a param cowork does NOT have, or a missing one) is NOT what the
    adapter derives — so the guard is not vacuous.
    """
    tools = {t["name"]: t for t in tool_definitions()}
    props = set(tools["record_mix_pass"]["inputSchema"]["properties"]) - set(CONTEXT_INPUTS)
    assert props == {"name", "reverted"}                 # the live truth
    assert props != {"name", "reverted", "ghost_param"}  # a stale-add would differ
    assert props != {"name"}                             # a stale-drop would differ


def test_drift_guard_follows_a_live_signature_change(monkeypatch):
    """A signature change flows straight through — proving no hardcoded schema.

    We inject a synthetic command with brand-new params into the LIVE registry;
    the derived tool def must expose EXACTLY those params. A hand-written schema
    could not know about a command that did not exist when it was authored.
    """
    def _synthetic(ctx, alpha=1, beta=None, **k):
        return {"ok": True}

    monkeypatch.setitem(cowork.COMMANDS, "synthetic_probe",
                        {"desc": "probe", "fn": _synthetic})
    tools = {t["name"]: t for t in tool_definitions()}
    assert "synthetic_probe" in tools
    props = set(tools["synthetic_probe"]["inputSchema"]["properties"]) - set(CONTEXT_INPUTS)
    assert props == {"alpha", "beta"}
    assert tools["synthetic_probe"]["inputSchema"]["properties"]["alpha"]["default"] == 1


# =========================================================================== #
# proof 4 — a read/planning command works through the adapter.
# =========================================================================== #
def test_read_planning_command_works_through_adapter(base_args):
    out = dispatch("detect_masking", dict(base_args))
    assert set(out) == {"result", "artifacts"}
    assert out["artifacts"] == []                        # a read writes nothing
    # identical to calling the registry directly on the same analysis
    from logic_mix_os.pipeline import analyze
    from logic_mix_os.project import load_manifest
    direct = run_command(
        "detect_masking",
        {"result": analyze(base_args["stems"], load_manifest(base_args["manifest"])),
         "memory": None},
    )
    assert out["result"] == direct


def test_generate_mix_plan_works_and_is_jsonable(base_args):
    out = dispatch("generate_mix_plan", dict(base_args))
    assert "overall_diagnosis" in out["result"]
    json.dumps(out)


# =========================================================================== #
# proof 5 + attack 8 — producer selection (and its clean-error boundary).
# =========================================================================== #
def test_producer_selection_works_through_adapter(base_args):
    halee = dispatch("score_mix", {**base_args, "producer": "halee_ramone"})
    timba = dispatch("score_mix", {**base_args, "producer": "timbaland"})
    assert "error" not in halee and "error" not in timba
    # a producer-attributable difference — the producer really threads through
    assert json.dumps(halee["result"]) != json.dumps(timba["result"])


def test_unknown_producer_is_a_clean_error(base_args):
    out = dispatch("score_mix", {**base_args, "producer": "not_a_producer"})
    assert "error" in out and "result" not in out
    assert "not_a_producer" in out["error"]
    # the available profiles are scanned from the directory, never hardcoded
    assert "halee_ramone" in out["error"] and "timbaland" in out["error"]


# =========================================================================== #
# proof 6 + attack 8 — mode selection (and its clean-error boundary).
# =========================================================================== #
def test_mode_selection_works_through_adapter(base_args):
    default = dispatch("run_creative_engine", dict(base_args))
    forked = dispatch("run_creative_engine", {**base_args, "mode": "deconstructive"})
    assert forked["result"]["search_mode"] == "deconstructive"
    # the creative surface genuinely reflects the mode (different candidate flow)
    assert json.dumps(default["result"]) != json.dumps(forked["result"])


def test_unknown_mode_is_a_clean_error(base_args):
    out = dispatch("run_creative_engine", {**base_args, "mode": "no_such_mode"})
    assert "error" in out and "result" not in out
    assert "no_such_mode" in out["error"]


# =========================================================================== #
# proof 8 + attack 9 — side effects marked clearly, nothing mislabeled.
# =========================================================================== #
def test_side_effecting_commands_are_marked_clearly():
    tools = {t["name"]: t for t in tool_definitions()}
    contract = _contract_commands()
    for name, entry in contract.items():
        desc = tools[name]["description"]
        assert entry["purpose"] in desc
        if entry["side_effect"] == "none":
            assert "read-only" in desc and "SIDE EFFECT" not in desc, name
        else:
            assert "SIDE EFFECT" in desc and "read-only" not in desc, name
            assert entry["side_effect"] in desc, name          # the exact label
            assert "memory" in desc.lower(), name              # the memory-only boundary


def test_no_command_is_mislabeled():
    """attack 9: the set of tools MARKED side-effecting is EXACTLY the registry's
    declared side-effecting set — derived, never hand-listed."""
    tools = {t["name"]: t for t in tool_definitions()}
    marked = {name for name, t in tools.items() if "SIDE EFFECT" in t["description"]}
    assert marked == set(_SIDE_EFFECTS)
    # and the four are exactly the documented four
    assert marked == {"record_mix_pass", "update_taste_calibration",
                      "write_mix_decision", "override_track_identity"}


def test_side_effecting_tools_require_memory_dir_in_schema():
    tools = {t["name"]: t for t in tool_definitions()}
    for name, t in tools.items():
        required = set(t["inputSchema"]["required"])
        assert "stems" in required
        if name in _SIDE_EFFECTS:
            assert "memory_dir" in required, name
        else:
            assert "memory_dir" not in required, name


# =========================================================================== #
# proof 9 + attack 2 — side-effecting commands require an explicit memory_dir;
# without it: clean error, ZERO writes, nothing analysed.
# =========================================================================== #
@pytest.mark.parametrize("name", sorted(_SIDE_EFFECTS))
def test_side_effecting_commands_require_explicit_memory_dir(name, base_args):
    out = dispatch(name, {**base_args, "name": "p1", "identity": "organ",
                          "track_id": "t0", "decision": {"d": "x"}, "label": "too wide"})
    assert "error" in out and "result" not in out
    assert "memory_dir" in out["error"]


def test_side_effecting_without_memory_dir_writes_nothing(base_args, tmp_path, monkeypatch):
    """attack 2: refused BEFORE any analysis or memory object is built — so the
    refusal cannot have written or even analysed anything."""
    intended = tmp_path / "mem"

    # a tripwire: if the gate let control reach analyze(), this would raise
    def _boom(*a, **k):
        raise AssertionError("analyze() must not run when the memory_dir gate fires")

    monkeypatch.setattr(adapter, "analyze", _boom)
    out = dispatch("record_mix_pass", {**base_args, "name": "p1"})
    assert "error" in out
    assert not intended.exists()                         # the store was never created
    assert list(tmp_path.iterdir()) == []                # nothing written anywhere


def test_write_command_reports_its_store(base_args, tmp_path):
    """proof 7 + proof 9: WITH an explicit memory_dir a memory write succeeds and
    its generated artifact path is reported and reachable."""
    mem = tmp_path / "mem"
    out = dispatch("record_mix_pass", {**base_args, "memory_dir": str(mem), "name": "p1"})
    assert "result" in out
    assert out["artifacts"], "the written history file must be surfaced"
    history = mem / "mix_pass_history.json"
    assert str(history) in out["artifacts"]
    assert history.exists()
    json.loads(history.read_text())                      # a real, readable artifact


def test_generated_artifacts_are_reported(base_args, tmp_path):
    """proof 7: taste + ledger writers each surface their own store file, and a
    session-only mutation (override) surfaces NO file artifact (honest)."""
    mem = tmp_path / "mem"
    taste = dispatch("update_taste_calibration",
                     {**base_args, "memory_dir": str(mem), "label": "too wide"})
    assert str(mem / "taste_profile.json") in taste["artifacts"]

    ledger = dispatch("write_mix_decision",
                      {**base_args, "memory_dir": str(mem),
                       "decision": {"decision": "widen", "reason": "narrow"}})
    assert str(mem / "decision_ledger.json") in ledger["artifacts"]

    tid = dispatch("detect_track_identities", dict(base_args))["result"][0]["track_id"]
    override = dispatch("override_track_identity",
                        {**base_args, "memory_dir": str(mem),
                         "track_id": tid, "identity": "organ"})
    assert override["result"]["updated"]["instrument_identity"] == "organ"
    assert override["artifacts"] == []                   # mutates:session — no disk write


# =========================================================================== #
# attack 1 — a tool without a stems path: clean error, nothing run.
# =========================================================================== #
def test_missing_stems_is_a_clean_error_nothing_run(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("analyze() must not run without stems")

    monkeypatch.setattr(adapter, "analyze", _boom)
    out = dispatch("detect_masking", {})
    assert "error" in out and "result" not in out
    assert "stems" in out["error"]


# =========================================================================== #
# attack 4 — dispatch reaches ONLY the cowork registry.
# =========================================================================== #
def test_dispatch_reaches_only_the_registry(base_args, monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("an unknown tool must not build a context or analyse")

    monkeypatch.setattr(adapter, "analyze", _boom)
    out = dispatch("__import__", dict(base_args))         # not a registry command
    assert "error" in out and "result" not in out
    out2 = dispatch("os.system", dict(base_args))
    assert "error" in out2 and "result" not in out2
    out3 = dispatch("does_not_exist", dict(base_args))
    assert "error" in out3


def test_dispatch_source_routes_only_via_run_command():
    """AST/source posture: the adapter's routing is the single ``run_command``
    entry point — no dynamic attribute routing that could reach an arbitrary
    callable."""
    src = (_MCP_DIR / "adapter.py").read_text()
    assert "run_command(" in src
    tree = ast.parse(src)
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "getattr" not in called                       # no dynamic dispatch
    assert "run_command" in called


# =========================================================================== #
# proofs 10-13 + attacks 5,6 — NO DAW/Logic execution surface anywhere.
# The house safety-grep, as a source scan over the whole new module.
# =========================================================================== #
FORBIDDEN_TOKENS = (
    "osascript", ".logicx", ".applescript",              # DAW / Logic execution
    "subprocess", "popen", "os.system", "os.exec", "pty.spawn",  # shelling out
    "eval(", "exec(", "__import__", "compile(",           # dynamic execution
    ".wav", ".aif",                                       # audio-write paths
)


def _forbidden_hits(text: str):
    low = text.lower()
    return [tok for tok in FORBIDDEN_TOKENS if tok in low]


@pytest.mark.parametrize("path", sorted(_MCP_DIR.glob("*.py")), ids=lambda p: p.name)
def test_no_daw_or_logic_execution_path_exists(path):
    assert _forbidden_hits(path.read_text()) == [], path.name


def test_the_safety_scan_would_bite_an_injected_execution_line():
    """The scan is not vacuous: an injected osascript / subprocess line is caught."""
    malicious = "import subprocess\nsubprocess.Popen(['osascript', 'x.applescript'])\n"
    hits = _forbidden_hits(malicious)
    assert "subprocess" in hits and "popen" in hits
    assert "osascript" in hits and ".applescript" in hits
    # the real modules, by contrast, are clean
    for path in _MCP_DIR.glob("*.py"):
        assert _forbidden_hits(path.read_text()) == [], path.name


# =========================================================================== #
# proof 14 + attack 7 — source stems are byte-unchanged after any run.
# =========================================================================== #
def _hash_tree(root: pathlib.Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def test_source_stems_are_byte_unchanged_after_a_run(base_args, tmp_path):
    root = pathlib.Path(base_args["stems"])
    before = _hash_tree(root)
    # run a read, a plan, and a memory write — none may touch the stems
    dispatch("detect_masking", dict(base_args))
    dispatch("generate_mix_plan", dict(base_args))
    dispatch("record_mix_pass",
             {**base_args, "memory_dir": str(tmp_path / "mem"), "name": "p1"})
    after = _hash_tree(root)
    assert before == after and before                    # non-empty and identical


# =========================================================================== #
# Determinism — same inputs, same JSON out.
# =========================================================================== #
def test_dispatch_is_deterministic(base_args):
    a = dispatch("suggest_next_pass", dict(base_args))
    b = dispatch("suggest_next_pass", dict(base_args))
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# =========================================================================== #
# proof 17 — the existing Cowork registry is unchanged by the adapter.
# =========================================================================== #
def test_existing_cowork_registry_is_unchanged():
    assert len(COMMANDS) == 35                            # no command added/removed
    # the contract is still pure/deterministic and drives the whole surface
    c1 = run_command("describe_contract", {"result": None, "memory": None})
    c2 = run_command("describe_contract", {"result": None, "memory": None})
    assert json.dumps(c1, sort_keys=True) == json.dumps(c2, sort_keys=True)
