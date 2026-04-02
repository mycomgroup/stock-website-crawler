# 超简单测试 - 只验证买卖逻辑
def init(context):
    context.benchmark = "000300.XSHG"
    context.count = 0

    scheduler.run_daily(test_buy, time_rule=market_open(minute=5))
    scheduler.run_daily(test_sell, time_rule=market_close(minute=10))


def test_buy(context, bar_dict):
    if len(context.portfolio.positions) >= 1:
        return

    context.count += 1
    if context.count > 3:
        return

    # 买沪深300第一只成分股
    hs300 = index_components("000300.XSHG")
    if len(hs300) == 0:
        return

    stock = hs300[0]
    if stock in bar_dict:
        try:
            order_value(stock, 10000)
            logger.info(f"买入测试 {stock}")
        except:
            pass


def test_sell(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        try:
            order_target_value(stock, 0)
            logger.info(f"卖出 {stock}")
        except:
            pass
