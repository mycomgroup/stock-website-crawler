# 原文链接：https://www.joinquant.com/post/45010
# 策略：低AH溢价选股
# 作者：AH溢价研究员
# 核心逻辑：选沪深港通标的中PB较低的股票（AH溢价低的代理），月度调仓
# 注：原版用finance.STK_AH_PRICE_COMP，此处改为用港股通标的+低PB代理

import numpy as np


# 沪股通标的（部分代表性股票，实际可扩展）
# 用沪深300成分股中低PB的股票作为AH溢价低的代理
def init(context):
    context.n_stocks = 10
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：沪深300中低PB股票（AH溢价低代理）"""
    # 沪深300成分股（多为AH两地上市或港股通标的）
    stocks = index_components('000300.XSHG')
    stocks = [s for s in stocks if not s.startswith('688')]

    # 选低PB股票（AH溢价低的代理：A股PB低说明相对港股溢价低）
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'pb_ratio', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 2.0]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 30.0]
    df = df[df['roe'] > 0.05]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        logger.info("[低AH溢价] 无数据")
        return

    context.stock_pool = list(df.index)[:context.n_stocks]
    logger.info(f"[低AH溢价] 选股={context.stock_pool}")

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
