# Trader-Company集成算法择时策略 - RiceQuant版本
# 来源：《浙商证券-Trader-Company集成算法交易策略》
# 结合多个简单交易规则

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.pos = False

def ma_signal(closes):
    """均线信号"""
    ma5 = np.mean(closes[-5:])
    ma20 = np.mean(closes[-20:])
    return 1 if ma5 > ma20 else -1

def momentum_signal(closes):
    """动量信号"""
    ret = (closes[-1] - closes[-20]) / closes[-20]
    return 1 if ret > 0 else -1

def volatility_signal(closes):
    """波动率信号"""
    if len(closes) < 45:
        return 0
    # 简化计算：使用标准差
    vol_short = np.std(closes[-20:])  # 短期波动
    vol_long = np.std(closes[-40:])   # 长期波动
    return 1 if vol_short < vol_long else -1  # 低波动偏好

def handle_bar(context, bar_dict):
    security = context.security

    prices = history_bars(security, 70, '1d', 'close')
    if prices is None or len(prices) < 65:
        return

    closes = np.array(prices)

    # 集成多个信号
    signals = []

    signals.append(ma_signal(closes))
    signals.append(momentum_signal(closes))
    signals.append(volatility_signal(closes))

    # 投票
    vote = np.sum(signals)

    # 交易逻辑
    # 多数信号看多 → 买入
    # 多数信号看空 → 卖出

    if vote >= 2 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: vote={vote}, signals={signals}")
    elif vote <= -2 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: vote={vote}, signals={signals}")