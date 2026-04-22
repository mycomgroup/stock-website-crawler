# 原文链接：https://www.joinquant.com/post/44950
# 策略：wywy1995大神机器学习策略年化提升版
# 作者：wywy1995改进版
# 核心逻辑：用市值、PE、ROE、营收增长多因子打分，选高分小市值股票，月度调仓
# 注：原版用jqfactor+sklearn，此处改为多因子评分选股

import numpy as np


def rank_normalize(series):
    """排名归一化到[0,1]"""
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
    """月度再平衡：多因子评分选股"""
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
    df = df[df['pe_ratio'] < 100.0]
    df = df[df['roe'] > 0.0]
    df = df.head(500)
    candidates = df.index.tolist()
    if df is None or len(df) < 10:
        logger.info("[多因子ML] 数据不足")
        return

    df = df.dropna()
    if len(df) < 10:
        return

    # 因子打分（小市值+低PE+高ROE+高营收增长）
    # 市值：越小越好 → 反向排名
    score_cap = 1 - rank_normalize(df['market_cap'].values)
    # PE：越低越好 → 反向排名
    score_pe  = 1 - rank_normalize(df['pe_ratio'].values)
    # ROE：越高越好
    score_roe = rank_normalize(df['roe'].values)
    # 营收增长：越高越好
    rev_col = 'inc_revenue_year_on_year'
    if rev_col in df.columns:
        score_rev = rank_normalize(df[rev_col].values)
    else:
        score_rev = np.ones(len(df)) * 0.5

    # 等权综合评分
    total_score = (score_cap + score_pe + score_roe + score_rev) / 4.0
    df['score'] = total_score
    df_sorted = df.sort_values('score', ascending=False)

    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[多因子ML] 选股={context.stock_pool}")

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
