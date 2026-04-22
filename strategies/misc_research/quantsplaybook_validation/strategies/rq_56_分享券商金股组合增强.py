# 原文链接：https://www.joinquant.com/post/56000
# 策略：分享券商金股组合增强
# 核心逻辑：券商金股组合，选沪深300中ROE最高+PE最低的股票，月度调仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.index = '000300.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 沪深300成分股
    stocks = index_components(context.index)
    stocks = [s for s in stocks if not s.startswith('688')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 50.0]
    df = df[df['roe'] > 0.05]
    df = df.head(50)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    # 综合评分：ROE高分+PE低分
    df['roe_rank'] = df['roe'].rank(ascending=False)
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True)
    df['score'] = df['roe_rank'] + df['pe_rank']
    df = df.sort_values('score', ascending=True)
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
    logger.info(f"券商金股调仓，持仓: {target}")
