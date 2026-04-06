# 原文链接：https://www.joinquant.com/post/北向Boll带ETF组合宝付费策略
# 策略：北向Boll带_ETF组合宝付费策略
# 核心逻辑：沪深300ETF+BOLL带择时，价格在布林带上轨买入，下轨卖出。

import numpy as np

def calc_boll(p, n=20, k=2):
    ma = np.mean(p[-n:]); std = np.std(p[-n:])
    return ma + k * std, ma, ma - k * std

def init(context):
    context.etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.boll_n = 20
    context.in_market = False
    scheduler.run_daily(check_signal, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def check_signal(context, bar_dict):
    prices = history_bars(context.etf, context.boll_n + 5, '1d', 'close')
    if len(prices) < context.boll_n:
        return

    upper, mid, lower = calc_boll(prices, context.boll_n, 2)
    current_price = prices[-1]

    if current_price > upper and not context.in_market:
        # 突破上轨，买入ETF
        if context.bond_etf in context.portfolio.positions:
            order_target_value(context.bond_etf, 0)
        order_target_value(context.etf, context.portfolio.total_value * 0.95)
        context.in_market = True
        logger.info(f"价格{current_price:.2f}突破上轨{upper:.2f}，买入{context.etf}")

    elif current_price < lower and context.in_market:
        # 跌破下轨，卖出ETF，持债
        order_target_value(context.etf, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        context.in_market = False
        logger.info(f"价格{current_price:.2f}跌破下轨{lower:.2f}，切换债券ETF")
