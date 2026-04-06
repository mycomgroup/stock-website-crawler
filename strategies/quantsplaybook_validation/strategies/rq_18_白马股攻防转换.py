# 白马股攻防转换策略 - RiceQuant版本
# 原文：国庆节献礼：实例说明白马股攻防转换策略
# 原文：https://www.joinquant.com/post/26648
# 逻辑：选择ROE高、市值大的白马股，用均线判断攻防状态切换

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.top_n = 10
    context.ma_period = 60
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks:
        return

    context.month = current_month

    # 用基本面筛选白马股：ROE > 15%，市值大
    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
            df = df[df['roe'] > 0.15]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 用均线判断攻防状态
    scores = {}
    for stock in candidates:
        try:
            prices = history_bars(stock, context.ma_period + 1, '1d', 'close')
            if prices is None or len(prices) < context.ma_period + 1:
                continue
            p = np.array(prices, dtype=float)
            ma = np.mean(p[-context.ma_period:])
            current = p[-1]
            # 攻势：价格在均线上方，动量为正
            momentum = (p[-1] / p[-context.ma_period] - 1)
            if current > ma:
                scores[stock] = momentum
        except Exception:
            continue

    if not scores:
        return

    target = sorted(scores, key=scores.get, reverse=True)[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
