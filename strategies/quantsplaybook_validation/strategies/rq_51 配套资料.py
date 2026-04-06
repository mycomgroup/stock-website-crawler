# 原文链接：https://www.joinquant.com/post/51xxx
# 策略：配套资料
# 核心逻辑：配套资料策略，基础小市值+低PE策略，月度调仓

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
            ['market_cap', 'pe_ratio'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 3e9]
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 40]
    df = df.sort_values('market_cap', ascending=True).head(HOLD_NUM * 3)
    if df.empty:
        return

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}")
