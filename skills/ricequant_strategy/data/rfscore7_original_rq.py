# RFScore7 PB10% 原始策略 (RiceQuant API 兼容版)
# 基于成功的简化模板，添加市场状态判断


import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.ipo_days = 180
    context.base_hold_num = 20
    context.reduced_hold_num = 10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
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

    market_state = calc_market_state(context, bar_dict)

    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        hold_num = 0
        picks = []
        logger.info(f"Market extreme, empty position")
    elif (
        market_state["breadth"] < context.breadth_reduce
        and not market_state["trend_on"]
    ):
        hold_num = context.reduced_hold_num
        picks = choose_stocks(context, bar_dict, stocks, hold_num)
        logger.info(f"Market weak, reduced position: {hold_num}")
    else:
        hold_num = context.base_hold_num
        picks = choose_stocks(context, bar_dict, stocks, hold_num)
        logger.info(f"Market normal, full position: {hold_num}")

    logger.info(f"Selected {len(picks)} stocks, breadth={market_state['breadth']:.2f}")

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


def calc_market_state(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")

        above_ma20 = 0
        total = 0

        for stock in hs300[:50]:
            try:
                bars = history_bars(stock, 20, "1d", "close")
                if bars is None or len(bars) < 20:
                    continue
                if bars[-1] > np.mean(bars):
                    above_ma20 += 1
                total += 1
            except Exception:
                continue

        breadth = above_ma20 / max(total, 1)

        idx_bars = history_bars("000300.XSHG", 20, "1d", "close")
        trend_on = (
            idx_bars[-1] > np.mean(idx_bars)
            if idx_bars and len(idx_bars) >= 20
            else False
        )

        return {"breadth": breadth, "trend_on": trend_on}
    except Exception as e:
        logger.warning(f"calc_market_state failed: {e}")
        return {"breadth": 0.5, "trend_on": True}


def choose_stocks(context, bar_dict, stocks, hold_num):
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
                results.append({"code": stock, "momentum": momentum})
        except Exception:
            continue

    results.sort(key=lambda x: -x["momentum"])

    return [r["code"] for r in results[:hold_num]]
