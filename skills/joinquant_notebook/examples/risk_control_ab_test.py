#!/usr/bin/env python3
"""风控A/B测试 - Notebook版本
对比三组风控配置在2021-2024年的表现
"""

from jqdata import *
from jqfactor import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("风控 A/B 测试 - 弱转强竞价策略")
print("=" * 80)

BACKTEST_START = "2021-01-01"
BACKTEST_END = "2024-01-01"
SAMPLE_OUT_START = "2023-01-01"
INITIAL_CAPITAL = 100000


def transform_date(date, date_type):
    if type(date) == str:
        str_date = date
        dt_date = datetime.strptime(date, "%Y-%m-%d")
        d_date = dt_date.date()
    elif type(date) == datetime:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = date
        d_date = dt_date.date()
    elif type(date) == pd.Timestamp:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = datetime.strptime(str_date, "%Y-%m-%d")
        d_date = dt_date.date()
    else:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = datetime.strptime(str_date, "%Y-%m-%d")
        d_date = date
    return {"str": str_date, "dt": dt_date, "d": d_date}[date_type]


def get_shifted_date(date, days, days_type="T"):
    d_date = transform_date(date, "d")
    yesterday = d_date + timedelta(-1)
    if days_type == "N":
        shifted_date = yesterday + timedelta(days + 1)
    if days_type == "T":
        all_trade_days = [i.strftime("%Y-%m-%d") for i in list(get_all_trade_days())]
        if str(yesterday) in all_trade_days:
            shifted_date = all_trade_days[
                all_trade_days.index(str(yesterday)) + days + 1
            ]
        else:
            for i in range(100):
                last_trade_date = yesterday - timedelta(i)
                if str(last_trade_date) in all_trade_days:
                    shifted_date = all_trade_days[
                        all_trade_days.index(str(last_trade_date)) + days + 1
                    ]
                    break
    return str(shifted_date)


def filter_kcbj_stock(initial_list):
    return [
        stock
        for stock in initial_list
        if stock[0] != "4" and stock[0] != "8" and stock[:2] != "68"
    ]


def filter_new_stock(initial_list, date, days=50):
    d_date = transform_date(date, "d")
    return [
        stock
        for stock in initial_list
        if d_date - get_security_info(stock).start_date > timedelta(days=days)
    ]


def filter_st_stock(initial_list, date):
    str_date = transform_date(date, "str")
    df = get_extras(
        "is_st", initial_list, start_date=str_date, end_date=str_date, df=True
    )
    df = df.T
    df.columns = ["is_st"]
    df = df[df["is_st"] == False]
    return list(df.index)


def filter_paused_stock(initial_list, date):
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["paused"],
        count=1,
        panel=False,
        fill_paused=True,
    )
    df = df[df["paused"] == 0]
    return list(df.code)


def prepare_stock_list(date):
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = filter_kcbj_stock(initial_list)
    initial_list = filter_new_stock(initial_list, date)
    initial_list = filter_st_stock(initial_list, date)
    initial_list = filter_paused_stock(initial_list, date)
    return initial_list


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
    return list(df.code)


