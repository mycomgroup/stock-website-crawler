# 北上净买入策略 - RiceQuant版本
# 原文：北上净买入策略
# 逻辑：由于RiceQuant无法直接获取北向资金数据，用市场强度（上涨股票比例）替代
# 月度调仓，选沪深300成分股中近期被"聪明钱"持续买入的股票（用动量代理）

import numpy as np


def init(context):
    context.stock_num = 10
    context.month = -1
    context.N = 2  # 持仓数量参数
    scheduler.run_daily(period2, time_rule=market_open(minute=0))


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return
    period(context, bar_dict)


def period(context, bar_dict):
    """月度选股：选沪深300中动量最强的股票"""
    current_month = context.now.month
    stocks = index_components('000300.XSHG')
    if not stocks:
        return

    context.month = current_month

    scores = {}
    for stock in stocks:
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            momentum = closes[-1] / closes[0] - 1
            scores[stock] = momentum
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


def period2(context, bar_dict):
    """日度止损检查"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        loss = bar.close / pos.avg_cost - 1
        if loss < -0.08:
            order_target_value(stock, 0)
