"""Persisted, append-only, tamper-evident governance ledger (Hardening Packet 4, Layer 2).

A dedicated audit trail for the governance kernel — deliberately SEPARATE from
``memory.py`` (which holds creative/taste state). Every governance event (an
action proposed, approved, an approval refused, an apply attempted/refused/done)
is appended as one JSON line to ``governance_ledger.jsonl``.

The file is *hash-chained*: each entry carries the ``entry_hash`` of the one
before it in ``prev_hash``, and its own ``entry_hash`` is the hash of its
canonical content (which includes ``prev_hash``). This makes tampering,
reordering, or truncation detectable by an honest verifier — it is NOT
cryptographic signing (no keys, no authorship proof), only integrity evidence.

The ledger survives process restart: a fresh kernel pointed at the same file
replays the events to reconstruct enough authority state (class / approval /
status per action) to keep gating correctly.

Pure, deterministic, local. No DAW, no network, no execution.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

GENESIS_HASH = "0" * 16

# The canonical, ordered set of event fields written for every entry.
EVENT_FIELDS = (
    "event_id", "event_type", "timestamp", "action_id", "receipt_id",
    "authority_class", "decision", "approval_required", "status",
    "actor", "reason", "prev_hash",
)

EVENT_TYPES = (
    "propose",
    "approve",
    "blocked_approval_attempt",
    "mark_applied_attempt",
    "mark_applied_refused",
    "applied",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(payload: Dict) -> str:
    """Stable JSON used for hashing — key order must never matter."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(prev_hash: str, payload: Dict) -> str:
    body = _canonical(payload)
    return hashlib.sha256(f"{prev_hash}|{body}".encode("utf-8")).hexdigest()[:16]


class GovernanceLedger:
    """Append-only hash-chained event log, optionally backed by a jsonl file."""

    def __init__(self, path: Optional[str] = None, clock: Optional[Callable[[], str]] = None):
        self.path = Path(path) if path else None
        self._clock = clock or _utc_now
        self._entries: List[Dict] = []
        self._last_hash = GENESIS_HASH
        self._seq = 0
        if self.path and self.path.exists():
            self._load()

    # -- persistence --------------------------------------------------------
    def _load(self) -> None:
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            self._entries.append(entry)
            self._last_hash = entry["entry_hash"]
            self._seq = entry["seq"] + 1

    def append(self, event_type: str, *, action_id: Optional[str], receipt_id: Optional[str],
               authority_class: Optional[int], decision: Optional[str],
               approval_required: Optional[bool], status: Optional[str],
               actor: str, reason: str, timestamp: Optional[str] = None) -> Dict:
        seq = self._seq
        prev_hash = self._last_hash
        ts = timestamp or self._clock()
        event_id = "evt_" + hashlib.sha256(
            f"{seq}|{event_type}|{action_id}|{ts}|{prev_hash}".encode("utf-8")
        ).hexdigest()[:12]
        payload = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp": ts,
            "action_id": action_id,
            "receipt_id": receipt_id,
            "authority_class": authority_class,
            "decision": decision,
            "approval_required": approval_required,
            "status": status,
            "actor": actor,
            "reason": reason,
            "prev_hash": prev_hash,
            "seq": seq,
        }
        entry_hash = _hash(prev_hash, payload)
        entry = {**payload, "entry_hash": entry_hash}

        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=True) + "\n")

        self._entries.append(entry)
        self._last_hash = entry_hash
        self._seq += 1
        return entry

    # -- inspection ---------------------------------------------------------
    def entries(self) -> List[Dict]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def verify(self) -> Dict:
        """Recompute the chain and report integrity. Detects content tampering,
        reordering, truncation of the prev/entry hash links, and seq gaps."""
        prev = GENESIS_HASH
        for i, entry in enumerate(self._entries):
            if entry.get("seq") != i:
                return self._broken(i, f"sequence gap: expected seq {i}, found {entry.get('seq')}")
            if entry.get("prev_hash") != prev:
                return self._broken(i, "prev_hash does not match previous entry_hash (reordered/spliced)")
            payload = {k: entry.get(k) for k in entry if k != "entry_hash"}
            recomputed = _hash(prev, payload)
            if recomputed != entry.get("entry_hash"):
                return self._broken(i, "entry_hash mismatch — entry content was altered")
            prev = entry["entry_hash"]
        return {"ok": True, "entries": len(self._entries), "broken_at": None,
                "reason": "intact", "head_hash": prev}

    @staticmethod
    def _broken(index: int, reason: str) -> Dict:
        return {"ok": False, "entries": index, "broken_at": index, "reason": reason}
