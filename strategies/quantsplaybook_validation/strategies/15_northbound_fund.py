# 北向资金择时策略 - RiceQuant版本
# 来源：《安信证券-北向资金交易能力一定强吗》
# 跟踪北向资金流向进行择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    # 获取历史收盘价
    prices = history_bars(security, period + 10, '1d', 'close')
    if prices is None or len(prices) < period:
        return

    closes = np.array(prices)

    # 由于RiceQuant无法直接获取北向资金数据，使用替代方案
    # 使用市场强度作为替代指标

    returns = np.diff(closes) / closes[:-1]

    # 计算市场强度（上涨天数占比）
    positive_days = np.sum(returns[-period:] > 0)
    market_strength = positive_days / period

    # 计算强度变化
    prev_positive_days = np.sum(returns[-period-5:-5] > 0)
    prev_strength = prev_positive_days / period

    strength_change = market_strength - prev_strength

    # 交易逻辑
    # 强度上升 + 强度高于阈值 → 买入
    # 强度下降 + 强度低于阈值 → 卖出

    if market_strength > 0.55 and strength_change > 0.05 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: strength={market_strength:.2f}, change={strength_change:.2f}")
    elif market_strength < 0.45 and strength_change < -0.05 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: strength={market_strength:.2f}, change={strength_change:.2f}")