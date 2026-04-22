# 原文链接：https://www.joinquant.com/post/35416
# 策略：宏观数据中长线策略，年化15%，最大回撤9%
# 核心逻辑：用沪深300长期均线（MA120）判断牛熊，牛市持有沪深300ETF，熊市持有国债ETF，每月调仓一次

import numpy as np

STOCK_ETF = '510300.XSHG'   # 沪深300ETF
BOND_ETF  = '511010.XSHG'   # 国债ETF
REF_INDEX = '000300.XSHG'   # 沪深300指数
MA_PERIOD = 120              # 长期均线

def init(context):
    context.month = -1
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass

def trade(context, bar_dict):
    if context.now.month == context.month:
        return
    context.month = context.now.month

    prices = history_bars(REF_INDEX, MA_PERIOD + 1, '1d', 'close')
    if prices is None or len(prices) < MA_PERIOD + 1:
        return

    p = np.array(prices, dtype=float)
    ma = np.mean(p[-MA_PERIOD:])
    current = p[-1]

    if current > ma:
        # 牛市：持有股票ETF
        target = STOCK_ETF
    else:
        # 熊市：持有债券ETF
        target = BOND_ETF

    for s in list(context.portfolio.positions.keys()):
        if s != target:
            order_target_value(s, 0)
    order_target_value(target, context.portfolio.total_value * 0.95)
    print(f"[宏观中长线] {'牛市' if target==STOCK_ETF else '熊市'} price={current:.2f} MA{MA_PERIOD}={ma:.2f}")
