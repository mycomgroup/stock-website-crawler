"""
wizard_mutator.py — 向导式策略配置变异器（只读基础设施）

本模块为 autoresearch-ricequant-wizard 系统提供 8 种 JSON 参数变异类型，
用于生成候选 wizard_config.json 配置。不依赖外部服务，纯本地计算。

新增功能：
- 预估候选池数量，自动调整筛选条件确保候选池在合理范围
- 候选太少（< min）→ 放宽筛选条件
- 候选太多（> max）→ 收紧筛选条件
"""

import copy
import random

# ---------------------------------------------------------------------------
# 因子候选库
# ---------------------------------------------------------------------------

FACTOR_CANDIDATES = {
    # ======================== fundamental ========================
    # 估值指标
    "pe_ratio": {
        "type": "fundamental",
        "operators": ["less_than", "in_range"],
        "range": [5, 80],
        "default_rhs": 20,
    },
    "pb_ratio": {
        "type": "fundamental",
        "operators": ["less_than", "in_range"],
        "range": [0.5, 5],
        "default_rhs": 2,
    },
    "ps_ratio": {
        "type": "fundamental",
        "operators": ["less_than"],
        "range": [0.5, 10],
        "default_rhs": 3,
    },
    "pcf_ratio": {
        "type": "fundamental",
        "operators": ["less_than"],
        "range": [5, 50],
        "default_rhs": 15,
    },
    "market_cap": {
        "type": "fundamental",
        "operators": ["greater_than", "less_than"],
        "range": [5e8, 1e11],
        "default_rhs": 1e9,
    },
    "circulating_market_cap": {
        "type": "fundamental",
        "operators": ["greater_than", "less_than"],
        "range": [5e8, 1e11],
        "default_rhs": 1e9,
    },
    "capitalization": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1e8, 1e10],
        "default_rhs": 1e9,
    },
    "circulating_cap": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1e8, 1e10],
        "default_rhs": 5e8,
    },
    # 盈利能力
    "roe": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [5, 30],
        "default_rhs": 10,
    },
    "roa": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [2, 20],
        "default_rhs": 5,
    },
    "gross_profit_margin": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [10, 60],
        "default_rhs": 20,
    },
    "net_profit_margin": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [5, 40],
        "default_rhs": 10,
    },
    "operating_profit_margin": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [5, 40],
        "default_rhs": 10,
    },
    "ebit_margin": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [5, 50],
        "default_rhs": 15,
    },
    "net_profit_after_tax": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1e7, 1e10],
        "default_rhs": 1e8,
    },
    # 成长能力
    "revenue_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 50],
        "default_rhs": 10,
    },
    "net_profit_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 50],
        "default_rhs": 10,
    },
    "operating_profit_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 50],
        "default_rhs": 10,
    },
    "total_assets_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 40],
        "default_rhs": 8,
    },
    "total_profit_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 50],
        "default_rhs": 10,
    },
    "net_profit_growth_rate_1y": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 100],
        "default_rhs": 20,
    },
    "revenue_growth_rate_1y": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 100],
        "default_rhs": 15,
    },
    # 财务健康
    "debt_ratio": {
        "type": "fundamental",
        "operators": ["less_than"],
        "range": [20, 70],
        "default_rhs": 50,
    },
    "current_ratio": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.5, 5],
        "default_rhs": 1.5,
    },
    "quick_ratio": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.3, 3],
        "default_rhs": 1,
    },
    "equity_ratio": {
        "type": "fundamental",
        "operators": ["less_than"],
        "range": [0.5, 3],
        "default_rhs": 1.5,
    },
    "tangible_asset_ratio": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.3, 1.0],
        "default_rhs": 0.6,
    },
    "interest_coverage_ratio": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 20],
        "default_rhs": 5,
    },
    # 营运能力
    "inventory_turnover": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 20],
        "default_rhs": 5,
    },
    "accounts_receivable_turnover": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 50],
        "default_rhs": 10,
    },
    "asset_turnover": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.2, 3],
        "default_rhs": 0.8,
    },
    # 现金流
    "operating_cash_flow_per_share": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.1, 5],
        "default_rhs": 0.5,
    },
    "free_cash_flow_per_share": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.1, 5],
        "default_rhs": 0.5,
    },
    "cash_flow_to_debt": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.1, 2],
        "default_rhs": 0.5,
    },
    "operating_cash_flow_growth_rate": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [-20, 100],
        "default_rhs": 10,
    },
    # 分红指标
    "dividend_yield": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 8],
        "default_rhs": 2,
    },
    "dividend_payout_ratio": {
        "type": "fundamental",
        "operators": ["greater_than", "less_than"],
        "range": [10, 80],
        "default_rhs": 30,
    },
    # 每股指标
    "eps": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.1, 10],
        "default_rhs": 0.5,
    },
    "book_value_per_share": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 50],
        "default_rhs": 5,
    },
    "revenue_per_share": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [1, 50],
        "default_rhs": 10,
    },
    "operating_profit_per_share": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.5, 20],
        "default_rhs": 2,
    },
    # 分析师预测
    "target_price": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [5, 500],
        "default_rhs": 50,
    },
    "rating": {
        "type": "fundamental",
        "operators": ["less_than"],
        "range": [1, 5],
        "default_rhs": 2,
    },
    "eps_forecast": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0.1, 10],
        "default_rhs": 1,
    },
    "revenue_forecast_growth": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 50],
        "default_rhs": 10,
    },
    "net_profit_forecast_growth": {
        "type": "fundamental",
        "operators": ["greater_than"],
        "range": [0, 100],
        "default_rhs": 20,
    },
    # ======================== pricing ========================
    # 价格指标
    "open": {
        "type": "pricing",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    "close": {
        "type": "pricing",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    "high": {
        "type": "pricing",
        "operators": ["greater_than"],
        "range": [1, 500],
        "default_rhs": 25,
    },
    "low": {
        "type": "pricing",
        "operators": ["less_than"],
        "range": [1, 500],
        "default_rhs": 15,
    },
    "last": {
        "type": "pricing",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    "limit_up": {
        "type": "pricing",
        "operators": ["greater_than"],
        "range": [1, 500],
        "default_rhs": 30,
    },
    "limit_down": {
        "type": "pricing",
        "operators": ["less_than"],
        "range": [1, 500],
        "default_rhs": 10,
    },
    # 成交量指标
    "volume": {
        "type": "pricing",
        "operators": ["greater_than"],
        "range": [1e6, 1e9],
        "default_rhs": 1e7,
    },
    "turnover": {
        "type": "pricing",
        "operators": ["greater_than"],
        "range": [1e6, 1e9],
        "default_rhs": 1e7,
    },
    "turnover_rate": {
        "type": "pricing",
        "operators": ["greater_than", "less_than"],
        "range": [0.5, 15],
        "default_rhs": 3,
    },
    # 涨跌指标
    "change_rate": {
        "type": "pricing",
        "operators": ["greater_than", "less_than"],
        "range": [-10, 10],
        "default_rhs": 0,
    },
    "n_day_gain_rate": {
        "type": "pricing",
        "operators": ["greater_than", "less_than", "in_range"],
        "range": [-30, 30],
        "default_rhs": 5,
    },
    "high_52w": {
        "type": "pricing",
        "operators": ["greater_than"],
        "range": [5, 500],
        "default_rhs": 50,
    },
    "low_52w": {
        "type": "pricing",
        "operators": ["less_than"],
        "range": [1, 200],
        "default_rhs": 20,
    },
    # ======================== technical ========================
    # 趋势指标
    "MA": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    "EMA": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    "MACD": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [-5, 5],
        "default_rhs": 0,
    },
    "ADX": {
        "type": "technical",
        "operators": ["greater_than"],
        "range": [0, 100],
        "default_rhs": 25,
    },
    "TRIX": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [-1, 1],
        "default_rhs": 0,
    },
    # 动量指标
    "RSI": {
        "type": "technical",
        "operators": ["less_than", "greater_than", "in_range"],
        "range": [0, 100],
        "default_rhs": 30,
    },
    "CCI": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [-300, 300],
        "default_rhs": -100,
    },
    "KDJ": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [0, 100],
        "default_rhs": 20,
    },
    "WILLR": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [-100, 0],
        "default_rhs": -80,
    },
    "MFI": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [0, 100],
        "default_rhs": 20,
    },
    # 波动率指标
    "ATR": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [0.5, 20],
        "default_rhs": 3,
    },
    "BOLL": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [0, 100],
        "default_rhs": 20,
    },
    "STDDEV": {
        "type": "technical",
        "operators": ["less_than", "greater_than"],
        "range": [0.5, 10],
        "default_rhs": 2,
    },
    "SAR": {
        "type": "technical",
        "operators": ["greater_than", "less_than"],
        "range": [1, 500],
        "default_rhs": 20,
    },
    # 成交量类指标
    "OBV": {
        "type": "technical",
        "operators": ["greater_than"],
        "range": [-1e8, 1e8],
        "default_rhs": 0,
    },
    # ======================== extra ========================
    "listed_days": {
        "type": "extra",
        "operators": ["greater_than"],
        "range": [30, 3650],
        "default_rhs": 180,
    },
}

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

