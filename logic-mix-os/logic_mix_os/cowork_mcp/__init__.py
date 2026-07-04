"""P-051 — Cowork Registry MCP Adapter (read/plan surface first).

Two layers, ZERO new dependency (stdlib + numpy only):

* :mod:`logic_mix_os.cowork_mcp.adapter` — the pure-Python heart. It reads the
  Cowork registry's own self-describing contract
  (:func:`logic_mix_os.cowork.describe_contract`) and:
    - generates MCP tool definitions (name / description / inputSchema) DERIVED
      from that contract, so the schema can never silently diverge from the
      Cowork command signatures (the drift guard);
    - dispatches a tool call by building a Cowork context and routing ONLY into
      the Cowork ``COMMANDS`` registry — it can ASK the system what it
      recommends, it can never make Logic do it.

* :mod:`logic_mix_os.cowork_mcp.server` (added in the second commit) — a
  minimal, self-contained JSON-RPC 2.0 over newline-delimited stdio MCP server
  shell that exposes the adapter. ``python -m logic_mix_os.cowork_mcp`` serves.

THE SAFETY DOCTRINE (verbatim, the invariant line):

    MCP can ask the system what it recommends.
    MCP cannot make Logic do it.

    Logic actions remain checklist / plan artifacts.
    Execution stays human/Cowork-in-the-loop.

This adapter runs entirely in-process. It never shells out to any external
program, never drives a DAW, never writes a Logic session or an audio file. The
only files any tool can touch are the memory/history store under an EXPLICIT
``memory_dir`` — and only for the four commands the registry declares as
side-effecting, which are refused here unless that ``memory_dir`` is supplied.
"""

from __future__ import annotations

from .adapter import (
    CONTEXT_INPUTS,
    dispatch,
    tool_definitions,
)

__all__ = ["CONTEXT_INPUTS", "dispatch", "tool_definitions"]
