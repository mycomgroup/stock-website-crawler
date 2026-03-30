#!/usr/bin/env python3
"""
任务02：情绪开关最小可用版定型
测试3套指标×2种用法=6种组合
接入任务01的首板低开主版本信号
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务02：情绪开关最小可用版定型")
print("测试6种组合：3套指标×2种用法")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2025-03-28"
OOS_START = "2024-01-01"
INITIAL_CAPITAL = 1000000
MAX_POSITION_SIZE = 0.05


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
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def get_dt_stocks(date):
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
        fields=["close", "low_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    dt_df = df[df["close"] == df["low_limit"]]
    return list(dt_df["code"])


def calc_lianban_count(stock, date, max_days=10):
    df = get_price(
        stock,
        end_date=date,
        count=max_days,
        fields=["close", "high_limit"],
        panel=False,
    )
    if len(df) < max_days:
        return 0

    count = 0
    for i in range(len(df) - 1, -1, -1):
        if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
            count += 1
        else:
            break
    return count


def calc_market_sentiment(date):
    zt_list = get_zt_stocks(date)
    dt_list = get_dt_stocks(date)

    max_lianban = 0
    if len(zt_list) > 0:
        for stock in zt_list[:50]:
            try:
                lb = calc_lianban_count(stock, date)
                max_lianban = max(max_lianban, lb)
            except:
                continue

    zt_dt_ratio = len(zt_list) / max(len(dt_list), 1)

    return {
        "zt_count": len(zt_list),
        "dt_count": len(dt_list),
        "zt_dt_ratio": zt_dt_ratio,
        "max_lianban": max_lianban,
    }


def select_first_board_low_open(date, prev_date):
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []

    selected = []
    for stock in prev_zt[:50]:
        try:
            prev_price = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            today_price = get_price(
                stock,
                end_date=date,
                count=1,
                fields=["open", "close", "high_limit", "low_limit"],
                panel=False,
            )

            if len(prev_price) == 0 or len(today_price) == 0:
                continue

            prev_close = prev_price.iloc[0]["close"]
            today_open = today_price.iloc[0]["open"]

            open_ratio = (today_open / prev_close - 1) * 100

            if 0.5 <= open_ratio <= 1.5:
                if today_open < today_price.iloc[0]["high_limit"]:
                    q = query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code == stock
                    )
                    val_df = get_fundamentals(q, date=date)
                    if len(val_df) > 0:
                        market_cap = val_df.iloc[0]["circulating_market_cap"]
                        if 50 <= market_cap <= 150:
                            selected.append(stock)
        except:
            continue

    return selected


def calc_position_size_hard_switch1(sentiment):
    if sentiment["zt_count"] >= 30:
        return 1.0
    return 0.0


def calc_position_size_hard_switch2(sentiment):
    if sentiment["max_lianban"] >= 2 and sentiment["zt_count"] >= 30:
        return 1.0
    return 0.0


def calc_position_size_hard_switch3(sentiment):
    if (
        sentiment["max_lianban"] >= 2
        and sentiment["zt_count"] >= 15
        and sentiment["zt_dt_ratio"] >= 1.5
    ):
        return 1.0
    return 0.0


def calc_position_size_position_regulator1(sentiment):
    if sentiment["zt_count"] >= 50:
        return 1.0
    elif sentiment["zt_count"] >= 30:
        return 0.5
    return 0.0


def calc_position_size_position_regulator2(sentiment):
    if sentiment["max_lianban"] >= 3 and sentiment["zt_count"] >= 50:
        return 1.0
    elif sentiment["max_lianban"] >= 2 and sentiment["zt_count"] >= 30:
        return 0.5
    return 0.0


def calc_position_size_position_regulator3(sentiment):
    if (
        sentiment["max_lianban"] >= 3
        and sentiment["zt_count"] >= 30
        and sentiment["zt_dt_ratio"] >= 2
    ):
        return 1.0
    elif (
        sentiment["max_lianban"] >= 2
        and sentiment["zt_count"] >= 15
        and sentiment["zt_dt_ratio"] >= 1.5
    ):
        return 0.5
    return 0.0


def backtest_strategy(date_list, position_func, strategy_name):
    capital = INITIAL_CAPITAL
    max_capital = capital
    min_capital = capital
    results = []
    total_trades = 0
    win_trades = 0
    total_profit = 0
    total_loss = 0
    max_drawdown = 0
    daily_returns = []

    for i in range(1, len(date_list)):
        date = date_list[i]
        prev_date = date_list[i - 1]
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else date
        prev_date_str = (
            prev_date.strftime("%Y-%m-%d")
            if hasattr(prev_date, "strftime")
            else prev_date
        )

        try:
            sentiment = calc_market_sentiment(prev_date_str)
            position_ratio = position_func(sentiment)

            if position_ratio == 0:
                results.append(
                    {
                        "date": date_str,
                        "capital": capital,
                        "return": 0,
                        "sentiment": sentiment,
                        "position": position_ratio,
                        "trades": 0,
                    }
                )
                continue

            selected = select_first_board_low_open(date_str, prev_date_str)

            if len(selected) == 0:
                results.append(
                    {
                        "date": date_str,
                        "capital": capital,
                        "return": 0,
                        "sentiment": sentiment,
                        "position": position_ratio,
                        "trades": 0,
                    }
                )
                continue

            trade_count = min(len(selected), int(20 / MAX_POSITION_SIZE))
            position_size_per_stock = (
                capital * position_ratio * MAX_POSITION_SIZE
            ) / max(len(selected), 1)

            trade_days = get_trade_days(
                date_str,
                (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=10)).strftime(
                    "%Y-%m-%d"
                ),
            )
            if len(trade_days) < 2:
                continue
            next_date = trade_days[1] if trade_days[0] == date_str else trade_days[0]

            day_returns = []
            for stock in selected[:5]:
                try:
                    buy_price = get_price(
                        stock, end_date=date_str, count=1, fields=["open"], panel=False
                    )
                    sell_price = get_price(
                        stock, end_date=next_date, count=1, fields=["high"], panel=False
                    )

                    if len(buy_price) > 0 and len(sell_price) > 0:
                        buy_open = buy_price.iloc[0]["open"]
                        sell_high = sell_price.iloc[0]["high"]
                        ret = sell_high / buy_open - 1
                        day_returns.append(ret)

                        trade_value = position_size_per_stock
                        profit = trade_value * ret

                        capital += profit
                        total_trades += 1

                        if ret > 0:
                            win_trades += 1
                            total_profit += abs(profit)
                        else:
                            total_loss += abs(profit)
                except:
                    continue

            if len(day_returns) > 0:
                avg_ret = np.mean(day_returns)
                daily_return = avg_ret * position_ratio * 0.2
                daily_returns.append(daily_return)

                max_capital = max(max_capital, capital)
                min_capital = min(min_capital, capital)
                drawdown = (max_capital - capital) / max_capital
                max_drawdown = max(max_drawdown, drawdown)

                results.append(
                    {
                        "date": date_str,
                        "capital": capital,
                        "return": daily_return,
                        "avg_stock_return": avg_ret,
                        "sentiment": sentiment,
                        "position": position_ratio,
                        "trades": len(day_returns),
                    }
                )
        except Exception as e:
            continue

    if len(results) == 0:
        return None

    df = pd.DataFrame(results)

    total_return = (capital - INITIAL_CAPITAL) / INITIAL_CAPITAL
    win_rate = win_trades / total_trades if total_trades > 0 else 0
    profit_loss_ratio = total_profit / total_loss if total_loss > 0 else 0

    years = (
        datetime.strptime(END_DATE, "%Y-%m-%d")
        - datetime.strptime(START_DATE, "%Y-%m-%d")
    ).days / 365
    annual_return = total_return / years if years > 0 else 0

    if len(daily_returns) > 0:
        volatility = np.std(daily_returns) * np.sqrt(250)
        sharpe = annual_return / volatility if volatility > 0 else 0
    else:
        sharpe = 0

    calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0

    oos_start_idx = df[df["date"] >= OOS_START].index
    if len(oos_start_idx) > 0:
        oos_df = df.loc[oos_start_idx[0] :]
        oos_return = (
            oos_df.iloc[-1]["capital"] - oos_df.iloc[0]["capital"]
        ) / oos_df.iloc[0]["capital"]
        oos_years = (
            datetime.strptime(END_DATE, "%Y-%m-%d")
            - datetime.strptime(OOS_START, "%Y-%m-%d")
        ).days / 365
        oos_annual_return = oos_return / oos_years if oos_years > 0 else 0
    else:
        oos_annual_return = 0

    summary = {
        "strategy_name": strategy_name,
        "total_return": total_return * 100,
        "annual_return": annual_return * 100,
        "max_drawdown": max_drawdown * 100,
        "calmar_ratio": calmar_ratio,
        "sharpe_ratio": sharpe,
        "total_trades": total_trades,
        "win_rate": win_rate * 100,
        "profit_loss_ratio": profit_loss_ratio,
        "oos_annual_return": oos_annual_return * 100,
        "sample_period": f"{START_DATE} ~ {END_DATE}",
        "oos_period": f"{OOS_START} ~ {END_DATE}",
    }

    return summary


all_trade_days = get_trade_days(START_DATE, END_DATE)
sample_days = all_trade_days[::5]
print(f"采样交易日数: {len(sample_days)}")

strategies = [
    ("涨停家数-硬开关", calc_position_size_hard_switch1),
    ("涨停家数-仓位调节", calc_position_size_position_regulator1),
    ("最高连板+涨停-硬开关", calc_position_size_hard_switch2),
    ("最高连板+涨停-仓位调节", calc_position_size_position_regulator2),
    ("三指标组合-硬开关", calc_position_size_hard_switch3),
    ("三指标组合-仓位调节", calc_position_size_position_regulator3),
]

print("\n开始测试6种组合...")
all_results = []

for name, func in strategies:
    print(f"\n测试: {name}")
    result = backtest_strategy(sample_days, func, name)
    if result:
        all_results.append(result)
        print(f"  年化收益: {result['annual_return']:.2f}%")
        print(f"  最大回撤: {result['max_drawdown']:.2f}%")
        print(f"  卡玛比率: {result['calmar_ratio']:.2f}")
        print(f"  交易次数: {result['total_trades']}")
        print(f"  胜率: {result['win_rate']:.2f}%")

print("\n" + "=" * 80)
print("对照表汇总")
print("=" * 80)

comparison_df = pd.DataFrame(all_results)
print(
    comparison_df[
        [
            "strategy_name",
            "total_trades",
            "win_rate",
            "profit_loss_ratio",
            "annual_return",
            "max_drawdown",
            "calmar_ratio",
        ]
    ].to_string()
)

print("\n" + "=" * 80)
print("样本外结果 (2024-01-01后)")
print("=" * 80)

print(comparison_df[["strategy_name", "oos_annual_return"]].to_string())

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/task02_sentiment_switch_mvp_results.json"
with open(result_file, "w") as f:
    json.dump(all_results, f, indent=2)
print(f"\n结果已保存至: {result_file}")

print("\n" + "=" * 80)
print("最终结论")
print("=" * 80)

best_calmar = max(all_results, key=lambda x: x["calmar_ratio"])
print(
    f"卡玛比率最高: {best_calmar['strategy_name']} (Calmar={best_calmar['calmar_ratio']:.2f})"
)

best_return = max(all_results, key=lambda x: x["annual_return"])
print(
    f"年化收益最高: {best_return['strategy_name']} (Return={best_return['annual_return']:.2f}%)"
)

best_drawdown = min(all_results, key=lambda x: x["max_drawdown"])
print(
    f"回撤最小: {best_drawdown['strategy_name']} (DD={best_drawdown['max_drawdown']:.2f}%)"
)

print("\n研究完成!")
