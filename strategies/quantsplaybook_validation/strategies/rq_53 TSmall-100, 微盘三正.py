# 原文链接：https://www.joinquant.com/post/53000
# 策略：TSmall-100, 微盘三正
# 核心逻辑：微盘三正策略，选市值最小的100只股票中连续3日收阳的股票，短线持有。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.small_pool_size = 100
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')
              and not s.startswith('4') and not s.startswith('9')]

    # 获取市值，选最小100只
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(context.small_pool_size)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return

    small_pool = list(df.index)

    # 筛选连续3日收阳（收盘>开盘）
    candidates = []
    for s in small_pool:
        try:
            closes = history_bars(s, 4, '1d', 'close')
            opens  = history_bars(s, 4, '1d', 'open')
            if closes is None or opens is None or len(closes) < 3:
                continue
            # 检查最近3日是否都是阳线（收盘>开盘）
            three_yang = all(closes[i] > opens[i] for i in [-3, -2, -1])
            if three_yang:
                candidates.append(s)
        except Exception:
            continue

    if not candidates:
        logger.info("无三正候选股")
        # 清仓不在候选的持仓
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    target = candidates[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"微盘三正调仓，持仓: {target}")
