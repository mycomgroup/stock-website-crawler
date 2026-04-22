"""
ranking_catalog.py - 排序条件目录管理

管理排序类条件（换手率从高到低、市值从小到大等），
提供排序方向反转、优先级排序能力。
"""

import json
import random
from pathlib import Path
from typing import Optional

CATALOGS_DIR = Path(__file__).resolve().parent / "catalogs"
RANKING_CATALOG_PATH = CATALOGS_DIR / "ranking_catalog.json"

_ranking_cache = None


def load_ranking_catalog() -> dict:
    """Load ranking catalog from JSON file."""
    global _ranking_cache
    if _ranking_cache is not None:
        return _ranking_cache
    
    if RANKING_CATALOG_PATH.exists():
        with open(RANKING_CATALOG_PATH, encoding="utf-8") as f:
            _ranking_cache = json.load(f)
    else:
        _ranking_cache = {"rankings": []}
    
    return _ranking_cache


def get_ranking_conditions(family: Optional[str] = None) -> list[dict]:
    """Get ranking conditions, optionally filtered by family."""
    catalog = load_ranking_catalog()
    rankings = catalog["rankings"]
    if family:
        rankings = [r for r in rankings if r.get("family") == family]
    return rankings


def get_rankings_for_tree(tree_name: str, min_weight: float = 0.3) -> list[dict]:
    """Get rankings relevant to a specific tree."""
    catalog = load_ranking_catalog()
    result = []
    for r in catalog["rankings"]:
        weights = r.get("tree_weights", {})
        if tree_name in weights and weights[tree_name] >= min_weight:
            result.append(r)
        elif not weights:
            result.append(r)
    return result


def reverse_sort_direction(clause: str) -> str:
    """Reverse the sort direction of a ranking clause."""
    reversals = [
        ("从高到低", "从低到高"),
        ("从低到高", "从高到低"),
        ("从大到小", "从小到大"),
        ("从小到大", "从大到小"),
        ("由近到远", "由远到近"),
        ("由远到近", "由近到远"),
    ]
    for old, new in reversals:
        if old in clause:
            return clause.replace(old, new)
    return clause


def sample_ranking_for_tree(tree_name: str, existing: Optional[list[str]] = None) -> Optional[str]:
    """Sample a ranking condition suitable for a tree."""
    existing = existing or []
    existing_set = set(existing)
    
    candidates = get_rankings_for_tree(tree_name)
    candidates = [r for r in candidates if r.get("template") not in existing_set]
    
    if not candidates:
        return None
    
    weights = [r.get("tree_weights", {}).get(tree_name, 0.5) for r in candidates]
    total = sum(weights)
    if total > 0:
        weights = [w / total for w in weights]
    else:
        weights = None
    
    chosen = random.choices(candidates, weights=weights, k=1)[0]
    return chosen.get("template")


def get_ranking_by_id(ranking_id: str) -> Optional[dict]:
    """Get a specific ranking by its ID."""
    catalog = load_ranking_catalog()
    for r in catalog["rankings"]:
        if r.get("id") == ranking_id:
            return r
    return None
