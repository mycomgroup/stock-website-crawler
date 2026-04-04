# 高频价量相关性（CPV）因子选股策略 - RiceQuant版本
# 来源：《高频价量相关性，意想不到的选股因子》
# 核心逻辑：原始论文用分钟级数据计算每日价量相关系数，再取20日均值/标准差
#           日线版本：用过去N日的日收益率与日成交量变化率的相关系数作为代理
#           CPV均值为负（量价背离）时，股票被高估，未来收益低；
#           CPV均值为正（量价共振）时，趋势确认，未来收益高
# 修复：原始实现基于分钟数据，改为日线版本的价量相关性

import numpy as np


def calc_cpv_daily(prices, volumes, window=20):
    """
    日线版本的价量相关性因子 CPV
    计算过去window日的日收益率与成交量变化率的相关系数
    """
    if len(prices) < window + 1 or len(volumes) < window + 1:
        return None, None

    p = np.array(prices[-(window+1):], dtype=float)
    v = np.array(volumes[-(window+1):], dtype=float)

    # 日收益率
    price_ret = np.diff(p) / (p[:-1] + 1e-10)
    # 成交量变化率
    vol_ret = np.diff(v) / (v[:-1] + 1e-10)

    if np.std(price_ret) == 0 or np.std(vol_ret) == 0:
        return None, None

    # 相关系数（均值因子）
    corr_mean = np.corrcoef(price_ret, vol_ret)[0, 1]

    # 波动性因子：用滚动5日相关系数的标准差
    roll_corrs = []
    sub_window = 5
    for i in range(window - sub_window + 1):
        pr = price_ret[i:i+sub_window]
        vr = vol_ret[i:i+sub_window]
        if np.std(pr) > 0 and np.std(vr) > 0:
            c = np.corrcoef(pr, vr)[0, 1]
            roll_corrs.append(c)

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
    context.month = current_month

    stocks = index_components(context.index)
    if not stocks:
        return

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

            corr_mean, corr_std = calc_cpv_daily(
                np.array(prices, dtype=float),
                np.array(volumes, dtype=float),
                context.window
            )
            if corr_mean is not None:
                scores_mean[stock] = corr_mean
                scores_std[stock] = corr_std
        except Exception:
            continue

    if not scores_mean:
        return

    # 横截面标准化后合并（参考原始论文：PV_corr = z(avg) + z(std)）
    # 均值因子：CPV均值越小越好（反转逻辑）
    # 波动性因子：CPV标准差越小越好（稳定的量价关系）
    all_stocks = list(scores_mean.keys())
    if len(all_stocks) < 5:
        return

    mean_vals = np.array([scores_mean[s] for s in all_stocks])
    std_vals = np.array([scores_std[s] for s in all_stocks])

    # z-score标准化
    def zscore(arr):
        s = np.std(arr)
        if s == 0:
            return np.zeros_like(arr)
        return (arr - np.mean(arr)) / s

    z_mean = zscore(mean_vals)
    z_std = zscore(std_vals)

    # 综合因子：均值越小越好（取负），波动越小越好（取负）
    combined = -z_mean - z_std

    final_scores = {all_stocks[i]: combined[i] for i in range(len(all_stocks))}

    sorted_stocks = sorted(final_scores, key=final_scores.get, reverse=True)
    target = sorted_stocks[:context.top_n]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_to(stock, 0)

    weight = 1.0 / len(target)
    total_value = context.portfolio.total_value
    for stock in target:
        order_target_value(stock, total_value * weight * 0.95)
