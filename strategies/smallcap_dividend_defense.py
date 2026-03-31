from jqdata import *
import pandas as pd
import numpy as np


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

    g.hold_num = 15
    g.min_cap = 15
    g.max_cap = 60
    g.ipo_days = 180
    g.min_dividend_yield = 2.0

    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")


def get_smallcap_universe(watch_date):
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
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
        valuation.market_cap >= g.min_cap,
        valuation.market_cap <= g.max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def check_dividend_stability(code, watch_date):
    try:
        years = 3
        end_date = watch_date
        start_date = end_date - pd.Timedelta(days=365 * years)

        q = query(
            finance.STK_DIVIDEND_INFO.code,
            finance.STK_DIVIDEND_INFO.pub_date,
            finance.STK_DIVIDEND_INFO.dividend_ratio,
        ).filter(
            finance.STK_DIVIDEND_INFO.code == code,
            finance.STK_DIVIDEND_INFO.pub_date >= start_date,
            finance.STK_DIVIDEND_INFO.pub_date <= end_date,
            finance.STK_DIVIDEND_INFO.dividend_ratio > 0,
        )

        df = finance.run_query(q)

        if len(df) >= years:
            return True
        return False
    except:
        return False


def select_stocks(watch_date, hold_num):
    stocks = get_smallcap_universe(watch_date)
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
        valuation.pe_ratio < 100,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df = df.drop_duplicates("code")

    dividend_data = {}
    for code in df["code"].tolist()[:50]:
        dividend_data[code] = check_dividend_stability(code, watch_date)

    df["dividend_stable"] = df["code"].map(dividend_data)

    df = df[df["dividend_stable"] == True]

    if len(df) == 0:
        return []

    try:
        q2 = query(
            valuation.code, valuation.market_cap, indicator.dividend_yield_ratio
        ).filter(valuation.code.in_(df["code"].tolist()))

        df2 = get_fundamentals(q2, date=watch_date)
        df2 = df2.drop_duplicates("code")

        df = df.merge(df2[["code", "dividend_yield_ratio"]], on="code", how="left")
        df = df[df["dividend_yield_ratio"] >= g.min_dividend_yield]

        if len(df) == 0:
            return []

        df = df.sort_values("dividend_yield_ratio", ascending=False)

        return df["code"].tolist()[:hold_num]
    except:
        df = df.sort_values(["roe", "pe_ratio"], ascending=[False, True])
        return df["code"].tolist()[:hold_num]


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

    stocks = select_stocks(watch_date, g.hold_num)
    stocks = filter_buyable(context, stocks)

    if len(stocks) == 0:
        log.info("No candidates available")
        return

    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(stocks)

    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in stocks:
            order_target_value(stock, 0)

    for stock in stocks:
        order_target_value(stock, target_value_per_stock)

    log.info(f"Dividend SmallCap Defense: {len(stocks)} stocks")
