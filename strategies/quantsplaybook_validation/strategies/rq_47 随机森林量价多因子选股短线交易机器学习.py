# 原文链接：https://www.joinquant.com/post/随机森林量价多因子选股短线交易机器学习
# 策略：随机森林量价多因子选股短线交易机器学习
# 核心逻辑：用量价因子（动量+换手率+波动率）多因子评分替代随机森林，选高分股票。

import numpy as np

def init(context):
    context.n_stocks = 15
    context.momentum_n = 20
    context.vol_n = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 基本面过滤
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'market_cap', 'turnover_ratio'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 1000000000]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 80.0]
    df = df[df['turnover_ratio'] > 0.5]
    df = df.head(200)
    candidates = df.index.tolist()
    candidates = list(df.index)

    # 量价因子计算
    factor_data = []
    for s in candidates:
        try:
            prices = history_bars(s, context.momentum_n + 1, '1d', 'close')
            volumes = history_bars(s, context.vol_n, '1d', 'volume')
            if len(prices) < context.momentum_n + 1 or len(volumes) < context.vol_n:
                continue

            # 动量因子
            momentum = (prices[-1] - prices[0]) / prices[0]
            # 波动率因子（越低越稳定）
            returns = np.diff(prices[-context.vol_n:]) / prices[-context.vol_n:-1]
            volatility = np.std(returns)
            # 换手率因子（适中换手率）
            vol_mean = np.mean(volumes)
            vol_std = np.std(volumes)
            vol_score = -abs(vol_std / vol_mean - 0.5)  # 换手率稳定性

            factor_data.append({
                'stock': s,
                'momentum': momentum,
                'volatility': volatility,
                'vol_score': vol_score
            })
        except Exception:
            continue

    if not factor_data:
        return

    import numpy as np
    mom_arr = np.array([d['momentum'] for d in factor_data])
    vol_arr = np.array([d['volatility'] for d in factor_data])
    vs_arr = np.array([d['vol_score'] for d in factor_data])

    # 标准化评分
    def rank_score(arr, ascending=True):
        ranks = arr.argsort()
        scores = np.zeros(len(arr))
        for i, r in enumerate(ranks):
            scores[r] = i if ascending else len(arr) - 1 - i
        return scores / len(arr)

    mom_score = rank_score(mom_arr, ascending=False)
    vol_score = rank_score(vol_arr, ascending=True)   # 低波动好
    vs_score = rank_score(vs_arr, ascending=False)

    total_scores = mom_score + vol_score + vs_score
    sorted_idx = total_scores.argsort()[::-1]
    target = [factor_data[i]['stock'] for i in sorted_idx[:context.n_stocks]]

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
    logger.info(f"量价多因子选股完成，持仓: {target}")
