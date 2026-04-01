"""
影子策略回测 - 优化版 (RiceQuant Notebook)

基于诊断结果优化：
- 时间段：2015年5月（牛市高峰，涨停比例7%）
- 测试股票数：1000只
- 情绪阈值：50只

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_optimized_rq.py --create-new --timeout-ms 300000
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("影子策略回测 - 优化版")
print("=" * 80)
print("参数配置：")
print("  时间段: 2015-05-01 至 2015-05-31")
print("  测试股票数: 1000只")
print("  情绪阈值: 50只")
print("=" * 80)

STRATEGY_MODE = "mainline"

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


def get_limit_up_count(date, stock_list, trading_dates):
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


def is_fake_weak_high_open(stock, date, trading_dates):
    try:
        prev_date = get_prev_trading_date(date, trading_dates)
        if prev_date is None:
            return False, None

        df = get_price(
            stock,
            start_date=prev_date,
            end_date=date,
            frequency="1d",
            fields=["close", "open", "high"],
        )
        if df is None or len(df) < 2:
            return False, None

        prev_close = df["close"].iloc[0]
        open_price = df["open"].iloc[-1]
        high_price = df["high"].iloc[-1]
        close_price = df["close"].iloc[-1]

        if prev_close <= 0:
            return False, None

        open_change = (open_price - prev_close) / prev_close

        if (
            open_change <= MAINLINE_PARAMS["open_change_min"]
            or open_change >= MAINLINE_PARAMS["open_change_max"]
        ):
            return False, None

        if high_price > open_price:
            return True, {
                "open_price": open_price,
                "close_price": close_price,
                "open_change": open_change,
            }

        return False, None
    except:
        return False, None


print("\n获取数据...")
all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

trading_dates = [
    str(d)[:10] for d in list(get_trading_dates("2015-05-01", "2015-05-31"))
]
print(f"交易日: {len(trading_dates)}天")

if len(all_stocks) == 0 or len(trading_dates) == 0:
    print("\n无法获取数据")
else:
    print("\n开始回测...")

    capital = 100000
    positions = {}
    trades = []
    daily_values = []

    for i, date in enumerate(trading_dates):
        limit_up, tested = get_limit_up_count(date, all_stocks, trading_dates)

        print(f"\n[{date}] 涨停{limit_up}/{tested}只", end="")

        if limit_up >= MAINLINE_PARAMS["emotion_threshold"]:
            print(f" ✓ 达标(>={MAINLINE_PARAMS['emotion_threshold']})")

            signals = []
            for stock in all_stocks[: MAINLINE_PARAMS["signal_sample_size"]]:
                is_signal, info = is_fake_weak_high_open(stock, date, trading_dates)
                if is_signal:
                    signals.append(
                        {
                            "stock": stock,
                            "open_change": info["open_change"],
                            "open_price": info["open_price"],
                        }
                    )

            print(f"  发现{len(signals)}个信号")

            if signals and len(positions) < 3:
                signal = signals[0]
                stock = signal["stock"]
                price = signal["open_price"]

                max_amount = min(100000, capital)
                shares = int(max_amount / price / 100) * 100

                if shares > 0 and capital >= shares * price:
                    capital -= shares * price
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
                            "open_change": signal["open_change"],
                        }
                    )
                    print(
                        f"  → 买入 {stock}: 价格{price:.2f}, 开盘涨幅{signal['open_change'] * 100:.2f}%"
                    )
        else:
            print(f" ✗ 不足(<{MAINLINE_PARAMS['emotion_threshold']})")

        stocks_to_sell = []
        for stock, pos in list(positions.items()):
            try:
                df = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    current_price = df["close"].iloc[0]
                    profit_pct = (current_price - pos["buy_price"]) / pos["buy_price"]

                    if profit_pct >= MAINLINE_PARAMS["sell_profit_threshold"]:
                        stocks_to_sell.append(
                            (stock, current_price, profit_pct, "冲高+3%止盈")
                        )
                    elif date > pos["buy_date"]:
                        stocks_to_sell.append(
                            (stock, current_price, profit_pct, "尾盘卖出")
                        )
            except:
                pass

        for stock, price, profit_pct, reason in stocks_to_sell:
            if stock in positions:
                pos = positions[stock]
                profit = (price - pos["buy_price"]) * pos["shares"]
                capital += price * pos["shares"]
                trades.append(
                    {
                        "date": date,
                        "stock": stock,
                        "action": "sell",
                        "price": price,
                        "profit": profit,
                        "profit_pct": profit_pct,
                        "reason": reason,
                    }
                )
                del positions[stock]
                print(f"  → 卖出 {stock}: {reason}, 收益{profit_pct * 100:.2f}%")

        total_value = capital
        for stock, pos in positions.items():
            try:
                df = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None:
                    total_value += df["close"].iloc[0] * pos["shares"]
            except:
                pass

        daily_values.append({"date": date, "value": total_value})

    print("\n" + "=" * 80)
    print("回测结果")
    print("=" * 80)

    sell_trades = [t for t in trades if t["action"] == "sell"]
    buy_trades = [t for t in trades if t["action"] == "buy"]

    if len(daily_values) > 0:
        final_value = daily_values[-1]["value"]
        total_return = (final_value - 100000) / 100000

        print(f"总收益率: {total_return * 100:.2f}%")
        print(f"最终资产: {final_value:.2f}")
        print(f"买入次数: {len(buy_trades)}")
        print(f"卖出次数: {len(sell_trades)}")

        if len(sell_trades) > 0:
            wins = [t for t in sell_trades if t.get("profit", 0) > 0]
            win_rate = len(wins) / len(sell_trades)
            avg_profit_pct = np.mean([t.get("profit_pct", 0) for t in sell_trades])

            print(f"胜率: {win_rate * 100:.1f}%")
            print(f"平均收益率: {avg_profit_pct * 100:.2f}%")

            if len(wins) > 0:
                avg_win = np.mean([t.get("profit_pct", 0) for t in wins])
                print(f"平均盈利: {avg_win * 100:.2f}%")

            losses = [t for t in sell_trades if t.get("profit", 0) <= 0]
            if len(losses) > 0:
                avg_loss = np.mean([t.get("profit_pct", 0) for t in losses])
                print(f"平均亏损: {avg_loss * 100:.2f}%")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
