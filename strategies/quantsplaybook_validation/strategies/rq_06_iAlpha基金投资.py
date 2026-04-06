# iAlpha基金投资策略 - RiceQuant版本
# 原文：iAlpha 基金投资策略
# 作者：Gyro
# 原文：https://www.joinquant.com/post/30024
# 逻辑：固定ETF组合，每月11日再平衡，按等权分配

import numpy as np


FUNDS = [
    '511260.XSHG',  # 国泰十年国债ETF
    '518880.XSHG',  # 华安黄金ETF
    '513500.XSHG',  # 博时标普500ETF
    '513100.XSHG',  # 国泰纳指100ETF
    '159928.XSHE',  # 汇添富中证消费ETF
    '512010.XSHG',  # 易方达沪深300医药ETF
    '513050.XSHG',  # 易方达中概互联50ETF
]
POSITION_N = 9  # 头寸数量（等权）


def init(context):
    context.funds = FUNDS
    context.position_n = POSITION_N
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month
    handle_trader(context, bar_dict)

def handle_trader(context, bar_dict):
    position = context.portfolio.total_value / context.position_n

    # 卖出不在基金池的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.funds:
            order_target_value(s, 0)

    # 买入或再平衡
    for s in context.funds:
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        pos = context.portfolio.positions.get(s)
        current_val = pos.market_value if pos else 0
        delta = position - current_val
        # 偏差超过10%或100倍股价才调仓
        if abs(delta) > max(0.1 * position, 100 * bar.close):
            if delta > 0 and context.portfolio.cash >= delta:
                order_target_value(s, delta)
            elif delta < 0:
                order_target_value(s, position)
