# 原文链接：https://www.joinquant.com/post/60000
# 策略：可能是最接近实盘的基本面三角
# 核心逻辑：基本面三角（ROE+营收增长+低PE），三因子等权打分，月度调仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'roe', 'revenue'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 60.0]
    df = df[df['roe'] > 0.08]
    df = df.head(200)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    # 三因子等权打分
    df['roe_rank'] = df['roe'].rank(ascending=True)   # ROE高分
    df['pe_rank'] = df['pe_ratio'].rank(ascending=False)            # PE低分
    df['cap_rank'] = df['market_cap'].rank(ascending=False)         # 市值适中

    df['total_score'] = df['roe_rank'] + df['pe_rank'] + df['cap_rank']
    df = df.sort_values('total_score', ascending=False)
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
    logger.info(f"基本面三角调仓，持仓: {target}")
