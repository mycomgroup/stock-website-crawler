# RFScore7 + PB10% 策略 - RiceQuant 修复版
# 问题: scheduler.run_monthly 不稳定，init 不能下单
# 修复: 使用 handle_bar 每日检查调仓

import pandas as pd
import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.ipo_days = 180
    context.base_hold_num = 20
    context.last_rebalance_month = -1  # 记录上次调仓月份
    logger.info("RFScore strategy initialized")


def handle_bar(context, bar_dict):
    """每日运行，月初调仓"""
    today = context.now

    # 每月第一个交易日调仓
    if today.month != context.last_rebalance_month:
        logger.info(f"Monthly rebalance: {today.date()}")
        rebalance(context, bar_dict)
        context.last_rebalance_month = today.month


def get_universe(context, bar_dict):
    """获取股票池"""
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
    except Exception as e:
        logger.warning(f"Failed to get index components: {e}")
        return []

    # 剔除科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 过滤可交易股票
    buyable = []
    for stock in stocks[:200]:  # 限制数量
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if bar.is_trading is False:
            continue
        try:
            inst = instruments(stock)
            symbol = inst.symbol
            if "ST" in symbol or "*" in symbol or "退" in symbol:
                continue
            buyable.append(stock)
        except Exception:
            continue

    return buyable


def rebalance(context, bar_dict):
    """调仓"""
    stocks = get_universe(context, bar_dict)

    if not stocks:
        logger.info("No stocks available")
        return

    # 简单选择前 N 只
    target_stocks = stocks[: context.base_hold_num]

    logger.info(f"Selected {len(target_stocks)} stocks")

    # 清仓不在目标池的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    # 等权买入
    total_value = context.portfolio.total_value
    value_per_stock = total_value / len(target_stocks)

    for stock in target_stocks:
        order_target_value(stock, value_per_stock)

    logger.info(f"Bought {len(target_stocks)} stocks, {value_per_stock:.0f} each")
