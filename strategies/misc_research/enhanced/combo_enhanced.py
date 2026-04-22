"""
组合策略增强版 - RFScore + 红利小盘

集成：
- 情绪开关（result_06实测有效）
- 四档仓位（基于result_05）
- 风控模块（时间止损+组合熔断，基于result_08）

增强点：
- 情绪动态权重调整
- 四档仓位规则
- 组合熔断保护
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import datetime as dt

from common_modules import SentimentSwitch, FourTierPosition, RiskControl


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


g = type("Global", (), {})()


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

    g.rfscore_base_weight = 0.60
    g.dividend_base_weight = 0.40
    g.use_dynamic_weight = True

    g.rfscore_hold_num = 12
    g.rfscore_pb_group = 1

    g.dividend_hold_num = 8
    g.dividend_min_cap = 10
    g.dividend_max_cap = 100
    g.dividend_max_pe = 30

    g.ipo_days = 180

    g.sentiment = SentimentSwitch()
    g.position_rule = FourTierPosition(base_hold=20)
    g.risk_control = RiskControl()

    run_daily(update_sentiment, "9:10")
    run_daily(check_risk_status, "9:15")
    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(time_stop_execute, "10:30")
    run_daily(record_state, "14:50")


def update_sentiment(context):
    date = context.previous_date
    g.sentiment.update(date)

    record(
        sentiment_score=g.sentiment.sentiment_score,
        sentiment_state=g.sentiment.sentiment_state,
        hl_count=g.sentiment.hl_count,
        max_lianban=g.sentiment.max_lianban,
    )


def check_risk_status(context):
    g.risk_control.init_period(context)
    g.risk_control.check_week_loss(context)
    g.risk_control.check_month_loss(context)

    in_rest = g.risk_control.is_in_rest(context)
    record(in_rest_mode=in_rest)


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

    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.rfscore_pb_group)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "pb_ratio"], ascending=[False, False, False, True]
    )
    picks = primary.index.tolist()

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


def select_dividend_stocks(watch_date, hold_num):
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

    if g.risk_control.is_in_rest(context):
        log.info("强制休息期，清仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    target_hold_num, breadth, trend_on = g.position_rule.get_target_hold_num(watch_date)
    sentiment_ratio = g.sentiment.get_position_ratio()

    if g.use_dynamic_weight:
        if g.sentiment.sentiment_state >= 3:
            g.rfscore_weight = g.rfscore_base_weight * 1.2
            g.dividend_weight = g.dividend_base_weight * 0.8
        elif g.sentiment.sentiment_state <= 1:
            g.rfscore_weight = g.rfscore_base_weight * 0.5
            g.dividend_weight = g.dividend_base_weight * 1.5
        else:
            g.rfscore_weight = g.rfscore_base_weight
            g.dividend_weight = g.dividend_base_weight

        g.rfscore_weight = min(g.rfscore_weight, 0.8)
        g.dividend_weight = min(g.dividend_weight, 0.8)

        total = g.rfscore_weight + g.dividend_weight
        if total > 1.0:
            g.rfscore_weight = g.rfscore_weight / total
            g.dividend_weight = g.dividend_weight / total
    else:
        g.rfscore_weight = g.rfscore_base_weight
        g.dividend_weight = g.dividend_base_weight

    adjusted_rfscore_hold = int(g.rfscore_hold_num * sentiment_ratio)
    adjusted_dividend_hold = int(g.dividend_hold_num * sentiment_ratio)

    log.info(
        f"rebalance: sentiment_state={g.sentiment.sentiment_state}, "
        f"rfscore_weight={g.rfscore_weight:.2f}, dividend_weight={g.dividend_weight:.2f}, "
        f"breadth={breadth:.3f}"
    )

    record(
        breadth=breadth,
        rfscore_weight=g.rfscore_weight,
        dividend_weight=g.dividend_weight,
    )

    if sentiment_ratio <= 0:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    rfscore_stocks = select_rfscore_stocks(watch_date, adjusted_rfscore_hold)
    dividend_stocks = select_dividend_stocks(watch_date, adjusted_dividend_hold)

    rfscore_stocks = filter_buyable(context, rfscore_stocks)
    dividend_stocks = filter_buyable(context, dividend_stocks)

    target_stocks = {}
    total_value = context.portfolio.total_value

    if rfscore_stocks and g.rfscore_weight > 0:
        per_stock_value = total_value * g.rfscore_weight / len(rfscore_stocks)
        for s in rfscore_stocks:
            target_stocks[s] = target_stocks.get(s, 0) + per_stock_value

    if dividend_stocks and g.dividend_weight > 0:
        per_stock_value = total_value * g.dividend_weight / len(dividend_stocks)
        for s in dividend_stocks:
            target_stocks[s] = target_stocks.get(s, 0) + per_stock_value

    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)

    for stock, target_val in target_stocks.items():
        order_target_value(stock, target_val)

    log.info(
        f"Holdings: RFScore={len(rfscore_stocks)}, Dividend={len(dividend_stocks)}"
    )


def time_stop_execute(context):
    current_time = context.current_dt
    hold_list = list(context.portfolio.positions)

    for stock in hold_list:
        if g.risk_control.time_stop_check(context, stock, current_time):
            order_target_value(stock, 0)
        if g.risk_control.gap_stop_check(context, stock):
            order_target_value(stock, 0)


def record_state(context):
    position_pct = (
        100 * context.portfolio.positions_value / max(context.portfolio.total_value, 1)
    )
    ret_pct = 100 * (
        context.portfolio.total_value / context.portfolio.starting_cash - 1
    )

    record(
        position_pct=position_pct,
        total_return=ret_pct,
    )