UNIVERSE_OPTIONS = ["000300.XSHG", "000905.XSHG", "000852.XSHG", "*"]
UNIVERSE_SIZE_MAP = {
    "000300.XSHG": 300,
    "000905.XSHG": 500,
    "000852.XSHG": 1000,
    "*": 5000,
}
HOLDING_NUM_OPTIONS = [5, 10, 15, 20, 25, 30]
REBALANCE_OPTIONS = [1, 3, 5, 10, 15, 20, 30]
MUTATION_TYPES = [
    "add_filter",
    "remove_filter",
    "adjust_filter_threshold",
    "add_sorting",
    "adjust_sorting_weight",
    "adjust_holding_num",
    "adjust_rebalance_interval",
    "change_universe",
]

DEFAULT_CANDIDATE_NUM_MIN = 5
DEFAULT_CANDIDATE_NUM_MAX = 50


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def estimate_candidate_pool_size(config: dict) -> int:
    """
    预估候选池数量（启发式方法）。

    基于：
    - universe 基础池大小
    - filters 数量和严格程度

    Args:
        config: wizard_config 配置字典

    Returns:
        int: 预估的候选池数量（筛选后、排序前）
    """
    universe_list = config.get("universe", ["000300.XSHG"])
    universe = universe_list[0] if universe_list else "000300.XSHG"
    base_size = UNIVERSE_SIZE_MAP.get(universe, 300)

    filters = config.get("filters", [])
    if not filters:
        return base_size

    candidate_size = float(base_size)

    for f in filters:
        operator = f.get("operator", "")
        rhs = f.get("rhs", 10)
        factor_name = f.get("factor", {}).get("name", "")

        reduction_factor = 0.8

        factor_info = FACTOR_CANDIDATES.get(factor_name)
        if factor_info:
            lo, hi = factor_info["range"]
            range_span = hi - lo

            if operator == "less_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                reduction_factor = max(0.1, min(0.95, 0.3 + normalized * 0.5))
            elif operator == "greater_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                reduction_factor = max(0.1, min(0.95, 0.95 - normalized * 0.6))
            elif operator == "in_range":
                if isinstance(rhs, list) and len(rhs) >= 2:
                    range_width = (rhs[1] - rhs[0]) / range_span if range_span > 0 else 0.2
                    reduction_factor = max(0.1, min(0.95, 0.3 + range_width * 0.4))

        candidate_size *= reduction_factor

    return int(candidate_size)


