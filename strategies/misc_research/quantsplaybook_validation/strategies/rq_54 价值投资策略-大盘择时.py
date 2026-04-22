# 原文链接：https://www.joinquant.com/post/54xxx
# 策略：价值投资策略-大盘择时
# 核心逻辑：价值投资+大盘择时，低PE低PB高ROE选股，MACD判断大盘趋势，趋势向下时清仓

import numpy as np

HOLD_NUM = 10

def ema(p, n):
    k = 2.0 / (n + 1); e = p[0]; r = []
    for x in p: e = x * k + e * (1 - k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def market_trend_ok():
    """判断大盘趋势是否向上"""
    try:
        closes = history_bars('000300.XSHG', 35, '1d', 'close')
        if len(closes) < 35:
            return True
        macd, signal, hist = calc_macd(closes)
        # MACD在零轴上方且MACD > Signal
        return macd[-1] > 0 and macd[-1] > signal[-1]
    except Exception:
        return True

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(timing_check, time_rule=market_open(minute=5))

def handle_bar(context, bar_dict):
    pass

def timing_check(context, bar_dict):
    """每日大盘择时检查"""
    if not market_trend_ok():
        if context.portfolio.positions:
            logger.info("大盘MACD趋势向下，清仓")
            for stock in list(context.portfolio.positions.keys()):
                order_target_value(stock, 0)

def rebalance(context, bar_dict):
    if not market_trend_ok():
        logger.info("大盘趋势向下，跳过选股")
        return

    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pe_ratio', 'pb_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 5e9]
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 25]
    df = df[df['pb_ratio'] > 0]
    df = df[df['pb_ratio'] < 3]
    df = df[df['roe'] > 0.12]
    df = df.head(100)
    if df.empty:
        return

    df['pe_rank'] = df['pe_ratio'].rank(ascending=True, pct=True)
    df['pb_rank'] = df['pb_ratio'].rank(ascending=True, pct=True)
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True)
    df['score'] = df['pe_rank'] + df['pb_rank'] + df['roe_rank']
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入价值股 {stock}")
