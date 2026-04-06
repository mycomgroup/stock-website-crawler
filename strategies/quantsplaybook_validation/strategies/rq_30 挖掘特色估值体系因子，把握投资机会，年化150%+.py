# 原文链接：https://www.joinquant.com/post/挖掘特色估值体系因子
# 策略：挖掘特色估值体系因子，把握投资机会，年化150%+
# 核心逻辑：用EV/EBITDA+ROE+市值多因子评分选股，选高分股票月度调仓。

import numpy as np

def init(context):
    context.n_stocks = 10
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    # 获取EV/EBITDA、ROE、市值
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
    df = df[df['roe'] > 0.08]
    df = df[df['market_cap'] > 2000000000]
    df = df.head(100)
    candidates = df.index.tolist()
    if df.empty:
        return

    # 多因子评分：EV/EBITDA越低越好，ROE越高越好，市值适中
    df['ev_score'] = df['pe_ratio'].rank(ascending=True)
    df['roe_score'] = df['roe'].rank(ascending=False)
    df['total_score'] = df['ev_score'] + df['roe_score']
    df = df.sort_values('total_score', ascending=True)
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
    logger.info(f"多因子评分选股完成，持仓: {target}")
