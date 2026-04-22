# 原文链接：https://www.joinquant.com/post/46977
# 策略：发一个学习策略5年70倍，思路可以学习
# 作者：xxzlw
# 核心逻辑：选小市值股票，盘中涨幅超过6.5%则卖出（高抛），每天买入新标的

import numpy as np

N_STOCKS = 5
SELL_THRESHOLD = 0.065  # 盘中涨幅超过6.5%卖出


def init(context):
    context.n_stocks = N_STOCKS
    context.muster = []
    scheduler.run_daily(prepare, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=30))
    scheduler.run_daily(sell_check, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    pass


def prepare(context, bar_dict):
    """盘前：选小市值低价股"""
    try:
        all_stocks_df = all_instruments('CS')
        all_stocks = [s for s in all_stocks_df['order_book_id'].tolist()
                      if not s.startswith('688') and not s.startswith('8') and not s.startswith('4')]
    except Exception:
        context.muster = []
        return

    valid = []
    for s in all_stocks:
        try:
            inst = instruments(s)
            if inst and (context.now - inst.listed_date).days >= 365:
                valid.append(s)
        except Exception:
            continue

    context.muster = valid[:context.n_stocks * 2]


def buy_stocks(context, bar_dict):
    """开盘后买入"""
    if not context.muster:
        return

    hold = set(context.portfolio.positions.keys())
    slots = context.n_stocks - len(hold)
    if slots <= 0:
        return

    weight = 1.0 / context.n_stocks
    for stock in context.muster:
        if slots <= 0:
            break
        if stock in hold:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
        slots -= 1


def sell_check(context, bar_dict):
    """收盘前：检查涨幅，超过阈值卖出"""
    for s in list(context.portfolio.positions.keys()):
        opens_s = history_bars(s, 2, '1d', 'open')
        closes_s = history_bars(s, 2, '1d', 'close')
        if opens_s is None or closes_s is None or len(opens_s) < 2:
            continue
        today_open = opens_s[-1]
        today_close = closes_s[-1]
        if today_open == 0:
            continue
        gain = (today_close - today_open) / today_open
        if gain > SELL_THRESHOLD:
            order_target_value(s, 0)
