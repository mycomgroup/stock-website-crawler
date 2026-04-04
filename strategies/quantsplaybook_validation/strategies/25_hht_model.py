# HHT模型择时策略 - RiceQuant版本
# 来源：《招商证券-结合改进HHT模型和分类算法的交易策略》
# 使用希尔伯特-黄变换思想，简化为EMD趋势分解

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.pos = False

def emd_like_decomposition(closes, n_imfs=3):
    """类EMD分解：使用不同窗口的均线模拟IMF"""
    imfs = []

    # 模拟不同频率的IMF
    windows = [5, 10, 20]  # 短、中、长期

    for w in windows:
        if len(closes) >= w:
            ma = np.mean(closes[-w:])
            imfs.append(ma)
        else:
            imfs.append(closes[-1])

    return imfs

def handle_bar(context, bar_dict):
    security = context.security

    prices = history_bars(security, 60, '1d', 'close')
    if prices is None or len(prices) < 30:
        return

    closes = np.array(prices)

    # EMD分解
    imfs = emd_like_decomposition(closes)

    # 分析各IMF的趋势
    # IMF1 (高频) - 短期波动
    # IMF2 (中频) - 中期趋势
    # IMF3 (低频) - 长期趋势

    short_trend = imfs[0] - imfs[1]  # 短期相对中期
    mid_trend = imfs[1] - imfs[2]    # 中期相对长期
    long_trend = imfs[2] - np.mean(closes[-60:])  # 长期相对历史

    # 计算前一期的状态
    prev_imfs = emd_like_decomposition(closes[:-1])
    prev_short_trend = prev_imfs[0] - prev_imfs[1]

    # 瞬时频率（趋势变化速度）
    freq_short = short_trend - prev_short_trend

    # 交易逻辑
    # 多层次趋势共振

    current = closes[-1]

    # 短期上穿中期 + 中期在长期之上
    cross_up = short_trend > 0 and prev_short_trend <= 0
    above_long = mid_trend > 0

    # 短期下穿中期
    cross_down = short_trend < 0 and prev_short_trend >= 0

    if cross_up and above_long and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: short={short_trend:.2f}, mid={mid_trend:.2f}")
    elif cross_down and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: short={short_trend:.2f}")