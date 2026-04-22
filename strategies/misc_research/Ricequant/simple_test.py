# Simple Test Strategy for RiceQuant
# 使用 order_target_value


def init(context):
    context.benchmark = "000300.XSHG"
    context.stocks = ["000001.XSHE", "600000.XSHG"]
    context.bought = False
    scheduler.run_daily(rebalance)


def rebalance(context, bar_dict):
    if context.bought:
        return

    # 检查股票是否可交易
    tradable = []
    for stock in context.stocks:
        if stock in bar_dict:
            bar = bar_dict[stock]
            if bar.is_trading:
                tradable.append(stock)

    if len(tradable) == 0:
        return

    # 等权买入
    total = context.portfolio.total_value
    per_stock = total / len(tradable)

    for stock in tradable:
        order_target_value(stock, per_stock)

    context.bought = True
    log.info(f"Bought {len(tradable)} stocks")
