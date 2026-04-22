# 原文链接：https://www.joinquant.com/post/51xxx
# 策略：北上资金持股比选股策略（北向港资外资）
# 核心逻辑：选沪深港通标的中基本面优质（高ROE低PE低PB）的股票，月度调仓

import numpy as np

HOLD_NUM = 10

def init(context):
    # 沪深港通标的（用沪深300代理）
    context.universe = index_components('000300.XSHG')
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    stocks = index_components('000300.XSHG')

    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['pe_ratio', 'pb_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 30]
    df = df[df['pb_ratio'] > 0]
    df = df[df['pb_ratio'] < 4]
    df = df[df['roe'] > 0.12]
    df = df.head(100)
    if df.empty:
        return

    # 综合评分
    df['pe_rank'] = df['pe_ratio'].rank(ascending=True, pct=True)
    df['pb_rank'] = df['pb_ratio'].rank(ascending=True, pct=True)
    df['roe_rank'] = df['roe'].rank(ascending=False, pct=True)
    df['score'] = df['pe_rank'] + df['pb_rank'] + df['roe_rank']
    df = df.sort_values('score', ascending=False)

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入北向标的 {stock}")
