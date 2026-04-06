# 稳健型ETF策略 - RiceQuant版本
# 原文：稳健型ETF策略
# 逻辑：基于MACD信号在宽基ETF和债券ETF之间切换，月度调仓

import numpy as np

CASH_ETF = '511010.XSHG'


def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300ETF
        '159915.XSHE',  # 创业板ETF
        '510050.XSHG',  # 上证50ETF
    ]
    context.bond_etf = '511010.XSHG'  # 国债ETF
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    on_start(context, bar_dict)
    context.month = current_month


def on_start(context, bar_dict):
    # 计算各ETF的MACD信号（用双均线代替）
    best_etf = None
    best_score = -999

    for etf in context.etf_pool:
        closes = history_bars(etf, 60, '1d', 'close')
        if closes is None or len(closes) < 60:
            continue
        closes = np.array(closes, dtype=float)
        ma20 = np.mean(closes[-20:])
        ma60 = np.mean(closes[-60:])
        # 动量得分
        momentum = closes[-1] / closes[-20] - 1
        trend = 1 if ma20 > ma60 else -1
        score = momentum * trend
        if score > best_score:
            best_score = score
            best_etf = etf

    # 如果最佳ETF得分为负或没有有效数据，持有债券ETF
    target = CASH_ETF if best_score < 0 or best_etf is None else best_etf

    # 卖出非目标持仓
    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    # 买入目标
    order_target_value(target, context.portfolio.total_value * 0.95)
