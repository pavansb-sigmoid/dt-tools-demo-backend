"""
Service to load and cache metadata JSON files from disk.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List


_BASE_DIR = Path(__file__).resolve().parent.parent
_METADATA_DIR = _BASE_DIR / "data" / "metadata"


def _load_json(filename: str) -> Dict[str, Any]:
    """Load JSON file from metadata directory."""
    path = _METADATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_markets() -> Dict[str, List[Dict[str, Any]]]:
    """Return markets data from markets.json (cached)."""
    return _load_json("markets.json")


@lru_cache(maxsize=1)
def get_brands() -> Dict[str, List[Dict[str, Any]]]:
    """Return brands data from brands.json (cached)."""
    return _load_json("brands.json")


@lru_cache(maxsize=1)
def get_time_periods() -> Dict[str, List[Dict[str, Any]]]:
    """Return time periods data from time_periods.json (cached)."""
    return _load_json("time_periods.json")

