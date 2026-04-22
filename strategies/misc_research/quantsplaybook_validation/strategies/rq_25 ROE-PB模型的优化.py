# 原文链接：https://www.joinquant.com/post/45100
# 策略：ROE-PB模型的优化
# 作者：ROE-PB研究员
# 核心逻辑：ROE/PB比值排序选股（高ROE低PB），月度调仓
# 注：原版用jqfactor，此处改为get_fundamentals

import numpy as np


def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：ROE/PB比值选股"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['pb_ratio', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pb_ratio'] > 0.5]
    df = df[df['pb_ratio'] < 10.0]
    df = df[df['roe'] > 0.05]
    df = df.head(500)
    candidates = df.index.tolist()
    if df is None or len(df) < 10:
        logger.info("[ROE-PB] 数据不足")
        return

    df = df.dropna()

    # ROE/PB 比值：越高越好（高ROE低PB）
    df['roe_pb_ratio'] = df['roe'] / df['pb_ratio']
    df_sorted = df.sort_values('roe_pb_ratio', ascending=False)

    context.stock_pool = list(df_sorted.index)[:context.n_stocks]
    logger.info(f"[ROE-PB] 选股={context.stock_pool} ROE/PB={list(df_sorted['roe_pb_ratio'].head(context.n_stocks).round(2))}")

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
