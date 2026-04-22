"""
condition_catalog.py - 统一条件目录管理

从 catalogs/condition_catalog.json 加载结构化条件定义，
提供条件查询、过滤、渲染能力。
"""

import json
import random
from pathlib import Path
from typing import Optional

CATALOGS_DIR = Path(__file__).resolve().parent / "catalogs"
CONDITION_CATALOG_PATH = CATALOGS_DIR / "condition_catalog.json"

_catalog_cache = None


def load_condition_catalog() -> dict:
    """Load condition catalog from JSON file."""
    global _catalog_cache
    if _catalog_cache is not None:
        return _catalog_cache
    
    if CONDITION_CATALOG_PATH.exists():
        with open(CONDITION_CATALOG_PATH, encoding="utf-8") as f:
            _catalog_cache = json.load(f)
    else:
        _catalog_cache = {"conditions": []}
    
    return _catalog_cache


def get_conditions_by_family(family: str) -> list[dict]:
    """Get all conditions belonging to a specific family."""
    catalog = load_condition_catalog()
    return [c for c in catalog["conditions"] if c.get("family") == family]


def get_conditions_for_tree(tree_name: str, min_weight: float = 0.3) -> list[dict]:
    """Get conditions relevant to a specific tree, filtered by minimum weight."""
    catalog = load_condition_catalog()
    result = []
    for c in catalog["conditions"]:
        weights = c.get("tree_weights", {})
        if tree_name in weights and weights[tree_name] >= min_weight:
            result.append(c)
        elif not weights and c.get("family") in ["pool"]:
            result.append(c)
    return result


def get_condition_by_id(cond_id: str) -> Optional[dict]:
    """Get a specific condition by its ID."""
    catalog = load_condition_catalog()
    for c in catalog["conditions"]:
        if c.get("id") == cond_id:
            return c
    return None


def render_condition(cond: dict, params: Optional[dict] = None) -> str:
    """Render a condition template with given parameters."""
    template = cond.get("template", "")
    if params:
        try:
            return template.format(**params)
        except KeyError:
            return template
    return template


def render_condition_with_default(cond: dict) -> str:
    """Render a condition using its default parameter values."""
    template = cond.get("template", "")
    cond_params = cond.get("params", {})
    if not cond_params:
        return template
    
    values = {}
    for param_name, param_def in cond_params.items():
        if "default" in param_def:
            values[param_name] = param_def["default"]
    
    if values:
        try:
            return template.format(**values)
        except KeyError:
            pass
    return template


def check_conflicts(formula: list[str], new_cond: dict) -> list[str]:
    """Check if adding new_cond would conflict with existing formula conditions."""
    conflicts = new_cond.get("conflicts_with", [])
    if not conflicts:
        return []
    
    found_conflicts = []
    for conflict_id in conflicts:
        conflict_cond = get_condition_by_id(conflict_id)
        if conflict_cond:
            conflict_template = conflict_cond.get("template", "")
            for clause in formula:
                if conflict_template.split("{")[0] in clause:
                    found_conflicts.append(conflict_id)
    
    return found_conflicts


def sample_condition_for_tree(tree_name: str, family: Optional[str] = None, stage: str = "coarse", existing: Optional[list[str]] = None) -> Optional[str]:
    """Sample a new condition suitable for a tree, stage, and existing formula."""
    existing = existing or []
    existing_set = set(existing)
    
    candidates = get_conditions_for_tree(tree_name)
    
    if family:
        candidates = [c for c in candidates if c.get("family") == family]
    
    candidates = [c for c in candidates if stage in c.get("stage_fit", [])]
    
    candidates = [c for c in candidates if render_condition_with_default(c) not in existing_set]
    
    if not candidates:
        return None
    
    weights = []
    for c in candidates:
        w = c.get("tree_weights", {}).get(tree_name, 0.5)
        weights.append(w)
    
    total = sum(weights)
    if total > 0:
        weights = [w / total for w in weights]
    else:
        weights = None
    
    chosen = random.choices(candidates, weights=weights, k=1)[0]
    return render_condition_with_default(chosen)


def get_all_families() -> list[str]:
    """Get all unique condition families."""
    catalog = load_condition_catalog()
    families = set()
    for c in catalog["conditions"]:
        families.add(c.get("family", "unknown"))
    return sorted(families)


def get_conditions_by_kind(kind: str) -> list[dict]:
    """Get conditions by kind (filter/pool/ranking)."""
    catalog = load_condition_catalog()
    return [c for c in catalog["conditions"] if c.get("kind") == kind]


def get_addable_conditions(tree_name: str, existing: list[str], stage: str = "coarse") -> list[str]:
    """Get list of addable condition strings for a tree."""
    candidates = get_conditions_for_tree(tree_name)
    existing_set = set(existing)
    result = []
    for c in candidates:
        if stage in c.get("stage_fit", []) and c.get("kind") != "pool":
            rendered = render_condition_with_default(c)
            if rendered not in existing_set:
                result.append(rendered)
    return result


def get_family_for_condition(condition_text: str) -> Optional[str]:
    """Infer the family of a condition string by keyword matching."""
    family_keywords = {
        "valuation": ["市盈率", "市净率", "PEG", "市销率", "估值"],
        "quality": ["ROE", "净资产收益率", "毛利率", "净利率", "盈利"],
        "growth": ["增长率", "增速", "同比", "环比", "增长"],
        "liquidity": ["换手率", "成交额", "成交量", "流动性"],
        "dividend": ["股息", "分红", "分红"],
        "cashflow": ["现金流", "现金流量"],
        "market_cap": ["市值", "流通市值", "总市值"],
        "technical": ["均线", "MACD", "KDJ", "RSI", "布林", "站上"],
        "price": ["涨幅", "跌幅", "股价", "价格"],
        "volume": ["成交量", "量比", "放量", "缩量"],
        "trend": ["多头", "空头", "趋势", "排列"],
        "fund_flow": ["股东户数", "机构持股", "主力", "资金流向", "持仓"],
        "event": ["预增", "扭亏", "中报", "年报", "预案"],
        "risk": ["非ST", "非退市", "非停牌", "资产负债率", "减持"],
        "pool": ["非ST", "非退市", "非科创板", "创业板", "沪深A股"],
    }
    for family, keywords in family_keywords.items():
        for kw in keywords:
            if kw in condition_text:
                return family
    return None


def get_missing_families(formula: list[str], primary_families: list[str]) -> list[str]:
    """Find which primary families are not yet represented in the formula."""
    families_in_formula = set()
    for clause in formula:
        f = get_family_for_condition(clause)
        if f:
            families_in_formula.add(f)
    return [f for f in primary_families if f not in families_in_formula]


def sample_condition_for_family_gap(formula: list[str], primary_families: list[str], tree_name: str, existing: list[str]) -> Optional[str]:
    """Sample a condition from a missing primary family."""
    missing = get_missing_families(formula, primary_families)
    if not missing:
        return None

    family = random.choice(missing)
    return sample_condition_for_tree(tree_name, family=family, existing=existing)
