# 原文链接：https://www.joinquant.com/post/48xxx
# 策略：配套资料
# 核心逻辑：基础量化策略模板，沪深300成分股等权持有，季度调仓

import numpy as np

def init(context):
    context.index = '000300.XSHG'
    scheduler.run_quarterly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    stocks = index_components(context.index)
    if not stocks:
        return

    value_per = context.portfolio.cash / len(stocks)
    for stock in stocks:
        order_target_value(stock, value_per)

    logger.info(f"季度调仓完成，持仓 {len(stocks)} 只沪深300成分股")
