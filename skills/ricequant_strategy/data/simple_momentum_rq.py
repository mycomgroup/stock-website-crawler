# 简化版动量策略 (RiceQuant)
# 使用预定义股票池，避免 index_components API 问题


import numpy as np


STOCK_POOL = [
    "600519.XSHG",
    "600036.XSHG",
    "601318.XSHG",
    "600000.XSHG",
    "601166.XSHG",
    "600030.XSHG",
    "601398.XSHG",
    "601288.XSHG",
    "600887.XSHG",
    "600276.XSHG",
    "600016.XSHG",
    "601939.XSHG",
    "601988.XSHG",
    "601328.XSHG",
    "600837.XSHG",
    "600048.XSHG",
    "600104.XSHG",
    "600332.XSHG",
    "600690.XSHG",
    "600309.XSHG",
    "000001.XSHE",
    "000002.XSHE",
    "000333.XSHE",
    "000651.XSHE",
    "000858.XSHE",
    "002415.XSHE",
    "002594.XSHE",
    "000063.XSHE",
    "002304.XSHE",
    "000725.XSHE",
]


def init(context):
    context.benchmark = "000300.XSHG"
    context.stock_pool = STOCK_POOL
    context.hold_num = 10
    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now

    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month
    rebalance(context, bar_dict)


def choose_stocks(context, bar_dict, hold_num):
    results = []

    for stock in context.stock_pool:
        if stock not in bar_dict:
            continue

        try:
            bars = history_bars(stock, 20, "1d", "close")
            if bars is None or len(bars) < 20:
                continue

            close = bars[-1]
            ma20 = np.mean(bars)
            momentum = (close / bars[0] - 1) * 100

            if close > ma20 and momentum > 0:
                results.append({"code": stock, "close": close, "momentum": momentum})
        except Exception as e:
            logger.warning(f"Error for {stock}: {e}")
            continue

    results.sort(key=lambda x: -x["momentum"])

    return [r["code"] for r in results[:hold_num]]


def rebalance(context, bar_dict):
    logger.info(f"Rebalance on {context.now}")

    target_stocks = choose_stocks(context, bar_dict, context.hold_num)

    logger.info(f"Selected {len(target_stocks)} stocks")

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)
            logger.info(f"Sell {stock}")

    if not target_stocks:
        return

    target_value = context.portfolio.total_value / len(target_stocks)

    for stock in target_stocks:
        order_target_value(stock, target_value)
        logger.info(f"Buy {stock} for {target_value:.0f}")
