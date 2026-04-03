from mindgo_api import *
import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


def calc_rfscore_table(stocks, watch_date):
    date_str = (
        watch_date.strftime("%Y%m%d") if hasattr(watch_date, "strftime") else watch_date
    )

    q = query(
        valuation.symbol,
        profit.roa,
        profit.roa_4,
        cashflow.net_operate_cash_flow,
        cashflow.net_operate_cash_flow_1,
        cashflow.net_operate_cash_flow_2,
        cashflow.net_operate_cash_flow_3,
        balance.total_assets,
        balance.total_assets_1,
        balance.total_assets_2,
        balance.total_assets_3,
        balance.total_assets_4,
        balance.total_assets_5,
        balance.total_non_current_liability,
        balance.total_non_current_liability_1,
        profit.gross_profit_margin,
        profit.gross_profit_margin_4,
        income.operating_revenue,
        income.operating_revenue_4,
        valuation.pb_ratio,
        valuation.pe_ratio,
    ).filter(valuation.symbol.in_(stocks))

    df = get_fundamentals(q, date=date_str)
    df = df.drop_duplicates("valuation_symbol").set_index("valuation_symbol")

    roa = df["profit_roa"]
    delta_roa = roa / df["profit_roa_4"] - 1

    cfo_sum = (
        df["cashflow_net_operate_cash_flow"]
        + df["cashflow_net_operate_cash_flow_1"]
        + df["cashflow_net_operate_cash_flow_2"]
        + df["cashflow_net_operate_cash_flow_3"]
    )
    ta_ttm = (
        df["balance_total_assets"]
        + df["balance_total_assets_1"]
        + df["balance_total_assets_2"]
        + df["balance_total_assets_3"]
    ) / 4
    ocfoa = cfo_sum / ta_ttm
    accrual = ocfoa - roa * 0.01

    leveler = df["balance_total_non_current_liability"] / df["balance_total_assets"]
    leveler1 = (
        df["balance_total_non_current_liability_1"] / df["balance_total_assets_1"]
    )
    delta_leveler = -(leveler / leveler1 - 1)

    delta_margin = (
        df["profit_gross_profit_margin"] / df["profit_gross_profit_margin_4"] - 1
    )

    turnover = (
        df["income_operating_revenue"]
        / (df["balance_total_assets"] + df["balance_total_assets_1"]).mean()
    )
    turnover_1 = (
        df["income_operating_revenue_4"]
        / (df["balance_total_assets_4"] + df["balance_total_assets_5"]).mean()
    )
    delta_turn = turnover / turnover_1 - 1

    result = pd.DataFrame(
        {
            "ROA": roa,
            "DELTA_ROA": delta_roa,
            "OCFOA": ocfoa,
            "ACCRUAL": accrual,
            "DELTA_LEVELER": delta_leveler,
            "DELTA_MARGIN": delta_margin,
            "DELTA_TURN": delta_turn,
            "pb_ratio": df["valuation_pb_ratio"],
            "pe_ratio": df["valuation_pe_ratio"],
        }
    )

    result = result.replace([-np.inf, np.inf], np.nan)
    result["RFScore"] = result[
        [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
    ].apply(lambda x: sign(x).sum(axis=1), axis=1)
    result = result.dropna(subset=["RFScore", "pb_ratio"])
    result["pb_group"] = (
        pd.qcut(
            result["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
        )
        + 1
    )

    return result


def get_universe(watch_date):
    date_str = (
        watch_date.strftime("%Y-%m-%d")
        if hasattr(watch_date, "strftime")
        else watch_date
    )

    hs300 = set(get_index_stocks("000300.SH", date=date_str))
    zz500 = set(get_index_stocks("000905.SH", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [stock for stock in stocks if not stock.startswith("688")]

    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)]
    stocks = sec.index.tolist()

    try:
        bar_dict = get_current(stocks)
        stocks = [s for s in stocks if s in bar_dict and not bar_dict[s].is_st]
    except:
        pass

    return stocks


def calc_market_state(watch_date):
    return {"breadth": 0.5, "trend_on": True, "idx_close": 1, "idx_ma20": 1}


def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, watch_date)

    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.primary_pb_group)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()

    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= g.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    if len(picks) < hold_num:
        fallback = df.sort_values(
            ["RFScore", "ROA", "OCFOA", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num], df


def filter_buyable(context, stocks):
    bar_dict = get_current(stocks)
    buyable = []
    for stock in stocks:
        if stock not in bar_dict:
            continue
        cd = bar_dict[stock]
        if cd.is_paused:
            continue
        if cd.is_st:
            continue
        if "ST" in cd.name or "*" in cd.name or "退" in cd.name:
            continue
        if cd.close >= cd.high_limit * 0.995:
            continue
        if cd.close <= cd.low_limit * 1.005:
            continue
        buyable.append(stock)
    return buyable


def get_prev_trade_date():
    days = get_trade_days(end_date=get_last_datetime().strftime("%Y%m%d"), count=5)
    return days[-2]


def rebalance(context, bar_dict):
    watch_date = get_prev_trade_date()
    market_state = calc_market_state(watch_date)
    g.last_market_state = market_state

    if market_state["breadth"] < g.breadth_stop:
        target_stocks = []
        target_hold_num = g.hold_num_stop
    elif market_state["breadth"] < g.breadth_reduce:
        target_hold_num = g.hold_num_weak
        target_stocks, factor_table = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)
    elif market_state["breadth"] < g.breadth_normal and (not market_state["trend_on"]):
        target_hold_num = g.hold_num_mid
        target_stocks, factor_table = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)
    else:
        target_hold_num = g.hold_num_normal
        target_stocks, factor_table = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable(context, target_stocks)

    log.info(
        "rebalance watch_date=%s breadth=%.3f trend_on=%s target_hold_num=%s target_count=%s"
        % (
            str(watch_date),
            market_state["breadth"],
            str(market_state["trend_on"]),
            str(target_hold_num),
            str(len(target_stocks)),
        )
    )

    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    target_value = context.portfolio.total_value / float(max(len(target_stocks), 1))
    bar_dict = get_current(target_stocks)
    for stock in target_stocks:
        if stock not in bar_dict:
            continue
        price = bar_dict[stock].close
        if price <= 0:
            continue
        target_amount = int(target_value / price / 100) * 100
        if target_amount < 100:
            continue
        order_target(stock, target_amount)


def init(context):
    set_benchmark("000300.SH")

    set_commission(PerShare(type="stock", cost=0.0003, min_trade_cost=5))
    set_slippage(PriceSlippage(0.001))

    g.ipo_days = 180
    g.hold_num_normal = 10
    g.hold_num_mid = 8
    g.hold_num_weak = 6
    g.hold_num_stop = 0
    g.breadth_normal = 0.35
    g.breadth_reduce = 0.25
    g.breadth_stop = 0.15
    g.primary_pb_group = 1
    g.reduced_pb_group = 2
    g.last_market_state = {}

    run_weekly(rebalance, 1)


def handle_bar(context, bar_dict):
    pass


def after_trading(context):
    pass
