#!/usr/bin/env python3
"""
任务04v2：二板2021-2023历史实测验证
严格按任务要求：逐年实测、年度对比、市场环境关联、策略层回测、稳定性判定
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务04v2：二板策略2021-2023历史实测验证")
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
        all_stocks,
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


def get_hl_stock(initial_list, date):
    """获取涨停股票"""
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    hl_list = list(df.code)
    return hl_list


def get_shifted_date(date, days):
    """获取相对交易日"""
    from jqdata import get_all_trade_days

    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        return all_days[idx + days]
    return date


def filter_yzb(stock_list, date):
    """过滤一字板"""
    result = []
    for stock in stock_list:
        df = get_price(
            stock, end_date=date, frequency="daily", fields=["low", "high"], count=1
        )
        if df["low"].iloc[0] != df["high"].iloc[0]:
            result.append(stock)
    return result


def get_turnover_ratio(stock, date):
    """获取换手率"""
    hsl = HSL([stock], date)
    if stock in hsl[0]:
        return hsl[0][stock]
    return 0


def get_free_market_cap(stock, date):
    """获取自由流通市值"""
    q = query(
        valuation.code, valuation.market_cap, valuation.circulating_market_cap
    ).filter(valuation.code == stock)
    df = get_fundamentals(q, date=date)
    if len(df) > 0:
        circulating_cap = df["circulating_market_cap"].iloc[0]
        return circulating_cap
    return 0


def calc_zt_count(date):
    """计算涨停家数"""
    return len(get_zt_stocks(date))


def get_market_index_change(date):
    """获取上证指数涨跌幅"""
    try:
        df = get_price(
            "000001.XSHG", end_date=date, count=2, fields=["close"], panel=False
        )
        if len(df) >= 2:
            return (df.iloc[-1]["close"] / df.iloc[-2]["close"] - 1) * 100
    except:
        pass
    return 0


def backtest_year(year, with_emotion_threshold=10):
    """
    单年度回测
    year: 年份（如2021）
    with_emotion_threshold: 情绪阈值（涨停家数>=阈值才开仓）
    """
    print(f"\n{'=' * 80}")
    print(f"年份: {year} | 情绪阈值: {with_emotion_threshold}")
    print(f"{'=' * 80}")

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    results = {
        "year": year,
        "trades": [],
        "signal_count": 0,
        "trade_count": 0,
        "win_rate": 0,
        "avg_profit": 0,
        "avg_max_profit": 0,
        "profit_loss_ratio": 0,
        "max_drawdown": 0,
        "cumulative_return": 0,
        "monthly_returns": {},
        "emotion_days": 0,
        "total_days": len(trade_days),
        "emotion_triggered_days": 0,
        "avg_zt_count": 0,
        "market_index_return": 0,
    }

    zt_count_list = []
    market_returns_list = []

    for i, date in enumerate(trade_days[:-1]):
        next_date = trade_days[i + 1]

        zt_count = calc_zt_count(date)
        zt_count_list.append(zt_count)

        market_change = get_market_index_change(date)
        market_returns_list.append(market_change)

        if zt_count < with_emotion_threshold:
            results["emotion_days"] += 1
            continue

        results["emotion_triggered_days"] += 1

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

        prev_vol = (
            get_price(
                stock_list, end_date=date, count=2, fields=["volume"], panel=False
            )
            if len(stock_list) > 0
            else None
        )
        if prev_vol is not None and len(prev_vol) >= 2:
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

        results["signal_count"] += len(stock_list)

        if len(stock_list) == 0:
            continue

        stock_list_sorted = sorted(
            stock_list, key=lambda s: get_free_market_cap(s, date)
        )
        target_stock = stock_list_sorted[0] if len(stock_list_sorted) > 0 else None

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

        open_pct = (today_open / prev_close - 1) * 100
        is_zt_open = today_open == high_limit

        if is_zt_open:
            continue

        buy_price = today_open * 1.005

        sell_price = today_close

        max_profit_pct = (today_high / buy_price - 1) * 100
        profit_pct = (sell_price / buy_price - 1) * 100

        results["trades"].append(
            {
                "date": next_date,
                "stock": target_stock,
                "zt_count": zt_count,
                "open_pct": open_pct,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "high_price": today_high,
                "max_profit_pct": max_profit_pct,
                "profit_pct": profit_pct,
                "is_zt_open": is_zt_open,
            }
        )

    results["trade_count"] = len(results["trades"])

    if results["trade_count"] > 0:
        profits = [t["profit_pct"] for t in results["trades"]]
        max_profits = [t["max_profit_pct"] for t in results["trades"]]
        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p <= 0]

        results["win_rate"] = len(wins) / results["trade_count"] * 100
        results["avg_profit"] = np.mean(profits)
        results["avg_max_profit"] = np.mean(max_profits)

        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = np.mean(losses) if len(losses) > 0 else 0
        results["profit_loss_ratio"] = abs(avg_win / avg_loss) if avg_loss != 0 else 0

        cumulative = []
        cum = 0
        for p in profits:
            cum += p
            cumulative.append(cum)

        results["cumulative_return"] = cumulative[-1] if len(cumulative) > 0 else 0

        peak = 0
        max_dd = 0
        for c in cumulative:
            peak = max(peak, c)
            dd = peak - c
            max_dd = max(max_dd, dd)

        results["max_drawdown"] = max_dd

        for t in results["trades"]:
            month = t["date"][:7]
            if month not in results["monthly_returns"]:
                results["monthly_returns"][month] = {"count": 0, "return": 0, "wins": 0}
            results["monthly_returns"][month]["count"] += 1
            results["monthly_returns"][month]["return"] += t["profit_pct"]
            if t["profit_pct"] > 0:
                results["monthly_returns"][month]["wins"] += 1

    if len(zt_count_list) > 0:
        results["avg_zt_count"] = np.mean(zt_count_list)

    if len(market_returns_list) > 0:
        results["market_index_return"] = np.sum(market_returns_list)

    return results


def analyze_market_environment(year_results):
    """分析市场环境"""
    print(f"\n{'=' * 80}")
    print("市场环境关联分析")
    print(f"{'=' * 80}")

    for year, r in year_results.items():
        market_return = r["market_index_return"]
        avg_zt_count = r["avg_zt_count"]

        if market_return > 10:
            env_type = "牛市"
        elif market_return < -10:
            env_type = "熊市"
        else:
            env_type = "震荡市"

        print(f"\n{year}年市场环境:")
        print(f"  市场类型: {env_type}")
        print(f"  上证指数年度涨跌: {market_return:.2f}%")
        print(f"  平均涨停家数: {avg_zt_count:.2f}")
        print(f"  情绪触发天数: {r['emotion_triggered_days']}/{r['total_days']}")
        print(f"  策略表现:")
        print(f"    信号数量: {r['signal_count']}")
        print(f"    交易次数: {r['trade_count']}")
        print(f"    胜率: {r['win_rate']:.2f}%")
        print(f"    日内收益均值: {r['avg_profit']:.2f}%")
        print(f"    最大收益均值: {r['avg_max_profit']:.2f}%")
        print(f"    盈亏比: {r['profit_loss_ratio']:.2f}")
        print(f"    累计收益: {r['cumulative_return']:.2f}%")
        print(f"    最大回撤: {r['max_drawdown']:.2f}%")


def compare_years(year_results):
    """年度对比分析"""
    print(f"\n{'=' * 80}")
    print("年度对比分析")
    print(f"{'=' * 80}")

    print(
        f"\n{'年份':<10} {'信号数':<10} {'交易数':<10} {'胜率':<10} {'日内收益均值':<15} {'最大收益均值':<15} {'盈亏比':<10} {'累计收益':<12} {'最大回撤':<12}"
    )
    print("-" * 100)

    for year in [2021, 2022, 2023]:
        if year in year_results:
            r = year_results[year]
            print(
                f"{year}{' ':<8} {r['signal_count']:<10} {r['trade_count']:<10} {r['win_rate']:<10.2f} {r['avg_profit']:<15.2f} {r['avg_max_profit']:<15.2f} {r['profit_loss_ratio']:<10.2f} {r['cumulative_return']:<12.2f} {r['max_drawdown']:<12.2f}"
            )

    win_rates = [
        year_results[y]["win_rate"] for y in [2021, 2022, 2023] if y in year_results
    ]
    if len(win_rates) >= 2:
        win_rate_diff = max(win_rates) - min(win_rates)
        print(f"\n胜率稳定性:")
        print(f"  最高胜率: {max(win_rates):.2f}%")
        print(f"  最低胜率: {min(win_rates):.2f}%")
        print(f"  胜率差异: {win_rate_diff:.2f}%")
        print(f"  稳定性判定: {'稳定' if win_rate_diff < 15 else '不稳定'}")

    cumulative_returns = [
        year_results[y]["cumulative_return"]
        for y in [2021, 2022, 2023]
        if y in year_results
    ]
    positive_years = len([r for r in cumulative_returns if r > 0])
    print(f"\n收益稳定性:")
    print(f"  正收益年份数: {positive_years}/3")
    print(f"  通过门槛: {'是' if positive_years >= 2 else '否'} (至少2年收益为正)")


def determine_stability(year_results):
    """跨周期稳定性判定"""
    print(f"\n{'=' * 80}")
    print("跨周期稳定性判定")
    print(f"{'=' * 80}")

    win_rates = [
        year_results[y]["win_rate"]
        for y in [2021, 2022, 2023]
        if y in year_results and year_results[y]["trade_count"] > 0
    ]
    cumulative_returns = [
        year_results[y]["cumulative_return"]
        for y in [2021, 2022, 2023]
        if y in year_results
    ]

    positive_years = len([r for r in cumulative_returns if r > 0])
    win_rate_diff = max(win_rates) - min(win_rates) if len(win_rates) >= 2 else 100

    stability = "稳定"
    unstable_years = []

    if positive_years < 2:
        stability = "不稳定"
        unstable_years = [
            y
            for y in [2021, 2022, 2023]
            if y in year_results and year_results[y]["cumulative_return"] <= 0
        ]
    elif win_rate_diff >= 15:
        stability = "不稳定"
        unstable_years = [
            y
            for y in [2021, 2022, 2023]
            if y in year_results
            and (
                year_results[y]["win_rate"] == max(win_rates)
                or year_results[y]["win_rate"] == min(win_rates)
            )
        ]

    print(f"\n判定结果: {stability}")
    print(f"依据:")
    print(f"  1. 正收益年份数: {positive_years}/3 (门槛: 至少2年)")
    print(f"  2. 胜率差异: {win_rate_diff:.2f}% (门槛: <15%)")

    if stability == "不稳定":
        print(f"\n不稳定年份: {unstable_years}")
        for y in unstable_years:
            if y in year_results:
                r = year_results[y]
                print(f"  {y}年:")
                print(f"    累计收益: {r['cumulative_return']:.2f}%")
                print(f"    胜率: {r['win_rate']:.2f}%")
                print(f"    交易次数: {r['trade_count']}")

    print(f"\n失效条件识别:")
    for y in [2021, 2022, 2023]:
        if y in year_results:
            r = year_results[y]
            if r["trade_count"] == 0:
                print(f"  {y}年: 无交易信号（情绪阈值过滤过严或市场无机会）")
            elif r["cumulative_return"] < 0:
                print(f"  {y}年: 策略失效（收益为负）")
            elif r["win_rate"] < 80:
                print(f"  {y}年: 胜率偏低（{r['win_rate']:.2f}%）")

    return stability, unstable_years


def final_decision(year_results, stability):
    """最终决策"""
    print(f"\n{'=' * 80}")
    print("最终决策")
    print(f"{'=' * 80}")

    positive_years = len(
        [
            y
            for y in [2021, 2022, 2023]
            if y in year_results and year_results[y]["cumulative_return"] > 0
        ]
    )
    win_rates = [
        year_results[y]["win_rate"]
        for y in [2021, 2022, 2023]
        if y in year_results and year_results[y]["trade_count"] > 0
    ]
    win_rate_diff = max(win_rates) - min(win_rates) if len(win_rates) >= 2 else 100

    if positive_years >= 2 and win_rate_diff < 15 and stability == "稳定":
        decision = "Go"
        print(f"\n决策: Go")
        print(f"理由:")
        print(f"  1. 至少2年收益为正: ✓ ({positive_years}/3)")
        print(f"  2. 各年胜率差异<15%: ✓ ({win_rate_diff:.2f}%)")
        print(f"  3. 跨周期稳定: ✓")
    elif positive_years >= 1 or win_rate_diff < 20:
        decision = "Watch"
        print(f"\n决策: Watch")
        print(f"理由:")
        if positive_years < 2:
            print(f"  1. 正收益年份不足: {positive_years}/3 (需要至少2年)")
        if win_rate_diff >= 15:
            print(f"  2. 胜率差异过大: {win_rate_diff:.2f}% (需要<15%)")
        print(f"  3. 需进一步验证或优化")
    else:
        decision = "No-Go"
        print(f"\n决策: No-Go")
        print(f"理由:")
        print(f"  1. 跨周期稳定性不足")
        print(f"  2. 收益与胜率均不符合门槛")

    return decision


if __name__ == "__main__":
    year_results = {}

    for year in [2021, 2022, 2023]:
        print(f"\n开始测试 {year} 年...")
        year_results[year] = backtest_year(year, with_emotion_threshold=10)

    analyze_market_environment(year_results)
    compare_years(year_results)
    stability, unstable_years = determine_stability(year_results)
    decision = final_decision(year_results, stability)

    output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/second_board_historical_2021_2023.json"
    with open(output_path, "w") as f:
        json.dump(year_results, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存至: {output_path}")
    print(f"\n任务04v2执行完成")
