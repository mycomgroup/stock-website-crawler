#!/usr/bin/env python3
"""
RFScore PB10 仓位控制规则详细对比测试
基于当前市场宽度38.5%，测试不同规则的详细效果
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("RFScore PB10 仓位控制规则详细对比分析")
print(f"分析日期: 2026-03-28")
print(f"当前市场宽度: 38.5% (震荡区间)")
print("=" * 80)

# 设置当前日期
end_date = "2026-03-28"

# ============ 1. 获取当前市场宽度 ============
print("\n【1】当前市场状态计算")
print("-" * 60)


def calc_current_market_state(watch_date):
    """计算当前市场状态"""
    try:
        # 市场宽度
        hs300 = get_index_stocks("000300.XSHG", date=watch_date)
        prices = get_price(
            hs300, end_date=watch_date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())

        # 趋势
        idx = get_price("000300.XSHG", end_date=watch_date, count=60, fields=["close"])
        current = float(idx["close"].iloc[-1])
        ma20 = float(idx["close"].rolling(20).mean().iloc[-1])
        ma60 = float(idx["close"].rolling(60).mean().iloc[-1])

        # 简单趋势判断
        trend_score = sum([current > ma20, current > ma60, ma20 > ma60])

        if trend_score >= 2:
            trend = "向上"
        elif trend_score == 0:
            trend = "向下"
        else:
            trend = "震荡"

        return {
            "breadth": breadth,
            "trend": trend,
            "trend_score": trend_score,
            "hs300_close": current,
            "ma20": ma20,
            "ma60": ma60,
        }
    except Exception as e:
        print(f"  计算失败: {e}")
        return None


market_state = calc_current_market_state(end_date)

if market_state:
    print(f"  市场宽度: {market_state['breadth']:.2%}")
    print(
        f"  趋势状态: {market_state['trend']} (得分: {market_state['trend_score']}/3)"
    )
    print(f"  沪深300: {market_state['hs300_close']:.2f}")
    print(f"  MA20: {market_state['ma20']:.2f}")
    print(f"  MA60: {market_state['ma60']:.2f}")

    current_breadth = market_state["breadth"]
else:
    # 使用给定的38.5%
    current_breadth = 0.385
    print(f"  使用给定宽度: {current_breadth:.2%}")

# ============ 2. 详细仓位规则对比表 ============
print("\n【2】仓位控制规则详细对比表")
print("-" * 60)

# 定义5套规则
position_rules = [
    {
        "name": "规则A-保守型",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.30,
        "breadth_stop": 0.15,
        "pb_group_normal": "PB10%",
        "pb_group_reduce": "PB10%",
        "rebalance_freq": "月度",
        "description": "正常20只，宽度<30%减仓至10只，<15%空仓",
    },
    {
        "name": "规则B-平衡型",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.25,
        "breadth_stop": 0.15,
        "pb_group_normal": "PB10%",
        "pb_group_reduce": "PB10%",
        "rebalance_freq": "月度",
        "description": "当前使用版本，宽度<25%减仓至10只，<15%空仓",
    },
    {
        "name": "规则C-激进型",
        "base_hold": 20,
        "reduced_hold": 15,
        "breadth_reduce": 0.20,
        "breadth_stop": 0.10,
        "pb_group_normal": "PB10%",
        "pb_group_reduce": "PB10%",
        "rebalance_freq": "月度",
        "description": "正常20只，宽度<20%减仓至15只，<10%空仓",
    },
    {
        "name": "规则D-无空仓线",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.25,
        "breadth_stop": 0.00,
        "pb_group_normal": "PB10%",
        "pb_group_reduce": "PB10%",
        "rebalance_freq": "月度",
        "description": "正常20只，宽度<25%减仓至10只，永不空仓",
    },
    {
        "name": "规则E-RFScore专属",
        "base_hold": 20,
        "reduced_hold": 15,  # 渐进减仓第一档
        "breadth_reduce": 0.40,
        "breadth_stop": 0.25,
        "pb_group_normal": "PB10%",
        "pb_group_reduce": "PB5%",
        "rebalance_freq": "动态",
        "description": "四档渐进：20→15→10→5只，底部收紧PB5%",
    },
]

print("\n  当前市场宽度 38.5% 下的各规则表现：")
print("  " + "=" * 110)
print(
    f"  {'规则':<18} {'减仓阈值':<10} {'空仓阈值':<10} {'当前持仓':<10} {'仓位比例':<10} {'PB分组':<12} {'空仓线':<8} {'适用性评分':<10}"
)
print("  " + "=" * 110)

for rule in position_rules:
    # 计算当前状态下的持仓
    if current_breadth < rule["breadth_stop"] and rule["breadth_stop"] > 0:
        current_hold = 0
        position_pct = "0% (空仓)"
        status = "空仓"
    elif current_breadth < rule["breadth_reduce"]:
        current_hold = rule["reduced_hold"]
        position_pct = f"{current_hold / 20 * 100:.0f}% (减仓)"
        status = "减仓"
    else:
        current_hold = rule["base_hold"]
        position_pct = "100% (满仓)"
        status = "满仓"

    # 适用性评分（基于RFScore特性）
    score = 0
    reasons = []

    # 1. 检查是否适合RFScore（基本面策略不适合频繁空仓）
    if rule["breadth_stop"] == 0:
        score += 2
        reasons.append("无空仓")
    elif rule["breadth_stop"] >= 0.15:
        score += 1
        reasons.append("空仓阈值合理")

    # 2. 检查渐进减仓
    if rule["reduced_hold"] >= 15:
        score += 2
        reasons.append("渐进减仓")

    # 3. 检查PB收紧
    if "PB5%" in rule["pb_group_reduce"]:
        score += 2
        reasons.append("PB收紧")

    # 4. 检查当前适用性
    if status == "满仓" and current_breadth >= 0.35:
        score += 1
        reasons.append("当前适用")

    has_empty_line = "✓" if rule["breadth_stop"] > 0 else "✗"

    print(
        f"  {rule['name']:<18} {rule['breadth_reduce']:<10.0%} {rule['breadth_stop']:<10.0%} {current_hold:>6}只    {position_pct:<10} {rule['pb_group_reduce']:<12} {has_empty_line:<8} {score}/7 {'(' + ','.join(reasons[:2]) + ')'}"
    )

print("  " + "=" * 110)

# ============ 3. 不同宽度区间下的规则表现 ============
print("\n【3】不同市场宽度区间下的规则表现")
print("-" * 60)

test_breadths = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75]

print("\n  各规则在不同宽度下的持仓数：")
print("  " + "-" * 100)
header = f"  {'规则':<18}"
for b in test_breadths:
    header += f" {b:>6.0%}"
print(header)
print("  " + "-" * 100)

for rule in position_rules:
    line = f"  {rule['name']:<18}"
    for b in test_breadths:
        if b < rule["breadth_stop"] and rule["breadth_stop"] > 0:
            hold = 0
        elif b < rule["breadth_reduce"]:
            hold = rule["reduced_hold"]
        else:
            hold = rule["base_hold"]
        line += f" {hold:>6}"
    print(line)

print("  " + "-" * 100)

# ============ 4. RFScore专属四档规则详解 ============
print("\n【4】RFScore专属四档渐进规则详解")
print("-" * 60)

print("""
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ 状态          │ 宽度区间      │ 持仓数 │ PB分组  │ 调仓频率 │ 仓位比例 │ 说明           │
  ├──────────────────────────────────────────────────────────────────────────────┤
  │ 正常          │ ≥ 40%        │ 20只   │ PB10%   │ 月度     │ 100%     │ 标准配置       │
  │ 防守          │ 25% - 40%    │ 15只   │ PB10%   │ 月度     │ 75%      │ 降低集中度     │
  │ 底部          │ 15% - 25%    │ 10只   │ PB5%    │ 双月     │ 50%      │ 优中选优       │
  │ 极端          │ < 15%        │ 5只    │ PB5%    │ 双月     │ 25%      │ 最小仓位       │
  └──────────────────────────────────────────────────────────────────────────────┘
  
  核心设计理念：
  1. **不设空仓线**: RFScore是基本面策略，低估值股票在熊市有相对优势
  2. **四档渐进**: 20→15→10→5，比两档(20→10→0)更平滑
  3. **质量优先**: 底部时收紧PB分组(PB10%→PB5%)，优中选优
  4. **摩擦成本控制**: 底部区域降低调仓频率(月度→双月)
