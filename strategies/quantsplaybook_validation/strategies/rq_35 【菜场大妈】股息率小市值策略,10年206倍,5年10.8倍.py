# 原文链接：https://www.joinquant.com/post/菜场大妈股息率小市值策略10年206倍5年10.8倍
# 策略：【菜场大妈】股息率小市值策略,10年206倍,5年10.8倍
# 核心逻辑：高股息率+小市值选股，用get_fundamentals获取股息率，月度调仓，持仓10只。

import numpy as np

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
        ['pe_ratio', 'market_cap', 'dividend_yield'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['dividend_yield'] > 2.0]
    df = df[df['market_cap'] > 500000000]
    df = df[df['market_cap'] < 8000000000]
    df = df[df['pe_ratio'] > 0.0]
    df = df[df['pe_ratio'] < 50.0]
    df = df.head(context.n_stocks + 10)
    candidates = df.index.tolist()

    if df.empty:
        return

    # 综合排名：高股息率 + 小市值
    df['div_rank'] = df['dividend_yield'].rank(ascending=False)
    df['cap_rank'] = df['market_cap'].rank(ascending=True)
    df['total_rank'] = df['div_rank'] + df['cap_rank']
    df = df.sort_values('total_rank', ascending=True)
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
    logger.info(f"菜场大妈高股息小市值调仓完成，持仓: {target}")
