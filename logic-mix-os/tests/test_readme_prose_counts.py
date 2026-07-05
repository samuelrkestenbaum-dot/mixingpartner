"""P-055 — README prose-count drift guard.

The sibling of ``tests/test_readme_numbers.py`` (P-054), one abstraction level
up: P-054 pinned the README's load-bearing *numeric* values (command count,
regression example, the five-producer table); this pins the *spelled-out prose*
counts — "five committed trees", "eleven producer x mode runs", "the four
example projects" — against the SAME live/committed single sources, so the next
producer / demo / fixture forces the prose to update or the suite fails loudly.

Like P-054 the extraction is TARGETED and anchored on the specific
"<word> <noun>" phrase shapes the recon enumerated — deliberately NOT a general
"scan every spelled number" parser. That anchoring is load-bearing: the README
carries OTHER fives that are NOT the producer/tree count and must never be
caught — the five hardcoded safety switches (~160) and the five creative
problem branches (~224) — and OTHER fours that are the (producers - 1) group,
not the fixture count (~123, ~149, ~329). Each expected value is DERIVED from
the one existing source (``SAMPLE_TREES`` / ``MODE_DEMOS`` / the committed
fixture set), never a re-hardcoded literal — so adding producer #6 bumps
``len(SAMPLE_TREES)`` and this guard then DEMANDS the prose say "six".

Four coverage areas:

1. Producer/tree count — every "<n> ... trees / producers / profiles /
   judgments" prose count equals ``len(SAMPLE_TREES)`` (the single source the
   sample-refresh suite already owns; == the number of shipped producer
   profiles).
2. Demo count — every "<n> ... producer x mode runs / directories / demos /
   creative pairs" count equals ``len(MODE_DEMOS)``.
3. Fixture count — every "<n> example projects / fixtures" count (spelled at
   ~46/~510, and the digit "(4 fixtures ...)" in the layout at ~499) equals the
   live committed fixture set (``fixtures/*/project_manifest.json`` — the
   projects the generator writes; conftest's autouse ``ensure_fixtures``
   guarantees they exist).
4. Neutral-vs-deviating split (~343) — "Of the eleven demos, seven win exactly
   the moves the neutral search picks; the four that deviate ..." is a COMPUTED
   split; both numbers are derived from the committed demo winners
   (``test_mode_demo_refresh.WINNERS``, which that suite pins byte-for-byte to
   each demo's ``creative.json``) against the neutral baseline
   (``_COMMON_WINNERS``): the count whose winner set equals the neutral set is
   the "win" number, the rest the "deviate" number.
"""

from __future__ import annotations

import re

from conftest import ROOT
# The single sources — imported, NEVER re-hardcoded here (the P-047/P-049/P-054
# derivation discipline).
from test_sample_refresh import SAMPLE_TREES
from test_mode_demo_refresh import (
    MODE_DEMOS,
    WINNERS as DEMO_WINNERS,
    _COMMON_WINNERS,
)

README = ROOT / "README.md"
FIXTURES_DIR = ROOT / "fixtures"


def _readme_text():
    return README.read_text(encoding="utf-8")


# A small spelled-number -> int map (three .. twelve is plenty for these
# counts). A pinned phrase whose captured token is NOT here has drifted and
# fails loudly rather than silently passing.
_WORD_TO_INT = {
    "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
}


def _num(word):
    assert word in _WORD_TO_INT, (
        f"README pinned phrase carried an unrecognized count word {word!r} "
        f"(expected one of {sorted(_WORD_TO_INT)}) — the phrase drifted"
    )
    return _WORD_TO_INT[word]


def _live_fixture_count():
    """The number of committed fixture projects — the single source for the
    README's "four example projects" / "four fixtures" prose. Each generated
    fixture is one ``<name>/project_manifest.json`` under ``fixtures/`` (all
    git-tracked; conftest's autouse ``ensure_fixtures`` also guarantees them)."""
    return len(sorted(FIXTURES_DIR.glob("*/project_manifest.json")))


# --------------------------------------------------------------------------
# 1. Producer / tree count == len(SAMPLE_TREES)
# --------------------------------------------------------------------------

# Each pattern's EVERY captured token must equal the live producer/tree count.
# Anchored on the SPECIFIC "<word> <noun>" shapes so the doc's other fives (the
# five hardcoded safety switches ~160, the five creative problem branches ~224)
# and the (producers - 1) fours (~123, ~149, ~329) are never caught.
_TREE_PRODUCER_PHRASES = [
    (r"(\w+) committed trees", "five committed trees (~63)"),
    (r"(\w+) committed sample trees", "the five committed sample trees (~81,~497)"),
    (r"same measurements, (\w+) judgments", "five judgments (~111)"),
    (r"all (\w+) profiles read", "all five profiles read (~125)"),
    (r"all (\w+) producers", "all five producers (~159)"),
    (r"all (\w+) trees", "all five trees (~163)"),
    (r"the (\w+) `examples/sample_output", "the five examples/sample_output* trees (~167)"),
    (r"the way the (\w+) trees above", "the five trees above (~221)"),
    (r"same stems, (\w+) producers\)", "five producers (~497)"),
]


