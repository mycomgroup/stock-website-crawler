#!/usr/bin/env python3
"""
validate.py - 果仁配置验证工具

验证 guorn_config.json 的合法性，包括：
  1. JSON 格式正确性
  2. 必需字段完整性
  3. 参数范围合理性
  4. 逻辑一致性

Usage:
    python validate.py --config experiments/<name>/guorn_config.json
    python validate.py --config experiments/<name>/guorn_config.json --strict
"""

import argparse
import json
from pathlib import Path


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
    required_fields = ["pool", "filters", "ranking", "holding_num", "rebalance_interval"]
    for field in required_fields:
        if field not in config:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return False, errors
    
    # 2. pool 验证
    pool = config.get("pool")
    valid_pools = {"hs300", "zz500", "zz1000", "all"}
    if pool not in valid_pools:
        errors.append(f"无效的 pool: {pool}，有效值: {valid_pools}")
    
    # 3. filters 验证
    filters = config.get("filters", [])
    if not isinstance(filters, list):
        errors.append("filters 必须是数组")
    else:
        for i, f in enumerate(filters):
            if not isinstance(f, dict):
                errors.append(f"filters[{i}] 必须是对象")
                continue
            
            if "factor" not in f:
                errors.append(f"filters[{i}] 缺少 factor 字段")
            if "operator" not in f:
                errors.append(f"filters[{i}] 缺少 operator 字段")
            if "value" not in f:
                errors.append(f"filters[{i}] 缺少 value 字段")
            
            # operator 验证
            op = f.get("operator")
            valid_ops = {">", "<", ">=", "<=", "==", "!=", "between"}
            if op not in valid_ops:
                errors.append(f"filters[{i}] 无效的 operator: {op}")
    
    # 4. ranking 验证
    ranking = config.get("ranking", [])
    if not isinstance(ranking, list):
        errors.append("ranking 必须是数组")
    else:
        for i, r in enumerate(ranking):
            if not isinstance(r, dict):
                errors.append(f"ranking[{i}] 必须是对象")
                continue
            
            if "factor" not in r:
                errors.append(f"ranking[{i}] 缺少 factor 字段")
            if "order" not in r:
                errors.append(f"ranking[{i}] 缺少 order 字段")
            if "weight" not in r:
                errors.append(f"ranking[{i}] 缺少 weight 字段")
            
            # order 验证
            order = r.get("order")
            if order not in ("asc", "desc"):
                errors.append(f"ranking[{i}] 无效的 order: {order}，有效值: asc, desc")
            
            # weight 验证
            weight = r.get("weight")
            if not isinstance(weight, (int, float)):
                errors.append(f"ranking[{i}] weight 必须是数字")
            elif weight <= 0:
                errors.append(f"ranking[{i}] weight 必须大于 0")
    
    # 5. holding_num 验证
    holding_num = config.get("holding_num")
    if not isinstance(holding_num, int):
        errors.append("holding_num 必须是整数")
    elif holding_num < 1 or holding_num > 50:
        errors.append(f"holding_num 超出合理范围 [1, 50]: {holding_num}")
    
    # 6. rebalance_interval 验证
    rebalance = config.get("rebalance_interval")
    if not isinstance(rebalance, int):
        errors.append("rebalance_interval 必须是整数")
    elif rebalance < 1 or rebalance > 60:
        errors.append(f"rebalance_interval 超出合理范围 [1, 60]: {rebalance}")
    
    # 7. 逻辑一致性检查（严格模式）
    if strict:
        # 检查重复因子
        filter_factors = [f.get("factor") for f in filters]
        if len(filter_factors) != len(set(filter_factors)):
            errors.append("filters 中存在重复因子")
        
        ranking_factors = [r.get("factor") for r in ranking]
        if len(ranking_factors) != len(set(ranking_factors)):
            errors.append("ranking 中存在重复因子")
        
        # 检查 filters 和 ranking 是否为空
        if not filters and not ranking:
            errors.append("filters 和 ranking 不能同时为空")
    
    return len(errors) == 0, errors


# ── 主函数 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="验证 guorn_config.json")
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
