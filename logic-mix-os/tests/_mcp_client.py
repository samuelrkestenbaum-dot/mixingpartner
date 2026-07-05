"""A minimal, stdlib-only MCP client harness for the real end-to-end test (P-052).

ZERO new dependency: ``subprocess`` + ``json`` + ``threading`` + ``queue`` only.
This is a genuine over-the-wire client — it spawns
``python -m logic_mix_os.cowork_mcp`` as a real child process and speaks
JSON-RPC 2.0 over the child's REAL stdin/stdout pipes (one JSON object per line).
It is NOT the in-memory ``handle_message`` path (that is P-051's coverage).

Design (robust by construction, never hangs the suite):

  * ``subprocess.Popen([sys.executable, "-m", "logic_mix_os.cowork_mcp"], ...)``
    with ``stdin/stdout/stderr=PIPE, text=True`` — the product launch path.
  * two daemon PUMP threads drain the child's stdout (into a bounded queue) and
    stderr (into a list) so a read never deadlocks on a full OS pipe buffer and
    the reader can be given a BOUNDED timeout.
  * ``request(method, params, id)`` writes one JSON-RPC line + ``flush()`` and
    reads exactly one response line with a timeout; on timeout it FAILS LOUDLY
    and terminates the child (a hung server fails the test fast).
  * ``notify(method, params)`` writes a notification and reads nothing.
  * ``call_tool(name, arguments)`` is the ``tools/call`` convenience: it returns
    ``(is_error, parsed_result)`` where ``parsed_result`` is the JSON parsed from
    ``content[0].text``.
  * used as a context manager so a failing test never leaks a child process:
    ``__exit__`` always terminates/reaps the child and closes the pipes.

This client can ONLY drive the server's stdio surface; it carries no DAW, no
``osascript``, no ``.logicx`` — it asks the system what it recommends, it cannot
make Logic do anything.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
from typing import Any, Dict, Optional, Tuple

# The exact product launch command — a real Python subprocess speaking MCP.
SERVER_ARGV = [sys.executable, "-m", "logic_mix_os.cowork_mcp"]

# Sentinel pushed onto the stdout queue when the child's stdout hits EOF.
_EOF = object()


class MCPClientError(RuntimeError):
    """A transport-level failure: a timeout, a closed pipe, or a dead child."""


class MCPClient:
    """A real MCP client over a spawned ``cowork_mcp`` server subprocess."""

    def __init__(
        self,
        cwd: str,
        *,
        timeout: float = 30.0,
        env: Optional[Dict[str, str]] = None,
    ) -> None:
        self.timeout = timeout
        self._next_id = 0
        self.proc = subprocess.Popen(
            SERVER_ARGV,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # line-buffered writes (belt-and-suspenders; we also flush)
            cwd=str(cwd),
            env=dict(os.environ if env is None else env),
        )
        self._out_q: "queue.Queue[Any]" = queue.Queue()
        self._err_lines: list[str] = []
        self._out_thread = threading.Thread(
            target=self._pump_stdout, name="mcp-stdout", daemon=True
        )
        self._err_thread = threading.Thread(
            target=self._pump_stderr, name="mcp-stderr", daemon=True
        )
        self._out_thread.start()
        self._err_thread.start()

    # ---- pump threads ---------------------------------------------------- #
    def _pump_stdout(self) -> None:
        stream = self.proc.stdout
        assert stream is not None
        while True:
            line = stream.readline()
            if line == "":  # EOF
                self._out_q.put(_EOF)
                return
            self._out_q.put(line)

    def _pump_stderr(self) -> None:
        stream = self.proc.stderr
        assert stream is not None
        while True:
            line = stream.readline()
            if line == "":  # EOF
                return
            self._err_lines.append(line)

    # ---- low-level wire I/O ---------------------------------------------- #
    def _write(self, message: Dict[str, Any]) -> None:
        if self.proc.stdin is None or self.proc.stdin.closed:
            raise MCPClientError("stdin is closed; the child is not accepting input")
        try:
            self.proc.stdin.write(json.dumps(message) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, ValueError, OSError) as exc:
            raise MCPClientError(f"failed to write to the server: {exc!r}") from exc

    def _read_line(self, method: str) -> str:
        try:
            item = self._out_q.get(timeout=self.timeout)
        except queue.Empty:
            self.terminate()
            raise MCPClientError(
                f"timed out after {self.timeout}s waiting for a response to "
                f"{method!r}; terminated the child"
            )
        if item is _EOF:
            raise MCPClientError(
                f"server closed stdout before responding to {method!r} "
                f"(exit code {self.proc.poll()!r})"
            )
        return item

    # ---- JSON-RPC surface ------------------------------------------------ #
    def request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        msg_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Send one JSON-RPC request over the wire and read one response line."""
        if msg_id is None:
            self._next_id += 1
            msg_id = self._next_id
        message: Dict[str, Any] = {"jsonrpc": "2.0", "id": msg_id, "method": method}
        if params is not None:
            message["params"] = params
        self._write(message)
        response = json.loads(self._read_line(method))
        return response

    def notify(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Send a JSON-RPC notification (no ``id``); read nothing back."""
        message: Dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self._write(message)

    def initialize(self, protocol_version: str = "2025-06-18") -> Dict[str, Any]:
        """Complete the handshake: ``initialize`` then ``notifications/initialized``."""
        response = self.request(
            "initialize",
            {
                "protocolVersion": protocol_version,
                "capabilities": {},
                "clientInfo": {"name": "p052-e2e-client", "version": "0"},
            },
        )
        self.notify("notifications/initialized")
        return response

    def call_tool(
        self, name: str, arguments: Dict[str, Any], msg_id: Optional[int] = None
    ) -> Tuple[bool, Any]:
        """Drive one ``tools/call`` over the wire; return ``(is_error, result)``.

        ``result`` is the JSON parsed from the single ``content[0].text`` block —
        i.e. the adapter's ``{"result": ..., "artifacts": [...]}`` or its
        ``{"error": ...}`` on a handled failure.
        """
        response = self.request(
            "tools/call", {"name": name, "arguments": arguments}, msg_id
        )
        result = response["result"]
        content = result["content"]
        assert content[0]["type"] == "text"
        return result["isError"], json.loads(content[0]["text"])

    # ---- lifecycle ------------------------------------------------------- #
    def shutdown(self, timeout: float = 15.0) -> Tuple[int, str]:
        """Close stdin (the clean-stop signal), reap the child, return (rc, stderr).

        This is the graceful path the product uses: closing stdin ends the
        server's read-loop and it exits on its own.
        """
        if self.proc.stdin is not None and not self.proc.stdin.closed:
            try:
                self.proc.stdin.close()
            except OSError:
                pass
        returncode = self.proc.wait(timeout=timeout)
        self._out_thread.join(timeout=timeout)
        self._err_thread.join(timeout=timeout)
        return returncode, "".join(self._err_lines)

    def terminate(self) -> None:
        """Force the child down (used on a timeout or in teardown)."""
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

    def close(self) -> None:
        """Idempotent teardown: reap the child and close every pipe."""
        if self.proc.poll() is None:
            if self.proc.stdin is not None and not self.proc.stdin.closed:
                try:
                    self.proc.stdin.close()
                except OSError:
                    pass
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.terminate()
        for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr):
            if stream is not None and not stream.closed:
                try:
                    stream.close()
                except OSError:
                    pass

    def __enter__(self) -> "MCPClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
