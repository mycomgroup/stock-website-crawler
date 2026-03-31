"""
简单买入测试 - RiceQuant handle_bar 方式
"""


def init(context):
    context.bought = False
    context.s1 = "000001.XSHE"


def handle_bar(context, bar_dict):
    if context.bought:
        return

    stock = context.s1

    if stock not in bar_dict:
        return

    bar = bar_dict[stock]

    # 买入
    shares = int(context.portfolio.cash / bar.close / 100) * 100
    if shares >= 100:
        order_shares(stock, shares)
        context.bought = True
        logger.info(f"Bought {stock} {shares} shares @ {bar.close}")
