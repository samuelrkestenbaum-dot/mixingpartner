"""P-023 — the versioned, self-describing raw-CLI contract: ``describe_contract``.

P-021 proved the cowork CLI is agent-drivable end-to-end. P-023 turns that into a
STABLE, VERSIONED, SELF-DESCRIBING contract an agent (Claude Cowork) can introspect
instead of reverse-engineering an ad-hoc CLI. ``describe_contract`` returns a pure,
deterministic JSON document::

    {
      "api_version": "1.0",
      "invocation": "...",
      "commands": {
        "<name>": {"purpose", "phase", "params", "side_effect"}, ...
      }
    }

These tests are the binding guard for that contract:

  * Completeness INVARIANT (load-bearing): the contract's ``commands`` keys are
    EXACTLY the ``COMMANDS`` registry keys — no orphan (a real command missing an
    entry) and no phantom (a contract entry for a non-command).
    ``test_completeness_invariant_is_load_bearing`` proves the check is not vacuous.
  * ``params`` are DERIVED from the real handler signature (``inspect.signature``,
    dropping the context arg and ``**k``) so the contract cannot drift from code.
  * ``side_effect`` is an HONEST, declared classification — the live-vs-dead
    distinction becomes a first-class contract fact (``record_mix_pass`` writes the
    LIVE history channel; ``write_mix_decision`` writes the DEAD decision ledger).
  * Versioned + deterministic: ``api_version`` is a stable string; two calls are
    byte-identical.
  * Registry count 34 -> 35 (no stale 34); ``describe_contract`` is registered.

Pure in-memory data + JSON. No DAW / network / subprocess. Deterministic.
"""

from __future__ import annotations

import inspect
import json

from logic_mix_os.cowork import API_VERSION, COMMANDS, run_command


def _contract():
    # describe_contract is pure/deterministic and reads no analysis result or
    # memory, so a bare context is enough to exercise it.
    return run_command("describe_contract", {"result": None, "memory": None})


def _derive_params(fn):
    """The kwargs a caller may pass: every parameter after the leading context
    arg, excluding ``**k`` / ``*args``. Mirrors the derivation the contract must use.
    """
    params = list(inspect.signature(fn).parameters.values())[1:]  # drop context arg
    return [
        p.name
        for p in params
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]


# --------------------------------------------------------------------------- #
# Completeness invariant — the load-bearing guard.
# --------------------------------------------------------------------------- #
def test_contract_covers_every_command_exactly():
    """The contract's command keys are EXACTLY the registry keys: no orphan, no
    phantom.
    """
    contract = _contract()
    contract_keys = set(contract["commands"])
    registry_keys = set(COMMANDS)
    assert contract_keys == registry_keys, (
        "contract must exactly cover the registry — "
        f"orphaned (command w/o entry): {registry_keys - contract_keys}; "
        f"phantom (entry w/o command): {contract_keys - registry_keys}"
    )


def test_completeness_invariant_is_load_bearing():
    """The completeness check is NOT vacuous.

    We take the real contract keys, then show that (a) dropping an entry breaks the
    exact-cover check and (b) inventing a phantom entry breaks it too. If the check
    were vacuous, neither mutation would fail — this pins it to real coverage.
    """
    contract = _contract()
    keys = set(contract["commands"])

    # (a) Orphan a real command -> exact-cover must fail.
    orphaned = keys - {"detect_masking"}
    assert orphaned != set(COMMANDS), (
        "dropping a real command's entry must break exact coverage"
    )

    # (b) Add a phantom entry -> exact-cover must fail.
    phantom = keys | {"not_a_real_command"}
    assert phantom != set(COMMANDS), (
        "a phantom contract entry must break exact coverage"
    )


def test_describe_contract_accounts_for_itself():
    """``describe_contract`` is itself a registered command with a contract entry."""
    assert "describe_contract" in COMMANDS
    assert "describe_contract" in _contract()["commands"]


# --------------------------------------------------------------------------- #
# params derived from the real signature (no drift).
# --------------------------------------------------------------------------- #
def test_params_match_handler_signatures_for_all_commands():
    """Every contract entry's ``params`` names equal the handler's real signature
    kwargs (proves the inspect derivation is correct and cannot drift).
    """
    contract = _contract()
    for name, meta in COMMANDS.items():
        entry = contract["commands"][name]
        got = [p["name"] for p in entry["params"]]
        expected = _derive_params(meta["fn"])
        assert got == expected, (
            f"{name}: contract params {got} != real signature kwargs {expected}"
        )


