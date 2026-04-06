# RiceQuant Python格式策略
# 来源: JoinQuant - 77 致敬市场（2）——随机选股
# 克隆自聚宽文章：https://www.joinquant.com/post/32870
# 标题：致敬市场（2）——随机选股
# 作者：Gyro

import pandas as pd
import numpy as np

def init(context):
    # setting parameters
    context.index = '399311.XSHE' # 国证1000
    context.position_num = 100 # num >= 100
    # setting system
    # setting strategy
    context.last_rebalance_month = -1
    context.buy_counter = 0
    context.sell_counter = 0


def handle_bar(context, bar_dict):
    today = context.now
    if context.now.month not in [1, 7]:
        return
    if context.last_rebalance_month == context.now.month:
        return
    context.last_rebalance_month = context.now.month
    context.buy_counter = 0
    context.sell_counter = 0
    iHandle(context, bar_dict)

def iHandle(context, bar_dict):
    # one trading-day one year
    if context.now.month not in [1, 7]:
        return
    # Begin to work
    print('Hello, working')
    # stocks
    stocks = index_components(context.index)
    if not stocks:
        return
    # Sell
    for s in list(context.portfolio.positions.keys()):
        if s not in stocks:
            print('sell', s, instruments(s).symbol)
            order_target_value(s, 0)
            context.sell_counter = context.sell_counter + 1
    # Buy
    N = len(stocks)
    position_size = context.portfolio.total_value / context.position_num
    while context.portfolio.cash > position_size:
        k = np.random.randint(N)
        s = stocks[k]
        if s not in context.portfolio.positions:
            print('buy', s, instruments(s).symbol)
            order_target_value(s, position_size)
            context.buy_counter = context.buy_counter + 1

def on_strategy_end(context):
    total_return = 0
    if context.portfolio.starting_cash:
        total_return = (
            (context.portfolio.total_value - context.portfolio.starting_cash)
            / context.portfolio.starting_cash
        )
    print('... ... ... Trading Report ... .... ...')
    print('total return', total_return)
    print('total buy', context.buy_counter)
    print('total sell', context.sell_counter)
    print('... ... ... END ... ... ...')
# end
