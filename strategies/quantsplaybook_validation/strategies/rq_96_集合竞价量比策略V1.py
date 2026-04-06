# 集合竞价量比策略V1 - RiceQuant版本
# 原文：集合竞价量比策略V1
# 逻辑：用日线成交量变化率代替集合竞价量比，选量比异常放大的股票

import numpy as np


def init(context):
    context.buy_num = 3
    context.stock_list = []
    context.month = -1
    scheduler.run_daily(auction, time_rule=market_open(minute=0))
    scheduler.run_daily(sell_norm, time_rule=market_open(minute=225))


def handle_bar(context, bar_dict):
    pass


def auction(context, bar_dict):
    """选量比异常放大的小市值股票"""
    current_month = context.now.month
    if current_month == context.month:
        return
    context.month = current_month

    all_stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8'))]

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
        df = df[df['market_cap'] > 5e+08]
        df = df[df['market_cap'] < 1e+10]
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    # 量比：今日成交量 / 过去5日平均成交量
    candidates = []
    result = []
    for stock in candidates:
        try:
            volumes = history_bars(stock, 6, '1d', 'volume')
            if volumes is None or len(volumes) < 6:
                continue
            avg_vol = np.mean(volumes[:-1])
            if avg_vol == 0:
                continue
            vol_ratio = volumes[-1] / avg_vol
            if vol_ratio > 2.0:  # 量比>2
                result.append((stock, vol_ratio))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1], reverse=True)
    context.stock_list = [s for s, _ in candidates[:context.buy_num * 2]]

    # 买入
    target = []
    for stock in context.stock_list:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.buy_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def sell_norm(context, bar_dict):
    """尾盘止损"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        loss = bar.close / pos.avg_cost - 1
        if loss < -0.05:
            order_target_value(stock, 0)
