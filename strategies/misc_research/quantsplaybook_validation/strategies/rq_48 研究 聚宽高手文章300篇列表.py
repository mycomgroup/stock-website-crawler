# 原文链接：https://www.joinquant.com/post/48xxx
# 策略：研究 聚宽高手文章300篇列表
# 核心逻辑：综合多篇高手策略的精华，小市值+低PE+高ROE三因子，月度调仓

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
            ['market_cap', 'pe_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] < 5e9]  # 小市值 < 50亿
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 40]
    df = df[df['roe'] > 0.08]
    df = df.sort_values('market_cap', ascending=True).head(100)
    if df.empty:
        return

    # 三因子综合评分
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True)
    df['roe_rank'] = df['roe'].rank(ascending=False)
    df['cap_rank'] = df['market_cap'].rank(ascending=True)
    df['score'] = df['pe_rank'] + df['roe_rank'] + df['cap_rank']
    df = df.sort_values('score', ascending=True)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}")
