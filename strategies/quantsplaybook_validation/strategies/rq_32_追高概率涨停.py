# 追高概率涨停策略 - RiceQuant版本
# 逻辑：选近期有涨停记录、价格适中的股票，周度筛选，日内买入

import numpy as np
import datetime


def init(context):
    context.buy_count = 3
    context.candidates = []
    context.week = -1
    scheduler.run_weekly(prepare_stock_list, weekday=1, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=5))
    scheduler.run_daily(check_stop_loss, time_rule=market_open(minute=180))


def handle_bar(context, bar_dict):
    pass


def has_recent_limit_up(stock, days=5):
    """检查近N天是否有涨停"""
    try:
        closes = history_bars(stock, days + 1, '1d', 'close')
        if closes is None or len(closes) < days + 1:
            return False
        closes = np.array(closes, dtype=float)
        for i in range(1, len(closes)):
            if closes[i] / closes[i-1] >= 1.095:
                return True
        return False
    except Exception:
        return False


def prepare_stock_list(context, bar_dict):
    current_week = context.now.isocalendar()[1]
    if current_week == context.week:
        return

    instruments_df = all_instruments('CS')
    instruments_df = instruments_df[instruments_df['status'] == 'Active']
    stocks = instruments_df['order_book_id'].tolist()
    stocks = [s for s in stocks
              if not s.startswith(('688', '4', '8', '3'))]

    candidates = []
    try:
        for stock in stocks[:1000]:
            if has_recent_limit_up(stock, days=10):
                candidates.append(stock)
            if len(candidates) >= context.buy_count * 10:
                break
    except Exception:
        pass

    if not candidates:
        return
    context.candidates = candidates[:context.buy_count * 5]
    context.week = current_week


def market_open_trade(context, bar_dict):
    if not context.candidates:
        return

    target = []
    for stock in context.candidates:
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        prices = history_bars(stock, 2, '1d', 'close')
        if prices is None or len(prices) < 2:
            continue
        change = bar.close / prices[-2] - 1
        if 0 < change < 0.05:
            target.append(stock)
        if len(target) >= context.buy_count:
            break

    if not target:
        return

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target:
            order_target_value(stock, 0)

    weight = 1.0 / len(target)
    for stock in target:
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)


def check_stop_loss(context, bar_dict):
    """止损：持仓跌幅超过5%卖出"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(stock)
        if pos is None:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None:
            continue
        cost = getattr(pos, 'avg_price', 0)
        if cost <= 0:
            continue
        loss = bar.close / cost - 1
        if loss < -0.05:
            order_target_value(stock, 0)
