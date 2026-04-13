#!/usr/bin/env python3
"""
validate.py - Wizard 配置验证工具

验证 wizard_config.json 的合法性，包括：
  1. JSON 格式正确性
  2. 必需字段完整性
  3. 因子名称有效性
  4. 参数范围合理性
  5. 逻辑一致性

Usage:
    python validate.py --config experiments/<name>/wizard_config.json
    python validate.py --config experiments/<name>/wizard_config.json --strict
"""

import argparse
import json
from pathlib import Path
from typing import Any


# ── 因子库定义 ────────────────────────────────────────────────────────────────

VALID_FACTORS = {
    # 估值指标
    "pe_ratio", "pb_ratio", "ps_ratio", "pcf_ratio",
    "market_cap", "circulating_market_cap",
    # 盈利能力
    "roe", "roa", "gross_profit_margin", "net_profit_margin", "operating_profit_margin",
    # 成长能力
    "revenue_growth_rate", "net_profit_growth_rate",
    "operating_profit_growth_rate", "total_assets_growth_rate",
    # 财务健康
    "debt_ratio", "current_ratio", "quick_ratio", "equity_ratio",
    # 现金流
    "operating_cash_flow_per_share", "free_cash_flow_per_share",
    # 分红指标
    "dividend_yield", "dividend_payout_ratio",
    # 每股指标
    "eps", "book_value_per_share",
    # 价格与成交量
    "turnover_rate", "volume", "change_rate",
}

VALID_OPERATORS = {"greater_than", "less_than", "in_range", "rank_in_range"}
VALID_UNIVERSES = {"000300.XSHG", "000905.XSHG", "000852.XSHG", "*"}
VALID_ST_OPTIONS = {"exclude", "include", "only"}
VALID_HOLDING_NUMS = {5, 10, 15, 20, 25, 30}
VALID_REBALANCE_INTERVALS = {1, 3, 5, 10, 15, 20, 30}


# ── 验证函数 ──────────────────────────────────────────────────────────────────

