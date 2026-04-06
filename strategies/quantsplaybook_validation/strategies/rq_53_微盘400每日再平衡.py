# 原文链接：https://www.joinquant.com/post/44853
# 策略：微盘400每日再平衡
# 作者：开心果
# 核心逻辑：全市场按市值升序选最小的400只，每天9:30再平衡，过滤ST、科创板、北交所

import numpy as np

N_STOCKS = 400

def init(context):
    context.n_stocks = N_STOCKS
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    try:
        all_stocks_df = all_instruments('CS')
        all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                      if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    except Exception:
        return

    # Get smallest 400 stocks by market cap
    prev_date = context.now.date()
    factor_df = get_factor(
        all_stocks,
        ['market_cap'],
    )
    if factor_df is None or factor_df.empty:
        return
    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 0]
    df = df.head(context.n_stocks)
    candidates = df.index.tolist()
    if df is None or len(df) == 0:
        return
    stocks = [s for s in df.index if s in bar_dict and bar_dict[s].is_trading]
    if not stocks:
        return

    value = context.portfolio.total_value / len(stocks)

    for s in list(context.portfolio.positions.keys()):
        if s not in stocks:
            order_target_value(s, 0)

    for s in stocks:
        order_target_value(s, value)
