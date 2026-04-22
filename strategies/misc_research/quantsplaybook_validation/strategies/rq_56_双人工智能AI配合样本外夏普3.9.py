# 原文链接：https://www.joinquant.com/post/56001
# 策略：双人工智能AI配合样本外夏普3.9
# 核心逻辑：双因子AI策略，用动量+价值双因子评分，选高分股票，月度调仓。

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
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 60.0]
    df = df[df['roe'] > 0.05]
    df = df.head(200)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    # 价值因子评分
    df['pe_rank'] = df['pe_ratio'].rank(ascending=False)
    df['roe_rank'] = df['roe'].rank(ascending=True)

    # 动量因子评分
    mom_scores = {}
    for s in df.index:
        try:
            closes = history_bars(s, context.momentum_days + 1, '1d', 'close')
            if closes is not None and len(closes) >= context.momentum_days + 1:
                mom_scores[s] = (closes[-1] - closes[0]) / closes[0]
            else:
                mom_scores[s] = 0
        except Exception:
            mom_scores[s] = 0

    import pandas as pd
    df['momentum'] = pd.Series(mom_scores)
    df['mom_rank'] = df['momentum'].rank(ascending=True)

    # 双因子综合评分
    df['ai_score'] = df['pe_rank'] + df['roe_rank'] + df['mom_rank'] * 2
    df = df.sort_values('ai_score', ascending=False)
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
    logger.info(f"双AI因子调仓，持仓: {target}")
