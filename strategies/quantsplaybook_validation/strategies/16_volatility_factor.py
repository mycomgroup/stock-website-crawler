# 波动率因子择时策略 - RiceQuant版本
# 使用波动率因子进行市场择时

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.vol_period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    vol_period = context.vol_period

    prices = history_bars(security, vol_period + 30, '1d', 'close')
    if prices is None or len(prices) < vol_period + 10:
        return

    closes = np.array(prices)
    returns = np.diff(closes) / closes[:-1]

    # 计算已实现波动率
    realized_vol = np.std(returns[-vol_period:]) * np.sqrt(252)

    # 计算波动率的历史分位数
    vol_history = []
    for i in range(vol_period, len(returns)):
        vol_history.append(np.std(returns[i-vol_period:i]) * np.sqrt(252))

    vol_percentile = np.mean(realized_vol > np.array(vol_history))

    # 计算波动率变化率
    prev_vol = np.std(returns[-vol_period-5:-5]) * np.sqrt(252)
    vol_change = (realized_vol - prev_vol) / prev_vol if prev_vol > 0 else 0

    # 交易逻辑
    # 低波动率环境 + 波动率上升 → 买入
    # 高波动率环境 → 卖出

    if vol_percentile < 0.3 and vol_change > 0 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: vol={realized_vol:.2f}, pct={vol_percentile:.2f}")
    elif vol_percentile > 0.7 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: vol={realized_vol:.2f}, pct={vol_percentile:.2f}")