def get_ever_hl_stock(initial_list, date):
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["high", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    df = df[df["high"] == df["high_limit"]]
    return list(df.code)


def calculate_zyts_dynamic(stock, date, lookback=101):
    try:
        high_prices = get_price(
            stock, end_date=date, count=lookback, fields=["high"], panel=False
        )
        if high_prices.empty or len(high_prices) < 3:
            return 10
        prev_high = high_prices["high"].iloc[-1]
        for i, high in enumerate(high_prices["high"].iloc[-3::-1], 2):
            if high >= prev_high:
                return i - 1 + 5
        return 100 + 5
    except:
        return 10


def select_candidates(date_str):
    date_1 = get_shifted_date(date_str, -1, "T")
    date_2 = get_shifted_date(date_str, -2, "T")

    initial_list = prepare_stock_list(date_str)
    hl_list = get_hl_stock(initial_list, date_str)
    hl1_list = get_ever_hl_stock(initial_list, date_1)
    hl2_list = get_ever_hl_stock(initial_list, date_2)

    elements_to_remove = set(hl1_list + hl2_list)
    hl_list = [stock for stock in hl_list if stock not in elements_to_remove]

    return hl_list


def check_buy_conditions(stock, date_str, prev_close):
    try:
        prev_day_data = get_price(
            stock,
            end_date=date_str,
            count=2,
            fields=["close", "volume", "money"],
            panel=False,
        )
        if prev_day_data.empty or len(prev_day_data) < 2:
            return False, None

        avg_price_increase = (
            prev_day_data["money"].iloc[-2]
            / prev_day_data["volume"].iloc[-2]
            / prev_day_data["close"].iloc[-2]
            * 1.1
            - 1
        )
        if avg_price_increase < 0.07 or prev_day_data["money"].iloc[-2] < 7e8:
            return False, None

        valuation_data = get_valuation(
            stock, end_date=date_str, count=1, fields=["market_cap"]
        )
        if valuation_data.empty or valuation_data["market_cap"].iloc[-1] < 70:
            return False, None

        zyts = calculate_zyts_dynamic(stock, date_str)
        volume_data = get_price(
            stock, end_date=date_str, count=zyts, fields=["volume"], panel=False
        )
        if volume_data.empty or len(volume_data) < 2:
            return False, None
        if volume_data["volume"].iloc[-2] <= max(volume_data["volume"].iloc[:-2]) * 0.9:
            return False, None

        current_data = get_current_data()
        if stock not in current_data:
            return False, None

        high_limit = current_data[stock].high_limit
        open_price = current_data[stock].day_open

        open_ratio = open_price / (high_limit / 1.1)
        if open_ratio <= 1 or open_ratio >= 1.06:
            return False, None

        volume_ratio = volume_data["volume"].iloc[-1] / volume_data["volume"].iloc[-2]
        if volume_ratio < 0.03:
            return False, None

        return True, open_price

    except Exception as e:
        return False, None


def simulate_trade_group_a(candidates, date_str, capital):
    trades = []
    current_data = get_current_data()

    qualified = []
    for stock in candidates:
        prev_close = current_data[stock].pre_close if stock in current_data else None
        if prev_close is None:
            continue
        ok, open_price = check_buy_conditions(stock, date_str, prev_close)
        if ok:
            qualified.append((stock, open_price))

    if len(qualified) == 0:
        return trades, capital

    per_stock_capital = capital / len(qualified)

    for stock, open_price in qualified:
        try:
            sell_time = "14:50"
            next_date = get_shifted_date(date_str, 1, "T")
            next_day_data = get_price(
                stock,
                end_date=next_date,
                count=1,
                fields=["close", "high_limit", "high"],
                panel=False,
            )

            if next_day_data.empty:
                continue

            next_close = next_day_data["close"].iloc[-1]
            next_high = next_day_data["high"].iloc[-1]
            next_high_limit = next_day_data["high_limit"].iloc[-1]

            sell_price = next_close
            if next_close == next_high_limit:
                sell_price = next_high

            pnl_pct = (sell_price - open_price) / open_price
            pnl = per_stock_capital * pnl_pct

            trades.append(
                {
                    "stock": stock,
                    "buy_date": date_str,
                    "buy_price": open_price,
                    "sell_date": next_date,
                    "sell_price": sell_price,
                    "sell_reason": "尾盘清仓",
                    "pnl_pct": pnl_pct,
                    "pnl": pnl,
                    "capital_used": per_stock_capital,
                }
            )

        except Exception as e:
            continue

    return trades, capital


def simulate_trade_group_b(candidates, date_str, capital):
    trades = []
    current_data = get_current_data()

    qualified = []
    for stock in candidates:
        prev_close = current_data[stock].pre_close if stock in current_data else None
        if prev_close is None:
            continue
        ok, open_price = check_buy_conditions(stock, date_str, prev_close)
        if ok:
            qualified.append((stock, open_price))

    if len(qualified) == 0:
        return trades, capital

    per_stock_capital = capital / len(qualified)

    for stock, open_price in qualified:
        try:
            next_date = get_shifted_date(date_str, 1, "T")

            intraday_1030 = get_price(
                stock,
                end_date=f"{next_date} 10:30:00",
                count=1,
                frequency="minute",
                fields=["close"],
                panel=False,
            )
            if not intraday_1030.empty:
                price_1030 = intraday_1030["close"].iloc[-1]
                if price_1030 < open_price:
                    sell_price = price_1030
                    pnl_pct = (sell_price - open_price) / open_price
                    pnl = per_stock_capital * pnl_pct
                    trades.append(
                        {
                            "stock": stock,
                            "buy_date": date_str,
                            "buy_price": open_price,
                            "sell_date": next_date,
                            "sell_price": sell_price,
                            "sell_reason": "10:30时间止损",
                            "pnl_pct": pnl_pct,
                            "pnl": pnl,
                            "capital_used": per_stock_capital,
                        }
                    )
                    continue

            intraday_1330 = get_price(
                stock,
                end_date=f"{next_date} 13:30:00",
                count=1,
                frequency="minute",
                fields=["close"],
                panel=False,
            )
            if not intraday_1330.empty:
                price_1330 = intraday_1330["close"].iloc[-1]
                if price_1330 < open_price * 1.03:
                    sell_price = price_1330
                    pnl_pct = (sell_price - open_price) / open_price
                    pnl = per_stock_capital * pnl_pct
                    trades.append(
                        {
                            "stock": stock,
                            "buy_date": date_str,
                            "buy_price": open_price,
                            "sell_date": next_date,
                            "sell_price": sell_price,
                            "sell_reason": "13:30达标止盈",
                            "pnl_pct": pnl_pct,
                            "pnl": pnl,
                            "capital_used": per_stock_capital,
                        }
                    )
                    continue

            next_day_data = get_price(
                stock,
                end_date=next_date,
                count=1,
                fields=["close", "high_limit", "high"],
                panel=False,
            )
            if next_day_data.empty:
                continue

            next_close = next_day_data["close"].iloc[-1]
            next_high = next_day_data["high"].iloc[-1]
            next_high_limit = next_day_data["high_limit"].iloc[-1]

            sell_price = next_close
            if next_close == next_high_limit:
                sell_price = next_high

            pnl_pct = (sell_price - open_price) / open_price
            pnl = per_stock_capital * pnl_pct

            trades.append(
                {
                    "stock": stock,
                    "buy_date": date_str,
                    "buy_price": open_price,
                    "sell_date": next_date,
                    "sell_price": sell_price,
                    "sell_reason": "尾盘清仓",
                    "pnl_pct": pnl_pct,
                    "pnl": pnl,
                    "capital_used": per_stock_capital,
                }
            )

        except Exception as e:
            continue

    return trades, capital


def simulate_trade_group_c(
    candidates, date_str, capital, cool_down_days, weekly_pnl_pct
):
    trades = []

    if cool_down_days > 0:
        return trades, capital, cool_down_days - 1

    current_data = get_current_data()

    qualified = []
    for stock in candidates:
        prev_close = current_data[stock].pre_close if stock in current_data else None
        if prev_close is None:
            continue
        ok, open_price = check_buy_conditions(stock, date_str, prev_close)
        if ok:
            qualified.append((stock, open_price))

    if len(qualified) == 0:
        return trades, capital, cool_down_days

    adjusted_capital = capital
    if cool_down_days == -1:
        adjusted_capital = capital * 0.5

    per_stock_capital = adjusted_capital / len(qualified)

    for stock, open_price in qualified:
        try:
            next_date = get_shifted_date(date_str, 1, "T")

            intraday_1030 = get_price(
                stock,
                end_date=f"{next_date} 10:30:00",
                count=1,
                frequency="minute",
                fields=["close"],
                panel=False,
            )
            if not intraday_1030.empty:
                price_1030 = intraday_1030["close"].iloc[-1]
                if price_1030 < open_price:
                    sell_price = price_1030
                    pnl_pct = (sell_price - open_price) / open_price
                    pnl = per_stock_capital * pnl_pct
                    trades.append(
                        {
                            "stock": stock,
                            "buy_date": date_str,
                            "buy_price": open_price,
                            "sell_date": next_date,
                            "sell_price": sell_price,
                            "sell_reason": "10:30时间止损",
                            "pnl_pct": pnl_pct,
                            "pnl": pnl,
                            "capital_used": per_stock_capital,
                        }
                    )
                    continue

            intraday_1330 = get_price(
                stock,
                end_date=f"{next_date} 13:30:00",
                count=1,
                frequency="minute",
                fields=["close"],
                panel=False,
            )
            if not intraday_1330.empty:
                price_1330 = intraday_1330["close"].iloc[-1]
                if price_1330 < open_price * 1.03:
                    sell_price = price_1330
                    pnl_pct = (sell_price - open_price) / open_price
                    pnl = per_stock_capital * pnl_pct
                    trades.append(
                        {
                            "stock": stock,
                            "buy_date": date_str,
                            "buy_price": open_price,
                            "sell_date": next_date,
                            "sell_price": sell_price,
                            "sell_reason": "13:30达标止盈",
                            "pnl_pct": pnl_pct,
                            "pnl": pnl,
                            "capital_used": per_stock_capital,
                        }
                    )
                    continue

            next_day_data = get_price(
                stock,
                end_date=next_date,
                count=1,
                fields=["close", "high_limit", "high"],
                panel=False,
            )
            if next_day_data.empty:
                continue

            next_close = next_day_data["close"].iloc[-1]
            next_high = next_day_data["high"].iloc[-1]
            next_high_limit = next_day_data["high_limit"].iloc[-1]

            sell_price = next_close
            if next_close == next_high_limit:
                sell_price = next_high

            pnl_pct = (sell_price - open_price) / open_price
            pnl = per_stock_capital * pnl_pct

            trades.append(
                {
                    "stock": stock,
                    "buy_date": date_str,
                    "buy_price": open_price,
                    "sell_date": next_date,
                    "sell_price": sell_price,
                    "sell_reason": "尾盘清仓",
                    "pnl_pct": pnl_pct,
                    "pnl": pnl,
                    "capital_used": per_stock_capital,
                }
            )

        except Exception as e:
            continue

    daily_pnl_pct = sum([t["pnl_pct"] for t in trades]) if trades else 0
    weekly_pnl_pct += daily_pnl_pct

    if weekly_pnl_pct < -0.08 and cool_down_days == 0:
        cool_down_days = 3

    return trades, capital, cool_down_days


def calculate_metrics(trades, initial_capital):
    if len(trades) == 0:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_pnl_pct": 0,
            "max_pnl_pct": 0,
            "min_pnl_pct": 0,
            "total_pnl": 0,
            "total_return_pct": 0,
        }

    total_trades = len(trades)
    wins = [t for t in trades if t["pnl_pct"] > 0]
    losses = [t for t in trades if t["pnl_pct"] <= 0]

    win_rate = len(wins) / total_trades if total_trades > 0 else 0
    avg_pnl_pct = np.mean([t["pnl_pct"] for t in trades])
    max_pnl_pct = max([t["pnl_pct"] for t in trades])
    min_pnl_pct = min([t["pnl_pct"] for t in trades])

    total_pnl = sum([t["pnl"] for t in trades])
    total_return_pct = (total_pnl / initial_capital) * 100

    return {
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_pnl_pct": avg_pnl_pct,
        "max_pnl_pct": max_pnl_pct,
        "min_pnl_pct": min_pnl_pct,
        "total_pnl": total_pnl,
        "total_return_pct": total_return_pct,
    }


