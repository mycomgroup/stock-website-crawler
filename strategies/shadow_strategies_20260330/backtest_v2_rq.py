"""
影子策略回测 - RiceQuant Notebook（修复版）

修复：资金计算逻辑

运行：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_v2_rq.py --create-new --timeout-ms 300000
"""

print("=" * 80)
print("影子策略回测 - RiceQuant Notebook")
print("=" * 80)

import numpy as np

PARAMS = {
    "emotion_threshold": 50,
    "open_change_min": 0.001,
    "open_change_max": 0.03,
    "sell_profit": 0.03,
    "sample_size": 1000,
}


def get_stocks():
    try:
        ins = all_instruments(type="CS")
        return list(ins.order_book_id)
    except:
        return []


def get_prev_date(date, dates):
    s = str(date)[:10]
    for i, d in enumerate(dates):
        if str(d)[:10] == s and i > 0:
            return str(dates[i - 1])[:10]
    return None


def count_limit_up(date, stocks, dates):
    prev = get_prev_date(date, dates)
    if not prev:
        return 0, 0

    cnt, tested = 0, 0
    for s in stocks[: PARAMS["sample_size"]]:
        try:
            df = get_price(
                s, start_date=prev, end_date=date, frequency="1d", fields=["close"]
            )
            if df is not None and len(df) >= 2:
                if df["close"].iloc[0] > 0:
                    pct = (df["close"].iloc[-1] - df["close"].iloc[0]) / df[
                        "close"
                    ].iloc[0]
                    if pct >= 0.095:
                        cnt += 1
                    tested += 1
        except:
            pass
    return cnt, tested


def check_signal(stock, date, dates):
    prev = get_prev_date(date, dates)
    if not prev:
        return None

    try:
        df = get_price(
            stock,
            start_date=prev,
            end_date=date,
            frequency="1d",
            fields=["close", "open", "high"],
        )
        if df is None or len(df) < 2:
            return None

        prev_close = df["close"].iloc[0]
        open_p = df["open"].iloc[-1]
        high_p = df["high"].iloc[-1]

        if prev_close <= 0:
            return None

        open_chg = (open_p - prev_close) / prev_close

        if (
            open_chg <= PARAMS["open_change_min"]
            or open_chg >= PARAMS["open_change_max"]
        ):
            return None

        if high_p > open_p:
            return {"open": open_p, "chg": open_chg}
        return None
    except:
        return None


print("\n获取数据...")
stocks = get_stocks()
all_dates = [str(d)[:10] for d in list(get_trading_dates("2015-05-01", "2015-06-30"))]

print(f"股票: {len(stocks)}, 交易日: {len(all_dates)}")

if stocks and all_dates:
    print("\n开始回测...")
    print("-" * 80)

    cash = 100000.0
    holdings = {}
    trades = []

    for date in all_dates:
        limit_up, tested = count_limit_up(date, stocks, all_dates)

        if limit_up >= PARAMS["emotion_threshold"]:
            print(f"[{date}] 涨停{limit_up}/{tested} ✓", end="")

            signals = []
            for s in stocks[:500]:
                sig = check_signal(s, date, all_dates)
                if sig:
                    signals.append({"stock": s, "open": sig["open"], "chg": sig["chg"]})

            print(f" 信号{len(signals)}", end="")

            if signals and len(holdings) < 3:
                sig = signals[0]
                stock = sig["stock"]
                price = sig["open"]

                use_cash = min(50000, cash)
                shares = int(use_cash / price / 100) * 100

                if shares > 0:
                    cost = shares * price
                    if cash >= cost:
                        cash -= cost
                        holdings[stock] = {
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
                        print(f" → 买{stock}@{price:.2f}x{shares}")
                    else:
                        print()
                else:
                    print()
            else:
                print()
        else:
            print(f"[{date}] 涨停{limit_up}/{tested} ✗")

        for stock in list(holdings.keys()):
            h = holdings[stock]
            if date <= h["buy_date"]:
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
                    curr_price = df["close"].iloc[-1]
                    pct = (curr_price - h["buy_price"]) / h["buy_price"]

                    if pct >= PARAMS["sell_profit"]:
                        revenue = curr_price * h["shares"]
                        cash += revenue
                        profit = (curr_price - h["buy_price"]) * h["shares"]
                        trades.append(
                            {
                                "date": date,
                                "stock": stock,
                                "action": "sell",
                                "price": curr_price,
                                "shares": h["shares"],
                                "pct": pct,
                                "profit": profit,
                                "reason": "止盈",
                            }
                        )
                        print(
                            f"        → 卖{stock}@{curr_price:.2f} 止盈 +{pct * 100:.1f}%"
                        )
                        del holdings[stock]
                    elif date > h["buy_date"]:
                        revenue = curr_price * h["shares"]
                        cash += revenue
                        profit = (curr_price - h["buy_price"]) * h["shares"]
                        trades.append(
                            {
                                "date": date,
                                "stock": stock,
                                "action": "sell",
                                "price": curr_price,
                                "shares": h["shares"],
                                "pct": pct,
                                "profit": profit,
                                "reason": "尾盘",
                            }
                        )
                        print(
                            f"        → 卖{stock}@{curr_price:.2f} 尾盘 {pct * 100:+.1f}%"
                        )
                        del holdings[stock]
            except:
                pass

    print("\n清仓...")
    if holdings:
        last_date = all_dates[-1]
        for stock in list(holdings.keys()):
            h = holdings[stock]
            try:
                df = get_price(
                    stock,
                    start_date=last_date,
                    end_date=last_date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None:
                    price = df["close"].iloc[-1]
                    revenue = price * h["shares"]
                    cash += revenue
                    pct = (price - h["buy_price"]) / h["buy_price"]
                    profit = (price - h["buy_price"]) * h["shares"]
                    trades.append(
                        {
                            "date": last_date,
                            "stock": stock,
                            "action": "sell",
                            "price": price,
                            "shares": h["shares"],
                            "pct": pct,
                            "profit": profit,
                            "reason": "清仓",
                        }
                    )
                    print(f"  清仓 {stock}@{price:.2f} {pct * 100:+.1f}%")
                    del holdings[stock]
            except:
                pass

    print("\n" + "=" * 80)
    print("回测结果")
    print("=" * 80)

    sells = [t for t in trades if t["action"] == "sell"]
    buys = [t for t in trades if t["action"] == "buy"]

    total_return = (cash - 100000) / 100000
    total_profit = sum([t.get("profit", 0) for t in sells])

    print(f"\n初始资金: 100,000.00")
    print(f"最终资金: {cash:.2f}")
    print(f"总收益率: {total_return * 100:.2f}%")
    print(f"总盈亏: {total_profit:.2f}元")

    print(f"\n买入: {len(buys)}次")
    print(f"卖出: {len(sells)}次")

    if sells:
        wins = [t for t in sells if t.get("profit", 0) > 0]
        losses = [t for t in sells if t.get("profit", 0) <= 0]

        win_rate = len(wins) / len(sells)
        avg_pct = np.mean([t["pct"] for t in sells])

        print(f"\n胜率: {win_rate * 100:.1f}% ({len(wins)}/{len(sells)})")
        print(f"平均收益率: {avg_pct * 100:.2f}%")

        if wins:
            print(f"平均盈利: {np.mean([t['pct'] for t in wins]) * 100:.2f}%")
        if losses:
            print(f"平均亏损: {np.mean([t['pct'] for t in losses]) * 100:.2f}%")

    print("\n" + "=" * 80)
    print("完成")
    print("=" * 80)
