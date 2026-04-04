# 时变夏普择时策略 - RiceQuant版本
# 来源：《国信证券-时变夏普率的择时策略》

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.lookback = 20  # 月度数据换算为日线约20天
    context.buy_threshold = 0.3
    context.sell_threshold = -0.3
    context.pos = False

def calc_tsharpe(daily_rets, rf=0.03/252):
    """计算时变夏普比率"""
    excess_ret = np.mean(daily_rets) - rf
    volatility = np.std(daily_rets)
    if volatility == 0:
        return 0
    return excess_ret / volatility * np.sqrt(252)  # 年化

def handle_bar(context, bar_dict):
    security = context.security
    lookback = context.lookback * 20  # 约20个交易日为一个月

    # 获取历史数据
    prices = history_bars(security, lookback + 20, '1d', 'close')
    if prices is None or len(prices) < lookback:
        return

    # 计算日收益率
    daily_rets = np.diff(prices[-lookback:]) / prices[-lookback:-1]

    # 计算时变夏普
    tsharpe = calc_tsharpe(daily_rets)

    # 交易逻辑
    if tsharpe > context.buy_threshold and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: TSharpe={tsharpe:.3f}")
    elif tsharpe < context.sell_threshold and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: TSharpe={tsharpe:.3f}")