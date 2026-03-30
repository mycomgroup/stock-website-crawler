# 最简单测试策略 - 固定买入一只股票


def init(context):
    context.benchmark = "000300.XSHG"
    context.test_stock = "600519.XSHG"


def handle_bar(context, bar_dict):
    stock = context.test_stock

    if stock not in bar_dict:
        logger.warning(f"Stock {stock} not in bar_dict")
        return

    bar = bar_dict[stock]
    logger.info(f"Stock {stock} found, close={bar.close}, is_trading={bar.is_trading}")

    if context.portfolio.positions[stock].quantity == 0:
        order_target_value(stock, context.portfolio.total_value * 0.9)
        logger.info(f"Buy {stock}")
