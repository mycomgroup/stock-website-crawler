"""
问财公式回测配置变异引擎

通过多种变异类型生成候选配置，支持 formula 数组和回测参数的变异。

变异类型分类：
1. Formula 条件变异（核心）
   - adjust_formula_threshold: 调整数值条件阈值
   - add_formula_condition: 添加新筛选条件
   - remove_formula_condition: 移除筛选条件
   - adjust_formula_sort: 调整排序条件

2. 回测参数变异
   - adjust_days_for_sale: 调整持仓天数策略
   - adjust_max_positions: 调整最大持仓数
   - adjust_daily_buy_count: 调整每日买入数
   - adjust_take_profit: 调整止盈阈值
   - adjust_stop_loss: 调整止损阈值
   - adjust_trailing_stop: 调整追踪止损阈值
"""

import copy
import re
import random
from typing import Optional, Tuple, List, Dict


FORMULA_NUMERIC_CONDITIONS = {
    "周成交量环比增长率": {
        "pattern": r"周成交量环比增长率大于(\d+(?:\.\d+)?)%",
        "range": [1, 20],
        "default": 8,
        "template": "周成交量环比增长率大于{value}%",
    },
    "涨幅": {
        "pattern": r"近(\d+)天的涨幅大于(\d+(?:\.\d+)?)%小于(\d+(?:\.\d+)?)%",
        "range_low": [0, 10],
        "range_high": [10, 30],
        "default_low": 0,
        "default_high": 20,
        "template": "近{days}天的涨幅大于{low}%小于{high}%",
    },
    "上市时间": {
        "pattern": r"上市时间大于(\d+)天",
        "range": [100, 1000],
        "default": 300,
        "template": "上市时间大于{value}天",
    },
    "成交额": {
        "pattern": r"成交额大于(\d+)(万|亿)",
        "range": [100, 10000],
        "default": 1000,
        "template": "成交额大于{value}万",
    },
    "流通市值": {
        "pattern": r"流通市值小于(\d+)亿",
        "range": [10, 500],
        "default": 100,
        "template": "流通市值小于{value}亿",
    },
    "换手率": {
        "pattern": r"换手率大于(\d+(?:\.\d+)?)%",
        "range": [1, 20],
        "default": 5,
        "template": "换手率大于{value}%",
    },
    "市盈率": {
        "pattern": r"市盈率小于(\d+)",
        "range": [10, 100],
        "default": 30,
        "template": "市盈率小于{value}",
    },
    "市净率": {
        "pattern": r"市净率小于(\d+(?:\.\d+)?)",
        "range": [1, 10],
        "default": 3,
        "template": "市净率小于{value}",
    },
    "净资产收益率": {
        "pattern": r"净资产收益率大于(\d+(?:\.\d+)?)%",
        "range": [5, 30],
        "default": 10,
        "template": "净资产收益率大于{value}%",
    },
    "毛利率": {
        "pattern": r"毛利率大于(\d+(?:\.\d+)?)%",
        "range": [10, 80],
        "default": 30,
        "template": "毛利率大于{value}%",
    },
    "净利润增长率": {
        "pattern": r"净利润增长率大于(\d+(?:\.\d+)?)%",
        "range": [0, 100],
        "default": 20,
        "template": "净利润增长率大于{value}%",
    },
    "营业收入增长率": {
        "pattern": r"营业收入增长率大于(\d+(?:\.\d+)?)%",
        "range": [0, 100],
        "default": 15,
        "template": "营业收入增长率大于{value}%",
    },
}

FORMULA_POOL_CONDITIONS = [
    "创业板",
    "非ST",
    "非科创板",
    "非退市",
    "沪深A股",
    "中证500",
    "沪深300",
    "热点概念",
    "次新股",
    "高送转预期",
    "破发股",
    "破净股",
]

FORMULA_SORT_CONDITIONS = {
    "涨跌幅": {
        "patterns": ["未来\\d+天涨跌幅从大到小", "涨跌幅从大到小"],
        "template_asc": "涨跌幅从小到大",
        "template_desc": "涨跌幅从大到小",
    },
    "龙脊线百分比": {
        "patterns": ["龙脊线百分比由近到远", "龙脊线百分比由远到近"],
        "template_asc": "龙脊线百分比由远到近",
        "template_desc": "龙脊线百分比由近到远",
    },
    "市值": {
        "patterns": ["市值从小到大", "市值从大到小"],
        "template_asc": "市值从小到大",
        "template_desc": "市值从大到小",
    },
    "换手率": {
        "patterns": ["换手率从高到低", "换手率从低到高"],
        "template_asc": "换手率从低到高",
        "template_desc": "换手率从高到低",
    },
    "成交额": {
        "patterns": ["成交额从大到小", "成交额从小到大"],
        "template_asc": "成交额从小到大",
        "template_desc": "成交额从大到小",
    },
}

