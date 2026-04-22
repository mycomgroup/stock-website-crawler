from jqdata import *
import pandas as pd
import numpy as np

DEFENSE_WEIGHT = 0.6
OFFENSE_WEIGHT = 0.4
DEFENSE_HOLD_NUM = 10
OFFENSE_HOLD_NUM = 5
MIN_CAP_DEFENSE = 15
MAX_CAP_DEFENSE = 60
MIN_CAP_OFFENSE = 50
MAX_CAP_OFFENSE = 150


def initialize(context):
    set_benchmark("000852.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.defense_weight = DEFENSE_WEIGHT
    g.offense_weight = OFFENSE_WEIGHT
    g.defense_hold_num = DEFENSE_HOLD_NUM
    g.offense_hold_num = OFFENSE_HOLD_NUM

    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")


def get_defense_universe(watch_date):
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=180)
    ]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= MIN_CAP_DEFENSE,
        valuation.market_cap <= MAX_CAP_DEFENSE,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_defense_stocks(watch_date, hold_num):
    stocks = get_defense_universe(watch_date)
    if len(stocks) < 5:
        return []

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 20,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 1.5,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return []

    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[:hold_num]


def select_offense_stocks(watch_date):
    prev_date = watch_date - pd.Timedelta(days=1)

    q = query(
        valuation.code,
        valuation.circulating_market_cap,
    ).filter(
        valuation.circulating_market_cap >= MIN_CAP_OFFENSE,
        valuation.circulating_market_cap <= MAX_CAP_OFFENSE,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    candidates = []

    for code in df["code"].tolist()[:100]:
        try:
            prev_data = get_price(
                code,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if prev_data.empty:
                continue

            prev_close = float(prev_data["close"].iloc[0])
            prev_high_limit = float(prev_data["high_limit"].iloc[0])

            if abs(prev_close - prev_high_limit) / prev_high_limit > 0.01:
                continue

            curr_data = get_price(
                code,
                end_date=watch_date,
                count=1,
                fields=["open", "close"],
                panel=False,
            )
            if curr_data.empty:
                continue

            curr_open = float(curr_data["open"].iloc[0])
            open_pct = (curr_open - prev_close) / prev_close * 100

            if not (0.5 <= open_pct <= 1.5):
                continue

            prices = get_price(
                code, end_date=watch_date, count=15, fields=["close"], panel=False
            )
            if prices.empty:
                continue

            high_15d = float(prices["close"].max())
            low_15d = float(prices["close"].min())
            position = (prices["close"].iloc[-1] - low_15d) / (high_15d - low_15d)

            if position > 0.30:
                continue

            candidates.append(code)

        except Exception as e:
            continue

    return candidates[: g.offense_hold_num]


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if "ST" in current_data[stock].name or "*" in current_data[stock].name:
            continue
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date

    defense_stocks = select_defense_stocks(watch_date, g.defense_hold_num)
    defense_stocks = filter_buyable(context, defense_stocks)

    offense_stocks = select_offense_stocks(watch_date)
    offense_stocks = filter_buyable(context, offense_stocks)

    all_stocks = defense_stocks + offense_stocks

    if len(all_stocks) == 0:
        log.info("No candidates available")
        return

    total_value = context.portfolio.total_value

    defense_value = total_value * g.defense_weight
    offense_value = total_value * g.offense_weight

    if len(defense_stocks) > 0:
        defense_value_per_stock = defense_value / len(defense_stocks)
        for stock in defense_stocks:
            order_target_value(stock, defense_value_per_stock)

    if len(offense_stocks) > 0:
        offense_value_per_stock = offense_value / len(offense_stocks)
        for stock in offense_stocks:
            order_target_value(stock, offense_value_per_stock)

    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in all_stocks:
            order_target_value(stock, 0)

    log.info(
        f"Defense-Offense Combo: {len(defense_stocks)} defense + {len(offense_stocks)} offense"
    )
