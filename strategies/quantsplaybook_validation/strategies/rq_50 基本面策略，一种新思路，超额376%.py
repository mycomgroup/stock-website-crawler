# 原文链接：https://www.joinquant.com/post/50xxx
# 策略：基本面策略，一种新思路，超额376%
# 核心逻辑：基本面新思路，用营收增长率+净利润增长率+ROE三因子打分，选高分股票

import numpy as np

HOLD_NUM = 10

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe', 'inc_revenue_year_on_year', 'inc_net_profit_year_on_year'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 2e10]
    df = df[df['roe'] > 0.05]
    df = df[df['inc_revenue_year_on_year'] > 0]
    df = df[df['inc_net_profit_year_on_year'] > 0]
    df = df.head(200)
    if df.empty:
        return

    # 三因子打分
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True)
    df['rev_rank'] = df['inc_revenue_year_on_year'].rank(ascending=False, pct=True)
    df['np_rank'] = df['inc_net_profit_year_on_year'].rank(ascending=False, pct=True)
    df['score'] = df['roe_rank'] + df['rev_rank'] + df['np_rank']
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}")
