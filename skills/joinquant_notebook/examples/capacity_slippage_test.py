from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

OUTPUT_FILE = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/capacity_slippage_results.json"
)

CAPACITIES = [5000000, 10000000, 30000000, 50000000]
CAPACITY_NAMES = ["500万", "1000万", "3000万", "5000万"]
SLIPPAGES = [0.002, 0.005, 0.010]
SLIPPAGE_NAMES = ["0.2%", "0.5%", "1.0%"]
COMMISSION_RATE = 0.0003
STAMP_DUTY = 0.001
MAX_VOLUME_RATIO = 0.10

START_DATE = "2024-01-01"
END_DATE = "2025-03-31"


def get_limit_up_stocks(date):
    prev_date = (pd.to_datetime(date) - timedelta(days=1)).strftime("%Y-%m-%d")
    trade_days = get_trade_days(prev_date, date)
    if len(trade_days) < 2:
        return []
    prev_date = trade_days[-2]

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "683"]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    if df.empty:
        return []

    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    return list(df["code"])


def get_open_pct(stock, date):
    try:
        df = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["open", "close"],
            count=2,
            panel=False,
        )
        if df.empty or len(df) < 2:
            return None
        prev_close = df["close"].iloc[-2]
        today_open = df["open"].iloc[-1]
        return (today_open - prev_close) / prev_close
    except:
        return None


def get_stock_volume(stock, date):
    try:
        df = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["volume", "money"],
            count=1,
            panel=False,
        )
        if df.empty:
            return 0, 0
        return df["volume"].iloc[-1], df["money"].iloc[-1]
    except:
        return 0, 0


def can_buy(stock, date, capital, slippage):
    open_pct = get_open_pct(stock, date)
    if open_pct is None:
        return False, 0, 0

    if not (-0.015 <= open_pct <= 0.015):
        return False, 0, 0

    volume, turnover = get_stock_volume(stock, date)
    if volume == 0 or turnover == 0:
        return False, 0, 0

    df = get_price(
        stock, end_date=date, frequency="daily", fields=["open"], count=1, panel=False
    )
    if df.empty:
        return False, 0, 0

    open_price = df["open"].iloc[-1]

    max_invest = turnover * MAX_VOLUME_RATIO

    actual_invest = min(capital, max_invest)

    if actual_invest < 100000:
        return False, 0, 0

    buy_price = open_price * (1 + slippage)
    max_shares = int(actual_invest / buy_price / 100) * 100

    return True, max_shares, buy_price


def simulate_trade(stock, buy_date, shares, buy_price, slippage, hold_days=1):
    try:
        sell_date_offset = hold_days + 1
        df = get_price(
            stock,
            end_date=buy_date,
            frequency="daily",
            fields=["open", "close", "high"],
            count=sell_date_offset + 5,
            panel=False,
        )

        if df.empty or len(df) < sell_date_offset:
            return None

        df = df.iloc[-sell_date_offset - 1 :]

        sell_date_idx = hold_days
        if sell_date_idx >= len(df):
            return None

        sell_price = df["high"].iloc[sell_date_idx]
        sell_price = sell_price * (1 - slippage)

        buy_value = shares * buy_price
        sell_value = shares * sell_price

        buy_commission = buy_value * COMMISSION_RATE
        sell_commission = sell_value * COMMISSION_RATE
        stamp = sell_value * STAMP_DUTY

        total_cost = buy_commission + sell_commission + stamp
        pnl = sell_value - buy_value - total_cost
        pnl_pct = pnl / buy_value

        return {
            "buy_date": buy_date,
            "shares": shares,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "pnl": pnl,
            "pnl_pct": pnl_pct,
            "turnover": buy_value,
        }
    except Exception as e:
        return None


