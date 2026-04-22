# 原文链接：https://www.joinquant.com/post/50xxx
# 策略：分享一种K线小碎步后突破的分钟级打法
# 核心逻辑：K线小碎步突破，选近期低波动后放量突破的股票，分钟级买入

import numpy as np

HOLD_NUM = 5
LOW_VOL_DAYS = 10   # 低波动观察期
BREAKOUT_RATIO = 0.03  # 突破幅度

def init(context):
    context.positions_to_sell = {}
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=1))
    scheduler.run_daily(sell_stocks, time_rule=market_open(minute=120))

def handle_bar(context, bar_dict):
    pass

def select_stocks(context, bar_dict):
    """开盘后选股买入"""
    stocks = index_components('000500.XSHG')
    candidates = []

    for stock in stocks:
        try:
            closes = history_bars(stock, LOW_VOL_DAYS + 5, '1d', 'close')
            volumes = history_bars(stock, LOW_VOL_DAYS + 5, '1d', 'volume')
            if len(closes) < LOW_VOL_DAYS + 2:
                continue
            # 近期低波动：标准差/均值 < 2%
            recent_closes = closes[-(LOW_VOL_DAYS + 1):-1]
            vol_ratio = np.std(recent_closes) / np.mean(recent_closes)
            if vol_ratio > 0.02:
                continue
            # 今日突破：收盘价高于近期最高价
            recent_high = np.max(closes[-(LOW_VOL_DAYS + 1):-1])
            if closes[-1] > recent_high * (1 + BREAKOUT_RATIO):
                # 成交量放大
                avg_vol = np.mean(volumes[-(LOW_VOL_DAYS + 1):-1])
                if volumes[-1] > avg_vol * 1.5:
                    candidates.append((stock, closes[-1]))
        except Exception:
            continue

    if not candidates:
        return

    candidates = candidates[:HOLD_NUM]
    value_per = context.portfolio.cash * 0.9 / len(candidates)

    for stock, price in candidates:
        if stock not in context.portfolio.positions:
            order_target_value(stock, value_per)
            context.positions_to_sell[stock] = 1
            logger.info(f"买入突破股 {stock}，价格 {price:.2f}")

def sell_stocks(context, bar_dict):
    """持有2小时后卖出"""
    for stock in list(context.positions_to_sell.keys()):
        order_target_value(stock, 0)
        del context.positions_to_sell[stock]
        logger.info(f"卖出 {stock}")
