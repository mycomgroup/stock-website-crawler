# RFScore 策略 - 简化版
# 修复: 使用 traded 标志位确保首次执行

import pandas as pd
import numpy as np


def init(context):
    context.traded = False
    context.benchmark = "000300.XSHG"
    context.hold_num = 10
    logger.info("RFScore simple strategy initialized")


def handle_bar(context, bar_dict):
    """每月初调仓"""
    today = context.now

    # 简单判断: 每月前3个交易日都尝试调仓
    if context.traded and today.day > 3:
        return

    # 每月重置 traded 标志
    if today.day <= 3:
        context.traded = False

    if context.traded:
        return

    context.traded = True
    logger.info(f"Rebalance on {today.date()}")

    # 获取股票池
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        logger.info(f"Total stocks: {len(stocks)}")
    except Exception as e:
        logger.error(f"index_components error: {e}")
        stocks = ["000001.XSHE"]

    # 过滤可交易股票
    buyable = []
    for stock in stocks:
        if stock.startswith("688"):  # 跳过科创板
            continue
        if stock not in bar_dict:
            continue
        bar = bar_dict[stock]
        if hasattr(bar, "is_trading") and not bar.is_trading:
            continue
        buyable.append(stock)
        if len(buyable) >= context.hold_num * 2:
            break

    if not buyable:
        logger.warning("No buyable stocks, buying 000001.XSHE")
        order_target_percent("000001.XSHE", 0.9)
        return

    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in buyable[: context.hold_num]:
            order_target_value(stock, 0)

    # 等权买入
    target = buyable[: context.hold_num]
    value_each = context.portfolio.total_value / len(target)

    for stock in target:
        order_target_value(stock, value_each)

    logger.info(f"Bought {len(target)} stocks, {value_each:.0f} each")
