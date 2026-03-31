#!/usr/bin/env python3
"""
任务04v2简化版：二板2021单年实测（轻量版）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("二板策略2021年实测验证（轻量版）")
print("=" * 80)


def get_zt_stocks(date):
    """获取涨停股票列表"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def get_hl_stock(initial_list, date):
    """获取涨停股票"""
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    return list(df.code)


def get_shifted_date(date, days):
    """获取相对交易日"""
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        return all_days[idx + days]
    return date


def filter_yzb(stock_list, date):
    """过滤一字板"""
    result = []
    for stock in stock_list:
        try:
            df = get_price(
                stock, end_date=date, frequency="daily", fields=["low", "high"], count=1
            )
            if len(df) > 0 and df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(stock)
        except:
            pass
    return result


def get_turnover_ratio(stock, date):
    """获取换手率"""
    try:
        hsl = HSL([stock], date)
        if stock in hsl[0]:
            return hsl[0][stock]
    except:
        pass
    return 0


def get_free_market_cap(stock, date):
    """获取流通市值"""
    try:
        q = query(valuation.circulating_market_cap).filter(valuation.code == stock)
        df = get_fundamentals(q, date=date)
        if len(df) > 0:
            return df["circulating_market_cap"].iloc[0]
    except:
        pass
    return 0


def calc_zt_count(date):
    """计算涨停家数"""
    try:
        return len(get_zt_stocks(date))
    except:
        return 0


year = 2021
emotion_threshold = 10

print(f"\n测试年份: {year}, 情绪阈值: {emotion_threshold}")

start_date = f"{year}-01-01"
end_date = f"{year}-12-31"

trade_days = get_trade_days(start_date=start_date, end_date=end_date)
print(f"交易日数: {len(trade_days)}")

trades = []
signal_count = 0
emotion_triggered_days = 0

print(f"\n开始逐日测试...")

for i, date in enumerate(trade_days[:-1]):
    next_date = trade_days[i + 1]

    try:
        zt_count = calc_zt_count(date)
    except:
        zt_count = 0
        continue

    if zt_count < emotion_threshold:
        continue

    emotion_triggered_days += 1

    try:
        prev_date = get_shifted_date(date, -1)
        prev2_date = get_shifted_date(date, -2)

        initial_list = get_all_securities("stock", date).index.tolist()
        initial_list = [
            s
            for s in initial_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        hl_1d = filter_yzb(get_hl_stock(initial_list, date), date)
        hl_2d = get_hl_stock(initial_list, prev_date)
        hl_3d = get_hl_stock(initial_list, prev2_date)

        stock_list = list(set(hl_1d) & set(hl_2d) - set(hl_3d))

        stock_list = [s for s in stock_list if get_turnover_ratio(s, date) < 30]

        if len(stock_list) > 0:
            prev_vol = get_price(
                stock_list, end_date=date, count=2, fields=["volume"], panel=False
            )
            shrink_stocks = []
            for stock in stock_list:
                stock_vol = prev_vol[prev_vol["code"] == stock]
                if len(stock_vol) >= 2:
                    vol_ratio = (
                        stock_vol.iloc[-1]["volume"] / stock_vol.iloc[-2]["volume"]
                    )
                    if vol_ratio <= 1.875:
                        shrink_stocks.append(stock)
            stock_list = shrink_stocks

        signal_count += len(stock_list)

        if len(stock_list) == 0:
            continue

        stock_list_sorted = sorted(
            stock_list, key=lambda s: get_free_market_cap(s, date)
        )
        target_stock = stock_list_sorted[0]

        if target_stock is None:
            continue

        try:
            today_open = get_price(
                target_stock, end_date=next_date, count=1, fields=["open"], panel=False
            ).iloc[0]["open"]
            today_high = get_price(
                target_stock, end_date=next_date, count=1, fields=["high"], panel=False
            ).iloc[0]["high"]
            today_close = get_price(
                target_stock, end_date=next_date, count=1, fields=["close"], panel=False
            ).iloc[0]["close"]
            prev_close = get_price(
                target_stock, end_date=date, count=1, fields=["close"], panel=False
            ).iloc[0]["close"]
            high_limit = get_price(
                target_stock,
                end_date=next_date,
                count=1,
                fields=["high_limit"],
                panel=False,
            ).iloc[0]["high_limit"]
        except:
            continue

        is_zt_open = today_open == high_limit

        if is_zt_open:
            continue

        buy_price = today_open * 1.005
        sell_price = today_close

        max_profit_pct = (today_high / buy_price - 1) * 100
        profit_pct = (sell_price / buy_price - 1) * 100

        trades.append(
            {
                "date": next_date,
                "stock": target_stock,
                "zt_count": zt_count,
                "profit_pct": profit_pct,
                "max_profit_pct": max_profit_pct,
            }
        )

        if i % 50 == 0:
            print(f"已处理 {i}/{len(trade_days)} 天, 累计交易: {len(trades)}")

    except Exception as e:
        continue

print(f"\n测试完成!")

trade_count = len(trades)
print(f"信号数量: {signal_count}")
print(f"交易次数: {trade_count}")
print(f"情绪触发天数: {emotion_triggered_days}")

if trade_count > 0:
    profits = [t["profit_pct"] for t in trades]
    max_profits = [t["max_profit_pct"] for t in trades]
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    win_rate = len(wins) / trade_count * 100
    avg_profit = np.mean(profits)
    avg_max_profit = np.mean(max_profits)

    avg_win = np.mean(wins) if len(wins) > 0 else 0
    avg_loss = np.mean(losses) if len(losses) > 0 else 0
    profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    cumulative = []
    cum = 0
    for p in profits:
        cum += p
        cumulative.append(cum)

    cumulative_return = cumulative[-1] if len(cumulative) > 0 else 0

    peak = 0
    max_dd = 0
    for c in cumulative:
        peak = max(peak, c)
        dd = peak - c
        max_dd = max(max_dd, dd)

    print(f"\n{year}年实测结果:")
    print(f"  交易次数: {trade_count}")
    print(f"  胜率: {win_rate:.2f}%")
    print(f"  日内收益均值: {avg_profit:.2f}%")
    print(f"  最大收益均值: {avg_max_profit:.2f}%")
    print(f"  盈亏比: {profit_loss_ratio:.2f}")
    print(f"  累计收益: {cumulative_return:.2f}%")
    print(f"  最大回撤: {max_dd:.2f}%")

    results = {
        "year": year,
        "signal_count": signal_count,
        "trade_count": trade_count,
        "win_rate": win_rate,
        "avg_profit": avg_profit,
        "avg_max_profit": avg_max_profit,
        "profit_loss_ratio": profit_loss_ratio,
        "cumulative_return": cumulative_return,
        "max_drawdown": max_dd,
        "emotion_triggered_days": emotion_triggered_days,
        "trades": trades,
    }

    output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/second_board_2021_lite.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n结果已保存至: {output_path}")

print("\n2021年测试完成")
