# 龙回头策略v3.0 - RiceQuant版本
# 原文：收益狂飙，年化收益100%，11年1700倍，绝无未来函数
# 逻辑：选中小综指成分股中，近期有涨停记录后回调的"龙回头"股票

import numpy as np


def init(context):
    context.stock_num = 5
    context.candidates = []
    scheduler.run_daily(my_trade, time_rule=market_open(minute=35))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def my_trade(context, bar_dict):
    instruments_df = all_instruments('CS')
    if 'status' in instruments_df.columns:
        instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = index_components('399101.XSHE')
    if not stocks:
        stocks = [s for s in instruments_df['order_book_id'].tolist()
                  if not s.startswith(('688', '4', '8'))][:500]

    # 龙回头：近10日内有涨停，且当前价格回调到涨停日收盘价附近
    candidates = []
    for stock in stocks:
        try:
            closes = history_bars(stock, 15, '1d', 'close')
            if closes is None or len(closes) < 15:
                continue
            closes = np.array(closes, dtype=float)

            # 检查近10日是否有涨停（涨幅>=9.5%）
            has_limit_up = False
            limit_up_idx = -1
            for i in range(1, 11):
                if closes[-i] / closes[-i-1] >= 1.095:
                    has_limit_up = True
                    limit_up_idx = len(closes) - i
                    break

            if not has_limit_up:
                continue

            # 当前价格在涨停日收盘价的95%-105%之间（回踩确认）
            limit_up_close = closes[limit_up_idx]
            cur_close = closes[-1]
            if 0.92 <= cur_close / limit_up_close <= 1.02:
                bar = (bar_dict[stock] if stock in bar_dict else None)
                if bar is None or bar.is_trading:
                    candidates.append(stock)
        except Exception:
            continue

    if not candidates:
        return

    target = candidates[:context.stock_num]

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def after_market_close(context, bar_dict):
    # 止损：持仓跌幅超过7%卖出（after_market_close无bar_dict，用history_bars取收盘价）
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bars = history_bars(stock, 1, '1d', 'close')
        if bars is None or len(bars) == 0:
            continue
        close = bars[-1]
        avg_cost = getattr(pos, 'avg_cost', getattr(pos, 'avg_price', 0))
        pnl = close / avg_cost - 1 if avg_cost > 0 else 0
        if pnl < -0.07:
            order_target_value(stock, 0)
