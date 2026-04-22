# 原文链接：https://www.joinquant.com/post/45160
# 策略：【深度解析 六】高股息率-低PEG-低股价-市值序列模型
# 作者：深度解析系列
# 核心逻辑：高股息率+低PEG+低股价多因子选股，月度调仓
# 注：原版用finance.STK_FINANCE_INCOME，此处改为用get_fundamentals股息率

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
    """月度再平衡：高股息率+低PEG+低股价"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe', 'inc_revenue_year_on_year'],
    )
    if factor_df is None or factor_df.empty:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 50.0]
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['roe'] > 0.05]
    df = df[df['inc_revenue_year_on_year'] > 0.0]
    df = df.head(500)
    if len(df) < 10:
        return

    # 股息率代理：ROE/PE（高ROE低PE → 高股息率）
    df = df.copy()
    df['div_proxy'] = df['roe'] / df['pe_ratio']

    # PEG = PE / 营收增长率（越低越好）
    df['peg_ratio'] = df['pe_ratio'] / (df['inc_revenue_year_on_year'] + 1e-9)
    df = df[df['peg_ratio'] > 0]

    if len(df) < 5:
        return

    # 多因子评分
    score_div = rank_normalize(df['div_proxy'].values)          # 高股息率：越高越好
    score_peg = 1 - rank_normalize(df['peg_ratio'].values)      # 低PEG：越低越好
    score_cap = 1 - rank_normalize(df['market_cap'].values)     # 低市值：越小越好

    total = (score_div * 0.4 + score_peg * 0.4 + score_cap * 0.2)
    df['score'] = total
    df_sorted = df.sort_values('score', ascending=False)

    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[高股息低PEG] 选股={context.stock_pool}")

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
