"""
tree_profile.py - 树级Profile读取、校验与默认值填充

每个树只保留一套核心配置 profile.json，包含6个核心字段：
- hard_guards: 永远保留的底线条件
- initial_formula: 初始最小公式
- search_space: 允许探索哪些条件家族
- promotion_rules: 这棵树"像不像它自己"的最低门槛
- soft_priors: 参数软先验
- run_policy: 长跑策略
"""

import json
from pathlib import Path
from typing import Optional

SKILL_ROOT = Path(__file__).resolve().parent
TREES_DIR = SKILL_ROOT / "trees"

DEFAULT_PROFILE = {
    "hard_guards": ["非ST", "非退市"],
    "initial_formula": ["非ST", "非退市"],
    "search_space": {
        "primary_families": ["valuation", "quality", "growth"],
        "secondary_families": ["dividend", "cashflow", "liquidity"],
        "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
    },
    "promotion_rules": {
        "min_primary_conditions": 1,
        "preferred_additional_families": []
    },
    "soft_priors": {
        "maxPositions": {"preferred": [4, 8], "allowed": [2, 12]},
        "takeProfit": {"preferred": [15, 25], "allowed": [10, 35]},
        "stopLoss": {"preferred": [7, 12], "allowed": [5, 15]},
        "trailingStopLoss": {"preferred": [5, 8], "allowed": [3, 10]}
    },
    "run_policy": {
        "rounds_per_run": 500,
        "num_restarts": 5,
        "restart_on_stagnation": 50,
        "novelty_threshold": 0.3
    }
}