def relax_filter(config: dict) -> tuple[dict, str]:
    """
    放宽筛选条件（用于候选池太少时）。
    优先选择最严格的 filter 进行放宽：
    - less_than: 提高 rhs 阈值
    - greater_than: 降低 rhs 阈值
    - in_range: 扩大范围

    若 filters 为空，则回退到 change_universe（扩大股票池）。
    """
    new_config = copy.deepcopy(config)
    filters = new_config.setdefault("filters", [])

    if not filters:
        return change_universe(new_config)

    strictness_scores = []
    for i, f in enumerate(filters):
        operator = f.get("operator", "")
        rhs = f.get("rhs", 10)
        factor_name = f.get("factor", {}).get("name", "")

        score = 0.5
        factor_info = FACTOR_CANDIDATES.get(factor_name)
        if factor_info:
            lo, hi = factor_info["range"]
            range_span = hi - lo

            if operator == "less_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                score = 1.0 - normalized  # 阈值越低，越严格
            elif operator == "greater_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                score = normalized  # 阈值越高，越严格

        strictness_scores.append((score, i))

    strictness_scores.sort(reverse=True)
    idx = strictness_scores[0][1]
    f = filters[idx]

    operator = f.get("operator", "")
    old_rhs = f.get("rhs", 10)
    factor_name = f.get("factor", {}).get("name", "")

    factor_info = FACTOR_CANDIDATES.get(factor_name)

    if operator == "less_than":
        multiplier = random.uniform(1.3, 1.8)
        new_rhs = old_rhs * multiplier
        if factor_info:
            lo, hi = factor_info["range"]
            new_rhs = _clamp(new_rhs, lo, hi)
        f["rhs"] = round(new_rhs, 4)
        desc = f"relax_filter: {factor_name} less_than {old_rhs} -> {new_rhs}"

    elif operator == "greater_than":
        multiplier = random.uniform(0.5, 0.7)
        new_rhs = old_rhs * multiplier
        if factor_info:
            lo, hi = factor_info["range"]
            new_rhs = _clamp(new_rhs, lo, hi)
        f["rhs"] = round(new_rhs, 4)
        desc = f"relax_filter: {factor_name} greater_than {old_rhs} -> {new_rhs}"

    elif operator == "in_range":
        if isinstance(old_rhs, list) and len(old_rhs) >= 2:
            expansion = (old_rhs[1] - old_rhs[0]) * random.uniform(0.3, 0.5)
            new_rhs = [old_rhs[0] - expansion, old_rhs[1] + expansion]
            if factor_info:
                lo, hi = factor_info["range"]
                new_rhs[0] = _clamp(new_rhs[0], lo, hi)
                new_rhs[1] = _clamp(new_rhs[1], lo, hi)
            f["rhs"] = [round(new_rhs[0], 4), round(new_rhs[1], 4)]
            desc = f"relax_filter: {factor_name} in_range [{old_rhs[0]}, {old_rhs[1]}] -> [{new_rhs[0]}, {new_rhs[1]}]"
        else:
            desc = f"relax_filter: {factor_name} (invalid in_range)"

    else:
        return adjust_filter_threshold(new_config)

    return new_config, desc


