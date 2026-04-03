# 低延迟趋势线择时策略 - RiceQuant版本
# 来源：《广发证券-低延迟趋势线与交易择时》
# 使用低延迟趋势线(Low-Lag Trend Line)减少传统均线的滞后性

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20  # 趋势线周期
    context.pos = False

def low_lag_trendline(prices, period):
    """
    低延迟趋势线算法
    传统均线滞后约period/2，通过加权减少滞后
    """
    n = len(prices)
    if n < period:
        return None

    # 使用线性加权减少滞后
    # LLTL = weighted average with forward-looking correction
    closes = prices[-period:]

    # 简化版：使用指数加权
    weights = np.exp(np.linspace(-1, 0, period))
    weights = weights / weights.sum()

    llt = np.sum(closes * weights)

    return llt

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史收盘价
    prices = history_bars(security, period + 10, '1d', 'close')
    if prices is None or len(prices) < period:
        return

    closes = np.array(prices)

    # 计算低延迟趋势线
    llt = low_lag_trendline(closes, period)
    if llt is None:
        return

    # 计算前一日的趋势线
    prev_llt = low_lag_trendline(closes[:-1], period)

    current_close = closes[-1]
    prev_close = closes[-2]

    # 交易逻辑：价格穿越趋势线
    # 上穿买入，下穿卖出

    if prev_llt is not None:
        # 上穿：昨收<昨趋势线 且 今收>今趋势线
        if prev_close < prev_llt and current_close > llt and not context.pos:
            order_value(security, context.portfolio.starting_cash * 0.95)
            context.pos = True
            print(f"买入上穿: close={current_close:.2f}, LLT={llt:.2f}")
        # 下穿：昨收>昨趋势线 且 今收<今趋势线
        elif prev_close > prev_llt and current_close < llt and context.pos:
            order_to(security, 0)
            context.pos = False
            print(f"卖出下穿: close={current_close:.2f}, LLT={llt:.2f}")