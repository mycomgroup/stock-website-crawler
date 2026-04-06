# 原文链接：https://www.joinquant.com/post/52xxx
# 策略：龙头战法之单阳不破
# 核心逻辑：选前日大阳线（涨幅>5%）且今日未跌破昨日开盘价的股票，持有至跌破止损

import numpy as np

HOLD_NUM = 5
BIG_YANG_RATIO = 0.05   # 大阳线涨幅阈值

def init(context):
    context.entry_prices = {}
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=30))
    scheduler.run_daily(check_stop, time_rule=market_open(minute=60))

def handle_bar(context, bar_dict):
    pass

def select_stocks(context, bar_dict):
    """选大阳线后未破位的股票"""
    stocks = index_components('000300.XSHG')
    candidates = []

    for stock in stocks:
        try:
            closes = history_bars(stock, 3, '1d', 'close')
            opens = history_bars(stock, 3, '1d', 'open')
            if len(closes) < 3 or len(opens) < 3:
                continue
            # 前日大阳线
            prev_ret = (closes[-2] - closes[-3]) / closes[-3]
            if prev_ret < BIG_YANG_RATIO:
                continue
            # 今日未跌破昨日开盘价
            if closes[-1] >= opens[-2]:
                candidates.append(stock)
        except Exception:
            continue

    new_stocks = [s for s in candidates if s not in context.portfolio.positions]
    if not new_stocks:
        return

    new_stocks = new_stocks[:HOLD_NUM]
    value_per = context.portfolio.cash * 0.9 / len(new_stocks)

    for stock in new_stocks:
        order_target_value(stock, value_per)
        try:
            context.entry_prices[stock] = bar_dict[stock].close
        except Exception:
            pass
        logger.info(f"买入单阳不破 {stock}")

def check_stop(context, bar_dict):
    """跌破昨日开盘价止损"""
    for stock in list(context.portfolio.positions.keys()):
        try:
            opens = history_bars(stock, 2, '1d', 'open')
            closes = history_bars(stock, 1, '1d', 'close')
            if len(opens) < 2 or len(closes) < 1:
                continue
            if closes[-1] < opens[-2]:
                order_target_value(stock, 0)
                logger.info(f"{stock} 跌破昨日开盘价，止损卖出")
        except Exception:
            continue
