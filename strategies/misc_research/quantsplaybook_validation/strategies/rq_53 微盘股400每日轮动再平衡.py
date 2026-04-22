# 原文链接：https://www.joinquant.com/post/53001
# 策略：微盘股400每日轮动再平衡
# 核心逻辑：全市场按市值升序选最小400只，每日再平衡，过滤ST/科创/北交。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 400
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    # 过滤科创板(688)、北交所(8开头)、ST
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(context.n_stocks + 20)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    target = list(df.index)[:context.n_stocks]

    # 清仓不在目标的持仓
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
    logger.info(f"微盘400再平衡完成，持仓数: {n}")
