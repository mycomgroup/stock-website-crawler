from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import datetime


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


def initialize(context):
    set_benchmark("000300.XSHG")
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

    # 组合配置参数
    g.rfscore_weight = 0.70  # RFScore权重 (70/30配置 - 进攻偏置)
    g.dividend_weight = 0.30  # 红利小盘权重
    g.use_dynamic_weight = False  # 是否使用动态权重

    # RFScore参数
    g.rfscore_hold_num = 15
    g.rfscore_pb_group = 1

    # 红利小盘参数
    g.dividend_hold_num = 10
    g.dividend_min_cap = 10
    g.dividend_max_cap = 100
    g.dividend_max_pe = 30

    # 风控参数
    g.breadth_reduce = 0.25
    g.breadth_stop = 0.15
    g.ipo_days = 180

    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(record_market_state, time="14:50", reference_security="000300.XSHG")


def calc_market_state(watch_date):
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)
    prices = get_price(
        hs300, end_date=watch_date, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
    idx_close = float(idx["close"].iloc[-1])
    idx_ma20 = float(idx["close"].mean())
    trend_on = idx_close > idx_ma20

    return {"breadth": breadth, "trend_on": trend_on}


def get_rfscore_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def select_rfscore_stocks(watch_date, hold_num):
    stocks = get_rfscore_universe(watch_date)
    if len(stocks) < 10:
        return []

    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # 选择RFScore=7且PB最低的
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.rfscore_pb_group)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "pb_ratio"], ascending=[False, False, False, True]
    )
    picks = primary.index.tolist()

    # 如果不够,补充RFScore>=6的
    if len(picks) < hold_num:
        secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "pb_ratio"], ascending=[False, False, True]
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num]


def select_dividend_smallcap_stocks(watch_date, hold_num):
    # 全市场小盘股筛选
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    # 过滤ST和停牌
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    # 排除科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 基本面筛选
    q = (
        query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.inc_net_profit_year_on_year,
            indicator.roe,
        )
        .filter(
            valuation.code.in_(stocks),
            valuation.market_cap >= g.dividend_min_cap,
            valuation.market_cap <= g.dividend_max_cap,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < g.dividend_max_pe,
            indicator.inc_net_profit_year_on_year > 5,
            indicator.roe > 5,
        )
        .order_by(valuation.pe_ratio.asc())
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    # 按PE排序选择
    df = df.sort_values("pe_ratio")
    return df["code"].tolist()[:hold_num]


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if (
            "ST" in current_data[stock].name
            or "*" in current_data[stock].name
            or "退" in current_data[stock].name
        ):
            continue
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        if last_price <= current_data[stock].low_limit * 1.005:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date
    market_state = calc_market_state(watch_date)

    # 动态权重调整
    if g.use_dynamic_weight:
        if market_state["breadth"] < g.breadth_stop and not market_state["trend_on"]:
            g.rfscore_weight = 0.0
            g.dividend_weight = 1.0
        elif (
            market_state["breadth"] < g.breadth_reduce and not market_state["trend_on"]
        ):
            g.rfscore_weight = 0.4
            g.dividend_weight = 0.6
        elif market_state["trend_on"]:
            g.rfscore_weight = 0.7
            g.dividend_weight = 0.3
        else:
            g.rfscore_weight = 0.6
            g.dividend_weight = 0.4

    log.info(
        f"Rebalance: breadth={market_state['breadth']:.3f}, trend_on={market_state['trend_on']}, "
        + f"RFScore_weight={g.rfscore_weight}, Dividend_weight={g.dividend_weight}"
    )

    # 选股
    rfscore_stocks = select_rfscore_stocks(watch_date, g.rfscore_hold_num)
    dividend_stocks = select_dividend_smallcap_stocks(watch_date, g.dividend_hold_num)

    rfscore_stocks = filter_buyable(context, rfscore_stocks)
    dividend_stocks = filter_buyable(context, dividend_stocks)

    # 构建目标持仓
    target_stocks = {}
    total_value = context.portfolio.total_value

    if rfscore_stocks and g.rfscore_weight > 0:
        rfscore_value = total_value * g.rfscore_weight / len(rfscore_stocks)
        for s in rfscore_stocks:
            target_stocks[s] = target_stocks.get(s, 0) + rfscore_value

    if dividend_stocks and g.dividend_weight > 0:
        dividend_value = total_value * g.dividend_weight / len(dividend_stocks)
        for s in dividend_stocks:
            target_stocks[s] = target_stocks.get(s, 0) + dividend_value

    # 调仓
    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    for stock, target_val in target_stocks.items():
        order_target_value(stock, target_val)

    log.info(
        f"Holdings: RFScore={len(rfscore_stocks)}, Dividend={len(dividend_stocks)}, Total={len(target_stocks)}"
    )


def record_market_state(context):
    watch_date = context.previous_date
    state = calc_market_state(watch_date)
    record(breadth=state["breadth"])
