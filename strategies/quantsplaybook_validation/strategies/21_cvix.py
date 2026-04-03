# C-VIX中国版VIX择时策略 - RiceQuant版本
# 来源：《国信证券-衍生品应用与产品设计系列之VIX介绍》
# 简化版：使用已实现波动率近似VIX

import numpy as np

def init(context):
    context.security = '000300.XSHG'
    context.period = 20
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    period = context.period

    prices = history_bars(security, period + 60, '1d', ['close', 'high', 'low'])
    if prices is None or len(prices) < period + 30:
        return

    closes = np.array(prices['close'])
    highs = np.array(prices['high'])
    lows = np.array(prices['low'])

    # Parkinson波动率（使用高低价）
    hl_ratio = np.log(highs / lows)
    parkinson_vol = np.sqrt(np.mean(hl_ratio[-period:] ** 2) / (4 * np.log(2))) * np.sqrt(252)

    # 已实现波动率
    returns = np.diff(closes) / closes[:-1]
    realized_vol = np.std(returns[-period:]) * np.sqrt(252)

    # 综合波动率（类似VIX）
    cvix = (parkinson_vol + realized_vol) / 2

    # 波动率的历史分位数
    cvix_history = []
    for i in range(period, len(returns)):
        r = returns[i-period:i]
        rv = np.std(r) * np.sqrt(252)
        hl = np.log(highs[i-period:i] / lows[i-period:i])
        pv = np.sqrt(np.mean(hl ** 2) / (4 * np.log(2))) * np.sqrt(252)
        cvix_history.append((pv + rv) / 2)

    cvix_percentile = np.mean(cvix > np.array(cvix_history)) if cvix_history else 0.5

    # VIX期限结构（简化）
    short_vol = np.std(returns[-5:]) * np.sqrt(252)
    long_vol = np.std(returns[-60:]) * np.sqrt(252)
    term_structure = short_vol / long_vol if long_vol > 0 else 1

    # 交易逻辑
    # 高VIX分位 + 期限结构倒挂 → 恐慌底部，买入
    # 低VIX分位 → 市场平静

    if cvix_percentile > 0.8 and term_structure > 1.2 and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入恐慌: CVIX={cvix:.2f}, term={term_structure:.2f}")
    elif cvix_percentile < 0.3 and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出平静: CVIX={cvix:.2f}")