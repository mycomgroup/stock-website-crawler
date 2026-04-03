# 双均线交叉+通道突破择时策略 - RiceQuant版本
# 来源：《申万宏源-均线交叉结合通道突破择时研究》
# 改进版：放宽交易条件

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.short_period = 5
    context.long_period = 20
    context.channel_period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security

    # 获取历史数据
    prices = history_bars(security, max(context.long_period, context.channel_period) + 10,
                          '1d', 'close')
    if prices is None or len(prices) < context.long_period:
        return

    closes = np.array(prices)

    # 计算均线
    short_ma = np.mean(closes[-context.short_period:])
    long_ma = np.mean(closes[-context.long_period:])
    prev_short_ma = np.mean(closes[-context.short_period-1:-1])
    prev_long_ma = np.mean(closes[-context.long_period-1:-1])

    # 计算通道 (使用收盘价代替高低价，因为RiceQuant数据结构可能不同)
    channel_high = np.max(closes[-context.channel_period:])
    channel_low = np.min(closes[-context.channel_period:])

    current_close = closes[-1]

    # 交易逻辑：放宽条件 - 均线金叉买入并需收盘价在长期均线之上
    # 金叉信号：短期均线上穿长期均线
    ma_cross_up = short_ma > long_ma and prev_short_ma <= prev_long_ma
    
    confirmed_up = ma_cross_up and current_close > long_ma

    if confirmed_up and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入金叉并且价格确认: 短MA={short_ma:.2f}, 长MA={long_ma:.2f}, Close={current_close:.2f}")
    # 死叉信号：短期均线下穿长期均线
    elif short_ma < long_ma and prev_short_ma >= prev_long_ma and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出死叉: 短MA={short_ma:.2f}, 长MA={long_ma:.2f}")