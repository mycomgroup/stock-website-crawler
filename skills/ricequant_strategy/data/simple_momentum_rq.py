"""
简单动量策略 - RiceQuant
买入跌幅超过2%的沪深300成分股
测试期间：2024-07-01 至 2025-03-31
"""

STOCK_POOL = [
    "600519.XSHG",
    "600036.XSHG",
    "601318.XSHG",
    "600000.XSHG",
    "601166.XSHG",
    "600030.XSHG",
    "601398.XSHG",
    "601288.XSHG",
    "600887.XSHG",
    "600276.XSHG",
    "000001.XSHE",
    "000002.XSHE",
    "000333.XSHE",
    "000651.XSHE",
    "000858.XSHE",
    "002415.XSHE",
]


def init(context):
    context.position_stock = None
    context.entry_price = 0
    context.hold_days = 0
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def trade(context, bar_dict):
    if context.position_stock is not None:
        context.hold_days += 1

        stock = context.position_stock
        if stock in bar_dict:
            current = bar_dict[stock].close
            profit = current / context.entry_price - 1

            if profit > 0.03 or profit < -0.03 or context.hold_days >= 3:
                order_target_percent(stock, 0)
                print(f"Sell {stock} at {current:.2f}, profit: {profit * 100:.1f}%")
                context.position_stock = None
                context.entry_price = 0
                context.hold_days = 0
        return

    today = context.now.date()

    for stock in STOCK_POOL:
        try:
            if stock not in bar_dict:
                continue

            current = bar_dict[stock].close
            limit_up = bar_dict[stock].limit_up
            limit_down = bar_dict[stock].limit_down

            if current <= 0:
                continue

            if limit_up and current >= limit_up * 0.99:
                continue

            bars = history_bars(stock, 2, "1d", "close", bar_dict=bar_dict)
            if bars is None or len(bars) < 2:
                continue

            prev_close = bars[-2]
            change = current / prev_close - 1

            if change < -0.02:
                order_target_percent(stock, 0.95)
                context.position_stock = stock
                context.entry_price = current
                context.hold_days = 0
                print(
                    f"[{today}] Buy {stock} at {current:.2f}, change: {change * 100:.1f}%"
                )
                break
        except Exception as e:
            continue


def after_trading_end(context, bar_dict):
    pass
