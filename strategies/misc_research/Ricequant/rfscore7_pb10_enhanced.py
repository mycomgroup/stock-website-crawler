# RiceQuant 增强策略 - 修正版

import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.hold_num = 10
    context.breadth_extreme = 0.15
    context.breadth_bottom = 0.25
    context.last_month = -1
    context.in_cash = False

    # 设置股票池
    stocks = index_components("000300.XSHG")
    update_universe(stocks)


def handle_bar(context, bar_dict):
    today = context.now

    # 广度
    breadth = calc_breadth(bar_dict)

    # 极端市场
    if not context.in_cash and breadth < context.breadth_extreme:
        logger.info(f"清仓 breadth={breadth:.2f}")
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        context.in_cash = True
        return

    if context.in_cash and breadth > context.breadth_bottom:
        logger.info(f"恢复 breadth={breadth:.2f}")
        context.in_cash = False

    if context.in_cash:
        return

    # 月度调仓
    if today.month != context.last_month:
        context.last_month = today.month
        rebalance(context, bar_dict)


def rebalance(context, bar_dict):
    stocks = []

    # 从 bar_dict 获取可交易股票
    for s in list(bar_dict.keys()):
        bar = bar_dict[s]
        if not bar.is_trading:
            continue
        if bar.close >= bar.limit_up * 0.98:
            continue
        try:
            inst = instruments(s)
            if "ST" in inst.symbol or "*" in inst.symbol:
                continue
        except:
            pass
        stocks.append(s)

    logger.info(f"rebalance: {len(stocks)} tradable stocks")

    if len(stocks) < 3:
        return

    # 按价格排序选低价股
    prices = [(s, bar_dict[s].close) for s in stocks]
    prices.sort(key=lambda x: x[1])

    selected = [p[0] for p in prices[: context.hold_num]]

    # 清仓
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    # 买入
    per = context.portfolio.total_value / len(selected)
    for s in selected:
        order_value(s, per)

    logger.info(f"bought {len(selected)} stocks")


def calc_breadth(bar_dict):
    count = 0
    above = 0

    for s in list(bar_dict.keys())[:50]:
        try:
            hist = history_bars(s, 20, "1d", "close")
            if hist is not None and len(hist) >= 20:
                count += 1
                if hist[-1] > np.mean(hist):
                    above += 1
        except:
            pass

    return above / max(count, 1) if count > 0 else 0.5
