# 原文链接：https://www.joinquant.com/post/45190
# 策略：稳定高回报周期股策略2
# 作者：周期股研究员
# 核心逻辑：选ROE稳定且高的周期股，季度调仓
# 注：原版用finance.STK_FINANCE_INCOME，此处改为用get_fundamentals

import numpy as np


# 周期行业代表性股票（能源、材料、工业）
# 用中证500成分股中高ROE的股票作为周期股代理
def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    # 季度调仓：每季度第一个交易日
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    context.quarter_count = 0


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """季度再平衡（每3个月执行一次）"""
    context.quarter_count += 1
    if context.quarter_count % 3 != 1:
        return  # 只在季度第一个月执行

    stocks_500 = index_components('000905.XSHG')
    stocks_500 = [s for s in stocks_500 if not s.startswith('688')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks_500,
        ['pb_ratio', 'market_cap', 'roe', 'inc_revenue_year_on_year'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 5.0]
    df = df[df['roe'] > 0.12]
    df = df[df['inc_revenue_year_on_year'] > 0.05]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        logger.info("[周期股] 无数据")
        return

    context.stock_pool = list(df.index)[:context.n_stocks]
    logger.info(f"[周期股] 季度调仓 选股={context.stock_pool}")

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
