# 罗伯·瑞克超额现金流选股策略 - RiceQuant版本
# 来源：《申万大师系列十三：罗伯·瑞克超额现金流选股法则》
# 5条选股标准（量价代理版本，因RiceQuant不支持JQ的fundamentals API）：
#   1. 低估值代理：价格相对历史低位（P/CF低代理）
#   2. 分红代理：长期持续上涨（稳定分红公司特征）
#   3. 低波动：财务稳健公司特征
#   4. 成交量稳定：机构持仓稳定（低负债率代理）
#   5. 现金流质量：近期成交量放大+价格上涨（经营现金流好代理）

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 120   # 约半年
    context.top_n = 20
    context.quarter = -1


def handle_bar(context, bar_dict):
    current_quarter = (context.now.month - 1) // 3
    if current_quarter == context.quarter:
        return
    context.quarter = current_quarter

    stocks = index_components(context.index)
    if not stocks:
        return

    scores = {}
    for stock in stocks:
        try:
            prices = history_bars(stock, context.lookback + 1, '1d', 'close')
            volumes = history_bars(stock, context.lookback, '1d', 'volume')
            if prices is None or len(prices) < context.lookback + 1:
                continue
            if volumes is None or len(volumes) < context.lookback:
                continue

            prices = np.array(prices, dtype=float)
            volumes = np.array(volumes, dtype=float)

            if prices[-1] == 0:
                continue

            returns = np.diff(prices) / prices[:-1]

            score = 0

            # 条件1：低估值代理 - 当前价格在过去半年的低分位（P/CF低）
            price_percentile = np.sum(prices[:-1] < prices[-1]) / len(prices[:-1])
            if price_percentile < 0.4:  # 价格在历史40%分位以下
                score += 2

            # 条件2：分红代理 - 长期趋势向上（稳定分红公司）
            long_trend = (prices[-1] / prices[0]) - 1
            if long_trend > 0:
                score += 2

            # 条件3：低波动（财务稳健）
            vol = np.std(returns)
            if vol < 0.025:  # 日波动率低于2.5%
                score += 2

            # 条件4：成交量稳定（机构持仓稳定）
            vol_cv = np.std(volumes) / (np.mean(volumes) + 1e-10)
            if vol_cv < 0.5:  # 成交量变异系数低
                score += 2

            # 条件5：现金流质量代理 - 近期量价共振
            recent_ret = returns[-20:].mean()
            recent_vol = volumes[-20:].mean()
            early_vol = volumes[:20].mean()
            if recent_ret > 0 and recent_vol > early_vol:
                score += 2

            scores[stock] = score
        except Exception:
            continue

    if not scores:
        return

    # 选得分最高的股票
    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
