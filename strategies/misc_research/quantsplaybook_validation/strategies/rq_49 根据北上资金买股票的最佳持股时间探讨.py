# 原文链接：https://www.joinquant.com/post/49xxx
# 策略：根据北上资金买股票的最佳持股时间探讨
# 核心逻辑：选沪深港通标的中近期涨幅强的股票，持有固定天数（5/10/20日）后卖出

import numpy as np

HOLD_DAYS = 10       # 持有天数
HOLD_NUM = 10
MOMENTUM_DAYS = 20

def init(context):
    context.hold_counter = {}  # 记录每只股票持有天数
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(check_hold_days, time_rule=market_open(minute=5))

def handle_bar(context, bar_dict):
    pass

def check_hold_days(context, bar_dict):
    """检查持有天数，到期卖出"""
    for stock in list(context.portfolio.positions.keys()):
        context.hold_counter[stock] = context.hold_counter.get(stock, 0) + 1
        if context.hold_counter[stock] >= HOLD_DAYS:
            order_target_value(stock, 0)
            del context.hold_counter[stock]
            logger.info(f"{stock} 持有 {HOLD_DAYS} 天，卖出")

def rebalance(context, bar_dict):
    # 获取沪深港通标的（用沪深300代理）
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
    top_stocks = [s for s in sorted_stocks[:HOLD_NUM] if s not in context.portfolio.positions]

    if not top_stocks:
        return

    value_per = context.portfolio.cash * 0.9 / len(top_stocks)
    for stock in top_stocks:
        order_target_value(stock, value_per)
        context.hold_counter[stock] = 0
        logger.info(f"买入 {stock}，动量 {momentum_scores[stock]:.4f}")
