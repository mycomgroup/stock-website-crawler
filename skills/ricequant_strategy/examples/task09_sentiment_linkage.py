#!/usr/bin/env python3
"""任务09：二板与情绪层联动测试 - RiceQuant版本
测试三组对比，使用最近日期数据（2024-01-01 至 2025-03-31）
"""

import pandas as pd
import numpy as np
import json

print("=" * 70)
print("任务09：二板与情绪层联动测试（RiceQuant完整回测）")
print("测试时间：2024-01-01 至 2025-03-31")
print("=" * 70)

START_DATE = "2024-01-01"
END_DATE = "2025-03-31"


def get_zt_stocks_rq(date):
    """获取涨停股票列表（RiceQuant API）"""
    try:
        all_stocks = list(all_instruments(type="CS", date=date).order_book_id)
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

        prices = get_price(
            all_stocks[:500],
            start_date=date,
            end_date=date,
            fields=["close", "limit_up"],
            expect_df=True,
        )

        if prices is None or len(prices) == 0:
            return []

        prices = prices.reset_index()
        zt_df = prices[prices["close"] == prices["limit_up"]]
        return list(zt_df["order_book_id"].unique())
    except:
        return []


def get_prev_trade_date_rq(date):
    """获取前一交易日"""
    try:
        trade_dates = get_trading_dates(start_date="2024-01-01", end_date=date)
        if len(trade_dates) > 1:
            return str(trade_dates[-2].date())
        return None
    except:
        return None


def filter_yzb_rq(stock_list, date):
    """过滤一字板"""
    result = []
    for s in stock_list[:50]:
        try:
            prices = get_price(
                s,
                start_date=date,
                end_date=date,
                fields=["low", "high"],
                expect_df=True,
            )
            if prices is not None and len(prices) > 0:
                if prices["low"].iloc[-1] != prices["high"].iloc[-1]:
                    result.append(s)
        except:
            continue
    return result


def get_turnover_rq(stock, date):
    """获取换手率"""
    try:
        df = get_turnover(stock, start_date=date, end_date=date)
        if df is not None and len(df) > 0:
            return df.iloc[-1]
        return 0
    except:
        return 0


def get_market_cap_rq(stock, date):
    """获取流通市值"""
    try:
        df = get_fundamentals(
            query(fundamentals.eod.market_cap).filter(
                fundamentals.eod.stockcode == stock
            ),
            entry_date=date,
            interval="1d",
        )
        if df is not None and len(df) > 0:
            return df["market_cap"].iloc[-1]
        return 0
    except:
        return 0


def check_volume_shrink_rq(stock, date, threshold=1.875):
    """检查缩量条件"""
    try:
        prev_date = get_prev_trade_date_rq(date)
        prev2_date = get_prev_trade_date_rq(prev_date) if prev_date else None

        if prev_date and prev2_date:
            prices = get_price(
                stock,
                start_date=prev2_date,
                end_date=prev_date,
                fields=["volume"],
                expect_df=True,
            )
            if prices is not None and len(prices) >= 2:
                yesterday_vol = prices["volume"].iloc[-1]
                prev2_vol = prices["volume"].iloc[-2]
                if prev2_vol > 0:
                    ratio = yesterday_vol / prev2_vol
                    return ratio <= threshold
        return True
    except:
        return True


