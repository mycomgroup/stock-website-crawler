# 简单股指期货尾盘策略 - RiceQuant版本
# 原文：简单到发指的股指策略(2013到现在收益10949%)
# 原文：https://www.joinquant.com/post/30480
# 逻辑：尾盘买入沪深300ETF，次日开盘卖出（日内动量）
# 注：原版交易股指期货，此版本改为ETF

import numpy as np


def init(context):
    context.security = '510300.XSHG'
    context.pos = False
    scheduler.run_daily(buy, time_rule=market_open(minute=235))
    scheduler.run_daily(sell, time_rule=market_open(minute=0))



def handle_bar(context, bar_dict):
    pass

def buy(context, bar_dict):
    if context.pos:
        return
    bar = (bar_dict[context.security] if context.security in bar_dict else None)
    if bar is None or not bar.is_trading:
        return
    order_target_value(context.security, context.portfolio.total_value * 0.95)
    context.pos = True


def sell(context, bar_dict):
    if not context.pos:
        return
    order_target_value(context.security, 0)
    context.pos = False
