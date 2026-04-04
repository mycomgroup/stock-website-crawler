# 投资者情绪指数择时策略 - RiceQuant版本
# 来源：《国信证券-投资者情绪指数择时模型》

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    prices = history_bars(security, period + 30, '1d', ['close', 'volume'])
    if prices is None or len(prices) < period + 10:
        return

    closes = np.array(prices['close'])
    volumes = np.array(prices['volume'])

    # 构建简化的情绪指数
    # 情绪 = 收益率 * 成交量变化

    returns = np.diff(closes) / closes[:-1]
    vol_changes = np.diff(volumes) / volumes[:-1]
    vol_changes = np.nan_to_num(vol_changes)

    # 情绪指数
    sentiment = returns[-period:] * vol_changes[-period:]
    sentiment_index = np.mean(sentiment)

    # 情绪指数标准化
    sentiment_history = []
    for i in range(period, len(returns)):
        s = returns[i-period:i] * vol_changes[i-period:i]
        sentiment_history.append(np.mean(s))

    if sentiment_history:
        mean_sent = np.mean(sentiment_history)
        std_sent = np.std(sentiment_history)
        if std_sent > 0:
            sentiment_z = (sentiment_index - mean_sent) / std_sent
        else:
            sentiment_z = 0
    else:
        sentiment_z = 0

    # 交易逻辑
    # 情绪高涨(z > 1) → 卖出（反向指标）
    # 情绪低迷(z < -1) → 买入

    if sentiment_z < -1.0 and not context.pos:
        order_value(security, context.portfolio.total_value * 0.95)
        context.pos = True
        print(f"买入: sentiment_z={sentiment_z:.2f}")
    elif sentiment_z > 1.0 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: sentiment_z={sentiment_z:.2f}")