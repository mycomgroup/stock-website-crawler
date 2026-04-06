# 原文链接：https://www.joinquant.com/post/自适应量化终极算法2.0全新升级
# 策略：自适应量化终极算法2.0 （全新升级）
# 核心逻辑：自适应动量+均值回归混合策略，根据市场波动率切换策略模式。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 10
    context.bond_etf = '511010.XSHG'
    context.index_etf = '510300.XSHG'
    context.vol_threshold = 0.02  # 波动率阈值
    context.mode = 'momentum'     # 当前策略模式
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 计算市场波动率
    prices = history_bars(context.index_etf, 21, '1d', 'close')
    if len(prices) < 21:
        return
    returns = np.diff(prices) / prices[:-1]
    vol = np.std(returns)

    # 根据波动率切换策略模式
    if vol > context.vol_threshold:
        context.mode = 'mean_reversion'  # 高波动：均值回归
    else:
        context.mode = 'momentum'        # 低波动：动量追涨

    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    if context.mode == 'momentum':
        # 动量模式：选近20日涨幅最大的小市值股票
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['market_cap'] > 500000000]
        df = df[df['market_cap'] < 6000000000]
        df = df[df['pe_ratio'] > 0.0]
        df = df.head(100)
        candidates = df.index.tolist()
        candidates = list(df.index)

        mom_list = []
        for s in candidates:
            try:
                p = history_bars(s, 21, '1d', 'close')
                if len(p) >= 21:
                    mom = (p[-1] - p[0]) / p[0]
                    mom_list.append((s, mom))
            except Exception:
                continue
        mom_list.sort(key=lambda x: x[1], reverse=True)
        target = [s for s, _ in mom_list[:context.n_stocks]]

    else:
        # 均值回归模式：选近期超跌的低PE高ROE股票
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pe_ratio'] > 0.0]
        df = df[df['pe_ratio'] < 25.0]
        df = df[df['roe'] > 0.12]
        df = df.head(100)
        candidates = df.index.tolist()
        candidates = list(df.index)

        rev_list = []
        for s in candidates:
            try:
                p = history_bars(s, 11, '1d', 'close')
                if len(p) >= 11:
                    ret = (p[-1] - p[0]) / p[0]
                    rev_list.append((s, ret))
            except Exception:
                continue
        rev_list.sort(key=lambda x: x[1])  # 跌幅最大的
        target = [s for s, _ in rev_list[:context.n_stocks]]

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
    logger.info(f"波动率={vol:.4f}，模式={context.mode}，持仓: {target}")
