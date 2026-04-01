"""
三档仓位调节测试 - A组：原始开关式（基准）优化版
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

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"


def get_sentiment_switch(zt_count, max_lianban):
    """原始开关式情绪判断"""
    if zt_count >= 30 and max_lianban >= 3:
        return 1.0
    else:
        return 0.0


trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日总数: {len(trade_days)}")

all_trades = []
position_stats = {"满仓": 0, "空仓": 0}
total_return = 0
win_count = 0
total_count = 0

for i, date in enumerate(trade_days):
    if i % 50 == 0:
        print(f"进度: {i}/{len(trade_days)} ({date})")

    try:
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
            fields=["paused", "close", "high_limit"],
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
            sample_stocks = zt_stocks[:20]
            df_lianban = get_price(
                sample_stocks,
                end_date=prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=5,
                panel=False,
                fill_paused=False,
            )
            for stock in sample_stocks:
                stock_df = df_lianban[df_lianban["code"] == stock].sort_values(
                    "time", ascending=False
                )
                count = 0
                for _, row in stock_df.iterrows():
                    if abs(row["close"] - row["high_limit"]) < 0.01:
                        count += 1
                    else:
                        break
                max_lianban = max(max_lianban, count)

        position_ratio = get_sentiment_switch(zt_count, max_lianban)

        if position_ratio == 1.0:
            position_stats["满仓"] += 1
        else:
            position_stats["空仓"] += 1
            continue

        if len(zt_stocks) == 0:
            continue

        prev_prev_dates = get_trade_days(end_date=prev_date, count=2)
        first_board = zt_stocks
        if len(prev_prev_dates) >= 2:
            prev_prev_date = prev_prev_dates[0]
            df_prev_prev = get_price(
                zt_stocks[:50],
                end_date=prev_prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
            )
            if len(df_prev_prev) > 0:
                df_prev_prev = df_prev_prev.dropna()
                prev_zt = df_prev_prev[
                    df_prev_prev["close"] == df_prev_prev["high_limit"]
                ]["code"].tolist()
                first_board = [s for s in zt_stocks if s not in prev_zt]

        if not first_board:
            continue

        selected_stocks = []
        df_curr = get_price(
            first_board[:20],
            end_date=date,
            frequency="daily",
            fields=["open", "close", "paused"],
            count=2,
            panel=False,
            fill_paused=False,
        )

        for stock in first_board[:20]:
            stock_df = df_curr[df_curr["code"] == stock].sort_values("time")
            if len(stock_df) < 2:
                continue

            curr_open = stock_df.iloc[-1]["open"]
            prev_close = stock_df.iloc[-2]["close"]
            paused = stock_df.iloc[-1]["paused"] if "paused" in stock_df.columns else 0

            if paused == 1 or prev_close <= 0:
                continue

            open_pct = (curr_open - prev_close) / prev_close
            if -0.05 <= open_pct <= -0.01:
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

        df_next = get_price(
            selected_stocks,
            end_date=next_date,
            frequency="daily",
            fields=["open"],
            count=1,
            panel=False,
            fill_paused=False,
        )

        for stock in selected_stocks:
            buy_df = df_curr[df_curr["code"] == stock]
            sell_df = df_next[df_next["code"] == stock]

            if len(buy_df) < 2 or len(sell_df) == 0:
                continue

            buy_price = buy_df.iloc[-1]["open"]
            sell_price = sell_df.iloc[0]["open"]
            pnl_pct = (sell_price - buy_price) / buy_price * 100

            all_trades.append(
                {
                    "date": date,
                    "stock": stock,
                    "pnl_pct": pnl_pct,
                }
            )

            total_return += pnl_pct
            total_count += 1
            if pnl_pct > 0:
                win_count += 1

    except Exception as e:
        continue

print(f"\n{'=' * 80}")
print("A组回测结果")
print(f"{'=' * 80}")
print(f"总交易次数: {total_count}")
print(f"胜率: {win_count / max(total_count, 1) * 100:.2f}%")
print(f"累计收益: {total_return:.2f}%")
print(f"\n仓位分布:")
print(f"  满仓天数: {position_stats['满仓']}")
print(f"  空仓天数: {position_stats['空仓']}")
print(
    f"  开仓比例: {position_stats['满仓'] / (position_stats['满仓'] + position_stats['空仓']) * 100:.1f}%"
)

if total_count > 0:
    df_trades = pd.DataFrame(all_trades)
    print(f"\n交易详情:")
    print(f"  平均单笔收益: {df_trades['pnl_pct'].mean():.2f}%")
    print(f"  最大单笔收益: {df_trades['pnl_pct'].max():.2f}%")
    print(f"  最大单笔亏损: {df_trades['pnl_pct'].min():.2f}%")
