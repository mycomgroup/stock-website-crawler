# RSRS择时策略（优化版）- RiceQuant版本
# 来源：《光大证券-基于阻力支撑相对强度（RSRS）的市场择时》
# 已验证策略，作为基准对比

import numpy as np
import statsmodels.api as sm

def init(context):
    context.security = '000300.XSHG'
    context.N = 18
    context.M = 300
    context.buy_threshold = 0.8
    context.sell_threshold = -0.8
    context.beta_history = []
    context.r2_history = []
    context.pos = False

def handle_bar(context, bar_dict):
    security = context.security
    N = context.N
    M = context.M

    # 获取历史数据
    lookback = M + N + 50
    prices = history_bars(security, lookback, '1d', ['high', 'low', 'close'])
    if prices is None or len(prices) < M:
        return

    # 初始化历史数据
    if len(context.beta_history) < M:
        for i in range(N, min(len(prices) - 1, M + N)):
            highs = prices['high'][i-N:i]
            lows = prices['low'][i-N:i]
            X = sm.add_constant(lows)
            try:
                model = sm.OLS(highs, X).fit()
                context.beta_history.append(model.params[1])
                context.r2_history.append(model.rsquared)
            except:
                continue
        if len(context.beta_history) < M:
            return
    else:
        # 正常更新
        highs = prices['high'][-N:]
        lows = prices['low'][-N:]
        X = sm.add_constant(lows)
        try:
            model = sm.OLS(highs, X).fit()
            context.beta_history.append(model.params[1])
            context.r2_history.append(model.rsquared)
        except:
            return

    # 保持长度
    if len(context.beta_history) > M:
        context.beta_history = context.beta_history[-M:]
        context.r2_history = context.r2_history[-M:]

    # 计算标准分
    beta_arr = np.array(context.beta_history)
    mu, sigma = np.mean(beta_arr), np.std(beta_arr)
    if sigma == 0:
        return

    zscore = (beta_arr[-1] - mu) / sigma
    beta = beta_arr[-1]
    r2 = context.r2_history[-1] if context.r2_history else 0.5

    # 右偏标准分
    rsrs = zscore * beta * r2

    # 交易逻辑
    if rsrs > context.buy_threshold and not context.pos:
        order_value(security, context.portfolio.starting_cash * 0.95)
        context.pos = True
        print(f"买入: RSRS={rsrs:.3f}")
    elif rsrs < context.sell_threshold and context.pos:
        order_to(security, 0)
        context.pos = False
        print(f"卖出: RSRS={rsrs:.3f}")