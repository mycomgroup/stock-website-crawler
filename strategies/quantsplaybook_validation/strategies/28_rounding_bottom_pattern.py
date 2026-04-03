# 圆弧底形态识别选股策略 - RiceQuant版本
# 来源：《技术分析算法框架与实战二：识别圆弧底》
# 核心逻辑：通过核回归识别局部极值，检测圆弧底形态，突破前高时买入

import numpy as np


def gaussian_kernel_regression(y, bandwidth=10):
    """高斯核回归平滑价格序列"""
    n = len(y)
    x = np.arange(n)
    smoothed = np.zeros(n)
    for i in range(n):
        weights = np.exp(-0.5 * ((x - i) / bandwidth) ** 2)
        weights /= weights.sum()
        smoothed[i] = np.dot(weights, y)
    return smoothed


def find_local_extrema(smoothed):
    """找局部极值点"""
    lows, highs = [], []
    for i in range(1, len(smoothed) - 1):
        if smoothed[i] < smoothed[i-1] and smoothed[i] < smoothed[i+1]:
            lows.append(i)
        elif smoothed[i] > smoothed[i-1] and smoothed[i] > smoothed[i+1]:
            highs.append(i)
    return lows, highs


def is_rounding_bottom(prices, p_low_idx, p_high_idx, p=0.3):
    """检测圆弧底形态"""
    if p_high_idx >= p_low_idx:
        return False
    d = p_low_idx - p_high_idx
    if d < 10:
        return False

    p_high = prices[p_high_idx]
    p_low = prices[p_low_idx]

    # 检查左侧下跌比例
    left = prices[p_high_idx:p_low_idx+1]
    if len(left) < 2:
        return False
    down_ratio = np.sum(np.diff(left) < 0) / len(np.diff(left))
    if down_ratio < 0.4:
        return False

    # 检查波动率
    r = np.abs(np.diff(left) / left[:-1])
    if np.mean(r) > 0.03:
        return False

    return True


def init(context):
    context.security = '000300.XSHG'
    context.lookback = 500      # 回溯天数（约2年）
    context.ma200 = 200         # 200日均线
    context.pos = False
    context.buy_price = None


def handle_bar(context, bar_dict):
    security = context.security
    prices = history_bars(security, context.lookback, '1d', 'close')
    if prices is None or len(prices) < context.lookback:
        return

    prices = np.array(prices)
    current = prices[-1]

    # 核回归平滑
    smoothed = gaussian_kernel_regression(prices, bandwidth=15)

    # 找极值点
    lows, highs = find_local_extrema(smoothed)

    if not lows or not highs:
        return

    # 取最近的极小值
    p_low_idx = lows[-1]
    # 找极小值前的极大值
    prev_highs = [h for h in highs if h < p_low_idx]
    if not prev_highs:
        return
    p_high_idx = prev_highs[-1]

    # 检测圆弧底
    if not is_rounding_bottom(prices, p_low_idx, p_high_idx):
        return

    p_high_price = prices[p_high_idx]
    ma200 = np.mean(prices[-context.ma200:])

    # 买入条件：当前价格突破前高且在200日均线上方
    if not context.pos:
        if current > p_high_price and current > ma200:
            order_value(security, context.portfolio.starting_cash * 0.95)
            context.pos = True
            context.buy_price = current
            print(f"买入(圆弧底突破): price={current:.2f}, p_high={p_high_price:.2f}")

    # 止损：跌破买入价的10%
    elif context.pos and context.buy_price:
        if current < context.buy_price * 0.90:
            order_to(security, 0)
            context.pos = False
            print(f"止损: price={current:.2f}")
