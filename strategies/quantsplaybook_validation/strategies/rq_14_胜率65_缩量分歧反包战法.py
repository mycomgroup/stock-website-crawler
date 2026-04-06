# 胜率65%缩量分歧反包战法 - RiceQuant版本
# 逻辑：选近期有涨停后出现缩量分歧（成交量萎缩）的股票，等待反包

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
        df = factor_df.groupby(level=0).last().dropna()
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
    context.stock_num = 5
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
            bars = history_bars(stock, 8, '1d', ['open', 'close', 'high', 'volume', 'limit_up'])
            if bars is None or len(bars) < 6:
                continue
            latest = bars[-1]
            prev = bars[-2]
            latest_close = float(latest['close'])
            latest_limit = float(latest['limit_up']) if latest['limit_up'] is not None else 0
            prev_close = float(prev['close'])
            prev_limit = float(prev['limit_up']) if prev['limit_up'] is not None else 0
            if prev_limit <= 0 or prev_close < prev_limit * 0.995:
                continue
            if latest_limit > 0 and latest_close >= latest_limit * 0.995:
                continue
            latest_vol = float(latest['volume'])
            prev_vol = float(prev['volume'])
            if latest_vol >= prev_vol * 0.75:
                continue
            if latest_close < prev_close * 0.94:
                continue
            score = prev_vol / max(latest_vol, 1) + latest_close / max(prev_close, 1e-6)
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
        today_limit = getattr(bar, 'limit_up', None)
        last_price = getattr(bar, 'close', None)
        if today_limit is None or last_price is None:
            continue
        if (
            bar.close > bar.open and
            bar.close > prev_close * 1.05 and
            bar.close < today_limit * 0.995
        ):
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