def backtest_group_rq(
    start_date,
    end_date,
    sentiment_mode="none",
    sentiment_threshold=10,
    volume_shrink=True,
):
    """回测函数（RiceQuant版本）"""
    mode_str = {
        "none": "无情绪过滤",
        "hard_switch": f"情绪硬开关（涨停≥{sentiment_threshold})",
        "position_adjust": "情绪仓位调节",
    }

    print(f"\n测试组：{mode_str[sentiment_mode]}")
    print("-" * 70)

    trade_days = get_trading_dates(start_date=start_date, end_date=end_date)
    results = []
    zt_distribution = {"low": 0, "medium": 0, "high": 0, "very_high": 0}

    for i, date_dt in enumerate(trade_days[:-1]):
        date = str(date_dt.date())
        next_date = str(trade_days[i + 1].date())

        prev_date = get_prev_trade_date_rq(date)
        if prev_date is None:
            continue

        prev2_date = get_prev_trade_date_rq(prev_date)

        # 获取涨停股票数量
        zt_count = len(get_zt_stocks_rq(date))

        # 统计涨停家数分布
        if zt_count < 10:
            zt_distribution["low"] += 1
        elif zt_count < 20:
            zt_distribution["medium"] += 1
        elif zt_count < 30:
            zt_distribution["high"] += 1
        else:
            zt_distribution["very_high"] += 1

        # 情绪处理
        position_size = 1.0

        if sentiment_mode == "hard_switch":
            if zt_count < sentiment_threshold:
                continue

        elif sentiment_mode == "position_adjust":
            if zt_count < 10:
                continue
            elif zt_count < 20:
                position_size = 0.5
            elif zt_count < 30:
                position_size = 0.8
            else:
                position_size = 1.0

        # 获取涨停股
        hl_today = get_zt_stocks_rq(date)
        hl_prev = get_zt_stocks_rq(prev_date)
        hl_prev2 = get_zt_stocks_rq(prev2_date) if prev2_date else []

        # 非一字板过滤
        non_yzb = filter_yzb_rq(hl_today, date)

        # 二板筛选
        candidates = list(set(non_yzb) & set(hl_prev) - set(hl_prev2))

        if len(candidates) == 0:
            continue

        # 换手率过滤
        low_hsl = [s for s in candidates[:20] if get_turnover_rq(s, date) < 30]

        # 缩量条件过滤
        if volume_shrink:
            low_hsl = [s for s in low_hsl if check_volume_shrink_rq(s, date, 1.875)]

        if len(low_hsl) == 0:
            continue

        # 按市值排序取最小
        caps = [(s, get_market_cap_rq(s, date)) for s in low_hsl]
        caps.sort(key=lambda x: x[1])
        target = caps[0][0] if len(caps) > 0 else None

        if target is None:
            continue

        # 模拟交易
        try:
            next_prices = get_price(
                target,
                start_date=next_date,
                end_date=next_date,
                fields=["open", "high", "close", "limit_up"],
                expect_df=True,
            )

            if next_prices is None or len(next_prices) == 0:
                continue

            open_price = next_prices["open"].iloc[-1]
            high_price = next_prices["high"].iloc[-1]
            limit_up = next_prices["limit_up"].iloc[-1]
            close_price = next_prices["close"].iloc[-1]

            is_zt_open = open_price == limit_up
            if is_zt_open:
                continue

            buy_price = open_price * 1.005
            sell_price = max(high_price, close_price)

            profit_pct = (sell_price / buy_price - 1) * 100

            results.append(
                {
                    "date": next_date,
                    "stock": target,
                    "profit": profit_pct,
                    "position_size": position_size,
                    "zt_count": zt_count,
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

    if sentiment_mode == "position_adjust":
        weighted_profit = df["profit"] * df["position_size"]
        cumulative = weighted_profit.cumsum()
    else:
        cumulative = df["profit"].cumsum()

    peak = cumulative.cummax()
    drawdown = peak - cumulative
    max_drawdown = drawdown.max()

    annual_return = (
        cumulative.iloc[-1] * 250 / len(trade_days) if len(trade_days) > 0 else 0
    )

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

    print(f"\n  涨停家数分布:")
    print(f"    <10（跳过）: {zt_distribution['low']}天")
    print(f"    10-20（50%仓）: {zt_distribution['medium']}天")
    print(f"    20-30（80%仓）: {zt_distribution['high']}天")
    print(f"    >=30（满仓）: {zt_distribution['very_high']}天")

    return {
        "mode": sentiment_mode,
        "mode_str": mode_str[sentiment_mode],
        "threshold": sentiment_threshold if sentiment_mode == "hard_switch" else None,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "profit_loss_ratio": profit_loss_ratio,
        "avg_profit": avg_profit,
        "total_return": cumulative.iloc[-1],
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "zt_distribution": zt_distribution,
    }


print("\n" + "=" * 70)
print("测试时间段：2024-01-01 至 2025-03-31")
print("=" * 70)

# 组1：无情绪过滤
r1 = backtest_group_rq(START_DATE, END_DATE, sentiment_mode="none", volume_shrink=True)

# 组2：情绪硬开关（涨停≥10）
r2 = backtest_group_rq(
    START_DATE,
    END_DATE,
    sentiment_mode="hard_switch",
    sentiment_threshold=10,
    volume_shrink=True,
)

# 组2b：情绪硬开关（涨停≥15）
r2b = backtest_group_rq(
    START_DATE,
    END_DATE,
    sentiment_mode="hard_switch",
    sentiment_threshold=15,
    volume_shrink=True,
)

# 组3：情绪仓位调节
r3 = backtest_group_rq(
    START_DATE, END_DATE, sentiment_mode="position_adjust", volume_shrink=True
)

print("\n" + "=" * 70)
print("最终结果对比")
print("=" * 70)

all_results = [r for r in [r1, r2, r2b, r3] if r]

print(
    f"\n{'模式':<30} {'交易次数':<10} {'胜率':<10} {'盈亏比':<10} {'累计收益':<12} {'最大回撤':<12}"
)
print("-" * 100)
for r in all_results:
    print(
        f"{r['mode_str']:<30} {r['total_trades']:<10} {r['win_rate']:<10.2f} {r['profit_loss_ratio']:<10.2f} {r['total_return']:<12.2f} {r['max_drawdown']:<12.2f}"
    )

# 对比分析
if all_results and r1:
    print("\n" + "=" * 70)
    print("对比分析")
    print("=" * 70)

    base = r1

    for r in [r2, r2b, r3]:
        if r:
            print(f"\n{r['mode_str']} vs 无情绪过滤:")

            return_pct_change = r["total_return"] / base["total_return"] * 100 - 100
            print(
                f"  收益变化: {r['total_return'] - base['total_return']:.2f}% ({return_pct_change:.1f}%)"
            )

            drawdown_pct_change = r["max_drawdown"] / base["max_drawdown"] * 100 - 100
            print(
                f"  回撤变化: {r['max_drawdown'] - base['max_drawdown']:.2f}% ({drawdown_pct_change:.1f}%)"
            )

            trades_pct_change = r["total_trades"] / base["total_trades"] * 100 - 100
            print(
                f"  交易次数变化: {r['total_trades'] - base['total_trades']} ({trades_pct_change:.1f}%)"
            )

            print(f"  胜率变化: {r['win_rate'] - base['win_rate']:.2f}%")

print("\n回测完成!")
