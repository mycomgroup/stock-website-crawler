# 原文链接：https://www.joinquant.com/post/45220
# 策略：近几年一直有效的股票BOLL择时策略
# 作者：BOLL择时达人
# 核心逻辑：小市值+低PE选股，用BOLL带择时买卖
# 注：原版用jqfactor+jqlib_ta，此处改为本地BOLL实现

import numpy as np


def calc_boll(prices, n=20, k=2):
    """计算布林带"""
    if len(prices) < n:
        return None, None, None
    p = np.array(prices[-n:], dtype=float)
    ma  = np.mean(p)
    std = np.std(p)
    upper = ma + k * std
    lower = ma - k * std
    return upper, ma, lower


def init(context):
    context.n_stocks = 8
    context.stock_pool = []
    context.boll_n = 20
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_daily(boll_trade, time_rule=market_open(minute=20))


def handle_bar(context, bar_dict):
    pass


def select_stocks(context, bar_dict):
    """月度选股：小市值+低PE"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['pe_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 40.0]
    df = df.head(50)
    candidates = df.index.tolist()
    if df is not None and len(df) > 0:
        df_sorted = df.sort_values('pe_ratio')
        context.stock_pool = list(df_sorted.index)[:context.n_stocks * 2]
    logger.info(f"[BOLL择时] 股票池={len(context.stock_pool)}")


def boll_trade(context, bar_dict):
    """日度BOLL择时"""
    for s in list(context.portfolio.positions.keys()):
        prices = history_bars(s, context.boll_n + 5, '1d', 'close')
        if prices is None or len(prices) < context.boll_n:
            continue
        upper, mid, lower = calc_boll(prices, context.boll_n)
        if upper is None:
            continue
        current = prices[-1]
        # 跌破中轨卖出
        if current < mid:
            order_target_value(s, 0)
            logger.info(f"[BOLL择时] 跌破中轨，卖出 {s}")

    # 买入：价格在下轨附近反弹（触及下轨后回升）
    for s in context.stock_pool:
        if s in context.portfolio.positions:
            continue
        prices = history_bars(s, context.boll_n + 5, '1d', 'close')
        if prices is None or len(prices) < context.boll_n:
            continue
        upper, mid, lower = calc_boll(prices, context.boll_n)
        if upper is None:
            continue
        # 昨日触及下轨，今日回升
        if prices[-2] <= lower and prices[-1] > lower:
            if s in bar_dict and bar_dict[s].is_trading:
                n = max(len(context.portfolio.positions), 1)
                value = context.portfolio.total_value * 0.95 / context.n_stocks
                order_target_value(s, value)
                logger.info(f"[BOLL择时] 下轨反弹，买入 {s}")
