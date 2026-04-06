# 原文链接：https://www.joinquant.com/post/53xxx
# 策略：筹码选股
# 核心逻辑：筹码集中度选股，用近期价格区间集中度（高低价差/均价）作为筹码因子，选筹码集中的股票

import numpy as np

HOLD_NUM = 10
CHIP_WINDOW = 20  # 筹码计算窗口

def calc_chip_concentration(closes, highs, lows):
    """计算筹码集中度：高低价差/均价，越小越集中"""
    price_range = np.max(highs[-CHIP_WINDOW:]) - np.min(lows[-CHIP_WINDOW:])
    mean_price = np.mean(closes[-CHIP_WINDOW:])
    if mean_price <= 0:
        return float('inf')
    return price_range / mean_price

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    stocks = index_components('000300.XSHG')
    chip_scores = {}

    for stock in stocks:
        try:
            closes = history_bars(stock, CHIP_WINDOW + 2, '1d', 'close')
            highs = history_bars(stock, CHIP_WINDOW + 2, '1d', 'high')
            lows = history_bars(stock, CHIP_WINDOW + 2, '1d', 'low')
            if len(closes) < CHIP_WINDOW:
                continue
            concentration = calc_chip_concentration(closes, highs, lows)
            # 同时要求近期有上涨趋势
            trend = (closes[-1] - closes[-5]) / closes[-5] if closes[-5] > 0 else 0
            if trend > 0:
                chip_scores[stock] = concentration
        except Exception:
            continue

    if not chip_scores:
        return

    # 选筹码最集中（值最小）的股票
    sorted_stocks = sorted(chip_scores, key=chip_scores.get, reverse=False)
    top_stocks = sorted_stocks[:HOLD_NUM]
    value_per = context.portfolio.cash / len(top_stocks)

    for stock in top_stocks:
        order_target_value(stock, value_per)
        logger.info(f"买入筹码集中股 {stock}，集中度 {chip_scores[stock]:.4f}")
