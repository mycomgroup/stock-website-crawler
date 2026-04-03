#!/usr/bin/env python3
"""弱转强+止损 - 2024年"""

import pandas as pd
from jqdata import *

print("=" * 60)
print("弱转强+止损策略回测")
print("=" * 60)

INITIAL_CAPITAL = 100000
START = "2024-01-01"
END = "2024-03-31"

trade_days = get_trade_days(start_date=START, end_date=END)
print(f"\n交易日: {len(trade_days)}天")

capital = INITIAL_CAPITAL
positions = {}
trades = []
STOP_LOSS = -0.03  # 止损线 -3%

for i in range(1, len(trade_days) - 1):
    current_date = trade_days[i]
    current_str = current_date.strftime("%Y-%m-%d")
    prev_date = trade_days[i - 1]
    prev_str = prev_date.strftime("%Y-%m-%d")

    try:
        all_stocks = get_all_securities("stock", prev_str).index.tolist()
        stocks = [
            s for s in all_stocks if s[0] not in ["3", "4", "8"] and s[:2] != "68"
        ]

        prices = get_price(
            stocks,
            end_date=prev_str,
            frequency="daily",
            fields=["close", "high_limit", "money"],
            count=1,
            panel=False,
        )
        if prices.empty:
            continue
        prices = prices.dropna()

        prices["is_hl"] = prices["close"] == prices["high_limit"]
        hl_df = prices[prices["is_hl"]].copy()

        if len(hl_df) == 0:
            continue

        hl_df = hl_df[hl_df["money"] > 5e8]

        if len(hl_df) == 0:
            continue

        stock_codes = list(hl_df["code"])

        today_prices = get_price(
            stock_codes,
            end_date=current_str,
            frequency="daily",
            fields=["open", "high_limit"],
            count=1,
            panel=False,
        )
        if today_prices.empty:
            continue
        today_prices = today_prices.dropna()

        today_prices["ratio"] = today_prices["open"] / (
            today_prices["high_limit"] / 1.1
        )
        qualified = today_prices[
            (today_prices["ratio"] >= 1.02) & (today_prices["ratio"] < 1.05)
        ]

        if len(qualified) == 0:
            continue

        buy_codes = list(qualified["code"])

        if len(buy_codes) > 0 and capital > 1000:
            per_stock = capital / len(buy_codes)
            for code in buy_codes:
                try:
                    open_price = qualified[qualified["code"] == code]["open"].iloc[0]
                    amount = int(per_stock / open_price / 100) * 100
                    if amount >= 100:
                        capital -= amount * open_price
                        positions[code] = {"cost": open_price, "amount": amount}
                        trades.append(
                            {"date": current_str, "code": code, "type": "buy"}
                        )
                except:
                    continue

        # 止损检查
        if len(positions) > 0:
            pos_codes = list(positions.keys())
            close_prices = get_price(
                pos_codes,
                end_date=current_str,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            if not close_prices.empty:
                close_prices = close_prices.dropna()
                for code in list(positions.keys()):
                    try:
                        cp = close_prices[close_prices["code"] == code]
                        if len(cp) == 0:
                            continue
                        close_price = cp["close"].iloc[0]
                        high_limit = cp["high_limit"].iloc[0]

                        # 止损检查
                        pos = positions[code]
                        ret = close_price / pos["cost"] - 1

                        # 涨停或止损
                        if close_price >= high_limit * 0.99:
                            continue  # 涨停持有
                        if ret <= STOP_LOSS:
                            # 止损卖出
                            proceeds = pos["amount"] * close_price * 0.999
                            capital += proceeds
                            trades.append(
                                {
                                    "date": current_str,
                                    "code": code,
                                    "type": "sell",
                                    "return": ret,
                                }
                            )
                            del positions[code]
                    except:
                        continue
    except:
        continue

# 最后一天清理
if len(positions) > 0:
    last = trade_days[-1].strftime("%Y-%m-%d")
    for code in list(positions.keys()):
        try:
            p = get_price(
                code,
                end_date=last,
                frequency="daily",
                fields=["close"],
                count=1,
                panel=False,
            )
            if not p.empty:
                capital += positions[code]["amount"] * p["close"].iloc[0] * 0.999
        except:
            pass

buy_trades = [t for t in trades if t["type"] == "buy"]
sell_trades = [t for t in trades if t["type"] == "sell"]
returns = [t["return"] for t in sell_trades if "return" in t]

print(f"\n【结果-止损版(-3%)】")
print(f"  买入次数: {len(buy_trades)}")
print(f"  卖出次数: {len(sell_trades)}")
if len(returns) > 0:
    total_ret = (capital - INITIAL_CAPITAL) / INITIAL_CAPITAL
    annual_ret = (1 + total_ret) ** (252 / len(trade_days)) - 1
    win_rate = len([r for r in returns if r > 0]) / len(returns)
    print(f"  总收益率: {total_ret * 100:.2f}%")
    print(f"  年化收益率: {annual_ret * 100:.2f}%")
    print(f"  胜率: {win_rate * 100:.1f}%")
print(f"  最终资金: {capital:.2f}")
print("=" * 60)
