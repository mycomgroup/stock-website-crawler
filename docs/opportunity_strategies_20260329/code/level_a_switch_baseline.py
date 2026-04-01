"""
三档仓位调节测试 - A组：原始开关式（基准）
时间范围：2024-01-01 至 2025-12-31
策略：首板低开策略
仓位模式：开关式（开仓/空仓）
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("A组：原始开关式回测（基准）")
print("=" * 80)
print("时间范围：2024-01-01 至 2025-12-31")
print("策略：首板低开策略")
print("仓位模式：开关式（开仓/空仓）")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def get_sentiment_switch(zt_count, max_lianban):
    """原始开关式情绪判断"""
    if zt_count >= 30 and max_lianban >= 3:
        return 1.0
    else:
        return 0.0


def get_position_type(position_ratio):
    """获取仓位类型标签"""
    if position_ratio == 1.0:
        return "满仓"
    elif position_ratio == 0.0:
        return "空仓"
    else:
        return f"仓位{position_ratio:.1%}"


trade_days = get_trade_days(START_DATE, END_DATE)
print(f"\n交易日总数: {len(trade_days)}")

all_trades = []
position_history = []
daily_pnl = []

for i, date in enumerate(trade_days):
    if i % 20 == 0:
        print(f"\n进度: {i}/{len(trade_days)} ({date})")

    prev_dates = get_trade_days(end_date=date, count=2)
    if len(prev_dates) < 2:
        continue
    prev_date = prev_dates[0]

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

    df_prev = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["paused", "close", "high_limit", "low_limit"],
        count=1,
        panel=False,
        fill_paused=False,
    )

    df_prev = df_prev.dropna()
    df_prev = df_prev[df_prev["paused"] == 0]

    zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()
    zt_count = len(zt_stocks)

    max_lianban = 0
    if len(zt_stocks) > 0:
        for stock in zt_stocks[:30]:
            df_lb = get_price(
                stock,
                end_date=prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=10,
                panel=False,
                fill_paused=False,
            )
            if len(df_lb) == 0:
                continue

            count = 0
            for j in range(len(df_lb) - 1, -1, -1):
                if df_lb.iloc[j]["close"] == df_lb.iloc[j]["high_limit"]:
                    count += 1
                else:
                    break
            max_lianban = max(max_lianban, count)

    position_ratio = get_sentiment_switch(zt_count, max_lianban)
    position_type = get_position_type(position_ratio)

    position_history.append(
        {
            "date": date,
            "zt_count": zt_count,
            "max_lianban": max_lianban,
            "position_ratio": position_ratio,
            "position_type": position_type,
        }
    )

    if position_ratio == 0.0:
        continue

    first_board = []
    if len(zt_stocks) > 0:
        prev_prev_dates = get_trade_days(end_date=prev_date, count=2)
        if len(prev_prev_dates) >= 2:
            prev_prev_date = prev_prev_dates[0]
            df_prev_prev = get_price(
                zt_stocks,
                end_date=prev_prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
            )
            df_prev_prev = df_prev_prev.dropna()
            prev_zt = df_prev_prev[df_prev_prev["close"] == df_prev_prev["high_limit"]][
                "code"
            ].tolist()
            first_board = [s for s in zt_stocks if s not in prev_zt]
        else:
            first_board = zt_stocks

    if not first_board:
        continue

    selected_stocks = []
    for stock in first_board[:30]:
        df_curr = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["open", "close", "high_limit", "paused"],
            count=2,
            panel=False,
        )

        if len(df_curr) < 2:
            continue

        curr_open = df_curr.iloc[1]["open"]
        prev_close = df_curr.iloc[0]["close"]
        paused = df_curr.iloc[1]["paused"] if "paused" in df_curr.columns else 0

        if paused == 1 or prev_close <= 0:
            continue

        open_pct = (curr_open - prev_close) / prev_close

        if not (-0.05 <= open_pct <= -0.01):
            continue

        selected_stocks.append(stock)

    if not selected_stocks:
        continue

    selected_stocks = selected_stocks[:3]

    next_dates = get_trade_days(
        start_date=date, end_date=pd.Timestamp(date) + timedelta(days=5)
    )
    if len(next_dates) < 2:
        continue
    next_date = next_dates[1]

    for stock in selected_stocks:
        df_next = get_price(
            stock,
            end_date=next_date,
            frequency="daily",
            fields=["open", "close"],
            count=1,
            panel=False,
        )

        if df_next.empty:
            continue

        buy_price = curr_open
        sell_price = df_next["open"].iloc[0]
        pnl_pct = (sell_price - buy_price) / buy_price * 100 * position_ratio

        all_trades.append(
            {
                "date": date,
                "stock": stock,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "pnl_pct": pnl_pct,
                "position_ratio": position_ratio,
                "position_type": position_type,
            }
        )

print(f"\n{'=' * 80}")
print("A组回测完成")
print(f"{'=' * 80}")

if all_trades:
    df_trades = pd.DataFrame(all_trades)
    df_positions = pd.DataFrame(position_history)

    print(f"\n【交易统计】")
    print(f"总交易次数: {len(df_trades)}")
    print(f"盈利次数: {(df_trades['pnl_pct'] > 0).sum()}")
    print(f"亏损次数: {(df_trades['pnl_pct'] < 0).sum()}")
    print(f"胜率: {(df_trades['pnl_pct'] > 0).sum() / len(df_trades) * 100:.2f}%")
    print(f"平均收益: {df_trades['pnl_pct'].mean():.2f}%")
    print(f"最大单笔收益: {df_trades['pnl_pct'].max():.2f}%")
    print(f"最大单笔亏损: {df_trades['pnl_pct'].min():.2f}%")

    total_return = df_trades["pnl_pct"].sum()
    print(f"\n累计收益: {total_return:.2f}%")

    print(f"\n【仓位分布】")
    print(df_positions["position_type"].value_counts())

    print(f"\n【情绪指标统计】")
    print(f"平均涨停数: {df_positions['zt_count'].mean():.1f}")
    print(f"平均连板数: {df_positions['max_lianban'].mean():.2f}")

    print(f"\n【开仓条件触发】")
    open_days = df_positions[df_positions["position_ratio"] > 0]
    print(
        f"开仓天数: {len(open_days)} / {len(df_positions)} ({len(open_days) / len(df_positions) * 100:.1f}%)"
    )

    df_trades.to_csv("/tmp/level_a_trades.csv", index=False)
    df_positions.to_csv("/tmp/level_a_positions.csv", index=False)
    print(f"\n详细数据已保存到: /tmp/level_a_trades.csv, /tmp/level_a_positions.csv")