def tighten_filter(config: dict) -> tuple[dict, str]:
    """
    收紧筛选条件（用于候选池太多时）。
    优先选择最宽松的 filter 进行收紧，或添加新 filter。

    收紧方式：
    - less_than: 降低 rhs 阈值
    - greater_than: 提高 rhs 阈值
    - in_range: 缩小范围
    - 或直接 add_filter
    """
    new_config = copy.deepcopy(config)
    filters = new_config.setdefault("filters", [])

    if not filters:
        return add_filter(new_config)

    if len(filters) >= 6:
        return adjust_filter_threshold(new_config)

    looseness_scores = []
    for i, f in enumerate(filters):
        operator = f.get("operator", "")
        rhs = f.get("rhs", 10)
        factor_name = f.get("factor", {}).get("name", "")

        score = 0.5
        factor_info = FACTOR_CANDIDATES.get(factor_name)
        if factor_info:
            lo, hi = factor_info["range"]
            range_span = hi - lo

            if operator == "less_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                score = normalized  # 阈值越高，越宽松
            elif operator == "greater_than":
                normalized = (rhs - lo) / range_span if range_span > 0 else 0.5
                score = 1.0 - normalized  # 阈值越低，越宽松

        looseness_scores.append((score, i))

    looseness_scores.sort(reverse=True)

    if looseness_scores and looseness_scores[0][0] > 0.7:
        idx = looseness_scores[0][1]
        f = filters[idx]

        operator = f.get("operator", "")
        old_rhs = f.get("rhs", 10)
        factor_name = f.get("factor", {}).get("name", "")

        factor_info = FACTOR_CANDIDATES.get(factor_name)

        if operator == "less_than":
            multiplier = random.uniform(0.5, 0.7)
            new_rhs = old_rhs * multiplier
            if factor_info:
                lo, hi = factor_info["range"]
                new_rhs = _clamp(new_rhs, lo, hi)
            f["rhs"] = round(new_rhs, 4)
            desc = f"tighten_filter: {factor_name} less_than {old_rhs} -> {new_rhs}"

        elif operator == "greater_than":
            multiplier = random.uniform(1.3, 1.8)
            new_rhs = old_rhs * multiplier
            if factor_info:
                lo, hi = factor_info["range"]
                new_rhs = _clamp(new_rhs, lo, hi)
            f["rhs"] = round(new_rhs, 4)
            desc = f"tighten_filter: {factor_name} greater_than {old_rhs} -> {new_rhs}"

        elif operator == "in_range":
            if isinstance(old_rhs, list) and len(old_rhs) >= 2:
                shrink = (old_rhs[1] - old_rhs[0]) * random.uniform(0.2, 0.4)
                new_rhs = [old_rhs[0] + shrink, old_rhs[1] - shrink]
                if factor_info:
                    lo, hi = factor_info["range"]
                    new_rhs[0] = _clamp(new_rhs[0], lo, hi)
                    new_rhs[1] = _clamp(new_rhs[1], lo, hi)
                f["rhs"] = [round(new_rhs[0], 4), round(new_rhs[1], 4)]
                desc = f"tighten_filter: {factor_name} in_range [{old_rhs[0]}, {old_rhs[1]}] -> [{new_rhs[0]}, {new_rhs[1]}]"
            else:
                desc = f"tighten_filter: {factor_name} (invalid in_range)"
        else:
            return add_filter(new_config)

        return new_config, desc

    else:
        return add_filter(new_config)


