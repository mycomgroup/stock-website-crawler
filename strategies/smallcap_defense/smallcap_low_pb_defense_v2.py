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

    g.hold_num_full = 10
    g.hold_num_mid = 7
    g.hold_num_weak = 5
    g.hold_num_extreme = 3
    g.min_cap = 15
    g.max_cap = 60
    g.ipo_days = 180
    g.max_pb = 1.5
    g.max_pe = 20

    g.breadth_threshold_full = 0.40
    g.breadth_threshold_mid = 0.25
    g.breadth_threshold_weak = 0.15

    g.trade_records = []
    g.position_records = []
    g.current_hold_num = g.hold_num_full

    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")
    run_daily(record_position, time="14:50", reference_security="000852.XSHG")


def calc_market_breadth(watch_date):
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)

    above_ma20 = 0
    total = 0

    for stock in hs300:
        try:
            prices = get_price(
                stock,
                end_date=watch_date,
                count=20,
                fields=["close"],
                panel=False,
                fill_paused=False,
            )
            if len(prices) >= 20:
                ma20 = prices["close"].mean()
                last_close = prices["close"].iloc[-1]
                if last_close >= ma20:
                    above_ma20 += 1
                total += 1
        except:
            continue

    breadth = above_ma20 / max(total, 1)
    return breadth


def get_target_hold_num(breadth):
    if breadth >= g.breadth_threshold_full:
        return g.hold_num_full
    elif breadth >= g.breadth_threshold_mid:
        return g.hold_num_mid
    elif breadth >= g.breadth_threshold_weak:
        return g.hold_num_weak
    else:
        return g.hold_num_extreme


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

    breadth = calc_market_breadth(watch_date)
    target_hold_num = get_target_hold_num(breadth)

    stocks = select_stocks(watch_date, target_hold_num)
    stocks = filter_buyable(context, stocks)

    if len(stocks) == 0:
        log.info("No candidates available")
        current_positions = list(context.portfolio.positions.keys())
        for stock in current_positions:
            order_target_value(stock, 0)
        g.current_hold_num = 0
        return

    actual_hold_num = min(len(stocks), target_hold_num)
    stocks = stocks[:actual_hold_num]

    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(stocks)

    current_positions = list(context.portfolio.positions.keys())

    trades_count = 0

    for stock in current_positions:
        if stock not in stocks:
            order_target_value(stock, 0)
            trades_count += 1

    for stock in stocks:
        if stock not in current_positions:
            order_target_value(stock, target_value_per_stock)
            trades_count += 1
        else:
            current_value = context.portfolio.positions[stock].value
            if (
                abs(current_value - target_value_per_stock)
                > target_value_per_stock * 0.05
            ):
                order_target_value(stock, target_value_per_stock)
                trades_count += 1

    g.current_hold_num = len(stocks)

    g.trade_records.append(
        {
            "date": watch_date.strftime("%Y-%m-%d"),
            "breadth": breadth,
            "target_hold_num": target_hold_num,
            "actual_hold_num": len(stocks),
            "trades_count": trades_count,
            "portfolio_value": total_value,
        }
    )

    log.info(
        f"Low PB SmallCap Defense v2: breadth={breadth:.1%}, target={target_hold_num}, actual={len(stocks)}, trades={trades_count}"
    )


def record_position(context):
    date = context.current_dt.strftime("%Y-%m-%d")

    portfolio_value = context.portfolio.total_value
    positions_count = len(context.portfolio.positions)

    g.position_records.append(
        {
            "date": date,
            "portfolio_value": portfolio_value,
            "positions_count": positions_count,
            "target_hold_num": g.current_hold_num,
        }
    )


def after_trading_end(context):
    pass
