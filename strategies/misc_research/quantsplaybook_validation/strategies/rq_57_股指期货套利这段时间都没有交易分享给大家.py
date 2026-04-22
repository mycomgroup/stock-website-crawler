# RiceQuant策略 - 股指期货套利
# 原文：https://www.joinquant.com/post/29295
# 作者：节点量化
# ⚠️ 注意：原策略为股指期货套利，依赖期货账户和期货合约API，
# 无法在股票回测环境中运行。
# 改为用沪深300 ETF做简单的均值回归策略替代。

import numpy as np


def init(context):
    context.etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.lookback = 20
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def trade(context, bar_dict):
    closes = history_bars(context.etf, context.lookback + 5, '1d', 'close')
    if closes is None or len(closes) < context.lookback:
        return
    closes = np.array(closes, dtype=float)
    ma = np.mean(closes[-context.lookback:])
    std = np.std(closes[-context.lookback:])
    if std == 0:
        return
    zscore = (closes[-1] - ma) / std

    has_etf = context.portfolio.positions.get(context.etf) is not None and \
              (context.portfolio.positions.get(context.etf) is not None and context.portfolio.positions.get(context.etf).quantity > 0)

    if zscore < -1.0 and not has_etf:
        if context.bond_etf in context.portfolio.positions:
            order_target_value(context.bond_etf, 0)
        bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(context.etf, context.portfolio.total_value * 0.95)
    elif zscore > 1.0 and has_etf:
        order_target_value(context.etf, 0)
        bar = (bar_dict[context.bond_etf] if context.bond_etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
