"""``python -m logic_mix_os.cowork_mcp`` — serve the Cowork MCP surface over stdio.

Zero new dependency: this launches the stdlib-only JSON-RPC 2.0 stdio server in
:mod:`logic_mix_os.cowork_mcp.server`. MCP can ask the system what it
recommends; MCP cannot make Logic do it.
"""

from __future__ import annotations

from .server import serve


def main() -> None:
    serve()


if __name__ == "__main__":
    main()