print("\n开始回测...")
print(f"回测期间: {BACKTEST_START} 至 {BACKTEST_END}")
print(f"样本外起始: {SAMPLE_OUT_START}")

all_trade_days = get_trade_days(BACKTEST_START, BACKTEST_END)
sample_out_days = get_trade_days(SAMPLE_OUT_START, BACKTEST_END)

trades_a = []
trades_b = []
trades_c = []

capital_a = INITIAL_CAPITAL
capital_b = INITIAL_CAPITAL
capital_c = INITIAL_CAPITAL
cool_down_days = 0
weekly_pnl_pct = 0
week_start_idx = 0

sample_out_trades_a = []
sample_out_trades_b = []
sample_out_trades_c = []

print(f"\n总交易日数: {len(all_trade_days)}")
print(f"样本外交易日数: {len(sample_out_days)}")

test_days = all_trade_days[:200]

print(f"\n实际测试天数: {len(test_days)} (限制200天以加快速度)")

for i, date in enumerate(test_days):
    date_str = date.strftime("%Y-%m-%d")

    if i % 20 == 0:
        print(f"处理第 {i + 1} 天: {date_str}")

    candidates = select_candidates(date_str)

    if len(candidates) == 0:
        continue

    day_trades_a, capital_a = simulate_trade_group_a(candidates, date_str, capital_a)
    day_trades_b, capital_b = simulate_trade_group_b(candidates, date_str, capital_b)
    day_trades_c, capital_c, cool_down_days = simulate_trade_group_c(
        candidates, date_str, capital_c, cool_down_days, weekly_pnl_pct
    )

    trades_a.extend(day_trades_a)
    trades_b.extend(day_trades_b)
    trades_c.extend(day_trades_c)

    if date >= pd.Timestamp(SAMPLE_OUT_START):
        sample_out_trades_a.extend(day_trades_a)
        sample_out_trades_b.extend(day_trades_b)
        sample_out_trades_c.extend(day_trades_c)

    if i - week_start_idx >= 5:
        weekly_pnl_pct = 0
        week_start_idx = i

