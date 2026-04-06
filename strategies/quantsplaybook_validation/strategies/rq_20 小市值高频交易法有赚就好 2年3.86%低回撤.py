# 原文链接：https://www.joinquant.com/post/44700
# 策略：小市值高频交易法有赚就好 2年3.86%低回撤
# 作者：稳健派
# 核心逻辑：小市值股票+EMA趋势过滤，低频换仓，控制回撤
# 注：原版用talib EMA，此处改为numpy本地EMA实现

import numpy as np


def ema(prices, n):
    """指数移动平均"""
    k = 2.0 / (n + 1)
    e = prices[0]
    res = []
    for x in prices:
        e = x * k + e * (1 - k)
        res.append(e)
    return np.array(res)


def init(context):
    context.n_stocks = 5
    context.stock_pool = []
    context.ema_short = 5
    context.ema_long = 20
    scheduler.run_monthly(select_stocks, tradingday=1, time_rule=market_open(minute=10))
    scheduler.run_daily(check_trend, time_rule=market_open(minute=20))


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
    df = df.head(50)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    # 在小市值50只中用EMA趋势过滤
    valid = []
    for s in list(df.index):
        prices = history_bars(s, 30, '1d', 'close')
        if prices is None or len(prices) < 25:
            continue
        p = np.array(prices, dtype=float)
        ema_s = ema(p, context.ema_short)
        ema_l = ema(p, context.ema_long)
        # EMA短线在长线上方，趋势向上
        if ema_s[-1] > ema_l[-1]:
            valid.append(s)

    context.stock_pool = valid[:context.n_stocks]
    logger.info(f"[小市值EMA] 股票池={context.stock_pool}")


def check_trend(context, bar_dict):
    """日度检查趋势，调整持仓"""
    # 卖出趋势转弱的持仓
    for s in list(context.portfolio.positions.keys()):
        prices = history_bars(s, 30, '1d', 'close')
        if prices is None or len(prices) < 25:
            order_target_value(s, 0)
            continue
        p = np.array(prices, dtype=float)
        ema_s = ema(p, context.ema_short)
        ema_l = ema(p, context.ema_long)
        if ema_s[-1] < ema_l[-1]:
            order_target_value(s, 0)
            logger.info(f"[小市值EMA] 趋势转弱，卖出 {s}")

    # 买入股票池中未持有的
    n = len(context.stock_pool)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in context.stock_pool:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
