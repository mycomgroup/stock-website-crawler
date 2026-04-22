# 超稳翻倍低Beta期指策略 - RiceQuant版本
# 逻辑：沪深300ETF + 国债ETF组合，根据大盘趋势动态调整比例，低Beta

import numpy as np


def init(context):
    context.stock_etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.ma_period = 20
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    closes = history_bars(context.stock_etf, 60, '1d', 'close')
    if closes is None or len(closes) < 60:
        return
    closes = np.array(closes, dtype=float)

    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:])
    returns = np.diff(closes) / closes[:-1]
    vol = np.std(returns[-20:])

    # 根据趋势和波动率动态调整股债比例
    if closes[-1] > ma20 and ma20 > ma60:
        # 强趋势：股票60%，债券40%
        stock_pct = 0.6
    elif closes[-1] > ma20:
        # 弱趋势：股票40%，债券60%
        stock_pct = 0.4
    else:
        # 下跌趋势：股票20%，债券80%
        stock_pct = 0.2

    # 高波动时降低股票仓位
    if vol > 0.015:
        stock_pct *= 0.7

    bond_pct = 0.95 - stock_pct

    for etf, pct in [(context.stock_etf, stock_pct), (context.bond_etf, bond_pct)]:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(etf, context.portfolio.total_value * pct)
