"""
主线策略最近日期测试 - RiceQuant
首板低开假弱高开策略
测试期间: 2025-01-01 至 2026-03-31
"""


def init(context):
    context.s1 = "000001.XSHE"
    scheduler.run_daily(check_and_trade, time_rule=market_open(minute=5))


def check_and_trade(context, bar_dict):
    today = context.now.date()

    all_stocks = all_instruments(type="CS", date=today)
    stock_list = [
        s.order_book_id
        for s in all_stocks
        if not s.order_book_id.startswith("688")
        and not s.order_book_id.startswith("4")
        and not s.order_book_id.startswith("8")
    ]

    selected = []

    for stock in stock_list[:500]:
        try:
            prices = history_bars(stock, 2, "1d", "close", bar_dict=bar_dict)
            if prices is None or len(prices) < 2:
                continue

            prev_close = prices[-2]
            today_open = bar_dict[stock].open if stock in bar_dict else None
            limit_up = bar_dict[stock].limit_up if stock in bar_dict else None

            if today_open is None or limit_up is None:
                continue

            open_pct = (today_open / prev_close - 1) * 100

            if 0.5 <= open_pct <= 1.5 and today_open < limit_up * 0.99:
                selected.append(
                    {"stock": stock, "open_pct": open_pct, "open_price": today_open}
                )
        except:
            continue

    if len(selected) > 0:
        target = selected[0]
        order_target_percent(target["stock"], 0.9)
        context.entry_price = target["open_price"]
        context.entry_stock = target["stock"]
        context.entry_date = today


def after_trading_end(context, bar_dict):
    if (
        hasattr(context, "entry_stock")
        and context.entry_stock in context.portfolio.positions
    ):
        order_target_percent(context.entry_stock, 0)