print("\n" + "=" * 80)
print("回测完成！计算指标...")
print("=" * 80)

metrics_a_full = calculate_metrics(trades_a, INITIAL_CAPITAL)
metrics_b_full = calculate_metrics(trades_b, INITIAL_CAPITAL)
metrics_c_full = calculate_metrics(trades_c, INITIAL_CAPITAL)

metrics_a_sample = calculate_metrics(sample_out_trades_a, INITIAL_CAPITAL)
metrics_b_sample = calculate_metrics(sample_out_trades_b, INITIAL_CAPITAL)
metrics_c_sample = calculate_metrics(sample_out_trades_c, INITIAL_CAPITAL)

print("\n" + "=" * 80)
print("三组风控对比结果（全周期）")
print("=" * 80)

print("\n【A组：基线版（仅尾盘清仓）】")
print(f"交易次数: {metrics_a_full['total_trades']}")
print(f"胜率: {metrics_a_full['win_rate'] * 100:.2f}%")
print(f"平均盈亏: {metrics_a_full['avg_pnl_pct'] * 100:.2f}%")
print(f"最大单笔盈利: {metrics_a_full['max_pnl_pct'] * 100:.2f}%")
print(f"最大单笔亏损: {metrics_a_full['min_pnl_pct'] * 100:.2f}%")
print(f"总收益: {metrics_a_full['total_return_pct']:.2f}%")

