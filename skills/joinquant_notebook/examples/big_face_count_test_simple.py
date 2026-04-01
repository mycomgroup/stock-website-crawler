"""
大面股数量指标测试 - 简化版本
使用涨跌停差值（涨停家数-跌停家数）作为替代指标

测试目标：
对比两组情绪择时框架的表现：
- A组：原始情绪开关（涨停家数+连板数）
- B组：新增大面股替代指标（涨停家数+连板数+涨跌停差值>0）

接入策略：首板低开策略
时间范围：2024-01-01 至 2025-12-31
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("大面股数量指标测试（简化版）")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

print(f"\n测试范围: {START_DATE} 至 {END_DATE}")
print(f"接入策略: 首板低开策略")
print("使用涨跌停差值作为大面股替代指标")


def get_zt_dt_count_and_lianban(date):
    """
    获取涨停家数、跌停家数、最高连板数
    """
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()

    zt_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()
    dt_stocks = df[df["close"] == df["low_limit"]]["code"].tolist()

    zt_count = len(zt_stocks)
    dt_count = len(dt_stocks)
    zt_dt_diff = zt_count - dt_count

    max_lianban = 0
    if len(zt_stocks) > 0:
        for stock in zt_stocks[:20]:
            df_lb = get_price(
                stock,
                end_date=date,
                count=10,
                fields=["close", "high_limit"],
                panel=False,
            )
            if len(df_lb) == 0:
                continue

            count = 0
            for i in range(len(df_lb) - 1, -1, -1):
                if df_lb.iloc[i]["close"] == df_lb.iloc[i]["high_limit"]:
                    count += 1
                else:
                    break
            max_lianban = max(max_lianban, count)

    return zt_count, dt_count, zt_dt_diff, max_lianban


def get_sentiment_switch_A(zt_count, max_lianban):
    """
    A组：原始情绪开关（涨停家数+连板数）
    条件：涨停家数>=15 且 最高连板数>=2
    """
    return zt_count >= 15 and max_lianban >= 2


def get_sentiment_switch_B(zt_count, max_lianban, zt_dt_diff):
    """
    B组：新增涨跌停差值指标
    条件：涨停家数>=15 且 最高连板数>=2 且 涨跌停差值>0（涨停多于跌停）

    说明：
    - 涨跌停差值>0 意味着涨停家数多于跌停家数，市场情绪相对好
    - 涨跌停差值<=0 意味着跌停家数多于涨停家数，市场恐慌，类似大面股多的情况
    """
    return zt_count >= 15 and max_lianban >= 2 and zt_dt_diff > 0


def get_first_board_signals(date):
    """
    获取首板低开信号（简化版）
    """
    prev_date = get_trade_days(end_date=date, count=2)[0]

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df_prev = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df_prev = df_prev.dropna()

    zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

    if not zt_stocks:
        return []

    prev_prev_date = get_trade_days(end_date=prev_date, count=2)[0]
    df_prev_prev = get_price(
        zt_stocks,
        end_date=prev_prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df_prev_prev = df_prev_prev.dropna()

    prev_zt = df_prev_prev[df_prev_prev["close"] == df_prev_prev["high_limit"]][
        "code"
    ].tolist()

    first_board = [s for s in zt_stocks if s not in prev_zt]

    if not first_board:
        return []

    signals = []

    for stock in first_board[:30]:
        df_curr = get_price(
            stock, end_date=date, count=2, fields=["open", "close"], panel=False
        )

        if len(df_curr) < 2:
            continue

        prev_close = df_curr.iloc[0]["close"]
        curr_open = df_curr.iloc[1]["open"]

        open_pct = (curr_open - prev_close) / prev_close * 100

        if not (-2.0 <= open_pct <= 1.5):
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code == stock
        )
        df_cap = get_fundamentals(q, date)

        if df_cap.empty:
            continue

        market_cap = float(df_cap["circulating_market_cap"].iloc[0])

        if not (5 <= market_cap <= 15):
            continue

        signals.append(
            {
                "stock": stock,
                "date": date,
                "open_pct": open_pct,
                "buy_price": curr_open,
                "market_cap": market_cap,
            }
        )

    return signals


def calculate_signal_returns(signal, date):
    """
    计算信号次日收益
    """
    next_dates = get_trade_days(end_date=date, count=2)
    if len(next_dates) < 2:
        return None

    next_date = next_dates[1]

    df_next = get_price(
        signal["stock"],
        end_date=next_date,
        count=1,
        fields=["high", "close"],
        panel=False,
    )

    if df_next.empty:
        return None

    buy_price = signal["buy_price"]
    next_high = float(df_next["high"].iloc[0])
    next_close = float(df_next["close"].iloc[0])

    return_high = (next_high - buy_price) / buy_price * 100
    return_close = (next_close - buy_price) / buy_price * 100

    return {"return_high": return_high, "return_close": return_close}


print("\n开始测试...")
print("=" * 80)

trading_dates = get_trade_days(START_DATE, END_DATE)
print(f"交易日数量: {len(trading_dates)}")

group_A_signals = []
group_B_signals = []
all_signals_no_filter = []

sentiment_data = []

for i, date in enumerate(trading_dates):
    if i % 30 == 0:
        print(f"\n进度: {i}/{len(trading_dates)} ({date})")

    zt_count, dt_count, zt_dt_diff, max_lianban = get_zt_dt_count_and_lianban(date)

    sentiment_data.append(
        {
            "date": date,
            "zt_count": zt_count,
            "dt_count": dt_count,
            "zt_dt_diff": zt_dt_diff,
            "max_lianban": max_lianban,
        }
    )

    switch_A = get_sentiment_switch_A(zt_count, max_lianban)
    switch_B = get_sentiment_switch_B(zt_count, max_lianban, zt_dt_diff)

    signals = get_first_board_signals(date)

    for signal in signals:
        returns = calculate_signal_returns(signal, date)
        if returns:
            signal.update(returns)
            all_signals_no_filter.append(signal)

            if switch_A:
                group_A_signals.append(signal)

            if switch_B:
                group_B_signals.append(signal)

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

df_sentiment = pd.DataFrame(sentiment_data)

print("\n情绪指标统计:")
print(f"  平均涨停家数: {df_sentiment['zt_count'].mean():.1f}")
print(f"  平均跌停家数: {df_sentiment['dt_count'].mean():.1f}")
print(f"  平均涨跌停差值: {df_sentiment['zt_dt_diff'].mean():.1f}")
print(f"  平均最高连板数: {df_sentiment['max_lianban'].mean():.1f}")

print(f"\n涨跌停差值分布:")
print(f"  最小值: {df_sentiment['zt_dt_diff'].min()}")
print(f"  最大值: {df_sentiment['zt_dt_diff'].max()}")
print(f"  中位数: {df_sentiment['zt_dt_diff'].median()}")

print(f"\n涨跌停差值>0的交易日: {(df_sentiment['zt_dt_diff'] > 0).sum()}天")
print(f"涨跌停差值<=0的交易日: {(df_sentiment['zt_dt_diff'] <= 0).sum()}天")

print(
    f"\n跌停家数>=涨停家数的交易日: {(df_sentiment['dt_count'] >= df_sentiment['zt_count']).sum()}天"
)

print("\n" + "=" * 80)
print("三组对比")
print("=" * 80)

print("\n无择时基线:")
if all_signals_no_filter:
    df_all = pd.DataFrame(all_signals_no_filter)
    print(f"  信号数量: {len(df_all)}")
    print(f"  平均次日最高收益: {df_all['return_high'].mean():.2f}%")
    print(f"  平均次日收盘收益: {df_all['return_close'].mean():.2f}%")
    print(
        f"  次日最高胜率: {(df_all['return_high'] > 0).sum() / len(df_all) * 100:.1f}%"
    )
    print(
        f"  盈亏比（最高）: {abs(df_all[df_all['return_high'] > 0]['return_high'].sum() / abs(df_all[df_all['return_high'] < 0]['return_high'].sum())):.2f}"
    )

print("\nA组（原始情绪开关：涨停>=15+连板>=2）:")
if group_A_signals:
    df_A = pd.DataFrame(group_A_signals)
    print(f"  信号数量: {len(df_A)}")
    print(f"  平均次日最高收益: {df_A['return_high'].mean():.2f}%")
    print(f"  平均次日收盘收益: {df_A['return_close'].mean():.2f}%")
    print(f"  次日最高胜率: {(df_A['return_high'] > 0).sum() / len(df_A) * 100:.1f}%")
    print(
        f"  盈亏比（最高）: {abs(df_A[df_A['return_high'] > 0]['return_high'].sum() / abs(df_A[df_A['return_high'] < 0]['return_high'].sum())):.2f}"
    )

print("\nB组（新增指标：涨停>=15+连板>=2+涨跌停差值>0）:")
if group_B_signals:
    df_B = pd.DataFrame(group_B_signals)
    print(f"  信号数量: {len(df_B)}")
    print(f"  平均次日最高收益: {df_B['return_high'].mean():.2f}%")
    print(f"  平均次日收盘收益: {df_B['return_close'].mean():.2f}%")
    print(f"  次日最高胜率: {(df_B['return_high'] > 0).sum() / len(df_B) * 100:.1f}%")
    print(
        f"  盈亏比（最高）: {abs(df_B[df_B['return_high'] > 0]['return_high'].sum() / abs(df_B[df_B['return_high'] < 0]['return_high'].sum())):.2f}"
    )

if group_A_signals and group_B_signals:
    df_A = pd.DataFrame(group_A_signals)
    df_B = pd.DataFrame(group_B_signals)

    print("\n" + "=" * 80)
    print("A组 vs B组详细对比")
    print("=" * 80)

    print(
        f"\n{'指标':<25} {'无择时':<12} {'A组':<12} {'B组':<12} {'A vs 无择时':<15} {'B vs A':<15}"
    )
    print("-" * 90)

    if all_signals_no_filter:
        df_all = pd.DataFrame(all_signals_no_filter)
        metrics = [
            ("信号数量", len(df_all), len(df_A), len(df_B)),
            (
                "平均次日最高收益%",
                df_all["return_high"].mean(),
                df_A["return_high"].mean(),
                df_B["return_high"].mean(),
            ),
            (
                "平均次日收盘收益%",
                df_all["return_close"].mean(),
                df_A["return_close"].mean(),
                df_B["return_close"].mean(),
            ),
            (
                "次日最高胜率%",
                (df_all["return_high"] > 0).sum() / len(df_all) * 100,
                (df_A["return_high"] > 0).sum() / len(df_A) * 100,
                (df_B["return_high"] > 0).sum() / len(df_B) * 100,
            ),
        ]
    else:
        metrics = [
            ("信号数量", 0, len(df_A), len(df_B)),
            (
                "平均次日最高收益%",
                0,
                df_A["return_high"].mean(),
                df_B["return_high"].mean(),
            ),
            (
                "平均次日收盘收益%",
                0,
                df_A["return_close"].mean(),
                df_B["return_close"].mean(),
            ),
            (
                "次日最高胜率%",
                0,
                (df_A["return_high"] > 0).sum() / len(df_A) * 100,
                (df_B["return_high"] > 0).sum() / len(df_B) * 100,
            ),
        ]

    for name, val_all, val_A, val_B in metrics:
        diff_A_all = val_A - val_all
        diff_B_A = val_B - val_A
        print(
            f"{name:<25} {val_all:<12.2f} {val_A:<12.2f} {val_B:<12.2f} {diff_A_all:<15.2f} {diff_B_A:<15.2f}"
        )

    print("\n" + "=" * 80)
    print("增益分析")
    print("=" * 80)

    print("\nA组增益（vs 无择时）:")
    if all_signals_no_filter:
        df_all = pd.DataFrame(all_signals_no_filter)
        improvement_A = (
            (df_A["return_high"].mean() - df_all["return_high"].mean())
            / abs(df_all["return_high"].mean())
            * 100
            if df_all["return_high"].mean() != 0
            else 0
        )
        print(f"  收益提升: {improvement_A:.1f}%")

    print("\nB组增益（vs A组）:")
    improvement_B = (
        (df_B["return_high"].mean() - df_A["return_high"].mean())
        / abs(df_A["return_high"].mean())
        * 100
        if df_A["return_high"].mean() != 0
        else 0
    )
    print(f"  收益提升: {improvement_B:.1f}%")

    print("\n过滤效果分析:")
    print(
        f"  A组过滤掉信号: {len(all_signals_no_filter) - len(df_A)}个 ({(len(all_signals_no_filter) - len(df_A)) / len(all_signals_no_filter) * 100:.1f}%)"
    )
    print(
        f"  B组进一步过滤: {len(df_A) - len(df_B)}个 ({(len(df_A) - len(df_B)) / len(df_A) * 100:.1f}%)"
    )

    print("\n" + "=" * 80)
    print("最终判定")
    print("=" * 80)

    if len(df_B) < len(df_A) * 0.5:
        print("  ⚠️  B组信号数量过少（<50%），过度过滤风险")

    if df_B["return_high"].mean() > df_A["return_high"].mean() * 1.15:
        print("\n  ** Go - 涨跌停差值指标有显著增益（收益提升>15%）**")
        print("  建议：将涨跌停差值>0加入情绪择时框架")
    elif df_B["return_high"].mean() > df_A["return_high"].mean():
        print("\n  ** Watch - 涨跌停差值指标有轻微增益**")
        print("  建议：继续验证，观察不同阈值的效果")
    elif df_B["return_high"].mean() >= df_A["return_high"].mean() * 0.95:
        print("\n  ** Watch - 涨跌停差值指标无明显增益或轻微负面影响**")
        print("  建议：进一步测试不同阈值或调整组合方式")
    else:
        print("\n  ** No-Go - 涨跌停差值指标有显著负面影响**")
        print("  建议：不使用涨跌停差值指标")

print("\n" + "=" * 80)
print("测试结束")
print("=" * 80)
