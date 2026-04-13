"""
果仁网策略配置变异引擎

通过 8 种预定义变异类型生成候选配置，支持智能因子选择和参数调整。

参考设计文档: .kiro/specs/autoresearch-guorn-strategy/design.md

⚠️  此文件为基础设施文件，agent 不可修改。只改配置文件。
"""

import copy
import random
from typing import Optional, Tuple


# ── 因子候选库 ────────────────────────────────────────────────────────────────

# 常用指标（基于果仁网平台实际支持的因子，已验证 ID 映射）
COMMON_INDICATORS = {
    # 估值指标（已验证）
    "pe_ttm": {
        "name": "市盈率",
        "type": "fundamental",
        "operators": ["<", ">"],
        "range": [5, 80],
        "default": 20,
    },
    "pb": {
        "name": "市净率",
        "type": "fundamental",
        "operators": ["<", ">"],
        "range": [0.5, 5],
        "default": 2,
    },
    "ps": {
        "name": "市销率",
        "type": "fundamental",
        "operators": ["<", ">"],
        "range": [0.5, 10],
        "default": 3,
    },
    "pcf": {
        "name": "市现率",
        "type": "fundamental",
        "operators": ["<", ">"],
        "range": [5, 50],
        "default": 15,
    },
    # 盈利指标（已验证）
    "roe": {
        "name": "净资产收益率",
        "type": "fundamental",
        "operators": [">"],
        "range": [5, 30],
        "default": 10,
    },
    "gross_profit_margin": {
        "name": "销售毛利率",
        "type": "fundamental",
        "operators": [">"],
        "range": [10, 80],
        "default": 30,
    },
    "net_profit_margin": {
        "name": "销售净利率",
        "type": "fundamental",
        "operators": [">"],
        "range": [5, 50],
        "default": 10,
    },
    # 成长指标（已验证）
    "revenue_growth": {
        "name": "营业收入增长",
        "type": "fundamental",
        "operators": [">"],
        "range": [5, 50],
        "default": 15,
    },
    "profit_growth": {
        "name": "净利润增长",
        "type": "fundamental",
        "operators": [">"],
        "range": [5, 50],
        "default": 15,
    },
    "operating_profit_growth": {
        "name": "营业利润增长",
        "type": "fundamental",
        "operators": [">"],
        "range": [5, 50],
        "default": 15,
    },
    # 红利指标（已验证）
    "dividend_yield": {
        "name": "股息率",
        "type": "fundamental",
        "operators": [">"],
        "range": [1, 8],
        "default": 2,
    },
    "dividend_yield_ttm": {
        "name": "股息率TTM",
        "type": "fundamental",
        "operators": [">"],
        "range": [1, 8],
        "default": 2,
    },
    # 财务质量指标（已验证）
    "debt_to_equity": {
        "name": "负债资产率",
        "type": "fundamental",
        "operators": ["<"],
        "range": [0.2, 0.8],
        "default": 0.6,
    },
    "current_ratio": {
        "name": "流动比率",
        "type": "fundamental",
        "operators": [">"],
        "range": [1, 5],
        "default": 2,
    },
    "quick_ratio": {
        "name": "速动比率",
        "type": "fundamental",
        "operators": [">"],
        "range": [0.5, 3],
        "default": 1,
    },
    # 市场指标（已验证）
    "turnover_rate": {
        "name": "当日换手率",
        "type": "pricing",
        "operators": ["<", ">"],
        "range": [0.5, 10],
        "default": 2,
    },
    "market_cap": {
        "name": "总市值",
        "type": "pricing",
        "operators": [">"],
        "range": [1000000000, 100000000000],
        "default": 10000000000,
    },
    "circulating_market_cap": {
        "name": "流通市值",
        "type": "pricing",
        "operators": [">"],
        "range": [1000000000, 100000000000],
        "default": 10000000000,
    },
}

# 股票池选项
POOL_OPTIONS = ["hs300", "zz500", "zz1000", "all"]

# 持仓数量选项（限制 5~20）
HOLDING_NUM_OPTIONS = [5, 10, 15, 20]

# 调仓间隔选项（天）
REBALANCE_OPTIONS = [1, 3, 5, 10, 15, 20, 30]

