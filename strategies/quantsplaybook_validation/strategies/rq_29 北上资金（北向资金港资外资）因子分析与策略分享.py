# 原文链接：https://www.joinquant.com/post/45430
# 策略：北上资金（北向资金港资外资）因子分析与策略分享
# 作者：北向资金研究员
# 核心逻辑：选沪深港通标的中基本面优质（高ROE低PE）的股票，月度调仓
# 注：原版用jqfactor+finance.STK_HK_CONNECT_DAILY，此处改为用沪深港通标的+基本面因子

import numpy as np


def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：沪深港通标的中高ROE低PE的股票"""
    # 沪深300成分股（多为沪深港通标的，外资重仓）
    stocks_300 = index_components('000300.XSHG')
    # 中证500成分股（部分为港股通标的）
    stocks_500 = index_components('000905.XSHG')
    universe = list(set(stocks_300) | set(stocks_500))
    universe = [s for s in universe if not s.startswith('688')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks_300,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 30.0]
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 5.0]
    df = df[df['roe'] > 0.1]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        logger.info("[北向资金] 无数据")
        return

    # 综合评分：高ROE + 低PE
    df = df.dropna()
    if len(df) < 5:
        return

    roe_rank = np.argsort(np.argsort(-df['roe'].values))
    pe_rank  = np.argsort(np.argsort(df['pe_ratio'].values))
    score = roe_rank + pe_rank
    df = df.copy()
    df['score'] = score
    df_sorted = df.sort_values('score')

    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[北向资金] 选股={context.stock_pool}")

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
