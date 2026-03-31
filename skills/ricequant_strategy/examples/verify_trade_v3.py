"""
验证交易 - RiceQuant 正确格式
关键发现：
1. 使用 logger.info() 而不是 log.info()
2. all_instruments("CS") 返回 DataFrame
3. 使用 handle_bar 而不是 scheduler
"""


def init(context):
    context.s1 = "000001.XSHE"
    context.bought = False
    logger.info("=== 策略初始化 ===")


def handle_bar(context, bar_dict):
    if context.bought:
        return

    stock = context.s1

    if stock not in bar_dict:
        return

    bar = bar_dict[stock]

    if not bar.is_trading:
        return

    position = context.portfolio.positions[stock]

    if position.quantity == 0:
        cash = context.portfolio.cash
        shares = int(cash / bar.close / 100) * 100

        if shares >= 100:
            order_shares(stock, shares)
            context.bought = True
            logger.info(f"买入 {stock} {shares}股 @ {bar.close:.2f}")