FORMULA_ADDABLE_CONDITIONS = [
    "换手率大于5%",
    "换手率大于8%",
    "换手率小于10%",
    "成交额大于1000万",
    "成交额大于5000万",
    "流通市值小于50亿",
    "流通市值小于100亿",
    "流通市值小于200亿",
    "市盈率小于30",
    "市盈率小于50",
    "市净率小于3",
    "市净率小于5",
    "净资产收益率大于10%",
    "净资产收益率大于15%",
    "毛利率大于30%",
    "毛利率大于50%",
    "净利润增长率大于20%",
    "净利润增长率大于30%",
    "营业收入增长率大于15%",
    "营业收入增长率大于30%",
    "非科创板",
    "非退市",
    "破发股",
    "破净股",
    "次新股",
]

DAYS_FOR_SALE_OPTIONS = ["1", "2", "3", "2,3", "3,5", "5,10"]
MAX_POSITIONS_OPTIONS = [1, 2, 3, 5, 10]
DAILY_BUY_COUNT_OPTIONS = [1, 2, 3, 5]
TAKE_PROFIT_OPTIONS = [10, 15, 20, 25, 30, 35, 40]
STOP_LOSS_OPTIONS = [5, 7, 9, 10, 12, 15]
TRAILING_STOP_OPTIONS = [3, 5, 7, 8, 10]

FORMULA_MUTATION_TYPES = [
    "adjust_formula_threshold",
    "add_formula_condition",
    "remove_formula_condition",
    "adjust_formula_sort",
]

PARAM_MUTATION_TYPES = [
    "adjust_days_for_sale",
    "adjust_max_positions",
    "adjust_daily_buy_count",
    "adjust_take_profit",
    "adjust_stop_loss",
    "adjust_trailing_stop",
]

MUTATION_TYPES = FORMULA_MUTATION_TYPES + PARAM_MUTATION_TYPES


def mutate(config: dict, mutation_type: Optional[str] = None) -> Tuple[dict, str]:
    """
    生成候选配置。

    Args:
        config: 当前配置
        mutation_type: 变异类型（可选，None 时随机选择）

    Returns:
        (new_config, mutation_description)
    """
    new_config = copy.deepcopy(config)

    if mutation_type is None:
        formula_weight = 0.6
        if random.random() < formula_weight:
            mutation_type = random.choice(FORMULA_MUTATION_TYPES)
        else:
            mutation_type = random.choice(PARAM_MUTATION_TYPES)

    dispatch = {
        "adjust_formula_threshold": _mutate_adjust_formula_threshold,
        "add_formula_condition": _mutate_add_formula_condition,
        "remove_formula_condition": _mutate_remove_formula_condition,
        "adjust_formula_sort": _mutate_adjust_formula_sort,
        "adjust_days_for_sale": _mutate_adjust_days_for_sale,
        "adjust_max_positions": _mutate_adjust_max_positions,
        "adjust_daily_buy_count": _mutate_adjust_daily_buy_count,
        "adjust_take_profit": _mutate_adjust_take_profit,
        "adjust_stop_loss": _mutate_adjust_stop_loss,
        "adjust_trailing_stop": _mutate_adjust_trailing_stop,
    }

    fn = dispatch.get(mutation_type)
    if fn is None:
        raise ValueError(f"Unknown mutation type: {mutation_type}")

    return fn(new_config)


def _find_numeric_condition(formula: List[str]) -> Tuple[int, str, dict, dict]:
    """
    在 formula 中找到数值条件及其参数。

    Returns:
        (index, original_text, extracted_params, condition_def)
        或 (-1, "", {}, {}) 如果没找到
    """
    numeric_conditions = [
        "周成交量环比增长率",
        "涨幅",
        "上市时间",
        "成交额",
        "流通市值",
        "换手率",
        "市盈率",
        "市净率",
        "净资产收益率",
        "毛利率",
        "净利润增长率",
        "营业收入增长率",
    ]

    for i, clause in enumerate(formula):
        for cond_name in numeric_conditions:
            if cond_name in FORMULA_NUMERIC_CONDITIONS:
                cond_def = FORMULA_NUMERIC_CONDITIONS[cond_name]
                match = re.search(cond_def["pattern"], clause)
                if match:
                    params = {"condition_name": cond_name}
                    if cond_name == "涨幅":
                        params["days"] = int(match.group(1))
                        params["low"] = float(match.group(2))
                        params["high"] = float(match.group(3))
                    else:
                        params["value"] = float(match.group(1))
                        if len(match.groups()) > 1 and match.group(2):
                            params["unit"] = match.group(2)
                    return i, clause, params, cond_def

    return -1, "", {}, {}


