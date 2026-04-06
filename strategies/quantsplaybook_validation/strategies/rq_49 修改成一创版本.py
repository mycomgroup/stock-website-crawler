# 原文链接：https://www.joinquant.com/post/49xxx
# 策略：修改成一创版本
# 核心逻辑：一创版本小市值策略，低PE+低PB+小市值，月度调仓，持仓10只

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
            ['market_cap', 'pe_ratio', 'pb_ratio'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 3e9]
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 30]
    df = df[df['pb_ratio'] > 0]
    df = df[df['pb_ratio'] < 3]
    df = df.sort_values('market_cap', ascending=True).head(50)
    if df.empty:
        return

    # 综合评分：低PE + 低PB + 小市值
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True)
    df['pb_rank'] = df['pb_ratio'].rank(ascending=True)
    df['cap_rank'] = df['market_cap'].rank(ascending=True)
    df['score'] = df['pe_rank'] + df['pb_rank'] + df['cap_rank']
    df = df.sort_values('score', ascending=True)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}")
