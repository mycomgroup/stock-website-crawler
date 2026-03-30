# 增强策略 - 四档仓位调整
# 根据市场趋势调整持仓数量：15/12/10/0


import numpy as np


def init(context):
    context.benchmark = "000300.XSHG"
    context.base_hold_num = 15
    context.defensive_hold_num = 12
    context.bottom_hold_num = 10
    context.extreme_hold_num = 0
    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now

    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month

    logger.info(f"Monthly rebalance: {today}")

    stocks = get_universe(context)
    if not stocks:
        return

    market_state = calc_market_state(context)
    hold_num = get_hold_num(context, market_state)

    logger.info(
        f"Market state: breadth={market_state['breadth']:.2f}, trend={market_state['trend_on']}, hold_num={hold_num}"
    )

    if hold_num == 0:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    picks = choose_stocks(context, stocks, hold_num)

    logger.info(f"Selected {len(picks)} stocks")

    for stock in list(context.portfolio.positions.keys()):
        if stock not in picks:
            order_target_value(stock, 0)

    if picks:
        target_value = context.portfolio.total_value / len(picks)
        for stock in picks:
            order_target_value(stock, target_value)


def get_universe(context):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]
        return stocks[:100]
    except Exception as e:
        logger.warning(f"get_universe failed: {e}")
        return []


def calc_market_state(context):
    try:
        idx_bars = history_bars("000300.XSHG", 20, "1d", "close")
        if idx_bars is None or len(idx_bars) < 20:
            return {"breadth": 0.5, "trend_on": True}

        idx_close = idx_bars[-1]
        idx_ma20 = np.mean(idx_bars)
        trend_on = idx_close > idx_ma20

        hs300 = index_components("000300.XSHG")
        above_ma20 = 0
        total = 0

        for stock in hs300[:30]:
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

        return {"breadth": breadth, "trend_on": trend_on}
    except Exception as e:
        logger.warning(f"calc_market_state failed: {e}")
        return {"breadth": 0.5, "trend_on": True}


def get_hold_num(context, market_state):
    breadth = market_state["breadth"]
    trend_on = market_state["trend_on"]

    if breadth < 0.15:
        return context.extreme_hold_num
    elif breadth < 0.25 and not trend_on:
        return context.bottom_hold_num
    elif breadth < 0.40 and not trend_on:
        return context.defensive_hold_num
    else:
        return context.base_hold_num


def choose_stocks(context, stocks, hold_num):
    results = []

    for stock in stocks:
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
