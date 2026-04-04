# ICU均线择时策略 - RiceQuant版本
# 来源：《中泰证券-均线才是绝对收益利器-ICU均线下的择时策略》
# 使用numpy替代scipy实现稳健回归

import numpy as np

def siegel_slope_numpy(y):
    """用numpy实现Siegel稳健回归斜率"""
    x = np.arange(len(y))
    n = len(y)

    # 计算所有点对之间的斜率
    slopes = []
    for i in range(n):
        for j in range(i+1, n):
            if x[j] != x[i]:
                slopes.append((y[j] - y[i]) / (x[j] - x[i]))

    # 取中位数作为稳健斜率
    slope = np.median(slopes)

    # 计算截距: median(y - slope * x)
    intercepts = y - slope * x
    intercept = np.median(intercepts)

    return slope, intercept

def init(context):
    context.security = '000300.XSHG'
    context.N = 20  # ICU均线周期 (Adapted from 5 to reduce drawdowns)
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    N = context.N

    # 获取历史收盘价
    prices = history_bars(security, N + 20, '1d', 'close')
    if prices is None or len(prices) < N:
        return

    closes = np.array(prices[-N:])

    # 计算ICU均线 (使用numpy实现的稳健回归)
    try:
        slope, intercept = siegel_slope_numpy(closes)
        icu_ma = intercept + slope * (N - 1)
    except Exception:
        return

    current_close = closes[-1]

    # 交易逻辑: 价格上穿ICU均线买入，下穿卖出
    if current_close > icu_ma and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: close={current_close:.2f}, ICU_MA={icu_ma:.2f}")
    elif current_close < icu_ma and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: close={current_close:.2f}, ICU_MA={icu_ma:.2f}")