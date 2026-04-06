# 原文链接：https://www.joinquant.com/post/44980
# 策略：大盘择时，逻辑简单
# 作者：简单择时派
# 核心逻辑：用沪深300 MACD判断大盘趋势，趋势向上时持有小市值股票，否则空仓
# 注：原版用jqfactor+talib，此处改为本地MACD实现

import numpy as np


def ema(prices, n):
    k = 2.0 / (n + 1)
    e = prices[0]
    res = []
    for x in prices:
        e = x * k + e * (1 - k)
        res.append(e)
    return np.array(res)


def calc_macd(prices, fast=12, slow=26, signal=9):
    ema_f = ema(prices, fast)
    ema_s = ema(prices, slow)
    diff = ema_f - ema_s
    dea  = ema(diff, signal)
    hist = (diff - dea) * 2
    return diff, dea, hist


def init(context):
    context.index = '000300.XSHG'
    context.n_stocks = 10
    context.stock_pool = []
    context.in_market = False
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=5))
    scheduler.run_daily(timing_trade, time_rule=market_open(minute=20))


def handle_bar(context, bar_dict):
    pass


def select_stocks(context, bar_dict):
    """月度选小市值股票"""
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
    logger.info(f"[大盘择时] 股票池={context.stock_pool}")


def timing_trade(context, bar_dict):
    """日度MACD择时"""
    prices = history_bars(context.index, 60, '1d', 'close')
    if prices is None or len(prices) < 40:
        return

    p = np.array(prices, dtype=float)
    diff, dea, hist = calc_macd(p)

    # 入场：MACD金叉（diff上穿dea）
    signal_up   = diff[-1] > dea[-1] and diff[-2] <= dea[-2]
    # 出场：MACD死叉（diff下穿dea）
    signal_down = diff[-1] < dea[-1] and diff[-2] >= dea[-2]

    if signal_up and not context.in_market:
        context.in_market = True
        n = len(context.stock_pool)
        if n == 0:
            return
        value = context.portfolio.total_value * 0.95 / n
        for s in context.stock_pool:
            if s in bar_dict and bar_dict[s].is_trading:
                order_target_value(s, value)
        logger.info("[大盘择时] MACD金叉，入场")

    elif signal_down and context.in_market:
        context.in_market = False
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        logger.info("[大盘择时] MACD死叉，清仓")
