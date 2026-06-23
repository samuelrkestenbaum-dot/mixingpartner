"""Doctrine package: the Halee/Ramone philosophy as loadable data + a scorer."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

_DIR = Path(__file__).parent


@lru_cache(maxsize=None)
def load_doctrine(name: str) -> Dict:
    """Load a doctrine JSON by stem name, e.g. ``load_doctrine("roy_halee")``."""
    path = _DIR / f"{name}.json"
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


__all__ = ["load_doctrine"]
