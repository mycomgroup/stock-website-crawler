# Auto-generated alias for placeholder rq_19 复现FFScore财务模型.txt
# Reuses migrated RiceQuant implementation from rq_18_微盘股400轮动.py
# Shared original URL: https://www.joinquant.com/post/34748

# 微盘股400轮动策略 - RiceQuant版本
# 原文：微盘股400多角度深入研究
# 作者：Gyro^.^
# 原文：https://www.joinquant.com/post/34748
# 逻辑：选全市场市值最小的400只股票，每日等权再平衡

import numpy as np


def init(context):
    context.n_choice = 120
    context.n_position = 100
    scheduler.run_daily(i_update, time_rule=market_open(minute=0))
    scheduler.run_daily(i_trader, time_rule=market_open(minute=35))


def handle_bar(context, bar_dict):
    pass


def i_update(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = instruments_df['order_book_id'].tolist()
    stock_ids = [s for s in stock_ids if not s.startswith(('688', '4', '8'))]

    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stock_ids,
            ['pb_ratio'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    context.position_size = (1.0 / context.n_position) * context.portfolio.total_value


def i_trader(context, bar_dict):
    choice = context.choice
    if not choice:
        return

    position_size = context.position_size
    lm_value = 0.8 * position_size
    hm_value = 1.2 * position_size

    # 卖出不在候选池的持仓
    for s in list(context.portfolio.positions.keys()):
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if s not in choice:
            order_target_value(s, 0)

    # 买入/再平衡
    for s in choice:
        if context.portfolio.cash < position_size:
            break
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        pos = context.portfolio.positions.get(s)
        if pos is None:
            order_target_value(s, position_size)
        elif pos.market_value < lm_value:
            order_target_value(s, position_size)
        elif pos.market_value > hm_value:
            order_target_value(s, position_size)
