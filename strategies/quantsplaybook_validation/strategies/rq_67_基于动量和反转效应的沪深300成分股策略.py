# 基于动量和反转效应的沪深300成分股策略 - RiceQuant版本
# 原文：基于动量和反转效应的沪深300成分股策略
# 逻辑：在沪深300成分股中，选近期动量强（12个月涨幅高）但短期反转（1个月涨幅低）的股票

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components('000300.XSHG')
    if not stocks or len(stocks) < 10:
        return

    context.month = current_month

    scores = {}
    for stock in stocks:
        try:
            closes = history_bars(stock, 252, '1d', 'close')
            if closes is None or len(closes) < 60:
                continue
            closes = np.array(closes, dtype=float)
            # 12个月动量（跳过最近1个月，避免短期反转）
            if len(closes) >= 252:
                momentum_12m = closes[-21] / closes[-252] - 1
            else:
                momentum_12m = closes[-21] / closes[0] - 1
            # 1个月反转（近1个月涨幅低的优先）
            reversal_1m = closes[-1] / closes[-21] - 1
            # 综合：动量强 + 短期反转（近1月涨幅不能太高）
            scores[stock] = momentum_12m - reversal_1m * 0.5
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = []
    for stock in sorted_stocks:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
