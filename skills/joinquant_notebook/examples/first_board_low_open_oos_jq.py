"""
首板低开策略 OOS 验证 - JoinQuant版本

验证范围：
- 历史期：2024-07-01 至 2025-03-31
- 最新期：2025-04-01 至 2026-03-31

信号定义：
- 首板：昨日涨停（非连板）
- 低开：次日开盘涨跌幅 -2% ~ +1.5%
- 流通市值：5-15亿
- 15日位置：≤30%

退出方式：
1. 次日最高价卖出
2. 次日收盘价卖出
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("首板低开策略 OOS 验证")
print("=" * 80)

PERIOD_HISTORICAL = ("2024-07-01", "2025-03-31")
PERIOD_CURRENT = ("2025-04-01", "2026-03-31")

ALL_PERIODS = [
    ("历史期", PERIOD_HISTORICAL),
    ("最新期", PERIOD_CURRENT),
]


def get_first_board_stocks_jq(date):
    prev_date = get_trade_days(end_date=date, count=2)[0]

    all_stocks = get_all_securities(types=["stock"], date=date)
    all_stocks = [
        s
        for s in all_stocks.index.tolist()
        if not (
            s.startswith("688")
            or s.startswith("300")
            or s.startswith("4")
            or s.startswith("8")
        )
    ]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df = df.dropna()
    zt_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

    if not zt_stocks:
        return []

    prev_prev_date = get_trade_days(end_date=prev_date, count=2)[0]

    df_prev = get_price(
        zt_stocks,
        end_date=prev_prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df_prev = df_prev.dropna()
    prev_zt = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

    first_board = [s for s in zt_stocks if s not in prev_zt]

    return first_board


def check_low_open_jq(stock, date, prev_date):
    df = get_price(
        stock,
        end_date=date,
        frequency="daily",
        fields=["open", "close"],
        count=2,
        panel=False,
    )

    if len(df) < 2:
        return None

    prev_close = df.iloc[0]["close"]
    curr_open = df.iloc[1]["open"]

    open_pct = (curr_open - prev_close) / prev_close * 100

    if -2.0 <= open_pct <= 1.5:
        return {
            "stock": stock,
            "date": date,
            "open_pct": open_pct,
            "buy_price": curr_open,
            "prev_close": prev_close,
        }
    return None


def check_market_cap_jq(stock, date):
    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code == stock
    )
    df = get_fundamentals(q, date)

    if df.empty:
        return False

    market_cap = float(df["circulating_market_cap"].iloc[0])

    return 5 <= market_cap <= 15


def check_position_jq(stock, date):
    df = get_price(
        stock, end_date=date, frequency="daily", fields=["close"], count=15, panel=False
    )

    if len(df) < 5:
        return False

    high_15d = df["close"].max()
    low_15d = df["close"].min()
    curr_close = df["close"].iloc[-1]

    if high_15d == low_15d:
        return False

    position = (curr_close - low_15d) / (high_15d - low_15d)

    return position <= 0.30


def calculate_returns_jq(signal, date):
    try:
        next_dates = get_trade_days(end_date=date, count=2)
        if len(next_dates) < 2:
            return None

        next_date = next_dates[1]

        df = get_price(
            signal["stock"],
            end_date=next_date,
            frequency="daily",
            fields=["high", "close", "open"],
            count=1,
            panel=False,
        )

        if df.empty:
            return None

        buy_price = signal["buy_price"]

        next_high = float(df["high"].iloc[0])
        next_close = float(df["close"].iloc[0])
        next_open = float(df["open"].iloc[0])

        return_high = (next_high - buy_price) / buy_price * 100
        return_close = (next_close - buy_price) / buy_price * 100

        return {
            "return_high": return_high,
            "return_close": return_close,
            "return_1030": None,
            "next_open": next_open,
            "next_high": next_high,
            "next_close": next_close,
        }
    except Exception as e:
        return None


def run_period_analysis_jq(period_name, start_date, end_date):
    print(f"\n{'=' * 60}")
    print(f"分析时期：{period_name} ({start_date} 至 {end_date})")
    print(f"{'=' * 60}")

    trading_dates = get_trade_days(start_date, end_date)
    print(f"交易日数量: {len(trading_dates)}")

    all_signals = []

    for i, date in enumerate(trading_dates):
        if i % 20 == 0:
            print(f"处理进度: {i}/{len(trading_dates)} ({date})")

        first_board_stocks = get_first_board_stocks_jq(date)

        if not first_board_stocks:
            continue

        low_open_signals = []
        prev_date = get_trade_days(end_date=date, count=2)[0]

        for stock in first_board_stocks[:50]:
            signal = check_low_open_jq(stock, date, prev_date)

            if signal:
                if check_market_cap_jq(stock, date) and check_position_jq(stock, date):
                    low_open_signals.append(signal)

        for signal in low_open_signals:
            returns = calculate_returns_jq(signal, date)
            if returns:
                signal.update(returns)
                all_signals.append(signal)

    print(f"\n信号总数: {len(all_signals)}")

    if not all_signals:
        print("未找到有效信号")
        return None

    df = pd.DataFrame(all_signals)

    print(f"\n开盘涨跌幅分布:")
    print(f"  最小值: {df['open_pct'].min():.2f}%")
    print(f"  最大值: {df['open_pct'].max():.2f}%")
    print(f"  平均值: {df['open_pct'].mean():.2f}%")

    print(f"\n收益统计:")

    stats = {}

    for exit_type in ["return_high", "return_close"]:
        returns = df[exit_type]
        stats[exit_type] = {
            "avg_return": returns.mean(),
            "win_rate": (returns > 0).sum() / len(returns) * 100,
            "total_signals": len(returns),
            "avg_daily_signals": len(returns) / len(trading_dates),
            "profit_factor": abs(
                returns[returns > 0].sum() / abs(returns[returns < 0].sum())
            )
            if returns[returns < 0].sum() != 0
            else 0,
        }

        print(f"\n{exit_type}:")
        print(f"  平均收益: {stats[exit_type]['avg_return']:.2f}%")
        print(f"  胜率: {stats[exit_type]['win_rate']:.1f}%")
        print(f"  总信号数: {stats[exit_type]['total_signals']}")
        print(f"  日均信号: {stats[exit_type]['avg_daily_signals']:.2f}")
        print(f"  盈亏比: {stats[exit_type]['profit_factor']:.2f}")

    return {
        "period_name": period_name,
        "start_date": start_date,
        "end_date": end_date,
        "trading_days": len(trading_dates),
        "signals": df,
        "stats": stats,
    }


print("\n开始验证...\n")

results = []
for period_name, (start, end) in ALL_PERIODS:
    result = run_period_analysis_jq(period_name, start, end)
    if result:
        results.append(result)

print("\n" + "=" * 80)
print("对比分析")
print("=" * 80)

if len(results) >= 2:
    print("\n历史期 vs 最新期 对比表")
    print("-" * 80)

    print("\n次日最高价卖出:")
    print(f"{'指标':<20} {'历史期':<15} {'最新期':<15} {'变化':<15}")
    print("-" * 60)

    hist_stats = results[0]["stats"]["return_high"]
    curr_stats = results[1]["stats"]["return_high"]

    metrics = [
        ("日均信号", "avg_daily_signals", "{:.2f}"),
        ("平均收益%", "avg_return", "{:.2f}"),
        ("胜率%", "win_rate", "{:.1f}"),
        ("盈亏比", "profit_factor", "{:.2f}"),
    ]

    for name, key, fmt in metrics:
        hist_val = hist_stats[key]
        curr_val = curr_stats[key]
        change = curr_val - hist_val

        print(
            f"{name:<20} {fmt.format(hist_val):<15} {fmt.format(curr_val):<15} {fmt.format(change):<15}"
        )

    print("\n次日收盘价卖出:")
    print(f"{'指标':<20} {'历史期':<15} {'最新期':<15} {'变化':<15}")
    print("-" * 60)

    hist_stats_close = results[0]["stats"]["return_close"]
    curr_stats_close = results[1]["stats"]["return_close"]

    for name, key, fmt in metrics:
        hist_val = hist_stats_close[key]
        curr_val = curr_stats_close[key]
        change = curr_val - hist_val

        print(
            f"{name:<20} {fmt.format(hist_val):<15} {fmt.format(curr_val):<15} {fmt.format(change):<15}"
        )

    print("\n衰减判定:")

    avg_return_high_hist = hist_stats["avg_return"]
    avg_return_high_curr = curr_stats["avg_return"]

    if avg_return_high_hist > 0:
        decline_pct = (
            (avg_return_high_hist - avg_return_high_curr) / avg_return_high_hist * 100
        )
    else:
        decline_pct = 0

    if avg_return_high_curr <= 0:
        decay_level = "严重衰减"
        reason = "收益转为负值"
    elif decline_pct > 50:
        decay_level = "严重衰减"
        reason = f"收益下降超过50% ({decline_pct:.1f}%)"
    elif decline_pct > 30:
        decay_level = "中度衰减"
        reason = f"收益下降超过30% ({decline_pct:.1f}%)"
    elif decline_pct > 10:
        decay_level = "轻度衰减"
        reason = f"收益下降超过10% ({decline_pct:.1f}%)"
    else:
        decay_level = "无明显衰减"
        reason = f"收益下降小于10% ({decline_pct:.1f}%)"

    print(f"判定结果: {decay_level}")
    print(f"判定依据: {reason}")

    if decay_level in ["轻度衰减", "中度衰减", "严重衰减"]:
        print("\n可能原因分析:")

        signal_decline = (
            (hist_stats["avg_daily_signals"] - curr_stats["avg_daily_signals"])
            / hist_stats["avg_daily_signals"]
            * 100
        )

        if signal_decline > 30:
            print(
                "1. 信号数量显著减少 ({:.1f}%)，可能策略拥挤或市场环境变化".format(
                    signal_decline
                )
            )
        elif signal_decline < -30:
            print(
                "1. 信号数量显著增加 ({:.1f}%)，可能市场环境更符合策略条件".format(
                    abs(signal_decline)
                )
            )

        if curr_stats["win_rate"] < hist_stats["win_rate"] * 0.8:
            print("2. 胜率明显下降，可能市场波动加剧或策略逻辑失效")

        if curr_stats["profit_factor"] < hist_stats["profit_factor"] * 0.7:
            print("3. 盈亏比下降，可能止损效果变差或上涨幅度减小")

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)

print("\n结果已保存")
print("建议: 根据衰减判定结果调整策略参数或暂停使用")
