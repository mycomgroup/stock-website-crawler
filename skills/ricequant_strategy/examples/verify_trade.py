"""
验证策略 - 确保能产生交易
测试 RiceQuant 回测系统是否正常工作
"""


def init(context):
    context.trade_count = 0
    context.target_stock = "000001.XSHE"
    logger.info("=== 策略初始化 ===")


def handle_bar(context, bar_dict):
    today = context.now.date()
    stock = context.target_stock

    # 检查股票是否可交易
    if stock not in bar_dict:
        return

    bar = bar_dict[stock]
    if not bar.is_trading:
        return

    # 获取当前持仓
    position = context.portfolio.positions.get(stock)
    current_shares = position.quantity if position else 0

    # 如果没有持仓，买入
    if current_shares == 0:
        # 计算可买股数
        cash = context.portfolio.cash
        price = bar.close
        shares = int(cash / price / 100) * 100  # 整手

        if shares >= 100:
            order_shares(stock, shares)
            context.trade_count += 1
            logger.info(f"{today}: 买入 {stock} {shares}股 @ {price:.2f}")

    # 如果有持仓，第二天卖出
    elif context.trade_count == 1:
        order_target(stock, 0)
        logger.info(f"{today}: 卖出 {stock} {current_shares}股 @ {bar.close:.2f}")


def after_trading(context):
    pass
