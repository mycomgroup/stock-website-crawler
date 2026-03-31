# RiceQuant 简化策略 - 调试版
# 直接使用 history_bars 获取数据，不用 get_factor

import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.hold_num = 10
    scheduler.run_monthly(rebalance, tradingday=1)


def rebalance(context, bar_dict):
    """月度调仓"""
    logger.info(f"=== rebalance on {context.now.date()} ===")

    # 获取沪深300成分股
    try:
        stocks = index_components("000300.XSHG")
        logger.info(f"Got {len(stocks)} stocks from HS300")
    except Exception as e:
        logger.warning(f"index_components failed: {e}")
        stocks = []

    if len(stocks) < 10:
        logger.warning("Not enough stocks")
        return

    # 过滤
    valid = []
    for s in stocks:
        if s.startswith("688"):
            continue
        if s not in bar_dict:
            continue
        bar = bar_dict[s]
        if not bar.is_trading:
            continue
        try:
            inst = instruments(s)
            if "ST" in inst.symbol or "*" in inst.symbol:
                continue
        except:
            pass
        valid.append(s)

    logger.info(f"Valid stocks: {len(valid)}")

    if len(valid) < 5:
        return

    # 简单选择：价格最低的 N 只（模拟低 PB）
    prices = []
    for s in valid[:100]:
        try:
            bar = bar_dict[s]
            prices.append((s, bar.close))
        except:
            pass

    # 按价格排序，选最低的
    prices.sort(key=lambda x: x[1])
    selected = [p[0] for p in prices[: context.hold_num]]

    logger.info(f"Selected {len(selected)} stocks")

    # 清仓
    for s in list(context.portfolio.positions.keys()):
        if s not in selected:
            order_target_value(s, 0)

    # 买入
    if selected:
        per_stock = context.portfolio.total_value / len(selected)
        for s in selected:
            order_target_value(s, per_stock)
        logger.info(f"Bought {len(selected)} stocks")
