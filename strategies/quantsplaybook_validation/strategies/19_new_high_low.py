# 行业指数顶底信号择时策略 - RiceQuant版本
# 来源：《华福证券-行业指数顶部和底部信号》
# 使用净新高占比指标

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.lookback = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    lookback = context.lookback

    prices = history_bars(security, lookback + 50, '1d', 'close')
    if prices is None or len(prices) < lookback + 20:
        return

    closes = np.array(prices)

    # 净新高占比 NH-NL%
    # 计算创新高和创新低的数量

    highs = []
    lows = []

    for i in range(lookback, len(closes)):
        window = closes[i-lookback:i]
        if closes[i-1] >= np.max(window):  # 创新高
            highs.append(1)
        else:
            highs.append(0)

        if closes[i-1] <= np.min(window):  # 创新低
            lows.append(1)
        else:
            lows.append(0)

    # 净新高占比
    new_highs = np.sum(highs[-5:])  # 最近5天创新高数
    new_lows = np.sum(lows[-5:])    # 最近5天创新低数
    nh_nl = (new_highs - new_lows) / 5  # 净新高占比

    # 历史分位数
    nh_nl_history = []
    for i in range(5, len(highs)):
        nh = np.sum(highs[i-5:i])
        nl = np.sum(lows[i-5:i])
        nh_nl_history.append((nh - nl) / 5)

    percentile = np.mean(nh_nl > np.array(nh_nl_history)) if nh_nl_history else 0.5

    # 交易逻辑
    # 净新高占比高 → 市场强势
    # 净新低占比高 → 市场弱势

    if nh_nl > 0.4 and percentile > 0.7 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: NH-NL={nh_nl:.2f}, pct={percentile:.2f}")
    elif nh_nl < -0.4 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: NH-NL={nh_nl:.2f}, pct={percentile:.2f}")