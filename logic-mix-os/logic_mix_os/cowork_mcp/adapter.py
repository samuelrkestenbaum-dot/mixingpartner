"""The pure-Python Cowork -> MCP adapter (P-051).

This module is the numpy-only, dependency-free heart of the MCP surface. It
holds NO server and NO network, and never shells out: it turns the existing
Cowork registry into MCP tool definitions and dispatches a tool call into that
registry. Every one of the packet's 18 proofs and 9 attacks is exercised by
``tests/test_cowork_mcp.py`` against this module alone — no server process and
no MCP SDK required.

Design (the drift-proof chain the user asked for):

    cowork.describe_contract()          # signatures -> a machine-readable contract
        -> tool_definitions()           # contract -> MCP {name, description, inputSchema}
        -> dispatch(name, arguments)    # validate -> analyze() -> build_context()
                                        #   -> run_command(name, ctx, **params)

Because the tool schemas are DERIVED from ``describe_contract()`` (whose
``params`` are themselves derived from the real handler signatures via
``inspect.signature``), a change to a Cowork command's signature flows straight
through to the MCP schema — or is caught loudly by the drift guard test. No
per-command schema is ever hand-written here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from ..cowork import (
    COMMANDS,
    _SIDE_EFFECTS,
    build_context,
    run_command,
)
from ..doctrine.producer_profile import _PRODUCERS_DIR, load_profile
from ..pipeline import analyze
from ..project import load_manifest

# The context inputs the adapter threads around every command's own params. They
# are NOT Cowork command params — they parameterise the shared analysis the
# command reads. Kept as an explicit, testable set so the drift guard can prove
# the per-command param surface equals the contract with these subtracted.
CONTEXT_INPUTS = ("stems", "manifest", "memory_dir", "producer", "mode")

_DEFAULT_PRODUCER = "halee_ramone"


# --------------------------------------------------------------------------- #
# Contract access — the single source of truth for the whole surface.
# --------------------------------------------------------------------------- #
def _bare_ctx() -> Dict[str, None]:
    """``describe_contract`` is pure and ignores the ctx, so a bare one suffices."""
    return {"result": None, "memory": None}


def _contract() -> Dict[str, Any]:
    return run_command("describe_contract", _bare_ctx())


def _json_type(value: Any) -> Optional[str]:
    """Best-effort JSON-Schema type from a param's declared default value.

    ``bool`` is checked before ``int`` (a bool IS an int in Python). A default of
    ``None`` (or no default) yields ``None`` -> the property omits ``type`` and
    stays permissive, exactly as the contract leaves it.
    """
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    return None


def _context_properties() -> Dict[str, Dict[str, Any]]:
    """The shared context inputs, as JSON-Schema properties (same for every tool)."""
    return {
        "stems": {
            "type": "string",
            "description": "Filesystem path to the folder of exported stems "
                           "(required; the analysis is built from these).",
        },
        "manifest": {
            "type": "string",
            "description": "Filesystem path to project_manifest.json (optional).",
        },
        "memory_dir": {
            "type": "string",
            "description": "Filesystem path to the project memory/history store. "
                           "REQUIRED for side-effecting tools; optional (history-"
                           "aware) for read/plan tools. Never a DAW/session path.",
        },
        "producer": {
            "type": "string",
            "description": "Producer profile name whose judgment drives the "
                           "analysis (resolved from the local producers directory).",
            "default": _DEFAULT_PRODUCER,
        },
        "mode": {
            "type": "string",
            "description": "Creative search mode from the selected producer "
                           "profile's search_modes (optional; default is the "
                           "profile's declared default mode).",
        },
    }


def _tool_description(entry: Dict[str, Any]) -> str:
    """Purpose plus an HONEST side-effect label derived from the contract.

    Read/plan commands are marked read-only; the four side-effecting commands
    carry their exact registry ``side_effect`` classification and the memory-only
    boundary. The label is DERIVED from the contract, never hand-listed, so a
    command cannot be mislabeled (attack 9).
    """
    purpose = entry["purpose"]
    side_effect = entry["side_effect"]
    if side_effect == "none":
        return f"{purpose} [read-only: plan/analysis surface, writes nothing]"
    return (
        f"{purpose} [SIDE EFFECT: {side_effect} — requires an explicit "
        f"memory_dir; writes ONLY to the memory/history store, never a "
        f"DAW/session/audio file]"
    )


def _input_schema(name: str, entry: Dict[str, Any]) -> Dict[str, Any]:
    """A JSON-Schema object: the shared context inputs + this command's params.

    The command params are read straight from the contract entry (whose names
    and defaults are derived from the real handler signature), so this schema
    cannot drift from the Cowork surface.
    """
    properties: Dict[str, Any] = _context_properties()
    for param in entry["params"]:
        prop: Dict[str, Any] = {"description": "Cowork command parameter."}
        if "default" in param:
            prop["default"] = param["default"]
            declared = _json_type(param["default"])
            if declared is not None:
                prop["type"] = declared
        properties[param["name"]] = prop

    required = ["stems"]
    if entry["side_effect"] != "none":
        required.append("memory_dir")
    return {"type": "object", "properties": properties, "required": required}


def tool_definitions() -> List[Dict[str, Any]]:
    """The MCP tool list, DERIVED from ``describe_contract()``.

    One tool per Cowork command: ``{name, description, inputSchema}``. Nothing is
    hand-written per command; a signature change in cowork.py flows through here
    automatically (and the drift guard test asserts exactly that).
    """
    contract = _contract()
    tools: List[Dict[str, Any]] = []
    for command_name, entry in contract["commands"].items():
        tools.append(
            {
                "name": command_name,
                "description": _tool_description(entry),
                "inputSchema": _input_schema(command_name, entry),
            }
        )
    return tools


# --------------------------------------------------------------------------- #
# Dispatch — validate, build context, route ONLY into the registry.
# --------------------------------------------------------------------------- #
def _error(message: str) -> Dict[str, str]:
    return {"error": message}


def _available_producers() -> str:
    return ", ".join(sorted(p.stem for p in _PRODUCERS_DIR.glob("*.json")))


def _json_snapshot(memory_dir: Optional[str]) -> Dict[str, Any]:
    """A snapshot of the memory store's JSON files: ``{path: (size, mtime_ns)}``.

    Used to report EXACTLY the artifacts a side-effecting command generated,
    without inventing an output directory: only the explicitly-supplied
    ``memory_dir`` is ever inspected, and only its ``*.json`` files.
    """
    if not memory_dir:
        return {}
    root = Path(memory_dir)
    if not root.exists():
        return {}
    snapshot: Dict[str, Any] = {}
    for path in root.glob("*.json"):
        if path.is_file():
            stat = path.stat()
            snapshot[str(path)] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def _new_or_changed(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    return sorted(p for p, sig in after.items() if before.get(p) != sig)


def dispatch(tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run one MCP tool call against the Cowork registry.

    Returns either ``{"error": <message>}`` (a handled, clean failure — nothing
    ran or wrote) or ``{"result": <json-able>, "artifacts": [<paths>]}``.

    Validation order is deliberate so a refused call NEVER touches analysis or
    disk:

      1. unknown tool  -> error (dispatch reaches ONLY the registry; attack 4).
      2. missing stems -> error, nothing run (attack 1).
      3. a side-effecting tool without an explicit memory_dir
                       -> error, ZERO writes (attack 2 / proofs 8, 9) — checked
                          BEFORE any analysis or memory object is constructed.
      4. unknown producer / unknown mode -> clean error (attack 8), not a crash.

    Only then is the shared analysis produced (threading BOTH producer and mode)
    and the command run. The four side-effecting commands may write ONLY to the
    memory store; no command can reach a DAW, a Logic session, or an audio file.
    """
    if tool_name not in COMMANDS:
        return _error(
            f"unknown tool {tool_name!r}: not a Cowork command. "
            f"Call tools/list to see the available commands."
        )

    args = dict(arguments or {})
    stems = args.pop("stems", None)
    manifest_path = args.pop("manifest", None)
    memory_dir = args.pop("memory_dir", None)
    producer = args.pop("producer", _DEFAULT_PRODUCER)
    mode = args.pop("mode", None)
    command_params = args  # whatever remains are the Cowork command's own params

    if not stems:
        return _error(
            f"tool {tool_name!r} requires a 'stems' path (the folder of exported "
            f"stems); nothing was run."
        )

    if tool_name in _SIDE_EFFECTS and not memory_dir:
        return _error(
            f"tool {tool_name!r} is side-effecting "
            f"({_SIDE_EFFECTS[tool_name]}) and requires an explicit 'memory_dir'; "
            f"refused — nothing was written."
        )

    try:
        profile = load_profile(producer)
    except FileNotFoundError:
        return _error(
            f"unknown producer {producer!r}. Available profiles: "
            f"{_available_producers()}."
        )

    if mode is not None and mode not in profile.search_modes:
        return _error(
            f"unknown mode {mode!r} for producer {producer!r}. Available modes: "
            f"{', '.join(sorted(profile.search_modes))}."
        )

    manifest = load_manifest(manifest_path) if manifest_path else {}

    # Produce the shared analysis with BOTH producer and mode threaded, then hand
    # the ready result to build_context (which, given a result, ignores producer
    # and simply wires the memory object) — no double analysis, no producer
    # conflict, and cowork.py stays byte-unchanged.
    result = analyze(
        stems,
        manifest,
        creative_mode=mode,
        producer=profile,
        memory_dir=memory_dir,
    )
    ctx = build_context(result=result, memory_dir=memory_dir)

    before = _json_snapshot(memory_dir)
    out = run_command(tool_name, ctx, **command_params)
    after = _json_snapshot(memory_dir)

    return {"result": out, "artifacts": _new_or_changed(before, after)}
