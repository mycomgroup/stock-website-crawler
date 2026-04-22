"""
RFScore7 PB10% 增强选股版

核心优化：
1. 综合评分：质量分50% + 估值分30% + 成长分20%
2. 行业上限：单行业最多30%仓位
3. 尾盘调仓：14:50调仓，避免开盘波动
4. 买入过滤：涨停/跌停/低开/高开过滤

回测周期：2018-01-01 至今
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


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

    g.ipo_days = 180
    g.base_hold_num = 20
    g.reduced_hold_num = 10
    g.breadth_reduce = 0.25
    g.breadth_stop = 0.15
    g.primary_pb_group = 1
    g.reduced_pb_group = 2
    g.industry_cap_ratio = 0.30
    g.last_market_state = {}

    run_monthly(rebalance, 1, time="14:50", reference_security="000300.XSHG")
    run_daily(record_market_state, time="14:50", reference_security="000300.XSHG")


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

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "idx_close": idx_close,
        "idx_ma20": idx_ma20,
    }


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

    df["质量分"] = df["RFScore"] / 7 * 100
    df["估值分"] = (1 - df["pb_group"] / 10) * 100
    df["成长分"] = np.clip(df["DELTA_ROA"] * 100, -50, 50) + np.clip(
        df["DELTA_MARGIN"] * 100, -50, 50
    )
    df["综合分"] = df["质量分"] * 0.5 + df["估值分"] * 0.3 + df["成长分"] * 0.2

    return df


def get_industry_map(codes, watch_date):
    if not codes:
        return {}
    raw = get_industry(codes, date=watch_date)
    result = {}
    for code in codes:
        result[code] = (
            raw.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        )
    return result


def apply_industry_cap(picks, hold_num, industry_map):
    limit_count = max(1, int(np.floor(hold_num * g.industry_cap_ratio)))
    final_picks = []
    industry_counts = {}

    for code in picks:
        if len(final_picks) >= hold_num:
            break
        industry_name = industry_map.get(code, "Unknown")
        if industry_counts.get(industry_name, 0) < limit_count:
            final_picks.append(code)
            industry_counts[industry_name] = industry_counts.get(industry_name, 0) + 1

    return final_picks


def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))

    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.primary_pb_group)].copy()
    primary = primary.sort_values(["综合分", "pb_ratio"], ascending=[False, True])
    picks = primary.index.tolist()

    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= g.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["综合分", "pb_ratio"], ascending=[False, True]
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    if len(picks) < hold_num:
        fallback = df.sort_values(["综合分", "pb_ratio"], ascending=[False, True])
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    industry_map = get_industry_map(picks, watch_date)
    picks = apply_industry_cap(picks, hold_num, industry_map)

    return picks[:hold_num], df


def filter_buyable_enhanced(context, stocks):
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
        yesterday_close = current_data[stock].yesterday_close
        high_limit = current_data[stock].high_limit
        low_limit = current_data[stock].low_limit

        if last_price >= high_limit * 0.98:
            continue
        if last_price <= low_limit * 1.02:
            continue
        if last_price < yesterday_close * 0.97:
            continue
        if last_price > yesterday_close * 1.03:
            continue

        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date
    market_state = calc_market_state(watch_date)
    g.last_market_state = market_state

    if market_state["breadth"] < g.breadth_stop and (not market_state["trend_on"]):
        target_stocks = []
        target_hold_num = 0
    elif market_state["breadth"] < g.breadth_reduce and (not market_state["trend_on"]):
        target_hold_num = g.reduced_hold_num
        target_stocks, factor_table = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable_enhanced(context, target_stocks)
    else:
        target_hold_num = g.base_hold_num
        target_stocks, factor_table = choose_stocks(watch_date, target_hold_num)
        target_stocks = filter_buyable_enhanced(context, target_stocks)

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

    current_data = get_current_data()
    target_value = context.portfolio.total_value / float(max(len(target_stocks), 1))
    for stock in target_stocks:
        price = current_data[stock].last_price
        if price <= 0:
            continue
        target_amount = int(target_value / price / 100) * 100
        if target_amount < 100:
            continue
        order_target(stock, target_amount)


def record_market_state(context):
    watch_date = context.previous_date
    state = calc_market_state(watch_date)
    record(
        breadth=state["breadth"],
        hs300_close=state["idx_close"],
        hs300_ma20=state["idx_ma20"],
    )
