# 原文链接：https://www.joinquant.com/post/45040
# 策略：多因子线性回归组合策略
# 作者：多因子研究员
# 核心逻辑：ARBR动量+市值+ROE多因子线性组合选股，月度调仓
# 注：原版用jqfactor，此处改为用get_fundamentals多因子

import numpy as np


def calc_arbr(highs, lows, opens, closes, n=26):
    """计算ARBR指标（人气指标+意愿指标）"""
    if len(highs) < n:
        return None, None
    h = np.array(highs[-n:], dtype=float)
    l = np.array(lows[-n:], dtype=float)
    o = np.array(opens[-n:], dtype=float)
    c = np.array(closes[-n:], dtype=float)

    # AR = sum(H-O) / sum(O-L) * 100
    ar_num = np.sum(h - o)
    ar_den = np.sum(o - l)
    ar = ar_num / (ar_den + 1e-9) * 100

    # BR = sum(max(H-prev_C,0)) / sum(max(prev_C-L,0)) * 100
    prev_c = c[:-1]
    br_num = np.sum(np.maximum(h[1:] - prev_c, 0))
    br_den = np.sum(np.maximum(prev_c - l[1:], 0))
    br = br_num / (br_den + 1e-9) * 100

    return ar, br


def rank_normalize(series):
    arr = np.array(series, dtype=float)
    ranks = np.argsort(np.argsort(arr))
    return ranks / (len(ranks) - 1 + 1e-9)


def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：多因子线性组合"""
    stocks_500 = index_components('000905.XSHG')  # 中证500
    stocks_500 = [s for s in stocks_500 if not s.startswith('688')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks_500,
        ['market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df[df['roe'] > 0.0]
    df = df.head(300)
    candidates = df.index.tolist()
    if df is None or len(df) < 10:
        return

    df = df.dropna()

    # 计算ARBR动量因子
    arbr_scores = {}
    for s in list(df.index)[:100]:  # 限制数量
        highs  = history_bars(s, 30, '1d', 'high')
        lows   = history_bars(s, 30, '1d', 'low')
        opens  = history_bars(s, 30, '1d', 'open')
        closes = history_bars(s, 30, '1d', 'close')
        if highs is None or len(highs) < 26:
            continue
        ar, br = calc_arbr(highs, lows, opens, closes)
        if ar is not None:
            arbr_scores[s] = (ar + br) / 2.0

    if not arbr_scores:
        # 无ARBR数据时直接用基本面
        df_sorted = df.sort_values('roe', ascending=False)
        context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    else:
        # 多因子综合评分
        common = [s for s in arbr_scores.keys() if s in df.index]
        if len(common) < 5:
            context.stock_pool = list(df.sort_values('roe', ascending=False).index)[:context.n_stocks]
        else:
            sub_df = df.loc[common]
            score_cap = 1 - rank_normalize(sub_df['market_cap'].values)
            score_roe = rank_normalize(sub_df['roe'].values)
            arbr_vals = np.array([arbr_scores[s] for s in common])
            score_arbr = rank_normalize(arbr_vals)
            total = (score_cap + score_roe + score_arbr) / 3.0
            sub_df = sub_df.copy()
            sub_df['score'] = total
            context.stock_pool = list(sub_df.sort_values('score', ascending=False).index)[:context.n_stocks]

    logger.info(f"[多因子线性] 选股={context.stock_pool}")

    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