TREE_PROFILES = {
    "A_value": {
        "tree_id": "A_value",
        "name": "价值树",
        "description": "探索估值低估带来的修复机会",
        "hard_guards": ["非ST", "非退市"],
        "initial_formula": ["非ST", "非退市", "市盈率小于30"],
        "search_space": {
            "primary_families": ["valuation", "dividend", "cashflow"],
            "secondary_families": ["quality", "growth"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_valuation_conditions": 1,
            "preferred_additional_families": ["dividend", "cashflow", "quality"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [15, 25], "allowed": [10, 35]},
            "stopLoss": {"preferred": [7, 12], "allowed": [5, 15]},
            "trailingStopLoss": {"preferred": [5, 8], "allowed": [3, 10]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "B_quality_growth": {
        "tree_id": "B_quality_growth",
        "name": "质量成长树",
        "description": "探索高质量成长机会",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "净资产收益率大于15%"],
        "search_space": {
            "primary_families": ["quality", "growth", "cashflow"],
            "secondary_families": ["valuation"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_quality_conditions": 1,
            "min_growth_or_cashflow": 1,
            "preferred_additional_families": ["valuation"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [20, 30], "allowed": [10, 35]},
            "stopLoss": {"preferred": [10, 15], "allowed": [5, 18]},
            "trailingStopLoss": {"preferred": [6, 10], "allowed": [3, 12]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "C_small_cap": {
        "tree_id": "C_small_cap",
        "name": "小盘风格树",
        "description": "探索小市值公司的收益放大机会",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "流通市值小于30亿", "市盈率小于20"],
        "search_space": {
            "primary_families": ["market_cap", "valuation", "growth"],
            "secondary_families": ["quality", "liquidity"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_market_cap_conditions": 1,
            "preferred_additional_families": ["valuation", "growth"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [3, 6], "allowed": [2, 8]},
            "takeProfit": {"preferred": [15, 25], "allowed": [10, 35]},
            "stopLoss": {"preferred": [8, 12], "allowed": [5, 15]},
            "trailingStopLoss": {"preferred": [5, 8], "allowed": [3, 10]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "D_mispricing_reversal": {
        "tree_id": "D_mispricing_reversal",
        "name": "错杀反转树",
        "description": "探索市场过度定价带来的反转机会",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "净利润增长率大于30%"],
        "search_space": {
            "primary_families": ["growth", "price", "reversal"],
            "secondary_families": ["valuation", "quality"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_growth_or_reversal": 1,
            "preferred_additional_families": ["valuation", "quality"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [30, 45], "allowed": [20, 50]},
            "stopLoss": {"preferred": [15, 20], "allowed": [10, 25]},
            "trailingStopLoss": {"preferred": [10, 15], "allowed": [5, 18]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "E_technical_trend": {
        "tree_id": "E_technical_trend",
        "name": "技术趋势树",
        "description": "探索价格、成交量和趋势本身提供的交易时点",
        "hard_guards": ["非ST", "非退市"],
        "initial_formula": ["非ST", "非退市", "换手率大于5%"],
        "search_space": {
            "primary_families": ["technical", "volume", "trend"],
            "secondary_families": ["liquidity", "momentum"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_technical_conditions": 1,
            "preferred_additional_families": ["volume", "momentum"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [15, 20], "allowed": [10, 30]},
            "stopLoss": {"preferred": [6, 10], "allowed": [5, 12]},
            "trailingStopLoss": {"preferred": [4, 7], "allowed": [3, 8]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "F_fund_flow": {
        "tree_id": "F_fund_flow",
        "name": "资金筹码树",
        "description": "探索资金筹码变化带来的机会",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "换手率大于5%"],
        "search_space": {
            "primary_families": ["fund_flow", "liquidity", "volume"],
            "secondary_families": ["quality", "growth"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_fund_flow_conditions": 1,
            "preferred_additional_families": ["liquidity", "quality"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [20, 30], "allowed": [10, 35]},
            "stopLoss": {"preferred": [10, 15], "allowed": [5, 18]},
            "trailingStopLoss": {"preferred": [6, 10], "allowed": [3, 12]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "G_event_driven": {
        "tree_id": "G_event_driven",
        "name": "事件消息树",
        "description": "探索市场预期因新信息变化带来的机会",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "净利润增长率大于30%"],
        "search_space": {
            "primary_families": ["event", "growth", "news"],
            "secondary_families": ["valuation", "quality"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_event_or_growth": 1,
            "preferred_additional_families": ["valuation", "quality"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [20, 30], "allowed": [10, 35]},
            "stopLoss": {"preferred": [10, 15], "allowed": [5, 18]},
            "trailingStopLoss": {"preferred": [6, 10], "allowed": [3, 12]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "H_composite": {
        "tree_id": "H_composite",
        "name": "复合策略树",
        "description": "探索多因子交叉复合策略",
        "hard_guards": ["非ST"],
        "initial_formula": ["非ST", "市盈率小于25", "净利润增长率大于30%"],
        "search_space": {
            "primary_families": ["valuation", "growth", "quality"],
            "secondary_families": ["technical", "fund_flow", "dividend"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_different_families": 2,
            "preferred_additional_families": ["technical", "fund_flow"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [4, 8], "allowed": [2, 10]},
            "takeProfit": {"preferred": [20, 30], "allowed": [10, 35]},
            "stopLoss": {"preferred": [10, 15], "allowed": [5, 18]},
            "trailingStopLoss": {"preferred": [6, 10], "allowed": [3, 12]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    },
    "I_portfolio_risk": {
        "tree_id": "I_portfolio_risk",
        "name": "组合与风控树",
        "description": "研究选股后如何通过仓位、调仓频率、风险控制提升收益",
        "hard_guards": ["非ST", "非退市"],
        "initial_formula": ["非ST", "非退市", "流通市值大于5亿"],
        "search_space": {
            "primary_families": ["risk", "liquidity", "market_cap"],
            "secondary_families": ["quality", "valuation"],
            "allowed_actions": ["add", "remove", "replace", "sort", "coarse_adjust", "fine_adjust"]
        },
        "promotion_rules": {
            "min_risk_conditions": 1,
            "preferred_additional_families": ["liquidity", "quality"]
        },
        "soft_priors": {
            "maxPositions": {"preferred": [8, 12], "allowed": [5, 15]},
            "takeProfit": {"preferred": [10, 20], "allowed": [5, 30]},
            "stopLoss": {"preferred": [6, 10], "allowed": [5, 12]},
            "trailingStopLoss": {"preferred": [4, 7], "allowed": [3, 8]}
        },
        "run_policy": {
            "rounds_per_run": 500,
            "num_restarts": 5,
            "restart_on_stagnation": 50,
            "novelty_threshold": 0.3
        }
    }
}


def load_tree_profile(tree_name: str) -> dict:
    """Load profile for a given tree. Tries profile.json first, falls back to built-in defaults."""
    tree_dir = TREES_DIR / tree_name
    profile_path = tree_dir / "profile.json"
    
    if profile_path.exists():
        with open(profile_path, encoding="utf-8") as f:
            profile = json.load(f)
        return merge_with_defaults(profile)
    
    if tree_name in TREE_PROFILES:
        return merge_with_defaults(TREE_PROFILES[tree_name])
    
    return merge_with_defaults(DEFAULT_PROFILE.copy())


def load_tree_profile_from_dir(tree_dir: Path) -> Optional[dict]:
    """Load profile from a specific tree directory path."""
    tree_dir = Path(tree_dir)
    if not tree_dir.is_absolute():
        tree_dir = TREES_DIR / tree_dir
    
    profile_path = tree_dir / "profile.json"
    if profile_path.exists():
        with open(profile_path, encoding="utf-8") as f:
            profile = json.load(f)
        return merge_with_defaults(profile)
    
    tree_name = tree_dir.name
    if tree_name in TREE_PROFILES:
        return merge_with_defaults(TREE_PROFILES[tree_name])
    
    return None


def merge_with_defaults(profile: dict) -> dict:
    """Merge profile with defaults, ensuring all required fields exist."""
    result = DEFAULT_PROFILE.copy()
    for key, value in profile.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = {**result[key], **value}
        else:
            result[key] = value
    return result


def validate_profile(profile: dict) -> list[str]:
    """Validate profile and return list of errors. Empty list means valid."""
    errors = []
    
    required_fields = ["hard_guards", "initial_formula", "search_space", "promotion_rules", "soft_priors", "run_policy"]
    for field in required_fields:
        if field not in profile:
            errors.append(f"缺少必需字段: {field}")
    
    if "hard_guards" in profile:
        if not isinstance(profile["hard_guards"], list):
            errors.append("hard_guards 必须是列表")
        elif len(profile["hard_guards"]) == 0:
            errors.append("hard_guards 不能为空")
    
    if "initial_formula" in profile:
        if not isinstance(profile["initial_formula"], list):
            errors.append("initial_formula 必须是列表")
        elif len(profile["initial_formula"]) < 2:
            errors.append("initial_formula 至少需要2个条件")
    
    if "search_space" in profile:
        ss = profile["search_space"]
        if "primary_families" not in ss:
            errors.append("search_space 缺少 primary_families")
        if "allowed_actions" not in ss:
            errors.append("search_space 缺少 allowed_actions")
    
    if "soft_priors" in profile:
        sp = profile["soft_priors"]
        for param in ["maxPositions", "takeProfit", "stopLoss", "trailingStopLoss"]:
            if param in sp:
                if "preferred" not in sp[param] or "allowed" not in sp[param]:
                    errors.append(f"soft_priors.{param} 缺少 preferred 或 allowed")
    
    return errors


def get_hard_guards(profile: dict) -> list[str]:
    """Get hard guard conditions from profile."""
    return profile.get("hard_guards", ["非ST", "非退市"])


def get_initial_formula(profile: dict) -> list[str]:
    """Get initial formula from profile."""
    return profile.get("initial_formula", ["非ST", "非退市"])


def get_search_space(profile: dict) -> dict:
    """Get search space configuration."""
    return profile.get("search_space", DEFAULT_PROFILE["search_space"])


def get_primary_families(profile: dict) -> list[str]:
    """Get primary condition families for this tree."""
    return get_search_space(profile).get("primary_families", [])


def get_secondary_families(profile: dict) -> list[str]:
    """Get secondary condition families for this tree."""
    return get_search_space(profile).get("secondary_families", [])


def get_allowed_actions(profile: dict) -> list[str]:
    """Get allowed mutation actions for this tree."""
    return get_search_space(profile).get("allowed_actions", [])


def check_promotion_rules(formula: list[str], profile: dict) -> bool:
    """Check if a formula meets the tree's promotion rules."""
    rules = profile.get("promotion_rules", {})
    
    if "min_valuation_conditions" in rules:
        valuation_count = sum(1 for c in formula if any(v in c for v in ["市盈率", "市净率", "PEG", "市销率"]))
        if valuation_count < rules["min_valuation_conditions"]:
            return False
    
    if "min_quality_conditions" in rules:
        quality_count = sum(1 for c in formula if any(q in c for q in ["ROE", "净资产收益率", "毛利率", "净利率"]))
        if quality_count < rules["min_quality_conditions"]:
            return False
    
    if "min_growth_or_cashflow" in rules:
        growth_cf_count = sum(1 for c in formula if any(g in c for g in ["增长率", "现金流", "现金流量"]))
        if growth_cf_count < rules["min_growth_or_cashflow"]:
            return False
    
    if "min_market_cap_conditions" in rules:
        mc_count = sum(1 for c in formula if any(m in c for m in ["市值", "流通市值", "总市值"]))
        if mc_count < rules["min_market_cap_conditions"]:
            return False
    
    if "min_technical_conditions" in rules:
        tech_count = sum(1 for c in formula if any(t in c for t in ["均线", "MACD", "KDJ", "RSI", "布林", "换手率"]))
        if tech_count < rules["min_technical_conditions"]:
            return False
    
    if "min_fund_flow_conditions" in rules:
        ff_count = sum(1 for c in formula if any(f in c for f in ["股东户数", "机构持股", "主力", "资金"]))
        if ff_count < rules["min_fund_flow_conditions"]:
            return False
    
    if "min_event_or_growth" in rules:
        eg_count = sum(1 for c in formula if any(e in c for e in ["预增", "扭亏", "中报", "年报", "增长率"]))
        if eg_count < rules["min_event_or_growth"]:
            return False
    
    if "min_different_families" in rules:
        families_found = set()
        for c in formula:
            if any(v in c for v in ["市盈率", "市净率", "PEG"]):
                families_found.add("valuation")
            if any(q in c for q in ["ROE", "净资产收益率", "毛利率"]):
                families_found.add("quality")
            if any(g in c for g in ["增长率", "增速"]):
                families_found.add("growth")
            if any(t in c for t in ["均线", "MACD", "换手率"]):
                families_found.add("technical")
        if len(families_found) < rules["min_different_families"]:
            return False
    
    if "min_risk_conditions" in rules:
        risk_count = sum(1 for c in formula if any(r in c for r in ["非ST", "非退市", "非停牌", "资产负债率", "风险"]))
        if risk_count < rules["min_risk_conditions"]:
            return False
    
    return True


def get_soft_prior_value(profile: dict, param: str) -> dict:
    """Get soft prior for a specific parameter."""
    return profile.get("soft_priors", {}).get(param, DEFAULT_PROFILE["soft_priors"].get(param, {}))


def is_param_preferred(profile: dict, param: str, value) -> bool:
    """Check if a parameter value is within the preferred range."""
    prior = get_soft_prior_value(profile, param)
    if not prior or "preferred" not in prior:
        return True
    preferred = prior["preferred"]
    if isinstance(preferred, list) and len(preferred) == 2:
        return preferred[0] <= value <= preferred[1]
    return True


def get_param_penalty(profile: dict, param: str, value) -> float:
    """Get penalty score for a parameter value. 0 = preferred, higher = more penalized."""
    prior = get_soft_prior_value(profile, param)
    if not prior:
        return 0.0
    
    preferred = prior.get("preferred", [])
    allowed = prior.get("allowed", [])
    
    if isinstance(preferred, list) and len(preferred) == 2:
        if preferred[0] <= value <= preferred[1]:
            return 0.0
        if isinstance(allowed, list) and len(allowed) == 2:
            if allowed[0] <= value <= allowed[1]:
                return 0.5
        return 1.0
    
    return 0.0


def get_run_policy(profile: dict) -> dict:
    """Get run policy configuration."""
    return profile.get("run_policy", DEFAULT_PROFILE["run_policy"])


def list_all_trees() -> list[str]:
    """List all available tree names."""
    if TREES_DIR.exists():
        return sorted([d.name for d in TREES_DIR.iterdir() if d.is_dir()])
    return list(TREE_PROFILES.keys())


def create_profile_json(tree_name: str) -> None:
    """Create profile.json for a tree if it doesn't exist."""
    tree_dir = TREES_DIR / tree_name
    profile_path = tree_dir / "profile.json"
    
    if profile_path.exists():
        return
    
    if tree_name in TREE_PROFILES:
        tree_dir.mkdir(parents=True, exist_ok=True)
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(TREE_PROFILES[tree_name], f, ensure_ascii=False, indent=2)
