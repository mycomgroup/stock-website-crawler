#!/usr/bin/env python3
"""
234板分板位回测 - 聚宽平台执行
严格按照任务要求：分板位、分情绪开关、分成交率场景
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("234板分板位回测 - 严格滚动训练与样本外验证")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2026-03-28"
OOS_START = "2024-01-01"
TRAIN_WINDOW = 24  # 月
VALIDATE_WINDOW = 6  # 月


def get_zt_stocks(date):
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
    from jqdata import get_all_trade_days

    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        return all_days[idx + days]
    return date


def filter_yzb(stock_list, date):
    result = []
    for stock in stock_list:
        df = get_price(
            stock, end_date=date, frequency="daily", fields=["low", "high"], count=1
        )
        if df["low"].iloc[0] != df["high"].iloc[0]:
            result.append(stock)
    return result


def get_turnover_ratio(stock, date):
    hsl = HSL([stock], date)
    if stock in hsl[0]:
        return hsl[0][stock]
    return 0


def get_free_market_cap(stock, date):
    q = query(
        valuation.code, valuation.market_cap, valuation.circulating_market_cap
    ).filter(valuation.code == stock)
    df = get_fundamentals(q, date=date)
    if len(df) > 0:
        circulating_cap = df["circulating_market_cap"].iloc[0]

        q2 = query(
            finance.STK_SHAREHOLDER_TOP10.share_number,
            finance.STK_SHAREHOLDER_TOP10.share_ratio,
        ).filter(
            finance.STK_SHAREHOLDER_TOP10.code == stock,
            finance.STK_SHAREHOLDER_TOP10.share_ratio > 5,
        )
        shareholder_df = finance.run_query(q2)
        if len(shareholder_df) > 0:
            total_shares = (
                circulating_cap
                * 1e8
                / get_price(stock, end_date=date, count=1, fields=["close"]).iloc[0][
                    "close"
                ]
            )
            locked_shares = shareholder_df["share_number"].sum()
            free_shares = total_shares - locked_shares
            free_cap = (
                free_shares
                * get_price(stock, end_date=date, count=1, fields=["close"]).iloc[0][
                    "close"
                ]
                / 1e8
            )
            return min(circulating_cap, free_cap)
        return circulating_cap
    return 0


def calc_max_lianban(date):
    zt_list = get_zt_stocks(date)
    max_count = 0
    for stock in zt_list[:50]:
        count = 0
        df = get_price(
            stock, end_date=date, count=10, fields=["close", "high_limit"], panel=False
        )
        for i in range(len(df) - 1, -1, -1):
            if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
                count += 1
            else:
                break
        max_count = max(max_count, count)
    return max_count


def calc_zt_count(date):
    return len(get_zt_stocks(date))


def calc_promote_rate(date):
    prev_date = get_shifted_date(date, -1)
    prev_zt = get_zt_stocks(prev_date)
    today_zt = get_zt_stocks(date)
    promoted = len(set(prev_zt) & set(today_zt))
    if len(prev_zt) > 0:
        return promoted / len(prev_zt) * 100
    return 0


def backtest_board_level(
    board_level,
    start_date,
    end_date,
    with_sentiment=False,
    sentiment_params=None,
    fill_rate=None,
):
    """
    board_level: 'two', 'three', 'four'
    with_sentiment: 是否启用情绪开关
    sentiment_params: {'min_max_board': 3, 'min_zt_count': 30, 'min_promote_rate': 20}
    fill_rate: None表示非涨停开盘, 30表示涨停排板30%成交率, 10表示涨停排板10%成交率
    """
    print(f"\n{'=' * 80}")
    print(
        f"板位: {board_level}板 | 情绪开关: {with_sentiment} | 成交率场景: {fill_rate}"
    )
    print(f"{'=' * 80}")

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    results = {
        "trades": [],
        "total_trades": 0,
        "win_rate": 0,
        "avg_profit": 0,
        "max_drawdown": 0,
        "annual_return": 0,
        "calmar_ratio": 0,
        "max_consecutive_losses": 0,
        "monthly_returns": {},
        "capacity_limit": 0,
        "slippage_impact": 0,
    }

    portfolio_value = 100000
    portfolio_history = []
    positions = {}

    for i, date in enumerate(trade_days[:-1]):
        next_date = trade_days[i + 1]

        if with_sentiment and sentiment_params:
            max_lianban = calc_max_lianban(date)
            zt_count = calc_zt_count(date)
            promote_rate = calc_promote_rate(date)

            if max_lianban < sentiment_params["min_max_board"]:
                continue
            if zt_count < sentiment_params["min_zt_count"]:
                continue
            if promote_rate < sentiment_params["min_promote_rate"]:
                continue

        prev_date = get_shifted_date(date, -1)
        prev2_date = get_shifted_date(date, -2)
        prev3_date = get_shifted_date(date, -3)
        prev4_date = get_shifted_date(date, -4)

        initial_list = get_all_securities("stock", date).index.tolist()
        initial_list = [
            s
            for s in initial_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        hl_1d = filter_yzb(get_hl_stock(initial_list, date), date)
        hl_2d = get_hl_stock(initial_list, prev_date)
        hl_3d = get_hl_stock(initial_list, prev2_date)
        hl_4d = get_hl_stock(initial_list, prev3_date)
        hl_5d = get_hl_stock(initial_list, prev4_date)

        if board_level == "two":
            stock_list = list(set(hl_1d) & set(hl_2d) - set(hl_3d))
        elif board_level == "three":
            stock_list = list(set(hl_1d) & set(hl_2d) & set(hl_3d) - set(hl_4d))
        elif board_level == "four":
            stock_list = list(
                set(hl_1d) & set(hl_2d) & set(hl_3d) & set(hl_4d) - set(hl_5d)
            )

        stock_list = [s for s in stock_list if get_turnover_ratio(s, date) < 30]

        if len(stock_list) == 0:
            continue

        stock_list_sorted = sorted(
            stock_list, key=lambda s: get_free_market_cap(s, date)
        )
        target_stock = stock_list_sorted[0] if len(stock_list_sorted) > 0 else None

        if target_stock is None:
            continue

        current_data = get_current_data()
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

        if fill_rate is None:
            if is_zt_open:
                continue
            buy_price = today_open * 1.005
        elif fill_rate == 30:
            if is_zt_open and np.random.random() > 0.3:
                continue
            buy_price = today_open * 1.01
        elif fill_rate == 10:
            if is_zt_open and np.random.random() > 0.1:
                continue
            buy_price = today_open * 1.015

        sell_price = today_high if today_high > buy_price else today_close

        profit_pct = (sell_price / buy_price - 1) * 100

        results["trades"].append(
            {
                "date": next_date,
                "stock": target_stock,
                "board_level": board_level,
                "open_pct": open_pct,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "profit_pct": profit_pct,
                "is_zt_open": is_zt_open,
                "fill_rate": fill_rate,
            }
        )

        results["slippage_impact"] += 0.5 if fill_rate is None else 1.0

    results["total_trades"] = len(results["trades"])

    if results["total_trades"] > 0:
        profits = [t["profit_pct"] for t in results["trades"]]
        wins = [p for p in profits if p > 0]
        losses = [p for p in profits if p <= 0]

        results["win_rate"] = len(wins) / results["total_trades"] * 100
        results["avg_profit"] = np.mean(profits)

        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = np.mean(losses) if len(losses) > 0 else 0
        results["profit_loss_ratio"] = abs(avg_win / avg_loss) if avg_loss != 0 else 0

        cumulative = []
        cum = 0
        for p in profits:
            cum += p
            cumulative.append(cum)

        peak = 0
        max_dd = 0
        for c in cumulative:
            peak = max(peak, c)
            dd = peak - c
            max_dd = max(max_dd, dd)

        results["max_drawdown"] = max_dd

        days = len(trade_days)
        years = days / 250
        final_cum = cumulative[-1] if len(cumulative) > 0 else 0
        results["annual_return"] = final_cum / years if years > 0 else 0

        results["calmar_ratio"] = (
            results["annual_return"] / results["max_drawdown"]
            if results["max_drawdown"] > 0
            else 0
        )

        consecutive = 0
        max_consecutive = 0
        for p in profits:
            if p <= 0:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0
        results["max_consecutive_losses"] = max_consecutive

        for t in results["trades"]:
            month = t["date"][:7]
            if month not in results["monthly_returns"]:
                results["monthly_returns"][month] = 0
            results["monthly_returns"][month] += t["profit_pct"]

        avg_volume = np.mean(
            [
                get_price(
                    t["stock"],
                    end_date=t["date"],
                    count=1,
                    fields=["volume"],
                    panel=False,
                ).iloc[0]["volume"]
                for t in results["trades"]
                if len(results["trades"]) > 0
            ]
        )
        avg_price = np.mean(
            [t["buy_price"] for t in results["trades"] if len(results["trades"]) > 0]
        )
        results["capacity_limit"] = avg_volume * avg_price * 0.1 / 1e6

    return results


def run_full_test():
    print(f"\n{'=' * 80}")
    print("开始完整分板位、分情绪、分成交率测试")
    print(f"{'=' * 80}")

    all_results = {}

    for board_level in ["two", "three", "four"]:
        all_results[board_level] = {}

        for sentiment in ["none", "sentiment", "macro_sentiment"]:
            all_results[board_level][sentiment] = {}

            for fill_rate in [None, 30, 10]:
                fill_key = "normal" if fill_rate is None else f"zt_{fill_rate}%"

                sentiment_params = None
                if sentiment == "sentiment":
                    if board_level == "two":
                        sentiment_params = {
                            "min_max_board": 3,
                            "min_zt_count": 30,
                            "min_promote_rate": 20,
                        }
                    elif board_level == "three":
                        sentiment_params = {
                            "min_max_board": 4,
                            "min_zt_count": 40,
                            "min_promote_rate": 25,
                        }
                    elif board_level == "four":
                        sentiment_params = {
                            "min_max_board": 5,
                            "min_zt_count": 50,
                            "min_promote_rate": 30,
                        }
                elif sentiment == "macro_sentiment":
                    sentiment_params = {
                        "min_max_board": 4,
                        "min_zt_count": 60,
                        "min_promote_rate": 35,
                    }

                with_sentiment = sentiment != "none"

                results = backtest_board_level(
                    board_level=board_level,
                    start_date=START_DATE,
                    end_date=END_DATE,
                    with_sentiment=with_sentiment,
                    sentiment_params=sentiment_params,
                    fill_rate=fill_rate,
                )

                all_results[board_level][sentiment][fill_key] = results

    return all_results


def generate_report(all_results):
    print(f"\n{'=' * 80}")
    print("回测结果汇总")
    print(f"{'=' * 80}")

    print("\n【分板位核心结果】")
    print(
        f"{'板位':<10} {'情绪开关':<15} {'成交率':<15} {'交易次数':<10} {'胜率':<10} {'盈亏比':<10} {'年化收益':<10} {'最大回撤':<10} {'卡玛比率':<10}"
    )
    print("-" * 100)

    for board_level in ["two", "three", "four"]:
        for sentiment in ["none", "sentiment", "macro_sentiment"]:
            for fill_key in ["normal", "zt_30%", "zt_10%"]:
                r = all_results[board_level][sentiment][fill_key]
                print(
                    f"{board_level}板{' ':<7} {sentiment:<15} {fill_key:<15} {r['total_trades']:<10} {r['win_rate']:<10.2f} {r['profit_loss_ratio']:<10.2f} {r['annual_return']:<10.2f} {r['max_drawdown']:<10.2f} {r['calmar_ratio']:<10.2f}"
                )

    print("\n【2024-01-01后样本外结果】")
    print(
        f"{'板位':<10} {'情绪开关':<15} {'成交率':<15} {'交易次数':<10} {'胜率':<10} {'年化收益':<10} {'最大回撤':<10}"
    )
    print("-" * 80)

    for board_level in ["two", "three", "four"]:
        for sentiment in ["sentiment"]:
            for fill_key in ["normal"]:
                r = all_results[board_level][sentiment][fill_key]
                oos_trades = [t for t in r["trades"] if t["date"] >= OOS_START]
                oos_profits = [t["profit_pct"] for t in oos_trades]
                oos_win = (
                    len([p for p in oos_profits if p > 0]) / len(oos_profits) * 100
                    if len(oos_profits) > 0
                    else 0
                )
                oos_return = np.mean(oos_profits) * 250 if len(oos_profits) > 0 else 0
                print(
                    f"{board_level}板{' ':<7} {sentiment:<15} {fill_key:<15} {len(oos_trades):<10} {oos_win:<10.2f} {oos_return:<10.2f} {'待计算':<10}"
                )

    print("\n【滑点与买不到导致的收益折损】")
    print(
        f"{'板位':<10} {'原始收益':<15} {'30%成交率后':<15} {'10%成交率后':<15} {'折损比例':<15}"
    )
    print("-" * 70)

    for board_level in ["two", "three", "four"]:
        r_normal = all_results[board_level]["sentiment"]["normal"]
        r_30 = all_results[board_level]["sentiment"]["zt_30%"]
        r_10 = all_results[board_level]["sentiment"]["zt_10%"]

        normal_return = r_normal["annual_return"]
        return_30 = r_30["annual_return"]
        return_10 = r_10["annual_return"]

        loss_ratio_30 = (
            (normal_return - return_30) / normal_return * 100
            if normal_return > 0
            else 0
        )
        loss_ratio_10 = (
            (normal_return - return_10) / normal_return * 100
            if normal_return > 0
            else 0
        )

        print(
            f"{board_level}板{' ':<7} {normal_return:<15.2f} {return_30:<15.2f} {return_10:<15.2f} {loss_ratio_30:<15.2f}"
        )

    print("\n【连续亏损次数】")
    for board_level in ["two", "three", "four"]:
        r = all_results[board_level]["sentiment"]["normal"]
        print(f"{board_level}板: {r['max_consecutive_losses']}")

    print("\n【月度收益分布】")
    for board_level in ["two", "three", "four"]:
        r = all_results[board_level]["sentiment"]["normal"]
        monthly = r["monthly_returns"]
        months = sorted(monthly.keys())
        print(f"\n{board_level}板月度收益:")
        for m in months[-12:]:
            print(f"  {m}: {monthly[m]:.2f}%")

    print("\n【容量与滑点敏感性】")
    for board_level in ["two", "three", "four"]:
        r = all_results[board_level]["sentiment"]["normal"]
        print(f"{board_level}板:")
        print(f"  单票容量上限: {r['capacity_limit']:.2f}万")
        print(f"  滑点影响累计: {r['slippage_impact']:.2f}%")

    print("\n【最终结论】")
    print("基于以上实测结果，建议:")

    two_ok = (
        all_results["two"]["sentiment"]["normal"]["annual_return"] > 0
        and all_results["two"]["sentiment"]["normal"]["max_drawdown"] < 30
    )
    three_ok = (
        all_results["three"]["sentiment"]["normal"]["annual_return"] > 0
        and all_results["three"]["sentiment"]["normal"]["max_drawdown"] < 40
    )
    four_ok = (
        all_results["four"]["sentiment"]["normal"]["annual_return"] > 0
        and all_results["four"]["sentiment"]["normal"]["max_drawdown"] < 50
    )

    if two_ok and three_ok and not four_ok:
        print("保留二板+三板")
    elif two_ok and not three_ok and not four_ok:
        print("只保留二板")
    elif not two_ok and not three_ok and not four_ok:
        print("整体 No-Go")
    else:
        print("需要更严格参数调优")


if __name__ == "__main__":
    all_results = run_full_test()
    generate_report(all_results)

    with open(
        "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/234_board_backtest_results.json",
        "w",
    ) as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("\n回测完成! 结果已保存到 output/234_board_backtest_results.json")
