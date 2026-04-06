# 基本不耍六毛的ETF轮动策略 - RiceQuant版本
# 原文：基本不耍六毛的ETF轮动策略
# 作者：jqz1226
# 原文：https://www.joinquant.com/post/24432
# 逻辑：动态筛选ETF，按成交量和涨幅选最优，大盘成交量信号控制仓位

import numpy as np


def init(context):
    context.etf_pool = [
        '510050.XSHG', '510300.XSHG', '510500.XSHG',
        '159915.XSHE', '518880.XSHG', '513100.XSHG',
        '513500.XSHG', '159928.XSHE', '512010.XSHG',
        '511010.XSHG',  # 国债ETF（空仓备选）
    ]
    context.cash_etf = '511010.XSHG'
    context.lag = 6
    context.lag0 = 7
    context.lag1 = 13
    context.month = -1
    scheduler.run_daily(etf_trade, time_rule=market_open(minute=220))



def handle_bar(context, bar_dict):
    pass

def get_market_signal(context):
    """大盘成交量信号：连续lag天成交量低于lag0天均量则空仓"""
    try:
        volumes = history_bars('399001.XSHE', context.lag0 + context.lag, '1d', 'volume')
        if volumes is None or len(volumes) < context.lag0 + context.lag:
            return 'BUY'
        v = np.array(volumes, dtype=float)
        ma_vol = np.mean(v[-context.lag0:])
        recent = v[-context.lag:]
        if np.all(recent < ma_vol):
            return 'SELL'
        return 'BUY'
    except Exception:
        return 'BUY'


def get_best_etf(etf_pool, lag1=13):
    """选涨幅最大且在均线上方的ETF"""
    scores = {}
    for etf in etf_pool:
        try:
            prices = history_bars(etf, lag1 + 1, '1d', 'close')
            if prices is None or len(prices) < lag1 + 1:
                continue
            p = np.array(prices, dtype=float)
            change = p[-1] / p[0] - 1
            ma = np.mean(p[-lag1:])
            if change > 0.01 and p[-1] > ma:
                scores[etf] = change
        except Exception:
            continue
    return sorted(scores, key=scores.get, reverse=True)


def etf_trade(context, bar_dict):
    signal = get_market_signal(context)

    if signal == 'SELL':
        for etf in list(context.portfolio.positions.keys()):
            if etf != context.cash_etf:
                order_target_value(etf, 0)
        order_target_value(context.cash_etf, context.portfolio.total_value * 0.95)
        return

    ranked = get_best_etf([e for e in context.etf_pool if e != context.cash_etf], context.lag1)

    if not ranked:
        return

    target = ranked[0]

    for etf in list(context.portfolio.positions.keys()):
        if etf != target:
            order_target_value(etf, 0)

    order_target_value(target, context.portfolio.total_value * 0.95)
