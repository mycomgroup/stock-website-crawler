# 小市值一致性风控策略 - RiceQuant版本
# 原文：韶华研究之十九，一致性用在微盘控制回撤
# 逻辑：选中小板小市值股票，用持仓一致性信号控制回撤

import numpy as np


def init(context):
    context.stock_num = 5
    context.month = -1
    context.week = -1
    context.hv_control = True
    context.hv_duration = 60
    context.hv_ratio = 0.9


def get_stock_list(context):
    try:
        all_stocks = all_instruments('CS')['order_book_id'].tolist()
        stocks = [s for s in all_stocks
                  if not s.startswith(('688', '4', '8'))]
    except Exception:
        return []


def check_high_volume(context, bar_dict):
    """高波动控制：检查市场整体波动率"""
    try:
        index_prices = history_bars('000001.XSHG', context.hv_duration, '1d', 'close')
        if index_prices is None or len(index_prices) < context.hv_duration:
            return False
        p = np.array(index_prices, dtype=float)
        returns = np.diff(p) / p[:-1]
        current_vol = np.std(returns[-20:])
        hist_vol = np.std(returns)
        return current_vol > hist_vol * context.hv_ratio
    except Exception:
        return False


def handle_bar(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    if context.hv_control and check_high_volume(context, bar_dict):
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    target = get_stock_list(context)
    if not target:
        return

    context.week = current_week

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
