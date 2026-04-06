# 原文链接：https://www.joinquant.com/post/50xxx
# 策略：【7日趋势】短线交易策略
# 核心逻辑：7日趋势策略，选近7日持续上涨（每日收盘价高于前日）的股票，短线持有

import numpy as np

HOLD_NUM = 5
TREND_DAYS = 7

def init(context):
    context.hold_days = {}
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 更新持有天数，超过7天卖出
    for stock in list(context.portfolio.positions.keys()):
        context.hold_days[stock] = context.hold_days.get(stock, 0) + 1
        if context.hold_days[stock] >= TREND_DAYS:
            order_target_value(stock, 0)
            del context.hold_days[stock]
            logger.info(f"{stock} 持有7天，卖出")

    stocks = index_components('000300.XSHG')
    candidates = []

    for stock in stocks:
        try:
            closes = history_bars(stock, TREND_DAYS + 1, '1d', 'close')
            if len(closes) < TREND_DAYS + 1:
                continue
            # 检查近7日是否持续上涨
            is_trend = all(closes[i] > closes[i - 1] for i in range(1, TREND_DAYS + 1))
            if is_trend:
                candidates.append(stock)
        except Exception:
            continue

    # 过滤已持仓
    new_stocks = [s for s in candidates if s not in context.portfolio.positions]
    if not new_stocks:
        return

    new_stocks = new_stocks[:HOLD_NUM]
    value_per = context.portfolio.cash * 0.9 / len(new_stocks)

    for stock in new_stocks:
        order_target_value(stock, value_per)
        context.hold_days[stock] = 0
        logger.info(f"买入7日趋势股 {stock}")
