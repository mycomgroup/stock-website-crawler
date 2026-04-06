# 原文链接：https://www.joinquant.com/post/追高概率涨停策略2022年化350
# 策略：追高概率涨停策略, 2022年化350%
# 核心逻辑：选昨日涨停且今日高开的股票，开盘后5分钟买入，收盘前卖出（日内）。

import numpy as np

def init(context):
    context.n_stocks = 3
    context.buy_stocks = []
    # 开盘后5分钟买入
    scheduler.run_daily(morning_buy, time_rule=market_open(minute=5))
    # 收盘前10分钟卖出
    scheduler.run_daily(afternoon_sell, time_rule=market_close(minute=10))

def handle_bar(context, bar_dict):
    pass

def morning_buy(context, bar_dict):
    context.buy_stocks = []
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    candidates = []
    for s in stocks[:500]:
        try:
            prices = history_bars(s, 3, '1d', 'close')
            opens = history_bars(s, 2, '1d', 'open')
            if len(prices) < 3 or len(opens) < 2:
                continue
            # 昨日涨停（涨幅接近10%）
            yesterday_ret = (prices[-1] - prices[-2]) / prices[-2]
            if yesterday_ret < 0.095:
                continue
            # 今日高开（开盘涨幅>0）
            if s not in bar_dict:
                continue
            today_open = bar_dict[s].open
            today_open_ret = (today_open - prices[-1]) / prices[-1]
            if today_open_ret > 0:
                candidates.append((s, today_open_ret))
        except Exception:
            continue

    candidates.sort(key=lambda x: x[1], reverse=True)
    context.buy_stocks = [s for s, _ in candidates[:context.n_stocks]]

    if not context.buy_stocks:
        return
    value = context.portfolio.cash * 0.9 / len(context.buy_stocks)
    for s in context.buy_stocks:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"日内买入涨停高开股: {context.buy_stocks}")

def afternoon_sell(context, bar_dict):
    # 收盘前全部卖出
    for s in list(context.portfolio.positions.keys()):
        order_target_value(s, 0)
    logger.info("日内策略收盘前清仓")
