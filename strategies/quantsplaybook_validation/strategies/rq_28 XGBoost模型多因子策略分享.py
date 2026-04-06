# 原文链接：https://www.joinquant.com/post/45370
# 策略：XGBoost模型多因子策略分享
# 作者：XGBoost量化
# 核心逻辑：用市值、PE、ROE、动量多因子等权打分选股（替代XGBoost）
# 注：原版用XGBoost机器学习，此处改为多因子评分替代

import numpy as np


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
    """月度再平衡：多因子等权打分（XGBoost替代）"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['pe_ratio', 'market_cap', 'roe', 'inc_revenue_year_on_year'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 80.0]
    df = df[df['roe'] > 0.0]
    df = df.head(500)
    candidates = df.index.tolist()
    if df is None or len(df) < 10:
        return

    df = df.dropna()

    # 计算动量因子
    momentum_dict = {}
    for s in list(df.index)[:200]:
        prices = history_bars(s, 21, '1d', 'close')
        if prices is None or len(prices) < 20:
            continue
        p = np.array(prices, dtype=float)
        momentum_dict[s] = p[-1] / p[0] - 1

    common = [s for s in df.index if s in momentum_dict]
    if len(common) < 10:
        common = list(df.index)
        for s in common:
            if s not in momentum_dict:
                momentum_dict[s] = 0.0

    sub_df = df.loc[common].copy()

    # 四因子等权打分
    score_cap = 1 - rank_normalize(sub_df['market_cap'].values)
    score_pe  = 1 - rank_normalize(sub_df['pe_ratio'].values)
    score_roe = rank_normalize(sub_df['roe'].values)
    mom_vals  = np.array([momentum_dict.get(s, 0) for s in common])
    score_mom = rank_normalize(mom_vals)

    total = (score_cap + score_pe + score_roe + score_mom) / 4.0
    sub_df['score'] = total
    df_sorted = sub_df.sort_values('score', ascending=False)

    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[XGBoost替代] 选股={context.stock_pool}")

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