def test_producer_and_tree_prose_counts_match_sample_trees():
    text = _readme_text()
    expected = len(SAMPLE_TREES)
    for pattern, label in _TREE_PRODUCER_PHRASES:
        words = re.findall(pattern, text)
        assert words, (
            f"pinned README producer/tree phrase not found: {label} "
            f"[{pattern!r}]"
        )
        for word in words:
            assert _num(word) == expected, (
                f"README prose count {word!r} in {label} = {_num(word)} != "
                f"len(SAMPLE_TREES)={expected} (single source: "
                f"tests/test_sample_refresh.SAMPLE_TREES — a shipped producer "
                f"was added/removed and this prose must say the new count)"
            )


# --------------------------------------------------------------------------
# 2. Demo count == len(MODE_DEMOS)
# --------------------------------------------------------------------------

_DEMO_PHRASES = [
    (r"(\w+) producer × mode runs", "eleven producer × mode runs (~76)"),
    (r"(\w+) directories, one per producer", "eleven directories (~222)"),
    (r"Of the (\w+) demos", "Of the eleven demos (~343)"),
    (r"(\w+) committed producer × mode creative pairs",
     "eleven committed producer × mode creative pairs (~498)"),
]


def test_demo_prose_counts_match_mode_demos():
    text = _readme_text()
    expected = len(MODE_DEMOS)
    for pattern, label in _DEMO_PHRASES:
        words = re.findall(pattern, text)
        assert words, (
            f"pinned README demo phrase not found: {label} [{pattern!r}]"
        )
        for word in words:
            assert _num(word) == expected, (
                f"README prose count {word!r} in {label} = {_num(word)} != "
                f"len(MODE_DEMOS)={expected} (single source: "
                f"tests/test_mode_demo_refresh.MODE_DEMOS — a committed demo "
                f"was added/removed and this prose must say the new count)"
            )


# --------------------------------------------------------------------------
# 3. Fixture count == the live committed fixture set
# --------------------------------------------------------------------------

_FIXTURE_SPELLED_PHRASES = [
    (r"the (\w+) example projects", "the four example projects (~46)"),
    (r"across (\w+) fixtures", "across four fixtures (~510)"),
]
# The layout section carries the same count as a DIGIT: "(4 fixtures, ...)".
_FIXTURE_DIGIT_PHRASE = r"\((\d+) fixtures,"


def test_fixture_prose_counts_match_live_fixture_count():
    text = _readme_text()
    expected = _live_fixture_count()
    for pattern, label in _FIXTURE_SPELLED_PHRASES:
        words = re.findall(pattern, text)
        assert words, (
            f"pinned README fixture phrase not found: {label} [{pattern!r}]"
        )
        for word in words:
            assert _num(word) == expected, (
                f"README prose count {word!r} in {label} = {_num(word)} != "
                f"live fixture count {expected} (single source: "
                f"fixtures/*/project_manifest.json)"
            )

    digits = re.findall(_FIXTURE_DIGIT_PHRASE, text)
    assert digits, (
        f"pinned README layout fixture count '(N fixtures, ...)' (~499) not "
        f"found [{_FIXTURE_DIGIT_PHRASE!r}]"
    )
    for digit in digits:
        assert int(digit) == expected, (
            f"README layout fixture count '{digit} fixtures' (~499) != live "
            f"fixture count {expected} (single source: "
            f"fixtures/*/project_manifest.json)"
        )


# --------------------------------------------------------------------------
# 4. The neutral-vs-deviating computed split (~343)
# --------------------------------------------------------------------------

# "Of the eleven demos, seven win exactly the moves the neutral search picks;
# the four that deviate ...". Both numbers derive from the committed demo
# winners (WINNERS, byte-pinned to each creative.json by
# test_mode_demo_refresh) against the neutral baseline (_COMMON_WINNERS).
_SPLIT_TOTAL_WIN = re.compile(
    r"Of the (\w+) demos, (\w+) win exactly the moves the neutral"
)
_SPLIT_DEVIATE = re.compile(r"the (\w+) that deviate all deviate")


def test_neutral_vs_deviating_split_matches_committed_winners():
    text = _readme_text()
    deviating = sum(
        1 for demo in MODE_DEMOS if DEMO_WINNERS[demo] != _COMMON_WINNERS
    )
    winning = len(MODE_DEMOS) - deviating

    m = _SPLIT_TOTAL_WIN.search(text)
    assert m, (
        "README split sentence 'Of the N demos, M win exactly the moves the "
        "neutral search picks' (~343) not found"
    )
    total_word, win_word = m.group(1), m.group(2)
    assert _num(total_word) == len(MODE_DEMOS), (
        f"README split total {total_word!r} = {_num(total_word)} != "
        f"len(MODE_DEMOS)={len(MODE_DEMOS)}"
    )
    assert _num(win_word) == winning, (
        f"README 'seven win' count {win_word!r} = {_num(win_word)} != the "
        f"derived win-neutral count {winning} (demos whose committed winners "
        f"== _COMMON_WINNERS; single source: tests/test_mode_demo_refresh)"
    )

    d = _SPLIT_DEVIATE.search(text)
    assert d, (
        "README split sentence 'the N that deviate all deviate' (~344) not found"
    )
    assert _num(d.group(1)) == deviating, (
        f"README 'four that deviate' count {d.group(1)!r} = {_num(d.group(1))} "
        f"!= the derived deviating count {deviating} (demos whose committed "
        f"winners != _COMMON_WINNERS; single source: tests/test_mode_demo_refresh)"
    )