def _mutate_adjust_formula_threshold(config: dict) -> Tuple[dict, str]:
    """调整 formula 数值条件阈值"""
    formula = config.get("formula", [])
    if not formula:
        return _mutate_adjust_max_positions(config)

    idx, orig_clause, params, cond_def = _find_numeric_condition(formula)
    if idx == -1:
        return _mutate_add_formula_condition(config)

    cond_name = params.get("condition_name", "")

    if cond_name == "涨幅":
        old_low = params["low"]
        old_high = params["high"]
        multiplier = random.uniform(0.7, 1.3)
        new_low = round(max(cond_def["range_low"][0], min(cond_def["range_low"][1], old_low * multiplier)), 1)
        multiplier = random.uniform(0.7, 1.3)
        new_high = round(max(cond_def["range_high"][0], min(cond_def["range_high"][1], old_high * multiplier)), 1)
        if new_low >= new_high:
            new_high = new_low + 10
        new_clause = cond_def["template"].format(days=params["days"], low=new_low, high=new_high)
        desc = f"[筛选阈值] 涨幅 {old_low}%~{old_high}% → {new_low}%~{new_high}%"
    else:
        old_value = params["value"]
        multiplier = random.uniform(0.7, 1.3)
        new_value = round(max(cond_def["range"][0], min(cond_def["range"][1], old_value * multiplier)), 1)
        new_clause = cond_def["template"].format(value=new_value)
        desc = f"[筛选阈值] {cond_name} {old_value} → {new_value}"

    formula[idx] = new_clause
    config["formula"] = formula

    return config, desc


def _mutate_add_formula_condition(config: dict) -> Tuple[dict, str]:
    """添加新的 formula 条件"""
    formula = config.get("formula", [])

    existing_text = set(formula)
    available = [c for c in FORMULA_ADDABLE_CONDITIONS if c not in existing_text]

    pool_conditions = [c for c in available if c in FORMULA_POOL_CONDITIONS]
    other_conditions = [c for c in available if c not in FORMULA_POOL_CONDITIONS]

    if other_conditions:
        new_condition = random.choice(other_conditions)
        insert_idx = len(formula) - len(
            [c for c in formula if "从大到小" in c or "由近到远" in c or "从小到大" in c or "由远到近" in c]
        )
        insert_idx = max(0, min(len(formula) - 1, insert_idx))
        formula.insert(insert_idx, new_condition)
    elif pool_conditions:
        new_condition = random.choice(pool_conditions)
        formula.insert(0, new_condition)
    else:
        return _mutate_adjust_formula_threshold(config)

    config["formula"] = formula
    desc = f"[添加条件] {new_condition}"

    return config, desc


def _mutate_remove_formula_condition(config: dict) -> Tuple[dict, str]:
    """移除 formula 条件"""
    formula = config.get("formula", [])
    if len(formula) <= 3:
        return _mutate_adjust_formula_threshold(config)

    removable_indices = []
    for i, clause in enumerate(formula):
        if clause in FORMULA_POOL_CONDITIONS:
            removable_indices.append(i)
        elif any(
            cond in clause
            for cond in [
                "增长率",
                "涨幅",
                "上市时间",
                "成交额",
                "市值",
                "换手率",
                "市盈率",
                "市净率",
                "收益率",
                "毛利率",
                "净利率",
            ]
        ):
            removable_indices.append(i)

    if not removable_indices:
        return _mutate_adjust_formula_threshold(config)

    idx = random.choice(removable_indices)
    removed_clause = formula[idx]
    formula.pop(idx)
    config["formula"] = formula

    desc = f"[移除条件] {removed_clause}"

    return config, desc


def _mutate_adjust_formula_sort(config: dict) -> Tuple[dict, str]:
    """调整 formula 排序条件"""
    formula = config.get("formula", [])

    sort_indices = []
    for i, clause in enumerate(formula):
        if any(kw in clause for kw in ["从大到小", "从小到大", "由近到远", "由远到近", "从高到低", "从低到高"]):
            sort_indices.append(i)

    if not sort_indices:
        return _mutate_add_formula_condition(config)

    idx = random.choice(sort_indices)
    orig_clause = formula[idx]

    if "从大到小" in orig_clause:
        new_clause = orig_clause.replace("从大到小", "从小到大")
    elif "从小到大" in orig_clause:
        new_clause = orig_clause.replace("从小到大", "从大到小")
    elif "由近到远" in orig_clause:
        new_clause = orig_clause.replace("由近到远", "由远到近")
    elif "由远到近" in orig_clause:
        new_clause = orig_clause.replace("由远到近", "由近到远")
    elif "从高到低" in orig_clause:
        new_clause = orig_clause.replace("从高到低", "从低到高")
    elif "从低到高" in orig_clause:
        new_clause = orig_clause.replace("从低到高", "从高到低")
    else:
        return _mutate_adjust_formula_threshold(config)

    formula[idx] = new_clause
    config["formula"] = formula

    desc = f"[排序方向] {orig_clause} → {new_clause}"

    return config, desc


