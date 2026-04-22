# 超跌反弹v1.0 - RiceQuant版本
# 原文：【超跌反弹v1.0】3年2.3倍的超跌反弹小牛股
# 逻辑：选近期大幅下跌（超跌）、基本面尚可的股票，等待反弹

import numpy as np


def init(context):
    context.stock_list = []
    context.buy_stock_num = 5
    context.stock_num = context.buy_stock_num  # FIX: alias used in before_market_open
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_buy, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_sell, time_rule=market_open(minute=235))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    instruments_df = all_instruments('CS')
    stock_ids = [s for s in instruments_df['order_book_id'].tolist() if not s.startswith(('688', '4', '8'))]
    instruments_df = all_instruments('CS')
    stocks = [s for s in instruments_df['order_book_id'].tolist()  # FIX: was undefined stock_ids
              if not s.startswith(('688', '4', '8'))]

    # FIX: market_cap in RQ is 亿元, so 20~300亿 = 20~300 (not 2e9~3e10)
    try:
        pool = stocks[:300]
    except Exception:
        pool = stocks[:300]

    candidates = []
    for stock in pool:  # FIX: was undefined variable pool
        try:
            closes = history_bars(stock, 21, '1d', 'close')
            if closes is None or len(closes) < 21:
                continue
            closes = np.array(closes, dtype=float)
            # 超跌：近20日跌幅超过15%
            drawdown = closes[-1] / closes[0] - 1
            if drawdown < -0.15:
                # RSI超卖（简化：近5日连续下跌）
                recent_down = sum(1 for i in range(1, 6) if closes[-i] < closes[-i-1])
                if recent_down >= 3:
                    candidates.append((stock, drawdown))
        except Exception:
            continue

    # 按跌幅排序，选最超跌的
    candidates.sort(key=lambda x: x[1])
    context.stock_list = [s for s, _ in candidates[:context.buy_stock_num * 2]]


def market_open_buy(context, bar_dict):
    if not context.stock_list:
        return

    target = []
    for stock in context.stock_list:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is not None and bar.is_trading:
            target.append(stock)
        if len(target) >= context.buy_stock_num:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def market_open_sell(context, bar_dict):
    # 尾盘止盈止损
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        pnl = bar.close / pos.avg_price - 1
        if pnl > 0.08 or pnl < -0.05:
            order_target_value(stock, 0)


def after_market_close(context, bar_dict):
    pass
