"""P-054 — README numbers drift guard.

Pins the README's load-bearing STATED numbers against their live/committed
sources so the staleness class that reached the product surface twice (a stale
regression-example count, a stale command count) fails LOUDLY instead of
shipping. The extraction is TARGETED and anchored on the specific known line/
block shapes — deliberately NOT a general "scan every digit" parser that would
flake on incidental numbers in prose. A legitimate future README edit that
keeps the numbers correct still passes; any number drifting from its live/
committed source fails with a message naming the drifted number and its source.

Three coverage areas:

1. Command count — every "N commands" claim equals the live registry
   ``len(logic_mix_os.cowork.COMMANDS)``, asserted at both authored spots (the
   CLI table + the section map) AND whole-file (no stale count survives
   anywhere — the check the P-053 sweep needed to catch a leftover "32").
2. Regression example — the ``{ "tests_run": …, "passed": …, "failed": … }``
   example block equals a live ``run_regression_suite()``. This is the exact
   class that shipped stale (68 vs the live 93); the guard makes it impossible.
3. Five-producer table — every table overall / vocal-role / loop-context cell
   equals the committed pin in ``tests/test_sample_refresh.py``'s ``HEADLINES``
   dict — the SINGLE SOURCE the sample-refresh suite already owns (no second
   hardcoded copy that could itself drift; the P-047/P-049 derivation-from-pins
   discipline). Also closes the standing P-046 gap: the README table numbers
   were never machine-pinned.
"""

from __future__ import annotations

import re

from logic_mix_os.cowork import COMMANDS
from logic_mix_os.regression import run_regression_suite

from conftest import ROOT
# The single source of truth for the five-producer table numbers already
# owned by the sample-refresh suite — imported, NEVER re-hardcoded here.
from test_sample_refresh import HEADLINES

README = ROOT / "README.md"


def _readme_text():
    return README.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# 1. Command count
# --------------------------------------------------------------------------

# The two authored spots (orchestrator recon): the CLI-table row (~401) and the
# section-map line (~574). Each is anchored on its surrounding prose so a stray
# digit elsewhere can never satisfy it.
_CLI_TABLE_COUNT = re.compile(r"Claude Cowork command surface \((\d+) commands\)")
# Tolerant of the ``**`` bold markers and the em dash between "(§43)" and the
# count (``...(§43)** — 35 bounded commands``): ``\D*?`` swallows them without
# pinning the exact punctuation, and also sidesteps any em-dash encoding worry.
_SECTION_MAP_COUNT = re.compile(
    r"Cowork command surface \(§43\)\D*?(\d+) bounded commands"
)
# The whole-file sweep: EVERY "N commands" / "N bounded commands" claim.
_ANY_COMMAND_COUNT = re.compile(r"(\d+) (?:bounded )?commands")


def test_command_count_authored_spots_match_live_registry():
    text = _readme_text()
    live = str(len(COMMANDS))

    cli = _CLI_TABLE_COUNT.search(text)
    assert cli, (
        "README CLI-table row 'Claude Cowork command surface (N commands)' not found"
    )
    assert cli.group(1) == live, (
        f"README CLI-table command count {cli.group(1)!r} != live "
        f"len(COMMANDS)={live!r}"
    )

    section = _SECTION_MAP_COUNT.search(text)
    assert section, (
        "README section-map line 'Cowork command surface (§43) — N bounded "
        "commands' not found"
    )
    assert section.group(1) == live, (
        f"README section-map command count {section.group(1)!r} != live "
        f"len(COMMANDS)={live!r}"
    )


def test_no_stale_command_count_anywhere_in_readme():
    text = _readme_text()
    live = str(len(COMMANDS))
    found = _ANY_COMMAND_COUNT.findall(text)
    assert found, "expected at least one 'N commands' claim in the README"
    stale = [n for n in found if n != live]
    assert not stale, (
        f"README carries stale command count(s) {stale}; live len(COMMANDS)="
        f"{live!r} (the P-053 whole-file check: e.g. a leftover '32 commands')"
    )


# --------------------------------------------------------------------------
# 2. Regression example
# --------------------------------------------------------------------------

# The example block at README ~532, anchored on its literal key order.
_REGRESSION_EXAMPLE = re.compile(
    r'\{\s*"tests_run":\s*(\d+),\s*"passed":\s*(\d+),\s*"failed":\s*(\d+)'
)


def test_regression_example_matches_live_suite():
    text = _readme_text()
    m = _REGRESSION_EXAMPLE.search(text)
    assert m, (
        'README regression example block { "tests_run": …, "passed": …, '
        '"failed": … } not found'
    )
    tests_run, passed, failed = (int(g) for g in m.groups())

    live = run_regression_suite()
    assert tests_run == live["tests_run"], (
        f"README regression example tests_run={tests_run} != live "
        f"run_regression_suite()['tests_run']={live['tests_run']}"
    )
    assert passed == live["passed"], (
        f"README regression example passed={passed} != live "
        f"passed={live['passed']}"
    )
    assert failed == live["failed"], (
        f"README regression example failed={failed} != live "
        f"failed={live['failed']}"
    )


# --------------------------------------------------------------------------
# 3. Five-producer table
# --------------------------------------------------------------------------

# Producer key (HEADLINES / SAMPLE_TREES) -> its README table column header.
_PRODUCER_COLUMN = {
    "halee_ramone": "Halee/Ramone (reference)",
    "timbaland": "Timbaland",
    "quincy_jones": "Quincy Jones",
    "brian_eno": "Brian Eno",
    "chris_lord_alge": "Chris Lord-Alge",
}
# README table row label -> the HEADLINES key it pins.
_ROW_LABEL_TO_KEY = {
    "Overall mix readiness": "overall_mix_readiness_score",
    "Vocal role fit": "vocal_role_fit_score",
    "Loop context": "loop_context_score",
}


def _table_row_cells(text, label):
    """Return the data cells of the markdown table row whose first cell is
    exactly ``label`` — anchored to line start, tolerant of bold (``**``)
    emphasis on cell values."""
    m = re.search(
        r"^\|\s*" + re.escape(label) + r"\s*\|(.+)\|\s*$", text, re.MULTILINE
    )
    assert m, f"README five-producer table row '{label}' not found"
    return [c.strip().strip("*").strip() for c in m.group(1).split("|")]


def test_five_producer_table_matches_committed_headlines():
    text = _readme_text()
    header = _table_row_cells(text, "Reading")
    col_index = {label: i for i, label in enumerate(header)}
    for producer, column in _PRODUCER_COLUMN.items():
        assert column in col_index, (
            f"README five-producer table missing column '{column}' "
            f"(header row: {header})"
        )

    for row_label, hkey in _ROW_LABEL_TO_KEY.items():
        cells = _table_row_cells(text, row_label)
        for producer, column in _PRODUCER_COLUMN.items():
            idx = col_index[column]
            expected = f"{HEADLINES[producer][hkey]:.1f}"
            assert cells[idx] == expected, (
                f"README table cell [{row_label} / {column}] = {cells[idx]!r} "
                f"!= committed HEADLINES['{producer}']['{hkey}'] = {expected!r} "
                f"(single source: tests/test_sample_refresh.py — do not "
                f"hardcode a second copy)"
            )
