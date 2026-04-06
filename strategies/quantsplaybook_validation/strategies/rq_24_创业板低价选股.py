# 创业板低价选股策略 - RiceQuant版本
# 原文：现在便宜的300就是最好的，收益惊人
# 作者：jqz1226
# 原文：https://www.joinquant.com/post/29096
# 逻辑：从创业板成分股中选价格最低的3只，每日调仓

import numpy as np


def init(context):
    context.index = '399102.XSHE'  # 创业板指
    context.buy_count = 3
    scheduler.run_daily(my_trade, time_rule=market_open(minute=220))



def handle_bar(context, bar_dict):
    pass

def my_trade(context, bar_dict):
    stocks = index_components(context.index)
    if not stocks:
        return

    # 获取当前价格，按价格升序排列
    prices = {}
    for stock in stocks:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            prices[stock] = bar.close

    if not prices:
        return

    # 选价格最低的股票
    sorted_stocks = sorted(prices, key=prices.get)
    target = sorted_stocks[:context.buy_count]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
