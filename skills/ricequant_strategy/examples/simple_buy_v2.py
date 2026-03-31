"""
简单买入测试 - RiceQuant 正确格式
"""


def init(context):
    context.bought = False
    scheduler.run_daily(check_buy, time_rule=market_open(minute=5))


def check_buy(context, bar_dict):
    if context.bought:
        return

    stock = "000001.XSHE"

    if stock not in bar_dict:
        return

    bar = bar_dict[stock]

    if not bar.is_trading:
        return

    logger.info(f"Found {stock}, open={bar.open}")

    # 买入
    order_shares(stock, 1000)
    context.bought = True
    logger.info(f"Bought {stock} 1000 shares")


def after_trading(context):
    pass
