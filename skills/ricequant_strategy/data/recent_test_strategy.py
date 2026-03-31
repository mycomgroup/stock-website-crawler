def init(context):
    context.stocks = ["000001.XSHE", "600000.XSHG"]
    scheduler.run_daily(rebalance)


def rebalance(context, bar_dict):
    for stock in context.stocks:
        if stock in context.portfolio.positions:
            continue
        order_target_percent(stock, 0.5)
