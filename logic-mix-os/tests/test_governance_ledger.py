"""Packet 4, Layer 2 — persisted, hash-chained, tamper-evident governance ledger."""

from __future__ import annotations

import json

from logic_mix_os.governance_kernel import GovernanceKernel
from logic_mix_os.governance_ledger import EVENT_FIELDS, GENESIS_HASH, GovernanceLedger


def _counter_clock():
    """Deterministic timestamps so tests don't depend on wall-clock."""
    n = {"i": 0}

    def clock():
        n["i"] += 1
        return f"2026-01-01T00:00:{n['i']:02d}+00:00"

    return clock


def test_events_are_appended_for_propose_approve_apply(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    k.approve(r["action_id"])
    k.mark_applied(r["action_id"])
    types = [e["event_type"] for e in k.events()]
    assert types == ["propose", "approve", "mark_applied_attempt", "applied"]


def test_class_5_apply_is_refused_and_logged(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "overwrite_source"})
    k.approve(r["action_id"])         # -> blocked_approval_attempt
    k.mark_applied(r["action_id"])    # -> attempt + refused
    types = [e["event_type"] for e in k.events()]
    assert types == ["propose", "blocked_approval_attempt", "mark_applied_attempt", "mark_applied_refused"]


def test_class_3_apply_attempt_is_refused_and_logged(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "insert_plugin", "reason": "Channel EQ on vocal"})
    k.approve(r["action_id"])
    res = k.mark_applied(r["action_id"])
    assert res["ok"] is False and "dry-run" in res["reason"].lower()
    types = [e["event_type"] for e in k.events()]
    assert types[-2:] == ["mark_applied_attempt", "mark_applied_refused"]


def test_every_event_has_the_required_fields(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "write_report"})
    k.mark_applied(r["action_id"])
    for e in k.events():
        for field in EVENT_FIELDS + ("entry_hash", "seq"):
            assert field in e, f"missing {field}"


def test_chain_links_first_entry_to_genesis(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    k.propose({"kind": "analyze"})
    first = k.events()[0]
    assert first["prev_hash"] == GENESIS_HASH


def test_each_entry_chains_to_the_previous(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    k.approve(r["action_id"])
    k.mark_applied(r["action_id"])
    events = k.events()
    for prev, cur in zip(events, events[1:]):
        assert cur["prev_hash"] == prev["entry_hash"]


def test_verify_passes_on_intact_ledger(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    k.approve(r["action_id"])
    k.mark_applied(r["action_id"])
    res = k.verify_ledger()
    assert res["ok"] is True and res["broken_at"] is None
    assert res["entries"] == len(k.events())


def test_verify_detects_content_tampering(tmp_path):
    path = tmp_path / "governance_ledger.jsonl"
    k = GovernanceKernel(ledger_path=str(path), clock=_counter_clock())
    r = k.propose({"kind": "insert_plugin", "reason": "Channel EQ on vocal"})
    k.approve(r["action_id"])

    # Tamper with the file: silently downgrade a Class-3 action to Class 0.
    lines = path.read_text().splitlines()
    first = json.loads(lines[0])
    first["authority_class"] = 0
    first["decision"] = "allow"
    lines[0] = json.dumps(first)
    path.write_text("\n".join(lines) + "\n")

    reloaded = GovernanceLedger(str(path))
    res = reloaded.verify()
    assert res["ok"] is False
    assert res["broken_at"] == 0


def test_verify_detects_truncation_reorder(tmp_path):
    path = tmp_path / "governance_ledger.jsonl"
    k = GovernanceKernel(ledger_path=str(path), clock=_counter_clock())
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    k.approve(r["action_id"])
    k.mark_applied(r["action_id"])

    # Drop the first entry (truncation) -> chain head no longer points to genesis.
    lines = path.read_text().splitlines()
    path.write_text("\n".join(lines[1:]) + "\n")

    res = GovernanceLedger(str(path)).verify()
    assert res["ok"] is False


def test_ledger_survives_process_restart(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    # First "process": propose a Class-2 action that needs approval, then stop.
    k1 = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    r = k1.propose({"kind": "offline_render", "source_immutable": False})
    action_id = r["action_id"]
    assert k1.mark_applied(action_id)["ok"] is False  # not yet approved

    # Second "process": a brand-new kernel reads the same file.
    k2 = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    rebuilt = k2._find(action_id)
    assert rebuilt is not None and rebuilt["authority_class"] == 2
    assert rebuilt.get("reconstructed") is True
    # Gating still works across the restart: approve, then it applies.
    assert k2.approve(action_id)["ok"] is True
    assert k2.mark_applied(action_id)["ok"] is True
    # And the reloaded-then-extended chain still verifies.
    assert k2.verify_ledger()["ok"] is True


def test_reconstruction_preserves_action_id_counter(tmp_path):
    path = str(tmp_path / "governance_ledger.jsonl")
    k1 = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    k1.propose({"kind": "analyze"})
    k1.propose({"kind": "write_report"})
    k2 = GovernanceKernel(ledger_path=path, clock=_counter_clock())
    # New proposals continue numbering, not restart from act_001.
    assert k2.propose({"kind": "analyze"})["action_id"] == "act_003"


def test_in_memory_ledger_still_works_without_a_path():
    """Back-compat: no path -> events live in memory, chain still valid."""
    k = GovernanceKernel()
    r = k.propose({"kind": "write_report"})
    k.mark_applied(r["action_id"])
    assert len(k.events()) == 3  # propose + attempt + applied
    assert k.verify_ledger()["ok"] is True


def test_persisted_file_is_one_json_object_per_line(tmp_path):
    path = tmp_path / "governance_ledger.jsonl"
    k = GovernanceKernel(ledger_path=str(path), clock=_counter_clock())
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    k.approve(r["action_id"])
    for line in path.read_text().splitlines():
        assert json.loads(line)["event_id"].startswith("evt_")
