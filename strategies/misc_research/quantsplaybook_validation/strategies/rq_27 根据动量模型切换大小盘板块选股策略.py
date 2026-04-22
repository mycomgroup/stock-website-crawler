# Auto-generated alias for placeholder rq_27 根据动量模型切换大小盘板块选股策略.txt
# Reuses migrated RiceQuant implementation from rq_27_动量模型切换大小盘.py
# Shared original URL: https://www.joinquant.com/post/43540

# 根据动量模型切换大小盘板块选股策略 - RiceQuant版本
# 原文：根据大小盘相对强弱选择合适的板块股票进行交易
# 作者：Jacobb75
# 原文：https://www.joinquant.com/post/43540
# 逻辑：比较上证50和国证2000的动量，强者选对应板块股票

import numpy as np


def get_momentum(security, period=89):
    try:
        prices = history_bars(security, period + 1, '1d', 'close')
        if prices is None or len(prices) < period + 1:
            return 0
        p = np.array(prices, dtype=float)
        return (p[-1] / p[0]) - 1
    except Exception:
        return 0


def init(context):
    context.large_index = '000016.XSHG'   # 上证50
    context.small_index = '399303.XSHE'   # 国证2000
    context.stock_num = 10
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    large_mom = get_momentum(context.large_index)
    small_mom = get_momentum(context.small_index)

    # 选强势板块
    if large_mom >= small_mom:
        # 大盘强：选沪深300成分股中ROE高的
        stocks = index_components('000300.XSHG')
        if not stocks:
            return
        size_filter = (50, 5000)  # 大市值
    else:
        # 小盘强：选小市值
        all_stocks = all_instruments('CS')['order_book_id'].tolist()
        stocks = [s for s in all_stocks
                  if not s.startswith(('688', '4', '8'))]
        size_filter = (5, 100)  # 小市值

    target = []
    candidates = stocks

    for stock in candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)