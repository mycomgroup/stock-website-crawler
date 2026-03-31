"""
主线策略简化版 - RiceQuant
首板低开假弱高开
测试期间：2024-07-01 至 2025-03-31
"""


def init(context):
    context.position_stock = None
    context.entry_price = 0
    scheduler.run_daily(select_stock, time_rule=market_open(minute=10))


def select_stock(context, bar_dict):
    if context.position_stock is not None:
        check_sell(context, bar_dict)
        return

    today = context.now.date()

    hs300 = index_components("000300.XSHG", date=today)
    zz500 = index_components("000905.XSHG", date=today)
    stock_pool = list(set(hs300) | set(zz500))[:100]

    candidates = []

    for stock in stock_pool:
        try:
            bars = history_bars(
                stock, 2, "1d", ["close", "open", "high", "limit_up"], bar_dict=bar_dict
            )
            if bars is None or len(bars) < 2:
                continue

            prev_close = bars[-2]["close"]
            today_open = bar_dict[stock].open if stock in bar_dict else bars[-1]["open"]
            today_high = bar_dict[stock].high if stock in bar_dict else bars[-1]["high"]
            limit_up = (
                bar_dict[stock].limit_up if stock in bar_dict else bars[-1]["limit_up"]
            )

            if today_open is None or limit_up is None:
                continue

            open_pct = (today_open / prev_close - 1) * 100

            if -3.0 <= open_pct <= -0.5 and today_open < limit_up * 0.99:
                candidates.append(
                    {"stock": stock, "open_pct": open_pct, "open_price": today_open}
                )
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
        print(f"[{today}] Buy {stock} at {price:.2f}")


def check_sell(context, bar_dict):
    stock = context.position_stock
    if stock is None:
        return

    if stock not in bar_dict:
        return

    current = bar_dict[stock].close

    profit_pct = current / context.entry_price - 1

    if profit_pct > 0.05 or profit_pct < -0.04:
        order_target_percent(stock, 0)
        print(
            f"[{context.now.date()}] Sell {stock} at {current:.2f}, profit: {profit_pct * 100:.1f}%"
        )
        context.position_stock = None
        context.entry_price = 0


def after_trading_end(context, bar_dict):
    pass
