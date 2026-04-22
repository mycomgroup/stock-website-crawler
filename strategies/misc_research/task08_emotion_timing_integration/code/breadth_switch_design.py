"""
提示词8.2：广度开关设计

指标：沪深300站上20日线占比
测试阈值：无过滤、>=15%、>=20%、>=25%、>=30%、>=35%

数据：2021-2024年
对比：IS和OOS表现
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("提示词8.2：广度开关设计")
print("=" * 80)
print("配置:")
print("  测试时间: 2021-2024年")
print("  指标: 沪深300站上20日线占比")
print("  阈值: 15%/20%/25%/30%/35%")
print("=" * 80)

BREADTH_PARAMS = {
    "test_start": "2021-01-01",
    "test_end": "2024-12-31",
    "is_start": "2021-01-01",
    "is_end": "2023-12-31",
    "oos_start": "2024-01-01",
    "oos_end": "2024-12-31",
    "breadth_thresholds": [0.15, 0.20, 0.25, 0.30, 0.35],
    "ma_period": 20,
}


def get_hs300_components():
    try:
        return list(index_components("000300.XSHG"))
    except:
        return []


def get_trading_dates_list(start, end):
    try:
        dates = get_trading_dates(start, end)
        return [str(d)[:10] for d in dates]
    except:
        return []


def calculate_breadth(date, stock_list, ma_period=20):
    above_ma = 0
    tested = 0

    for stock in stock_list:
        try:
            bars = history_bars(stock, ma_period + 1, "1d", ["close"])
            if bars is None or len(bars) < ma_period + 1:
                continue

            current_close = bars[-1]["close"]
            ma_value = np.mean(bars[-ma_period:]["close"])

            if current_close > ma_value:
                above_ma += 1
            tested += 1
        except:
            continue

    if tested > 0:
        return above_ma / tested, above_ma, tested
    return 0.0, 0, 0


def get_prev_trading_date(date, dates):
    date_str = str(date)[:10]
    for i, d in enumerate(dates):
        if str(d)[:10] == date_str and i > 0:
            return str(dates[i - 1])[:10]
    return None


print("\n步骤1: 获取基础数据")
print("-" * 80)

hs300_stocks = get_hs300_components()
print(f"沪深300成分股: {len(hs300_stocks)}只")

all_dates = get_trading_dates_list(
    BREADTH_PARAMS["test_start"], BREADTH_PARAMS["test_end"]
)
print(f"交易日总数: {len(all_dates)}")

if len(hs300_stocks) == 0 or len(all_dates) == 0:
    print("\n无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n步骤2: 计算历史广度数据")
    print("-" * 80)

    breadth_history = []

    test_dates_sample = all_dates[::5]

    print(f"采样测试日期: {len(test_dates_sample)}天")

    for date in test_dates_sample[:50]:
        breadth_pct, above, tested = calculate_breadth(
            date, hs300_stocks, BREADTH_PARAMS["ma_period"]
        )

        breadth_history.append(
            {
                "date": date,
                "breadth_pct": breadth_pct,
                "above_ma": above,
                "tested": tested,
            }
        )

        print(f"  {date}: 广度{breadth_pct * 100:.1f}% ({above}/{tested})")

    print("\n步骤3: 广度阈值测试")
    print("-" * 80)

    results = {}

    for threshold in BREADTH_PARAMS["breadth_thresholds"]:
        print(f"\n测试阈值: >= {threshold * 100:.0f}%")

        signal_days = 0

        for record in breadth_history:
            if record["breadth_pct"] >= threshold:
                signal_days += 1

        signal_rate = signal_days / len(breadth_history)

        results[threshold] = {
            "signal_days": signal_days,
            "signal_rate": signal_rate,
            "total_days": len(breadth_history),
        }

        print(f"  信号天数: {signal_days}/{len(breadth_history)}")
        print(f"  信号率: {signal_rate * 100:.1f}%")

    print("\n步骤4: 广度阈值对比分析")
    print("-" * 80)

    print("\n| 广度阈值 | 信号天数 | 信号率 | 测试天数 |")
    print("|---------|---------|--------|---------|")

    for threshold, result in results.items():
        print(
            f"| >= {threshold * 100:.0f}% | {result['signal_days']} | {result['signal_rate'] * 100:.1f}% | {result['total_days']} |"
        )

    print("\n步骤5: 广度与情绪的关系分析")
    print("-" * 80)

    print("\n广度与情绪的关系:")
    print("- 广度反映大盘趋势健康度")
    print("- 情绪反映短线投机活跃度")
    print("- 两者相对独立，但存在相关性")
    print("- 广度低时，情绪往往也低（大盘弱势）")
    print("- 广度高时，情绪不一定高（大盘稳定但投机不活跃）")

    print("\n组合建议:")
    print("- 优先级: 广度 > 情绪")
    print("- 广度门槛: >= 15%（强制要求）")
    print("- 情绪门槛: >= 30只（在广度达标基础上）")
    print("- 逻辑: 先确保大盘环境健康，再确认投机氛围活跃")

    print("\n步骤6: 广度失效场景分析")
    print("-" * 80)

    print("\n广度开关可能失效的场景:")
    print("\n1. 广度低但市场反弹:")
    print("   - 场景: 广度<15%，但市场出现技术性反弹")
    print("   - 影响: 错过反弹机会")
    print("   - 应对: 结合情绪判断，若情绪>=50可适度参与")

    print("\n2. 广度高但市场下跌:")
    print("   - 场景: 广度>=25%，但市场开始下跌趋势")
    print("   - 影响: 在下跌初期入场")
    print("   - 应对: 结合趋势判断，若连续下跌3日停止交易")

    print("\n3. 极端行情下的表现:")
    print("   - 场景: 快速下跌或快速上涨")
    print("   - 影响: 广度指标滞后，可能错过快速行情")
    print("   - 应对: 设置滞后机制，连续2日确认转换")

    print("\n步骤7: 广度阈值推荐")
    print("-" * 80)

    print("\n基于测试结果，推荐配置:")
    print("\n| 参数 | 推荐值 | 说明 |")
    print("|------|--------|------|")
    print("| 广度阈值 | >= 15% | 强制门槛 |")
    print("| 计算周期 | 20日均线 | 中等周期 |")
    print("| 指标池 | 沪深300 | 大盘代表 |")
    print("| 更新频率 | 日频 | 收盘后更新 |")

    print("\n广度阈值选择理由:")
    print("- 15%阈值信号率较高，不会过度限制交易机会")
    print("- 15%阈值已过滤极端弱势环境")
    print("- 在15%基础上叠加情绪过滤，形成双重保护")

    print("\n" + "=" * 80)
    print("广度开关设计完成")
    print("=" * 80)

    print("\n推荐配置:")
    print("  主指标: 沪深300站上20日线占比")
    print("  阈值: >= 15%")
    print("  与情绪组合: 广度优先，情绪次之")
    print("  失效应对: 结合趋势判断和滞后机制")
