# 原文链接：https://www.joinquant.com/post/44620
# 策略：机器学习线性回归小市值
# 作者：量化学习者
# 核心逻辑：小市值+高ROE选股，每月调仓
# 注：原版用jqfactor+sklearn线性回归，此处改为直接用市值+ROE因子选股

import numpy as np


def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    # 获取全市场A股
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]

    # 用市值升序+ROE降序选股（小市值高ROE）
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df[df['roe'] > 0.0]
    df = df.head(200)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        logger.info("[小市值线性回归] 无数据")
        return

    # 在小市值200只中按ROE降序选前N只
    df_sorted = df.sort_values('roe', ascending=False)
    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[小市值线性回归] 选股={context.stock_pool}")

    # 卖出不在池中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    # 等权买入
    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
