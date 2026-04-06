# 北上詹姆斯策略 - RiceQuant版本
# 逻辑：用大盘动量代替北向资金数据，选沪深300中动量最强的股票，月度调仓

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1
    scheduler.run_daily(rebalance, time_rule=market_open(minute=0))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    current_month = context.now.month
    if not hasattr(context, 'last_month'):
        context.last_month = -1
    if current_month == context.last_month:
        return
    context.last_month = current_month

    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            scores[stock] = closes[-1] / closes[0] - 1
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = [s for s in sorted_stocks if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
