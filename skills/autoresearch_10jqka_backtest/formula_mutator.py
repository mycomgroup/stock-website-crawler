"""
问财公式回测配置变异引擎

通过多种变异类型生成候选配置，支持 formula 数组和回测参数的变异。

变异类型分类：
1. Formula 条件变异（核心）
   - adjust_formula_threshold: 调整数值条件阈值
   - add_formula_condition: 添加新筛选条件
   - remove_formula_condition: 移除筛选条件
   - adjust_formula_sort: 调整排序条件
   - simplify_formula: 移除冗余条件
   - coarse_threshold_adjust: 大步长阈值调整
   - fine_threshold_adjust: 小步长阈值调整
   - probe_stability: 探测稳定性

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
import json
from dataclasses import dataclass, asdict
from typing import Optional, Tuple, List, Dict
from pathlib import Path

from condition_catalog import get_addable_conditions, sample_condition_for_tree, get_conditions_for_tree
from ranking_catalog import sample_ranking_for_tree, get_rankings_for_tree
from tree_profile import load_tree_profile_from_dir, get_primary_families, get_secondary_families, check_promotion_rules, get_soft_prior_value


GROWTH_STEP = 5
PROFITABILITY_STEP = 2
VALUATION_STEP = 5
TURNOVER_STEP = 1
MARKET_CAP_STEP = 20
PRICE_STEP = 5


CONDITION_CATEGORIES = {
    "周成交量环比增长率": "growth",
    "涨幅": "price",
    "上市时间": "time",
    "成交额": "volume",
    "流通市值": "market_cap",
    "换手率": "turnover",
    "市盈率": "valuation",
    "市净率": "valuation",
    "净资产收益率": "profitability",
    "毛利率": "profitability",
    "净利润增长率": "growth",
    "营业收入增长率": "growth",
}


SEMANTIC_EQUIVALENCE = {
    "市盈率": ["动态市盈率", "静态市盈率", "滚动市盈率"],
    "市净率": ["PB", "账面价值比"],
    "流通市值": ["自由流通市值"],
}


def format_numeric_value(value: float) -> str:
    rounded = round(float(value), 4)
    if abs(rounded - round(rounded)) < 1e-9:
        return str(int(round(rounded)))
    return f"{rounded:.4f}".rstrip("0").rstrip(".")


def replace_last_numeric_token(clause: str, new_value: float) -> str:
    matches = list(re.finditer(r"\d+(?:\.\d+)?", clause))
    if not matches:
        return clause
    last = matches[-1]
    replacement = format_numeric_value(new_value)
    return clause[: last.start()] + replacement + clause[last.end() :]


@dataclass
class SeedMetadata:
    """Metadata constraining valid mutations for a seed direction."""
    core_formula: list[str]
    locked_formula: list[str]
    forbidden_formula: list[str]
    parameter_ranges: dict[str, tuple]
    parameter_priors: dict[str, any]
    expected_holding_profile: str
    expected_position_range: tuple


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

    def get_step_size(self, condition_name: str, fine_tuning: bool = False) -> float:
        """Get step size for a condition category"""
        category = CONDITION_CATEGORIES.get(condition_name, "")
        
        if fine_tuning:
            step_map = {
                "growth": 2,
                "profitability": 1,
                "valuation": 2,
                "turnover": 0.5,
                "market_cap": 10,
                "price": 2,
            }
        else:
            step_map = {
                "growth": GROWTH_STEP,
                "profitability": PROFITABILITY_STEP,
                "valuation": VALUATION_STEP,
                "turnover": TURNOVER_STEP,
                "market_cap": MARKET_CAP_STEP,
                "price": PRICE_STEP,
            }
        
        return step_map.get(category, 5)

    def stepped_mutate(self, condition_name: str, current_value: float, fine_tuning: bool = False) -> float:
        """Mutate value in fixed steps"""
        step = self.get_step_size(condition_name, fine_tuning)
        
        direction = random.choice([-1, 1])
        steps = random.randint(1, 3) if not fine_tuning else random.randint(1, 2)
        
        template = self.INDICATOR_TEMPLATES.get(condition_name)
        if template:
            low, high = template["range"]
            new_value = current_value + (direction * step * steps)
            return max(low, min(high, new_value))
        
        new_value = current_value + (direction * step * steps)
        return max(0, new_value)


class AdaptiveMutationStrategy:
    """自适应变异策略选择器 - 使用 UCB1 算法"""

    def __init__(self, experiment_dir: Optional[Path] = None):
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
            "coarse_threshold_adjust": [],
            "fine_threshold_adjust": [],
            "simplify_formula": [],
            "probe_stability": [],
        }
        self.total_pulls = 0
        self.condition_engine = ConditionTemplateEngine()
        self.experiment_dir = experiment_dir
        if experiment_dir:
            loaded = load_adaptive_stats(experiment_dir)
            if loaded:
                for k, v in loaded.items():
                    if k in self.strategy_rewards and isinstance(v, dict) and "rewards" in v:
                        self.strategy_rewards[k] = v["rewards"]
                self.total_pulls = sum(len(v) for v in self.strategy_rewards.values())

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
            exploration_bonus = math.sqrt(2 * math.log(max(1, self.total_pulls)) / len(rewards))
            ucb_values[strategy] = avg_reward + exploration_bonus

        return max(ucb_values, key=ucb_values.get)

    def record_reward(self, mutation_type: str, score_delta: float) -> None:
        """记录变异策略的得分变化"""
        if mutation_type not in self.strategy_rewards:
            self.strategy_rewards[mutation_type] = []
        self.strategy_rewards[mutation_type].append(score_delta)
        self.total_pulls += 1
        
        if self.experiment_dir:
            save_adaptive_stats(self._get_stats_for_save(), self.experiment_dir)

    def _get_stats_for_save(self) -> dict:
        return {k: {"rewards": v, "count": len(v)} for k, v in self.strategy_rewards.items()}

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

        if not has_sort:
            available = [a for a in available if a != "adjust_formula_sort"]

        if len(formula) <= 2:
            available = [a for a in available if a != "remove_formula_condition"]

        return available


def save_adaptive_stats(stats: dict, experiment_dir: Path) -> None:
    """Save strategy rewards to file."""
    experiment_dir.mkdir(parents=True, exist_ok=True)
    stats_file = experiment_dir / "adaptive_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f)


def load_adaptive_stats(experiment_dir: Path) -> dict:
    """Load strategy rewards from file."""
    stats_file = experiment_dir / "adaptive_stats.json"
    if stats_file.exists():
        with open(stats_file, "r") as f:
            return json.load(f)
    return {}


global_adaptive_strategy = AdaptiveMutationStrategy()


def detect_duplicate_conditions(formula: list[str]) -> list[tuple[str, str]]:
    """
    Find duplicate/semantic-redundant condition pairs.
    
    Returns list of (condition1, condition2) pairs that are redundant.
    """
    engine = ConditionTemplateEngine()
    duplicates = []
    
    parsed = []
    for clause in formula:
        params = engine.parse_condition(clause)
        if params:
            parsed.append((clause, params))
    
    for i, (clause1, params1) in enumerate(parsed):
        for j, (clause2, params2) in enumerate(parsed[i+1:], i+1):
            if params1["condition_name"] == params2["condition_name"]:
                comparator1 = "大于" if "大于" in clause1 else "小于" if "小于" in clause1 else None
                comparator2 = "大于" if "大于" in clause2 else "小于" if "小于" in clause2 else None
                
                if comparator1 == comparator2:
                    if "value" in params1 and "value" in params2:
                        val1, val2 = params1["value"], params2["value"]
                        if comparator1 == "大于":
                            if val1 <= val2:
                                duplicates.append((clause1, clause2))
                            else:
                                duplicates.append((clause2, clause1))
                        elif comparator1 == "小于":
                            if val1 >= val2:
                                duplicates.append((clause1, clause2))
                            else:
                                duplicates.append((clause2, clause1))
    
    return duplicates


def canonicalize_formula(formula: list[str]) -> list[str]:
    """
    Normalize formula by:
    1. Removing duplicate conditions (same indicator, same direction, keep stricter)
       e.g., "净利润增长率大于18%" + "净利润增长率大于20%" → only keep "大于20%"
    2. Removing semantically subsumed conditions
       e.g., "市盈率小于100" + "市盈率小于50" → keep "小于50" (it's stricter)
    3. Sorting: risk filters first, then numeric conditions, then sort conditions last
    4. Normalizing whitespace and formatting
    
    Returns normalized formula list
    """
    engine = ConditionTemplateEngine()
    
    canonical = []
    seen_indicators = {}
    
    for clause in formula:
        clause = clause.strip()
        if not clause:
            continue
            
        params = engine.parse_condition(clause)
        if params:
            cond_name = params["condition_name"]
            comparator = "大于" if "大于" in clause else "小于" if "小于" in clause else None
            
            key = (cond_name, comparator)
            
            if key in seen_indicators:
                existing_clause, existing_params = seen_indicators[key]
                if "value" in params and "value" in existing_params:
                    if comparator == "大于":
                        if params["value"] > existing_params["value"]:
                            seen_indicators[key] = (clause, params)
                    elif comparator == "小于":
                        if params["value"] < existing_params["value"]:
                            seen_indicators[key] = (clause, params)
            else:
                seen_indicators[key] = (clause, params)
        else:
            if clause not in canonical:
                canonical.append(clause)
    
    for (clause, params) in seen_indicators.values():
        canonical.append(clause)
    
    def sort_key(c: str) -> tuple:
        if c in ["非ST", "非科创板", "非退市", "沪深A股", "创业板"]:
            return (0, c)
        if any(kw in c for kw in ["从大到小", "从小到大", "由近到远", "由远到近", "从高到低", "从低到高"]):
            return (2, c)
        return (1, c)
    
    canonical = sorted(canonical, key=sort_key)
    
    return canonical


def is_semantically_equivalent(cond1: str, cond2: str) -> bool:
    """Check if two conditions are semantically equivalent (allowing for minor variations)"""
    if cond1 == cond2:
        return True
    
    for base, equivalents in SEMANTIC_EQUIVALENCE.items():
        for eq in equivalents:
            if base in cond1 and eq in cond2:
                return True
    
    engine = ConditionTemplateEngine()
    p1 = engine.parse_condition(cond1)
    p2 = engine.parse_condition(cond2)
    
    if p1 and p2:
        if p1["condition_name"] == p2["condition_name"]:
            if "大于" in cond1 and "大于" in cond2:
                return abs(p1.get("value", 0) - p2.get("value", 0)) < 0.01
            if "小于" in cond1 and "小于" in cond2:
                return abs(p1.get("value", 0) - p2.get("value", 0)) < 0.01
    
    return False


def is_fragile_peak(config: dict, neighbor_results: list[dict]) -> bool:
    """
    Determine if this config is a fragile peak.
    
    Returns True if:
    - This config has highest score
    - But neighboring configs have significantly lower scores
    - (std/mean > 0.3)
    """
    if not neighbor_results or len(neighbor_results) < 2:
        return False
    
    scores = [r.get("score", 0) for r in neighbor_results]
    current_score = config.get("last_score", 0)
    
    if current_score == 0:
        return False
    
    max_neighbor = max(scores)
    if current_score <= max_neighbor:
        return False
    
    mean = sum(scores) / len(scores)
    if mean == 0:
        return True
    
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    std = math.sqrt(variance)
    
    return (std / mean) > 0.3


def validate_config(config: dict, parameter_ranges: Optional[dict] = None) -> bool:
    """
    Extended validation with parameter ranges.
    """
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

    if parameter_ranges:
        for param, (low, high) in parameter_ranges.items():
            if param in config:
                val = config[param]
                if val < low or val > high:
                    return False

    return True


def mutate_with_seed_constraints(
    config: dict,
    seed_metadata: SeedMetadata,
    mutation_type: Optional[str] = None,
) -> Tuple[dict, str, str]:
    """
    Mutate config respecting seed constraints.
    
    Constraints:
    - Cannot remove conditions in core_formula
    - Cannot modify conditions in locked_formula
    - Cannot add conditions in forbidden_formula
    - Parameters must stay within parameter_ranges
    """
    new_config = copy.deepcopy(config)
    formula = list(new_config.get("formula", []))
    
    core_set = set(seed_metadata.core_formula)
    locked_set = set(seed_metadata.locked_formula)
    forbidden_set = set(seed_metadata.forbidden_formula)
    
    if mutation_type is None:
        mutation_type = global_adaptive_strategy.select_mutation_type(formula)
    
    if mutation_type == "remove_formula_condition":
        removable = [c for c in formula if c not in core_set and c not in locked_set]
        if removable:
            to_remove = random.choice(removable)
            formula.remove(to_remove)
            new_config["formula"] = formula
            return new_config, f"[移除条件-约束] {to_remove}", mutation_type
        return new_config, "[移除条件-约束] 无可移除条件", mutation_type
    
    elif mutation_type == "add_formula_condition":
        available = [c for c in seed_metadata.forbidden_formula if c not in formula]
        if not available:
            available = [c for c in FORMULA_ADDABLE_CONDITIONS if c not in formula and c not in forbidden_set]
        if available:
            to_add = random.choice(available)
            formula.append(to_add)
            new_config["formula"] = canonicalize_formula(formula)
            return new_config, f"[添加条件-约束] {to_add}", mutation_type
        return new_config, "[添加条件-约束] 无可用条件", mutation_type
    
    elif mutation_type in ("adjust_formula_threshold", "coarse_threshold_adjust", "fine_threshold_adjust"):
        fine_tuning = (mutation_type == "fine_threshold_adjust")

        adjustable = [(i, c) for i, c in enumerate(formula) if c not in locked_set]
        if not adjustable:
            return new_config, "[阈值调整-约束] 无可调整条件", mutation_type

        # 尝试最多 10 次找到有实际变化的调整
        for _ in range(10):
            idx, clause = random.choice(adjustable)
            engine = ConditionTemplateEngine()
            params = engine.parse_condition(clause)

            if params and "value" in params:
                cond_name = params["condition_name"]
                old_val = params["value"]
                new_val = engine.stepped_mutate(cond_name, old_val, fine_tuning)

                if new_val == old_val:
                    continue  # 无变化，重试

                new_clause = replace_last_numeric_token(clause, new_val)
                formula[idx] = new_clause
                new_config["formula"] = formula

                step_type = "细调" if fine_tuning else "粗调"
                return new_config, f"[阈值调整-{step_type}] {cond_name} {format_numeric_value(old_val)}→{format_numeric_value(new_val)}", mutation_type

        return new_config, "[阈值调整-约束] 条件无可调整阈值", mutation_type
    
    elif mutation_type == "simplify_formula":
        duplicates = detect_duplicate_conditions(formula)
        removed = []
        for redundant, to_remove in duplicates:
            if to_remove not in core_set and to_remove not in locked_set:
                formula.remove(to_remove)
                removed.append(to_remove)
        
        if removed:
            new_config["formula"] = canonicalize_formula(formula)
            return new_config, f"[简化公式] 移除{len(removed)}个冗余条件", mutation_type
        return new_config, "[简化公式] 无冗余条件", mutation_type
    
    else:
        result_config, desc, actual_type = mutate(new_config, mutation_type)
        
        if seed_metadata.parameter_ranges:
            for param, (low, high) in seed_metadata.parameter_ranges.items():
                if param in result_config:
                    result_config[param] = max(low, min(high, result_config[param]))
        
        return result_config, desc, actual_type


def mutate(
    config: dict, mutation_type: Optional[str] = None, mutation_hint: Optional[str] = None,
    seed_metadata: Optional[SeedMetadata] = None, tree_name: Optional[str] = None
) -> Tuple[dict, str, str]:
    """
    生成候选配置。

    Args:
        config: 当前配置
        mutation_type: 变异类型（可选，None 时使用自适应策略选择）
        mutation_hint: 额外提示，例如 add_formula_condition 时指定具体条件
        seed_metadata: 种子约束（可选）

    Returns:
        (new_config, mutation_description, actual_mutation_type)
    """
    if seed_metadata:
        return mutate_with_seed_constraints(config, seed_metadata, mutation_type)
    
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
        "coarse_threshold_adjust": _mutate_coarse_threshold,
        "fine_threshold_adjust": _mutate_fine_threshold,
        "simplify_formula": _mutate_simplify_formula,
        "probe_stability": _mutate_probe_stability,
    }

    fn = dispatch.get(raw_type)
    if fn is None:
        raise ValueError(f"Unknown mutation type: {raw_type}")

    if raw_type == "add_formula_condition":
        result_config, desc = _mutate_add_formula_condition(
            new_config,
            specified_condition=mutation_hint,
            tree_name=tree_name,
        )
        return result_config, desc, raw_type
    if raw_type == "remove_formula_condition" and mutation_hint:
        result_config, desc = _mutate_remove_formula_condition(new_config, specified_clause=mutation_hint)
        return result_config, desc, raw_type
    if raw_type == "replace_formula_condition":
        parts = mutation_hint.split("->", 1) if mutation_hint else []
        if len(parts) == 2:
            result_config, desc = _mutate_replace_formula_condition(
                new_config,
                old_clause=parts[0].strip(),
                new_clause=parts[1].strip(),
                tree_name=tree_name,
            )
        else:
            result_config, desc = _mutate_replace_formula_condition(new_config, tree_name=tree_name)
        return result_config, desc, raw_type

    if raw_type == "adjust_max_positions":
        result_config, desc = _mutate_adjust_max_positions(new_config, tree_name=tree_name)
        return result_config, desc, raw_type
    if raw_type == "adjust_take_profit":
        result_config, desc = _mutate_adjust_take_profit(new_config, tree_name=tree_name)
        return result_config, desc, raw_type
    if raw_type == "adjust_stop_loss":
        result_config, desc = _mutate_adjust_stop_loss(new_config, tree_name=tree_name)
        return result_config, desc, raw_type
    if raw_type == "adjust_trailing_stop":
        result_config, desc = _mutate_adjust_trailing_stop(new_config, tree_name=tree_name)
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
    """调整 formula 数值条件阈值（使用步进）"""
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
        step = engine.get_step_size(cond_name)
        direction = random.choice([-1, 1])
        steps = random.randint(1, 3)
        new_low = old_low + (direction * step * steps * 0.5)
        new_high = old_high + (direction * step * steps)
        new_low = max(0, new_low)
        new_high = max(new_low + 5, new_high)
        new_clause = cond_def["template"].format(days=params["days"], low=round(new_low, 1), high=round(new_high, 1))
        desc = f"[筛选阈值] 涨幅 {old_low}%~{old_high}% → {new_low:.1f}%~{new_high:.1f}%"
    else:
        old_value = params["value"]
        new_value = engine.stepped_mutate(cond_name, old_value)
        new_clause = cond_def["template"].format(value=int(new_value))
        desc = f"[筛选阈值] {cond_name} {old_value} → {int(new_value)}"

    formula[idx] = new_clause
    config["formula"] = formula

    return config, desc


def _mutate_coarse_threshold(config: dict) -> Tuple[dict, str]:
    """大步长阈值调整"""
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
        step = engine.get_step_size(cond_name) * 2
        direction = random.choice([-1, 1])
        steps = random.randint(1, 2)
        new_low = old_low + (direction * step * steps * 0.5)
        new_high = old_high + (direction * step * steps)
        new_low = max(0, new_low)
        new_high = max(new_low + 5, new_high)
        new_clause = cond_def["template"].format(days=params["days"], low=round(new_low, 1), high=round(new_high, 1))
        desc = f"[粗调阈值] 涨幅 {old_low}%~{old_high}% → {new_low:.1f}%~{new_high:.1f}%"
    else:
        old_value = params["value"]
        new_value = engine.stepped_mutate(cond_name, old_value, fine_tuning=False)
        new_clause = cond_def["template"].format(value=int(new_value))
        desc = f"[粗调阈值] {cond_name} {old_value} → {int(new_value)}"

    formula[idx] = new_clause
    config["formula"] = formula

    return config, desc


def _mutate_fine_threshold(config: dict) -> Tuple[dict, str]:
    """小步长阈值调整"""
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
        step = engine.get_step_size(cond_name, fine_tuning=True) * 0.5
        direction = random.choice([-1, 1])
        steps = random.randint(1, 2)
        new_low = old_low + (direction * step * steps * 0.5)
        new_high = old_high + (direction * step * steps)
        new_low = max(0, new_low)
        new_high = max(new_low + 5, new_high)
        new_clause = cond_def["template"].format(days=params["days"], low=round(new_low, 1), high=round(new_high, 1))
        desc = f"[细调阈值] 涨幅 {old_low}%~{old_high}% → {new_low:.1f}%~{new_high:.1f}%"
    else:
        old_value = params["value"]
        new_value = engine.stepped_mutate(cond_name, old_value, fine_tuning=True)
        new_clause = cond_def["template"].format(value=int(new_value))
        desc = f"[细调阈值] {cond_name} {old_value} → {int(new_value)}"

    formula[idx] = new_clause
    config["formula"] = formula

    return config, desc


def _mutate_simplify_formula(config: dict) -> Tuple[dict, str]:
    """移除冗余条件"""
    formula = config.get("formula", [])
    if len(formula) <= 3:
        return config, "[简化公式] 条件数量不足"

    duplicates = detect_duplicate_conditions(formula)
    removed = []
    for redundant, to_remove in duplicates:
        formula.remove(to_remove)
        removed.append(to_remove)

    if removed:
        config["formula"] = canonicalize_formula(formula)
        return config, f"[简化公式] 移除{len(removed)}个冗余条件: {', '.join(removed[:3])}"
    return config, "[简化公式] 无冗余条件"


def _mutate_probe_stability(config: dict) -> Tuple[dict, str]:
    """探测稳定性 - 微调参数但不意图保留"""
    formula = config.get("formula", [])
    if not formula:
        return _mutate_adjust_max_positions(config)

    idx, orig_clause, params, cond_def = _find_numeric_condition(formula)
    if idx == -1:
        idx = random.randint(0, len(formula) - 1)
        orig_clause = formula[idx]

    engine = ConditionTemplateEngine()
    parsed = engine.parse_condition(orig_clause)
    
    if parsed and "value" in parsed:
        cond_name = parsed["condition_name"]
        old_val = parsed["value"]
        step = engine.get_step_size(cond_name, fine_tuning=True) * 0.5
        direction = random.choice([-1, 1])
        new_val = old_val + (direction * step)
        new_clause = orig_clause.replace(str(int(old_val)), str(int(new_val)))
        formula[idx] = new_clause
        config["formula"] = formula
        return config, f"[稳定性探测] {cond_name} {old_val}→{int(new_val)}"
    
    param_mutation = random.choice(["adjust_take_profit", "adjust_stop_loss", "adjust_trailing_stop"])
    param_map = {
        "adjust_take_profit": ("takeProfit", 1),
        "adjust_stop_loss": ("stopLoss", 1),
        "adjust_trailing_stop": ("trailingStopLoss", 0.5),
    }
    param, step = param_map[param_mutation]
    old_val = config.get(param, 10)
    direction = random.choice([-1, 1])
    new_val = old_val + (direction * step)
    config[param] = max(1, new_val)
    return config, f"[稳定性探测] {param} {old_val}→{new_val}"


def _mutate_add_formula_condition(config: dict, specified_condition: Optional[str] = None, tree_name: Optional[str] = None) -> Tuple[dict, str]:
    """添加新的 formula 条件，优先从 catalog 抽样"""
    formula = config.get("formula", [])
    engine = ConditionTemplateEngine()

    existing_text = set(formula)

    if specified_condition and specified_condition not in existing_text:
        new_condition = specified_condition
    elif tree_name:
        new_condition = sample_condition_for_tree(tree_name, existing=formula)
        if new_condition is None:
            new_condition = sample_ranking_for_tree(tree_name, existing=formula)
        if new_condition is None:
            new_condition = engine.generate_condition(formula)
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
    config: dict,
    old_clause: Optional[str] = None,
    new_clause: Optional[str] = None,
    tree_name: Optional[str] = None,
) -> Tuple[dict, str]:
    """替换 formula 中的某个条件为另一个条件。"""
    formula = config.get("formula", [])
    if not formula:
        return _mutate_add_formula_condition(config, tree_name=tree_name)

    engine = ConditionTemplateEngine()

    replaceable_indices = []
    for i, clause in enumerate(formula):
        if clause not in ["非ST", "非科创板", "非退市", "沪深A股"]:
            replaceable_indices.append(i)

    if old_clause and old_clause in formula:
        idx = formula.index(old_clause)
    elif replaceable_indices:
        idx = random.choice(replaceable_indices)
        old_clause = formula[idx]
    else:
        return _mutate_add_formula_condition(config, tree_name=tree_name)

    existing_without_old = formula[:idx] + formula[idx + 1 :]

    if not new_clause:
        is_sort_clause = any(
            kw in old_clause
            for kw in ["从大到小", "从小到大", "由近到远", "由远到近", "从高到低", "从低到高"]
        )
        if tree_name and is_sort_clause:
            new_clause = sample_ranking_for_tree(tree_name, existing=existing_without_old)
        if tree_name and not new_clause:
            new_clause = sample_condition_for_tree(tree_name, existing=existing_without_old)
        if not new_clause:
            new_clause = engine.generate_condition(existing_without_old)

    if not new_clause or new_clause == old_clause or new_clause in existing_without_old:
        return config, "[替换条件] 无可用替换"

    formula[idx] = new_clause
    config["formula"] = canonicalize_formula(formula)
    return config, f"[替换条件] {old_clause} → {new_clause}"


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


def _mutate_adjust_max_positions(config: dict, tree_name: Optional[str] = None) -> Tuple[dict, str]:
    """调整最大持仓数，优先从 soft_priors 采样"""
    old_value = config.get("maxPositions", 2)

    if tree_name:
        from tree_profile import load_tree_profile_from_dir
        profile = load_tree_profile_from_dir(tree_name)
        if profile:
            prior = get_soft_prior_value(profile, "maxPositions")
            preferred = prior.get("preferred", [])
            allowed = prior.get("allowed", [])
            if isinstance(preferred, list) and len(preferred) == 2:
                preferred_values = list(range(preferred[0], preferred[1] + 1))
                available_preferred = [v for v in preferred_values if v != old_value]
                if available_preferred and random.random() < 0.7:
                    new_value = random.choice(available_preferred)
                    config["maxPositions"] = new_value
                    desc = f"[最大持仓] {old_value} → {new_value} (preferred)"
                    return config, desc
            if isinstance(allowed, list) and len(allowed) == 2:
                allowed_values = list(range(allowed[0], allowed[1] + 1))
                available_allowed = [v for v in allowed_values if v != old_value]
                if available_allowed:
                    new_value = random.choice(available_allowed)
                    config["maxPositions"] = new_value
                    desc = f"[最大持仓] {old_value} → {new_value} (allowed)"
                    return config, desc

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


def _mutate_adjust_take_profit(config: dict, tree_name: Optional[str] = None) -> Tuple[dict, str]:
    """调整止盈阈值，优先从 soft_priors 采样"""
    old_value = config.get("takeProfit", 25)

    if tree_name:
        from tree_profile import load_tree_profile_from_dir
        profile = load_tree_profile_from_dir(tree_name)
        if profile:
            prior = get_soft_prior_value(profile, "takeProfit")
            preferred = prior.get("preferred", [])
            allowed = prior.get("allowed", [])
            if isinstance(preferred, list) and len(preferred) == 2:
                preferred_values = list(range(preferred[0], preferred[1] + 1, 5))
                available_preferred = [v for v in preferred_values if v != old_value]
                if available_preferred and random.random() < 0.7:
                    new_value = random.choice(available_preferred)
                    config["takeProfit"] = new_value
                    desc = f"[止盈] {old_value}% → {new_value}% (preferred)"
                    return config, desc

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


def _mutate_adjust_stop_loss(config: dict, tree_name: Optional[str] = None) -> Tuple[dict, str]:
    """调整止损阈值，优先从 soft_priors 采样"""
    old_value = config.get("stopLoss", 9)

    if tree_name:
        from tree_profile import load_tree_profile_from_dir
        profile = load_tree_profile_from_dir(tree_name)
        if profile:
            prior = get_soft_prior_value(profile, "stopLoss")
            preferred = prior.get("preferred", [])
            if isinstance(preferred, list) and len(preferred) == 2:
                preferred_values = list(range(preferred[0], preferred[1] + 1))
                available_preferred = [v for v in preferred_values if v != old_value]
                if available_preferred and random.random() < 0.7:
                    new_value = random.choice(available_preferred)
                    config["stopLoss"] = new_value
                    desc = f"[止损] {old_value}% → {new_value}% (preferred)"
                    return config, desc

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


def _mutate_adjust_trailing_stop(config: dict, tree_name: Optional[str] = None) -> Tuple[dict, str]:
    """调整追踪止损阈值，优先从 soft_priors 采样"""
    old_value = config.get("trailingStopLoss", 5)

    if tree_name:
        from tree_profile import load_tree_profile_from_dir
        profile = load_tree_profile_from_dir(tree_name)
        if profile:
            prior = get_soft_prior_value(profile, "trailingStopLoss")
            preferred = prior.get("preferred", [])
            if isinstance(preferred, list) and len(preferred) == 2:
                preferred_values = list(range(preferred[0], preferred[1] + 1))
                available_preferred = [v for v in preferred_values if v != old_value]
                if available_preferred and random.random() < 0.7:
                    new_value = random.choice(available_preferred)
                    config["trailingStopLoss"] = new_value
                    desc = f"[追踪止损] {old_value}% → {new_value}% (preferred)"
                    return config, desc

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
    "coarse_threshold_adjust",
    "fine_threshold_adjust",
    "simplify_formula",
    "probe_stability",
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