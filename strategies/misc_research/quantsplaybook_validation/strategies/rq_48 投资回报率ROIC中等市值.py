# 原文链接：https://www.joinquant.com/post/48xxx
# 策略：投资回报率ROIC中等市值
# 核心逻辑：中等市值（50-500亿）+高ROIC（用ROE代理）选股，月度调仓，持仓10只

import numpy as np

HOLD_NUM = 10
CAP_MIN = 5e9   # 50亿
CAP_MAX = 5e10  # 500亿

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取基本面数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > CAP_MIN]
    df = df[df['market_cap'] < CAP_MAX]
    df = df[df['roe'] > 0.10]
    df = df.sort_values('roe', ascending=False).head(50)
    if df.empty:
        return

    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}")
