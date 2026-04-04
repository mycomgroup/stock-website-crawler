# 小波分析择时策略 - RiceQuant版本
# 来源：《国信证券-基于小波分析和支持向量机的指数预测模型》
# 简化版：使用多尺度均线代替小波分解

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security

    prices = history_bars(security, 100, '1d', 'close')
    if prices is None or len(prices) < 60:
        return

    closes = np.array(prices)

    # 模拟小波分解的多尺度分析
    # 使用不同周期的均线代表不同频率成分

    ma_short = np.mean(closes[-5:])    # 高频
    ma_mid = np.mean(closes[-20:])     # 中频
    ma_long = np.mean(closes[-60:])    # 低频（趋势）

    # 计算各尺度的方向
    trend_short = ma_short - ma_mid
    trend_mid = ma_mid - ma_long

    # 计算前一期的状态
    prev_ma_short = np.mean(closes[-6:-1])
    prev_ma_mid = np.mean(closes[-21:-1])
    prev_trend_short = prev_ma_short - prev_ma_mid

    # 交易逻辑
    # 多尺度共振：高频、中频、低频方向一致

    current_close = closes[-1]

    # 短期上穿中期 + 中期在长期之上
    cross_up = trend_short > 0 and prev_trend_short <= 0
    above_long = ma_mid > ma_long

    # 短期下穿中期
    cross_down = trend_short < 0 and prev_trend_short >= 0

    if cross_up and above_long and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: short={ma_short:.2f}, mid={ma_mid:.2f}, long={ma_long:.2f}")
    elif cross_down and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: short={ma_short:.2f}, mid={ma_mid:.2f}")