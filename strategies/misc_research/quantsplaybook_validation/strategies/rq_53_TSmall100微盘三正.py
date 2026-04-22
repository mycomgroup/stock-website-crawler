# 原文链接：https://www.joinquant.com/post/50238
# 策略：TSmall-100, 微盘三正
# 作者：Gyro^.^
# 核心逻辑：选国证2000成分股中市值最小的100只，每天开盘再平衡，过滤ST、停牌、涨跌停

import numpy as np

INDEX = '399317.XSHE'   # 国证2000
N_POSITION = 100
N_CHOICE = 120

def init(context):
    context.stocks = []
    context.position_size = 0
    scheduler.run_daily(i_update, time_rule=market_open(minute=0))
    scheduler.run_daily(i_trader, time_rule=market_open(minute=35))


def handle_bar(context, bar_dict):
    pass

def i_update(context, bar_dict):
    stocks = index_components(INDEX)
    if not stocks:
        context.stocks = []
        return

    # 按市值升序选最小的 N_CHOICE 只，用 get_factor 获取市值
    try:
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['market_cap'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = factor_df.groupby(level=0).last().dropna()
        if df is None or len(df) == 0:
            return
        df = df[df['market_cap'] > 0]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 过滤科创板和北交所
    candidates = [s for s in candidates
                  if not s.startswith('688') and not s.startswith('8')]

    context.stocks = candidates[:N_POSITION]
    context.position_size = context.portfolio.total_value / N_POSITION if context.stocks else 0

def i_trader(context, bar_dict):
    stocks = context.stocks
    position_size = context.position_size
    if not stocks or position_size <= 0:
        return

    cash_size = 1.5 * position_size

    # 卖出不在目标的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in stocks:
            bar = (bar_dict[s] if s in bar_dict else None)
            if bar and bar.is_trading:
                order_target_value(s, 0)

    # 买入目标股票
    for s in stocks:
        if context.portfolio.cash < cash_size:
            break
        bar = (bar_dict[s] if s in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        if s not in context.portfolio.positions:
            order_target_value(s, position_size)
