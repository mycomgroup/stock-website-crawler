"""
影子策略完整回测 - RiceQuant Notebook

修复：
1. 确保所有持仓平仓
2. 正确计算资产
3. 延长测试时间

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_final_rq.py --create-new --timeout-ms 300000
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("影子策略完整回测 - RiceQuant Notebook")
print("=" * 80)
print("配置:")
print("  时间段: 2015-05-01 至 2015-06-30")
print("  测试股票数: 1000只")
print("  情绪阈值: 50只涨停")
print("  初始资金: 100,000元")
print("=" * 80)

MAINLINE_PARAMS = {
    "emotion_threshold": 50,
    "open_change_min": 0.001,
    "open_change_max": 0.03,
    "sell_profit_threshold": 0.03,
    "limit_up_sample_size": 1000,
    "signal_sample_size": 500,
}


def get_all_stocks_list():
    try:
        instruments = all_instruments(type="CS")
        return list(instruments.order_book_id)
    except:
        return []


def get_prev_trading_date(date, trading_dates):
    date_str = str(date)[:10]
    for i, d in enumerate(trading_dates):
        if str(d)[:10] == date_str and i > 0:
            return str(trading_dates[i - 1])[:10]
    return None


def count_limit_ups(date, stock_list, trading_dates):
    limit_up = 0
    tested = 0
    prev_date = get_prev_trading_date(date, trading_dates)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[: MAINLINE_PARAMS["limit_up_sample_size"]]:
        try:
            df = get_price(
                stock,
                start_date=prev_date,
                end_date=date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None and len(df) >= 2:
                prev_close = df["close"].iloc[0]
                curr_close = df["close"].iloc[-1]
                if prev_close > 0:
                    pct = (curr_close - prev_close) / prev_close
                    if pct >= 0.095:
                        limit_up += 1
                    tested += 1
        except:
            continue

    return limit_up, tested


def check_fake_weak_high_open(stock, date, trading_dates):
    try:
        prev_date = get_prev_trading_date(date, trading_dates)
        if prev_date is None:
            return None

        df = get_price(
            stock,
            start_date=prev_date,
            end_date=date,
            frequency="1d",
            fields=["close", "open", "high"],
        )
        if df is None or len(df) < 2:
            return None

        prev_close = df["close"].iloc[0]
        open_price = df["open"].iloc[-1]
        high_price = df["high"].iloc[-1]

        if prev_close <= 0:
            return None

        open_change = (open_price - prev_close) / prev_close

        if (
            open_change <= MAINLINE_PARAMS["open_change_min"]
            or open_change >= MAINLINE_PARAMS["open_change_max"]
        ):
            return None

        if high_price > open_price:
            return {"open_price": open_price, "open_change": open_change}

        return None
    except:
        return None


print("\n步骤1: 获取基础数据")
print("-" * 80)

all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

all_trading_dates = [
    str(d)[:10] for d in list(get_trading_dates("2015-01-01", "2015-12-31"))
]
test_dates = [d for d in all_trading_dates if "2015-05-" in d or "2015-06-" in d]
print(f"测试交易日: {len(test_dates)}天 ({test_dates[0]} 至 {test_dates[-1]})")

if len(all_stocks) == 0 or len(test_dates) == 0:
    print("\n无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n步骤2: 开始回测")
    print("-" * 80)

    initial_capital = 100000.0
    cash = 100000.0
    positions = {}
    trades = []

    print(f"  初始资金: {initial_capital:.2f}")

    for i, date in enumerate(test_dates):
        limit_up, tested = count_limit_ups(date, all_stocks, all_trading_dates)

        emotion_ok = limit_up >= MAINLINE_PARAMS["emotion_threshold"]
        status = "✓" if emotion_ok else "✗"
        print(f"[{date}] 涨停{limit_up:3d}/{tested}只 {status}", end="")

        if emotion_ok:
            print()

            signals = []
            for stock in all_stocks[: MAINLINE_PARAMS["signal_sample_size"]]:
                result = check_fake_weak_high_open(stock, date, all_trading_dates)
                if result:
                    signals.append(
                        {
                            "stock": stock,
                            "open_price": result["open_price"],
                            "open_change": result["open_change"],
                        }
                    )

            print(f"        信号: {len(signals)}个", end="")

            if signals and len(positions) < 3:
                signal = signals[0]
                stock = signal["stock"]
                price = signal["open_price"]

                max_amount = min(100000, cash)
                shares = int(max_amount / price / 100) * 100

                if shares > 0 and cash >= shares * price:
                    cost = shares * price
                    cash -= cost
                    positions[stock] = {
                        "buy_date": date,
                        "buy_price": price,
                        "shares": shares,
                    }
                    trades.append(
                        {
                            "date": date,
                            "stock": stock,
                            "action": "buy",
                            "price": price,
                            "shares": shares,
                        }
                    )
                    print(f" → 买入{stock}@{price:.2f}x{shares}")
                else:
                    print()
            else:
                print()
        else:
            print()

        for stock in list(positions.keys()):
            pos = positions[stock]

            if date <= pos["buy_date"]:
                continue

            try:
                df = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    current_price = df["close"].iloc[-1]
                    profit_pct = (current_price - pos["buy_price"]) / pos["buy_price"]

                    should_sell = False
                    reason = ""

                    if profit_pct >= MAINLINE_PARAMS["sell_profit_threshold"]:
                        should_sell = True
                        reason = "冲高止盈"
                    else:
                        should_sell = True
                        reason = "尾盘卖出"

                    if should_sell:
                        revenue = current_price * pos["shares"]
                        cash += revenue
                        profit = (current_price - pos["buy_price"]) * pos["shares"]

                        trades.append(
                            {
                                "date": date,
                                "stock": stock,
                                "action": "sell",
                                "price": current_price,
                                "shares": pos["shares"],
                                "profit": profit,
                                "profit_pct": profit_pct,
                                "reason": reason,
                            }
                        )

                        print(
                            f"        → 卖出{stock}@{current_price:.2f} {reason} 收益{profit_pct * 100:+.2f}%"
                        )
                        del positions[stock]
            except:
                pass

    print("\n步骤3: 清理剩余持仓")
    print("-" * 80)

    last_date = test_dates[-1]
    for stock in list(positions.keys()):
        pos = positions[stock]
        try:
            df = get_price(
                stock,
                start_date=last_date,
                end_date=last_date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None and len(df) > 0:
                final_price = df["close"].iloc[-1]
                revenue = final_price * pos["shares"]
                cash += revenue
                profit = (final_price - pos["buy_price"]) * pos["shares"]
                profit_pct = profit / (pos["buy_price"] * pos["shares"])

                trades.append(
                    {
                        "date": last_date,
                        "stock": stock,
                        "action": "sell",
                        "price": final_price,
                        "shares": pos["shares"],
                        "profit": profit,
                        "profit_pct": profit_pct,
                        "reason": "强制平仓",
                    }
                )

                print(
                    f"  强制平仓 {stock}@{final_price:.2f} 收益{profit_pct * 100:+.2f}%"
                )
                del positions[stock]
        except:
            pass

    print("\n" + "=" * 80)
    print("回测结果")
    print("=" * 80)

    buy_trades = [t for t in trades if t["action"] == "buy"]
    sell_trades = [t for t in trades if t["action"] == "sell"]

    final_value = cash
    total_return = (final_value - 100000) / 100000

    print(f"\n资金情况:")
    print(f"  初始资金: 100,000.00")
    print(f"  最终资金: {final_value:.2f}")
    print(f"  总收益率: {total_return * 100:.2f}%")

    print(f"\n交易情况:")
    print(f"  买入次数: {len(buy_trades)}")
    print(f"  卖出次数: {len(sell_trades)}")

    if len(sell_trades) > 0:
        wins = [t for t in sell_trades if t.get("profit", 0) > 0]
        losses = [t for t in sell_trades if t.get("profit", 0) <= 0]

        win_rate = len(wins) / len(sell_trades)
        avg_return = np.mean([t["profit_pct"] for t in sell_trades])

        print(f"\n盈亏分析:")
        print(f"  胜率: {win_rate * 100:.1f}% ({len(wins)}/{len(sell_trades)})")
        print(f"  平均收益率: {avg_return * 100:.2f}%")

        if len(wins) > 0:
            avg_win = np.mean([t["profit_pct"] for t in wins])
            print(f"  平均盈利: {avg_win * 100:.2f}%")

        if len(losses) > 0:
            avg_loss = np.mean([t["profit_pct"] for t in losses])
            print(f"  平均亏损: {avg_loss * 100:.2f}%")

        total_profit = sum([t.get("profit", 0) for t in sell_trades])
        print(f"\n  总盈亏: {total_profit:.2f}元")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