""")

# ============ 5. 当前市场(38.5%)下的具体建议 ============
print("\n【5】当前市场状态(宽度38.5%)下的具体建议")
print("-" * 60)

print(f"""
  📊 当前市场诊断 (2026-03-28):
     • 市场宽度: {current_breadth:.2%}
     • 趋势状态: {market_state["trend"] if market_state else "震荡偏向上"}
     • 状态判定: 【防守→正常过渡期】
  
  🎯 各规则当前建议：
""")

for rule in position_rules:
    if current_breadth < rule["breadth_stop"] and rule["breadth_stop"] > 0:
        suggestion = "🚫 空仓观望"
        detail = "等待市场企稳"
    elif current_breadth < rule["breadth_reduce"]:
        if rule["name"] == "规则E-RFScore专属":
            suggestion = f"✅ {rule['reduced_hold']}只，PB10%"
            detail = "进入防守状态，降低仓位但保持一定敞口"
        else:
            suggestion = f"⚠️  {rule['reduced_hold']}只，{rule['pb_group_reduce']}"
            detail = "减仓操作"
    else:
        suggestion = f"✅ {rule['base_hold']}只满仓，{rule['pb_group_normal']}"
        detail = "正常配置"

    print(f"     {rule['name']:<18} {suggestion}")
    print(f"     {'':<18} {detail}")
    print()

print(f"""
  💡 综合建议（基于RFScore策略特性）：
     
     当前宽度38.5%，接近40%阈值，建议：
     
     ✅ 首选方案 - 规则E (RFScore专属):
        • 持仓: 15只（防守状态）
        • PB分组: PB10%
        • 说明: 宽度接近阈值，提前减仓防守，保持一定敞口
     
     ✅ 备选方案 - 规则D (无空仓线):
        • 持仓: 20只（正常状态）
        • PB分组: PB10%
        • 说明: 不空仓原则，维持满仓但密切监控
     
     ⚠️  风险提示:
        • 若宽度跌破35%且趋势转弱，应果断减仓至15只
        • 若宽度回升至42%以上且趋势向上，可恢复20只满仓
        • 建议保留15-20%现金应对波动
""")

# ============ 6. 输出结果汇总 ============
print("\n【6】结果汇总")
print("-" * 60)

result = {
    "timestamp": datetime.now().isoformat(),
    "market_state": {
        "date": end_date,
        "breadth": current_breadth,
        "breadth_pct": f"{current_breadth:.2%}",
        "trend": market_state["trend"] if market_state else "震荡偏向上",
    },
    "recommendation": {
        "primary": "规则E-RFScore专属",
        "hold_num": 15,
        "pb_group": "PB10%",
        "position_pct": "75%",
        "reason": "宽度38.5%接近防守阈值40%，建议提前减仓至15只",
    },
    "alternative": {
        "rule": "规则D-无空仓线",
        "hold_num": 20,
        "position_pct": "100%",
        "reason": "维持满仓，但需密切监控宽度变化",
    },
    "risk_alert": [
        "若宽度跌破35%且趋势转弱，减仓至15只",
        "若宽度跌破25%，进一步减仓至10只并收紧PB5%",
        "建议保留15-20%现金应对波动",
    ],
}

print("\n  结果JSON:")
print(json.dumps(result, ensure_ascii=False, indent=2))

print("\n" + "=" * 80)
print("分析完成!")
print("=" * 80)
