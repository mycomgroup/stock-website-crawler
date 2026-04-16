# 趋势筛选后相关性最小ETF轮动加速版 - RiceQuant版本
# 逻辑：先用趋势过滤（MA20>MA60），再选相关性最小的ETF组合

import numpy as np


def init(context):
    context.etf_pool = [
        '510300.XSHG', '159915.XSHE', '510500.XSHG',
        '518880.XSHG', '511010.XSHG', '513100.XSHG',
        '159928.XSHE', '510050.XSHG',
    ]
    context.top_n = 3
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    # 趋势过滤：MA20>MA60
    trend_etfs = []
    returns_dict = {}
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, 65, '1d', 'close')
            if closes is None or len(closes) < 65:
                continue
            closes = np.array(closes, dtype=float)
            ma20 = np.mean(closes[-20:])
            ma60 = np.mean(closes[-60:])
            if ma20 <= ma60:
                continue
            trend_etfs.append(etf)
            returns = np.diff(closes[-21:]) / closes[-21:-1]
            returns_dict[etf] = returns
            scores[etf] = closes[-1] / closes[-20] - 1
        except Exception:
            continue

    if not trend_etfs:
        for etf in list(context.portfolio.positions.keys()):
            order_target_value(etf, 0)
        return

    # 从趋势ETF中选相关性最小的组合
    if len(trend_etfs) <= context.top_n:
        target = trend_etfs
    else:
        # 贪心选择：每次选与已选ETF相关性最小的
        target = [max(scores, key=scores.get)]  # 先选动量最强的
        while len(target) < context.top_n and len(target) < len(trend_etfs):
            min_avg_corr = float('inf')
            best_next = None
            for etf in trend_etfs:
                if etf in target:
                    continue
                if etf not in returns_dict:
                    continue
                avg_corr = 0
                count = 0
                for selected in target:
                    if selected in returns_dict:
                        r1 = returns_dict[etf]
                        r2 = returns_dict[selected]
                        if len(r1) == len(r2):
                            avg_corr += abs(np.corrcoef(r1, r2)[0, 1])
                            count += 1
                if count > 0:
                    avg_corr /= count
                    if avg_corr < min_avg_corr:
                        min_avg_corr = avg_corr
                        best_next = etf
            if best_next:
                target.append(best_next)
            else:
                break

    context.month = current_month
    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for etf in target:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is None or bar.is_trading:
            order_target_value(etf, context.portfolio.total_value * weight * 0.95)
