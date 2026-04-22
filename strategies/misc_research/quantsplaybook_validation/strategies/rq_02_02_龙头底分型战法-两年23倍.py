# 龙头底分型战法 - RiceQuant版本
# 逻辑：识别底分型（三根K线形态：中间K线最低），选近期出现底分型的强势股

import numpy as np


def init(context):
    context.stock_num = 5
    context.candidates = []
    context.last_week_date = None
    scheduler.run_daily(update_pool, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=5))
    scheduler.run_daily(stop_loss, time_rule=market_open(minute=210))


def handle_bar(context, bar_dict):
    pass


def has_bottom_fractal(closes):
    """检测近期是否有底分型（中间K线最低）"""
    if len(closes) < 5:
        return False
    for i in range(2, len(closes) - 1):
        if closes[i] < closes[i-1] and closes[i] < closes[i+1]:
            # 底分型后价格反弹
            if closes[-1] > closes[i] * 1.02:
                return True
    return False


def update_pool(context, bar_dict):
    today_key = context.now.strftime('%Y-%m-%d')
    if today_key == context.last_week_date:
        return

    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    all_stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in all_stocks
              if not s.startswith(('688', '4', '8', '3'))]

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
        df = df[df['market_cap'] > 1e+09]
        df = df[df['market_cap'] < 2e+10]
        df = df.sort_values('market_cap')
        df = df.head(context.stock_num * 3)
        candidates = df.index.tolist()
    except Exception:
        return
    result = []
    for stock in candidates:
        try:
            closes = history_bars(stock, 10, '1d', 'close')
            if closes is None or len(closes) < 10:
                continue
            closes = np.array(closes, dtype=float)
            if has_bottom_fractal(closes):
                result.append(stock)
        except Exception:
            continue

    context.candidates = result[:context.stock_num * 3]
    context.last_week_date = today_key


def trade(context, bar_dict):
    if not context.candidates:
        return

    target = [s for s in context.candidates if (bar_dict[s] if s in bar_dict else None) and bar_dict[s].is_trading][:context.stock_num]

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
        if bar.close / pos.avg_cost - 1 < -0.06:
            order_target_value(stock, 0)
