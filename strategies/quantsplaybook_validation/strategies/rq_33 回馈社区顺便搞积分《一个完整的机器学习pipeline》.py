# 原文链接：https://www.joinquant.com/post/回馈社区顺便搞积分一个完整的机器学习pipeline
# 策略：回馈社区顺便搞积分《一个完整的机器学习pipeline》
# 核心逻辑：多因子评分pipeline（市值+PE+ROE+动量），等权打分选股，月度调仓。

import numpy as np

def init(context):
    context.n_stocks = 20
    context.momentum_n = 20
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    prev_date = context.now.date()
    factor_df = get_factor(
        stocks,
        ['pe_ratio', 'pb_ratio', 'market_cap', 'roe'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 80.0]
    df = df[df['market_cap'] > 500000000]
    df = df.head(300)
    candidates = df.index.tolist()
    if df.empty:
        return

    # 多因子等权评分pipeline
    # 市值因子：越小越好（小市值溢价）
    df['cap_score'] = df['market_cap'].rank(ascending=True, pct=True)
    # PE因子：越低越好
    df['pe_score'] = df['pe_ratio'].rank(ascending=True, pct=True)
    # ROE因子：越高越好
    df['roe_score'] = df['roe'].rank(ascending=False, pct=True)

    # 动量因子
    momentum_scores = {}
    for s in df.index:
        try:
            prices = history_bars(s, context.momentum_n + 1, '1d', 'close')
            if len(prices) > context.momentum_n:
                mom = (prices[-1] - prices[0]) / prices[0]
                momentum_scores[s] = mom
        except Exception:
            momentum_scores[s] = 0.0

    df['momentum'] = df.index.map(lambda s: momentum_scores.get(s, 0.0))
    df['mom_score'] = df['momentum'].rank(ascending=False, pct=True)

    # 等权综合评分
    df['total_score'] = (df['cap_score'] + df['pe_score'] + df['roe_score'] + df['mom_score']) / 4
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
    logger.info(f"多因子pipeline选股完成，持仓: {target}")
