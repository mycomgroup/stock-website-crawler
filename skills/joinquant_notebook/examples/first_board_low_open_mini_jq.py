"""
首板低开策略迷你测试 - JoinQuant版本

先测试最近2个月数据，验证逻辑正确性
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("首板低开策略迷你测试")
print("=" * 60)

TEST_PERIOD = ("2026-01-01", "2026-03-31")

print(f"\n测试范围: {TEST_PERIOD[0]} 至 {TEST_PERIOD[1]}")

trading_dates = get_trade_days(TEST_PERIOD[0], TEST_PERIOD[1])
print(f"交易日数量: {len(trading_dates)}")

all_signals = []

for i, date in enumerate(trading_dates):
    print(f"\n[{i + 1}/{len(trading_dates)}] 处理 {date}")

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

    print(f"  筛选股票数: {len(all_stocks)}")

    df_prev = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )

    df_prev = df_prev.dropna()
    zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

    print(f"  涨停股票数: {len(zt_stocks)}")

    if not zt_stocks:
        continue

    prev_prev_date = prev_dates[0] if len(prev_dates) >= 1 else None
    if prev_prev_date:
        df_prev_prev = get_price(
            zt_stocks,
            end_date=prev_prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )

        df_prev_prev = df_prev_prev.dropna()
        prev_zt = df_prev_prev[df_prev_prev["close"] == df_prev_prev["high_limit"]][
            "code"
        ].tolist()

        first_board = [s for s in zt_stocks if s not in prev_zt]
    else:
        first_board = zt_stocks

    print(f"  首板股票数: {len(first_board)}")

    if not first_board:
        continue

    for stock in first_board[:10]:
        df_curr = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["open", "close"],
            count=2,
            panel=False,
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
            fields=["high", "close", "open"],
            count=1,
            panel=False,
        )

        if df_next.empty:
            continue

        buy_price = curr_open
        next_high = float(df_next["high"].iloc[0])
        next_close = float(df_next["close"].iloc[0])

        return_high = (next_high - buy_price) / buy_price * 100
        return_close = (next_close - buy_price) / buy_price * 100

        signal = {
            "stock": stock,
            "date": date,
            "open_pct": open_pct,
            "buy_price": buy_price,
            "market_cap": market_cap,
            "position": position,
            "return_high": return_high,
            "return_close": return_close,
        }

        all_signals.append(signal)
        print(
            f"    发现信号: {stock}, 开盘{open_pct:.2f}%, 市值{market_cap:.1f}亿, 位置{position:.2f}"
        )
        print(f"    次日最高收益: {return_high:.2f}%, 收盘收益: {return_close:.2f}%")

print(f"\n{'=' * 60}")
print(f"测试完成")
print(f"{'=' * 60}")

print(f"\n信号总数: {len(all_signals)}")

if all_signals:
    df_signals = pd.DataFrame(all_signals)

    print(f"\n信号统计:")
    print(f"  平均开盘涨跌幅: {df_signals['open_pct'].mean():.2f}%")
    print(f"  平均市值: {df_signals['market_cap'].mean():.1f}亿")
    print(f"  平均位置: {df_signals['position'].mean():.2f}")

    print(f"\n收益统计:")
    print(f"  次日最高平均收益: {df_signals['return_high'].mean():.2f}%")
    print(
        f"  次日最高胜率: {(df_signals['return_high'] > 0).sum() / len(df_signals) * 100:.1f}%"
    )
    print(f"  次日收盘平均收益: {df_signals['return_close'].mean():.2f}%")
    print(
        f"  次日收盘胜率: {(df_signals['return_close'] > 0).sum() / len(df_signals) * 100:.1f}%"
    )

    print(f"\n所有信号详情:")
    for s in all_signals:
        print(
            f"{s['date']} {s['stock']}: 开盘{s['open_pct']:.2f}% -> 最高{s['return_high']:.2f}% 收盘{s['return_close']:.2f}%"
        )
