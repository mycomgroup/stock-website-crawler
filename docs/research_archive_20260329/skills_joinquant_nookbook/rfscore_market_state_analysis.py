#!/usr/bin/env python3
"""
RFScore PB10 市场状态与仓位控制分析
计算市场宽度、趋势，并测试不同仓位控制规则
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 70)
print("RFScore PB10 市场状态与仓位控制分析")
print(f"分析日期: {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 70)

# ============ 1. 计算市场宽度 ============
print("\n【1】市场宽度计算 (沪深300成分股 close > MA20 比例)")
print("-" * 60)


def calc_market_breadth(end_date, days_back=60):
    """计算市场宽度历史序列"""
    trade_days = get_trade_days(end_date=end_date, count=days_back)
    breadth_history = []

    for day in trade_days:
        try:
            # 获取沪深300成分股
            hs300 = get_index_stocks("000300.XSHG", date=day)

            # 获取20日价格数据
            prices = get_price(
                hs300, end_date=day, count=20, fields=["close"], panel=False
            )

            if len(prices) == 0:
                continue

            close = prices.pivot(index="time", columns="code", values="close")

            # 计算MA20
            ma20 = close.rolling(20).mean()

            # 计算宽度 (收盘价 > MA20 的比例)
            last_close = close.iloc[-1]
            last_ma = ma20.iloc[-1]
            breadth = (last_close > last_ma).mean()

            breadth_history.append(
                {
                    "date": str(day),
                    "breadth": round(breadth, 4),
                    "stock_count": len(hs300),
                }
            )
        except Exception as e:
            print(f"  {day} 计算失败: {e}")
            continue

    return breadth_history


# 获取最近60天的市场宽度
end_date = datetime.now().strftime("%Y-%m-%d")
breadth_history = calc_market_breadth(end_date, days_back=60)

if breadth_history:
    latest = breadth_history[-1]
    print(f"\n  最新市场宽度: {latest['breadth']:.2%} ({latest['date']})")
    print(f"  样本股票数: {latest['stock_count']}")

    # 判断状态
    if latest["breadth"] < 0.30:
        breadth_status = "底部 (<30%)"
    elif latest["breadth"] < 0.50:
        breadth_status = "中性 (30-50%)"
    elif latest["breadth"] < 0.70:
        breadth_status = "偏暖 (50-70%)"
    else:
        breadth_status = "过热 (>70%)"

    print(f"  宽度状态: {breadth_status}")

    # 显示最近10天趋势
    print(f"\n  最近10天宽度趋势:")
    for item in breadth_history[-10:]:
        bar = "█" * int(item["breadth"] * 50)
        print(f"    {item['date']}: {item['breadth']:.2%} {bar}")

# ============ 2. 计算趋势信号 ============
print("\n【2】趋势信号计算 (沪深300 MA20/MA60)")
print("-" * 60)


def calc_trend_signal(end_date):
    """计算趋势信号"""
    try:
        # 获取沪深300价格
        idx_prices = get_price(
            "000300.XSHG", end_date=end_date, count=80, fields=["close"]
        )

        if len(idx_prices) < 60:
            return None

        close = idx_prices["close"]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        current = close.iloc[-1]

        # 计算RSRS (简化版)
        returns = close.pct_change().dropna()
        if len(returns) >= 20:
            high_beta = (
                returns.rolling(20)
                .apply(
                    lambda x: np.polyfit(range(len(x)), x.values, 1)[0]
                    if len(x) == 20
                    else np.nan
                )
                .dropna()
            )
            rsrs = high_beta.iloc[-1] if len(high_beta) > 0 else 0
        else:
            rsrs = 0

        return {
            "current": float(current),
            "ma20": float(ma20),
            "ma60": float(ma60),
            "above_ma20": current > ma20,
            "above_ma60": current > ma60,
            "ma20_above_ma60": ma20 > ma60,
            "rsrs_slope": float(rsrs) if not np.isnan(rsrs) else 0,
        }
    except Exception as e:
        print(f"  趋势计算失败: {e}")
        return None


trend_signal = calc_trend_signal(end_date)

if trend_signal:
    print(f"\n  沪深300当前价格: {trend_signal['current']:.2f}")
    print(f"  MA20: {trend_signal['ma20']:.2f}")
    print(f"  MA60: {trend_signal['ma60']:.2f}")
    print(f"  价格在MA20之上: {trend_signal['above_ma20']}")
    print(f"  价格在MA60之上: {trend_signal['above_ma60']}")
    print(f"  MA20在MA60之上: {trend_signal['ma20_above_ma60']}")
    print(f"  RSRS斜率: {trend_signal['rsrs_slope']:.4f}")

    # 综合趋势判断
    trend_score = sum(
        [
            trend_signal["above_ma20"],
            trend_signal["above_ma60"],
            trend_signal["ma20_above_ma60"],
            trend_signal["rsrs_slope"] > 0,
        ]
    )

    if trend_score >= 3:
        trend_status = "向上"
    elif trend_score <= 1:
        trend_status = "向下"
    else:
        trend_status = "震荡"

    print(f"\n  综合趋势状态: {trend_status} (得分: {trend_score}/4)")

# ============ 3. RFScore仓位规则对比测试 ============
print("\n【3】RFScore仓位控制规则对比")
print("-" * 60)

# 定义要测试的仓位规则
position_rules = [
    {
        "name": "规则A: 保守型",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.30,
        "breadth_stop": 0.15,
        "description": "正常20只，宽度<30%减仓至10只，<15%空仓",
    },
    {
        "name": "规则B: 平衡型(当前)",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.25,
        "breadth_stop": 0.15,
        "description": "正常20只，宽度<25%减仓至10只，<15%空仓",
    },
    {
        "name": "规则C: 激进型",
        "base_hold": 20,
        "reduced_hold": 15,
        "breadth_reduce": 0.20,
        "breadth_stop": 0.10,
        "description": "正常20只，宽度<20%减仓至15只，<10%空仓",
    },
    {
        "name": "规则D: 无空仓线",
        "base_hold": 20,
        "reduced_hold": 10,
        "breadth_reduce": 0.25,
        "breadth_stop": 0.00,
        "description": "正常20只，宽度<25%减仓至10只，永不空仓",
    },
    {
        "name": "规则E: 渐进减仓",
        "base_hold": 20,
        "reduced_hold": 5,
        "breadth_reduce": 0.35,
        "breadth_stop": 0.15,
        "description": "正常20只，宽度<35%开始减仓，<15%降至5只",
    },
]

# 当前市场状态
if breadth_history:
    current_breadth = breadth_history[-1]["breadth"]
else:
    current_breadth = 0.385  # 默认值

if trend_signal:
    current_trend = trend_status
else:
    current_trend = "震荡"

print(f"\n  当前市场状态:")
print(f"    - 市场宽度: {current_breadth:.2%}")
print(f"    - 趋势状态: {current_trend}")
print()

print("  仓位规则对比表:")
print("  " + "-" * 100)
print(
    f"  {'规则':<15} {'阈值(减仓)':<12} {'阈值(空仓)':<12} {'正常持仓':<10} {'减仓持仓':<10} {'当前建议':<15}"
)
print("  " + "-" * 100)

for rule in position_rules:
    # 根据当前市场状态计算建议持仓
    if current_breadth < rule["breadth_stop"]:
        if rule["breadth_stop"] == 0:
            suggested = rule["reduced_hold"]
            suggested_text = f"{rule['reduced_hold']}只(最低)"
        else:
            suggested = 0
            suggested_text = "空仓"
    elif current_breadth < rule["breadth_reduce"]:
        suggested = rule["reduced_hold"]
        suggested_text = f"{rule['reduced_hold']}只(减仓)"
    else:
        suggested = rule["base_hold"]
        suggested_text = f"{rule['base_hold']}只(满仓)"

    print(
        f"  {rule['name']:<15} {rule['breadth_reduce']:<12.0%} {rule['breadth_stop']:<12.0%} {rule['base_hold']:<10} {rule['reduced_hold']:<10} {suggested_text:<15}"
    )

print("  " + "-" * 100)

# ============ 4. 宽度阈值敏感性分析 ============
print("\n【4】宽度阈值敏感性分析")
print("-" * 60)

# 使用历史数据进行敏感性分析
if len(breadth_history) >= 20:
    print("\n  历史宽度分布(最近60天):")
    breadth_values = [item["breadth"] for item in breadth_history]

    import numpy as np

    print(f"    最小值: {min(breadth_values):.2%}")
    print(f"    最大值: {max(breadth_values):.2%}")
    print(f"    平均值: {np.mean(breadth_values):.2%}")
    print(f"    中位数: {np.median(breadth_values):.2%}")
    print(f"    25分位: {np.percentile(breadth_values, 25):.2%}")
    print(f"    75分位: {np.percentile(breadth_values, 75):.2%}")

    # 统计各阈值下的触发频率
    thresholds = [0.15, 0.20, 0.25, 0.30, 0.35]
    print("\n  各减仓阈值历史触发频率:")
    for threshold in thresholds:
        count = sum(1 for b in breadth_values if b < threshold)
        freq = count / len(breadth_values)
        bar = "█" * int(freq * 50)
        print(
            f"    < {threshold:.0%}: {freq:.1%} ({count}/{len(breadth_values)}) {bar}"
        )

# ============ 5. RFScore专属市场状态定义 ============
print("\n【5】RFScore专属市场状态定义")
print("-" * 60)

print("""
  基于RFScore策略特性(基本面选股+低估值)，定义以下市场状态:
  
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 状态          │ 宽度阈值      │ 趋势      │ RFScore策略行为          │
  ├─────────────────────────────────────────────────────────────────────┤
  │ 底部精选      │ < 25%        │ 任意      │ 10只精选，质量优先       │
  │ 震荡防守      │ 25-40%       │ 震荡/向下 │ 15只，降低频率           │
  │ 趋势跟随      │ > 40%        │ 向上      │ 20只满仓                 │
  │ 过热观望      │ > 70%        │ 向上      │ 10只，PB组收紧至5%       │
  └─────────────────────────────────────────────────────────────────────┘
  
  RFScore专属逻辑:
  1. 底部时反而应该增加研究，因为低估值股票在熊市中更具防御性
  2. 宽度<25%时，从PB10%收紧到PB5%，优中选优
  3. 不盲目空仓，因为基本面好的股票在市场底部有相对优势
  4. 过热时降低仓位但不空仓，防止踏空
