# 手把手教你构建ETF策略候选池优化版 - RiceQuant版本
# 逻辑：从宽基+行业ETF中，用动量+波动率+相关性筛选最优ETF组合，月度调仓

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300
        '159915.XSHE',  # 创业板
        '510500.XSHG',  # 中证500
        '510050.XSHG',  # 上证50
        '518880.XSHG',  # 黄金
        '511010.XSHG',  # 国债
        '513100.XSHG',  # 纳指100
        '159928.XSHE',  # 消费
    ]
    context.top_n = 2
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    # 计算各ETF的动量得分
    scores = {}
    returns_dict = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 61, '1d', 'close')
            if closes is None or len(closes) < 61:
                continue
            closes = np.array(closes, dtype=float)
            momentum = closes[-1] / closes[0] - 1
            returns = np.diff(closes) / closes[:-1]
            vol = np.std(returns)
            # 只选趋势向上的ETF（价格在20日均线上方）
            ma20 = np.mean(closes[-20:])
            if closes[-1] < ma20:
                continue
            scores[etf] = momentum / (vol + 1e-10)
            returns_dict[etf] = returns
        except Exception:
            continue

    if not scores:
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        return

    context.month = current_month

    # 按得分排序，选top_n
    sorted_etfs = sorted(scores, key=scores.get, reverse=True)
    candidates = sorted_etfs[:min(4, len(sorted_etfs))]

    # 相关性过滤：从候选中选相关性最小的组合
    if len(candidates) >= 2 and len(returns_dict) >= 2:
        best_pair = candidates[:context.top_n]
        min_corr = float('inf')
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                e1, e2 = candidates[i], candidates[j]
                if e1 in returns_dict and e2 in returns_dict:
                    r1 = returns_dict[e1][-20:]
                    r2 = returns_dict[e2][-20:]
                    if len(r1) == len(r2):
                        corr = abs(np.corrcoef(r1, r2)[0, 1])
                        if corr < min_corr:
                            min_corr = corr
                            best_pair = [e1, e2]
        target = best_pair
    else:
        target = candidates[:context.top_n]

    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for etf in target:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is not None and bar.is_trading:
            order_target_value(etf, context.portfolio.total_value * weight * 0.95)