def _used_factor_names(items: list) -> set:
    """从 filters 或 sorting 列表中提取已使用的因子名称集合。"""
    return {item["factor"]["name"] for item in items if "factor" in item}


def _clamp(value: float, lo: float, hi: float) -> float:
    """将 value 限制在 [lo, hi] 范围内。"""
    return max(lo, min(hi, value))


def _random_rhs(factor_name: str) -> float:
    """在因子的合法范围内生成一个随机 rhs 值。"""
    info = FACTOR_CANDIDATES.get(factor_name)
    if info is None:
        return 10.0
    lo, hi = info["range"]
    return round(random.uniform(lo, hi), 4)


def _adjust_multiplier() -> float:
    """随机生成 ±20%~±50% 的调整乘数（避开 [0.8, 1.2] 区间）。"""
    # 从 [0.5, 0.8] 或 [1.2, 1.5] 中随机选一段
    if random.random() < 0.5:
        return random.uniform(0.5, 0.8)
    else:
        return random.uniform(1.2, 1.5)


# ---------------------------------------------------------------------------
# 8 种变异函数
# ---------------------------------------------------------------------------


def add_filter(config: dict) -> tuple[dict, str]:
    """
    新增一个筛选条件。
    若所有候选因子已在 filters 中使用，则回退到 adjust_filter_threshold。
    """
    new_config = copy.deepcopy(config)
    filters = new_config.setdefault("filters", [])

    used = _used_factor_names(filters)
    available = [name for name in FACTOR_CANDIDATES if name not in used]

    if not available:
        return adjust_filter_threshold(new_config)

    factor_name = random.choice(available)
    info = FACTOR_CANDIDATES[factor_name]
    operator = random.choice(info["operators"])
    rhs = _random_rhs(factor_name)

    new_filter = {
        "operator": operator,
        "factor": {"type": info["type"], "name": factor_name},
        "rhs": rhs,
    }
    filters.append(new_filter)

    desc = f"add_filter: {factor_name} {operator} {rhs}"
    return new_config, desc


