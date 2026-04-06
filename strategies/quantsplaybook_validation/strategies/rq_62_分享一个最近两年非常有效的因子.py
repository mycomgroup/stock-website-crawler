# 原文链接：https://www.joinquant.com/post/62001
# 策略：分享一个最近两年非常有效的因子
# 核心逻辑：有效因子策略，用近期价格动量+换手率变化因子选股，月度调仓。

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

    # 计算动量+换手率变化因子
    factor_scores = {}
    for s in pool:
        try:
            closes = history_bars(s, context.momentum_days + 1, '1d', 'close')
            volumes = history_bars(s, context.momentum_days + 1, '1d', 'volume')
            if closes is None or volumes is None:
                continue
            if len(closes) < context.momentum_days + 1:
                continue
            # 动量因子
            mom = (closes[-1] - closes[0]) / closes[0]
            # 换手率变化：近5日均量/近20日均量
            recent_vol = np.mean(volumes[-5:])
            long_vol = np.mean(volumes[-context.momentum_days:])
            turnover_change = recent_vol / long_vol if long_vol > 0 else 1
            # 综合因子：动量上升+换手率放大
            factor_scores[s] = mom * 0.6 + (turnover_change - 1) * 0.4
        except Exception:
            continue

    if not factor_scores:
        return

    sorted_stocks = sorted(factor_scores, key=factor_scores.get, reverse=True)
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
    logger.info(f"有效因子调仓，持仓: {target}")
