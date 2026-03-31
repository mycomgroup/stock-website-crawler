from jqdata import *
import pandas as pd


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

    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")


def rebalance(context):
    watch_date = context.previous_date

    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=180)
    ]
    stocks = all_stocks.index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = (
        query(valuation.code, valuation.market_cap)
        .filter(
            valuation.code.in_(stocks),
            valuation.market_cap >= g.min_cap,
            valuation.market_cap <= g.max_cap,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 50,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return

    stocks = df["code"].tolist()[: g.hold_num]

    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        buyable.append(stock)

    if len(buyable) == 0:
        return

    total_value = context.portfolio.total_value
    target_value = total_value / len(buyable)

    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in buyable:
            order_target_value(stock, 0)

    for stock in buyable:
        order_target_value(stock, target_value)
