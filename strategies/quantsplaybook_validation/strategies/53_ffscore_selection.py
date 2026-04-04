# 华泰FFScore选股策略 - RiceQuant版本
# 来源：《华泰FFScore》（比乔斯基FScore改进版）
# 核心逻辑：9个财务指标打分，选低PB+高质量股票
# RiceQuant版本：用量价代理指标实现，因RiceQuant不支持JQ的fundamentals API
# 代理逻辑：低波动+上涨趋势+成交量放大 ≈ 盈利质量好的低估值股

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.lookback = 60
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

            # FScore代理指标1：ROA代理 - 近期收益率为正（盈利）
            roa_proxy = 1 if returns[-20:].mean() > 0 else 0

            # FScore代理指标2：CFO代理 - 成交量趋势向上（资金流入）
            vol_trend = np.polyfit(np.arange(context.lookback), volumes, 1)[0]
            cfo_proxy = 1 if vol_trend > 0 else 0

            # FScore代理指标3：ΔROA - 收益率改善
            recent_ret = returns[-20:].mean()
            early_ret = returns[:20].mean()
            delta_roa = 1 if recent_ret > early_ret else 0

            # FScore代理指标4：低波动（财务稳定性）
            vol_stability = 1 if np.std(returns) < np.std(returns[-20:]) * 1.5 else 0

            # FScore代理指标5：价格趋势（长期上涨 = 市场认可）
            price_trend = 1 if prices[-1] > prices[-context.lookback] else 0

            # 综合得分（0-5分）
            fscore = roa_proxy + cfo_proxy + delta_roa + vol_stability + price_trend

            # 额外：低波动率加分（类似低PB）
            low_vol_bonus = -np.std(returns) * 10  # 波动率越低得分越高

            scores[stock] = fscore + low_vol_bonus
        except Exception:
            continue

    if not scores:
        return

    sorted_stocks = sorted(scores, key=scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
