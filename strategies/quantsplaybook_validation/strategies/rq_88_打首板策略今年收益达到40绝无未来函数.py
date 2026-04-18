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


# 打首板策略 - RiceQuant版本
# 逻辑：选首次涨停（首板）的小市值股票，次日低开买入

import numpy as np


def _build_stock_pool(min_cap=5, max_cap=60, max_size=500):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = [s for s in instruments_df['order_book_id'].tolist()
              if not s.startswith(('688', '4', '8', '3'))]
    try:
        factor_df = get_factor(stocks, ['market_cap'])
        if factor_df is None or len(factor_df) == 0:
            return stocks[:max_size]
        df = _normalize_factor_frame(factor_df)
        if not hasattr(df, 'columns'):
            df = df.to_frame(name='market_cap')
        if 'market_cap' not in df.columns:
            return stocks[:max_size]
        df = df[(df['market_cap'] > min_cap) & (df['market_cap'] < max_cap)]
        df = df.sort_values('market_cap').head(max_size)
        return df.index.tolist()
    except Exception:
        return stocks[:max_size]


def init(context):
    context.stock_num = 3
    context.candidates = []
    context.last_week_date = None
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def update_pool(context, bar_dict):
    today_key = context.now.strftime('%Y-%m-%d')
    if today_key == context.last_week_date:
        return

    pool = _build_stock_pool(min_cap=5, max_cap=80, max_size=500)
    result = []
    for stock in pool:
        try:
            bars = history_bars(stock, 8, '1d', ['close', 'limit_up'])
            if bars is None or len(bars) < 6:
                continue
            latest = bars[-1]
            latest_limit = float(latest['limit_up']) if latest['limit_up'] is not None else 0
            if latest_limit <= 0 or float(latest['close']) < latest_limit * 0.995:
                continue
            yesterday_limit = True
            no_prev_limit = not any(
                row['limit_up'] is not None and float(row['close']) >= float(row['limit_up']) * 0.995
                for row in bars[-6:-1]
            )
            if yesterday_limit and no_prev_limit:
                score = float(latest['close']) / max(float(bars[-2]['close']), 1e-6)
                result.append((score, stock))
        except Exception:
            continue

    context.candidates = [stock for _, stock in sorted(result, reverse=True)[:context.stock_num * 12]]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        daily = history_bars(stock, 2, '1d', ['close', 'limit_up'])
        if daily is None or len(daily) < 2:
            continue
        prev_close = float(daily[-1]['close'])
        if 0.955 <= bar.open / max(prev_close, 1e-6) <= 1.02 and bar.close > bar.open:
            target.append(stock)
        if len(target) >= context.stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def stop_loss(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        avg_cost = getattr(pos, 'avg_cost', getattr(pos, 'avg_price', 0))
        if avg_cost > 0 and bar.close / avg_cost - 1 < -0.05:
            order_target_value(stock, 0)
