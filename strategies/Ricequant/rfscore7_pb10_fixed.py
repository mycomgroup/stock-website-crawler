# RFScore7 + PB10% 策略修复版
# 问题: scheduler.run_monthly 可能不触发
# 修复: 添加 handle_bar 每日检查是否需要调仓

import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


def init(context):
    context.benchmark = "000300.XSHG"
    context.ipo_days = 180
    context.base_hold_num = 20
    context.reduced_hold_num = 10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
    context.primary_pb_group = 1
    context.reduced_pb_group = 2
    context.last_market_state = {}
    context.last_rebalance = None  # 上次调仓日期

    logger.info("RFScore strategy initialized")


def handle_bar(context, bar_dict):
    """每日检查是否需要调仓"""
    context.bar_dict = bar_dict
    today = context.now.date()

    # 每月第一个交易日调仓
    if context.last_rebalance is None or today.month != context.last_rebalance.month:
        logger.info(f"Monthly rebalance triggered: {today}")
        rebalance(context, bar_dict)
        context.last_rebalance = today


def get_universe(context):
    bar_dict = context.bar_dict

    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
    except Exception as e:
        logger.warning(f"Failed to get index components: {e}")
        return []

    stocks = [s for s in stocks if not s.startswith("688")]

    final_stocks = []
    for stock in stocks:
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if bar.is_trading is False:
            continue
        try:
            inst = instruments(stock)
            if "ST" in inst.symbol or "*" in inst.symbol:
                continue
            final_stocks.append(stock)
        except Exception:
            continue

    logger.info(f"Universe size: {len(final_stocks)}")
    return final_stocks


def calc_market_state(context):
    bar_dict = context.bar_dict

    try:
        hs300 = index_components("000300.XSHG")
    except Exception:
        return {"breadth": 0.5, "trend_on": True}

    above_ma20 = 0
    total = 0

    for stock in hs300[:100]:  # 限制数量避免超时
        if stock not in bar_dict:
            continue
        try:
            hist = history_bars(stock, 20, "1d", "close")
            if len(hist) >= 20:
                if hist[-1] > hist.mean():
                    above_ma20 += 1
                total += 1
        except Exception:
            continue

    breadth = above_ma20 / max(total, 1)

    try:
        idx_hist = history_bars("000300.XSHG", 20, "1d", "close")
        trend_on = idx_hist[-1] > idx_hist.mean()
    except Exception:
        trend_on = True

    return {"breadth": breadth, "trend_on": trend_on}


def choose_stocks_simple(context, hold_num):
    """简化版选股: 直接买入沪深300前N只"""
    stocks = get_universe(context)

    if not stocks:
        return []

    # 简单取前 hold_num 只可交易股票
    buyable = []
    for stock in stocks[: hold_num * 2]:
        if stock in context.bar_dict:
            bar = context.bar_dict[stock]
            if bar.is_trading:
                buyable.append(stock)
        if len(buyable) >= hold_num:
            break

    return buyable


def rebalance(context, bar_dict):
    context.bar_dict = bar_dict
    watch_date = context.now.date()

    market_state = calc_market_state(context)
    context.last_market_state = market_state

    logger.info(
        f"Market state: breadth={market_state['breadth']:.2f}, trend={market_state['trend_on']}"
    )

    # 根据市场状态决定仓位
    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        target_stocks = []
        logger.info("Market condition poor, clearing positions")
    else:
        target_stocks = choose_stocks_simple(context, context.base_hold_num)
        logger.info(f"Selected {len(target_stocks)} stocks")

    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    # 等权买入
    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(target_stocks)

    for stock in target_stocks:
        if stock in bar_dict:
            order_target_value(stock, target_value_per_stock)

    logger.info(
        f"Rebalance complete: {len(target_stocks)} stocks, {target_value_per_stock:.0f} each"
    )