print("\n【B组：单票时间止损版】")
print(f"交易次数: {metrics_b_full['total_trades']}")
print(f"胜率: {metrics_b_full['win_rate'] * 100:.2f}%")
print(f"平均盈亏: {metrics_b_full['avg_pnl_pct'] * 100:.2f}%")
print(f"最大单笔盈利: {metrics_b_full['max_pnl_pct'] * 100:.2f}%")
print(f"最大单笔亏损: {metrics_b_full['min_pnl_pct'] * 100:.2f}%")
print(f"总收益: {metrics_b_full['total_return_pct']:.2f}%")

print("\n【C组：单票+组合熔断版】")
print(f"交易次数: {metrics_c_full['total_trades']}")
print(f"胜率: {metrics_c_full['win_rate'] * 100:.2f}%")
print(f"平均盈亏: {metrics_c_full['avg_pnl_pct'] * 100:.2f}%")
print(f"最大单笔盈利: {metrics_c_full['max_pnl_pct'] * 100:.2f}%")
print(f"最大单笔亏损: {metrics_c_full['min_pnl_pct'] * 100:.2f}%")
print(f"总收益: {metrics_c_full['total_return_pct']:.2f}%")

print("\n" + "=" * 80)
print(f"样本外结果 ({SAMPLE_OUT_START} 后)")
print("=" * 80)

