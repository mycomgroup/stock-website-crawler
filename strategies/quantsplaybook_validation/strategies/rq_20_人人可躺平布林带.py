# 人人可躺平布林带策略 - RiceQuant版本
# 原文：人人可躺平16年3400%
# 作者：逆流的鱼
# 原文：https://www.joinquant.com/post/33859
# 标的：162605.XSHE (富国天惠成长混合)
# 逻辑：布林带中轨附近买入，突破上轨或跌破下轨卖出

import numpy as np

SECURITY = '162605.XSHE'


def init(context):
    context.security = SECURITY
    context.days = 20


def handle_bar(context, bar_dict):
    security = context.security
    if security not in bar_dict:
        return

    bar = bar_dict[security]
    if not bar.is_trading:
        return

    current_price = bar.close
    prices = history_bars(security, context.days, '1d', 'close')
    if prices is None or len(prices) < context.days:
        return

    prices = np.array(prices, dtype=float)
    middle = np.mean(prices)
    std = np.std(prices)
    up = middle + 2.75 * std
    down = middle - 1.0 * std

    # 价格在中轨附近（±0.5std）买入
    if middle - 0.5 * std < current_price < middle + 0.5 * std:
        cash = context.portfolio.cash
        num_shares = int(cash / current_price / 100) * 100
        if num_shares > 0:
            order_shares(security, num_shares)

    # 突破上轨或跌破下轨卖出
    elif current_price > up or current_price < down:
        order_target_value(security, 0)
