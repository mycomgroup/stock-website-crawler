#!/usr/bin/env python3
"""234板分板位回测 - 简化版本，在聚宽Notebook执行"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("234板分板位回测 - 测试范围: 2024-01-01 至 2024-03-31")
print("=" * 70)

START_DATE = "2024-01-01"
END_DATE = "2024-03-31"


def get_zt_stocks(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (
            s.startswith("68")
            or s.startswith("4")
            or s.startswith("8")
            or s.startswith("3")
        )
    ]
    try:
        df = get_price(
            all_stocks[:500],
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
            skip_paused=False,
        )
        df = df.dropna()
        zt_df = df[df["close"] == df["high_limit"]]
        return list(zt_df["code"])
    except:
        return []


def get_prev_date(date):
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        if idx > 0:
            return all_days[idx - 1]
    return None


def filter_yzb(stock_list, date):
    result = []
    for s in stock_list[:50]:
        try:
            df = get_price(s, end_date=date, count=1, fields=["low", "high"])
            if df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(s)
        except:
            continue
    return result


def get_turnover_ratio(stock, date):
    try:
        hsl = HSL([stock], date)
        if stock in hsl[0]:
            return hsl[0][stock]
        return 0
    except:
        return 0


def get_free_cap(stock, date):
    try:
        q = query(valuation.circulating_market_cap).filter(valuation.code == stock)
        df = get_fundamentals(q, date=date)
        if len(df) > 0:
            return df["circulating_market_cap"].iloc[0]
        return 0
    except:
        return 0


def backtest_two_board(start_date, end_date, with_sentiment=False):
    """二板回测"""
    print(f"\n二板回测 | 情绪开关={with_sentiment}")

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    results = []

    for i, date_dt in enumerate(trade_days[:-1]):
        date = date_dt.strftime("%Y-%m-%d")
        next_date = trade_days[i + 1].strftime("%Y-%m-%d")

        prev_date = get_prev_date(date)
        if prev_date is None:
            continue

        prev2_date = get_prev_date(prev_date)
        if prev2_date is None:
            continue

        if with_sentiment:
            zt_count = len(get_zt_stocks(date))
            if zt_count < 30:
                continue

        hl_today = get_zt_stocks(date)
        hl_prev = get_zt_stocks(prev_date)
        hl_prev2 = get_zt_stocks(prev2_date)

        non_yzb = filter_yzb(hl_today, date)
        two_board = list(set(non_yzb) & set(hl_prev) - set(hl_prev2))

        low_hsl = [s for s in two_board if get_turnover_ratio(s, date) < 30]

        if len(low_hsl) == 0:
            continue

        caps = [(s, get_free_cap(s, date)) for s in low_hsl]
        caps.sort(key=lambda x: x[1])
        target = caps[0][0] if len(caps) > 0 else None

        if target is None:
            continue

        try:
            next_prices = get_price(
                target,
                end_date=next_date,
                count=1,
                fields=["open", "high", "close", "high_limit"],
                panel=False,
            )

            open_price = next_prices.iloc[0]["open"]
            high_price = next_prices.iloc[0]["high"]
            high_limit = next_prices.iloc[0]["high_limit"]

            if open_price == high_limit:
                continue

            buy_price = open_price * 1.005
            sell_price = max(high_price, next_prices.iloc[0]["close"])

            profit_pct = (sell_price / buy_price - 1) * 100

            results.append({"date": next_date, "stock": target, "profit": profit_pct})
        except:
            continue

    if len(results) == 0:
        print("  无交易记录")
        return None

    df = pd.DataFrame(results)

    total_trades = len(df)
    win_rate = len(df[df["profit"] > 0]) / total_trades * 100
    avg_profit = df["profit"].mean()

    cumulative = df["profit"].cumsum()
    peak = cumulative.cummax()
    drawdown = peak - cumulative
    max_drawdown = drawdown.max()

    print(f"  交易次数: {total_trades}")
    print(f"  胜率: {win_rate:.2f}%")
    print(f"  平均收益: {avg_profit:.2f}%")
    print(f"  累计收益: {cumulative.iloc[-1]:.2f}%")
    print(f"  最大回撤: {max_drawdown:.2f}%")

    return {
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "total_return": cumulative.iloc[-1],
        "max_drawdown": max_drawdown,
    }


# 执行回测
result_no_sentiment = backtest_two_board(START_DATE, END_DATE, with_sentiment=False)
result_with_sentiment = backtest_two_board(START_DATE, END_DATE, with_sentiment=True)

print("\n" + "=" * 70)
print("回测结果对比")
print("=" * 70)

if result_no_sentiment:
    print(f"\n无情绪开关:")
    print(f"  交易次数: {result_no_sentiment['total_trades']}")
    print(f"  胜率: {result_no_sentiment['win_rate']:.2f}%")
    print(f"  累计收益: {result_no_sentiment['total_return']:.2f}%")
    print(f"  最大回撤: {result_no_sentiment['max_drawdown']:.2f}%")

if result_with_sentiment:
    print(f"\n有情绪开关:")
    print(f"  交易次数: {result_with_sentiment['total_trades']}")
    print(f"  胜率: {result_with_sentiment['win_rate']:.2f}%")
    print(f"  累计收益: {result_with_sentiment['total_return']:.2f}%")
    print(f"  最大回撤: {result_with_sentiment['max_drawdown']:.2f}%")

print("\n回测完成!")