def remove_filter(config: dict) -> tuple[dict, str]:
    """
    移除一个随机筛选条件。
    若 filters 为空，则回退到 add_filter。
    """
    new_config = copy.deepcopy(config)
    filters = new_config.setdefault("filters", [])

    if not filters:
        return add_filter(new_config)

    idx = random.randrange(len(filters))
    removed = filters.pop(idx)
    factor_name = removed.get("factor", {}).get("name", "unknown")
    operator = removed.get("operator", "")

    desc = f"remove_filter: {factor_name} {operator}"
    return new_config, desc


def adjust_filter_threshold(config: dict) -> tuple[dict, str]:
    """
    调整某个筛选条件的 rhs 值（±20%~±50%）。
    若 filters 为空，则回退到 add_filter。
    """
    new_config = copy.deepcopy(config)
    filters = new_config.setdefault("filters", [])

    if not filters:
        return add_filter(new_config)

    idx = random.randrange(len(filters))
    f = filters[idx]
    factor_name = f.get("factor", {}).get("name", "")
    old_rhs = f.get("rhs", 10)

    multiplier = _adjust_multiplier()
    new_rhs = old_rhs * multiplier

    # 若因子在候选库中，限制在合法范围内
    if factor_name in FACTOR_CANDIDATES:
        lo, hi = FACTOR_CANDIDATES[factor_name]["range"]
        new_rhs = _clamp(new_rhs, lo, hi)

    new_rhs = round(new_rhs, 4)
    f["rhs"] = new_rhs

    desc = f"adjust_filter_threshold: {factor_name} rhs {old_rhs} -> {new_rhs}"
    return new_config, desc


def add_sorting(config: dict) -> tuple[dict, str]:
    """
    新增一个排序规则。
    若所有候选因子已在 sorting 中使用，则回退到 adjust_sorting_weight。
    """
    new_config = copy.deepcopy(config)
    sorting = new_config.setdefault("sorting", [])

    used = _used_factor_names(sorting)
    available = [name for name in FACTOR_CANDIDATES if name not in used]

    if not available:
        return adjust_sorting_weight(new_config)

    factor_name = random.choice(available)
    info = FACTOR_CANDIDATES[factor_name]
    ascending = random.choice([True, False])

    new_rule = {
        "factor": {"type": info["type"], "name": factor_name},
        "ascending": ascending,
        "weight": 0.3,
    }
    sorting.append(new_rule)

    direction = "asc" if ascending else "desc"
    desc = f"add_sorting: {factor_name} {direction} weight=0.3"
    return new_config, desc


def adjust_sorting_weight(config: dict) -> tuple[dict, str]:
    """
    调整某个排序规则的权重（±20%~±50%，最小值 0.1）。
    若 sorting 为空，则回退到 add_sorting。
    """
    new_config = copy.deepcopy(config)
    sorting = new_config.setdefault("sorting", [])

    if not sorting:
        return add_sorting(new_config)

    idx = random.randrange(len(sorting))
    rule = sorting[idx]
    old_weight = rule.get("weight", 0.3)

    multiplier = _adjust_multiplier()
    new_weight = max(0.1, round(old_weight * multiplier, 4))
    rule["weight"] = new_weight

    factor_name = rule.get("factor", {}).get("name", "unknown")
    desc = f"adjust_sorting_weight: {factor_name} weight {old_weight} -> {new_weight}"
    return new_config, desc


