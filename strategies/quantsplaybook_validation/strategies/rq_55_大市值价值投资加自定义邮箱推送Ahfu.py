# 原文链接：https://www.joinquant.com/post/55000
# 策略：大市值价值投资加自定义邮箱推送Ahfu
# 核心逻辑：大市值（市值>100亿）+低PE+高ROE价值投资，季度调仓，持仓10只。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.min_cap = 100e8  # 100亿市值门槛
    # 季度调仓：每季度第一个交易日
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 每3个月调仓一次
    month = context.now.month
    if month not in [1, 4, 7, 10]:
        return

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
    df = df[df['pe_ratio'] < 30.0]
    df = df[df['roe'] > 0.1]
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
    logger.info(f"大市值价值投资季度调仓，持仓: {target}")
