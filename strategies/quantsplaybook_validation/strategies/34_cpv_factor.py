# 高频价量相关性（CPV）因子选股策略 - RiceQuant版本
# 来源：《高频价量相关性，意想不到的选股因子》
# 核心逻辑：日线版本的价量相关性因子
#           CPV均值越小（量价背离）→ 股票被高估，未来收益低
# 修复：
#   1. 月度调仓失败时不更新 month，下个 bar 重试
#   2. 加强数据校验

import numpy as np


def calc_cpv_daily(prices, volumes, window=20):
    """日线价量相关性因子"""
    p = np.array(prices[-(window + 1):], dtype=float)
    v = np.array(volumes[-(window + 1):], dtype=float)

    price_ret = np.diff(p) / (p[:-1] + 1e-10)
    vol_ret = np.diff(v) / (v[:-1] + 1e-10)

    if np.std(price_ret) == 0 or np.std(vol_ret) == 0:
        return None, None

    corr_mean = np.corrcoef(price_ret, vol_ret)[0, 1]

    # 滚动5日相关系数的标准差
    roll_corrs = []
    sub = 5
    for i in range(window - sub + 1):
        pr = price_ret[i:i + sub]
        vr = vol_ret[i:i + sub]
        if np.std(pr) > 0 and np.std(vr) > 0:
            roll_corrs.append(np.corrcoef(pr, vr)[0, 1])

    corr_std = np.std(roll_corrs) if len(roll_corrs) >= 3 else 0.0
    return corr_mean, corr_std


def init(context):
    context.index = '000300.XSHG'
    context.window = 20
    context.top_n = 30
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    stocks = index_components(context.index)
    if not stocks or len(stocks) < 10:
        return  # 不更新 month，重试

    scores_mean = {}
    scores_std = {}

    for stock in stocks:
        try:
            prices = history_bars(stock, context.window + 2, '1d', 'close')
            volumes = history_bars(stock, context.window + 2, '1d', 'volume')
            if prices is None or volumes is None:
                continue
            if len(prices) < context.window + 1 or len(volumes) < context.window + 1:
                continue

            cm, cs = calc_cpv_daily(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                context.window
            )
            if cm is not None:
                scores_mean[stock] = cm
                scores_std[stock] = cs
        except Exception:
            continue

    all_stocks = list(scores_mean.keys())
    if len(all_stocks) < 5:
        return  # 不更新 month，重试

    context.month = current_month

    mean_vals = np.array([scores_mean[s] for s in all_stocks])
    std_vals = np.array([scores_std[s] for s in all_stocks])

    def zscore(arr):
        s = np.std(arr)
        return (arr - np.mean(arr)) / s if s > 0 else np.zeros_like(arr)

    combined = -zscore(mean_vals) - zscore(std_vals)
    final_scores = {all_stocks[i]: combined[i] for i in range(len(all_stocks))}

    target = sorted(final_scores, key=final_scores.get, reverse=True)[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