def _mutate_adjust_days_for_sale(config: dict) -> Tuple[dict, str]:
    """调整持仓天数策略"""
    old_value = config.get("daysForSaleStrategy", "2,3")

    available = [opt for opt in DAYS_FOR_SALE_OPTIONS if opt != old_value]
    if not available:
        parts = old_value.split(",")
        if len(parts) == 1:
            new_val = str(int(parts[0]) + random.choice([-1, 1]))
            new_val = max(1, min(10, int(new_val)))
            new_value = str(new_val)
        else:
            new_value = old_value
    else:
        new_value = random.choice(available)

    config["daysForSaleStrategy"] = new_value

    desc = f"[持仓天数] {old_value} → {new_value}"
    return config, desc


def _mutate_adjust_max_positions(config: dict) -> Tuple[dict, str]:
    """调整最大持仓数"""
    old_value = config.get("maxPositions", 2)

    available = [opt for opt in MAX_POSITIONS_OPTIONS if opt != old_value]
    if not available:
        new_value = old_value + random.choice([-1, 1])
        new_value = max(1, min(20, new_value))
    else:
        new_value = random.choice(available)

    config["maxPositions"] = new_value

    desc = f"[最大持仓] {old_value} → {new_value}"
    return config, desc


def _mutate_adjust_daily_buy_count(config: dict) -> Tuple[dict, str]:
    """调整每日买入数"""
    old_value = config.get("dailyBuyCount", 2)

    available = [opt for opt in DAILY_BUY_COUNT_OPTIONS if opt != old_value]
    if not available:
        new_value = old_value + random.choice([-1, 1])
        new_value = max(1, min(10, new_value))
    else:
        new_value = random.choice(available)

    config["dailyBuyCount"] = new_value

    desc = f"[每日买入] {old_value} → {new_value}"
    return config, desc


def _mutate_adjust_take_profit(config: dict) -> Tuple[dict, str]:
    """调整止盈阈值"""
    old_value = config.get("takeProfit", 25)

    available = [opt for opt in TAKE_PROFIT_OPTIONS if opt != old_value]
    if not available:
        multiplier = random.uniform(0.7, 1.3)
        new_value = int(old_value * multiplier)
        new_value = max(5, min(50, new_value))
    else:
        new_value = random.choice(available)

    config["takeProfit"] = new_value

    desc = f"[止盈] {old_value}% → {new_value}%"
    return config, desc


def _mutate_adjust_stop_loss(config: dict) -> Tuple[dict, str]:
    """调整止损阈值"""
    old_value = config.get("stopLoss", 9)

    available = [opt for opt in STOP_LOSS_OPTIONS if opt != old_value]
    if not available:
        multiplier = random.uniform(0.7, 1.3)
        new_value = int(old_value * multiplier)
        new_value = max(3, min(20, new_value))
    else:
        new_value = random.choice(available)

    config["stopLoss"] = new_value

    desc = f"[止损] {old_value}% → {new_value}%"
    return config, desc


def _mutate_adjust_trailing_stop(config: dict) -> Tuple[dict, str]:
    """调整追踪止损阈值"""
    old_value = config.get("trailingStopLoss", 5)

    available = [opt for opt in TRAILING_STOP_OPTIONS if opt != old_value]
    if not available:
        multiplier = random.uniform(0.7, 1.3)
        new_value = int(old_value * multiplier)
        new_value = max(2, min(15, new_value))
    else:
        new_value = random.choice(available)

    config["trailingStopLoss"] = new_value

    desc = f"[追踪止损] {old_value}% → {new_value}%"
    return config, desc


def validate_config(config: dict) -> bool:
    """验证配置合法性"""
    required_fields = ["formula", "startDate", "endDate"]
    for field in required_fields:
        if field not in config:
            return False

    if not isinstance(config.get("formula"), list):
        return False

    if len(config.get("formula", [])) < 2:
        return False

    if config.get("maxPositions", 2) < 1 or config.get("maxPositions", 2) > 20:
        return False

    if config.get("dailyBuyCount", 2) < 1 or config.get("dailyBuyCount", 2) > 10:
        return False

    if config.get("takeProfit", 25) < 5 or config.get("takeProfit", 25) > 50:
        return False

    if config.get("stopLoss", 9) < 3 or config.get("stopLoss", 9) > 20:
        return False

    if config.get("trailingStopLoss", 5) < 2 or config.get("trailingStopLoss", 5) > 15:
        return False

    return True
