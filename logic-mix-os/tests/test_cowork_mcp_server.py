"""P-051 Commit-2 — the minimal stdio JSON-RPC MCP server shell.

proof 1 ("the MCP server starts") is proven deterministically WITHOUT a live
client: ``handle_message`` is a pure function driven with request dicts, and
``serve`` is driven with in-memory stdio streams (initialize -> initialized ->
tools/list -> tools/call), asserting the response objects in order.

The tool surface (proof 2) and the safety guarantees (proofs 8-14) are proven in
tests/test_cowork_mcp.py against the adapter the server wraps; this file proves
the transport faithfully carries them (a handled adapter error becomes
``isError: true`` on the wire, never a crash).
"""

from __future__ import annotations

import io
import json

from logic_mix_os import __version__
from logic_mix_os.cowork_mcp import adapter
from logic_mix_os.cowork_mcp.server import (
    METHOD_NOT_FOUND,
    PARSE_ERROR,
    PROTOCOL_VERSION,
    SERVER_NAME,
    handle_line,
    handle_message,
    serve,
)

from conftest import ROOT

STEMS = str(ROOT / "fixtures" / "dense_chorus_with_loops" / "stems")
MANIFEST = str(ROOT / "fixtures" / "dense_chorus_with_loops" / "project_manifest.json")


# =========================================================================== #
# proof 1 — the handshake.
# =========================================================================== #
def test_initialize_handshake():
    resp = handle_message({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                   "clientInfo": {"name": "test", "version": "0"}},
    })
    assert resp["jsonrpc"] == "2.0" and resp["id"] == 1
    result = resp["result"]
    assert result["protocolVersion"] == PROTOCOL_VERSION
    assert result["capabilities"] == {"tools": {}}
    assert result["serverInfo"] == {"name": SERVER_NAME, "version": __version__}


def test_initialized_notification_has_no_response():
    assert handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


# =========================================================================== #
# proof 2 (transport view) — tools/list carries the adapter's tool defs.
# =========================================================================== #
def test_tools_list_returns_the_adapter_tools():
    resp = handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = resp["result"]["tools"]
    assert tools == adapter.tool_definitions()
    assert [t["name"] for t in tools]  # non-empty, one per Cowork command


# =========================================================================== #
# proof 4 (transport view) — tools/call returns text content.
# =========================================================================== #
def test_tools_call_returns_text_content():
    resp = handle_message({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "detect_masking",
                   "arguments": {"stems": STEMS, "manifest": MANIFEST}},
    })
    result = resp["result"]
    assert result["isError"] is False
    content = result["content"]
    assert content[0]["type"] == "text"
    payload = json.loads(content[0]["text"])
    assert set(payload) == {"result", "artifacts"}
    assert payload["artifacts"] == []


def test_tools_call_handled_error_sets_iserror_not_a_crash():
    # missing stems -> the adapter returns a clean error; the transport must
    # carry it as isError:true, still a valid JSON-RPC RESULT (not an -32xxx).
    resp = handle_message({
        "jsonrpc": "2.0", "id": 4, "method": "tools/call",
        "params": {"name": "detect_masking", "arguments": {}},
    })
    assert "result" in resp and "error" not in resp   # transport did not crash
    assert resp["result"]["isError"] is True
    assert "stems" in json.loads(resp["result"]["content"][0]["text"])["error"]


def test_side_effecting_tool_over_transport_is_gated():
    resp = handle_message({
        "jsonrpc": "2.0", "id": 5, "method": "tools/call",
        "params": {"name": "record_mix_pass",
                   "arguments": {"stems": STEMS, "name": "p1"}},  # no memory_dir
    })
    assert resp["result"]["isError"] is True
    assert "memory_dir" in json.loads(resp["result"]["content"][0]["text"])["error"]


# =========================================================================== #
# JSON-RPC error core.
# =========================================================================== #
def test_unknown_method_is_method_not_found():
    resp = handle_message({"jsonrpc": "2.0", "id": 6, "method": "no/such/method"})
    assert resp["error"]["code"] == METHOD_NOT_FOUND


def test_unknown_notification_gets_no_response():
    assert handle_message({"jsonrpc": "2.0", "method": "no/such/notification"}) is None


def test_parse_error_on_malformed_line():
    resp = handle_line("{ this is not json ")
    assert resp["error"]["code"] == PARSE_ERROR
    assert resp["id"] is None


def test_invalid_params_on_tools_call_without_name():
    resp = handle_message({
        "jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"arguments": {}},
    })
    assert resp["error"]["code"] == -32602


# =========================================================================== #
# proof 1 — the full stdio read-loop, deterministically (server "starts").
# =========================================================================== #
def test_full_handshake_sequence_over_stdio():
    lines = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                    "clientInfo": {"name": "t", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},   # no response
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "suggest_next_pass",
                    "arguments": {"stems": STEMS, "manifest": MANIFEST}}},
    ]
    stdin = io.StringIO("".join(json.dumps(m) + "\n" for m in lines))
    stdout = io.StringIO()
    serve(stdin=stdin, stdout=stdout)

    responses = [json.loads(l) for l in stdout.getvalue().splitlines()]
    # exactly THREE responses (the notification produced none)
    assert [r["id"] for r in responses] == [1, 2, 3]
    assert responses[0]["result"]["serverInfo"]["name"] == SERVER_NAME
    assert responses[1]["result"]["tools"] == adapter.tool_definitions()
    assert responses[2]["result"]["isError"] is False


def test_blank_lines_and_notifications_produce_no_output():
    stdin = io.StringIO(
        "\n"
        + json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
        + "\n"
    )
    stdout = io.StringIO()
    serve(stdin=stdin, stdout=stdout)
    assert stdout.getvalue() == ""


def test_serve_response_is_one_json_object_per_line():
    stdin = io.StringIO(json.dumps({"jsonrpc": "2.0", "id": 9, "method": "tools/list"}) + "\n")
    stdout = io.StringIO()
    serve(stdin=stdin, stdout=stdout)
    out = stdout.getvalue()
    assert out.endswith("\n")
    assert len(out.splitlines()) == 1
    json.loads(out)  # a single, valid object
