#!/usr/bin/env python3
"""234板分板位回测 - 优化版本
包含：情绪开关优化、缩量条件、市值过滤、成交率场景
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("234板分板位回测 - 优化版本")
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


def check_volume_shrink(stock, date, threshold=1.875):
    """检查缩量条件：昨日量 <= 前日量 * threshold"""
    try:
        prev_date = get_prev_date(date)
        prev2_date = get_prev_date(prev_date)

        if prev_date and prev2_date:
            df = get_price(
                stock, end_date=prev_date, count=2, fields=["volume"], panel=False
            )
            if len(df) >= 2:
                yesterday_vol = df.iloc[-1]["volume"]
                prev2_vol = df.iloc[-2]["volume"]
                if prev2_vol > 0:
                    ratio = yesterday_vol / prev2_vol
                    return ratio <= threshold
        return True
    except:
        return True


def backtest_board_optimized(
    board_level,
    start_date,
    end_date,
    sentiment_threshold=None,
    volume_shrink=True,
    cap_range=None,
    fill_rate=None,
):
    """优化版回测

    Args:
        board_level: 'two', 'three'
        sentiment_threshold: 涨停家数阈值，None表示无情绪开关
        volume_shrink: 是否添加缩量条件
        cap_range: (min_cap, max_cap) 市值范围（亿）
        fill_rate: 成交率，None=100%（非涨停开盘），30=涨停排板30%，10=涨停排板10%
    """
    config_str = f"{board_level}板 | 情绪={sentiment_threshold} | 缩量={volume_shrink} | 市值={cap_range} | 成交率={fill_rate}"
    print(f"\n{config_str}")

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

        # 情绪开关
        if sentiment_threshold:
            zt_count = len(get_zt_stocks(date))
            if zt_count < sentiment_threshold:
                continue

        # 获取涨停股
        hl_today = get_zt_stocks(date)
        hl_prev = get_zt_stocks(prev_date)
        hl_prev2 = get_zt_stocks(prev2_date) if prev2_date else []
        hl_prev3 = get_zt_stocks(prev3_date) if prev3_date else []

        # 非一字板过滤
        non_yzb = filter_yzb(hl_today, date)

        # 板位筛选
        if board_level == "two":
            candidates = list(set(non_yzb) & set(hl_prev) - set(hl_prev2))
        elif board_level == "three":
            candidates = list(
                set(non_yzb) & set(hl_prev) & set(hl_prev2) - set(hl_prev3)
            )
        else:
            continue

        # 换手率过滤
        low_hsl = [s for s in candidates if get_turnover_ratio(s, date) < 30]

        # 缩量条件过滤
        if volume_shrink:
            low_hsl = [s for s in low_hsl if check_volume_shrink(s, date, 1.875)]

        # 市值过滤
        if cap_range:
            min_cap, max_cap = cap_range
            cap_filtered = []
            for s in low_hsl:
                cap = get_free_cap(s, date)
                if min_cap <= cap <= max_cap:
                    cap_filtered.append(s)
            low_hsl = cap_filtered

        if len(low_hsl) == 0:
            continue

        # 按市值排序取最小
        caps = [(s, get_free_cap(s, date)) for s in low_hsl]
        caps.sort(key=lambda x: x[1])
        target = caps[0][0] if len(caps) > 0 else None

        if target is None:
            continue

        # 模拟交易
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
            close_price = next_prices.iloc[0]["close"]

            is_zt_open = open_price == high_limit

            # 成交率场景
            if fill_rate is None:
                # 非涨停开盘买入
                if is_zt_open:
                    continue
                buy_price = open_price * 1.005
            elif fill_rate == 30:
                # 涨停排板30%成交率
                if is_zt_open and np.random.random() > 0.3:
                    continue
                buy_price = open_price * 1.01
            elif fill_rate == 10:
                # 涨停排板10%成交率
                if is_zt_open and np.random.random() > 0.1:
                    continue
                buy_price = open_price * 1.015

            # 卖出价格：取最高价和收盘价的较大值
            sell_price = max(high_price, close_price)

            profit_pct = (sell_price / buy_price - 1) * 100

            results.append(
                {
                    "date": next_date,
                    "stock": target,
                    "profit": profit_pct,
                    "is_zt_open": is_zt_open,
                    "fill_rate": fill_rate,
                }
            )
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

    # 计算盈亏比
    wins = df[df["profit"] > 0]["profit"]
    losses = df[df["profit"] <= 0]["profit"]
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = abs(losses.mean()) if len(losses) > 0 else 0
    profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    print(f"  交易次数: {total_trades}")
    print(f"  胜率: {win_rate:.2f}%")
    print(f"  盈亏比: {profit_loss_ratio:.2f}")
    print(f"  平均收益: {avg_profit:.2f}%")
    print(f"  累计收益: {cumulative.iloc[-1]:.2f}%")
    print(f"  年化收益: {annual_return:.2f}%")
    print(f"  最大回撤: {max_drawdown:.2f}%")

    return {
        "config": config_str,
        "board": board_level,
        "sentiment": sentiment_threshold,
        "volume_shrink": volume_shrink,
        "cap_range": cap_range,
        "fill_rate": fill_rate,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "profit_loss_ratio": profit_loss_ratio,
        "avg_profit": avg_profit,
        "total_return": cumulative.iloc[-1],
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
    }


print("\n" + "=" * 70)
print("测试1：情绪开关优化（涨停≥15/10）")
print("=" * 70)

# 二板：放宽情绪阈值
r1 = backtest_board_optimized("two", START_DATE, END_DATE, sentiment_threshold=15)
r2 = backtest_board_optimized("two", START_DATE, END_DATE, sentiment_threshold=10)

print("\n" + "=" * 70)
print("测试2：添加缩量条件")
print("=" * 70)

r3 = backtest_board_optimized(
    "two", START_DATE, END_DATE, sentiment_threshold=15, volume_shrink=True
)
r4 = backtest_board_optimized(
    "three", START_DATE, END_DATE, sentiment_threshold=20, volume_shrink=True
)

print("\n" + "=" * 70)
print("测试3：添加市值上下限")
print("=" * 70)

# 二板：5-20亿，三板：10-30亿
r5 = backtest_board_optimized(
    "two",
    START_DATE,
    END_DATE,
    sentiment_threshold=15,
    volume_shrink=True,
    cap_range=(5, 20),
)
r6 = backtest_board_optimized(
    "three",
    START_DATE,
    END_DATE,
    sentiment_threshold=20,
    volume_shrink=True,
    cap_range=(10, 30),
)

print("\n" + "=" * 70)
print("测试4：涨停排板成交率场景（基于优化版本）")
print("=" * 70)

# 二板：优化版本 + 涨停排板30%
r7 = backtest_board_optimized(
    "two",
    START_DATE,
    END_DATE,
    sentiment_threshold=15,
    volume_shrink=True,
    cap_range=(5, 20),
    fill_rate=30,
)
# 二板：优化版本 + 涨停排板10%
r8 = backtest_board_optimized(
    "two",
    START_DATE,
    END_DATE,
    sentiment_threshold=15,
    volume_shrink=True,
    cap_range=(5, 20),
    fill_rate=10,
)

print("\n" + "=" * 70)
print("最终结果对比")
print("=" * 70)

all_results = [r for r in [r1, r2, r3, r4, r5, r6, r7, r8] if r]

print(
    f"\n{'配置':<60} {'交易':<6} {'胜率':<8} {'盈亏比':<8} {'累计收益':<10} {'回撤':<8}"
)
print("-" * 100)
for r in all_results:
    config_short = r["config"][:55] + "..." if len(r["config"]) > 55 else r["config"]
    print(
        f"{config_short:<60} {r['total_trades']:<6} {r['win_rate']:<8.2f} {r['profit_loss_ratio']:<8.2f} {r['total_return']:<10.2f} {r['max_drawdown']:<8.2f}"
    )

# 找出最优配置
if all_results:
    best = max(all_results, key=lambda x: x["total_return"])
    print(f"\n最优配置: {best['config']}")
    print(f"  累计收益: {best['total_return']:.2f}%")
    print(f"  最大回撤: {best['max_drawdown']:.2f}%")
    print(f"  胜率: {best['win_rate']:.2f}%")

print("\n回测完成!")
