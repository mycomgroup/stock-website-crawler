# RiceQuant策略 - 【复现】北向资金交易能力一定强吗
# 原文：https://www.joinquant.com/post/29573
# 作者：Hugo2046
# ⚠️ 注意：原策略依赖北向资金成交数据（finance.STK_ML_QUOTA），
# 该数据在米筐平台不可用。
# 改为用沪深300 ETF动量信号替代北向资金信号。

import numpy as np


def init(context):
    context.target_etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.long_period = 71
    context.short_period = 6
    context.threshold_h = 0.5
    context.threshold_l = -0.5
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def get_momentum_signal(context):
    """用价格动量替代北向资金信号"""
    closes = history_bars(context.target_etf, context.long_period + 5, '1d', 'close')
    if closes is None or len(closes) < context.long_period:
        return None
    closes = np.array(closes, dtype=float)
    long_ma = np.mean(closes[-context.long_period:])
    short_ma = np.mean(closes[-context.short_period:])
    std = np.std(closes[-context.long_period:])
    if std == 0:
        return None
    signal = (short_ma - long_ma) / std
    return signal


def trade(context, bar_dict):
    signal = get_momentum_signal(context)
    if signal is None:
        return

    has_position = len(context.portfolio.positions) > 0

    if signal > context.threshold_h and not has_position:
        bar = (bar_dict[context.target_etf] if context.target_etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(context.target_etf, context.portfolio.total_value * 0.95)

    elif signal < context.threshold_l and has_position:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
