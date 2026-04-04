# 单向波动差值择时策略 - RiceQuant版本
# 来源：《国信证券-市场波动率研究：基于相对强弱下单向波动差值应用》
# 利用上涨波动与下跌波动的差值进行择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20  # 波动计算周期
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史高低收盘价
    prices = history_bars(security, period + 5, '1d', ['open', 'high', 'low', 'close'])
    if prices is None or len(prices) < period:
        return

    opens = np.array(prices['open'])
    highs = np.array(prices['high'])
    lows = np.array(prices['low'])
    closes = np.array(prices['close'])

    # 计算单向波动
    # 上涨波动 = high - open (当日向上波动)
    # 下跌波动 = open - low (当日向下波动)

    up_volatilities = []
    down_volatilities = []

    for i in range(len(opens)):
        up_vol = (highs[i] - opens[i]) / opens[i]  # 上涨波动率
        down_vol = (opens[i] - lows[i]) / opens[i]  # 下跌波动率
        up_volatilities.append(up_vol)
        down_volatilities.append(down_vol)

    up_volatilities = np.array(up_volatilities)
    down_volatilities = np.array(down_volatilities)

    # 计算周期内平均波动
    avg_up_vol = np.mean(up_volatilities[-period:])
    avg_down_vol = np.mean(down_volatilities[-period:])

    # 波动差值指标
    vol_diff = avg_up_vol - avg_down_vol

    # 相对强弱 = (up - down) / (up + down)
    total_vol = avg_up_vol + avg_down_vol
    if total_vol > 0:
        relative_strength = (avg_up_vol - avg_down_vol) / total_vol
    else:
        relative_strength = 0

    # 计算历史相对强弱分位数
    rs_history = []
    for i in range(period, len(opens)):
        up_avg = np.mean(up_volatilities[i-period:i])
        down_avg = np.mean(down_volatilities[i-period:i])
        total = up_avg + down_avg
        if total > 0:
            rs_history.append((up_avg - down_avg) / total)

    rs_percentile = np.mean(relative_strength > np.array(rs_history)) if rs_history else 0.5

    # 交易逻辑
    # 相对强弱高分位(>0.7) → 上涨波动占优 → 买入
    # 相对强弱低分位(<0.3) → 下跌波动占优 → 卖出

    if rs_percentile > 0.7 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: RS={relative_strength:.3f}, percentile={rs_percentile:.2f}")
    elif rs_percentile < 0.3 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: RS={relative_strength:.3f}, percentile={rs_percentile:.2f}")