def _normalize_factor_frame(factor_df):
    if factor_df is None:
        return None
    try:
        if hasattr(factor_df, 'empty') and factor_df.empty:
            return factor_df
        if not hasattr(factor_df, 'columns'):
            factor_df = factor_df.to_frame()
        index = getattr(factor_df, 'index', None)
        if index is not None and getattr(index, 'nlevels', 1) > 1:
            factor_df = factor_df.groupby(level=-1).last()
        return factor_df.dropna()
    except Exception:
        return None


# 为实盘做的更新_盘中止损版 - RiceQuant版本
# 逻辑：小市值选股 + 盘中止损（日线近似），月度选股+日度止损

import numpy as np


def init(context):
    context.stock_num = 20
    context.month = -1
    scheduler.run_daily(monthly_rebalance, time_rule=market_open(minute=5))
    scheduler.run_daily(intraday_stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def monthly_rebalance(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    all_stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

    try:
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'roe'],
        )
        if factor_df is None or len(factor_df) == 0:
            return
        df = _normalize_factor_frame(factor_df)
        if df is None or len(df) == 0:
            return
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['market_cap'] > 5]
        df = df[df['market_cap'] < 100]
        df = df[df['roe'] > 0.05]
        df = df.sort_values(['roe', 'market_cap'], ascending=[False, True])
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return

    target = [s for s in candidates if (s not in bar_dict) or bar_dict[s].is_trading][:context.stock_num]
    if not target:
        return

    context.month = current_month

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def intraday_stop_loss(context, bar_dict):
    """盘中止损：跌幅超过5%卖出"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        if bar.close / pos.avg_cost - 1 < -0.05:
            order_target_value(stock, 0)