# 变异类型
MUTATION_TYPES = [
    "add_filter",
    "remove_filter",
    "adjust_filter_threshold",
    "add_ranking",
    "adjust_ranking_weight",
    "adjust_holding_num",
    "adjust_rebalance_interval",
    "change_pool",
]


# ── 核心函数 ──────────────────────────────────────────────────────────────────


def mutate(config: dict, mutation_type: Optional[str] = None) -> Tuple[dict, str]:
    """
    生成候选配置。

    Args:
        config: 当前配置
        mutation_type: 变异类型（可选，None 时随机选择）

    Returns:
        (new_config, mutation_description)

    Mutation Types:
        - add_filter: 添加筛选条件
        - remove_filter: 移除筛选条件
        - adjust_filter_threshold: 调整筛选阈值（±20%~±50%）
        - add_ranking: 添加排序规则
        - adjust_ranking_weight: 调整排序权重
        - adjust_holding_num: 调整持仓数量
        - adjust_rebalance_interval: 调整调仓间隔
        - change_pool: 更换股票池
    """
    # 深拷贝配置，避免修改原配置
    new_config = copy.deepcopy(config)

    # 如果未指定变异类型，随机选择
    if mutation_type is None:
        mutation_type = random.choice(MUTATION_TYPES)

    # 根据变异类型调用对应的函数
    if mutation_type == "add_filter":
        return _mutate_add_filter(new_config)
    elif mutation_type == "remove_filter":
        return _mutate_remove_filter(new_config)
    elif mutation_type == "adjust_filter_threshold":
        return _mutate_adjust_filter_threshold(new_config)
    elif mutation_type == "add_ranking":
        return _mutate_add_ranking(new_config)
    elif mutation_type == "adjust_ranking_weight":
        return _mutate_adjust_ranking_weight(new_config)
    elif mutation_type == "adjust_holding_num":
        return _mutate_adjust_holding_num(new_config)
    elif mutation_type == "adjust_rebalance_interval":
        return _mutate_adjust_rebalance_interval(new_config)
    elif mutation_type == "change_pool":
        return _mutate_change_pool(new_config)
    else:
        raise ValueError(f"Unknown mutation type: {mutation_type}")


def _mutate_add_filter(config: dict) -> Tuple[dict, str]:
    """添加筛选条件"""
    filters = config.get("filters", [])
    used_factors = {f["factor"] for f in filters}

    # 找出未使用的因子
    available_factors = [
        factor for factor in COMMON_INDICATORS.keys() if factor not in used_factors
    ]

    if not available_factors:
        # 如果所有因子都已使用，切换到 adjust_filter_threshold
        return _mutate_adjust_filter_threshold(config)

    # 随机选择一个未使用的因子
    factor = random.choice(available_factors)
    indicator = COMMON_INDICATORS[factor]

    # 随机选择操作符
    operator = random.choice(indicator["operators"])

    # 生成阈值（在合理范围内）
    value_range = indicator["range"]
    if operator == "<":
        # 对于 < 操作符，选择范围的中上部分
        value = random.uniform(
            value_range[0] + (value_range[1] - value_range[0]) * 0.3, value_range[1]
        )
    elif operator == ">":
        # 对于 > 操作符，选择范围的中下部分
        value = random.uniform(
            value_range[0], value_range[0] + (value_range[1] - value_range[0]) * 0.7
        )
    else:
        # 默认使用中间值
        value = (value_range[0] + value_range[1]) / 2

    # 添加新的筛选条件
    new_filter = {"factor": factor, "operator": operator, "value": round(value, 2)}
    config["filters"].append(new_filter)

    description = f"[筛选] 添加 {indicator['name']} {operator} {value:.2f}"
    return config, description


def _mutate_remove_filter(config: dict) -> Tuple[dict, str]:
    """移除筛选条件"""
    filters = config.get("filters", [])

    if not filters:
        # 如果没有筛选条件，切换到 add_filter
        return _mutate_add_filter(config)

    # 随机选择一个筛选条件移除
    removed_filter = random.choice(filters)
    config["filters"].remove(removed_filter)

    factor_name = COMMON_INDICATORS.get(removed_filter["factor"], {}).get(
        "name", removed_filter["factor"]
    )
    description = f"[筛选] 移除 {factor_name} {removed_filter['operator']} {removed_filter['value']}"
    return config, description


