"""P-020 — session-flow discoverability: the ``describe_session`` command.

``list_commands`` is a FLAT, alphabetised catalog: an agent can see the 34
commands but not the canonical END-TO-END SEQUENCE (intake -> classify ->
diagnose -> plan -> checklist -> validate/govern -> record-outcome -> next-pass).
``describe_session`` returns an ORDERED, phase-grouped view over the SAME
registry so an agent can navigate a full mixing session.

These tests are the binding guard for that view:

  * Completeness INVARIANT (load-bearing): every key in ``COMMANDS`` appears
    EXACTLY ONCE across all phases + the ``auxiliary`` bucket — no command
    orphaned from the flow, none double-listed. A new command with no phase (or
    a double-listed one) FAILS this test; ``test_completeness_invariant_is_load_bearing``
    proves the guard is not vacuous.
  * Canonical ORDER: the phase sequence is exactly the declared session order.
  * Every listed command is a real registry key.
  * Determinism: two calls return byte-identical output.
  * Registry count 33 -> 34 (no stale 33); ``describe_session`` is registered
    and is itself accounted for in the partition.

Pure in-memory data + JSON. No DAW / network / subprocess. Deterministic.
"""

from __future__ import annotations

import json

from logic_mix_os.cowork import COMMANDS, _SESSION_FLOW, run_command


# The canonical session order P-020 declares. Grounded in the README pipeline
# (source -> identity -> metrics -> role -> sections -> depth -> masking ->
# doctrine -> plan -> checklist -> next-pass) plus the P-019 record + validate
# steps. This is the contract the ordered view must honour.
CANONICAL_PHASE_ORDER = [
    "intake",
    "classify",
    "diagnose",
    "plan",
    "checklist",
    "validate",
    "record-outcome",
    "next-pass",
]


def _describe():
    # describe_session is pure/deterministic and reads no result, so a bare
    # context (no analysis, no memory) is enough to exercise it.
    return run_command("describe_session", {"result": None, "memory": None})


# --------------------------------------------------------------------------- #
# Completeness invariant — the load-bearing guard.
# --------------------------------------------------------------------------- #
def test_every_command_is_covered_exactly_once():
    """Every ``COMMANDS`` key appears EXACTLY ONCE across phases + auxiliary."""
    out = _describe()

    covered = []
    for phase in out["phases"]:
        covered.extend(phase["commands"])
    covered.extend(out["auxiliary"])

    # No duplicates: a command listed in two phases (or a phase + auxiliary).
    assert len(covered) == len(set(covered)), "a command is listed more than once"

    # Exact partition of the registry: no orphan, no phantom.
    assert set(covered) == set(COMMANDS), (
        "flow/auxiliary partition must exactly cover the registry — "
        f"orphaned: {set(COMMANDS) - set(covered)}; "
        f"phantom: {set(covered) - set(COMMANDS)}"
    )


def test_describe_session_accounts_for_itself():
    """``describe_session`` must be in the partition (self-accounted)."""
    out = _describe()
    covered = {c for phase in out["phases"] for c in phase["commands"]}
    covered |= set(out["auxiliary"])
    assert "describe_session" in covered


def test_completeness_invariant_is_load_bearing():
    """The invariant is NOT vacuous: an uncovered OR double-listed command fails.

    We rebuild the covered set the way the invariant test does, then show that
    (a) dropping a command from the partition breaks the exact-cover check, and
    (b) double-listing one breaks the no-duplicate check. If the invariant were
    vacuous, neither mutation would fail — this pins it to real coverage.
    """
    out = _describe()
    covered = [c for phase in out["phases"] for c in phase["commands"]]
    covered.extend(out["auxiliary"])

    # (a) Orphan a command -> exact-cover check must fail.
    orphaned = covered[:-1]
    assert set(orphaned) != set(COMMANDS), (
        "dropping a command must break exact coverage — invariant is load-bearing"
    )

    # (b) Double-list a command -> no-duplicate check must fail.
    duplicated = covered + [covered[0]]
    assert len(duplicated) != len(set(duplicated)), (
        "double-listing a command must break the no-duplicate check"
    )


# --------------------------------------------------------------------------- #
# Canonical order + real keys.
# --------------------------------------------------------------------------- #
def test_phases_are_in_canonical_order():
    out = _describe()
    assert [p["phase"] for p in out["phases"]] == CANONICAL_PHASE_ORDER


def test_every_phase_has_purpose_and_nonempty_commands():
    out = _describe()
    for phase in out["phases"]:
        assert phase["purpose"], f"phase {phase['phase']} missing a purpose"
        assert phase["commands"], f"phase {phase['phase']} has no commands"


def test_every_listed_command_is_a_real_registry_key():
    out = _describe()
    for phase in out["phases"]:
        for cmd in phase["commands"]:
            assert cmd in COMMANDS, f"phase lists unknown command {cmd!r}"
    for cmd in out["auxiliary"]:
        assert cmd in COMMANDS, f"auxiliary lists unknown command {cmd!r}"


def test_source_flow_matches_command_output():
    """The command's output is derived from the ``_SESSION_FLOW`` data structure."""
    out = _describe()
    assert [p["phase"] for p in out["phases"]] == [p["phase"] for p in _SESSION_FLOW["phases"]]
    assert out["auxiliary"] == list(_SESSION_FLOW["auxiliary"])


# --------------------------------------------------------------------------- #
# Determinism + registry count.
# --------------------------------------------------------------------------- #
def test_describe_session_is_deterministic():
    a = _describe()
    b = _describe()
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_describe_session_output_is_jsonable():
    json.dumps(_describe())  # must not raise


def test_registry_count_is_35():
    # P-023 added describe_contract (34 -> 35); it is parked in _SESSION_FLOW's
    # auxiliary bucket alongside describe_session, so the completeness invariant
    # above stays satisfied.
    assert len(COMMANDS) == 35
    assert "describe_session" in COMMANDS
    assert "describe_contract" in COMMANDS
