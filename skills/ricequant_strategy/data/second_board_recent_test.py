"""
二板策略最近日期测试 - RiceQuant
二板接力策略 (缩量条件 + 情绪过滤)
测试期间: 2025-01-01 至 2026-03-31
"""


def init(context):
    context.zt_threshold = 10
    scheduler.run_daily(rebalance, time_rule=market_open(minute=10))


def get_limit_up_stocks(context, date, bar_dict):
    all_stocks = all_instruments(type="CS", date=date)
    stock_list = [
        s.order_book_id
        for s in all_stocks
        if not s.order_book_id.startswith("688")
        and not s.order_book_id.startswith("4")
        and not s.order_book_id.startswith("8")
    ]

    limit_up_list = []

    for stock in stock_list[:800]:
        try:
            prices = history_bars(
                stock, 2, "1d", ["close", "high", "limit_up"], bar_dict=bar_dict
            )
            if prices is None or len(prices) < 2:
                continue

            today_close = prices[-1]["close"]
            today_high = prices[-1]["high"]
            prev_close = prices[-2]["close"]
            limit_up = prices[-1]["limit_up"]

            if today_close >= today_high * 0.995 and today_close >= prev_close * 1.095:
                limit_up_list.append(stock)
        except:
            continue

    return limit_up_list


def get_zt_count(context, date, bar_dict):
    return len(get_limit_up_stocks(context, date, bar_dict))


def rebalance(context, bar_dict):
    today = context.now.date()

    zt_count = get_zt_count(context, today, bar_dict)

    if zt_count < context.zt_threshold:
        return

    today_zt = get_limit_up_stocks(context, today, bar_dict)

    prev_trading_date = get_previous_trading_date(today)
    prev_zt = get_limit_up_stocks(context, prev_trading_date, bar_dict)

    prev2_trading_date = get_previous_trading_date(prev_trading_date)
    prev2_zt = get_limit_up_stocks(context, prev2_trading_date, bar_dict)

    candidates = list(set(today_zt) & set(prev_zt) - set(prev2_zt))

    if len(candidates) == 0:
        return

    for stock in candidates[:3]:
        try:
            prices = history_bars(
                stock, 2, "1d", ["open", "limit_up"], bar_dict=bar_dict
            )
            if prices is None:
                continue

            today_open = prices[-1]["open"]
            limit_up = prices[-1]["limit_up"]

            if today_open < limit_up * 0.99:
                order_target_percent(stock, 0.3)
        except:
            continue


def after_trading_end(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_percent(stock, 0)