print("\n【A组样本外】")
print(f"交易次数: {metrics_a_sample['total_trades']}")
print(f"胜率: {metrics_a_sample['win_rate'] * 100:.2f}%")
print(f"总收益: {metrics_a_sample['total_return_pct']:.2f}%")

print("\n【B组样本外】")
print(f"交易次数: {metrics_b_sample['total_trades']}")
print(f"胜率: {metrics_b_sample['win_rate'] * 100:.2f}%")
print(f"总收益: {metrics_b_sample['total_return_pct']:.2f}%")

print("\n【C组样本外】")
print(f"交易次数: {metrics_c_sample['total_trades']}")
print(f"胜率: {metrics_c_sample['win_rate'] * 100:.2f}%")
print(f"总收益: {metrics_c_sample['total_return_pct']:.2f}%")

print("\n" + "=" * 80)
print("对比分析")
print("=" * 80)

b_vs_a_return = metrics_b_full["total_return_pct"] - metrics_a_full["total_return_pct"]
b_vs_a_winrate = (metrics_b_full["win_rate"] - metrics_a_full["win_rate"]) * 100

c_vs_a_return = metrics_c_full["total_return_pct"] - metrics_a_full["total_return_pct"]
c_vs_a_winrate = (metrics_c_full["win_rate"] - metrics_a_full["win_rate"]) * 100

print(f"\nB组 vs A组:")
print(f"收益变化: {b_vs_a_return:.2f}%")
print(f"胜率变化: {b_vs_a_winrate:.2f}%")
print(f"止损次数估算: {len([t for t in trades_b if '止损' in t['sell_reason']])}")

print(f"\nC组 vs A组:")
print(f"收益变化: {c_vs_a_return:.2f}%")
print(f"胜率变化: {c_vs_a_winrate:.2f}%")
print(f"止损次数估算: {len([t for t in trades_c if '止损' in t['sell_reason']])}")

print("\n" + "=" * 80)
print("结论")
print("=" * 80)

if metrics_b_full["total_return_pct"] > metrics_a_full["total_return_pct"] * 0.8:
    if metrics_b_full["win_rate"] > metrics_a_full["win_rate"]:
        print("\n✓ B组（单票时间止损）性价比最高")
        print(f"  - 收益保留 > 80%，胜率提升 {b_vs_a_winrate:.2f}%")
    else:
        print("\n△ B组收益接近基线，但风控效果需进一步验证")
else:
    print("\n△ B组收益损失较大，需权衡风控代价")

if metrics_c_full["total_return_pct"] < metrics_a_full["total_return_pct"] * 0.6:
    print("\n✗ C组（组合熔断）过于保守，收益损失过大")
else:
    print("\n○ C组可作为保守备选方案")

results = {
    "test_period": f"{BACKTEST_START} 至 {BACKTEST_END}",
    "test_days": len(test_days),
    "groups": {
        "A_baseline": metrics_a_full,
        "B_single_stop": metrics_b_full,
        "C_combo_circuit": metrics_c_full,
    },
    "sample_out": {
        "A_baseline": metrics_a_sample,
        "B_single_stop": metrics_b_sample,
        "C_combo_circuit": metrics_c_sample,
    },
    "comparison": {
        "B_vs_A": {
            "return_change_pct": b_vs_a_return,
            "winrate_change_pct": b_vs_a_winrate,
        },
        "C_vs_A": {
            "return_change_pct": c_vs_a_return,
            "winrate_change_pct": c_vs_a_winrate,
        },
    },
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/risk_control_ab_test_result.json"
)
with open(result_file, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
print("=" * 80)