def _mutate_adjust_filter_threshold(config: dict) -> Tuple[dict, str]:
    """调整筛选阈值（±20%~±50%）"""
    filters = config.get("filters", [])

    if not filters:
        # 如果没有筛选条件，切换到 add_filter
        return _mutate_add_filter(config)

    # 随机选择一个筛选条件
    filter_to_adjust = random.choice(filters)
    old_value = filter_to_adjust["value"]

    # 应用 ±20%~±50% 的乘数
    multiplier = random.uniform(0.5, 1.8)  # 50% ~ 180%
    new_value = old_value * multiplier

    # 确保新值在合理范围内
    factor = filter_to_adjust["factor"]
    if factor in COMMON_INDICATORS:
        value_range = COMMON_INDICATORS[factor]["range"]
        new_value = max(value_range[0], min(value_range[1], new_value))

    filter_to_adjust["value"] = round(new_value, 2)

    factor_name = COMMON_INDICATORS.get(factor, {}).get("name", factor)
    description = f"[筛选] 调整 {factor_name} 阈值 {old_value:.2f} → {new_value:.2f}"
    return config, description


def _mutate_add_ranking(config: dict) -> Tuple[dict, str]:
    """添加排序规则"""
    rankings = config.get("rankings", [])
    used_factors = {r["factor"] for r in rankings}

    # 找出未使用的因子
    available_factors = [
        factor for factor in COMMON_INDICATORS.keys() if factor not in used_factors
    ]

    if not available_factors:
        # 如果所有因子都已使用，切换到 adjust_ranking_weight
        return _mutate_adjust_ranking_weight(config)

    # 随机选择一个未使用的因子
    factor = random.choice(available_factors)
    indicator = COMMON_INDICATORS[factor]

    # 确定排序方向（降序 = False，升序 = True）
    # 对于 ">" 操作符的因子，通常降序排列（值越大越好）
    # 对于 "<" 操作符的因子，通常升序排列（值越小越好）
    if ">" in indicator["operators"]:
        ascending = False  # 降序
    else:
        ascending = True  # 升序

    # 分配权重（如果已有排序规则，平均分配权重）
    if rankings:
        # 重新分配权重
        new_weight = 1.0 / (len(rankings) + 1)
        for r in rankings:
            r["weight"] = new_weight
        weight = new_weight
    else:
        weight = 1.0

    # 添加新的排序规则
    new_ranking = {"factor": factor, "ascending": ascending, "weight": round(weight, 2)}
    config["rankings"].append(new_ranking)

    factor_name = indicator["name"]
    direction = "升序" if ascending else "降序"
    description = f"[排序] 添加 {factor_name}，{direction}，权重 {weight:.2f}"
    return config, description


def _mutate_adjust_ranking_weight(config: dict) -> Tuple[dict, str]:
    """调整排序权重"""
    rankings = config.get("rankings", [])

    if not rankings:
        # 如果没有排序规则，切换到 add_ranking
        return _mutate_add_ranking(config)

    if len(rankings) == 1:
        # 如果只有一个排序规则，权重必须为 1，无法调整
        # 切换到 add_ranking
        return _mutate_add_ranking(config)

    # 随机选择两个排序规则，调整它们的权重
    ranking1, ranking2 = random.sample(rankings, 2)

    # 在两个排序规则之间转移权重（±10%~±30%）
    transfer_amount = random.uniform(0.1, 0.3) * min(
        ranking1["weight"], ranking2["weight"]
    )

    old_weight1 = ranking1["weight"]
    old_weight2 = ranking2["weight"]

    ranking1["weight"] = round(ranking1["weight"] - transfer_amount, 2)
    ranking2["weight"] = round(ranking2["weight"] + transfer_amount, 2)

    # 确保权重总和为 1
    total_weight = sum(r["weight"] for r in rankings)
    if abs(total_weight - 1.0) > 0.01:
        # 归一化权重
        for r in rankings:
            r["weight"] = round(r["weight"] / total_weight, 2)

    factor1_name = COMMON_INDICATORS.get(ranking1["factor"], {}).get(
        "name", ranking1["factor"]
    )
    factor2_name = COMMON_INDICATORS.get(ranking2["factor"], {}).get(
        "name", ranking2["factor"]
    )
    description = (
        f"[排序] 调整权重：{factor1_name} {old_weight1:.2f} → {ranking1['weight']:.2f}，"
        f"{factor2_name} {old_weight2:.2f} → {ranking2['weight']:.2f}"
    )
    return config, description


