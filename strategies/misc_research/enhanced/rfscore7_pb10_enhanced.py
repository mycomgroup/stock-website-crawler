"""
RFScore PB10 增强版策略

集成：
- 情绪开关（result_06实测有效）
- 四档仓位（15/12/10/0，基于result_05）
- 风控模块（时间止损+组合熔断，基于result_08）

与原始版本对比：
- 原版：月度调仓，两档仓位（20/10/0）
- 增强版：情绪动态仓位，四档仓位，时间止损
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

    g.ipo_days = 180
    g.primary_pb_group = 1
    g.reduced_pb_group = 2

    g.sentiment = SentimentSwitch()
    g.position_rule = FourTierPosition(base_hold=15)
    g.risk_control = RiskControl()

    g.last_sentiment_state = 2
    g.last_breadth = 0.5

    run_daily(update_sentiment, "9:10")
    run_daily(check_risk_status, "9:15")
    run_monthly(rebalance, 1, time="9:35", reference_security="000300.XSHG")
    run_daily(time_stop_execute, "10:30")
    run_daily(stop_profit_execute, "13:30")
    run_daily(tail_sell, "14:50")
    run_daily(record_state, "15:00")


def update_sentiment(context):
    date = context.previous_date
    g.sentiment.update(date)
    g.last_sentiment_state = g.sentiment.sentiment_state

    record(
        sentiment_score=g.sentiment.sentiment_score,
        sentiment_state=g.sentiment.sentiment_state,
        hl_count=g.sentiment.hl_count,
        max_lianban=g.sentiment.max_lianban,
    )


def check_risk_status(context):
    g.risk_control.init_period(context)

    week_triggered = g.risk_control.check_week_loss(context)
    month_triggered = g.risk_control.check_month_loss(context)

    in_rest = g.risk_control.is_in_rest(context)

    record(
        in_rest_mode=in_rest,
        week_loss_triggered=week_triggered,
        month_loss_triggered=month_triggered,
    )


def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [stock for stock in stocks if not stock.startswith("688")]

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


def calc_rfscore_table(stocks, watch_date):
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
            df["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
        )
        + 1
    )

    return df


def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    if len(stocks) < 10:
        return [], pd.DataFrame()

    df = calc_rfscore_table(stocks, str(watch_date))

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

    return picks[:hold_num], df


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if current_data[stock].paused:
            continue
        if current_data[stock].is_st:
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
    g.last_breadth = breadth

    sentiment_ratio = g.sentiment.get_position_ratio()
    adjusted_hold_num = int(target_hold_num * sentiment_ratio)

    log.info(
        f"rebalance: breadth={breadth:.3f}, trend={trend_on}, "
        f"sentiment_state={g.sentiment.sentiment_state}, "
        f"base_hold={target_hold_num}, adjusted_hold={adjusted_hold_num}"
    )

    record(
        breadth=breadth,
        trend_on=trend_on,
        target_hold_num=target_hold_num,
        adjusted_hold_num=adjusted_hold_num,
    )

    if adjusted_hold_num <= 0:
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    target_stocks, factor_table = choose_stocks(watch_date, adjusted_hold_num)
    target_stocks = filter_buyable(context, target_stocks)

    if len(target_stocks) < adjusted_hold_num:
        adjusted_hold_num = len(target_stocks)

    current_positions = list(context.portfolio.positions.keys())
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if not target_stocks:
        return

    current_data = get_current_data()
    total_value = context.portfolio.total_value * sentiment_ratio
    target_value = total_value / float(max(len(target_stocks), 1))

    for stock in target_stocks:
        price = current_data[stock].last_price
        if price <= 0:
            continue
        target_amount = int(target_value / price / 100) * 100
        if target_amount < 100:
            continue
        order_target(stock, target_amount)


def time_stop_execute(context):
    current_time = context.current_dt

    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for stock in hold_list:
        if g.risk_control.time_stop_check(context, stock, current_time):
            order_target_value(stock, 0)
            log.info(f"时间止损: {stock}")

        if g.risk_control.gap_stop_check(context, stock):
            order_target_value(stock, 0)
            log.info(f"跳空止损: {stock}")


def stop_profit_execute(context):
    current_time = context.current_dt

    hold_list = list(context.portfolio.positions)

    for stock in hold_list:
        if g.risk_control.stop_profit_check(context, stock, current_time):
            order_target_value(stock, 0)
            log.info(f"止盈检查: {stock}")


def tail_sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for stock in hold_list:
        position = context.portfolio.positions[stock]
        if position.closeable_amount == 0:
            continue

        if current_data[stock].last_price == current_data[stock].high_limit:
            continue

        cost = position.avg_cost
        price = current_data[stock].last_price

        if price > cost:
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
