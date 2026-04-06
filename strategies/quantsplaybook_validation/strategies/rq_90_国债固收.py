# 国债固收策略 - RiceQuant版本
# 逻辑：持有国债ETF为主，大盘趋势向上时适当配置股票ETF

import numpy as np


def init(context):
    context.bond_etf = '511010.XSHG'
    context.stock_etf = '510300.XSHG'
    context.ref = '000300.XSHG'
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    closes = history_bars(context.ref, 60, '1d', 'close')
    if closes is None or len(closes) < 60:
        return
    closes = np.array(closes, dtype=float)
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:])

    if closes[-1] > ma20 and ma20 > ma60:
        stock_pct = 0.4
    elif closes[-1] > ma20:
        stock_pct = 0.2
    else:
        stock_pct = 0.0

    bond_pct = 0.95 - stock_pct

    for etf, pct in [(context.stock_etf, stock_pct), (context.bond_etf, bond_pct)]:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(etf, context.portfolio.total_value * pct)
