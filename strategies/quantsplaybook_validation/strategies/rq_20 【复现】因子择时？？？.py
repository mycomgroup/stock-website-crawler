# 原文链接：https://www.joinquant.com/post/44650
# 策略：【复现】因子择时？？？
# 作者：复现系列
# 核心逻辑：用沪深300动量信号择时，在场时持有小市值股票
# 注：原版用sklearn SVM/RF做因子择时，此处改为简单动量择时

import numpy as np


def init(context):
    context.index = '000300.XSHG'
    context.n_stocks = 10
    context.stock_pool = []
    context.in_market = False
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_daily(timing, time_rule=market_open(minute=15))


def handle_bar(context, bar_dict):
    pass


def select_stocks(context, bar_dict):
    """月度选股：小市值"""
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(context.n_stocks + 5)
    candidates = df.index.tolist()
    if df is not None and len(df) > 0:
        context.stock_pool = list(df.index)[:context.n_stocks]
    logger.info(f"[因子择时] 股票池={context.stock_pool}")


def timing(context, bar_dict):
    """日度择时：沪深300动量"""
    prices = history_bars(context.index, 60, '1d', 'close')
    if prices is None or len(prices) < 60:
        return

    p = np.array(prices, dtype=float)
    # 动量信号：20日均线 > 60日均线 且 近5日上涨
    ma20 = np.mean(p[-20:])
    ma60 = np.mean(p[-60:])
    momentum_5d = p[-1] / p[-6] - 1

    signal_up = (ma20 > ma60) and (momentum_5d > 0)

    if signal_up and not context.in_market:
        # 入场
        context.in_market = True
        n = len(context.stock_pool)
        if n == 0:
            return
        value = context.portfolio.total_value * 0.95 / n
        for s in context.stock_pool:
            if s in bar_dict and bar_dict[s].is_trading:
                order_target_value(s, value)
        logger.info("[因子择时] 入场信号，买入小市值")

    elif not signal_up and context.in_market:
        # 出场
        context.in_market = False
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        logger.info("[因子择时] 出场信号，清仓")
