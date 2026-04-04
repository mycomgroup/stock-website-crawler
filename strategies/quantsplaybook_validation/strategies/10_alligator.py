#鳄鱼线择时策略 - RiceQuant版本
# 来源：《招商证券-基于鳄鱼线的指数择时及轮动策略》
# 鳄鱼线(Alligator) = 三条平滑移动平均线

import numpy as np

def smoothed_ma(prices, period):
    """平滑移动平均线 (SMMA)"""
    n = len(prices)
    if n < period:
        return None

    # SMMA = (前一日SMMA * (period-1) + 今日收盘) / period
    smma = np.mean(prices[:period])
    for i in range(period, n):
        smma = (smma * (period - 1) + prices[i]) / period

    return smma

def init(context):
    context.security = '000300.XSHG'
    context.jaw_period = 13   # 颚线（蓝线）
    context.teeth_period = 8  # 齿线（红线）
    context.lips_period = 5   # 嘴线（绿线）
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security

    # 获取历史收盘价（需要足够长的数据）
    prices = history_bars(security, 50, '1d', 'close')
    if prices is None or len(prices) < 40:
        return

    closes = np.array(prices)

    # 计算三条鳄鱼线（需要前移8根K线）
    # 颚线前移8根，齿线前移5根，嘴线前移3根
    jaw = smoothed_ma(closes[:-8], context.jaw_period)  # 颚线
    teeth = smoothed_ma(closes[:-5], context.teeth_period)  # 齿线
    lips = smoothed_ma(closes[:-3], context.lips_period)  # 嘴线

    if jaw is None or teeth is None or lips is None:
        return

    current_close = closes[-1]

    # 鳄鱼线状态判断
    # 睡眠期：三条线纠缠在一起
    # 唤醒期：嘴线在上，齿线在中，颚线在下（多头排列）
    # 进食期：价格在嘴线之上，持续上涨
    # 疲倦期：嘴线在下，齿线在中，颚线在上（空头排列）

    # 交易逻辑
    # 多头排列 + 价格突破嘴线 → 买入
    # 空头排列 + 价格跌破嘴线 → 卖出

    bullish = lips > teeth > jaw  # 多头排列
    bearish = lips < teeth < jaw  # 空头排列

    # 前一日状态
    prev_prices = closes[:-1]
    prev_jaw = smoothed_ma(prev_prices[:-8], context.jaw_period)
    prev_teeth = smoothed_ma(prev_prices[:-5], context.teeth_period)
    prev_lips = smoothed_ma(prev_prices[:-3], context.lips_period)

    if prev_jaw and prev_teeth and prev_lips:
        prev_bullish = prev_lips > prev_teeth > prev_jaw

        # 突破买入：从睡眠/空头转为多头排列
        if bullish and not prev_bullish and not context.pos:
            order_value(security, context.portfolio.total_value * 0.95)
            context.pos = True
            print(f"买入鳄鱼唤醒: lips={lips:.2f}, teeth={teeth:.2f}, jaw={jaw:.2f}")

        # 跌破卖出：多头排列转为空头排列
        if bearish and context.pos:
            order_to(security, 0)
            context.pos = False
            print(f"卖出鳄鱼疲倦: lips={lips:.2f}, teeth={teeth:.2f}, jaw={jaw:.2f}")