def adjust_holding_num(config: dict) -> tuple[dict, str]:
    """
    调整最大持仓数量，从 HOLDING_NUM_OPTIONS 中选一个不同的值。
    """
    new_config = copy.deepcopy(config)
    current = new_config.get("maxHoldingNum", 15)

    options = [v for v in HOLDING_NUM_OPTIONS if v != current]
    if not options:
        options = HOLDING_NUM_OPTIONS  # 极端情况：全部相同，随机选一个

    new_value = random.choice(options)
    new_config["maxHoldingNum"] = new_value

    desc = f"adjust_holding_num: {current} -> {new_value}"
    return new_config, desc


def adjust_rebalance_interval(config: dict) -> tuple[dict, str]:
    """
    调整调仓间隔，从 REBALANCE_OPTIONS 中选一个不同的值。
    """
    new_config = copy.deepcopy(config)
    current = new_config.get("rebalanceInterval", 10)

    options = [v for v in REBALANCE_OPTIONS if v != current]
    if not options:
        options = REBALANCE_OPTIONS

    new_value = random.choice(options)
    new_config["rebalanceInterval"] = new_value

    desc = f"adjust_rebalance_interval: {current} -> {new_value}"
    return new_config, desc


def change_universe(config: dict) -> tuple[dict, str]:
    """
    切换股票池，从 UNIVERSE_OPTIONS 中选一个不同的值。
    若只有一个选项可用，则回退到 adjust_holding_num。
    """
    new_config = copy.deepcopy(config)

    # 当前 universe 可能是列表，取第一个元素作为当前值
    current_list = new_config.get("universe", ["000300.XSHG"])
    current = current_list[0] if current_list else "000300.XSHG"

    options = [v for v in UNIVERSE_OPTIONS if v != current]
    if not options:
        return adjust_holding_num(new_config)

    new_universe = random.choice(options)
    new_config["universe"] = [new_universe]

    desc = f"change_universe: {current} -> {new_universe}"
    return new_config, desc


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

_DISPATCH = {
    "add_filter": add_filter,
    "remove_filter": remove_filter,
    "adjust_filter_threshold": adjust_filter_threshold,
    "add_sorting": add_sorting,
    "adjust_sorting_weight": adjust_sorting_weight,
    "adjust_holding_num": adjust_holding_num,
    "adjust_rebalance_interval": adjust_rebalance_interval,
    "change_universe": change_universe,
    "relax_filter": relax_filter,
    "tighten_filter": tighten_filter,
}


def smart_mutate(
    config: dict,
    candidate_num_min: int = DEFAULT_CANDIDATE_NUM_MIN,
    candidate_num_max: int = DEFAULT_CANDIDATE_NUM_MAX,
) -> tuple[dict, str]:
    """
    智能变异：根据候选池数量自动选择合适的变异类型。

    Args:
        config: 当前 champion 配置
        candidate_num_min: 候选池最小数量（默认 5）
        candidate_num_max: 候选池最大数量（默认 50）

    Returns:
        (new_config, description)
    """
    estimated_size = estimate_candidate_pool_size(config)

    if estimated_size < candidate_num_min:
        return relax_filter(config)
    elif estimated_size > candidate_num_max:
        return tighten_filter(config)
    else:
        return mutate(config)


def mutate(config: dict, mutation_type: str = None) -> tuple[dict, str]:
    """
    对 wizard_config 执行一次变异，返回 (new_config, mutation_description)。

    Args:
        config: 当前 champion 配置（不会被修改）。
        mutation_type: 指定变异类型；为 None 时随机选择。

    Returns:
        (new_config, description) — new_config 是深拷贝后的新配置，
        description 是人类可读的变异描述字符串。
    """
    if mutation_type is None:
        base_types = [
            "add_filter",
            "remove_filter",
            "adjust_filter_threshold",
            "add_sorting",
            "adjust_sorting_weight",
            "adjust_holding_num",
            "adjust_rebalance_interval",
            "change_universe",
        ]
        mutation_type = random.choice(base_types)

    fn = _DISPATCH.get(mutation_type)
    if fn is None:
        raise ValueError(f"未知的变异类型: {mutation_type!r}，合法值: {MUTATION_TYPES}")

    return fn(config)
