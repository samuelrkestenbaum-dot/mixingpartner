"""A minimal, self-contained JSON-RPC 2.0 over stdio MCP server shell (P-051).

ZERO new dependency: stdlib ``json`` + ``sys`` only. This is the thin transport
around :mod:`logic_mix_os.cowork_mcp.adapter`. It implements the stable core of
the MCP protocol over newline-delimited stdio:

    * one JSON-RPC 2.0 object per line on stdin; one response object per line on
      stdout, flushed per message;
    * ``initialize``               -> protocolVersion + tools capability + serverInfo;
    * ``notifications/initialized`` -> a notification (no response);
    * ``tools/list``               -> the adapter's tool definitions;
    * ``tools/call``               -> ``{content:[{type:"text", text: <json>}], isError}``;
      a HANDLED adapter error is returned as ``isError: true`` (never a crash);
    * unknown method -> -32601; parse error -> -32700; invalid params -> -32602.

The read-loop is deliberately split so it is UNIT-TESTABLE without real stdio:
``handle_message(dict)`` is a pure function the loop calls. Tests feed
``initialize`` -> ``tools/list`` -> ``tools/call`` dicts and assert the
responses, so "the MCP server starts" is proven deterministically.

An SDK-based transport is a trivial future swap and OUT OF SCOPE here. This
server never drives a DAW, never writes a Logic session or an audio file, and
carries no execution backend — it exposes exactly the adapter's read/plan
surface and its explicitly-gated memory writes.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional

from .. import __version__
from .adapter import dispatch, tool_definitions

# A recent, pinned MCP protocol version reported at the handshake. Kept as a
# documented constant so the surface is deterministic and explicit.
PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "logic-mix-os-cowork"

# JSON-RPC 2.0 error codes (the stable core).
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602


def _result(msg_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def _error(msg_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _initialize_result() -> Dict[str, Any]:
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": __version__},
    }


def handle_message(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handle one parsed JSON-RPC message; return a response dict, or ``None``.

    Pure and side-effect-free at the transport layer (the only effects are the
    adapter's own gated ones). Notifications (no ``id``) never get a response.
    """
    method = message.get("method")
    msg_id = message.get("id")
    is_notification = "id" not in message

    if method == "initialize":
        return _result(msg_id, _initialize_result())

    if method == "notifications/initialized":
        return None  # a notification: acknowledged by doing nothing, no response

    if method == "tools/list":
        return _result(msg_id, {"tools": tool_definitions()})

    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(name, str) or not name:
            return _error(msg_id, INVALID_PARAMS, "Invalid params: 'name' is required")
        outcome = dispatch(name, arguments)
        is_error = isinstance(outcome, dict) and "error" in outcome
        return _result(
            msg_id,
            {"content": [{"type": "text", "text": json.dumps(outcome)}],
             "isError": is_error},
        )

    # Any other method.
    if is_notification:
        return None  # never respond to a notification
    if not method:
        return _error(msg_id, INVALID_REQUEST, "Invalid Request: missing method")
    return _error(msg_id, METHOD_NOT_FOUND, "Method not found")


def handle_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse one stdin line and handle it; a malformed line -> a -32700 error."""
    try:
        message = json.loads(line)
    except ValueError:
        return _error(None, PARSE_ERROR, "Parse error")
    if not isinstance(message, dict):
        return _error(None, INVALID_REQUEST, "Invalid Request")
    return handle_message(message)


def serve(stdin=None, stdout=None) -> None:
    """Run the stdio read-loop: one JSON-RPC object per line, responses flushed.

    Thin by design — all logic lives in :func:`handle_message`. ``stdin``/
    ``stdout`` are injectable so the loop can be driven from in-memory streams in
    a test.
    """
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    for raw in stdin:
        line = raw.strip()
        if not line:
            continue
        response = handle_line(line)
        if response is not None:
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()
