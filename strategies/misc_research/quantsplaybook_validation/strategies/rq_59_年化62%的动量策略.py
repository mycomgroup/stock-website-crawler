# 原文链接：https://www.joinquant.com/post/59001
# 策略：年化62%的动量策略
# 核心逻辑：动量策略，选近20日涨幅最强的股票，月度调仓，持仓10只。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.momentum_days = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 先用基本面过滤
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 80.0]
    df = df.head(300)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    pool = list(df.index)

    # 计算动量
    mom_scores = {}
    for s in pool:
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
    logger.info(f"动量策略调仓，持仓: {target}")
