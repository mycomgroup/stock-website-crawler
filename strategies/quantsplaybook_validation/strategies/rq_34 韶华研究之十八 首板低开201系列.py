# 原文链接：https://www.joinquant.com/post/韶华研究之十八首板低开201系列
# 策略：韶华研究之十八 首板低开201系列
# 核心逻辑：选首次涨停（首板）后低开的股票，次日开盘买入，持有1-3天。

import numpy as np

def init(context):
    context.n_stocks = 3
    context.hold_days = {}  # 记录持仓天数
    context.max_hold = 3    # 最多持有3天
    scheduler.run_daily(morning_buy, time_rule=market_open(minute=5))
    scheduler.run_daily(check_sell, time_rule=market_open(minute=2))

def handle_bar(context, bar_dict):
    pass

def check_sell(context, bar_dict):
    """检查持仓天数，超过最大持有天数则卖出"""
    to_sell = []
    for s in list(context.portfolio.positions.keys()):
        days = context.hold_days.get(s, 0)
        if days >= context.max_hold:
            to_sell.append(s)
        else:
            context.hold_days[s] = days + 1

    for s in to_sell:
        order_target_value(s, 0)
        context.hold_days.pop(s, None)
        logger.info(f"持有{context.max_hold}天，卖出: {s}")

def morning_buy(context, bar_dict):
    """选首板低开股票买入"""
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    candidates = []
    for s in stocks[:500]:
        try:
            prices = history_bars(s, 5, '1d', 'close')
            if len(prices) < 5:
                continue

            # 昨日涨停（首板：前日未涨停，昨日涨停）
            yesterday_ret = (prices[-1] - prices[-2]) / prices[-2]
            prev_ret = (prices[-2] - prices[-3]) / prices[-3]
            if yesterday_ret < 0.095 or prev_ret >= 0.095:
                continue  # 不是首板

            # 今日低开
            if s not in bar_dict:
                continue
            today_open = bar_dict[s].open
            open_ret = (today_open - prices[-1]) / prices[-1]
            if -0.05 < open_ret < -0.01:  # 低开1%-5%
                candidates.append((s, open_ret))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1])  # 低开幅度排序
    new_buys = [s for s, _ in candidates[:context.n_stocks]]

    # 只买入新股票
    current_positions = set(context.portfolio.positions.keys())
    to_buy = [s for s in new_buys if s not in current_positions]

    if not to_buy:
        return

    cash_budget = context.portfolio.cash * 0.9
    value = cash_budget / len(to_buy)
    for s in to_buy:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
            context.hold_days[s] = 0
    logger.info(f"首板低开买入: {to_buy}")
