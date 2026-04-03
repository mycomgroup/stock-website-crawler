# 点位效率理论择时策略 - RiceQuant版本
# 来源：《兴业证券-基于点位效率理论的量化择时体系搭建》

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def calculate_efficiency(closes):
    """计算点位效率：实际位移/总路程"""
    if len(closes) < 2:
        return 0

    # 实际位移
    displacement = abs(closes[-1] - closes[0])

    # 总路程
    path = np.sum(np.abs(np.diff(closes)))

    if path == 0:
        return 0

    efficiency = displacement / path
    return efficiency

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    prices = history_bars(security, period + 20, '1d', 'close')
    if prices is None or len(prices) < period + 10:
        return

    closes = np.array(prices)

    # 计算效率
    efficiency = calculate_efficiency(closes[-period:])

    # 计算效率历史分位数
    eff_history = []
    for i in range(period, len(closes)):
        eff = calculate_efficiency(closes[i-period:i])
        eff_history.append(eff)

    eff_percentile = np.mean(efficiency > np.array(eff_history)) if eff_history else 0.5

    # 计算方向
    trend = 1 if closes[-1] > closes[-period] else -1

    # 交易逻辑
    # 高效率 + 上升趋势 → 买入
    # 高效率 + 下降趋势 → 卖出

    if efficiency > 0.5 and trend > 0 and eff_percentile > 0.6 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: eff={efficiency:.2f}, trend={trend}")
    elif (efficiency > 0.5 and trend < 0) or (eff_percentile < 0.3 and context.pos):
        order_to(security, 0)
        context.pos = False
        print(f"卖出: eff={efficiency:.2f}, trend={trend}")