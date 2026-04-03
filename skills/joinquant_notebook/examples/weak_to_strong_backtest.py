#!/usr/bin/env python3
"""
弱转强策略完整回测 - 2024年 (最终版)
"""

import pandas as pd
from jqdata import *

print("=" * 60)
print("弱转强策略回测 - 2024-01-01 to 2024-03-31")
print("=" * 60)

INITIAL_CAPITAL = 100000
START = "2024-01-01"
END = "2024-03-31"

trade_days = get_trade_days(start_date=START, end_date=END)
print(f"\n交易日: {len(trade_days)}天")

capital = INITIAL_CAPITAL
positions = {}
trades = []

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

        # 使用 "code" 列获取股票代码
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

        # 使用 "code" 列获取买入的股票代码
        buy_codes = list(qualified["code"])

        if len(buy_codes) > 0 and capital > 1000:
            per_stock = capital / len(buy_codes)
            for code in buy_codes:
                try:
                    open_price = qualified[qualified["code"] == code]["open"].iloc[0]
                    amount = int(per_stock / open_price / 100) * 100
                    if amount >= 100:
                        cost = amount * open_price
                        capital -= cost
                        positions[code] = {
                            "cost": open_price,
                            "amount": amount,
                            "buy_date": current_str,
                        }
                        trades.append(
                            {"date": current_str, "code": code, "type": "buy"}
                        )
                except:
                    continue

        # 卖出 - 使用收盘价
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
            if close_prices.empty:
                continue
            close_prices = close_prices.dropna()

            for code in list(positions.keys()):
                try:
                    cp = close_prices[close_prices["code"] == code]
                    if len(cp) == 0:
                        continue
                    close_price = cp["close"].iloc[0]
                    high_limit = cp["high_limit"].iloc[0]

                    if close_price >= high_limit * 0.99:
                        continue

                    pos = positions[code]
                    proceeds = pos["amount"] * close_price * 0.999
                    ret = close_price / pos["cost"] - 1
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

    except Exception as e:
        continue

# 清理持仓
if len(positions) > 0:
    last_date = trade_days[-1].strftime("%Y-%m-%d")
    pos_codes = list(positions.keys())
    close_prices = get_price(
        pos_codes,
        end_date=last_date,
        frequency="daily",
        fields=["close"],
        count=1,
        panel=False,
    )
    if not close_prices.empty:
        close_prices = close_prices.dropna()
        for code in list(positions.keys()):
            try:
                cp = close_prices[close_prices["code"] == code]
                if len(cp) > 0:
                    pos = positions[code]
                    proceeds = pos["amount"] * cp["close"].iloc[0] * 0.999
                    capital += proceeds
                    trades.append({"date": last_date, "code": code, "type": "sell"})
            except:
                continue

buy_trades = [t for t in trades if t["type"] == "buy"]
sell_trades = [t for t in trades if t["type"] == "sell"]
returns = [t["return"] for t in sell_trades if "return" in t]

print(f"\n【结果】")
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

    print(f"\n【交易明细】")
    for t in sell_trades[:10]:
        ret_str = f"{t['return'] * 100:.2f}%" if "return" in t else "N/A"
        print(f"  {t['date']} {t['code']} return={ret_str}")
else:
    print("  无有效交易")

print("\n" + "=" * 60)
