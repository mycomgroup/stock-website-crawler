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


# 最新解密追涨龙头打板策略 - RiceQuant版本
# 逻辑：选近期有涨停的小市值股票，MA5向上时打板买入

import numpy as np


def _build_stock_pool(min_cap=10, max_cap=100, max_size=500):
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

    pool = _build_stock_pool(min_cap=10, max_cap=120, max_size=500)
    result = []
    for stock in pool:
        try:
            bars = history_bars(stock, 8, '1d', ['close', 'limit_up'])
            if bars is None or len(bars) < 6:
                continue
            limit_hits = sum(
                1 for row in bars[-5:]
                if row['limit_up'] is not None and float(row['close']) >= float(row['limit_up']) * 0.995
            )
            if limit_hits < 1:
                continue
            closes = np.array([float(row['close']) for row in bars], dtype=float)
            ma5 = np.mean(closes[-5:])
            ma5_prev = np.mean(closes[-6:-1])
            if ma5 > ma5_prev:
                score = limit_hits + ma5 / max(ma5_prev, 1e-6)
                result.append((score, stock))
        except Exception:
            continue

    result.sort(key=lambda item: item[0], reverse=True)
    context.candidates = [stock for _, stock in result[:context.stock_num * 12]]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        daily = history_bars(stock, 1, '1d', ['close'])
        if daily is None or len(daily) < 1:
            continue
        prev_close = float(daily[-1]['close'])
        if bar.close > bar.open and bar.close > prev_close * 1.02:
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
        if avg_cost > 0 and bar.close / avg_cost - 1 < -0.06:
            order_target_value(stock, 0)
