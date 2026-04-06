# 原文链接：https://www.joinquant.com/post/49xxx
# 策略：动量策略年化62%
# 核心逻辑：选近20日涨幅最强的股票（动量因子），月度调仓，持仓10只

import numpy as np

HOLD_NUM = 10
MOMENTUM_DAYS = 20

def init(context):
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    stocks = index_components('000300.XSHG')
    momentum_scores = {}

    for stock in stocks:
        try:
            closes = history_bars(stock, MOMENTUM_DAYS + 1, '1d', 'close')
            if len(closes) < MOMENTUM_DAYS + 1:
                continue
            momentum = (closes[-1] - closes[0]) / closes[0]
            momentum_scores[stock] = momentum
        except Exception:
            continue

    if not momentum_scores:
        return

    sorted_stocks = sorted(momentum_scores, key=momentum_scores.get, reverse=True)
    top_stocks = sorted_stocks[:HOLD_NUM]
    value_per = context.portfolio.cash / len(top_stocks)

    for stock in top_stocks:
        order_target_value(stock, value_per)
        logger.info(f"买入 {stock}，动量 {momentum_scores[stock]:.4f}")
