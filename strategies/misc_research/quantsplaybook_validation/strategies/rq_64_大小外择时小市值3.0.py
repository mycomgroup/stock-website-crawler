# 原文链接：https://www.joinquant.com/post/64002
# 策略：大小外择时小市值3.0
# 核心逻辑：大盘/小盘/外资三重择时，根据市场状态切换大市值/小市值/空仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.n_stocks = 10
    context.large_etf = '510300.XSHG'   # 沪深300（大盘）
    context.small_etf = '510500.XSHG'   # 中证500（小盘）
    context.mode = 'small'  # 当前模式：large/small/cash
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def get_market_signal(etf):
    """获取ETF的MACD信号"""
    closes = history_bars(etf, 60, '1d', 'close')
    if closes is None or len(closes) < 40:
        return 0
    dif, dea, macd = calc_macd(closes)
    if dif[-1] > dea[-1] and dif[-1] > 0:
        return 1   # 上涨
    elif dif[-1] < dea[-1] and dif[-1] < 0:
        return -1  # 下跌
    return 0

def rebalance(context, bar_dict):
    large_signal = get_market_signal(context.large_etf)
    small_signal = get_market_signal(context.small_etf)

    # 三重择时逻辑
    if large_signal < 0 and small_signal < 0:
        # 大小盘均弱，空仓
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        context.mode = 'cash'
        logger.info("大小盘均弱，空仓")
        return

    # 选择大市值或小市值
    if large_signal >= small_signal:
        # 大盘强，选大市值股票
        context.mode = 'large'
        prev_date = context.now.date()
        instruments_df = all_instruments('CS')
        stocks = instruments_df['order_book_id'].tolist()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 50000000000]
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 30.0]
        df = df.head(context.n_stocks + 5)
        candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    target = list(df.index)[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    if n == 0:
        return
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"大小外择时模式={context.mode}，持仓: {target}")