""")

# ============ 6. 当前市场建议 ============
print("\n【6】当前市场仓位建议")
print("-" * 60)

print(f"""
  📊 当前市场诊断:
     • 市场宽度: {current_breadth:.2%} ({"底部" if current_breadth < 0.25 else "震荡" if current_breadth < 0.40 else "偏暖"}区域)
     • 趋势状态: {current_trend}
     • 估值状态: 参考FED和格雷厄姆指数判断
  
  🎯 RFScore PB10 建议配置:
     • 建议持仓数: {"10只(精选)" if current_breadth < 0.25 else "15只(防守)" if current_breadth < 0.40 else "20只(满仓)"}
     • PB分组: {"PB5%(优中选优)" if current_breadth < 0.25 else "PB10%(标准)"}
     • 调仓频率: {"双月" if current_breadth < 0.30 else "月度"}
     • 仓位比例: {"30-50%" if current_breadth < 0.25 else "50-70%" if current_breadth < 0.40 else "80-100%"}
  
  ⚠️  风险提示:
     • 当前宽度处于{"底部区域" if current_breadth < 0.30 else "中性区间"}，注意控制仓位
     • 建议保留部分现金应对波动
     • 优先选择现金流稳健、负债率低的标的
""")

# ============ 7. 输出结果 ============
result = {
    "timestamp": datetime.now().isoformat(),
    "market_state": {
        "breadth": current_breadth,
        "trend": current_trend,
        "breadth_history": breadth_history[-10:] if breadth_history else [],
    },
    "position_rules_comparison": [
        {
            "name": rule["name"],
            "breadth_reduce": rule["breadth_reduce"],
            "breadth_stop": rule["breadth_stop"],
            "base_hold": rule["base_hold"],
            "reduced_hold": rule["reduced_hold"],
        }
        for rule in position_rules
    ],
    "recommendation": {
        "current_breadth": current_breadth,
        "suggested_hold_num": 10
        if current_breadth < 0.25
        else (15 if current_breadth < 0.40 else 20),
        "suggested_pb_group": 1 if current_breadth < 0.25 else 2,
        "position_pct": "30-50%"
        if current_breadth < 0.25
        else ("50-70%" if current_breadth < 0.40 else "80-100%"),
    },
}

print("\n" + "=" * 70)
print("分析完成，结果已准备输出")
print("=" * 70)

# 输出JSON结果(用于文件保存)
print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
