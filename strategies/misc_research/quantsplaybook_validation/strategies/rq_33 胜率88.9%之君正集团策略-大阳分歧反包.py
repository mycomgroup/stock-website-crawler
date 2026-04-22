# 原文链接：https://www.joinquant.com/post/胜率88.9之君正集团策略大阳分歧反包
# 策略：胜率88.9%之君正集团策略-大阳分歧反包
# 核心逻辑：选前日大阳线（涨幅>5%）今日低开（开盘跌幅>-2%）的股票，开盘买入，次日卖出。

import numpy as np

def init(context):
    context.n_stocks = 3
    context.hold_stocks = []
    # 每日开盘后5分钟选股买入
    scheduler.run_daily(morning_buy, time_rule=market_open(minute=5))
    # 次日开盘卖出（持有1天）
    scheduler.run_daily(morning_sell, time_rule=market_open(minute=1))

def handle_bar(context, bar_dict):
    pass

def morning_sell(context, bar_dict):
    """次日开盘卖出昨日买入的股票"""
    for s in list(context.portfolio.positions.keys()):
        order_target_value(s, 0)
    logger.info("大阳分歧反包：次日开盘清仓")

def morning_buy(context, bar_dict):
    """选前日大阳线今日低开的股票"""
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    candidates = []
    for s in stocks[:500]:
        try:
            prices = history_bars(s, 3, '1d', 'close')
            if len(prices) < 3:
                continue
            # 前日大阳线：涨幅>5%
            prev_ret = (prices[-1] - prices[-2]) / prices[-2]
            if prev_ret < 0.05:
                continue
            # 今日低开：开盘跌幅>-2%（相对昨收）
            if s not in bar_dict:
                continue
            today_open = bar_dict[s].open
            open_ret = (today_open - prices[-1]) / prices[-1]
            if open_ret < -0.02 and open_ret > -0.08:
                candidates.append((s, prev_ret, open_ret))
        except Exception:
            continue

    # 按前日涨幅排序
    candidates.sort(key=lambda x: x[1], reverse=True)
    target = [s for s, _, _ in candidates[:context.n_stocks]]

    if not target:
        return

    value = context.portfolio.cash * 0.9 / len(target)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"大阳分歧反包买入: {target}")
