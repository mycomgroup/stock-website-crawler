# 原文链接：https://www.joinquant.com/post/年化46的北向资金加20日涨幅的创业板策略
# 策略：年化46%的北向资金+20日涨幅的创业板策略
# 核心逻辑：创业板成分股中选近20日涨幅最强的股票，月度调仓。

import numpy as np

def init(context):
    context.n_stocks = 10
    context.index_code = '399006.XSHE'  # 创业板指
    context.momentum_n = 20
    context.bond_etf = '511010.XSHG'
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 获取创业板成分股
    try:
        cyb_stocks = index_components(context.index_code)
    except Exception:
        cyb_stocks = []

    if not cyb_stocks:
        return

    # 计算近20日涨幅
    mom_list = []
    for s in cyb_stocks:
        try:
            prices = history_bars(s, context.momentum_n + 1, '1d', 'close')
            if len(prices) > context.momentum_n:
                mom = (prices[-1] - prices[0]) / prices[0]
                mom_list.append((s, mom))
        except Exception:
            continue

    if not mom_list:
        return

    # 选涨幅最强的股票
    mom_list.sort(key=lambda x: x[1], reverse=True)
    target = [s for s, _ in mom_list[:context.n_stocks] if mom_list[0][1] > 0]

    if not target:
        # 创业板整体下跌，持债
        for s in list(context.portfolio.positions.keys()):
            if s != context.bond_etf:
                order_target_value(s, 0)
        order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
        logger.info("创业板动量为负，持债")
        return

    if context.bond_etf in context.portfolio.positions:
        order_target_value(context.bond_etf, 0)

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"创业板20日动量选股完成，持仓: {target}")
