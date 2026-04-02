#!/usr/bin/env python3
"""234板分板位回测 - 2024全年测试"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("234板分板位回测 - 2024全年测试")
print("=" * 70)

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"


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


def backtest_board(board_level, start_date, end_date, sentiment_threshold=None):
    """分板位回测

    Args:
        board_level: 'two', 'three', 'four'
        sentiment_threshold: 涨停家数阈值，None表示无情绪开关
    """
    print(f"\n{board_level}板回测 | 情绪阈值={sentiment_threshold}")

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    results = []

    for i, date_dt in enumerate(trade_days[:-1]):
        date = date_dt.strftime("%Y-%m-%d")
        next_date = trade_days[i + 1].strftime("%Y-%m-%d")

        prev_date = get_prev_date(date)
        if prev_date is None:
            continue

        prev2_date = get_prev_date(prev_date)
        prev3_date = get_prev_date(prev2_date) if prev2_date else None

        if sentiment_threshold:
            zt_count = len(get_zt_stocks(date))
            if zt_count < sentiment_threshold:
                continue

        hl_today = get_zt_stocks(date)
        hl_prev = get_zt_stocks(prev_date)
        hl_prev2 = get_zt_stocks(prev2_date) if prev2_date else []
        hl_prev3 = get_zt_stocks(prev3_date) if prev3_date else []

        non_yzb = filter_yzb(hl_today, date)

        if board_level == "two":
            candidates = list(set(non_yzb) & set(hl_prev) - set(hl_prev2))
        elif board_level == "three":
            candidates = list(
                set(non_yzb) & set(hl_prev) & set(hl_prev2) - set(hl_prev3)
            )
        elif board_level == "four":
            candidates = list(
                set(non_yzb) & set(hl_prev) & set(hl_prev2) & set(hl_prev3)
            )
        else:
            continue

        low_hsl = [s for s in candidates if get_turnover_ratio(s, date) < 30]

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
    win_trades = len(df[df["profit"] > 0])
    win_rate = win_trades / total_trades * 100 if total_trades > 0 else 0
    avg_profit = df["profit"].mean()

    cumulative = df["profit"].cumsum()
    peak = cumulative.cummax()
    drawdown = peak - cumulative
    max_drawdown = drawdown.max()

    annual_return = (
        cumulative.iloc[-1] * 250 / len(trade_days) if len(trade_days) > 0 else 0
    )

    print(f"  交易次数: {total_trades}")
    print(f"  胜率: {win_rate:.2f}%")
    print(f"  平均收益: {avg_profit:.2f}%")
    print(f"  累计收益: {cumulative.iloc[-1]:.2f}%")
    print(f"  年化收益: {annual_return:.2f}%")
    print(f"  最大回撤: {max_drawdown:.2f}%")

    return {
        "board": board_level,
        "sentiment": sentiment_threshold,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "total_return": cumulative.iloc[-1],
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
    }


# 测试配置
test_configs = [
    ("two", None),  # 二板，无情绪
    ("two", 20),  # 二板，涨停>=20
    ("three", None),  # 三板，无情绪
    ("three", 30),  # 三板，涨停>=30
    ("four", None),  # 四板，无情绪
]

all_results = []

for board_level, sentiment in test_configs:
    result = backtest_board(board_level, START_DATE, END_DATE, sentiment)
    if result:
        all_results.append(result)

print("\n" + "=" * 70)
print("最终结论")
print("=" * 70)

valid_boards = [
    r for r in all_results if r["total_return"] > 0 and r["max_drawdown"] < 30
]

if len([r for r in all_results if r["board"] == "two"]) > 0:
    two_result = [r for r in all_results if r["board"] == "two"][0]
    print(
        f"\n二板: 累计收益={two_result['total_return']:.2f}%, 胜率={two_result['win_rate']:.2f}%, 回撤={two_result['max_drawdown']:.2f}%"
    )
    print(f"  结论: {'有效' if two_result['total_return'] > 0 else '无效'}")

if len([r for r in all_results if r["board"] == "three"]) > 0:
    three_result = [r for r in all_results if r["board"] == "three"][0]
    print(
        f"\n三板: 累计收益={three_result['total_return']:.2f}%, 胜率={three_result['win_rate']:.2f}%, 回撤={three_result['max_drawdown']:.2f}%"
    )
    print(f"  结论: {'有效' if three_result['total_return'] > 0 else '无效'}")

if len([r for r in all_results if r["board"] == "four"]) > 0:
    four_result = [r for r in all_results if r["board"] == "four"][0]
    print(
        f"\n四板: 累计收益={four_result['total_return']:.2f}%, 胜率={four_result['win_rate']:.2f}%, 回撤={four_result['max_drawdown']:.2f}%"
    )
    print(f"  结论: {'有效' if four_result['total_return'] > 0 else '无效'}")

print("\n最终建议:")
if (
    len([r for r in all_results if r["board"] == "two" and r["total_return"] > 0]) > 0
    and len([r for r in all_results if r["board"] == "three" and r["total_return"] > 0])
    > 0
):
    print("保留二板+三板")
elif len([r for r in all_results if r["board"] == "two" and r["total_return"] > 0]) > 0:
    print("只保留二板")
else:
    print("整体No-Go")

print("\n回测完成!")