def validate_config(config: dict, strict: bool = False) -> tuple[bool, list[str]]:
    """
    验证配置合法性
    
    Args:
        config: 配置字典
        strict: 严格模式（检查更多规则）
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # 1. 必需字段
    required_fields = ["universe", "stOption", "filters", "sorting", "maxHoldingNum", "rebalanceInterval"]
    for field in required_fields:
        if field not in config:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return False, errors
    
    # 2. universe 验证
    universe = config.get("universe", [])
    if not isinstance(universe, list) or not universe:
        errors.append("universe 必须是非空数组")
    else:
        for u in universe:
            if u not in VALID_UNIVERSES:
                errors.append(f"无效的 universe: {u}，有效值: {VALID_UNIVERSES}")
    
    # 3. stOption 验证
    st_option = config.get("stOption")
    if st_option not in VALID_ST_OPTIONS:
        errors.append(f"无效的 stOption: {st_option}，有效值: {VALID_ST_OPTIONS}")
    
    # 4. filters 验证
    filters = config.get("filters", [])
    if not isinstance(filters, list):
        errors.append("filters 必须是数组")
    else:
        for i, f in enumerate(filters):
            if not isinstance(f, dict):
                errors.append(f"filters[{i}] 必须是对象")
                continue
            
            # operator
            op = f.get("operator")
            if op not in VALID_OPERATORS:
                errors.append(f"filters[{i}] 无效的 operator: {op}")
            
            # factor
            factor = f.get("factor", {})
            if not isinstance(factor, dict):
                errors.append(f"filters[{i}] factor 必须是对象")
            else:
                factor_type = factor.get("type")
                factor_name = factor.get("name")
                if factor_type not in ("fundamental", "pricing"):
                    errors.append(f"filters[{i}] 无效的 factor.type: {factor_type}")
                if factor_name not in VALID_FACTORS:
                    errors.append(f"filters[{i}] 无效的 factor.name: {factor_name}")
            
            # rhs
            if "rhs" not in f:
                errors.append(f"filters[{i}] 缺少 rhs 字段")
            elif not isinstance(f["rhs"], (int, float, list)):
                errors.append(f"filters[{i}] rhs 必须是数字或数组")
    
    # 5. sorting 验证
    sorting = config.get("sorting", [])
    if not isinstance(sorting, list):
        errors.append("sorting 必须是数组")
    else:
        for i, s in enumerate(sorting):
            if not isinstance(s, dict):
                errors.append(f"sorting[{i}] 必须是对象")
                continue
            
            # factor
            factor = s.get("factor", {})
            if not isinstance(factor, dict):
                errors.append(f"sorting[{i}] factor 必须是对象")
            else:
                factor_type = factor.get("type")
                factor_name = factor.get("name")
                if factor_type not in ("fundamental", "pricing"):
                    errors.append(f"sorting[{i}] 无效的 factor.type: {factor_type}")
                if factor_name not in VALID_FACTORS:
                    errors.append(f"sorting[{i}] 无效的 factor.name: {factor_name}")
            
            # ascending
            if "ascending" not in s:
                errors.append(f"sorting[{i}] 缺少 ascending 字段")
            elif not isinstance(s["ascending"], bool):
                errors.append(f"sorting[{i}] ascending 必须是布尔值")
            
            # weight
            if "weight" not in s:
                errors.append(f"sorting[{i}] 缺少 weight 字段")
            elif not isinstance(s["weight"], (int, float)):
                errors.append(f"sorting[{i}] weight 必须是数字")
            elif s["weight"] <= 0:
                errors.append(f"sorting[{i}] weight 必须大于 0")
    
    # 6. maxHoldingNum 验证
    holding_num = config.get("maxHoldingNum")
    if not isinstance(holding_num, int):
        errors.append("maxHoldingNum 必须是整数")
    elif holding_num not in VALID_HOLDING_NUMS:
        if strict:
            errors.append(f"maxHoldingNum 建议值: {sorted(VALID_HOLDING_NUMS)}")
        elif holding_num < 1 or holding_num > 50:
            errors.append(f"maxHoldingNum 超出合理范围 [1, 50]: {holding_num}")
    
    # 7. rebalanceInterval 验证
    rebalance = config.get("rebalanceInterval")
    if not isinstance(rebalance, int):
        errors.append("rebalanceInterval 必须是整数")
    elif rebalance not in VALID_REBALANCE_INTERVALS:
        if strict:
            errors.append(f"rebalanceInterval 建议值: {sorted(VALID_REBALANCE_INTERVALS)}")
        elif rebalance < 1 or rebalance > 60:
            errors.append(f"rebalanceInterval 超出合理范围 [1, 60]: {rebalance}")
    
    # 8. 逻辑一致性检查（严格模式）
    if strict:
        # 检查重复因子
        filter_factors = [f.get("factor", {}).get("name") for f in filters]
        if len(filter_factors) != len(set(filter_factors)):
            errors.append("filters 中存在重复因子")
        
        sorting_factors = [s.get("factor", {}).get("name") for s in sorting]
        if len(sorting_factors) != len(set(sorting_factors)):
            errors.append("sorting 中存在重复因子")
        
        # 检查 filters 和 sorting 是否为空
        if not filters and not sorting:
            errors.append("filters 和 sorting 不能同时为空")
    
    return len(errors) == 0, errors


# ── 主函数 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="验证 wizard_config.json")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--strict", action="store_true", help="严格模式")
    args = parser.parse_args()
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return 1
    
    try:
        config = json.load(open(config_path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return 1
    
    is_valid, errors = validate_config(config, strict=args.strict)
    
    if is_valid:
        print(f"✅ 配置验证通过: {config_path}")
        return 0
    else:
        print(f"❌ 配置验证失败: {config_path}")
        for error in errors:
            print(f"  • {error}")
        return 1


if __name__ == "__main__":
    exit(main())
