"""
二板策略 - RiceQuant
二板接力 + 情绪过滤
测试期间：2024-07-01 至 2025-03-31
"""


def init(context):
    context.position_stock = None
    context.entry_price = 0
    context.zt_threshold = 10
    scheduler.run_daily(find_second_board, time_rule=market_open(minute=15))


def get_limit_up_count(context, bar_dict, date):
    hs300 = index_components("000300.XSHG", date=date)
    count = 0
    for stock in hs300[:100]:
        try:
            bars = history_bars(stock, 2, "1d", ["close", "high"], bar_dict=bar_dict)
            if bars is None or len(bars) < 2:
                continue
            if bars[-1]["close"] >= bars[-1]["high"] * 0.995:
                count += 1
        except:
            continue
    return count * 8


def find_second_board(context, bar_dict):
    if context.position_stock is not None:
        check_exit(context, bar_dict)
        return

    today = context.now.date()

    zt_count = get_limit_up_count(context, bar_dict, today)
    if zt_count < context.zt_threshold:
        return

    hs300 = index_components("000300.XSHG", date=today)
    candidates = []

    for stock in hs300[:50]:
        try:
            bars = history_bars(
                stock,
                3,
                "1d",
                ["close", "high", "limit_up", "volume"],
                bar_dict=bar_dict,
            )
            if bars is None or len(bars) < 3:
                continue

            t1_close = bars[-1]["close"]
            t1_high = bars[-1]["high"]
            t2_close = bars[-2]["close"]
            t2_high = bars[-2]["high"]
            t3_close = bars[-3]["close"]
            t3_high = bars[-3]["high"]

            t1_zt = t1_close >= t1_high * 0.995
            t2_zt = t2_close >= t2_high * 0.995
            t3_not_zt = t3_close < t3_high * 0.99

            if t1_zt and t2_zt and t3_not_zt:
                today_open = (
                    bar_dict[stock].open if stock in bar_dict else bars[-1]["close"]
                )
                limit_up = (
                    bar_dict[stock].limit_up
                    if stock in bar_dict
                    else bars[-1]["limit_up"]
                )

                if today_open < limit_up * 0.99:
                    candidates.append({"stock": stock, "open_price": today_open})
        except:
            continue

    if len(candidates) == 0:
        return

    target = candidates[0]
    stock = target["stock"]
    price = target["open_price"]

    cash = context.portfolio.total_value * 0.9
    shares = int(cash / price / 100) * 100

    if shares > 0:
        order_shares(stock, shares)
        context.position_stock = stock
        context.entry_price = price
        print(f"[{today}] 2Board Buy {stock} at {price:.2f}, ZT count: {zt_count}")


def check_exit(context, bar_dict):
    stock = context.position_stock
    if stock is None or stock not in bar_dict:
        return

    current = bar_dict[stock].close
    profit = current / context.entry_price - 1

    if profit > 0.06 or profit < -0.04:
        order_target_percent(stock, 0)
        print(
            f"[{context.now.date()}] Sell {stock} at {current:.2f}, profit: {profit * 100:.1f}%"
        )
        context.position_stock = None
        context.entry_price = 0


def after_trading_end(context, bar_dict):
    pass
