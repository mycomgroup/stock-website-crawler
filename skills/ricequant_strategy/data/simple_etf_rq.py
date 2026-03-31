"""
最简单的买入持有策略 - RiceQuant
每月第一天买入沪深300ETF
"""


def init(context):
    context.last_month = -1
    context.stock = "510300.XSHG"
    scheduler.run_daily(rebalance)


def rebalance(context, bar_dict):
    today = context.now

    if today.month == context.last_month:
        return

    context.last_month = today.month

    stock = context.stock

    if stock not in bar_dict:
        print(f"{stock} not in bar_dict")
        return

    price = bar_dict[stock].close
    if price <= 0:
        return

    order_target_percent(stock, 0.95)
    print(f"[{today.date()}] Buy {stock} at {price:.2f}")
