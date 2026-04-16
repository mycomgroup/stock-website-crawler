# 全A创新高比例择时策略 - RiceQuant版本
# 逻辑：计算沪深300成分股中创近60日新高的比例，比例>60%时买入沪深300ETF

import numpy as np


def init(context):
    context.etf = '510300.XSHG'
    context.lookback = 60
    context.buy_threshold = 0.6
    context.sell_threshold = 0.4
    context.pos = False


def handle_bar(context, bar_dict):
    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    new_high_count = 0
    total = 0
    for stock in stocks[:100]:  # 取前100只避免超时
        try:
            closes = history_bars(stock, context.lookback + 1, '1d', 'close')
            if closes is None or len(closes) < context.lookback + 1:
                continue
            closes = np.array(closes, dtype=float)
            if closes[-1] >= np.max(closes[:-1]):
                new_high_count += 1
            total += 1
        except Exception:
            continue

    if total == 0:
        return

    ratio = new_high_count / total

    bar = (bar_dict[context.etf] if context.etf in bar_dict else None)
    if bar is not None and not bar.is_trading:
        return

    if ratio > context.buy_threshold and not context.pos:
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.pos = True
    elif ratio < context.sell_threshold and context.pos:
        order_target_value(context.etf, 0)
        context.pos = False
