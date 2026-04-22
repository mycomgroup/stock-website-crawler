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
    g.max_pb = 1.5
    g.max_pe = 20
    g.zt_count = 50

    run_daily(get_sentiment, time="9:30")
    run_monthly(rebalance, 1, time="9:35")


def get_sentiment(context):
    prev_date = context.previous_date

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    try:
        df = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        if not df.empty:
            df = df.dropna()
            g.zt_count = len(df[df["close"] == df["high_limit"]])
        else:
            g.zt_count = 0
    except:
        g.zt_count = 0


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
        valuation.pe_ratio < g.max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < g.max_pb,
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

    if g.zt_count < 30:
        log.info(f"涨停数{g.zt_count}<30, 完全停手")
        return

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

    log.info(f"涨停数{g.zt_count}>=30, 正常交易: {len(stocks)} stocks")
