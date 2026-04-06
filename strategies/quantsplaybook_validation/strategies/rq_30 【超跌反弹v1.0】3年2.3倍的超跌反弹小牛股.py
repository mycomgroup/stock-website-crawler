# Auto-generated alias for placeholder rq_30 【超跌反弹v1.0】3年2.3倍的超跌反弹小牛股.txt
# Reuses migrated RiceQuant implementation from rq_30_超跌反弹小牛股.py
# Shared original URL: https://www.joinquant.com/post/35377

# 超跌反弹小牛股策略 - RiceQuant版本
# 原文：【超跌反弹v1.0】3年2.3倍的超跌反弹小牛股
# 作者：_查尔斯葱_
# 原文：https://www.joinquant.com/post/35377
# 逻辑：选ROE高、市值适中的股票，在MA55附近买入，跌破止损

import numpy as np


def init(context):
    context.stock_num = 5
    context.month = -1


def check_buy_point(stock, ma_period=55):
    """检查是否在MA55附近形成买点"""
    try:
        prices = history_bars(stock, ma_period + 10, '1d', 'close')
        if prices is None or len(prices) < ma_period + 1:
            return False
        p = np.array(prices, dtype=float)
        ma55 = np.mean(p[-ma_period:])
        current = p[-1]
        return 0.97 * ma55 <= current <= 1.03 * ma55
    except Exception:
        return False


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith(('688', '4', '8'))]

    candidates = stocks[:200]  # 取前200只股票筛选

    buy_candidates = []
    result = []
    for stock in candidates:
        if check_buy_point(stock):
            buy_result.append(stock)
        if len(buy_candidates) >= context.stock_num * 2:
            break

    target = []
    for stock in buy_candidates:
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
