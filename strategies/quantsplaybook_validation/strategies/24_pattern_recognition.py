# 技术形态识别择时策略 - RiceQuant版本
# 来源：《中泰证券-技术分析算法、框架与实战》
# 识别简单技术形态

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.lookback = 20
    context.pos = False

def detect_double_bottom(closes):
    """检测双底形态"""
    if len(closes) < 20:
        return False

    window = closes[-20:]
    min_idx = np.argmin(window)

    # 双底：两个低点，中间有反弹
    if min_idx > 3 and min_idx < 17:
        left_min = np.min(window[:min_idx])
        right_min = np.min(window[min_idx+1:])

        # 两个低点接近
        if abs(left_min - right_min) / left_min < 0.03:
            return True

    return False

def detect_breakout(closes):
    """检测突破形态"""
    if len(closes) < 20:
        return False

    window = closes[-20:]
    resistance = np.max(window[:-1])
    current = window[-1]

    return current > resistance

def handle_bar(context, bar_dict):
    security = context.security
    lookback = context.lookback

    prices = history_bars(security, lookback + 10, '1d', 'close')
    if prices is None or len(prices) < lookback:
        return

    closes = np.array(prices)

    # 检测形态
    is_double_bottom = detect_double_bottom(closes)
    is_breakout = detect_breakout(closes)

    # 交易逻辑
    # 双底 + 突破 → 买入
    # 跌破支撑 → 卖出

    support = np.min(closes[-lookback:-1])
    current = closes[-1]

    if (is_double_bottom or is_breakout) and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: double_bottom={is_double_bottom}, breakout={is_breakout}")
    elif current < support * 0.97 and context.pos:  # 跌破支撑3%
        order_to(security, 0)
        context.pos = False
        print(f"卖出: support_break")