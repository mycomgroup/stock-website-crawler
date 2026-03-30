# 简化版 RFScore 策略测试
# RiceQuant API 兼容版本


import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.ipo_days = 180
    context.base_hold_num = 20
    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now

    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month

    logger.info(f"Monthly rebalance: {today}")

    stocks = get_universe(context, bar_dict)

    if not stocks:
        return

    picks = choose_stocks_simple(context, bar_dict, stocks, context.base_hold_num)

    for stock in list(context.portfolio.positions.keys()):
        if stock not in picks:
            order_target_value(stock, 0)

    if picks:
        target_value = context.portfolio.total_value / len(picks)
        for stock in picks:
            order_target_value(stock, target_value)


def get_universe(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]
        return stocks[:100]
    except Exception as e:
        logger.warning(f"get_universe failed: {e}")
        return []


def choose_stocks_simple(context, bar_dict, stocks, hold_num):
    results = []

    for stock in stocks[:50]:
        try:
            bars = history_bars(stock, 20, "1d", "close")
            if bars is None or len(bars) < 20:
                continue

            close = bars[-1]
            ma20 = np.mean(bars)
            momentum = (close / bars[0] - 1) * 100

            if close > ma20 and momentum > 0:
                results.append({"code": stock, "close": close, "momentum": momentum})
        except Exception:
            continue

    results.sort(key=lambda x: -x["momentum"])

    return [r["code"] for r in results[:hold_num]]
