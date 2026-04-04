# 特征分布建模择时策略 - RiceQuant版本
# 来源：《华创证券-特征分布建模择时系列》

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    prices = history_bars(security, period + 40, '1d', 'close')
    if prices is None or len(prices) < period + 20:
        return

    closes = np.array(prices)
    returns = np.diff(closes) / closes[:-1]

    # 计算特征分布
    # 收益率分布特征：均值、标准差、偏度

    recent_returns = returns[-period:]
    mean_ret = np.mean(recent_returns)
    std_ret = np.std(recent_returns)

    if std_ret > 0:
        skewness = np.mean(((recent_returns - mean_ret) / std_ret) ** 3)
    else:
        skewness = 0

    # 分位数位置
    percentile_25 = np.percentile(recent_returns, 25)
    percentile_75 = np.percentile(recent_returns, 75)

    # 当前收益率在分布中的位置
    current_ret = returns[-1]
    position = (current_ret - percentile_25) / (percentile_75 - percentile_25) if percentile_75 != percentile_25 else 0.5

    # 极端位置判断
    is_extreme_low = position < 0.1 and skewness < -0.5
    is_extreme_high = position > 0.9 and skewness > 0.5

    # 历史极端位置频率
    extreme_history = []
    for i in range(period + 10, len(returns)):
        r = returns[i-period:i]
        p25 = np.percentile(r, 25)
        p75 = np.percentile(r, 75)
        pos = (r[-1] - p25) / (p75 - p25) if p75 != p25 else 0.5
        extreme_history.append(pos)

    extreme_pct = np.mean(position < np.percentile(extreme_history, 10))

    # 交易逻辑
    # 物极必反：极端低位买入，极端高位卖出

    if is_extreme_low and extreme_pct < 0.1 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: pos={position:.2f}, skew={skewness:.2f}")
    elif is_extreme_high and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: pos={position:.2f}, skew={skewness:.2f}")