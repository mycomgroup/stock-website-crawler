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
import math
from typing import Optional, Tuple, List, Dict


class ConditionTemplateEngine:
    """动态条件生成器 - 基于模板生成和解析 formula 条件"""

    INDICATOR_TEMPLATES = {
        "周成交量环比增长率": {
            "pattern": r"周成交量环比增长率大于(\d+(?:\.\d+)?)%",
            "range": [1, 20],
            "default": 8,
            "template": "周成交量环比增长率大于{value}%",
            "category": "growth",
        },
        "涨幅": {
            "pattern": r"近(\d+)天的涨幅大于(\d+(?:\.\d+)?)%小于(\d+(?:\.\d+)?)%",
            "range_low": [0, 10],
            "range_high": [10, 30],
            "default_low": 0,
            "default_high": 20,
            "template": "近{days}天的涨幅大于{low}%小于{high}%",
            "category": "price",
        },
        "上市时间": {
            "pattern": r"上市时间大于(\d+)天",
            "range": [100, 1000],
            "default": 300,
            "template": "上市时间大于{value}天",
            "category": "time",
        },
        "成交额": {
            "pattern": r"成交额大于(\d+)(万|亿)",
            "range": [100, 10000],
            "default": 1000,
            "template": "成交额大于{value}万",
            "category": "volume",
        },
        "流通市值": {
            "pattern": r"流通市值小于(\d+)亿",
            "range": [10, 500],
            "default": 100,
            "template": "流通市值小于{value}亿",
            "category": "market_cap",
        },
        "换手率": {
            "pattern": r"换手率大于(\d+(?:\.\d+)?)%",
            "range": [1, 20],
            "default": 5,
            "template": "换手率大于{value}%",
            "category": "turnover",
        },
        "市盈率": {
            "pattern": r"市盈率小于(\d+)",
            "range": [10, 100],
            "default": 30,
            "template": "市盈率小于{value}",
            "category": "valuation",
        },
        "市净率": {
            "pattern": r"市净率小于(\d+(?:\.\d+)?)",
            "range": [1, 10],
            "default": 3,
            "template": "市净率小于{value}",
            "category": "valuation",
        },
        "净资产收益率": {
            "pattern": r"净资产收益率大于(\d+(?:\.\d+)?)%",
            "range": [5, 30],
            "default": 10,
            "template": "净资产收益率大于{value}%",
            "category": "profitability",
        },
        "毛利率": {
            "pattern": r"毛利率大于(\d+(?:\.\d+)?)%",
            "range": [10, 80],
            "default": 30,
            "template": "毛利率大于{value}%",
            "category": "profitability",
        },
        "净利润增长率": {
            "pattern": r"净利润增长率大于(\d+(?:\.\d+)?)%",
            "range": [0, 100],
            "default": 20,
            "template": "净利润增长率大于{value}%",
            "category": "growth",
        },
        "营业收入增长率": {
            "pattern": r"营业收入增长率大于(\d+(?:\.\d+)?)%",
            "range": [0, 100],
            "default": 15,
            "template": "营业收入增长率大于{value}%",
            "category": "growth",
        },
    }

    COMPARATORS = ["大于", "小于", "等于"]

    TIME_WINDOWS = [1, 3, 5, 10, 20, 30, 60]

    DYNAMIC_INDICATORS = {
        "成交量": {"range": (100, 10000), "unit": "万", "comparator": "大于", "category": "volume"},
        "振幅": {"range": (2, 15), "unit": "%", "comparator": "大于", "category": "volatility"},
        "量比": {"range": (1, 5), "unit": "", "comparator": "大于", "category": "volume"},
        "委比": {"range": (-50, 50), "unit": "%", "comparator": "大于", "category": "sentiment"},
        "均价": {"range": (5, 100), "unit": "元", "comparator": "大于", "category": "price"},
        "总市值": {"range": (20, 1000), "unit": "亿", "comparator": "小于", "category": "market_cap"},
        "流通股本": {"range": (1, 50), "unit": "亿", "comparator": "小于", "category": "market_cap"},
        "总股本": {"range": (1, 100), "unit": "亿", "comparator": "小于", "category": "market_cap"},
        "股息率": {"range": (1, 8), "unit": "%", "comparator": "大于", "category": "dividend"},
        "资产负债率": {"range": (20, 80), "unit": "%", "comparator": "小于", "category": "risk"},
        "速动比率": {"range": (0.5, 3), "unit": "", "comparator": "大于", "category": "risk"},
        "流动比率": {"range": (1, 5), "unit": "", "comparator": "大于", "category": "risk"},
    }

    POOL_CONDITIONS = [
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

    ADDABLE_CONDITIONS = [
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
        "经营活动产生的现金流量净额大于0",
        "经营活动产生的现金流量净额大于净利润",
        "经营活动产生的现金流量净额连续三年为正",
        "市盈率大于0小于20",
        "市盈率大于0小于25",
        "动态市盈率大于0小于20",
        "PEG小于1",
        "PEG小于1.5",
        "净利润同比增速递增",
        "扣非净利润同比转正",
        "最近两年经营活动产生的现金流量净额大于净利润",
        "最近两年营业收入同比增长率均大于10%",
        "最近8个季度净利润同比增长率均大于20%",
        "最近两个季度净利润同比增长率持续改善",
        "最近三个季度归属母公司股东净利润同比增长率大于20%",
        "最近一个季度净利润同比增长率大于20%",
        "换手率从高到低",
        "换手率从低到高",
        "市值从小到大",
        "市值从大到小",
        "成交额从大到小",
        "成交额从小到大",
    ]

    def __init__(self):
        self._compiled_patterns = {}
        for name, template in self.INDICATOR_TEMPLATES.items():
            self._compiled_patterns[name] = re.compile(template["pattern"])

    def parse_condition(self, clause: str) -> Optional[Dict]:
        """解析单个条件子句，返回结构化信息"""
        for name, pattern in self._compiled_patterns.items():
            match = pattern.search(clause)
            if match:
                params = {"condition_name": name, "category": self.INDICATOR_TEMPLATES[name].get("category", "unknown")}
                if name == "涨幅":
                    params["days"] = int(match.group(1))
                    params["low"] = float(match.group(2))
                    params["high"] = float(match.group(3))
                else:
                    params["value"] = float(match.group(1))
                    if len(match.groups()) > 1 and match.group(2):
                        params["unit"] = match.group(2)
                return params
        return None

    def generate_condition(self, existing: List[str], category: Optional[str] = None) -> str:
        """动态生成一个不在 existing 中的新条件"""
        existing_set = set(existing)

        if category:
            candidates = [name for name, t in self.INDICATOR_TEMPLATES.items() if t.get("category") == category]
        else:
            candidates = list(self.INDICATOR_TEMPLATES.keys())

        random.shuffle(candidates)

        for name in candidates:
            template = self.INDICATOR_TEMPLATES[name]
            condition = self._generate_from_template(name, template)
            if condition not in existing_set:
                return condition

        for name, indicator in self.DYNAMIC_INDICATORS.items():
            if category and indicator.get("category") != category:
                continue
            condition = self._generate_dynamic_condition(name, indicator)
            if condition not in existing_set:
                return condition

        pool_candidates = [c for c in self.POOL_CONDITIONS if c not in existing_set]
        if pool_candidates:
            return random.choice(pool_candidates)

        return self._generate_fallback_condition(existing)

    def _generate_from_template(self, name: str, template: Dict) -> str:
        """从预定义模板生成条件"""
        if name == "涨幅":
            days = random.choice(self.TIME_WINDOWS)
            low = random.uniform(template["range_low"][0], template["range_low"][1])
            high = random.uniform(template["range_high"][0], template["range_high"][1])
            if low >= high:
                high = low + 5
            return template["template"].format(days=days, low=round(low, 1), high=round(high, 1))
        else:
            value = random.uniform(template["range"][0], template["range"][1])
            return template["template"].format(value=int(value))

    def _generate_dynamic_condition(self, name: str, indicator: Dict) -> str:
        """从动态指标生成条件"""
        low, high = indicator["range"]
        value = random.uniform(low, high)
        unit = indicator["unit"]
        comparator = indicator["comparator"]

        if unit == "%":
            return f"{name}{comparator}{int(value)}%"
        elif unit == "万":
            return f"{name}{comparator}{int(value)}万"
        elif unit == "亿":
            return f"{name}{comparator}{int(value)}亿"
        elif unit == "元":
            return f"{name}{comparator}{int(value)}元"
        else:
            if value == int(value):
                return f"{name}{comparator}{int(value)}"
            return f"{name}{comparator}{round(value, 2)}"

    def _generate_fallback_condition(self, existing: List[str]) -> str:
        """兜底条件生成"""
        fallbacks = [
            "换手率大于3%",
            "成交额大于800万",
            "流通市值小于150亿",
            "市盈率小于40",
            "市净率小于4",
        ]
        existing_set = set(existing)
        for fb in fallbacks:
            if fb not in existing_set:
                return fb
        return f"换手率大于{random.randint(2, 8)}%"

    def mutate_value(self, condition_name: str, current_value: float, exploration_rate: float = 0.3) -> float:
        """变异数值，支持局部和全局探索"""
        template = self.INDICATOR_TEMPLATES.get(condition_name)
        if not template:
            return current_value * random.uniform(0.7, 1.3)

        if random.random() < exploration_rate:
            low, high = template["range"]
            return random.uniform(low, high)
        else:
            multiplier = random.uniform(0.7, 1.3)
            new_value = current_value * multiplier
            low, high = template["range"]
            return max(low, min(high, new_value))


class AdaptiveMutationStrategy:
    """自适应变异策略选择器 - 使用 UCB1 算法"""

    def __init__(self):
        self.strategy_rewards: Dict[str, List[float]] = {
            "adjust_formula_threshold": [],
            "add_formula_condition": [],
            "remove_formula_condition": [],
            "adjust_formula_sort": [],
            "replace_formula_condition": [],
            "adjust_days_for_sale": [],
            "adjust_max_positions": [],
            "adjust_daily_buy_count": [],
            "adjust_take_profit": [],
            "adjust_stop_loss": [],
            "adjust_trailing_stop": [],
        }
        self.total_pulls = 0
        self.condition_engine = ConditionTemplateEngine()

    def select_mutation_type(self, formula: Optional[List[str]] = None) -> str:
        """使用 UCB1 算法选择变异类型"""
        available = list(self.strategy_rewards.keys())

        if formula:
            available = self._filter_available_types(available, formula)

        for strategy in available:
            if len(self.strategy_rewards[strategy]) == 0:
                return strategy

        ucb_values = {}
        for strategy in available:
            rewards = self.strategy_rewards[strategy]
            avg_reward = sum(rewards) / len(rewards)
            exploration_bonus = math.sqrt(2 * math.log(self.total_pulls) / len(rewards))
            ucb_values[strategy] = avg_reward + exploration_bonus

        return max(ucb_values, key=ucb_values.get)

    def record_reward(self, mutation_type: str, score_delta: float) -> None:
        """记录变异策略的得分变化"""
        if mutation_type not in self.strategy_rewards:
            self.strategy_rewards[mutation_type] = []
        self.strategy_rewards[mutation_type].append(score_delta)
        self.total_pulls += 1

    def get_strategy_stats(self) -> Dict[str, Dict]:
        """获取各策略的统计信息"""
        stats = {}
        for strategy, rewards in self.strategy_rewards.items():
            if rewards:
                stats[strategy] = {
                    "count": len(rewards),
                    "avg_reward": sum(rewards) / len(rewards),
                    "max_reward": max(rewards),
                    "min_reward": min(rewards),
                }
            else:
                stats[strategy] = {"count": 0, "avg_reward": 0, "max_reward": 0, "min_reward": 0}
        return stats

    def _filter_available_types(self, available: List[str], formula: List[str]) -> List[str]:
        """根据当前 formula 过滤可用的变异类型"""
        has_sort = any(
            kw in clause
            for clause in formula
            for kw in ["从大到小", "从小到大", "由近到远", "由远到近", "从高到低", "从低到高"]
        )

        if not has_sort and "adjust_formula_sort" in available:
            available.remove("adjust_formula_sort")

        if len(formula) <= 2 and "remove_formula_condition" in available:
            available.remove("remove_formula_condition")

        return available


global_adaptive_strategy = AdaptiveMutationStrategy()


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
    # B4 branch: 现金流质量
    "经营活动产生的现金流量净额大于0",
    "经营活动产生的现金流量净额大于净利润",
    "经营活动产生的现金流量净额连续三年为正",
    # B5 branch: 戴维斯双击/PEG
    "市盈率大于0小于20",
    "市盈率大于0小于25",
    "动态市盈率大于0小于20",
    "PEG小于1",
    "PEG小于1.5",
    "净利润同比增速递增",
    "扣非净利润同比转正",
    "最近两年经营活动产生的现金流量净额大于净利润",
    "最近两年营业收入同比增长率均大于10%",
    "最近8个季度净利润同比增长率均大于20%",
    "最近两个季度净利润同比增长率持续改善",
    "最近三个季度归属母公司股东净利润同比增长率大于20%",
    "最近一个季度净利润同比增长率大于20%",
    # 排序条件
    "换手率从高到低",
    "换手率从低到高",
    "市值从小到大",
    "市值从大到小",
    "成交额从大到小",
    "成交额从小到大",
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


def mutate(
    config: dict, mutation_type: Optional[str] = None, mutation_hint: Optional[str] = None
) -> Tuple[dict, str, str]:
    """
    生成候选配置。

    Args:
        config: 当前配置
        mutation_type: 变异类型（可选，None 时使用自适应策略选择）
        mutation_hint: 额外提示，例如 add_formula_condition 时指定具体条件

    Returns:
        (new_config, mutation_description, actual_mutation_type)
    """
    new_config = copy.deepcopy(config)

    raw_type = mutation_type
    if raw_type and raw_type.startswith("add_formula_condition:"):
        raw_type = "add_formula_condition"
        mutation_hint = mutation_type.split(":", 1)[1]
    elif raw_type and raw_type.startswith("remove_formula_condition:"):
        raw_type = "remove_formula_condition"
        mutation_hint = mutation_type.split(":", 1)[1]
    elif raw_type and raw_type.startswith("replace_formula_condition:"):
        raw_type = "replace_formula_condition"
        mutation_hint = mutation_type.split(":", 1)[1]

    if raw_type is None:
        raw_type = global_adaptive_strategy.select_mutation_type(config.get("formula", []))

    dispatch = {
        "adjust_formula_threshold": _mutate_adjust_formula_threshold,
        "add_formula_condition": _mutate_add_formula_condition,
        "remove_formula_condition": _mutate_remove_formula_condition,
        "adjust_formula_sort": _mutate_adjust_formula_sort,
        "replace_formula_condition": _mutate_replace_formula_condition,
        "adjust_days_for_sale": _mutate_adjust_days_for_sale,
        "adjust_max_positions": _mutate_adjust_max_positions,
        "adjust_daily_buy_count": _mutate_adjust_daily_buy_count,
        "adjust_take_profit": _mutate_adjust_take_profit,
        "adjust_stop_loss": _mutate_adjust_stop_loss,
        "adjust_trailing_stop": _mutate_adjust_trailing_stop,
    }

    fn = dispatch.get(raw_type)
    if fn is None:
        raise ValueError(f"Unknown mutation type: {raw_type}")

    if raw_type == "add_formula_condition" and mutation_hint:
        result_config, desc = _mutate_add_formula_condition(new_config, specified_condition=mutation_hint)
        return result_config, desc, raw_type
    if raw_type == "remove_formula_condition" and mutation_hint:
        result_config, desc = _mutate_remove_formula_condition(new_config, specified_clause=mutation_hint)
        return result_config, desc, raw_type
    if raw_type == "replace_formula_condition" and mutation_hint:
        parts = mutation_hint.split("->", 1)
        if len(parts) == 2:
            result_config, desc = _mutate_replace_formula_condition(
                new_config, old_clause=parts[0].strip(), new_clause=parts[1].strip()
            )
        else:
            result_config, desc = _mutate_replace_formula_condition(new_config)
        return result_config, desc, raw_type

    result_config, desc = fn(new_config)
    return result_config, desc, raw_type


def _find_numeric_condition(formula: List[str]) -> Tuple[int, str, dict, dict]:
    """
    在 formula 中找到数值条件及其参数。

    Returns:
        (index, original_text, extracted_params, condition_def)
        或 (-1, "", {}, {}) 如果没找到
    """
    engine = ConditionTemplateEngine()

    for i, clause in enumerate(formula):
        params = engine.parse_condition(clause)
        if params:
            cond_name = params["condition_name"]
            cond_def = FORMULA_NUMERIC_CONDITIONS.get(cond_name, {})
            if cond_def:
                return i, clause, params, cond_def

    for i, clause in enumerate(formula):
        for cond_name in FORMULA_NUMERIC_CONDITIONS:
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
    engine = ConditionTemplateEngine()

    if cond_name == "涨幅":
        old_low = params["low"]
        old_high = params["high"]
        new_low = round(engine.mutate_value(cond_name, old_low), 1)
        new_high = round(engine.mutate_value(cond_name, old_high), 1)
        if new_low >= new_high:
            new_high = new_low + 10
        new_clause = cond_def["template"].format(days=params["days"], low=new_low, high=new_high)
        desc = f"[筛选阈值] 涨幅 {old_low}%~{old_high}% → {new_low}%~{new_high}%"
    else:
        old_value = params["value"]
        new_value = round(engine.mutate_value(cond_name, old_value), 0)
        new_clause = cond_def["template"].format(value=int(new_value))
        desc = f"[筛选阈值] {cond_name} {old_value} → {int(new_value)}"

    formula[idx] = new_clause
    config["formula"] = formula

    return config, desc


def _mutate_add_formula_condition(config: dict, specified_condition: Optional[str] = None) -> Tuple[dict, str]:
    """添加新的 formula 条件"""
    formula = config.get("formula", [])
    engine = ConditionTemplateEngine()

    existing_text = set(formula)

    if specified_condition and specified_condition not in existing_text:
        new_condition = specified_condition
    else:
        new_condition = engine.generate_condition(formula)

    if new_condition in engine.POOL_CONDITIONS:
        formula.insert(0, new_condition)
    else:
        insert_idx = len(formula) - len(
            [c for c in formula if "从大到小" in c or "由近到远" in c or "从小到大" in c or "由远到近" in c]
        )
        insert_idx = max(0, min(len(formula) - 1, insert_idx))
        formula.insert(insert_idx, new_condition)

    config["formula"] = formula
    desc = f"[添加条件] {new_condition}"

    return config, desc


def _mutate_remove_formula_condition(config: dict, specified_clause: Optional[str] = None) -> Tuple[dict, str]:
    """移除 formula 条件"""
    formula = config.get("formula", [])
    if len(formula) <= 3:
        return _mutate_adjust_formula_threshold(config)

    if specified_clause and specified_clause in formula:
        idx = formula.index(specified_clause)
        removed_clause = formula[idx]
        formula.pop(idx)
        config["formula"] = formula
        return config, f"[移除条件] {removed_clause}"

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


def _mutate_replace_formula_condition(
    config: dict, old_clause: Optional[str] = None, new_clause: Optional[str] = None
) -> Tuple[dict, str]:
    """替换 formula 中的某个条件为另一个条件"""
    formula = config.get("formula", [])
    if not formula:
        return _mutate_add_formula_condition(config)

    if old_clause and old_clause in formula:
        idx = formula.index(old_clause)
        formula[idx] = new_clause or old_clause
        config["formula"] = formula
        return config, f"[替换条件] {old_clause} → {new_clause}"

    replaceable_indices = []
    for i, clause in enumerate(formula):
        if clause not in ["非ST", "非科创板", "非退市", "沪深A股"]:
            replaceable_indices.append(i)

    if not replaceable_indices or not new_clause:
        return _mutate_add_formula_condition(config)

    idx = random.choice(replaceable_indices)
    old = formula[idx]
    formula[idx] = new_clause
    config["formula"] = formula
    return config, f"[替换条件] {old} → {new_clause}"


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


def record_mutation_reward(mutation_type: str, score_delta: float) -> None:
    """记录变异得分变化，用于自适应策略学习"""
    global_adaptive_strategy.record_reward(mutation_type, score_delta)


def get_adaptive_stats() -> Dict[str, Dict]:
    """获取自适应策略统计信息"""
    return global_adaptive_strategy.get_strategy_stats()


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