def _mutate_adjust_holding_num(config: dict) -> Tuple[dict, str]:
    """调整持仓数量"""
    old_holding_num = config.get("holding_num", 15)

    # 从预定义列表中选择新值（排除当前值）
    available_options = [n for n in HOLDING_NUM_OPTIONS if n != old_holding_num]
    if not available_options:
        # 如果没有其他选项，随机增减
        new_holding_num = old_holding_num + random.choice([-5, 5])
        new_holding_num = max(5, min(20, new_holding_num))
    else:
        new_holding_num = random.choice(available_options)

    config["holding_num"] = new_holding_num

    description = f"[持仓] holding_num {old_holding_num} → {new_holding_num}"
    return config, description


def _mutate_adjust_rebalance_interval(config: dict) -> Tuple[dict, str]:
    """调整调仓间隔"""
    old_rebalance_interval = config.get("rebalance_interval", 10)

    # 从预定义列表中选择新值（排除当前值）
    available_options = [n for n in REBALANCE_OPTIONS if n != old_rebalance_interval]
    if not available_options:
        # 如果没有其他选项，随机增减 5
        new_rebalance_interval = old_rebalance_interval + random.choice([-5, 5])
        new_rebalance_interval = max(1, min(30, new_rebalance_interval))
    else:
        new_rebalance_interval = random.choice(available_options)

    config["rebalance_interval"] = new_rebalance_interval

    description = f"[调仓] rebalance_interval {old_rebalance_interval} → {new_rebalance_interval} 天"
    return config, description


def _mutate_change_pool(config: dict) -> Tuple[dict, str]:
    """更换股票池"""
    old_pool = config.get("pool", "hs300")

    # 从预定义列表中选择新值（排除当前值）
    available_options = [p for p in POOL_OPTIONS if p != old_pool]
    if not available_options:
        # 如果没有其他选项，切换到 adjust_holding_num
        return _mutate_adjust_holding_num(config)

    new_pool = random.choice(available_options)
    config["pool"] = new_pool

    pool_names = {
        "hs300": "沪深300",
        "zz500": "中证500",
        "zz1000": "中证1000",
        "all": "全市场",
    }
    old_pool_name = pool_names.get(old_pool, old_pool)
    new_pool_name = pool_names.get(new_pool, new_pool)

    description = f"[股票池] {old_pool_name} → {new_pool_name}"
    return config, description


def validate_config(config: dict) -> bool:
    """
    验证配置合法性。

    Args:
        config: 策略配置

    Returns:
        bool: 配置是否合法
    """
    # 检查必需字段
    required_fields = [
        "name",
        "filters",
        "rankings",
        "pool",
        "holding_num",
        "rebalance_interval",
    ]
    for field in required_fields:
        if field not in config:
            return False

    # 检查 filters 格式
    filters = config.get("filters", [])
    for f in filters:
        if not all(k in f for k in ["factor", "operator", "value"]):
            return False

    # 检查 rankings 格式
    rankings = config.get("rankings", [])
    for r in rankings:
        if not all(k in r for k in ["factor", "ascending", "weight"]):
            return False

    # 检查权重总和
    if rankings:
        total_weight = sum(r["weight"] for r in rankings)
        if abs(total_weight - 1.0) > 0.1:  # 允许 10% 的误差
            return False

    # 检查 pool 在可选列表中
    if config["pool"] not in POOL_OPTIONS:
        return False

    # 检查 holding_num 在合理范围内（5~20）
    if not (5 <= config["holding_num"] <= 20):
        return False

    # 检查 rebalance_interval 在合理范围内
    if not (1 <= config["rebalance_interval"] <= 30):
        return False

    return True


def load_factor_library(catalog_path: Optional[str] = None) -> dict:
    """
    从 GUORN_INDICATORS_CATALOG.md 加载因子库。

    Args:
        catalog_path: 因子库文件路径（可选）

    Returns:
        dict: 因子库字典
            {
                "common_indicators": {...}
            }

    Note:
        当前版本使用硬编码的因子库，未来可以从文件加载
    """
    return {
        "common_indicators": COMMON_INDICATORS,
    }
