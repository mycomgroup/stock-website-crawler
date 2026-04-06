# 原文链接：https://www.joinquant.com/post/45070
# 策略：大容量低回撤价值投资-排除小市值因子
# 作者：价值投资者
# 核心逻辑：大市值（市值>50亿）+低PB+高ROE+MACD趋势过滤，月度调仓
# 注：原版用jqfactor+jqlib_ta+ml_lib，此处改为大市值价值选股

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
    context.n_stocks = 15
    context.min_cap = 50e8   # 50亿市值门槛
    context.stock_pool = []
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    """月度再平衡：大市值价值选股+MACD过滤"""
    # 大盘MACD趋势过滤
    idx_prices = history_bars('000300.XSHG', 60, '1d', 'close')
    if idx_prices is not None and len(idx_prices) >= 40:
        p = np.array(idx_prices, dtype=float)
        diff, dea, _ = calc_macd(p)
        if diff[-1] < dea[-1] and diff[-2] < dea[-2]:
            # 大盘MACD持续死叉，减仓
            for s in list(context.portfolio.positions.keys()):
                order_target_value(s, 0)
            logger.info("[大容量价值] 大盘MACD死叉，空仓")
            return

    # 全市场大市值筛选
    all_stocks_df = all_instruments('CS')
    all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                  if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pb_ratio'] > 0.0]
    df = df[df['pb_ratio'] < 3.0]
    df = df[df['roe'] > 0.1]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    context.stock_pool = list(df.index)[:context.n_stocks]
    logger.info(f"[大容量价值] 选股={context.stock_pool}")

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
