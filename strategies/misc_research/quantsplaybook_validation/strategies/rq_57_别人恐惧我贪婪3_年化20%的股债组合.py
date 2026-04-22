# RiceQuant策略 - 别人恐惧我贪婪3——年化20%的股债组合
# 原文：https://www.joinquant.com/post/37633
# 作者：潜水的白鱼

def init(context):

    context.pool = ['512100.XSHG']
    context.nationaldabt = ['511010.XSHG']
    context.buttun = 0

    scheduler.run_daily(market_1455, time_rule=market_close(minute=5))


def handle_bar(context, bar_dict):
    pass


def market_1455(context, bar_dict):
    """尾盘运行：根据指数涨跌切换股票/国债"""
    df = history_bars('000001.XSHG', 2, '1d', 'close')
    if df is None or len(df) < 2:
        return

    price_change = (df[-1] - df[-2]) / df[-2] if df[-2] != 0 else 0

    if price_change < -0.01:
        if context.buttun == 1:
            for stock in list(context.portfolio.positions.keys()):
                order_target_value(stock, 0)
            context.buttun = 0
    else:
        if context.buttun == 0:
            for etf in list(context.portfolio.positions.keys()):
                order_target_value(etf, 0)
            context.buttun = 1

    if context.buttun == 0:
        for nd in context.nationaldabt:
            order_target_value(nd, context.portfolio.total_value)
    else:
        for stock in context.pool:
            order_target_value(stock, context.portfolio.total_value)
