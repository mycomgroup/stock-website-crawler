# 原文链接：https://www.joinquant.com/post/56003
# 策略：大盘一路向上时追总龙头2个月3倍
# 核心逻辑：大盘上涨时追龙头，选近20日涨幅最强的股票，持有2个月。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.n_stocks = 5
    context.index_etf = '510300.XSHG'
    context.momentum_days = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 判断大盘是否上涨（用沪深300ETF的MACD）
    index_closes = history_bars(context.index_etf, 60, '1d', 'close')
    if index_closes is None or len(index_closes) < 40:
        return

    dif, dea, macd = calc_macd(index_closes)
    market_up = dif[-1] > dea[-1] and dif[-1] > 0

    if not market_up:
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        logger.info("大盘非上涨趋势，空仓")
        return

    # 选近20日涨幅最强的股票
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    stocks = stocks[:500]  # 限制范围

    mom_scores = {}
    for s in stocks:
        try:
            closes = history_bars(s, context.momentum_days + 1, '1d', 'close')
            if closes is not None and len(closes) >= context.momentum_days + 1:
                mom = (closes[-1] - closes[0]) / closes[0]
                if mom > 0:
                    mom_scores[s] = mom
        except Exception:
            continue

    if not mom_scores:
        return

    sorted_stocks = sorted(mom_scores, key=mom_scores.get, reverse=True)
    target = sorted_stocks[:context.n_stocks]

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
    logger.info(f"追龙头调仓，持仓: {target}")