def run_backtest(capacity, slippage):
    trade_days = get_trade_days(START_DATE, END_DATE)

    results = []
    equity_curve = [1.0]
    equity = 1.0

    for i, date in enumerate(trade_days[:-1]):
        next_date = trade_days[i + 1]

        limit_up_stocks = get_limit_up_stocks(date)

        signals = []
        for stock in limit_up_stocks[:50]:
            can, shares, price = can_buy(stock, next_date, capacity, slippage)
            if can and shares >= 100:
                signals.append((stock, shares, price))

        if signals:
            per_stock_capital = capacity / min(len(signals), 3)
            actual_signals = signals[:3]

            daily_pnl = 0
            for stock, max_shares, buy_price in actual_signals:
                shares = min(max_shares, int(per_stock_capital / buy_price / 100) * 100)
                if shares >= 100:
                    trade = simulate_trade(
                        stock, next_date, shares, buy_price, slippage
                    )
                    if trade:
                        daily_pnl += trade["pnl_pct"]
                        results.append(trade)

            if daily_pnl != 0:
                daily_avg = daily_pnl / len(actual_signals)
                equity = equity * (1 + daily_avg)
                equity_curve.append(equity)

    return {
        "trades": len(results),
        "final_equity": equity,
        "total_return": (equity - 1) * 100,
        "equity_curve": equity_curve,
        "trade_results": results,
    }


print("=" * 80)
print("首板低开策略 - 容量与滑点实测")
print("=" * 80)
print(f"测试期间: {START_DATE} ~ {END_DATE}")
print(f"资金规模: {CAPACITY_NAMES}")
print(f"滑点设置: {SLIPPAGE_NAMES}")
print(f"单票成交额占比上限: {MAX_VOLUME_RATIO * 100}%")
print("=" * 80)

all_results = {}

for cap_idx, capacity in enumerate(CAPACITIES):
    cap_name = CAPACITY_NAMES[cap_idx]
    all_results[cap_name] = {}

    for slip_idx, slippage in enumerate(SLIPPAGES):
        slip_name = SLIPPAGE_NAMES[slip_idx]
        key = f"{cap_name}_{slip_name}"

        print(f"\n测试: 资金={cap_name}, 滑点={slip_name}")

        result = run_backtest(capacity, slippage)
        all_results[cap_name][slip_name] = {
            "trades": result["trades"],
            "total_return": result["total_return"],
            "final_equity": result["final_equity"],
            "equity_curve_length": len(result["equity_curve"]),
        }

        print(f"  交易次数: {result['trades']}")
        print(f"  总收益率: {result['total_return']:.2f}%")
        print(f"  最终权益: {result['final_equity']:.4f}")


print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

summary_table = []
for cap_name in CAPACITY_NAMES:
    row = {"资金规模": cap_name}
    for slip_name in SLIPPAGE_NAMES:
        if slip_name in all_results.get(cap_name, {}):
            ret = all_results[cap_name][slip_name]["total_return"]
            trades = all_results[cap_name][slip_name]["trades"]
            row[f"滑点{slip_name}"] = f"{ret:.2f}% ({trades}笔)"
        else:
            row[f"滑点{slip_name}"] = "N/A"
    summary_table.append(row)

print("\n容量-收益表:")
print("-" * 100)
print(f"{'资金规模':<12} {'滑点0.2%':<20} {'滑点0.5%':<20} {'滑点1.0%':<20}")
print("-" * 100)
for row in summary_table:
    print(
        f"{row['资金规模']:<12} {row['滑点0.2%']:<20} {row['滑点0.5%']:<20} {row['滑点1.0%']:<20}"
    )

with open(OUTPUT_FILE, "w") as f:
    json.dump(
        {
            "all_results": all_results,
            "summary_table": summary_table,
            "params": {
                "capacities": CAPACITY_NAMES,
                "slippages": SLIPPAGE_NAMES,
                "start_date": START_DATE,
                "end_date": END_DATE,
                "max_volume_ratio": MAX_VOLUME_RATIO,
                "commission_rate": COMMISSION_RATE,
                "stamp_duty": STAMP_DUTY,
            },
        },
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"\n结果已保存到: {OUTPUT_FILE}")
print("=" * 80)
