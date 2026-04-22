# 原文链接：https://www.joinquant.com/post/54xxx
# 策略：sales_growth今年最优版
# 核心逻辑：营收增长率因子选股，选近期营收增长最快的股票，月度调仓，持仓10只

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
            ['market_cap', 'inc_revenue_year_on_year', 'inc_net_profit_year_on_year', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 2e10]
    df = df[df['inc_revenue_year_on_year'] > 0.15]    # 营收增长>15%
    df = df[df['inc_net_profit_year_on_year'] > 0.10] # 净利润增长>10%
    df = df[df['roe'] > 0.08]
    df = df.sort_values('inc_revenue_year_on_year', ascending=False).head(50)
    if df.empty:
        return

    # 综合评分：营收增长 + 净利润增长 + ROE
    df['rev_rank'] = df['inc_revenue_year_on_year'].rank(ascending=False, pct=True)
    df['np_rank'] = df['inc_net_profit_year_on_year'].rank(ascending=False, pct=True)
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True)
    df['score'] = df['rev_rank'] * 0.4 + df['np_rank'] * 0.3 + df['roe_rank'] * 0.3
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入营收增长股 {stock}")