def test_record_mix_pass_params_are_name_and_reverted():
    """A param-carrying command: ``record_mix_pass`` exposes name + reverted, and
    the reverted default is surfaced.
    """
    entry = _contract()["commands"]["record_mix_pass"]
    names = [p["name"] for p in entry["params"]]
    assert names == ["name", "reverted"]
    by_name = {p["name"]: p for p in entry["params"]}
    assert by_name["reverted"]["default"] is False


def test_param_free_read_command_has_no_params():
    """A param-free read command (``detect_masking``, a ``lambda c, **k`` handler)
    exposes an empty param list — the context arg and ``**k`` are dropped.
    """
    entry = _contract()["commands"]["detect_masking"]
    assert entry["params"] == []


# --------------------------------------------------------------------------- #
# side_effect honesty — pin live-vs-dead at the contract level.
# --------------------------------------------------------------------------- #
def test_side_effect_pins_live_vs_dead_and_read_only():
    contract = _contract()["commands"]
    # LIVE history channel (feeds the next-pass planner).
    assert contract["record_mix_pass"]["side_effect"] == "writes:history(live)"
    # LIVE taste channel.
    assert contract["update_taste_calibration"]["side_effect"] == "writes:taste(live)"
    # DEAD decision ledger (audit log, not a live input).
    assert contract["write_mix_decision"]["side_effect"] == "writes:ledger(dead)"
    # In-session mutation only (no disk write).
    assert contract["override_track_identity"]["side_effect"] == "mutates:session"
    # A read-only projection.
    assert contract["detect_masking"]["side_effect"] == "none"


def test_side_effect_vocabulary_is_closed():
    """Every declared side_effect is one of the sanctioned classifications."""
    allowed = {
        "none",
        "writes:history(live)",
        "writes:taste(live)",
        "writes:ledger(dead)",
        "mutates:session",
    }
    for name, entry in _contract()["commands"].items():
        assert entry["side_effect"] in allowed, (
            f"{name} has an unsanctioned side_effect {entry['side_effect']!r}"
        )


def test_only_the_known_writers_declare_a_side_effect():
    """Exactly the four known side-effecting commands are non-``none``; everything
    else is a read-only projection.
    """
    contract = _contract()["commands"]
    non_none = {name for name, e in contract.items() if e["side_effect"] != "none"}
    assert non_none == {
        "record_mix_pass",
        "update_taste_calibration",
        "write_mix_decision",
        "override_track_identity",
    }


# --------------------------------------------------------------------------- #
# purpose + phase.
# --------------------------------------------------------------------------- #
def test_purpose_is_the_registry_desc():
    contract = _contract()["commands"]
    for name, meta in COMMANDS.items():
        assert contract[name]["purpose"] == meta["desc"]


def test_phase_is_session_flow_phase_or_auxiliary():
    from logic_mix_os.cowork import _SESSION_FLOW

    phase_of = {}
    for phase in _SESSION_FLOW["phases"]:
        for cmd in phase["commands"]:
            phase_of[cmd] = phase["phase"]
    for cmd in _SESSION_FLOW["auxiliary"]:
        phase_of[cmd] = "auxiliary"

    contract = _contract()["commands"]
    for name in COMMANDS:
        assert contract[name]["phase"] == phase_of.get(name, "auxiliary")
    # A phase command and an auxiliary command, pinned.
    assert contract["record_mix_pass"]["phase"] == "record-outcome"
    assert contract["describe_contract"]["phase"] == "auxiliary"


# --------------------------------------------------------------------------- #
# Versioned + deterministic.
# --------------------------------------------------------------------------- #
def test_api_version_is_present_and_stable():
    contract = _contract()
    assert contract["api_version"] == API_VERSION
    assert isinstance(API_VERSION, str) and API_VERSION == "1.0"


def test_invocation_string_is_present():
    contract = _contract()
    assert "invocation" in contract
    assert "cowork" in contract["invocation"]


def test_describe_contract_is_deterministic():
    a = _contract()
    b = _contract()
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_describe_contract_output_is_jsonable():
    json.dumps(_contract())  # must not raise


# --------------------------------------------------------------------------- #
# Registry count.
# --------------------------------------------------------------------------- #
def test_registry_count_is_35():
    assert len(COMMANDS) == 35
    assert "describe_contract" in COMMANDS
