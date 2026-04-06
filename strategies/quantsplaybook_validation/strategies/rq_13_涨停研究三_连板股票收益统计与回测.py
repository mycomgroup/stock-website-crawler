# 涨停研究三_连板股票收益统计与回测 - RiceQuant版本
# 逻辑：选近期有连板（2-3板）记录的股票，统计连板后收益，日度交易

import numpy as np


def _build_stock_pool(min_cap=5, max_cap=80, max_size=500):
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

    pool = _build_stock_pool(min_cap=5, max_cap=80, max_size=500)
    result = []
    for stock in pool:
        try:
            bars = history_bars(stock, 8, '1d', ['close', 'limit_up'])
            if bars is None or len(bars) < 6:
                continue
            limit_count = sum(
                1 for row in bars[-6:]
                if row['limit_up'] is not None and float(row['close']) >= float(row['limit_up']) * 0.995
            )
            if 2 <= limit_count <= 3:
                score = limit_count + float(bars[-1]['close']) / max(float(bars[-3]['close']), 1e-6)
                result.append((score, stock))
        except Exception:
            continue

    result.sort(key=lambda x: x[0], reverse=True)
    context.candidates = [s for _, s in result[:context.stock_num * 12]]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        daily = history_bars(stock, 2, '1d', ['close'])
        if daily is None or len(daily) < 2:
            continue
        prev_close = float(daily[-1]['close'])
        if 0.97 <= bar.open / max(prev_close, 1e-6) <= 1.05 and bar.close > bar.open:
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
