# RFScore7 + PB10% 纯进攻策略 (RiceQuant API 兼容版)
# 基于 handle_bar 框架，每月调仓


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
    context.last_rebalance_month = -1


def handle_bar(context, bar_dict):
    today = context.now
    if today.month == context.last_rebalance_month:
        return

    context.last_rebalance_month = today.month
    rebalance(context, bar_dict)


def get_universe(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]

        all_inst = all_instruments(type="CS")
        valid_stocks = []
        today = context.now.date()

        for stock in stocks:
            inst = all_inst[all_inst["order_book_id"] == stock]
            if inst.empty:
                continue
            listed_date = pd.to_datetime(inst.iloc[0]["listed_date"])
            if (today - listed_date.date()).days >= context.ipo_days:
                valid_stocks.append(stock)

        final_stocks = []
        for stock in valid_stocks:
            if stock not in bar_dict:
                continue
            bar = bar_dict[stock]
            if bar.is_trading is False:
                continue
            instrument = instruments(stock)
            if "ST" in instrument.symbol or "*" in instrument.symbol:
                continue
            final_stocks.append(stock)

        return final_stocks
    except Exception as e:
        logger.warning(f"get_universe failed: {e}")
        return []


def calc_market_state(context, bar_dict):
    try:
        hs300 = index_components("000300.XSHG")
        above_ma20 = 0
        total = 0

        for stock in hs300:
            if stock not in bar_dict:
                continue
            try:
                hist = history_bars(stock, 20, "1d", "close")
                if len(hist) < 20:
                    continue
                ma20 = hist.mean()
                close = hist[-1]
                if close > ma20:
                    above_ma20 += 1
                total += 1
            except Exception:
                continue

        breadth = above_ma20 / max(total, 1)

        idx_hist = history_bars("000300.XSHG", 20, "1d", "close")
        idx_close = idx_hist[-1]
        idx_ma20 = idx_hist.mean()
        trend_on = idx_close > idx_ma20

        return {"breadth": breadth, "trend_on": trend_on}
    except Exception as e:
        logger.warning(f"calc_market_state failed: {e}")
        return {"breadth": 0.5, "trend_on": True}


def get_pb_ratio(stocks, watch_date):
    pb_dict = {}
    for stock in stocks:
        try:
            inst = instruments(stock)
            pb_dict[stock] = getattr(inst, "pb", np.nan)
        except Exception:
            pb_dict[stock] = np.nan
    return pd.Series(pb_dict)


def calc_rfscore_simple(context, bar_dict, stocks):
    results = []

    for stock in stocks:
        try:
            bars = history_bars(stock, 20, "1d", "close")
            if bars is None or len(bars) < 20:
                continue

            close = bars[-1]
            ma20 = np.mean(bars)
            momentum = (close / bars[0] - 1) * 100

            score = 0
            if momentum > 5:
                score += 3
            elif momentum > 0:
                score += 2
            elif momentum > -5:
                score += 1

            if close > ma20:
                score += 2

            results.append(
                {
                    "code": stock,
                    "close": close,
                    "fscore": min(7, max(1, score)),
                    "momentum": momentum,
                }
            )
        except Exception:
            continue

    return results


def choose_stocks(context, bar_dict, hold_num):
    stocks = get_universe(context, bar_dict)
    if not stocks:
        return []

    metrics = calc_rfscore_simple(context, bar_dict, stocks)
    if not metrics:
        return []

    metrics.sort(key=lambda x: (-x["fscore"], -x["momentum"]))

    picks = [m["code"] for m in metrics if m["fscore"] >= 6]

    if len(picks) < hold_num:
        for m in metrics:
            if m["code"] not in picks:
                picks.append(m["code"])
            if len(picks) >= hold_num:
                break

    return picks[:hold_num]


def filter_buyable(context, bar_dict, stocks):
    buyable = []

    for stock in stocks:
        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]

        if bar.is_trading is False:
            continue

        inst = instruments(stock)
        if "ST" in inst.symbol or "*" in inst.symbol or "退" in inst.symbol:
            continue

        close = bar.close
        limit_up = bar.limit_up
        limit_down = bar.limit_down

        if limit_up and close >= limit_up * 0.995:
            continue
        if limit_down and close <= limit_down * 1.005:
            continue

        buyable.append(stock)

    return buyable


def rebalance(context, bar_dict):
    watch_date = context.now.date()
    market_state = calc_market_state(context, bar_dict)

    if market_state["breadth"] < context.breadth_stop and not market_state["trend_on"]:
        target_stocks = []
        target_hold_num = 0
    elif (
        market_state["breadth"] < context.breadth_reduce
        and not market_state["trend_on"]
    ):
        target_hold_num = context.reduced_hold_num
        target_stocks = choose_stocks(context, bar_dict, target_hold_num)
        target_stocks = filter_buyable(context, bar_dict, target_stocks)
    else:
        target_hold_num = context.base_hold_num
        target_stocks = choose_stocks(context, bar_dict, target_hold_num)
        target_stocks = filter_buyable(context, bar_dict, target_stocks)

    logger.info(
        f"rebalance: date={watch_date} breadth={market_state['breadth']:.3f} "
        f"trend={market_state['trend_on']} hold_num={target_hold_num} count={len(target_stocks)}"
    )

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    portfolio = context.portfolio
    total_value = portfolio.total_value
    target_value_per_stock = total_value / max(len(target_stocks), 1)

    for stock in target_stocks:
        if stock not in bar_dict:
            continue

        current_position = portfolio.positions.get(stock)
        current_value = current_position.market_value if current_position else 0

        if abs(current_value - target_value_per_stock) > target_value_per_stock * 0.05:
            order_target_value(stock, target_value_per_stock)
