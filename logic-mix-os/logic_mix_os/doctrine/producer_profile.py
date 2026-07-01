"""ProducerProfile — the swappable producer-specific judgment (P-025 foundation).

The producer-agnostic *physics* (analyzers, safety kill-switches, the
bounded-nudge mechanism, determinism/evidence contract, the move-kind vocabulary)
stays fixed in the pipeline. The producer-specific *judgment* — today 100%
hardcoded across ``creative.py`` / ``governance.py`` / ``doctrine_engine.py`` /
``pipeline.py`` — becomes a swappable ``ProducerProfile`` loaded from JSON.

**P-025 is data + loader + tests ONLY.** Nothing in the runtime path imports
``load_profile`` yet — the modules above keep using their hardcoded dicts. The
byte-identical round-trip test (``tests/test_producer_profile.py``) is the guard
that the extracted ``halee_ramone.json`` reconstructs today's judgment exactly;
P-026→P-029 will wire consumers against that guard.

The loader is pure, deterministic, and reads a local JSON file only. The returned
``ProducerProfile`` is a frozen dataclass; its collection fields are freshly
parsed from JSON on every load, so a caller can never mutate the live module
dicts (or a previous load) through it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

_DIR = Path(__file__).parent
_PRODUCERS_DIR = _DIR / "producers"

# The producer-specific structures a profile must carry (extraction-completeness
# is asserted against this in the tests). Metadata is validated separately.
_REQUIRED_DATA_FIELDS = (
    "kind_scores",
    "nudge_table",
    "promotion_table",
    "creative_nudge_cap",
    "creative_promotion_cap",
    "risk_penalty",
    "search_modes",
    "philosophy",
    "truth_alignment",
    "taste_kind_bias",
    "taste_max_delta",
    "aesthetic_kill_switches",
    "doctrine",
    "default_creative_mode",
)

_REQUIRED_METADATA_FIELDS = (
    "name",
    "display_name",
    "provenance",
    "confidence",
    "risk_class",
)


@dataclass(frozen=True)
class ProducerProfile:
    """An immutable view of one producer's judgment, loaded from JSON.

    Field names mirror the source structures verbatim so the round-trip guard is
    a direct ``==`` against the still-hardcoded module dicts (or, for the values
    computed inline in functions, an indirect drive-the-function comparison).
    """

    # metadata (honesty scaffolding — set up now, enforced in P-031)
    metadata: Dict[str, Any]

    # creative.py
    kind_scores: Dict[str, Dict[str, Any]]
    nudge_table: List[Dict[str, Any]]
    promotion_table: List[Dict[str, Any]]
    creative_nudge_cap: float
    creative_promotion_cap: float
    risk_penalty: Dict[str, int]
    search_modes: Dict[str, Dict[str, str]]
    philosophy: str

    # governance.py
    truth_alignment: Dict[str, Dict[str, int]]
    taste_kind_bias: Dict[str, Dict[str, int]]
    taste_max_delta: int
    aesthetic_kill_switches: List[str]

    # doctrine_engine.py (weights / baselines / inline penalty coefficients)
    doctrine: Dict[str, Any]

    # pipeline.py (_default_creative_mode truth -> mode map)
    default_creative_mode: Dict[str, Any]


def _normalize_kinds_sets(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """JSON has no set type: the nudge/promotion rows store ``kinds`` as a list.
    Rehydrate it to a ``set`` so the round-trip ``==`` against the source rows
    (which use sets) is honest rather than loosened to compare lists."""
    out: List[Dict[str, Any]] = []
    for row in rows:
        row = dict(row)
        if "kinds" in row and not isinstance(row["kinds"], set):
            row["kinds"] = set(row["kinds"])
        out.append(row)
    return out


def _validate(raw: Dict[str, Any], name: str) -> None:
    if "metadata" not in raw:
        raise ValueError(f"profile {name!r}: missing 'metadata'")
    meta = raw["metadata"]
    for f in _REQUIRED_METADATA_FIELDS:
        if f not in meta:
            raise ValueError(f"profile {name!r}: metadata missing {f!r}")
    if not isinstance(meta["risk_class"], int) or isinstance(meta["risk_class"], bool):
        raise ValueError(f"profile {name!r}: metadata.risk_class must be an int")
    for key in ("name", "display_name", "provenance", "confidence"):
        if not isinstance(meta[key], str):
            raise ValueError(f"profile {name!r}: metadata.{key} must be a str")
    for f in _REQUIRED_DATA_FIELDS:
        if f not in raw:
            raise ValueError(f"profile {name!r}: missing data field {f!r}")
    doctrine = raw["doctrine"]
    for key in ("weights", "baselines", "penalty_coeffs"):
        if key not in doctrine:
            raise ValueError(f"profile {name!r}: doctrine missing {key!r}")


def load_profile(name: str = "halee_ramone") -> ProducerProfile:
    """Read ``producers/<name>.json``, validate it, and return a frozen profile.

    Pure and deterministic: a local JSON read plus structural validation, no I/O
    beyond the file, no time/randomness/network. Every collection is freshly
    parsed, so the returned profile never aliases the live module dicts.
    """
    path = _PRODUCERS_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"no producer profile named {name!r} at {path}")
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    _validate(raw, name)
    return ProducerProfile(
        metadata=raw["metadata"],
        kind_scores=raw["kind_scores"],
        nudge_table=_normalize_kinds_sets(raw["nudge_table"]),
        promotion_table=_normalize_kinds_sets(raw["promotion_table"]),
        creative_nudge_cap=raw["creative_nudge_cap"],
        creative_promotion_cap=raw["creative_promotion_cap"],
        risk_penalty=raw["risk_penalty"],
        search_modes=raw["search_modes"],
        philosophy=raw["philosophy"],
        truth_alignment=raw["truth_alignment"],
        taste_kind_bias=raw["taste_kind_bias"],
        taste_max_delta=raw["taste_max_delta"],
        aesthetic_kill_switches=raw["aesthetic_kill_switches"],
        doctrine=raw["doctrine"],
        default_creative_mode=raw["default_creative_mode"],
    )


__all__ = ["ProducerProfile", "load_profile"]
