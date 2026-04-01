"""
首板低开策略 Notebook 回测 - JoinQuant

验证范围：2026-01-01 至 2026-03-31（最新期）
"""

print("=" * 80)
print("首板低开策略 Notebook 回测")
print("=" * 80)

from jqdata import *
import pandas as pd
import numpy as np

PERIOD_START = "2025-04-01"
PERIOD_END = "2026-03-31"

print(f"\n验证范围: {PERIOD_START} 至 {PERIOD_END} (最新期)")
print("筛选条件：市值5-15亿，位置≤30%，开盘涨跌幅-2%~+1.5%")
print("注意：由于筛选条件严格，信号可能很少\n")

trading_dates = get_trade_days(PERIOD_START, PERIOD_END)
print(f"交易日数: {len(trading_dates)}")

all_signals = []
total_zt = 0
total_fb = 0

print("\n开始扫描...")

for i, date in enumerate(trading_dates):
    if i % 20 == 0:
        print(f"进度: {i}/{len(trading_dates)} ({date})")

    prev_dates = get_trade_days(end_date=date, count=2)
    if len(prev_dates) < 2:
        continue

    prev_date = prev_dates[0]

    all_stocks = get_all_securities(types=["stock"], date=date)
    stocks_list = [
        s
        for s in all_stocks.index.tolist()
        if not (
            s.startswith("688")
            or s.startswith("300")
            or s.startswith("4")
            or s.startswith("8")
        )
    ]

    df_zt = get_price(
        stocks_list,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df_zt = df_zt.dropna()
    zt_df = df_zt[df_zt["close"] == df_zt["high_limit"]]
    zt_stocks = zt_df["code"].tolist()

    total_zt += len(zt_stocks)

    if not zt_stocks:
        continue

    prev_prev_dates = get_trade_days(end_date=prev_date, count=2)

    if len(prev_prev_dates) < 2:
        first_board = zt_stocks
        total_fb += len(first_board)
    else:
        prev_prev_date = prev_prev_dates[0]

        df_prev_zt = get_price(
            zt_stocks,
            end_date=prev_prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        df_prev_zt = df_prev_zt.dropna()
        prev_zt_df = df_prev_zt[df_prev_zt["close"] == df_prev_zt["high_limit"]]
        prev_zt_stocks = prev_zt_df["code"].tolist()

        first_board = [s for s in zt_stocks if s not in prev_zt_stocks]
        total_fb += len(first_board)

    if not first_board:
        continue

    for stock in first_board[:20]:
        try:
            df_open = get_price(
                stock,
                end_date=prev_date,
                frequency="daily",
                fields=["close"],
                count=1,
                panel=False,
            )

            if df_open.empty:
                continue

            zt_close = float(df_open["close"].iloc[0])

            df_curr = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["open"],
                count=1,
                panel=False,
            )

            if df_curr.empty:
                continue

            curr_open = float(df_curr["open"].iloc[0])
            open_pct = (curr_open - zt_close) / zt_close * 100

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

            df_pos = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close"],
                count=15,
                panel=False,
            )

            if len(df_pos) < 5:
                continue

            high_15d = df_pos["close"].max()
            low_15d = df_pos["close"].min()
            curr_close = df_pos["close"].iloc[-1]

            if high_15d == low_15d:
                continue

            position = (curr_close - low_15d) / (high_15d - low_15d)

            if position > 0.30:
                continue

            next_dates = get_trade_days(end_date=date, count=2)
            if len(next_dates) < 2:
                continue

            next_date = next_dates[1]

            df_next = get_price(
                stock,
                end_date=next_date,
                frequency="daily",
                fields=["high", "close"],
                count=1,
                panel=False,
            )

            if df_next.empty:
                continue

            next_high = float(df_next["high"].iloc[0])
            next_close = float(df_next["close"].iloc[0])

            return_high = (next_high - curr_open) / curr_open * 100
            return_close = (next_close - curr_open) / curr_open * 100

            all_signals.append(
                {
                    "date": date,
                    "stock": stock,
                    "open_pct": open_pct,
                    "market_cap": market_cap,
                    "position": position,
                    "return_high": return_high,
                    "return_close": return_close,
                }
            )

        except Exception as e:
            continue

print(f"\n{'=' * 80}")
print("统计结果")
print(f"{'=' * 80}")

print(f"\n扫描统计:")
print(f"  总涨停数: {total_zt}")
print(f"  总首板数: {total_fb}")
print(f"  有效信号数: {len(all_signals)}")

if all_signals:
    df = pd.DataFrame(all_signals)

    trading_days = len(trading_dates)

    print(f"\n信号特征:")
    print(f"  日均信号: {len(df) / trading_days:.2f}")
    print(f"  平均开盘涨跌幅: {df['open_pct'].mean():.2f}%")
    print(f"  平均市值: {df['market_cap'].mean():.1f}亿")
    print(f"  平均位置: {df['position'].mean():.2f}")

    print(f"\n收益统计（次日最高卖出）:")
    avg_return_high = df["return_high"].mean()
    win_rate_high = (df["return_high"] > 0).sum() / len(df) * 100
    profit_sum = df[df["return_high"] > 0]["return_high"].sum()
    loss_sum = abs(df[df["return_high"] < 0]["return_high"].sum())
    profit_factor = profit_sum / loss_sum if loss_sum > 0 else 0

    print(f"  平均收益: {avg_return_high:.2f}%")
    print(f"  胜率: {win_rate_high:.1f}%")
    print(f"  盈亏比: {profit_factor:.2f}")

    print(f"\n收益统计（次日收盘卖出）:")
    avg_return_close = df["return_close"].mean()
    win_rate_close = (df["return_close"] > 0).sum() / len(df) * 100
    print(f"  平均收益: {avg_return_close:.2f}%")
    print(f"  胜率: {win_rate_close:.1f}%")

    print(f"\n年化收益估算:")
    annual_return = avg_return_high * (len(df) / trading_days) * 250
    print(f"  年化收益（次日最高）: {annual_return:.1f}%")

    print(f"\n前10个信号详情:")
    for idx, row in df.head(10).iterrows():
        print(
            f"  {row['date']} {row['stock']}: 开盘{row['open_pct']:.2f}% -> 最高{row['return_high']:.2f}% 收盘{row['return_close']:.2f}%"
        )

print(f"\n{'=' * 80}")
print("回测完成")
print(f"{'=' * 80}")
